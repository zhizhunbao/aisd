# Midterm Review: RL 期中复习 — 代码参考

> **See also:** [_cheatsheet.md](week6_midterm_review_cheatsheet.md) | [_math.md](week6_midterm_review_math.md)
> **Source:** Labs 1-2 + Assignment 1 + Slides Week 3-5
> **Coverage:** Gymnasium API + Q-Learning 实现 + SB3 用法

---

## ★ Q-Learning 更新公式 (Midterm 必考 — Slide 6)

```python
# Q-Learning update rule — Q-Learning 更新规则
# 每一步的核心更新 | Core update for each step
qtable[state][action] = (
    qtable[state][action]
    + alpha * (
        reward
        + gamma * max(qtable[next_state])
        - qtable[state][action]
    )
)
```

| Variable | Type | Meaning |
|----------|------|---------|
| `qtable` | `dict` or `np.array` | Q 表: 动作价值函数 |
| `state` | `int` | 当前状态 |
| `action` | `int` | 当前动作 |
| `alpha` | `float` | 学习率 (step size), e.g. 0.1 |
| `reward` | `float` | 即时奖励 |
| `gamma` | `float` | 折扣因子, e.g. 0.99 |
| `next_state` | `int` | 下一状态 |

---

## Q-Learning 完整训练循环

```python
import numpy as np
import gymnasium as gym

# ── 超参数 | Hyperparameters ──
alpha = 0.1          # 学习率 | Learning rate
gamma = 0.99         # 折扣因子 | Discount factor
epsilon = 1.0        # 探索率 | Exploration rate
epsilon_decay = 0.995
epsilon_min = 0.05
num_episodes = 1000

# ── 创建环境 | Create environment ──
env = gym.make("CliffWalking-v0")
n_states = env.observation_space.n
n_actions = env.action_space.n

# ── 初始化 Q 表 | Initialize Q-table ──
qtable = np.zeros((n_states, n_actions))

# ── 训练循环 | Training loop ──
for episode in range(num_episodes):
    state, info = env.reset()
    terminated = False
    truncated = False

    while not (terminated or truncated):
        # ε-greedy 动作选择 | ε-greedy action selection
        if np.random.random() < epsilon:
            action = env.action_space.sample()  # 探索 | Explore
        else:
            action = np.argmax(qtable[state])    # 利用 | Exploit

        # 执行动作 | Take action
        next_state, reward, terminated, truncated, info = env.step(action)

        # Q-Learning 更新 | Q-Learning update
        qtable[state][action] = qtable[state][action] + alpha * (
            reward + gamma * np.max(qtable[next_state]) - qtable[state][action]
        )

        state = next_state

    # ε 衰减 | Decay epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

env.close()
```

---

## Gymnasium 核心 API

### 创建和使用环境

```python
import gymnasium as gym

# ── 创建环境 | Create environment ──
env = gym.make("CliffWalking-v0")
# 带渲染 | With rendering:
env = gym.make("CliffWalking-v0", render_mode="human")

# ── 重置环境 | Reset ──
state, info = env.reset()
# state: 初始状态 | Initial state
# info: 额外信息字典 | Extra info dict

# ── 执行动作 | Step ──
next_state, reward, terminated, truncated, info = env.step(action)
# terminated: 到达终止状态 | Reached terminal state
# truncated:  到达最大步数限制 | Reached max steps

# ── 查看空间 | Inspect spaces ──
env.observation_space    # 观测空间 | e.g. Discrete(48)
env.action_space         # 动作空间 | e.g. Discrete(4)
env.action_space.n       # 动作数量 | Number of actions
env.observation_space.n  # 状态数量 | Number of states

# ── 随机动作 | Random action ──
action = env.action_space.sample()

# ── 关闭环境 | Close ──
env.close()
```

### step() 返回值详解

| Return Value | Type | Description |
|---|---|---|
| `next_state` | `int` or `np.array` | 新状态 |
| `reward` | `float` | 即时奖励 |
| `terminated` | `bool` | 是否到达终止状态 (goal/fail) |
| `truncated` | `bool` | 是否被截断 (max steps) |
| `info` | `dict` | 额外调试信息 |

---

## 自定义 Gymnasium 环境

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MyCustomEnv(gym.Env):
    """自定义 RL 环境模板 | Custom RL environment template"""

    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode=None):
        super().__init__()
        # ── 定义动作空间 | Define action space ──
        self.action_space = spaces.Discrete(4)  # 4 个离散动作

        # ── 定义观测空间 | Define observation space ──
        self.observation_space = spaces.Discrete(16)  # 16 个状态

        self.render_mode = render_mode
        self.state = None

    def reset(self, seed=None, options=None):
        """重置环境到初始状态 | Reset to initial state"""
        super().reset(seed=seed)
        self.state = 0  # 起始状态
        info = {}
        return self.state, info

    def step(self, action):
        """执行一步 | Execute one step"""
        # 1. 根据 action 计算新状态 | Compute new state
        # 2. 计算奖励 | Compute reward
        # 3. 判断是否终止 | Check termination
        next_state = self.state  # 替换为实际逻辑
        reward = -1.0
        terminated = False
        truncated = False
        info = {}

        self.state = next_state
        return next_state, reward, terminated, truncated, info

    def render(self):
        """渲染环境 (可选) | Render (optional)"""
        pass
```

### 注册自定义环境

```python
from gymnasium.envs.registration import register

register(
    id="MyCustomEnv-v0",
    entry_point="my_module:MyCustomEnv",
    max_episode_steps=200,
)
```

---

## Gymnasium Wrapper

```python
import gymnasium as gym
from gymnasium import Wrapper

# ── 使用内置 Wrapper ──
env = gym.make("CartPole-v1")
from gymnasium.wrappers import TimeLimit
env = TimeLimit(env, max_episode_steps=500)

# ── 自定义 Wrapper ──
class MyWrapper(Wrapper):
    """自定义 wrapper: 修改奖励 | Custom wrapper: modify reward"""

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        # 修改奖励 | Modify reward
        modified_reward = reward * 2.0
        return obs, modified_reward, terminated, truncated, info

env = gym.make("CartPole-v1")
env = MyWrapper(env)
```

---

## Stable-Baselines3 基本用法

### DQN 训练流程

```python
from stable_baselines3 import DQN
import gymnasium as gym

# ── 创建环境 ──
env = gym.make("CartPole-v1")

# ── 创建模型 ──
model = DQN(
    "MlpPolicy",           # 多层感知机策略网络
    env,
    learning_rate=1e-3,     # 学习率
    buffer_size=50000,      # 经验回放缓冲区大小
    learning_starts=1000,   # 开始学习前的随机步数
    verbose=1               # 打印训练信息
)

# ── 训练 ──
model.learn(total_timesteps=100000)

# ── 保存 & 加载 ──
model.save("dqn_cartpole")
model = DQN.load("dqn_cartpole")

# ── 测试 ──
obs, info = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

### PPO 训练流程

```python
from stable_baselines3 import PPO

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
```

### 常用 SB3 Callbacks

```python
from stable_baselines3.common.callbacks import EvalCallback

# 每隔一段时间评估并保存最佳模型
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./logs/",
    log_path="./logs/",
    eval_freq=5000,
    deterministic=True,
    render=False
)

model.learn(total_timesteps=100000, callback=eval_callback)
```

---

## 常用 Imports 速查

```python
# ── Gymnasium ──
import gymnasium as gym
from gymnasium import spaces
from gymnasium import Wrapper

# ── Numpy ──
import numpy as np

# ── Stable-Baselines3 ──
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env

# ── Matplotlib (用于绘图) ──
import matplotlib.pyplot as plt

# ── 环境检查 (验证自定义环境) ──
from stable_baselines3.common.env_checker import check_env
env = MyCustomEnv()
check_env(env)  # 会报告问题
```

---

## 代码模式速查 (Code Patterns Quick Reference)

| 模式 | 代码片段 | 用途 |
|------|---------|------|
| 创建环境 | `env = gym.make("EnvName-v0")` | 标准环境 |
| 重置 | `state, info = env.reset()` | 每个 episode 开始 |
| 执行步 | `s, r, term, trunc, info = env.step(a)` | 单步交互 |
| 随机动作 | `action = env.action_space.sample()` | 探索 |
| 贪婪动作 | `action = np.argmax(qtable[state])` | 利用 |
| ε-greedy | `if random() < ε: sample else argmax` | 探索-利用平衡 |
| Q 更新 | `Q[s,a] += α*(r+γ*max(Q[s'])-Q[s,a])` | Q-Learning 核心 |
| SB3 训练 | `model.learn(total_timesteps=N)` | 训练 |
| SB3 预测 | `action, _ = model.predict(obs)` | 推理 |
| SB3 保存 | `model.save("name")` | 持久化 |
| SB3 加载 | `model = DQN.load("name")` | 恢复 |
