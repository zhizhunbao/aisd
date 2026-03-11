# Week 1: 强化学习入门 学习地图

## 1. 核心问题

本讲回答：
- 强化学习是什么？和监督学习有什么不同？
- Agent / Environment / Reward 三要素是什么关系？
- 什么是 Markov Property？为什么它重要？
- Policy 和 Value Function 各是什么？

---

## 2. 全景位置

```
Week 1 [你在这里]
  ↓ 奠定概念基础
Week 2: MDP + Q-Learning（算法）
  ↓
Week 3: Gymnasium（工具）
  ↓
Week 4: SB3（工业工具）
  ↓
Week 5: DQN（神经网络 Q-Learning）
  ↓
Week 6: 期中复习
```

Week 1 是整门课的**概念地基**，没有这里的抽象框架，后续每周的算法都会看不懂。

---

## 3. 依赖地图

```
前置知识
  ├── 条件概率 P(A|B)               ← 理解随机策略 π(a|s)
  ├── 期望值 E[X]                   ← 理解 Value Function
  └── 几何级数求和                   ← 理解折扣回报 G_t 收敛性

Week 1 输出 → 被依赖 →
  ├── Week 2: MDP / Q-Learning 的符号体系
  ├── Week 3: Gymnasium reset()/step() 返回 S_t, R_t
  ├── Week 5: DQN 用神经网络近似 Q_π(s,a)
  └── Week 6: 期中考试核心考点
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week1_rl_intro_slides.md](week1_rl_intro_slides.md) | 幻灯片笔记，原始课堂内容 | 第一次学习 |
| [week1_rl_intro_storyline.md](week1_rl_intro_storyline.md) | 叙事线索，帮助理解"为什么" | 第一次学习 |
| [week1_rl_intro_concepts.md](week1_rl_intro_concepts.md) | 核心术语速查 + 易错点 | 复习 / 考前 |
| [week1_rl_intro_math.md](week1_rl_intro_math.md) | 全部公式 + 手算练习 | 做题 / 期中 |
| [week1_rl_intro_code.md](week1_rl_intro_code.md) | 代码参考 | 写代码时 |
| [week1_rl_intro_tutorial.md](week1_rl_intro_tutorial.md) | 操作教程，手把手实践 | 做 Lab 前 |
| [week1_rl_intro_history.md](week1_rl_intro_history.md) | 历史演进，理解来龙去脉 | 想了解背景时 |
| [week1_rl_intro_quiz.md](week1_rl_intro_quiz.md) | 老师原版 Quiz（15 题） | 自测 |

---

## 5. 学习路线

**第一次学习：**
1. `slides.md` — 了解本周内容框架
2. `storyline.md` — 理解 RL 的动机和直觉
3. `concepts.md` — 确认术语理解正确
4. `math.md` — 看懂公式，做手算练习

**复习 / 期中备考：**
1. `concepts.md` — 术语和易错点速查
2. `math.md` 中的手算练习
3. `quiz.md` — 做老师原版题

**扩展理解：**
- `history.md` — 了解 RL 思想从行为主义到 DQN 的演进

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
| Quiz | ✅（来自 quize2.md） |
| 学习地图 | ✅（本文件） |
