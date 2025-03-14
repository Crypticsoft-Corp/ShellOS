import os

script_dir = os.path.dirname(os.path.abspath(__file__))

GUI = os.path.join(script_dir, "Graphical_Shell/GraphicalShell.py")

# Check if the ShellOS script exists
if os.path.exists(GUI):
    os.system(f'python "{GUI}"')
else:
    print(f"Error: {GUI} not found.")
