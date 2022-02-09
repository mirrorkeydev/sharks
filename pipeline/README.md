# Feature Extraction

## Pipeline:

1. Extract features + blobs with blank labels from images with `extract_features.py`. This generates an unlabeled `data.json` and a `gameframes` directory.
2. Play the "labeling game" with `game.py`, passing in the unlabeled `data.json` and `gameframes` from the last step. This generates a new labeled `data.json`. Before you move onto the next step, commit this `data.json` or save a copy of it in some form, just in case. If you lose this file by overwriting it (for example, if you run `update_features.py` later and the blob generation isn't correct), it will be costly to replace.
3. Generate a `training_data.json` (ready to pass to a ML model) by running `generate_training_data.py`.
4. Train a model with `training_data.json`.
5. If you determine your blob data needs more features or needs to generate the features slightly differently, you can edit the logic in `blob_extraction.py` and then run `update_features.py`, and it will generate a new `data.json` for you using the old one, keeping the label + filename information. If you need this data in training data form, run step 3 again on the new file.

## Main files:
- `classifier_data.json`:
  Used to generate new training data. Per-blob features (with names), including the source image of the blob, the number of the blob in the image, and the label of the blob (which is potentially unknown (`None`) or skipped due to being unclear (`999`)).
- `classifier_training_data.json`:
  For feeding into machine learning packages. Per-blob features vectors (without names), the last number in each vector (array) is the label.
- `update_features.py`:
  "Refreshes" features for an already-labeled dataset. Will generate a new `data.json` upon running. To add new features: add generation code, add the result and feature name to the features object, and run script. It then packages the known label (from the old `data.json`) together with the new features to create a new set of data.
- `generate_training_data.py`:
  Takes a `data.json` (which has multiple descriptors of the data in the file) and creates a `training_data.json` for ML model consumption (all numbers, no descriptors in the file). 

## Helper files:
- `extract_features.py`:
  The original script I used to extract blob features from images and generated "game" slides with a square around the blob in question.
- `game.py`:
  The PySimpleGUI game used to assign labels to blobs (0 = not an event of interest, 1 = event of interest).
- `stats.py`:
  Generates neat histograms for `data.json`.
