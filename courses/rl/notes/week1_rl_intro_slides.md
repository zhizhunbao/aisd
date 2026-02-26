# Week 1: 强化学习入门 (Introduction to Reinforcement Learning)

> Source: `CST8509_01_RL_Intro.pdf`
> Total slides: 37
> Instructor: Todd Kelley (Lectures) / Ali Mohamed Ali (Labs) | Winter 2026

---

## 1. 课程介绍 (Course Introduction)

![Page 1](week1_rl_intro_slides_pages/page_001.png)

- Introduction to Reinforcement Learning

![Page 2](week1_rl_intro_slides_pages/page_002.png)

- CST8509: Reinforcement Learning
- Meet your Professors
  - Lectures: Todd Kelley, Office: T315, Phone: 613-727-4723 x7474, Email: kelleyt@algonquincollege.com
  - Labs: Ali Mohamed Ali <mohamea2@algonquincollege.com>
- Contact your Professor
  - email me with enquiries (can expect reply same or next day)
  - email me to arrange office-hour style meetings

![Page 3](week1_rl_intro_slides_pages/page_003.png)

- Weekly schedule
  - Lecture Mondays 1:00-3:00pm in C346
  - Lab Section 101 Wednesdays 5:00 to 7:00pm in B320
  - Lab Section 102 Wednesdays 7:00 to 9:00pm in B119
  - One hour (average) of asynchronous (Hybrid) activity
- Late lab/assignment submissions are subject to a penalty:
  - 10% < 1 week
  - 100% > 1 week

> **📝 Notes:**
>
> _(To be added)_

---

## 2. 学术诚信与成功建议 (Academic Integrity & Tips for Success)

### 2.1 作业期望 (Expectations for Assignments)

![Page 4](week1_rl_intro_slides_pages/page_004.png)

- Unless an Assignment or Lab explicitly states that it is a group activity, ALL practical and theory work in this course is individual work:
  - You must complete solutions by yourself
  - You are allowed to participate in study groups and use ChatGPT or similar facilities
  - You are allowed to help each other understand the concepts of the course
  - You are not allowed to copy or use for any purpose any portion of a solution from another student, from ChatGPT, or from any other source
  - You are not allowed to provide any portion of your solution to anyone else

### 2.2 成功建议 (Tips for Success)

![Page 5](week1_rl_intro_slides_pages/page_005.png)

- Assignments are large bodies of work that cannot reasonably be completed in one or two sessions, even long sessions
- Get started early
- Get clarification and help early
- Make good use of Lab Periods

![Page 6](week1_rl_intro_slides_pages/page_006.png)

- **Rule One: 15 minute rule** — if you are frustrated and not making progress for 15 minutes, you need to:
  - take a break, move on to another part of the assignment, switch to other course work, come back to it later
  - sleep on it
  - seek help from a peer
  - seek help from the instructor

![Page 7](week1_rl_intro_slides_pages/page_007.png)

- **Rule Two: Don't leave it to the last few days before the due date**
  - Rule One is not feasible without Rule Two
  - Get started early, read through and understand the focus of the assignment and the tasks, as soon as you can
  - Keep up with the course pace (every week, you're expected to put in about 5 hours of time in addition to 5 hours of Hybrid Activities, Lectures, and Labs)

### 2.3 过度帮助与抄袭 (Excessive Help & Plagiarism)

![Page 8](week1_rl_intro_slides_pages/page_008.png)

- Beware of receiving excessive help
- Do it yourself (you need to learn how to):
  - read EVERY word of the Lab and Assignment Documents
  - consult course materials and resources
  - apply what you read and what you see in videos
  - solve apparent inconsistencies/problems

![Page 9](week1_rl_intro_slides_pages/page_009.png)

- Like excessive help, shortcuts are bad
- If you cannot explain your own work in a demonstration, you risk getting a zero on the lab or assignment

![Page 10](week1_rl_intro_slides_pages/page_010.png)

- Cheating is unacceptable. You may not copy or provide code or text: don't plagiarize
- The person you copy from is in just as much trouble as you

> **📝 Notes:**
>
> _(To be added)_

---

## 3. 课程概览与学习目标 (Course Overview & Learning Outcomes)

![Page 11](week1_rl_intro_slides_pages/page_011.png)

- **Introduction to RL**
- **Foundational Principles of RL**
  - Mathematical definitions
  - RL Algorithms
- **Solving RL problems**
  - Game-based, maze based, etc
  - Robotics
  - Create
  - OpenAI Gymnasium/Gym, Gazebo

![Page 12](week1_rl_intro_slides_pages/page_012.png)

**Week 1 Outcomes:**
1. Agent
2. Environment
3. Reward
4. Policy
5. Value Function
6. Model

> **📝 Notes:**
>
> _(To be added)_

---

## 4. 什么是强化学习 (What is Reinforcement Learning)

### 4.1 RL 在机器学习中的位置 (RL in Machine Learning)

![Page 13](week1_rl_intro_slides_pages/page_013.png)

- Reinforcement Learning is a **third type of Machine Learning**
- Based on **Markov Decision Processes**
- Used for **agent-based systems**
  - Agent uses a **policy** for choosing an action in each time step
  - Each action taken results in a **reward**
  - The goal is for the agent to learn a policy that **maximizes the reward**

### 4.2 RL 领域名人 (Who's Who of Reinforcement Learning)

![Page 14](week1_rl_intro_slides_pages/page_014.png)

- **Andrew Barto**, University of Massachusetts Amherst
- **Richard Sutton**, University of Alberta (Co-founder of Edmonton office of DeepMind) — textbook
- **David Silver**, University of Alberta PhD graduate, now at DeepMind and University College London
  - David Silver's RL course on Youtube: https://www.youtube.com/playlist?list=PLzuuYNsE1EZAXYR4FJ75jcJseBmo4KQ9-

### 4.3 RL 的广泛应用 (How Broad and Applicable is RL)

![Page 15](week1_rl_intro_slides_pages/page_015.png)

- David Silver lecture 1 (youtube), 6:29
- (venn diagrams showing RL is at the intersection of many different fields of human endeavor)

![Page 16](week1_rl_intro_slides_pages/page_016.png)

- How does reinforcement learning compare to other machine learning (supervised, and unsupervised)?
- David Silver lecture 1 - 9:35

### 4.4 RL 应用实例 (RL Examples)

![Page 17](week1_rl_intro_slides_pages/page_017.png)

- David Silver Lecture 1: 12:45 - examples of RL, starting with stunt manoeuvers model helicopter (training is done offline with a model of a helicopter world)
- David Silver Lecture 1: after helicopter - video games (many Atari games better than humans) decisions at 15HZ (3 or 4 days of training per game)
- Tetris: https://www.cbc.ca/player/play/2296942659841
- our coffee robot?
- monkey and banana?

![Page 18](week1_rl_intro_slides_pages/page_018.png)

- **AlphaGo movie** — Go board game
  - begins with Demis Hassabis (co-founder of DeepMind)
  - After Fan Hui, we see David Silver
  - At 30:00 the start of the first match

> **📝 Notes:**
>
> _(To be added)_

---

## 5. 奖励 (Reward)

![Page 19](week1_rl_intro_slides_pages/page_019.png)

- Reward is a **scalar feedback signal** $R_t$
- $R_t$ represents how well the agent is doing at Step $t$
- reinforcement learning problems are set up such that goal is to **maximize cumulative reward**
- **Reward Hypothesis:** All goals can be described by the maximization of expected cumulative reward

![Page 20](week1_rl_intro_slides_pages/page_020.png)

- reward can be received along the way, or it might come all at the end
- if shorter time is better, then reward per step can be negative, which favors shorter episodes
- to maximize reward overall, agent may need to accept small or negative rewards short-term to maximize the total reward

> **📝 Notes:**
>
> _(To be added)_

---

## 6. Agent-Environment 交互 (Anatomy of an RL Problem)

### 6.1 Agent 与 Environment 的关系 (Agent-Environment Interaction)

![Page 21](week1_rl_intro_slides_pages/page_021.png)

- agent and environment diagram
- our algorithm operates in the agent

![Page 22](week1_rl_intro_slides_pages/page_022.png)

- each time step, the agent receives **Reward**, **Observation**, and performs **Action**
- the time series of Reward, Observation, and Actions is the data for Reinforcement learning
- the history at time step $t$ is $H_t = R_1, O_1, A_1, ..., R_t, O_t, A_t$

### 6.2 历史与状态 (History and State)

![Page 23](week1_rl_intro_slides_pages/page_023.png)

- the agent picks the next action at time $t$ based on the information/data contained in $H_t$
- the environment determines Observations and Rewards
- processing the whole history is cumbersome after many steps
- **State** is a summary of the information that is used to determine what happens next ($t+1$)

![Page 24](week1_rl_intro_slides_pages/page_024.png)

- $S_t = f(H_t)$
- **environment state** ($S_t^e$) is not usually directly accessible by the agent; whatever information is used to pick the next observation and reward
- **agent state** ($S_t^a$) is directly accessible to the agent, the agent keeps track of this, and it's used (somehow) to select the next action
- The programmer is responsible for the (somehow). The programmer decides what the function is:
  - $S_t^a = f(H_t)$ for some function $f$ of the programmer's choosing

> **📝 Notes:**
>
> _(To be added)_

---

## 7. 马尔可夫状态 (Markov State)

![Page 25](week1_rl_intro_slides_pages/page_025.png)

- Important question in RL is whether the state satisfies the **Markov Property**, in other words, is it a **Markov State**
- **Definition of a Markov State:** The probability of each possible value for $S_t$ and $R_t$ depends only on the immediately preceding state and action, $S_{t-1}$ and $A_{t-1}$
- **Intuition:** "The future is independent of the past given the present"
- Examples:
  - linear motion of a particle in classical mechanics
  - does the position constitute a Markov state?
  - does the position and velocity constitute a Markov state?

![Page 26](week1_rl_intro_slides_pages/page_026.png)

- helicopter example (position, velocity, angular velocity, angular position, wind velocity)
- $S_t^e$ environment state is Markov
- $H_t$ is Markov, $S_t = f(H_t) = H_t$
- It's always possible to come up with a Markov state, but we want to identify the Markov states that are more useful for us, efficient, less redundancy, etc.

![Page 27](week1_rl_intro_slides_pages/page_027.png)

- **Rat Example** — David Silver Lecture 1, 47:54
- depending on what function is chosen for $f(H_t)$, the question mark can be electric shock, cheese, or unknown

> **📝 Notes:**
>
> _(To be added)_

---

## 8. RL Agent 的组成 (Components of RL Agents)

### 8.1 概述 (Overview)

![Page 28](week1_rl_intro_slides_pages/page_028.png)

- RL Agents may include one or more of the following:
  - **Policy:** function that maps state to action
  - **Value Function:** represents the value (how good is it?) of each state or action
  - **Model:** agent's internal representation of the environment, as opposed to the environment itself

### 8.2 策略 (Policy)

![Page 29](week1_rl_intro_slides_pages/page_029.png)

- **Function:** map from state to action
- **Deterministic policy:** one where there is only one choice, one action
  - $a = \pi(S)$
- our goal will be to learn a function $\pi$, from experience, such that we maximize reward
- **Stochastic policy:**
  - $\pi(a|s) = P[A=a|S=s]$
  - This function gives the probability of one or more actions, given State $s$ (non-deterministic)
  - Example: in certain state, $a_1$ chosen 20% of the time, $a_2$ chosen 80% of the time

### 8.3 价值函数 (Value Function)

![Page 30](week1_rl_intro_slides_pages/page_030.png)

- the value function indicates how good it is to be in a particular state with respect to **expected future reward**
- used to pick actions, interacts with policy
- the value function for a policy is the **sum of the expected reward for all future states**

![Page 31](week1_rl_intro_slides_pages/page_031.png)

- in the case of Atari games, as states are visited, value goes up and down, because if something good is about to happen, value function is elevated
  - after something good happens, that reward is behind you, and not included in the future reward
  - in other words the value function does not include the sum of rewards received so far, just future reward, which oscillates
  - David Silver Lecture 1: 1:02:15

### 8.4 模型 (Model)

![Page 32](week1_rl_intro_slides_pages/page_032.png)

- allows inferences about how the environment will behave
- model indicates or implies the next state and next reward
- From Sutton, page 7: "Models are used for **planning**, by which we mean any way of deciding on a course of action by considering possible future situations before they are actually experienced."
- David Silver Lecture 1: **Transition model** (predicts states) **Reward Model** (predicts rewards)
- not all Reinforcement Learning Problems/Solutions include a model

### 8.5 迷宫示例 (Maze Example)

![Page 33](week1_rl_intro_slides_pages/page_033.png)

- David Silver, Lecture 1: 1:08:00

> **📝 Notes:**
>
> _(To be added)_

---

## 9. RL Agent 分类 (Taxonomy of RL Agents)

![Page 34](week1_rl_intro_slides_pages/page_034.png)

- **Value Based**
  - no policy (choose actions based on Value function)
  - value function
- **Policy Based**
  - Policy
  - no value function

![Page 35](week1_rl_intro_slides_pages/page_035.png)

- **Actor Critic**
  - Policy (actor)
  - Value Function (critic)
- **Model Free**
  - Policy and/or Value Function
  - no Model
- **Model Based**
  - Policy and/or Value Function
  - Model

> **📝 Notes:**
>
> _(To be added)_

---

## 10. 关键子问题 (Key Subproblems)

![Page 36](week1_rl_intro_slides_pages/page_036.png)

- **Learning vs Planning** — David Silver Lecture 1: 1:16:10
  - reinforcement learning
  - planning
- **Exploitation vs Exploration**
  - Example: Always go to a good restaurant (exploit the good restaurant) vs Randomly choose a new restaurant (exploration, might be better, might be worse. This is our chance to find better, but it's a risk)
- **Prediction vs Control**
  - prediction (evaluate future reward) vs control (optimize policy)

> **📝 Notes:**
>
> _(To be added)_

---

## 11. 学习检查 (Check Your Learning)

![Page 37](week1_rl_intro_slides_pages/page_037.png)

- What is the Markov Property?
- What are the possible components in an RL agent?
- What is a policy in the context of RL?
- What is a value function in the context of RL?
- What is a model in the context of RL?

> **📝 Notes:**
>
> _(To be added)_
