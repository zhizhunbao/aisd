# Markov Chains & MDP | 马尔可夫链与马尔可夫决策过程

> **Purpose:** Define Markov chains (stochastic processes with memoryless transitions) and extend to MDPs (adding actions and rewards) — the mathematical foundation of all reinforcement learning.
> **Primary Source:** Sutton & Barto, _Reinforcement Learning_ (2nd ed.), Ch. 3; David Silver, UCL RL Course, Lectures 1–2; Grinstead & Snell, _Introduction to Probability_, Ch. 11
> **See also:** [conditional_probability.md](conditional_probability.md) | [geometric_series.md](../calculus/geometric_series.md) | [argmax.md](../general/argmax.md)
> **Prerequisites:** [Conditional Probability](conditional_probability.md) — you need $P(A \mid B)$ to read this file.

---

## Notation (符号约定)

| Symbol        | Meaning (EN)              | 含义 (中文)        |
| ------------- | ------------------------- | ------------------ |
| $\mathcal{S}$ | Set of all states         | 状态集合           |
| $\mathcal{A}$ | Set of all actions        | 动作集合           |
| $P(\cdot)$    | Probability               | 概率               |
| $s, s'$       | Current state, next state | 当前状态，下一状态 |
| $a$           | Action                    | 动作               |
| $r$           | Reward                    | 奖励               |
| $t$           | Time step                 | 时间步             |

---

## §1 Markov Property (马尔可夫性质)

> 📚 Source: Sutton §3.1, p. 69; David Silver L1 Slide 21 (p. 21), "Information State"
> 📚 Also: Grinstead §11.1, p. 405 — "Markov Chains"

### 1.1 Definition (定义)

A state $S_t$ has the **Markov property** if and only if the future depends only on the present, not on the past:

一个状态 $S_t$ 具有**马尔可夫性质**，当且仅当未来仅取决于当前，与过去无关：

| Symbol    | Meaning (EN)                 | 含义 (中文)       | Type              |
| --------- | ---------------------------- | ----------------- | ----------------- |
| $S_t$     | State at time $t$            | 时间步 $t$ 的状态 | $\in \mathcal{S}$ |
| $S_{t+1}$ | Next state                   | 下一个状态        | $\in \mathcal{S}$ |
| $R_{t+1}$ | Reward received at next step | 下一步收到的奖励  | $\in \mathbb{R}$  |

$$P(S_{t+1}, R_{t+1} \mid S_t) = P(S_{t+1}, R_{t+1} \mid S_0, S_1, \ldots, S_t)$$

> 📖 **Reading the notation:** "The probability of the next state and reward given the current state equals the probability given the _entire_ history." In other words, $S_t$ alone contains all the information needed to predict the future — knowing $S_0, S_1, \ldots, S_{t-1}$ gives no additional predictive power.
> 📖 **读符号：** "给定当前状态后，下一步的概率 = 给定完整历史后的概率。" 也就是说，当前状态包含了预测未来所需的全部信息。

David Silver calls this an **information state** (a.k.a. Markov state): "A state $S_t$ is Markov if and only if $P[S_{t+1} \mid S_t] = P[S_{t+1} \mid S_1, \ldots, S_t]$" — once the state is known, the history may be thrown away. The state is a **sufficient statistic** of the future.

> 📚 David Silver L1 Slide 21: "$H_{1:t} \to S_t \to H_{t+1:\infty}$" — the state blocks the past from the future.
> 📚 Silver also notes: "The environment state $S_t^e$ is Markov" and "The history $H_t$ is Markov" (trivially).

### 1.2 Intuition (直觉理解)

**One-sentence version:** "The future is independent of the past given the present."
**一句话版：** "给定现在，未来与过去无关。"

**Physical analogy (Sutton §3.1, David Silver L1):** In classical mechanics, a particle's future trajectory is fully determined by its current **position + velocity**. Knowing where it was 5 seconds ago adds nothing.

| State definition              | Markov? | Why?                                                             |
| ----------------------------- | ------- | ---------------------------------------------------------------- |
| Position only                 | ❌ No   | Don't know direction/speed → can't predict next position         |
| Position + velocity           | ✅ Yes  | Sufficient to compute all future positions (Newton's laws)       |
| Full history of all positions | ✅ Yes  | Trivially Markov (contains everything), but wastefully redundant |

> 📚 Sutton §3.1, p. 69: "The state must include information about all aspects of the past agent–environment interaction that make a difference for the future."

> 🔗 **Course Connection:**
>
> - **RL W1:** The Markov property is the foundational assumption — Slides p. 25, Quiz 1 Q3
> - **RL W2 MDP:** All Bellman equations assume Markov states

### 1.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** A robot navigates a grid. Its state is defined as its $(x, y)$ position. Is this a Markov state if the robot has momentum (i.e., the speed matters for its next position)?

一个机器人在网格中导航。状态定义为 $(x, y)$ 位置。如果机器人有惯性（速度影响下一个位置），这是马尔可夫状态吗？

> 📐 Original Problem — based on Sutton §3.1 particle example

> 💡 **Hint:** Does knowing only $(x, y)$ tell you which direction and how fast the robot is moving?

**Solution:**

**No.** Position alone is not Markov when momentum exists. The robot at $(3, 2)$ moving right at speed 2 will be at $(5, 2)$ next step, but a robot at $(3, 2)$ moving up at speed 1 will be at $(3, 3)$. Same current position, different futures → not Markov. Need state = $(x, y, v_x, v_y)$.

不是。仅位置在有惯性时不满足马尔可夫性。需要状态 = $(x, y, v_x, v_y)$。

#### 🟡 Medium | 中等题

**P2.** A chess game has been going on for 40 moves. The current board position is state $S_{40}$. Argue whether $S_{40}$ (the current board layout) satisfies the Markov property. Consider: does the board position alone determine all legal future moves and their consequences?

> 📐 Original Problem — inspired by David Silver Lecture 1 discussion

> 💡 **Hint:** Think about castling rights and en passant — these depend on move history, not just piece positions.

**Solution:**

**Almost but not quite.** The board position alone determines most legal moves, but NOT:

- **Castling rights** (requires knowing if king/rook have previously moved)
- **En passant** (requires knowing if opponent's last move was a two-square pawn advance)
- **Threefold repetition** / **50-move rule** (requires move history)

To make it truly Markov, the state must include: board position + castling flags + en passant square + move counters. This is exactly what chess engines do (e.g., FEN notation).

This illustrates Sutton's point: "the programmer is responsible for choosing the state function $f$" (Slides p. 24).

---

## §2 Markov Chain (马尔可夫链)

> 📚 Source: Grinstead §11.1, pp. 405–408; Murphy PML2 §2.6

### 2.1 Definition (定义)

A **Markov chain** is a sequence of random variables $S_0, S_1, S_2, \ldots$ where each state transition depends only on the current state:

**马尔可夫链**是一列随机变量 $S_0, S_1, S_2, \ldots$，每次状态转移仅取决于当前状态：

| Symbol        | Meaning (EN)                               | 含义 (中文)                      | Type                        |
| ------------- | ------------------------------------------ | -------------------------------- | --------------------------- |
| $\mathcal{S}$ | Finite set of states                       | 有限状态集合                     | $\{s_1, s_2, \ldots, s_n\}$ |
| $P_{ij}$      | Transition probability from $s_i$ to $s_j$ | 从状态 $s_i$ 到 $s_j$ 的转移概率 | $\in [0, 1]$                |
| $\mathbf{P}$  | Transition matrix                          | 转移矩阵                         | $n \times n$                |

$$P_{ij} = P(S_{t+1} = s_j \mid S_t = s_i)$$

> 📖 **Reading the notation:** "$P_{ij}$" means "the probability of going from state $i$ to state $j$ in one step." Row $i$, column $j$ of the transition matrix.

**Key constraint (关键约束):** Each row of $\mathbf{P}$ sums to 1:

$$\sum_{j=1}^{n} P_{ij} = 1 \quad \forall \ i$$

> 📚 Grinstead §11.1, p. 405: "A Markov chain is a process that moves among the elements of a set of states in a series of steps."

### 2.2 Worked Example: Weather (手算例题：天气)

> 📚 Adapted from Grinstead §11.1, p. 406 — Example 11.1

**Problem:** Tomorrow's weather depends only on today. Sunny (☀️) stays sunny 80%, Rain (🌧️) stays rainy 60%.

|          | ☀️ Tomorrow | 🌧️ Tomorrow |
| -------- | ----------- | ----------- |
| ☀️ Today | 0.8         | 0.2         |
| 🌧️ Today | 0.4         | 0.6         |

$$\mathbf{P} = \begin{pmatrix} 0.8 & 0.2 \\ 0.4 & 0.6 \end{pmatrix}$$

If today is sunny, what is $P(\text{rain in 2 days})$?

**Solution:**

Two paths to rain on day 2:

$$P(\text{rain}_2 \mid \text{sun}_0) = P(\text{sun}_1 \mid \text{sun}_0) \cdot P(\text{rain}_2 \mid \text{sun}_1) + P(\text{rain}_1 \mid \text{sun}_0) \cdot P(\text{rain}_2 \mid \text{rain}_1)$$

$$= 0.8 \times 0.2 + 0.2 \times 0.6 = 0.16 + 0.12 = 0.28$$

Or equivalently: $\mathbf{P}^2_{1,2} = 0.28$ (row 1, col 2 of $\mathbf{P}^2$).

> ⚠️ **Note:** This is why the Markov property matters for computation — we only need the current state, not the full weather history.

> 🔗 **Course Connection:**
>
> - **RL W1:** Markov chain = the simplest model of sequential state transitions (Quiz 1 Q1)
> - **RL W2:** MDP extends this by adding actions and rewards to each transition

### 2.3 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P3.** Given the weather transition matrix above, if today is rainy (🌧️), what is the probability of sun tomorrow?

用上面的天气转移矩阵，如果今天下雨，明天晴天的概率是多少？

> 📚 From: Grinstead §11.1, adapted from Example 11.1

> 💡 **Hint:** Look at the rain row (row 2) of $\mathbf{P}$.

**Solution:**

$P(\text{sun tomorrow} \mid \text{rain today}) = P_{21} = 0.4$

Directly read from row 2 (rain), column 1 (sun) of $\mathbf{P}$.

#### 🟡 Medium | 中等题

**P4.** Write the transition matrix for a 3-state system: states {A, B, C}. From A: 50% stay, 50% go to B. From B: 30% go to A, 70% go to C. From C: 100% go to A. Verify each row sums to 1.

> 📐 Original Problem — based on Grinstead §11.1 format

> 💡 **Hint:** Each row represents one starting state. Fill in probabilities, ensure $\sum = 1$.

**Solution:**

$$\mathbf{P} = \begin{pmatrix} 0.5 & 0.5 & 0.0 \\ 0.3 & 0.0 & 0.7 \\ 1.0 & 0.0 & 0.0 \end{pmatrix}$$

Row sums: $0.5+0.5+0.0=1$ ✓ | $0.3+0.0+0.7=1$ ✓ | $1.0+0.0+0.0=1$ ✓

---

## §3 Markov Decision Process / MDP (马尔可夫决策过程)

> 📚 Source: Sutton §3.1, pp. 69–74 — "The Agent–Environment Interface"
> 📚 Also: David Silver L1 Slide 23 (MDP = fully observable), L2 Slides 5–9 (MDP formal definition); Barber §7.5

### 3.1 Definition (定义)

An MDP extends the Markov chain by adding **actions** (agent choices) and **rewards** (feedback signals):

MDP 在马尔可夫链的基础上增加了 **动作**（智能体的选择）和 **奖励**（反馈信号）：

| Symbol               | Meaning (EN)       | 含义 (中文)       | Type             |
| -------------------- | ------------------ | ----------------- | ---------------- |
| $\mathcal{S}$        | Set of states      | 状态集合          | finite           |
| $\mathcal{A}$        | Set of actions     | 动作集合          | finite           |
| $p(s', r \mid s, a)$ | Dynamics function  | 动力学函数        | probability      |
| $R_t$                | Reward at time $t$ | 时间步 $t$ 的奖励 | $\in \mathbb{R}$ |

> 📖 **Markov Chain vs MDP:**
>
> - Markov Chain: $P(S_{t+1} \mid S_t)$ — state transitions happen automatically
> - MDP: $p(s', r \mid s, a)$ — an **agent** chooses action $a$, which affects the transition

**The MDP dynamics function (MDP 动力学函数):**

$$p(s', r \mid s, a) \doteq P(S_{t+1}=s', R_{t+1}=r \mid S_t=s, A_t=a)$$

> 📖 **Reading "$\doteq$":** This symbol means "is defined as" (left side is defined to be the right side).
> 📖 **读 "$\doteq$"：** 这个符号表示"定义为"（左边被定义为右边）。

> 📚 Sutton §3.1, Eq. 3.2, p. 70

**David Silver's notation (Silver L1 Slide 29, L2 Slides 7–8):**

Silver uses a different but equivalent notation, splitting the dynamics into two models:

- **Transition model (转移模型):** $\mathcal{P}^a_{ss'} = P[S_{t+1} = s' \mid S_t = s, A_t = a]$
- **Reward model (奖励模型):** $\mathcal{R}^a_s = E[R_{t+1} \mid S_t = s, A_t = a]$

> 📚 David Silver L1 Slide 29: "$\mathcal{P}$ predicts the next state; $\mathcal{R}$ predicts the next (immediate) reward"

Both notations are equivalent — Sutton's $p(s', r \mid s, a)$ bundles state transition and reward into one function, while Silver separates them. Your course slides use Silver's notation.

**Key constraint:** For each state-action pair, probabilities sum to 1:

$$\sum_{s' \in \mathcal{S}} \sum_{r \in \mathcal{R}} p(s', r \mid s, a) = 1, \quad \forall\ s \in \mathcal{S}, \ a \in \mathcal{A}(s)$$

> 📚 Sutton §3.1, Eq. 3.3, p. 70

### 3.2 Derived Quantities (派生量)

From $p(s', r \mid s, a)$, we can derive three useful functions:

从 $p(s', r \mid s, a)$ 可以推导出三个有用的函数：

**State-transition probability (状态转移概率):**

$$p(s' \mid s, a) \doteq \sum_{r \in \mathcal{R}} p(s', r \mid s, a)$$

> 📚 Sutton §3.1, Eq. 3.4, p. 71

**Expected reward for state-action pair (状态-动作对的期望奖励):**

$$r(s, a) \doteq \mathbb{E}[R_{t+1} \mid S_t=s, A_t=a] = \sum_{r \in \mathcal{R}} r \sum_{s' \in \mathcal{S}} p(s', r \mid s, a)$$

> 📚 Sutton §3.1, Eq. 3.5, p. 71

**Expected reward for state-action-next_state triple (三元组的期望奖励):**

$$r(s, a, s') \doteq \mathbb{E}[R_{t+1} \mid S_t=s, A_t=a, S_{t+1}=s'] = \frac{\sum_{r \in \mathcal{R}} r \cdot p(s', r \mid s, a)}{p(s' \mid s, a)}$$

> 📚 Sutton §3.1, Eq. 3.6, p. 71

### 3.3 Intuition: Markov Chain → MDP (直觉理解)

|                     | Markov Chain       | MDP                                                    |
| ------------------- | ------------------ | ------------------------------------------------------ |
| **Who decides?**    | Nature (automatic) | Agent (chooses action)                                 |
| **Transition**      | $P(s' \mid s)$     | $p(s', r \mid s, a)$ or $\mathcal{P}^a_{ss'}$          |
| **Reward**          | ❌ None            | ✅ $r$ at each step ($\mathcal{R}^a_s$)                |
| **Goal**            | Model/predict      | Maximize cumulative reward                             |
| **Example**         | Weather forecast   | Robot learning to navigate                             |
| **Silver notation** | —                  | $\mathcal{P}^a_{ss'}$, $\mathcal{R}^a_s$ (L1 Slide 29) |

> 💡 **Think of it this way:** A Markov chain is like watching raindrops slide down a window — you can predict their path, but you can't control it. An MDP is like driving a car in that rain — _you_ choose which turn to take, and the GPS (reward) tells you if you're getting closer to your destination.

**MDP vs POMDP** (David Silver L1 Slides 23–24):

- **MDP** = fully observable: agent directly sees environment state ($O_t = S^a_t = S^e_t$)
- **POMDP** = partially observable: agent only sees observations, must infer state
- This course focuses on MDPs.

> 📚 David Silver L1 Slide 23: "Full observability... Formally, this is a Markov decision process (MDP)"

> 🔗 **Course Connection:**
>
> - **RL W1:** Quiz 1 Q2 — "MDP = Markov chain + actions + rewards"
> - **RL W2:** Bellman equations are derived from the MDP dynamics function $p(s', r \mid s, a)$
> - **RL W1 Lab 1:** Cliff Walking is a concrete MDP: states = grid cells, actions = {up, down, left, right}, rewards = {-1 per step, -100 for cliff}

### 3.4 Worked Example: Recycling Robot (手算例题：回收机器人)

> 📚 Adapted from Sutton §3.1, Example 3.3, pp. 72–73

**Problem:** A recycling robot has 2 states: {high battery, low battery} and 3 actions: {search, wait, recharge}.

| State | Action   | Next State | Probability  | Reward              |
| ----- | -------- | ---------- | ------------ | ------------------- |
| high  | search   | high       | $\alpha$     | $r_{\text{search}}$ |
| high  | search   | low        | $1 - \alpha$ | $r_{\text{search}}$ |
| high  | wait     | high       | 1            | $r_{\text{wait}}$   |
| low   | search   | high       | $1 - \beta$  | $-3$ (rescued)      |
| low   | search   | low        | $\beta$      | $r_{\text{search}}$ |
| low   | wait     | low        | 1            | $r_{\text{wait}}$   |
| low   | recharge | high       | 1            | 0                   |

With $\alpha = 0.7, \beta = 0.4, r_{\text{search}} = 2, r_{\text{wait}} = 1$:

$$p(\text{high}, 2 \mid \text{high}, \text{search}) = 0.7$$
$$p(\text{low}, 2 \mid \text{high}, \text{search}) = 0.3$$

Verify: $0.7 + 0.3 = 1.0$ ✓

Expected reward: $r(\text{high}, \text{search}) = 0.7 \times 2 + 0.3 \times 2 = 2.0$

### 3.5 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P5.** In Cliff Walking (Lab 1), identify: (a) $\mathcal{S}$, (b) $\mathcal{A}$, (c) $p(s', r \mid s, a)$ for the action "right" at position $(0, 3)$ (start).

在 Cliff Walking 中，识别：(a) 状态集 (b) 动作集 (c) 从起点 $(0, 3)$ 向右的转移概率。

> 📚 From: Lab 1 Cliff Walking environment, connected to Sutton §3.1

> 💡 **Hint:** The grid is 4×12. Actions are {up, down, left, right}. Moving right from start (0,3) lands on cliff column 1.

**Solution:**

(a) $\mathcal{S} = \{0, 1, 2, \ldots, 47\}$ (4×12 = 48 states)

(b) $\mathcal{A} = \{\text{up, down, left, right}\}$ (4 actions)

(c) Moving right from $(0, 3)$: next position is $(1, 3)$ — this is the **cliff**!
$$p(\text{start}, -100 \mid (0,3), \text{right}) = 1.0$$
The agent falls into the cliff, receives $r = -100$, and is sent back to start. This is a **deterministic** MDP ($p = 1$).

#### 🔴 Hard | 挑战题

**P6.** The Sutton dynamics function $p(s', r \mid s, a)$ is a 4-argument function. Explain why a simpler $p(s' \mid s, a)$ is insufficient for defining an MDP. What information would be lost?

Sutton 的动力学函数 $p(s', r \mid s, a)$ 有 4 个参数。解释为什么更简单的 $p(s' \mid s, a)$ 不足以定义 MDP。

> 📐 Original Problem — based on Sutton §3.1 discussion

> 💡 **Hint:** Think about whether different rewards can occur for the same state transition.

**Solution:**

$p(s' \mid s, a)$ only tells us _where_ we go, not _what reward_ we get. In general, the same transition $(s, a) \to s'$ could produce different rewards. For example, a robot moving forward might arrive at the same cell but receive different rewards depending on whether it picked up an object along the way.

The full $p(s', r \mid s, a)$ jointly specifies the probability of **both** the next state _and_ the reward, allowing for stochastic rewards. From this single function, we can derive $p(s' \mid s, a)$, $r(s, a)$, and $r(s, a, s')$ (Sutton Eqs. 3.4–3.6), but not the reverse.

In Lab 1 Cliff Walking, rewards are deterministic given the transition, so $p(s' \mid s, a)$ + a deterministic reward function would suffice. But Sutton's general formulation handles stochastic rewards too.

---

## §4 Stochastic vs Deterministic Transitions (随机 vs 确定性转移)

> 📚 Source: Sutton §3.1, p. 69; David Silver Lecture 1; Quiz 1 Q3

### 4.1 Key Distinction (关键区分)

A common misconception: "taking action $a$ in state $s$ always leads to the same next state."

一个常见误解："在状态 $s$ 采取动作 $a$ 总是到达相同的下一状态。"

This is **FALSE** for general MDPs (Quiz 1 Q3).

| Type          | Transition                                 | Example                               |
| ------------- | ------------------------------------------ | ------------------------------------- |
| Deterministic | $p(s' \mid s, a) = 1$ for exactly one $s'$ | Cliff Walking grid movement           |
| Stochastic    | $p(s' \mid s, a) < 1$ for multiple $s'$    | Slippery Frozen Lake, recycling robot |

> 📚 Sutton §3.1, p. 69: The dynamics function $p$ defines a probability distribution, not a deterministic mapping.
> Quiz 1 Q3: "In a MDP, taking an action in a state always leads to the same result state." → **FALSE**

> 🔗 **Course Connection:**
>
> - **RL W1 Quiz 1 Q3:** This is a direct exam question — answer is FALSE
> - **RL W2:** Bellman equation uses $\sum_{s'} p(s' \mid s, a)$ — the sum only matters when transitions are stochastic

### 4.2 Practice Problems (练习题)

#### 🟡 Medium | 中等题

**P7.** The "Frozen Lake" environment has a 4×4 grid with ice. When the agent tries to move right, there is a 1/3 chance of sliding left, 1/3 straight, 1/3 right. Write $p(s' \mid s, a)$ for action "right" at state $s=5$ (grid position (1,1)) on a 4×4 grid, assuming no walls block movement.

> 📐 Original Problem — based on OpenAI Gymnasium's FrozenLake-v1

> 💡 **Hint:** "Right" attempt → could go up (1/3), right (1/3), or down (1/3) due to slippery ice. Position (1,1) on 4×4 grid.

**Solution:**

State $s=5$ is position (1,1). Action = right. Due to slippery ice:

- $p(s'=1 \mid s=5, \text{right}) = 1/3$ (slid up to (0,1))
- $p(s'=6 \mid s=5, \text{right}) = 1/3$ (moved right to (1,2))
- $p(s'=9 \mid s=5, \text{right}) = 1/3$ (slid down to (2,1))

Sum: $1/3 + 1/3 + 1/3 = 1$ ✓. This is a stochastic MDP.

---

## Quick Reference (速查表)

| Concept                   | Formula                                                                | Source          | Used In                   |
| ------------------------- | ---------------------------------------------------------------------- | --------------- | ------------------------- |
| Markov property           | $P(S_{t+1} \mid S_t) = P(S_{t+1} \mid S_0, \ldots, S_t)$               | Sutton §3.1     | All RL                    |
| Transition matrix row sum | $\sum_j P_{ij} = 1$                                                    | Grinstead §11.1 | Markov chain verification |
| MDP dynamics              | $p(s', r \mid s, a) \doteq P(S_{t+1}=s', R_{t+1}=r \mid S_t=s, A_t=a)$ | Sutton Eq. 3.2  | Bellman equations         |
| State-transition prob     | $p(s' \mid s, a) = \sum_r p(s', r \mid s, a)$                          | Sutton Eq. 3.4  | Policy evaluation         |
| Expected reward           | $r(s, a) = \sum_r r \sum_{s'} p(s', r \mid s, a)$                      | Sutton Eq. 3.5  | Bellman derivation        |
| MDP completeness          | $\sum_{s'} \sum_r p(s', r \mid s, a) = 1$                              | Sutton Eq. 3.3  | MDP verification          |

---

## Source Index (来源索引)

| Section            | Textbook          | Chapter/Section                                     | Pages/Slides |
| ------------------ | ----------------- | --------------------------------------------------- | ------------ |
| §1 Markov property | Sutton & Barto    | §3.1                                                | pp. 69–70    |
| §1 Markov property | David Silver L1   | Slide 21 ("Information State")                      | p. 21        |
| §1 Markov property | David Silver L1   | Slides 18–20 (History, State)                       | pp. 18–20    |
| §2 Markov chain    | Grinstead & Snell | §11.1                                               | pp. 405–408  |
| §2 Markov chain    | Murphy PML2       | §2.6                                                | —            |
| §3 MDP definition  | Sutton & Barto    | §3.1, Eqs. 3.2–3.6                                  | pp. 69–74    |
| §3 MDP notation    | David Silver L1   | Slide 29 ($\mathcal{P}^a_{ss'}$, $\mathcal{R}^a_s$) | p. 29        |
| §3 MDP vs POMDP    | David Silver L1   | Slides 23–24                                        | pp. 23–24    |
| §3 Recycling robot | Sutton & Barto    | §3.1, Ex. 3.3                                       | pp. 72–73    |
| §3 MDP             | Barber            | §7.5                                                | —            |
| §4 Stochastic      | Sutton & Barto    | §3.1                                                | p. 69        |
| §4 Quiz connection | Course Quiz 1     | Q3                                                  | —            |
