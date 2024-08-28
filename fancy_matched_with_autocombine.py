import os
import shutil
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyPDF2 import PdfReader, PdfWriter, errors

def select_directories(search_directory):
    job_folder = QFileDialog.getExistingDirectory(None, "Select job folder", search_directory)
    selected_directory_list = []
    
    if job_folder:
        for folder_name in os.listdir(job_folder):
            folder_path = os.path.join(job_folder, folder_name)
            if os.path.isdir(folder_path) and (folder_name.startswith("A -") or folder_name.startswith("C -") or folder_name.startswith("S -")):
                selected_directory_list.append(folder_path)
    return selected_directory_list

def combine_files(source_dir, output_filename):
    global errors_found
    errors_found = False
    pdf_writer = PdfWriter()

    for file in os.listdir(source_dir):
        if file.endswith('.pdf'):
            file_path = os.path.join(source_dir, file)
            try:
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            except errors.EmptyFileError:
                print(f"The file {file_path} is empty or corrupted!")
                errors_found = True

    with open(output_filename, 'wb') as output_file:
        pdf_writer.write(output_file)

def main():
    app = QApplication([])
    global errors_found
    errors_found = False

    folders_to_clear = ["Current", "Revision", "matched_Current", "matched_Revision"]
    for folder_name in folders_to_clear:
        folder_path = os.path.join(os.getcwd(), folder_name)
        shutil.rmtree(folder_path, ignore_errors=True)
        os.makedirs(folder_path, exist_ok=True)

    current_dirs = select_directories('/')
    if not current_dirs:
        print("No job directory selected. Exiting.")
        return

    revision_dir = QFileDialog.getExistingDirectory(None, 'Select Revision Directory')
    if not revision_dir:
        print("No revision directory selected. Exiting.")
        return

    current_files = [os.path.join(current_dir, file) for current_dir in current_dirs for file in os.listdir(current_dir) if file.endswith('.pdf')]
    revision_files = [os.path.join(revision_dir, file) for file in os.listdir(revision_dir) if file.endswith('.pdf')]

    matched_Current_dir = os.path.join(os.getcwd(), 'matched_Current')
    matched_Revision_dir = os.path.join(os.getcwd(), 'matched_Revision')
    os.makedirs(matched_Current_dir, exist_ok=True)
    os.makedirs(matched_Revision_dir, exist_ok=True)

    matches_found = False
    for current_file in current_files:
        base_name = os.path.splitext(os.path.basename(current_file))[0]
        if base_name in (os.path.splitext(os.path.basename(file))[0] for file in revision_files):
            shutil.copy(current_file, os.path.join(matched_Current_dir, os.path.basename(current_file)))
            matches_found = True

    for revision_file in revision_files:
        base_name = os.path.splitext(os.path.basename(revision_file))[0]
        if base_name in (os.path.splitext(os.path.basename(file))[0] for file in current_files):
            shutil.copy(revision_file, os.path.join(matched_Revision_dir, os.path.basename(revision_file)))
            matches_found = True

    if matches_found:
        output_filename_current = os.path.join(matched_Current_dir, f'Combined_Current.pdf')
        output_filename_revision = os.path.join(matched_Revision_dir, f'Combined_Revision.pdf')
        combine_files(matched_Current_dir, output_filename_current)
        combine_files(matched_Revision_dir, output_filename_revision)
        os.startfile(output_filename_revision)
        os.startfile(output_filename_current)
        if errors_found:
            print("Errors were encountered during processing.")
        else:
            print("Errors: None found")
        print("Files are combined and ready to be overlaid")
    else:
        print("No matching files were found. Operation cancelled.")

if __name__ == "__main__":
    main()
