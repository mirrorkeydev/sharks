# Feature Extraction

## Main files:
- `data.json`:
  Used to generate new training data. Per-blob features (with names), including the source image of the blob, the number of the blob in the image, and the label of the blob.
- `training_data.json`:
  For feeding into machine learning packages. Per-blob features vectors (without names), the last number in each vector (array) is the label.
- `update_features.py`:
  The new feature extraction script, will generate a new `data.json` and `training_data.json` upon running. To add new features: add generation code, add the result and feature name to the features object, and run script. It then packages the known label (from the old `data.json`) together with the new features to create a new set of training data.

## Helper files:
- `extract_features.py`:
  The original script I used to extract blob features from images and generated "game" slides with a square around the blob in question.
- `game.py`:
  The PySimpleGUI game used to assign labels to blobs (0 = not an event of interest, 1 = event of interest).
- `stats.py`:
  Generates neat histograms for `data.json`.
