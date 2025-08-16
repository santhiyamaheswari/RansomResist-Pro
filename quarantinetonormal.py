import os
import shutil

# Directory paths
quarantine_dir = 'quarantine'

# Get file paths
file_paths = [os.path.join(quarantine_dir, file) for file in os.listdir(quarantine_dir) if os.path.isfile(os.path.join(quarantine_dir, file))]

# Iterate through each file and move it back to the original location
for file_path in file_paths:
    new_location = os.path.join(os.getcwd(), os.path.basename(file_path))
    shutil.move(file_path, new_location)
    print(f"File {os.path.basename(file_path)} moved to {new_location}")
