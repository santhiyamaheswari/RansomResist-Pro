import os

# Function to create files of different sizes
def create_files_with_different_sizes(directory):
    for i in range(5):
        file_path = os.path.join(directory, f'file_{i}.txt')
        # Create a file with random content
        with open(file_path, 'w') as f:
            f.write('a' * (i+1) * 1000)  # Multiply by 1000 to convert KB to bytes

# Create files with different sizes in ransomware_samples directory
create_files_with_different_sizes('ransomware_samples')
