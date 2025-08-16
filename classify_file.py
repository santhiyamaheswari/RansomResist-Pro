# Function to classify a file
def classify_file(file_path):
    features = extract_features(file_path)
    prediction = loaded_model.predict([features])
    if prediction == 1:
        print(f"The file {file_path} is ransomware.")
    else:
        print(f"The file {file_path} is benign.")
