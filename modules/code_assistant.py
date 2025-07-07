import os
import re
from modules.git_assistant import analyze_project
from core.longterm_memory import save_memory_entry
from core.mood_engine import update_current_mood
from modules.response_style import respond

def suggest_refactor(path):
    suggestions = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if len(line.strip()) > 80:
            suggestions.append((i + 1, "Zeile ist sehr lang"))
        if "==" in line and "if" not in line and "==" not in line.strip().startswith("#"):
            suggestions.append((i + 1, "Vergleich möglicherweise außerhalb eines if-Statements"))
        if "import" in line and "," in line:
            suggestions.append((i + 1, "Mehrere Imports in einer Zeile trennen"))

    return suggestions

def enter_code_assistant(project_path="."):
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
            save_memory_entry(f"Verbesserungsvorschläge für {os.path.basename(path)}", mood="neugierig", tags=["code", "analyse"])
        else:
            print(f"✅ {os.path.basename(path)} sieht gut aus!")

    print(respond("neugierig"))

# Beispiel
if __name__ == "__main__":
    enter_code_assistant()
