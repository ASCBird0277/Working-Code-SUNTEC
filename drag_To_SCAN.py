import pyautogui
import time

def create_pagelabel_IDS_nemo():

    # Move to Create Page label button
    pyautogui.moveTo(2132, 116, duration=2)    
    pyautogui.click()

    # Move to "Select"
    pyautogui.moveTo(1956, 1032, duration=2)
    pyautogui.click()

    # Scan page label
    pyautogui.moveTo(3688, 1492, duration=2)
    pyautogui.dragTo(3747, 1519, duration=2)

    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')

def main():
    time.sleep(1)

    create_pagelabel_IDS_nemo()

if __name__ == "__main__":
    main()