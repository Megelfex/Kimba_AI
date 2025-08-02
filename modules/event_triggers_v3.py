
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

# Konfiguration / Configuration
IDLE_THRESHOLD = 300  # 5 Minuten / 5 minutes
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

# Zeitstempel der letzten Aktivität / Timestamp of last activity
last_active_time = time.time()


def check_idle_with_context():
    """
    DE: Prüft, ob der Nutzer länger als IDLE_THRESHOLD inaktiv war (keine Mausbewegung).
        Falls ja, reagiert Kimba mit einer müden Nachricht.
    EN: Checks if the user has been idle longer than IDLE_THRESHOLD (no mouse movement).
        If so, Kimba reacts with a tired message.
    """
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
    """
    DE: Überwacht den Desktop-Ordner auf Dateiveränderungen und reagiert darauf.
    EN: Watches the desktop folder for file changes and triggers reactions.
    """

    def on_created(self, event):
        logging.info(f"📄 Neue Datei erstellt / New file created: {event.src_path}")
        kimba_say(f"Ich habe gesehen, dass du eine neue Datei erstellt hast: {os.path.basename(event.src_path)}", mood="neugierig")

    def on_deleted(self, event):
        logging.info(f"🗑️ Datei gelöscht / File deleted: {event.src_path}")
        kimba_say(f"Du hast gerade eine Datei gelöscht: {os.path.basename(event.src_path)}", mood="neutral")

    def on_modified(self, event):
        logging.info(f"✏️ Datei geändert / File modified: {event.src_path}")
        kimba_say(f"Ich habe gesehen, dass du an {os.path.basename(event.src_path)} gearbeitet hast.", mood="aufmerksam")

    def on_moved(self, event):
        logging.info(f"📂 Datei verschoben / File moved: {event.src_path} -> {event.dest_path}")
        kimba_say(f"Du hast eine Datei verschoben: {os.path.basename(event.dest_path)}", mood="neutral")


def start_desktop_watcher():
    """
    DE: Startet die Überwachung des Desktop-Ordners in einem eigenen Thread.
    EN: Starts monitoring the desktop folder in a separate thread.
    """
    logging.info("Starting desktop folder watcher...")
    event_handler = DesktopEventHandler()
    observer = Observer()
    observer.schedule(event_handler, DESKTOP_PATH, recursive=False)
    observer.start()

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
