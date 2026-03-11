# 🕰️ Lab 2 Gymnasium — 技术演进历史线

> **课程:** CST8509 Reinforcement Learning | **主题:** Gymnasium & 标准化 RL 接口
> **时间跨度:** 1957 — 2022
> **核心脉络:** 手写环境 → OpenAI Gym → Gymnasium → SB3 生态
> **Source:** Brockman et al. 2016 + Towers et al. 2023 + Raffin et al. 2021 + Lab 2 指导文档

---

## 📍 全景时间线（Timeline Overview）

```
1957         1989         2013         2016         2019         2021         2022
  │            │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼            ▼
Bellman      Q-Learning   DeepMind     OpenAI       SB3 前身     Stable-      Gymnasium
DP 基础      诞生         ALE Atari    Gym          rl-baselines Baselines3   (Farama)
                          环境                      发布         发布         接管维护
  │            │            │            │            │            │            │
  └──── 算法 ──┘            └──── 基准 ──┘            └──── 工具链 ─┘            │
                                                                      ← 我们在这 ──┘
```

---

## 第 1 站：手写环境的困境 (1989–2012)

### 🧩 之前的问题

Q-Learning 提出后，研究者们需要在各种环境中测试算法。问题：**每篇论文都自己写一套环境，既不可复现，又无法公平比较不同算法。**

早期 RL 实验的典型问题：
- 环境实现细节不透明（奖励缩放、episode 截断策略各不相同）
- 实验结果差异很大，难以判断来自算法还是环境
- 超参数共享困难，调参经验无法迁移

### 💡 核心创新

研究者开始意识到需要**标准化环境**。第一个重要里程碑是：

**Arcade Learning Environment (ALE, 2013)**  
Bellemare 等人将 Atari 2600 游戏包装为 RL 基准，提供统一接口——这是 OpenAI Gym 的直接前身。

### 👤 关键人物

- **Marc Bellemare** — University of Alberta, 2013
- 论文: "The Arcade Learning Environment: An Evaluation Platform for General Agents" (JAIR, 2013)

### ⚠️ 遗留问题

ALE 只覆盖 Atari 游戏。研究者需要一个**通用框架**，能支持从简单网格到复杂机器人控制的各类环境。

---

## 第 2 站：OpenAI Gym 诞生 (2016)

### 🧩 之前的问题

2015–2016 年，RL 算法（DQN、PPO、TRPO 等）快速涌现。问题：每个研究组用不同的环境测试，**结果几乎无法复现和比较**。

### 💡 核心创新

**OpenAI** 在 2016 年发布 **Gym**——第一个被广泛采用的标准化 RL 环境框架：

```python
# Gym 定义了标准接口（影响至今）
env = gym.make("CartPole-v1")
obs = env.reset()
obs, reward, done, info = env.step(action)  # 4 个返回值
```

**关键设计：**
- `reset()` / `step()` / `render()` 三个核心方法
- `observation_space` / `action_space` 声明接口
- 一组经典环境：CartPole、MountainCar、Atari、MuJoCo

CliffWalking 也作为经典教材环境被收入：`gym.make("CliffWalking-v0")`

### 👤 关键人物

- **Greg Brockman, Vicki Cheung, Ludwig Pettersson** 等 — OpenAI, 2016
- 论文: "OpenAI Gym" (arXiv, 2016)

### 📊 里程碑数据

- 截至 2022 年：GitHub 超过 **30,000 Stars**
- 被引用超过 **10,000 次**（Google Scholar）
- 支持 50+ 环境，第三方实现数百个

### ⚠️ 遗留问题

随着社区用量增大，Gym 出现多个问题：
1. `done` 混淆了自然终止和超时截断
2. `reset()` 不支持 `seed` 参数（可复现性差）
3. OpenAI 逐渐停止维护（2021 年后无实质更新）

---

## 第 3 站：Stable-Baselines3 (2021)

### 🧩 之前的问题

Gym 标准化了环境，但**算法实现**仍然分散且质量参差不齐。研究者想要"可以直接信任的"算法实现。

### 💡 核心创新

**Antonin Raffin 等人**（本课程 Week 4 的主角）发布 **Stable-Baselines3（SB3）**——可靠的 PyTorch RL 算法库：

```python
from stable_baselines3 import DQN, PPO, A2C
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100_000)
```

**关键特性：**
- 实现了 8+ 种主流算法（DQN、PPO、SAC、TD3 等）
- 每个算法都经过严格测试，性能与论文基本一致
- 与 Gym/Gymnasium 深度集成

### 👤 关键人物

- **Antonin Raffin, Ashley Hill, Adam Gleave** 等
- 论文: "Stable-Baselines3: Reliable Reinforcement Learning Implementations" (JMLR, 2021)

### 🔗 与 Lab 2 的关联

> Lab 2 要求使用 SB3 算法在你的 Gymnasium 环境上运行。Raffin 的 RL 实践建议（Week 4 内容 + Quiz 4）是 SB3 设计理念的直接体现。

---

## 第 4 站：Gymnasium 发布——接管维护 (2022)

### 🧩 之前的问题

2021 年末，OpenAI Gym 实际上已经停止维护。社区需要一个可持续维护的替代版本来修复已知问题。

### 💡 核心创新

**Farama Foundation**（非营利组织）接管了 Gym，发布 **Gymnasium**：

**主要改进（与旧 Gym 的区别）：**

| 方面 | 旧 OpenAI Gym | 新 Gymnasium |
|------|-------------|-------------|
| `step()` 返回值 | `(obs, reward, done, info)` — 4 个 | `(obs, reward, terminated, truncated, info)` — 5 个 |
| `reset()` 参数 | 无 `seed` 参数 | 支持 `seed` 参数（可复现） |
| `done` 语义 | 混合自然终止和超时 | 明确区分 `terminated` vs `truncated` |
| 维护状态 | 停止维护 | 积极维护（2022–至今） |

`terminated`（终止）vs `truncated`（截断）的区分是 Lab 2 的核心概念：

```python
# terminated=True：自然结束（到达目标 / 掉入悬崖）
# truncated=True：超时截断（TimeLimit wrapper，非 MDP 的一部分）
obs, reward, terminated, truncated, info = env.step(action)
done = terminated or truncated  # 合并使用时的惯用写法
```

### 👤 关键人物

- **Mark Towers** (主要维护者) + Farama Foundation 团队, 2022
- 论文: "Gymnasium: A Standard Interface for Reinforcement Learning Environments" (arXiv, 2023)

### 📊 里程碑数据

- Gymnasium 0.26.0 (2022年9月)：首个稳定版本，引入 5 返回值 `step()`
- SB3 v1.6+ 同步支持 Gymnasium 接口
- 兼容旧 Gym 代码的 `shimmy` 包提供过渡方案

### 🔗 与 Lab 2 的关联

> Lab 2 使用的是 **Gymnasium**（新版），而非旧版 Gym。这解释了为什么你的 `step()` 返回 5 个值而不是 4 个，以及为什么掉崖后应该 `terminated=True` 而不是旧风格的 `done=True`。
