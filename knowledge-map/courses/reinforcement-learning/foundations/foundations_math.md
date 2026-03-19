---
topic: foundations
dimension: math
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.2-3 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Paper: Auer et al., 'Finite-time Analysis of the Multiarmed Bandit Problem', Machine Learning 2002 — https://link.springer.com/article/10.1023/A:1013689704352"
expiry: 12m
status: current
---

# RL 基础 数学基础

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2-3

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| s, sₜ | 时刻 t 的状态 | State | 状态空间 S |
| a, aₜ | 时刻 t 的动作 | Action | 动作空间 A |
| r, rₜ | 时刻 t 的奖励 | Reward | ℝ（实数） |
| π | 策略（状态→动作映射） | Policy | π: S → A 或 π(a\|s) |
| γ | 折扣因子（多重视未来） | Discount Factor | [0, 1] |
| Gₜ | 从 t 开始的回报 | Return | ℝ |
| T | 终止时间步 | Terminal Time Step | ℕ 或 ∞ |
| q*(a) | 动作 a 的真实期望价值 | True Action Value | ℝ |
| Qₜ(a) | 时刻 t 对 q*(a) 的估计 | Estimated Action Value | ℝ |
| Nₜ(a) | 到 t 为止选 a 的次数 | Action Count | ℕ |
| ε | 探索概率 | Exploration Rate | [0, 1] |
| c | UCB 探索系数 | UCB Exploration Coefficient | ℝ⁺ |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2-3

---

## 核心公式

### 公式 1: 折扣回报 (Discounted Return)

**直觉：** 从现在开始，把所有未来奖励加起来，但越远的奖励打越多折扣——因为未来不确定，也为了数学上不发散。

$$
G_t = r_{t+1} + \gamma \, r_{t+2} + \gamma^2 \, r_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k \, r_{t+k+1}
$$

> 📚 Book: Sutton & Barto, Eq. 3.8

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| Gₜ | t 时刻开始的总回报 | "这局游戏从现在算起能赚多少" |
| rₜ₊ₖ₊₁ | 第 t+k+1 步的即时奖励 | 每一步的得分 |
| γ | 折扣因子 | 0.9 → 10 步后的奖励只算 0.9¹⁰ ≈ 0.35 |
| k | 从当前步算起的偏移量 | 第 0, 1, 2, … 步 |

**推导过程：** 回报的递推形式

1. 定义：Gₜ = rₜ₊₁ + γ·rₜ₊₂ + γ²·rₜ₊₃ + …
2. 提取第一项后：Gₜ = rₜ₊₁ + γ·(rₜ₊₂ + γ·rₜ₊₃ + …)
3. 括号内就是 Gₜ₊₁：**Gₜ = rₜ₊₁ + γ·Gₜ₊₁**

这个递推关系是后续贝尔曼方程的基础。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3 §3.3, Eq. 3.9

### 公式 2: 样本均值估计动作价值 (Sample-Average Action Value)

**直觉：** 估计一台老虎机有多好？就是把你之前拉它获得的所有奖励取平均。拉得越多，估计越准。

$$
Q_t(a) = \frac{\sum_{i=1}^{t-1} r_i \cdot \mathbb{1}_{A_i = a}}{N_t(a)} = \frac{\text{选 } a \text{ 所得奖励总和}}{\text{选 } a \text{ 的次数}}
$$

> 📚 Book: Sutton & Barto, Eq. 2.1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| Qₜ(a) | 到时刻 t 对动作 a 价值的估计 | "我觉得这台老虎机平均能赢 $2.3" |
| rᵢ | 第 i 次交互的奖励 | 每次拉老虎机的奖金 |
| 𝟙{Aᵢ=a} | 指示函数：第 i 次选了 a 就是 1 | 标记哪些是这台机器的结果 |
| Nₜ(a) | 到 t 为止选 a 的总次数 | 这台机器拉了几次 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.1

### 公式 3: 增量更新 (Incremental Update Rule)

**直觉：** 不需要每次都重新算平均，只要每来一个新数据，就把旧估计往新数据方向"推"一小步。这个"小步"的大小就是 1/n（第 n 次更新的学习率）。

$$
Q_{n+1} = Q_n + \frac{1}{n} \bigl[ r_n - Q_n \bigr]
$$

> 📚 Book: Sutton & Barto, Eq. 2.3

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| Qₙ₊₁ | 更新后的估计 | 新的平均 |
| Qₙ | 更新前的估计 | 旧的平均 |
| 1/n | 学习率（步长） | 第 5 次更新，步长 1/5 = 0.2 |
| rₙ - Qₙ | 预测误差 | "新奖励比我预期的多了多少" |

**推导过程：**

1. 定义样本均值：Qₙ = (r₁ + r₂ + … + rₙ₋₁) / (n-1)
2. 加入第 n 个样本：Qₙ₊₁ = (r₁ + … + rₙ) / n
3. 拆开分子：= [(n-1)·Qₙ + rₙ] / n
4. 展开：= Qₙ + (rₙ - Qₙ) / n
5. 得到：**Qₙ₊₁ = Qₙ + (1/n)·[rₙ - Qₙ]**

通用形式：**NewEstimate ← OldEstimate + StepSize × [Target - OldEstimate]**

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.4, Eq. 2.3

### 公式 4: UCB 动作选择 (Upper Confidence Bound Action Selection)

**直觉：** 选动作时，不光看"我觉得它有多好"，还看"我对它有多不确定"。试得少的动作不确定性大，给它加一个"探索奖励"——越不确定越值得试。

$$
A_t = \arg\max_a \left[ Q_t(a) + c \sqrt{\frac{\ln t}{N_t(a)}} \right]
$$

> 📖 Paper: Auer et al. 2002, Theorem 1

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| Qₜ(a) | 对动作 a 的估计值 | 利用项："我觉得它值多少" |
| c | 探索系数 | c=2 是常见选择，越大越鼓励探索 |
| ln t | 总时间步的对数 | 时间越长，允许越多探索 |
| Nₜ(a) | 选 a 的次数 | 分母：试得越多，不确定性越小 |
| √(ln t / Nₜ(a)) | 探索项 (置信上界) | 试得少 → 大 → 更值得探索 |

> 📖 Paper: Auer et al., [Finite-time Analysis of the Multiarmed Bandit Problem](https://link.springer.com/article/10.1023/A:1013689704352), Machine Learning 2002

---

## 公式关系图

    样本均值（Qₜ）
         │
         ├──→ 增量更新规则（在线版本）
         │         │
         │         └──→ 通用更新公式: New ← Old + α[Target - Old]
         │                   │
         │                   └──→ 贝尔曼方程基础（→ MDP 主题）
         │
         └──→ UCB 动作选择（Qₜ + 探索项）
                   │
                   └──→ 遗憾界分析（→ Bandit Theory）

    折扣回报（Gₜ）
         │
         ├──→ 递推形式: Gₜ = rₜ₊₁ + γ·Gₜ₊₁
         │         │
         │         └──→ 贝尔曼方程（→ MDP 主题）
         │
         └──→ γ = 0: 只看眼前 │ γ → 1: 等权所有未来

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2-3

---

## 手算练习

### 练习 1: 计算折扣回报

**题目：** 一个 3 步 episode，奖励序列为 r₁=1, r₂=2, r₃=3，γ=0.9。求 G₀。

**解答步骤：**

1. 代入公式：G₀ = r₁ + γ·r₂ + γ²·r₃
2. 计算：G₀ = 1 + 0.9×2 + 0.9²×3
3. G₀ = 1 + 1.8 + 0.81×3 = 1 + 1.8 + 2.43
4. **结果：G₀ = 5.23**

验证递推：G₂ = r₃ = 3，G₁ = r₂ + γG₂ = 2 + 0.9×3 = 4.7，G₀ = r₁ + γG₁ = 1 + 0.9×4.7 = 5.23 ✅

### 练习 2: 增量更新

**题目：** 你拉了一台老虎机 4 次，奖励分别是 1, 3, 2, 4。用增量更新规则逐步计算 Q 值（Q₁=0 初始化）。

**解答步骤：**

1. n=1: Q₂ = Q₁ + (1/1)×[r₁ - Q₁] = 0 + 1×[1 - 0] = **1.0**
2. n=2: Q₃ = Q₂ + (1/2)×[r₂ - Q₂] = 1.0 + 0.5×[3 - 1.0] = 1.0 + 1.0 = **2.0**
3. n=3: Q₄ = Q₃ + (1/3)×[r₃ - Q₃] = 2.0 + 0.333×[2 - 2.0] = 2.0 + 0 = **2.0**
4. n=4: Q₅ = Q₄ + (1/4)×[r₄ - Q₄] = 2.0 + 0.25×[4 - 2.0] = 2.0 + 0.5 = **2.5**

验证：直接算均值 = (1+3+2+4)/4 = 10/4 = 2.5 ✅

### 练习 3: UCB 动作选择

**题目：** 3 个动作，t=10。Q₁₀(a₁)=2.5, Q₁₀(a₂)=3.0, Q₁₀(a₃)=1.0。选择次数 N(a₁)=5, N(a₂)=3, N(a₃)=2。c=2。选哪个？

**解答步骤：**

1. UCB(a₁) = 2.5 + 2√(ln10/5) = 2.5 + 2√(2.303/5) = 2.5 + 2×0.679 = **3.858**
2. UCB(a₂) = 3.0 + 2√(ln10/3) = 3.0 + 2√(2.303/3) = 3.0 + 2×0.876 = **4.753**
3. UCB(a₃) = 1.0 + 2√(ln10/2) = 1.0 + 2√(2.303/2) = 1.0 + 2×1.073 = **3.146**
4. **选 a₂**（UCB 值最大）—— 虽然 a₃ 试的次数最少，但它的估计值太低，探索奖励不足以弥补

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 折扣回报 | Gₜ = Σ γᵏrₜ₊ₖ₊₁ | 定义 Agent 的优化目标 | — |
| 回报递推 | Gₜ = rₜ₊₁ + γGₜ₊₁ | 递推计算回报 | 折扣回报 |
| 样本均值 | Qₜ(a) = Σrᵢ / Nₜ(a) | 估计动作价值 | — |
| 增量更新 | Q ← Q + (1/n)[r - Q] | 在线更新估计值 | 样本均值 |
| 通用更新 | Q ← Q + α[Target - Q] | 所有 RL 更新的通用形式 | 增量更新 |
| UCB 选择 | argmax[Q(a) + c√(ln t/N(a))] | 智能探索 | 样本均值 |
