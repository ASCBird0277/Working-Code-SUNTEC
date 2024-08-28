import time
import pyautogui

# Disable the PyAutoGUI fail-safe feature for testing
pyautogui.FAILSAFE = False

def run_apply_stamp_script():
    try:
        # Give some time for Bluebeam Revu to be in focus
        time.sleep(5)  # Adjust sleep time if needed
        
        # Print message to indicate the script is running
        print("Attempting to click the shortcut...")

        # Use the actual coordinates captured earlier
        shortcut_x = 994  # Replace with the correct x-coordinate
        shortcut_y = 47  # Replace with the correct y-coordinate
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
    # Run the "Apply Stamp" script
    run_apply_stamp_script()

if __name__ == "__main__":
    main()
