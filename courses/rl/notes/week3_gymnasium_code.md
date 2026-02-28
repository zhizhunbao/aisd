# Week 3: Gymnasium — 代码参考 (Code Reference)

> See also: [概念速查](week3_gymnasium_cheatsheet.md) | [数学公式](week3_gymnasium_math.md)

---

## 🔧 环境基本用法

### 创建和运行环境

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
obs, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()  # 随机动作
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```

### 检查空间信息

```python
print(env.observation_space)       # Box(-4.8, 4.8, (4,), float32)
print(env.action_space)            # Discrete(2)
print(env.observation_space.shape) # (4,)
print(env.action_space.n)          # 2
```

---

## 🔧 自定义环境模板

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MyGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=4):
        super().__init__()
        self.size = size
        self.observation_space = spaces.Discrete(size * size)
        self.action_space = spaces.Discrete(4)  # 右上左下
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # 设置 self.np_random
        self._agent_pos = 0
        self._target_pos = self.size * self.size - 1
        observation = self._agent_pos
        info = {}
        return observation, info

    def step(self, action):
        # 执行动作，更新状态
        # ... (状态转移逻辑)
        terminated = (self._agent_pos == self._target_pos)
        truncated = False
        reward = 1.0 if terminated else -0.01
        observation = self._agent_pos
        info = {}
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            pass  # PyGame 渲染逻辑

    def close(self):
        pass  # 释放资源
```

---

## 🔧 Spaces API

### Discrete

```python
from gymnasium import spaces

action_space = spaces.Discrete(4)
print(action_space.sample())  # 随机: 0, 1, 2, or 3
print(action_space.n)         # 4
print(action_space.contains(3))  # True
print(action_space.contains(5))  # False
```

### Box

```python
obs_space = spaces.Box(low=0, high=255, shape=(84, 84, 3), dtype=np.uint8)
print(obs_space.shape)  # (84, 84, 3)
print(obs_space.sample().shape)  # (84, 84, 3)
```

### Dict

```python
obs_space = spaces.Dict({
    "agent": spaces.Discrete(12),
    "target": spaces.Discrete(12),
})
sample = obs_space.sample()  # {"agent": 7, "target": 3}
```

---

## 🔧 环境注册

### `__init__.py`

```python
from gymnasium.envs.registration import register

register(
    id="my_env/GridWorld-v0",
    entry_point="my_env.envs:MyGridWorldEnv",
    max_episode_steps=200,
)
```

### `pyproject.toml`

```toml
[project]
name = "my_env"
version = "0.0.1"
dependencies = ["gymnasium>=0.26"]

[tool.setuptools.packages.find]
include = ["my_env*"]
```

### 安装和使用

```bash
pip install -e .
```

```python
import my_env
env = gym.make("my_env/GridWorld-v0")
```

---

## 🔧 Stable-Baselines3

### 安装

```bash
pip install stable-baselines3[extra]
```

### DQN（离散动作）

```python
from stable_baselines3 import DQN

env = gym.make("my_env/GridWorld-v0")
model = DQN("MlpPolicy", env, verbose=1,
            learning_rate=1e-3,
            buffer_size=50000,
            exploration_fraction=0.1)
model.learn(total_timesteps=10000, log_interval=4)
model.save("dqn_gridworld")

# 加载和评估
model = DQN.load("dqn_gridworld")
obs, info = env.reset()
for _ in range(100):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
```

### PPO（离散或连续动作）

```python
from stable_baselines3 import PPO

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

### Policy 选择速查

```python
# Discrete 观测 → MlpPolicy
model = DQN("MlpPolicy", env)

# Dict 观测 → MultiInputPolicy
model = DQN("MultiInputPolicy", env)

# 图像观测 (Box with shape HxWxC) → CnnPolicy
model = PPO("CnnPolicy", env)
```

---

## 🔧 Q-Learning + Gymnasium

```python
import gymnasium as gym
import numpy as np

env = gym.make("my_env/GridWorld-v0")
qtable = np.zeros((env.observation_space.n, env.action_space.n))

alpha = 0.1    # 学习率
gamma = 0.99   # 折扣因子
epsilon = 0.1  # 探索率

for episode in range(1000):
    obs, info = env.reset()
    done = False

    while not done:
        # epsilon-greedy
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(qtable[obs])

        next_obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        # Q-Learning 更新
        qtable[obs, action] += alpha * (
            reward + gamma * np.max(qtable[next_obs]) - qtable[obs, action]
        )
        obs = next_obs

env.close()
```

---

## 🔧 PyGame 渲染模板

```python
import pygame

class PyGameRenderer:
    def __init__(self, width=400, height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RL Environment")

    def render(self, state):
        self.screen.fill((255, 255, 255))  # 白色背景
        # 绘制网格、智能体、目标等
        pygame.display.flip()

    def close(self):
        pygame.quit()
```
