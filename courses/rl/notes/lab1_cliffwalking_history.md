# 🕰️ Lab 1 CliffWalking — 技术演进历史线

> **课程:** CST8509 Reinforcement Learning | **主题:** Q-Learning & CliffWalking
> **时间跨度:** 1953 — 2018
> **核心脉络:** 动态规划 → 时序差分学习 → Q-Learning → 经典基准问题
> **Source:** Sutton §1.7 (Early History of RL) + Watkins 1989 + Sutton §6 (TD Learning)

---

## 📍 全景时间线（Timeline Overview）

```
1953         1959         1988         1989         1992         1998         2018
  │            │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼            ▼
Bellman      Samuel       TD(λ)        Watkins      Watkins &    S&B 第一版   S&B 第二版
动态规划     Checkers     算法         Q-Learning   Dayan        教科书       (开放版)
             首次 RL      Sutton       论文         收敛性证明   出版
                          提出
  │            │            │            │            │            │            │
  └──── 数学基础 ┘           │            └──── 理论完善 ┘            └── 标准化 ─┘
               └── 学习启发 ─┘
                                                         ← CliffWalking 作为例子 ──┘
```

---

## 第 1 站：Bellman 与动态规划 (1953–1957)

### 🧩 之前的问题

1950 年代初，工程师和数学家需要解决多阶段决策问题（如火箭轨迹优化、资源分配）。问题：面对未来数百个决策点，如何找到最优策略？

### 💡 核心创新

**Richard Bellman** 提出了**动态规划（Dynamic Programming, DP）**，核心思想是**最优子结构**：最优策略的子序列也是最优的。

这直接导出了 Bellman 方程：

$$V(s) = \max_a \left[ R(s,a) + \gamma V(s') \right]$$

或 Q 函数版本（后来被 Watkins 使用）：

$$Q(s,a) = R + \gamma \max_{a'} Q(s', a')$$

### 👤 关键人物

- **Richard Bellman** — RAND Corporation, 1953–1957
- 主要著作: *Dynamic Programming* (1957, Princeton University Press)
- 命名: 他创造了 "**Curse of Dimensionality**" 一词——维度每增加 1，状态空间指数级增长

### ⚠️ 遗留问题

DP **需要已知环境模型**（完整的 $P(s'\|s,a)$ 和 $R(s,a)$）。现实问题中环境模型往往未知——需要一种**无模型（model-free）**的学习方法。

### 🔗 与 Lab 1 的关联

> Q-Learning 更新公式 $Q \leftarrow Q + \alpha[R + \gamma \max Q' - Q]$ 正是 Bellman 方程的**采样近似版本**。理解这个历史背景可以解答"为什么 Q-Learning 有效"。

---

## 第 2 站：Samuel 的 Checkers (1959)

### 🧩 之前的问题

DP 要求知道模型，而 Samuel 面对的是跳棋——规则已知，但最优策略未知。他想让机器自己通过下棋学习。

### 💡 核心创新

Samuel 开发了**通过自我对弈学习**的西洋跳棋程序，并创造了 "Machine Learning" 这个词。他的方法使用**评估函数**（类似 $V(s)$）打分，通过对弈不断调整参数。

这是历史上第一个通过经验改进性能的游戏 AI。

### 👤 关键人物

- **Arthur Samuel** — IBM Research, 1959
- 论文: "Some Studies in Machine Learning Using the Game of Checkers" (IBM J. R&D, 1959)

### ⚠️ 遗留问题

Samuel 的评估函数是**人工设计的特征组合**。他没有一个通用的学习算法——每个问题还是需要特定设计。**需要一种通用的值函数更新算法。**

---

## 第 3 站：时序差分学习 TD(λ) (1988)

### 🧩 之前的问题

DP 需要完整模型，Monte Carlo 方法需要等完整回合结束后才能更新。问题：能不能在每一步之后就立即更新估计值？

### 💡 核心创新

**Richard Sutton** 在 1988 年发表了 **TD(λ)** 算法——**时序差分学习（Temporal Difference Learning）**的通用框架。

核心思想：用**相邻时间步的估计差异**来更新当前估计：

$$V(s) \leftarrow V(s) + \alpha \underbrace{[R + \gamma V(s') - V(s)]}_{\text{TD 误差}}$$

关键特性：
- **Model-free**：不需要知道转移概率
- **Online**：每一步都可以更新，无需等 episode 结束
- **TD 误差** 是 DP（bootstrapping）和 MC（sampling）的结合

### 👤 关键人物

- **Richard Sutton** — GTE Labs, 1988
- 论文: "Learning to Predict by the Methods of Temporal Differences" (Machine Learning, 1988)

### 🔗 与 Lab 1 的关联

> Lab 1 指导文档要求你能"解释 Temporal Difference learning（Q-learning）如何工作"。Q-Learning 是 TD 学习的特例——用 max 操作选取下一步最优动作值。

---

## 第 4 站：Q-Learning 诞生 (1989)

### 🧩 之前的问题

Sutton 的 TD(λ) 对策略评估很有效，但**如何直接学习最优策略**而不需要策略迭代？

### 💡 核心创新

**Chris Watkins** 在其博士论文中提出了 **Q-Learning**——第一个被证明能够直接学习最优 Q 函数的算法：

$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[ R + \gamma \max_{a'} Q(s',a') - Q(s,a) \right]$$

**关键突破：**
- **Off-policy**：学习最优策略，同时用 ε-greedy 策略探索（两者可以不同）
- **Q-Table**：有限状态 + 动作空间时，用一张表存储所有 Q 值
- **Model-free**：只需要 $(s, a, r, s')$ 样本，不需要模型

### 👤 关键人物

- **Christopher Watkins** — Cambridge University, 1989
- 博士论文: "Learning from Delayed Rewards" (1989)

### 📊 里程碑

- 1992年，**Watkins & Dayan** 发表收敛性证明：只要每个状态-动作对被访问足够多次，Q-Learning 一定收敛到最优 $Q^*$
- **条件：** 有限状态、有限动作、学习率满足 Robbins-Monro 条件 $\sum \alpha_t = \infty$，$\sum \alpha_t^2 < \infty$

### ⚠️ 遗留问题

Q-Table 只适用于**有限且较小的状态空间**。状态维度一增加，表格就会爆炸（Curse of Dimensionality）。用神经网络近似 Q 值的 DQN 在 2013 年才解决这个问题。

### 🔗 与 Lab 1 的关联

> CliffWalking 的状态空间 $|S| = 48$，动作空间 $|A| = 4$，Q-Table 只有 192 个元素——完全在 Q-Table 适用范围内（Quiz 2 Q13 的考点）。

---

## 第 5 站：CliffWalking 成为标准基准 (1998)

### 🧩 之前的问题

如何演示 Q-Learning（off-policy）与 SARSA（on-policy）的本质区别？需要一个既简单又能清晰展现差异的例子。

### 💡 核心创新

**Sutton & Barto** 在 1998 年版教科书中选用 **CliffWalking** 作为 Q-Learning vs SARSA 对比的经典示例（§6.5, p.132）：

- **Q-Learning** 学到最优路径：沿悬崖边缘走（最短路，平均 return ≈ -13）
- **SARSA** 学到安全路径：绕上方走（远离悬崖，平均 return ≈ -17 但更稳定）

原因：Q-Learning 用 $\max_{a'}$ 假设下一步总是最优，SARSA 用实际执行的动作（含 ε 探索噪声），所以更"保守"。

### 👤 关键人物

- **Richard Sutton & Andrew Barto** — *Reinforcement Learning: An Introduction* (MIT Press, 1998; 2nd ed. 2018)

### 📊 里程碑数据

| 算法 | 路径 | 在线 Return（训练中） | 最优 Return |
|------|------|----------------------|------------|
| Q-Learning | 崖边 | 较差（时常掉崖） | -13（最短路） |
| SARSA | 绕远 | 较好（少掉崖） | -17（安全路） |

### 🔗 与 Lab 1 的关联

> Lab 1 只要求实现 Q-Learning。上表的对比说明了为什么你的 Q-Learning agent 训练时 return 会频繁出现 -100 惩罚——但最终仍然收敛到最优路径。
