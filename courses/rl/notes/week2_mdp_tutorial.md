# Week 2 教程：MDP 的形式化定义与 Bellman 方程推导

> **数学前置：** [马尔可夫链与MDP](../../math/probability/markov_chains.md) | [几何级数与折扣回报](../../math/calculus/geometric_series.md) | [Argmax](../../math/general/argmax.md)
> **教科书来源：** Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.), Chapters 3 & 6

本教程补充 Slides 未深入讲解的内容，基于 Sutton & Barto 教科书 Chapter 3（MDP 框架）和 Chapter 6（TD 学习）。

---

## §0 前置知识：本教程用到的核心概念

| 概念 | 含义 | 在本教程中的作用 |
|------|------|-----------------| 
| 条件概率 $P(A \mid B)$ | 已知 B 发生时 A 的概率 | 定义转移概率 $p(s' \mid s, a)$ |
| 期望 $\mathbb{E}[X]$ | 随机变量的加权平均值 | 定义价值函数 |
| 几何级数 $\sum_{k=0}^{\infty} r^k = \frac{1}{1-r}$ | 无穷等比数列求和（$\mid r\mid < 1$） | 证明折扣回报有界 |
| Argmax | 使函数取最大值的参数 | 定义贪婪策略 |

**贯穿例子：** CliffWalking 4×12 网格 — 与 Lab 1/2 完全一致。Agent 从左下角出发，目标是右下角，底行中间 10 格是悬崖（-100 奖励），每步 -1 奖励。

---

## §1 MDP 的正式定义：从直觉到数学

> 📚 Ref: Sutton §3.1, p.47-49

### 1.1 Slides 没讲什么？

Slides 多次使用"MDP"这个术语，但从未给出**正式的数学定义**。Sutton 在 §3.1 给出了完整的形式化：

> ⚠️ **Slides 未覆盖：** MDP 的五元组 $(S, A, R, p, \gamma)$ 的正式定义和转移概率函数的完整形式。
> — 📚 Sutton §3.1, p.48

### 1.2 MDP 五元组

一个有限 MDP 由以下五个要素构成：

| 符号 | 含义（中文） | 英文 | CliffWalking 例子 |
|------|------------|------|------------------|
| $S$ | 有限状态集 | Finite set of states | {0, 1, 2, ..., 47}（4×12 = 48 个格子） |
| $A$ | 有限动作集 | Finite set of actions | {上, 下, 左, 右} |
| $R \subset \mathbb{R}$ | 有限奖励集 | Finite set of rewards | {-100, -1, 0} |
| $p(s', r \mid s, a)$ | 转移概率函数 | Dynamics function | 见下文 |
| $\gamma \in [0, 1)$ | 折扣因子 | Discount factor | 通常设为 0.9 |

### 1.3 转移概率函数的完整形式

Slides 只提到"下一个状态取决于当前状态和动作"，但没有给出精确的概率定义：

$$p(s', r \mid s, a) \doteq P(S_t = s', R_t = r \mid S_{t-1} = s, A_{t-1} = a)$$

— 📚 Sutton Eq. 3.2, p.48

**含义：** 在状态 $s$ 执行动作 $a$ 后，转移到状态 $s'$ 并获得奖励 $r$ 的概率。

**CliffWalking 例子（确定性环境）：**
- $p(s_{右边}, -1 \mid s_{普通格}, \text{右}) = 1.0$ — 在普通格子往右走，100% 到达右边格子，奖励 -1
- $p(s_{起点}, -100 \mid s_{悬崖上方}, \text{下}) = 1.0$ — 在悬崖上方往下走，100% 掉入悬崖回到起点，奖励 -100

> 💡 **为什么这很重要？** 因为从这一个函数 $p$ 可以推导出所有其他有用的量（状态转移概率、期望奖励等）。这就是"Markov"的力量——一个函数就包含了完整的环境模型。

### 1.4 从 $p$ 推导其他量

Sutton 在 §3.2 展示了如何从 $p(s', r \mid s, a)$ 推导出更常用的量：

**状态转移概率（对 $r$ 求和消去奖励）：**

$$p(s' \mid s, a) = \sum_{r \in R} p(s', r \mid s, a)$$

— 📚 Sutton Eq. 3.4, p.49

**期望奖励（对 $s'$ 和 $r$ 加权求和）：**

$$r(s, a) = \mathbb{E}[R_t \mid S_{t-1}=s, A_{t-1}=a] = \sum_{r \in R} r \sum_{s' \in S} p(s', r \mid s, a)$$

— 📚 Sutton Eq. 3.5, p.49

**过渡：** 有了 MDP 的精确定义，下一个问题是：agent 的目标到底是什么？我们如何将"最大化奖励"这个直觉变成数学表达式？

---

## §2 回报的形式化：为什么需要折扣？

> 📚 Ref: Sutton §3.3, p.54-57

### 2.1 Slides 没讲什么？

Slides 给出了折扣回报公式 $G_t = R_{t+1} + \gamma G_{t+1}$，但没有证明折扣回报**为什么是有界的**（为什么不会发散到无穷）。

> ⚠️ **Slides 未覆盖：** 折扣回报上界的证明。
> — 📚 Sutton §3.3, p.55

### 2.2 折扣回报有界的证明

如果 $\gamma < 1$ 且奖励有界（$|R_k| \leq R_{\max}$），则：

$$|G_t| = \left| \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \right| \leq \sum_{k=0}^{\infty} \gamma^k |R_{t+k+1}| \leq R_{\max} \sum_{k=0}^{\infty} \gamma^k = \frac{R_{\max}}{1 - \gamma}$$

| 步骤 | 操作 | 依据 |
|------|------|------|
| 第1步 | 展开绝对值 | 三角不等式 |
| 第2步 | 用 $R_{\max}$ 替换 | 奖励有界假设 |
| 第3步 | 几何级数求和 | $\sum_{k=0}^{\infty} \gamma^k = \frac{1}{1-\gamma}$，$\gamma < 1$ 时收敛 |

— 📚 推导基于 Sutton §3.3 的讨论

**CliffWalking 数值验证：** $R_{\max} = 100$（悬崖惩罚的绝对值），$\gamma = 0.9$：

$$|G_t| \leq \frac{100}{1 - 0.9} = \frac{100}{0.1} = 1000$$

所以任何时刻的回报绝对值不超过 1000。这保证了 Q 表中的值不会无限增长。

### 2.3 统一公式：吸收状态的数学

Sutton 引入**吸收状态**来统一回合制和持续任务（§3.3, p.56）：

> ⚠️ **Slides 只简单提到但未形式化：** 回合制任务可以看作一种特殊的持续任务——在终止状态后进入吸收状态（永远回到自身，奖励 = 0）。

为什么这有效？因为吸收状态后 $R_{T+1} = R_{T+2} = \cdots = 0$，所以：

$$G_t = R_{t+1} + \gamma R_{t+2} + \cdots + \gamma^{T-t-1} R_T + \underbrace{\gamma^{T-t} \cdot 0 + \gamma^{T-t+1} \cdot 0 + \cdots}_{= 0}$$

等价于有限求和 $G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}$。

**过渡：** 现在我们有了目标（最大化 $G_t$）的精确定义。接下来的问题是：怎么用数学工具来评估一个策略的好坏？答案是价值函数和 Bellman 方程。

---

## §3 Bellman 方程：价值函数的递归分解

> 📚 Ref: Sutton §3.5, p.58-60

### 3.1 Slides 没讲什么？

Slides 给出了 $v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$ 的定义，但没有推导 **Bellman 方程是怎么从定义推导出来的**。

> ⚠️ **Slides 未覆盖：** Bellman 方程的完整推导过程，从价值函数定义到递归形式。
> — 📚 Sutton §3.5, Eq. 3.14, p.59

### 3.2 Bellman 方程的推导

从定义出发，逐步展开：

**第 1 步：用 $G_t$ 的递归形式替换**

$$v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s]$$
$$= \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t = s]$$

**第 2 步：按策略 $\pi$ 对所有可能的动作 $a$ 展开期望**

$$= \sum_a \pi(a \mid s) \sum_{s'} \sum_r p(s', r \mid s, a) \left[ r + \gamma \mathbb{E}_\pi[G_{t+1} \mid S_{t+1} = s'] \right]$$

注意：$\mathbb{E}_\pi[G_{t+1} \mid S_{t+1} = s']$ 就是 $v_\pi(s')$（价值函数本身！）这里是递归出现。

**第 3 步：替换得到 Bellman 方程**

$$v_\pi(s) = \sum_a \pi(a \mid s) \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma v_\pi(s') \right]$$

— 📚 Sutton Eq. 3.14, p.59

| 符号 | 含义 | 直觉 |
|------|------|------|
| $\sum_a \pi(a \mid s)$ | 对策略下所有可能动作加权 | "我可能采取哪些动作？" |
| $\sum_{s', r} p(s', r \mid s, a)$ | 对所有可能的转移加权 | "每个动作可能导致什么结果？" |
| $r$ | 即时奖励 | "这一步能得到什么？" |
| $\gamma v_\pi(s')$ | 折扣后的未来价值 | "从下一个状态开始还能得到多少？" |

### 3.3 Bellman 方程的直觉理解

一句话总结 Bellman 方程的含义：

> **当前状态的价值 = 所有可能"一步转移"的加权平均值**，其中每次转移的价值 = 即时奖励 + 折扣后的下一状态价值。

**CliffWalking 例子：** 某个靠近终点的格子（假设状态 $s_{46}$，终点左边一格）：
- 动作 = 右（π 选择右的概率很高）：$r = -1$，$s' = s_{47}$（终点），$v_\pi(s_{47}) = 0$（终止）
- 动作 = 上：$r = -1$，$s' = s_{34}$，$v_\pi(s_{34})$ 要更多步才能到终点
- 结果：$v_\pi(s_{46})$ 主要由往右走的 $-1 + 0.9 \times 0 = -1$ 决定（因为策略大概率选右）

**过渡：** Bellman 方程定义了任意策略 $\pi$ 下的价值函数。但我们真正想要的是**最优策略**——让每个状态的价值都最大。这就引出了 Bellman 最优方程。

---

## §4 Bellman 最优方程：Q-Learning 的数学基础

> 📚 Ref: Sutton §3.6, p.62-66

### 4.1 Slides 没讲什么？

Slides 给出了 Q-Learning 的更新规则，但没有解释这个更新规则是**从什么数学原理推导出来的**。

> ⚠️ **Slides 未覆盖：** Bellman 最优方程及其与 Q-Learning 更新规则的关系。
> — 📚 Sutton §3.6, Eq. 3.19-3.20

### 4.2 最优价值函数的定义

**最优状态价值函数：**

$$v_*(s) = \max_\pi v_\pi(s), \quad \forall s \in S$$

— 📚 Sutton Eq. 3.15, p.62

**含义：** $v_*(s)$ 是所有可能策略中，从状态 $s$ 出发能获得的**最大**期望回报。

**最优动作价值函数：**

$$q_*(s, a) = \max_\pi q_\pi(s, a), \quad \forall s \in S, a \in A$$

— 📚 Sutton Eq. 3.16, p.63

**含义：** $q_*(s, a)$ 是在状态 $s$ 执行动作 $a$ 后，再按最优策略行动能获得的**最大**期望回报。

### 4.3 $v_*$ 和 $q_*$ 的关系

$$v_*(s) = \max_a q_*(s, a)$$

— 📚 Sutton p.63

**一句话：** 最优状态价值 = 最优动作价值中最大的那个。这正是为什么 Q-Learning 用 $\max_a Q(s, a)$ 来近似 $V(s)$。

### 4.4 Bellman 最优方程

将 §3.2 Bellman 方程中的 $\sum_a \pi(a \mid s)$（对策略加权）替换为 $\max_a$（选最优动作）：

$$v_*(s) = \max_a \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma v_*(s') \right]$$

— 📚 Sutton Eq. 3.19, p.63

对于动作价值函数：

$$q_*(s, a) = \sum_{s', r} p(s', r \mid s, a) \left[ r + \gamma \max_{a'} q_*(s', a') \right]$$

— 📚 Sutton Eq. 3.20, p.64

### 4.5 从 Bellman 最优方程到 Q-Learning 更新规则

现在回看 Q-Learning 更新规则：

$$Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_{a'} Q(S', a') - Q(S, A) \right]$$

这个更新规则的含义变得清晰了：

| 部分 | 来源 | 含义 |
|------|------|------|
| $R + \gamma \max_{a'} Q(S', a')$ | Bellman 最优方程 Eq. 3.20 右边 | 目标值：即时奖励 + 折扣后的下一状态最优价值 |
| $Q(S, A)$ | 当前估计 | 旧的估计值 |
| 目标 - 估计 | TD 误差 | 新信息与旧信息的差距 |
| $\alpha$ | 学习率 | 朝目标迈一小步（而不是一步到位） |

> ⚠️ **关键洞察：** Q-Learning 不需要知道转移概率 $p(s', r \mid s, a)$！Bellman 最优方程需要对所有 $s', r$ 求和，但 Q-Learning 用**实际经历的单次采样** $(R, S')$ 来近似这个求和。这就是为什么 Q-Learning 是 **model-free**（无模型）的——它不需要环境模型，只需要与环境交互。

**过渡：** Q-Learning 用 $\max$ 来更新。SARSA 用实际动作来更新。上面推导让我们理解了两者的数学本质区别。

---

## §5 TD 学习：SARSA 和 Q-Learning 的统一框架

> 📚 Ref: Sutton §6.1-6.5, p.119-134

### 5.1 Slides 没讲什么？

Slides 给出了 SARSA 和 Q-Learning 的更新规则，但没有解释它们属于什么样的**学习框架**，也没有解释 TD 学习的核心思想。

> ⚠️ **Slides 未覆盖：** TD（Temporal Difference）学习的核心思想——用"估计值"来更新"另一个估计值"（bootstrapping），以及 TD 误差的定义。
> — 📚 Sutton §6.1, p.119

### 5.2 TD 的核心思想：Bootstrapping

**Monte Carlo 方法：** 等到回合结束，用实际的完整回报 $G_t$ 来更新：

$$V(S_t) \leftarrow V(S_t) + \alpha \left[ G_t - V(S_t) \right]$$

问题：必须等到回合结束才能学习。

**TD 方法：** 不等到结束，用"即时奖励 + 下一状态估计值"来近似 $G_t$：

$$V(S_t) \leftarrow V(S_t) + \alpha \left[ R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \right]$$

— 📚 Sutton Eq. 6.2, p.120

**为什么叫"Temporal Difference"（时序差分）？**

因为更新量 $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ 衡量的是**相邻两个时间步估计值的差异**。如果 $\delta_t > 0$，说明到了下一步发现比预期好，应该调高当前估计；反之调低。

> 💡 **类比：** 你估计从家到公司要 30 分钟。开了 10 分钟后已经到一半了（预期只用 20 分钟）。TD 让你**现在**就更新估计为 20 分钟，不需要等到真的到达公司。这就是 bootstrapping 的威力。

### 5.3 SARSA 和 Q-Learning 都是 TD 方法

两者都使用 TD 思想（bootstrapping），区别仅在于更新目标：

| 方法 | TD 目标 | 数学基础 |
|------|--------|---------|
| TD(0) | $R_{t+1} + \gamma V(S_{t+1})$ | Bellman 方程 for $v_\pi$ |
| SARSA | $R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})$ | Bellman 方程 for $q_\pi$ |
| Q-Learning | $R_{t+1} + \gamma \max_a Q(S_{t+1}, a)$ | Bellman **最优**方程 for $q_*$ |

**关键区别的数学本质：**
- SARSA 逼近的是 $q_\pi$（当前策略的价值）→ on-policy
- Q-Learning 逼近的是 $q_*$（最优策略的价值）→ off-policy

这就是为什么 SARSA 考虑探索风险（因为 $q_\pi$ 包含了 ε-greedy 探索的影响），而 Q-Learning 不考虑（因为 $q_*$ 假设最终使用最优策略）。

---

## §6 Agent-Environment 边界：设计哲学

> 📚 Ref: Sutton §3.1, p.50-51; §3.2, p.53-54

### 6.1 Slides 没讲什么？

Slides 引用了 Sutton 关于边界的几段话，但没有深入讨论 Sutton 给出的**具体案例和推理**。

> ⚠️ **Slides 未深入：** Sutton 通过肌肉控制和义肢的例子解释了为什么边界不是物理边界。
> — 📚 Sutton §3.1, p.51

### 6.2 边界设计的关键原则

Sutton 的原则：**agent 不能任意改变的任何事物都是环境的一部分。**

具体案例：

| 组件 | 归属 | 为什么？ |
|------|------|---------|
| 机器人的"选择去哪"的决策 | Agent | agent 可以任意选择 |
| 机器人的马达和关节 | Environment | agent 发出命令，但不能任意改变马达的物理特性 |
| 人的肌肉 | Environment | 大脑（agent）发出信号，肌肉（环境）执行 |
| 义肢的控制信号 | Agent | 与自然肢体的神经信号相同的抽象 |

### 6.3 奖励设计：为什么不要对"如何做"给奖励？

Sutton（§3.2, p.53-54）给出了一个深刻的警告：

> 📚 "In particular, the reward signal is not the place to impart to the agent prior knowledge about *how* to achieve what we want it to do."
> — Sutton p.54

**为什么？** 因为如果你对子目标给奖励（如象棋中对吃子给奖励），agent 可能学到**专门针对子目标的策略**而忽略真正的目标。它可能会不断吃子但从不赢棋。

**正确的做法：** 奖励只编码"想实现什么"（赢棋 = +1），让 agent 自己发现"如何实现"（该不该吃子是 agent 自己学出来的策略）。

**类比：** 这就像声明式编程——你说"我要排好序的数组"（奖励），不说"先比较 a[0] 和 a[1]"（策略）。

---

## 参考索引表

| 教程章节 | 教科书来源 | 核心内容 | Slides 覆盖？ |
|---------|-----------|---------|--------------| 
| §1 MDP 五元组 | Sutton §3.1, p.47-49 | MDP 的形式化定义 $(S, A, R, p, \gamma)$ 和转移概率完整形式 | ❌ 未覆盖（Slides 使用 MDP 但未定义五元组） |
| §1 从 $p$ 推导其他量 | Sutton §3.2, Eq. 3.4-3.5 | 状态转移概率、期望奖励 | ❌ 未覆盖 |
| §2 折扣回报有界证明 | Sutton §3.3, p.55 | $\|G_t\| \leq R_{\max}/(1-\gamma)$ | ❌ 未覆盖（Slides 给了公式但没证明有界性） |
| §2 吸收状态的数学 | Sutton §3.3, p.56 | 统一回合制和持续任务的公式 | ⚠️ 部分（Slides 简单提到，未给出数学推导） |
| §3 Bellman 方程推导 | Sutton §3.5, Eq. 3.14 | 从 $v_\pi$ 定义推导递归形式 | ❌ 未覆盖（Slides 给了结论但没推导） |
| §4 Bellman 最优方程 | Sutton §3.6, Eq. 3.19-3.20 | $v_*$, $q_*$ 的定义和递归方程 | ❌ 未覆盖 |
| §4 Q-Learning 的数学基础 | Sutton §3.6 + §6.5 | 从 Bellman 最优方程到 Q-Learning 更新规则 | ⚠️ 部分（给了更新规则但没解释来源） |
| §5 TD 学习框架 | Sutton §6.1, p.119-120 | Bootstrapping 思想 + TD 误差 | ❌ 未覆盖（Slides 提到 "Temporal Difference" 但未解释含义） |
| §5 SARSA/Q-Learning 统一视角 | Sutton §6.4-6.5 | 两者都是 TD 方法，区别在于逼近 $q_\pi$ vs $q_*$ | ⚠️ 部分（给了公式但没放在 TD 框架下理解） |
| §6 边界设计 | Sutton §3.1, p.50-51 | 肌肉/义肢例子 + 设计原则 | ⚠️ 部分（引用了文字但未深入讨论案例） |
| §6 奖励设计警告 | Sutton §3.2, p.53-54 | 不要对"如何做"给奖励 | ⚠️ 部分（给了原则但未展开 Sutton 的论证） |
