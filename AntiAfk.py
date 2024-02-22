import time
import pygetwindow as gw
import pyautogui
import keyboard

# ANSI escape codes for color formatting
RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
YELLOW_COLOR = '\033[93m'
WHITE_COLOR = '\033[97m'
RESET_COLOR = '\033[0m'

# Messages for user
TOGGLE_MESSAGE = f"{YELLOW_COLOR}Make sure the instances you want on anti-afk are minimized and not focused{RESET_COLOR}"
TOGGLE_PROMPT = f"{YELLOW_COLOR}Press the toggle key again to toggle off, or press 'Home' to change the keybind.{RESET_COLOR}"
KEYBIND_CHANGE_PROMPT = f"{YELLOW_COLOR}Would you like to change the keybind for toggling the script? (y/n): {RESET_COLOR}"
MINIMIZE_PROMPT = f"{YELLOW_COLOR}Would you like to minimize all instances of 'Roblox' before toggling? (y/n): {RESET_COLOR}"

toggle = False  # Initial toggle state
toggle_key = 'f12'  # Default toggle key
asked_to_minimize = False  # Keep track if the user has been asked to minimize the instance

def minimize_all_instances():
    try:
        roblox_windows = gw.getWindowsWithTitle("Roblox")
        for window in roblox_windows:
            window.minimize()
        print(f"{GREEN_COLOR}All instances of 'Roblox' minimized.{RESET_COLOR}") if roblox_windows else \
            print(f"{RED_COLOR}No instances of 'Roblox' found.{RESET_COLOR}")
    except Exception as e:
        print(f"{RED_COLOR}Error while minimizing instances: {e}{RESET_COLOR}")

def maximize_and_press_space(window):
    try:
        window.maximize()
        time.sleep(0.5)  # Wait for the window to maximize
        window.activate()  # Ensure the window is activated before clicking
        screen_width, screen_height = pyautogui.size()  # Get the screen size
        pyautogui.click(button='left', x=screen_width // 2, y=screen_height // 2)  # Click at the center of the screen
        time.sleep(0.2)  # Wait for a short time
        window.minimize()
        print(f"{GREEN_COLOR}Action performed on window '{window.title}' successfully.{RESET_COLOR}")
    except Exception as e:
        print(f"{RED_COLOR}Error while processing window '{window.title}': {e}{RESET_COLOR}")

def toggle_action():
    global toggle
    toggle = not toggle  # Toggle the value of the 'toggle' variable
    print(f"{GREEN_COLOR}Toggle is {toggle}{RESET_COLOR}")
    print(TOGGLE_PROMPT)

def detect_existing_instances():
    global asked_to_minimize
    try:
        roblox_windows = gw.getWindowsWithTitle("Roblox")
        for window in roblox_windows:
            if window.title == "Roblox" and window.isMinimized and not window.isActive:
                print(f"{WHITE_COLOR}-" * 40)
                print(f"{GREEN_COLOR}Existing instance of Roblox detected: '{window.title}'{RESET_COLOR}")
                maximize_and_press_space(window)
                print(f"{GREEN_COLOR}New instance of Roblox detected.{RESET_COLOR}")
                time.sleep(0.5)  # Add a short delay between processing each window
            elif window.title == "Roblox" and not window.isMinimized and not window.isActive and not asked_to_minimize:
                print(f"{WHITE_COLOR}-" * 40)
                print(f"{RED_COLOR}Instance of Roblox detected but not minimized: '{window.title}'{RESET_COLOR}")
                choice = input("Would you like to minimize this instance? (y/n): ")
                if choice.lower() == "y":
                    window.minimize()
                    print(f"{RED_COLOR}Instance '{window.title}' minimized.{RESET_COLOR}")
                asked_to_minimize = True  # Set to True after asking the question
    except Exception as e:
        print(f"{WHITE_COLOR}-" * 40)
        print(f"{RED_COLOR}Error while detecting existing instances: {e}{RESET_COLOR}")

def change_keybind():
    global toggle_key
    print(KEYBIND_CHANGE_PROMPT)
    choice = input().lower()
    if choice == "y":
        print(f"{YELLOW_COLOR}Please press the desired key for toggle...{RESET_COLOR}")
        toggle_key = keyboard.read_event(suppress=False).name
        keyboard.add_hotkey(toggle_key, toggle_action)  # Bind the new key to toggle_action function
        print(f"{GREEN_COLOR}Key '{toggle_key}' has been set as the toggle key.{RESET_COLOR}")
    else:
        print(f"{YELLOW_COLOR}Keybind change cancelled. Current keybind remains '{toggle_key}'.{RESET_COLOR}")
        # Re-register the F12 keybind if the user chooses not to change it
        keyboard.add_hotkey(toggle_key, toggle_action)

if __name__ == "__main__":
    print(TOGGLE_MESSAGE)
    change_keybind()  # Change keybind if user wants
    print(f"{YELLOW_COLOR}The current toggle keybind is '{toggle_key}'.{RESET_COLOR}")
    print(MINIMIZE_PROMPT)
    minimize_choice = input()
    if minimize_choice.lower() == "y":
        minimize_all_instances()
    
    while True:
        if toggle:  # Only execute the loop if toggle is True
            detect_existing_instances()  # Check for existing instances
            time.sleep(10 * 60)  # Wait for 10 minutes before checking again
        else:
            time.sleep(1)  # If toggle is False, wait for 1 second before checking
