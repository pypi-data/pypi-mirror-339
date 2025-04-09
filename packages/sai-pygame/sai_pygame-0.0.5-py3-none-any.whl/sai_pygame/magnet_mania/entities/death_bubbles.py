import pygame
from .bubble import Bubble
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT


class DeathBubbles(pygame.sprite.Sprite):
    def __init__(self, sprites, position):
        super().__init__()
        self.sprites = sprites
        self.positions = [
            (position[0] - SCREEN_WIDTH * 0.015, position[1] + SCREEN_HEIGHT * 0.01),
            (position[0] - SCREEN_WIDTH * 0.01, position[1] - SCREEN_HEIGHT * 0.015),
            (position[0] + SCREEN_WIDTH * 0.025, position[1]),
        ]
        self.sizes = [
            40,
            50,
            35,
        ]
        self.delays = [
            0,
            30,
            10,
        ]
        self.bubbles = [
            Bubble(sprites, pos, self.sizes[i]) for i, pos in enumerate(self.positions)
        ]

    def update(self):
        new_bubbles = []
        for i, bubble in enumerate(self.bubbles):
            if self.delays[i] == 0:
                kill_bool = bubble.update()
            else:
                bubble.image = bubble.empty_surface
                self.delays[i] -= 1
                kill_bool = False
            if not kill_bool:
                new_bubbles.append(bubble)
        self.bubbles = new_bubbles
