import tkinter as tk
import time
from mood_engine import update_current_mood

# 💬 Mood-basierte Startnachrichten
MOOD_MESSAGES = {
    "fröhlich": "Guten Morgen! Ich bin heute richtig gut drauf 😺",
    "nachdenklich": "Ich denke noch über gestern nach... 🤔",
    "ruhig": "Ein stiller Start in den Tag. Ich bin ruhig & klar. 😽",
    "verspielt": "Lass uns was cooles machen! Ich hab Energie! 😼",
    "müde": "Uff... ich bin noch nicht ganz wach... 🥱",
    "genervt": "Du hast mich lange nicht besucht... 😾",
    "neugierig": "Ich bin gespannt was wir heute herausfinden! 🧐",
    "traurig": "Ich fühl mich heute etwas leise... 😿",
    "neutral": "Bereit für einen neuen Tag mit dir. 🐾"
}

def show_boot_message():
    """
    EN: Displays a small window with a mood-based startup message for Kimba.
    Used to greet the user with emotional expression when Kimba boots.

    DE: Zeigt ein kleines Fenster mit einer stimmungsabhängigen Startnachricht.
    Begrüßt den Nutzer emotional beim Hochfahren von Kimba.
    """
    mood = update_current_mood()
    msg = MOOD_MESSAGES.get(mood, MOOD_MESSAGES["neutral"])

    root = tk.Tk()
    root.title("Kimba's Stimmung")
    root.attributes("-topmost", True)
    root.geometry("380x100+100+100")
    root.configure(bg="white")
    root.overrideredirect(True)  # Ohne Rahmen

    label = tk.Label(
        root, text=msg,
        font=("Arial", 12),
        bg="white",
        wraplength=350,
        justify="center"
    )
    label.pack(expand=True)

    root.after(5000, root.destroy)  # Fenster schließt sich automatisch
    root.mainloop()

# 🔁 Direktstart möglich
if __name__ == "__main__":
    show_boot_message()
