# Function to encrypt a file (simple XOR encryption for demonstration purposes)
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())
    
    for i in range(len(data)):
        data[i] ^= key
        
    encrypted_file_path = os.path.join('ransomware_samples', os.path.basename(file_path) + '.encrypted')
    with open(encrypted_file_path, 'wb') as f:
        f.write(data)

# Encrypt all text files in a directory
def encrypt_files_in_directory(directory, key):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            encrypt_file(file_path, key)

# Encrypt files in the current directory
encrypt_files_in_directory('.', key)
