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

> **📝 Notes:**
>
> _(To be added)_

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

> **📝 Notes:**
>
> _(To be added)_

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

> **📝 Notes:**
>
> _(To be added)_
