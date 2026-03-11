# Week 6: 期中复习 — 操作教程 (Midterm Review Tutorial)

> See also: [幻灯片笔记](week6_midterm_review_slides.md) | [数学公式](week6_midterm_review_math.md) | [Quiz](week6_midterm_review_quiz.md)

---

## §0 考试范围总览 (Midterm Scope)

期中考试涵盖 **Week 1–5 + SB3**，分为以下主题：

| 主题 | 关键概念 | 核心来源 |
|------|---------|---------|
| RL 基础 | Agent/Env/Reward 三要素、Markov Property、Policy、Value Function、$G_t$ | Week 1 |
| 基础 Q-Learning | Q-table 更新公式、ε-greedy | Week 2 |
| Gymnasium 自定义环境 | `reset()`/`step()` 返回值、ObsSpace/ActionSpace、Pygame | Week 3 |
| Q-Learning + CliffWalking | Off-policy vs On-policy（Q-Learning vs SARSA） | Week 2 + Lab 1 |
| Q-Learning Deep Dive | Q-table 初始化、终止状态 Q=0 的重要性 | Week 5 |
| Stable-Baselines3 | Vectorized env、callbacks、`learn()`/`predict()` | Week 4 |

> ⚠️ **优先级：** §3 笔试样题直接来自老师 slides，是最高优先级复习内容。

---

## §1 RL 基础快速复习 (RL Fundamentals)

### 1.1 三要素

```
           ┌─────────────────────┐
 ┌────────► │        Agent        │────────┐
 │          └─────────────────────┘        │ action A_t
 │                                         │
 state S_t                                 │
 reward R_t   ┌─────────────────────┐      │
 └────────────│     Environment     │◄─────┘
  R_{t+1},    └─────────────────────┘
  S_{t+1}
```

- **Agent**：感知状态 $S_t$，输出动作 $A_t$
- **Environment**：接收 $A_t$，返回 $R_{t+1}$ 和 $S_{t+1}$
- **Reward**：标量信号，Agent 的唯一优化目标

### 1.2 Markov Property

$$P(S_{t+1}, R_{t+1} \mid S_t, A_t) = P(S_{t+1}, R_{t+1} \mid S_1, A_1, \ldots, S_t, A_t)$$

**一句话：** 未来只依赖当前状态，与历史无关。

> ⚠️ **实践意义：** 这是简化问题的关键假设。如果状态设计不好（遗漏关键信息），Markov Property 就不成立，算法性能会下降。

### 1.3 策略与价值函数

| 概念 | 公式 | 含义 |
|------|------|------|
| 确定性策略 | $a = \pi(s)$ | 每个状态对应唯一动作 |
| 随机性策略 | $\pi(a\|s) = P[A=a\|S=s]$ | 每个状态对应动作概率分布 |
| 状态价值 | $V_\pi(s) = \mathbb{E}\_\pi[G_t \mid S_t=s]$ | 从状态 $s$ 开始的期望回报 |
| 动作价值 | $Q_\pi(s,a) = \mathbb{E}\_\pi[G_t \mid S_t=s, A_t=a]$ | 在 $s$ 做 $a$ 的期望回报 |

### 1.4 折扣回报

$$G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k+1} = r_{t+1} + \gamma G_{t+1}$$

**记忆技巧：** $G_t$ 是"从时间步 $t$ 起所有未来奖励的加权求和"，越远的奖励权重越小（$\gamma^k$）。

---

## §2 Q-Learning 核心公式 (Midterm 必考)

### 2.1 更新公式

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \Big]$$

**Python 对照：**

```python
qtable[state][action] = qtable[state][action] + alpha * (
    reward + gamma * max(qtable[next_state]) - qtable[state][action]
)
```

| Python 变量 | 数学符号 | 含义 |
|------------|---------|------|
| `qtable[state][action]` | $Q(s,a)$ | 当前 Q 值 |
| `alpha` | $\alpha$ | 学习率，控制更新幅度 |
| `reward` | $r$ | 即时奖励 |
| `gamma` | $\gamma$ | 折扣因子 |
| `max(qtable[next_state])` | $\max_{a'} Q(s',a')$ | 下一状态最大 Q 值 |

### 2.2 TD 拆分记忆法

更新公式可拆为三部分，逐层理解：

```
Q(s,a) ← Q(s,a) + α × [  TD target   -    Q(s,a)  ]
                          └─────────┘    └────────┘
                          r + γ max Q(s',a')   当前值
                          └──────────── TD error ──────────────┘
```

- **TD target** = 我们希望 Q 值最终达到的目标
- **TD error** = 目标与当前估值的差距，也叫"惊喜量"

---

## §3 Q-Learning Deep Dive — 必考讨论题

### 3.1 为什么 Q-Learning 收敛到最短路径？（Off-Policy vs On-Policy）

**问题：** CliffWalking 中 Q-Learning 收敛到紧贴悬崖的最短路径，而 SARSA 收敛到更安全但稍长的路径。为什么？

**答案：**

| 算法 | 更新目标 | 策略类型 | 结果 |
|------|---------|---------|------|
| Q-Learning | $\max_{a'} Q(s', a')$（假设下一步最优） | Off-policy | 紧贴悬崖的最短路径 |
| SARSA | $Q(s', a')$，其中 $a'$ 来自当前策略 | On-policy | 远离悬崖的安全路径 |

- **Q-Learning（Off-policy）**：更新目标*假设*下一步会选最优动作，与实际执行的策略（含随机探索）无关。即使偶尔随机探索掉入悬崖，也不影响 Q 值的更新目标。因此学到"理论最优"的最短路径。
- **SARSA（On-policy）**：更新目标用*实际执行*的动作。悬崖边的随机探索会真的掉落并产生巨额负奖励，这个负奖励被记入 Q 值，最终让 agent 害怕靠近悬崖。

> ⚠️ **一句话对比：** Q-Learning 学"如果我完美行动的最优"，SARSA 学"考虑到我会犯错的最优"。

### 3.2 Q-Table 初始化策略

| 初始化方式 | 效果 | 适用场景 |
|-----------|------|---------|
| 全部初始化为 0 | 未探索状态无动力访问，探索慢 | 简单环境 |
| 乐观初始化（高值）| 未访问状态"看起来更好"，驱动系统性探索 | 推荐 |
| 随机初始化 | 探索彻底但不稳定 | 理论分析 |

**乐观初始化的直觉：** 假设所有 Q 值初始为 10（远高于实际奖励），任何被访问的状态获得真实奖励（通常低于 10）后，Q 值下降，计算机会优先访问那些"还没被'失望'过"的高初始值状态。

### 3.3 终止状态 Q 值为什么必须为 0？

**更新公式在终止状态的情况：**

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ r + \gamma \max_{a'} Q(s_{\text{terminal}}, a') - Q(s, a) \Big]$$

若终止状态 $Q \neq 0$，则 $\gamma \max Q(s_{\text{terminal}}, a')$ 会给更新目标添加"虚假未来奖励"——但终止状态之后不会有任何交互。这破坏了 Bellman 方程的正确性，Q 值无法收敛到真实值。

**设为 0 的保证：** 更新目标变为 $r + \gamma \times 0 = r$，仅反映当前步的真实奖励。

---

## §4 Gymnasium 自定义环境要点

### 4.1 `step()` 返回值（必须记住）

```python
obs, reward, terminated, truncated, info = env.step(action)
```

| 返回值 | 类型 | 含义 |
|--------|------|------|
| `obs` | np.ndarray / dict | 新状态观测 |
| `reward` | float | 即时奖励 |
| `terminated` | bool | 自然结束（达到目标/失败） |
| `truncated` | bool | 超时结束（TimeLimit 触发） |
| `info` | dict | 调试信息 |

> ⚠️ **常见错误：** 旧版 Gym 只返回 4 个值（`done` 代替 `terminated + truncated`），Gymnasium 5 个值。考试中按 Gymnasium 标准。

### 4.2 空间定义常见类型

```python
# 离散动作空间 (4 个动作)
self.action_space = gym.spaces.Discrete(4)

# 连续状态空间 (2D 坐标)
self.observation_space = gym.spaces.Box(low=0.0, high=1.0, shape=(2,))

# 字典观测空间
self.observation_space = gym.spaces.Dict({
    "current": gym.spaces.Discrete(n_states),
    "target": gym.spaces.Discrete(n_states)
})
```

### 4.3 什么是 Gymnasium Wrapper？

标准答案（来自老师 slides）：

> A convenient way to modify an existing environment without altering the underlying code directly. You initialize a base environment first, then pass it to the wrapper's constructor.

用途示例：
- `TimeLimit(env, max_episode_steps=200)` — 限制步数
- `DiscreteActionWrapper(env)` — 修改动作空间

---

## §5 Stable-Baselines3 核心 API

### 5.1 什么是 SB3？（标准答案）

> Stable-baselines3 is a set of reliable Reinforcement Learning algorithm implementations that includes features such as **vectorized environments** and **callbacks**.

### 5.2 核心 API 速查

```python
# 创建向量化环境（4 个并行副本）
env = make_vec_env(make_env_fn, n_envs=4)

# 创建模型
model = PPO("MlpPolicy", env, verbose=1)
model = DQN("MultiInputPolicy", env, learning_starts=100, batch_size=512)

# 训练
model.learn(total_timesteps=1_000_000)

# 保存和加载
model.save("ppo_model")
model = PPO.load("ppo_model", env)

# 推理
obs = env.reset()
action, _ = model.predict(obs, deterministic=True)
```

### 5.3 Vectorized Environments 的意义

| 类型 | 含义 |
|------|------|
| `DummyVecEnv` | 单进程串行，适合简单环境 |
| `SubprocVecEnv` | 多进程并行，适合复杂环境 |

**为什么向量化？** On-policy 算法（PPO/A2C）每次更新后丢弃数据，并行 $n$ 个环境意味着每步收集 $n$ 倍数据，显著提高采样效率。

---

## §6 期中笔试备考策略 (Exam Strategy)

### 6.1 必记公式清单

| 公式 | 优先级 |
|------|--------|
| Q-Learning 更新公式 + Python 版 | ⭐⭐⭐ 必考 |
| 折扣回报 $G_t$ 展开式 | ⭐⭐⭐ |
| ε-Greedy 公式 | ⭐⭐ |
| 状态价值函数 $V_\pi(s)$ 定义 | ⭐⭐ |
| Markov Property 公式 | ⭐ |

### 6.2 必答概念题

根据老师 slides 中的笔试样题，以下问答必须能流畅作答：

1. **画出 RL 框架图** — Agent ↔ Environment，标出 $S_t$, $A_t$, $R_{t+1}$, $S_{t+1}$
2. **Q-table 更新公式（Python 语法）** — 附变量解释表
3. **What is Gymnasium?** — API standard + reference environments
4. **What is a Gymnasium Wrapper?** — 不修改底层代码的环境修改方式
5. **What is Stable-Baselines3?** — 可靠 RL 算法实现集合，含 vectorized env + callbacks

### 6.3 概念辨析题 — Q-Learning vs SARSA

| 维度 | Q-Learning | SARSA |
|------|-----------|-------|
| On/Off-Policy | Off-policy | On-policy |
| 更新目标 | $\max_{a'} Q(s', a')$ | $Q(s', a')$（实际执行） |
| CliffWalking 收敛路径 | 最短（贴悬崖） | 更安全（远离悬崖） |
| 实际性能差异 | 理论最优 | 实际执行时更好 |

---

## 📋 期中备考检查清单

**RL 基础**
- [ ] 能画出 Agent-Environment 交互图并标注所有符号
- [ ] 能说出 Markov Property 并解释其实践意义
- [ ] 能写出折扣回报 $G_t$ 公式并做手算

**Q-Learning**
- [ ] 能默写 Q-Learning 更新公式（数学版 + Python 版）
- [ ] 能解释 TD target, TD error 各是什么
- [ ] 能区分 Q-Learning（off-policy）与 SARSA（on-policy）

**Deep Dive**
- [ ] 能解释终止状态 Q=0 的重要性
- [ ] 能比较三种 Q-table 初始化策略

**Gymnasium**
- [ ] 能说出 `step()` 的 5 个返回值
- [ ] 能定义 `Discrete`, `Box`, `Dict` 观测空间
- [ ] 能描述 Gymnasium Wrapper 是什么

**SB3**
- [ ] 能用一句话描述 SB3 是什么
- [ ] 知道 `learn()`, `predict()`, `save()`, `load()` 的用途
- [ ] 能解释 vectorized env 的意义
