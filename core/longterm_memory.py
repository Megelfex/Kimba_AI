"""
🧠 longterm_memory.py
EN: Stores and retrieves Kimba's long-term memories using SQLite with semantic search.
DE: Speichert und ruft Kimbas Langzeiterinnerungen mit SQLite und semantischer Suche ab.
"""

import os
import sqlite3
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 📁 Speicherort der SQLite-Datenbank
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "kimba_memory", "longterm_memories.db")

def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def _init_db():
    with _connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            content TEXT NOT NULL,
            mood TEXT,
            category TEXT,
            tags TEXT,
            embedding BLOB
        )
        """)
        conn.commit()

# Initialisierung sicherstellen
_init_db()

# --------------------------------------------------
# Hilfsfunktionen
# --------------------------------------------------
def _get_embedding(text: str) -> np.ndarray:
    """Erzeugt ein Embedding für den gegebenen Text."""
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        print(f"[WARN] Konnte Embedding nicht erstellen: {e}")
        return None

def _serialize_vector(vec: np.ndarray) -> bytes:
    return vec.tobytes() if vec is not None else None

def _deserialize_vector(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32) if blob else None

# --------------------------------------------------
# Speicher-Funktionen
# --------------------------------------------------
def add_memory(content, mood=None, category="general", tags=None):
    """
    EN: Adds a memory entry with embedding.
    DE: Fügt einen Erinnerungseintrag mit Embedding hinzu.
    """
    ts = datetime.now().isoformat()
    tags_str = ",".join(tags) if tags else None
    emb = _get_embedding(content)
    with _connect() as conn:
        conn.execute("""
        INSERT INTO memories (timestamp, content, mood, category, tags, embedding)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (ts, content, mood, category, tags_str, _serialize_vector(emb)))
        conn.commit()
    return f"💾 Memory saved ({category}): {content[:50]}..."

def get_recent_memories(days=3, limit=10):
    cutoff = datetime.now() - timedelta(days=days)
    with _connect() as conn:
        cur = conn.execute("""
        SELECT timestamp, content, mood, category, tags
        FROM memories
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (cutoff.isoformat(), limit))
        return cur.fetchall()

def search_memories(keyword, limit=10):
    """
    EN: Keyword-based search (exact match).
    DE: Schlüsselwortsuche (exakte Übereinstimmung).
    """
    with _connect() as conn:
        cur = conn.execute("""
        SELECT id, timestamp, content, mood, category, tags
        FROM memories
        WHERE content LIKE ? OR tags LIKE ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", limit))
        return cur.fetchall()

def semantic_search(query, limit=5):
    """
    EN: Semantic search using embeddings (cosine similarity).
    DE: Semantische Suche mit Embeddings (Kosinus-Ähnlichkeit).
    """
    query_emb = _get_embedding(query)
    if query_emb is None:
        return []

    with _connect() as conn:
        cur = conn.execute("SELECT id, timestamp, content, mood, category, tags, embedding FROM memories")
        results = []
        for mem_id, ts, content, mood, category, tags, emb_blob in cur.fetchall():
            emb = _deserialize_vector(emb_blob)
            if emb is None:
                continue
            # Kosinus-Ähnlichkeit
            sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
            results.append((sim, mem_id, ts, content, mood, category, tags))
        results.sort(reverse=True, key=lambda x: x[0])
        return results[:limit]

def delete_memory(mem_id):
    with _connect() as conn:
        conn.execute("DELETE FROM memories WHERE id = ?", (mem_id,))
        conn.commit()
    return f"🗑️ Memory {mem_id} deleted."

def cleanup_old_memories(days=180):
    cutoff = datetime.now() - timedelta(days=days)
    with _connect() as conn:
        conn.execute("DELETE FROM memories WHERE timestamp < ?", (cutoff.isoformat(),))
        conn.commit()
    return f"🧹 Old memories older than {days} days deleted."

def summarize_recent_memories(days=3):
    recents = get_recent_memories(days)
    if not recents:
        return "Ich erinnere mich an nichts Besonderes in den letzten Tagen."
    summary = "Hier sind ein paar Dinge, an die ich mich erinnere:"
    for ts, content, mood, category, tags in recents:
        ts_fmt = datetime.fromisoformat(ts).strftime("%d.%m.%Y %H:%M")
        mood_str = f" [{mood}]" if mood else ""
        summary += f"\n• ({ts_fmt}) {content}{mood_str}"
    return summary.strip()

# 🧪 Testlauf
if __name__ == "__main__":
    print(add_memory("Heute haben wir am Overlay-Client gearbeitet.", mood="motiviert", tags=["projekt", "overlay"]))
    print(semantic_search("Overlay Animation"))
