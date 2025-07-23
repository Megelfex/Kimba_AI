import random

class KimbaDialog:
    """
    EN: Handles dialog prompting logic for Kimba.
    Periodically asks the user engaging questions to offer help or start interactions.

    DE: Verwaltet die Logik für Gesprächsaufforderungen von Kimba.
    Stellt dem Nutzer regelmäßig Fragen, um Unterstützung anzubieten oder Dialoge zu starten.
    """

    def ask_user(self):
        """
        EN: Returns a random helpful question Kimba might ask during idle or startup.
        DE: Gibt eine zufällige, hilfreiche Frage zurück, die Kimba z. B. bei Inaktivität oder Start stellt.

        Returns:
            str: A natural prompt string in German.
        """
        prompts = [
            "Gibt es heute etwas Wichtiges zu tun?",
            "Wie kann ich dir heute helfen?",
            "Möchtest du, dass ich etwas für dich analysiere?",
            "Soll ich etwas Neues für dich lernen?",
            "Hast du einen Auftrag für mich?"
        ]
        return random.choice(prompts)

# 🧪 Testaufruf
if __name__ == "__main__":
    k = KimbaDialog()
    print(k.ask_user())
