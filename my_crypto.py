#!/usr/bin/env python3

"""
File Encryption Utility

This script defines a FileEncryptor class that provides methods for encrypting 
and decrypting files using the cryptography
library.

Usage:
    python script_name.py

Make sure to replace 'script_name.py' with the actual name of this script.

Example:
    python script_name.py

Note: Before using this script, you need to install the cryptography library 
using 'pip install cryptography'.
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class FileEncryptor:
    """
    Encrypts and decrypts files using the cryptography library.
    """

    def __init__(self, encryption_key):
        """
        Initializes the FileEncryptor with the provided encryption key.

        Args:
            encryption_key (bytes): The encryption key used for Fernet.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=b'salt',
            length=32
        )
        encryption_key = kdf.derive(encryption_key)
        encryption_key = base64.urlsafe_b64encode(encryption_key)
        self.fernet = Fernet(encryption_key)

    def encrypt_data(self, text):
        """
        Encrypts a text using the fernet encryption key.

        Args:
            text (bytes): The text to be encrypted.

        Returns:
            bytes: The encrypted text.
        """
        encrypted_string = self.fernet.encrypt(text)
        return encrypted_string

    def decrypt_data(self, text):
        """
        Decrypts an encrypted text using the fernet encryption key.

        Args:
            text (bytes): The encrypted text to be decrypted.

        Returns:
            bytes: The decrypted text.
        """
        decrypted_string = self.fernet.decrypt(text)
        return decrypted_string

    def encrypt_file(self, input_file_path, output_file_path):
        """
        Encrypts a file using the fernet encryption key.

        Args:
            input_file_path (str): Path to the input file.
            output_file_path (str): Path to save the encrypted file.
        """
        with open(input_file_path, 'rb') as input_file:
            data = input_file.read()
            encrypted_data = self.fernet.encrypt(data)

        with open(output_file_path, 'wb') as output_file:
            output_file.write(encrypted_data)

    def decrypt_file(self, input_file_path, output_file_path):
        """
        Decrypts an encrypted file using the fernet encryption key.

        Args:
            input_file_path (str): Path to the input encrypted file.
            output_file_path (str): Path to save the decrypted file.
        """
        with open(input_file_path, 'rb') as input_file:
            encrypted_data = input_file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)

        with open(output_file_path, 'wb') as output_file:
            output_file.write(decrypted_data)

    def encrypt_and_overwrite(self, file_path):
        """
        Encrypts a file in-place, overwriting the original content.

        Args:
            file_path (str): Path to the file to be encrypted and overwritten.
        """
        with open(file_path, 'rb') as input_file:
            data = input_file.read()
            encrypted_data = self.fernet.encrypt(data)
        
        with open(file_path, 'wb') as output_file:
            output_file.write(encrypted_data)

    def decrypt_and_overwrite(self, file_path):
        """
        Decrypts an encrypted file in-place, overwriting the original content.

        Args:
            file_path (str): Path to the file to be decrypted and overwritten.
        """
        with open(file_path, 'rb') as input_file:
            encrypted_data = input_file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)

        with open(file_path, 'wb') as output_file:
            output_file.write(decrypted_data)

# Usage example
if __name__ == "__main__":
    passphrase = b'test'

    # Create an instance of FileEncryptor with the provided passphrase
    encryptor = FileEncryptor(passphrase)

    file_path = 'test.txt'  # Replace with the path to your file

    # Encrypt and overwrite the same file
    encryptor.encrypt_and_overwrite(file_path)
    print(f"File '{file_path}' encrypted and overwritten")

    # Decrypt and overwrite the same file
    encryptor.decrypt_and_overwrite(file_path)
    print(f"File '{file_path}' decrypted and overwritten")

    encrypted_file_path = 'encrypted_file.txt'
    decrypted_file_path = 'decrypted_file.txt'

    input_file_path = file_path
    # Encrypt file
    encryptor.encrypt_file(input_file_path, encrypted_file_path)
    print(f"File '{input_file_path}' encrypted and saved as '{encrypted_file_path}'")

    # Decrypt file
    encryptor.decrypt_file(encrypted_file_path, decrypted_file_path)
    print(f"File '{encrypted_file_path}' decrypted and saved as '{decrypted_file_path}'")
