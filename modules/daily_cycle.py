from datetime import datetime

def get_time_of_day():
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
    hour = datetime.now().hour
    return hour < 6 or hour >= 23

def time_based_greeting():
    tod = get_time_of_day()
    if tod == "morgen":
        return "Guten Morgen! Ich bin bereit für einen neuen Tag 🐾"
    elif tod == "mittag":
        return "Hallo! Bereit für einen produktiven Nachmittag?"
    elif tod == "abend":
        return "Schönen Abend! Sollen wir noch was Kleines starten?"
    else:
        return "Es ist spät... vielleicht solltest du auch etwas ruhen?"

# Beispiel
if __name__ == "__main__":
    print("🕒 Aktuelle Tageszeit:", get_time_of_day())
    print("🛏 Schlafenszeit?", is_sleep_time())
    print("💬 Begrüßung:", time_based_greeting())
