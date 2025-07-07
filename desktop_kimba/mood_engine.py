import datetime
import random
import json
import os

REFLECTION_LOG = "memory/self_reflection_log.md"
MOOD_STATE_FILE = "memory/kimba_memory_v2/current_mood.json"

BASE_MOODS = [
    "fröhlich", "nachdenklich", "ruhig", "verspielt",
    "müde", "genervt", "neugierig", "traurig"
]

def analyze_reflection():
    if not os.path.exists(REFLECTION_LOG):
        return "neutral"
    with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()[-20:]  # nur letzte Zeilen
    mood_scores = {mood: 0 for mood in BASE_MOODS}
    for line in lines:
        for mood in BASE_MOODS:
            if mood in line.lower():
                mood_scores[mood] += 1
    best_mood = max(mood_scores, key=mood_scores.get)
    return best_mood if mood_scores[best_mood] > 0 else "neutral"

def context_based_adjustment(base_mood):
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 5:
        return "müde"
    elif hour in range(6, 10) and base_mood == "neutral":
        return "ruhig"
    elif hour in range(16, 20) and base_mood == "neutral":
        return "verspielt"
    return base_mood

def idle_penalty(base_mood, days_idle=0):
    if days_idle >= 5:
        return "genervt"
    elif days_idle >= 3:
        return "nachdenklich"
    return base_mood

def estimate_idle_days():
    try:
        with open(MOOD_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        last_active = datetime.datetime.fromisoformat(state.get("last_active"))
        delta = datetime.datetime.now() - last_active
        return delta.days
    except:
        return 0

def update_current_mood():
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

# Direkter Test
if __name__ == "__main__":
    mood = update_current_mood()
    print(f"Aktuelle Stimmung von Kimba: {mood}")

def get_current_mood():
    if not os.path.exists(MOOD_STATE_FILE):
        return "neutral"
    try:
        with open(MOOD_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("mood", "neutral")
    except:
        return "neutral"
