import pygame
from ..constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverScreen:
    def __init__(self):
        self.font = pygame.font.Font("freesansbold.ttf", 64)
        self.text = self.font.render("GAME OVER", True, WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))

    def render(self, surface):
        surface.blit(self.text, self.text_rect)
