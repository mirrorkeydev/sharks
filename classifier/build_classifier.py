# =============================================== #
#
# build and export rf classifier
# input:  training data
# output: serialized model
#
# =============================================== #

import json
import numpy as np
import pickle
from pathlib import Path
from sklearn.ensemble        import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score

# parameters
trees = 100
k     = 10
data_file  = "./training_data.json"
model_file = "./trained_model.json"

# load data from json file
data_list = json.loads(Path(data_file).read_text())

# capture data as numpy array
data          = np.array(data_list)
data_points   = len(data)
feature_count = len(data[0])-1

# split data into features and labels
features = np.delete(data, feature_count, axis = 1)
labels   = data[:, feature_count]
print("Loaded", data_points, "labeled data points with", feature_count, "features.")

# build and train rf model
rf = RandomForestClassifier(n_estimators = trees)
rf.fit(features, labels)
print("Trained random forest with", trees, "trees.\n")

# perform cross validation
print("Performing", k, "fold cross validation.")
scores = cross_val_score(rf, features, labels, scoring = 'accuracy', cv = KFold(n_splits = k, random_state = 1, shuffle = True))
print("Cross validation accuracy: ", np.mean(scores), "\n")

# dump the pickles
pickle.dump(rf, open(model_file, "wb"))
