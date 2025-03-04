# -*- coding: utf-8 -*-
"""SVM NN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DjSDs2-AXtlXoqV6tdHFFqxqZWWPOm6h
"""

# Install necessary libraries
!pip install tensorflow scikit-learn pandas matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load Dataset
def read_datasets():
    genuine_users = pd.read_csv("/content/users.csv")
    fake_users = pd.read_csv("/content/fusers.csv")
    data = pd.concat([genuine_users, fake_users])
    labels = np.array([1] * len(genuine_users) + [0] * len(fake_users))  # 1 for genuine, 0 for fake
    return data, labels

# Feature Extraction
def extract_features(data):
    feature_columns = ['statuses_count', 'followers_count', 'friends_count',
                       'favourites_count', 'listed_count']
    return data[feature_columns]

# Load data
data, labels = read_datasets()
data = extract_features(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 1: Train SVM Model
svm_model = SVC(kernel='rbf', probability=True, random_state=42)
svm_model.fit(X_train, y_train)

# Get SVM Probability Scores as Features
X_train_svm = svm_model.predict_proba(X_train)  # Probabilities of being Fake/Genuine
X_test_svm = svm_model.predict_proba(X_test)

# Combine SVM Probabilities with Original Features for Neural Network
X_train_combined = np.hstack((X_train, X_train_svm))
X_test_combined = np.hstack((X_test, X_test_svm))

# Step 2: Train ANN Model
ann_model = Sequential([
    Dense(16, activation='relu', input_shape=(X_train_combined.shape[1],)),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')  # Binary Classification
])

# Compile ANN Model
ann_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train ANN
ann_model.fit(X_train_combined, y_train, epochs=20, batch_size=32, validation_split=0.2)

# Predict on Test Data
y_pred = (ann_model.predict(X_test_combined) > 0.5).astype(int)

# Evaluate Model
print("E_SVM-NN Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=['Fake', 'Genuine']))