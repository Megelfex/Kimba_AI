import os
import threading
from visual.interface import launch_gui
from core.llm_router import KimbaLLM
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity
from core.kimba_core import start_core

def launch_trigger():
    os.system("python event_triggers_v3.py")

def main():
    print("🧠 Kimba vX wird gestartet ...")

    # Kimba lädt ihre Identität
    identity = load_identity("identity/personality.json")
    print(f"🧬 Geladene Identität: {identity['identity']['role']}")

    # Initialisiere Gedächtnis
    memory = KimbaMemory("memory/kimba_memory/")

    # Initialisiere LLM-Schnittstelle
    llm = KimbaLLM(model=identity['identity']['version'], mode="auto")

    # Starte Kimba Core (Bewusstsein, Desktop-Verknüpfung etc.)
    start_core()

    # Starte Trigger-System
    threading.Thread(target=launch_trigger).start()

    # Starte grafische Oberfläche
    launch_gui(llm, memory, identity)

if __name__ == "__main__":
    main()
