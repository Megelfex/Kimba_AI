import pygame
import time
import json
import os

pygame.init()
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("Kimba Desktop")

SPRITES = {
    "neutral": "cat_idle.gif",
    "verspielt": "cat_happy.gif",
    "nachdenklich": "cat_sad.gif",
    # weitere...
}

def get_current_mood():
    try:
        with open("desktop_kimba/current_mood.json", "r") as f:
            return json.load(f)["mood"]
    except:
        return "neutral"

def load_sprite(mood):
    path = os.path.join("desktop_kimba/sprites", SPRITES.get(mood, "cat_idle.gif"))
    return pygame.image.load(path)

clock = pygame.time.Clock()
current_sprite = load_sprite(get_current_mood())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))
    mood = get_current_mood()
    current_sprite = load_sprite(mood)
    screen.blit(current_sprite, (0, 0))
    pygame.display.update()
    clock.tick(1)
