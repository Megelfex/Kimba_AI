import os
import shutil
from datetime import datetime
from core.longterm_memory import save_memory_entry
from core.mood_engine import update_current_mood
from modules.response_style import respond

# Erweiterbare Kategorien
FOLDER_MAP = {
    ".pdf": "Dokumente",
    ".txt": "Notizen",
    ".jpg": "Bilder",
    ".png": "Bilder",
    ".gif": "Bilder",
    ".mp3": "Musik",
    ".wav": "Musik",
    ".mp4": "Videos",
    ".py": "Code",
    ".js": "Code",
    ".zip": "Archive",
    ".exe": "Programme"
}

TARGET_BASE = os.path.join(os.path.expanduser("~"), "Desktop", "Sortiert")

def ensure_target_dirs():
    os.makedirs(TARGET_BASE, exist_ok=True)
    for folder in set(FOLDER_MAP.values()):
        os.makedirs(os.path.join(TARGET_BASE, folder), exist_ok=True)

def organize_folder(path):
    ensure_target_dirs()
    moved_files = []

    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in FOLDER_MAP:
                target_folder = os.path.join(TARGET_BASE, FOLDER_MAP[ext])
                target_path = os.path.join(target_folder, file)
                shutil.move(full_path, target_path)
                moved_files.append(file)

    if moved_files:
        mood = "fokussiert"
        update_current_mood(mood)
        save_memory_entry(f"Ich habe {len(moved_files)} Datei(en) sortiert: {', '.join(moved_files)}", mood=mood, tags=["sortierung", "dateien"])
        print(f"🧹 Kimba (fokussiert): Ich habe den Ordner aufgeräumt!")
        print(respond(mood))
    else:
        print("✨ Kimba: Alles war schon ordentlich!")

# Beispiel
if __name__ == "__main__":
    organize_folder(os.path.join(os.path.expanduser("~"), "Desktop"))
