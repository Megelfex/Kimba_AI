import pygame
import time
import random
import os
import sys
from screeninfo import get_monitors
from core.mood_engine import update_current_mood

# 🐱 Mapping zwischen Stimmungen und Sprite-Dateien (GIFs)
# 😺 Mood → Sprite path mapping
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
    EN: Updates the current desktop sprite of Kimba based on mood by saving the
    corresponding GIF path to a shared file. Used by the Pygame display loop.

    DE: Aktualisiert den Sprite der Desktop-Kimba je nach Stimmung, indem der
    Pfad zur GIF-Datei in eine gemeinsame Datei geschrieben wird. Wird von der Pygame-Schleife genutzt.

    Args:
        mood (str): Current mood keyword (e.g. "fröhlich", "genervt", etc.)
    """
    sprite_path = MOOD_GIFS.get(mood, MOOD_GIFS["neutral"])

    if not os.path.exists(sprite_path):
        print(f"[WARNUNG] Sprite für Stimmung '{mood}' nicht gefunden: {sprite_path}")
        return

    with open("desktop_kimba/current_sprite.txt", "w", encoding="utf-8") as f:
        f.write(sprite_path)

    print(f"[INFO] Desktop-Kimba-Sprite aktualisiert auf Stimmung: {mood} ({sprite_path})")

def load_gif(path):
    """
    EN: Loads a sprite (GIF) from file or returns fallback surface if not found.
    DE: Lädt einen Sprite (GIF) von der Festplatte oder gibt eine Ersatzfläche zurück.

    Args:
        path (str): Path to the GIF file.

    Returns:
        pygame.Surface: Loaded sprite surface or placeholder.
    """
    try:
        return pygame.image.load(path)
    except:
        print(f"[WARNUNG] GIF nicht gefunden: {path}")
        return pygame.Surface((100, 100))  # fallback black square

def main():
    """
    EN: Main loop to run the desktop Kimba avatar window using Pygame.
    Displays a sprite based on current mood and stays at a random bottom position on screen.

    DE: Hauptschleife für das Desktop-Kimba-Fenster via Pygame.
    Zeigt einen Sprite basierend auf der aktuellen Stimmung und positioniert sich zufällig am unteren Bildschirmrand.
    """
    pygame.init()
    screen = get_monitors()[0]
    screen_width, screen_height = screen.width, screen.height

    cat_surface = pygame.display.set_mode((100, 100), pygame.NOFRAME)
    pygame.display.set_caption("Kimba Desktop")

    mood = update_current_mood()
    sprite_path = MOOD_GIFS.get(mood, MOOD_GIFS["neutral"])
    cat_sprite = load_gif(sprite_path)

    # Random bottom position on screen
    x = random.randint(0, screen_width - 100)
    y = screen_height - 120

    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"  # For Linux window position

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cat_surface.fill((0, 0, 0))  # background color
        cat_surface.blit(cat_sprite, (0, 0))  # draw sprite
        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
