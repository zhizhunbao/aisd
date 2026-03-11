# Lab 1 代码速查：手写 Q-Learning CliffWalking

> **Source:** `courses/rl/code/lab1/`
> **故事线：** [lab1_cliffwalking_storyline.md](lab1_cliffwalking_storyline.md)
> **关联 slides：** [Week 2 MDP](week2_mdp_slides.md) | [Week 6 复习](week6_midterm_review_slides.md)

---

## 1. 环境类（`cliff_env.py`）

### 1.1 完整接口定义

```python
import abc

class Env(abc.ABC):
    @abc.abstractmethod
    def actions(self) -> int: ...     # 动作空间大小

    @abc.abstractmethod
    def states(self) -> int: ...      # 状态空间大小

    @abc.abstractmethod
    def step(self, action: int) -> tuple[int, int, bool]: ...
    # 返回：(next_state, reward, done) ← 3个值（与 Gymnasium 不同！）

    @abc.abstractmethod
    def reset(self) -> tuple[int, int, bool]: ...
    # 返回：(initial_state, reward=0, done=False)

    @abc.abstractmethod
    def render(self): ...             # 打印当前网格到终端
```

> ⚠️ **Lab 1 vs Lab 2 关键差异：**
> Lab 1 `step()` → `(next_state, reward, done)` — **3 个值**
> Lab 2 Gymnasium `step()` → `(obs, reward, terminated, truncated, info)` — **5 个值**

### 1.2 GridEnv（CliffWalking 实现）

```python
class GridEnv(Env):
    def __init__(self, size: int):
        self.x, self.y = 0, 3          # 起点：左下角
        self.height, self.width = 4, 12 # 4行 × 12列网格
        self.end_x, self.end_y = 11, 3  # 目标：右下角
        self.done = False
        self.cliff = False

    def actions(self) -> int:
        return 4   # 左(0) 右(1) 上(2) 下(3)

    def states(self) -> int:
        return self.height * self.width  # 4 × 12 = 48

    def step(self, action: int) -> tuple[int, int, bool]:
        # 移动（带边界检查）
        if action == 0: self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1: self.x = self.x + 1 if self.x < self.width - 1 else self.x
        if action == 2: self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3: self.y = self.y + 1 if self.y < self.height - 1 else self.y

        # 悬崖检测：底行第 1-10 列
        if self.y == 3 and 1 <= self.x <= 10:
            self.cliff = True
            reward = -100
            self.x, self.y = 0, 3      # 返回起点，episode 不结束！
            done = False
        else:
            self.cliff = False
            reward = -1                 # 普通步：每步 -1
            done = (self.x == self.end_x and self.y == self.end_y)

        next_state = self.y * self.width + self.x  # 坐标→整数索引
        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        self.x, self.y = 0, 3
        self.done = self.cliff = False
        return self.y * self.width + self.x, 0, False
```

---

## 2. 状态索引转换

```python
# 坐标 (x, y) → 整数 state
state = y * width + x        # = y * 12 + x

# 整数 state → 坐标
x = state % width            # = state % 12
y = state // width           # = state // 12
```

| 关键位置 | (x, y) | state |
|---------|--------|-------|
| 起点 S | (0, 3) | 36 |
| 目标 G | (11, 3) | 47 |
| 悬崖首格 | (1, 3) | 37 |
| 悬崖末格 | (10, 3) | 46 |
| 左上角 | (0, 0) | 0 |

---

## 3. Q-Learning Agent（`qlearning_agent.py`）

### 3.1 Q-table 初始化

```python
import random

# 随机初始化：打破对称性，鼓励早期探索
qtable = [
    [random.random() for _ in range(env.actions())]  # 4 个动作
    for _ in range(env.states())                      # 48 个状态
]
# qtable[state][action] → 该 (s, a) 的估计价值
```

### 3.2 ε-greedy 动作选择

```python
if random.random() < epsilon:
    action = random.choice(range(env.actions()))  # 探索：随机
else:
    action = qtable[state].index(max(qtable[state]))  # 利用：贪心
```

### 3.3 Bellman 方程更新

```python
# alpha=1 时的简化版（Lab 1 实际使用）：
qtable[state][action] = reward + gamma * max(qtable[next_state])

# 完整版（含 alpha）：
qtable[state][action] = qtable[state][action] + alpha * (
    reward + gamma * max(qtable[next_state]) - qtable[state][action]
)
```

### 3.4 完整训练循环

```python
def train(env, episodes=50, gamma=0.9, epsilon=0.1, decay=0.5, alpha=1.0):
    qtable = [[random.random() for _ in range(env.actions())]
              for _ in range(env.states())]

    for episode in range(episodes):
        state, _, done = env.reset()   # ← 3 个返回值
        steps = 0
        episode_reward = 0

        while not done:
            # ε-greedy
            if random.random() < epsilon:
                action = random.choice(range(env.actions()))
            else:
                action = qtable[state].index(max(qtable[state]))

            next_state, reward, done = env.step(action)  # ← 3 个返回值
            episode_reward += reward

            # Q-table 更新
            qtable[state][action] = reward + gamma * max(qtable[next_state])
            state = next_state

            steps += 1
            if steps > 1000: break   # 防止无限循环

        # ε 衰减
        epsilon -= decay * epsilon   # epsilon = epsilon * (1 - decay)

    return qtable
```

### 3.5 超参数说明

```python
EPISODES = 50     # 训练回合数
GAMMA    = 0.9    # 折扣因子：0.9 → 重视未来但不过度
EPSILON  = 0.1    # 初始探索率：10% 随机，90% 贪心
DECAY    = 0.5    # ε 每 episode 减半：0.1 → 0.05 → 0.025 → ...
ALPHA    = 1.0    # 学习率（演示讨论用，代码里直接赋值）
```

---

## 4. 网格渲染（`render()` 输出格式）

```
. . . . . . . . . . . .
. . . . . . . . . . . .
. . . . . . . . . . . .
A X X X X X X X X X X G
```

| 字符 | 含义 |
|------|------|
| `.` | 空格 |
| `A` | Agent 当前位置 |
| `X` | 悬崖 |
| `G` | 目标 |
| `S` | 起点（Agent 不在时显示）|

---

## 5. CliffWalking 关键数字速查

| 参数 | 值 |
|------|-----|
| 网格大小 | 4 行 × 12 列 |
| 总状态数 | **48** |
| 总动作数 | **4**（左/右/上/下）|
| 悬崖位置 | y=3, x=1~10（共 10 格）|
| 掉崖奖励 | **-100**，返回起点，不结束 |
| 普通步奖励 | **-1** |
| 起点 state 索引 | **36** |
| 目标 state 索引 | **47** |

---

## 6. 常见错误速查

| 错误 | 原因 | 修复 |
|------|------|------|
| `too many values to unpack` | 用 Lab 2 的 5 值解包接收 Lab 1 的 `step()` | Lab 1 只返回 3 个值：`state, reward, done = env.step(action)` |
| agent 卡在悬崖边不动 | Q-table 初始化为 0，没有探索动力 | 改为随机初始化，或提高初始 ε |
| episode 无法结束 | 忘记 `if steps > 1000: break` 安全机制 | 添加步数上限检查 |
| 悬崖检测错误 | 忘记检查 `y==3` 条件，只检查 `x` | 必须同时满足 `y==3 and 1<=x<=10` |
