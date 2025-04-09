import pygame
from ..constants import RED, BLACK, BEAM_SPEED, BEAM_HEIGHT, BEAM_WIDTH


class Beam(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.reset()
        self.image = pygame.Surface([BEAM_WIDTH, BEAM_HEIGHT])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, RED, [0, 0, BEAM_WIDTH, self.current_height])
        self.rect = self.image.get_rect()

    def change_charge(self):
        self.charge *= -1

    def toggle(self):
        self.on = not self.on
        if self.on:
            self.growth_increment = BEAM_SPEED
        else:
            self.growth_increment = -BEAM_SPEED

    def adjust_size(self):
        if (self.on and self.current_height < BEAM_HEIGHT) or (
            not self.on and self.current_height > 0
        ):
            self.current_height += self.growth_increment
            self.current_height = max(min(self.current_height, BEAM_HEIGHT), 0)

            self.image.fill(BLACK)
            pygame.draw.rect(self.image, RED, [0, 0, BEAM_WIDTH, self.current_height])

    def rotate(self, rotation):
        pass

    def set_position(self, position):
        pass

    def reset(self):
        self.on = False
        self.charge = -1
        self.current_height = 0
