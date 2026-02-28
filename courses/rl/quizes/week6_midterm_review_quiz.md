# Week 6: 期中复习综合测验 (Midterm Review Comprehensive Quiz)

> 覆盖范围: Weeks 1-5 全部内容 (RL Intro, MDP, Gymnasium, SB3, DQN)
> 来源: Slides Week 1-5 + Quiz 1-4 + Labs 1-2 + Assignment 1 + Midterm Review Slides
> 难度: ★ 基础 | ★★ 中等 | ★★★ 综合

---

## 选择题 (Multiple Choice)

### Q1. ★ 强化学习的三个核心要素是什么？(Quiz 2 Q2)

A. Input, Output, Loss
B. Agent, Environment, Reward
C. State, Action, Policy
D. Training, Validation, Testing

### Q2. ★ 马尔可夫性质 (Markov Property) 的正确描述是？(Quiz 2 Q3)

A. 未来状态取决于所有历史状态
B. 先前状态完全决定未来
C. 未来状态只依赖于当前状态，与历史无关
D. 状态转移是确定性的

### Q3. ★ MDP 是什么的扩展？(Quiz 1 Q2)

A. Hidden Markov Model
B. Markov Chain
C. Bayesian Network
D. Decision Tree

### Q4. ★ 奖励假说 (Reward Hypothesis) 的含义是？(Quiz 2 Q5)

A. 奖励总是正数
B. 所有目标都可以用期望累积奖励的最大化来描述
C. 奖励越大越好
D. 奖励必须在每一步都给出

### Q5. ★ 贪婪策略 (Greedy Policy) 的定义是？(Quiz 1 Q8, Quiz 2 Q12)

A. 最大化总回报的策略
B. 总是选择即时奖励最大的动作
C. 总是选择使 Q 值最大的动作: $a = \arg\max_{a'} Q(s, a')$
D. 随机选择动作

### Q6. ★ $V(s)$ 和 $Q(s,a)$ 的区别是什么？(Quiz 2 Q10)

A. $V(s)$ 输入状态+动作，$Q(s,a)$ 只输入状态
B. $V(s)$ 只输入状态，$Q(s,a)$ 输入状态+动作
C. 两者完全相同
D. $V(s)$ 在环境中，$Q(s,a)$ 在 Agent 中

### Q7. ★★ Q-Learning 需要什么前提条件？(Quiz 2 Q13)

A. 只需要已知状态集 $S$
B. 只需要已知动作集 $A$
C. 需要已知且有限的状态集 $S$ 和动作集 $A$
D. 不需要任何前提

### Q8. ★★ Bellman 方程的正确描述包括哪些？(Quiz 2 Q11)

A. 只有 B: 将当前值与后继值关联
B. 只有 D: 将价值计算分解为递归子问题
C. 只有 E: 构成 Q-Learning 的数学基础
D. B, D, E 都正确

### Q9. ★★ Q-Learning 为什么在 CliffWalking 上收敛到最短路径？(Midterm Slide 4)

A. 因为它是 on-policy 的
B. 因为更新时用 max Q(s',a')，忽略了探索时的危险
C. 因为 ε 值太小
D. 因为 Q 表初始化为零

### Q10. ★★ SARSA 为什么在 CliffWalking 上收敛到安全路径？

A. 因为它是 off-policy 的
B. 因为它使用 max Q(s',a') 更新
C. 因为它是 on-policy 的，更新时考虑了 ε-greedy 的随机性
D. 因为学习率更低

### Q11. ★★ 以下哪个不是 Stable-Baselines3 的特性？(Midterm Slide 9)

A. Vectorized environments
B. Callbacks
C. 自动奖励函数设计
D. 可靠的 RL 算法实现

### Q12. ★ Gymnasium 中 `env.step(action)` 返回几个值？(Week 3)

A. 3
B. 4
C. 5
D. 6

### Q13. ★★ DQN 中 Target Network 的作用是什么？(Week 5)

A. 加速训练
B. 减少内存使用
C. 稳定训练目标，防止目标 Q 值不断漂移
D. 增加探索能力

### Q14. ★★ Tabular Q-Learning 和 DQN 的关键区别是什么？

A. DQN 不需要奖励信号
B. DQN 用神经网络替代 Q 表，可以处理大/连续状态空间
C. DQN 是 on-policy 的
D. DQN 不使用 Bellman 方程

### Q15. ★★★ 以下哪个术语是错误的？(Quiz 2 Q14)

A. Temporal Difference
B. Temporal Distance
C. TD Learning
D. TD Error

---

## 判断题 (True/False)

### T1. ★ RL 是监督学习的一个子类。

### T2. ★ MDP 中的状态转移是确定性的（同一状态+动作总是到达同一下一状态）。(Quiz 1 Q3)

### T3. ★ 折扣因子 $\gamma$ 的作用是解决无限步回报可能发散的问题。(Quiz 1 Q4)

### T4. ★ Policy $\pi$ 在 Environment 中，不在 Agent 中。(Quiz 2 Q15)

### T5. ★★ Q-Learning 是 on-policy 算法。

### T6. ★ 终止状态的 Q 值必须设为 0。

### T7. ★★ Replay Buffer 按时间顺序提供训练数据。

### T8. ★ Gymnasium Wrapper 需要修改底层环境的源代码。(Midterm Slide 8)

### T9. ★★ DQN 可以处理连续动作空间。

### T10. ★ Episode 是从起始状态到终止/截断状态的一次完整运行。(Quiz 2 Q6)

---

## 简答题 (Short Answer)

### S1. ★★★ 写出 Q-Learning 更新公式（Python 语法），并列出每个变量的含义。(Midterm Slide 6)

### S2. ★★ 画出 RL 的 Agent-Environment 交互图，标注 State、Action、Reward 的流向。(Midterm Slide 5)

### S3. ★★ 已知 $Q(s,a) = 3.0$，$\alpha = 0.2$，$\gamma = 0.9$，$R = 2$，$\max_{a'} Q(s', a') = 4.0$。计算更新后的 $Q(s,a)$。

### S4. ★★ 解释 Q-Learning 和 SARSA 在 CliffWalking 上路径不同的原因。

---

## 答案 (Answers)

### 选择题

| 题号 | 答案 | 解释 |
|------|------|------|
| Q1 | B | RL 三要素: Agent, Environment, Reward |
| Q2 | C | 马尔可夫性质: 未来只依赖当前状态 |
| Q3 | B | MDP 是 Markov Chain 加入动作和奖励的扩展 |
| Q4 | B | 奖励假说: 所有目标 = 最大化期望累积奖励 |
| Q5 | C | Greedy = $\arg\max_{a'} Q(s, a')$，注意是即时 Q 值最大，不是总回报 |
| Q6 | B | $V(s)$ 只输入状态，$Q(s,a)$ 输入状态+动作 |
| Q7 | C | Q-Learning 需要同时知道有限的 $S$ 和 $A$ |
| Q8 | D | Bellman 方程: 关联当前与后继值 + 递归分解 + Q-Learning 基础 |
| Q9 | B | Off-policy: max 忽略探索危险，学到最短路径 |
| Q10 | C | On-policy: 考虑 ε-greedy 随机性，学到安全路径 |
| Q11 | C | SB3 不自动设计奖励函数，这需要人工定义 |
| Q12 | C | step() 返回 5 个值: next_state, reward, terminated, truncated, info |
| Q13 | C | Target Network 冻结副本作为稳定目标，每 N 步同步 |
| Q14 | B | DQN 用神经网络替代 Q 表，可处理大/连续状态空间 |
| Q15 | B | "Temporal Distance" 是错误术语，正确是 "Temporal Difference" |

### 判断题

| 题号 | 答案 | 解释 |
|------|------|------|
| T1 | False | RL 是第三种 ML 范式，不是监督学习的子类 |
| T2 | False | MDP 转移是随机的 $P(s'|s,a)$，同一状态+动作可能到达不同状态 |
| T3 | True | $\gamma < 1$ 确保无限步回报收敛 |
| T4 | False | Policy 在 Agent 中，不在 Environment 中 |
| T5 | False | Q-Learning 是 off-policy 算法 |
| T6 | True | 终止状态没有后续，$Q(s_T, a) = 0$ |
| T7 | False | Replay Buffer 随机采样，打破时间相关性 |
| T8 | False | Wrapper 不修改底层代码，通过包装修改行为 |
| T9 | False | DQN 只支持 Discrete 动作空间 |
| T10 | True | Episode = 从起始到终止/截断的一次完整运行 |

### 简答题

**S1:**
```python
qtable[state][action] = qtable[state][action] + alpha * (
    reward + gamma * max(qtable[next_state]) - qtable[state][action]
)
```

| 变量 | 含义 |
|------|------|
| `qtable` | Q 表，实现动作价值函数 |
| `state` | 当前状态 |
| `action` | 当前动作 |
| `alpha` | 学习率 (step size) |
| `reward` | 即时奖励 |
| `gamma` | 折扣因子 |
| `next_state` | 下一状态 |

**S2:**
```
Agent ──Action a_t──> Environment
Agent <──Reward R_{t+1}── Environment
Agent <──State S_{t+1}── Environment
(每个时间步重复)
```

**S3:**
- TD Target = $R + \gamma \max_{a'} Q(s', a') = 2 + 0.9 \times 4.0 = 5.6$
- TD Error = $5.6 - 3.0 = 2.6$
- $Q(s,a) \leftarrow 3.0 + 0.2 \times 2.6 = 3.0 + 0.52 = 3.52$

**S4:**
Q-Learning 是 off-policy 算法，更新时用 $\max_{a'} Q(s', a')$（假设未来总选最优动作），忽略了探索时可能掉下悬崖的风险，因此学到沿悬崖边的最短路径。SARSA 是 on-policy 算法，更新时用实际采取的动作 $Q(s', a')$（包含 ε-greedy 的随机探索），考虑了探索时可能走到悬崖边的危险，因此学到远离悬崖的安全路径。
