# Week 3: Gymnasium — 概念速查 (Concept Cheatsheet)

> See also: [数学公式](week3_gymnasium_math.md) | [代码参考](week3_gymnasium_code.md)

---

## 📖 核心定义

### Gymnasium
- OpenAI Gym 的继任者（由 Farama Foundation 维护）
- 提供 RL 环境的标准 API
- `import gymnasium as gym`

### gymnasium.Env
- 所有自定义环境必须继承的基类
- 5 个核心方法：`__init__`, `reset`, `step`, `render`, `close`

### Spaces（空间）
- 描述观测空间和动作空间的元信息（类型、范围、维度）
- `from gymnasium import spaces`

### Stable-Baselines3 (SB3)
- 一组与 Gymnasium 兼容的标准 RL 算法实现
- 包含 DQN, PPO, A2C 等

---

## 💡 关键要点

1. **Gym → Gymnasium 三大变化：**
   - `import gymnasium as gym`（不再是 `import gym`）
   - `reset()` 新增 `seed` 参数
   - `step()` 返回 5 个值（新增 `truncated`）

2. **`step()` 返回值：** `(observation, reward, terminated, truncated, info)`

3. **`terminated` vs `truncated`：**
   - `terminated` = 任务自然结束（到达目标/掉入悬崖）
   - `truncated` = 人为截断（超过 `max_episode_steps`）

4. **`reset()` 返回值：** `(observation, info)` — 只有 2 个值

5. **环境注册格式：** `"namespace/EnvName-vN"`（如 `"blocksworld_env/BlocksWorld-v0"`）

6. **安装自定义环境：** `pip install -e .`（editable mode）

---

## ⚠️ 常见陷阱

| 陷阱 | 正确做法 | 来源 |
|------|---------|------|
| `step()` 只解包 4 个值 | 必须解包 5 个：`obs, reward, terminated, truncated, info` | Slide 7 |
| Dict 观测用 `MlpPolicy` | Dict 观测必须用 `MultiInputPolicy` | Slide 12-13 |
| `reset()` 不传 seed | 传 `seed` 以确保可复现性 | Slide 7 |
| 用 `np.random` 生成随机数 | 用 `self.np_random`（通过 `super().reset(seed=seed)` 设置）| Gymnasium Docs |
| `from gym import spaces` | 必须 `from gymnasium import spaces` | Slide 8 |
| 忘记调用 `super().reset()` | `reset()` 中必须先调用 `super().reset(seed=seed)` | Gymnasium Docs |

---

## 📊 对比表

### Spaces 类型对比

| Space | 数学含义 | 示例 | SB3 Policy |
|-------|---------|------|-----------|
| `Discrete(n)` | {0, ..., n-1} | 4 个方向 | `MlpPolicy` |
| `Box(low, high, shape)` | 连续/整数范围 | 坐标 (x,y) | `MlpPolicy` |
| `Dict({...})` | 多空间组合 | agent+target | `MultiInputPolicy` |
| `MultiDiscrete([n1,n2])` | 多维离散 | 网格坐标 | `MlpPolicy` |

### SB3 算法对比

| 算法 | 类型 | 动作空间 | 特点 |
|------|------|---------|------|
| DQN | Off-policy, Value-based | 仅 Discrete | 经典，适合小离散空间 |
| PPO | On-policy, Policy Gradient | Discrete + Continuous | 通用，稳定 |
| A2C | On-policy, Actor-Critic | Discrete + Continuous | 简单，快速 |

### Lab 1 vs Lab 2 vs Assignment 1

| 维度 | Lab 1 | Lab 2 | Assignment 1 |
|------|-------|-------|-------------|
| 环境 | 自制 Env | Gymnasium Env | Gymnasium + Prolog |
| 算法 | Q-Learning | Q-Learning | Q-Learning + SB3 |
| 渲染 | 无 | PyGame | PyGame |
| 状态 | 手动编码 | spaces API | spaces.Discrete |
