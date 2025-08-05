import time
import threading
import pyautogui
import imagehash
from PIL import Image
from datetime import datetime
from core.vision import KimbaVision
from core.longterm_memory import add_memory
from core.llm_router import KimbaLLMRouter

# ==========================
# Einstellungen
# ==========================
VISION_INTERVAL = 45         # Sekunden zwischen regulären Analysen
VISION_RUNNING = True
HASH_THRESHOLD = 12          # Unterschiedswert für "Major Change"
CHECK_FREQUENCY = 5          # Wie oft wir prüfen (Sekunden)
REACTION_COOLDOWN = 60       # Mindestens 60 Sek. zwischen zwei Reaktionen

# Vision-Handler & LLM
vision_handler = KimbaVision(vision_api="gpt4o", api_key=None)
llm = KimbaLLMRouter()
last_hash = None

# Callback für UI
reaction_callback = None

# Spam-Filter-Tracking
last_reaction_time = 0
pending_changes = []  # Speichert mehrere Änderungen, die wir zusammenfassen

# ==========================
# Callback setzen
# ==========================
def set_reaction_callback(callback):
    """Setzt eine Funktion, die Reaktionen ins UI weitergibt."""
    global reaction_callback
    reaction_callback = callback

# ==========================
# Screenshot & Analyse
# ==========================
def capture_screenshot():
    return pyautogui.screenshot()

def analyze_and_save(screenshot, reason="Intervall"):
    try:
        analysis = vision_handler.analyze_image(screenshot)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory_entry = (
            f"[Vision] Analyse am {timestamp} (Grund: {reason}):\n"
            f"{analysis}"
        )
        add_memory(content=memory_entry, category="vision", tags=["screen", "context"])
        print(f"[Live-Vision] 📸 Analyse gespeichert ({reason})")
        return analysis
    except Exception as e:
        print(f"[Live-Vision] ❌ Fehler bei der Analyse: {e}")
        return None

# ==========================
# Reaktionssystem mit Spam-Filter
# ==========================
def process_pending_changes():
    """Fasst gesammelte Änderungen zusammen und reagiert."""
    global pending_changes, last_reaction_time
    if not pending_changes:
        return

    combined_context = "\n".join(pending_changes)
    prompt = (
        "Du bist Kimba, meine ständige virtuelle Begleiterin.\n"
        "Es gab mehrere große Änderungen auf meinem Bildschirm.\n"
        f"Das habe ich gesehen:\n{combined_context}\n"
        "Formuliere eine kurze, freundliche Reaktion, in der du mich fragst, "
        "ob ich mehr zu einer der Änderungen wissen möchte."
    )
    reaction = llm.ask(prompt)
    print(f"[Live-Vision] 💬 Kimba reagiert (kombiniert): {reaction}")

    if reaction_callback:
        reaction_callback(reaction)

    # Reset
    pending_changes.clear()
    last_reaction_time = time.time()

def queue_major_change_reaction(analysis_text):
    """Fügt eine Änderung zur Warteschlange hinzu und prüft, ob reagiert werden soll."""
    global pending_changes, last_reaction_time
    pending_changes.append(analysis_text)

    if time.time() - last_reaction_time >= REACTION_COOLDOWN:
        process_pending_changes()

# ==========================
# Hauptloop
# ==========================
def run_live_vision():
    global last_hash, last_reaction_time
    last_analysis_time = 0

    while VISION_RUNNING:
        screenshot = capture_screenshot()
        current_hash = imagehash.average_hash(screenshot)

        if last_hash is None:
            analysis = analyze_and_save(screenshot, reason="Erste Aufnahme")
            last_hash = current_hash
            last_analysis_time = time.time()

        else:
            diff = abs(current_hash - last_hash)

            # Major Change → in Warteschlange legen
            if diff >= HASH_THRESHOLD:
                analysis = analyze_and_save(screenshot, reason="Major Change")
                if analysis:
                    queue_major_change_reaction(analysis)
                last_hash = current_hash
                last_analysis_time = time.time()

            # Intervall-Analyse
            elif time.time() - last_analysis_time >= VISION_INTERVAL:
                analyze_and_save(screenshot, reason="Intervall")
                last_hash = current_hash
                last_analysis_time = time.time()

        time.sleep(CHECK_FREQUENCY)

# ==========================
# Start / Stop
# ==========================
def start_live_vision_in_background():
    global VISION_RUNNING
    VISION_RUNNING = True
    thread = threading.Thread(target=run_live_vision, daemon=True)
    thread.start()
    print("[Live-Vision] 🚀 Hintergrund-Vision gestartet.")

def stop_live_vision():
    global VISION_RUNNING
    VISION_RUNNING = False
    print("[Live-Vision] ⏹ Gestoppt.")
