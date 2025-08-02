import os
import threading
from visual.interface import launch_gui
from archive.llm_router import KimbaLLMRouter
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity
from archive.kimba_core import start_core

def launch_trigger():
    """
    EN: Starts the external event trigger system (e.g., desktop monitoring).
    DE: Startet das externe Ereignis-Trigger-System (z. B. Desktop-Überwachung).
    """
    os.system("python modules/event_triggers_v3.py")

def main():
    """
    EN: Main entry point of Kimba vX.
    Loads identity, initializes memory and language model,
    starts internal core (self-awareness), launches event triggers and GUI.

    DE: Haupteinstiegspunkt von Kimba vX.
    Lädt die Identität, initialisiert Gedächtnis & Sprachmodell,
    startet Kimba Core (Selbstbewusstsein), Trigger und GUI.
    """
    print("🧠 Kimba vX wird gestartet ...")

    # 🧬 Load identity
    identity = load_identity("identity/personality.json")
    print(f"🧬 Geladene Identität: {identity['identity']['role']}")

    # 🧠 Initialize long-term memory
    memory = KimbaMemory("memory/kimba_memory/")

    # 🔤 Initialize language model (LLM)
    llm = KimbaLLMRouter()

    # 🔁 Start Kimba Core (self-awareness, reasoning loop, mood sync)
    start_core()

    # 🖥️ Launch background trigger system (file events, idle check, etc.)
    threading.Thread(target=launch_trigger).start()

    # 🎨 Start GUI
    launch_gui()

from visual.interface import launch_gui

# ▶️ Direct start if run as main
if __name__ == "__main__":
    main()
