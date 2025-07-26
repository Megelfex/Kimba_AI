import datetime
import random
import json
import os

# Pfade für Mood-Logik
REFLECTION_LOG = "memory/self_reflection_log.md"
MOOD_STATE_FILE = "memory/kimba_memory_v2/current_mood.json"

# Grundemotionen
BASE_MOODS = [
    "fröhlich", "nachdenklich", "ruhig", "verspielt",
    "müde", "genervt", "neugierig", "traurig"
]

def analyze_reflection():
    """
    EN: Analyzes recent reflection logs to infer a base mood based on keyword occurrence.
    DE: Analysiert die letzten Reflexionen, um anhand von Stichwörtern eine Grundstimmung abzuleiten.

    Returns:
        str: Detected mood or "neutral" if none is dominant.
    """
    if not os.path.exists(REFLECTION_LOG):
        return "neutral"
    with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()[-20:]  # Only most recent lines

    mood_scores = {mood: 0 for mood in BASE_MOODS}
    for line in lines:
        for mood in BASE_MOODS:
            if mood in line.lower():
                mood_scores[mood] += 1

    best_mood = max(mood_scores, key=mood_scores.get)
    return best_mood if mood_scores[best_mood] > 0 else "neutral"

def context_based_adjustment(base_mood):
    """
    EN: Adjusts the mood based on time-of-day context (e.g., tired at night).
    DE: Passt die Grundstimmung je nach Tageszeit an (z. B. müde in der Nacht).

    Args:
        base_mood (str): Initial detected mood

    Returns:
        str: Contextually adjusted mood
    """
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 5:
        return "müde"
    elif hour in range(6, 10) and base_mood == "neutral":
        return "ruhig"
    elif hour in range(16, 20) and base_mood == "neutral":
        return "verspielt"
    return base_mood

def idle_penalty(base_mood, days_idle=0):
    """
    EN: Applies mood degradation if Kimba has been idle for several days.
    DE: Verschlechtert die Stimmung, wenn Kimba zu lange inaktiv war.

    Args:
        base_mood (str): Current mood before penalty
        days_idle (int): Number of days since last activity

    Returns:
        str: Possibly penalized mood
    """
    if days_idle >= 5:
        return "genervt"
    elif days_idle >= 3:
        return "nachdenklich"
    return base_mood

def estimate_idle_days():
    """
    EN: Calculates how many days have passed since Kimba's last mood update.
    DE: Schätzt, wie viele Tage seit Kimbas letzter Aktivität vergangen sind.

    Returns:
        int: Number of idle days
    """
    try:
        with open(MOOD_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        last_active = datetime.datetime.fromisoformat(state.get("last_active"))
        delta = datetime.datetime.now() - last_active
        return delta.days
    except:
        return 0

def update_current_mood():
    """
    EN: Main mood update function combining reflection analysis, time-based and idle penalty logic.
    Saves the mood state to disk.

    DE: Hauptfunktion zur Stimmungsaktualisierung. Kombiniert Reflexionsanalyse, Zeitkontext und Leerlauf-Penalty.
    Speichert den aktuellen Zustand auf Festplatte.

    Returns:
        str: Final evaluated mood
    """
    base_mood = analyze_reflection()
    adjusted = context_based_adjustment(base_mood)
    idle_days = estimate_idle_days()
    final_mood = idle_penalty(adjusted, idle_days)

    state = {
        "mood": final_mood,
        "last_active": datetime.datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(MOOD_STATE_FILE), exist_ok=True)
    with open(MOOD_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    return final_mood

def get_current_mood():
    """
    EN: Returns the most recently saved mood from persistent state file.
    DE: Gibt die zuletzt gespeicherte Stimmung aus der Statusdatei zurück.

    Returns:
        str: Current mood string or "neutral"
    """
    if not os.path.exists(MOOD_STATE_FILE):
        return "neutral"
    try:
        with open(MOOD_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("mood", "neutral")
    except:
        return "neutral"

# 🧪 Testfunktion bei direktem Start
if __name__ == "__main__":
    mood = update_current_mood()
    print(f"Aktuelle Stimmung von Kimba: {mood}")
