import os
import datetime

class KimbaSelfMod:
    """
    EN: Handles self-generated modification proposals and applies low-risk changes automatically.
    DE: Verarbeitet selbstgenerierte Änderungsvorschläge und wendet risikoarme Änderungen automatisch an.
    """

    def __init__(self, proposals_path="proposals/"):
        """
        EN: Initializes the self-mod engine with the path to store proposals.
        DE: Initialisiert die Self-Mod-Engine mit dem Pfad für Vorschlagsdateien.

        Args:
            proposals_path (str): Directory where proposals will be saved.
        """
        self.proposals_path = proposals_path
        self.safe_zones = ["dialog_prompter", "task_manager.json", "identity"]

    def evaluate_change(self, module, description, code_block):
        """
        EN: Evaluates a proposed code change and either applies it (if safe) or logs it for approval.
        DE: Bewertet eine vorgeschlagene Code-Änderung und übernimmt sie (falls sicher) oder speichert sie zur Freigabe.

        Args:
            module (str): Name or path of the module to be changed.
            description (str): Human-readable explanation of the change.
            code_block (str): Python code to be executed or stored.

        Returns:
            str: Feedback message indicating outcome (executed or pending approval).
        """
        severity = self.assess_risk(module)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.proposals_path}/proposal_{module}_{timestamp}.txt"
        content = f"""# Änderungsvorschlag
Modul: {module}

Beschreibung:
{description}

Code:
{code_block}

Risiko: {severity}"""

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        if severity == "high":
            return f"🛑 Änderung gespeichert, aber wartet auf deine Freigabe: {filename}"
        else:
            exec(code_block, globals())
            return f"✅ Kleine Änderung sofort übernommen."

    def assess_risk(self, module):
        """
        EN: Determines the risk level of modifying a module.
        DE: Bewertet das Risiko einer Modifikation anhand des Modulpfads.

        Args:
            module (str): Target module name or path.

        Returns:
            str: "low" or "high" indicating risk level.
        """
        if any(safe in module for safe in self.safe_zones):
            return "low"
        return "high"
