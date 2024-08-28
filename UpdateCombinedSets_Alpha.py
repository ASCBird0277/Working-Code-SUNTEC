import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfMerger

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory()
    root.destroy()
    return directory_path

def find_and_merge_folders(directory, prefix):
    folders = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir.startswith(prefix):
                folders.append(os.path.join(root, dir))
    return folders

def find_file_with_prefix(directory, prefix):
    # Look for a file starting with the specified prefix in the directory
    for file in os.listdir(directory):
        if file.startswith(prefix) and file.endswith(".pdf"):
            return file
    return None

def merge_pdfs(files_to_merge, output_file):
    merger = PdfMerger()
    for pdf_file in files_to_merge:
        merger.append(pdf_file)
    with open(output_file, 'wb') as f:
        merger.write(f)
    merger.close()

def find_and_merge_pdfs(directory, prefix):
    subfolders = find_and_merge_folders(directory, prefix)
    combined_pdfs = []

    for subfolder in subfolders:
        pdf_files = [os.path.join(subfolder, file) for file in os.listdir(subfolder) if file.endswith(".pdf")]
        if pdf_files:
            temporary_combined_pdf_path = os.path.join(subfolder, f"temporary_{prefix}_combined.pdf")
            merge_pdfs(pdf_files, temporary_combined_pdf_path)
            matching_file = find_file_with_prefix(directory, prefix)
            if matching_file:
                new_file_path = os.path.join(directory, matching_file)
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)
                os.rename(temporary_combined_pdf_path, new_file_path)
                combined_pdfs.append(new_file_path)
            else:
                os.remove(temporary_combined_pdf_path)
    return combined_pdfs

def final_merge_and_replace(directory, combined_pdfs):
    asc_file = find_file_with_prefix(directory, "ASC -")
    if asc_file:
        final_path = os.path.join(directory, asc_file)
        merge_pdfs(combined_pdfs, final_path)
        print(f"All combined PDFs merged and replaced as {final_path}")
    else:
        print("No 'ASC -' file found for final replacement.")

def main():
    directory = select_directory()
    if directory:
        combined_a = find_and_merge_pdfs(directory, "A -")
        combined_s = find_and_merge_pdfs(directory, "S -")
        combined_c = find_and_merge_pdfs(directory, "C -")
        all_combined = combined_a + combined_s + combined_c
        final_merge_and_replace(directory, all_combined)
        messagebox.showinfo("Task Completed", "PDF processing completed.")
        print("Script execution completed.")

if __name__ == "__main__":
    main()
