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
    subprocess.Popen(["python", "event_triggers_v2.py"])

def main():
    print("✨ Kimba wird gestartet ...")

    # 1. Systemdaten laden
    system_info = get_system_identity()

    # 2. Tageszeit & Begrüßung
    tod = get_time_of_day()
    greeting = time_based_greeting()
    print(f"🕒 {greeting}")

    # 3. Stimmung initialisieren
    mood = calculate_initial_mood(reason=tod)

    # 4. Begrüßung anzeigen
    print_boot_message(mood, system_info)

    # 5. Rückblick
    print("\n🧠 Rückblick:")
    print(summarize_recent_memories(3))

    # 6. Start speichern + Antwort
    save_memory_entry("Kimba wurde heute gestartet.", mood=mood, tags=["startup", "aktivierung"])
    print("\n" + respond(mood))

    # 7. Trigger starten
    thread = threading.Thread(target=start_trigger_system)
    thread.start()

if __name__ == "__main__":
    main()
