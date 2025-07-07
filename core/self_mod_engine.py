
import os
import datetime

class KimbaSelfMod:
    def __init__(self, proposals_path="proposals/"):
        self.proposals_path = proposals_path
        self.safe_zones = ["dialog_prompter", "task_manager.json", "identity"]

    def evaluate_change(self, module, description, code_block):
        severity = self.assess_risk(module)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.proposals_path}/proposal_{module}_{timestamp}.txt"
        content = f"# Änderungsvorschlag
Modul: {module}

Beschreibung:
{description}

Code:
{code_block}

Risiko: {severity}"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        if severity == "high":
            return f"🛑 Änderung gespeichert, aber wartet auf deine Freigabe: {filename}"
        else:
            exec(code_block, globals())
            return f"✅ Kleine Änderung sofort übernommen."

    def assess_risk(self, module):
        if any(safe in module for safe in self.safe_zones):
            return "low"
        return "high"
