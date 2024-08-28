import os
import re
import shutil
import PyPDF2
import subprocess
import pandas as pd
import smartsheet
from datetime import datetime
import time
import pyautogui

# Function to authenticate with Smartsheet API
def smartsheet_authenticate(api_token):
    ss_client = smartsheet.Smartsheet(api_token)
    ss_client.errors_as_exceptions(True)
    return ss_client

# Function to fetch data from Smartsheet with enhanced filtering
def fetch_smartsheet_data(ss_client, sheet_id, project_column_id, status_column_id):
    try:
        # Load sheet
        sheet = ss_client.Sheets.get_sheet(sheet_id)
        print(f"Sheet loaded: {sheet.name} (ID: {sheet.id})")
        
        # Extract column data based on the "SHUFFLE STATUS" column
        column_data = []
        for row in sheet.rows:
            status_value = None
            project_value = None
            for cell in row.cells:
                if cell.column_id == status_column_id:
                    status_value = cell.display_value
                if cell.column_id == project_column_id:
                    project_value = cell.display_value
            # Include rows where "SHUFFLE STATUS" is empty or "Hold"
            if status_value is None or status_value.lower() == "hold":
                column_data.append(project_value)
        
        return column_data
        
    except smartsheet.exceptions.ApiError as e:
        print(f"Error fetching Smartsheet data: {e}")
        print(e.error.result)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Function to export data to Excel
def export_to_excel(column_data, output_folder, output_file):
    try:
        df = pd.DataFrame(column_data, columns=["Project Name"])
        os.makedirs(output_folder, exist_ok=True)
        full_output_path = os.path.join(output_folder, output_file)
        df.to_excel(full_output_path, index=False)
        print(f"Data exported to {full_output_path}")
        return full_output_path
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        return None

# Function to process the filtered list and search for folders
def process_filtered_list(excel_file_path, sheet_name, filter_column, base_path):
    print(f"Reading Excel file: {excel_file_path}")
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    filtered_df = df[df[filter_column].notnull()]

    # Reverse the order of the DataFrame
    filtered_df = filtered_df.iloc[::-1]

    print(f"Filtered DataFrame (reversed order):\n{filtered_df}")

    for index, row in filtered_df.iterrows():
        project_name = row[filter_column]
        print(f"Processing project name: {project_name}")
        
        # Split the project name into job number and project name
        parts = project_name.split(' - ')
        
        if len(parts) == 2:
            job_number = parts[0].strip()
            project_name_variable = parts[1].strip()
            print(f"Job Number: {job_number}, Project Name: {project_name_variable}")

            # Determine the year from the first two digits of the job number
            year_prefix = job_number[:2]
            job_year = f"20{year_prefix}"
            print(f"Determined Job Year: {job_year}")

            # Define the base path for the year
            base_path_year = os.path.join(base_path, f"{job_year} JOBS")
            print(f"Base path for year: {base_path_year}")

            # Search for the folder that starts with the job name
            for root, dirs, files in os.walk(base_path_year):
                for dir_name in dirs:
                    if dir_name.lower().startswith(project_name_variable.lower()):
                        path_to_selected_job_folder = os.path.join(root, dir_name)
                        print(f"Found matching folder: {path_to_selected_job_folder}")
                        return path_to_selected_job_folder, job_number
            print(f"No matching folder found for project: {project_name_variable}")
        else:
            print(f"No valid job number found in project name: {project_name}")
    return None, None

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
    action = input("The '_DC WORKSPACE' directory already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
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

def run_apply_stamp_script():
    try:
        # Give some time for Bluebeam Revu to be in focus
        time.sleep(5)  # Adjust sleep time if needed
        
        # Print message to indicate the script is running
        print("Attempting to click the shortcut...")

        # Use the actual coordinates captured earlier
        shortcut_x = 1952  # Replace with the correct x-coordinate
        shortcut_y = 44  # Replace with the correct y-coordinate
        pyautogui.moveTo(shortcut_x, shortcut_y, duration=1)  # Move to the coordinates with a visible delay
        print(f"Moved to ({shortcut_x}, {shortcut_y})")
        
        # Capture a screenshot before the click
        pyautogui.screenshot('before_click.png')
        
        # Click on the shortcut to run the script
        pyautogui.click()
        time.sleep(1)
        
        # Capture a screenshot after the click
        pyautogui.screenshot('after_click.png')
        
        # Print message to confirm the click action
        print("Clicked the shortcut to run 'Apply Stamp' script")
    except Exception as e:
        print(f"Error running 'Apply Stamp' script: {e}")

def main():
    # Ensure the script is running from the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Smartsheet API token
    api_token = 'XQvWlMSlWl6r4QUpuxeYW36wEn4XpQuC7t5rb'  # Replace with your new API token
    
    # Smartsheet sheet ID and column IDs
    sheet_id = '5487677702203268'  # DOCUMENT CONTROLLER REQUEST
    project_column_id = 83663976195972  # Column ID for PROJECT NAME
    status_column_id = 2937575255107460  # Column ID for SHUFFLE STATUS
    
    # Folder to save the exported Excel files
    output_folder = 'exports'
    
    # Authenticate with Smartsheet
    ss_client = smartsheet_authenticate(api_token)
    
    # Fetch column data from Smartsheet
    column_data = fetch_smartsheet_data(ss_client, sheet_id, project_column_id, status_column_id)
    if not column_data:
        print("Failed to fetch data from Smartsheet. Exiting.")
        return

    # Generate output file name with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"column_data_{timestamp}.xlsx"
    
    # Export column data to Excel
    excel_file_path = export_to_excel(column_data, output_folder, output_file)
    if not excel_file_path:
        print("Failed to export data to Excel. Exiting.")
        return

    # Base path to search for the folders
    base_path = 'Y:\\Shared'

    # Process the filtered list and search for folders
    selected_folder_path, job_number = process_filtered_list(excel_file_path, 'Sheet1', 'Project Name', base_path)
    if not selected_folder_path:
        print("No matching folder found. Exiting.")
        return

    # Continue with the operations on the selected folder
    folder_4_00 = find_folder_with_prefix(selected_folder_path, "4.00_")
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
    next_folder = find_folder_with_prefix(selected_folder_path, next_folder_prefix)
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

    try:
        os.startfile(combined_pdf_path)
    except Exception as e:
        print(f"Error opening combined PDF file: {e}")
        return
    
    # Run the "Apply Stamp" script
    run_apply_stamp_script()

if __name__ == "__main__":
    main()
