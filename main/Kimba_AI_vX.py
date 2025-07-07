
# Kimba vX – Hauptmodul
# Starte dein Soulmate-Interface & Routing

import os
import sys
from visual.interface import launch_gui
from core.llm_router import KimbaLLM
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity

def main():
    print("🧠 Kimba vX wird gestartet ...")

    # Kimba lädt ihre Identität
    identity = load_identity("identity/personality.json")
    print(f"🧬 Geladene Identität: {identity['identity']['role']}")

    # Initialisiere Gedächtnis
    memory = KimbaMemory("memory/kimba_memory/")

    # Initialisiere LLM-Schnittstelle
    llm = KimbaLLM(model=identity['version'], mode="auto")

    # Starte grafische Oberfläche
    launch_gui(llm, memory, identity)

if __name__ == "__main__":
    main()
