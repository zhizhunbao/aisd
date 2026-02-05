# Reinforcement Learning Quiz 1

Question 1 (1 point)
What is a Markov chain?

Question 1 options:
A) A chain with a rubber coating
B) A sequence of nodes in a graph with cycles
C) A sequence of nodes in a graph without cycles
D) A mathematical model that experiences transition of states with probabilistic rules
E) None of these answers

> **Answer**: D
> **Explanation**:
> 马尔可夫链是"状态按概率规则转移"的数学模型；**为什么是 D**：只有 D 描述了概率性状态转移。A/B/C 分别是物理描述和图结构描述，与概率转移无关；E 不成立。
> **Key**: Markov chain — a probabilistic state-transition model.

Question 2 (1 point)
What is a Markov Decision Process?

Question 2 options:
A) A process for making a decision between two options
B) The underlying logic of a Turing Machine
C) A process for making a decision between more than two options
D) An extension of the Markov chain with actions and rewards
E) None of these answers

> **Answer**: D
> **Explanation**:
> MDP 是"马尔可夫链 + 动作 + 奖励"的序贯决策模型；**为什么是 D**：只有 D 明确指出在马尔可夫链基础上加入动作与奖励。A/C 只是泛化的决策描述，缺少状态转移与奖励；B 与 MDP 无关；E 不成立。
> **Key**: MDP = Markov chain + actions + rewards.

Question 3 (1 point)
In a Markov Decision Process, taking an action in a state always leads to the same result state.

Question 3 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> MDP 的转移由概率分布 $P(s'|s,a)$ 定义；**为什么是 B (False)**：同一状态-动作对可到达多个后继状态，非确定性。A (True) 要求每次都到同一状态，与随机转移矛盾。
>   - **$P(s'|s,a)$**: 状态转移概率 (Transition probability)
> **Key**: MDP transitions are stochastic via $P(s'|s,a)$, not deterministic.

Question 4 (1 point)
What is a problem with defining total reward from a starting point to be the sum of all subsequent rewards?

Question 4 options:
A) The sum of all subsequent rewards might be negative
B) The sum of all subsequent rewards might be zero
C) The sum of all subsequent rewards might be positive
D) None of these answers
E) The sum of all subsequent rewards might be infinite

> **Answer**: E
> **Explanation**:
> 在无限步任务中直接求和可能发散到 $\infty$，无法比较策略；**为什么是 E**：E 指出了真正的问题——总和可能无穷大，这正是引入折扣因子 $\gamma$ 的原因。
>   - **A/B/C 错**：负数、零、正数都不是"定义失效"的原因，问题核心在于发散。
>   - D 不成立（存在明确问题）。
>   - **$\gamma$**: 折扣因子 (Discount factor)，$0 \le \gamma < 1$
>   - **$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$**: 折扣回报，$\gamma^k$ 确保几何级数收敛
> **Key**: Infinite-horizon sum may diverge; discount factor $\gamma$ ensures convergence.

Question 5 (1 point)
What is a policy in Reinforcement Learning?

Question 5 options:
A) A function that specifies what action to take in a certain state
B) A function that specifies the next state to visit
C) A function that gives the list all the possible actions in a state
D) None of these answers
E) A function that gives the list of all impossible actions in a state

> **Answer**: A
> **Explanation**:
> 策略 $\pi(a|s)$ 是"给定状态，告诉你选什么动作"的映射；**为什么是 A**：A 正是策略的定义。B 描述的是状态转移预测；C/E 描述的是动作列表，不是选择规则；D 不成立。
> **Key**: Policy $\pi(a|s)$ — maps states to actions.

Question 6 (1 point)
What is given by the state value function?

Question 6 options:
A) It takes a state and gives the expected total reward we can get starting from that state
B) It takes a state and gives an action that results in the highest reward
C) None of these answers
D) It takes an action and a state and gives the expected total reward we can get from taking that action
E) It takes an action and gives the state that results from taking that action

> **Answer**: A
> **Explanation**:
> 状态价值函数 $V(s)$ 输出从该状态出发的期望累计回报；**为什么是 A**：A 准确描述了 $V(s)$ 的定义。
>   - **B 错**：选动作是策略 $\pi$ 的职责，不是 $V(s)$。
>   - **D 错**：接受状态-动作对并输出期望回报的是动作价值函数 $Q(s,a)$，不是 $V(s)$。
>   - C/E 分别不成立和描述状态转移。
>   - **$V(s)$**: 状态 → 期望回报 | **$Q(s,a)$**: 状态-动作对 → 期望回报
> **Key**: $V(s)$ = expected return from state $s$. Distinct from $Q(s,a)$.

Question 7 (1 point)
What is the action value function?

Question 7 options:
A) It takes a state and gives expected total reward we can get starting from that state
B) It takes a state and an action and gives the state resulting from taking the action
C) It takes a state and an action and gives the immediate reward resulting from taking that action
D) It takes a state and an action and gives the expected total reward we can get starting from that state and taking that action
E) None of these answers

> **Answer**: D
> **Explanation**:
> 动作价值函数 $Q(s,a)$ 输出在状态 $s$ 采取动作 $a$ 后的期望累计回报；**为什么是 D**：只有 D 同时包含状态、动作与期望总回报。
>   - **A 错**：这是状态价值函数 $V(s)$——只接受状态，不接受动作。
>   - **C 错**：只描述即时奖励 $R$，不是累计期望回报。
>   - B 描述状态转移结果；E 不成立。
>   - **$Q(s,a)$**: 动作价值函数 (Action-value function)
> **Key**: $Q(s,a)$ = expected return from state $s$ taking action $a$. Differs from $V(s)$ by including action.

Question 8 (1 point)
What is a greedy policy?

Question 8 options:
A) A policy that rotates through all actions
B) A policy that dictates always taking rather than giving
C) None of these answers
D) A policy that dictates always taking the action that results in the highest immediate reward
E) A policy that always specifies the same action

> **Answer**: D
> **Explanation**:
> 贪婪策略是"每次都选当前估计价值最高的动作"；**为什么是 D**：D 明确说"总是选最高即时回报的动作"，符合 $a = \arg\max_{a'} Q(s, a')$。A/B/E 分别是轮换、无关描述和固定动作，都不是贪婪；C 不成立。
>   - **$\arg\max_{a'} Q(s, a')$**: 选使 $Q$ 值最大的动作
> **Key**: Greedy policy — always pick $\arg\max Q$, prioritizing immediate reward.

Question 9 (1 point)
What does the Bellman Equation say in the context of Q-Learning?

Question 9 options:
A) It says that the value of an action a in some state s is the immediate reward you get for taking that action, plus the total past rewards from the previous next state.
B) It says that the value of taking an action a in some state s is the immediate reward you get for taking that action, minus the maximum expected future rewards you can get in the next state.
C) It says that the value of taking an action a in some state s is the immediate reward you get for taking that action, plus the minimum expected future rewards you can get in the next state.
D) None of these answers
E) It says that the value of taking an action a in some state s is the immediate reward you get for taking that action, plus the maximum expected future rewards you can get in the next state.

> **Answer**: E
> **Explanation**:
> 贝尔曼方程：$Q(s, a) = R + \gamma \max_{a'} Q(s', a')$，即 Q 值 = 即时奖励 + 折扣后的下一状态最大 Q 值；**为什么是 E**：只有 E 说"即时奖励 **+** **最大**未来回报"，与公式一致。
>   - **A 错**：说"过去回报 (past rewards)"，贝尔曼方程面向未来，不回溯。
>   - **B 错**：用减号 (minus)，公式是加号。
>   - **C 错**：取最小 (minimum)，公式是取最大 $\max$。
>   - D 不成立。
>   - **$R$**: 即时奖励 (Immediate reward)
>   - **$\gamma$**: 折扣因子 (Discount factor)
>   - **$\max_{a'} Q(s', a')$**: 下一状态的最大预期收益
> **Key**: Bellman: $Q(s,a) = R + \gamma \max_{a'} Q(s',a')$ — immediate reward + discounted max future value.
