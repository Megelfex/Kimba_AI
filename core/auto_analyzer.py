import os
import time
import threading
from datetime import datetime
from core.project_analyzer import scan_project
from core.longterm_memory import add_memory

# Intervall in Sekunden (z. B. 3600 = 1 Stunde)
ANALYZE_INTERVAL = 3600

AUTO_ANALYZER_RUNNING = True

def run_auto_analyzer():
    """Startet den Auto-Analyzer im Hintergrund."""
    while AUTO_ANALYZER_RUNNING:
        try:
            print("[Auto-Analyzer] 🔍 Starte automatische Projektanalyse...")
            report = scan_project()

            # Bericht ins Gedächtnis schreiben
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            memory_text = (
                f"Automatische Analyse am {timestamp}:\n"
                f"Sinnlos: {len(report['sinnlos'])} Dateien\n"
                f"Nicht genutzt: {len(report['nicht_genutzt'])} Dateien\n"
                f"Veraltet: {len(report['veraltet'])} Dateien\n"
                f"→ Vollständiger Bericht gespeichert."
            )
            add_memory(content=memory_text, category="auto_analysis", tags=["projekt", "analyse"])

            print("[Auto-Analyzer] ✅ Analyse abgeschlossen und ins Gedächtnis gespeichert.")

        except Exception as e:
            print(f"[Auto-Analyzer] ❌ Fehler: {e}")

        # Warten bis zum nächsten Durchlauf
        time.sleep(ANALYZE_INTERVAL)


def start_auto_analyzer_in_background():
    """Startet den Analyzer als separaten Thread."""
    thread = threading.Thread(target=run_auto_analyzer, daemon=True)
    thread.start()
    print("[Auto-Analyzer] 🚀 Hintergrund-Analyzer gestartet.")


def stop_auto_analyzer():
    """Stoppt den Analyzer."""
    global AUTO_ANALYZER_RUNNING
    AUTO_ANALYZER_RUNNING = False
    print("[Auto-Analyzer] ⏹ Gestoppt.")
