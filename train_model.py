import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import math

# Function to extract features from a file
def extract_features(file_path):
    # Extract file size
    file_size = os.path.getsize(file_path)
    
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1]
    
    # Extract file modification time (in seconds since epoch)
    modification_time = os.path.getmtime(file_path)
    
    # Check if the file extension has changed
    original_extension = file_extension[1:] if file_extension else None
    new_extension = file_extension[1:] if file_extension else None
    extension_changed = 1 if original_extension != new_extension else 0
    
    # Check if the file has .encrypted extension
    is_encrypted = 1 if file_extension == '.encrypted' else 0
    
    # Calculate file entropy
    entropy = calculate_entropy(file_path)
    
    return [file_size, modification_time, extension_changed, is_encrypted, entropy]

# Function to calculate file entropy
def calculate_entropy(file_path):
    # Initialize variables
    entropy = 0
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        byte_freq = [0] * 256
        for byte in f.read():
            byte_freq[byte] += 1
    # Calculate entropy
    for freq in byte_freq:
        if freq != 0:
            p = freq / file_size
            entropy -= p * math.log2(p)
    return entropy

# Load the ransomware samples
ransomware_samples_dir = 'ransomware_samples'
ransomware_samples = [os.path.join(ransomware_samples_dir, file) for file in os.listdir(ransomware_samples_dir)]

# Load benign files
benign_samples_dir = 'benign_samples'  # Directory containing benign files
benign_samples = [os.path.join(benign_samples_dir, file) for file in os.listdir(benign_samples_dir)]

# Extract features for ransomware samples
X_ransomware = np.array([extract_features(file) for file in ransomware_samples])
y_ransomware = np.ones(len(X_ransomware))  # Labels for ransomware samples (1)

# Extract features for benign samples
X_benign = np.array([extract_features(file) for file in benign_samples])
y_benign = np.zeros(len(X_benign))  # Labels for benign samples (0)

# Combine ransomware and benign samples
X = np.vstack((X_ransomware, X_benign))
y = np.hstack((y_ransomware, y_benign))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
