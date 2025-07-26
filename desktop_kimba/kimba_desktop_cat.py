import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import time
import threading

# 📂 Pfade & Konfiguration
SPRITE_FOLDER = "sprites"
STATE_FILE = "desktop_kimba/kimba_state.json"

# 😺 Zuordnung von Stimmung → Sprite-Datei
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
    EN: A floating transparent desktop pet that changes its sprite based on mood read from a JSON state file.
    DE: Ein schwebendes, transparentes Desktop-Haustier, das je nach Stimmung (aus JSON-Datei) den Sprite wechselt.
    """

    def __init__(self):
        """
        EN: Initializes the transparent window and starts the mood update loop.
        DE: Initialisiert das transparente Fenster und startet die Stimmungsaktualisierungsschleife.
        """
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "white")
        self.configure(bg="white")
        self.geometry("+1000+800")  # Startposition

        self.label = tk.Label(self, bg="white")
        self.label.pack()
        self.running = True
        self.current_sprite = None

        threading.Thread(target=self.update_loop, daemon=True).start()

    def update_loop(self):
        """
        EN: Continuously checks for mood changes and updates the sprite accordingly.
        DE: Überwacht kontinuierlich die Stimmung und aktualisiert bei Änderungen den Sprite.
        """
        while self.running:
            mood = self.read_mood()
            sprite_file = MOOD_TO_SPRITE.get(mood, MOOD_TO_SPRITE["default"])
            sprite_path = os.path.join(SPRITE_FOLDER, sprite_file)

            if os.path.exists(sprite_path) and sprite_path != self.current_sprite:
                self.show_sprite(sprite_path)
                self.current_sprite = sprite_path

            time.sleep(2)

    def read_mood(self):
        """
        EN: Reads the current mood from a shared JSON file (set by other modules).
        DE: Liest die aktuelle Stimmung aus einer gemeinsamen JSON-Datei (gesetzt von anderen Modulen).

        Returns:
            str: Mood keyword (e.g. "ruhig", "verspielt") or "default"
        """
        if not os.path.exists(STATE_FILE):
            return "default"
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("mood", "default")
        except:
            return "default"

    def show_sprite(self, path):
        """
        EN: Loads and displays a PNG sprite on the floating window.
        DE: Lädt und zeigt einen PNG-Sprite im schwebenden Fenster an.

        Args:
            path (str): Path to the sprite image.
        """
        try:
            img = Image.open(path)
            img = img.convert("RGBA")
            img = img.resize((100, 100), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.label.configure(image=tk_img)
            self.label.image = tk_img
        except Exception as e:
            print(f"Fehler beim Laden des Sprites: {e}")

if __name__ == "__main__":
    app = AnimatedCat()
    app.mainloop()
