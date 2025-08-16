import os

# Function to change modification time of a file
def change_file_modification_time(file_path):
    # Set the modification time to 0 (Unix epoch)
    os.utime(file_path, (0, 0))

# Change modification time of a file in ransomware_samples directory
change_file_modification_time('ransomware_samples/source_file.txt')
