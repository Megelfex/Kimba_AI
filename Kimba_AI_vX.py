import os
import threading
from visual.interface import launch_gui
from core.llm_router import KimbaLLM
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity
from core.kimba_core import start_core

def launch_trigger():
    """
    EN: Starts the external event trigger system (e.g., desktop monitoring).
    DE: Startet das externe Ereignis-Trigger-System (z. B. Desktop-Überwachung).
    """
    os.system("python event_triggers_v3.py")

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
    llm = KimbaLLM(model=identity['identity']['version'], mode="auto")

    # 🔁 Start Kimba Core (self-awareness, reasoning loop, mood sync)
    start_core()

    # 🖥️ Launch background trigger system (file events, idle check, etc.)
    threading.Thread(target=launch_trigger).start()

    # 🎨 Start GUI
    launch_gui(llm, memory, identity)

# ▶️ Direct start if run as main
if __name__ == "__main__":
    main()
