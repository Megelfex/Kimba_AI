import json
from core.task_loop import KimbaTaskLoop
from tools.dialog_prompter import KimbaDialog

class KimbaTaskEngine:
    """
    EN: Loads and executes scheduled tasks defined in a JSON file.
    DE: Lädt und führt geplante Aufgaben aus, die in einer JSON-Datei definiert sind.
    """

    def __init__(self, task_file="config/task_manager.json"):
        """
        EN: Initializes the task engine and loads the task configuration.
        DE: Initialisiert die Task-Engine und lädt die Aufgaben-Konfiguration.

        Args:
            task_file (str): Path to the JSON file containing the task definitions.
        """
        self.task_loop = KimbaTaskLoop()
        self.dialog = KimbaDialog()
        with open(task_file, "r", encoding="utf-8") as f:
            self.tasks = json.load(f).get("tasks", [])

    def run(self):
        """
        EN: Executes all enabled tasks from the configuration. Currently supports:
            - Task ID "ask_user": Kimba asks a user-defined question via dialog module.

        DE: Führt alle aktivierten Aufgaben aus der Konfiguration aus. Unterstützt derzeit:
            - Task-ID "ask_user": Kimba stellt eine benutzerdefinierte Frage via Dialogmodul.
        """
        for task in self.tasks:
            if task.get("enabled", False) and task["id"] == "ask_user":
                question = self.dialog.ask_user()
                print(f"Kimba fragt: {question}")
            else:
                print(f"⏳ Keine Aufgabe ausgeführt: {task['id']}")
