import tkinter as tk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
import os
import sys

# Determine the correct path to system version module
system_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SYSTEM'))
sys.path.append(system_path)

try:
    from version import __version__ 
except ImportError as e:
    raise ImportError(f"Failed to import __version__. Ensure 'SYSTEM/version.py' exists and is accessible. Details: {e}")

def about_program():
    # Create the about window
    about_win = Toplevel()
    about_win.title("About ShellOS")
    about_win.geometry("400x300")
    about_win.resizable(False, False)

    # Load and display the ShellOS logo
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'System69', 'resources', 'images', 'shellosverlogo.png'))
    if os.path.exists(logo_path):
        img = Image.open(logo_path)

        # Calculate the new size based on the original aspect ratio (15.12:4.25)
        original_width, original_height = img.size
        aspect_ratio = 15.12 / 4.25
        new_width = 150
        new_height = int(new_width / aspect_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)  # Resize image with high-quality resampling
        img = ImageTk.PhotoImage(img)
        logo_label = Label(about_win, image=img)
        logo_label.image = img  # Keep a reference
        logo_label.pack(pady=10)
    else:
        error_label = Label(about_win, text="Image not found!", font=("Arial", 12), fg="red")
        error_label.pack(pady=10)
    
    # Display version information
    info_text = f"""
ShellOS
Version: {__version__}
Python 3.12.6
Pip 24.2
"""
    info_label = Label(about_win, text=info_text, font=("Arial", 12), justify="center")
    info_label.pack(pady=10)

    about_win.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    about_program()

if __name__ == "__main__":
    main()
