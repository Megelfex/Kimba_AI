
"""
Kimba Desktop Cat
=================
DE: Ein animiertes Desktop-Haustier, das auf der aktuellen Stimmung basiert.
    Liest die Stimmung aus einer JSON-Datei und passt den angezeigten Sprite an.

EN: An animated desktop pet that reacts to the current mood.
    Reads mood from a JSON file and updates the displayed sprite accordingly.
"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import time
import threading
import logging

# Logging-Konfiguration / Logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s") 

# Konfiguration / Configuration
SPRITE_FOLDER = "desktop_kimba/sprites"
STATE_FILE = "desktop_kimba/shared/mood.json"
UPDATE_INTERVAL = 5  # Sekunden / seconds

# Stimmung zu Sprite-Mapping / Mood to sprite mapping
MOOD_TO_SPRITE = {
    "ruhig": "kimba_ruhig.png",
    "verspielt": "kimba_verspielt.png",
    "neugierig": "kimba_neugierig.png",
    "müde": "kimba_nachdenklich.png",
    "fokussiert": "kimba_fokussiert.png",
    "default": "kimba_ruhig.png"
}


class AnimatedCat(tk.Tk):
    """
    DE: Ein schwebendes, transparentes Desktop-Haustier, das seinen Sprite basierend auf der Stimmung ändert.
    EN: A floating, transparent desktop pet that changes its sprite based on mood.
    """

    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # Kein Rahmen / No window border
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")
        self.configure(bg="white")
        self.geometry("+1000+800")  # Startposition / Start position

        self.label = tk.Label(self, bg="white")
        self.label.pack()

        self.running = True
        self.current_sprite = None

        logging.info("🐾 Kimba Desktop Cat gestartet / started")
        threading.Thread(target=self.update_loop, daemon=True).start()

        self.bind("<Escape>", lambda e: self.quit_app())

    def quit_app(self):
        """
        DE: Beendet die Anwendung.
        EN: Quits the application.
        """
        logging.info("Kimba Desktop Cat beendet / stopped")
        self.running = False
        self.destroy()

    def update_loop(self):
        """
        DE: Endlosschleife, die regelmäßig die Stimmung prüft und das Sprite aktualisiert.
        EN: Endless loop that regularly checks mood and updates the sprite.
        """
        while self.running:
            try:
                mood = self.get_current_mood()
                self.update_sprite(mood)
            except Exception as e:
                logging.error(f"Fehler beim Aktualisieren der Stimmung / Error updating mood: {e}")
            time.sleep(UPDATE_INTERVAL)

    def get_current_mood(self):
        """
        DE: Liest die aktuelle Stimmung aus der STATE_FILE JSON-Datei.
        EN: Reads the current mood from the STATE_FILE JSON file.
        """
        if not os.path.exists(STATE_FILE):
            logging.warning(f"Stimmungsdatei nicht gefunden / Mood file not found: {STATE_FILE}")
            return "default"

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("mood", "default")

    def update_sprite(self, mood):
        """
        DE: Aktualisiert das Sprite basierend auf der Stimmung.
        EN: Updates the sprite based on mood.
        """
        sprite_file = MOOD_TO_SPRITE.get(mood, MOOD_TO_SPRITE["default"])
        sprite_path = os.path.join(SPRITE_FOLDER, sprite_file)

        if not os.path.exists(sprite_path):
            logging.error(f"Sprite nicht gefunden / Sprite not found: {sprite_path}")
            return

        if sprite_path != self.current_sprite:
            img = Image.open(sprite_path)
            tk_img = ImageTk.PhotoImage(img)
            self.label.config(image=tk_img)
            self.label.image = tk_img
            self.current_sprite = sprite_path
            logging.info(f"Sprite geändert zu / Sprite changed to: {sprite_file}")


if __name__ == "__main__":
    app = AnimatedCat()
    app.mainloop()
