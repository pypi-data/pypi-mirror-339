import pygame
import math
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Moveable(pygame.sprite.Sprite):
    def __init__(self, speed, velocity_growth):
        super().__init__()
        self.position_rect = pygame.Rect(0, 0, 0, 0)
        self.speed = speed
        self.velocity_growth = velocity_growth
        self.velocity = [0, 0]
        self.width = self.width or 0
        self.height = self.height or 0

    def set_center_position(self, position):
        self.position_rect.x = position[0] - self.width / 2
        self.position_rect.y = position[1] - self.height / 2

    def adjust_velocity(self, delta):
        self.velocity = [
            min(max(v + delta[i], -self.speed), self.speed)
            for i, v in enumerate(self.velocity)
        ]

    def check_bounds(self, target_position):
        if target_position[0] < self.width / 2:
            target_position[0] = self.width / 2
            self.velocity[0] = 0
        elif target_position[0] > SCREEN_WIDTH - self.width / 2:
            target_position[0] = SCREEN_WIDTH - self.width / 2
            self.velocity[0] = 0
        elif target_position[1] < self.height / 2:
            target_position[1] = self.height / 2
            self.velocity[1] = 0
        elif target_position[1] > SCREEN_HEIGHT - self.height / 2:
            target_position[1] = SCREEN_HEIGHT - self.height / 2
            self.velocity[1] = 0
        return target_position

    def apply_velocity(self):
        target_position = [
            self.position_rect.center[0] + self.velocity[0],
            self.position_rect.center[1] + self.velocity[1],
        ]
        adjusted_position = self.check_bounds(target_position)
        self.set_center_position(adjusted_position)

    def move_up(self):
        self.adjust_velocity([0, -self.velocity_growth])

    def move_down(self):
        self.adjust_velocity([0, self.velocity_growth])

    def move_left(self):
        self.adjust_velocity([-self.velocity_growth, 0])

    def move_right(self):
        self.adjust_velocity([self.velocity_growth, 0])

    def settle_movement(self, axis):
        self.velocity[axis] -= (
            math.copysign(1, self.velocity[axis]) * self.velocity_growth / 2
        )
