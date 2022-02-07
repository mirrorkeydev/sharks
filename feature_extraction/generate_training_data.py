# This script generates a minimal feature vector for ML model consumption.
#
# Before you run this script:
# 1. Set the variables at the top of the script to point to appropriate
#    locations.

import json
from pathlib import Path

# Set these appropriately:
labeled_data = json.loads(Path("./feature_extraction/fish_classifier_data.json").read_text())
output_training_data_path = Path("./feature_extraction/fish_classifier_training_data.json")

features_and_labels = []
for data in labeled_data:
  # ML model doesn't know what do with None or Skip (999) labels,
  # so exclude these from training data generation.
  if data["label"] != None and data["label"] != 999:
    features_and_labels.append([val for _, val in data["features"].items()] + [data["label"]])

with open(output_training_data_path, "w") as f:
  f.write(json.dumps(features_and_labels))
