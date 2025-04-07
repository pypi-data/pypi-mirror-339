import pygame
import random
import numpy as np
import gymnasium as gym
from typing import Optional

from sai_pygame.utils.play import ActionManager


class ArenaXGameBase(gym.Env):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "engine": "pygame",
    }

    def __init__(
        self,
        width: int,
        height: int,
        framerate: int,
        render_mode: str = "rgb_array",
        game_name: str = "SAI - Minigame",
        action_mapping: dict = {},
        seed: Optional[int] = None,
    ):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.framerate = framerate
        self.game_name = game_name

        self.action_manager = ActionManager(action_mapping)

        self.time = 0
        self.frame = 1
        self.done = False

        self.screen_width = width
        self.screen_height = height

        self.clock = pygame.time.Clock()
        self.set_render_mode(render_mode)

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    ## Custom methods
    def set_render_mode(self, new_render_mode):
        self.close()
        self.render_mode = new_render_mode

        pygame.font.init()
        if self.render_mode == "human":
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height)
            )
            pygame.display.set_caption(self.game_name)
        else:
            self.screen = pygame.Surface((self.screen_width, self.screen_height))

    def get_human_action(self, keys_pressed):
        return self.action_manager.get_action(keys_pressed)

    ## Gym methods
    def reset(self, **kwargs):
        """
        Reset the game to its initial state.
        """
        self.time = 0
        self.frame = 1
        self.done = False

    def step(self):
        """
        Move the game state forward one frame, given an action for the paddle(s).
        """
        # increment frame and update time
        self.frame += 1
        self.time = self.frame / self.framerate

    def render(self):
        """
        Render the game based on the mode.
        """
        self.clock.tick(self.framerate)
        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.flip()
        elif self.render_mode == "rgb_array":
            return np.flipud(
                np.rot90(np.array(pygame.surfarray.pixels3d(self.screen)), k=1)
            )

    def close(self):
        pygame.quit()
