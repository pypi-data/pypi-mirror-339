import pygame
import math
from ..helpers import check_circle_circle_collision
from ..constants import BLACK, WAVE_RADIUS_MIN, WAVE_RADIUS_MAX, WAVE_LIFE, WAVE_SPEED


class MagneticWave(pygame.sprite.Sprite):
    def __init__(self, id, charge, color, starting_power, position, rotation):
        super().__init__()

        self.owner = id
        self.charge = charge
        self.color = color
        self.power = starting_power
        self.image = pygame.Surface(
            [WAVE_RADIUS_MAX * 2, WAVE_RADIUS_MAX * 2], pygame.SRCALPHA
        )
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.get_velocity(rotation)
        self.adjust_radius()
        self.draw()
        self.rect = self.image.get_rect(center=position)

    def get_velocity(self, rotation):
        radians = math.radians(rotation)
        sin = math.sin(radians)
        cos = math.cos(radians)
        self.velocity = [cos * WAVE_SPEED, -sin * WAVE_SPEED]

    def get_opacity(self):
        return max(min(255 * self.power, 255), 0)

    def adjust_radius(self):
        self.radius = WAVE_RADIUS_MAX + (WAVE_RADIUS_MIN - WAVE_RADIUS_MAX) * self.power

    def draw(self):
        self.image.fill(BLACK)
        pygame.draw.circle(
            self.image,
            self.color + (self.get_opacity(),),
            (WAVE_RADIUS_MAX, WAVE_RADIUS_MAX),
            self.radius,
        )

    def check_collision(self, object):
        return check_circle_circle_collision(
            self.rect.center,
            object.rect.center,
            self.radius,
            object.width,  # hack that assumes it is a square
        )

    def set_position(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def move(self):
        self.rect.x += int(self.velocity[0])
        self.rect.y += int(self.velocity[1])

    def update(self):
        keep_wave = True
        self.power = max(self.power - 1 / WAVE_LIFE, 0)
        self.adjust_radius()
        self.move()
        self.draw()
        if self.power <= 0:
            keep_wave = False
        return keep_wave
