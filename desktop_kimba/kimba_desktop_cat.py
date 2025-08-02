import os
import pygame

class AnimatedCat:
    def __init__(self, sprite_path, position):
        """
        Initialisiert die Desktop-Katze.
        DE: Lädt Sprite oder Platzhalter, falls Sprite fehlt.
        """
        self.position = position
        self.sprite = self.load_sprite(sprite_path)

    def load_sprite(self, path):
        """
        Lädt das Sprite-Bild oder verwendet ein Platzhalterbild,
        falls die Datei nicht existiert.
        """
        if not os.path.exists(path):
            print(f"[WARNUNG] Sprite nicht gefunden: {path} – verwende Platzhalter.")
            # Platzhalter erstellen (50x50 Pixel, grau)
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((200, 200, 200))
            return placeholder
        else:
            return pygame.image.load(path)

    def run(self):
        """
        Startet die Katze als eigenständiges Pygame-Fenster.
        """
        pygame.init()
        screen = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("Kimba Desktop Cat")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            screen.blit(self.sprite, self.position)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    print("[INFO] Starte Desktop-Katze im Testmodus...")
    try:
        cat = AnimatedCat("sprites/cat_idle.gif", (100, 100))
        cat.run()
    except Exception as e:
        print(f"[ERROR] Katze konnte nicht gestartet werden: {e}")
