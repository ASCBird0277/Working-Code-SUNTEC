import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import fitz  # PyMuPDF

def select_directory():
    root = tk.Tk()
    root.withdraw()
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
    for file in os.listdir(directory):
        if file.startswith(prefix) and file.endswith(".pdf"):
            return file
    return None

def merge_pdfs(files_to_merge, output_file):
    doc = fitz.open()
    for pdf_file in files_to_merge:
        pdf = fitz.open(pdf_file)
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            doc.insert_pdf(pdf, from_page=page_num, to_page=page_num)
            # Add page label
            label = f"{os.path.basename(pdf_file)} - Page {page_num + 1}"
            inserted_page = doc[-1]  # Get the last page which was just added
            inserted_page.insert_text((72, 72), label, fontsize=10, color=(0, 0, 0))
    doc.save(output_file)
    doc.close()

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
    final_combined_pdf_path = os.path.join(directory, "final_combined_set.pdf")
    merge_pdfs(combined_pdfs, final_combined_pdf_path)
    print(f"All combined PDFs merged and saved as {final_combined_pdf_path}")

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
