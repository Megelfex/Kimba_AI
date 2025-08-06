"""
🧠 AwarenessLoop – Kimba's autonomous self-reflection cycle
===========================================================

EN:
This module defines the AwarenessLoop class, a recurring process where Kimba reflects based on its mood.
It uses the MoodEngine to determine a current mood, then generates and writes a context-specific reflection
via the ReflectionWriter.

DE:
Dieses Modul definiert die AwarenessLoop-Klasse – einen wiederkehrenden Prozess, in dem Kimba basierend auf
ihrer Stimmung reflektiert. Die aktuelle Stimmung wird mit der MoodEngine ermittelt, und anschließend wird
eine passende Reflexion mit dem ReflectionWriter gespeichert.
"""

import time
from tools.mood_engine import MoodEngine
from tools.reflection_writer import ReflectionWriter
import random

class AwarenessLoop:
    """
    EN:
    The AwarenessLoop manages Kimba's self-reflective thinking.
    It periodically generates a thought based on current mood and writes it to a file.

    DE:
    Die AwarenessLoop steuert Kimbas selbstreflektierendes Denken.
    In regelmäßigen Abständen erzeugt sie einen Gedanken basierend auf der aktuellen Stimmung
    und schreibt diesen in eine Datei.
    """
    
    def __init__(self):
        """
        EN:
        Initializes the mood engine and reflection writer.

        DE:
        Initialisiert die MoodEngine und den ReflectionWriter.
        """
        self.mood_engine = MoodEngine()
        self.writer = ReflectionWriter()

    def think(self):
        """
        EN:
        Determines Kimba's current mood and writes a reflective thought accordingly.
        Output is printed to console after writing.

        DE:
        Ermittelt Kimbas aktuelle Stimmung und schreibt einen entsprechenden Reflexionsgedanken.
        Die Ausgabe wird nach dem Schreiben in der Konsole angezeigt.
        """
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
        """
        EN:
        Starts the awareness loop. Kimba thinks and writes a reflection every `interval_minutes`.
        Can be stopped via KeyboardInterrupt (Ctrl+C).

        DE:
        Startet die Awareness-Schleife. Kimba reflektiert alle `interval_minutes` Minuten.
        Kann mit KeyboardInterrupt (Strg+C) gestoppt werden.
        """
        print("🧠 Kimbas Awareness Loop läuft ...")
        try:
            while True:
                self.think()
                time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("⏹ Awareness Loop gestoppt.")
