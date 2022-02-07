# This script extracts features for blobs with unset (None/null) labels,
# and creates "game frames" to make the labeling of these blobs faster.
# The game frames and resultant json are fed into game.py.
#
# Before you run this script:
# 1. Set the variables at the top of this script to the location of the
#    images you would like to blob detect + feature extract.
# 2. (Optional) Change the blob detection logic. Warning: if you have
#    already labeled data using different blob detection logic, then changing
#    this logic will make the previous data incompatible with the new data.
#    This is ok if you are going to use the new data in a separate classifier.

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
import json
from pathlib import Path

# Set these appropriately:
input_images_path = Path("./extractedframeskelp/")
game_frames_dir_name = "kelpgameframes" # Will auto-create if it doesn't exist
output_json_path = Path("./feature_extraction/kelp_classifier_unlabeled_data.json")

matplotlib.use('Agg')
pyplot.ioff()
data = []

for image_path in input_images_path.iterdir():
  fig, axes = pyplot.subplot_mosaic([
    ['top', 'top', 'top'],
    ['top', 'top', 'top'],
    ['p1', 'p2', 'p3'],
    ['p4', 'p5', '.']
  ], figsize=(15, 13)) # type:ignore
  axes['top'].set_title("Image")
  axes['p1'].set_title("Local Thresholding")
  axes['p2'].set_title("Edge blobs removed")
  axes['p3'].set_title(f"Small objects removed")
  axes['p4'].set_title("Noisy objects removed")
  axes['p5'].set_title("Blobs")
  start = time.time()
  # Greyscale image
  try:
    image = pyplot.imread(image_path.absolute(), False) # type:ignore
  except Exception as e:
    print(e)
    continue
  scale = 0.5
  rescaled_original = rescale(image, scale, anti_aliasing=False, channel_axis=2)
  gray  = color.rgb2gray(rescaled_original)

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

  dilated = morphology.binary_erosion(small_removed, footprint=np.full((3,3), 1))
  small_removed_2 = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

  axes['top'].imshow(rescaled_original)
  axes['p1'].imshow(binary, cmap="gray")
  axes['p2'].imshow(no_edge_blobs, cmap="gray")
  axes['p3'].imshow(small_removed, cmap="gray")
  axes['p4'].imshow(small_removed_2, cmap="gray")
  axes['p5'].imshow(gray, cmap="gray")

  # Find blobs
  labels, num_blobs = label(small_removed_2, return_num=True) # type:ignore
  regions = regionprops(labels, rescaled_original)
  for blob_num, props in enumerate(regions):
    # get box dimentions
    y, x = props.centroid
    y0, x0, y1, x1 = props.bbox
    w, h = x1 - x0, y1 - y0

    # get major and minor axis
    orientation = props.orientation
    x2 = x + math.cos(orientation) * 0.5 * props.minor_axis_length
    y2 = y - math.sin(orientation) * 0.5 * props.minor_axis_length
    x3 = x - math.sin(orientation) * 0.5 * props.major_axis_length
    y3 = y - math.cos(orientation) * 0.5 * props.major_axis_length

    # draw major and minor axis
    axes['p5'].plot((x, x2), (y, y2), color="r", linewidth=1)
    axes['p5'].plot((x, x3), (y, y3), color="g", linewidth=1)

    # draw box
    box = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor="b", facecolor="none")
    axes['p5'].add_patch(box)
    
    image_y_size, image_x_size = gray.shape
    image_total_area = image_x_size * image_y_size

    features = {
      "blob_x_coord": x / image_x_size,
      "blob_y_coord": y / image_y_size,
      "blob_width": w / image_x_size,
      "blob_height": h / image_y_size,
      "blob_bbox": props.bbox_area / image_total_area,
      "blob_euler_num": props.euler_number.item(),
      "blob_extent": props.extent,
      "blob_orientation": props.orientation,
      "blob_perimeter": props.perimeter, # perimeter is very difficult to normalize
      "blob_num_pixels": props.area.item() / image_total_area,
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
    }

    data.append({
      "filename": str(image_path.absolute()),
      "blob_num": blob_num,
      "features": features,
      "label": None,
    })

    # Put "game frames" into directory (and create directory if it doesn't exist)
    results_dir = Path.cwd().joinpath(game_frames_dir_name)
    if not os.path.isdir(results_dir.absolute()):
      results_dir.mkdir(parents=True, exist_ok=True)
    pyplot.savefig(f"./{game_frames_dir_name}/{image_path.stem}blob{blob_num}.png")
    print(f"./{game_frames_dir_name}/{image_path.stem}blob{blob_num}.png")

    box.remove()
    pyplot.draw()

  axes['p5'].clear()
  pyplot.close('all')

with open(output_json_path, "w") as f:
  try:
    f.write(json.dumps(data))
  except Exception as e:
    print(e)
    print("error json encoding, writing plaintext")
    f.write(str(data))
