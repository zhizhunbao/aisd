---
topic: dynamic-programming
dimension: map
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.4 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Paper: Howard, 'Dynamic Programming and Markov Processes', MIT Press 1960"
  - "📖 Paper: Bellman, 'Dynamic Programming', Princeton University Press 1957"
expiry: 12m
status: current
---

# 动态规划 知识地图

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4

## 1. 核心问题

- **动态规划在 RL 中干什么？** → 在已知完整环境模型（转移概率 + 奖励函数）的条件下，计算最优策略
- **策略评估是什么意思？** → 给定一个策略 π，算出每个状态的值 V^π(s)——即"按照这个策略走，未来能拿多少回报"
- **策略改进是怎么工作的？** → 在每个状态，用当前值函数找一个比旧策略更好的动作，形成新策略
- **策略迭代和值迭代有什么区别？** → 策略迭代交替做"评估→改进"直到收敛；值迭代把两步合成一步，直接迭代贝尔曼最优方程
- **为什么 DP 在实践中不够用？** → DP 需要完整的环境模型，但真实世界中通常不知道转移概率——这就催生了 MC 和 TD 方法

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.1-4.7

---

## 2. 全景位置

    Reinforcement Learning（强化学习课程）
    ├── 基础概念
    │   ├── Foundations (Agent/环境/奖励/策略/探索vs利用)
    │   └── Multi-Armed Bandit (探索-利用入门模型)
    ├── 规划方法
    │   ├── MDP (马尔可夫决策过程框架)
    │   ├──【Dynamic Programming】← 你在这里
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
    │ MDP 框架          │─────→│                  │─────→│ Monte Carlo 方法     │
    │ 贝尔曼方程        │─────→│   Dynamic        │─────→│ TD Learning          │
    │ 线性代数基础      │─────→│   Programming    │─────→│ Model-Based RL       │
    │ Foundations 基础  │─────→│   动态规划        │─────→│ Function Approx.     │
    └──────────────────┘      └──────────────────┘      └──────────────────────┘

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.1

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [dynamic_programming_map.md](dynamic_programming_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [dynamic_programming_concepts.md](dynamic_programming_concepts.md) | ② 概念 | 理解策略评估/改进/迭代等核心术语 |
| [dynamic_programming_math.md](dynamic_programming_math.md) | ③ 公式 | 推导贝尔曼方程、迭代更新公式 |
| [dynamic_programming_tutorial.md](dynamic_programming_tutorial.md) | ④ 教程 | Why-First 理解 DP 的设计动机与原理 |
| [dynamic_programming_code.md](dynamic_programming_code.md) | ⑤ 代码 | 实现策略迭代和值迭代算法 |
| [dynamic_programming_pitfalls.md](dynamic_programming_pitfalls.md) | ⑥ 踩坑 | 调试收敛问题、理解同步/异步更新 |
| [dynamic_programming_history.md](dynamic_programming_history.md) | ⑦ 历史 | 了解从 Bellman 到 Howard 的演进 |
| [dynamic_programming_bridge.md](dynamic_programming_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [dynamic_programming_first_principles.md](dynamic_programming_first_principles.md) | ⑨ 第一性原理 | 追问 DP 的底层公理与边界 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [dynamic_programming_map.md](dynamic_programming_map.md) 了解 DP 在 RL 中的全局位置
2. 读 [dynamic_programming_tutorial.md](dynamic_programming_tutorial.md) 理解为什么需要 DP
3. 读 [dynamic_programming_concepts.md](dynamic_programming_concepts.md) 掌握策略评估/改进/迭代等核心术语
4. 读 [dynamic_programming_math.md](dynamic_programming_math.md) 手算一次策略评估迭代
5. 跟 [dynamic_programming_code.md](dynamic_programming_code.md) 在 GridWorld 上跑策略迭代和值迭代
6. 读 [dynamic_programming_history.md](dynamic_programming_history.md) 了解 DP 从运筹学到 RL 的演进
7. 读 [dynamic_programming_first_principles.md](dynamic_programming_first_principles.md) 追问 DP 的底层公理

### 日常参考 🔧

1. 查 [dynamic_programming_code.md](dynamic_programming_code.md) API 速查表
2. 查 [dynamic_programming_math.md](dynamic_programming_math.md) 公式速查
3. 查 [dynamic_programming_pitfalls.md](dynamic_programming_pitfalls.md) 排查收敛和实现问题

### 深度研究 🔬

1. 读 [dynamic_programming_history.md](dynamic_programming_history.md) 完整演进线
2. 读 [dynamic_programming_first_principles.md](dynamic_programming_first_principles.md) 追问底层公理
3. 读 [dynamic_programming_bridge.md](dynamic_programming_bridge.md) 探索 MC 和 TD 方向
4. 阅读 Bellman (1957) 和 Howard (1960) 原始著作

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
| [《Reinforcement Learning: An Introduction》Ch.4](../../../textbooks/sutton_barto_rl_intro.pdf) | 📚 教科书 | 全文核心参考 |
| [Bellman 1957 "Dynamic Programming"](https://press.princeton.edu/books/paperback/9780691146683/dynamic-programming) | 📖 著作 | DP 理论奠基 |
| [Howard 1960 "Dynamic Programming and Markov Processes"](https://mitpress.mit.edu/9780262080095/dynamic-programming-and-markov-processes/) | 📖 著作 | 策略迭代算法提出 |
| [Gymnasium Docs](https://gymnasium.farama.org/) | 📖 文档 | 代码实现参考 |
