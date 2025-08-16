import os
import joblib
import numpy as np
from plyer import notification

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
            entropy -= p * np.log2(p)
    return entropy

# Function to classify a file
def classify_file(file_path):
    features = extract_features(file_path)
    prediction = loaded_model.predict([features])
    if prediction == 1:
        print(f"The file {file_path} is ransomware.")
        # Take actions for ransom files
        notify_administrator(file_path)
    else:
        print(f"The file {file_path} is benign.")

# Function to notify the system administrator via system notification
def notify_administrator(file_path):
    # System notification content
    title = "Ransomware Alert"
    message = f"The file {file_path} has been detected as ransomware. Please take appropriate action."
    
    # Send system notification
    try:
        notification.notify(
            title=title,
            message=message,
            app_name='Ransomware Detector',
            timeout=10
        )
        print("System notification sent to the system administrator.")
    except Exception as e:
        print(f"Failed to send system notification. Error: {e}")

# Load the trained model
loaded_model = joblib.load('random_forest_model.pkl')

# Directory paths
ransom_samples_dir = 'ransomware_samples'
benign_samples_dir = 'benign_samples'

# Get file paths for ransom samples
ransom_samples = [os.path.join(ransom_samples_dir, file) for file in os.listdir(ransom_samples_dir)]

# Get file paths for benign samples
benign_samples = [os.path.join(benign_samples_dir, file) for file in os.listdir(benign_samples_dir)]

# List of all file paths
all_samples = ransom_samples + benign_samples

# Iterate through each file and classify
for file_path in all_samples:
    classify_file(file_path)
