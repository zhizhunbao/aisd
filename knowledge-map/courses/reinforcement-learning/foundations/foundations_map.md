---
topic: foundations
dimension: map
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.1-2 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Paper: Robbins, 'Some aspects of the sequential design of experiments', Bull. Amer. Math. Soc. 1952 — https://projecteuclid.org/euclid.bams/1183517370"
  - "📖 Paper: Auer et al., 'Finite-time Analysis of the Multiarmed Bandit Problem', Machine Learning 2002 — https://link.springer.com/article/10.1023/A:1013689704352"
expiry: 12m
status: current
---

# RL 基础 知识地图

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1-2

## 1. 核心问题

- **什么是强化学习？和监督学习、无监督学习有什么区别？** → RL 是通过与环境交互、根据奖励信号学习最优行为策略的框架，没有标签，也不只是找结构
- **Agent 是怎么和环境交互的？** → Agent 在每个时间步观察状态、选择动作、收到奖励和新状态，形成循环
- **策略、回报、折扣因子分别是什么意思？** → 策略是状态到动作的映射，回报是未来奖励的加权和，折扣因子控制对未来奖励的重视程度
- **为什么需要探索？总是选当前最好的不行吗？** → 总选当前最优（纯利用）可能错过全局最优，需要探索来发现更好的选择
- **多臂赌博机问题为什么是 RL 的入门模型？** → 它是最简单的探索-利用权衡场景：只有动作和奖励，没有状态转移

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 §1.1, Ch.2 §2.1

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念 ← 你在这里
    │   ├── 【Foundations】 (Agent/环境/奖励/策略/探索vs利用)
    │   └── Multi-Armed Bandit (探索-利用入门模型)
    ├── 规划方法
    │   ├── MDP (马尔可夫决策过程框架)
    │   ├── Dynamic Programming (已知模型的最优解)
    │   └── Model-Based RL (学习+规划)
    ├── 无模型方法
    │   ├── Monte Carlo (回合制采样学习)
    │   ├── Temporal Difference (每步在线学习)
    │   └── Function Approximation (DQN/深度扩展)
    ├── 策略优化
    │   ├── Policy Gradient (直接优化策略)
    │   └── Actor-Critic (策略+值函数双网络)
    └── 高级主题
        ├── IRL & Imitation Learning (从示范学习)
        ├── Multi-Agent RL (多智能体)
        └── RLHF & Alignment (人类反馈对齐)

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 Figure 1.1

---

## 3. 依赖地图

    前置知识                    本主题                     后续方向
    ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
    │ 概率论基础         │─────→│                  │─────→│ MDP (状态转移+贝尔曼) │
    │ 期望值/方差        │─────→│   Foundations    │─────→│ Monte Carlo (采样)   │
    │ 基础编程 (Python)  │─────→│   RL 基础        │─────→│ TD Learning (在线)   │
    └──────────────────┘      └──────────────────┘      └──────────────────────┘

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1 §1.5

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [foundations_map.md](foundations_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [foundations_concepts.md](foundations_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [foundations_math.md](foundations_math.md) | ③ 公式 | 推导回报公式、贝尔曼方程预备 |
| [foundations_tutorial.md](foundations_tutorial.md) | ④ 教程 | Why-First 理解 RL 设计动机与原理 |
| [foundations_code.md](foundations_code.md) | ⑤ 代码 | 快速实现多臂赌博机和 ε-greedy |
| [foundations_pitfalls.md](foundations_pitfalls.md) | ⑥ 踩坑 | 调试探索率、奖励设计等常见问题 |
| [foundations_history.md](foundations_history.md) | ⑦ 历史 | 了解从动物心理学到 DeepMind 的演进 |
| [foundations_bridge.md](foundations_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [foundations_first_principles.md](foundations_first_principles.md) | ⑨ 第一性原理 | 追问 RL 的底层公理与边界 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.1-2

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [foundations_map.md](foundations_map.md) 了解 RL 在 AI 中的全局位置
2. 读 [foundations_tutorial.md](foundations_tutorial.md) Section 1 理解 RL 要解决什么问题
3. 读 [foundations_concepts.md](foundations_concepts.md) 掌握 Agent/环境/奖励/策略等核心术语
4. 读 [foundations_math.md](foundations_math.md) 手算一次回报公式和样本均值更新
5. 跟 [foundations_code.md](foundations_code.md) 快速开始跑一个 ε-greedy 多臂赌博机
6. 读 [foundations_history.md](foundations_history.md) 了解 RL 从心理学到 AI 的演进
7. 读 [foundations_first_principles.md](foundations_first_principles.md) 追问 RL 的底层公理

### 日常参考 🔧

1. 查 [foundations_code.md](foundations_code.md) API 速查表
2. 查 [foundations_math.md](foundations_math.md) 公式速查
3. 查 [foundations_pitfalls.md](foundations_pitfalls.md) 排查探索率和奖励设计问题

### 深度研究 🔬

1. 读 [foundations_history.md](foundations_history.md) 完整演进线
2. 读 [foundations_first_principles.md](foundations_first_principles.md) 追问底层公理
3. 读 [foundations_bridge.md](foundations_bridge.md) 探索 MDP 和 TD 方向
4. 阅读 Robbins (1952) 和 Auer et al. (2002) 原始论文

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-19 | 12m | ✅ current |
| Concepts | 2026-03-19 | 12m | ✅ current |
| Math | 2026-03-19 | 12m | ✅ current |
| Tutorial | 2026-03-19 | 12m | ✅ current |
| Code | 2026-03-19 | 6m | ✅ current |
| Pitfalls | 2026-03-19 | 6m | ✅ current |
| History | 2026-03-19 | never | ✅ current |
| Bridge | 2026-03-19 | 12m | ✅ current |
| First Principles | 2026-03-19 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Reinforcement Learning: An Introduction》Ch.1-2](../../../textbooks/sutton_barto_rl_intro.pdf) | 📚 教科书 | 全文核心参考 |
| [Robbins 1952](https://projecteuclid.org/euclid.bams/1183517370) | 📖 论文 | 多臂赌博机原始问题提出 |
| [Auer et al. 2002](https://link.springer.com/article/10.1023/A:1013689704352) | 📖 论文 | UCB 算法有限时间分析 |
| [Gymnasium Docs](https://gymnasium.farama.org/) | 📖 文档 | 代码实现参考 |
