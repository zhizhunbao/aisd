"""
CST8509 Lab 2: Cliff Walking Gymnasium Environment
Author: Peng Wang
Student Number: 041107730

Description:
A custom Gymnasium environment for the Cliff Walking problem.
The environment uses a 12x4 grid where the agent must navigate from start to goal
while avoiding a "cliff" that sends it back to the start with a large penalty.
"""

# 导入 Gymnasium 核心模块和空间控制模块
# Import Gymnasium core modules and spaces for environment definition
import gymnasium as gym
from gymnasium import spaces

# 导入 PyGame 用于图形化渲染
# Import PyGame for graphical rendering
import pygame

# 导入 NumPy 用于数值计算和阵列操作
# Import NumPy for numerical calculations and array operations
import numpy as np


class CliffWalkingEnv(gym.Env):
    """悬崖行走 Gymnasium 环境类
    Cliff Walking Gymnasium Environment class"""

    # 定义渲染元数据和帧率
    # Define rendering metadata and frame rate
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=(12, 4)):
        """初始化环境，设置网格尺寸和动作空间
        Initialize environment, set grid size and action space"""

        # 设置网格的 X 和 Y 轴尺寸
        # Set X and Y dimensions of the grid
        self.xsize, self.ysize = size
        
        # 设置 PyGame 窗口的基础尺寸
        # Set base size for the PyGame window
        self.window_size = 512

        # 定义观测空间：包含代理位置和目标位置的字典
        # Define observation space: dictionary containing agent and target locations
        # 范围限定在 [0, xsize-1] 和 [0, ysize-1] 之间
        # Range limited between [0, xsize-1] and [0, ysize-1]
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(
                    low=np.array([0, 0]), 
                    high=np.array([self.xsize - 1, self.ysize - 1]), 
                    shape=(2,), 
                    dtype=int
                ),
                "target": spaces.Box(
                    low=np.array([0, 0]), 
                    high=np.array([self.xsize - 1, self.ysize - 1]), 
                    shape=(2,), 
                    dtype=int
                ),
            }
        )

        # 定义动作空间：4个离散动作（左、右、上、下）
        # Define action space: 4 discrete actions (left, right, up, down)
        self.action_space = spaces.Discrete(4)

        # 映射抽象动作到具体的坐标移动向量
        # Map abstract actions to specific coordinate movement vectors
        # 遵循实验室标准：0:左, 1:右, 2:上, 3:下
        # Following lab standard: 0:left, 1:right, 2:up, 3:down
        self._action_to_direction = {
            0: np.array([-1, 0]), # 左 / Left
            1: np.array([1, 0]),  # 右 / Right
            2: np.array([0, -1]), # 上 / Up
            3: np.array([0, 1]),  # 下 / Down
        }

        # 验证渲染模式是否合法
        # Validate if the render mode is valid
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # 初始化渲染相关的窗口和时钟对象
        # Initialize rendering related window and clock objects
        self.window = None
        self.clock = None

    def _get_obs(self):
        """获取当前的观测字典
        Get the current observation dictionary"""

        # 返回包含代理和目标位置的字典
        # Return dictionary with agent and target locations
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        """获取辅助信息（如曼哈顿距离）
        Get auxiliary information (such as Manhattan distance)"""

        # 计算代理到目标的 L1 范数距离
        # Calculate L1 norm distance from agent to target
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
        """重置环境到初始状态
        Reset environment to initial state"""

        # 调用父类的 reset 以处理种子
        # Call parent reset to handle seeding
        super().reset(seed=seed)

        # 设置代理起始位置为左下角 (0, 3)
        # Set agent start position to bottom-left (0, 3)
        self._agent_location = np.array([0, 3])

        # 设置目标位置为右下角 (11, 3)
        # Set target location to bottom-right (11, 3)
        self._target_location = np.array([11, 3])

        # 获取初始观测和信息
        # Get initial observation and info
        observation = self._get_obs()
        info = self._get_info()

        # 如果开启了 human 渲染模式，执行渲染
        # If human render mode is enabled, perform rendering
        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        """执行一个动作并返回结果
        Execute an action and return results"""

        # 获取动作对应的移动方向
        # Get movement direction corresponding to the action
        direction = self._action_to_direction[action]
        
        # 更新代理位置并限制在网格边界内
        # Update agent location and clip within grid boundaries
        self._agent_location = np.clip(
            self._agent_location + direction,
            [0, 0],
            [self.xsize - 1, self.ysize - 1],
        )

        # 初始化终止状态和默认每步奖励
        # Initialize termination flag and default step reward
        terminated = False
        reward = -1
        
        # 检查是否掉入悬崖（Y=3 且 X 在 1 到 10 之间）
        # Check if agent falls into cliff (Y=3 and X between 1 and 10)
        # 原因：这是悬崖行走问题的核心惩罚逻辑
        # Reason: This is the core penalty logic of the Cliff Walking problem
        if self._agent_location[1] == 3 and 1 <= self._agent_location[0] <= 10:
            # 掉入悬崖：给予大负惩罚并返回起点
            # Fall into cliff: give large negative penalty and return to start
            reward = -100
            self._agent_location = np.array([0, 3])
        else:
            # 检查是否到达目标位置
            # Check if target location is reached
            terminated = np.array_equal(self._agent_location, self._target_location)
            if terminated:
                # 到达目标：奖励为 0
                # Reached goal: reward is 0
                reward = 0

        # 获取新的观测和辅助信息
        # Get new observation and auxiliary info
        observation = self._get_obs()
        info = self._get_info()

        # 执行渲染
        # Perform rendering
        if self.render_mode == "human":
            self._render_frame()

        # 返回 5 元组：观测、奖励、终止、截断、信息
        # Return 5-tuple: observation, reward, terminated, truncated, info
        return observation, reward, terminated, False, info

    def render(self):
        """由 Gymnasium 环境调用的渲染接口
        Rendering interface called by Gymnasium environment"""

        # 支持 rgb_array 模式返回图像数组
        # Support rgb_array mode to return image array
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        """渲染一帧画面
        Render a single frame"""

        # 如果窗口尚未初始化，创建 PyGame 窗口
        # If window is not initialized, create PyGame window
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("CST8509 Lab 2: Cliff Walking")
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            
        # 如果时钟尚未初始化，创建 PyGame 时钟
        # If clock is not initialized, create PyGame clock
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # 创建一个画布并填充白色背景
        # Create a canvas and fill with white background
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        
        # 计算单个网格方块在像素中的尺寸
        # Calculate size of a single grid square in pixels
        pix_square_size_x = self.window_size / self.xsize
        pix_square_size_y = self.window_size / self.ysize

        # 绘制目标位置（绿色方块）
        # Draw target location (green square)
        pygame.draw.rect(
            canvas,
            (0, 255, 0),
            pygame.Rect(
                (self._target_location[0] * pix_square_size_x, self._target_location[1] * pix_square_size_y),
                (pix_square_size_x, pix_square_size_y),
            ),
        )
        
        # 绘制悬崖区域（灰色方块）
        # Draw cliff area (grey squares)
        # 原因：让用户直观看到不可触碰的危险区域
        # Reason: Let user visually see the dangerous zones that shouldn't be touched
        for x in range(1, 11):
            pygame.draw.rect(
                canvas,
                (128, 128, 128),
                pygame.Rect(
                    (x * pix_square_size_x, 3 * pix_square_size_y),
                    (pix_square_size_x, pix_square_size_y),
                ),
            )

        # 绘制代理（蓝色圆形）
        # Draw the agent (blue circle)
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (
                int((self._agent_location[0] + 0.5) * pix_square_size_x),
                int((self._agent_location[1] + 0.5) * pix_square_size_y),
            ),
            int(min(pix_square_size_x, pix_square_size_y) / 3),
        )

        # 绘制网格线以区分状态
        # Draw grid lines to distinguish states
        for x in range(self.xsize + 1):
            pygame.draw.line(
                canvas,
                (200, 200, 200),
                (pix_square_size_x * x, 0),
                (pix_square_size_x * x, self.window_size),
                width=1,
            )
        for y in range(self.ysize + 1):
            pygame.draw.line(
                canvas,
                (200, 200, 200),
                (0, pix_square_size_y * y),
                (self.window_size, pix_square_size_y * y),
                width=1,
            )

        # 如果是 human 模式，将画布刷新到可见窗口
        # If in human mode, blit canvas to the visible window
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            
            # 维持稳定的帧率
            # Maintain a stable frame rate
            self.clock.tick(self.metadata["render_fps"])
        else:
            # 返回图像数组
            # Return image array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def close(self):
        """关闭环境，释放 PyGame 资源
        Close environment, release PyGame resources"""

        # 如果窗口存在，退出 PyGame
        # If window exists, quit PyGame
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None
