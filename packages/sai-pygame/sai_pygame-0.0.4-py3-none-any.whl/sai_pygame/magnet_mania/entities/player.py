import pygame
import os
from ..assets import GAME_ASSETS_BASE
from .movable import Moveable
from .magnetic_wave import MagneticWave
from ..constants import (
    RED,
    GREEN,
    PLAYER_MAX_SPEED,
    PLAYER_VELOCITY_GROWTH,
    PLAYER_STARTING_POSITIONS,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    DEFAULT_ROTATION,
    WAVE_COST,
    WAVE_LIFE,
    PLAYER_STARTING_ROTATIONS,
    ROTATION_SPEED,
)


class Outliner:
    def __init__(self):
        self.convolution_mask = pygame.mask.Mask((3, 3), fill=True)

    def outline_surface(self, surface, color="black"):
        mask = pygame.mask.from_surface(surface)
        surface_outline = mask.convolve(self.convolution_mask).to_surface(
            setcolor=color, unsetcolor=surface.get_colorkey()
        )
        surface_outline.blit(surface, (1, 1))
        return surface_outline


class Player(Moveable):
    def __init__(self, id, magnetic_wave_sprites, projectiles):
        super().__init__(PLAYER_MAX_SPEED, PLAYER_VELOCITY_GROWTH)

        self.id = id
        self.set_starter_attributes()
        self.magnetic_wave_sprites = magnetic_wave_sprites
        self.projectiles = projectiles
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.rotation = DEFAULT_ROTATION

        self.image_base = pygame.image.load(
            os.path.join(GAME_ASSETS_BASE, "players/shadow.png")
        )
        self.image_base = pygame.transform.scale(
            self.image_base, (self.width, self.height)
        )
        self.original_image = pygame.image.load(
            os.path.join(GAME_ASSETS_BASE, "players/player-{}.png".format(id + 1))
        )
        self.original_image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.image_base.blit(self.original_image, (0, 0))
        self.rect = self.original_image.get_rect()
        self.position_rect = self.original_image.get_rect()

        self.outliner = Outliner()
        self.rotation = PLAYER_STARTING_ROTATIONS[self.id]
        self.set_rotation(self.position_rect.center)

    def set_center_position(self, position):
        super().set_center_position(position)

    def rotate(self, direction):
        self.rotation = (self.rotation + direction * ROTATION_SPEED) % 360
        self.set_rotation(self.position_rect.center)

    def set_rotation(self, center):
        self.image = pygame.transform.rotate(self.image_base, self.rotation + 90)
        self.image = self.outliner.outline_surface(self.image, self.get_charge_color())
        self.rect = self.image.get_rect(center=center)

    def set_position(self, position):
        self.rect.center = (position[0], position[1])

    def change_charge(self):
        self.charge *= -1
        self.set_rotation(self.position_rect.center)

    def get_charge_color(self):
        if self.charge == 1:
            return GREEN
        elif self.charge == -1:
            return RED

    def shoot(self):
        wave = MagneticWave(
            self.id,
            self.magnetic_wave_sprites,
            self.charge,
            self.get_charge_color(),
            self.power,
            self.position_rect.center,
            self.rotation,
        )
        self.power -= WAVE_COST
        return wave

    def reset_magnetization(self):
        self.magnetized = {"on": False, "power": 0, "charge": 1, "velocity": 0}

    def apply_magnetization(self, power, charge, velocity):
        if not self.magnetized["on"]:
            self.magnetized = {
                "on": True,
                "power": power,
                "charge": charge,
                "velocity": velocity,
            }

    def adjust_magnetized_velocity(self):
        factor = self.magnetized["charge"] * self.magnetized["power"]
        magnet_force = [v * factor for v in self.magnetized["velocity"]]
        self.velocity = [
            min(
                max(v + magnet_force[i] / 4, -abs(magnet_force[i])),
                abs(magnet_force[i]),
            )
            for i, v in enumerate(self.velocity)
        ]

    def fall(self):
        self.on_stage = False

    def remove_player(self):
        self.dead = True
        # self.kill()

    def update(self):
        if self.on_stage:
            if self.magnetized["on"]:
                self.magnetized["power"] = max(
                    self.magnetized["power"] - 1 / WAVE_LIFE, 0
                )
                if self.magnetized["power"] > 0:
                    self.adjust_magnetized_velocity()
                else:
                    self.reset_magnetization()
            if self.power < 1:
                self.power = min(self.power + 0.01, 1)
        else:
            slowdown_factor = 0.9
            self.velocity = [
                self.velocity[0] * slowdown_factor,
                self.velocity[1] * slowdown_factor,
            ]
            if self.opacity <= 0:
                self.remove_player()
            else:
                self.opacity = max(self.opacity - 5, 0)
                self.image.fill(
                    (255, 70, 20, self.opacity), None, pygame.BLEND_RGBA_MULT
                )
                if self.opacity < 200:
                    self.drowned = True

        self.set_position(self.position_rect.center)

    def set_starter_attributes(self):
        self.opacity = 255
        self.charge = 1
        self.power = 1
        self.on_stage = True
        self.dead = False
        self.drowned = False
        self.reset_magnetization()

    def reset(self):
        self.set_starter_attributes()
        self.set_center_position(PLAYER_STARTING_POSITIONS[self.id])
        self.rotation = PLAYER_STARTING_ROTATIONS[self.id]
        self.set_rotation(self.position_rect.center)
