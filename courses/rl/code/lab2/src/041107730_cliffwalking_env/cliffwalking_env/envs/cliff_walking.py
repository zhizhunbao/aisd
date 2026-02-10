# cliffwalking_env/envs/cliff_walking.py
#
# Copied from grid_world.py and modified:
# - Renamed GridWorldEnv -> CliffWalkingEnv
# - Changed 5x5 grid to 12x4 grid (size=(12,4))
# - Added cliff cells, start position, goal position
# - Reward: -1 per step, -100 for cliff, episode ends at goal

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

# Grid dimensions
GRID_WIDTH = 12
GRID_HEIGHT = 4

# Reward constants
REWARD_STEP = -1
REWARD_CLIFF = -100

# Rendering constants
RENDER_FPS = 10
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_CLIFF = (128, 128, 128)
COLOR_GOAL = (0, 255, 0)
COLOR_START = (255, 255, 0)
COLOR_AGENT = (0, 0, 255)


class CliffWalkingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": RENDER_FPS}

    def __init__(self, render_mode=None, size=(GRID_WIDTH, GRID_HEIGHT)):
        self.xsize = size[0]
        self.ysize = size[1]
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT

        # Observation space: agent and target positions on the grid
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([self.xsize - 1, self.ysize - 1]),
                    shape=(2,),
                    dtype=int,
                ),
                "target": spaces.Box(
                    low=np.array([0, 0]),
                    high=np.array([self.xsize - 1, self.ysize - 1]),
                    shape=(2,),
                    dtype=int,
                ),
            }
        )

        # 4 actions: left, right, up, down
        self.action_space = spaces.Discrete(4)

        self._action_to_direction = {
            0: np.array([-1, 0]),  # left
            1: np.array([1, 0]),   # right
            2: np.array([0, -1]),  # up
            3: np.array([0, 1]),   # down
        }

        # Fixed start and goal positions
        self._start_location = np.array([0, self.ysize - 1])
        self._target_location = np.array([self.xsize - 1, self.ysize - 1])
        self._agent_location = self._start_location.copy()

        # Cliff: bottom row, columns 1 through 10
        self._cliff_columns = list(range(1, self.xsize - 1))
        self._cliff_row = self.ysize - 1

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
            "agent": self._agent_location.copy(),
            "target": self._target_location.copy(),
        }

    def _get_info(self):
        return {
            "distance": np.abs(self._agent_location - self._target_location).sum()
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Always start at the start position
        self._agent_location = self._start_location.copy()

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # SB3 may pass numpy array actions; convert to int for dict key lookup
        direction = self._action_to_direction[int(action)]

        # Move agent with boundary clipping
        new_location = self._agent_location + direction
        self._agent_location = np.clip(
            new_location,
            [0, 0],
            [self.xsize - 1, self.ysize - 1],
        )

        # Check if agent fell into cliff
        fell_in_cliff = (
            self._agent_location[1] == self._cliff_row
            and self._agent_location[0] in self._cliff_columns
        )

        if fell_in_cliff:
            reward = REWARD_CLIFF
            self._agent_location = self._start_location.copy()
            terminated = False
        else:
            reached_goal = np.array_equal(self._agent_location, self._target_location)
            reward = REWARD_STEP
            terminated = reached_goal

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_width, self.window_height))
        canvas.fill(COLOR_WHITE)

        pix_x = self.window_width // self.xsize
        pix_y = self.window_height // self.ysize

        # Draw cliff cells (grey)
        for col in self._cliff_columns:
            pygame.draw.rect(
                canvas,
                COLOR_CLIFF,
                pygame.Rect(col * pix_x, self._cliff_row * pix_y, pix_x, pix_y),
            )

        # Draw goal (green)
        pygame.draw.rect(
            canvas,
            COLOR_GOAL,
            pygame.Rect(
                self._target_location[0] * pix_x,
                self._target_location[1] * pix_y,
                pix_x,
                pix_y,
            ),
        )

        # Draw start (yellow)
        pygame.draw.rect(
            canvas,
            COLOR_START,
            pygame.Rect(
                self._start_location[0] * pix_x,
                self._start_location[1] * pix_y,
                pix_x,
                pix_y,
            ),
        )

        # Draw agent (blue circle)
        pygame.draw.circle(
            canvas,
            COLOR_AGENT,
            (
                int((self._agent_location[0] + 0.5) * pix_x),
                int((self._agent_location[1] + 0.5) * pix_y),
            ),
            min(pix_x, pix_y) // 3,
        )

        # Draw gridlines
        for x in range(self.xsize + 1):
            pygame.draw.line(
                canvas, COLOR_BLACK,
                (x * pix_x, 0), (x * pix_x, self.window_height),
                width=1,
            )
        for y in range(self.ysize + 1):
            pygame.draw.line(
                canvas, COLOR_BLACK,
                (0, y * pix_y), (self.window_width, y * pix_y),
                width=1,
            )

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
