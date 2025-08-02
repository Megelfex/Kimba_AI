
"""
Kimba Event Triggers v3
=======================
DE: Überwacht Nutzeraktivität und Dateisystem-Ereignisse, um automatische Reaktionen von Kimba auszulösen.

EN: Monitors user activity and file system events to trigger automatic reactions from Kimba.
"""

import time
import os
import logging
import pyautogui
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.kimba_core import kimba_say, run_file_organizer

# Logging-Konfiguration / Logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

IDLE_THRESHOLD = 300  # Sekunden (5 Minuten)
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

# Zeitstempel der letzten Aktivität / Timestamp of last activity
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
        logging.info("User idle detected. Triggering tired mood response.")
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
    observer = Observer()
    observer.schedule(event_handler, DESKTOP_PATH, recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    print("🔄 Kimba Trigger-System v3 gestartet.")
    desktop_observer = monitor_desktop()

    try:
        while True:
            check_idle_with_context()
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Stopping desktop watcher...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_desktop_watcher()
