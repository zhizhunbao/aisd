"""
Lab 2: Cliff Walking Environment
Student ID: 041107730

Modified from Hybrid Activity 1 to implement the Cliff Walking problem
from Sutton & Barto's Reinforcement Learning textbook (Page 132)

Grid Layout (4 rows × 12 columns):
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    . . . . . . . . . . . .
    S X X X X X X X X X X G

Where:
    S = Start (bottom-left)
    G = Goal (bottom-right)
    X = Cliff (10 grey squares in the bottom row)
"""

# 导入抽象基类模块，用于定义环境接口
# Import abstract base class module for defining environment interface
import abc


class Env(abc.ABC):
    """环境抽象基类，定义强化学习环境的标准接口
    Environment abstract base class that defines the standard interface for RL environments"""

    @abc.abstractmethod
    def actions(self) -> int:
        """返回动作空间的大小
        Return the size of action space"""
        raise NotImplementedError()

    @abc.abstractmethod
    def states(self) -> int:
        """返回状态空间的大小
        Return the size of state space"""
        raise NotImplementedError()

    @abc.abstractmethod
    def step(self, action: int) -> tuple[int, int, bool]:
        """执行一个动作，返回下一状态、奖励和是否结束
        Execute an action and return next state, reward, and done flag"""
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self) -> tuple[int, int, bool]:
        """重置环境到初始状态
        Reset environment to initial state"""
        raise NotImplementedError()

    @abc.abstractmethod
    def render(self):
        """渲染环境的当前状态到控制台
        Render the current state of environment to console"""
        raise NotImplementedError()


class GridEnv(Env):
    """悬崖行走网格环境，实现Sutton & Barto书中的悬崖行走问题
    Cliff Walking grid environment that implements the Cliff Walking problem from Sutton & Barto's book"""

    def __init__(self, size: int):
        """初始化悬崖行走环境
        Initialize Cliff Walking environment"""

        # 初始化智能体起始位置（左下角）
        # Initialize agent start position (bottom-left)
        self.x = 0
        self.y = 3

        # 设置网格尺寸（4行 × 12列），原始版本是方形网格（size × size）
        # Set grid dimensions (4 rows × 12 columns), original was square grid (size × size)
        self.height = 4
        self.width = 12

        # 设置目标位置（右下角）
        # Set goal position (bottom-right)
        self.end_x = 11
        self.end_y = 3

        # 初始化状态标志
        # Initialize state flags
        self.done = False
        self.cliff = False

    def actions(self) -> int:
        """返回动作空间大小
        Return action space size"""

        # 返回4个动作：左(0)、右(1)、上(2)、下(3)
        # Return 4 actions: left(0), right(1), up(2), down(3)
        return 4

    def states(self) -> int:
        """返回状态空间大小
        Return state space size"""

        # 返回4×12网格的总状态数 = 48
        # Return total states for 4×12 grid = 48
        return self.height * self.width

    def step(self, action: int) -> tuple[int, int, bool]:
        """执行一个动作并返回结果
        Execute an action and return the result"""

        # 根据动作移动智能体，边界检查防止越界
        # Move agent based on action, boundary check to prevent out of bounds
        if action == 0:
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:
            self.x = self.x + 1 if self.x < self.width - 1 else self.x
        if action == 2:
            self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3:
            self.y = self.y + 1 if self.y < self.height - 1 else self.y

        # 检查是否掉下悬崖（底行，第1-10列）
        # Check if agent fell off cliff (bottom row, columns 1-10)
        if self.y == 3 and 1 <= self.x <= 10: # magic number
            # 掉下悬崖：设置标志、给予大负奖励、返回起点
            # Fell off cliff: set flag, give large negative reward, return to start
            self.cliff = True
            reward = -100
            self.x = 0
            self.y = 3
            done = False
        else:
            # 正常移动：每步奖励为-1，鼓励寻找最短路径
            # Normal move: reward -1 per step, encourages shortest path
            self.cliff = False
            reward = -1

            # 检查是否到达目标
            # Check if reached goal
            done = self.x == self.end_x and self.y == self.end_y

        # 计算下一状态索引：状态编号 = 行号 * 列数 + 列号
        # Calculate next state index: state number = row * width + col
        next_state = self.y * self.width + self.x

        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        """重置环境到初始状态
        Reset environment to initial state"""

        # 重置到起始位置（左下角）
        # Reset to start position (bottom-left)
        self.x = 0
        self.y = 3

        # 清除所有状态标志
        # Clear all state flags
        self.done = False
        self.cliff = False

        return self.y * self.width + self.x, 0, False

    def render(self):
        """渲染网格世界到控制台
        Render the grid world to console"""

        # 遍历每一行每一列，根据位置打印相应符号
        # Iterate through each row and column, print appropriate symbol based on position
        for i in range(self.height):
            for j in range(self.width):
                if self.y == i and self.x == j:
                    print("O", end='')
                elif i == self.end_y and j == self.end_x:
                    print("G", end='')
                elif i == 3 and 1 <= j <= 10:
                    print("X", end='')
                elif i == 3 and j == 0:
                    print("S", end='')
                else:
                    print(".", end='')
            print("")
