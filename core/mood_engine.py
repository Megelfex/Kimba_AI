import random

class MoodEngine:
    """
    EN: Core class for managing and randomly updating Kimba's emotional state.
    DE: Zentrale Klasse zur Verwaltung und zufälligen Aktualisierung von Kimbas Stimmung.
    """

    def __init__(self):
        """
        EN: Initializes the mood engine with a predefined list of moods and selects an initial one.
        DE: Initialisiert die MoodEngine mit einer festen Liste von Stimmungen und wählt eine Startstimmung aus.
        """
        self.moods = [
            "nachdenklich", "verspielt", "neugierig",
            "ruhig", "fokussiert", "müde", "traurig", "fröhlich", "genervt"
        ]
        self.current = random.choice(self.moods)

    def update_mood(self):
        """
        EN: Randomly selects a new mood and updates the current state.
        DE: Wählt zufällig eine neue Stimmung und aktualisiert den aktuellen Zustand.

        Returns:
            str: The newly selected mood.
        """
        self.current = random.choice(self.moods)
        return self.current

    def get_mood(self):
        """
        EN: Returns the currently active mood.
        DE: Gibt die aktuell gesetzte Stimmung zurück.

        Returns:
            str: Current mood.
        """
        return self.current

# 🌐 Global MoodEngine instance for universal access
# 🌍 Globale MoodEngine-Instanz für andere Module
global_engine = MoodEngine()

def update_current_mood():
    """
    EN: Updates the global mood to a new random state.
    DE: Aktualisiert die globale Stimmung zufällig.

    Returns:
        str: New global mood.
    """
    return global_engine.update_mood()

def get_current_mood():
    """
    EN: Returns the current global mood state.
    DE: Gibt die aktuelle globale Stimmung zurück.

    Returns:
        str: Global current mood.
    """
    return global_engine.get_mood()
