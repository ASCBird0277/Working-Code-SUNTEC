import pyautogui

print("Move the mouse to the target position and press Ctrl+C")
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}", end="\r", flush=True)
except KeyboardInterrupt:
    print(f"\nCaptured Coordinates: X: {x}, Y: {y}")
