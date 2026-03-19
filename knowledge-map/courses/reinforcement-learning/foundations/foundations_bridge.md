---
topic: foundations
dimension: bridge
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
expiry: 12m
status: current
---

# RL 基础 衔接与扩展

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 概率论基础 | 期望值、条件概率是理解奖励和回报的数学工具 | — |
| ← 前置 | Python 编程 | 实现 Agent 和环境交互的编程基础 | — |
| → 后续 | MDP | 在 Agent-环境循环上加入"状态转移"和"贝尔曼方程" | [mdp](../mdp/mdp_map.md) |
| → 后续 | Monte Carlo 方法 | 用完整回合的回报来学习值函数 | [monte_carlo](../monte_carlo/monte_carlo_map.md) |
| → 后续 | Temporal Difference | 结合了蒙特卡洛和动态规划的在线学习 | [temporal_difference](../temporal_difference/temporal_difference_map.md) |
| → 后续 | Gazebo 仿真器 | RL 环境的物理实现，仿真中无限试错 | [gazebo](../gazebo/gazebo_map.md) |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 §1.5

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 概率论 | 期望值 E[X] | 定义动作价值 q*(a) = E[R \| A=a] |
| 概率论 | 条件概率 | 随机策略 π(a\|s) 是条件概率分布 |
| 统计学 | 样本均值 | 样本均值法估计动作价值 Q(a) |
| 统计学 | 置信区间 | UCB 的探索项来自置信上界思想 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| MDP | Agent-环境交互循环 | 扩展为完整的马尔可夫决策过程框架 |
| MDP | 回报 Gₜ | 用于定义值函数 V(s) 和 Q(s,a) |
| MDP | 折扣因子 γ | 贝尔曼方程的递推核心 |
| TD Learning | 增量更新规则 | 推广为 TD 更新：Q ← Q + α[r + γQ' - Q] |
| Policy Gradient | 策略 π | 策略参数化：π_θ(a\|s) |
| Function Approx | Q 值估计 | 从表格 Q(s,a) → 神经网络 Q(s,a;θ) |
| RLHF | 奖励假说 | 用人类偏好替代手工设计的奖励函数 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1-2

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 试错学习 | 动物心理学的定性观察 (Thorndike 1898) | 数学化的 Q-Learning + 神经网络 | 计算力和深度学习的发展 |
| 探索策略 | ε-Greedy 随机探索 (1960s) | UCB/Thompson Sampling/Curiosity-driven | 需要更高效的探索 |
| 奖励信号 | 手工设计标量奖励 | RLHF 从人类偏好学习奖励 | 奖励设计太难，用人类反馈替代 |
| 值函数估计 | 查表法 (Tabular Q) | 深度神经网络 (DQN) | 状态空间爆炸，查表存不下 |
| 环境 | 真实物理环境 | 大规模仿真器 (MuJoCo, Atari) | 真实探索成本太高 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Sutton & Barto Ch.2](../../../textbooks/sutton_barto_rl_intro.pdf) | 📚 教科书 | 多臂赌博机的完整理论和实验 | ⭐⭐ |
| [Lattimore & Szepesvári "Bandit Algorithms"](https://tor-lattimore.com/downloads/book/book.pdf) | 📚 教科书 | 多臂赌博机的深度数学理论 | ⭐⭐⭐⭐ |
| [Auer et al. 2002](https://link.springer.com/article/10.1023/A:1013689704352) | 📖 论文 | UCB 的有限时间遗憾界证明 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Multi-Agent RL 基础](../multi_agent/multi_agent_map.md) | 从单 Agent 到多 Agent | 理解 Foundations 后 |
| 博弈论入门 | 探索-利用 vs 纳什均衡 | 对 MARL 感兴趣时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [OpenAI Spinning Up](https://spinningup.openai.com/) | 实践导向的 Deep RL 入门 | 掌握 Foundations + MDP 后 |
| [Deep RL Bootcamp](https://sites.google.com/view/deep-rl-bootcamp-2017) | UC Berkeley 暑期课程视频 | 想系统学 Deep RL 时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| Deep Learning 课程 | 15+ 主题 | dense_layer, cnn, transformer | RL 的 Function Approximation 需要 DL 基础 |
| Machine Learning 课程 | 14 主题 | model_evaluation_metrics, overfitting | RL 的评估方法和过拟合概念可类比 |
| 数学课程 | 3 主题 | differentiation, integration | 策略梯度需要微积分基础 |
