import os
# Function to create files with different entropy
def create_files_with_different_entropy(directory):
    # Create a file with low entropy
    low_entropy_file = os.path.join(directory, 'low_entropy_file.txt')
    with open(low_entropy_file, 'wb') as f:  # Open the file in binary mode
        f.write(b'a' * 1000)  # Low entropy content

    # Create a file with high entropy
    high_entropy_file = os.path.join(directory, 'high_entropy_file.txt')
    with open(high_entropy_file, 'wb') as f:  # Open the file in binary mode
        f.write(os.urandom(1000))  # High entropy content

# Create files with different entropy in ransomware_samples directory
create_files_with_different_entropy('ransomware_samples')

