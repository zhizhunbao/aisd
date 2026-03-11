# Lab 2 Gymnasium — 教程 (Tutorial)

> 📚 Ref: [Gymnasium 官方文档](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/) + Sutton §3.1 + Lab 2 指导文档
> **核心问题：** Lab 指导文档给出了完整步骤，但没解释 Gymnasium API 与 Lab 1 手写接口的根本区别，以及为什么需要这些额外层（注册、`pyproject.toml`、editable install）。
> **数学前置：** [lab2_gymnasium_math.md](lab2_gymnasium_math.md) — 空间大小、观测索引转换
> **概念前置：** [lab1_cliffwalking_tutorial.md](lab1_cliffwalking_tutorial.md) — Lab 1 手写环境 | [week3_gymnasium_tutorial.md](week3_gymnasium_tutorial.md) — Gymnasium 概念
> **See also:** [故事线](lab2_gymnasium_storyline.md) | [代码速查](lab2_gymnasium_code.md)

---

## §0 前置知识：Lab 1 vs Lab 2 接口对比

这是 Lab 2 最重要的理解起点——**为什么 Lab 2 的接口与 Lab 1 完全不同？**

| 方面 | Lab 1 手写接口 | Lab 2 Gymnasium 接口 |
|------|--------------|---------------------|
| `reset()` 返回 | `(state, reward, done)` — 3 个值 | `(observation, info)` — 2 个值 |
| `step()` 返回 | `(next_state, reward, done)` — 3 个值 | `(obs, reward, terminated, truncated, info)` — 5 个值 |
| 掉崖后行为 | `done=False`，返回起点继续 | `terminated=True`，episode 结束 |
| 状态表示 | 整数（0–47） | Dict/Box（坐标字典） |
| 算法兼容性 | 只兼容自己的 Q-Learning | 兼容所有 SB3 算法 |
| 安装方式 | 直接 import | `pip install -e .`（editable） |

> ⚠️ **最常见 bug：** 从 Lab 1 迁移代码时，忘记适配 `step()` 的返回值差异（3值 vs 5值）。

---

## §1 项目结构与 editable install

### 1.1 目录结构

```
Lab2/
├── lab2_venv/                       ← Python 虚拟环境
└── src/
    ├── null_agent.py                ← 测试脚本
    ├── lab2_qlearning_agent.py      ← 从 Lab 1 迁移的 Q-Learning agent
    └── <id>_cliffwalking_env/       ← Gymnasium 环境包（copier 生成）
        ├── pyproject.toml
        └── cliffwalking_env/
            ├── __init__.py          ← 环境注册
            └── envs/
                ├── __init__.py      ← 导入 CliffWalkingEnv
                ├── grid_world.py    ← 模板（GridWorldEnv）
                └── cliff_walking.py ← 你的实现（CliffWalkingEnv）
```

### 1.2 为什么需要 editable install？

```bash
pip install -e .   # 在 <id>_cliffwalking_env/ 目录下执行
```

**普通 install：** 将代码复制到 `site-packages/`，修改后需要重新安装。

**editable install（`-e`）：** 在 `site-packages/` 中放一个"链接"指向你的源码目录，修改后**立即生效**，无需重新安装。

> 📚 这是开发阶段的标准实践——修改频繁时避免反复安装。

---

## §2 创建 CliffWalkingEnv

### 2.1 从 GridWorldEnv 复制并重命名

```bash
cp envs/grid_world.py envs/cliff_walking.py
```

然后在 `cliff_walking.py` 中：1. 将所有 `GridWorldEnv` 改为 `CliffWalkingEnv`

### 2.2 注册环境（关键步骤）

**`cliffwalking_env/__init__.py`：**

```python
from gymnasium.envs.registration import register

register(
    id="cliffwalking_env/GridWorld-v0",       # 原有
    entry_point="cliffwalking_env.envs:GridWorldEnv",
)
register(
    id="cliffwalking_env/CliffWalking-v0",    # 新增
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
)
```

**`cliffwalking_env/envs/__init__.py`：**

```python
from cliffwalking_env.envs.grid_world import GridWorldEnv
from cliffwalking_env.envs.cliff_walking import CliffWalkingEnv  # 新增
```

> ⚠️ **漏掉注册后的错误：** `gymnasium.error.NameNotFound: Environment 'cliffwalking_env/CliffWalking-v0' doesn't exist`。检查两个 `__init__.py` 是否都正确添加。

---

## §3 实现 CliffWalkingEnv

### 3.1 `__init__()` — 修改网格大小

```python
def __init__(self, render_mode=None, size=(12, 4)):
    self.xsize, self.ysize = size  # 12列 × 4行

    # 观测空间：agent 坐标 + target 坐标
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
    self.action_space = spaces.Discrete(4)
    self.render_mode = render_mode
```

### 3.2 `reset()` — 设置起点和目标

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)  # ← 必须调用，初始化随机数生成器

    self._agent_location = np.array([0, self.ysize - 1], dtype=int)    # 左下角 (0,3)
    self._target_location = np.array([self.xsize - 1, self.ysize - 1], dtype=int)  # 右下角 (11,3)

    return self._get_obs(), self._get_info()
```

> ⚠️ **Gymnasium 约定：** y=0 是顶部，y=3 是底部。起点是左下角 `(0, ysize-1)`，目标是右下角 `(xsize-1, ysize-1)`。

### 3.3 `step()` — 添加悬崖逻辑

```python
def step(self, action):
    direction = self._action_to_direction[action]
    self._agent_location = np.clip(
        self._agent_location + direction,
        [0, 0], [self.xsize - 1, self.ysize - 1]
    )

    x, y = self._agent_location
    bottom_row = (y == self.ysize - 1)
    on_cliff = bottom_row and (1 <= x <= self.xsize - 2)  # 底行非起点非终点
    on_goal = np.array_equal(self._agent_location, self._target_location)

    if on_cliff:
        reward = -100
        terminated = True   # ← Lab 2 与 Lab 1 的关键区别
    elif on_goal:
        reward = 0
        terminated = True
    else:
        reward = -1
        terminated = False

    return self._get_obs(), reward, terminated, False, self._get_info()
```

### 3.4 辅助方法

```python
def _get_obs(self):
    return {
        "agent": self._agent_location,
        "target": self._target_location
    }

def _get_info(self):
    return {
        "distance": np.linalg.norm(
            self._agent_location - self._target_location, ord=1
        )
    }
```

---

## §4 将 Lab 1 Q-Learning 接入 Gymnasium

### 4.1 适配观测转换

```python
def obs_to_state(obs):
    """将 Dict 观测转为整数 state，兼容 Q-Table"""
    x, y = obs["agent"]
    return int(y) * 12 + int(x)   # 对应 Lab 1 的编码方式
```

### 4.2 修改主循环

```python
env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
Q = np.zeros((48, 4))  # 48 states × 4 actions

obs, info = env.reset()                    # ← reset() 返回 2 个值
state = obs_to_state(obs)

while not (terminated or truncated):
    action = np.argmax(Q[state])
    obs, reward, terminated, truncated, info = env.step(action)  # ← step() 返回 5 个值
    next_state = obs_to_state(obs)

    # Q-Learning 更新（与 Lab 1 相同）
    Q[state, action] += alpha * (
        reward + gamma * np.max(Q[next_state]) - Q[state, action]
    )
    state = next_state
```

---

## §5 用 Stable-Baselines3 测试

```python
from stable_baselines3 import PPO, DQN, A2C

# Gymnasium 标准接口使得直接接入 SB3 成为可能
model = PPO("MultiInputPolicy", env, verbose=1)  # MultiInput 处理 Dict 观测
model.learn(total_timesteps=50_000)

obs, _ = env.reset()
for _ in range(200):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    if terminated or truncated:
        obs, _ = env.reset()
```

> 📚 SB3 使用 `"MultiInputPolicy"` 来处理 Dict 观测空间——它会自动展平各个子空间并传入神经网络。这是 Lab 2 相对于 Lab 1 最大的优势：**标准化接口带来了即插即用的算法生态**。
