---
topic: dynamic-programming
dimension: bridge
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.4 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
expiry: 12m
status: current
---

# 动态规划 衔接与扩展

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Foundations | Agent/环境/奖励/策略/探索vs利用的基本概念 | [foundations](../foundations/foundations_map.md) |
| ← 前置 | MDP | 贝尔曼方程、状态/动作值函数定义 | — |
| ← 前置 | 线性代数 | 矩阵运算，理解方程组求解 vs 迭代逼近 | — |
| → 后续 | Monte Carlo 方法 | 不需要模型的策略评估和控制 | — |
| → 后续 | Temporal Difference | 结合 MC（采样）和 DP（自举）的方法 | — |
| → 后续 | Model-Based RL | 先学模型再用 DP 规划 (Dyna) | — |
| → 后续 | Function Approximation | 用神经网络替代表格 V/Q | — |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.7

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| MDP | 贝尔曼期望方程 V^π(s) | 策略评估的迭代更新规则 |
| MDP | 贝尔曼最优方程 V*(s) | 值迭代的迭代更新规则 |
| MDP | 转移概率 P(s'\|s,a) | DP 更新公式的核心组成部分 |
| MDP | 折扣因子 γ | 控制迭代收敛速度和解的性质 |
| Foundations | 策略 π(a\|s) | 策略评估和改进的输入/输出 |
| Foundations | 值函数概念 V(s), Q(s,a) | DP 计算的目标对象 |
| 线性代数 | 矩阵求逆 / 迭代法 | 理解为什么不直接解而用迭代 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3-4

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------| 
| Monte Carlo | 策略评估的思想 | MC 用采样回报替代 DP 的期望计算 |
| Monte Carlo | GPI 框架 | MC 控制 = MC 评估 + 贪心改进 |
| TD Learning | 自举 (Bootstrapping) | TD 用 r + γV(s') 替代 DP 的完整期望 |
| TD Learning | 贝尔曼更新结构 | TD 误差 δ = r + γV(s') - V(s) 直接对应 DP 更新 |
| Q-Learning | 贝尔曼最优方程 | Q-Learning 更新 = 值迭代的采样版本 |
| Function Approx | 值迭代思想 | DQN = 值迭代 + 神经网络 + 经验回放 |
| Model-Based RL | 完整 DP 过程 | Dyna = 学模型 + 在模型上做 DP 规划 |
| Actor-Critic | GPI 框架 | Actor = 策略改进, Critic = 策略评估 |
| Planning | 异步 DP | MCTS 和其他规划方法中的值更新策略 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4-8

---

## 概念演变追踪

| 概念 | 在 DP 中 | 在后续方法中 | 变化原因 |
|------|---------|------------|---------|
| 值函数更新 | Σ_P [R + γV]（期望） | r + γV(s')（采样） | 不知道 P → 用经验替代 |
| 策略评估 | 完全迭代至收敛 | MC: 完整回合 / TD: 每步 | 没有模型 → 用样本逼近 |
| 策略改进 | argmax_a Q^π(s,a) | ε-greedy 改进 | 需要探索，不能纯贪心 |
| GPI | 评估→改进交替 | 评估和改进同时进行 | 在线学习不能等评估完 |
| 自举 | 用 V_k(s') 更新 V_{k+1}(s) | 用 V(s') 估计更新 V(s) | 相同思想，从精确到近似 |
| 状态遍历 | 扫描所有状态 | 只更新遇到的状态 | 状态太多/不知道有哪些 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4-6

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Sutton & Barto Ch.4](../../../textbooks/sutton_barto_rl_intro.pdf) | 📚 教科书 | DP 在 RL 中的完整阐述 | ⭐⭐ |
| [Bertsekas "Dynamic Programming and Optimal Control"](https://www.athenasc.com/dpbook.html) | 📚 教科书 | DP 的工程视角和高级变体 | ⭐⭐⭐⭐ |
| [Bellman 1957 "Dynamic Programming"](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) | 📖 著作 | 原始理论，理解思想根源 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| Monte Carlo 方法 | Model-Free vs Model-Based | 理解 DP 后 |
| TD Learning | 自举+采样 vs 纯自举 | 理解 DP 和 MC 后 |
| 线性规划解 MDP | 另一种精确求解思路 | 对优化方法感兴趣时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Dyna-Q (Sutton Ch.8)](../../../textbooks/sutton_barto_rl_intro.pdf) | DP + 模型学习的结合 | 理解 DP + MC/TD 后 |
| [AlphaGo 论文](https://www.nature.com/articles/nature16961) | MCTS 中的值更新借鉴 DP 思想 | 对规划方法感兴趣时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| RL 课程 | 4 主题 | foundations, gazebo, rviz | DP 是 foundations → MC/TD 的桥梁 |
| Optimization 课程 | — | convex optimization | 贝尔曼方程 = 函数空间上的不动点迭代，与优化理论相通 |
| Deep Learning 课程 | 15+ 主题 | dense_layer, cnn | 函数近似 DP (DQN) 需要 DL 基础 |
