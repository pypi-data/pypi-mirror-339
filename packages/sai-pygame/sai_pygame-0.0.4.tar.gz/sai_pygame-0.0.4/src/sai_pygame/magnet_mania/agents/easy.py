import random
import numpy as np
from math import atan2, degrees, pi, sin, cos, sqrt
from ..constants import STAGE_RADIUS, STAGE_POSITION

NUM_PLAYERS = 4

action_to_index = {
    "up": 3,
    "up-left": 1,
    "up-right": 2,
    "down": 6,
    "down-left": 4,
    "down-right": 5,
    "left": 7,
    "right": 8,
    "shoot": 0,
    "change_charge": 10,
    "rotate_cc": 11,
    "rotate_c": 12,
    "nothing": 9,
}


class EasyAgent:
    def __init__(self, id, players):
        self.id = id
        self.max_duration = 200
        self.randomly_select_target(players)

    def randomly_select_target(self, players):
        options = [
            i for i in range(NUM_PLAYERS) if i != self.id and not players[i].dead
        ]
        self.current_target = {"id": random.choice(options), "duration": 0}

    @staticmethod
    def get_angle_between_objects(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads), -sin(rads), cos(rads)

    def check_near_edge(self, p):
        return (
            sqrt((p[0] - STAGE_POSITION[0]) ** 2 + (p[1] - STAGE_POSITION[1]) ** 2)
            > STAGE_RADIUS * 0.9
        )

    @staticmethod
    def get_movement(vector, threshold):
        movement_string = ""
        if vector[1] > threshold:
            movement_string += "up"
        elif vector[1] < threshold:
            movement_string += "down"

        if abs(vector[0]) > threshold:
            if movement_string != "":
                movement_string += "-"
            if vector[0] > threshold:
                movement_string += "left"
            elif vector[0] < threshold:
                movement_string += "right"
        return movement_string

    @staticmethod
    def get_rot_diff(current_rot, rot):
        diff = rot - current_rot
        if diff < -180:
            diff += 360
        elif diff > 180:
            diff -= 360
        return diff

    @staticmethod
    def get_closest_rotation(diff):
        if diff > 180:
            return "rotate_c"
        elif diff < -180:
            return "rotate_cc"
        elif abs(diff) < 180:
            return "rotate_c" if diff > 0 else "rotate_cc"
        else:
            return "rotate_cc"

    def select_action(self, players):
        p1 = players[self.id].rect.center
        p2 = players[self.current_target["id"]].rect.center
        rot, _, _ = self.get_angle_between_objects(
            players[self.current_target["id"]].rect.center, players[self.id].rect.center
        )

        current_rot = (players[self.id].rotation) % 360
        action_string = "nothing"

        movement_string = ""
        if self.check_near_edge(p1):
            _, y_dir, x_dir = self.get_angle_between_objects(
                STAGE_POSITION,
                players[self.id].rect.center,
            )
            movement_string = self.get_movement([x_dir, y_dir], 0)
        else:
            movement_string = self.get_movement([p1[0] - p2[0], p1[1] - p2[1]], 100)

        if movement_string != "":
            action_string = movement_string
        else:
            diff = self.get_rot_diff(current_rot, rot)
            if self.id == 3:
                print(diff)
            if abs(diff) < 20 or (diff < 0 and abs(diff + 180) < 20):
                if np.random.rand() < 0.02:
                    action_string = "shoot"
            else:
                action_string = self.get_closest_rotation(diff)

        self.current_target["duration"] += 1
        if self.current_target["duration"] >= self.max_duration:
            self.randomly_select_target(players)

        return action_to_index[action_string]
