import tkinter as tk
from tkinter import messagebox
import os
import sys

system_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'System'))
sys.path.append(system_path)

try:
    from version import __version__ 
except ImportError as e:
    raise ImportError(f"Failed to import __version__. Ensure 'System/version.py' exists and is accessible. Details: {e}")

def about_program():
    info = f"""ShellOS 
    Version: {__version__}
    Python 3.12.6
    Pip 24.2
    """
    messagebox.showinfo("About ShellOS", info)

def main():
    about_program()

if __name__ == "__main__":
    main()
