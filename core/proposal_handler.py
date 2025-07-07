
import os

class ProposalHandler:
    def __init__(self, proposal_dir="proposals"):
        self.proposal_dir = proposal_dir

    def list_proposals(self):
        files = [f for f in os.listdir(self.proposal_dir) if f.endswith(".txt")]
        return files if files else ["(Keine Vorschläge gefunden)"]

    def read_proposal(self, filename):
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def execute_proposal(self, filename):
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            code_block = content.split("Code:
")[1].split("

Risiko:")[0]
            exec(code_block, globals())
            return f"✅ Vorschlag aus {filename} wurde ausgeführt."
        except Exception as e:
            return f"❌ Fehler beim Ausführen: {e}"
