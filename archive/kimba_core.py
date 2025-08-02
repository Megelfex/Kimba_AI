import threading
from desktop_kimba.mood_engine import get_current_mood
from core.longterm_memory import save_memory_entry
from modules.response_style import respond
from desktop_kimba.desktop_kimba_mood_sync import update_desktop_cat_mood
from modules.file_organizer import organize_folder
from modules.git_assistant import get_git_status
from modules.code_assistant import enter_code_assistant

# ======================================================
# 🧠 Kimba Core – Central control & interaction interface
# ======================================================
# EN: Main control functions for handling interactions, automations, and system states.
# DE: Zentrale Steuerfunktionen für Interaktionen, Automatisierungen und Systemzustände.
# ======================================================

def kimba_say(message, mood=None, store=True):
    """
    EN: Makes Kimba respond to a message based on the current mood and optionally saves it to memory.
    DE: Lässt Kimba auf eine Nachricht reagieren, basierend auf der aktuellen Stimmung, und speichert sie optional im Gedächtnis.

    Args:
        message (str): The user message or prompt.
        mood (str, optional): Current mood. If None, it will be auto-detected.
        store (bool): Whether to store this interaction in long-term memory.
    """
    mood = mood or get_current_mood()
    response = respond(mood)
    print(f"Kimba ({mood}): {response}")
    if store:
        save_memory_entry(message, mood=mood, tags=["kommunikation", "antwort"])
    update_desktop_cat_mood(mood)


def kimba_organize(path):
    """
    EN: Triggers Kimba's file organization tool for the given folder path.
    DE: Startet Kimbas Dateiorganisator für den angegebenen Ordnerpfad.

    Args:
        path (str): Absolute or relative folder path to organize.
    """
    print("📁 Kimba organisiert Dateien...")
    organize_folder(path)


def kimba_git_check():
    """
    EN: Checks and prints the current Git status of the project directory.
    DE: Überprüft und zeigt den aktuellen Git-Status des Projektverzeichnisses an.
    """
    print("🧩 Git Status:")
    print(get_git_status())


def kimba_code_scan():
    """
    EN: Launches Kimba’s code assistant to analyze and process code-related tasks.
    DE: Startet Kimbas Code-Assistenten zur Analyse und Verarbeitung von Code-Aufgaben.
    """
    print("🧪 Kimba analysiert deinen Code...")
    enter_code_assistant()


def kimba_wake():
    """
    EN: Simulates Kimba waking up – updates mood and sends a greeting.
    DE: Simuliert Kimbas Erwachen – aktualisiert die Stimmung und sendet eine Begrüßung.
    """
    print("🌞 Kimba erwacht...")
    mood = get_current_mood()
    update_desktop_cat_mood(mood)
    kimba_say("Ich bin wach!", mood=mood, store=False)


def start_core():
    """
    EN: Initializes the Kimba core system and triggers startup actions (e.g., mood sync, background checks).
    DE: Initialisiert das Kimba-Core-System und startet zugehörige Prozesse (z. B. Stimmungssync, Hintergrundchecks).
    """
    print("🎮 Kimba Core ist aktiv.")
    kimba_wake()

    # EN: Start a background thread to check Git status
    # DE: Starte einen Hintergrund-Thread zur Git-Statusprüfung
    threading.Thread(target=kimba_git_check).start()


# EN: Optional direct start when run as main script
# DE: Optionaler Direktstart bei direktem Skriptaufruf
if __name__ == "__main__":
    start_core()
