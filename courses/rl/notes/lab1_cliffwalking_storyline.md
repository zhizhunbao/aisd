# Lab 1 故事线：手写 Q-Learning — 从 Bellman 方程到 CliffWalking

> **Source:** `CST8509_Lab1_CliffWalking.md`
> **核心问题：** 不依赖任何框架，你能从零手写一个能学会走悬崖的 Q-Learning agent 吗？
> **前置知识：** [Week 1 RL 入门](week1_rl_intro_storyline.md) | [Week 2 MDP](week2_mdp_storyline.md)
> **代码速查：** [lab1_cliffwalking_code.md](lab1_cliffwalking_code.md)
> **后续：** [Lab 2 Gymnasium](lab2_gymnasium_storyline.md)

---

## 🗺️ 路线图 (Roadmap)

```
Hybrid Activity 1              Lab 1                          Lab 2
┌──────────────────┐    ┌─────────────────────┐    ┌──────────────────────────┐
│ 简单方形网格       │ →  │ CliffWalking 4×12   │ →  │ Gymnasium 标准接口        │
│ 无边界、无悬崖    │    │ 悬崖 -100 奖励       │    │ 同一 Q-Learning + 标准化  │
│ 完全随机初始化    │    │ 每步 -1 奖励         │    │ 兼容 SB3 算法             │
│ 理解 Q-table 原理 │    │ ε-greedy + 衰减      │    │                          │
└──────────────────┘    └─────────────────────┘    └──────────────────────────┘
```

---

## 📖 因果叙事 (Causal Narrative)

### 第一章：为什么要手写？

**Hybrid Activity 1 的任务：** 先读懂一个最简单的 Q-Learning 示例——方形网格，Q-table 是一个二维列表，没有任何库，没有框架，纯 Python。

**这样做的目的：**
- 不用任何黑盒，你能完整看到 Bellman 方程的每一次计算
- 理解 Q-table 是"状态 × 动作"的价值估计表，而不是神经网络
- 掌握 ε-greedy 探索的实现细节

**Lab 1 的任务：** 在这个手写基础上，修改环境使其符合 Sutton 教材 P132 的 CliffWalking 问题。

---

### 第二章：CliffWalking 问题的定义

**网格布局（4 行 × 12 列）：**

```
. . . . . . . . . . . .   ← row 0 (top)
. . . . . . . . . . . .   ← row 1
. . . . . . . . . . . .   ← row 2
S X X X X X X X X X X G   ← row 3 (bottom)
```

| 符号 | 含义 | 位置 |
|------|------|------|
| `S` | 起点 Start | (x=0, y=3) — 左下角 |
| `G` | 目标 Goal | (x=11, y=3) — 右下角 |
| `X` | 悬崖 Cliff | (x=1~10, y=3) — 底行中间 10 格 |
| `.` | 普通格 | 其余 38 格 |

**奖励设计：**
- 每走一步：`reward = -1`（鼓励走最短路径）
- 掉入悬崖：`reward = -100`，**返回起点**（episode 不结束！）
- 到达目标：`done = True`，episode 结束

> 💡 **为什么悬崖奖励是 -100 而不是直接结束 episode？**
> 这正是 Q-Learning vs SARSA 行为差异的来源。掉崖但不结束，意味着 agent 还有机会从悬崖边恢复，Q-Learning（off-policy）会学到"贴着悬崖走的最短路径"，SARSA（on-policy）则因为 ε-greedy 有概率掉崖而学会"绕道走安全路径"。

---

### 第三章：状态表示——坐标→整数索引

Q-table 需要用整数作索引，但环境用 (x, y) 坐标表示位置。转换规则：

$$\text{state} = y \times \text{width} + x = y \times 12 + x$$

| 位置 | state 索引 |
|------|-----------|
| (0, 3) — 起点 S | $3 \times 12 + 0 = 36$ |
| (11, 3) — 目标 G | $3 \times 12 + 11 = 47$ |
| (1, 3) — 悬崖首格 | $3 \times 12 + 1 = 37$ |
| (0, 0) — 左上角 | $0 \times 12 + 0 = 0$ |

总状态数：$4 \times 12 = 48$

---

### 第四章：Q-Learning 更新的全过程

**一次完整的 step 流程：**

```
当前状态 state (整数)
    │
    ├── ε-greedy 选动作 action
    │       ├── 以概率 ε：随机动作（探索）
    │       └── 以概率 1-ε：argmax Q[state]（利用）
    │
    ├── env.step(action) → (next_state, reward, done)
    │       ├── 正常移动：reward=-1
    │       ├── 掉悬崖：reward=-100，返回起点，cliff=True
    │       └── 到目标：reward=-1，done=True
    │
    └── Bellman 更新（alpha=1 时简化为直接赋值）：
        Q[state][action] = reward + γ × max(Q[next_state])
```

**完整 Bellman 方程（含 alpha）：**

$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s,a) \right]$$

**当 alpha=1 时退化为：**

$$Q(s,a) \leftarrow r + \gamma \max_{a'} Q(s', a')$$

> ⚠️ **Lab 1 的代码用 alpha=1**，但只把 alpha 作为超参数标记在注释中，实际代码是直接赋值。这是有意的——演示时需要解释 alpha 的含义。

---

### 第五章：ε 衰减的作用

```
epsilon_0 = 0.1   (初始)
                   │
                   ▼  每个 episode 后：epsilon -= decay × epsilon
                   │  即：epsilon = epsilon × (1 - decay)
                   ▼
epsilon_final ≈ 0  (训练末期)
```

**直觉：** 训练初期 agent 什么都不知道，多探索是合理的。随着 Q-table 逐渐准确，应该越来越多地利用已学知识，减少随机探索。ε 衰减就是这个"从探索到利用的过渡"。

---

### 第六章：从 Lab 1 到 Lab 2 的演进

| | Lab 1（手写）| Lab 2（Gymnasium）|
|--|-------------|-----------------|
| **接口** | 自定义 `Env` 抽象类 | Gymnasium 标准 `gym.Env` |
| **`step()` 返回** | `(next_state, reward, done)` 3个值 | `(obs, reward, terminated, truncated, info)` 5个值 |
| **状态格式** | 整数（手动计算） | 字典 `{'agent': [x,y], 'target': [tx,ty]}` |
| **渲染** | 纯文本 `render()` | PyGame GUI |
| **与SB3兼容** | ❌ | ✅ |
| **总状态** | 48（4×12） | 48（同一问题） |

> 💡 **关键领悟：** Lab 1 的 `step()` 返回 3 个值，Lab 2 的 Gymnasium `step()` 返回 5 个值（`terminated` 和 `truncated` 拆分）。这是 Lab 2 中 Q-Learning agent 需要适配的最关键变化。

---

## ✅ 考试 Checklist

- [ ] CliffWalking 网格大小？→ **4 行 × 12 列 = 48 个状态**
- [ ] 悬崖奖励？每步奖励？→ 悬崖 **-100**（返回起点），普通步 **-1**
- [ ] 掉入悬崖后 episode 结束吗？→ **不结束**，返回起点继续
- [ ] 状态索引计算？→ `state = y × 12 + x`
- [ ] `alpha=1` 时 Bellman 方程简化为？→ `Q[s][a] = r + γ × max(Q[s'])`
- [ ] ε-greedy：ε 的作用？→ 以概率 ε 随机探索，防止局部最优
- [ ] ε 衰减的目的？→ 训练初期多探索，后期多利用
- [ ] Lab 1 用的是 on-policy 还是 off-policy？→ **off-policy**（Q-Learning）

---

## 📚 参考资料

| 资源 | 说明 |
|------|------|
| [Lab 1 原文](../labs/CST8509_Lab1_CliffWalking.md) | 完整实验描述 |
| [lab1_cliffwalking_code.md](lab1_cliffwalking_code.md) | 关键代码速查 |
| [Week 2 MDP 故事线](week2_mdp_storyline.md) | Bellman 方程的数学来源 |
| [Week 6 期中复习 slides](week6_midterm_review_slides.md) | 笔试样题（Q-table 更新公式） |
| [Lab 2 Gymnasium 故事线](lab2_gymnasium_storyline.md) | Lab 1 的后续 |
