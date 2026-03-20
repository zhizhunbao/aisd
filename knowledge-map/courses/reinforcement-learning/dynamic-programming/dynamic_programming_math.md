---
topic: dynamic-programming
dimension: math
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.4 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Paper: Bellman, 'Dynamic Programming', Princeton University Press 1957"
  - "📖 Paper: Howard, 'Dynamic Programming and Markov Processes', MIT Press 1960"
expiry: 12m
status: current
---

# 动态规划 数学基础

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| s, s' | 当前状态 / 下一状态 | State / Next State | 状态空间 S（有限） |
| a | 动作 | Action | 动作空间 A(s)（有限） |
| π(a\|s) | 策略：在状态 s 选动作 a 的概率 | Policy | [0, 1]，Σ_a = 1 |
| P(s'\|s,a) | 转移概率 | Transition Probability | [0, 1]，Σ_{s'} = 1 |
| R(s,a,s') | 从 (s,a) 转移到 s' 的即时奖励 | Reward | ℝ |
| γ | 折扣因子 | Discount Factor | [0, 1) |
| V^π(s) | 策略 π 下状态 s 的值 | State-Value Function | ℝ |
| Q^π(s,a) | 策略 π 下在 s 取动作 a 的值 | Action-Value Function | ℝ |
| V*(s) | 最优状态值函数 | Optimal State-Value | ℝ |
| Q*(s,a) | 最优动作值函数 | Optimal Action-Value | ℝ |
| π* | 最优策略 | Optimal Policy | — |
| θ | 收敛阈值 | Convergence Threshold | ℝ⁺ (e.g., 1e-4) |
| k | 迭代轮次 | Iteration Index | ℕ |
| Δ | 一轮中值函数最大变化量 | Max Change | ℝ⁺ |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3-4

---

## 核心公式

### 公式 1: 贝尔曼期望方程 (Bellman Expectation Equation for V^π)

**直觉：** 一个状态的"好坏"等于：按策略选动作 → 按环境概率到下一状态 → 得到的即时奖励 + 折扣后下一状态好坏的加权平均。

$$
V^\pi(s) = \sum_{a} \pi(a|s) \sum_{s'} P(s'|s,a) \left[ R(s,a,s') + \gamma \, V^\pi(s') \right]
$$

> 📚 Book: Sutton & Barto, Eq. 4.4

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| V^π(s) | 在策略 π 下从 s 出发的长期回报期望 | "按照策略走，s 值多少分" |
| π(a\|s) | 策略选动作 a 的概率 | 随机策略：π = 1/4 (4个方向等概率) |
| P(s'\|s,a) | 执行 a 后到 s' 的概率 | GridWorld: P = 1（确定性转移） |
| R(s,a,s') | 转移时的即时奖励 | GridWorld: R = -1 (每步代价) |
| γ | 折扣因子 | 0.9 → 10步后的值只算 0.35 |

**推导过程：**

1. 定义：V^π(s) = E_π[Gₜ | Sₜ=s]
2. 展开回报：= E_π[Rₜ₊₁ + γGₜ₊₁ | Sₜ=s]
3. 对动作取期望：= Σ_a π(a|s) E[Rₜ₊₁ + γGₜ₊₁ | Sₜ=s, Aₜ=a]
4. 对转移取期望：= Σ_a π(a|s) Σ_{s'} P(s'|s,a) [R(s,a,s') + γ E_π[Gₜ₊₁ | Sₜ₊₁=s']]
5. 递推关系：= Σ_a π(a|s) Σ_{s'} P(s'|s,a) [R(s,a,s') + γ V^π(s')]

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3 §3.5, Ch.4 §4.1

### 公式 2: 策略评估迭代更新 (Iterative Policy Evaluation Update)

**直觉：** 将贝尔曼期望方程变为更新规则——用旧值算新值，反复扫描直到所有值不再变。

$$
V_{k+1}(s) = \sum_{a} \pi(a|s) \sum_{s'} P(s'|s,a) \left[ R(s,a,s') + \gamma \, V_k(s') \right]
$$

> 📚 Book: Sutton & Barto, Eq. 4.5

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| V_{k+1}(s) | 第 k+1 轮的状态值（新值） | 本轮计算结果 |
| V_k(s') | 第 k 轮的状态值（旧值） | 从上轮结果读取 |
| k | 迭代轮次 | k=0 初始化，k=1,2,… 更新 |

**收敛性：** V_k → V^π 当 k → ∞（有限 MDP 中保证收敛，因为贝尔曼算子是 γ-压缩映射）

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.1

### 公式 3: 贝尔曼最优方程 (Bellman Optimality Equation for V*)

**直觉：** 最优值 = 选最好的动作 → 按环境概率到下一状态 → 即时奖励 + 折扣后下一状态的最优值。与期望方程的区别：用 max 替代策略概率加权。

$$
V^*(s) = \max_{a} \sum_{s'} P(s'|s,a) \left[ R(s,a,s') + \gamma \, V^*(s') \right]
$$

> 📚 Book: Sutton & Barto, Eq. 3.19

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| V*(s) | 状态 s 能获得的最大长期回报 | "最好情况下 s 值多少分" |
| max_a | 在所有可用动作中取最优 | 替代了 π(a\|s) 的概率加权 |

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.3 §3.6

### 公式 4: 值迭代更新 (Value Iteration Update)

**直觉：** 直接对贝尔曼最优方程迭代——每轮在每个状态取 max，不需要先评估完再改进。

$$
V_{k+1}(s) = \max_{a} \sum_{s'} P(s'|s,a) \left[ R(s,a,s') + \gamma \, V_k(s') \right]
$$

> 📚 Book: Sutton & Barto, Eq. 4.10

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| max_a | 对所有动作取最大 | 与策略评估的区别：不用策略概率，直接选最好的 |

**收敛性：** V_k → V* 当 k → ∞。收敛后从 V* 提取最优策略：π*(s) = argmax_a Σ_{s'} P(s'|s,a) [R + γV*(s')]

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.4

### 公式 5: 策略改进 — 贪心策略 (Greedy Policy from V^π)

**直觉：** 知道了每个状态的值之后，在每个状态选一步动作里 Q 值最大的那个，形成新策略。

$$
\pi'(s) = \arg\max_{a} \sum_{s'} P(s'|s,a) \left[ R(s,a,s') + \gamma \, V^\pi(s') \right] = \arg\max_{a} Q^\pi(s,a)
$$

> 📚 Book: Sutton & Barto, Eq. 4.9

**策略改进定理：** 如果对所有 s 有 Q^π(s, π'(s)) ≥ V^π(s)，则 V^{π'}(s) ≥ V^π(s)。即贪心改进后的策略至少不比原策略差。

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.2

---

## 公式关系图

    贝尔曼期望方程 (V^π)
         │
         ├──→ 策略评估迭代更新: V_{k+1} = Σπ Σ_P [R + γV_k]
         │         │
         │         └──→ 收敛后得到 V^π
         │                   │
         │                   └──→ 策略改进: π' = argmax Q^π(s,a)
         │                              │
         │                              └──→ 策略迭代 (Policy Iteration)
         │
    贝尔曼最优方程 (V*)
         │
         └──→ 值迭代更新: V_{k+1} = max_a Σ_P [R + γV_k]
                   │
                   └──→ 收敛后得到 V* → 提取 π*

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4

---

## 手算练习

### 练习 1: 策略评估 — 2 状态 MDP

**题目：** 2 个状态 {s₁, s₂}，1 个动作 {right}。转移：s₁→s₂（R=5），s₂→s₂（R=1）。γ=0.9，策略 π 只能选 right。求 V^π(s₁) 和 V^π(s₂)。

**解答步骤：**

1. 贝尔曼方程组：
   - V^π(s₁) = R(s₁→s₂) + γV^π(s₂) = 5 + 0.9·V^π(s₂)
   - V^π(s₂) = R(s₂→s₂) + γV^π(s₂) = 1 + 0.9·V^π(s₂)
2. 解 s₂：V^π(s₂) = 1/(1-0.9) = **10**
3. 代入 s₁：V^π(s₁) = 5 + 0.9×10 = **14**

验证：s₂ 的回报 = 1 + 0.9 + 0.81 + … = 1/(1-0.9) = 10 ✅

### 练习 2: 值迭代 — 2 状态 2 动作

**题目：** 2 个状态 {s₁, s₂}，2 个动作 {a, b}。转移和奖励：
- s₁, a → s₂, R=10
- s₁, b → s₁, R=2
- s₂, a → s₁, R=1
- s₂, b → s₂, R=3

γ=0.5，V₀(s₁)=V₀(s₂)=0。做 2 轮值迭代。

**解答步骤：**

**第 1 轮 (k=0→1):**
- V₁(s₁) = max(R(s₁,a)+γV₀(s₂), R(s₁,b)+γV₀(s₁)) = max(10+0, 2+0) = **10**
- V₁(s₂) = max(R(s₂,a)+γV₀(s₁), R(s₂,b)+γV₀(s₂)) = max(1+0, 3+0) = **3**

**第 2 轮 (k=1→2):**
- V₂(s₁) = max(10+0.5×3, 2+0.5×10) = max(11.5, 7) = **11.5**
- V₂(s₂) = max(1+0.5×10, 3+0.5×3) = max(6, 4.5) = **6**

最优策略趋势：π*(s₁)=a, π*(s₂)=a

### 练习 3: 4×4 GridWorld 策略评估 (一步)

**题目：** Sutton & Barto Example 4.1：4×4 GridWorld，终止状态在左上角和右下角。随机策略 π = 1/4 (等概率上下左右)。γ=1，R=-1 每步。V₀=0。对状态 (1,0)（第二行第一列）做一步策略评估更新。

**解答步骤：**

1. 状态 (1,0) 的四个邻居：
   - 上 → (0,0) 终止态，V=0，R=-1
   - 下 → (2,0)，V₀=0，R=-1
   - 左 → 撞墙回 (1,0)，V₀=0，R=-1
   - 右 → (1,1)，V₀=0，R=-1
2. 更新：V₁(1,0) = 1/4 × [(-1+0) + (-1+0) + (-1+0) + (-1+0)] = 1/4 × (-4) = **-1**

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 Example 4.1

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 贝尔曼期望方程 | V^π(s) = Σ_a π(a\|s) Σ_{s'} P[R + γV^π(s')] | 定义给定策略的值 | 回报定义 Gₜ |
| 策略评估更新 | V_{k+1}(s) = Σ_a π Σ_P [R + γV_k(s')] | 迭代计算 V^π | 贝尔曼期望 |
| 贝尔曼最优方程 | V*(s) = max_a Σ_{s'} P[R + γV*(s')] | 定义最优值函数 | 贝尔曼期望 |
| 值迭代更新 | V_{k+1}(s) = max_a Σ_P [R + γV_k(s')] | 直接计算 V* | 贝尔曼最优 |
| 策略改进 | π'(s) = argmax_a Q^π(s,a) | 从 V^π 提取更好策略 | 策略评估 |
| Q 值从 V 计算 | Q^π(s,a) = Σ_{s'} P[R + γV^π(s')] | 评估单个动作 | V^π |
