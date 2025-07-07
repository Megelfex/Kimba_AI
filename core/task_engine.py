
import json
from core.task_loop import KimbaTaskLoop
from tools.dialog_prompter import KimbaDialog

class KimbaTaskEngine:
    def __init__(self, task_file="config/task_manager.json"):
        self.task_loop = KimbaTaskLoop()
        self.dialog = KimbaDialog()
        with open(task_file, "r", encoding="utf-8") as f:
            self.tasks = json.load(f).get("tasks", [])

    def run(self):
        for task in self.tasks:
            if task.get("enabled", False) and task["id"] == "ask_user":
                question = self.dialog.ask_user()
                print(f"Kimba fragt: {question}")
            else:
                print(f"⏳ Keine Aufgabe ausgeführt: {task['id']}")
