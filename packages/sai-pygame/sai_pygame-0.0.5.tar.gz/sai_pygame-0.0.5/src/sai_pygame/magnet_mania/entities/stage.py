import pygame
import os
from ..assets import GAME_ASSETS_BASE
from ..helpers import get_squared_distance
from ..constants import STAGE_RADIUS, STAGE_POSITION, SCREEN_WIDTH, SCREEN_HEIGHT


class Stage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(GAME_ASSETS_BASE, "background.png"))
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()

    def outside_stage(self, position):
        squared_distance = get_squared_distance(position, STAGE_POSITION)
        return squared_distance > STAGE_RADIUS

    def check_fall(self, player_positions):
        falls = []
        for i, position in enumerate(player_positions):
            if self.outside_stage(position):
                falls.append(i)
        return falls
