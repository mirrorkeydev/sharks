# This script launches a "labeling game" in which the user can assign labels
# to blobs in images.
#
# Before you run this script:
# 1. Run extract_features.py on the image dataset you would like to label.
#    This will give you a json data file and a directory of "game frames".
# 2. Set the variables at the top of this script to the location of the
#    json file and the game frames.
#
# IMPORTANT:
# The game can be exited without destroying your progress. Exit using "X" in the
# top right, and it will output a new json with labels for all frames you got
# to, and None/null for the frames you didn't get to. If you load in this output
# json as the input json for your next play session, it will pick up where you 
# left off.

import PySimpleGUI as sg
from pathlib import Path
import json
import sys

# Set these appropriately:
input_data_path = Path("./feature_extraction/classifier_unlabeled_data.json")
output_data_path = Path("./feature_extraction/classifier_data.json")
game_frames_path = Path("./gameframes")

def output_data(data):
  with open(output_data_path, "w") as f:
    json.dump(data, f)
    pass

label_lookup = {
  "Noise (0)": 0,
  "Fish (1)": 1,
  "Kelp (2)": 2,
  "Shark (3)": 3,
  "Sunspot (4)": 4,
  "Rock (5)": 5,
  "Bubble (6)": 6,
  "Camera Edge (7)": 7,
  "Skip/Unclear": 999,
}

feature_data = json.loads(input_data_path.read_text())

for i, data in enumerate(feature_data):

  if data["label"] != None:
    continue

  img_stem = Path(data["filename"]).stem
  blob_num = data["blob_num"]
  game_img_path = f"{game_frames_path}/{img_stem}blob{blob_num}.png"

  layout = [
    [sg.Image(game_img_path)],
    [sg.Button(x) for x in label_lookup.keys()]
  ]

  sg.OneLineProgressMeter("progressbar", i, len(feature_data), 'progress')

  window = sg.Window('Game time', layout, location=(0,0))
  while True:
    event, _ = window.read() # type:ignore
    if event == sg.WIN_CLOSED:
      output_data(feature_data)
      sys.exit(0)
    break

  feature_data[i] = {**data, "label": label_lookup[event]}
  window.close()

output_data(feature_data)
print("You did all of the data!")
