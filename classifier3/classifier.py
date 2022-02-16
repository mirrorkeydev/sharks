# =============================================== #
#
# classify all objects in video, export labels
# input:  video, pretrained serialized model
# output: frame labels as csv
# 
# pyinstaller -F --noconsole classifier.py
#
# need to do:
# model + icon image should be bundled
#
# =============================================== #

from csv     import writer
from math    import floor
from pickle  import load
from imageio import *
from numpy                import copy, full
from skimage              import data, filters, util, color, morphology, measure, transform
from skimage.measure      import label, regionprops
from skimage.transform    import rescale
from skimage.segmentation import flood_fill
from skimage.util         import crop
from sklearn.ensemble     import RandomForestClassifier
from sklearn.neighbors    import _partition_nodes

# parameters
model_file  = "./trained_model.json"
output_file = "output.csv"

upsidedown  = True  # does the footage need to be flipped 180 degrees?
frame_step  = 6     # only looks at every nth frame
scale       = 0.5   # image scale multiplier
border_size = 25    # number of pixels

def main(root, progress_bar, video_file):

##### FILES & THINGS & WHATEVER ##########################################################

    # load the model (this sucks, model needs to be bundled with .exe)
    try:
        rf = load(open(model_file, "rb"))
    except:
        print("Error: Cannot find/load model, probably because the file", model_file, "does not exist. Try running build_classifier.py.")
        quit()

    # load the output file
    try:
        csv = open(output_file, 'w', newline="")
        csv_writer = writer(csv) 
        csv_writer.writerow(["Time", "Frame", "Number of not-fish", "Number of fish"])
        time = 0
    except:
        print("Error: Cannot open", output_file, ".")
        quit()

    # video time
    print("Reading 1 in every", frame_step, "frames, predicting labels for all found objects, and exporting them as a gif.\nMight take a minute.\n")

    # read video
    video = get_reader(video_file, 'ffmpeg')
    num_frames = video.count_frames() # can take a few seconds on larger videos, but nice to know how long it will take
    fps        = video.get_meta_data()['fps']

    progress_bar['maximum'] = num_frames
    progress_bar['value'] = 0
    root.update_idletasks()

    # each every i frames
    for frame, image in enumerate(video):

        progress_bar['value'] = frame
        root.update()

        if frame % frame_step == 0:

##### IMAGE PROCESSING ###################################################################

            # resize and convert image to grayscale
            if (upsidedown): image = transform.rotate(image, 180)
            rescaled  = rescale(image, scale, anti_aliasing=False, multichannel=True)
            grayscale = color.rgb2gray(rescaled)

            # local thresholding
            threshold = filters.threshold_local(grayscale, 255 * scale, offset=0.005)
            binary    = grayscale > threshold
            binary    = util.invert(binary)

            border_size = 25

            x_min = border_size; x_max = binary.shape[1]
            y_min = border_size; y_max = binary.shape[0]

            cropped = copy(binary.astype(int)*255)

            # remove horizontal borders
            for x in range(0, x_max):
                for y in list(range(0, y_min)) + list(range(y_max - border_size, y_max)):
                    cropped[y][x] = 0

            # remove vertical borders
            for y in range(0, y_max):
                for x in list(range(0, x_min)) + list(range(x_max - border_size, x_max)):
                    cropped[y][x] = 0

            # remove small objects (faster than area_opening as it works on binary images)
            area = 512 * scale # lower gives more false positives
            small_removed = morphology.remove_small_objects(cropped.astype(bool), min_size=area, connectivity=1)

            dilated = morphology.binary_erosion(small_removed, selem=full((3,3), 1))
            final   = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

##### CLASSIFIER TIME ####################################################################

            # label objects in image
            labels, num_blobs = label(final, return_num=True)

            # 
            not_fish_count, fish_count = 0, 0

            # get properties of each object
            regions = regionprops(labels, rescaled)
            for blob_num, props in enumerate(regions):

                # get position and box dimentions
                y, x           = props.centroid
                y0, x0, y1, x1 = props.bbox
                w, h = x1 - x0, y1 - y0

                # build features list
                features = [
                    x, y, # coordinate location in image
                    w, h, # height, width of blob
                    props.bbox_area, # bounding box area
                    props.euler_number, # number of connected components subtracted by number of holes
                    props.extent, # ratio of pixels in the region to pixels in the total bounding box
                    props.orientation, # angle between the 0th axis (rows) and the major axis of the ellipse 
                    props.perimeter, # perimeter of object
                    props.area, # number of pixels of the region.
                    # value with the max intensity in the region (RGB 0-1)
                    props.max_intensity[0], props.max_intensity[1], props.max_intensity[2],
                    # value with the mean intensity in the region (RGB 0-1)
                    props.mean_intensity[0], props.mean_intensity[1], props.mean_intensity[2],
                    # value with the min intensity in the region (RGB 0-1)
                    props.min_intensity[0], props.min_intensity[1], props.min_intensity[2],
                    props.solidity, # ratio of pixels in the region to pixels of the convex hull image.
                ]

                # test model with features
                confidence = int(rf.predict_proba([features])[0][1] * 100)
                if rf.predict([features])[0] == 1:
                    fish_count += 1
                else:
                    not_fish_count += 1

##### OUTPUT RESULTS #####################################################################

            # create and write row to output
            row = [str(round(time, 1)), str(frame), str(not_fish_count), str(fish_count)]
            csv_writer.writerow(row)

            # update timestamp
            time += (frame_step / floor(fps + 0.5))
