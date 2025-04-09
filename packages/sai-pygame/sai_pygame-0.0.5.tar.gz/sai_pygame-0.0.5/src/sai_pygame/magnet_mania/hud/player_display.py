import pygame
import numpy as np
from ..constants import SCREEN_HEIGHT, SCREEN_WIDTH
from ..assets import GAME_ASSETS_BASE


class PlayerDisplay:
    def __init__(self, name, position, id):
        self.name = name
        self.id = id

        self.original_image = pygame.image.load(
            "{}/hud-cards/hud-card-{}.png".format(GAME_ASSETS_BASE, id + 1)
        )
        self.image = pygame.transform.scale(
            self.original_image, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 9)
        )
        self.rect = self.image.get_rect(center=position)

        self.dead = False

    def grayscale(self):
        arr = pygame.surfarray.pixels3d(self.image)
        grayscale_arr = np.dot(arr[..., :3], [0.298, 0.587, 0.114])
        grayscale_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        for channel in range(3):  # Loop through R, G, B channels
            pygame.surfarray.pixels3d(grayscale_surface)[:, :, channel] = grayscale_arr
        alpha_channel = pygame.surfarray.pixels_alpha(self.image)
        pygame.surfarray.pixels_alpha(grayscale_surface)[:] = alpha_channel
        self.image = grayscale_surface
        self.dead = True

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def reset(self):
        self.dead = False
        self.image = pygame.transform.scale(
            self.original_image, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 9)
        )
