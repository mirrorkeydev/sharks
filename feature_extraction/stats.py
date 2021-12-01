import json
from pathlib import Path
import matplotlib.pyplot as plt
data = json.loads(Path("./feature_extraction/training_data_with_labels.json").read_text())

fig, axes = plt.subplot_mosaic([
  ['1', '2', '3', '4'],
  ['5', '6', '7', '8'],
  ['9', '10', '11', '12'],
  ['13', '14', '15', '.']
], figsize=(15, 13))
axes['1'].set_title("Blob x coord")
axes['2'].set_title("Blob y coord")
axes['3'].set_title("Blob width")
axes['4'].set_title("Blob height")
axes['5'].set_title("Blob bounding box area")
axes['6'].set_title("Blob Euler number")
axes['7'].set_title("Blob extent")
axes['8'].set_title("Blob orientation")
axes['9'].set_title("Blob perimeter")
axes['10'].set_title("Blob number of pixels")
axes['11'].set_title("Blob max intensity")
axes['12'].set_title("Blob mean intensity")
axes['13'].set_title("Blob min intensity")
axes['14'].set_title("Blob solidity")
axes['15'].set_title("Label")

print(f"{len(data)} training points")
for i in range(15):
  axes[str(i+1)].hist([x[i] for x in data], 10)


# fig.savefig("test.png")
plt.show()

print("example data point:")
print("""
coordinate x (possible values 0-960): {}
coordinate y (possible values 0-540): {}
width of blob: {}
height of blob: {}
blob bounding box area : {}
euler_number (number of connected components subtracted by number of holes): {}
extent (ratio of pixels in the region to pixels in the total bounding box): {}
orientation (angle between the 0th axis (rows) and the major axis of the ellipse): {}
perimeter of blob: {}
number of pixels in the blob: {}
value with the max intensity in the region (RGB each 0-1): {}
value with the mean intensity in the region (RGB each 0-1): {}
value with the min intensity in the region (RGB each 0-1): {}
solidity (ratio of pixels in the region to pixels of the convex hull image): {}
event (1) or noise (0): {}
""".format(*data[258]))
