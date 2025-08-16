import random
import string
import os

# Function to generate random text
def generate_random_text(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to create synthetic benign files
def create_benign_files(directory, num_files, file_size):
    for i in range(num_files):
        file_name = f'benign_file_{i}.txt'
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            f.write(generate_random_text(file_size))

# Create 100 synthetic benign text files with 1000 characters each
create_benign_files('benign_samples', 100, 1000)
