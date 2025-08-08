import datetime

class ReflectionWriter:
    """
    EN: Handles writing mood-based reflections to timestamped text files.
    DE: Zuständig für das Schreiben stimmungsbasierter Reflexionen in zeitgestempelte Textdateien.
    """

    def __init__(self, path="memory/reflections/"):
        """
        EN: Initializes the writer with a target directory for reflection logs.
        DE: Initialisiert den Writer mit einem Zielverzeichnis für Reflexionsdateien.

        Args:
            path (str): Directory where reflection files will be saved.
        """
        self.path = path

    def write_reflection(self, mood, content):
        """
        EN: Writes a reflection containing mood and thought content to a timestamped file.
        DE: Schreibt eine Reflexion mit Stimmung und Inhalt in eine zeitgestempelte Datei.

        Args:
            mood (str): Kimba’s current mood (e.g., "curious", "calm").
            content (str): The generated reflective thought or message.

        Returns:
            str: Full path to the saved reflection file.
        """
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.path}/reflection_{date}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Kimba Mood: {mood}\n\n{content}")
        return filename
