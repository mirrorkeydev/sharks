# =============================================== #
#
# classify all objects in video, export labeled frames as gif
# input:  video, pretrained serialized model
# output: gif
#
# =============================================== #

import os
import math
import time
import pickle
import imageio
import numpy as np
from skimage              import data, filters, util, color, morphology, measure, transform
from skimage.measure      import label, regionprops
from skimage.transform    import rescale
from skimage.segmentation import flood_fill
from skimage.util         import crop
from sklearn.ensemble     import RandomForestClassifier

import matplotlib
from matplotlib           import pyplot, patches

# not sure what this does, but it prevents pyplot from crashing after 368 figures created
#matplotlib.use("agg")

# parameters
video_file  = "../videos/yellow tail.mp4"
model_file  = "./trained_model.json"

upsidedown  = True  # does the footage need to be flipped 180 degrees?
frame_step  = 10    # only looks at every nth frame
scale       = 0.5   # image scale multiplier
border_size = 25    # number of pixels

# load the model
try:
    rf = pickle.load(open(model_file, "rb"))
except:
    print("Error: Cannot find/load model, probably because the file", model_file, "does not exist. Try running build_classifier.py.")
    quit()

# video time
print("Reading 1 in every", frame_step, "frames, predicting labels for all found objects, and exporting them as a gif.\nMight take a minute.\n")

# setup list of pngs, read video
filenames = []
video = imageio.get_reader(video_file, 'ffmpeg')

# each every i frames
for frame, image in enumerate(video):

    if frame % frame_step == 0:

        # resize and convert image to grayscale
        if (upsidedown): image = transform.rotate(image, 180)
        rescaled  = rescale(image, scale, anti_aliasing=False, multichannel=True)
        grayscale = color.rgb2gray(rescaled)

        # local thresholding
        threshold = filters.threshold_local(grayscale, 255 * scale, offset=0.005)
        binary    = grayscale > threshold
        binary    = util.invert(binary)

##### CROP & REMOVE NOISE ################################################################

        border_size = 25

        x_min = border_size; x_max = binary.shape[1]
        y_min = border_size; y_max = binary.shape[0]

        cropped = np.copy(binary.astype(int)*255)

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

        dilated = morphology.binary_erosion(small_removed, selem=np.full((3,3), 1))
        final   = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

##### CLASSIFIER TIME ####################################################################

        # label objects in image
        labels, num_blobs = label(final, return_num=True)

        # create file name and append it to a list
        filename = f'images/{frame//frame_step}.png'
        filenames.append(filename)

        # setup plots
        fig, axes = pyplot.subplots(1, 2, figsize=(2*5, 5))

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

            # change box color and text based on prediction
            c = "r"; t = "Not Fish"
            # test model with features
            confidence = int(rf.predict_proba([features])[0][1] * 100)
            if rf.predict([features])[0] == 1:
                c = "b"; t = "Fish"

            # draw box
            box = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor=c, facecolor="none")
            axes[1].add_patch(box)

            # add text
            pyplot.text(x0-1, y0-5, t, color=c)
            pyplot.text(x0-1, y0-20, str(confidence)+"%", color=c)

        # build .png
        axes[0].set_title("Binary")
        axes[0].imshow(final, cmap="gray")
        axes[1].set_title("Color")
        axes[1].imshow(rescaled, cmap="gray")
        axes[1].tick_params(left = False, bottom = False)
        for a in axes:
            a.get_xaxis().set_visible(False)
            a.get_yaxis().set_visible(False)
        fig.tight_layout()
        pyplot.savefig(filename)  # create .png
        pyplot.close("all")       # close the plot so matplotlib doesn't yell at me

# build gif from .pngs
with imageio.get_writer('output.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

# delete .pngs
for f in filenames:
    #os.remove(f)
    pass
