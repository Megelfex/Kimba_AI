import os
import json
import datetime
from difflib import SequenceMatcher
from mood_logic import adjust_response_by_mood

class KimbaMemoryV2:
    def __init__(self, memory_path="memory/kimba_memory_v2/"):
        self.memory_path = memory_path
        os.makedirs(memory_path, exist_ok=True)
        self.memory_file = os.path.join(memory_path, "memory_log.json")
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = []

    def _save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def add_memory(self, user_input, kimba_response, mood="neutral", context_tags=None):
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
        return adjusted_response  # Gibt finalisierte Antwort zurück

    def search_memory(self, query, threshold=0.6):
        results = []
        for entry in self.memory:
            text = entry["user_input"] + " " + entry["kimba_response"]
            ratio = SequenceMatcher(None, query, text).ratio()
            if ratio >= threshold:
                results.append((ratio, entry))
        return sorted(results, key=lambda x: x[0], reverse=True)

    def get_recent(self, n=5):
        return self.memory[-n:]

# Beispielnutzung
if __name__ == "__main__":
    mem = KimbaMemoryV2()
    response = mem.add_memory(
        "Kannst du meine Dateien sortieren?",
        "Ich habe deine Ordner alphabetisch und thematisch sortiert.",
        mood="ruhig"
    )
    print(response)
    print(mem.get_recent())
