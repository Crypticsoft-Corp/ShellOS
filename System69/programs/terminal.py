import tkinter as tk
from tkinter import scrolledtext
import os
import platform
import subprocess
import sys

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal")

        # Set the icon for the title bar
        icon_path = self.resolve_path("ShellOS/System69/resources/icons/terminal.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"Warning: Icon file not found at {icon_path}")

        # Create a scrolled text widget to simulate terminal
        self.terminal = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="white", insertbackground="white", font=("Consolas", 12))
        self.terminal.pack(expand=True, fill=tk.BOTH)

        # Bind the Enter key to process commands
        self.terminal.bind("<Return>", self.process_command)

        # Add a prompt with the device name
        device_name = platform.node()  # Get the device name
        self.prompt = f"ShellOS>"
        self.terminal.insert(tk.END, self.prompt)
        self.terminal.mark_set("insert", tk.END)

        # Dictionary of command locations (update this to add new commands)
        self.command_locations = {
            "Help": self.resolve_path("ShellOS/System69/Cmdlets/help.py"),
            "Notepad": self.resolve_path("ShellOS/System69/Programs/Notepad.py"),
            "Sysfetch": self.resolve_path("ShellOS/System69/Programs/Sysfetch.py"),
            "About": self.resolve_path("ShellOS/System69/Programs/About.py"),
            "Calc": self.resolve_path("ShellOS/System69/Programs/Calc.py"),
            "echo": self.resolve_path("ShellOS/System69/Cmdlets/echo.py"),
            "listdir": self.resolve_path("ShellOS/System69/Cmdlets/listdir.py"),
            "shlzip": self.resolve_path("ShellOS/System69/programs/shlzip.py"),
        }

    def resolve_path(self, relative_path):
        """Convert a relative path (starting from 'ShellOS') to an absolute path."""
        current_dir = os.path.abspath(os.getcwd())  # Get the current working directory
        shellos_index = current_dir.find("ShellOS")

        if shellos_index == -1:
            print("Error: 'ShellOS' directory not found in path.")
            return relative_path  # Fallback to relative path

        shellos_root = current_dir[:shellos_index] + "ShellOS"
        return os.path.join(shellos_root, *relative_path.split("/")[1:])  # Append the subdirectory

    def process_command(self, event):
        # Get the current line
        line_start = self.terminal.index("insert linestart")
        line_end = self.terminal.index("insert lineend")
        line_text = self.terminal.get(line_start, line_end).strip()

        # Remove the prompt from the input to isolate the command
        if line_text.startswith(self.prompt):
            command_text = line_text[len(self.prompt):].strip()
        else:
            command_text = line_text.strip()

        # Insert a new line
        self.terminal.insert(tk.END, "\n")

        # Split the command and arguments
        parts = command_text.split()
        command = parts[0] if parts else ""
        args = parts[1:]

        # Run the external command if found
        if command in self.command_locations:
            self.run_file(self.command_locations[command], args)
        else:
            self.terminal.insert(tk.END, f"Command not found: {command}\n")

        # Add a new prompt
        self.terminal.insert(tk.END, self.prompt)
        self.terminal.mark_set("insert", tk.END)
        self.terminal.see(tk.END)

        # Prevent default newline behavior
        return "break"

    def run_file(self, file_path, args):
        if not os.path.isfile(file_path):
            self.terminal.insert(tk.END, f"Error: File '{file_path}' not found.\n")
            return

        try:
            if file_path.endswith(".py"):
                result = subprocess.run(["python", file_path, *args], capture_output=True, text=True)
            elif file_path.endswith(".bat"):
                result = subprocess.run([file_path, *args], capture_output=True, text=True, shell=True)
            elif file_path.endswith(".sh"):
                result = subprocess.run(["bash", file_path, *args], capture_output=True, text=True)
            else:
                self.terminal.insert(tk.END, "Error: Unsupported file type.\n")
                return

            self.terminal.insert(tk.END, result.stdout)
            if result.stderr:
                self.terminal.insert(tk.END, result.stderr)
        except Exception as e:
            self.terminal.insert(tk.END, f"Error: {str(e)}\n")


root = tk.Tk()
app = TerminalApp(root)
root.geometry("1020x642")
root.mainloop()
