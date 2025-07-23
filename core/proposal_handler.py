import os

class ProposalHandler:
    """
    EN: Handles GPT-generated proposal files for review and optional execution.
    DE: Verarbeitet von GPT-generierte Vorschlagsdateien zur Anzeige und optionalen Ausführung.
    """

    def __init__(self, proposal_dir="proposals"):
        """
        EN: Initializes the handler with a directory where proposals are stored.
        DE: Initialisiert den Handler mit dem Verzeichnis, in dem die Vorschläge gespeichert sind.

        Args:
            proposal_dir (str): Directory path containing proposal text files.
        """
        self.proposal_dir = proposal_dir

    def list_proposals(self):
        """
        EN: Lists all available .txt proposals in the proposals directory.
        DE: Listet alle verfügbaren .txt-Vorschläge im Verzeichnis auf.

        Returns:
            list[str]: List of filenames or a message if none found.
        """
        files = [f for f in os.listdir(self.proposal_dir) if f.endswith(".txt")]
        return files if files else ["(Keine Vorschläge gefunden)"]

    def read_proposal(self, filename):
        """
        EN: Loads and returns the content of a proposal file.
        DE: Lädt und gibt den Inhalt einer Vorschlagsdatei zurück.

        Args:
            filename (str): Name of the .txt file to read.

        Returns:
            str: File content or error message if not found.
        """
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def execute_proposal(self, filename):
        """
        EN: Attempts to execute the Python code block found in a proposal file.
        DE: Versucht, den Python-Code-Block in einer Vorschlagsdatei auszuführen.

        Expected format in file:
            Code:
            <Python-Code>

            Risiko:
            <Einschätzung>

        Args:
            filename (str): Name of the file to execute.

        Returns:
            str: Success or error message.
        """
        path = os.path.join(self.proposal_dir, filename)
        if not os.path.exists(path):
            return "❌ Vorschlag nicht gefunden."

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            code_block = content.split("Code:\n")[1].split("\n\nRisiko:")[0]
            exec(code_block, globals())
            return f"✅ Vorschlag aus {filename} wurde ausgeführt."
        except Exception as e:
            return f"❌ Fehler beim Ausführen: {e}"
