# Week 2: MDP — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week2_mdp_slides.md) | [数学公式](week2_mdp_math.md)

---

## 时间轴概览

```
1906          1950s          1957            1960            1989            1998
  │              │              │               │               │               │
  ▼              ▼              ▼               ▼               ▼               ▼
Markov        Shannon       Bellman          Howard         Watkins          Sutton
链式随机      信息论        贝尔曼方程       策略迭代       Q-Learning       RLAI 教科书
过程          (决策理论)    (DP 框架)        算法           博士论文         系统化 RL
```

---

## Station 1: 马尔可夫链的提出（1906）

**问题：** 俄国文学中的元音/辅音分布能否用数学建模？自然过程的"无记忆性"如何描述？

**创新：** Andrey Markov（安德烈·马尔可夫）提出**马尔可夫链**——系统下一状态只依赖当前状态，与过去历史无关。

$$P(S_{t+1} \mid S_t, S_{t-1}, \ldots, S_0) = P(S_{t+1} \mid S_t)$$

**关键人物：**
- Andrey Markov（1856-1922）— 俄国数学家，研究俄语诗歌中字母序列

**历史意义：** 这个看似简单的"无记忆性"假设，成为了整个现代 RL 的数学基础。

**遗留问题：** 原始马尔可夫链中没有"奖励"和"决策者"，只是描述随机转移过程。

**课程联系：** RL 的核心假设——Markov Property——直接来自这里。

---

## Station 2: 贝尔曼方程与动态规划（1957）

**问题：** 在多阶段决策（今天的选择影响未来）中，如何数学化地找到最优策略？

**创新：** Richard Bellman 提出**动态规划 (Dynamic Programming)** 和**最优性原理**：

> "最优策略的子策略也必须是最优的。"

贝尔曼方程（状态价值版本）：

$$V^*(s) = \max_a \left[ R(s, a) + \gamma \sum_{s'} P(s' | s, a) V^*(s') \right]$$

**关键人物：**
- Richard Bellman（1920-1984）— 兰德公司研究员，"optimization under uncertainty"

**遗留问题：** DP 需要知道完整的状态转移概率 $P(s' | s, a)$。真实环境中这通常未知。

**课程联系：** Q-Learning 的更新公式正是贝尔曼方程的**无模型采样版本**，用观测到的 $r$ 和 $s'$ 代替期望。

---

## Station 3: 马尔可夫决策过程形式化（1960）

**问题：** 如何将"带奖励的决策问题"整合为统一的数学框架？

**创新：** Ronald Howard 在 *Dynamic Programming and Markov Processes* 中正式定义了 **MDP (Markov Decision Process)** 的元组：

$$\text{MDP} = (S, A, P, R, \gamma)$$

- $S$：状态空间
- $A$：动作空间  
- $P(s' | s, a)$：转移概率
- $R(s, a)$：奖励函数
- $\gamma$：折扣因子

**关键人物：**
- Ronald Howard — MDP 形式化体系的建立者
- 同期：Shapley（1953）提出随机博弈，是 MDP 的前身

**遗留问题：** MDP 框架假设模型已知（$P$ 和 $R$ 已知），即"规划"问题，而非学习。

**课程联系：** Week 2 全篇的数学语言（$S, A, P, R, \gamma$）就是这个框架。

---

## Station 4: Q-Learning 的诞生（1989）

**问题：** 如果 agent 不知道环境的转移概率（Model-free），能否通过交互学习最优策略？

**创新：** Chris Watkins 在博士论文中提出 **Q-Learning**，这是第一个有收敛保证的无模型 off-policy RL 算法：

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

**关键人物：**
- Chris Watkins（剑桥大学，1989）— Q-Learning 提出者
- Peter Dayan — 1992 年与 Watkins 合作证明了 Q-Learning 的收敛性

**Q-Learning 的关键性质：**
- Off-policy：学习最优策略，与实际执行策略无关
- 无需环境模型：只需要 $(s, a, r, s')$ 元组
- 保证在有限状态/动作 + 充分探索时收敛

**遗留问题：** Q 值用表格存储，无法处理大规模或连续状态空间。

**课程联系：** 这就是 Week 2（以及 Lab 1/2 + Assignment 1）的核心算法。

---

## Station 5: SARSA — On-Policy 的对比（1994）

**问题：** Q-Learning 学到的"理论最优"策略在实际执行中可能不安全（如 CliffWalking 贴悬崖）。是否有更贴近实际行为的算法？

**创新：** SARSA (State-Action-Reward-State-Action) 算法使用当前策略**实际选择**的 $a'$ 来更新：

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma Q(s', a') - Q(s, a) \right]$$

其中 $a'$ 是当前策略（含随机性）实际选择的动作。

**关键人物：**
- Gavin Rummery 和 Mahesan Niranjan（1994）— SARSA 首次提出
- Sutton & Barto（1998）将其命名为 SARSA

**核心差别（一张图说明）：**

```
Q-Learning:  s --a--> r, s' --[max a']--> Q(s',max)
SARSA:       s --a--> r, s' --[policy]--> Q(s', a')
                                           ^ 来自实际策略
```

**课程联系：** Week 6 Deep Dive 直接讨论 CliffWalking 中 Q-Learning vs SARSA 的路径差异。

---

## Station 6: Sutton & Barto 教科书系统化 RL（1998）

**问题：** RL 的各种算法分散在论文中，如何建立统一的教学框架？

**创新：** Richard Sutton 和 Andrew Barto 出版 *Reinforcement Learning: An Introduction*（1998 第一版，2018 第二版），将 TD Learning、Q-Learning、SARSA、Policy Gradient 等统一在一个框架下，成为 RL 圣经。

**关键人物：**
- Richard Sutton — "RL 之父"之一，现 Google DeepMind 研究员
- Andrew Barto — Sutton 的博士导师，UMass Amherst

**历史意义：** 本课程使用的大量概念（MDP、策略、价值函数、TD Error）直接来自这本教科书。

**课程联系：** 老师在 Week 2 Slides 中特别提到教科书的 Table of Contents，课程内容与 Sutton & Barto 高度对应。
