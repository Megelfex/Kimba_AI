import os
import time
import threading
from datetime import datetime
from core.proposal_executor import execute_proposal
from core.longterm_memory import add_memory

# Ordner, in dem genehmigte Vorschläge liegen
APPROVED_DIR = "proposals/approved"
# Intervall in Sekunden (z. B. 1800 = 30 Minuten)
EXECUTOR_INTERVAL = 1800

AUTO_EXECUTOR_RUNNING = True

def run_auto_executor():
    """Führt genehmigte Vorschläge automatisch aus."""
    while AUTO_EXECUTOR_RUNNING:
        try:
            if not os.path.exists(APPROVED_DIR):
                os.makedirs(APPROVED_DIR, exist_ok=True)

            approved_files = [f for f in os.listdir(APPROVED_DIR) if f.endswith(".txt")]

            if approved_files:
                for proposal_file in approved_files:
                    file_path = os.path.join(APPROVED_DIR, proposal_file)

                    with open(file_path, "r", encoding="utf-8") as f:
                        proposal_text = f.read()

                    print(f"[Auto-Executor] 🚀 Starte Umsetzung von: {proposal_file}")
                    try:
                        new_module_path = execute_proposal(proposal_text)
                        msg = (
                            f"Automatische Umsetzung am {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n"
                            f"- Vorschlag: {proposal_file}\n"
                            f"- Modul gespeichert unter: {new_module_path}"
                        )
                        add_memory(content=msg, category="auto_executor", tags=["projekt", "umsetzung"])
                        print(f"[Auto-Executor] ✅ Fertig: {proposal_file}")

                        # Verschiebe umgesetzte Vorschläge in "archived"
                        archived_dir = "proposals/archived"
                        os.makedirs(archived_dir, exist_ok=True)
                        os.rename(file_path, os.path.join(archived_dir, proposal_file))

                    except Exception as e:
                        print(f"[Auto-Executor] ❌ Fehler bei {proposal_file}: {e}")

            else:
                print("[Auto-Executor] Keine genehmigten Vorschläge gefunden.")

        except Exception as e:
            print(f"[Auto-Executor] ❌ Fehler: {e}")

        time.sleep(EXECUTOR_INTERVAL)


def start_auto_executor_in_background():
    """Startet den Auto-Executor im Hintergrund."""
    thread = threading.Thread(target=run_auto_executor, daemon=True)
    thread.start()
    print("[Auto-Executor] 🚀 Hintergrund-Executor gestartet.")


def stop_auto_executor():
    """Stoppt den Auto-Executor."""
    global AUTO_EXECUTOR_RUNNING
    AUTO_EXECUTOR_RUNNING = False
    print("[Auto-Executor] ⏹ Gestoppt.")
