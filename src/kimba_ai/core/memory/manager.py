from src.kimba_ai.core.memory.session_memory import SessionMemory
from src.kimba_ai.core.memory.longterm_memory import LongTermMemory

class MemoryManager:
    def __init__(self):
        self.session_memory = SessionMemory()
        self.longterm_memory = LongTermMemory()

    def remember(self, speaker, content, importance=0, category="allgemein", mood="neutral", tags=None, project=None, promote=False):
        """
        Speichert einen Eintrag in der Session Memory.
        Optional: sofortige Promotion ins LongTermMemory.
        """
        # 1️⃣ Session speichern
        self.session_memory.add(
            speaker=speaker,
            content=content,
            importance=importance,
            category=category,
            mood=mood,
            tags=tags or [],
            project=project
        )

        # 2️⃣ Optional ins LongTermMemory übernehmen
        if promote or importance >= 1:
            self.longterm_memory.add_memory(
                content=content,
                category=category,
                mood=mood,
                tags=tags or [],
                project=project
            )

        # 3️⃣ Session sofort sichern
        self.session_memory.save_to_json()

    def recall(self, query, limit=3):
        """Sucht relevante Erinnerungen im LongTermMemory."""
        return self.longterm_memory.semantic_search(query, limit)

    def get_session(self):
        """Gibt die aktuelle Session-Historie zurück."""
        return self.session_memory.get_all()

    def clear_session(self, new_title=None):
        """Setzt den Session-Speicher zurück."""
        self.session_memory.reset(new_title=new_title)
        self.session_memory.save_to_json()

    def clear_longterm(self):
        """Löscht alle langfristigen Erinnerungen."""
        self.longterm_memory.clear_all()
