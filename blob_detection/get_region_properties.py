
# python 3.10.0
# scikit-image 0.19.0

import math
import time
import numpy as np
from skimage         import data, filters, util, color, morphology, measure
from matplotlib      import pyplot, patches

### binirization/thresholding
### https://en.wikipedia.org/wiki/Thresholding_%28image_processing%29
### https://towardsdatascience.com/image-processing-blob-detection-204dc6428dd
### https://scikit-image.org/docs/0.12.x/auto_examples/segmentation/plot_threshold_adaptive.html

### opening / closing
### https://scikit-image.org/docs/dev/api/skimage.morphology.html#skimage.morphology.opening

### region properties
### https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_regionprops.html

start = time.time()

# setup plot
numplots = 3
fig, axes = pyplot.subplots(1, numplots, figsize=(numplots*5, 5))

# get image in color and grayscale
image = pyplot.imread("yellowtail.jpg", False)
gray  = color.rgb2gray(image)

# local thresholding (seems most promising)
# offset is VERY precise
threshold   = filters.threshold_local(gray, 55, offset=0.005)
binary      = gray > threshold
binary      = util.invert(binary)  # <==== blob_log() detects light blobs on dark background, must invert

# before opening should remove edge blobs

# open + close
opened = morphology.opening(binary, morphology.disk(3))
closed = morphology.closing(opened, morphology.disk(3))

# label objects in image
labels = measure.label(closed, background=0)

# get properties of each object
# https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_regionprops.html
regions = measure.regionprops(labels)
for props in regions:

	# get box dimentions
	y, x           = props.centroid
	y0, x0, y1, x1 = props.bbox
	w, h = x1 - x0, y1 - y0

	# get major and minor axis
	orientation = props.orientation
	x2 = x + math.cos(orientation) * 0.5 * props.minor_axis_length
	y2 = y - math.sin(orientation) * 0.5 * props.minor_axis_length
	x3 = x - math.sin(orientation) * 0.5 * props.major_axis_length
	y3 = y - math.cos(orientation) * 0.5 * props.major_axis_length

	# draw major and minor axis
	axes[2].plot((x, x2), (y, y2), color="r", linewidth=1)
	axes[2].plot((x, x3), (y, y3), color="g", linewidth=1)

	# colors
	r = (x2 / x3) / (y2 / y3)
	if (r > 1):  c = "r"
	else:        c = "b"

	# draw box
	box = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor=c, facecolor="none")
	axes[2].add_patch(box)

# setup plot
axes[0].set_title("Original")
axes[0].imshow(image)
axes[1].set_title("Binary")
axes[1].imshow(closed, cmap="gray")
axes[2].set_title("Labeled")
axes[2].imshow(labels, cmap="nipy_spectral")


end = time.time()
print("Took {:.1f} seconds.".format(end - start))

pyplot.show()


