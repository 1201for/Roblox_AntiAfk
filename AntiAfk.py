import time
import pyautogui
import pygetwindow as gw
import keyboard

toggle = False

def maximize_and_press_space(window):
    window.maximize()
    time.sleep(1)  # Wait for the window to maximize and gain focus
    window.activate()  # Ensure the window is activated before clicking
    screen_width, screen_height = pyautogui.size()  # Get the screen size
    pyautogui.click(button='left', x=screen_width // 2, y=screen_height // 2)  # Click at the center of the screen
    pyautogui.press('space')  # Press space bar
    time.sleep(0.5)  # Wait for the key press to be processed
    window.minimize()
    print(f"Action performed on window '{window.title}' successfully.")

def toggle_action():
    global toggle
    toggle = not toggle
    print("Toggle is", "ON" if toggle else "OFF")

def on_key_press(event):
    if event.name == 'f12':
        print("'F12' key pressed")
        toggle_action()

def detect_existing_instances():
    roblox_windows = gw.getWindowsWithTitle("Roblox")
    if roblox_windows:
        for window in roblox_windows:
            if window.title == "Roblox":
                print(f"Found window with title: '{window.title}'")
                print(f"Existing instance of Roblox detected: '{window.title}'")
                maximize_and_press_space(window)
                time.sleep(2)  # Add a 2-second delay between processing each window
    else:
        print("No windows with the title 'Roblox' found.")

if __name__ == "__main__":
    keyboard.on_press_key('f12', on_key_press)

    detect_existing_instances()  # Check for existing instances when the script starts

    while True:
        if toggle:
            print("Toggle is ON")  # Debugging print statement
            roblox_windows = gw.getWindowsWithTitle("Roblox")
            if roblox_windows:
                for window in roblox_windows:
                    if window.title == "Roblox":
                        print(f"Found window with title: '{window.title}'")
                        print(f"Existing instance of Roblox detected: '{window.title}'")
                        maximize_and_press_space(window)
                        print("New instance of Roblox detected.")
                        time.sleep(2)  # Add a 2-second delay between processing each window
            else:
                print("No windows with the title 'Roblox' found.")
        else:
            print("Toggle is OFF")  # Debugging print statement
        time.sleep(10 * 60)  # Wait for 10 minutes
