import json
from core.task_loop import KimbaTaskLoop
from tools.dialog_prompter import KimbaDialog

class KimbaTaskEngine:
    """
    EN: Loads and executes scheduled tasks defined in a JSON file.
    DE: Lädt und führt geplante Aufgaben aus, die in einer JSON-Datei definiert sind.
    """


from modules.image_generation import comfy_engine, sd_engine
from modules import response_style

from archive.llm_router import KimbaLLMRouter

llm = KimbaLLMRouter()

antwort = llm.ask("Wie kann ich meinen eigenen Code verbessern?", purpose="code")
print(antwort)


def handle_image_task(prompt, purpose="default"):
    """
    Entscheidet automatisch, ob ComfyUI oder SD WebUI verwendet wird,
    und gibt einen passenden Antworttext + generiertes Bild zurück.
    
    Args:
        prompt (str): Der Textprompt für die Bildgenerierung.
        purpose (str): Optionaler Zweck oder Kontext der Anfrage.

    Returns:
        dict: Enthält Kimba-Antworttext und Bildpfad/URL.
    """
    try:
        if comfy_engine.is_comfyui_running():
            kimba_response = response_style.kimba_say(
                "Ich verwende ComfyUI für diese Bildgenerierung – es ist aktiv und optimal für diesen Fall."
            )
            image_url = comfy_engine.generate_image(prompt)
        else:
            kimba_response = response_style.kimba_say(
                "ComfyUI ist momentan nicht aktiv. Ich nutze stattdessen Stable Diffusion über SD WebUI."
            )
            image_url = sd_engine.generate_image(prompt, purpose)

        return {
            "message": kimba_response,
            "image_url": image_url
        }

    except Exception as e:
        return {
            "message": response_style.kimba_say(f"Fehler beim Generieren: {str(e)}"),
            "image_url": None
        }


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
