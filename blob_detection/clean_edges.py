import time
from skimage import filters, util, color
from matplotlib import pyplot
from skimage.feature import blob_log
from skimage.morphology import area_opening
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from math import sqrt
import numpy as np

start = time.time()

fig, axes = pyplot.subplots(2, 3, figsize=(15, 10))

# Greyscale image
image = pyplot.imread("./sample_images/manyfish.png", False)
gray  = color.rgb2gray(image)
scale = 0.5
gray = rescale(gray, scale, anti_aliasing=False)

# local thresholding
threshold   = filters.threshold_local(gray, 389*scale, offset=0.005)
binary      = gray > threshold
binary      = util.invert(binary)  # <==== blob_log() detects light blobs on dark backgroud, must invert

# Remove blobs touching borders
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

# Area opening
area = 1024*scale # lower gives more false positives
area_opened = area_opening(no_edge_blobs, area_threshold=area)

# Intersect area opening with grayscale image
diff = gray * area_opened

# Find blobs
blobs = blob_log(diff, min_sigma=50*scale, max_sigma=100*scale, num_sigma=10, threshold=0.2, overlap=0.0, exclude_border=(40))
print("Detected", len(blobs), "blobs.")
for b in blobs:
    y, x, s = b
    r = s * sqrt(2)
    c = pyplot.Circle((x, y), r, color="red", linewidth=1, fill=False)
    axes[1, 2].add_patch(c)
    
# setup plot
axes[0, 0].set_title("Grayscale")
axes[0, 0].imshow(gray, cmap="gray")
axes[0, 1].set_title("Local Thresholding")
axes[0, 1].imshow(binary, cmap="gray")
axes[0, 2].set_title("Remove edge blobs")
axes[0, 2].imshow(no_edge_blobs, cmap="gray")
axes[1, 0].set_title(f"Area Opening")
axes[1, 0].imshow(area_opened, cmap="gray")
axes[1, 1].set_title("Diff")
axes[1, 1].imshow(diff, cmap="gray")
axes[1, 2].set_title("Laplacian of Gaussian")
axes[1, 2].imshow(gray, cmap="gray")

end = time.time()
print("Took {:.2f} seconds.".format(end - start))

pyplot.show()

