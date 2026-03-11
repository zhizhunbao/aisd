# Week 5: DQN 学习地图

## 1. 核心问题

本讲回答：
- 为什么 Q-Table 在高维状态空间失效（维度诅咒）？
- DQN 的三大创新（Q-Network / Target Network / Replay Buffer）各解决什么问题？
- `DiscreteActionWrapper` 是什么，为什么 DQN 需要它？
- ε-Greedy 衰减策略如何影响训练？
- DQN 的超参数（`learning_rate`、`batch_size`、`buffer_size` 等）如何调？
- DQN vs Q-Table vs PPO：何时选哪个？

---

## 2. 全景位置

```
Week 2: 手写 Q-Learning（Q-table 版本）
  ↓ Q-Learning 的本质相同
Week 4: SB3（DQN 已内置，会用）
  ↓ 揭秘内部原理
Week 5 [你在这里]: DQN（为什么有神经网络 + 三大稳定化技巧）
  ↓
Week 6: 期中（DQN 创新点是重点考题）
```

Week 5 是从"会用"到"理解原理"的过渡，承接 Week 2 的 Q-Learning 数学和 Week 4 的 SB3 实践。

---

## 3. 依赖地图

```
前置
  ├── Week 2: Q-Learning 公式、Bellman 方程（DQN 是同一公式的神经网络版）
  ├── Week 3: Gymnasium Wrapper 机制（DiscreteActionWrapper 是 Gymnasium Wrapper）
  ├── Week 4: SB3 DQN 的外部训练流程（`learn()` / `predict()`）
  └── 深度学习基础：神经网络 forward pass（了解即可，不考推导）

Week 5 输出 → 被依赖 →
  ├── Lab 4: DQN 训练 BipedalWalker（需要 DiscreteActionWrapper）
  ├── Week 6: 期中 DQN 三大创新考题
  └── Assignment 2: 可选用 DQN 算法
```

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [week5_dqn_slides.md](week5_dqn_slides.md) | 幻灯片笔记：维度诅咒、三大创新、超参数 | 第一次学习 |
| [week5_dqn_storyline.md](week5_dqn_storyline.md) | 叙事：从 Q-Table 到 DQN 的历史演进 | 第一次学习 |
| [week5_dqn_concepts.md](week5_dqn_concepts.md) | 术语速查：三大创新定义、ε衰减、算法对比表 | 复习 / 考前 |
| [week5_dqn_math.md](week5_dqn_math.md) | DQN 损失函数、TD 误差、Bellman 对比 | 理解公式时 |
| [week5_dqn_code.md](week5_dqn_code.md) | DiscreteActionWrapper + SB3 DQN 训练代码 | 做 Lab 4 时 |
| [week5_dqn_tutorial.md](week5_dqn_tutorial.md) | 操作教程：§0-§7，从前提到 TensorBoard | 做 Lab 4 前 |
| [week5_dqn_history.md](week5_dqn_history.md) | 历史：Q-Learing(1989)→DQN(2013)→Rainbow | 想了解背景时 |

> ⚠️ **没有 Quiz**：本周没有老师提供的原版 Quiz，不生成。

---

## 5. 学习路线

**第一次学习：**
1. `storyline.md` — Q-Table 失效是理解 DQN 的起点
2. `slides.md` — 三大创新重点（§3 Q-Network，§4 Target Network，§5 Replay Buffer）
3. `concepts.md` — 确认三大创新的"问题→解决方案"对应关系
4. `math.md` — 对比 Q-Learning 和 DQN 损失函数（形式相同，参数化不同）

**做 Lab 4：**
1. `tutorial.md` — §4 DiscreteActionWrapper（Lab 的核心难点）
2. `code.md` — 复制 DiscreteActionWrapper + 训练流程
3. `tutorial.md` § 5-6 — 超参数调整和 TensorBoard 可视化

**期中备考：**
1. `concepts.md` — 三大创新速查（DQN 是最高频考点之一）
2. `math.md` — TD 误差公式（可能要求写出）
3. `week6_midterm_review_concepts.md` — 跨周高频考点汇总

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
| Quiz | ➖（无老师原版，不生成） |
| 学习地图 | ✅（本文件） |
