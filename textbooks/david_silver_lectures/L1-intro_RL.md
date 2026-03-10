# L1-intro_RL

> Source: L1-intro_RL.pdf (46 pages)

---


## Page 1

Lecture 1: Introduction to Reinforcement Learning
Lecture 1: Introduction to Reinforcement
Learning
David Silver


## Page 2

Lecture 1: Introduction to Reinforcement Learning
Outline
1 Admin
2 About Reinforcement Learning
3 The Reinforcement Learning Problem
4 Inside An RL Agent
5 Problems within Reinforcement Learning


## Page 3

Lecture 1: Introduction to Reinforcement Learning
Admin
Class Information
Thursdays 9:30 to 11:00am
Website:
http://www.cs.ucl.ac.uk/staﬀ/D.Silver/web/Teaching.html
Group:
http://groups.google.com/group/csml-advanced-topics
Contact me: d.silver@cs.ucl.ac.uk


## Page 4

Lecture 1: Introduction to Reinforcement Learning
Admin
Assessment
Assessment will be 50% coursework, 50% exam
Coursework
Assignment A: RL problem
Assignment B: Kernels problem
Assessment = max(assignment1, assignment2)
Examination
A: 3 RL questions
B: 3 kernels questions
Answer any 3 questions


## Page 5

Lecture 1: Introduction to Reinforcement Learning
Admin
Textbooks
An Introduction to Reinforcement Learning, Sutton and
Barto, 1998
MIT Press, 1998
∼40 pounds
Available free online!
http://webdocs.cs.ualberta.ca/∼sutton/book/the-book.html
Algorithms for Reinforcement Learning, Szepesvari
Morgan and Claypool, 2010
∼20 pounds
Available free online!
http://www.ualberta.ca/∼szepesva/papers/RLAlgsInMDPs.pdf


## Page 6

Lecture 1: Introduction to Reinforcement Learning
About RL
Many Faces of Reinforcement Learning
Computer Science
Economics
Mathematics
Engineering
Neuroscience
Psychology
Machine 
Learning
Classical/Operant
Conditioning
Optimal 
Control
Reward
System
Operations 
Research
Bounded
Rationality
Reinforcement 
Learning


## Page 7

Lecture 1: Introduction to Reinforcement Learning
About RL
Branches of Machine Learning
Reinforcement 
Learning
Supervised 
Learning
Unsupervised 
Learning
Machine
Learning


## Page 8

Lecture 1: Introduction to Reinforcement Learning
About RL
Characteristics of Reinforcement Learning
What makes reinforcement learning diﬀerent from other machine
learning paradigms?
There is no supervisor, only a reward signal
Feedback is delayed, not instantaneous
Time really matters (sequential, non i.i.d data)
Agent’s actions aﬀect the subsequent data it receives


## Page 9

Lecture 1: Introduction to Reinforcement Learning
About RL
Examples of Reinforcement Learning
Fly stunt manoeuvres in a helicopter
Defeat the world champion at Backgammon
Manage an investment portfolio
Control a power station
Make a humanoid robot walk
Play many diﬀerent Atari games better than humans


## Page 10

Lecture 1: Introduction to Reinforcement Learning
About RL
Helicopter Manoeuvres


## Page 11

Lecture 1: Introduction to Reinforcement Learning
About RL
Bipedal Robots


## Page 12

Lecture 1: Introduction to Reinforcement Learning
About RL
Atari


## Page 13

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
Reward
Rewards
A reward Rt is a scalar feedback signal
Indicates how well agent is doing at step t
The agent’s job is to maximise cumulative reward
Reinforcement learning is based on the reward hypothesis
Deﬁnition (Reward Hypothesis)
All goals can be described by the maximisation of expected
cumulative reward
Do you agree with this statement?


## Page 14

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
Reward
Examples of Rewards
Fly stunt manoeuvres in a helicopter
+ve reward for following desired trajectory
−ve reward for crashing
Defeat the world champion at Backgammon
+/−ve reward for winning/losing a game
Manage an investment portfolio
+ve reward for each $ in bank
Control a power station
+ve reward for producing power
−ve reward for exceeding safety thresholds
Make a humanoid robot walk
+ve reward for forward motion
−ve reward for falling over
Play many diﬀerent Atari games better than humans
+/−ve reward for increasing/decreasing score


## Page 15

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
Reward
Sequential Decision Making
Goal: select actions to maximise total future reward
Actions may have long term consequences
Reward may be delayed
It may be better to sacriﬁce immediate reward to gain more
long-term reward
Examples:
A ﬁnancial investment (may take months to mature)
Refuelling a helicopter (might prevent a crash in several hours)
Blocking opponent moves (might help winning chances many
moves from now)


## Page 16

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
Environments
Agent and Environment
observation
reward
action
At
Rt
Ot


## Page 17

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
Environments
Agent and Environment
observation
reward
action
At
Rt
Ot
At each step t the agent:
Executes action At
Receives observation Ot
Receives scalar reward Rt
The environment:
Receives action At
Emits observation Ot+1
Emits scalar reward Rt+1
t increments at env. step


## Page 18

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
History and State
The history is the sequence of observations, actions, rewards
Ht = O1, R1, A1, ..., At−1, Ot, Rt
i.e. all observable variables up to time t
i.e. the sensorimotor stream of a robot or embodied agent
What happens next depends on the history:
The agent selects actions
The environment selects observations/rewards
State is the information used to determine what happens next
Formally, state is a function of the history:
St = f (Ht)


## Page 19

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Environment State
observation
reward
action
At
Rt
Ot
St
e
environment state
The environment state Se
t is
the environment’s private
representation
i.e. whatever data the
environment uses to pick the
next observation/reward
The environment state is not
usually visible to the agent
Even if Se
t is visible, it may
contain irrelevant
information


## Page 20

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Agent State
observation
reward
action
At
Rt
Ot
St
a
agent state
The agent state Sa
t is the
agent’s internal
representation
i.e. whatever information
the agent uses to pick the
next action
i.e. it is the information
used by reinforcement
learning algorithms
It can be any function of
history:
Sa
t = f (Ht)


## Page 21

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Information State
An information state (a.k.a. Markov state) contains all useful
information from the history.
Deﬁnition
A state St is Markov if and only if
P[St+1 | St] = P[St+1 | S1, ..., St]
“The future is independent of the past given the present”
H1:t →St →Ht+1:∞
Once the state is known, the history may be thrown away
i.e. The state is a suﬃcient statistic of the future
The environment state Se
t is Markov
The history Ht is Markov


## Page 22

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Rat Example
What if agent state = last 3 items in sequence?
What if agent state = counts for lights, bells and levers?
What if agent state = complete sequence?


## Page 23

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Fully Observable Environments
state
reward
action
At
Rt
St
Full observability: agent directly
observes environment state
Ot = Sa
t = Se
t
Agent state = environment
state = information state
Formally, this is a Markov
decision process (MDP)
(Next lecture and the
majority of this course)


## Page 24

Lecture 1: Introduction to Reinforcement Learning
The RL Problem
State
Partially Observable Environments
Partial observability: agent indirectly observes environment:
A robot with camera vision isn’t told its absolute location
A trading agent only observes current prices
A poker playing agent only observes public cards
Now agent state ̸= environment state
Formally this is a partially observable Markov decision process
(POMDP)
Agent must construct its own state representation Sa
t , e.g.
Complete history: Sa
t = Ht
Beliefs of environment state: Sa
t = (P[Se
t = s1], ..., P[Se
t = sn])
Recurrent neural network: Sa
t = σ(Sa
t−1Ws + OtWo)


## Page 25

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Major Components of an RL Agent
An RL agent may include one or more of these components:
Policy: agent’s behaviour function
Value function: how good is each state and/or action
Model: agent’s representation of the environment


## Page 26

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Policy
A policy is the agent’s behaviour
It is a map from state to action, e.g.
Deterministic policy: a = π(s)
Stochastic policy: π(a|s) = P[At = a|St = s]


## Page 27

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Value Function
Value function is a prediction of future reward
Used to evaluate the goodness/badness of states
And therefore to select between actions, e.g.
vπ(s) = Eπ

Rt+1 + γRt+2 + γ2Rt+3 + ... | St = s



## Page 28

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Example: Value Function in Atari


## Page 29

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Model
A model predicts what the environment will do next
P predicts the next state
R predicts the next (immediate) reward, e.g.
Pa
ss′ = P[St+1 = s′ | St = s, At = a]
Ra
s = E [Rt+1 | St = s, At = a]


## Page 30

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Maze Example
Start
Goal
Rewards: -1 per time-step
Actions: N, E, S, W
States: Agent’s location


## Page 31

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Maze Example: Policy
Start
Goal
Arrows represent policy π(s) for each state s


## Page 32

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Maze Example: Value Function
-14
-13
-12
-11
-10
-9
-16
-15
-12
-8
-16
-17
-6
-7
-18
-19
-5
-24
-20
-4
-3
-23
-22
-21
-22
-2
-1
Start
Goal
Numbers represent value vπ(s) of each state s


## Page 33

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Maze Example: Model
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
-1
Start
Goal
Agent may have an internal
model of the environment
Dynamics: how actions
change the state
Rewards: how much reward
from each state
The model may be imperfect
Grid layout represents transition model Pa
ss′
Numbers represent immediate reward Ra
s from each state s
(same for all a)


## Page 34

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Categorizing RL agents (1)
Value Based
No Policy (Implicit)
Value Function
Policy Based
Policy
No Value Function
Actor Critic
Policy
Value Function


## Page 35

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
Categorizing RL agents (2)
Model Free
Policy and/or Value Function
No Model
Model Based
Policy and/or Value Function
Model


## Page 36

Lecture 1: Introduction to Reinforcement Learning
Inside An RL Agent
RL Agent Taxonomy
Model
Value Function
Policy
Actor
Critic
Value-Based
Policy-Based
Model-Free 
Model-Based 


## Page 37

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Learning and Planning
Two fundamental problems in sequential decision making
Reinforcement Learning:
The environment is initially unknown
The agent interacts with the environment
The agent improves its policy
Planning:
A model of the environment is known
The agent performs computations with its model (without any
external interaction)
The agent improves its policy
a.k.a. deliberation, reasoning, introspection, pondering,
thought, search


## Page 38

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Atari Example: Reinforcement Learning
observation
reward
action
At
Rt
Ot
Rules of the game are
unknown
Learn directly from
interactive game-play
Pick actions on
joystick, see pixels
and scores


## Page 39

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Atari Example: Planning
Rules of the game are known
Can query emulator
perfect model inside agent’s brain
If I take action a from state s:
what would the next state be?
what would the score be?
Plan ahead to ﬁnd optimal policy
e.g. tree search
right
left
right
right
left
left


## Page 40

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Exploration and Exploitation (1)
Reinforcement learning is like trial-and-error learning
The agent should discover a good policy
From its experiences of the environment
Without losing too much reward along the way


## Page 41

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Exploration and Exploitation (2)
Exploration ﬁnds more information about the environment
Exploitation exploits known information to maximise reward
It is usually important to explore as well as exploit


## Page 42

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Examples
Restaurant Selection
Exploitation Go to your favourite restaurant
Exploration Try a new restaurant
Online Banner Advertisements
Exploitation Show the most successful advert
Exploration Show a diﬀerent advert
Oil Drilling
Exploitation Drill at the best known location
Exploration Drill at a new location
Game Playing
Exploitation Play the move you believe is best
Exploration Play an experimental move


## Page 43

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Prediction and Control
Prediction: evaluate the future
Given a policy
Control: optimise the future
Find the best policy


## Page 44

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Gridworld Example: Prediction
3.3 8.8 4.4 5.3 1.5
1.5 3.0 2.3 1.9 0.5
0.1 0.7 0.7 0.4 -0.4
-1.0 -0.4 -0.4 -0.6 -1.2
-1.9 -1.3 -1.2 -1.4 -2.0
A
B
A’
B’
+10
+5
Actions
(a)
(b)
What is the value function for the uniform random policy?


## Page 45

Lecture 1: Introduction to Reinforcement Learning
Problems within RL
Gridworld Example: Control
a) gridworld
b) V*
c) *
22.0 24.4 22.0 19.4 17.5
19.8 22.0 19.8 17.8 16.0
17.8 19.8 17.8 16.0 14.4
16.0 17.8 16.0 14.4 13.0
14.4 16.0 14.4 13.0 11.7
A
B
A’
B’
+10
+5
π
v⇤
⇡⇤
What is the optimal value function over all possible policies?
What is the optimal policy?


## Page 46

Lecture 1: Introduction to Reinforcement Learning
Course Outline
Course Outline
Part I: Elementary Reinforcement Learning
1 Introduction to RL
2 Markov Decision Processes
3 Planning by Dynamic Programming
4 Model-Free Prediction
5 Model-Free Control
Part II: Reinforcement Learning in Practice
1 Value Function Approximation
2 Policy Gradient Methods
3 Integrating Learning and Planning
4 Exploration and Exploitation
5 Case study - RL in games
