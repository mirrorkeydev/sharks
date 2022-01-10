# Feature Extraction

- `data.json`: Per-blob features, including the source image of the blob, the number of the blob in the image, and the label of the blob.
- `extract_features.py`: The original script I used to extract blob features from images and generated "game" slides with a square around the blob in question.
- `game.py`. The PySimpleGUI game used to assign labels to blobs (0 = not an event of interest, 1 = event of interest).
- `stats.py`: Generates neat histograms for `data.json`.
- `training_data_with_labels.json`: Deprecated, use `data.json` instead.
- `update_features.py`: The new feature extraction script, will generate a new `data.json` upon running. To add new features: add generation code, add the result and feature name to the features object, and run script. It then packages the known label (from the old `data.json`) together with the new features to create a new set of training data.
