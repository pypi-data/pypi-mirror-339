import pygame
import math
import numpy as np

from gymnasium.spaces import Discrete, Box

from sai_pygame.utils.env import ArenaXGameBase
from sai_pygame.utils.sprites import load_sprites_from_separate_files

from .hud import HUD
from .entities import Player, Stage, Magma
from .constants import BLACK, RED, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from .assets import GAME_ASSETS_BASE
from .agents.easy import EasyAgent

FRAMERATE = 60

ACTION_MAPPING = {
    "up": (pygame.K_w, 1),
    "down": (pygame.K_s, 2),
    "left": (pygame.K_a, 3),
    "right": (pygame.K_d, 4),
}

DIRECTION_ACTIONS = {
    "up": [1, 2, 3],
    "down": [4, 5, 6],
    "left": [1, 4, 7],
    "right": [2, 5, 8],
}

NUM_PLAYERS = 4
TEAMMATES = {"0": 1, "1": 0, "2": 3, "3": 2}

agents = {"easy": EasyAgent}


class MagnetManiaEnv(ArenaXGameBase):
    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": FRAMERATE,
        "width": SCREEN_WIDTH,
        "height": SCREEN_HEIGHT,
        "engine": "pygame",
        "game_mode": ["free-for-all", "co-op"],
        "reward_functions": ["classic"],
    }

    def __init__(
        self,
        render_mode="rgb_array",
        game_mode="free-for-all",
        num_agents=1,
        primary_agent_id=0,
        seed=None,
        reward_function="classic",
        **kwags,
    ):
        # initialize game
        self.multi_agent_bool = True
        self.num_agents = num_agents
        self.primary_agent_id = primary_agent_id

        super().__init__(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            framerate=FRAMERATE,
            render_mode=render_mode,
            game_name="Magnet Mania - ArenaX Labs",
            action_mapping=ACTION_MAPPING,
            seed=seed,
            **kwags,
        )

        self.game_mode = (
            0 if game_mode == "free-for-all" else 1
        )  # 0: Free-for-All, 1: Co-operative

        if num_agents > NUM_PLAYERS:
            raise Exception("You cannot have more than {} agents".format(NUM_PLAYERS))

        self.magnetic_wave_sprites = {
            RED: load_sprites_from_separate_files(
                "{}/magnet-wave/magnet-wave--red-".format(GAME_ASSETS_BASE), 10
            ),
            GREEN: load_sprites_from_separate_files(
                "{}/magnet-wave/magnet-wave--green-".format(GAME_ASSETS_BASE), 10
            ),
        }

        # initialize paddles and ball
        self.num_agents = num_agents
        self.projectiles = []
        self.players = [
            Player(i, self.magnetic_wave_sprites, self.projectiles)
            for i in range(NUM_PLAYERS)
        ]
        self.stage = Stage()

        self.agent_difficulty = "easy"
        if self.num_agents < 4:
            self.cpus = [
                agents[self.agent_difficulty](i + self.num_agents, self.players)
                for i in range(4 - self.num_agents)
            ]

        # Create sprite sheets for animating
        bubble_sprites = load_sprites_from_separate_files(
            "{}/bubble/magma-bubble".format(GAME_ASSETS_BASE), 8
        )
        self.magma = Magma(bubble_sprites)

        # create the hud
        self.hud = HUD(self.players, bubble_sprites)
        self.death_bubbles = []

        # create a group of sprites for easier updating and rendering
        self.projectile_sprites_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.stage)
        self.all_sprites_list.add(self.players)
        self.all_sprites_list.add(self.magma.bubbles)

        # reset game
        self.reset()
        self.iteration = 0

        # define action and observation space
        self.possible_agents = ["player_" + str(r) for r in range(self.num_agents)]
        self.set_env_space()

        # get initial state
        self.init_obs = self.get_observation()

    def set_env_space(self):
        self.action_space = Discrete(13)
        self.observation_space = Box(
            low=np.array([-1] * 10 + [0] * 5), high=np.array([1] * 15), dtype=np.float64
        )

    def move_player(self, id, action):
        if action in DIRECTION_ACTIONS["up"]:
            self.players[id].move_up()
        elif action in DIRECTION_ACTIONS["down"]:
            self.players[id].move_down()
        else:
            self.players[id].settle_movement(1)

        if action in DIRECTION_ACTIONS["left"]:
            self.players[id].move_left()
        elif action in DIRECTION_ACTIONS["right"]:
            self.players[id].move_right()
        else:
            self.players[id].settle_movement(0)

    def rotate_player(self, id, action):
        if action == 11:
            self.players[id].rotate(1)
        elif action == 12:
            self.players[id].rotate(-1)

    def handle_magnetic_waves(self, id, action):
        if action == 0 and self.players[id].power > 0.1:
            wave = self.players[id].shoot()
            self.projectiles.append(wave)
            self.projectile_sprites_list.add(wave)
        elif action == 10:
            self.players[id].change_charge()

    def handle_action(self, action, i):
        for player in self.players:
            if player.id == i:
                if player.on_stage:
                    self.move_player(player.id, action)
                    self.rotate_player(player.id, action)
                    self.handle_magnetic_waves(player.id, action)
                if not player.dead:
                    player.apply_velocity()
                    player.update()

    def handle_cpu_actions(self):
        for i in range(self.num_agents, NUM_PLAYERS):
            action = self.cpus[i - self.num_agents].select_action(self.players)
            self.handle_action(action, i)
            # self.handle_action(9, i)

    def handle_projectile_collisions(self, projectile):
        for player in self.players:
            if player.id != projectile.owner:
                collision = projectile.check_collision(player)
                if collision:
                    player.apply_magnetization(
                        projectile.power, projectile.charge, projectile.velocity
                    )

    def update_projectiles(self):
        new_projectiles = []
        for projectile in self.projectiles:
            keep_projectile = projectile.update()
            if keep_projectile:
                new_projectiles.append(projectile)
                self.handle_projectile_collisions(projectile)
            else:
                projectile.kill()
        self.projectiles = new_projectiles

    def handle_stage_collisions(self):
        falls = self.stage.check_fall([player.rect.center for player in self.players])
        for player_idx in falls:
            self.players[player_idx].fall()

    def check_game_over(self):
        self.done = (
            sum([player.dead for player in self.players]) == NUM_PLAYERS - 1
            or self.players[0].dead
        )

    def render_death_bubbles(self, new_death_bubbles):
        if len(new_death_bubbles) > 0:
            for b in new_death_bubbles:
                self.death_bubbles.append(b)
                self.all_sprites_list.add(b.bubbles)

        bubbles_to_keep = []
        for death_bubble in self.death_bubbles:
            death_bubble.update()
            if len(death_bubble.bubbles) > 0:
                bubbles_to_keep.append(death_bubble)
        self.death_bubbles = bubbles_to_keep

    def get_player_position(self, i):
        return [
            ((self.players[i].rect.center[0] / self.screen_width) - 0.5) * 2,
            ((self.players[i].rect.center[1] / self.screen_height) - 0.5) * 2,
        ]

    def get_relative_distance(self, your_position, i):
        other_position = self.get_player_position(i)
        return [(p - other_position[j]) / 2 for j, p in enumerate(your_position)]

    def set_static_agents(self, static_agents):
        if len(static_agents) != self.num_agents - 1:
            raise ValueError(
                "Incorrect number of agents. Expecting {}".format(self.num_agents - 1)
            )
        self.static_agents = static_agents

    def single_agent_step(self, action, i):
        if not self.done:
            self.handle_action(action, i)
            if i == self.num_agents - 1:
                self.handle_cpu_actions()
                self.update_projectiles()
                self.handle_stage_collisions()
                self.check_game_over()
                super().step()

    def action_array_step(self, actions):
        for i in range(len(actions)):
            self.single_agent_step(actions[i], i)

    def all_agents_step(self, action):
        previous_state = self.get_observation_space()
        for i in range(self.num_agents):
            if i == self.primary_agent_id:
                self.single_agent_step(action, i)
            else:
                static_agent_action, _ = self.static_agents[i].predict(
                    previous_state[i], deterministic=False
                )
                self.single_agent_step(static_agent_action, i)

    def step(self, action):
        """
        Perform one step of the game, then extract the observation.
        """
        if isinstance(action, list):
            self.action_array_step(action)
        else:
            self.all_agents_step(action)
        self.iteration += 1

        observation = self.get_observation()

        done = self.done
        truncated = done or self.iteration > 3600  # Truncate at 1 min (at 60fps)
        reward = self.get_reward()

        info = {
            "timestep": self.iteration,
            "magnetized": [player.magnetized for player in self.players],
        }

        return observation, reward, done, truncated, info

    def reset(self, num_agents=1, **kwargs):
        """
        Reset the game state.
        """
        if "num_agents" in kwargs:
            self.num_agents = kwargs["num_agents"]

        self.set_env_space()
        super().reset()
        self.num_agents = num_agents
        self.reset_reward_tracker()
        [p.kill() for p in self.projectiles]
        self.projectiles = []
        self.hud.reset()
        for player in self.players:
            player.reset()
        self.iteration = 0

        observation = self.get_observation()

        info = {
            "timestep": self.iteration,
            "magnetized": [player.magnetized for player in self.players],
        }

        return observation, info

    def get_single_observation_space(self, i):
        agent_rotation = [
            math.sin(math.radians(self.players[i].rotation)),
            math.cos(math.radians(self.players[i].rotation)),
        ]
        agent_position = self.get_player_position(i)
        relative_distances = [
            distance
            for j in range(NUM_PLAYERS)
            if j != i
            for distance in self.get_relative_distance(agent_position, j)
        ]
        magnetized_inputs = [self.players[i].charge, self.players[i].power]
        death_inputs = [
            -int(self.players[j].dead) for j in range(NUM_PLAYERS) if j != i
        ]
        return (
            agent_rotation
            + agent_position
            + relative_distances
            + magnetized_inputs
            + death_inputs
        )

    def get_observation_space(self):
        return np.array(
            [self.get_single_observation_space(i) for i in range(self.num_agents)]
        )

    def get_observation(self):
        """
        Return the current observation from the game.
        """
        return self.get_observation_space()[self.primary_agent_id]

    def reset_reward_tracker(self):
        self.reward_tracker = {
            f"{state}": {i: False for i in range(NUM_PLAYERS)}
            for state in ["dead", "magnetized", "kill"]
        }

    def update_reward_tracker(self):
        self.reward_tracker = {
            "dead": {i: self.players[i].dead for i in range(NUM_PLAYERS)},
            "magnetized": {
                i: self.players[i].magnetized["on"] for i in range(NUM_PLAYERS)
            },
            "kill": {
                i: not self.reward_tracker["dead"][i] and self.players[i].dead
                for i in range(NUM_PLAYERS)
            },
        }

    def get_single_reward(self, i):
        reward = 0
        if self.done:
            if self.players[i].dead:
                reward = -2
            else:
                reward = 2
        else:
            for j in range(NUM_PLAYERS):
                if i != j:
                    if self.reward_tracker["kill"][j]:
                        reward += 0.5
        self.update_reward_tracker()
        return reward

    def get_all_reward(self):
        return [self.get_single_reward(i) for i in range(NUM_PLAYERS)]

    # def get_human_action(self, keys_pressed, agent_id=0):
    #     return self.action_manager.get_action(keys_pressed, agent_id)

    def get_reward(self):
        """
        Return the reward for the current state in the game.
        """
        return self.get_all_reward()[self.primary_agent_id]

    def render(self):
        """
        Render the game.
        """
        self.screen.fill(BLACK)
        self.all_sprites_list.draw(self.screen)
        self.projectile_sprites_list.draw(self.screen)
        new_death_bubbles = self.hud.update(self.screen, self.done)
        self.render_death_bubbles(new_death_bubbles)
        self.magma.update()
        return super().render()

    def close(self):
        """
        Close the game.
        """
        super().close()
