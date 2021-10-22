
# python 3.10.0
# scikit-iamge 0.19.0

import time
from skimage         import data, filters, util, color
from matplotlib      import pyplot
from skimage.feature import blob_dog, blob_log, blob_doh
from math            import sqrt

### binirization/thresholding
### https://en.wikipedia.org/wiki/Thresholding_%28image_processing%29
### https://towardsdatascience.com/image-processing-blob-detection-204dc6428dd
### https://scikit-image.org/docs/0.12.x/auto_examples/segmentation/plot_threshold_adaptive.html

### blob detection concept and implementation
### https://en.wikipedia.org/wiki/Blob_detection
### https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_blob.html

###  kelp: FI010844.MOV
###  fish: 00000198.mov
### fish2: Consumption_cage_boat.mov


### steps are: grayscale -> binarize (thresholding) -> blob detection

### local thresholding looks at some section of the image as oppsosed to the entire image at once
### makes it possible to ignore drastic changes in lighting/seafloor that occur in a frame


start = time.time()

# setup plot
numplots = 4
fig, axes = pyplot.subplots(1, numplots, figsize=(numplots*5, 5))

# get image in color and grayscale
image = pyplot.imread("fish1.jpg", False)
gray  = color.rgb2gray(image)

# local thresholding (seems most promising)
# offset is VERY precise
threshold   = filters.threshold_local(gray, 55, offset=0.005)
binary      = gray > threshold
binary      = util.invert(binary)  # <==== blob_log() detects light blobs on dark backgroud, must invert

# blob detection
# these perameters matter a lot!
blobs = blob_log(binary, min_sigma=10, max_sigma=100, num_sigma=10, threshold=0.2, overlap=0.0, exclude_border=(40))
print("Detected", len(blobs), "blobs.")

# for each blob, draw circle
for b in blobs:
    y, x, s = b
    r = s * sqrt(2)
    c = pyplot.Circle((x, y), r, color="red", linewidth=1, fill=False)
    axes[3].add_patch(c)
    print("  Blob at", x, "/", y)

# setup plot
axes[0].set_title("Original")
axes[0].imshow(image)
axes[1].set_title("Grayscale")
axes[1].imshow(gray, cmap="gray")
axes[2].set_title("Thresholding (Local)")
axes[2].imshow(binary, cmap="gray")
axes[3].set_title("Laplacian of Gaussian (" + str(len(blobs)) + " blobs)")
axes[3].imshow(image)

end = time.time()
print("Took {:.2f} seconds.".format(end - start))

pyplot.show()

