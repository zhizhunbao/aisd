# Week 6: 期中复习 — 核心概念 (Core Concepts)

> See also: [幻灯片笔记](week6_midterm_review_slides.md) | [操作教程](week6_midterm_review_tutorial.md) | [Quiz](week6_midterm_review_quiz.md)

---

> 本文件是 Week 1-5 全部核心概念的**压缩版速查表**，作为期中备考的单一入口。每个概念附来源周，详细内容查对应文件。

---

## RL 基础（来自 Week 1）

### Agent-Environment 交互

```
Agent ──(action At)──► Environment ──(reward R_{t+1}, state S_{t+1})──► Agent
```

三要素：**Agent**（观察状态、选择动作）、**Environment**（接受动作、返回奖励+状态）、**Reward**（标量反馈信号）

### Markov Property

未来只依赖当前状态，与历史无关：$P(S_{t+1} \mid S_t, A_t) = P(S_{t+1} \mid H_t)$

### Policy（策略）

| 类型 | 公式 |
|------|------|
| 确定性 | $a = \pi(s)$ |
| 随机性 | $\pi(a \mid s) = P[A=a \mid S=s]$，约束 $\sum_a \pi(a\|s) = 1$ |

### Return（折扣回报）

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} = R_{t+1} + \gamma G_{t+1}$$

### Value Functions（价值函数）

| 函数 | 公式 |
|------|------|
| $V_\pi(s)$ | $\mathbb{E}_\pi[G_t \mid S_t=s]$ |
| $Q_\pi(s,a)$ | $\mathbb{E}_\pi[G_t \mid S_t=s, A_t=a]$ |

---

## Q-Learning（来自 Week 2）

### 更新公式（★★★ 必考）

$$Q(s,a) \leftarrow Q(s,a) + \alpha \Big[ r + \gamma \max_{a'} Q(s',a') - Q(s,a) \Big]$$

**Python 版：**
```python
qtable[s][a] = qtable[s][a] + alpha * (reward + gamma * max(qtable[s_]) - qtable[s][a])
```

### ε-Greedy

$$a = \begin{cases} \arg\max_{a'} Q(s,a') & 1-\varepsilon \\ \text{random} & \varepsilon \end{cases}$$

### Off-Policy vs On-Policy

| | Q-Learning | SARSA |
|-|-----------|-------|
| 类型 | Off-policy | On-policy |
| target | $\max_{a'} Q(s',a')$ | $Q(s', a')$（实际执行） |
| CliffWalking | 最短路径（贴悬崖） | 更安全路径 |

### Q-Table 初始化

- **全 0**：探索动力不足
- **乐观高值**：驱动主动探索，推荐
- **终止状态必须为 0**：否则 Bellman 更新引入虚假未来奖励

---

## Gymnasium（来自 Week 3）

### `step()` 五个返回值（必考）

```python
obs, reward, terminated, truncated, info = env.step(action)
```

- `terminated`：自然结束（目标达成/死亡）
- `truncated`：超时结束（TimeLimit）

### 空间类型速查

| 空间 | 用途 |
|------|------|
| `Discrete(n)` | $n$ 个离散动作/状态 |
| `Box(low, high, shape)` | 连续多维数组 |
| `Dict({...})` | 多 key 字典观测 |
| `MultiDiscrete([n1,n2])` | 多个独立离散变量 |

### Wrapper

不修改底层代码的环境修改方式。先初始化环境，再传给 Wrapper 构造函数。

### Policy 选择

- `Dict` 观测 → `MultiInputPolicy`
- 单一 `Discrete`/`Box` → `MlpPolicy`

---

## Stable-Baselines3（来自 Week 4）

### 什么是 SB3

一套可靠的 RL 算法实现，包含向量化环境支持和回调函数机制。

### 算法选择

| 动作空间 | 推荐算法 |
|---------|---------|
| 离散 | DQN, PPO, A2C |
| 连续 | SAC, TD3, PPO |

### 核心 API

```python
model = PPO("MlpPolicy", env)
model.learn(total_timesteps=100_000)
action, _ = model.predict(obs, deterministic=True)
model.save("path") ; model = PPO.load("path", env)
```

### Vectorized Environments

$n$ 个并行环境，每步收集 $n$ 个转移。On-policy 算法（PPO）受益最大。

---

## DQN 深入（来自 Week 5）

### 三大创新

| 创新 | 解决问题 |
|------|---------|
| Q-Network（神经网络） | Q-table 无法处理大状态空间（维度诅咒） |
| Target Network | 同一网络计算预测和目标 → 不稳定（追移动靶） |
| Replay Buffer | 时间相关数据 → 违反独立同分布假设 |

### 目标 Q 值

$$y = r + \gamma \max_{a'} Q_{\theta^-}(s', a')$$

用**目标网络** $Q_{\theta^-}$ 计算（非主网络）

### DiscreteActionWrapper

`MultiDiscrete([4,4])` → `Discrete(16)`，用 `np.unravel_index()` 还原

---

## 期中高频考点汇总

| 考点 | 关键答案 |
|------|---------|
| Q-Learning 公式 Python 版 | `q[s][a] = q[s][a] + alpha*(r + gamma*max(q[s_]) - q[s][a])` |
| RL 框架图 | Agent↔Environment，标注 $S_t, A_t, R_{t+1}, S_{t+1}$ |
| 终止状态 Q=0 的原因 | 防止引入虚假未来奖励，破坏 Bellman 方程正确性 |
| Q-Learning 最短路径原因 | Off-policy，更新目标不感知随机探索风险 |
| What is Gymnasium | API standard for RL with diverse reference environments |
| What is a Wrapper | Modify env without altering underlying code |
| What is SB3 | Reliable RL algorithm implementations + VecEnv + Callbacks |

---

## 易错点汇总（跨周）

| 错误 | 正确 |
|------|------|
| `terminated` = `done` | `done = terminated or truncated`（语义不同） |
| DQN 支持连续动作 | DQN 只支持 `Discrete` |
| SAC 用于离散动作 | SAC 只支持连续动作空间 |
| Target Network 每步更新 | 每隔 `target_update_interval` 步同步一次 |
| $\gamma = 1$ 是最好的 | 持续任务中 $G_t$ 发散，必须 $\gamma < 1$ |
