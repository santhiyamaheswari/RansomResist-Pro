import os
import shutil

# Function to create .encrypted files
def create_encrypted_files(directory):
    source_file = 'source_file.txt'  # Name of the source file
    encrypted_file = os.path.join(directory, 'encrypted_file.txt.encrypted')
    shutil.copy(source_file, encrypted_file)

# Create .encrypted files in ransomware_samples directory
create_encrypted_files('ransomware_samples')
