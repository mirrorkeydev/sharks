# Feature Extraction

## Pipeline:

1. Extract features + blobs with blank labels from images with `extract_features.py`. This generates a `data.json` and a `gameframes` directory.
2. Play the "labeling game" with `game.py`, passing in the `data.json` and `gameframes` from the last step. This generates a new `data.json` with all labels filled out.
3. Generate a `training_data.json` (ready to pass to a ML model) by running `update_features.py`.
4. Train a model. If you determine your blob data needs more features or needs to generate them slightly differently, you can edit the logic in `update_features.py`, and it will overwrite `data.json` and `training_data.json` for you, keeping the label + filename information.

## Main files:
- `[name]_data.json`:
  Used to generate new training data. Per-blob features (with names), including the source image of the blob, the number of the blob in the image, and the label of the blob.
- `[name]_training_data.json`:
  For feeding into machine learning packages. Per-blob features vectors (without names), the last number in each vector (array) is the label.
- `update_features.py`:
  "Refreshes" features for an already-labeled dataset. Will generate a new `data.json` and `training_data.json` upon running. To add new features: add generation code, add the result and feature name to the features object, and run script. It then packages the known label (from the old `data.json`) together with the new features to create a new set of training data.

## Helper files:
- `extract_features.py`:
  The original script I used to extract blob features from images and generated "game" slides with a square around the blob in question.
- `game.py`:
  The PySimpleGUI game used to assign labels to blobs (0 = not an event of interest, 1 = event of interest).
- `stats.py`:
  Generates neat histograms for `data.json`.
