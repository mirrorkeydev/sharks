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
from sklearn.ensemble     import RandomForestClassifier
from matplotlib           import pyplot, patches

# parameters
video_file = "../videos/yellow tail.mp4"
model_file = "./trained_model.json"
frame_step = 10
scale = 0.5

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
        image = transform.rotate(image, 180)
        rescaled = rescale(image, scale, anti_aliasing=False, multichannel=True)
        gray = color.rgb2gray(rescaled)

        # local thresholding
        threshold = filters.threshold_local(gray, 255 * scale, offset=0.005)
        binary    = gray > threshold
        binary    = util.invert(binary)

        # remove blobs touching borders
        no_edge_blobs = np.copy(binary.astype(int)*255)
        def flood(value, location):
            if value > 0:
                flood_fill(no_edge_blobs, location, 0, tolerance=70, in_place=True)
        x_max = no_edge_blobs.shape[1] - 1
        for i, row in enumerate(no_edge_blobs):
            if i == 0 or i == no_edge_blobs.shape[0] - 1:
                for j, cell in enumerate(row):
                    flood(cell, (i, j))
            elif row[0] > 0:
                flood(row[0], (i, 0))
            elif row[x_max] > 0:
                flood(row[x_max], (i, x_max))

        # remove small objects (faster than area_opening as it works on binary images)
        area = 512 * scale # lower gives more false positives
        small_removed = morphology.remove_small_objects(no_edge_blobs.astype(bool), min_size=area, connectivity=1)

        dilated = morphology.binary_erosion(small_removed, selem=np.full((3,3), 1))
        small_removed_2 = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

        # label objects in image
        labels, num_blobs = label(small_removed_2, return_num=True)

        # create file name and append it to a list
        filename = f'{frame//frame_step}.png'
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

            # change box color based on prediction
            c = "r"
            # test model with features
            if rf.predict([features])[0] == 1:
                c = "b"

            # draw box
            box = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor=c, facecolor="none")
            axes[1].add_patch(box)

        # build .png
        axes[0].set_title("Binary")
        axes[0].imshow(small_removed_2, cmap="gray")
        axes[1].set_title("Predicted")
        axes[1].imshow(rescaled)
        axes[1].tick_params(left = False, bottom = False)
        for a in axes:
            a.get_xaxis().set_visible(False)
            a.get_yaxis().set_visible(False)
        fig.tight_layout()
        pyplot.savefig(filename)   # create .png
        pyplot.close()             # close the plot so matplotlib doesn't yell at me

# build gif from .pngs
with imageio.get_writer('output.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

# delete .pngs
for f in filenames:
    os.remove(f)
