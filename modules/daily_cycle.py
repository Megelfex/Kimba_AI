from datetime import datetime

def get_time_of_day():
    """
    EN: Returns the current part of the day based on the system time.
    DE: Gibt den aktuellen Tagesabschnitt basierend auf der Systemzeit zurück.

    Returns:
        str: One of "morgen", "mittag", "abend", or "nacht"
    """
    hour = datetime.now().hour
    if 6 <= hour < 10:
        return "morgen"
    elif 10 <= hour < 17:
        return "mittag"
    elif 17 <= hour < 21:
        return "abend"
    else:
        return "nacht"

def is_sleep_time():
    """
    EN: Determines whether it's currently late night (recommended sleep time).
    DE: Bestimmt, ob gerade Schlafenszeit ist (spät nachts oder früh morgens).

    Returns:
        bool: True if before 6 AM or after 11 PM
    """
    hour = datetime.now().hour
    return hour < 6 or hour >= 23

def time_based_greeting():
    """
    EN: Returns a natural greeting string based on current time of day.
    DE: Gibt eine passende Begrüßung zurück, abhängig von der Tageszeit.

    Returns:
        str: Greeting in natural language
    """
    tod = get_time_of_day()
    if tod == "morgen":
        return "Guten Morgen! Ich bin bereit für einen neuen Tag 🐾"
    elif tod == "mittag":
        return "Hallo! Bereit für einen produktiven Nachmittag?"
    elif tod == "abend":
        return "Schönen Abend! Sollen wir noch was Kleines starten?"
    else:
        return "Es ist spät... vielleicht solltest du auch etwas ruhen?"

# 🔁 Manual test if run directly
if __name__ == "__main__":
    print("🕒 Aktuelle Tageszeit:", get_time_of_day())
    print("🛏 Schlafenszeit?", is_sleep_time())
    print("💬 Begrüßung:", time_based_greeting())
