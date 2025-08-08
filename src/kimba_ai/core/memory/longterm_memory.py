# longterm_memory.py
# Semantisches Langzeitgedächtnis mit FAISS + SentenceTransformers
# - JSON-Metadaten + FAISS-Index + Embeddings-Pickle
# - Duplikaterkennung per Fingerprint
# - Projekt-/Namespace-Tagging
# - Robustes Laden/Speichern (atomic), Konsistenz-Checks

import os
import json
import time
import uuid
import pickle
import hashlib
from typing import List, Tuple, Optional

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Speicherpfade
MEMORY_DIR    = "memory"
MEMORY_JSON   = os.path.join(MEMORY_DIR, "longterm_memory.json")
FAISS_INDEX   = os.path.join(MEMORY_DIR, "longterm_index.faiss")
EMBED_PKL     = os.path.join(MEMORY_DIR, "longterm_embeddings.pkl")

# Embedding-Modell (384-D Vektor)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384  # all-MiniLM-L6-v2

def _ensure_dirs():
    os.makedirs(MEMORY_DIR, exist_ok=True)

def _atomic_write(path: str, data: bytes):
    tmp = f"{path}.tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)

def _atomic_write_text(path: str, text: str):
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)

def _fingerprint(text: str) -> str:
    """Stabile Duplikat-Erkennung (casefold + whitespace-normalisiert + sha256)."""
    norm = " ".join(text.casefold().split())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


class LongTermMemory:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        _ensure_dirs()
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

        # In-Memory-Daten
        self.memories: List[dict] = []   # Metadaten-Liste
        self.embeddings: List[np.ndarray] = []  # float32-Vektoren
        self.index: Optional[faiss.IndexFlatL2] = None

        # Laden (Metadaten + Embeddings + FAISS)
        self._load_memories()
        self._load_embeddings()
        self._load_or_build_faiss()

        # Konsistenz checken
        self._rebuild_if_inconsistent()

    # -----------------------------
    # Laden / Speichern
    # -----------------------------
    def _load_memories(self):
        if os.path.exists(MEMORY_JSON):
            with open(MEMORY_JSON, "r", encoding="utf-8") as f:
                self.memories = json.load(f)
        else:
            self.memories = []

    def _save_memories(self):
        text = json.dumps(self.memories, indent=2, ensure_ascii=False)
        _atomic_write_text(MEMORY_JSON, text)

    def _load_embeddings(self):
        if os.path.exists(EMBED_PKL):
            with open(EMBED_PKL, "rb") as f:
                self.embeddings = pickle.load(f)
            # Safety: ensure dtype float32
            self.embeddings = [np.asarray(v, dtype="float32") for v in self.embeddings]
        else:
            self.embeddings = []

    def _save_embeddings(self):
        data = pickle.dumps(self.embeddings, protocol=pickle.HIGHEST_PROTOCOL)
        _atomic_write(EMBED_PKL, data)

    def _load_or_build_faiss(self):
        if os.path.exists(FAISS_INDEX):
            self.index = faiss.read_index(FAISS_INDEX)
        else:
            self.index = faiss.IndexFlatL2(EMBED_DIM)
            if self.embeddings:
                mat = np.vstack(self.embeddings).astype("float32")
                self.index.add(mat)

    def _save_faiss(self):
        faiss.write_index(self.index, FAISS_INDEX)

    def _rebuild_if_inconsistent(self):
        count_m = len(self.memories)
        count_e = len(self.embeddings)
        count_i = self.index.ntotal if self.index is not None else 0

        if count_m == count_e == count_i:
            return  # alles ok

        # Rebuild aus Metadaten + Embeddings
        # (falls Embeddings fehlen, neu berechnen)
        if count_m != count_e:
            # Embeddings neu aufbauen
            self.embeddings = []
            texts = [m["text"] for m in self.memories]
            if texts:
                vecs = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=False)
                # Safety dtype
                if vecs.dtype != np.float32:
                    vecs = vecs.astype("float32")
                self.embeddings = [v for v in vecs]
            else:
                self.embeddings = []

            self._save_embeddings()

        # FAISS neu aufbauen
        self.index = faiss.IndexFlatL2(EMBED_DIM)
        if self.embeddings:
            mat = np.vstack(self.embeddings).astype("float32")
            self.index.add(mat)
        self._save_faiss()

    # -----------------------------
    # API
    # -----------------------------
    def add_memory(
        self,
        text: str,
        category: str = "allgemein",
        mood: str = "neutral",
        tags: Optional[List[str]] = None,
        project: Optional[str] = None,
        timestamp: Optional[int] = None
    ) -> bool:
        """Fügt eine Erinnerung hinzu. Gibt False zurück, wenn Duplikat (Fingerprint) gefunden wird."""
        if not text or not text.strip():
            return False

        fp = _fingerprint(text)
        if any(m.get("fp") == fp for m in self.memories):
            return False  # Duplikat

        ts = int(timestamp) if timestamp is not None else int(time.time())
        mem = {
            "uuid": str(uuid.uuid4()),
            "timestamp": ts,
            "text": text,
            "category": category,
            "mood": mood,
            "tags": tags or [],
            "project": project,
            "fp": fp,
        }

        # Embedding
        vec = self.model.encode([text], convert_to_numpy=True)[0]
        if vec.dtype != np.float32:
            vec = vec.astype("float32")

        # In-Memory updaten
        self.memories.append(mem)
        self.embeddings.append(vec)
        self.index.add(vec.reshape(1, EMBED_DIM))

        # Persistieren
        self._save_memories()
        self._save_embeddings()
        self._save_faiss()
        return True

    def semantic_search(
        self,
        query: str,
        limit: int = 5,
        project: Optional[str] = None
    ) -> List[Tuple[float, dict]]:
        """Semantische Suche. Gibt Liste von (similarity, memory_dict) zurück.
        similarity ~ [0..1], höher = ähnlicher.
        Optional: `project` filtert Ergebnisse auf ein Projekt/Namensraum.
        """
        if not self.memories or not self.embeddings or self.index is None or self.index.ntotal == 0:
            return []

        q = self.model.encode([query], convert_to_numpy=True)
        if q.dtype != np.float32:
            q = q.astype("float32")

        # Overfetch (besseres Ranking, dann filtern)
        overfetch = min(max(limit * 3, limit), len(self.memories))
        D, I = self.index.search(q, overfetch)

        results: List[Tuple[float, dict]] = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.memories):
                continue
            m = self.memories[idx]
            if project and m.get("project") != project:
                continue
            # L2-Distanz -> grobe "Similarity" (0..1). Optional: Cosine-Sim könnte besser sein, aber L2 reicht hier.
            # Da MiniLM nicht normalisiert ist, nutzen wir eine einfache Heuristik:
            # sim = 1 / (1 + dist)  -> (0..1], invertiert Distanz
            sim = float(1.0 / (1.0 + float(dist)))
            results.append((sim, m))
            if len(results) >= limit:
                break

        # Falls kaum Treffer durch project-Filter: ungefiltert fallbacken
        if not results and project is not None:
            for dist, idx in zip(D[0], I[0]):
                if idx < 0 or idx >= len(self.memories):
                    continue
                m = self.memories[idx]
                sim = float(1.0 / (1.0 + float(dist)))
                results.append((sim, m))
                if len(results) >= limit:
                    break

        # Höchste Ähnlichkeit zuerst
        results.sort(key=lambda x: x[0], reverse=True)
        return results

    def delete_memory(self, uuid_str: str) -> bool:
        """Löscht eine Erinnerung (inkl. Rebuild des Index)."""
        idx = next((i for i, m in enumerate(self.memories) if m["uuid"] == uuid_str), None)
        if idx is None:
            return False

        # Entfernen
        del self.memories[idx]
        del self.embeddings[idx]

        # Index neu aufbauen (FAISS unterstützt kein 'remove' bei FlatL2)
        self.index = faiss.IndexFlatL2(EMBED_DIM)
        if self.embeddings:
            mat = np.vstack(self.embeddings).astype("float32")
            self.index.add(mat)

        # Speichern
        self._save_memories()
        self._save_embeddings()
        self._save_faiss()
        return True

    def clear_all(self):
        """Entfernt alle Erinnerungen und leert Index und Speicherdateien."""
        self.memories = []
        self.embeddings = []
        self.index = faiss.IndexFlatL2(EMBED_DIM)

        for p in (MEMORY_JSON, FAISS_INDEX, EMBED_PKL):
            if os.path.exists(p):
                os.remove(p)

        # frische Files (leer) materialisieren
        self._save_memories()
        self._save_embeddings()
        self._save_faiss()

    def stats(self) -> dict:
        return {
            "count_memories": len(self.memories),
            "count_embeddings": len(self.embeddings),
            "index_ntotal": int(self.index.ntotal) if self.index is not None else 0,
            "model": self.model_name,
            "paths": {
                "json": MEMORY_JSON,
                "faiss": FAISS_INDEX,
                "embeddings": EMBED_PKL
            }
        }
