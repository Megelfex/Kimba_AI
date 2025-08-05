import os
from datetime import datetime
from core.project_analyzer import analyze_report
from core.longterm_memory import add_memory

class ProposalHandler:
    """
    EN: Handles proposals generated either automatically from project analysis or stored in text files.
    DE: Verarbeitet Vorschläge, die entweder automatisch aus der Projektanalyse erstellt oder als Textdateien gespeichert sind.
    """

    def __init__(self, proposal_dir="proposals"):
        self.proposal_dir = proposal_dir
        os.makedirs(self.proposal_dir, exist_ok=True)

    # -----------------------------
    # 1. Automatische Vorschläge aus der Analyse
    # -----------------------------
    def generate_proposals_from_analysis(self):
        """
        DE: Liest die Projektanalyse und erzeugt daraus Vorschläge.
        EN: Reads the project analysis and generates proposals.
        """
        analysis_text = analyze_report()
        proposals = []

        for line in analysis_text.split("\n"):
            if line.strip().startswith("- "):
                proposals.append(line.strip("- ").strip())

        if not proposals:
            proposals.append("✨ Keine automatischen Vorschläge erkannt – bitte manuell Aufgaben setzen.")

        # Priorisierung: fehlende Features > technische Fixes > Cleanup
        proposals.sort(key=lambda p: (
            "Keine" in p or "fehlend" in p,
            "Overlay" in p or "Kimba" in p or "Iuno" in p,
            "Aufräumen" in p or "Archivieren" in p
        ), reverse=True)

        return proposals

    def formatted_proposals(self):
        """
        DE: Gibt formatierte Vorschläge zurück, die im Chat anzeigt werden können.
        EN: Returns formatted proposals for chat display.
        """
        proposals = self.generate_proposals_from_analysis()
        output = "✨ Basierend auf meiner Analyse könnten wir Folgendes tun:\n"
        for i, p in enumerate(proposals, start=1):
            output += f"{i}. {p}\n"
        output += "\n❓ Was möchtest du zuerst angehen?"
        return output

    # -----------------------------
    # 2. Vorschläge aus gespeicherten Dateien
    # -----------------------------
    def list_proposals(self):
        """
        DE: Listet gespeicherte Vorschlagsdateien im proposals-Ordner.
        EN: Lists stored proposal files in the proposals folder.
        """
        files = [f for f in os.listdir(self.proposal_dir) if f.endswith(".txt")]
        return files if files else ["(Keine gespeicherten Vorschläge gefunden)"]

    def read_proposal(self, filename):
        """
        DE: Liest eine gespeicherte Vorschlagsdatei.
        EN: Reads a stored proposal file.
        """
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def save_proposal(self, title, content):
        """
        DE: Speichert einen neuen Vorschlag als .txt-Datei.
        EN: Saves a new proposal as a .txt file.
        """
        safe_title = title.replace(" ", "_").replace("/", "_")[:50]
        path = os.path.join(self.proposal_dir, f"{safe_title}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Vorschlag gespeichert unter: {path}"

    # -----------------------------
    # 3. Verwaltung von Vorschlägen
    # -----------------------------
    def reject_proposal(self, proposal_text):
        """
        DE: Speichert die Ablehnung eines Vorschlags im Langzeitgedächtnis.
        EN: Saves the rejection of a proposal in the long-term memory.
        """
        add_memory(
            content=f"Am {datetime.now().strftime('%d.%m.%Y')} Vorschlag '{proposal_text[:80]}...' abgelehnt.",
            category="rejected_task",
            tags=["proposal", "rejected"]
        )
        return f"❌ Vorschlag abgelehnt: {proposal_text}"

    def confirm_proposal(self, proposal_text):
        """
        DE: Speichert die Bestätigung eines Vorschlags im Langzeitgedächtnis (falls nicht direkt ausgeführt).
        EN: Saves the confirmation of a proposal in the long-term memory (if not executed immediately).
        """
        add_memory(
            content=f"Am {datetime.now().strftime('%d.%m.%Y')} Vorschlag '{proposal_text[:80]}...' bestätigt.",
            category="approved_task",
            tags=["proposal", "approved"]
        )
        return f"✅ Vorschlag bestätigt: {proposal_text}"

    def execute_proposal(self, filename):
        """
        DE: Führt den Python-Code aus, der in einer Vorschlagsdatei enthalten ist.
        EN: Executes Python code contained in a proposal file.
        """
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            if "Code:" not in content:
                return "⚠️ Kein Codeblock gefunden."
            code_block = content.split("Code:\n")[1].split("\n\nRisiko:")[0]
            exec(code_block, globals())
            return f"✅ Vorschlag aus {filename} wurde ausgeführt."
        except Exception as e:
            return f"❌ Fehler beim Ausführen: {e}"
