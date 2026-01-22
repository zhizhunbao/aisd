# Q-Learning Math - Python Code

**Source:** https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6

---

# Math of Q-Learning — Python
## Derive the Bellman equation from scratch
[![Omar Aflak](https://miro.medium.com/v2/resize:fill:32:32/1*qRE-csBHtvwOsE2M_YV7UQ.png)](/@omaraflak?source=post_page---byline--5dcbdc49b6f6---------------------------------------)
[Omar Aflak](/@omaraflak?source=post_page---byline--5dcbdc49b6f6---------------------------------------)
Dec 6, 2018
![](https://miro.medium.com/v2/resize:fit:700/0*aOdvtfjd2JClq20o)
Photo by [Brett Jordan](https://unsplash.com/@brett_jordan?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)
### **UPDATE: Check out the updated version of this article at**[**https://omaraflak.com/articles/q-learning**](https://omaraflak.com/articles/q-learning)
## Q-Learning
 _Q-Learning_ is a type of **_Reinforcement Learning_** which is a type of _Machine Learning_. Reinforcement learning has been used lately to teach AIs to play games (Google DeepMind Atari, etc). Our goal is to understand a simple version of reinforcement learning called Q-Learning, and write a program that will learn how to play a simple game. Let’s dive in!
## High-level overview
In Q-Learning, we call the program trying to solve the problem the **_agent_**. The agent is going to navigate an **_environment_** , that is the problem being solved. The environment is modeled mathematically by a _Markov Decision Process_ , which is a graph where each node is a **_state_** the agent may be in (think state in a game, e.g. position of the user, coins collected, etc.), and where the edges between those nodes are **_actions_** the agent can take to transition from one state to another (think commands in a game, e.g. right, left, jump, run, etc.). The goal of Q-Learning is to learn a so called **_Q-function_** , which tells the agent what action to take in a given state in order to maximize a **_reward_** function** __** that we will define.
## Markov Chain
A Markov chain is a mathematical model that experiences transition of states with probabilistic rules.
![](https://miro.medium.com/v2/resize:fit:220/1*xfK_RdBZOkE4buKDPDZdKg.png)
Markov chain — Wikipedia
Here we have two states **E** and **A** , and the probabilities of going from one state to another, e.g. there is 70% chance of going to state A starting from state E. In this model, you start from a node of the graph, and simply experience the transition probabilities.
## Markov Decision Process
A Markov Decision Process (MDP) is an extension of the Markov chain and it is used to model more complex environments. In this extension, we add the possibility to make a choice at every state which is called an **action**. We also add a **reward** which is a feedback from the environment for going from one state to another through an action.
![](https://miro.medium.com/v2/resize:fit:700/1*eevLRhyeokWPDFu1e7iuMQ.png)
Image by Author
In the image above, we are in the initial state **_don’t understand_** _,_ where we have two possible actions, **_study_** and **_don’t study_**. For the _study_ action, we may end up in different states according to a probabilistic rule. This is what we call a **stochastic** environment (random), in the sense that for one same action taken in the same state, we might have different results (**_understand_** and **_don’t understand_**).
_In reinforcement learning, this is how we model a game or environment, and our goal will be to maximize the_** _reward_** _we get from that environment._
## Reward
The reward is the feedback from the environment that tells us _how good_ we are doing. It can be the number of coins you grab in a game for example. Our goal is to maximize the total reward.
![](https://miro.medium.com/v2/resize:fit:511/0*lXszd8hM87XmeQLg.png)
We write **_Rt_** to denote the total reward we can get starting at some point **_t_** in time, as the sum of all the subsequent rewards earned at each time step.
For example, if we use the MDP presented above. We’re initially in the state **_don’t understand_** _,_ we take the __**_study_** __ action which takes us randomly to __**_don’t understand_**. Therefore we experienced the reward r(t+1)=-1. Now we can decide to take another action which will give r(t+2) and so on. The total reward is the sum of all the immediate rewards we get for taking actions in the environment.
Defining the reward this way leads to two major problems :
  * This sum can potentially go to infinity, which is problematic since we want to maximize it.
  * We are accounting as much for future rewards as we do for immediate rewards.
One way to fix up these problems is to use a decreasing factor for future rewards.
![](https://miro.medium.com/v2/resize:fit:577/0*mflzCazg40-MvyTu.png)
Setting **γ=1** takes us back to the first expression where every reward is equally important. Setting **γ=0** results in only looking for the immediate reward (always acting for the optimal next step). Setting **γ** between**0** and**1** is a compromise to look more for immediate reward but still account for future rewards.
We can rewrite that expression in a recursive manner, that will come handy later on.
![](https://miro.medium.com/v2/resize:fit:590/0*SLvOh8O40AgFlUFf.png)
## Policy
A policy is a function that tells what action to take in a certain state. This function is usually denoted **π(s,a)** and yields the probability of taking action **a** in state**s**. We want to **find the policy that maximizes the reward** function.
If we get back to the previous MDP for example, the policy can tell you the probability of taking action **_study_** __ when you’re in the state __**_don’t understand_** _._
## Get Omar Aflak’s stories in your inbox
Moreover, because this is a probability distribution, the sum over all the possible actions in a given state **must be equal to 1**.
![](https://miro.medium.com/v2/resize:fit:255/0*g4HPsjrUtYNqHTiK.png)
## Notations
We are going to start playing around with some equations, and for that we need to introduce new notations.
![](https://miro.medium.com/v2/resize:fit:700/0*_dLhsfjo8I_4Xb1X.png)
This is the expected **immediate reward r(t+1)** for going from state **s** to state **s’** through action **a**.
![](https://miro.medium.com/v2/resize:fit:676/0*bpCGFbMgE2LYD_-W.png)
This is the **transition probability** of going from state **s** to state **s’** through action **a**. In other words, the probability of ending up in state **s’** by taking action **a** in state **s**.
![](https://miro.medium.com/v2/resize:fit:700/1*eevLRhyeokWPDFu1e7iuMQ.png)
Image by Author
In this example :
  * The expected immediate reward for going from state __**_don’t understand_** to state **_don’t understand_** through action **_don’t study_** is equal to **0**.
  * The probability of going from state **_don’t understand_** to state **_understand_** through action **_study_** is equal to **80%**.
## **Value functions**
Two so-called “value functions” exist. The **state value** function, and the **action value** function. These functions are a way to measure the “value”, or _how good_ some state is, or _how good_ some action is, by looking at the reward obtained for being in a given state or taking a certain action.
### State value
![](https://miro.medium.com/v2/resize:fit:465/0*sjMCQm0KLpuJbDxd.png)
The _value_ of a state is the expected total reward we can get starting from that state. It depends on the policy **π** which dictates the actions to take.
### Value function
![](https://miro.medium.com/v2/resize:fit:637/0*vhfCtTbOJxElBWKd.png)
The _value_ of an action taken in some state is the expected total reward we can get starting from that state and taking that action. It also depends on the policy **π**.
## Bellman Equation for Q-Learning
Now that we are settled with notations we can finally start playing around with the math! Looking at the following diagram during the calculation can help you understand.
![](https://miro.medium.com/v2/resize:fit:586/1*Jy8LqMijoDoVADWexjLi0g.png)
Image by Author
We will start by expanding the state value function. The **_expected_** operator is **_linear_**.
![](https://miro.medium.com/v2/resize:fit:700/0*cK3VBvGUKU4Q4upU.png)
Next, we can expand the action value function.
![](https://miro.medium.com/v2/resize:fit:700/0*nQj2YTrt1B-1VgtV.png)
This form of the Q-Value is very generic. It handles stochastic environments, but we could write it down in a **deterministic** one. Meaning, whenever you take an action you always end up in the **same next state** and receive the **same reward**. In that case, we simply do not need to make a weighted sum with probabilities, and the equation becomes:
![](https://miro.medium.com/v2/resize:fit:343/0*XMde4eknDv11n547.png)
Where **s’** is the state you end up in for taking action **a** in state **s**. Written, more explicitly, this is:
![](https://miro.medium.com/v2/resize:fit:606/0*FZt3-7XbfIjNYQJx.png)
You can read that as the value of (the goodness of) taking action **a** in state **s(t)** , is the immediate reward obtained for taking action **a** in state **s(t)** plus the value of being in state **s(t+1)**(the expected future rewards for being in state **s(t+1)** …).
### Greedy Policy
You probably already came across _greedy policy_ reading on the internet. A greedy policy is a policy where you always choose the **optimal next step**.
![](https://miro.medium.com/v2/resize:fit:300/0*rQ7hXKOPSxcR271w.gif)
Greedy Algorithm — Wikipedia
In a **greedy policy context** , we can write a relation between the state value and the action value functions.
![](https://miro.medium.com/v2/resize:fit:380/0*1uaMoqlk7RTkWKba.png)
Therefore, plugging this into the previous equation, we get the Q-Value of a (state, action) pair in a deterministic environment, following a greedy policy.
![](https://miro.medium.com/v2/resize:fit:700/0*Oy_aMmqo0ghQRA56.png)
Or simply,
![](https://miro.medium.com/v2/resize:fit:515/0*Chz7J204az5VkjBi.png)
And this is the **Bellman equation** in the Q-Learning context ! It says that the value of an action **a** in some state **s** is the **immediate reward** you get for taking that action, plus the **maximum expected future rewards** you can get in the **next state**.
It actually makes sense when you think about it.
![](https://miro.medium.com/v2/resize:fit:401/1*aWIfTBbwF5DGGrc2Qfdd5A.png)
left or right ? — Image by Author
Here, if you only look at the**immediate reward** , you surely choose to go left. Unfortunately, the game ends after and you cannot get more points.
If you add the **maximum expected reward** of the **next state** , then you will most probably go to the right since the maximum expected reward of **_S1_** is equal to zero and the maximum expected reward of **_S2_** is probably higher than 10–5=5** _._**
You can also tweak **γ** to specify****_how important_**** are the next rewards.
## Python Code
Here is a simple environment which consists of a **5-by-5** grid. A treasure (T) is placed at the bottom right corner of the grid. The agent (O) starts at the top left corner of the grid.
    O....  
    .....  
    .....  
    .....  
    ....T
The agent needs to get to the treasure using the 4 available actions : **_left_** , **_right_** , **_up_** , **_down_**.
If the agent takes an action that leads him directly to T, he gets a reward of **1** , otherwise a reward of **0**.
The code is well commented and it is simply what we just discussed. Now the interesting part, the Q-Learning algorithm !
I almost commented every single line of this code, so hopefully, it will be easy to understand!
### Run the code
Put both of the above files in the same directory, and run :
    python3 medium_qlearning_rl.py
Around the epoch number** _40_** , the agent should have learned to get to the treasure using one of the shortest paths (8 steps).
## Conclusion
We have seen how to derive statistical formulas to find the Bellman equation and used it to teach an AI how to play a simple game. Notice that in this game, the number of possible states is **finite**(the number of different cells you might end up in), which is why building a Q-Table (a table of values that approaches the real value of the Q function for discrete values) is still manageable. What about a graphical game, such as Flappy Bird, Mario Bros, or Call Of Duty ? Every frame displayed by the game can be considered as a different state. In that case it’s impossible to build a Q-Table, and what we do instead is use a neural network who’s goal will be to learn the Q function. That neural network will typically take as input the current state of the game, and output the best possible action to take in that state. This is known as **Deep Q Learning** and is exactly how AIs such as Deep Blue or Alpha Go managed to beat world champions at Chess or Go.
## I hope you enjoyed this article! Stay around for more! 😎

---

## 📦 Code from Updated Version

**Source:** [https://omaraflak.com/articles/q-learning](https://omaraflak.com/articles/q-learning)

> The following code is from the updated version of the article.

### Code Block 1

```python
class Node:
    def __init__(self, value: int, children: list['Node']):
        self.value = value
        self.children = children


def max_sum(tree: Node) -> int:
    # TODO: find the highest sum for all branches
```

### Code Block 2

```python
def max_sum(tree: Node) -> int:
    return tree.value + max([max_sum(child) for child in tree.children], default=0)
```

### Code Block 3

```python
O.........
..........
..........
..........
.........T
```

### Code Block 4

```python
import abc


class Env(abc.ABC):
    @abc.abstractmethod
    def actions(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def states(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def step(self, action: int) -> tuple[int, int, bool]:
        raise NotImplementedError()

    @abc.abstractmethod
    def reset(self) -> tuple[int, int, bool]:
        raise NotImplementedError()

    @abc.abstractmethod
    def render(self):
        raise NotImplementedError()


class GridEnv(Env):
    def __init__(self, size: int):
        self.x = 0
        self.y = 0
        self.size = size
        self.end_x = size - 1
        self.end_y = size - 1
        self.done = False

    def actions(self) -> int:
        return 4

    def states(self) -> int:
        return self.size ** 2

    def step(self, action: int) -> tuple[int, int, bool]:
        if action == 0:  # left
            self.x = self.x - 1 if self.x > 0 else self.x
        if action == 1:  # right
            self.x = self.x + 1 if self.x < self.size - 1 else self.x
        if action == 2:  # up
            self.y = self.y - 1 if self.y > 0 else self.y
        if action == 3:  # down
            self.y = self.y + 1 if self.y < self.size - 1 else self.y

        done = self.x == self.end_x and self.y == self.end_y
        next_state = self.size * self.y + self.x
        reward = 1 if done else 0
        return next_state, reward, done

    def reset(self) -> tuple[int, int, bool]:
        self.x = 0
        self.y = 0
        self.done = False
        return 0, 0, False

    def render(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.y == i and self.x == j:
                    print("O", end='')
                elif self.end_y == i and self.end_x == j:
                    print("T", end='')
                else:
                    print(".", end='')
            print("")
```

### Code Block 5

```python
import os
import env
import time
import random


def train(e: env.Env) -> list[list[float]]:
    qtable = [
        [random.random() for _ in range(e.actions())]
        for _ in range(e.states())
    ]

    # hyperparameters
    epochs = 50
    gamma = 0.1
    epsilon = 0.08
    decay = 0.5

    # training loop
    for i in range(epochs):
        state, reward, done = e.reset()
        steps = 0

        while not done:
            os.system('clear')
            print("epoch #", i+1, "/", epochs)
            e.render()
            time.sleep(0.01)

            # count steps to finish game
            steps += 1

            if random.random() < epsilon:
                # act randomly to allow exploration
                action = random.choice(range(e.actions()))
            else:
                # act greedy and select action with max probability
                action = qtable[state].index(max(qtable[state]))

            # take action
            next_state, reward, done = e.step(action)

            # update qtable value with Bellman equation
            qtable[state][action] = reward + gamma * max(qtable[next_state])

            # update state
            state = next_state

        # The more we learn, the less we take random actions
        epsilon -= decay * epsilon

        print("\nDone in", steps, "steps".format(steps))
        time.sleep(0.8)

    return qtable


grid = env.GridEnv(10)
train(grid)
```

