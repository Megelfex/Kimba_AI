import os
import subprocess
from datetime import datetime
from core.longterm_memory import save_memory_entry
from core.mood_engine import update_current_mood
from modules.response_style import respond

def analyze_project(path="."):
    print("🔍 Kimba schaut sich dein Projekt an...")
    update_current_mood("fokussiert")
    save_memory_entry("Kimba hat ein Projekt analysiert.", mood="fokussiert", tags=["projekt", "analyse"])

    # Liste aller Python-Dateien
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".py") and not f.startswith("test_"):
                files.append(os.path.join(root, f))

    print(respond("fokussiert"))
    print(f"📂 {len(files)} Python-Datei(en) gefunden.")
    return files

def get_git_status():
    try:
        output = subprocess.check_output(["git", "status", "--short"], text=True)
        return output.strip()
    except Exception:
        return "❌ Kein Git-Repo gefunden."

def commit_changes(message="Auto-Commit von Kimba"):
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
    status = get_git_status()
    if status == "":
        return "📦 Alles ist aktuell – keine Änderungen."
    else:
        lines = status.split("\n")
        summary = [f"🔸 {line}" for line in lines]
        return "\n".join(summary)

# Beispiel
if __name__ == "__main__":
    print("🧠 Kimba Git-Assistant aktiviert!")
    print(get_git_status())
    print(suggest_change_summary())
