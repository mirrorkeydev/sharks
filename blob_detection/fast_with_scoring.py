# Fairly accurate blob detector taking about 0.33 seconds per resized frame.
# On a 30FPS video, this would take around 10 seconds per second of footage.

from scipy.ndimage import morphology
from skimage import filters, util, color
from matplotlib import pyplot, patches
from skimage.feature import blob_log
from skimage import morphology 
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from skimage.measure import label, regionprops
from math import sqrt
import numpy as np
import time
import math
from pathlib import Path
import os
from scoring import Scorer

scorer = Scorer()

for image_path in Path("./extractedframesscoring").iterdir():
  start = time.time()
  # Greyscale image
  try:
    image = pyplot.imread(image_path.absolute(), False)
  except Exception as e:
    print(e)
    continue
  gray  = color.rgb2gray(image)
  scale = 0.5
  gray = rescale(gray, scale, anti_aliasing=False)

  # local thresholding
  # This is the most time-consuming step.
  threshold   = filters.threshold_local(gray, 255*scale, offset=0.005)
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

  # Remove small objects (faster than area_opening as it works on binary images)
  area = 512*scale # lower gives more false positives
  small_removed = morphology.remove_small_objects(no_edge_blobs.astype(bool), min_size=area, connectivity=1)

  dilated = morphology.binary_erosion(small_removed, selem=np.full((3,3), 1))
  small_removed_2 = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

  # Find blobs
  labels, num_blobs = label(small_removed_2, return_num=True)
  scorer.score_frame(image_path.stem, num_blobs)

  end = time.time()

print("Took {:.2f} seconds for last image.".format(end - start))
scorer.print_results()
