import tkinter as tk
from tkinter import filedialog
import os

# Create the Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a folder using a system dialog
folder_path = filedialog.askdirectory(title="Select a folder")
if not folder_path:
    print("No folder selected. Exiting script")

if folder_path:
    # Get the list of file names from the selected directory
    file_names = os.listdir(folder_path)

    # Rename files that have "G" as the 5th character by adding an underscore prefix
    for file_name in file_names:
        if len(file_name) >= 5 and file_name[4] == 'G':
            new_file_name = "_" + file_name
            original_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_file_name)
            os.rename(original_path, new_path)
            print(f"Renamed file: {file_name} -> {new_file_name}")
else:
    print("No folder selected.")
