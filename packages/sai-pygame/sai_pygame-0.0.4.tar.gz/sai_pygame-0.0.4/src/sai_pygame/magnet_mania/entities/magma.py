import pygame
from .bubble import Bubble
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Magma(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.sprites = sprites
        self.positions = [
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.83),
            (SCREEN_WIDTH * 0.85, SCREEN_HEIGHT * 0.75),
            (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.17),
            (SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.25),
            (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.53),
            (SCREEN_WIDTH * 0.12, SCREEN_HEIGHT * 0.68),
            (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.13),
            (SCREEN_WIDTH * 0.88, SCREEN_HEIGHT * 0.25),
            (SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.48),
            (SCREEN_WIDTH * 0.88, SCREEN_HEIGHT * 0.6),
            (SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85),
        ]
        self.sizes = [40, 50, 35, 55, 40, 25, 35, 55, 35, 55, 40]
        self.delays = [0, 60, 20, 5, 15, 90, 25, 110, 75, 30, 0]
        self.max_time_offscreen = 120
        self.bubble_metadata = [
            {
                "time_offscreen": self.max_time_offscreen - self.delays[i],
                "killed": self.delays[i] > 0,
            }
            for i in range(len(self.positions))
        ]
        self.bubbles = [
            Bubble(sprites, pos, self.sizes[i]) for i, pos in enumerate(self.positions)
        ]

    def update(self):
        for i, bubble in enumerate(self.bubbles):
            if not self.bubble_metadata[i]["killed"]:
                kill_bool = bubble.update()
                if kill_bool:
                    self.bubble_metadata[i]["killed"] = True
            else:
                self.bubble_metadata[i]["time_offscreen"] += 1
                if self.bubble_metadata[i]["time_offscreen"] >= self.max_time_offscreen:
                    self.bubble_metadata[i]["time_offscreen"] = 0
                    self.bubble_metadata[i]["killed"] = False
                    bubble.reset_animation()
