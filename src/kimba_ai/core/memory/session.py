import json
import os
from datetime import datetime
from uuid import uuid4

SESSION_DIR = "memory/sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

VALID_SPEAKERS = {"user", "persona"}

class SessionMemory:
    def __init__(self, session_id: str | None = None, title: str | None = None, max_entries: int = 2000):
        self.session_id = session_id or str(uuid4())[:8]
        self.title = title or f"Session {self.session_id}"
        self.max_entries = max_entries
        self.messages: list[dict] = []

    def add(self, speaker: str, content: str, importance: int = 0, tags: list[str] | None = None,
            category: str | None = None, mood: str | None = None, project: str | None = None):
        """Fügt einen Eintrag hinzu; ignoriert leere Inhalte und invalid speaker."""
        if not content or not content.strip():
            return False
        if speaker not in VALID_SPEAKERS:
            speaker = "user"  # fallback statt crash

        entry = {
            "id": str(uuid4()),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "speaker": speaker,                    # "user" | "persona"
            "content": content.strip(),
            "importance": int(importance),         # 0 normal, 1 wichtig, 2 sehr wichtig
            "tags": tags or [],
            "category": category,                  # z.B. "request", "code", "decision"
            "mood": mood,                          # optional
            "project": project                     # z.B. "finance_tracker"
        }
        self.messages.append(entry)
        if len(self.messages) > self.max_entries:
            # Älteste un-wichtige Einträge zuerst entfernen
            self._prune()
        return True

    def _prune(self):
        # behalte wichtige zuerst, droppe die ältesten unwichtigen
        important = [m for m in self.messages if m.get("importance", 0) >= 1]
        normal = [m for m in self.messages if m.get("importance", 0) < 1]
        # halte z.B. 80% Budget für wichtige frei
        budget = self.max_entries - len(important)
        normal = normal[-max(budget, 0):]
        self.messages = important + normal
        self.messages.sort(key=lambda m: m["timestamp"])  # chronologisch

    def get_all(self) -> list[dict]:
        return self.messages

    def get_important(self, min_importance: int = 1) -> list[dict]:
        return [m for m in self.messages if m.get("importance", 0) >= min_importance]

    def save_to_json(self) -> str:
        path = os.path.join(SESSION_DIR, f"session_{self.session_id}.json")
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({
                "session_id": self.session_id,
                "title": self.title,
                "messages": self.messages
            }, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
        return path

    def load_from_json(self, path: str) -> bool:
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.session_id = data.get("session_id", self.session_id)
        self.title = data.get("title", self.title)
        self.messages = data.get("messages", [])
        return True

    def export_markdown(self) -> str:
        """Gibt die Session hübsch formatiert als Markdown zurück."""
        lines = [f"# {self.title} ({self.session_id})", ""]
        for m in self.messages:
            who = "👤 User" if m["speaker"] == "user" else "🤖 Persona"
            tags = f"  _tags: {', '.join(m['tags'])}_" if m.get("tags") else ""
            meta = []
            if m.get("category"): meta.append(m["category"])
            if m.get("project"): meta.append(f"proj:{m['project']}")
            if m.get("mood"): meta.append(f"mood:{m['mood']}")
            meta_str = f"  _({' | '.join(meta)})_" if meta else ""
            lines.append(f"- **{who}** [{m['timestamp']}]: {m['content']}{tags}{meta_str}")
        return "\n".join(lines)

    def reset(self, new_title: str | None = None):
        self.session_id = str(uuid4())[:8]
        self.title = new_title or f"Session {self.session_id}"
        self.messages = []

    def __len__(self) -> int:
        return len(self.messages)
