Question 1 (1 point) 
What is Reinforcement Learning (RL)?

Question 1 options:

All of these answers.


RL is a third type of machine learning, along with supervised learning and unsupervised learning.


RL is a form of supervised machine learning used for learning to play games.


RL is a form of unsupervised machine learning used in control applications.


None of these answers.

Question 2 (1 point) 
Which of the following can be considered primary aspects of a Reinforcement Learning problem setup?

Question 2 options:

Values, Step function, and Actions.


Agent, Environment, and Reward.


Reward, Environment, and States.


Agent, Values, and Step function.


None of these answers.

Question 3 (1 point) 
What is a Markov state?

Question 3 options:

None of these answers.


All of these answers.


Markov states are states that form a single deterministic chain.


Intuitively, a Markov state has the property that all its previous states completely determine its future states.


Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states.

Question 4 (1 point) 
What is the relationship between Reinforcement Learning (RL) and Markov Decision Processes (MDPs)?

Question 4 options:

MDPs are a mathematical model of the sequential decision making processes addressed by RL.


None of these asnwers.


MDPs are a component of the software used to implement video games.


MDPs are known specific strategies developed for playing games like chess, go, and video games played by RL systems.


All of these answers.

Question 5 (1 point) 
What is the Reward Hypothesis of Reinforcement Learning?

Question 5 options:

The Reward Hypothesis basically states that some goals cannot be thought of as maximizing the expected cumulative value of a scalar reward function.


The Reward Hypothesis basically states that all goals can be thought of as minimizing the the number of steps to maximize a scalar reward function.


The Reward Hypothesis basically states that some goals cannot be thought of as minimizing the the number of steps to maximize a scalar reward function.


None of these answers.


The Reward Hypothesis basically states that all goals can be thought of as maximizing the expected cumulative value of a scalar reward function.

Question 6 (1 point) 
What is meant by "episode" in Reinforcement Learning?

Question 6 options:

An episode is a single cycle of performing an action, recieving a reward, and observing the resulting state.


An episode is a single run from the starting state to a terminal (or truncated) state.


An episode is a single run that does not reach the terminal state.


An episode is the number of steps actually taken to reach the terminal state.


None of these answers.

Question 7 (1 point) 
Why role does the discount factor 
 play in Reinforcement Learning?

Question 7 options:

 addresses the problem of infinite cumulative rewards in non-terminating processes.


 determines how many times an action is chosen randomly during training.


 represents the total discount which is subtracted from the reward function cumulative total.


None of these answers.


 represents the weighting of the current goal of a Reinforcement Learning problem.

Question 8 (1 point) 
What is a Policy in Reinforcement Learning?

Question 8 options:

None of these answers.


The Policy is a table that assigns a value to each action.


The Policy is a function that assigns a value to each action-state pair.


The Policy is a function that determines the probability of an agent taking an action.


All of these answers.

Question 9 (1 point) 
What is a Value Function in Reinforcement Learning?

Question 9 options:

A Value Function gives a measure of the expected total reward of an episode.


A Value Function gives a measure of the expected total reward given a state or state-action pair.


None of these answers.


A Value Function gives a measure of the expected total number of steps to maximize reward.


All of these answers.

Question 10 (1 point) 
What is the difference between an action value function and a state value function?

Question 10 options:

None of these answers.


State value functions return total reward to termination, and action-value functions return immediate reward of taking the action.


State value functions take a state, and action value functions take just actions.


Action value functions return the average reward for taking an action, and State value functions return a state's average total future reward.


Action value functions take state-action pairs, whereas state value functions take just states.

Question 11 (1 point) 
Which of the following statements is true about the Bellman equation in Reinforcement Learning?

Question 11 options:

None of these answers.


It expresses the relationship between the value of a state or a state-action pair, and the value of the successor states.


All of these answers.


It breaks the problem of determining the value of a state into smaller problems recursively.


It forms the mathematical basis for the Q-Learning algorithm in Reinforcement Learning.

Question 12 (1 point) 
What does "greedy" mean in the context of Reinforcement Learning?

Question 12 options:

None of these answers.


It implies a policy that tries to maximize total reward.


It implies a policy where future reward is considered over immediate reward.


It implies a policy where immediate reward is considered over future reward.


It implies a policy tha ttries to maximize future reward.

Question 13 (1 point) 
What is a condition for applying Q-learning to a Reinforcement Learning problem?

Question 13 options:

None of these answers.


The complete set of possible states must be known.


The complete set of actions must be known.


The complete set of actions and the complete set of possible states must be known.


The optimal value function must be known.

Question 14 (1 point) 
Which of the following statements is true in the context of Reinforcement Learning?

Question 14 options:

All of these answers.


Q-learning is a form of Temporal Distance (TD) learning.


Temporal Distance (TD) learning involves learning from differences in time steps as opposed to complete episodes.


Temporal Distance (TD) learning does not require that the agent have a model of the environment.


None of these answers.

Question 15 (1 point) 
Which of the following statements is true in the context of Reinforcement Learning?

Question 15 options:

The value function and policy function are implemented in the agent rather than the environment.


The results of an action are determined by the agent rather than the environment.


The value function is implemented in the environment rather than the agent.


The policy function is implemented in the environment rather than the agent.


None of these answers.


Question 1: What is Reinforcement Learning?

答案: RL is a third type of machine learning, along with supervised learning and unsupervised learning.

解析：RL 是机器学习的第三大范式，与监督学习（有标签）和无监督学习（无标签）并列。它既不是 supervised 也不是 unsupervised，而是通过与环境交互获得奖励信号来学习。

Question 2: Primary aspects of RL problem setup?

答案: Agent, Environment, and Reward.

解析：RL 的三个核心要素是智能体 (Agent)、环境 (Environment) 和奖励 (Reward)。Values 和 Step function 是派生概念，不是问题设置的主要方面。

Question 3: What is a Markov state?

答案: Intuitively, a Markov state has the property that its subsequent states do not depend on its previous states.

解析：Markov 性质的核心是"未来只取决于当前状态，与历史无关"。即 P(S_{t+1}|S_t) = P(S_{t+1}|S_1,...,S_t)，后续状态不依赖于之前的状态历史，只依赖于当前状态。

Question 4: Relationship between RL and MDPs?

答案: MDPs are a mathematical model of the sequential decision making processes addressed by RL.

解析：MDP（马尔可夫决策过程）为 RL 提供了形式化的数学框架，用于建模序列决策问题。

Question 5: What is the Reward Hypothesis?

答案: The Reward Hypothesis basically states that all goals can be thought of as maximizing the expected cumulative value of a scalar reward function.

解析：这是 Sutton & Barto 教材中的经典定义——所有目标都可以被描述为最大化一个标量奖励函数的期望累积值。

Question 6: What is an "episode"?

答案: An episode is a single run from the starting state to a terminal (or truncated) state.

解析：Episode 是从初始状态到终止状态的一次完整交互过程，而不是单个 step 或步数。

Question 7: Role of discount factor γ?

答案: γ addresses the problem of infinite cumulative rewards in non-terminating processes.

解析：折扣因子 γ ∈ [0, 1) 确保在 continuing tasks（非终止任务）中累积奖励收敛，避免无穷大的问题。它让未来奖励按指数衰减。

Question 8: What is a Policy?

答案: The Policy is a function that determines the probability of an agent taking an action.

解析：策略 π(a|s) 是从状态到动作概率分布的映射，决定了智能体在某状态下采取各动作的概率。它不是为动作分配"值"的表（那是 Q-table）。

Question 9: What is a Value Function?

答案: A Value Function gives a measure of the expected total reward given a state or state-action pair.

解析：价值函数 V(s) 或 Q(s,a) 衡量的是从给定状态（或状态-动作对）出发的期望累积回报，不是整个 episode 的总奖励，也不是步数。

Question 10: Difference between action value function and state value function?

答案: Action value functions take state-action pairs, whereas state value functions take just states.

解析：Q(s, a) 接受状态-动作对作为输入，V(s) 只接受状态。这是两者最本质的区别——输入不同。

Question 11: Bellman equation?

答案: All of these answers.

解析：Bellman 方程同时满足以下三点：

表达当前状态价值与后续状态价值的关系
递归地将价值计算分解为子问题
是 Q-Learning 算法的数学基础
Question 12: What does "greedy" mean?

答案: It implies a policy where immediate reward is considered over future reward.

解析：Greedy（贪婪）意味着优先选择当前看起来最优的动作（即时利益），而不考虑探索可能带来更好长期回报的选择。这也是 exploration vs exploitation 权衡中的 exploitation 端。

Question 13: Condition for applying Q-learning?

答案: The complete set of actions and the complete set of possible states must be known.

解析：表格式 Q-learning 需要构建 Q-table，其索引为所有 (state, action) 对，因此必须知道完整的状态空间和动作空间。

Question 14: TD learning statements?

答案: None of these answers.

解析：所有选项中使用的术语是 "Temporal Distance"，但正确术语是 "Temporal Difference"（时序差分）。由于术语错误，所有相关陈述都不成立。如果改为 Temporal Difference，则这三条描述都是正确的。

Question 15: Which statement is true?

答案: The value function and policy function are implemented in the agent rather than the environment.

解析：在 RL 架构中，Agent 负责维护 policy（决策）和 value function（评估）；Environment 负责提供 state 和 reward。动作的结果由环境决定，不是由智能体决定。

