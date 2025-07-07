
import time
from tools.system_control import KimbaSystem

class KimbaTaskLoop:
    def __init__(self):
        self.system = KimbaSystem()
        self.tasks = []

    def add_task(self, func, *args):
        self.tasks.append((func, args))

    def run(self):
        while self.tasks:
            func, args = self.tasks.pop(0)
            try:
                result = func(*args)
                print(f"✅ Aufgabe ausgeführt: {result}")
            except Exception as e:
                print(f"❌ Fehler bei Aufgabe: {e}")
            time.sleep(1)  # kleine Pause zwischen Aufgaben
