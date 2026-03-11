# Week 3: Gymnasium — 核心概念 (Core Concepts)

> See also: [幻灯片笔记](week3_gymnasium_slides.md) | [历史背景](week3_gymnasium_history.md) | [操作教程](week3_gymnasium_tutorial.md)

---

## 核心术语速查

### Gymnasium

强化学习环境的 API 标准，包含大量参考环境。提供统一接口（`reset()`/`step()`/`render()`），使任何 RL 算法可以作用于任何兼容环境。

> Gymnasium 是 OpenAI Gym 的继任者，由 Farama 基金会（2022）维护。

---

### `reset()` 方法

```python
obs, info = env.reset(seed=None, options=None)
```

重置环境到初始状态，返回初始观测和调试信息。每个 episode 开始时调用。

- `seed`：随机种子，用于复现实验

---

### `step()` 方法（★ 必考）

```python
obs, reward, terminated, truncated, info = env.step(action)
```

| 返回值 | 类型 | 含义 |
|--------|------|------|
| `obs` | array/dict | 执行动作后的新观测 |
| `reward` | float | 即时奖励 |
| `terminated` | bool | 自然结束（到达目标/死亡等） |
| `truncated` | bool | 超时结束（TimeLimit 触发） |
| `info` | dict | 调试信息，不用于学习 |

> ⚠️ **易错：** 旧 Gym 返回 4 个值（`done`），Gymnasium 返回 5 个。`terminated` 和 `truncated` 语义不同，不能混用。

---

### `terminated` vs `truncated`

| 信号 | 触发原因 | 处理方式 |
|------|---------|---------|
| `terminated = True` | 自然结束（任务完成或失败） | Q 值更新不含未来奖励 |
| `truncated = True` | 时间限制到期（TimeLimit wrapper） | 可能还有未来奖励，bootstrap 处理 |

**价值估计的区别：** `terminated` 时终止状态 $Q = 0$；`truncated` 时终止状态 $Q \neq 0$（任务还没真正结束）。

---

### Observation Space（观测空间）

描述环境返回的观测的数据格式：

| 类型 | 用法 | 示例 |
|------|------|------|
| `Discrete(n)` | $n$ 个离散整数 $[0, n)$ | 状态编号 |
| `Box(low, high, shape, dtype)` | 连续 n 维数组 | 像素图像、关节角度 |
| `Dict({...})` | 多个空间的字典 | `{"current": Discrete, "target": Discrete}` |

---

### Action Space（动作空间）

描述 Agent 可以选择的动作格式：

| 类型 | 含义 |
|------|------|
| `Discrete(n)` | $n$ 个离散动作（整数 $0$ 到 $n-1$） |
| `Box(...)` | 连续动作（如机器人关节力矩） |
| `MultiDiscrete([n1, n2, ...])` | 多个独立离散变量（如"选积木 + 选位置"） |

---

### Wrapper（包装器）

不修改底层环境代码，在其外层添加功能的设计模式：

```python
env = gym.make("SomeEnv-v0")
env = TimeLimit(env, max_episode_steps=200)   # 添加时间限制
env = DiscreteActionWrapper(env)               # 修改动作空间
```

**Wrapper 的工作方式：** 拦截 `step()` / `reset()` 等方法，在调用底层环境前后做处理。

常用内置 Wrapper：
- `TimeLimit` — 限制每 episode 最大步数
- `RecordEpisodeStatistics` — 记录 episode 统计

---

### Policy 选择（MlpPolicy vs MultiInputPolicy）

| Policy | 适用观测空间 | 何时使用 |
|--------|------------|---------|
| `MlpPolicy` | `Discrete` 或 `Box` | 单一观测 |
| `MultiInputPolicy` | `Dict` | 字典观测（含多个 key） |

---

### 自定义环境创建步骤

```python
class MyEnv(gymnasium.Env):
    def __init__(self):
        self.observation_space = spaces.Discrete(n)
        self.action_space = spaces.Discrete(m)

    def reset(self, seed=None, options=None):
        return obs, info

    def step(self, action):
        return obs, reward, terminated, truncated, info

    def render(self): ...
    def close(self): ...
```

---

## 概念辨析

### `Discrete` vs `Box` vs `MultiDiscrete`

| 空间 | 数据类型 | 典型场景 |
|------|---------|---------|
| `Discrete(n)` | 单一整数 | 方向键（上下左右） |
| `Box(...)` | 浮点数组 | 连续控制（速度、角度） |
| `MultiDiscrete([n1,n2])` | 整数数组 | 多个独立离散决策 |

DQN 只支持 `Discrete`，PPO/SAC 支持 `Box`（连续）和 `Discrete`（离散）。这是 Week 5 需要 `DiscreteActionWrapper` 的根本原因。

### `terminated` vs `truncated` 对价值估计的影响

- `terminated`：真正的终止状态，Bellman 更新用 $Q = 0$（无未来）
- `truncated`：人为截断，理论上任务还可以继续。高质量实现中应 bootstrap（用 $V(s')$ 估计未来价值）

---

## 易错点速查

| 错误 | 正确理解 |
|------|---------|
| `import gym` | 用 `import gymnasium as gym`（课程全程用 Gymnasium） |
| `step()` 解包 4 个值 | Gymnasium 返回 5 个：`obs, reward, terminated, truncated, info` |
| `terminated or truncated` 判断结束 | 两者都要检测：`done = terminated or truncated` |
| `MultiDiscrete` 直接用 DQN | 需要 `DiscreteActionWrapper` 先展平 |
| 先用 Dict 空间却选 `MlpPolicy` | Dict 空间必须用 `MultiInputPolicy` |
