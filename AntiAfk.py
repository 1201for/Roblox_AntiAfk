
import os
import tkinter as tk
from tkinter import font as tkfont
import time
import pygetwindow as gw
import pyautogui
import subprocess
import win32gui
import threading

# Define color tags for the text widget
COLORS = {
    "green": "#00FF00",
    "yellow": "#FFFF00",
    "red": "#FF0000",
    "blue": "#0000FF",
    "white": "#FFFFFF",
    "black": "#000000",
    "dark_bg": "#1E1E1E",
    "light_text": "#E0E0E0"
}

toggle = False  # Initial toggle state

def append_to_log(message, color="light_text"):
    log_window.config(state=tk.NORMAL)
    log_window.insert(tk.END, message + "\n")
    log_window.tag_add(color, "end-1c linestart", "end-1c lineend")
    log_window.tag_configure(color, foreground=COLORS[color])
    log_window.config(state=tk.DISABLED)
    log_window.yview(tk.END)  # Scroll to the end

def minimize_all_instances():
    try:
        roblox_windows = gw.getWindowsWithTitle("Roblox")
        if roblox_windows:
            for window in roblox_windows:
                window.minimize()
            append_to_log("All instances of 'Roblox' minimized.", "green")
        else:
            append_to_log("No instances of 'Roblox' found.", "red")
    except Exception as e:
        append_to_log(f"Error while minimizing instances: {e}", "red")

def maximize_and_press_space(window):
    try:
        append_to_log(f"Maximizing window: '{window.title}'", "light_text")
        window.maximize()
        time.sleep(0.2)  # Shorter wait for window to maximize
        window.activate()  # Ensure the window is activated before clicking
        screen_width, screen_height = pyautogui.size()  # Get the screen size
        pyautogui.click(button='left', x=screen_width // 2, y=screen_height // 2)  # Click at the center of the screen
        time.sleep(0.1)  # Shorter wait after clicking
        window.minimize()
        append_to_log(f"Action performed on window '{window.title}' successfully.", "green")
    except Exception as e:
        append_to_log(f"Error while processing window '{window.title}': {e}", "red")

def is_window_on_top(hwnd):
    try:
        return win32gui.GetForegroundWindow() == hwnd
    except Exception as e:
        append_to_log(f"Error checking if window is on top: {e}", "red")
        return False

def toggle_action():
    global toggle
    toggle = not toggle  # Toggle the value of the 'toggle' variable
    status_text = "ON" if toggle else "OFF"
    status_color = "green" if toggle else "red"
    append_to_log(f"Toggle is {status_text}", status_color)
    status_label.config(text=f"Current Status: {status_text}", fg=status_color)

def detect_existing_instances():
    try:
        roblox_windows = gw.getWindowsWithTitle("Roblox")
        append_to_log("-" * 40, "light_text")
        if not roblox_windows:
            append_to_log("No instances of 'Roblox' detected.", "red")
        for window in roblox_windows:
            hwnd = window._hWnd  # Get the window handle
            append_to_log(f"Checking window: '{window.title}'", "light_text")
            
            # Only proceed if the title is exactly "Roblox"
            if window.title.strip() == "Roblox":
                if window.isActive:
                    append_to_log(f"Instance of Roblox is currently active: '{window.title}'", "blue")
                elif is_window_on_top(hwnd):
                    append_to_log(f"Instance of Roblox is on top: '{window.title}'", "blue")
                elif not window.isMinimized and not window.isActive:
                    append_to_log(f"Instance of Roblox is not minimized and not active: '{window.title}'", "blue")
                    maximize_and_press_space(window)  # Maximize and press space
                elif window.isMinimized and not window.isActive:
                    append_to_log(f"Instance of Roblox is minimized and not active: '{window.title}'", "green")
                    maximize_and_press_space(window)
                else:
                    append_to_log(f"Unhandled window state for '{window.title}'", "red")
                
                time.sleep(0.3)  # Shorter delay between processing each window
    except Exception as e:
        append_to_log("-" * 40, "light_text")
        append_to_log(f"Error while detecting existing instances: {e}", "blue")

def find_roblox_executable():
    roblox_versions_path = os.path.expanduser("~\\AppData\\Local\\Roblox\\Versions")
    try:
        for folder in os.listdir(roblox_versions_path):
            if folder.startswith("version-"):
                roblox_executable_path = os.path.join(roblox_versions_path, folder, "RobloxPlayerBeta.exe")
                if os.path.isfile(roblox_executable_path):
                    return roblox_executable_path
    except Exception as e:
        append_to_log(f"Error finding Roblox executable: {e}", "red")
    return None

def launch_roblox_instance():
    roblox_path = find_roblox_executable()
    if roblox_path:
        try:
            # Launch Roblox in a new instance by using a different command line
            subprocess.Popen([roblox_path, '--app', '--disable-roblox-beta'])
            append_to_log("Launched new Roblox instance.", "green")
        except Exception as e:
            append_to_log(f"Error launching Roblox instance: {e}", "red")
    else:
        append_to_log("Roblox executable not found.", "red")

def on_toggle():
    toggle_action()
    toggle_button.config(text="Toggle OFF" if toggle else "Toggle ON")

def on_launch():
    launch_roblox_instance()

def gui():
    def start_detection():
        global detection_thread
        if detection_thread is None or not detection_thread.is_alive():
            detection_thread = threading.Thread(target=run_detection_loop)
            detection_thread.start()

    def run_detection_loop():
        while True:
            if toggle:  # Only execute the loop if toggle is True
                append_to_log("Checking for Roblox instances...", "yellow")
                detect_existing_instances()  # Check for existing instances
                time.sleep(5 * 60)  # Reduced to 5 minutes for faster detection
            else:
                time.sleep(1)  # If toggle is False, wait for 1 second before checking

    root = tk.Tk()
    root.title("Roblox Anti-AFK")

    # Set window size and center it
    root.geometry('600x400')
    root.resizable(False, False)

    # Define a custom font
    custom_font = tkfont.Font(family="Helvetica", size=12)

    # Create a frame for the content
    frame = tk.Frame(root, padx=20, pady=20, bg=COLORS["dark_bg"])
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Add a title label
    title_label = tk.Label(frame, text="Roblox Anti-AFK Control Panel", font=tkfont.Font(family="Helvetica", size=16, weight="bold"), bg=COLORS["dark_bg"], fg=COLORS["white"])
    title_label.pack(pady=10)

    # Add a status label
    global status_label
    status_label = tk.Label(frame, text="Current Status: OFF", font=custom_font, fg="red", bg=COLORS["dark_bg"])
    status_label.pack(pady=10)

    # Add the toggle button
    global toggle_button
    toggle_button = tk.Button(frame, text="Toggle ON", command=on_toggle, width=20, font=custom_font, bg="#4CAF50", fg="white", relief=tk.RAISED)
    toggle_button.pack(pady=10)

    # Add the launch button
    launch_button = tk.Button(frame, text="Launch Roblox Instance", command=on_launch, width=20, font=custom_font, bg="#2196F3", fg="white", relief=tk.RAISED)
    launch_button.pack(pady=10)

    # Add the log text box
    global log_window
    log_window = tk.Text(frame, wrap=tk.WORD, height=10, width=70, font=custom_font, bg=COLORS["dark_bg"], fg=COLORS["light_text"])
    log_window.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() and exit())  # Ensure clean exit
    start_detection()
    root.mainloop()

if __name__ == "__main__":
    detection_thread = None
    gui()
