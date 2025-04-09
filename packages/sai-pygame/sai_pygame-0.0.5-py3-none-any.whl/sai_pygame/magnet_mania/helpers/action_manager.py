import pygame
from .input_tracker import InputTracker


class ActionManager:
    def __init__(self):
        self.player_input_mappings = [
            # Player 1
            {
                "up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "shoot": pygame.K_SPACE,
                "change_charge": pygame.K_l,
                "rotate_cc": pygame.K_j,
                "rotate_c": pygame.K_k,
            },
            # Player 2
            {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN,
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "shoot": pygame.K_KP0,
                "change_charge": pygame.K_KP1,
                "rotate_cc": pygame.K_KP2,
                "rotate_c": pygame.K_KP3,
            },
        ]
        self.input_tracker = InputTracker(
            self.get_input_keys(0) + self.get_input_keys(1)
        )

    def print_input_mapping(self):
        mapping = {
            "up": "W",
            "down": "S",
            "left": "A",
            "right": "D",
            "shoot": "SPACE",
            "change_charge": "L",
            "rotate_cc": "J",
            "rotate_c": "K",
        }
        print("\nInput Mappings\n")
        for key, item in mapping.items():
            print("{}: {}".format(key, item))

    def get_input_keys(self, i):
        return [v for v in self.player_input_mappings[i].values()]

    def get_player_action(self, i):
        mapping = self.player_input_mappings[i]
        if self.input_tracker.held[mapping["shoot"]] == 1:
            return 0  # Toggle magnet on/off
        elif self.input_tracker.held[mapping["change_charge"]] == 1:
            return 10  # Change magnet charge
        elif self.input_tracker.pressed[mapping["rotate_cc"]]:
            return 11  # Rotate counter clockwise
        elif self.input_tracker.pressed[mapping["rotate_c"]]:
            return 12  # Rotate clockwise
        elif self.input_tracker.pressed[mapping["up"]]:
            if self.input_tracker.pressed[mapping["left"]]:
                return 1  # Up-Left
            elif self.input_tracker.pressed[mapping["right"]]:
                return 2  # Up-Right
            else:
                return 3  # Up
        elif self.input_tracker.pressed[mapping["down"]]:
            if self.input_tracker.pressed[mapping["left"]]:
                return 4  # Down-Left
            elif self.input_tracker.pressed[mapping["right"]]:
                return 5  # Down-Right
            else:
                return 6  # Down
        elif self.input_tracker.pressed[mapping["left"]]:  # Left
            return 7
        elif self.input_tracker.pressed[mapping["right"]]:  # Right
            return 8
        return 9

    def get_action(self, keys_pressed, agent_id):
        self.input_tracker.press(keys_pressed)
        return self.get_player_action(agent_id)

    def reset(self):
        self.input_tracker.reset()
