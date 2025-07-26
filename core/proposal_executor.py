"""
🛠️ proposal_executor.py
EN: Executes GPT-generated upgrade proposals by generating and saving new modules.
DE: Führt von GPT generierte Verbesserungsvorschläge aus, erstellt neue Module.
"""

import openai
import os
from datetime import datetime

def generate_module_code(proposal_text):
    """
    EN: Prompts GPT to generate a Python module based on a proposal.
    DE: Fragt GPT, ein Python-Modul basierend auf einem Vorschlag zu erstellen.
    """
    prompt = f"""
You are Kimba's coding brain.
Based on the following improvement proposal, write a new modular Python file.

Rules:
- Use clean, well-structured Python 3.10+
- Add bilingual (English + German) docstrings
- Only output code, no explanations

Proposal:
{proposal_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def save_module(code, name=None, folder="proposals/generated_modules"):
    """
    Speichert das generierte Modul im Vorschlagsordner.
    """
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = name or f"module_{timestamp}.py"
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return path

def execute_proposal(proposal_text):
    """
    Führt den gesamten Erstellungsprozess aus.
    """
    print("🧠 Generiere Modul aus Vorschlag ...")
    code = generate_module_code(proposal_text)
    file_path = save_module(code)
    print(f"✅ Modul gespeichert unter: {file_path}")
    return file_path

# ▶️ Testlauf
if __name__ == "__main__":
    sample = "Kimba sollte ein Modul bekommen, das Wetterdaten lokal speichert und stimmungsabhängig nutzt."
    execute_proposal(sample)
