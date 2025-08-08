import os
import re
from modules.git_assistant import analyze_project
from core.longterm_memory import save_memory_entry
from core.mood_engine import update_current_mood
from modules.response_style import respond

def suggest_refactor(path):
    """
    EN: Scans a given source file and suggests refactorings based on basic heuristics.
    DE: Durchsucht eine Quelldatei und gibt Vorschläge zur Refaktorierung auf Basis einfacher Heuristiken.

    Args:
        path (str): Path to a Python file.

    Returns:
        list[tuple[int, str]]: List of (line number, suggestion) tuples.
    """
    suggestions = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if len(line.strip()) > 80:
            suggestions.append((i + 1, "Zeile ist sehr lang"))
        if "==" in line and "if" not in line and not line.strip().startswith("#"):
            suggestions.append((i + 1, "Vergleich möglicherweise außerhalb eines if-Statements"))
        if "import" in line and "," in line:
            suggestions.append((i + 1, "Mehrere Imports in einer Zeile trennen"))

    return suggestions

def enter_code_assistant(project_path="."):
    """
    EN: Launches the Kimba Code Assistant. It analyzes each Python file in a given project folder,
    suggests improvements, and stores them in memory.

    DE: Startet den Kimba-Codeassistenten. Analysiert Python-Dateien im Projektordner,
    gibt Verbesserungsvorschläge aus und speichert diese im Langzeitspeicher.

    Args:
        project_path (str): Path to the root directory of the codebase.
    """
    print("🧪 Kimba Code-Assistent gestartet.")
    update_current_mood("neugierig")

    files = analyze_project(project_path)
    for path in files:
        print(f"🔍 Scanne: {path}")
        findings = suggest_refactor(path)
        if findings:
            print(f"⚠️ Verbesserungsvorschläge für {os.path.basename(path)}:")
            for line, msg in findings:
                print(f"  → Zeile {line}: {msg}")
            save_memory_entry(
                f"Verbesserungsvorschläge für {os.path.basename(path)}",
                mood="neugierig",
                tags=["code", "analyse"]
            )
        else:
            print(f"✅ {os.path.basename(path)} sieht gut aus!")

    print(respond("neugierig"))

# 🧪 Manuell testbar
if __name__ == "__main__":
    enter_code_assistant()
