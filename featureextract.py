import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Function to extract features from a file
def extract_features(file_path):
    file_size = os.path.getsize(file_path)
    return file_size

# Collecting data
ransomware_samples = r'G:\ransomware\ransomware_samples'  # List of file paths for ransomware files
benign_samples =  r'G:\ransomware\benign_samples'     # List of file paths for benign files

# Extracting features
X_ransomware = np.array([extract_features(file) for file in ransomware_samples])
X_benign = np.array([extract_features(file) for file in benign_samples])
X = np.vstack((X_ransomware, X_benign))

# Creating labels
y = np.hstack((np.ones(len(X_ransomware)), np.zeros(len(X_benign))))

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, 'random_forest_model.pkl')

# Evaluate the model
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Function to predict if a file is ransomware or benign
def predict_file(file_path):
    features = extract_features(file_path)
    loaded_model = joblib.load('random_forest_model.pkl')
    prediction = loaded_model.predict([features])
    return prediction

# Example usage
file_path = "G:\ransomware>"
prediction = predict_file(file_path)
if prediction == 1:
    print(f"The file {file_path} is ransomware.")
else:
    print(f"The file {file_path} is benign.")
