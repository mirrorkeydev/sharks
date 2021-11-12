# Fairly accurate blob detector taking about 0.33 seconds per resized frame.
# On a 30FPS video, this would take around 10 seconds per second of footage.
# This was tested manually and appears to work well on all sample_images,
# but will need further automated testing to conclude relative score.
from scipy.ndimage import morphology
from skimage import filters, util, color
from matplotlib import pyplot, patches
from skimage.feature import blob_log
from skimage import morphology 
from skimage.transform import rescale
from skimage.segmentation import flood_fill
from skimage.measure import label, regionprops
from math import sqrt
import numpy as np
import time
import math
from pathlib import Path
import os

for image_path in Path("./extractedframesscoring").iterdir():
	print(image_path.stem)
	fig, axes = pyplot.subplots(2, 3, figsize=(15, 10))
	t1 = time.time()

	start = time.time()

	# Greyscale image
	try:
		image = pyplot.imread(image_path.absolute(), False)
	except Exception as e:
		print(e)
		continue
	gray  = color.rgb2gray(image)
	scale = 0.5
	gray = rescale(gray, scale, anti_aliasing=False)

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

	# Find blobs
	labels, num_blobs = label(small_removed_2, return_num=True)
	print(f"{num_blobs} blobs found")
	regions = regionprops(labels)
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
		axes[1, 2].plot((x, x2), (y, y2), color="r", linewidth=1)
		axes[1, 2].plot((x, x3), (y, y3), color="g", linewidth=1)

		# draw box
		box = patches.Rectangle((x0, y0), w, h, linewidth=1, edgecolor="b", facecolor="none")
		axes[1, 2].add_patch(box)

	end = time.time()
	print("Took {:.2f} seconds.".format(end - start))

	# setup plot
	axes[0, 0].set_title("Grayscale")
	axes[0, 0].imshow(gray, cmap="gray")
	axes[0, 1].set_title("Local Thresholding")
	axes[0, 1].imshow(binary, cmap="gray")
	axes[0, 2].set_title("Edge blobs removed")
	axes[0, 2].imshow(no_edge_blobs, cmap="gray")
	axes[1, 0].set_title(f"Small objects removed")
	axes[1, 0].imshow(small_removed, cmap="gray")
	axes[1, 1].set_title("Noisy objects removed")
	axes[1, 1].imshow(small_removed_2, cmap="gray")
	axes[1, 2].set_title("Blobs")
	axes[1, 2].imshow(gray, cmap="gray")

	pyplot.show()
	# results_dir = Path.cwd().joinpath("results")
	# if not os.path.isdir(results_dir.absolute()):
	# 	results_dir.mkdir(parents=True, exist_ok=True)
	# pyplot.savefig(f"./results/{image_path.stem}.png")

	# del fig
	# pyplot.clf()
	# pyplot.close()
