from pathlib import Path
import pprint
import json

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)

files_and_features = json.loads(Path("./feature_extraction/out.json").read_text())
features_and_labels = json.loads(Path("./feature_extraction/training_data_with_labels.json").read_text())

data = []

for i in range(len(files_and_features)):
  file_name, blob_num, features = files_and_features[i]

  if i < len(features_and_labels):
    data.append({
      "filename": file_name,
      "blob_num": blob_num,
      "features": {
        "blob_x_coord": features[0],
        "blob_y_coord": features[1],
        "blob_width": features[2],
        "blob_height": features[3],
        "blob_bbox": features[4],
        "blob_euler_num": features[5],
        "blob_extent": features[6],
        "blob_orientation": features[7],
        "blob_perimeter": features[8],
        "blob_num_pixels": features[9],
        "blob_max_intensity": features[10],
        "blob_mean_intensity": features[11],
        "blob_min_intensity": features[12],
        "blob_solidity": features[13],
      },
      "label": features_and_labels[i][-1],
    })
    # pp.pprint(data)

with open("data.json", "w") as f:
  try:
    f.write(json.dumps(data))
  except Exception as e:
    print(e)
