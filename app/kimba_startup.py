import subprocess
import threading
import time
from mood_engine import calculate_initial_mood
from boot_message import print_boot_message
from system_identity import get_system_identity
from longterm_memory import summarize_recent_memories, save_memory_entry
from response_style import respond
from daily_cycle import time_based_greeting, get_time_of_day

def start_trigger_system():
    """
    EN: Starts the background trigger system for file monitoring and idle detection.
    DE: Startet das Hintergrund-Trigger-System für Dateiüberwachung und Inaktivitätsprüfung.
    """
    subprocess.Popen(["python", "event_triggers_v2.py"])

def main():
    """
    EN: Main startup function for Kimba.
    Loads system info, calculates mood, greets the user, shows boot message,
    recalls recent memories, logs the startup, and starts background triggers.

    DE: Haupt-Startfunktion für Kimba.
    Lädt Systemdaten, berechnet Stimmung, begrüßt den Nutzer, zeigt Startnachricht,
    ruft Erinnerungen ab, speichert den Start und startet Hintergrund-Trigger.
    """
    print("✨ Kimba wird gestartet ...")

    # 🖥️ 1. Systemdaten ermitteln
    system_info = get_system_identity()

    # ⏰ 2. Begrüßung abhängig von Tageszeit
    tod = get_time_of_day()
    greeting = time_based_greeting()
    print(f"🕒 {greeting}")

    # 💫 3. Stimmung berechnen
    mood = calculate_initial_mood(reason=tod)

    # 👁️ 4. Visuelle Bootmeldung anzeigen
    print_boot_message(mood, system_info)

    # 🧠 5. Erinnerung (Gedächtnisrückblick)
    print("\n🧠 Rückblick:")
    print(summarize_recent_memories(3))

    # 💾 6. Start protokollieren
    save_memory_entry("Kimba wurde heute gestartet.", mood=mood, tags=["startup", "aktivierung"])

    # 💬 7. Stimmungsbasierte Begrüßung
    print("\n" + respond(mood))

    # 🔁 8. Hintergrund-Trigger starten
    thread = threading.Thread(target=start_trigger_system)
    thread.start()

# ▶️ Wenn direkt ausgeführt, dann starten
if __name__ == "__main__":
    main()
