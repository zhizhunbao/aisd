# Week 3: Gymnasium 环境 — 故事线 (Storyline)

> 基于 CST8509_03_Gymnasium slides + Lab 2
> 核心问题：如何将"自制"RL 环境升级为工业标准的 Gymnasium 接口？

---

## 🗺️ 路线图 (Roadmap)

```
Lab 1: 自制环境                    Lab 2: Gymnasium 环境              Assignment 1: 完整系统
┌──────────────┐              ┌──────────────────┐              ┌──────────────────────┐
│ 手写 Env 类   │  ──升级──→  │ gymnasium.Env     │  ──扩展──→  │ Prolog + Gymnasium   │
│ 手写 Q-table  │              │ spaces API        │              │ + Stable-Baselines3  │
│ 无渲染        │              │ PyGame 渲染       │              │ + PyGame 渲染        │
└──────────────┘              └──────────────────┘              └──────────────────────┘
```

---

## 📖 因果叙事 (Causal Narrative)

### 问题起点：Lab 1 的"自制"环境有什么问题？

Lab 1 中我们手写了 `cliff_env.py`，它能跑，但有几个致命缺陷：

1. **接口不标准** — 每个人写的 `reset()`、`step()` 签名不同，换个算法就得改代码
2. **无法复用算法库** — Stable-Baselines3 等工业级 RL 库要求标准接口
3. **无渲染能力** — 看不到智能体在做什么，调试困难

### 解决方案：Gymnasium 标准化

Gymnasium（OpenAI Gym 的继任者）定义了一套标准 API：

```python
import gymnasium as gym

class MyEnv(gymnasium.Env):
    def __init__(self, render_mode=None): ...
    def reset(self, seed=None, options=None): ...
    def step(self, action):
        return observation, reward, terminated, truncated, info
    def render(self): ...
    def close(self): ...
```

关键改进（Gym → Gymnasium）：
- `reset()` 新增 `seed` 参数 → 可复现随机序列
- `step()` 新增 `truncated` 返回值 → 区分"任务完成"和"超时截断"
- `import gymnasium as gym` 替代 `import gym`

### 核心概念：Spaces（空间定义）

Gymnasium 用 `spaces` 模块定义观测空间和动作空间：

| Space 类型 | 用途 | 示例 |
|-----------|------|------|
| `spaces.Discrete(n)` | 离散整数 {0, 1, ..., n-1} | 4 个方向动作 |
| `spaces.Box(low, high, shape)` | 连续/整数范围 | 网格坐标 (x, y) |
| `spaces.Dict({...})` | 字典组合多个空间 | agent 位置 + target 位置 |

### 观测空间的三种设计方式

Slides 展示了三种递进的观测空间设计：

| 方式 | observation_space | 适用场景 | SB3 Policy |
|------|------------------|---------|------------|
| Box Dict | `Dict({"agent": Box(...), "target": Box(...)})` | 连续坐标 | `MultiInputPolicy` |
| Discrete Dict | `Dict({"agent": Discrete(n), "target": Discrete(n)})` | 离散状态+分离目标 | `MultiInputPolicy` |
| Single Discrete | `Discrete(n)` | 状态和目标合并为一个整数 | `MlpPolicy` |

⚠️ **关键陷阱：** Policy 选择必须匹配观测空间类型！
- `Dict` 观测 → `MultiInputPolicy`
- `Discrete` 观测 → `MlpPolicy`

### 与 Stable-Baselines3 的集成

有了标准 Gymnasium 接口，就可以直接使用工业级算法：

```python
from stable_baselines3 import DQN

env = gym.make("blocksworld_env/BlocksWorld-v0", render_mode="human")
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("dqn_blocks")
```

这比手写 Q-Learning 强大得多：
- DQN 用神经网络近似 Q 函数 → 可处理大状态空间
- PPO 是 policy gradient 方法 → 可处理连续动作空间
- 训练、保存、加载都是标准化的

### 环境打包与注册

Gymnasium 要求环境以 Python 包的形式安装：

```
<name>_blocksworld_env/
    pyproject.toml
    blocksworld_env/
        __init__.py          # 注册环境
        envs/
            __init__.py
            blocks_world.py  # 环境实现
```

安装后通过 `gym.make("blocksworld_env/BlocksWorld-v0")` 使用。

### Assignment 1 预览：Prolog + Gymnasium + PyGame

Assignment 1 将所有组件整合：
- **Prolog** — 用情境演算（situation calculus）定义积木世界的逻辑规则
- **Gymnasium** — 标准化环境接口
- **PyGame** — 可视化渲染
- **Agent** — Q-Learning 或 Stable-Baselines3 (DQN/PPO)

```
Agent ──action──→ Gymnasium Env ──Prolog──→ 状态转移
  ↑                    │                      │
  └── reward, obs ←────┘         render() ──→ PyGame
```

---

## 📊 对比表 (Comparison Table)

| 维度 | Lab 1 自制环境 | Lab 2 Gymnasium | Assignment 1 |
|------|---------------|-----------------|--------------|
| 环境接口 | 自定义 | `gymnasium.Env` 标准 | `gymnasium.Env` 标准 |
| 状态表示 | 手动编码 | `spaces` API | `spaces.Discrete` |
| 算法 | 手写 Q-Learning | 手写 Q-Learning | Q-Learning + SB3 |
| 渲染 | 无 | PyGame | PyGame |
| 后端逻辑 | Python | Python | Prolog + Swiplserver |
| 可复用性 | ❌ 低 | ✅ 高 | ✅ 高 |

---

## ✅ 考试 Checklist

- [ ] Gymnasium 是 OpenAI Gym 的继任者，`import gymnasium as gym`
- [ ] `reset()` 返回 `(observation, info)`，接受 `seed` 参数
- [ ] `step()` 返回 `(observation, reward, terminated, truncated, info)` — 5 个值
- [ ] `terminated` vs `truncated`：任务完成 vs 超时截断
- [ ] `spaces.Discrete(n)` 用于离散空间，`spaces.Dict` 用于组合空间
- [ ] Dict 观测 → `MultiInputPolicy`，Discrete 观测 → `MlpPolicy`
- [ ] 环境需打包为 Python 包并通过 `pip install -e .` 安装
- [ ] `gym.make("namespace/EnvName-v0")` 创建环境实例

---

## 📚 参考资料

- [Gymnasium 官方文档 - 环境创建教程](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)
- [Stable-Baselines3 文档](https://stable-baselines3.readthedocs.io/)
- Lab 2: `courses/rl/labs/CST8509_Lab2_Gymnasium.md`
- Week 3 Tutorial: `week3_gymnasium_tutorial.md`（教科书补充）
