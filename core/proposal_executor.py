"""
🛠️ proposal_executor.py
EN: Executes AI-generated improvement proposals by creating or updating Python modules.
DE: Führt KI-generierte Verbesserungsvorschläge aus, erstellt oder aktualisiert Python-Module.
"""

import os
from datetime import datetime
from core.llm_router import KimbaLLMRouter
from core.file_editor import create_file
from core.longterm_memory import add_memory
from dotenv import load_dotenv

load_dotenv()

# LLM-Instanz (nutzt API-First + Local-Fallback)
llm = KimbaLLMRouter()

def generate_module_code(proposal_text):
    """
    EN: Generates Python module code from a proposal using Kimba's LLM router.
    DE: Generiert Python-Modulcode aus einem Vorschlag über Kimbas LLM-Router.
    """
    prompt = f"""
You are Kimba's coding brain.
Based on the following improvement proposal, write a new modular Python 3.10+ file.

Rules:
- Use clean, well-structured Python
- Add bilingual (English + German) docstrings for every class and function
- Only output code, no explanations or markdown
- Keep it self-contained unless specified otherwise

Proposal:
{proposal_text}
    """
    code = llm.ask(prompt)
    return code.strip()

def save_module(code, name=None, folder="proposals/generated_modules"):
    """
    EN: Saves the generated module using file_editor (with backup & logging).
    DE: Speichert das generierte Modul mit file_editor (inkl. Backup & Logging).
    """
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = name or f"module_{timestamp}.py"
    path = os.path.join(folder, filename)
    create_file(path, code)  # nutzt file_editor mit Backup & Logging
    return path

def execute_proposal(proposal_text, module_name=None, target_folder="proposals/generated_modules", auto_run=False):
    """
    EN: Executes the entire process: generate -> save -> (optional) run.
    DE: Führt den gesamten Prozess aus: generieren -> speichern -> (optional) ausführen.

    Args:
        proposal_text (str): Description of the feature to implement.
        module_name (str): Optional custom filename.
        target_folder (str): Directory where the module will be saved.
        auto_run (bool): If True, executes the module after saving.
    """
    print("🧠 Generiere Modul aus Vorschlag ...")
    code = generate_module_code(proposal_text)
    file_path = save_module(code, name=module_name, folder=target_folder)
    print(f"✅ Modul gespeichert unter: {file_path}")

    # 📝 Automatische Speicherung ins Langzeitgedächtnis
    add_memory(
        content=f"Am {datetime.now().strftime('%d.%m.%Y')} Vorschlag '{proposal_text[:80]}...' umgesetzt.",
        category="completed_task",
        tags=["proposal", "completed"]
    )

    if auto_run:
        print(f"▶️ Starte Modul {file_path} ...")
        os.system(f'python "{file_path}"')

    return file_path

# ▶️ Testlauf
if __name__ == "__main__":
    sample = "Kimba sollte ein Modul bekommen, das Wetterdaten lokal speichert und stimmungsabhängig nutzt."
    execute_proposal(sample, auto_run=False)
