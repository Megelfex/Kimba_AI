import threading
from desktop_kimba.mood_engine import get_current_mood
from core.longterm_memory import save_memory_entry
from modules.response_style import respond
from desktop_kimba.desktop_kimba_mood_sync import update_desktop_cat_mood
from modules.file_organizer import organize_folder
from modules.git_assistant import get_git_status
from modules.code_assistant import enter_code_assistant

# Globale Steuerung & Nachrichtenverarbeitung

def kimba_say(message, mood=None, store=True):
    mood = mood or get_current_mood()
    response = respond(mood)
    print(f"Kimba ({mood}): {response}")
    if store:
        save_memory_entry(message, mood=mood, tags=["kommunikation", "antwort"])
    update_desktop_cat_mood(mood)

def kimba_organize(path):
    print("📁 Kimba organisiert Dateien...")
    organize_folder(path)

def kimba_git_check():
    print("🧩 Git Status:")
    print(get_git_status())

def kimba_code_scan():
    print("🧪 Kimba analysiert deinen Code...")
    enter_code_assistant()

def kimba_wake():
    print("🌞 Kimba erwacht...")
    mood = get_current_mood()
    update_desktop_cat_mood(mood)
    kimba_say("Ich bin wach!", mood=mood, store=False)

def start_core():
    print("🎮 Kimba Core ist aktiv.")
    kimba_wake()

    # Beispielhafte Hintergrundaktion
    threading.Thread(target=kimba_git_check).start()

# Optional: Direktstart
if __name__ == "__main__":
    start_core()
