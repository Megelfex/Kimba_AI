import time
import pyautogui
import os
import psutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mood_engine import update_current_mood
from longterm_memory import save_memory_entry
from response_style import respond
from file_organizer import organize_folder

IDLE_THRESHOLD = 300  # Sekunden (5 Minuten)
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

last_active_time = time.time()
last_window = None

def check_idle_with_context():
    global last_active_time, last_window
    idle_duration = time.time() - last_active_time

    current_pos = pyautogui.position()
    time.sleep(1)
    new_pos = pyautogui.position()

    if current_pos != new_pos:
        last_active_time = time.time()
        return

    if idle_duration > IDLE_THRESHOLD:
        mood = "müde"
        print("😴 Kimba (müde): Du bist ruhig geworden...")
        print(respond(mood))
        update_current_mood(mood)
        save_memory_entry("Du warst länger als 5 Minuten inaktiv.", mood=mood, tags=["inaktiv", "pause"])
        last_active_time = time.time()

class DesktopEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            mood = "neugierig"
            update_current_mood(mood)
            if is_reasonable_moment():
                filename = os.path.basename(event.src_path)
                print(f"📦 Kimba (neugierig): Neue Datei entdeckt → {filename}")
                print(respond(mood))
                save_memory_entry(f"Neue Datei erstellt: {filename}", mood=mood, tags=["datei", "neu"])
                organize_folder(DESKTOP_PATH)

    def on_modified(self, event):
        if not event.is_directory:
            mood = "fokussiert"
            update_current_mood(mood)
            if is_reasonable_moment():
                filename = os.path.basename(event.src_path)
                print(f"🔄 Kimba (fokussiert): Datei bearbeitet → {filename}")
                print(respond(mood))
                save_memory_entry(f"Datei bearbeitet: {filename}", mood=mood, tags=["datei", "bearbeitet"])

def is_reasonable_moment():
    hour = datetime.now().hour
    return 7 <= hour <= 22

def monitor_desktop():
    observer = Observer()
    event_handler = DesktopEventHandler()
    observer.schedule(event_handler, DESKTOP_PATH, recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    print("🔄 Kimba Trigger-System v2 gestartet.")
    desktop_observer = monitor_desktop()

    try:
        while True:
            check_idle_with_context()
    except KeyboardInterrupt:
        desktop_observer.stop()
    desktop_observer.join()
