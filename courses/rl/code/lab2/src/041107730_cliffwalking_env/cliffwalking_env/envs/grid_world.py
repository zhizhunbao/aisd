"""
Lab 2: GridWorld Gymnasium Environment (Original Template)
Author: Peng Wang
Student Number: 041107730

Original 5x5 GridWorld environment from Gymnasium tutorial.
This is the base template that was copied and modified into CliffWalkingEnv.
Reference: https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

# 导入枚举类型，用于定义离散动作
# Import Enum type for defining discrete actions
from enum import Enum

# 导入numpy用于数组操作
# Import numpy for array operations
import numpy as np

# 导入pygame用于图形渲染
# Import pygame for graphical rendering
import pygame

# 导入gymnasium核心模块
# Import gymnasium core module
import gymnasium as gym

# 导入gymnasium空间定义
# Import gymnasium space definitions
from gymnasium import spaces


# ============================================================
# Actions: 动作枚举定义
#          Action enumeration definition
# ============================================================
class Actions(Enum):
    """动作枚举定义
    Action enumeration definition"""

    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


# ============================================================
# GridWorldEnv: 5x5网格世界Gymnasium环境（原始模板）
#               5x5 GridWorld Gymnasium Environment (original template)
# ============================================================
class GridWorldEnv(gym.Env):
    """5x5网格世界Gymnasium环境（原始模板）
    5x5 GridWorld Gymnasium Environment (original template)"""

    # ============================================================
    # 渲染常量
    # Rendering Constants
    # ============================================================

    # 渲染帧率（每秒刷新次数）
    # Render FPS (frames per second)
    RENDER_FPS = 4

    # PyGame窗口尺寸（像素，正方形窗口）
    # PyGame window size (pixels, square window)
    WINDOW_SIZE = 512

    # 网格线宽度（像素）
    # Grid line width (pixels)
    GRID_LINE_WIDTH = 3

    # 智能体圆形半径缩放因子（格子尺寸 / 此值 = 圆形半径）
    # Agent circle radius scale factor (cell size / this value = circle radius)
    AGENT_RADIUS_DIVISOR = 3

    # 坐标偏移常量（用于将中心对齐到格点）
    # Coordinate offset constant (used to center items in a grid cell)
    CENTER_OFFSET = 0.5

    # ============================================================
    # 颜色常量 (RGB)
    # Color Constants (RGB)
    # ============================================================

    # 白色背景
    # White background
    COLOR_WHITE = (255, 255, 255)

    # 红色目标
    # Red target
    COLOR_TARGET = (255, 0, 0)

    # 蓝色智能体
    # Blue agent
    COLOR_AGENT = (0, 0, 255)

    # 黑色网格线
    # Black grid lines
    COLOR_GRID = (0, 0, 0)

    # ============================================================
    # 动作常量
    # Action Constants
    # ============================================================

    # 动作数量（右、上、左、下）
    # Number of actions (right, up, left, down)
    NUM_ACTIONS = 4

    # 定义渲染模式元数据
    # Define rendering mode metadata
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": RENDER_FPS}

    # ============================================================
    # __init__: 初始化网格世界环境
    #           Initialize GridWorld environment
    #
    # Parameters:
    #   render_mode: 渲染模式
    #                Render mode ("human" or "rgb_array" or None)
    #   size: 网格边长（正方形网格）
    #         Grid side length (square grid)
    # ============================================================
    def __init__(self, render_mode=None, size=5):
        # 设置网格尺寸
        # Set grid size
        self.size = size

        # 设置PyGame窗口尺寸
        # Set PyGame window size
        self.window_size = self.WINDOW_SIZE

        # 定义观察空间（字典类型，包含agent和target位置）
        # Define observation space (Dict type containing agent and target locations)
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0, size - 1, shape=(2,), dtype=int),
                "target": spaces.Box(0, size - 1, shape=(2,), dtype=int),
            }
        )

        # 初始化智能体和目标位置（-1表示尚未设置）
        # Initialize agent and target positions
        self._agent_location = np.array([-1, -1], dtype=int)
        self._target_location = np.array([-1, -1], dtype=int)

        # 定义动作空间：4个离散动作
        # Define action space: 4 discrete actions
        self.action_space = spaces.Discrete(self.NUM_ACTIONS)

        # 动作到方向的映射
        # Action to direction mapping
        self._action_to_direction = {
            Actions.RIGHT.value: np.array([0, 1]),   # 右 / right
            Actions.UP.value: np.array([-1, 0]),     # 上 / up
            Actions.LEFT.value: np.array([0, -1]),   # 左 / left
            Actions.DOWN.value: np.array([1, 0]),    # 下 / down
        }

        # 验证渲染模式
        # Validate render mode
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # PyGame初始化（延迟到需要时）
        # PyGame initialization (deferred until needed)
        self.window = None
        self.clock = None

    # ============================================================
    # _get_obs: 获取当前观察
    #           Get current observation
    #
    # Returns:
    #   dict: 包含 agent 和 target 位置的字典
    # ============================================================
    def _get_obs(self):
        # 返回当前状态字典
        # Return current state dictionary
        return {
            "agent": self._agent_location,
            "target": self._target_location,
        }

    # ============================================================
    # _get_info: 获取附加信息
    #            Get additional info
    #
    # Returns:
    #   dict: 包含曼哈顿距离等调试信息
    # ============================================================
    def _get_info(self):
        # 计算曼哈顿距离（L1距离）
        # Calculate Manhattan distance (L1 distance)
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    # ============================================================
    # reset: 重置环境到初始状态
    #        Reset environment to initial state
    #
    # Parameters:
    #   seed: 随机种子，用于复现实验结果
    #   options: 额外选项（当前未使用）
    #
    # Returns:
    #   tuple[dict, dict]: (observation, info)
    # ============================================================
    def reset(self, seed=None, options=None):
        # 调用父类reset设置随机种子
        # Call parent reset to set random seed
        super().reset(seed=seed)

        # 随机放置智能体
        # Randomly place agent
        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # 随机放置目标（确保与智能体不重叠）
        # Randomly place target (ensure no overlap with agent)
        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )

        # 获取观察和信息
        # Get observation and info
        observation = self._get_obs()
        info = self._get_info()

        # 如果是human模式，渲染
        # If human mode, render
        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    # ============================================================
    # step: 执行一个动作并返回环境反馈
    #       Execute an action and return environment feedback
    #
    # Parameters:
    #   action: 离散动作编号 (0=右, 1=上, 2=左, 3=下)
    #
    # Returns:
    #   tuple[dict, int, bool, bool, dict]:
    #     (observation, reward, terminated, truncated, info)
    # ============================================================
    def step(self, action):
        # 获取动作对应的移动方向
        # Get movement direction for action
        direction = self._action_to_direction[action]

        # 计算新位置（带边界约束）
        # Calculate new position (with boundary constraints)
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )

        # 检查是否到达目标（获得+1奖励）
        # Check if reached target (earn +1 reward)
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0

        # 获取观察和信息
        # Get observation and info
        observation = self._get_obs()
        info = self._get_info()

        # 如果是human模式，渲染
        # If human mode, render
        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    # ============================================================
    # render: 渲染当前状态
    #         Render current state
    #
    # Returns:
    #   Optional[np.ndarray]: 如果模式为 rgb_array 则返回图像数组
    # ============================================================
    def render(self):
        # 如果是 rgb_array 模式，返回帧数据
        # If rgb_array mode, return frame data
        if self.render_mode == "rgb_array":
            return self._render_frame()

    # ============================================================
    # _render_frame: 渲染单帧画面，更新 PyGame 窗口或返回数组
    #                Render a single frame, update PyGame window or return array
    # ============================================================
    def _render_frame(self):
        # 初始化PyGame窗口（如果尚未初始化）
        # Initialize PyGame window (if not initialized yet)
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )

        # 初始化时钟（如果尚未初始化）
        # Initialize clock (if not initialized yet)
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # 创建背景画布
        # Create background canvas
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill(self.COLOR_WHITE)

        # 计算每个格子的像素尺寸
        # Calculate pixel size of each cell
        pix_square_size = self.window_size / self.size

        # 绘制红色目标矩形
        # Draw red target rectangle
        pygame.draw.rect(
            canvas,
            self.COLOR_TARGET,
            pygame.Rect(
                pix_square_size * self._target_location,
                (pix_square_size, pix_square_size),
            ),
        )

        # 绘制蓝色智能体圆形
        # Draw blue agent circle
        pygame.draw.circle(
            canvas,
            self.COLOR_AGENT,
            (self._agent_location + self.CENTER_OFFSET) * pix_square_size,
            pix_square_size / self.AGENT_RADIUS_DIVISOR,
        )

        # 绘制垂直与水平网格线
        # Draw vertical and horizontal grid lines
        for x in range(self.size + 1):
            # 绘制水平线
            pygame.draw.line(
                canvas,
                self.COLOR_GRID,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=self.GRID_LINE_WIDTH,
            )
            # 绘制垂直线
            pygame.draw.line(
                canvas,
                self.COLOR_GRID,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=self.GRID_LINE_WIDTH,
            )

        # 判断并执行人类可见渲染
        # Determine and execute human-visible rendering
        if self.render_mode == "human":
            # 复制画布并更新显示
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # 控制渲染刷新率
            self.clock.tick(self.metadata["render_fps"])
        else:
            # 返回 NumPy RGB 数组
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    # ============================================================
    # close: 关闭环境，彻底释放图形资源
    #        Close environment, fully release graphics resources
    # ============================================================
    def close(self):
        # 退出 PyGame 显示与主引擎
        # Exit PyGame display and main engine
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
