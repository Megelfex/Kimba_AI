import time
from tools.system_control import KimbaSystem

class KimbaTaskLoop:
    """
    EN: Simple task queue and runner that executes registered functions with optional arguments.
    DE: Einfache Aufgabenwarteschlange, die registrierte Funktionen mit optionalen Argumenten ausführt.
    """

    def __init__(self):
        """
        EN: Initializes the task loop and connects to Kimba's system control module.
        DE: Initialisiert die Task-Schleife und verbindet sich mit dem Kimba-Systemkontrollmodul.
        """
        self.system = KimbaSystem()
        self.tasks = []

    def add_task(self, func, *args):
        """
        EN: Adds a function with arguments to the task queue.
        DE: Fügt eine Funktion mit Argumenten zur Aufgabenliste hinzu.

        Args:
            func (callable): The function to execute.
            *args: Arguments to be passed to the function.
        """
        self.tasks.append((func, args))

    def run(self):
        """
        EN: Executes all tasks in the queue one after another. Logs success or errors.
        DE: Führt alle Aufgaben in der Warteschlange nacheinander aus. Gibt Erfolg oder Fehler aus.
        """
        while self.tasks:
            func, args = self.tasks.pop(0)
            try:
                result = func(*args)
                print(f"✅ Aufgabe ausgeführt: {result}")
            except Exception as e:
                print(f"❌ Fehler bei Aufgabe: {e}")
            time.sleep(1)  # kleine Pause zwischen Aufgaben
