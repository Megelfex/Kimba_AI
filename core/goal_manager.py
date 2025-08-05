import time
import threading
from datetime import datetime
from core.longterm_memory import add_memory, search_memories

GOAL_CHECK_INTERVAL = 3600  # 1 Stunde
GOAL_MANAGER_RUNNING = True

def add_goal(description, priority="medium"):
    """Fügt ein neues Ziel ins Langzeitgedächtnis ein."""
    goal_entry = f"[ZIEL] {description} (Priorität: {priority})"
    add_memory(content=goal_entry, category="goal", tags=["ziel", priority])
    print(f"[GoalManager] 🎯 Neues Ziel gespeichert: {description}")

def check_goals():
    """Prüft offene Ziele und meldet Fortschritt oder Blockaden."""
    print("[GoalManager] 🔍 Prüfe aktuelle Ziele...")
    goals = search_memories("[ZIEL]", limit=50)

    if not goals:
        print("[GoalManager] Keine Ziele gefunden.")
        return

    for _, ts, content, mood, category, tags in goals:
        description = content.replace("[ZIEL]", "").strip()
        print(f"[GoalManager] 📝 Ziel: {description} (Tags: {tags})")

        # Dummy-Logik für Fortschrittsprüfung:
        # Hier könnten wir z. B. prüfen, ob Dateien/Module aus diesem Ziel erstellt wurden
        if "Animation" in description:
            status = "In Arbeit"
        else:
            status = "Keine Änderung festgestellt"

        # Ergebnis ins Gedächtnis schreiben
        add_memory(
            content=f"Zielstatus-Update ({description}): {status} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
            category="goal_update",
            tags=["ziel", "status"]
        )

def run_goal_manager():
    """Startet den Ziel-Manager im Hintergrund."""
    while GOAL_MANAGER_RUNNING:
        try:
            check_goals()
        except Exception as e:
            print(f"[GoalManager] ❌ Fehler: {e}")
        time.sleep(GOAL_CHECK_INTERVAL)

def start_goal_manager_in_background():
    """Startet den Ziel-Manager als separaten Thread."""
    thread = threading.Thread(target=run_goal_manager, daemon=True)
    thread.start()
    print("[GoalManager] 🚀 Hintergrund-Ziel-Manager gestartet.")

def stop_goal_manager():
    """Stoppt den Ziel-Manager."""
    global GOAL_MANAGER_RUNNING
    GOAL_MANAGER_RUNNING = False
    print("[GoalManager] ⏹ Gestoppt.")
