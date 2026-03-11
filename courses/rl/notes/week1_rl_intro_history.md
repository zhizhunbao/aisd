# Week 1: 强化学习入门 — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week1_rl_intro_slides.md) | [数学公式](week1_rl_intro_math.md)

---

## 时间轴概览

```
1890s          1950s          1960s-70s       1980s           1990s-2000s     2010s-today
  │              │               │              │                 │               │
  ▼              ▼               ▼              ▼                 ▼               ▼
Thorndike    Turing 1950     Dynamic       TD Learning      TD-Gammon        AlphaGo
Effect of    "Can machines  Programming    Sutton 1988     Tesauro 1992      2016
Behavior     think?"        Bellman 1957   Watkins 1989    Q-Learning beats  Deep RL
(RL 萌芽)    (AI 诞生)      (理论基础)    (算法突破)     人类跳棋冠军      全面突破
```

---

## Station 1: 行为主义心理学 — RL 的思想根源（1890s）

**问题：** 动物如何学习？如何将"刺激-反应"关系量化？

**创新：** Edward Thorndike 的**效果律（Law of Effect）**

> "满意结果会加强当前行为，不满意结果会减弱它。"

**关键人物：**
- Edward Thorndike（1874-1949）— 猫逃出迷箱实验
- B.F. Skinner（1904-1990）— 操作性条件反射、Skinner Box

**核心洞察：** 通过奖励/惩罚信号指导行为，无需逐步告诉 agent"正确答案"——这正是 RL 的核心思想。

**课程联系：** RL 中的 Reward 信号 = 心理学中的"强化物"（Reinforcer）。

---

## Station 2: 图灵测试与人工智能萌芽（1950）

**问题：** 能否让机器"思考"或"学习"？如何评估机器智能？

**创新：** Alan Turing 在论文 *"Computing Machinery and Intelligence"* 中提出**图灵测试**，探讨机器学习的可能性。

**关键人物：**
- Alan Turing（1912-1954）— 计算机科学之父

**背景影响：** Turing 的工作启发了整个 AI 领域，间接推动了 RL 的理论化探索。

**遗留问题：** 如何让机器在**序列决策**（不只是一次性问答）场景下学习？

---

## Station 3: 动态规划与 Bellman 方程（1957）

**问题：** 序列决策问题（今天的选择影响明天的状态）如何系统化求解？

**创新：** Richard Bellman 提出**动态规划 (Dynamic Programming)** 和**贝尔曼方程**：

$$V(s) = \max_a \left[ R(s, a) + \gamma V(s') \right]$$

将最优决策问题分解为子问题，递归求解。

**关键人物：**
- Richard Bellman（1920-1984）— "最优性原理"的提出者
- 同期：Howard (1960) 提出策略迭代算法

**遗留问题：** DP 需要完整的环境模型（状态转移概率），真实场景中往往未知。

**课程联系：** Week 2 MDP 的 Bellman 方程直接来源于此。Q-Learning 是 Bellman 方程的无模型版本。

---

## Station 4: 时序差分学习与 Q-Learning（1988-1989）

**问题：** 如果没有环境模型，agent 能否通过与环境交互逐步学习最优策略？

**创新（两步）：**
1. Richard Sutton（1988）提出**时序差分学习 (TD Learning)**：不需要等到 episode 结束，每步都可以更新价值估计
2. Chris Watkins（1989）提出 **Q-Learning**：第一个无模型的 off-policy 强化学习算法（博士论文）

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

**关键人物：**
- Richard Sutton — TD(λ) 算法，RL 领域开创性贡献者
- Andrew Barto — Sutton 的导师，共同奠定 RL 理论基础
- Chris Watkins — Q-Learning 的提出者

**遗留问题：** Q-Learning 仅适用于离散状态和动作空间，连续状态空间无法用表格表示。

**课程联系：** 这就是 Week 2 学的 Q-Learning 算法，也是 Lab 1/2 的核心实现。

---

## Station 5: TD-Gammon 与深度强化学习的前身（1992）

**问题：** Q-Learning/TD 方法能否应用于复杂的真实问题？

**创新：** Gerald Tesauro 用**神经网络**近似价值函数（TD-Gammon），实现了世界级水平的双陆棋（Backgammon）对弈。

**关键人物：**
- Gerald Tesauro（IBM）— 第一个将 TD Learning 与神经网络结合的成功案例

**意义：** 证明了 RL + 函数近似（神经网络）的可行性，但当时计算力不足，无法大规模应用。

**遗留问题：** 训练不稳定，难以扩展到更复杂问题（后来由 DQN 的三大创新解决）。

**课程联系：** Week 5 DQN 正是解决了 TD-Gammon 时代的稳定性问题。

---

## Station 6: DQN 与深度强化学习时代（2013-2016）

**问题：** 如何让 RL agent 在 Atari 游戏（连续视觉像素输入）中达到超人类水平？

**创新：** DeepMind 的 DQN（Deep Q-Network）——将 Q-Learning 与**深度卷积网络**结合，引入 Target Network 和 Replay Buffer 解决训练不稳定问题。

**里程碑：**
- 2013 NIPS — DQN 在 7 个 Atari 游戏超越人类
- 2015 Nature — DQN 在 49 个 Atari 游戏超越人类
- 2016 AlphaGo — DeepMind RL 击败围棋世界冠军李世乭
- 2017 AlphaZero — 无需人类知识，自学围棋、象棋、将棋

**关键人物：**
- Volodymyr Mnih（DeepMind）— DQN 第一作者
- David Silver（DeepMind）— DQN 和 AlphaGo 核心成员

**课程联系：** Week 5 的 DQN 就是这个历史节点的直接实现。

---

## 课程全局位置

```
Week 1: 了解 RL 是什么 → 来自哪里（本文）
Week 2: Q-Learning 算法（Station 4 的具体实现）
Week 3: Gymnasium 框架
Week 4: SB3（DQN, PPO 可用）
Week 5: DQN（Station 6 的具体实现）
```
