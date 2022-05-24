# Ocean Life Visual Classifier

## Introduction 

The program our team has developed is designed to assist OSU’s Big Fish Lab in analyzing video taken from cameras attached to sharks. It can identify ~10 different forms of ocean events, some of which the lab finds interesting (e.g. fish, kelp), and some of which are identified as being something non-interesting (e.g. sunlight, noise).
The program has two main components: the graphical user interface (GUI), and the underlying machine learning model (classifier) that it interacts with. The program itself is provided as platform-specific executables (Windows), and comes bundled with all dependencies needed to run the program.

## Development

Development of the program requires:
- Python 3 (tested on 3.9) with packages:
  - scikit-image (0.19.1+ recommended)
  - numpy
  - openpyxl
  - ffmpeg-python
  - pysimplegui
  - sklearn
  - pandas
  - alive-progress
  - imageio-ffmpeg
  - seaborn
  - pyinstaller

Please refer to the handoff document for in-depth instructions on how to get the program running.
