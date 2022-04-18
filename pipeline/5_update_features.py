# This script updates features for a labeled json dataset, keeping the 
# label and other metadata intact while modifying
#
# Before you run this script:
# 1. Set the variables at the top of the script to point to appropriate
#    locations.

from blob_extraction import process_image, extract_blobs, get_blob_features
from matplotlib import pyplot
import json
from pathlib import Path
from alive_progress import alive_bar

# Set these appropriately:
labeled_data = json.loads(Path("./feature_extraction/classifier_data.json").read_text())
output_json_path = Path("./feature_extraction/classifier_data_updated.json")

training_data = []

data_length = len(labeled_data)
print(f"Updating {data_length} labeled data points with new feature values...")

with alive_bar(data_length) as bar:
  for blob in labeled_data:
    try:
      image = pyplot.imread(blob["filename"])
    except Exception as e:
      print(e)
      continue

    processed_images = process_image(image)
    blobs = extract_blobs(processed_images.final, processed_images.rescaled)

    for blob_num, props in enumerate(blobs):
      features, _ = get_blob_features(props, processed_images.grayscaled)

      training_data.append({
        "filename": blob["filename"],
        "blob_num": blob["blob_num"],
        "features": features,
        "label": blob["label"],
      })
  
    bar()

with open(output_json_path, "w") as f:
  f.write(json.dumps(training_data))
