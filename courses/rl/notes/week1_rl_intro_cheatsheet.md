# Week 1: RL 入门 — 概念速查

> **See also:** [_math.md](week1_rl_intro_math.md) | [_code.md](week1_rl_intro_code.md)
> **Source:** Slides CST8509_01 + Quiz 1 + Lab 1

---

## Reinforcement Learning

### Definition

- **RL (Reinforcement Learning, 强化学习):** A third type of machine learning where an agent learns to maximize cumulative reward through trial-and-error interaction with an environment
- **Agent (智能体):** The learner/decision-maker that interacts with the environment
- **Environment (环境):** Everything outside the agent that it interacts with
- **Reward (奖励):** A scalar feedback signal $R_t$ indicating how well the agent is doing at step $t$
- **Reward Hypothesis (奖励假说):** All goals can be described by the maximization of expected cumulative reward
- **MDP (Markov Decision Process, 马尔可夫决策过程):** An extension of the Markov chain with actions and rewards; the mathematical framework for RL problems

### Key Points

- RL is the **third** ML paradigm (alongside supervised and unsupervised)
- RL has NO "correct answer" labels — only reward signals
- Two core features: **trial-and-error search** + **delayed reward**
- Agent may need to accept negative short-term rewards to maximize total reward
- Reward can come along the way OR all at the end
- Negative per-step reward favors shorter episodes

### Traps

- MDP transitions are **stochastic** — same action in same state can lead to different next states (Quiz 1 Q3: FALSE that action always leads to same result)
- Sum of all subsequent rewards might be **infinite** — this is why we need discount factor $\gamma$ (Quiz 1 Q4)
- Don't confuse RL with unsupervised learning — RL maximizes reward, UL finds hidden structure

### Compare

| Feature | Supervised Learning | Unsupervised Learning | Reinforcement Learning |
|---------|--------------------|-----------------------|----------------------|
| Feedback | Labeled examples | None | Reward signal |
| Goal | Learn mapping | Find structure | Maximize reward |
| Data | (input, label) pairs | Unlabeled data | State-action-reward sequences |
| Exploration needed? | No | No | Yes |

---

## History, State, Markov Property

### Definition

- **History (历史):** $H_t = R_1, O_1, A_1, ..., R_t, O_t, A_t$ — the complete sequence of observations, actions, and rewards
- **State (状态):** A summary of history used to determine what happens next: $S_t = f(H_t)$
- **Environment State (环境状态, $S_t^e$):** Internal state of the environment; usually NOT directly accessible to the agent
- **Agent State (智能体状态, $S_t^a$):** Information the agent maintains; used to select actions: $S_t^a = f(H_t)$
- **Markov Property (马尔可夫性质):** $P(S_t, R_t)$ depends only on $S_{t-1}$ and $A_{t-1}$ — "the future is independent of the past given the present"
- **Markov Chain (马尔可夫链):** A mathematical model that experiences transition of states with probabilistic rules (Quiz 1 Q1)

### Key Points

- State = compressed version of history — processing full history is impractical
- The programmer chooses function $f$ for agent state — this choice critically affects learning
- Environment state is always Markov
- Full history $H_t$ is always Markov (trivially)
- We want Markov states that are efficient and low-redundancy

### Traps

- Position alone is NOT Markov for moving objects — need position + velocity (Quiz 1 Q3 concept)
- Rat example: different $f(H_t)$ choices → completely different predictions (shock vs cheese vs unknown)

---

## Policy

### Definition

- **Policy (策略, $\pi$):** A function that maps states to actions — tells the agent what to do
- **Deterministic Policy (确定性策略):** $a = \pi(s)$ — one state → one action
- **Stochastic Policy (随机性策略):** $\pi(a|s) = P[A=a|S=s]$ — one state → probability distribution over actions
- **Greedy Policy (贪婪策略):** Always takes the action with highest estimated value: $a = \arg\max_{a'} Q(s, a')$ (Quiz 1 Q8)

### Key Points

- Policy is the CORE of an RL agent — it alone determines behavior
- Goal: learn $\pi$ from experience to maximize reward
- Policy can be a simple lookup table or complex computation

### Traps

- Greedy policy = always pick highest **immediate** reward action (Quiz 1 Q8: answer D)
- Policy $\pi(a|s)$ is a probability distribution — sum over all actions = 1

---

## Value Function

### Definition

- **State Value Function (状态价值函数, $V(s)$):** Expected total reward starting from state $s$ — takes a STATE, gives expected return (Quiz 1 Q6)
- **Action Value Function (动作价值函数, $Q(s,a)$):** Expected total reward starting from state $s$ and taking action $a$ — takes STATE + ACTION, gives expected return (Quiz 1 Q7)

### Key Points

- Value function looks at **future** rewards only — does NOT include past rewards
- In Atari: value oscillates — rises before good events, drops after
- We make decisions based on **value** (long-term), not reward (immediate)
- Values must be estimated and re-estimated from experience; rewards are given directly

### Traps

- $V(s)$ takes only STATE → return. $Q(s,a)$ takes STATE + ACTION → return. Don't confuse them (Quiz 1 Q6 vs Q7)
- Value function does NOT include rewards already received — only future

### Compare

| | $V(s)$ | $Q(s,a)$ |
|---|---|---|
| Input | State only | State + Action |
| Output | Expected return from $s$ | Expected return from $s$ taking $a$ |
| Used by | Evaluate states | Choose actions directly |

---

## Model

### Definition

- **Model (模型):** Agent's internal representation of the environment — predicts next state and reward
- **Transition Model (转移模型):** Predicts next state given current state and action
- **Reward Model (奖励模型):** Predicts next reward given current state and action
- **Planning (规划):** Deciding on actions by considering possible future situations before experiencing them

### Key Points

- Not all RL methods use a model — model is optional
- Model enables planning: "think ahead" without actually acting
- Model-free methods learn purely from experience (trial-and-error)

---

## RL Agent Taxonomy

### Definition

- **Value Based (基于价值):** Agent has value function, no explicit policy — chooses actions via value function
- **Policy Based (基于策略):** Agent has policy, no value function
- **Actor Critic (演员-评论家):** Agent has both policy (actor) and value function (critic)
- **Model Free (无模型):** No model of environment — learns from direct experience
- **Model Based (基于模型):** Has model of environment — can plan ahead

### Compare

| Type | Policy | Value Function | Model |
|------|--------|---------------|-------|
| Value Based | ❌ (implicit) | ✅ | Optional |
| Policy Based | ✅ | ❌ | Optional |
| Actor Critic | ✅ (actor) | ✅ (critic) | Optional |

---

## Key Subproblems

### Definition

- **Exploitation (利用):** Using the best known action to get reward
- **Exploration (探索):** Trying new actions to discover potentially better options
- **Prediction (预测):** Evaluating future reward under current policy
- **Control (控制):** Finding the optimal policy

### Key Points

- Exploration-exploitation tradeoff is **unique to RL** — does not exist in supervised/unsupervised learning
- Neither pure exploration nor pure exploitation works alone — must balance

### Compare

| Subproblem | Question | Example |
|-----------|----------|---------|
| Learning vs Planning | Real experience vs simulated | Actually eating at restaurant vs reading reviews |
| Exploit vs Explore | Known best vs try new | Go to favorite restaurant vs try new one |
| Prediction vs Control | How good is current policy? vs What's the best policy? | "How many points will I get?" vs "How to get max points?" |
