import pygame
import time
import random
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.mood_engine import update_current_mood
from screeninfo import get_monitors

import pygame
import os

# Mapping der Stimmung zu GIF-Dateien
MOOD_GIFS = {
    "fröhlich": "sprites/cat_idle.gif",
    "verspielt": "sprites/cat_play.gif",
    "ruhig": "sprites/cat_sit.gif",
    "müde": "sprites/cat_sleep.gif",
    "genervt": "sprites/cat_angry.gif",
    "traurig": "sprites/cat_sad.gif",
    "neugierig": "sprites/cat_look.gif",
    "nachdenklich": "sprites/cat_think.gif",
    "neutral": "sprites/cat_idle.gif"
}

def update_desktop_cat_mood(mood: str):
    """
    Diese Funktion aktualisiert den aktuellen Sprite der Desktop-Kimba
    basierend auf ihrer Stimmung.
    """
    sprite_path = MOOD_GIFS.get(mood, MOOD_GIFS["neutral"])
    
    if not os.path.exists(sprite_path):
        print(f"[WARNUNG] Sprite für Stimmung '{mood}' nicht gefunden: {sprite_path}")
        return
    
    # Speicher Sprite für anderen Prozess (z. B. Pygame-Loop)
    with open("desktop_kimba/current_sprite.txt", "w", encoding="utf-8") as f:
        f.write(sprite_path)

    print(f"[INFO] Desktop-Kimba-Sprite aktualisiert auf Stimmung: {mood} ({sprite_path})")


def load_gif(path):
    try:
        return pygame.image.load(path)
    except:
        print(f"[WARNUNG] GIF nicht gefunden: {path}")
        return pygame.Surface((100, 100))

def main():
    pygame.init()
    screen = get_monitors()[0]
    screen_width, screen_height = screen.width, screen.height

    cat_surface = pygame.display.set_mode((100, 100), pygame.NOFRAME)
    pygame.display.set_caption("Kimba Desktop")

    mood = update_current_mood()
    sprite_path = MOOD_GIFS.get(mood, MOOD_GIFS["neutral"])
    cat_sprite = load_gif(sprite_path)

    # Position zufällig unten am Bildschirm
    x = random.randint(0, screen_width - 100)
    y = screen_height - 120

    # Fensterposition anpassen (Linux-kompatibel)
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cat_surface.fill((0, 0, 0))
        cat_surface.blit(cat_sprite, (0, 0))
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
