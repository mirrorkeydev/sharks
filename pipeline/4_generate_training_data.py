# This script generates a minimal feature vector for ML model consumption.
#
# Before you run this script:
# 1. Set the variables at the top of the script to point to appropriate
#    locations.

import json
from pathlib import Path

# Set these appropriately:
labeled_data = [
    json.loads(Path("./pipeline/data/blake_classifier_complete_data.json").read_text()),
    json.loads(Path("./pipeline/data/blake_classifier_complete_data_2.json").read_text()),
    json.loads(Path("./pipeline/data/melanie_classifier_complete_data.json").read_text()),
    json.loads(Path("./pipeline/data/scott_classifier_complete_data.json").read_text()),
  ]
output_training_data_path = Path("./pipeline/data/classifier_training_data.json")

features_and_labels = []
for dataset in labeled_data:
  for data in dataset:
    # ML model doesn't know what do with None or Skip (999) labels,
    # so exclude these from training data generation.
    if data["label"] != None and data["label"] != 999:
      features_and_labels.append([val for _, val in data["features"].items()] + [data["label"]])

# Add in some more fish data
fishies = json.loads(Path("./pipeline/data/old_fish_classifier_data.json").read_text())
for data in fishies:
  if data["label"] == 1: # fish in the old dataset are labled 1
    features_and_labels.append([val for _, val in data["features"].items()] + [2]) # fish in the new dataset are labeled 2

with open(output_training_data_path, "w") as f:
  f.write(json.dumps(features_and_labels))
