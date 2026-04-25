# Reinforcement Learning Quiz 3

---

**Question 1**
What is a condition for applying Q‑Learning to a RL problem?
将 Q-Learning 应用于 RL 问题的条件是什么？

A) None of these answers
B) Rewards must be known in advance
C) Transition probabilities must be known
D) Optimal value function must be known
E) Action value table must be known

> **Answer**: A
> Q-Learning is model-free — no prior knowledge of rewards, transitions, or values needed.
> Q-Learning 是 model-free 的，不需要预先知道奖励、转移概率或价值函数。

---

**Question 2**
What does greedy mean in RL?
"贪婪"是什么意思？

A) Choose action with highest estimated value / 选择估计值最高的动作
B) Choose action maximizing future reward directly
C) Choose action maximizing total reward
D) Choose action maximizing past reward
E) None

> **Answer**: A
> Greedy: always pick $\arg\max Q(s,a')$.
> 贪婪：总是选 Q 值最高的动作。

---

**Question 3**
What is an episode in RL?
什么是回合(Episode)？

A) A new state added
B) One step of action
C) A run from start state to terminal state / 从起始到终止状态的完整运行
D) Observing cumulative reward
E) Number of steps

> **Answer**: C
> Episode = complete trajectory $(s_0, a_0, r_1, \ldots, s_T)$.
> 回合 = 完整轨迹。

---

**Question 4**
What is reinforcement learning?
什么是强化学习？

A) Unsupervised learning
B) Supervised learning
C) Sensor learning
D) Clustering algorithm
E) Learning through interaction with an environment to maximize reward / 通过与环境交互来最大化奖励

> **Answer**: E
> RL = agent-environment interaction. Core: Agent, Environment, State, Action, Reward.
> RL = 智能体与环境交互。核心要素：Agent、Environment、State、Action、Reward。

---

**Question 5**
Difference between state value and action value functions?
状态价值函数和动作价值函数的区别？

A) None
B) Action value returns state
C) State value takes state and action
D) State value returns action reward
E) Action value evaluates action in a state; state value evaluates a state / 动作价值评估某状态下的动作，状态价值评估状态

> **Answer**: E
> $V(s)$: state → expected return. $Q(s,a)$: state+action → expected return.
> 区别在于是否指定了动作。

---

**Question 6**
What if the Markov Property does not hold?
马尔可夫性质不成立怎么办？

A) None
B) RL cannot be applied
C) RL requires a non‑Markov algorithm
D) RL may still be applied but learning may take longer / RL 仍可用但学习可能更慢
E) Redefine the state

> **Answer**: D
> RL still works without perfect Markov property, but learning is slower.
> 即使马尔可夫性不完美，RL 仍可用，但学习更慢。

---

**Question 7**
What is the Reward Hypothesis?
什么是奖励假设？

A) Some goals cannot be expressed as reward
B) All goals = maximizing cumulative reward / 所有目标 = 最大化累积奖励
C) None
D) Rewards minimize steps
E) Goals define Markov property

> **Answer**: B
> All goals can be expressed as maximizing expected cumulative scalar reward.
> 所有目标都可以表述为最大化标量奖励的累积期望值。

---

**Question 8**
What is a Policy?
什么是策略(Policy)？

A) A mapping from state to action / 状态到动作的映射
B) Value function
C) Reward table
D) None
E) All

> **Answer**: A
> Deterministic: $\pi(s) = a$. Stochastic: $\pi(a|s)$.
> 确定性：$\pi(s)=a$。随机性：$\pi(a|s)$。

---

**Question 9**
Where is the policy implemented?
策略在哪里实现？

A) Environment
B) None
C) Value function in environment
D) Policy and value function are in the agent / 策略和价值函数在 Agent 中
E) Agent determines environment results

> **Answer**: D
> Agent: policy + value function. Environment: next state + reward.
> Agent 包含策略和价值函数。Environment 提供下一状态和奖励。

---

**Question 10**
What is a Value Function?
什么是价值函数？

A) Expected immediate steps
B) Same as policy
C) Episode reward
D) Expected immediate reward
E) None of these answers

> **Answer**: E
> None correct. Value function = expected cumulative return: $V(s)$ for states, $Q(s,a)$ for state-action pairs.
> 没有选项正确。价值函数 = 期望累积回报。

---

# Reference Tables

## Q-Learning vs SARSA

| | Q-Learning (Off-policy) | SARSA (On-policy) |
|---|---|---|
| Update | $Q \leftarrow Q + \alpha[r + \gamma \max Q(s',a') - Q]$ | $Q \leftarrow Q + \alpha[r + \gamma Q(s',a') - Q]$ |

**Q-Learning example**: Q=5, α=0.1, r=2, γ=0.9, maxQ=8 → **5.42**
**SARSA example**: Q=5, α=0.1, r=2, γ=0.9, Q(s',a')=6 → **5.24**

## Practice Answers

1. Off-policy algorithm? → **Q-Learning**
2. Equation defining state value? → **Bellman**
3. Discount factor controls? → **importance of future reward / 未来奖励的重要性**
4. Exploration means? → **try new actions / 尝试新动作**
5. Evaluates state-action pairs? → **Q(s,a)**
6. Chooses the action? → **agent**
7. γ close to 1? → **future rewards more important / 未来奖励更重要**
8. Uses max future Q? → **Q-Learning**
9. Uses next chosen action value? → **SARSA**
10. Policy represents? → **state → action mapping / 状态到动作的映射**
