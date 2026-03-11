# Lab 2 代码速查：Gymnasium 自定义 CliffWalking 环境

> **Source:** `CST8509_Lab2_Gymnasium.md`
> **故事线：** [lab2_gymnasium_storyline.md](lab2_gymnasium_storyline.md)
> **关联 slides：** [Week 3 Gymnasium](week3_gymnasium_slides.md) | [Week 6 复习](week6_midterm_review_slides.md)

---

## 1. Gymnasium 环境标准接口

### 1.1 核心方法签名

```python
import gymnasium as gym
import numpy as np
from gymnasium import spaces

class CliffWalkingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=(12, 4)):
        self.xsize, self.ysize = size

        # 观测空间：字典，包含 agent 位置和 target 位置
        self.observation_space = spaces.Dict({
            "agent": spaces.Box(
                low=np.array([0, 0]),
                high=np.array([self.xsize - 1, self.ysize - 1]),
                shape=(2,), dtype=int
            ),
            "target": spaces.Box(
                low=np.array([0, 0]),
                high=np.array([self.xsize - 1, self.ysize - 1]),
                shape=(2,), dtype=int
            ),
        })

        # 动作空间：离散4个方向（右/上/左/下）
        self.action_space = spaces.Discrete(4)
        self.render_mode = render_mode

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # 初始化 agent 位置和 target 位置
        self._agent_location = np.array([0, 0], dtype=int)
        self._target_location = np.array([self.xsize - 1, 0], dtype=int)
        observation = self._get_obs()
        info = self._get_info()
        return observation, info  # ← 返回 2 个值

    def step(self, action):
        # 执行动作，更新 agent 位置
        direction = self._action_to_direction[action]
        self._agent_location = np.clip(
            self._agent_location + direction,
            [0, 0], [self.xsize - 1, self.ysize - 1]
        )
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0
        observation = self._get_obs()
        info = self._get_info()
        return observation, reward, terminated, False, info  # ← 返回 5 个值

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        return {"distance": np.linalg.norm(
            self._agent_location - self._target_location, ord=1)}
```

> ⚠️ **关键记忆点：**
> - `reset()` → 返回 `(observation, info)` — **2 个值**
> - `step()` → 返回 `(obs, reward, terminated, truncated, info)` — **5 个值**
> - `terminated`：自然结束（到达目标 / 掉入悬崖）
> - `truncated`：超时截断（`TimeLimit` wrapper 触发）

---

## 2. 环境注册

### 2.1 `cliffwalking_env/__init__.py`

```python
from gymnasium.envs.registration import register

register(
    id="cliffwalking_env/CliffWalking-v0",
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
)
```

### 2.2 `cliffwalking_env/envs/__init__.py`

```python
from cliffwalking_env.envs.cliff_walking import CliffWalkingEnv
```

### 2.3 使用注册的环境

```python
import gymnasium
import cliffwalking_env  # 需要先 import 触发 register()

env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
```

---

## 3. Null Agent（验证环境可运行）

```python
import gymnasium
import cliffwalking_env

env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # 随机动作
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

---

## 4. Q-Learning Agent 适配（Lab 1 → Lab 2）

### 4.1 状态空间与动作空间计算

```python
# 总状态数：xsize × ysize = 12 × 4 = 48
numstates = (env.observation_space['agent'].high[0] + 1) * \
            (env.observation_space['agent'].high[1] + 1)

# 总动作数：Discrete(4)
numactions = env.action_space.n

# 初始化 Q-table
qtable = np.zeros((numstates, numactions))
```

### 4.2 观测字典 → 整数 state 索引

```python
def obs_to_state(state_dict, env):
    x = state_dict['agent'][0]
    y = state_dict['agent'][1]
    xsize = env.observation_space['agent'].high[0] + 1
    return y * xsize + x  # 行优先展平：state = y * xsize + x
```

> 💡 **直觉：** 把 12×4 网格按行展平为 48 个格子，state = y 行 × 12 + x 列

### 4.3 完整 Q-Learning 训练循环

```python
import numpy as np

alpha = 0.1    # 学习率
gamma = 0.99   # 折扣因子
epsilon = 1.0  # 初始探索率
epsilon_min = 0.01
epsilon_decay = 0.995

for episode in range(num_episodes):
    state_dict, info = env.reset()
    state = obs_to_state(state_dict, env)
    done = False

    while not done:
        # ε-greedy 动作选择
        if np.random.random() < epsilon:
            action = env.action_space.sample()       # 探索
        else:
            action = np.argmax(qtable[state])        # 利用

        next_state_dict, reward, terminated, truncated, info = env.step(action)
        next_state = obs_to_state(next_state_dict, env)
        done = terminated or truncated

        # Q-table 更新（Bellman 方程）
        qtable[state][action] = qtable[state][action] + alpha * (
            reward + gamma * max(qtable[next_state]) - qtable[state][action]
        )

        state = next_state

    epsilon = max(epsilon_min, epsilon * epsilon_decay)
```

---

## 5. Stable-Baselines3 接入

### 5.1 DQN

```python
import gymnasium
import cliffwalking_env
from stable_baselines3 import DQN

env = gymnasium.make("cliffwalking_env/CliffWalking-v0")

# MultiInputPolicy：因为观测是字典（多输入）
model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000, log_interval=4)
model.save("dqn_cliff")
```

### 5.2 PPO

```python
from stable_baselines3 import PPO

model = PPO("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_cliff")
```

### 5.3 加载并运行已训练模型

```python
model = DQN.load("dqn_cliff", env=env)

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
```

> ⚠️ **为什么用 `MultiInputPolicy`？**
> 观测是 `{"agent": [...], "target": [...]}` 字典格式（多输入）。
> `MlpPolicy` 只接受单一 numpy array。
> `MultiInputPolicy` 为每个键分别编码再合并。

---

## 6. 关键接口对比速查

| | Lab 1（手写） | Lab 2（Gymnasium） |
|--|--------------|-------------------|
| `reset()` 返回 | 取决于自己实现 | `(observation, info)` |
| `step()` 返回 | `(next_state, reward, done)` | `(obs, reward, terminated, truncated, info)` |
| 状态格式 | 整数 | 字典 `{"agent": [x,y], "target": [tx,ty]}` |
| 与 SB3 兼容 | ❌ | ✅ |
| PyGame 渲染 | ❌ | ✅ `render_mode="human"` |

---

## 7. 常见错误速查

| 错误 | 原因 | 修复 |
|------|------|------|
| `EnvNotFound` | 忘记 `import cliffwalking_env` | 在 `gymnasium.make()` 前加 import |
| `ValueError: too many values to unpack` | 用 Lab 1 的 3-值解包接收 `step()` | 改为 5 个变量接收 |
| Q-table 索引错误 | 直接用字典 obs 作索引 | 用 `obs_to_state()` 转换为整数 |
| SB3 报错 `Box observation expected` | 用了 `MlpPolicy` 但观测是字典 | 改用 `MultiInputPolicy` |
