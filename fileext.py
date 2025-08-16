import shutil
import os

# Function to create files with extension changes
def create_files_with_extension_changes(directory):
    source_file = 'source_file.txt'  # Name of the source file
    dest_file = os.path.join(directory, 'file_with_extension_change.docx')
    shutil.copy(source_file, dest_file)

# Create files with extension changes in ransomware_samples directory
create_files_with_extension_changes('ransomware_samples')
