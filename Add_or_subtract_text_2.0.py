import os
import tkinter as tk
from tkinter import filedialog, simpledialog

def rename_files(folder_path, operation, position, text):
    # Get list of files in the specified folder
    files = os.listdir(folder_path)

    # Check if text ends with '*'
    if text.endswith('*'):
        symbol = text[:-1]
        remove_symbol = simpledialog.askstring("Input", f"Do you want to remove the symbol '{symbol}' as well? (yes/no)", initialvalue="no")
        remove_symbol = remove_symbol.lower() == 'yes'

    # Perform the specified operation on each file name
    for file_name in files:
        # Get the file extension
        file_name_parts = file_name.split('.')
        file_extension = ''
        if len(file_name_parts) > 1:
            file_extension = '.' + file_name_parts[-1]

        # Remove the file extension from the file name
        file_name_without_extension = '.'.join(file_name_parts[:-1])

        # Handle special case for removing everything after the symbol
        if text.endswith('*') and operation == 'subtract' and symbol in file_name_without_extension:
            symbol_index = file_name_without_extension.find(symbol)
            if remove_symbol:
                new_name = file_name_without_extension[:symbol_index]
            else:
                new_name = file_name_without_extension[:symbol_index + len(symbol)]
        else:
            # Perform the operation based on position
            if position == 'beginning':
                if operation == 'add':
                    new_name = text + file_name_without_extension
                elif operation == 'subtract':
                    if text == file_name_without_extension[:len(text)]:
                        new_name = file_name_without_extension[len(text):]
                    else:
                        new_name = file_name_without_extension
            elif position == 'end':
                if operation == 'add':
                    new_name = file_name_without_extension + text
                elif operation == 'subtract':
                    if text == file_name_without_extension[-len(text):]:
                        new_name = file_name_without_extension[:-len(text)]
                    else:
                        new_name = file_name_without_extension
            else:
                print("Invalid position. Please choose 'beginning' or 'end'.")
                return

        # Add the file extension back to the new name
        new_name += file_extension

        # Rename the file
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {file_name} to {new_name}")

def get_folder_path():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_rename():
    folder_path = folder_entry.get()
    operation = operation_var.get()
    position = position_var.get()
    text = text_entry.get()

    rename_files(folder_path, operation, position, text)

# Create main window
window = tk.Tk()
window.title("File Renamer")

# Folder path
folder_label = tk.Label(window, text="Folder Path:")
folder_label.pack()
folder_entry = tk.Entry(window, width=50)
folder_entry.pack()
browse_button = tk.Button(window, text="Browse", command=get_folder_path)
browse_button.pack()

# Operation
operation_label = tk.Label(window, text="Operation:")
operation_label.pack()
operation_var = tk.StringVar(window)
operation_var.set("add")
operation_option = tk.OptionMenu(window, operation_var, "add", "subtract")
operation_option.pack()

# Position
position_label = tk.Label(window, text="Position:")
position_label.pack()
position_var = tk.StringVar(window)
position_var.set("beginning")
position_option = tk.OptionMenu(window, position_var, "beginning", "end")
position_option.pack()

# Text
text_label = tk.Label(window, text="Text:")
text_label.pack()
text_entry = tk.Entry(window, width=50)
text_entry.pack()

# Start button
start_button = tk.Button(window, text="Start", command=start_rename)
start_button.pack()

# Run the main loop
window.mainloop()
