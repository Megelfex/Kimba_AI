import os
import json

# 📍 Pfad zur Statusdatei der Desktop-Kimba (wird regelmäßig gelesen)
STATE_FILE = "desktop_kimba/kimba_state.json"

def update_desktop_cat_mood(mood):
    """
    EN: Updates the emotional state of the desktop cat by writing to a shared JSON file.
    This file is monitored by the animation engine to reflect Kimba's current mood.

    DE: Aktualisiert den emotionalen Zustand der Desktop-Kimba,
    indem eine gemeinsame JSON-Datei beschrieben wird.
    Diese Datei wird von der Animations-Engine ausgelesen.

    Args:
        mood (str): New mood string (e.g., "fröhlich", "neugierig", "müde")

    Returns:
        None
    """
    try:
        state = {"mood": mood}
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
        print(f"[Desktop-Kimba] Mood aktualisiert: {mood}")
    except Exception as e:
        print(f"[Fehler] Mood-Update der Desktop-Kimba fehlgeschlagen: {e}")
