
import random

class KimbaDialog:
    def ask_user(self):
        prompts = [
            "Gibt es heute etwas Wichtiges zu tun?",
            "Wie kann ich dir heute helfen?",
            "Möchtest du, dass ich etwas für dich analysiere?",
            "Soll ich etwas Neues für dich lernen?",
            "Hast du einen Auftrag für mich?"
        ]
        return random.choice(prompts)
