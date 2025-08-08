
"""
Kimba Core
==========
DE: Zentrale Steuerung der Kimba-KI. Hier werden Interaktionen, Automatisierungen, 
    Systemzustände und Stimmungsanpassungen koordiniert.

EN: Central control of the Kimba AI. Coordinates interactions, automations, 
    system states, and mood adjustments.
"""

import logging
import threading
from desktop_kimba.mood_engine import get_current_mood
from core.longterm_memory import save_memory_entry
from modules.response_style import respond
from desktop_kimba.desktop_kimba_mood_sync import update_desktop_cat_mood
from modules.file_organizer import organize_folder
from modules.git_assistant import get_git_status
from modules.code_assistant import enter_code_assistant 

# Logging-Konfiguration / Logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def kimba_say(message: str, mood: str = None, store: bool = True):
    """
    DE: Lässt Kimba auf eine Nachricht reagieren, basierend auf der aktuellen Stimmung.
        Optional wird die Interaktion im Langzeitgedächtnis gespeichert.
    EN: Makes Kimba respond to a message based on the current mood.
        Optionally stores the interaction in long-term memory.

    Args:
        message (str): Die Nutzernachricht / User message.
        mood (str, optional): Stimmung, wenn None -> automatisch ermittelt.
        store (bool): Ob die Interaktion gespeichert werden soll.
    """
    mood = mood or get_current_mood()
    response = respond(mood)
    logging.info(f"Kimba ({mood}): {response}")

    if store:
        save_memory_entry(message, mood=mood, tags=["communication"])

    return response


def sync_mood_with_desktop():
    """
    DE: Synchronisiert Kimbas Stimmung mit der Desktop-Katze.
    EN: Syncs Kimba's mood with the desktop cat.
    """
    mood = get_current_mood()
    logging.info(f"Synchronizing mood to desktop cat: {mood}")
    update_desktop_cat_mood(mood)


def run_file_organizer(path: str):
    """
    DE: Organisiert einen angegebenen Ordner automatisch.
    EN: Automatically organizes a given folder.
    """
    logging.info(f"Organizing folder: {path}")
    organize_folder(path)


def check_git_status(repo_path: str):
    """
    DE: Überprüft den Git-Status eines Projekts.
    EN: Checks the Git status of a project.
    """
    logging.info(f"Checking Git status for: {repo_path}")
    return get_git_status(repo_path)


def start_code_assistant():
    """
    DE: Startet den Code-Assistenten in einem eigenen Thread.
    EN: Starts the code assistant in a separate thread.
    """
    logging.info("Starting code assistant...")
    threading.Thread(target=enter_code_assistant, daemon=True).start()


def run_core_cycle():
    """
    DE: Führt einen zentralen Steuerzyklus aus (Beispiel: Automatisierungen, Mood-Sync).
    EN: Runs a central control cycle (example: automations, mood sync).
    """
    logging.info("Running core cycle...")
    sync_mood_with_desktop()
    # Weitere Automatisierungen könnten hier hinzugefügt werden / More automations can be added here
