# Week 6 故事线：期中复习 — 从零到 Q-Learning 的完整旅程

> **Source:** `CST8509_06_Midterm_Review.pdf` + Weeks 1-5 Slides + Quiz 1-4 + Labs 1-2 + Assignment 1
> **核心主题：** 五周知识的因果链条——为什么每一步都是前一步的自然延伸
> **故事线：** 从"什么是RL"到"用工业级工具训练Agent"——一段完整的学习旅程

---

## 🎬 序幕：这五周我们学了什么？为什么这样学？

想象你要从零开始制造一辆自动驾驶汽车：

1. **Week 1：** 先搞清楚"自动驾驶是什么"——RL 的基本概念
2. **Week 2：** 给问题建立数学模型——MDP
3. **Week 3：** 搭建模拟器——Gymnasium 环境
4. **Week 4：** 引入工业级训练框架——Stable-Baselines3
5. **Week 5：** 使用高级算法训练——DQN + SB3 实战

这不是五个独立的话题，而是**一条因果链**：每一步都是因为前一步不够用而自然演进的。

---

## 📚 第一章：RL 基础 — 认识所有零件 (Week 1)

### 核心问题
> "什么是强化学习？它和监督学习/无监督学习有什么不同？"

### 关键概念总览

```
┌─────────────────────────────────────────────────────┐
│           RL 问题的基本骨架                            │
│                                                      │
│   Environment (环境)                                  │
│       ↓ Observation + Reward                         │
│   Agent (智能体)                                      │
│       ↓ Action                                       │
│   → 重复循环                                         │
│                                                      │
│   Agent 的三大组件：                                   │
│   ┌──────────┐ ┌──────────────┐ ┌──────────┐       │
│   │ Policy π │ │Value Fn V/Q  │ │ Model    │       │
│   │ 选动作    │ │评估好坏       │ │预测未来   │       │
│   └──────────┘ └──────────────┘ └──────────┘       │
└─────────────────────────────────────────────────────┘
```

### 必考知识点

| 概念 | 定义 | Quiz 来源 |
|------|------|-----------|
| **Agent** | 执行动作的学习者 | Q2 Q2 |
| **Environment** | Agent 交互的外部世界 | Q2 Q2 |
| **Reward** $R_t$ | 标量反馈信号 | Q2 Q2, Q2 Q5 |
| **Policy** $\pi(a \mid s)$ | 状态 → 动作的映射 | Q1 Q5, Q2 Q8 |
| **Value Function** $V(s)$ | 状态 → 期望回报 | Q1 Q6 |
| **Action Value** $Q(s,a)$ | 状态+动作 → 期望回报 | Q1 Q7 |
| **Markov Property** | 未来只依赖当前状态 | Q1 Q1-Q3, Q2 Q3 |
| **Reward Hypothesis** | 所有目标 = 最大化期望累积奖励 | Q2 Q5 |
| **Discount factor** $\gamma$ | 解决无限步回报发散问题 | Q1 Q4, Q2 Q7 |
| **Greedy Policy** | $a = \arg\max_{a'} Q(s, a')$ | Q1 Q8, Q2 Q12 |
| **Episode** | 从起始到终止的一次完整运行 | Q2 Q6 |

### Agent 分类表（必背）

| 类型 | Policy | Value Fn | Model |
|------|--------|----------|-------|
| Value Based | ❌ (隐式) | ✅ | 可选 |
| Policy Based | ✅ | ❌ | 可选 |
| Actor Critic | ✅ actor | ✅ critic | 可选 |
| Model Free | π 和/或 V/Q | | ❌ |
| Model Based | π 和/或 V/Q | | ✅ |

> 💡 **Q-Learning = Value Based + Model Free** — 本课程的核心方法

### 三大子问题

| 子问题 | 含义 | 记忆技巧 |
|--------|------|----------|
| Exploit vs Explore | 用已知最好 vs 尝试新的 | 老餐厅 vs 新餐厅 |
| Learning vs Planning | 真实经验 vs 模型模拟 | 真吃 vs 看点评 |
| Prediction vs Control | 评估策略 vs 优化策略 | "多少分" vs "最高分" |

---

## 🧮 第二章：MDP — 给问题建立数学模型 (Week 2)

### 从 Week 1 到 Week 2 的过渡
> Week 1 说了"RL 有 Agent、Environment、Reward"，但怎么用**数学语言**精确描述这个问题？→ **MDP (Markov Decision Process)**

### 核心问题
> "如何把 RL 问题形式化为数学模型？"

### MDP 五元组

$$\langle S, A, P, R, \gamma \rangle$$

| 符号 | 含义 | 说明 |
|------|------|------|
| $S$ | 状态集 (State Space) | 所有可能的状态 |
| $A$ | 动作集 (Action Space) | 所有可能的动作 |
| $P(s' \mid s, a)$ | 转移概率 (Transition Probability) | 在状态 $s$ 采取动作 $a$ 到达 $s'$ 的概率 |
| $R(s, a)$ | 奖励函数 (Reward Function) | 在状态 $s$ 采取动作 $a$ 获得的奖励 |
| $\gamma$ | 折扣因子 (Discount Factor) | $0 \le \gamma < 1$，控制未来奖励衰减 |

### Bellman 方程 — Q-Learning 的数学基础

**Bellman 方程**（Quiz 1 Q9, Quiz 2 Q11）：

$$Q(s, a) = R + \gamma \max_{a'} Q(s', a')$$

含义：一个状态-动作对的价值 = 即时奖励 + 折扣后的下一状态最大价值

**Q-Learning 更新规则**（Midterm 必考 — Slide 6）：

```python
qtable[state][action] = qtable[state][action] + alpha * (
    reward + gamma * max(qtable[next_state]) - qtable[state][action]
)
```

| 变量 | 含义 |
|------|------|
| `qtable` | Q 表，实现动作价值函数 |
| `state` | 当前状态 |
| `action` | 当前动作 |
| `alpha` | 学习率（步长），控制更新幅度 |
| `reward` | 即时奖励 |
| `gamma` | 折扣因子 |
| `next_state` | 下一状态 |

### Q-Learning vs SARSA — 深入理解

| 特性 | Q-Learning | SARSA |
|------|-----------|-------|
| 类型 | Off-policy（离策略） | On-policy（在策略） |
| 更新目标 | $\max_{a'} Q(s', a')$ | $Q(s', a')$（实际采取的 $a'$） |
| 行为 | 学习最优策略（不管当前如何探索） | 学习当前策略（包括探索） |
| CliffWalking 结果 | **最短路径**（沿悬崖边） | **安全路径**（远离悬崖） |
| 原因 | 更新用 max，忽略探索时的危险 | 更新考虑了 ε-greedy 的随机性 |

> ⚠️ **Midterm Slide 4 的讨论题：** 为什么 Q-Learning 收敛到最短路径而 SARSA 不同？
> → Q-Learning 是 off-policy，更新时用 max（假设未来总选最优），所以学到最短路径。
> → SARSA 是 on-policy，更新时考虑了实际探索行为（ε-greedy 可能走到悬崖边），所以学到更安全的路径。

### ε-Greedy 探索策略

$$
a = \begin{cases}
\arg\max_{a'} Q(s, a') & \text{with probability } 1-\epsilon \\
\text{random action} & \text{with probability } \epsilon
\end{cases}
$$

- $\epsilon$ 通常从高值（如 1.0）衰减到低值（如 0.05）
- 高 $\epsilon$ = 多探索，低 $\epsilon$ = 多利用

### Q 表初始化 — 影响收敛的关键

| 初始化方式 | 效果 | 适用场景 |
|-----------|------|----------|
| 初始化为 0 | 保守，缺乏探索动机 | 奖励全为正时 |
| 随机初始化 | 鼓励探索（乐观初始值） | 通用方法 |
| 乐观初始化 | 所有值设高 → 强制全面探索 | 确保覆盖所有状态-动作 |

> ⚠️ **Midterm Slide 4 问题：** 终止状态的 Q 值为什么必须设为 0？
> → 终止状态没有"下一步"，$Q(s_{terminal}, a) = 0$ 对所有 $a$。如果不设为 0，会导致值函数估计偏差。

---

## 🏗️ 第三章：Gymnasium — 搭建标准化模拟器 (Week 3)

### 从 Week 2 到 Week 3 的过渡
> Week 2 有了数学模型和算法，但怎么**实际运行**？我们需要一个标准化的环境来跑实验 → **Gymnasium**

### 核心问题
> "Gymnasium 是什么？如何用它创建和使用 RL 环境？"

### Gymnasium 标准定义（Midterm 必考 — Slide 7）

> **Gymnasium** is a framework for creating Reinforcement Learning environments with a standard interface such that various RL algorithms/agents can be applied to the environment in a standard way.
> 
> Gymnasium 是一个用于创建 RL 环境的框架，具有标准接口，使各种 RL 算法/智能体可以用标准方式应用于环境。

### Gymnasium 核心 API

```python
import gymnasium as gym

# 创建环境
env = gym.make("CliffWalking-v0")

# 重置环境 → 返回初始状态和信息
state, info = env.reset()

# 执行动作 → 返回 5 个值
next_state, reward, terminated, truncated, info = env.step(action)
```

**关键方法 & 返回值：**

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `env.reset()` | `(state, info)` | 重置到初始状态 |
| `env.step(action)` | `(next_state, reward, terminated, truncated, info)` | 执行一步 |
| `env.action_space` | `Space` | 动作空间（Discrete 或 Box） |
| `env.observation_space` | `Space` | 观测空间 |

### 自定义环境 (Custom Environment)

创建自定义 Gymnasium 环境需要实现：

1. `__init__()` — 定义 `action_space` 和 `observation_space`
2. `reset()` — 返回初始状态
3. `step(action)` — 执行动作，返回 (state, reward, terminated, truncated, info)
4. `render()` — 可视化（可选，常用 Pygame）

### Wrapper — 修改环境行为（Midterm 必考 — Slide 8）

> **Wrapper** = 在不修改底层代码的情况下修改现有环境
> 
> 使用方法：先初始化基础环境，然后传给 Wrapper 构造函数

```python
from gymnasium.wrappers import TimeLimit

env = gym.make("MyEnv-v0")
env = TimeLimit(env, max_episode_steps=200)  # 添加截断功能
```

---

## 🔧 第四章：Stable-Baselines3 — 工业级训练框架 (Week 4)

### 从 Week 3 到 Week 4 的过渡
> 有了标准化环境，但自己写 Q-Learning 太低效了。有没有**开箱即用的高性能算法库**？→ **Stable-Baselines3 (SB3)**

### 核心问题
> "SB3 是什么？为什么要用它？"

### SB3 标准定义（Midterm 必考 — Slide 9）

> **Stable-baselines3** is a set of reliable Reinforcement Learning algorithm implementations.
> 
> Stable-baselines3 是一套**可靠的**强化学习算法实现。

关键特性：
- **Vectorized environments** — 同时运行多个环境副本 → 加速训练
- **Callbacks** — 自定义代码（监控、自动保存、模型操作、进度条）

### SB3 基本用法

```python
from stable_baselines3 import DQN

# 创建模型
model = DQN("MlpPolicy", env, verbose=1)

# 训练
model.learn(total_timesteps=10000)

# 测试
obs, info = env.reset()
action, _states = model.predict(obs, deterministic=True)
```

---

## 🧠 第五章：DQN — 深度 Q 网络 (Week 5)

### 从 Week 4 到 Week 5 的过渡
> 表格式 Q-Learning 只能处理**有限**的状态-动作空间。真实问题（如 Atari 游戏、机器人控制）状态空间巨大怎么办？→ 用**神经网络替代 Q 表** → **DQN**

### 核心问题
> "当状态空间太大无法建表时，如何做 Q-Learning？"

### 从 Q-Table 到 DQN 的演进

```
Q-Table:       状态+动作 → 查表 → Q值
    ↓ 状态太多，表太大
DQN:           状态 → 神经网络 → 所有动作的 Q值
```

| 特性 | Tabular Q-Learning | DQN |
|------|-------------------|-----|
| Q值存储 | 表格 | 神经网络 |
| 状态空间 | 有限、已知 | 可以连续/巨大 |
| 前提条件 | 完整的 $S$ 和 $A$ 已知（Quiz 2 Q13） | 只需 $A$ 已知 |
| 泛化能力 | ❌ 无 | ✅ 可泛化到未见状态 |

### 在 SB3 中使用 DQN

```python
from stable_baselines3 import DQN

model = DQN(
    "MlpPolicy",         # 多层感知机策略
    env,
    learning_rate=1e-3,   # 学习率
    buffer_size=50000,    # 经验回放缓冲区
    learning_starts=1000, # 开始学习前的步数
    verbose=1
)
model.learn(total_timesteps=100000)
```

---

## 🗺️ 全局路线图：五周知识的因果链条

```
┌──────────────────────────────────────────────────────────────┐
│                    RL 学习路线图 (Weeks 1-5)                   │
│                                                               │
│  Week 1: 概念                                                 │
│  ✅ Agent / Environment / Reward                              │
│  ✅ Policy / Value Function / Model                           │
│  ✅ Markov Property                                           │
│  ✅ Agent 分类 (Value/Policy/Actor-Critic, Model Free/Based)   │
│         │                                                     │
│         ▼ "概念有了,怎么用数学描述?"                              │
│  Week 2: 数学模型                                              │
│  ✅ MDP ⟨S, A, P, R, γ⟩                                       │
│  ✅ Bellman 方程: Q(s,a) = R + γ max Q(s',a')                 │
│  ✅ Q-Learning 更新规则                                        │
│  ✅ ε-Greedy / Q-table 初始化                                  │
│         │                                                     │
│         ▼ "有了算法,在哪跑?"                                    │
│  Week 3: 标准化环境                                            │
│  ✅ Gymnasium API (reset/step/render)                          │
│  ✅ Custom Environment                                         │
│  ✅ Wrapper                                                    │
│  ✅ Pygame rendering                                           │
│         │                                                     │
│         ▼ "自己写算法太慢,有现成的吗?"                            │
│  Week 4: 工业级框架                                            │
│  ✅ Stable-Baselines3                                          │
│  ✅ Vectorized Environments                                    │
│  ✅ Callbacks                                                  │
│         │                                                     │
│         ▼ "Q-table 状态太多放不下,怎么办?"                       │
│  Week 5: 深度 RL                                              │
│  ✅ DQN (用神经网络替代 Q 表)                                   │
│  ✅ SB3 + DQN 实战                                             │
│         │                                                     │
│         ▼                                                     │
│  Week 6: 期中考试 📝                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## ⚠️ 重点提醒：Antonin Raffin 最佳实践 (Quiz 4)

| 话题 | 关键建议 |
|------|----------|
| RL 为什么难？ | 超参敏感 + 采样低效 + Agent自采集数据 + 奖励设计难 |
| Reward Hacking | 最大化奖励但没学到期望行为 |
| 最佳实践 | 用推荐超参、不依赖旧算法、记录所有参数、多次运行做定量评估 |
| 开始前先问 | 真的需要 RL 吗？安全/稳定性有保证吗？ |
| 定义自定义任务 | 观测空间 + 奖励函数 + 终止条件 + 动作空间 |
| 观测空间 | 归一化 + 信息足够 + 不违反 Markov 假设 |
| 动作空间 | 确定离散/连续 + 连续必须归一化 + 权衡复杂度/性能 |
| 奖励函数 | 从简单开始 + 注意 reward hacking + 主/次奖励 + 稀疏/塑形 |
| 选算法 | 考虑动作类型（连续 vs 离散） |
| 不工作怎么办 | 增加训练时间 + 可信实现 + 检查最佳实践 + 先简化再复杂化 |

---

## 🎓 考试/复习重点检查清单

### ✍️ 必须能写的

- [ ] **画 Agent-Environment 交互图**（Slide 5）
- [ ] **写 Q-Learning 更新公式** + 每个变量含义（Slide 6）
- [ ] 定义 Gymnasium（Slide 7）
- [ ] 定义 Gymnasium Wrapper（Slide 8）
- [ ] 定义 Stable-Baselines3 + 两个关键特性（Slide 9）

### 🧠 必须能回答的

- [ ] RL 与监督/无监督学习的区别
- [ ] 马尔可夫性质的定义和含义
- [ ] Policy 的两种形式（确定性 vs 随机性）
- [ ] $V(s)$ vs $Q(s,a)$ 的区别
- [ ] Bellman 方程含义
- [ ] Greedy 策略定义
- [ ] $\gamma$ 的作用（解决无限回报发散）
- [ ] Episode 的定义
- [ ] Q-Learning 为什么收敛到最短路径
- [ ] Q-Learning vs SARSA 的区别
- [ ] Q 表初始化对收敛的影响
- [ ] 终止状态 Q 值为什么设为 0
- [ ] TD (Temporal Difference) ≠ Temporal Distance（Quiz 2 Q14 陷阱）

### 📊 必须能对比的

- [ ] Q-Learning vs SARSA（on-policy vs off-policy）
- [ ] Tabular Q-Learning vs DQN（表格 vs 神经网络）
- [ ] Value Based vs Policy Based vs Actor Critic
- [ ] Model Free vs Model Based
- [ ] Exploit vs Explore
