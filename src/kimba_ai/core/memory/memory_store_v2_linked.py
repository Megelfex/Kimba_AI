import os
import json
import datetime
from difflib import SequenceMatcher
from mood_logic import adjust_response_by_mood

class KimbaMemoryV2:
    """
    EN: Enhanced memory system for storing, retrieving and mood-adjusting conversational entries.
    DE: Erweiterter Speicherdienst zur Ablage, Abfrage und stimmungsbasierten Anpassung von Gesprächen.
    """

    def __init__(self, memory_path="memory/kimba_memory_v2/"):
        """
        EN: Initializes the memory directory and loads existing memory entries if present.
        DE: Initialisiert das Speicherverzeichnis und lädt vorhandene Erinnerungen, falls vorhanden.

        Args:
            memory_path (str): Path to the folder for storing memory JSON files.
        """
        self.memory_path = memory_path
        os.makedirs(memory_path, exist_ok=True)
        self.memory_file = os.path.join(memory_path, "memory_log.json")
        self._load_memory()

    def _load_memory(self):
        """
        EN: Loads memory from JSON file into memory buffer.
        DE: Lädt Erinnerungsdaten aus der JSON-Datei in den Arbeitsspeicher.
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = []

    def _save_memory(self):
        """
        EN: Saves the in-memory memory list back to the JSON file.
        DE: Speichert den aktuellen Speicherinhalt zurück in die JSON-Datei.
        """
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def add_memory(self, user_input, kimba_response, mood="neutral", context_tags=None):
        """
        EN: Adds a new memory entry, adjusts Kimba's response based on mood, and saves it.
        DE: Fügt einen neuen Erinnerungseintrag hinzu, passt Kimbas Antwort stimmungsbasiert an und speichert ihn.

        Args:
            user_input (str): User’s original prompt or message.
            kimba_response (str): Kimba’s raw response before mood adjustment.
            mood (str): Emotional state for the current entry.
            context_tags (list[str], optional): Custom tags to classify the memory.

        Returns:
            str: Final mood-adjusted response stored with the entry.
        """
        adjusted_response = adjust_response_by_mood(kimba_response, mood)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "kimba_response": adjusted_response,
            "mood": mood,
            "context_tags": context_tags or []
        }
        self.memory.append(entry)
        self._save_memory()
        return adjusted_response

    def search_memory(self, query, threshold=0.6):
        """
        EN: Performs fuzzy search over past memory entries based on user input + response.
        DE: Führt eine unscharfe Suche über frühere Einträge basierend auf Anfrage & Antwort durch.

        Args:
            query (str): Search string to match against memory content.
            threshold (float): Minimum similarity ratio for inclusion (0.0 to 1.0).

        Returns:
            list[tuple]: List of (similarity_score, memory_entry) tuples sorted by score descending.
        """
        results = []
        for entry in self.memory:
            text = entry["user_input"] + " " + entry["kimba_response"]
            ratio = SequenceMatcher(None, query, text).ratio()
            if ratio >= threshold:
                results.append((ratio, entry))
        return sorted(results, key=lambda x: x[0], reverse=True)

    def get_recent(self, n=5):
        """
        EN: Returns the last N memory entries.
        DE: Gibt die letzten N gespeicherten Einträge zurück.

        Args:
            n (int): Number of recent entries to return.

        Returns:
            list[dict]: List of memory entries.
        """
        return self.memory[-n:]

# 🧪 Example usage for testing
if __name__ == "__main__":
    mem = KimbaMemoryV2()
    response = mem.add_memory(
        "Kannst du meine Dateien sortieren?",
        "Ich habe deine Ordner alphabetisch und thematisch sortiert.",
        mood="ruhig"
    )
    print(response)
    print(mem.get_recent())
