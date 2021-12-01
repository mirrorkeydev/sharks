import PySimpleGUI as sg
from pathlib import Path
import json
import sys

def output_data(data):
  with open("training_data_with_labels.json", "w") as f:
    json.dump(data, f)

feature_data = json.loads(Path("./feature_extraction/out.json").read_text())
training_data_with_labels = []

for data in feature_data:
  absolute_path, blob_num, features = data
  img_stem = Path(absolute_path).stem
  game_img_path = f"./trainingnoisedone/{img_stem}blob{blob_num}.png"

  layout = [
    [sg.Image(game_img_path)],
    [sg.Button('Noise'), sg.Button('Event')]
  ]

  window = sg.Window('Game time', layout, location=(0,0))
  while True:
    event, _ = window.read()
    if event == sg.WIN_CLOSED:
      output_data(training_data_with_labels)
      sys.exit(0)
    break

  training_data_with_labels.append(features + [1 if event == "Event" else 0])
  print(training_data_with_labels)
  window.close()

output_data(training_data_with_labels)
print("You did all of the data!")
