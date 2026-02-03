"""
Lab 2: CliffWalking Gymnasium Environment
Author: Peng Wang
Student Number: 041107730

Custom Gymnasium environment implementing the Cliff Walking problem
from Sutton & Barto's Reinforcement Learning textbook (Page 132).

Grid Layout (4 rows × 12 columns):
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    S X X X X X X X X X X G

Where:
    S = Start (bottom-left, position [0, 3])
    G = Goal (bottom-right, position [11, 3])
    X = Cliff (grey squares in bottom row, columns 1-10)
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

# 导入类型提示和可选类型
# Import type hints and optional type
from typing import Optional

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
# CliffWalkingEnv: 悬崖行走Gymnasium环境
#                  CliffWalking Gymnasium Environment
# ============================================================
class CliffWalkingEnv(gym.Env):
    """悬崖行走Gymnasium环境
    CliffWalking Gymnasium Environment"""

    # ============================================================
    # 渲染常量
    # Rendering Constants
    # ============================================================

    # 渲染帧率（每秒刷新次数）
    # Render FPS (frames per second)
    RENDER_FPS = 10

    # PyGame窗口显示分辨率
    # PyGame window display resolution
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 300

    # 智能体圆形半径缩放因子
    # Agent circle radius scale factor
    AGENT_RADIUS_DIVISOR = 3

    # 坐标平移常量（用于居中绘制）
    # Coordinate translation constant (used for centered drawing)
    CENTER_OFFSET = 0.5

    # ============================================================
    # 颜色常量 (RGB 系统)
    # Color Constants (RGB System)
    # ============================================================

    # 统一色盘定义
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_CLIFF = (128, 128, 128)
    COLOR_GOAL = (0, 255, 0)
    COLOR_START = (255, 255, 0)
    COLOR_AGENT = (0, 0, 255)

    # ============================================================
    # 奖励机制常量
    # Reward Mechanism Constants
    # ============================================================

    # 掉入悬崖的重度惩罚
    # Heavy penalty for falling into cliff
    REWARD_CLIFF = -100

    # 正常移动的时间成本
    # Time cost for normal movement
    REWARD_STEP = -1

    # ============================================================
    # 动作属性
    # Action Attributes
    # ============================================================

    # 离散动作总数
    # Total discrete actions
    NUM_ACTIONS = 4

    # 内部元数据配置
    # Internal metadata configuration
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": RENDER_FPS}

    # ============================================================
    # __init__: 构造并初始化悬崖环境
    #           Construct and initialize cliff environment
    #
    # Parameters:
    #   render_mode: 渲染方式
    #   size: 逻辑网格分辩率 (Width, Height)
    # ============================================================
    def __init__(self, render_mode: Optional[str] = None, size: tuple = (12, 4)):
        # 应用逻辑尺寸
        # Apply logical dimensions
        self.xsize = size[0]
        self.ysize = size[1]

        # 应用物理窗口尺寸
        # Apply physical window size
        self.window_width = self.WINDOW_WIDTH
        self.window_height = self.WINDOW_HEIGHT

        # 预计算格子像素步长
        # Precompute cell pixel step
        self.pix_square_size_x = self.window_width // self.xsize
        self.pix_square_size_y = self.window_height // self.ysize

        # 构建 Gym 观察空间映射
        # Build Gym observation space mapping
        pos_low = np.array([0, 0])
        pos_high = np.array([self.xsize - 1, self.ysize - 1])
        self.observation_space = spaces.Dict({
            "agent": spaces.Box(low=pos_low, high=pos_high, shape=(2,), dtype=np.int64),
            "target": spaces.Box(low=pos_low, high=pos_high, shape=(2,), dtype=np.int64),
        })

        # 构建动作空间
        # Build action space
        self.action_space = spaces.Discrete(self.NUM_ACTIONS)

        # 映射数字序号到坐标偏移
        # Map indices to coordinate offsets
        self._action_to_direction = {
            0: np.array([-1, 0]),  # 左 / left
            1: np.array([1, 0]),   # 右 / right
            2: np.array([0, -1]),  # 上 / up
            3: np.array([0, 1]),   # 下 / down
        }

        # 固化起点与终点逻辑位置
        # Solidify start and goal logical positions
        self._start_location = np.array([0, self.ysize - 1])
        self._target_location = np.array([self.xsize - 1, self.ysize - 1])

        # 设置初始对象状态
        # Set initial object states
        self._agent_location = self._start_location.copy()

        # 定义危险区域集合
        # Define danger zone set
        self._cliff_columns = list(range(1, self.xsize - 1))
        self._cliff_row = self.ysize - 1

        # 同步渲染引擎标志
        # Sync render engine flag
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # 初始化显示后端句柄
        # Initialize display backend handles
        self.window = None
        self.clock = None

    # ============================================================
    # _get_obs: 检索当前的传感器观察数据
    #           Retrieve current sensor observation data
    #
    # Returns:
    #   dict: 包含 Agent 与 Target 坐标的快照
    # ============================================================
    def _get_obs(self) -> dict:
        # 获取位置镜像，防止外部篡改
        # Get position mirrors to prevent external tampering
        return {
            "agent": self._agent_location.copy(),
            "target": self._target_location.copy(),
        }

    # ============================================================
    # _get_info: 检索辅助调试信息 (非状态数据)
    #            Retrieve auxiliary debug info (Non-state data)
    #
    # Returns:
    #   dict: 包含核心指标（如曼哈顿距离）
    # ============================================================
    def _get_info(self) -> dict:
        # 计算 Agent 到目标的几何距离
        # Calculate geometric distance from Agent to target
        return {
            "distance": np.abs(self._agent_location - self._target_location).sum()
        }

    # ============================================================
    # reset: 系统级重置，回归到实验起始点
    #        System-level reset, return to experiment starting point
    #
    # Parameters:
    #   seed: 伪随机数种子
    #   options: 高级配置项
    #
    # Returns:
    #   tuple[dict, dict]: (观察, 辅助信息)
    # ============================================================
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> tuple:
        # 重置父类底层随机权重
        # Reset parent base random weights
        super().reset(seed=seed)

        # 强制回归起点
        # Force return to start
        self._agent_location = self._start_location.copy()

        # 捕获初态环境快照
        # Capture initial state environment snapshot
        observation = self._get_obs()
        info = self._get_info()

        # 视觉反馈同步
        # Visual feedback sync
        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    # ============================================================
    # step: 推进物理仿真时间步
    #       Step forward physical simulation time
    #
    # Parameters:
    #   action: 执行的离散动作索引
    #
    # Returns:
    #   tuple: (观察, 奖励, 终止标志, 截断标志, 信息)
    # ============================================================
    def step(self, action: int) -> tuple:
        # 计算位移矢量
        # Calculate displacement vector
        direction = self._action_to_direction[action]

        # 执行带有碰撞箱限制的位移
        # Execute displacement with collision box limits
        new_location = self._agent_location + direction
        self._agent_location = np.clip(
            new_location,
            [0, 0],
            [self.xsize - 1, self.ysize - 1]
        )

        # 执行危险判定逻辑
        # Execute danger detection logic
        fell_in_cliff = (
            self._agent_location[1] == self._cliff_row and
            self._agent_location[0] in self._cliff_columns
        )

        if fell_in_cliff:
            # 触发：坠落惩罚并强制复位
            # Trigger: Fall penalty and forced reset
            reward = self.REWARD_CLIFF
            self._agent_location = self._start_location.copy()
            terminated = False
        else:
            # 执行目标达成判定
            # Execute goal achievement detection
            reached_goal = np.array_equal(self._agent_location, self._target_location)
            reward = self.REWARD_STEP
            terminated = reached_goal

        # 构造回传数据包
        # Construct return data packet
        observation = self._get_obs()
        info = self._get_info()

        # 触发图形管线刷新
        # Trigger graphics pipeline refresh
        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    # ============================================================
    # render: 图形化展示当前状态
    #         Graphically display current state
    # ============================================================
    def render(self):
        # 处理 RGB 阵列请求
        # Handle RGB array requests
        if self.render_mode == "rgb_array":
            return self._render_frame()

    # ============================================================
    # _render_frame: 执行绘图引擎的基础渲染循环
    #                Execute drawing engine's base render loop
    # ============================================================
    def _render_frame(self):
        # 延迟激活 PyGame 显示终端
        # Deferred activation of PyGame display terminal
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # 延迟激活高精度计时器
        # Deferred activation of high-precision timer
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # 创建后台离屏画布
        # Create background off-screen canvas
        canvas = pygame.Surface((self.window_width, self.window_height))
        canvas.fill(self.COLOR_WHITE)

        # 1. 绘制静态悬崖背景
        for col in self._cliff_columns:
            pygame.draw.rect(
                canvas,
                self.COLOR_CLIFF,
                pygame.Rect(
                    col * self.pix_square_size_x,
                    self._cliff_row * self.pix_square_size_y,
                    self.pix_square_size_x,
                    self.pix_square_size_y,
                ),
            )

        # 2. 绘制终点标志位
        pygame.draw.rect(
            canvas,
            self.COLOR_GOAL,
            pygame.Rect(
                self._target_location[0] * self.pix_square_size_x,
                self._target_location[1] * self.pix_square_size_y,
                self.pix_square_size_x,
                self.pix_square_size_y,
            ),
        )

        # 3. 绘制起点基础色
        pygame.draw.rect(
            canvas,
            self.COLOR_START,
            pygame.Rect(
                self._start_location[0] * self.pix_square_size_x,
                self._start_location[1] * self.pix_square_size_y,
                self.pix_square_size_x,
                self.pix_square_size_y,
            ),
        )

        # 4. 绘制实时智能体圆形
        # 参数：坐标点由 (位置 + 偏移) * 像素尺寸 计算得出
        agent_pos_pix = (
            int((self._agent_location[0] + self.CENTER_OFFSET) * self.pix_square_size_x),
            int((self._agent_location[1] + self.CENTER_OFFSET) * self.pix_square_size_y),
        )
        pygame.draw.circle(
            canvas,
            self.COLOR_AGENT,
            agent_pos_pix,
            min(self.pix_square_size_x, self.pix_square_size_y) // self.AGENT_RADIUS_DIVISOR,
        )

        # 5. 生成遮罩网格线
        # 绘制 X 轴分隔符
        for x in range(self.xsize + 1):
            pygame.draw.line(
                canvas, self.COLOR_BLACK,
                (x * self.pix_square_size_x, 0),
                (x * self.pix_square_size_x, self.window_height),
                width=1
            )
        # 绘制 Y 轴分隔符
        for y in range(self.ysize + 1):
            pygame.draw.line(
                canvas, self.COLOR_BLACK,
                (0, y * self.pix_square_size_y),
                (self.window_width, y * self.pix_square_size_y),
                width=1
            )

        # 提交绘图到显示缓冲区
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            # 导出为数据流阵列
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)),
                axes=(1, 0, 2)
            )

    # ============================================================
    # close: 环境卸载，销毁所有窗口线程与缓冲区
    #        Environment unload, destroy all window threads and buffers
    # ============================================================
    def close(self):
        # 安全退出 PyGame 全局引擎
        # Safely exit PyGame global engine
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
