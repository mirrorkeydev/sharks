# Feature Extraction

## Pipeline:

Run the scripts listed in the following steps in order to go from a set of csv/video pairs to a set of training data that can be passed to a model.

Important: At the top of each file is a comment explaining which files need to exist and which variables need to be set in order for the scripts to work correctly.

1. `1_extract_video_frames.py`: Extract frames from the csv/video pairs described in `deployments_data`. You may want to edit the logic in `main()` to only extract frames containing kelp, frames containing any event, frames containing fish, etc.
2. `2_extract_features.py`: Extract features + blobs with blank labels from images. This generates an unlabeled `data.json` and a `gameframes` directory.
3. `3_game.py`: Play the "labeling game", passing in the unlabeled `data.json` and `gameframes` from the last step. This generates a new labeled `data.json`. Before you move onto the next step, commit this `data.json` or save a copy of it in some form, just in case. If you lose this file by overwriting it (for example, if you run `update_features.py` later and the blob generation isn't correct), it will be costly to replace.
4. `4_generate_training_data.py`: Generate a `training_data.json` (ready to pass to a ML model). Train a model with this `training_data.json`.
5. `5_update_features.py`: If you determine your blob data needs more features or needs to generate the features slightly differently, you can edit the logic in `blob_extraction.py` and then run `5_update_features.py`, and it will generate a new `data.json` for you using the old one, keeping the label + filename information. If you need this data in training data form, run step 4 again on the new file.

## Helper files:
- `blob_extraction.py`:
  Module that contains all of the blob extraction logic.
- `deployments_data.py`:
  Module that contains metadata linking CSVs to videos, as well as extra information e.g. whether the video is flipped or not.
