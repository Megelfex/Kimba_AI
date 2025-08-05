"""
🧠 memory_filter.py
EN: Filters incoming messages to decide if they should be stored in long-term memory.
DE: Filtert eingehende Nachrichten, um zu entscheiden, ob sie im Langzeitgedächtnis gespeichert werden sollen.
"""

from core.llm_router import KimbaLLMRouter

# LLM-Instanz (API-First mit Fallback)
llm = KimbaLLMRouter()

def is_relevant_message(message: str) -> bool:
    """
    EN: Uses Kimba's LLM to decide if a message should be stored in memory.
    DE: Nutzt Kimbas LLM, um zu entscheiden, ob eine Nachricht im Gedächtnis gespeichert werden soll.
    """
    prompt = f"""
Decide if the following message contains information worth remembering
for an AI assistant that acts as a personal companion and project partner.

Only answer with YES or NO.

Message:
\"\"\"{message}\"\"\"
    """
    try:
        result = llm.ask(prompt).strip().lower()
        return "yes" in result
    except Exception:
        # Fallback: Wenn LLM nicht verfügbar, lieber speichern
        return True
