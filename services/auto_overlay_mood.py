import time
import threading
from core.longterm_memory import search_memories
from overlay_client.control import send_overlay_command

MOOD_CHECK_INTERVAL = 30  # alle 30 Sekunden prüfen
IDLE_TIMEOUT = 180  # nach 3 Minuten Inaktivität Idle/Sleep

AUTO_OVERLAY_RUNNING = True
last_user_action_time = time.time()

def register_user_activity():
    """Wird aufgerufen, wenn der Nutzer mit Kimba interagiert."""
    global last_user_action_time
    last_user_action_time = time.time()

def get_latest_mood(character):
    """Ermittelt die letzte gespeicherte Stimmung aus dem Gedächtnis."""
    results = search_memories(category="mood", limit=5)
    for _, ts, content, mood, category, tags in results:
        if character.lower() in tags:
            return mood
    return None

def update_overlay_emotion():
    """Prüft Stimmung und Aktivität und aktualisiert die Overlays."""
    # Aktivitätsprüfung
    inactive_time = time.time() - last_user_action_time
    if inactive_time > IDLE_TIMEOUT:
        send_overlay_command("iuno", "idle")
        send_overlay_command("kimba", "sleep")
        return

    # Stimmung setzen (nur wenn aktiv)
    iuno_mood = get_latest_mood("iuno")
    kimba_mood = get_latest_mood("kimba")

    if iuno_mood:
        send_overlay_command("iuno", iuno_mood)
    else:
        send_overlay_command("iuno", "idle")

    if kimba_mood:
        send_overlay_command("kimba", kimba_mood)
    else:
        send_overlay_command("kimba", "idle")

def run_auto_overlay_mood():
    """Startet den Overlay-Mood-Manager im Hintergrund."""
    while AUTO_OVERLAY_RUNNING:
        try:
            update_overlay_emotion()
        except Exception as e:
            print(f"[Overlay-Mood] ❌ Fehler: {e}")
        time.sleep(MOOD_CHECK_INTERVAL)

def start_auto_overlay_mood_in_background():
    """Startet den Manager als separaten Thread."""
    thread = threading.Thread(target=run_auto_overlay_mood, daemon=True)
    thread.start()
    print("[Overlay-Mood] 🚀 Hintergrund-Stimmungsmanager gestartet.")

def stop_auto_overlay_mood():
    """Stoppt den Manager."""
    global AUTO_OVERLAY_RUNNING
    AUTO_OVERLAY_RUNNING = False
    print("[Overlay-Mood] ⏹ Gestoppt.")
