import math
from sai_pygame.utils.animation import AnimationBase
from ..helpers import check_circle_circle_collision
from ..constants import (
    WAVE_RADIUS_MIN,
    WAVE_RADIUS_MAX,
    WAVE_LIFE,
    WAVE_SPEED,
    PLAYER_WIDTH,
)


class MagneticWave(AnimationBase):
    def __init__(
        self, id, all_sprites, charge, color, starting_power, position, rotation
    ):
        super().__init__(
            all_sprites[color], position, WAVE_RADIUS_MAX, 10, [2 for _ in range(10)]
        )

        self.owner = id
        self.charge = charge
        self.color = color
        self.power = 1  # starting_power
        self.rotation = rotation
        self.get_velocity(rotation)
        # self.adjust_radius()
        self.radius = WAVE_RADIUS_MIN * 0.5

        rotation_offset = self.get_rotation_offset()
        self.rect.x += int(rotation_offset[0] - PLAYER_WIDTH / 3)
        self.rect.y += int(rotation_offset[1] - PLAYER_WIDTH / 3)

    def get_rotation_offset(self):
        offset_factor = PLAYER_WIDTH  # / 2
        radians = math.radians(self.rotation)
        sin = math.sin(radians)
        cos = math.cos(radians)
        return [offset_factor * cos, -offset_factor * sin]

    def get_velocity(self, rotation):
        radians = math.radians(rotation)
        sin = math.sin(radians)
        cos = math.cos(radians)
        self.velocity = [cos * WAVE_SPEED, -sin * WAVE_SPEED]

    def get_opacity(self):
        return max(min(255 * self.power, 255), 0)

    def adjust_radius(self):
        self.radius = WAVE_RADIUS_MAX + (WAVE_RADIUS_MIN - WAVE_RADIUS_MAX) * self.power

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
        kill_bool = super().update()
        keep_wave = not kill_bool
        self.power = max(self.power - 1 / WAVE_LIFE, 0)
        self.move()
        return keep_wave
