
# RL_CST8509_ToddKelley_Master_Review_FINAL

Course: CST8509 Reinforcement Learning
Instructor: Todd Kelley
Student: Hye Ran Yoo

This document includes
1 Quiz Review (10 questions)
2 Core Reinforcement Learning Concepts
3 Key RL Formulas
4 Q‑Learning and SARSA calculation examples
5 Additional Todd Kelley style multiple‑choice questions

==================================================

# 1 Quiz Review

## Question 1
What is a condition for applying Q‑Learning to a Reinforcement Learning problem?

Options
a None of these answers
b Rewards must be known in advance
c Transition probabilities must be known
d Optimal value function must be known
e Action value table must be known

Answer
a

Key Concept
Q‑Learning is a model‑free reinforcement learning algorithm.
Transition probabilities and reward models do not need to be known.

University Exam Focus

| Topic | Key Idea |
|---|---|
| Model‑free vs Model‑based | Q‑Learning is model‑free |
| Off‑policy learning | Q‑Learning is off‑policy |
| Update equation | Often appears in exam calculations |


## Question 2
What does greedy mean in reinforcement learning?

Options
a Choose action with highest estimated value
b Choose action maximizing future reward directly
c Choose action maximizing total reward
d Choose action maximizing past reward
e None

Answer
a

Key Concept
A greedy policy always selects the action with the highest estimated Q value.

Common exam topic
Exploration vs exploitation trade‑off.


## Question 3
What is an episode in reinforcement learning?

Options
a A new state added
b One step of action
c A run from start state to terminal state
d Observing cumulative reward
e Number of steps

Answer
c

Key Concept
An episode is the complete trajectory from starting state to terminal state.

Example
(s0, a0, r1, s1, a1, r2 ... sT)


## Question 4
What is reinforcement learning?

Options
a Unsupervised learning
b Supervised learning
c Sensor learning
d Clustering algorithm
e Learning through interaction with an environment to maximize reward

Answer
e

Core elements

| Component | Meaning |
|---|---|
| Agent | decision maker |
| Environment | external world |
| State | current situation |
| Action | possible decision |
| Reward | feedback signal |


## Question 5
What is the difference between state value and action value functions?

Options
a None
b Action value returns state
c State value takes state and action
d State value returns action reward
e Action value evaluates action in a state while state value evaluates a state

Answer
e

Concept

| Function | Meaning |
|---|---|
| V(s) | expected return from state |
| Q(s,a) | expected return from taking action a in state s |


## Question 6
What can be done in reinforcement learning if the Markov Property does not hold?

Options
a None
b RL cannot be applied
c RL requires a non‑Markov algorithm
d RL may still be applied but learning may take longer
e Redefine the state

Answer
d

Key Concept
Markov Property means the current state contains all information required for future prediction.

Formula
P(s' | s)


## Question 7
What is the Reward Hypothesis in reinforcement learning?

Options
a Some goals cannot be expressed as reward
b All goals can be expressed as maximizing cumulative reward
c None
d Rewards minimize steps
e Goals define Markov property

Answer
b

Key Concept
All goals can be expressed as maximizing expected cumulative reward.


## Question 8
What is a Policy in reinforcement learning?

Options
a A mapping from state to action
b Value function
c Reward table
d None
e All

Answer
a

Policy representation

Deterministic policy
π(s) = a

Stochastic policy
π(a|s)


## Question 9
Where is the policy implemented?

Options
a Environment
b None
c Value function in environment
d Policy and value function are implemented in the agent
e Agent determines environment results

Answer
d

Concept
Agent contains policy and value function.
Environment provides next state and reward.


## Question 10
What is a Value Function?

Options
a Expected immediate steps
b Same as policy
c Episode reward
d Expected immediate reward
e None of these answers

Answer
e

Concept
Value functions estimate expected return.

| Function | Meaning |
|---|---|
| V(s) | state value |
| Q(s,a) | action value |


==================================================

# 2 Important Reinforcement Learning Concepts

## Markov Decision Process (MDP)

| Symbol | Meaning |
|---|---|
| S | states |
| A | actions |
| P(s'|s,a) | transition probability |
| R(s,a) | reward |
| γ | discount factor |


## Return

Return represents cumulative future reward.

G_t = r_t + γr_{t+1} + γ²r_{t+2} + ...


## Bellman Equation

State value

V(s) = E[r + γV(s')]

Action value

Q(s,a) = E[r + γ max Q(s',a')]


## Exploration vs Exploitation

Exploration
Trying new actions

Exploitation
Choosing the best known action

Most common method
epsilon‑greedy


==================================================

# 3 Core RL Algorithms

## Q‑Learning

Q(s,a) ← Q(s,a) + α [ r + γ max Q(s',a') − Q(s,a) ]

Type
Off‑policy learning


## SARSA

Q(s,a) ← Q(s,a) + α [ r + γ Q(s',a') − Q(s,a) ]

Type
On‑policy learning


==================================================

# 4 Calculation Example

## Q‑Learning Example

| Variable | Value |
|---|---|
| Q(s,a) | 5 |
| α | 0.1 |
| r | 2 |
| γ | 0.9 |
| maxQ | 8 |

target = 2 + 0.9 × 8 = 9.2

Q = 5 + 0.1(9.2 − 5)

New Q value = 5.42


## SARSA Example

| Variable | Value |
|---|---|
| Q(s,a) | 5 |
| α | 0.1 |
| r | 2 |
| γ | 0.9 |
| Q(s',a') | 6 |

target = 2 + 0.9 × 6 = 7.4

Q = 5 + 0.1(7.4 − 5)

New Q value = 5.24


==================================================

# 5 Todd Kelley Style Practice Questions

1 Which algorithm is off‑policy?

a SARSA
b Q‑Learning
c Monte Carlo
d Policy Gradient

Answer
b


2 Which equation defines the value of a state?

a Bellman equation
b Update equation
c Gradient descent
d Transition equation

Answer
a


3 What does the discount factor control?

a reward normalization
b importance of future reward
c policy selection
d environment update

Answer
b


4 What does exploration mean in reinforcement learning?

a always choose best action
b try new actions
c remove randomness
d maximize reward immediately

Answer
b


5 Which function evaluates the value of a state‑action pair?

a V(s)
b Q(s,a)
c π(s)
d R(s)

Answer
b


6 Which component chooses the action?

a environment
b reward
c agent
d state

Answer
c


7 If γ is close to 1 what happens?

a future rewards become more important
b immediate reward only
c learning stops
d rewards ignored

Answer
a


8 Which algorithm uses the max future Q value?

a SARSA
b Q‑Learning
c Monte Carlo
d Policy Gradient

Answer
b


9 Which algorithm uses the next chosen action value?

a Q‑Learning
b SARSA
c DQN
d Actor‑Critic

Answer
b


10 What does a policy represent?

a reward function
b mapping from state to action
c transition probability
d environment rule

Answer
b
