from scipy.ndimage import morphology
from skimage import filters, util, color
from matplotlib import pyplot, patches
from skimage import morphology 
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from skimage.measure import label, regionprops
from matplotlib.widgets import Button
import numpy as np
import time
import math
from pathlib import Path

class Answer():
  def __init__(self):
    self.value = None
  def event(self, event):
    self.value = 1
  def noise(self, event):
    self.value = 0

training_set = []
fig, axes = pyplot.subplot_mosaic([
  ['top', 'top', 'top'],
  ['top', 'top', 'top'],
  ['p1', 'p2', 'p3'],
  ['p4', 'p5', '.']
], figsize=(15, 13))
axes['top'].set_title("Image")
axes['p1'].set_title("Local Thresholding")
axes['p2'].set_title("Edge blobs removed")
axes['p3'].set_title(f"Small objects removed")
axes['p4'].set_title("Noisy objects removed")
axes['p5'].set_title("Blobs")
event_button_axis = pyplot.axes([0.7, 0.05, 0.1, 0.075])
noise_button_axis = pyplot.axes([0.81, 0.05, 0.1, 0.075])
event_button = Button(event_button_axis, 'Event')
noise_button = Button(noise_button_axis, "Noise")
fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))


for image_path in Path("./extractedframesscoring").iterdir():
  start = time.time()
  # Greyscale image
  try:
    image = pyplot.imread(image_path.absolute(), False)
  except Exception as e:
    print(e)
    continue
  scale = 0.5
  rescaled_original = rescale(image, scale, anti_aliasing=False, multichannel=True)
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

  dilated = morphology.binary_erosion(small_removed, selem=np.full((3,3), 1))
  small_removed_2 = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

  axes['top'].imshow(rescaled_original)
  axes['p1'].imshow(binary, cmap="gray")
  axes['p2'].imshow(no_edge_blobs, cmap="gray")
  axes['p3'].imshow(small_removed, cmap="gray")
  axes['p4'].imshow(small_removed_2, cmap="gray")
  axes['p5'].imshow(gray, cmap="gray")

  # Find blobs
  labels, num_blobs = label(small_removed_2, return_num=True)
  regions = regionprops(labels, rescaled_original)
  for props in regions:
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

    features = [
      x, y, # coordinate location in image
      w, h, # height, width of blob
      props.bbox_area, # bounding box area
      props.euler_number, # number of connected components subtracted by number of holes
      props.extent, # ratio of pixels in the region to pixels in the total bounding box
      props.orientation, # angle between the 0th axis (rows) and the major axis of the ellipse 
      props.perimeter, # perimeter of object
      props.area, # number of pixels of the region.
      props.max_intensity, # value with the max intensity in the region (RGB 0-1)
      props.mean_intensity, # value with the mean intensity in the region (RGB 0-1)
      props.min_intensity, # value with the min intensity in the region (RGB 0-1)
      props.solidity, # ratio of pixels in the region to pixels of the convex hull image.
    ]

    a = Answer()
    event_button.on_clicked(a.event)
    noise_button.on_clicked(a.noise)
    pyplot.show(block=False)
    while a.value is None:
      pyplot.pause(0.1)

    # training_set.append(({k: props[k] for k in [*props]}, a.value))
    training_set.append((features, a.value))

    box.remove()
    box_shadow = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor="#666", facecolor="none")
    axes['p5'].add_patch(box_shadow)
    pyplot.draw()

    print(training_set[-1])

  axes['p5'].clear()

pyplot.close(fig)

with open("out.txt", "w") as f:
  f.write(str(training_set))
