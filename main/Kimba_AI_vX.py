# Kimba vX – Hauptmodul
# Starte dein Soulmate-Interface & Routing

import os
import sys
from visual.interface import launch_gui
from core.llm_router import KimbaLLM
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity

def main():
    """
    EN: Entry point of Kimba vX. Loads identity, initializes memory and language model,
    then launches the graphical interface.

    DE: Einstiegspunkt von Kimba vX. Lädt die Identität, initialisiert Gedächtnis und Sprachmodell
    und startet anschließend die grafische Oberfläche.
    """
    print("🧠 Kimba vX wird gestartet ...")

    # 🧬 Load personality profile
    identity = load_identity("identity/personality.json")
    print(f"🧬 Geladene Identität: {identity['identity']['role']}")

    # 🧠 Initialize memory system
    memory = KimbaMemory("memory/kimba_memory/")

    # 🔤 Initialize LLM interface
    llm = KimbaLLM(model=identity['identity']['version'], mode="auto")

    # 🎨 Launch visual interface
    launch_gui(llm, memory, identity)

# 🔁 Direktstart, wenn Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()
