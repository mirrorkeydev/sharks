from random import Random
import numpy as np                  #linear algebra
import matplotlib.pyplot as plt     #data visuals
import seaborn as sns               #statistics visuals
import json                         #data processing, json
import pickle
from pathlib import Path
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score, train_test_split, permutation_test_score
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Random Forest Model Variables
trees = 100
k = 10
ratio = 0.3

# Training Data
training_file = 'training.json'
trained_file = 'trained.json'

# Test Data
feature_titles = ["X Position", "Y Position", "Bounding Box Width", "Bounding Box Height", "Bounding Box Area", "Connectivity", "Object Area / Bounding Box Area", "Orientation", "Object Perimeter", "Object Area", "Max Intensity (R)", "Max Intensity (G)", "Max Intensity (B)", "Mean Intensity (R)", "Mean Intensity (G)", "Mean Intensity (B)", "Min Intensity (R)", "Min Intensity (G)", "Min Intensity (B)", "Solidity"]

# Load json data
data = json.loads(Path(training_file).read_text())  # Use the training data for now

data_array = np.array(data)         # Convert to Array
data_points = len(data)             # Capture data points as each bracket
feature_count = len(data[0]) - 1    # Find ammount of features in each bracket

# Split the data
features = np.delete(data_array, feature_count, axis = 1)
labels = data_array[:, feature_count]
#print("Loaded", data_points, " labeled data points with ", feature_count, " features.")

# Build the Random Forest Model
rf = RandomForestClassifier(n_estimators= trees)

# Split data and train
x_train, x_test, y_train, y_test, = train_test_split(features, labels, test_size = ratio)
rf.fit(x_train, y_train)

# Predictions
p = rf.predict(x_test)

# Confusion Matrix and Classifier Report
cm = confusion_matrix(y_test, p)
print("Confusion Matrix: \n\n", cm)
print("Classification Report: \n\n", classification_report(y_test, p))

# Train model on all data
rf.fit(features, labels)

# Create Figure Feature hierarchy
feature_hierarchy = permutation_importance(rf, x_test, y_test).importances_mean

# Bar Chart
fig, ax = plt.subplots()
ax.barh(np.arange(len(feature_hierarchy)), feature_hierarchy, color = ['midnightblue', 'navy', 'darkblue', 'mediumblue', 'blue', 'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'blueviolet', 'indigo', 'darkorchid', 'darkviolet', 'mediumorchid', 'violet', 'purple', 'darkmagenta', 'fuchsia', 'magenta' ]) # Calculates how many features there are
ax.set_title("Feature Graph")
ax.set_yticks(range(feature_count))
ax.set_yticklabels(feature_titles)
fig.tight_layout()
ax.set_xlabel("Accuracy")     # Expresses how much accuracy the model loses by excluding these variables
ax.set_ylabel("Features")
plt.show()
