
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

SPRITE_FOLDER = "sprites"
STATE_FILE = "desktop_kimba/kimba_state.json"
MOOD_TO_SPRITE = {
    "ruhig": "kimba_ruhig.png",
    "verspielt": "kimba_verspielt.png",
    "neugierig": "kimba_neugierig.png",
    "müde": "kimba_nachdenklich.png",
    "fokussiert": "kimba_fokussiert.png",
    "default": "kimba_ruhig.png"
}


class AnimatedCat(tk.Tk):
    def __init__(self):
        """
        EN: Initializes the transparent window and starts the mood update loop.
        DE: Initialisiert das transparente Fenster und startet die Stimmungsaktualisierungsschleife.
        """
        super().__init__()
        self.overrideredirect(True)  # Kein Rahmen / No window border
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")
        self.configure(bg="white")
        self.geometry("+1000+800")

        self.label = tk.Label(self, bg="white")
        self.label.pack()

        self.running = True
        self.current_sprite = None

        threading.Thread(target=self.update_loop).start()

    def update_loop(self):
        while self.running:
            mood = self.read_mood()
            sprite_file = MOOD_TO_SPRITE.get(mood, MOOD_TO_SPRITE["default"])
            sprite_path = os.path.join(SPRITE_FOLDER, sprite_file)
            if os.path.exists(sprite_path) and sprite_path != self.current_sprite:
                self.show_sprite(sprite_path)
                self.current_sprite = sprite_path
            time.sleep(2)

    def read_mood(self):
        if not os.path.exists(STATE_FILE):
            logging.warning(f"Stimmungsdatei nicht gefunden / Mood file not found: {STATE_FILE}")
            return "default"
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("mood", "default")
        except:
            return "default"

    def show_sprite(self, path):
        try:
            img = Image.open(path)
            img = img.convert("RGBA")
            img = img.resize((100, 100), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.label.config(image=tk_img)
            self.label.image = tk_img
            self.current_sprite = sprite_path
            logging.info(f"Sprite geändert zu / Sprite changed to: {sprite_file}")


if __name__ == "__main__":
    app = AnimatedCat()
    app.mainloop()
