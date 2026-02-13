import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Function to generate a random 256-bit AES key
def generate_key():
    key = os.urandom(32)  # 256 bits = 32 bytes
    print(f"Generated AES-256 Key: {key.hex()}")  # Debug: print the key
    return key

# Function to encrypt a file using AES-256
def encrypt_file(file_path: str, key: bytes):
    print(f"Encrypting file: {file_path}")  # Debug: print file being encrypted
    # Open the file in binary read mode ('rb')
    with open(file_path, 'rb') as file:
        data = file.read()  # Read the content of the file
    
    # Generate a random IV (16 bytes)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the data to ensure it's a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Return IV + encrypted data to store together
    return iv + encrypted_data

# Function to decrypt a file using AES-256
def decrypt_file(file_path: str, key: bytes):
    print(f"Decrypting file: {file_path}")  # Debug: print file being decrypted
    # Open the encrypted file in binary read mode ('rb')
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()  # Read the encrypted data
    
    # Extract the IV (first 16 bytes) and the encrypted content (remaining bytes)
    iv = encrypted_data[:16]
    encrypted_content = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_content) + decryptor.finalize()

    # Unpad the decrypted data using the same padding scheme as encryption
    unpadder = padding.PKCS7(128).unpadder()
    original_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return original_data

# Main function to manage the flow
def main():
    print("Welcome to the AES-256 Encryption/Decryption Program")  # Debug: start message
    action = input("Choose an action - (1) Encrypt File (2) Decrypt File: ").strip()

    if action == '1':
        print("Starting Encryption Process...")  # Debug: print encryption start
        # Generate the AES-256 key
        key = generate_key()
        
        # Specify the file to encrypt
        file_path = input("Enter the file path to encrypt: ")
        print(f"File to encrypt: {file_path}")  # Debug: print the file path entered
        
        # Encrypt the file
        encrypted_data = encrypt_file(file_path, key)
        
        # Write the encrypted file to disk (with .enc extension)
        with open(file_path + '.enc', 'wb') as enc_file:
            enc_file.write(encrypted_data)
        
        print(f"Encrypted file saved as {file_path}.enc")
    
    elif action == '2':
        print("Starting Decryption Process...")  # Debug: print decryption start
        # Enter the AES-256 key manually (in hexadecimal format)
        key_hex = input("Enter the AES-256 key in hexadecimal format: ")
        key = bytes.fromhex(key_hex)

        # Specify the file to decrypt
        file_path = input("Enter the file path to decrypt: ")
        
        # Decrypt the file
        try:
            decrypted_data = decrypt_file(file_path, key)
            # Save the decrypted data as a new file (with .dec extension)
            with open(file_path + '.dec', 'wb') as dec_file:
                dec_file.write(decrypted_data)
            
            print(f"Decrypted file saved as {file_path}.dec")
        except ValueError as e:
            print(f"Decryption failed: {e}")

if __name__ == "__main__":
    main()
