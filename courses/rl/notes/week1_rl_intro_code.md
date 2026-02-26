# Week 1: RL 入门 — 代码参考

> **See also:** [_cheatsheet.md](week1_rl_intro_cheatsheet.md) | [_math.md](week1_rl_intro_math.md)
> **Source:** Lab 1 (Cliff Walking) + Medium Q-Learning 文章

---

## ★ 代码基础 (Code Foundations)

### Python 基础模式

- **抽象基类 (Abstract Base Class):**

```python
import abc

class Env(abc.ABC):
    @abc.abstractmethod
    def actions(self) -> int:
        # 返回动作空间大小
        # Return action space size
        raise NotImplementedError()

    @abc.abstractmethod
    def step(self, action: int) -> tuple[int, int, bool]:
        # 执行动作，返回 (next_state, reward, done)
        # Execute action, return (next_state, reward, done)
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self) -> tuple[int, int, bool]:
        # 重置环境到初始状态
        # Reset environment to initial state
        raise NotImplementedError()
```

- **随机数与列表操作:**

```python
import random

# 随机选择动作（探索）
# Randomly choose action (exploration)
action = random.choice(range(num_actions))

# 选择最大值的索引（利用）
# Select index of max value (exploitation)
action = qtable[state].index(max(qtable[state]))
```

---

## 环境实现 (Environment Implementation)

### Grid World 环境模式

- **基本网格环境 (10x10 Grid):**

```python
class GridEnv(Env):
    def __init__(self, size: int):
        self.x = 0          # Agent x position / 智能体 x 坐标
        self.y = 0          # Agent y position / 智能体 y 坐标
        self.size = size     # Grid size / 网格大小
        self.end_x = size - 1  # Goal x / 目标 x
        self.end_y = size - 1  # Goal y / 目标 y

    def states(self) -> int:
        return self.size ** 2  # Total states = size² / 总状态数

    def step(self, action: int) -> tuple[int, int, bool]:
        # 4 actions: left(0), right(1), up(2), down(3)
        # 4 个动作：左(0)、右(1)、上(2)、下(3)
        if action == 0:
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:
            self.x = self.x + 1 if self.x < self.size - 1 else self.x
        # ... up/down similar

        done = self.x == self.end_x and self.y == self.end_y
        next_state = self.size * self.y + self.x  # 2D → 1D index
        reward = 1 if done else 0
        return next_state, reward, done
```

- **状态编码：2D 坐标 → 1D 索引:**

```python
# 2D (row, col) → 1D state index
# 二维坐标 → 一维状态索引
state = row * num_cols + col

# Example: 4x12 grid, position (3, 5)
# 示例：4x12 网格，位置 (3, 5)
state = 3 * 12 + 5  # = 41
```

### Cliff Walking 环境 (Lab 1)

- **Cliff Walking 网格布局:**

```python
# 4x12 grid layout / 4x12 网格布局:
# . . . . . . . . . . . .
# . . . . . . . . . . . .
# . . . . . . . . . . . .
# S X X X X X X X X X X G
#
# S = Start (0, 3) / 起点
# G = Goal (11, 3) / 终点
# X = Cliff (columns 1-10, row 3) / 悬崖
```

- **悬崖检测与奖励:**

```python
def step(self, action: int) -> tuple[int, int, bool]:
    # ... move agent based on action ...

    # 检查是否掉入悬崖（底行，第1-10列）
    # Check if fell off cliff (bottom row, columns 1-10)
    if self.y == 3 and 1 <= self.x <= 10:
        self.cliff = True
        reward = -100        # 掉入悬崖惩罚 / Cliff penalty
        self.x = 0           # 返回起点 / Return to start
        self.y = 3
        done = False
    else:
        self.cliff = False
        reward = -1           # 每步 -1 鼓励最短路径 / -1 per step encourages shortest path
        done = self.x == self.end_x and self.y == self.end_y

    next_state = self.y * self.width + self.x
    return next_state, reward, done
```

---

## Q-Learning 算法 (Q-Learning Algorithm)

### Q-Table 初始化

- **随机初始化 Q 表:**

```python
# Q-table: states × actions, random init
# Q 表：状态数 × 动作数，随机初始化
qtable = [
    [random.random() for _ in range(num_actions)]
    for _ in range(num_states)
]
```

### 超参数 (Hyperparameters)

- **典型超参数设置:**

```python
episodes = 50     # 训练回合数 / Number of training episodes
gamma = 0.9       # 折扣因子 / Discount factor (0=myopic, 1=farsighted)
epsilon = 0.1     # 初始探索率 / Initial exploration rate
decay = 0.5       # 探索率衰减 / Exploration decay
alpha = 1.0       # 学习率 / Learning rate (1=full replacement)
```

### ε-Greedy 策略 (ε-Greedy Policy)

- **ε-Greedy 动作选择:**

```python
# ε-greedy: balance exploration vs exploitation
# ε-贪婪：平衡探索与利用
if random.random() < epsilon:
    # 探索：随机选择动作
    # Exploration: random action
    action = random.choice(range(env.actions()))
else:
    # 利用：选择 Q 值最大的动作
    # Exploitation: greedy action (max Q)
    action = qtable[state].index(max(qtable[state]))
```

### Bellman 方程更新 (Bellman Update)

- **Q 值更新（alpha=1 简化版）:**

```python
# Bellman equation: Q(s,a) = r + γ * max Q(s',a')
# 贝尔曼方程：Q(s,a) = r + γ * max Q(s',a')
qtable[state][action] = reward + gamma * max(qtable[next_state])
```

- **Q 值更新（完整版，含学习率 alpha）:**

```python
# Full update: Q(s,a) = (1-α)Q(s,a) + α[r + γ * max Q(s',a')]
# 完整更新：Q(s,a) = (1-α)Q(s,a) + α[r + γ * max Q(s',a')]
old_value = qtable[state][action]
td_target = reward + gamma * max(qtable[next_state])
qtable[state][action] = (1 - alpha) * old_value + alpha * td_target
# When alpha=1: simplifies to direct assignment
# 当 alpha=1 时：简化为直接赋值
```

### 完整训练循环 (Full Training Loop)

- **Q-Learning 训练主循环:**

```python
for episode in range(episodes):
    state, _, done = env.reset()
    steps = 0
    total_reward = 0

    while not done:
        steps += 1

        # ε-greedy action selection
        if random.random() < epsilon:
            action = random.choice(range(env.actions()))
        else:
            action = qtable[state].index(max(qtable[state]))

        # Take action, observe result
        next_state, reward, done = env.step(action)
        total_reward += reward

        # Bellman update
        qtable[state][action] = reward + gamma * max(qtable[next_state])

        state = next_state

        if steps > 1000:  # Safety break / 安全中断
            break

    # Decay exploration rate / 衰减探索率
    epsilon -= decay * epsilon

    print(f"Episode {episode+1}: {steps} steps, reward={total_reward}")
```

### 探索率衰减 (Epsilon Decay)

- **线性衰减模式:**

```python
# 每回合衰减：epsilon = epsilon * (1 - decay)
# Per-episode decay: epsilon = epsilon * (1 - decay)
epsilon -= decay * epsilon
# With decay=0.5: 0.1 → 0.05 → 0.025 → ...
```

---

## Key API Cheat Sheet

| 操作 (Operation) | 代码 (Code) | 说明 (Note) |
|-----------------|-------------|-------------|
| 初始化 Q 表 | `[[random.random() for _ in range(actions)] for _ in range(states)]` | 随机初始化 |
| 随机动作 | `random.choice(range(num_actions))` | 探索 |
| 贪婪动作 | `qtable[s].index(max(qtable[s]))` | 利用 |
| Bellman 更新 | `qtable[s][a] = r + gamma * max(qtable[s'])` | alpha=1 |
| 完整更新 | `(1-alpha)*Q_old + alpha*(r + gamma*max(Q_next))` | 含学习率 |
| 环境重置 | `state, reward, done = env.reset()` | 每回合开始 |
| 执行动作 | `next_state, reward, done = env.step(action)` | 每步 |
| 衰减 epsilon | `epsilon -= decay * epsilon` | 每回合结束 |
| 2D→1D 状态 | `state = row * width + col` | 网格编码 |
