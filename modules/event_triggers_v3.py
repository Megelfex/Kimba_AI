import time
import pyautogui
import os
import psutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kimba_core import kimba_say, kimba_organize

# ⏱️ Zeit in Sekunden bis als "inaktiv" gezählt wird
IDLE_THRESHOLD = 300  # 5 Minuten
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
last_active_time = time.time()

def check_idle_with_context():
    """
    EN: Checks if the user has been idle (no mouse movement) longer than IDLE_THRESHOLD.
    If so, Kimba reacts with a gentle message in tired mood.

    DE: Prüft, ob der Nutzer länger als IDLE_THRESHOLD inaktiv war (keine Mausbewegung).
    Falls ja, reagiert Kimba mit einer müden Nachricht.
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
        kimba_say("Du bist ruhig geworden...", mood="müde")
        last_active_time = time.time()

class DesktopEventHandler(FileSystemEventHandler):
    """
    EN: Watches the desktop folder for file changes and triggers reactions.
    DE: Überwacht den Desktop-Ordner auf Dateiveränderungen und reagiert darauf.
    """

    def on_created(self, event):
        """
        EN: Called when a new file is created. Kimba reacts curiously and organizes the desktop.
        DE: Wird bei neuer Datei aufgerufen. Kimba reagiert neugierig und organisiert den Desktop.
        """
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            kimba_say(f"Neue Datei entdeckt: {filename}", mood="neugierig")
            kimba_organize(DESKTOP_PATH)

    def on_modified(self, event):
        """
        EN: Called when a file is modified. Kimba reacts in a focused mood.
        DE: Wird bei Dateiänderung aufgerufen. Kimba reagiert fokussiert.
        """
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            kimba_say(f"Datei bearbeitet: {filename}", mood="fokussiert")

def monitor_desktop():
    """
    EN: Starts a watchdog observer to monitor the desktop for file events.
    DE: Startet einen Watchdog-Observer zur Überwachung von Dateiaktionen auf dem Desktop.

    Returns:
        Observer: The active observer instance
    """
    observer = Observer()
    event_handler = DesktopEventHandler()
    observer.schedule(event_handler, DESKTOP_PATH, recursive=False)
    observer.start()
    return observer

# ▶️ Direkter Start
if __name__ == "__main__":
    print("🔄 Kimba Trigger-System v3 gestartet.")
    desktop_observer = monitor_desktop()

    try:
        while True:
            check_idle_with_context()
    except KeyboardInterrupt:
        desktop_observer.stop()
    desktop_observer.join()
