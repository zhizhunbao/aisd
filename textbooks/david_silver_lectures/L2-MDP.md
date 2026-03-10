# L2-MDP

> Source: L2-MDP.pdf (57 pages)

---


## Page 1

Lecture 2: Markov Decision Processes
Lecture 2: Markov Decision Processes
David Silver


## Page 2

Lecture 2: Markov Decision Processes
1 Markov Processes
2 Markov Reward Processes
3 Markov Decision Processes
4 Extensions to MDPs


## Page 3

Lecture 2: Markov Decision Processes
Markov Processes
Introduction
Introduction to MDPs
Markov decision processes formally describe an environment
for reinforcement learning
Where the environment is fully observable
i.e. The current state completely characterises the process
Almost all RL problems can be formalised as MDPs, e.g.
Optimal control primarily deals with continuous MDPs
Partially observable problems can be converted into MDPs
Bandits are MDPs with one state


## Page 4

Lecture 2: Markov Decision Processes
Markov Processes
Markov Property
Markov Property
“The future is independent of the past given the present”
Deﬁnition
A state St is Markov if and only if
P [St+1 | St] = P [St+1 | S1, ..., St]
The state captures all relevant information from the history
Once the state is known, the history may be thrown away
i.e. The state is a suﬃcient statistic of the future


## Page 5

Lecture 2: Markov Decision Processes
Markov Processes
Markov Property
State Transition Matrix
For a Markov state s and successor state s′, the state transition
probability is deﬁned by
Pss′ = P

St+1 = s′ | St = s

State transition matrix P deﬁnes transition probabilities from all
states s to all successor states s′,
to
P
= from


P11
. . .
P1n
...
Pn1
. . .
Pnn


where each row of the matrix sums to 1.


## Page 6

Lecture 2: Markov Decision Processes
Markov Processes
Markov Chains
Markov Process
A Markov process is a memoryless random process, i.e. a sequence
of random states S1, S2, ... with the Markov property.
Deﬁnition
A Markov Process (or Markov Chain) is a tuple ⟨S, P⟩
S is a (ﬁnite) set of states
P is a state transition probability matrix,
Pss′ = P [St+1 = s′ | St = s]


## Page 7

Lecture 2: Markov Decision Processes
Markov Processes
Markov Chains
Example: Student Markov Chain
0.5
0.5
0.2
0.8
0.6
0.4
Sleep
Facebook
Class 2
0.9
0.1
Pub
Class 3
Pass
Class 1
0.2
0.4
0.4
1.0


## Page 8

Lecture 2: Markov Decision Processes
Markov Processes
Markov Chains
Example: Student Markov Chain Episodes
0.5
0.5
0.2
0.8
0.6
0.4
Sleep
Facebook
Class 2
0.9
0.1
Pub
Class 3
Pass
Class 1
0.2
0.4
0.4
1.0
Sample episodes for Student Markov
Chain starting from S1 = C1
S1, S2, ..., ST
C1 C2 C3 Pass Sleep
C1 FB FB C1 C2 Sleep
C1 C2 C3 Pub C2 C3 Pass Sleep
C1 FB FB C1 C2 C3 Pub C1 FB FB
FB C1 C2 C3 Pub C2 Sleep


## Page 9

Lecture 2: Markov Decision Processes
Markov Processes
Markov Chains
Example: Student Markov Chain Transition Matrix
0.5
0.5
0.2
0.8
0.6
0.4
Sleep
Facebook
Class 2
0.9
0.1
Pub
Class 3
Pass
Class 1
0.2
0.4
0.4
1.0
P =


C1
C2
C3
Pass
Pub
FB
Sleep
C1
0.5
0.5
C2
0.8
0.2
C3
0.6
0.4
Pass
1.0
Pub
0.2
0.4
0.4
FB
0.1
0.9
Sleep
1




## Page 10

Lecture 2: Markov Decision Processes
Markov Reward Processes
MRP
Markov Reward Process
A Markov reward process is a Markov chain with values.
Deﬁnition
A Markov Reward Process is a tuple ⟨S, P, R, γ⟩
S is a ﬁnite set of states
P is a state transition probability matrix,
Pss′ = P [St+1 = s′ | St = s]
R is a reward function, Rs = E [Rt+1 | St = s]
γ is a discount factor, γ ∈[0, 1]


## Page 11

Lecture 2: Markov Decision Processes
Markov Reward Processes
MRP
Example: Student MRP
R = +10
0.5
0.5
0.2
0.8
0.6
0.4
Sleep
Facebook
Class 2
0.9
0.1
R = +1
R = -1
R = 0
Pub
Class 3
Pass
Class 1
R = -2
R = -2
R = -2
0.2
0.4
0.4
1.0


## Page 12

Lecture 2: Markov Decision Processes
Markov Reward Processes
Return
Return
Deﬁnition
The return Gt is the total discounted reward from time-step t.
Gt = Rt+1 + γRt+2 + ... =
∞
X
k=0
γkRt+k+1
The discount γ ∈[0, 1] is the present value of future rewards
The value of receiving reward R after k + 1 time-steps is γkR.
This values immediate reward above delayed reward.
γ close to 0 leads to ”myopic” evaluation
γ close to 1 leads to ”far-sighted” evaluation


## Page 13

Lecture 2: Markov Decision Processes
Markov Reward Processes
Return
Why discount?
Most Markov reward and decision processes are discounted. Why?
Mathematically convenient to discount rewards
Avoids inﬁnite returns in cyclic Markov processes
Uncertainty about the future may not be fully represented
If the reward is ﬁnancial, immediate rewards may earn more
interest than delayed rewards
Animal/human behaviour shows preference for immediate
reward
It is sometimes possible to use undiscounted Markov reward
processes (i.e. γ = 1), e.g. if all sequences terminate.


## Page 14

Lecture 2: Markov Decision Processes
Markov Reward Processes
Value Function
Value Function
The value function v(s) gives the long-term value of state s
Deﬁnition
The state value function v(s) of an MRP is the expected return
starting from state s
v(s) = E [Gt | St = s]


## Page 15

Lecture 2: Markov Decision Processes
Markov Reward Processes
Value Function
Example: Student MRP Returns
Sample returns for Student MRP:
Starting from S1 = C1 with γ = 1
2
G1 = R2 + γR3 + ... + γT−2RT
C1 C2 C3 Pass Sleep
v1 = −2 −2 ∗1
2 −2 ∗1
4 + 10 ∗1
8
=
−2.25
C1 FB FB C1 C2 Sleep
v1 = −2 −1 ∗1
2 −1 ∗1
4 −2 ∗1
8 −2 ∗
1
16
=
−3.125
C1 C2 C3 Pub C2 C3 Pass Sleep
v1 = −2 −2 ∗1
2 −2 ∗1
4 + 1 ∗1
8 −2 ∗
1
16 ...
=
−3.41
C1 FB FB C1 C2 C3 Pub C1 ...
v1 = −2 −1 ∗1
2 −1 ∗1
4 −2 ∗1
8 −2 ∗
1
16 ...
=
−3.20
FB FB FB C1 C2 C3 Pub C2 Sleep


## Page 16

Lecture 2: Markov Decision Processes
Markov Reward Processes
Value Function
Example: State-Value Function for Student MRP (1)
10
-2
-2
-2
0
-1
R = +10
0.5
0.5
0.2
0.8
0.6
0.4
0.9
0.1
R = +1
R = -1
R = 0
+1
R = -2
R = -2
R = -2
0.2
0.4
0.4
1.0
v(s) for γ =0


## Page 17

Lecture 2: Markov Decision Processes
Markov Reward Processes
Value Function
Example: State-Value Function for Student MRP (2)
10
-5.0
0.9
4.1
0
-7.6
R = +10
0.5
0.5
0.2
0.8
0.6
0.4
0.9
0.1
R = +1
R = -1
R = 0
1.9
R = -2
R = -2
R = -2
0.2
0.4
0.4
1.0
v(s) for γ =0.9


## Page 18

Lecture 2: Markov Decision Processes
Markov Reward Processes
Value Function
Example: State-Value Function for Student MRP (3)
10
-13
1.5
4.3
0
-23
R = +10
0.5
0.5
0.2
0.8
0.6
0.4
0.9
0.1
R = +1
R = -1
R = 0
+0.8
R = -2
R = -2
R = -2
0.2
0.4
0.4
1.0
v(s) for γ =1


## Page 19

Lecture 2: Markov Decision Processes
Markov Reward Processes
Bellman Equation
Bellman Equation for MRPs
The value function can be decomposed into two parts:
immediate reward Rt+1
discounted value of successor state γv(St+1)
v(s) = E [Gt | St = s]
= E

Rt+1 + γRt+2 + γ2Rt+3 + ... | St = s

= E [Rt+1 + γ (Rt+2 + γRt+3 + ...) | St = s]
= E [Rt+1 + γGt+1 | St = s]
= E [Rt+1 + γv(St+1) | St = s]


## Page 20

Lecture 2: Markov Decision Processes
Markov Reward Processes
Bellman Equation
Bellman Equation for MRPs (2)
v(s) = E [Rt+1 + γv(St+1) | St = s]
v(s)
7!
s
v(s0)
7!
s0
r
v(s) = Rs + γ
X
s′∈S
Pss′v(s′)


## Page 21

Lecture 2: Markov Decision Processes
Markov Reward Processes
Bellman Equation
Example: Bellman Equation for Student MRP
10
-13
1.5
4.3
0
-23
R = +10
0.5
0.5
0.2
0.8
0.6
0.4
0.9
0.1
R = +1
R = -1
R = 0
0.8
R = -2
R = -2
R = -2
0.2
0.4
0.4
1.0
4.3 = -2 + 0.6*10 + 0.4*0.8


## Page 22

Lecture 2: Markov Decision Processes
Markov Reward Processes
Bellman Equation
Bellman Equation in Matrix Form
The Bellman equation can be expressed concisely using matrices,
v = R + γPv
where v is a column vector with one entry per state


v(1)
...
v(n)

=


R1
...
Rn

+ γ


P11
. . .
P1n
...
P11
. . .
Pnn




v(1)
...
v(n)




## Page 23

Lecture 2: Markov Decision Processes
Markov Reward Processes
Bellman Equation
Solving the Bellman Equation
The Bellman equation is a linear equation
It can be solved directly:
v = R + γPv
(I −γP) v = R
v = (I −γP)−1 R
Computational complexity is O(n3) for n states
Direct solution only possible for small MRPs
There are many iterative methods for large MRPs, e.g.
Dynamic programming
Monte-Carlo evaluation
Temporal-Diﬀerence learning


## Page 24

Lecture 2: Markov Decision Processes
Markov Decision Processes
MDP
Markov Decision Process
A Markov decision process (MDP) is a Markov reward process with
decisions. It is an environment in which all states are Markov.
Deﬁnition
A Markov Decision Process is a tuple ⟨S, A, P, R, γ⟩
S is a ﬁnite set of states
A is a ﬁnite set of actions
P is a state transition probability matrix,
Pa
ss′ = P [St+1 = s′ | St = s, At = a]
R is a reward function, Ra
s = E [Rt+1 | St = s, At = a]
γ is a discount factor γ ∈[0, 1].


## Page 25

Lecture 2: Markov Decision Processes
Markov Decision Processes
MDP
Example: Student MDP
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0


## Page 26

Lecture 2: Markov Decision Processes
Markov Decision Processes
Policies
Policies (1)
Deﬁnition
A policy π is a distribution over actions given states,
π(a|s) = P [At = a | St = s]
A policy fully deﬁnes the behaviour of an agent
MDP policies depend on the current state (not the history)
i.e. Policies are stationary (time-independent),
At ∼π(·|St), ∀t > 0


## Page 27

Lecture 2: Markov Decision Processes
Markov Decision Processes
Policies
Policies (2)
Given an MDP M = ⟨S, A, P, R, γ⟩and a policy π
The state sequence S1, S2, ... is a Markov process ⟨S, Pπ⟩
The state and reward sequence S1, R2, S2, ... is a Markov
reward process ⟨S, Pπ, Rπ, γ⟩
where
Pπ
s,s′ =
X
a∈A
π(a|s)Pa
ss′
Rπ
s =
X
a∈A
π(a|s)Ra
s


## Page 28

Lecture 2: Markov Decision Processes
Markov Decision Processes
Value Functions
Value Function
Deﬁnition
The state-value function vπ(s) of an MDP is the expected return
starting from state s, and then following policy π
vπ(s) = Eπ [Gt | St = s]
Deﬁnition
The action-value function qπ(s, a) is the expected return
starting from state s, taking action a, and then following policy π
qπ(s, a) = Eπ [Gt | St = s, At = a]


## Page 29

Lecture 2: Markov Decision Processes
Markov Decision Processes
Value Functions
Example: State-Value Function for Student MDP
-1.3
2.7
7.4
0
-2.3
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
vπ(s) for π(a|s)=0.5, γ =1


## Page 30

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation
The state-value function can again be decomposed into immediate
reward plus discounted value of successor state,
vπ(s) = Eπ [Rt+1 + γvπ(St+1) | St = s]
The action-value function can similarly be decomposed,
qπ(s, a) = Eπ [Rt+1 + γqπ(St+1, At+1) | St = s, At = a]


## Page 31

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation for V π
v⇡(s)
7!
s
q⇡(s, a)
7!
a
vπ(s) =
X
a∈A
π(a|s)qπ(s, a)


## Page 32

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation for Qπ
v⇡(s0)
7!
s0
q⇡(s, a)
7!
s, a
r
qπ(s, a) = Ra
s + γ
X
s′∈S
Pa
ss′vπ(s′)


## Page 33

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation for vπ (2)
v⇡(s0)
7!
s0
v⇡(s)
7!
s
r
a
vπ(s) =
X
a∈A
π(a|s)
 
Ra
s + γ
X
s′∈S
Pa
ss′vπ(s′)
!


## Page 34

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation for qπ (2)
q⇡(s, a)
7!
s, a
q⇡(s0, a0)
7!
a0
r
s0
qπ(s, a) = Ra
s + γ
X
s′∈S
Pa
ss′
X
a′∈A
π(a′|s′)qπ(s′, a′)


## Page 35

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Example: Bellman Expectation Equation in Student MDP
-1.3
2.7
7.4
0
-2.3
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
7.4 = 0.5 * (1 + 0.2* -1.3 + 0.4 * 2.7 + 0.4 * 7.4) 
+ 0.5 * 10


## Page 36

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Expectation Equation
Bellman Expectation Equation (Matrix Form)
The Bellman expectation equation can be expressed concisely
using the induced MRP,
vπ = Rπ + γPπvπ
with direct solution
vπ = (I −γPπ)−1 Rπ


## Page 37

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Optimal Value Function
Deﬁnition
The optimal state-value function v∗(s) is the maximum value
function over all policies
v∗(s) = max
π
vπ(s)
The optimal action-value function q∗(s, a) is the maximum
action-value function over all policies
q∗(s, a) = max
π
qπ(s, a)
The optimal value function speciﬁes the best possible
performance in the MDP.
An MDP is “solved” when we know the optimal value fn.


## Page 38

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Example: Optimal Value Function for Student MDP
6
8
10
0
6
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
v*(s) for γ =1


## Page 39

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Example: Optimal Action-Value Function for Student MDP
6
8
10
0
6
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
q*(s,a) for γ =1
q* =5
q* =6
q* =6
q* =5
q* =8
q* = 0
q* =10
q* =8.4


## Page 40

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Optimal Policy
Deﬁne a partial ordering over policies
π ≥π′ if vπ(s) ≥vπ′(s), ∀s
Theorem
For any Markov Decision Process
There exists an optimal policy π∗that is better than or equal
to all other policies, π∗≥π, ∀π
All optimal policies achieve the optimal value function,
vπ∗(s) = v∗(s)
All optimal policies achieve the optimal action-value function,
qπ∗(s, a) = q∗(s, a)


## Page 41

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Finding an Optimal Policy
An optimal policy can be found by maximising over q∗(s, a),
π∗(a|s) =
( 1
if a = argmax
a∈A
q∗(s, a)
0
otherwise
There is always a deterministic optimal policy for any MDP
If we know q∗(s, a), we immediately have the optimal policy


## Page 42

Lecture 2: Markov Decision Processes
Markov Decision Processes
Optimal Value Functions
Example: Optimal Policy for Student MDP
6
8
10
0
6
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
π*(a|s) for γ =1
q* =5
q* =6
q* =6
q* =5
q* =8
q* =0
q* =10
q* =8.4


## Page 43

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Bellman Optimality Equation for v∗
The optimal value functions are recursively related by the Bellman
optimality equations:
v⇤(s)
7!
s
q⇤(s, a)
7!
a
v∗(s) = max
a
q∗(s, a)


## Page 44

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Bellman Optimality Equation for Q∗
q⇤(s, a)
7!
s, a
v⇤(s0)
7!
s0
r
q∗(s, a) = Ra
s + γ
X
s′∈S
Pa
ss′v∗(s′)


## Page 45

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Bellman Optimality Equation for V ∗(2)
v⇤(s0)
7!
s0
v⇤(s)
7!
s
a
r
v∗(s) = max
a
Ra
s + γ
X
s′∈S
Pa
ss′v∗(s′)


## Page 46

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Bellman Optimality Equation for Q∗(2)
q⇤(s0, a0)
7!
a0
r
q⇤(s, a)
7!
s, a
s0
q∗(s, a) = Ra
s + γ
X
s′∈S
Pa
ss′max
a′
q∗(s′, a′)


## Page 47

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Example: Bellman Optimality Equation in Student MDP
6
8
10
0
6
R = +10
R = +1
R = -1
R = 0
R = -2
R = -2
0.2
0.4
0.4
Study
Facebook
Study
Sleep
Facebook
Quit
Pub
Study
R = -1
R = 0
6 = max {-2 + 8,  -1 + 6}


## Page 48

Lecture 2: Markov Decision Processes
Markov Decision Processes
Bellman Optimality Equation
Solving the Bellman Optimality Equation
Bellman Optimality Equation is non-linear
No closed form solution (in general)
Many iterative solution methods
Value Iteration
Policy Iteration
Q-learning
Sarsa


## Page 49

Lecture 2: Markov Decision Processes
Extensions to MDPs
Extensions to MDPs
(no exam)
Inﬁnite and continuous MDPs
Partially observable MDPs
Undiscounted, average reward MDPs


## Page 50

Lecture 2: Markov Decision Processes
Extensions to MDPs
Inﬁnite MDPs
Inﬁnite MDPs
(no exam)
The following extensions are all possible:
Countably inﬁnite state and/or action spaces
Straightforward
Continuous state and/or action spaces
Closed form for linear quadratic model (LQR)
Continuous time
Requires partial diﬀerential equations
Hamilton-Jacobi-Bellman (HJB) equation
Limiting case of Bellman equation as time-step →0


## Page 51

Lecture 2: Markov Decision Processes
Extensions to MDPs
Partially Observable MDPs
POMDPs
(no exam)
A Partially Observable Markov Decision Process is an MDP with
hidden states. It is a hidden Markov model with actions.
Deﬁnition
A POMDP is a tuple ⟨S, A, O, P, R, Z, γ⟩
S is a ﬁnite set of states
A is a ﬁnite set of actions
O is a ﬁnite set of observations
P is a state transition probability matrix,
Pa
ss′ = P [St+1 = s′ | St = s, At = a]
R is a reward function, Ra
s = E [Rt+1 | St = s, At = a]
Z is an observation function,
Za
s′o = P [Ot+1 = o | St+1 = s′, At = a]
γ is a discount factor γ ∈[0, 1].


## Page 52

Lecture 2: Markov Decision Processes
Extensions to MDPs
Partially Observable MDPs
Belief States
(no exam)
Deﬁnition
A history Ht is a sequence of actions, observations and rewards,
Ht = A0, O1, R1, ..., At−1, Ot, Rt
Deﬁnition
A belief state b(h) is a probability distribution over states,
conditioned on the history h
b(h) = (P

St = s1 | Ht = h

, ..., P [St = sn | Ht = h])


## Page 53

Lecture 2: Markov Decision Processes
Extensions to MDPs
Partially Observable MDPs
Reductions of POMDPs
(no exam)
The history Ht satisﬁes the Markov property
The belief state b(Ht) satisﬁes the Markov property
a1
a2
a1o1
a1o2
a2o1
a2o2
a1o1a1
a1o1a2
...
...
...
a1
a2
o1
o2
o1
o2
a1
a2
...
...
...
a1
a2
o1
o2
o1
o2
a1
a2
P(s)
P(s|a1)
P(s|a2)
P(s|a1o1)
P(s|a1o2)
P(s|a2o1)
P(s|a2o2)
History tree
Belief tree
P(s|a1o1a1) P(s|a1o1a2)
A POMDP can be reduced to an (inﬁnite) history tree
A POMDP can be reduced to an (inﬁnite) belief state tree


## Page 54

Lecture 2: Markov Decision Processes
Extensions to MDPs
Average Reward MDPs
Ergodic Markov Process
(no exam)
An ergodic Markov process is
Recurrent: each state is visited an inﬁnite number of times
Aperiodic: each state is visited without any systematic period
Theorem
An ergodic Markov process has a limiting stationary distribution
dπ(s) with the property
dπ(s) =
X
s′∈S
dπ(s′)Ps′s


## Page 55

Lecture 2: Markov Decision Processes
Extensions to MDPs
Average Reward MDPs
Ergodic MDP
(no exam)
Deﬁnition
An MDP is ergodic if the Markov chain induced by any policy is
ergodic.
For any policy π, an ergodic MDP has an average reward per
time-step ρπ that is independent of start state.
ρπ = lim
T→∞
1
T E
" T
X
t=1
Rt
#


## Page 56

Lecture 2: Markov Decision Processes
Extensions to MDPs
Average Reward MDPs
Average Reward Value Function
(no exam)
The value function of an undiscounted, ergodic MDP can be
expressed in terms of average reward.
˜vπ(s) is the extra reward due to starting from state s,
˜vπ(s) = Eπ
" ∞
X
k=1
(Rt+k −ρπ) | St = s
#
There is a corresponding average reward Bellman equation,
˜vπ(s) = Eπ
"
(Rt+1 −ρπ) +
∞
X
k=1
(Rt+k+1 −ρπ) | St = s
#
= Eπ [(Rt+1 −ρπ) + ˜vπ(St+1) | St = s]


## Page 57

Lecture 2: Markov Decision Processes
Extensions to MDPs
Average Reward MDPs
Questions?
The only stupid question is the one you were afraid to
ask but never did.
-Rich Sutton
