import tkinter as tk
from tkinter import filedialog
import os

# Create the Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select a folder using a system dialog
folder_path = filedialog.askdirectory(title="Select a folder")

if folder_path:
    # Get the list of file names from the selected directory
    file_names = os.listdir(folder_path)
    
    print(f"Processing folder: {folder_path}")

    # Rename files where the 5th character is 'G'
    for file_name in file_names:
        print(f"Checking file: {file_name}")
        if len(file_name) > 4 and file_name[4] == 'G':
            new_file_name = "_" + file_name
            original_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_file_name)
            try:
                os.rename(original_path, new_path)
                print(f"Renamed file: {file_name} -> {new_file_name}")
            except Exception as e:
                print(f"Error renaming file {file_name}: {e}")
else:
    print("No folder selected.")
