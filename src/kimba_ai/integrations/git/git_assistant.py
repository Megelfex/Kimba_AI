import os
import subprocess
from datetime import datetime
from core.longterm_memory import save_memory_entry
from core.mood_engine import update_current_mood
from modules.response_style import respond

def analyze_project(path="."):
    """
    EN: Scans the project directory for Python source files (excluding tests).
    Updates mood and logs the analysis.

    DE: Durchsucht das Projektverzeichnis nach Python-Dateien (ohne Testdateien).
    Aktualisiert Stimmung und speichert Analyse im Gedächtnis.

    Args:
        path (str): Base directory to analyze

    Returns:
        list[str]: List of found .py files
    """
    print("🔍 Kimba schaut sich dein Projekt an...")
    update_current_mood("fokussiert")
    save_memory_entry("Kimba hat ein Projekt analysiert.", mood="fokussiert", tags=["projekt", "analyse"])

    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".py") and not f.startswith("test_"):
                files.append(os.path.join(root, f))

    print(respond("fokussiert"))
    print(f"📂 {len(files)} Python-Datei(en) gefunden.")
    return files

def get_git_status():
    """
    EN: Returns the current short Git status of the project.
    DE: Gibt den aktuellen Git-Status (kurzform) des Projekts zurück.

    Returns:
        str: Git status output or error message
    """
    try:
        output = subprocess.check_output(["git", "status", "--short"], text=True)
        return output.strip()
    except Exception:
        return "❌ Kein Git-Repo gefunden."

def commit_changes(message="Auto-Commit von Kimba"):
    """
    EN: Stages and commits all changes with a given commit message.
    Updates mood and memory log on success.

    DE: Fügt alle Änderungen zum Git-Index hinzu und committet sie mit Nachricht.
    Aktualisiert Stimmung und schreibt Eintrag ins Gedächtnis bei Erfolg.

    Args:
        message (str): Commit message (default is auto-generated)
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        mood = "dankbar"
        print("✅ Kimba: Änderungen gespeichert.")
        print(respond(mood))
        save_memory_entry("Kimba hat einen Git-Commit durchgeführt.", mood=mood, tags=["git", "commit"])
    except Exception as e:
        print(f"⚠️ Fehler beim Commit: {e}")

def suggest_change_summary():
    """
    EN: Summarizes the current Git changes in natural language.
    DE: Gibt eine kurze Zusammenfassung der aktuellen Git-Änderungen zurück.

    Returns:
        str: Summary string (or confirmation that nothing changed)
    """
    status = get_git_status()
    if status == "":
        return "📦 Alles ist aktuell – keine Änderungen."
    else:
        lines = status.split("\n")
        summary = [f"🔸 {line}" for line in lines]
        return "\n".join(summary)

# 🧪 Beispielstart
if __name__ == "__main__":
    print("🧠 Kimba Git-Assistant aktiviert!")
    print(get_git_status())
    print(suggest_change_summary())
