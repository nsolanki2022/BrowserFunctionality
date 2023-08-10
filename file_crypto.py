#!/usr/bin/env python3
"""
File Encryption and Decryption Script

This script provides a command-line interface to encrypt and decrypt files using a passphrase.
It uses the my_crypto module for encryption and decryption operations.

Usage:
    python script_name.py <filename> <passphrase> [-e] [-d]

Arguments:
    filename (str): Name of the file to be processed.
    passphrase (str): Passphrase used for encryption or decryption.

Options:
    -e, --encrypt: Encrypt the file.
    -d, --decrypt: Decrypt the file.
"""

import argparse
import my_crypto


def encrypt_file(filepath, passphrase):
    """
    Encrypts the file at the given filepath using the provided passphrase.

    Args:
        filepath (str): Path to the file to be encrypted.
        passphrase (bytes): Passphrase used for encryption.
    """
    encryptor = my_crypto.FileEncryptor(passphrase)
    encryptor.encrypt_and_overwrite(filepath)


def decrypt_file(filepath, passphrase):
    """
    Decrypts the file at the given filepath using the provided passphrase.

    Args:
        filepath (str): Path to the file to be decrypted.
        passphrase (bytes): Passphrase used for decryption.
    """
    decryptor = my_crypto.FileEncryptor(passphrase)
    decryptor.decrypt_and_overwrite(filepath)


def main():
    """
    Command-line interface for file encryption and decryption.
    """
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file.")
    parser.add_argument('filename', help="Name of the file to process")
    parser.add_argument('passphrase', help="Passphrase for encryption or decryption")
    parser.add_argument('-e', action='store_true', help="Encrypt the file")
    parser.add_argument('-d', action='store_true', help="Decrypt the file")

    args = parser.parse_args()

    # Convert passphrase to bytes
    passphrase = args.passphrase.encode()

    if args.e:
        encrypt_file(args.filename, passphrase)
        print("File encrypted successfully.")
    elif args.d:
        decrypt_file(args.filename, passphrase)
        print("File decrypted successfully.")
    else:
        print("Please specify either encryption or decryption.")


if __name__ == "__main__":
    main()
