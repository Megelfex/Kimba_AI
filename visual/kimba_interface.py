import os
import json

# Dieser Pfad wird von der Desktop-Kimba regelmäßig gelesen
STATE_FILE = "desktop_kimba/kimba_state.json"

def update_desktop_cat_mood(mood):
    try:
        state = {"mood": mood}
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f)
        print(f"[Desktop-Kimba] Mood aktualisiert: {mood}")
    except Exception as e:
        print(f"[Fehler] Mood-Update der Desktop-Kimba fehlgeschlagen: {e}")
