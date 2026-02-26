# Week 2: MDP — 代码参考

> **See also:** [_cheatsheet.md](week2_mdp_cheatsheet.md) | [_math.md](week2_mdp_math.md)
> **Source:** Lab 2 (Gymnasium) + Slides CST8509_02

---

## ★ SARSA 算法 (SARSA Algorithm)

### SARSA 伪代码实现

```python
# SARSA: On-policy TD control
# SARSA：同策略时序差分控制
# 名字来源：(S, A, R, S', A') — 更新需要的五元组
# Name origin: (S, A, R, S', A') — the quintuple needed for update

import random
import numpy as np

# 超参数 / Hyperparameters
episodes = 500       # 训练回合数 / Training episodes
gamma = 0.9          # 折扣因子 / Discount factor
epsilon = 0.1        # 探索率 / Exploration rate
alpha = 0.1          # 学习率 / Learning rate (step size)
decay = 0.01         # 探索率衰减 / Epsilon decay

# Q 表初始化 / Q-table initialization
# 终止状态的 Q 值必须为 0
# Terminal state Q-values must be 0
qtable = np.zeros((num_states, num_actions))

for episode in range(episodes):
    state, _, done = env.reset()

    # SARSA 特有：在循环前先选动作 A
    # SARSA-specific: choose initial action A before loop
    if random.random() < epsilon:
        action = random.choice(range(num_actions))
    else:
        action = np.argmax(qtable[state])

    while not done:
        # 执行动作 A，观察 R, S'
        # Take action A, observe R, S'
        next_state, reward, done = env.step(action)

        # SARSA 特有：从 S' 选择 A'（用同一个 ε-greedy 策略）
        # SARSA-specific: choose A' from S' using SAME ε-greedy policy
        if random.random() < epsilon:
            next_action = random.choice(range(num_actions))
        else:
            next_action = np.argmax(qtable[next_state])

        # SARSA 更新：用 Q(S', A') 而不是 max Q(S', a')
        # SARSA update: use Q(S', A') NOT max Q(S', a')
        td_target = reward + gamma * qtable[next_state][next_action]
        td_error = td_target - qtable[state][action]
        qtable[state][action] += alpha * td_error

        # S ← S'; A ← A'
        state = next_state
        action = next_action  # SARSA 特有：下一步用 A' 作为当前动作

    epsilon -= decay * epsilon
```

---

## Q-Learning vs SARSA 更新对比

### 关键区别一行代码

```python
# ========== Q-Learning 更新 (Off-policy) ==========
# 用 max Q(S', a') — 不管实际选了什么动作
# Use max Q(S', a') — regardless of actual next action
td_target = reward + gamma * np.max(qtable[next_state])
qtable[state][action] += alpha * (td_target - qtable[state][action])

# ========== SARSA 更新 (On-policy) ==========
# 用 Q(S', A') — 实际选择的下一动作
# Use Q(S', A') — the actually chosen next action
td_target = reward + gamma * qtable[next_state][next_action]
qtable[state][action] += alpha * (td_target - qtable[state][action])
```

---

## Gymnasium 环境 (Gymnasium Environment)

### 基本 Gymnasium 环境交互

```python
import gymnasium
import cliffwalking_env  # 注册自定义环境 / Register custom env

# 创建环境 / Create environment
env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")

# 重置环境，获取初始观测 / Reset, get initial observation
observation, info = env.reset()

# 交互循环 / Interaction loop
for _ in range(1000):
    action = env.action_space.sample()  # 随机动作 / Random action
    # Gymnasium 返回 5 个值（比 Lab 1 多 truncated 和 info）
    # Gymnasium returns 5 values (more than Lab 1's 3)
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

### Gymnasium vs Lab 1 自定义环境接口对比

```python
# ========== Lab 1 自定义环境 (3 返回值) ==========
next_state, reward, done = env.step(action)
state, reward, done = env.reset()

# ========== Gymnasium 标准接口 (5 返回值) ==========
observation, reward, terminated, truncated, info = env.step(action)
observation, info = env.reset()
# terminated: 自然结束（到达目标）/ Natural end (reached goal)
# truncated:  强制截断（超时等）/ Forced end (timeout, etc.)
# info: 额外调试信息 / Extra debug info (dict)
```

### 从 Gymnasium 观测中提取状态

```python
# Gymnasium 观测是字典型 / Gymnasium observation is a dict
# observation = {'agent': array([x, y]), 'target': array([tx, ty])}

# 提取 agent 位置 / Extract agent position
agent_pos = observation['agent']  # e.g., array([3, 2])

# 2D 坐标 → 1D 状态索引 / 2D coords → 1D state index
x_size = env.observation_space['agent'].high[0] + 1  # e.g., 12
state = agent_pos[1] * x_size + agent_pos[0]         # row * width + col

# 获取状态和动作空间大小 / Get state and action space sizes
num_states = (env.observation_space['agent'].high[0] + 1) * \
             (env.observation_space['agent'].high[1] + 1)
num_actions = env.action_space.n
```

---

## Stable-Baselines3 (SB3) 算法

### DQN Agent

```python
import gymnasium
import cliffwalking_env
from stable_baselines3 import DQN

# 创建环境 / Create environment
env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")

# 训练 DQN / Train DQN
model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000, log_interval=4)

# 保存与加载 / Save and load
model.save("dqn_cliff")
model = DQN.load("dqn_cliff")

# 评估 / Evaluate
obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
```

### PPO Agent

```python
from stable_baselines3 import PPO

# PPO 用法与 DQN 相同，只需替换类名
# PPO usage identical to DQN, just change class name
model = PPO("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_cliff")
```

---

## ε-Greedy 策略 (ε-Greedy Policy)

### 标准 ε-Greedy（两种写法）

```python
# ========== 写法 1：Lab 1 风格（list） ==========
if random.random() < epsilon:
    action = random.choice(range(env.actions()))          # 探索 / Explore
else:
    action = qtable[state].index(max(qtable[state]))      # 利用 / Exploit

# ========== 写法 2：NumPy 风格（ndarray） ==========
if np.random.uniform() < epsilon:
    action = env.action_space.sample()                    # 探索 / Explore
else:
    action = np.argmax(qtable[state])                     # 利用 / Exploit
```

---

## 可视化 (Visualization)

### 绘制训练曲线

```python
import matplotlib.pyplot as plt

# 记录每个 episode 的数据 / Record per-episode data
episode_rewards = []   # 每回合总奖励 / Total reward per episode
episode_steps = []     # 每回合步数 / Steps per episode

# ... 训练循环中添加 ...
# episode_rewards.append(total_reward)
# episode_steps.append(steps)

# 绘制回报曲线 / Plot return curve
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(episode_rewards)
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward')
ax1.set_title('Episode Returns')

ax2.plot(episode_steps)
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.set_title('Steps per Episode')

plt.tight_layout()
plt.savefig('training_curves.png')
plt.show()
```

---

## Key API Cheat Sheet

| 操作 (Operation) | 代码 (Code) | 说明 (Note) |
|-----------------|-------------|-------------|
| Q-Learning 更新 | `Q[s][a] += α * (r + γ * max(Q[s']) - Q[s][a])` | Off-policy |
| SARSA 更新 | `Q[s][a] += α * (r + γ * Q[s'][a'] - Q[s][a])` | On-policy |
| Gym 创建环境 | `gymnasium.make("env_id", render_mode="human")` | 标准接口 |
| Gym 重置 | `obs, info = env.reset()` | 返回 2 值 |
| Gym 执行动作 | `obs, r, term, trunc, info = env.step(a)` | 返回 5 值 |
| Gym 动作空间 | `env.action_space.n` | 离散动作数 |
| Gym 随机动作 | `env.action_space.sample()` | 探索用 |
| SB3 训练 | `model.learn(total_timesteps=N)` | DQN/PPO 通用 |
| SB3 预测 | `action, _ = model.predict(obs, deterministic=True)` | 评估用 |
| SB3 保存加载 | `model.save("name")` / `DQN.load("name")` | 持久化 |
| NumPy argmax | `np.argmax(qtable[state])` | 贪婪选择 |
| 2D→1D 状态 | `state = row * width + col` | 网格编码 |
