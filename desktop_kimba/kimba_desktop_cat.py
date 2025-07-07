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
        super().__init__()
        self.overrideredirect(True)
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
            self.label.configure(image=tk_img)
            self.label.image = tk_img
        except Exception as e:
            print(f"Fehler beim Laden des Sprites: {e}")

if __name__ == "__main__":
    app = AnimatedCat()
    app.mainloop()
