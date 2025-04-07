import pygame
import math
from ..constants import (
    BLACK,
    PLAYER_STARTING_ROTATIONS,
    DIRECTION_INDICATOR_SIZE,
    ROTATION_SPEED,
    DEFAULT_ROTATION,
)


class DirectionIndicator(pygame.sprite.Sprite):
    def __init__(self, id, player_position, color):
        super().__init__()

        self.id = id
        self.position = player_position
        self.rotation = DEFAULT_ROTATION
        self.original_image = pygame.Surface(
            [DIRECTION_INDICATOR_SIZE * 2, DIRECTION_INDICATOR_SIZE * 2]
        )
        self.original_image.fill(BLACK)
        self.original_image.set_colorkey(BLACK)

        self.draw(self.original_image, color)
        self.rect = self.original_image.get_rect()
        self.set_rotation(player_position, PLAYER_STARTING_ROTATIONS[self.id])

    def get_corner(self, rotation):
        return (
            self.position[0]
            + math.cos(math.radians(rotation)) * DIRECTION_INDICATOR_SIZE,
            self.position[1]
            + math.sin(math.radians(rotation)) * DIRECTION_INDICATOR_SIZE,
        )

    def draw(self, screen, color):
        tip = self.get_corner(DEFAULT_ROTATION)
        left_base = self.get_corner(DEFAULT_ROTATION - 120)
        right_base = self.get_corner(DEFAULT_ROTATION + 120)
        pygame.draw.polygon(screen, color, [tip, left_base, right_base])

    def get_rotation_offset(self):
        offset_factor = DIRECTION_INDICATOR_SIZE * 1.75
        radians = math.radians(self.rotation)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return [offset_factor * cos, -offset_factor * sin]

    def rotate(self, center, direction):
        rotation = (self.rotation + direction * ROTATION_SPEED) % 360
        self.set_rotation(center, rotation)

    def set_rotation(self, center, rotation):
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.set_position(center)

    def set_position(self, position):
        offset = self.get_rotation_offset()
        self.rect = self.image.get_rect(
            center=(position[0] + offset[0], position[1] + offset[1])
        )

    def change_color(self, color, position):
        self.original_image.fill(BLACK)
        self.draw(self.original_image, color)
        self.rect = self.original_image.get_rect()
        self.set_rotation(position, self.rotation)

    def reset(self):
        self.rotation = PLAYER_STARTING_ROTATIONS[self.id]
