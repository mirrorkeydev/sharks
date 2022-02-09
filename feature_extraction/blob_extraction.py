from scipy.ndimage import morphology
from skimage import filters, util, color, transform
from skimage import morphology 
from skimage.transform import rescale
from skimage.measure import label, regionprops
import numpy as np
import math
from dataclasses import dataclass

@dataclass
class ProcessedImages:
  rescaled: np.ndarray
  grayscaled: np.ndarray
  binary: np.ndarray
  cropped: np.ndarray
  small_removed: np.ndarray
  dilated: np.ndarray
  final: np.ndarray

@dataclass
class BlobDrawingAttributes:
  """
  Provides helper attributes to draw boxes around blobs on images.
  These are not the same as the attributes used for machine learning
  because they are not normalized on a 0-1 scale.
  """
  x: float
  y: float
  x0: float
  y0: float
  x2: float
  y2: float
  x3: float
  y3: float
  w: float
  h: float

def process_image(image) :
  scale = 0.5
  upsidedown = False
  border_size = 25

  # resize and convert image to grayscale
  if (upsidedown): image = transform.rotate(image, 180)
  rescaled  = rescale(image, scale, anti_aliasing=False, channel_axis=2)
  grayscale = color.rgb2gray(rescaled)

  # local thresholding
  threshold = filters.threshold_local(grayscale, 255 * scale, offset=0.005)
  binary    = grayscale > threshold
  binary    = util.invert(binary)

  x_min = border_size; x_max = binary.shape[1]
  y_min = border_size; y_max = binary.shape[0]

  cropped = np.copy(binary.astype(int)*255)

  # remove horizontal borders
  for x in range(0, x_max):
      for y in list(range(0, y_min)) + list(range(y_max - border_size, y_max)):
          cropped[y][x] = 0

  # remove vertical borders
  for y in range(0, y_max):
      for x in list(range(0, x_min)) + list(range(x_max - border_size, x_max)):
          cropped[y][x] = 0

  # remove small objects (faster than area_opening as it works on binary images)
  area = 512 * scale # lower gives more false positives
  small_removed = morphology.remove_small_objects(cropped.astype(bool), min_size=area, connectivity=1)

  dilated = morphology.binary_erosion(small_removed, footprint=np.full((3,3), 1))
  final = morphology.remove_small_objects(dilated.astype(bool), min_size=area, connectivity=1)

  return ProcessedImages(rescaled, grayscale, binary, cropped, small_removed, dilated, final)

def extract_blobs(processed_image, rescaled_image):
  labels, _ = label(processed_image, return_num=True) # type:ignore
  regions = regionprops(labels, rescaled_image)
  return regions

def get_blob_features(props, grayscaled_image):

  # get box dimensions
  y, x = props.centroid
  y0, x0, y1, x1 = props.bbox
  w, h = x1 - x0, y1 - y0

  # get major and minor axis
  orientation = props.orientation
  x2 = x + math.cos(orientation) * 0.5 * props.minor_axis_length
  y2 = y - math.sin(orientation) * 0.5 * props.minor_axis_length
  x3 = x - math.sin(orientation) * 0.5 * props.major_axis_length
  y3 = y - math.cos(orientation) * 0.5 * props.major_axis_length
  
  image_y_size, image_x_size = grayscaled_image.shape
  image_total_area = image_x_size * image_y_size

  features = {
    "blob_x_coord": x / image_x_size,
    "blob_y_coord": y / image_y_size,
    "blob_width": w / image_x_size,
    "blob_height": h / image_y_size,
    "blob_bbox": props.bbox_area / image_total_area,
    "blob_euler_num": props.euler_number.item(),
    "blob_extent": props.extent,
    "blob_orientation": props.orientation,
    "blob_perimeter": props.perimeter, # perimeter is very difficult to normalize
    "blob_num_pixels": props.area.item() / image_total_area,
    "blob_max_intensity_r": props.max_intensity.tolist()[0],
    "blob_max_intensity_g": props.max_intensity.tolist()[1],
    "blob_max_intensity_b": props.max_intensity.tolist()[2],
    "blob_mean_intensity_r": props.mean_intensity.tolist()[0],
    "blob_mean_intensity_g": props.mean_intensity.tolist()[1],
    "blob_mean_intensity_b": props.mean_intensity.tolist()[2],
    "blob_min_intensity_r": props.min_intensity.tolist()[0],
    "blob_min_intensity_g": props.min_intensity.tolist()[1],
    "blob_min_intensity_b": props.min_intensity.tolist()[2],
    "blob_solidity": props.solidity,
    # To add new features to a set of data that you've already labeled,
    # just add them here and run update_features.py.
    # Some ideas for new features:
    # http://www.cyto.purdue.edu/cdroms/micro2/content/education/wirth10.pdf
  }

  return features, BlobDrawingAttributes(x, y, x0, y0, x2, y2, x3, y3, w, h)
