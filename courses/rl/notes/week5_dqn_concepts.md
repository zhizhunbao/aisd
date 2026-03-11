# Week 5: DQN — 核心概念 (Core Concepts)

> See also: [幻灯片笔记](week5_dqn_slides.md) | [数学公式](week5_dqn_math.md) | [操作教程](week5_dqn_tutorial.md) | [历史背景](week5_dqn_history.md)

---

## 核心术语速查

### DQN（Deep Q-Network）

用神经网络代替 Q-table 来近似 Q 值函数：

$$Q_\theta(s, a) \approx Q^*(s, a)$$

输入状态 $s$，输出所有动作的 Q 值向量。参数 $\theta$ 固定大小，不随状态空间增大。

---

### 维度诅咒（Curse of Dimensionality）

Q-table 大小 = 状态数 × 动作数。状态空间指数增长时（如 8 块积木 = $8^8$ 种状态），表格不可行。DQN 用神经网络拟合，绕过这个问题。

---

### Q-Network（主网络）

参数为 $\theta$ 的神经网络，负责：
- 预测当前 $(s, a)$ 的 Q 值
- 通过反向传播更新（每步都更新）

---

### Target Network（目标网络）

主网络的**延迟副本**，参数为 $\theta^-$，负责计算训练目标：

$$y = r + \gamma \max_{a'} Q_{\theta^-}(s', a')$$

**每隔 `target_update_interval` 步**将主网络参数同步到目标网络。

**为什么需要？** 如果用同一个网络计算预测和目标，目标一直在动，训练极其不稳定——类似"追移动靶"。目标网络固定一段时间，使训练目标稳定。

---

### Replay Buffer（经验回放）

存储历史转移 $(s, a, r, s')$ 的固定大小队列，训练时随机采样 mini-batch：

**为什么需要？** 连续采样的数据时间相关（$s_0→s_1→s_2$ 是序列），违反神经网络训练"独立同分布"假设，导致不稳定。随机采样打破相关性。

| 参数 | 含义 |
|------|------|
| `buffer_size` | 缓冲区容量（默认 1,000,000） |
| `learning_starts` | 至少收集多少步随机数据后才开始训练 |
| `batch_size` | 每次训练采样多少条数据 |

---

### DQN 损失函数（MSE）

$$L(\theta) = \frac{1}{N} \sum_{i=1}^{N} \left( Q_\theta(s_i, a_i) - y_i \right)^2$$

其中 $y_i = r_i + \gamma \max_{a'} Q_{\theta^-}(s_i', a')$（目标网络计算）

---

### DiscreteActionWrapper

将 `MultiDiscrete` 动作空间展平为 `Discrete`，使 DQN 可以使用：

$$|\text{Discrete}| = \prod_i d_i$$

- `MultiDiscrete([4, 4])` → `Discrete(16)`
- 还原：`np.unravel_index(flat_action, dims)`

**需要的原因：** DQN 的 Q-Network 输出层大小 = 动作数（一个整数），必须是单一的 `Discrete` 空间。

---

### ε-Greedy 衰减（SB3 DQN）

SB3 中 ε 的衰减由两个参数控制：

| 参数 | 含义 |
|------|------|
| `exploration_fraction` | 在前 X% 的总步数内，ε 从 1.0 线性衰减 |
| `exploration_final_eps` | ε 衰减到的最终值（保持不变） |

---

### TensorBoard 关键指标

| 指标 | 含义 |
|------|------|
| `rollout/ep_rew_mean` | 最近 100 个 episode 的平均奖励（主要训练信号） |
| `train/loss` | Q 网络的 MSE 损失（应下降） |
| `rollout/exploration_rate` | 当前 ε 值（应从 1.0 下降到 0.05） |

---

## 概念辨析

### DQN 三大创新对比

| 创新 | 解决的问题 | 关键参数 |
|------|-----------|---------|
| Replay Buffer | 数据时间相关导致不稳定 | `buffer_size`, `batch_size`, `learning_starts` |
| Target Network | 训练目标不断移动导致不稳定 | `target_update_interval` |
| Q-Network | Q-table 无法处理大状态空间 | 网络结构（`policy_kwargs`） |

### DQN vs Q-Learning vs PPO

| 维度 | Q-Learning | DQN | PPO |
|------|-----------|-----|-----|
| Q 值存储 | 表格 | 神经网络 | 不存 Q 值（直接学策略） |
| 状态空间 | 小型离散 | 大型/连续 | 任意 |
| 动作空间 | 离散 | **仅离散** | 离散或连续 |
| Off/On-policy | Off | Off | On |
| 数据复用 | 可复用 | Replay Buffer | 一次性 |

### `learning_starts` vs `buffer_size`

- `learning_starts=100`：前 100 步只收集数据，不训练（确保 Buffer 不为空）
- `buffer_size=1_000_000`：Buffer 的**总容量**（满了后丢弃最旧的数据）

---

## 易错点速查

| 错误 | 正确理解 |
|------|---------|
| "DQN 可以处理连续动作空间" | DQN 只支持 `Discrete`，连续动作用 TD3/SAC |
| "Target Network 每步都更新" | 每隔 `target_update_interval` 步才同步一次 |
| "Replay Buffer 越大越好" | 过大的 Buffer 包含过时的经验，可能减慢学习 |
| VecEnv `step()` 返回 5 个值 | VecEnv 返回 4 个（自动处理 terminated/truncated） |
| "`deterministic=True` 在训练时用" | 推理时用 `deterministic=True`，训练时 SB3 自动管理 ε |
