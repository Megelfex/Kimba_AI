
import datetime

class ReflectionWriter:
    def __init__(self, path="memory/reflections/"):
        self.path = path

    def write_reflection(self, mood, content):
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.path}/reflection_{date}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Kimba Mood: {mood}\n\n{content}")
        return filename
