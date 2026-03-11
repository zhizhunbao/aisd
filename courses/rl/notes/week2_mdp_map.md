# Week 2: MDP 学习地图

## 1. 核心问题

本讲回答：
- MDP 的五元组 $(S, A, P, R, \gamma)$ 各是什么？
- Q-Learning 更新公式是什么？如何手算？
- Off-policy（Q-Learning）和 On-policy（SARSA）有什么区别？
- 为什么 CliffWalking 中 Q-Learning 走最短路径，SARSA 走安全路径？
- Q-Table 初始化和终止状态 Q=0 有什么讲究？

---

## 2. 全景位置

```
Week 1: RL 概念框架（Agent/Env/Reward/Policy/Value）
  ↓ 给出算法
Week 2 [你在这里]: MDP 框架 + Q-Learning 算法
  ↓ 给出标准环境
Week 3: Gymnasium（把 Q-Learning 接入标准接口）
  ↓
Week 4: SB3（用工业工具替代手写 Q-Learning）
  ↓
Week 5: DQN（用神经网络解决 Q-Table 的扩展性问题）
  ↓
Week 6: 期中复习（Q-Learning 是最重要的考点）
```

Week 2 是**算法核心**。Lab 1 / Lab 2 / Assignment 1 全部基于 Q-Learning，期中考试 Q-Learning 公式必考。

---

## 3. 依赖地图

```
前置（Week 1）
  ├── Policy π，Value Function Q
  ├── 折扣回报 G_t = Σ γ^k r_{t+k+1}
  └── Markov Property

Week 2 输出 → 被依赖 →
  ├── Lab 1/2: 手写 Q-Learning agent
  ├── Assignment 1: Q-Learning + BlocksWorld
  ├── Week 5: DQN 是 Q-Learning 的神经网络版
  └── Week 6: Q-Learning 更新公式 = 期中必考
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week2_mdp_slides.md](week2_mdp_slides.md) | 幻灯片笔记，含 David Silver 视频参考 | 第一次学习 |
| [week2_mdp_storyline.md](week2_mdp_storyline.md) | 叙事线索，Q-Learning 的动机推导 | 第一次学习 |
| [week2_mdp_concepts.md](week2_mdp_concepts.md) | 术语速查：MDP/Q-Learning/SARSA/Off-policy | 复习 / 考前 |
| [week2_mdp_math.md](week2_mdp_math.md) | 完整公式 + 5 个手算练习 | 做题 / 期中 |
| [week2_mdp_code.md](week2_mdp_code.md) | Q-Learning Python 实现 | 写 Lab 时 |
| [week2_mdp_tutorial.md](week2_mdp_tutorial.md) | 操作教程，手把手 CliffWalking | 做 Lab 前 |
| [week2_mdp_history.md](week2_mdp_history.md) | 历史：马尔可夫链 → 贝尔曼 → Q-Learning → SARSA | 想理解背景时 |
| [week2_mdp_quiz.md](week2_mdp_quiz.md) | 老师原版 Quiz（9 题，MDP+Bellman） | 自测 |

---

## 5. 学习路线

**第一次学习：**
1. `storyline.md` — 理解"为什么需要 Q-Learning"
2. `slides.md` — 课堂内容详情
3. `math.md` — 逐项过公式，做练习 1-2
4. `code.md` — 看 Q-Learning 代码实现
5. `tutorial.md` — 跑通 CliffWalking

**做 Lab 1 / Lab 2：**
1. `code.md` — Q-Table 更新代码参考
2. `math.md` 练习 3-5 — 熟悉手算

**期中备考（高优先级）：**
1. `concepts.md` — Off-policy vs On-policy，易错点
2. `math.md` — Q-Learning 公式默写练习
3. `quiz.md` — Bellman 方程题

---

## 6. 缺口检查

| 类型 | 状态 |
|------|------|
| 幻灯片笔记 | ✅ |
| 叙事线索 | ✅ |
| 核心概念 | ✅ |
| 数学公式 | ✅ |
| 代码参考 | ✅ |
| 操作教程 | ✅ |
| 历史背景 | ✅ |
| Quiz | ✅（来自 quize1.md） |
| 学习地图 | ✅（本文件） |
