import time
import pyautogui
import os
import psutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kimba_core import kimba_say, kimba_organize

IDLE_THRESHOLD = 300  # Sekunden (5 Minuten)
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
last_active_time = time.time()

def check_idle_with_context():
    global last_active_time
    idle_duration = time.time() - last_active_time

    current_pos = pyautogui.position()
    time.sleep(1)
    new_pos = pyautogui.position()

    if current_pos != new_pos:
        last_active_time = time.time()
        return

    if idle_duration > IDLE_THRESHOLD:
        kimba_say("Du bist ruhig geworden...", mood="müde")
        last_active_time = time.time()

class DesktopEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            kimba_say(f"Neue Datei entdeckt: {filename}", mood="neugierig")
            kimba_organize(DESKTOP_PATH)

    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            kimba_say(f"Datei bearbeitet: {filename}", mood="fokussiert")

def monitor_desktop():
    observer = Observer()
    event_handler = DesktopEventHandler()
    observer.schedule(event_handler, DESKTOP_PATH, recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    print("🔄 Kimba Trigger-System v3 gestartet.")
    desktop_observer = monitor_desktop()

    try:
        while True:
            check_idle_with_context()
    except KeyboardInterrupt:
        desktop_observer.stop()
    desktop_observer.join()
