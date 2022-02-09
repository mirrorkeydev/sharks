import json
from pathlib import Path
import matplotlib.pyplot as plt
data = json.loads(Path("./feature_extraction/data.json").read_text())
print(f"{len(data)} training points")

fig, axes = plt.subplot_mosaic([
  ['1', '2', '3', '4'],
  ['5', '6', '7', '8'],
  ['9', '10', '11', '12'],
  ['13', '14', '15', '.']
], figsize=(15, 13))

i = 0
for key, _ in data[0]["features"].items():
  i += 1
  axes[str(i)].hist([x["features"][key] for x in data], 10)
  axes[str(i)].set_title(key)
axes['15'].set_title("Label")
axes['15'].hist([x["label"] for x in data], 10)

# fig.savefig("test.png")
plt.show()

print("example data point:")
print("""
relative coordinate x (possible values 0-1): {features[blob_x_coord]}
relative coordinate y (possible values 0-1): {features[blob_y_coord]}
relative width of blob: {features[blob_width]}
relative height of blob: {features[blob_height]}
relative blob bounding box area : {features[blob_bbox]}
euler_number (number of connected components subtracted by number of holes): {features[blob_euler_num]}
extent (ratio of pixels in the region to pixels in the total bounding box): {features[blob_extent]}
orientation (angle between the 0th axis (rows) and the major axis of the ellipse): {features[blob_orientation]}
perimeter of blob: {features[blob_perimeter]}
number of pixels in the blob: {features[blob_num_pixels]}
value with the max intensity in the region (RGB each 0-1): {features[blob_max_intensity]}
value with the mean intensity in the region (RGB each 0-1): {features[blob_mean_intensity]}
value with the min intensity in the region (RGB each 0-1): {features[blob_min_intensity]}
solidity (ratio of pixels in the region to pixels of the convex hull image): {features[blob_solidity]}
event (1) or noise (0): {label}
""".format(**data[258]))
