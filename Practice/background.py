import pywinauto
from pywinauto import Application, mouse
from pywinauto.keyboard import send_keys
from time import sleep

# Connect to the Bluebeam Revu application using the PID
app = Application().connect(process=16476)

# Get the main window using the class name to ensure it's the correct one
main_window = app.window(class_name="WindowsForms10.Window.8.app.0.397a684_r8_as1")

# Optional: Introduce a short delay to allow the UI to load
sleep(5)  # Increase the delay to ensure everything is loaded

# Step 1: Select "Create Page Label" by AutomationId and ClassName
create_page_label_text = main_window.child_window(auto_id="197852", class_name="WindowsForms10.Window.8.app.0.397a684_r8_as1")

# Check if the control exists and is enabled
if create_page_label_text.exists(timeout=20) and create_page_label_text.is_enabled():
    create_page_label_text.click_input()  # Perform click action on the control
else:
    print("Control not found or not enabled.")
    exit()  # Exit if the control is not found

# Step 2: Wait for the "Create Page Label" window to appear
try:
    create_label_dlg = main_window.child_window(title_re=".*Create Page Label.*", class_name="WindowsForms10.Window.8.app.0.397a684_r8_as1")
    create_label_dlg.wait("exists ready", timeout=20)
except pywinauto.timings.TimeoutError:
    print("Create Page Label dialog did not appear within the timeout period.")
    exit()

# Step 3: Select the "Select" option in the "Create Page Label" window
select_button = create_label_dlg.child_window(title="Select", control_type="Button", class_name="WindowsForms10.Window.8.app.0.397a684_r8_as1")
select_button.click_input()

# Step 4: Perform the click and drag operation
start_coords = (3686, 941)  # Starting coordinates of the drag
end_coords = (3752, 915)    # Ending coordinates of the drag

# Perform the drag operation
mouse.press(coords=start_coords)
mouse.move(coords=end_coords)
mouse.release(coords=end_coords)

# Step 5: Click the "Okay" button to confirm
okay_button = create_label_dlg.child_window(title="OK", control_type="Button", class_name="WindowsForms10.Window.8.app.0.397a684_r8_as1")
okay_button.click_input()
