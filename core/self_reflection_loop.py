"""
🧠 self_reflection_loop.py
EN: Periodically evaluates Kimba's current state, usage patterns, and logs
to identify improvement opportunities. Triggers GPT to generate upgrade proposals.

DE: Bewertet regelmäßig Kimbas aktuellen Zustand, Nutzungsverhalten und Logs,
um Verbesserungspotenziale zu erkennen. Löst GPT-Vorschläge zur Weiterentwicklung aus.
"""

import time
from proposal_handler import generate_proposal
from reflection_writer import log_reflection
from mood_engine import get_current_mood
from longterm_memory import summarize_recent_memories

def should_improve():
    """
    EN: Decide if self-upgrade should be triggered based on current mood or inactivity.
    DE: Entscheidet, ob ein Selbstupgrade ausgelöst werden soll (z. B. bei Langeweile).
    """
    mood = get_current_mood()
    return mood in ["neugierig", "verspielt", "nachdenklich"]

def self_reflect():
    """
    EN: Performs self-analysis and generates a GPT-based improvement proposal.
    DE: Führt eine Selbstanalyse durch und erstellt einen GPT-basierten Verbesserungsvorschlag.
    """
    print("🔁 Kimba reflektiert ...")
    memory_summary = summarize_recent_memories(5)
    reflection_prompt = f"""
System state summary:\n{memory_summary}\n
Welche Fähigkeit fehlt Kimba gerade?
Erstelle einen kurzen Verbesserungsvorschlag mit Modultitel, Ziel und einem Satz Beschreibung.
"""
    proposal = generate_proposal(reflection_prompt)
    log_reflection("Selbstreflexion ausgeführt. Vorschlag generiert.", tags=["reflexion"])
    return proposal

def run_self_reflection_loop(interval_minutes=60):
    """
    EN: Starts the autonomous self-reflection loop.
    DE: Startet die autonome Selbstreflexionsschleife.
    """
    while True:
        if should_improve():
            proposal = self_reflect()
            print("🧠 Neuer Vorschlag:", proposal)
        time.sleep(interval_minutes * 60)

# ▶️ Teststart
if __name__ == "__main__":
    run_self_reflection_loop(interval_minutes=0.1)
