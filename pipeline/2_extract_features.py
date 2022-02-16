# This script extracts features for blobs with unset (None/null) labels,
# and creates "game frames" to make the labeling of these blobs faster.
# The game frames and resultant json are fed into game.py.
#
# Before you run this script:
# 1. Set the variables at the top of this script to the location of the
#    images you would like to blob detect + feature extract.

import matplotlib
from matplotlib import pyplot, patches
from blob_extraction import process_image, extract_blobs, get_blob_features
import os
import json
from pathlib import Path

# Set these appropriately:
input_images_path = Path("./frames1/") # The images you want to extract blobs from
game_frames_dir_name = "gameframes" # Will auto-create if it doesn't exist
output_json_path = Path("./pipeline/classifier_unlabeled_data.json")

matplotlib.use('Agg')
pyplot.ioff()
data = []

# Just testing that the output path is ok
with open(output_json_path, "w") as f:
  pass

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
  
  try:
    image = pyplot.imread(image_path.absolute(), False) # type:ignore
  except Exception as e:
    print(e)
    continue

  processed_images = process_image(image)

  axes['top'].imshow(processed_images.rescaled)
  axes['p1'].imshow(processed_images.binary, cmap="gray")
  axes['p2'].imshow(processed_images.cropped, cmap="gray")
  axes['p3'].imshow(processed_images.small_removed, cmap="gray")
  axes['p4'].imshow(processed_images.final, cmap="gray")
  axes['p5'].imshow(processed_images.grayscaled, cmap="gray")

  blobs = extract_blobs(processed_images.final, processed_images.rescaled)

  for blob_num, props in enumerate(blobs):
    features, da = get_blob_features(props, processed_images.grayscaled)

    # draw major and minor axis
    axes['p5'].plot((da.x, da.x2), (da.y, da.y2), color="r", linewidth=1)
    axes['p5'].plot((da.x, da.x3), (da.y, da.y3), color="g", linewidth=1)

    # draw box
    box = patches.Rectangle((da.x0, da.y0), da.w, da.h, linewidth=1, edgecolor="b", facecolor="none")
    axes['p5'].add_patch(box)

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
