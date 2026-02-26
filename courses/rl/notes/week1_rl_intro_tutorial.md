# Week 1 教程：强化学习基础概念深入

> **数学前置：** [条件概率](../../math/probability/conditional_probability.md) | [马尔可夫链与MDP](../../math/probability/markov_chains.md) | [几何级数与折扣回报](../../math/calculus/geometric_series.md) | [Argmax](../../math/general/argmax.md)
> **教科书来源：** Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.), Chapter 1

本教程补充 Slides 未深入讲解的内容，基于 Sutton & Barto 教科书 Chapter 1。

---

## §0 前置知识：本教程用到的核心概念

本教程不涉及复杂数学推导。需要的前置概念：

| 概念 | 含义 | 在本教程中的作用 |
|------|------|-----------------|
| 概率 $P(A)$ | 事件 A 发生的可能性 | 定义随机策略、状态转移 |
| 条件概率 $P(A \mid B)$ | 已知 B 发生时 A 的概率 | 定义策略 $\pi(a \mid s)$ |
| 期望 $\mathbb{E}[X]$ | 随机变量的加权平均值 | 定义价值函数 |

**贯穿例子：** 井字棋（Tic-Tac-Toe）——Sutton 教科书 §1.5 的经典例子。两个玩家轮流在 3×3 棋盘上放 X 或 O，先连成三个的赢。我们将用这个例子来具体化所有抽象概念。

---

## §1 RL 的本质：试错学习与延迟奖励

> 📚 Ref: Sutton §1.1, p.1-3

### 1.1 Slides 没讲什么？

Slides 给出了 RL 的定义（"第三种机器学习"），但没有深入解释 RL 的**两个核心特征**。Sutton 在 §1.1 明确指出：

> ⚠️ **Slides 未强调：** RL 的两个最重要的区分特征是 **trial-and-error search（试错搜索）** 和 **delayed reward（延迟奖励）**。
> — 📚 Sutton §1.1, p.1

**试错搜索（Trial-and-error search）：** agent 不被告知该采取哪个动作，必须通过尝试来发现哪些动作能产生最多奖励。这与监督学习根本不同——监督学习有"正确答案"标签，RL 没有。

**延迟奖励（Delayed reward）：** 当前动作不仅影响即时奖励，还影响下一个状态，进而影响所有后续奖励。这意味着 agent 不能只看眼前，必须考虑长远。

**井字棋例子：** 你下了一步棋（动作），对手回应（环境转移），几步之后才知道赢没赢（延迟奖励）。你不能只看这一步好不好，要看它对整盘棋的影响。

### 1.2 RL 是问题、方法、还是领域？

> ⚠️ **Slides 未强调：** Sutton 特别指出 "reinforcement learning" 同时指三件事：(1) 一个问题，(2) 一类解决方法，(3) 研究这个问题和方法的领域。混淆这三者是许多困惑的来源。
> — 📚 Sutton §1.1, p.2

这个区分很重要：当我们说"Q-Learning 是一种 RL 方法"时，我们说的是 (2)；当我们说"Cliff Walking 是一个 RL 问题"时，我们说的是 (1)。

---

## §2 RL 与监督学习、无监督学习的本质区别

> 📚 Ref: Sutton §1.1, p.2-3

Slides 只说 RL 是"第三种类型"，但没有解释**为什么**它不能归入前两种。Sutton 给出了清晰的论证：

### 2.1 为什么 RL ≠ 监督学习？

监督学习需要一个"知识渊博的外部监督者"提供标记样本。但在交互式问题中：
- 获取"正确行为"的样本通常不切实际
- 在未知领域（uncharted territory），agent 必须从自己的经验中学习
- 没有人能告诉你每个状态下的"正确动作"是什么

**井字棋例子：** 没有人给你一本"每种棋局该怎么下"的手册。你只能通过不断下棋、赢了或输了来学习。

### 2.2 为什么 RL ≠ 无监督学习？

虽然 RL 不依赖标记数据（像无监督学习），但：
- 无监督学习的目标是**发现隐藏结构**（如聚类）
- RL 的目标是**最大化奖励信号**
- 发现结构可能对 RL 有用，但它本身不解决 RL 问题

> 📚 Sutton §1.1, p.2: "We therefore consider reinforcement learning to be a third machine learning paradigm, alongside supervised learning and unsupervised learning."

---

## §3 RL 的四大子元素：教科书的精确定义

> 📚 Ref: Sutton §1.3, p.6

Slides 列出了 Policy、Value Function、Model 三个组件。但 Sutton 的分类是**四个子元素**，而且给出了更精确的定义和更深的洞察。

### 3.1 策略（Policy）

**教科书定义：** "A policy defines the learning agent's way of behaving at a given time. Roughly speaking, a policy is a mapping from perceived states of the environment to actions to be taken when in those states." — 📚 Sutton §1.3, p.6

> ⚠️ **Slides 未强调：** Sutton 指出策略可以是简单的查找表，也可以涉及大量计算（如搜索过程）。策略是 RL agent 的核心——**仅凭策略就足以决定行为**。

**井字棋例子：** 策略就是"看到这个棋局，我下哪里"的规则。可以是一张表（每种棋局对应一个落子位置），也可以是一个复杂的搜索算法。

### 3.2 奖励信号（Reward Signal）

**教科书定义：** "A reward signal defines the goal of a reinforcement learning problem. On each time step, the environment sends to the reinforcement learning agent a single number called the reward." — 📚 Sutton §1.3, p.6

> ⚠️ **Slides 未强调：** Sutton 用生物学类比——奖励类似于**快乐或痛苦**的体验。奖励信号是改变策略的**主要依据**：如果策略选择的动作导致低奖励，策略可能会被修改。

**井字棋例子：** 赢了 = +1，输了 = -1，平局 = 0。这个简单的信号驱动了整个学习过程。

### 3.3 价值函数（Value Function）

**教科书定义：** "The value of a state is the total amount of reward an agent can expect to accumulate over the future, starting from that state." — 📚 Sutton §1.3, p.6

这是 Sutton 最重要的洞察之一：

> ⚠️ **Slides 未强调：** **奖励 vs 价值的本质区别**——
> - 奖励是**即时的、内在的**（环境直接给的）
> - 价值是**长期的、预测性的**（需要估计的）
> - 一个状态可能即时奖励低，但价值高（因为后续状态奖励高）
> - 反之亦然
> — 📚 Sutton §1.3, p.6

**Sutton 的人类类比：** 奖励像快乐（高）和痛苦（低），价值对应更精细、更有远见的判断——"我们对环境处于某个状态有多满意或不满意"。

**关键结论：** 我们做决策时基于**价值判断**，而不是奖励判断。我们寻找能带来**最高价值**状态的动作，而不是最高即时奖励的动作——因为这些动作在长期内能获得最多奖励。

**井字棋例子：** 某一步棋可能不直接得分（即时奖励 = 0），但它把你放在了一个很可能赢的位置（高价值）。

### 3.4 模型（Model）

Slides 已经覆盖了模型的基本定义。Sutton 补充的关键点：

> ⚠️ **Slides 未强调：** 模型用于**规划（planning）**——在实际经历之前，通过考虑可能的未来情况来决定行动。这是 **model-based** 方法的核心。没有模型的方法（**model-free**）则是纯粹的试错学习者。
> — 📚 Sutton §1.3, p.7

---

## §4 探索与利用的困境：RL 独有的挑战

> 📚 Ref: Sutton §1.1, p.3

Slides 用餐厅例子简单提到了 exploitation vs exploration。Sutton 给出了更深入的分析：

> ⚠️ **Slides 未强调：** 探索-利用困境是 RL **独有的**挑战——在监督学习和无监督学习中根本不存在这个问题。
> — 📚 Sutton §1.1, p.3

**为什么这是个困境？**
- 纯利用（只选已知最好的）→ 可能错过更好的选择
- 纯探索（只尝试新的）→ 浪费时间在差的选择上
- 两者都不能单独追求，必须平衡

**在随机任务中：** 每个动作必须被尝试**多次**才能获得其期望奖励的可靠估计。

**井字棋例子：** 你发现了一个不错的开局策略（利用），但如果你从不尝试其他开局（探索），你可能永远不知道有更好的策略存在。

> 📚 Sutton §1.1, p.3: "The exploration–exploitation dilemma has been intensively studied by mathematicians for many decades, yet remains unresolved."

---

## §5 RL 的整体视角：完整的、交互的、目标导向的 Agent

> 📚 Ref: Sutton §1.1, p.3

这是 Sutton 强调但 Slides 完全没提到的一个重要观点：

> ⚠️ **Slides 未覆盖：** RL 与其他方法的关键区别在于它**显式地考虑了一个目标导向的 agent 与不确定环境交互的完整问题**。许多其他方法只研究子问题（如监督学习研究预测，规划研究决策），而不考虑它们如何融入更大的图景。
> — 📚 Sutton §1.1, p.3

这意味着：
- RL agent 有**明确的目标**
- 能**感知**环境的某些方面
- 能**选择动作**来影响环境
- 必须在**对环境有显著不确定性**的情况下运作

---

## 参考索引表

| 教程章节 | 教科书来源 | 核心内容 | Slides 覆盖？ |
|---------|-----------|---------|--------------|
| §1 RL 的本质 | Sutton §1.1, p.1 | 试错搜索 + 延迟奖励 | ⚠️ 部分（只提到了 RL 定义，未强调两个核心特征） |
| §1 问题/方法/领域 | Sutton §1.1, p.2 | RL 同时指三件事 | ❌ 未覆盖 |
| §2 RL vs SL vs UL | Sutton §1.1, p.2-3 | 为什么是第三种范式 | ⚠️ 部分（只说了"第三种"，未解释为什么） |
| §3 四大子元素 | Sutton §1.3, p.6 | Policy, Reward, Value, Model 精确定义 | ⚠️ 部分（有定义但缺少教科书的深度洞察） |
| §3 奖励 vs 价值 | Sutton §1.3, p.6 | 即时 vs 长期，快乐 vs 远见 | ⚠️ 部分（提到了但未用 Sutton 的类比） |
| §4 探索-利用困境 | Sutton §1.1, p.3 | RL 独有的挑战 | ⚠️ 部分（有餐厅例子但未说明是 RL 独有的） |
| §5 整体视角 | Sutton §1.1, p.3 | 完整交互目标导向 agent | ❌ 未覆盖 |
