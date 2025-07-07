import os
import json
from datetime import datetime, timedelta

MEMORY_PATH = "memory/kimba_memory/longterm_memories.json"

def ensure_memory_file():
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

def save_memory_entry(content, mood=None, category="general", tags=None):
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
    recent = load_recent_memories(days)
    if not recent:
        return "Ich erinnere mich an nichts Besonderes in den letzten Tagen."
    summary = "Hier sind ein paar Dinge, an die ich mich erinnere:"
    for mem in recent[-5:]:
        ts = datetime.fromisoformat(mem["timestamp"]).strftime("%d.%m.%Y %H:%M")
        summary += f"• ({ts}) {mem['content']}"
    return summary.strip()

# Beispiel
if __name__ == "__main__":
    save_memory_entry("Du hast gestern an meinem Code gearbeitet.", mood="dankbar", tags=["projekt", "entwicklung"])
    print(summarize_recent_memories(7))
