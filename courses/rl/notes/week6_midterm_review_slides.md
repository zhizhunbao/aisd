# Week 6: 期中复习 (Midterm Review)

> Source: `CST8509_06_Midterm_Review.pptx`
> Total slides: 9
> Instructor: Todd Kelley | Winter 2026

---

## 1. 考试范围 (Midterm Scope)

![Page 1](week6_slides_pages/page_001.png)

- **Midterm Review** — 期中复习

![Page 2](week6_slides_pages/page_002.png)

- **Today's Agenda** — 今日议程
  - Review RL (CST8509_RL_Intro, CST8509_02_MDP, CST8509_03_Gymnasium) — 复习 RL（RL入门、MDP、Gymnasium）
  - Review Q-Learning (Lab2, Assignment1) — 复习 Q-Learning（实验2、作业1）
  - Sample Written Questions — 笔试样题

![Page 3](week6_slides_pages/page_003.png)

- **Midterm Scope** — 期中考试范围：
  - Reinforcement Learning Fundamentals — 强化学习基础
  - Basic Q-Learning with Basic "homemade" environment class — 基础 Q-Learning 配合自制环境类
  - Gymnasium custom environment, Pygame rendering — Gymnasium 自定义环境，Pygame 渲染
  - Q-learning with Gymnasium Cliffwalking — 用 Gymnasium Cliffwalking 做 Q-Learning
  - Q-learning deep dive — Q-Learning 深入剖析
  - Stable-baselines3 — Stable-baselines3 框架

> **📝 Notes — 考试范围 Checklist:**
>
> | 主题                                | 关键考点                                                                                                                        |
> | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
> | **RL Fundamentals**           | Agent/Environment/Reward 三要素、Markov Property、Policy$\pi$、Value Function、折扣回报 $G_t = \sum \gamma^k R_{t+k+1}$     |
> | **Q-Learning (homemade env)** | Q-table 更新公式、ε-greedy 探索、收敛条件                                                                                      |
> | **Gymnasium custom env**      | `reset()` / `step()` 返回值（obs, reward, terminated, truncated, info）、自定义 ObservationSpace / ActionSpace、Pygame 渲染 |
> | **Q-Learning + CliffWalking** | off-policy vs on-policy（Q-Learning vs SARSA）、最短路径 vs 安全路径                                                            |
> | **Q-Learning Deep Dive**      | Q-table 初始化对收敛的影响、终止状态 Q 值为 0 的重要性                                                                          |
> | **Stable-Baselines3**         | vectorized env、callbacks、`learn()` / `predict()` / `save()` / `load()`                                                |
>
> ⚠️ **重点提示**：笔试样题（§3）直接来自老师 slides，是最高优先级复习内容。

---

## 2. Q-Learning 深入剖析 (Q-Learning Deep Dive)

![Page 4](week6_slides_pages/page_004.png)

- **Question:** Why does our CliffWalking Example converge on the shortest path? — 问题：为什么我们的 CliffWalking 示例会收敛到最短路径？
- Q-Learning CliffWalking animation — Q-Learning CliffWalking 动画演示
- **Discussion** — 讨论：
  - Why does Sarsa converge on a different path? — 为什么 Sarsa 会收敛到不同路径？
  - How does the initialization of the qtable affect convergence? — Q表的初始化如何影响收敛？
    - Randomized? Initialize to zero? — 随机初始化？还是初始化为零？
  - How important is setting the action-values of the terminal state to zero? — 将终止状态的动作值设为零有多重要？

> **📝 Notes — Q-Learning Deep Dive 模型答案:**
>
> **Q1: 为什么 Q-Learning 收敛到最短路径（CliffWalking）？**
> Q-Learning 是 **off-policy** 算法：更新目标用 $\max_{a'} Q(s', a')$，不管当前策略实际执行什么动作，总是假设下一步会选最优动作。这意味着 Q-Learning 学习时"不怕"偶尔随机探索到悬崖边——更新目标与实际行为解耦。因此它能学到紧贴悬崖边的最短路径（理论最优路径）。
>
> **Q2: 为什么 SARSA 收敛到不同（更安全）的路径？**
> SARSA 是 **on-policy** 算法：更新目标用 $Q(s', a')$，其中 $a'$ 是策略（含 ε-greedy 随机性）**实际选择**的动作。在悬崖边探索时，随机动作有概率导致掉落悬崖（巨额负奖励）。SARSA 的更新会感知这种风险并惩罚靠近悬崖的状态，因此收敛到远离悬崖、稍长但更安全的路径。
> → **一句话对比**：Q-Learning 学"理论最优"，SARSA 学"实际执行时最优"（考虑了自身 ε-greedy 的不完美行为）。
>
> **Q3: Q-table 初始化如何影响收敛？**
>
> - **初始化为 0（保守）**：所有未访问状态价值相同，agent 缺乏探索动力，收敛可能较慢。
> - **初始化为乐观高值（Optimistic Init）**：任何被访问状态的实际奖励都低于初始值，令未访问状态"看起来更好"，主动驱动 agent 探索所有状态，通常收敛更快且更彻底。
> - **随机初始化**：初期行为随机，探索彻底但较不稳定。
>
> **Q4: 终止状态的动作值设为零有多重要？**
> **非常重要。** Q-Learning 更新公式为：
>
> $$
> Q(s,a) \leftarrow Q(s,a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s,a) \right]
> $$
>
> 若终止状态 $s'$ 的 Q 值非零，则 $\gamma \max Q(s', a')$ 会给更新目标添加"虚假的未来回报"——但终止状态之后不会再有任何交互。这会破坏 Bellman 方程的正确性，导致 Q 值无法收敛到真实值。**设为 0 确保更新目标仅反映当前步奖励 $r$，不含幻象未来回报。**

---

## 3. 笔试样题 (Sample Written Questions)

### 3.1 画图题：RL 框架图 (Draw RL Framework Diagram)

![Page 5](week6_slides_pages/page_005.png)

- Questions from "Time to check your learning" slides — 来自"检查学习成果"幻灯片的题目
- **Draw the diagram that represents the primary aspects of a Reinforcement Learning problem/solution with agent-environment interaction** — 画出代表强化学习问题/解决方案的主要方面的图，包含智能体-环境交互

### 3.2 写代码题：Q-Learning 更新公式 (Write Q-Learning Update Formula)

![Page 6](week6_slides_pages/page_006.png)

- **Write down the q-table update portion of the q-learning algorithm in python syntax. Give a list of each variable used and its meaning.** — 用 Python 语法写出 Q-Learning 算法中 Q 表更新部分，并列出每个变量的含义。

```python
qtable[state][action] = qtable[state][action] + alpha * (reward + gamma * max(qtable[next_state]) - qtable[state][action])
```

| Variable — 变量 | Meaning — 含义                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| `qtable`       | the table of action-values implementing the action-value function — 实现动作价值函数的动作值表 |
| `state`        | the current state — 当前状态                                                                   |
| `action`       | the current action — 当前动作                                                                  |
| `alpha`        | step size — 学习率（步长）                                                                     |
| `reward`       | reward received from taking action in state — 在该状态采取该动作后获得的奖励                   |
| `gamma`        | discount factor — 折扣因子                                                                     |
| `next_state`   | the state resulting from taking action in state — 在该状态采取该动作后达到的新状态             |

### 3.3 概念题：Gymnasium 是什么 (What is Gymnasium?)

![Page 7](week6_slides_pages/page_007.png)

- **What is Gymnasium?** — Gymnasium 是什么？

  > An API standard for reinforcement learning with a diverse collection of reference environments — 一个用于强化学习的 API 标准，包含多种参考环境
  >

  or / 或者

  > Gymnasium is a framework for creating Reinforcement Learning environments with a standard interface such that various RL algorithms/agents can be applied to the environment in a standard way — Gymnasium 是一个用于创建强化学习环境的框架，具有标准接口，使得各种 RL 算法/智能体可以用标准方式应用于环境
  >

### 3.4 概念题：Gymnasium Wrapper (What is a Gymnasium Wrapper?)

![Page 8](week6_slides_pages/page_008.png)

- **What is a Gymnasium Wrapper?** — Gymnasium Wrapper 是什么？

  > From the docs: Wrappers are a convenient way to modify an existing environment without having to alter the underlying code directly. — 来自文档：Wrapper 是一种便捷方式，可以在不直接修改底层代码的情况下修改现有环境。
  >

  > In order to wrap an environment, you must first initialize a base environment. Then you can pass this environment along with (possibly optional) parameters to the wrapper's constructor. — 要包装一个环境，必须先初始化一个基础环境。然后将该环境连同（可能是可选的）参数传递给 wrapper 的构造函数。
  >

### 3.5 概念题：Stable-Baselines3 是什么 (What is Stable-Baselines3?)

![Page 9](week6_slides_pages/page_009.png)

- **What is Stable-Baselines3?** — Stable-Baselines3 是什么？

  > Stable-baselines3 is a set of reliable Reinforcement Learning algorithm implementations that includes features such as: — Stable-baselines3 是一套可靠的强化学习算法实现，包含以下特性：
  >

  - **Vectorized environments** (running the algorithm on several copies of the environment at the same time) — 矢量化环境（同时在多个环境副本上运行算法）
  - **Callbacks** (giving the programmer mechanisms to run custom code to do monitoring, auto saving, model manipulation, progress bars, etc) — 回调函数（为程序员提供机制运行自定义代码来实现监控、自动保存、模型操作、进度条等）

> **📝 Notes — 笔试样题模型答案（直接背这里）:**
>
> ---
>
> **题1：画 RL 框架图**
>
> ![1773181524682](image/week6_midterm_review_slides/1773181524682.png)
>
> ```
>                    ┌─────────────────────┐
>          ┌────────►│        Agent        │────────┐
>          │         └─────────────────────┘        │
>          │                                        │ action
>  state S_t                                        │  A_t
>  reward R_t                                       │
>          │         ┌─────────────────────┐        │
>          └─────────│     Environment     │◄───────┘
>   R_{t+1}, S_{t+1} └─────────────────────┘
> ```
> 核心三要素：**Agent**（观察 $S_t$，选择动作 $A_t$）、**Environment**（接受 $A_t$，返回 $R_{t+1}$, $S_{t+1}$）、**Reward**（标量奖励信号）
>
> ---
>
> **题2：Q-table 更新公式（Python）**
>
> ```python
> qtable[state][action] = qtable[state][action] + alpha * (reward + gamma * max(qtable[next_state]) - qtable[state][action])
> ```
> | 变量           | 含义                                         |
> | -------------- | -------------------------------------------- |
> | `qtable`     | 动作价值表，实现动作价值函数$Q(s,a)$       |
> | `state`      | 当前状态$s$                                |
> | `action`     | 当前动作$a$                                |
> | `alpha`      | 学习率（步长）$\alpha$，控制每次更新的幅度 |
> | `reward`     | 执行动作后获得的即时奖励$r$                |
> | `gamma`      | 折扣因子$\gamma$，平衡即时与未来奖励       |
> | `next_state` | 执行动作后到达的新状态$s'$                 |
>
> ---
>
> **题3：What is Gymnasium?**
> Gymnasium is an **API standard** for reinforcement learning with a diverse collection of reference environments. It provides a standard interface (`reset()`, `step()`, `render()`) so that various RL algorithms can be applied to any environment in a consistent way.
>
> ---
>
> **题4：What is a Gymnasium Wrapper?**
> A Gymnasium Wrapper is a **convenient way to modify an existing environment without altering the underlying code directly**. You initialize a base environment first, then pass it to the wrapper's constructor (along with optional parameters).
>
> ```python
> env = gym.make("CartPole-v1")
> env = TimeLimit(env, max_episode_steps=200)  # wrapper 示例
> ```
> ---
>
> **题5：What is Stable-Baselines3?**
> Stable-Baselines3 is a set of **reliable, well-tested RL algorithm implementations** (DQN, PPO, SAC, etc.) that includes:
>
> - **Vectorized environments** — run multiple environment copies in parallel to collect experience faster
> - **Callbacks** — hooks for custom code during training (monitoring, auto-saving, progress bars, early stopping)
>
> Key API: `model.learn()` / `model.predict()` / `model.save()` / `Model.load()`
