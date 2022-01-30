# This script updates features and generates a minimal feature vector for
# ML model consumption.
#
# Before you run this script:
# 1. Set the variables at the top of the script to point to appropriate
#    locations.
# 2. Ensure that the blob detection logic between the "BLOB LOGIC START"
#    and "BLOB LOGIC END" comments matches the same logic with which
#    the old_data was generated with. If it doesn't match, then labels
#    will be arbitrarily assigned to blobs and the data becomes garbage.
#
# TODO: split feature vector and feature updating functionality into
# separate scripts?

from scipy.ndimage import morphology
from skimage import filters, util, color
from matplotlib import pyplot, patches
from skimage import morphology 
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from skimage.measure import label, regionprops
import numpy as np
import json
from pathlib import Path

# Set these appropriately:
labeled_data = json.loads(Path("./feature_extraction/kelp_classifier_data.json").read_text())
output_json_path = Path("./feature_extraction/kelp_classifier_data_updated.json")
output_training_data_path = Path("./feature_extraction/kelp_classifier_training_data.json")

training_data = []

for counter, blob in enumerate(labeled_data):
  try:
    image = pyplot.imread(blob["filename"])
  except Exception as e:
    print(e)
    continue

  # BLOB LOGIC START ----------------------------------------------------------
  scale = 0.5
  rescaled_original = rescale(image, scale, anti_aliasing=False, channel_axis=2)
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

  dilated = morphology.binary_erosion(small_removed, footprint=np.full((3,3), 1))
  small_removed_2 = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

  # Find blobs
  labels, num_blobs = label(small_removed_2, return_num=True) # type:ignore
  regions = regionprops(labels, rescaled_original)
  props = regions[blob["blob_num"]]

  # BLOB LOGIC END ----------------------------------------------------------

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
    "blob_max_intensity_r": props.max_intensity.tolist()[0],
    "blob_max_intensity_g": props.max_intensity.tolist()[1],
    "blob_max_intensity_b": props.max_intensity.tolist()[2],
    "blob_mean_intensity_r": props.mean_intensity.tolist()[0],
    "blob_mean_intensity_g": props.mean_intensity.tolist()[1],
    "blob_mean_intensity_b": props.mean_intensity.tolist()[2],
    "blob_min_intensity_r": props.min_intensity.tolist()[0],
    "blob_min_intensity_g": props.min_intensity.tolist()[1],
    "blob_min_intensity_b": props.min_intensity.tolist()[2],
    "blob_solidity": props.solidity,
    # To add new features to the set, just add them here.
    # All features will be overwritten with new values if
    # you tweak how they're generated. The filename, blob
    # number, and label will be taken from the old data.
    }

  training_data.append({
    "filename": blob["filename"],
    "blob_num": blob["blob_num"],
    "features": features,
    "label": blob["label"],
  })

with open(output_json_path, "w") as f:
  f.write(json.dumps(training_data))

features_and_labels = []
for data in training_data:
  # ML model doesn't know what do with None or Skip (999) labels,
  # so exclude these from training data generation.
  if data["label"] != None and data["label"] != 999:
    features_and_labels.append([val for _, val in data["features"].items()] + [data["label"]])

with open(output_training_data_path, "w") as f:
  f.write(json.dumps(features_and_labels))
