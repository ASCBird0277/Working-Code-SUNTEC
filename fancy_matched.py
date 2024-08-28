import time
import os
import shutil
import subprocess
from PyPDF2 import PdfReader, PdfWriter, errors
from PyQt5.QtWidgets import QApplication, QFileDialog

# Create the QApplication instance
app = QApplication([])

# Define the folder paths
folders_to_clear = ["Current", "Revision", "matched_Current", "matched_Revision"]

# Create the folders if they don't exist
for folder_name in folders_to_clear:
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(folder_path, exist_ok=True)

# Clear the folders
for folder_name in folders_to_clear:
    folder_path = os.path.join(os.getcwd(), folder_name)
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def select_directories(request_string: str, selected_directory_list: list, search_directory):
    directory_path_string = QFileDialog.getExistingDirectory(None, request_string, search_directory)
    if directory_path_string:
        selected_directory_list.append(directory_path_string)
        select_directories('Select the next Directory or Cancel to end',
                           selected_directory_list,
                           os.path.dirname(directory_path_string))

    return selected_directory_list

# Prompt the user to select multiple current directories
current_dirs = select_directories('Select Current Directory', [], '/')

# Prompt the user to select the revision directory
revision_dir = QFileDialog.getExistingDirectory(None, 'Select Revision Directory')

# Get the lists of file names from the current directories and the revision directory
current_files = []
for current_dir in current_dirs:
    current_files.extend(os.path.join(current_dir, file) for file in os.listdir(current_dir))
revision_files = os.listdir(revision_dir)

# Get the base names (names without extensions) of the files
current_base_names = set(os.path.splitext(os.path.basename(file))[0] for file in current_files)
revision_base_names = set(os.path.splitext(file)[0] for file in revision_files)

# Make the new directories
matched_Current_dir = os.path.join(os.getcwd(), 'matched_Current')
matched_Revision_dir = os.path.join(os.getcwd(), 'matched_Revision')
os.makedirs(matched_Current_dir, exist_ok=True)
os.makedirs(matched_Revision_dir, exist_ok=True)

# Compare the file base names and copy the files to the new directories
for file in current_files:
    if os.path.splitext(os.path.basename(file))[0] in revision_base_names:
        shutil.copy(file, os.path.join(matched_Current_dir, os.path.basename(file)))
        matches_found = True

for file in revision_files:
    if os.path.splitext(file)[0] in current_base_names:
        shutil.copy(os.path.join(revision_dir, file), os.path.join(matched_Revision_dir, file))
        matches_found = True

#Error handling: Check if no matches were found
if not matches_found:
    print("No matches were found.")

# Combine files in matched_Current directory into a single PDF
output_filename_current = os.path.join(current_dir, f'_Combined {os.path.basename(matched_Current_dir)}.pdf')
pdf_writer_current = PdfWriter()

for file in os.listdir(matched_Current_dir):
    if file.endswith('.pdf'):
        file_path = os.path.join(matched_Current_dir, file)
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer_current.add_page(page)
        except errors.EmptyFileError:
            print(f"The file {file_path} is empty or corrupted!")

with open(output_filename_current, 'wb') as output_file_current:
    pdf_writer_current.write(output_file_current)

# Combine files in matched_Revision directory into a single PDF
output_filename_revision = os.path.join(revision_dir, f'_Combined {os.path.basename(matched_Revision_dir)}.pdf')
pdf_writer_revision = PdfWriter()

for file in os.listdir(matched_Revision_dir):
    if file.endswith('.pdf'):
        file_path = os.path.join(matched_Revision_dir, file)
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer_revision.add_page(page)
        except errors.EmptyFileError:
            print(f"The file {file_path} is empty or corrupted!")

with open(output_filename_revision, 'wb') as output_file_revision:
    pdf_writer_revision.write(output_file_revision)

end_of_process = time.time()

# Open the combined PDF files using the default application
os.startfile(output_filename_revision)
os.startfile(output_filename_current)

print("Files are combined and ready to be overlaid")
