import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import subprocess
import datetime

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    print(f"Folder selected: {folder_path}")
    return folder_path

def find_folder_with_prefix(base_path, prefix):
    print(f"Searching for folders starting with '{prefix}' in '{base_path}'")
    prefix_lower = prefix.lower()
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.lower().startswith(prefix_lower):
                found_folder = os.path.join(root, dir_name)
                print(f"Found folder: {found_folder}")
                return found_folder
    print("No folder found with the given prefix.")
    return None

def find_next_folder_version(folder_name):
    match = re.search(r"thru(?:ugh)? (\d+\.\d+)", folder_name, re.IGNORECASE)
    if match:
        current_version = float(match.group(1))
        next_version = current_version + 0.01
        return "{:.2f}".format(next_version)
    return None

def combine_pdfs(directory, output_filename):
    print(f"Combining PDF files from {directory} into {output_filename}")
    pdf_writer = PyPDF2.PdfWriter()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)
    print(f"PDF files combined into {output_filename}")

def cleanup_workspace(directory, exclude_file):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item_path != exclude_file:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

def handle_existing_workspace(workspace_folder):
    print(f"Handling existing workspace at {workspace_folder}")
    action = messagebox.askquestion("Workspace exists",
                                    "The '_DC WORKSPACE' directory already exists. Do you want to overwrite it?")
    if action == 'yes':
        shutil.rmtree(workspace_folder)
    os.makedirs(workspace_folder, exist_ok=True)
    return workspace_folder

def open_excel_file(excel_file):
    print(f"Opening Excel file: {excel_file}")
    try:
        os.startfile(excel_file)
    except AttributeError:
        subprocess.call(['open', excel_file])
    except Exception as e:
        print(f"Error opening Excel file: {e}")

def copy_contents_to_workspace(source_folder, workspace_folder):
    if not os.path.exists(workspace_folder):
        os.makedirs(workspace_folder)
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(workspace_folder, item)
        if os.path.isdir(source_path) and source_path != workspace_folder:
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        elif os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)

def main():
    base_folder = select_folder()
    if not base_folder:
        print("No base folder selected. Exiting.")
        return

    folder_4_00 = find_folder_with_prefix(base_folder, "4.00_")
    if not folder_4_00:
        print("No folder starting with '4.00_' found.")
        return

    excel_file_found = False
    for file in os.listdir(folder_4_00):
        if file.lower().endswith(".xlsx"):
            excel_file = os.path.join(folder_4_00, file)
            open_excel_file(excel_file)
            excel_file_found = True
            break

    if not excel_file_found:
        print("No Excel file found in the folder.")
        return

    next_version = find_next_folder_version(folder_4_00)
    if not next_version:
        print("No valid version number found in folder name to increment.")
        return

    next_folder_prefix = next_version
    next_folder = find_folder_with_prefix(base_folder, next_folder_prefix)
    if not next_folder:
        print(f"No folder found for version {next_folder_prefix}")
        return

    print(f"Next folder: {next_folder}")
    workspace_folder = os.path.join(next_folder, "_DC WORKSPACE")
    if os.path.exists(workspace_folder):
        workspace_folder = handle_existing_workspace(workspace_folder)
    else:
        os.makedirs(workspace_folder)

    copy_contents_to_workspace(next_folder, workspace_folder)

    combined_pdf_name = f" {next_version}.pdf"
    combined_pdf_path = os.path.join(workspace_folder, combined_pdf_name)
    combine_pdfs(workspace_folder, combined_pdf_path)

    cleanup_workspace(workspace_folder, combined_pdf_path)

    os.startfile(combined_pdf_path)

if __name__ == "__main__":
    main()
