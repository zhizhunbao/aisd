# Week 6: 期中复习 — 历史与背景 (History & Context)

> See also: [幻灯片笔记](week6_midterm_review_slides.md) | [操作教程](week6_midterm_review_tutorial.md)

---

## 这一文件的定位

Week 6 是**期中复习周**，没有新技术内容——它的历史背景就是 Week 1-5 的整条线索串联。本文件将课程前半段的技术演进整合为一个完整故事。

---

## 课程前半段技术演进一览

```
1890s 行为主义         → "奖励信号改变行为" 思想根源
  ↓
1957 贝尔曼方程        → 序列决策的数学框架
  ↓
1989 Q-Learning       → 无模型、off-policy 算法
  ↓
2016 OpenAI Gym       → 标准化 RL 环境接口
  ↓
2015 DQN              → 神经网络 Q-Learning
  ↓
2021 SB3              → 工业级 RL 算法库
  ↓
2022 Gymnasium        → OpenAI Gym 的继承者（Farama 基金会）
```

---

## 期中考试回顾的六大主题历史溯源

### Theme 1: RL Fundamentals（来自 Week 1）

**历史根源：**
- Thorndike 效果律（1890s）→ 奖励驱动行为
- Turing 图灵测试（1950）→ 机器学习的可能性
- Bellman 动态规划（1957）→ 价值函数、折扣回报的数学形式化

**为什么重要：** RL 的三要素（Agent/Environment/Reward）来自行为心理学；$G_t = \sum \gamma^k r_{t+k+1}$ 来自贝尔曼的最优性原理。

---

### Theme 2: Basic Q-Learning（来自 Week 2 + Week 2 Deep Dive）

**历史根源：**
- Watkins（1989）提出 Q-Learning 博士论文
- Sutton & Barto（1998）教科书系统化

**关键历史争论（2006-2008）：**

Q-Learning vs SARSA 在 CliffWalking 的差异不只是算法问题，它反映了一个深层问题：

> "我们要学习'如果 agent 完美行动的最优策略'，还是'考虑到 agent 实际会犯错的最优策略'？"

这个问题在 2010 年代的安全强化学习（Safe RL）领域再次成为焦点。

---

### Theme 3: Gymnasium（来自 Week 3）

**历史根源：**
- ALE（2013）— 第一个标准化 RL 基准
- OpenAI Gym（2016）— 统一接口
- Gymnasium（2022）— Farama 基金会维护，修复旧 API

**历史意义：** 没有统一的环境接口，就没有算法的可比较性，也就没有深度 RL 的爆发。Gym 的出现和 DQN 几乎同步（2013 ALE + 2013 DQN），相辅相成。

---

### Theme 4: Q-Learning + CliffWalking（深入理解）

**历史根源：**
- CliffWalking 作为经典 RL 教学示例，最早出现在 Sutton & Barto 1998 教科书第 6 章
- 它成为了 on-policy vs off-policy 对比的**标准教学案例**，被全球 RL 课程广泛采用

**学术价值：** CliffWalking 的简单性使它成为了"理论与实践差距"的完美展示案例：
- Q-Learning 在理论上是最优的（最短路径）
- SARSA 在实际执行中更好（考虑了 ε-greedy 噪声）

这个 trade-off 至今在 Safe RL、Risk-sensitive RL 等方向仍然活跃研究。

---

### Theme 5: Q-Learning Deep Dive（来自 Week 5）

**历史根源：**
- Q-table 初始化问题 → 连接 Optimistic Initial Values 研究（Sutton & Barto Ch.2）
- 终止状态 Q=0 的重要性 → 与 Bellman 方程正确性直接相关

**工业延伸：** 终止状态处理不当是 RL 工程中常见 Bug 之一。2019 年 OpenAI 发现某些 Baselines 实现中存在这个 Bug，影响了当时多篇论文的可靠性。

---

### Theme 6: Stable-Baselines3（来自 Week 4）

**历史根源：**
- PPO（2017）— 目前最广泛使用的 RL 算法
- SB3（2021）— 将 DQN/PPO/A2C/SAC/TD3 等打包为可靠工具

**现实影响：**
- ChatGPT 的 RLHF（Reinforcement Learning from Human Feedback）阶段使用 PPO
- Autonomous driving, robotics 广泛使用 SB3 作为基线

---

## 期中考试历史视角备考提示

| 考点 | 历史来源 | 理解要点 |
|------|---------|---------|
| Q-Learning 公式 | Watkins 1989 博士论文 | 无模型 + off-policy + TD error |
| Markov Property | Markov 1906 链 | 未来只依赖当前状态 |
| ε-Greedy | Sutton & Barto 1998 | 探索-利用权衡 |
| Gymnasium Wrapper | OpenAI Gym → Farama 2022 | 不修改底层代码的修改方式 |
| SB3 | Raffin et al. 2021 | PPO/DQN/SAC 可靠实现 |
| Off-policy vs On-policy | Q-Learning vs SARSA 1994 | 最短路径 vs 安全路径 |

---

## 这段历史给了我们什么

1. **RL 的核心思想 100 年前就有了**（行为主义），数学化只花了 50 年（Bellman 1957），可用算法又花了 30 年（DQN 2013）
2. **标准化接口改变一切**：Gym 的出现让 RL 算法可以比较，这是深度 RL 爆发的工程基础
3. **工程可靠性与算法创新同等重要**：SB3 存在是因为研究代码往往有 Bug，"可靠的实现"本身就是贡献
