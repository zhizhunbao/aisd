# Week 3: Gymnasium 环境 — 教程 (Tutorial)

> 📚 基于 Gymnasium 官方文档 + Sutton & Barto Ch.3 (The Agent-Environment Interface)
> 核心问题：Slides 展示了 API 用法，但没解释 Gymnasium 的设计哲学和 MDP 接口的理论基础

---

## §0 前置知识 (Prerequisites)

> **数学前置：** 本周主要是工程实践，数学要求较低。
> **概念前置：** MDP 五元组 $(S, A, P, R, \gamma)$ — 参见 `week2_mdp_tutorial.md`

### 贯穿例子：4×3 GridWorld

本教程使用一个 4×3 网格世界贯穿所有示例：

```
┌───┬───┬───┬───┐
│ S │   │   │ +1│  ← 目标（terminated=True）
├───┼───┼───┼───┤
│   │ ▓ │   │ -1│  ← 悬崖（terminated=True）
├───┼───┼───┼───┤
│   │   │   │   │
└───┴───┴───┴───┘
  S = 起点, ▓ = 墙壁
  动作: {0: 右, 1: 上, 2: 左, 3: 下}
  状态: 0-11 的整数（4×3=12 个格子）
```

---

## §1 Agent-Environment Interface 的形式化

> 📚 Ref: Sutton & Barto §3.1 — The Agent-Environment Interface

Sutton 教科书将 RL 问题形式化为 Agent 和 Environment 之间的交互循环：

$$A_t \rightarrow \text{Environment} \rightarrow (S_{t+1}, R_{t+1})$$

在每个时间步 $t$：
1. Agent 观察状态 $S_t$
2. Agent 选择动作 $A_t$
3. Environment 返回新状态 $S_{t+1}$ 和奖励 $R_{t+1}$

**Gymnasium 的 `step()` 方法正是这个循环的代码实现：**

```python
# 理论：Agent 选择 A_t，Environment 返回 S_{t+1}, R_{t+1}
# 代码：
observation, reward, terminated, truncated, info = env.step(action)
#  S_{t+1}    R_{t+1}   是否结束    是否截断    额外信息
```

> ⚠️ **Slides 未强调：** `terminated` 和 `truncated` 的区分是 Gymnasium 相对于旧版 Gym 的重要改进。
> - `terminated=True`：任务自然结束（到达目标或掉入悬崖）— 对应 MDP 的终止状态
> - `truncated=True`：人为截断（超过最大步数）— 不是 MDP 的一部分，是工程需要

---

## §2 Observation Space 的设计哲学

> 📚 Ref: Gymnasium API Documentation — Spaces

Slides 展示了三种观测空间，但没解释**为什么要这样设计**。

### 2.1 为什么需要 Spaces？

MDP 理论中，状态空间 $S$ 是一个抽象集合。但在代码中，算法需要知道：
- 状态是什么类型？（整数？向量？字典？）
- 状态的范围是什么？（0-11？还是连续的 [-1, 1]？）
- 状态的维度是什么？（标量？2D 坐标？图像？）

`spaces` 模块就是用来**声明这些元信息**的：

| Space | 数学对应 | 代码示例 | 适用场景 |
|-------|---------|---------|---------|
| `Discrete(n)` | $S = \{0, 1, ..., n-1\}$ | `Discrete(12)` | 网格位置编号 |
| `Box(low, high, shape)` | $S \subseteq \mathbb{R}^d$ | `Box(0, 11, shape=(2,))` | 连续坐标 |
| `Dict({...})` | $S = S_1 \times S_2$ | `Dict({"pos": ..., "vel": ...})` | 复合状态 |
| `MultiBinary(n)` | $S = \{0, 1\}^n$ | `MultiBinary(4)` | 开关状态 |
| `MultiDiscrete([n1, n2])` | $S = \{0..n_1\} \times \{0..n_2\}$ | `MultiDiscrete([4, 3])` | 网格坐标 |

### 2.2 观测空间设计的权衡

Slides 展示了三种方式，它们的权衡是：

```
Dict + Box          Dict + Discrete       Single Discrete
(最灵活)            (中间方案)             (最简单)
┌─────────┐        ┌─────────┐           ┌─────────┐
│ agent: [x,y] │   │ agent: 7  │         │ state: 42 │
│ target: [x,y]│   │ target: 3 │         │           │
└─────────┘        └─────────┘           └─────────┘
  ↓                  ↓                     ↓
MultiInputPolicy   MultiInputPolicy      MlpPolicy
  ↓                  ↓                     ↓
更多参数，更慢      中等                   最少参数，最快
```

**选择原则：**
- 状态空间小（<1000）→ `Discrete` 足够
- 需要分离 agent/target 信息 → `Dict`
- 连续状态（如物理模拟）→ `Box`

---

## §3 Gymnasium 环境的生命周期

> 📚 Ref: Gymnasium API — `gymnasium.Env`

Slides 列出了 5 个方法但没解释它们的**调用顺序和职责边界**。

### 3.1 完整生命周期

```
gym.make() ──→ __init__()
                  │
                  ↓
              reset() ←──────────────────┐
                  │                       │
                  ↓                       │
              step(action) ──→ terminated │
                  │              or       │
                  ↓           truncated?──┘
              render()            │
                                  ↓ (全部 episode 结束)
                              close()
```

### 3.2 每个方法的职责

| 方法 | 输入 | 输出 | 职责 |
|------|------|------|------|
| `__init__` | `render_mode`, 环境参数 | — | 定义 spaces，初始化渲染 |
| `reset` | `seed`, `options` | `(obs, info)` | 重置到初始状态，设置 RNG |
| `step` | `action` | `(obs, reward, terminated, truncated, info)` | 执行一步，返回结果 |
| `render` | — | 帧或 None | 可视化当前状态 |
| `close` | — | — | 释放资源（关闭窗口等）|

### 3.3 `reset()` 的 seed 机制

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)  # 设置 self.np_random
    # 之后用 self.np_random 生成随机数
    self._agent_location = self.np_random.integers(0, self.size, size=2)
    return observation, info
```

> ⚠️ **Slides 未强调：** `super().reset(seed=seed)` 会设置 `self.np_random`（一个 NumPy RandomGenerator）。所有环境内的随机操作都应该用 `self.np_random` 而不是 `np.random`，这样才能通过 seed 复现。

---

## §4 环境注册与打包

> 📚 Ref: Gymnasium Documentation — Registration

Slides 展示了目录结构但没解释**注册机制**。

### 4.1 `__init__.py` 中的注册

```python
# blocksworld_env/__init__.py
from gymnasium.envs.registration import register

register(
    id="blocksworld_env/BlocksWorld-v0",  # 唯一标识符
    entry_point="blocksworld_env.envs:BlocksWorldEnv",  # 类的路径
    max_episode_steps=200,  # 可选：最大步数（触发 truncated）
)
```

### 4.2 命名规范

```
namespace/EnvName-vN
   │         │     │
   │         │     └── 版本号（从 0 开始）
   │         └── 环境名（CamelCase）
   └── 包名（通常与目录名一致）
```

### 4.3 `pyproject.toml` 最小配置

```toml
[project]
name = "blocksworld_env"
version = "0.0.1"
dependencies = ["gymnasium>=0.26", "pygame>=2.1"]

[tool.setuptools.packages.find]
include = ["blocksworld_env*"]
```

安装：`pip install -e .`（editable mode，修改代码后无需重新安装）

---

## §5 Stable-Baselines3 集成

> 📚 Ref: Stable-Baselines3 Documentation — Getting Started

### 5.1 SB3 的核心抽象

Stable-Baselines3 将 RL 算法封装为统一接口：

```python
from stable_baselines3 import DQN, PPO, A2C

# 所有算法共享相同的 API
model = DQN("MlpPolicy", env, verbose=1)  # 创建
model.learn(total_timesteps=10000)          # 训练
model.save("model_name")                    # 保存
model = DQN.load("model_name")             # 加载
action, _ = model.predict(obs)              # 预测
```

### 5.2 Policy 与 Space 的对应关系

这是 Slides 的核心知识点，但容易混淆：

| 观测空间类型 | SB3 Policy | 内部处理 |
|-------------|-----------|---------|
| `Discrete(n)` | `MlpPolicy` | one-hot 编码 → 全连接网络 |
| `Box(shape=(d,))` | `MlpPolicy` | 直接输入 → 全连接网络 |
| `Dict({...})` | `MultiInputPolicy` | 每个 key 单独编码 → 拼接 → 全连接 |
| `Box(shape=(H,W,C))` | `CnnPolicy` | 图像 → CNN → 全连接 |

> ⚠️ **常见错误：** 用 `MlpPolicy` 处理 `Dict` 观测会报错。必须用 `MultiInputPolicy`。

### 5.3 DQN vs PPO vs A2C

| 算法 | 类型 | 动作空间 | 适用场景 |
|------|------|---------|---------|
| DQN | Off-policy, Value-based | 仅 Discrete | 小离散动作空间 |
| PPO | On-policy, Policy Gradient | Discrete + Continuous | 通用，稳定 |
| A2C | On-policy, Actor-Critic | Discrete + Continuous | 简单，快速 |

---

## 📚 参考索引表

| 教程章节 | 来源 | 核心内容 | Slides 覆盖？ |
|---------|------|---------|-------------|
| §1 Agent-Environment Interface | Sutton §3.1 | step() 的理论基础 | ⚠️ 部分（只展示了 API） |
| §2 Observation Space 设计 | Gymnasium Docs | spaces 的设计哲学和权衡 | ⚠️ 部分（只展示了 3 种方式） |
| §3 环境生命周期 | Gymnasium Docs | 方法调用顺序和 seed 机制 | ❌ 未覆盖 |
| §4 环境注册与打包 | Gymnasium Docs | register() 和命名规范 | ⚠️ 部分（只展示了目录结构） |
| §5 SB3 集成 | SB3 Docs | Policy 选择和算法对比 | ⚠️ 部分（只展示了 DQN） |
