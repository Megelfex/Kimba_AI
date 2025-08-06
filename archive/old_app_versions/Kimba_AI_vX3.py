
"""
Kimba AI vX - Main Entry Point
==============================
DE: Hauptstarter für die Kimba-KI. Lädt alle Kernmodule, initialisiert Speicher & Sprachmodell,
    startet Kernprozesse, Trigger-Systeme und wahlweise die Benutzeroberflächen.

EN: Main launcher for the Kimba AI. Loads all core modules, initializes memory & language model,
    starts core processes, trigger systems, and optionally the user interfaces.
"""

import os
import threading
import logging
import argparse
from visual.interface import launch_gui
from core.llm_router import KimbaLLMRouter
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity
from core.kimba_core import run_core_cycle

# Logging-Konfiguration / Logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def launch_trigger():
    """
    DE: Startet das externe Ereignis-Trigger-System (z. B. Desktop-Überwachung).
    EN: Starts the external event trigger system (e.g., desktop monitoring).
    """
    logging.info("Starting event trigger system...")
    os.system("python modules/event_triggers_v3_clean.py")


def main(start_gui=True, start_triggers=True):
    """
    DE: Haupteinstiegspunkt von Kimba vX.
        Lädt Identität, initialisiert Gedächtnis & Sprachmodell, startet Kernprozesse,
        optional Trigger-System und GUI.

    EN: Main entry point of Kimba vX.
        Loads identity, initializes memory & language model, starts core processes,
        optionally the trigger system and GUI.

    Args:
        start_gui (bool): Falls True, GUI starten / If True, start GUI.
        start_triggers (bool): Falls True, Trigger-System starten / If True, start trigger system.
    """
    logging.info("🧠 Starting Kimba vX...")

    # 🧬 Load identity
    try:
        identity = load_identity("identity/personality.json")
        logging.info(f"🧬 Identity loaded: {identity['identity']['role']}")
    except Exception as e:
        logging.error(f"Failed to load identity: {e}")
        return

    # 🧠 Initialize long-term memory
    try:
        memory = KimbaMemory("memory/kimba_memory/")
        logging.info("💾 Long-term memory initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize memory: {e}")
        return

    # 🔤 Initialize language model (LLM)
    try:
        llm = KimbaLLMRouter()
        logging.info("🔤 LLM Router initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize LLM Router: {e}")
        return

    # 🔁 Start Kimba Core (self-awareness, reasoning loop, mood sync)
    run_core_cycle()

    # 🖥️ Launch background trigger system
    if start_triggers:
        threading.Thread(target=launch_trigger, daemon=True).start()

    # 🎨 Start GUI
    if start_gui:
        launch_gui()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Kimba AI vX")
    parser.add_argument("--no-gui", action="store_true", help="Start without GUI")
    parser.add_argument("--no-triggers", action="store_true", help="Start without event triggers")
    args = parser.parse_args()

    main(start_gui=not args.no_gui, start_triggers=not args.no_triggers)
