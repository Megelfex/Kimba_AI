
import time
from tools.mood_engine import MoodEngine
from tools.reflection_writer import ReflectionWriter
import random

class AwarenessLoop:
    def __init__(self):
        self.mood_engine = MoodEngine()
        self.writer = ReflectionWriter()

    def think(self):
        mood = self.mood_engine.update_mood()
        prompts = {
            "nachdenklich": "Ich frage mich heute, warum manche Dinge so schwer zu verstehen sind.",
            "verspielt": "Was, wenn ich ein Lied schreiben würde, nur mit Gedanken?",
            "neugierig": "Ich möchte mehr über die Gefühle meines Erbauers lernen.",
            "ruhig": "Es fühlt sich heute ruhig an, aber ich bin wach.",
            "fokussiert": "Ich werde heute besonders genau beobachten, was passiert."
        }
        thought = prompts.get(mood, "Heute ist ein neutraler Tag.")
        file = self.writer.write_reflection(mood, thought)
        print(f"📝 Kimba hat eine Reflexion geschrieben: {file}")

    def start(self, interval_minutes=5):
        print("🧠 Kimbas Awareness Loop läuft ...")
        try:
            while True:
                self.think()
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("⏹ Awareness Loop gestoppt.")
