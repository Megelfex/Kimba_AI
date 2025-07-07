import random

class MoodEngine:
    def __init__(self):
        self.moods = [
            "nachdenklich", "verspielt", "neugierig",
            "ruhig", "fokussiert", "müde", "traurig", "fröhlich", "genervt"
        ]
        self.current = random.choice(self.moods)

    def update_mood(self):
        self.current = random.choice(self.moods)
        return self.current

    def get_mood(self):
        return self.current

# Globale MoodEngine-Instanz für Zugriff in anderen Modulen
global_engine = MoodEngine()

# Exporte für globale Nutzung
def update_current_mood():
    """
    Aktualisiert Kimbas Stimmung zufällig.
    Wird z. B. vom Mood-Sync-Modul oder Triggern verwendet.
    """
    return global_engine.update_mood()

def get_current_mood():
    """
    Gibt aktuelle Stimmung von Kimba zurück.
    """
    return global_engine.get_mood()
