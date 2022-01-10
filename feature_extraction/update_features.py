from re import S
import matplotlib
from scipy.ndimage import morphology
from skimage import filters, util, color
from matplotlib import pyplot, patches
from skimage import morphology 
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from skimage.measure import label, regionprops
import numpy as np
import time
import math
import os
import sys
import json
from pathlib import Path

old_data = json.loads(Path("./feature_extraction/data.json").read_text())
new_data = []

for counter, blob in enumerate(old_data):
  try:
    image = pyplot.imread(blob["filename"], False)
  except Exception as e:
    print(e)
    continue

  scale = 0.5
  rescaled_original = rescale(image, scale, anti_aliasing=False, multichannel=True)
  gray  = color.rgb2gray(rescaled_original)

  # local thresholding
  # This is the most time-consuming step.
  threshold   = filters.threshold_local(gray, 255*scale, offset=0.005)
  binary      = gray > threshold
  binary      = util.invert(binary)

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
  regions = regionprops(labels, rescaled_original)
  props = regions[blob["blob_num"]]
  
  # Calculate box dimensions
  y, x = props.centroid
  y0, x0, y1, x1 = props.bbox
  w, h = x1 - x0, y1 - y0

  features = {
    "blob_x_coord": x,
    "blob_y_coord": y,
    "blob_width": w,
    "blob_height": h,
    "blob_bbox": props.bbox_area,
    "blob_euler_num": props.euler_number.item(),
    "blob_extent": props.extent,
    "blob_orientation": props.orientation,
    "blob_perimeter": props.perimeter,
    "blob_num_pixels": props.area.item(),
    "blob_max_intensity": props.max_intensity.tolist(),
    "blob_mean_intensity": props.mean_intensity.tolist(),
    "blob_min_intensity": props.min_intensity.tolist(),
    "blob_solidity": props.solidity,
    # To add new features to the set, just add them here.
    # All features will be overwritten with new values if
    # you tweak how they're generated. The filename, blob
    # number, and label will be taken from the old data.
    }

  new_data.append({
    "filename": blob["filename"],
    "blob_num": blob["blob_num"],
    "features": features,
    "label": blob["label"],
  })

  print(counter)

with open("new_data.json", "w") as f:
  try:
    f.write(json.dumps(new_data))
  except Exception as e:
    print(e)
