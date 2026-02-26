# Week 2: MDP — 概念速查

> **See also:** [_math.md](week2_mdp_math.md) | [_code.md](week2_mdp_code.md)
> **Source:** Slides CST8509_02 + Quiz 2 + Lab 2

---

## Q-Learning Deep Dive

### Definition

- **Q-Learning Convergence (Q-Learning 收敛):** In grid worlds with negative per-step reward and large cliff penalty, Q-Learning converges to the shortest safe path because fewer steps = less total negative reward
- **Q-table Initialization (Q 表初始化):** Random initialization encourages early exploration; zero initialization is more conservative; optimistic initialization (high values) promotes maximum exploration
- **Terminal State Q-value (终止状态 Q 值):** Must be set to zero — no future exists after termination

### Key Points

- Negative per-step reward → agent learns shortest path (fewer penalties)
- Zero per-step reward → agent has no incentive to hurry (may wander)
- Positive per-step reward → agent avoids termination (wants to keep collecting rewards forever)
- Q-table structure mirrors grid world structure in grid-based environments

### Traps

- Positive per-step reward creates an agent that **never wants to stop** — it will avoid the goal
- Q-table must have Q(terminal, ·) = 0, otherwise Bellman update references nonexistent future rewards

---

## SARSA vs Q-Learning

### Definition

- **SARSA (State-Action-Reward-State-Action):** On-policy TD control; updates Q using the **actual next action** $A'$ chosen by the current policy
- **Q-Learning:** Off-policy TD control; updates Q using the **best possible next action** $\max_{a'} Q(S', a')$ regardless of what action was actually taken
- **On-policy (同策略):** The policy used to generate behavior is the **same** policy being improved
- **Off-policy (异策略):** The policy being improved is **different** from the policy used to generate behavior

### Key Points

- Both use ε-greedy as the **behavior policy** (for exploration)
- Q-Learning's **target policy** is greedy (always picks max), making it off-policy
- SARSA's **target policy** is the same ε-greedy, making it on-policy
- Difference is magnified when ε is large (more random exploration)

### Traps

- SARSA learns a **safer, more conservative** path in CliffWalking (accounts for exploration risk near cliffs)
- Q-Learning learns the **optimal but risky** path (assumes final policy will be greedy, ignoring exploration mishaps during training)
- The name "SARSA" comes from the tuple $(S, A, R, S', A')$ used in updates

### Compare

| Feature | Q-Learning | SARSA |
|---------|-----------|-------|
| Update target | $\max_{a'} Q(S', a')$ | $Q(S', A')$ |
| Policy type | Off-policy | On-policy |
| Behavior policy | ε-greedy | ε-greedy |
| Learning policy | Greedy (max) | Same ε-greedy |
| CliffWalking path | Optimal (near cliff) | Safe (far from cliff) |
| Risk awareness | Ignores exploration risk | Accounts for exploration risk |

---

## RL Programmer's Methodology

### Definition

- **Problem Identification (问题识别):** Select which aspects of a domain to model as the RL problem — not everything needs to be part of the problem
- **Agent-Environment Boundary (智能体-环境边界):** Anything the agent cannot arbitrarily change is part of the environment (Sutton p.50-51)

### Key Points

- Boundary ≠ physical boundary (robot's motors can be "environment")
- The boundary is a **design choice** — same problem can have different boundaries
- Any goal-directed learning problem reduces to 3 signals: actions, states, rewards
- Representational choices are "more art than science" (Sutton)

### Traps

- Do NOT encode "how to achieve" in rewards — only encode "what to achieve"
- Do NOT design rewards around subgoals (chess: reward winning, not capturing pieces)
- Do NOT base rewards on previous actions (unless action sequence IS the goal)

---

## Returns and Episodes

### Definition

- **Episode (回合):** A single run from start state to terminal/truncated state (Quiz 2 Q6: answer B)
- **Episodic Task (回合制任务):** Task with terminal state; T is finite random variable (games, mazes)
- **Continuing Task (持续任务):** Task that never ends; T = ∞ (power plant control, thermostat)
- **Return (回报, $G_t$):** Cumulative (possibly discounted) reward from time step $t$ onward
- **Absorbing State (吸收状态):** Special state that always transitions to itself with reward 0; used to unify episodic and continuing formulations
- **Epoch (纪元):** A single pass through a dataset — RL has no dataset, so this term doesn't truly apply to RL (though sometimes used loosely)

### Key Points

- Undiscounted return may be infinite for continuing tasks → need discount factor $\gamma$
- Recursive form: $G_t = R_{t+1} + \gamma G_{t+1}$ — this recursion is the foundation of Bellman equations
- Higher $\gamma$ → more farsighted agent; lower $\gamma$ → more myopic agent

### Traps

- An episode is NOT a single step (Quiz 2 Q6: A is wrong — that's a time step, not an episode)
- $\gamma = 1$ may cause return to diverge in continuing tasks (Quiz 2 Q7)
- Episode vs Epoch: Episode = one complete RL run; Epoch = one pass through dataset (DL/ML term, not RL)

---

## Policies and Value Functions

### Definition

- **Policy (策略, $\pi$):** A function that determines the probability of taking an action: $\pi(a|s) = P[A_t = a | S_t = s]$ (Quiz 2 Q8: answer D)
- **State-value Function (状态价值函数, $v_\pi(s)$):** Expected return starting from state $s$ under policy $\pi$
- **Action-value Function (动作价值函数, $q_\pi(s,a)$):** Expected return starting from state $s$, taking action $a$, then following $\pi$
- **Value Function (价值函数):** Gives expected total reward given a state or state-action pair (Quiz 2 Q9: answer B)

### Key Points

- Policy determines agent's behavior completely
- Policy is about **action probabilities**, NOT about assigning values (Quiz 2 Q8: B/C are wrong — those describe value functions)
- Value function and policy are implemented in the **Agent**, not Environment (Quiz 2 Q15: answer A)

### Traps

- Policy ≠ value function: policy maps states → action probabilities; value function maps states → expected return (Quiz 2 Q8 vs Q9)
- $V(s)$ takes only state; $Q(s,a)$ takes state + action (Quiz 2 Q10: answer E)
- Value function gives expected total reward, not "total number of steps" (Quiz 2 Q9: D is wrong)

### Compare

| | $v_\pi(s)$ | $q_\pi(s,a)$ |
|---|---|---|
| Input | State only | State + Action |
| Output | Expected return from $s$ | Expected return from $s$ taking $a$ |
| Used for | Evaluate states | Choose actions directly |

---

## Bellman Equation

### Definition

- **Bellman Equation (贝尔曼方程):** Expresses the value of a state as immediate reward + discounted value of successor state
- **Temporal Difference (TD, 时序差分):** Learning method that updates estimates based on differences between successive time-step predictions (Quiz 2 Q14: correct term is "Difference" not "Distance")

### Key Points

- Bellman equation is recursive: value = reward + γ × next value
- It breaks value computation into smaller subproblems (dynamic programming)
- It forms the mathematical basis for Q-Learning (Quiz 2 Q11: all of B/D/E are correct → answer C)
- Q-Learning is a form of TD learning (model-free, step-by-step updates)

### Traps

- ⚠️ **Terminology trap** (Quiz 2 Q14): "Temporal **Distance**" is WRONG — correct term is "Temporal **Difference**"
- All options in Q14 use wrong term → answer is E (None)
- Greedy ≠ optimal: greedy picks immediate best estimate, which may not be globally optimal (Quiz 2 Q12: answer D)

---

## Q-Learning Prerequisites

### Definition

- **Tabular Q-Learning Prerequisites (表格 Q-Learning 前提条件):** Both the complete state set $S$ and action set $A$ must be known (Quiz 2 Q13: answer D)

### Key Points

- Q-table dimensions = $|S| \times |A|$ — if either is unknown, can't build the table
- Only knowing states (B) or only knowing actions (C) is insufficient
- The optimal value function does NOT need to be known — that's what we're learning (E is wrong)

### Compare

| Condition | Q-Learning works? |
|-----------|-------------------|
| States AND actions known | ✅ Yes |
| Only states known | ❌ No (can't define action columns) |
| Only actions known | ❌ No (can't define state rows) |
| Optimal V/Q already known | No need for Q-Learning at all |
