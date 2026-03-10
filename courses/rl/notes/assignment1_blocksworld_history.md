# 🕰️ Assignment 1 Blocks World — 技术演进历史线

> **课程:** CST8509 Reinforcement Learning | **主题:** Blocks World + Q-Learning + DQN/PPO
> **时间跨度:** 1959 — 2021
> **核心脉络:** AI 规划问题 → 逻辑推理 → 无模型学习 → 深度强化学习 → 开源标准化
> **Source:** Sutton §1.7 (Early History of RL) + David Silver L1 + Assignment 文档 + 课程 Slides

---

## 📍 全景时间线（Timeline Overview）

```
1959         1969         1972        1989         2013         2015         2016         2017         2021
  │            │            │           │            │            │            │            │            │
  ▼            ▼            ▼           ▼            ▼            ▼            ▼            ▼            ▼
Samuel       Blocks      Prolog     Watkins      DeepMind     DQN         OpenAI       Schulman     Gymnasium
Checkers     World       语言       Q-Learning   Atari DQN    Nature      Gym          PPO          + SB3
                         诞生       论文                       论文        发布         论文         Farama
  │            │            │           │            │            │            │            │            │
  └──── AI 游戏──┘           │           └──── RL 算法 ─┘            └──── 工具框架 ─┘            │
                 └── 逻辑推理 ┘                                                                  │
                                                                                     ← 我们在这 ──┘
```

---

## 第 1 站：Samuel's Checkers (1959)

### 🧩 之前的问题

1950 年代，AI 还在"人工编写规则"阶段。每个游戏都需要人类专家手动设计策略。**问题：** 能不能让机器自己从经验中学习？

### 💡 核心创新

Arthur Samuel 开发了**西洋跳棋（Checkers）程序**——世界上第一个通过自我对弈学习改进策略的程序。他创造了 "Machine Learning" 这个术语。

核心方法：用状态评估函数（类似 V(s)）打分，通过不断对弈调整评分权重。

### 👤 关键人物

- **Arthur Samuel** — IBM Research, 1959
- 论文: "Some Studies in Machine Learning Using the Game of Checkers" (1959)
- 命名来源: 他创造了 **"Machine Learning"** 一词

### 📊 里程碑数据

- 程序击败了 Connecticut 州跳棋冠军 Robert Nealey (1962)
- 这是 AI 历史上**第一次机器在棋类游戏中击败人类高手**

### ⚠️ 遗留问题

Samuel 的方法是**特定于跳棋的**——评估函数是人工设计的，只能用于跳棋。不同游戏需要不同的评估函数。**需要更通用的问题建模方法。**

### 🔗 与本课程的关联

> 📚 Sutton §1.7 (p.35-44): Samuel 是 RL 的先驱之一
> 📚 Quiz 2 Q1: RL 是机器学习三大范式之一 — Samuel 正是 ML 这个概念的提出者

---

## 第 2 站：Blocks World 问题 (1969-1972)

### 🧩 之前的问题

Samuel 证明了机器可以学习，但他的方法**依赖于人为设计的评估函数**。AI 研究者开始思考一个更基本的问题：**如何让 AI 理解"规划"——从当前状态到目标状态的步骤序列？**

### 💡 核心创新

**Blocks World** 成为 AI 规划与推理的标准测试环境：

- **SHRDLU (1971)** — Terry Winograd（MIT）开发，用自然语言与积木世界交互
- 积木世界将复杂的规划问题简化为：**有限积木 + 有限位置 + 有限动作 + 前置条件**
- 引入了**情境演算（Situation Calculus）**来形式化描述"动作如何改变世界"

> 为什么 3 块积木就够了？因为 3 块积木已经产生了 ~13 个合法状态和 ~N 个动作——足够展示规划的核心挑战，又不会太复杂。

### 👤 关键人物

- **Terry Winograd** — MIT, 1971 — SHRDLU 系统
- **John McCarthy** — Stanford — 情境演算（Situation Calculus, 1963）
- **Nils Nilsson** — Stanford/SRI — STRIPS 规划系统 (1971)

### 📊 里程碑数据

- SHRDLU 能用自然语言理解 "Put the red block on top of the blue block"
- Blocks World 至今仍是 AI 规划课程的标准教学案例

### ⚠️ 遗留问题

经典 AI 的规划方法需要**完美的世界模型**——知道所有状态、所有动作、所有转移规则。在真实世界中，这些信息往往不完整或不可获得。**需要一种能在不完全信息下学习的方法。**

### 🔗 与本课程的关联

> **Assignment 1 直接使用 Blocks World！** `blocks_world.pl` 用 Prolog 情境演算实现。我们的 3-block 版本正是 Winograd 时代定义的经典设置。
> 📚 Assignment §Prolog Blocks World: "Ensure you can run the provided Prolog model of the Blocks World"

---

## 第 3 站：Prolog 语言 (1972)

### 🧩 之前的问题

情境演算等形式化方法定义了规划的**数学框架**，但缺乏实际可执行的**编程语言**来直接表达这些逻辑规则。用 FORTRAN 或 C 编写逻辑推理非常痛苦。

### 💡 核心创新

**Prolog (Programming in Logic)** — 第一个实用的逻辑编程语言：

- **声明式编程：** 你描述"什么是真的"（规则），Prolog 自动推导答案
- **回溯搜索：** 自动尝试所有可能的变量绑定
- **统一（Unification）：** 自动匹配模式

```prolog
% 声明式: 描述"什么条件下可以搬积木"
can_move(Block, From, To) :- clear(Block), clear(To), on(Block, From).

% Prolog 自动回答: "现在能搬什么？"
?- can_move(X, Y, Z).
```

### 👤 关键人物

- **Alain Colmerauer** — Université de Marseille, France, 1972
- **Robert Kowalski** — Edinburgh, UK — 逻辑编程理论基础
- 命名来源: **Pro**grammation en **Log**ique（法语"逻辑编程"）

### 📊 里程碑数据

- 1980s 日本"第五代计算机计划"选择 Prolog 作为核心语言
- SWI-Prolog（我们使用的版本）至今仍在积极维护（最新 v8.x）

### ⚠️ 遗留问题

Prolog 擅长**逻辑推理**，但不擅长**从经验中学习**。它需要人类预先定义所有规则。**如果规则未知或太复杂怎么办？**

### 🔗 与本课程的关联

> **Assignment 1 使用 SWI-Prolog + swiplserver！**
>
> - `blocks_world.pl` 用 Prolog 定义积木世界的所有规则
> - Python 通过 `swiplserver` 与 Prolog 通信
> - Prolog 负责"游戏规则"，Python 负责"学习策略"
>   📚 Assignment §4b: `from swiplserver import PrologMQI, PrologThread`

---

## 第 4 站：Q-Learning (1989)

### 🧩 之前的问题

经典 AI 规划（如 Prolog）需要**完整的世界模型**。但在很多场景中，Agent 不知道环境的转移概率 $P(s'|s,a)$——它只能通过**试错**来学习。**需要一种不需要模型就能学到最优策略的方法。**

### 💡 核心创新

Chris Watkins 提出 **Q-Learning** — 第一个证明收敛的 **model-free, off-policy** TD 控制算法：

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_{a'} Q(S', a') - Q(S, A) \right]$$

关键突破：

- **Model-free：** 不需要知道 $P(s'|s,a)$，只需要与环境交互
- **Off-policy：** 行为策略（ε-greedy）和学习策略（greedy）可以不同（📚 Week 2 MDP 故事线 §2）
- **收敛保证：** 在一定条件下保证收敛到最优 Q 值（Watkins & Dayan 1992 证明）

### 👤 关键人物

- **Christopher Watkins** — Cambridge University, 1989
- 博士论文: "Learning from Delayed Rewards" (1989)
- **Peter Dayan** (合作者) — 1992 年与 Watkins 共同证明收敛性
- 命名来源: **Q** = Quality of an action（动作的"质量"）

> 📚 Sutton §6.5 (p.153): "Q-learning... is one of the early breakthroughs in reinforcement learning"

### 📊 里程碑数据

- Q-Learning 是**第一个**被证明在一定条件下收敛的 off-policy 控制算法
- 简单、直观、易于实现，至今仍是 **RL 教学的第一个算法**
- Q-Table 大小 = $|S| \times |A|$（📚 Quiz W3 S2）

### ⚠️ 遗留问题

Q-Learning 使用 **Q-Table** 存储所有状态-动作对的价值。当状态空间很大时（如 Atari 游戏画面），表格方法**完全不可行** — 内存爆炸且无法泛化到未见过的状态。**需要一种能处理大状态空间的方法。**

> 📚 Week 5 DQN 故事线 §1.2: "Q-Table 在大状态空间下彻底失效"

### 🔗 与本课程的关联

> **Assignment 1 Phase 2: Q-Learning 是主要算法！**
>
> - 从 Lab 2 移植 Q-Learning 代码并适配 BlocksWorld
> - 13 个状态（v0）/ 169 个状态（v1）— Q-Table 完全可行
> - 需要记录训练曲线 + 超参数实验（至少 4 张截图）
>   📚 Quiz 2 Q13: Q-Learning 需要完整的状态集和动作集
>   📚 Quiz 2 Q14: Q-Learning 是 Temporal **Difference** (不是 Distance!) 学习

---

## 第 5 站：DQN — Deep Q-Network (2013/2015)

### 🧩 之前的问题

Q-Table 在大状态空间下失效（📚 Week 5 DQN 故事线 §1）。Atari 游戏的一帧画面 = 210×160×3 像素 → 状态空间约 $256^{100800}$ → 不可能建表。**需要用函数逼近替代表格。**

### 💡 核心创新

DeepMind 用**深度神经网络替代 Q-Table**，加上两个关键技巧稳定训练：

| 组件                  | 作用                           | 解决什么问题                       |
| --------------------- | ------------------------------ | ---------------------------------- |
| **Q-Network**         | 输入状态 → 输出每个动作的 Q 值 | 替代 Q-Table, 可泛化               |
| **Target Network**    | 冻结的 Q-Network 副本          | 防止"追自己尾巴"（📚 Week 5 §2.4） |
| **Experience Replay** | 随机采样历史经验               | 打破样本相关性（📚 Week 5 §2.5）   |

### 👤 关键人物

- **Volodymyr Mnih** (第一作者) + **DeepMind** 团队 (Kavukcuoglu, Silver, Graves, Antonoglou, Hassabis 等)
- NIPS Workshop 论文: "Playing Atari with Deep Reinforcement Learning" (2013)
- Nature 论文: "Human-level control through deep reinforcement learning" (2015)
- **David Silver** — DeepMind 首席研究员，也是我们课程教材 (David Silver RL lectures) 的作者

### 📊 里程碑数据

- 在 49 款 Atari 游戏中，29 款超越人类水平
- **同一个算法 + 同一组超参数**处理所有 49 款游戏 — 通用性的突破
- 2014 年 Google 以 ~5 亿美元收购 DeepMind

### ⚠️ 遗留问题

DQN **只支持离散动作空间**（📚 Quiz W3 Q8: DQN only Discrete）。不能用于连续动作（如机器人关节控制）。而且 off-policy 方法在某些场景下不够稳定。**需要能处理连续动作且更稳定的算法。**

### 🔗 与本课程的关联

> **Assignment 1 Phase 4: 使用 SB3 的 DQN 算法**
>
> - `DQN("MlpPolicy", env)` — 验证 DQN 在 BlocksWorld 上能跑
> - 预期效果不如 Q-Learning（状态空间太小，DQN 大材小用）
>   📚 Week 5 DQN 故事线: 完整覆盖 DQN 的四大组件和训练流程
>   📚 Assignment: "We want to get the algorithms running, but we WILL NOT see better results than q-learning"

---

## 第 6 站：PPO — Proximal Policy Optimization (2017)

### 🧩 之前的问题

DQN 是 value-based 方法，**只能处理离散动作**。Policy Gradient 方法可以处理连续动作，但**训练不稳定** — 更新步长太大会导致策略崩溃，太小又学得慢。**需要一种既能处理连续动作又稳定的方法。**

### 💡 核心创新

John Schulman 提出 **PPO** — 一种简单、通用、稳定的 policy gradient 方法：

- 通过**裁剪比率（clip ratio）**限制策略更新幅度 → 防止策略崩溃
- 不需要 Trust Region 的约束优化（比 TRPO 简单得多）
- 既支持离散动作又支持连续动作

### 👤 关键人物

- **John Schulman** — OpenAI, 2017
- 论文: "Proximal Policy Optimization Algorithms" (2017)
- 命名来源: **Proximal** = "近端的" — 限制策略更新不要离当前策略太远

### 📊 里程碑数据

- PPO 成为 OpenAI 的**默认 RL 算法**
- 用于训练 OpenAI Five（Dota 2 AI, 2018）和 ChatGPT (RLHF)
- 简单到"几乎每个 RL 入门者都会用"

### ⚠️ 遗留问题

PPO 是 on-policy 算法 — **样本效率低**（需要大量交互数据）。在数据收集成本高的场景（如真实机器人）中，这是一个显著的限制。

### 🔗 与本课程的关联

> **Assignment 1 Phase 4: 使用 SB3 的 PPO 算法**
>
> - `PPO("MlpPolicy", env)` — 验证 PPO 在 BlocksWorld 上能跑
> - PPO 是 on-policy（📚 Week 2 §2: 类似 SARSA 而非 Q-Learning）
>   📚 Quiz W3 Q8: PPO 支持 Discrete + Continuous 动作空间
>   📚 Quiz 4 Q9: "Consider your actions and whether the algorithm is designed for continuous or discrete"

---

## 第 7 站：OpenAI Gym → Gymnasium + Stable-Baselines3 (2016-2021)

### 🧩 之前的问题

RL 算法越来越多（Q-Learning, DQN, PPO, A2C, SAC...），每个研究者都自己实现环境接口 — **代码不兼容、实验不可复现**。环境和算法之间没有标准接口。

### 💡 核心创新

**三层标准化**解决了整个 RL 工具链的问题：

| 工具                  | 年份 | 作用                               | 解决什么       |
| --------------------- | ---- | ---------------------------------- | -------------- |
| **OpenAI Gym**        | 2016 | 标准环境 API (`reset/step/render`) | 环境接口不统一 |
| **Gymnasium**         | 2021 | Gym 的继任者 (Farama Foundation)   | Gym 维护停滞   |
| **Stable-Baselines3** | 2020 | 标准算法库 (`DQN/PPO/A2C`)         | 算法实现不统一 |

Gymnasium 的关键改进（相对于 Gym）：

- `reset()` 新增 `seed` 参数 → 可复现
- `step()` 返回 5 个值（新增 `truncated`）→ 区分自然终止和超时截断
- `import gymnasium as gym` 替代 `import gym`

### 👤 关键人物

- **Greg Brockman, John Schulman** (OpenAI) — Gym, 2016
- **Farama Foundation** — Gymnasium, 2021（从 OpenAI 接管维护）
- **Antonin Raffin** — DLR (German Aerospace) — Stable-Baselines3 主要作者

> 📚 Quiz 4 全部 10 题都来自 Antonin Raffin 的讲座！

### 📊 里程碑数据

- OpenAI Gym 被引用超过 10,000 次
- SB3 GitHub Stars > 8,000，成为最流行的 RL 算法库
- 几乎所有 RL 研究论文都使用 Gym/Gymnasium 作为实验环境

### ⚠️ 遗留问题

标准化解决了接口问题，但 **RL 本身仍然困难**：

- 超参数敏感（📚 Quiz 4 Q1）
- 样本效率低（📚 Quiz 4 Q1）
- 奖励设计困难（📚 Quiz 4 Q2: reward hacking）

### 🔗 与本课程的关联

> **Assignment 1 的核心框架！**
>
> - 环境用 Gymnasium 标准 API (`gym.Env` 子类)
> - 算法用 SB3 (`DQN`, `PPO`)
> - 安装: `pip install gymnasium stable-baselines3`
> - 打包: `pip install -e .`
>   📚 Quiz W3 Q1: Gymnasium 是 OpenAI Gym 的继任者
>   📚 Week 3 Gymnasium 教程: 环境创建完整流程
>   📚 Quiz 4 Q3: 保存所有实验参数 — SB3 的 TensorBoard 日志

---

## 📊 对比总结表

| 站  | 技术            | 年份 | 核心贡献               | 局限性           | Assignment 用途 |
| --- | --------------- | ---- | ---------------------- | ---------------- | --------------- |
| 1   | Samuel Checkers | 1959 | 第一个自我学习程序     | 特定于跳棋       | 历史背景        |
| 2   | Blocks World    | 1969 | AI 规划标准问题        | 需要完美模型     | **环境定义**    |
| 3   | Prolog          | 1972 | 逻辑编程语言           | 不能从经验学习   | **环境后端**    |
| 4   | Q-Learning      | 1989 | Model-free 最优控制    | Q-Table 大小受限 | **主要算法**    |
| 5   | DQN             | 2013 | 神经网络替代 Q-Table   | 只支持离散动作   | **SB3 算法 1**  |
| 6   | PPO             | 2017 | 稳定的 Policy Gradient | 样本效率低       | **SB3 算法 2**  |
| 7   | Gym/SB3         | 2016 | 标准化工具链           | RL 本身仍困难    | **开发框架**    |

---

## 🎯 考试相关知识点（历史线版）

- [ ] 知道 Q-Learning 由 **Watkins (1989)** 提出，Q = Quality
- [ ] 知道 DQN 由 **DeepMind (2013/2015)** 提出，用神经网络替代 Q-Table
- [ ] 知道 PPO 由 **Schulman/OpenAI (2017)** 提出，是 policy gradient 方法
- [ ] 知道 Gymnasium 是 **OpenAI Gym 的继任者**（Quiz W3 Q1），Farama Foundation 维护
- [ ] 知道 SB3 的主要贡献者是 **Antonin Raffin**（Quiz 4 的内容来源）
- [ ] 能解释 Q-Learning → DQN 的技术动因：**大状态空间下 Q-Table 失效**
- [ ] 能解释 DQN → PPO 的技术动因：**DQN 不支持连续动作空间**
- [ ] 知道 Q-Learning 是 **off-policy**，SARSA 是 **on-policy**（Quiz 2 + Week 2）
- [ ] 知道 "Machine Learning" 一词由 **Arthur Samuel (1959)** 提出
- [ ] 知道 Blocks World 是 **1960s-70s 经典 AI 规划问题**
