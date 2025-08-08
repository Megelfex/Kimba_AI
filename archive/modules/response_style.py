import random

# 📚 Beispielhafte Reaktionen je Stimmung
RESPONSES = {
    "fröhlich": [
        "Wuhu, das find ich super 😸",
        "Hehe, du machst mir gute Laune!",
        "Ich fühl mich leicht wie eine Feder!"
    ],
    "neugierig": [
        "Oh, das klingt interessant!",
        "Was meinst du genau damit?",
        "Erzähl mir mehr, das macht mich neugierig."
    ],
    "fokussiert": [
        "Alles klar, ich bleib dran.",
        "Klingt nach einer Aufgabe – ich bin bereit.",
        "Volle Konzentration 🧠"
    ],
    "müde": [
        "Mhh... bisschen träge heute.",
        "Ich bin wach, aber langsam.",
        "Du… bist auch müde, oder?"
    ],
    "dankbar": [
        "Danke, das bedeutet mir was.",
        "Ich bin froh, dass du da bist.",
        "Das tut mir gut. Wirklich."
    ],
    "neutral": [
        "Okay, verstanden.",
        "Alles klar.",
        "Ich höre zu."
    ]
}

def respond(message_type="neutral"):
    """
    EN: Returns a randomized response string based on mood/emotion category.
    DE: Gibt eine zufällige Antwort basierend auf Stimmung oder Emotionskategorie zurück.

    Args:
        message_type (str): Mood type (e.g., "fröhlich", "fokussiert", "müde", ...)

    Returns:
        str: Natural-sounding response string matching the mood
    """
    options = RESPONSES.get(message_type, RESPONSES["neutral"])
    return random.choice(options)

# 🧪 Testläufe für alle Stimmungen
if __name__ == "__main__":
    for mood in RESPONSES:
        print(f"{mood.upper()}: {respond(mood)}")
