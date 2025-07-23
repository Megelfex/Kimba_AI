import os
import json
from datetime import datetime, timedelta

# 📁 Speicherort für das Langzeitgedächtnis
# EN: File path for storing long-term memory entries
MEMORY_PATH = "memory/kimba_memory/longterm_memories.json"

def ensure_memory_file():
    """
    EN: Ensures that the memory file and its directory exist. Creates an empty JSON array if missing.
    DE: Stellt sicher, dass die Speicherdatei und der Ordner existieren. Erstellt bei Bedarf eine leere JSON-Datei.
    """
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_memory_entry(content, mood=None, category="general", tags=None):
    """
    EN: Saves a memory entry to the long-term memory file.
    DE: Speichert einen Erinnerungseintrag in die Langzeitspeicherdatei.

    Args:
        content (str): Main content or message to remember.
        mood (str, optional): Associated emotional state.
        category (str): Memory category label.
        tags (list[str], optional): List of tags for search or context.
    """
    ensure_memory_file()
    timestamp = datetime.now().isoformat()
    memory_entry = {
        "timestamp": timestamp,
        "content": content,
        "mood": mood,
        "category": category,
        "tags": tags or []
    }
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.append(memory_entry)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_recent_memories(days=3):
    """
    EN: Loads memory entries from the last X days.
    DE: Lädt Erinnerungseinträge der letzten X Tage.

    Args:
        days (int): Time window (in days) to look back.

    Returns:
        list[dict]: List of memory entries within the given timeframe.
    """
    ensure_memory_file()
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    cutoff = datetime.now() - timedelta(days=days)
    recent = [
        mem for mem in data
        if datetime.fromisoformat(mem["timestamp"]) >= cutoff
    ]
    return recent

def summarize_recent_memories(days=3):
    """
    EN: Returns a short textual summary of the most recent memories.
    DE: Gibt eine kurze Zusammenfassung der letzten Erinnerungen zurück.

    Args:
        days (int): How many past days to include in the summary.

    Returns:
        str: Human-readable summary of recent memory entries.
    """
    recent = load_recent_memories(days)
    if not recent:
        return "Ich erinnere mich an nichts Besonderes in den letzten Tagen."
    summary = "Hier sind ein paar Dinge, an die ich mich erinnere:"
    for mem in recent[-5:]:
        ts = datetime.fromisoformat(mem["timestamp"]).strftime("%d.%m.%Y %H:%M")
        summary += f"\n• ({ts}) {mem['content']}"
    return summary.strip()

# 🧪 Example usage for standalone test
if __name__ == "__main__":
    save_memory_entry(
        "Du hast gestern an meinem Code gearbeitet.",
        mood="dankbar",
        tags=["projekt", "entwicklung"]
    )
    print(summarize_recent_memories(7))
