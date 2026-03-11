# Lab 1 CliffWalking — 数学公式 (Math)

> **See also:** [代码速查](lab1_cliffwalking_code.md) | [故事线](lab1_cliffwalking_storyline.md) | [教程](lab1_cliffwalking_tutorial.md)
> **Source:** Sutton & Barto §6.5 (Q-Learning) + §6.1 (TD Learning) + Lab 1 指导文档

---

## ★ Q-Learning 更新公式 (📚 Sutton §6.5 Eq. 6.8)

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_{a'} Q(S', a') - Q(S, A) \right]$$

| 符号 | 含义（中文） | CliffWalking 对应 | 典型值 |
|------|------------|------------------|--------|
| $Q(S,A)$ | 状态-动作对的当前估计价值 | `Q[state, action]` | 初始=0 |
| $\alpha$ | 学习率（步长） | `alpha=1`（Lab 1 演示用） | 0.1–1.0 |
| $R$ | 即时奖励 | 普通=-1, 悬崖=-100 | 见下表 |
| $\gamma$ | 折扣因子 | `gamma` | 0.9–0.99 |
| $\max_{a'} Q(S', a')$ | 下一状态的最大 Q 值 | `np.max(Q[next_state])` | — |
| $R + \gamma \max Q' - Q(S,A)$ | **TD 误差 (TD Error)** | — | 目标 - 估计 |

---

## ★ CliffWalking 奖励结构 (📚 Sutton p.132)

$$R(s, a) = \begin{cases} -100 & \text{掉入悬崖（底行 } x \in [1,10]\text{）} \\ 0 & \text{到达目标 G（底行 } x=11\text{）} \\ -1 & \text{其他所有步骤} \end{cases}$$

> ⚠️ **注意：** Sutton 原书目标奖励为 0（达到终止即停止，最后 step 返回 -1）。Lab 1 代码中 `done=True` 时不会再执行 step，所以终止状态等效。

---

## ★ 状态索引转换

$$\text{state} = y \times \text{width} + x = y \times 12 + x$$

$$x = \text{state} \mod 12, \quad y = \text{state} \div 12 \text{ (整除)}$$

| 关键位置 | 坐标 $(x, y)$ | state 整数 |
|---------|--------------|------------|
| 起点 S | $(0, 3)$ | $3 \times 12 + 0 = 36$ |
| 目标 G | $(11, 3)$ | $3 \times 12 + 11 = 47$ |
| 悬崖首格 | $(1, 3)$ | $3 \times 12 + 1 = 37$ |
| 悬崖末格 | $(10, 3)$ | $3 \times 12 + 10 = 46$ |
| 左上角 | $(0, 0)$ | $0$ |

---

## ★ Q-Table 大小

$$|Q\text{-Table}| = |S| \times |A| = 48 \times 4 = 192$$

| 维度 | 值 | 说明 |
|------|-----|------|
| 状态数 $\|S\|$ | $4 \times 12 = 48$ | 4行×12列网格 |
| 动作数 $\|A\|$ | $4$ | 左/右/上/下 |
| Q-Table 元素总数 | $192$ | `np.zeros((48, 4))` |

---

## ★ ε-Greedy 探索策略

$$a = \begin{cases} \text{random action} & \text{with probability } \varepsilon \\ \arg\max_{a'} Q(s, a') & \text{with probability } 1 - \varepsilon \end{cases}$$

| $\varepsilon$ 值 | 效果 |
|-----------------|------|
| $\varepsilon = 1$ | 纯随机探索 |
| $\varepsilon = 0$ | 纯贪婪利用 |
| $\varepsilon$ 衰减 | 早期探索 → 后期利用 |

---

## ★ 折扣回报 (📚 Sutton §3.3)

$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

**递归形式：**
$$G_t = R_{t+1} + \gamma G_{t+1}$$

---

## 📝 手算 1：Q-Learning 更新

**题目：** $\alpha=0.5$, $\gamma=0.9$. 当前 $Q(\text{state}=36, \text{right}) = -5.0$（起点向右走）。执行右移，未到悬崖，$R=-1$，到达 $s'=37$（悬崖首格）。$\max_{a'} Q(37, a') = -20.0$。求更新后的 Q 值。

**解：**

Step 1: TD target = $R + \gamma \max Q' = -1 + 0.9 \times (-20.0) = -1 - 18 = -19$

Step 2: TD error = $-19 - Q(36, \text{right}) = -19 - (-5.0) = -14$

Step 3: $Q(36, \text{right}) \leftarrow -5.0 + 0.5 \times (-14) = -5.0 - 7.0 = -12.0$

> **解读：** Q 值从 -5 降至 -12，说明智能体"学到了"从起点向右走很危险（接近悬崖）。

---

## 📝 手算 2：CliffWalking 掉崖后的更新

**题目：** $\alpha=0.1$, $\gamma=0.9$. Agent 在状态 $s=36$（起点）执行右移，掉入悬崖，$R=-100$，返回起点 $s'=36$。$\max_{a'} Q(36, a') = -2.0$。当前 $Q(36, \text{right}) = 0$。

**解：**

Step 1: TD target = $-100 + 0.9 \times (-2.0) = -100 - 1.8 = -101.8$

Step 2: TD error = $-101.8 - 0 = -101.8$

Step 3: $Q(36, \text{right}) \leftarrow 0 + 0.1 \times (-101.8) = -10.18$

> **注意：** 掉崖后 `done` 仍为 False，episode 继续从起点出发。这与到达目标的 `done=True` 不同。
