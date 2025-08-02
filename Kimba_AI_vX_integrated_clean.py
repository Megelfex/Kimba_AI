"""
Kimba AI vX - Integrated Clean Version (GUI als Hauptkommunikationszentrum)
==========================================================================

DE: Hauptstarter für Kimba mit der erweiterten Terminal-GUI als Standard.
    Startet immer die GUI, Event-Trigger und optional die Desktop-Katze.

EN: Main launcher for Kimba with the extended Terminal GUI as the default.
    Always launches the GUI, event triggers, and optionally the desktop cat.
"""

import threading
import logging
import argparse

from visual.kimba_terminal_ui import KimbaTerminalUI
from core.llm_router import KimbaLLMRouter
from core.memory_store import KimbaMemory
from identity.identity_engine import load_identity
from core.kimba_core import run_core_cycle
from modules.event_triggers_v3 import start_desktop_watcher
from desktop_kimba.kimba_desktop_cat import AnimatedCat

# Logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def main(start_triggers=True, start_cat=False):
    """DE: Startet Kimba mit GUI, Triggern und optional Desktop-Katze.
       EN: Starts Kimba with GUI, triggers, and optionally desktop cat."""
    logging.info("🧠 Starting Kimba Clean Version with GUI...")

    # 🧬 Identity
    try:
        identity = load_identity("identity/personality.json")
        logging.info(f"🧬 Identity loaded: {identity['identity']['role']}")
    except Exception as e:
        logging.error(f"Failed to load identity: {e}")
        return

    # 💾 Memory
    try:
        memory = KimbaMemory("memory/kimba_memory/")
        logging.info("💾 Long-term memory initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize memory: {e}")
        return

    # 🔤 LLM Router
    try:
        llm = KimbaLLMRouter()
        logging.info("🔤 LLM Router initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize LLM Router: {e}")
        return

    # 🔁 Core Cycle
    run_core_cycle()

    # Trigger
    if start_triggers:
        threading.Thread(target=start_desktop_watcher, daemon=True).start()

    # Desktop Cat
    if start_cat:
        threading.Thread(target=lambda: AnimatedCat().mainloop(), daemon=True).start()

    # 🎨 Start GUI
    KimbaTerminalUI().run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start Kimba with GUI as Main Interface")
    parser.add_argument("--no-triggers", action="store_true", help="Disable event triggers")
    parser.add_argument("--cat", action="store_true", help="Start desktop cat")
    args = parser.parse_args()

    main(start_triggers=not args.no_triggers, start_cat=args.cat)
