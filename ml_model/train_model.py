import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import RandomizedSearchCV, train_test_split

# import seaborn as sns
# import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

Path(__file__).parents[2]

DATA_PATH = "Crop_recommendation.csv"
df = pd.read_csv(DATA_PATH)


X = df.iloc[:, :-1]  # selecting all features except 'label' feature
y = df.iloc[:, -1]  # selecting 'label' feature as dependent feature


# Splitting dataset into train and test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=2
)


print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)


KNN_model = KNeighborsClassifier()
KNN_model.fit(X_train, y_train)

y_pred = KNN_model.predict(X_test)


# open a file, where you ant to store the data
file = open("KNN_model_crop_prediction_new.pkl", "wb")
# dump information to that file
pickle.dump(KNN_model, file)
