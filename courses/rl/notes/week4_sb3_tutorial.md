# Week 4: Stable-Baselines3 — 教程 (Tutorial)

> 📚 基于 SB3 官方文档 + Sutton & Barto Ch.6 (TD Learning) / Ch.13 (Policy Gradient)
> 核心问题：Slides 展示了 SB3 的 API 用法，但没解释各算法背后的理论基础

---

## §0 前置知识 (Prerequisites)

> **概念前置：** Q-Learning 更新规则 — 参见 `week2_mdp_tutorial.md`
> **概念前置：** Gymnasium 环境 API — 参见 `week3_gymnasium_tutorial.md`

---

## §1 从 Q-Learning 到 DQN

> 📚 Ref: Mnih et al. 2015 "Human-level control through deep reinforcement learning" (Nature)

### 1.1 Q-Learning 的瓶颈

Q-Learning 用表格存储 Q 值：$Q(s,a)$ 对每个 $(s,a)$ 对存一个数。

| 符号 | 含义 | 例子 |
|------|------|------|
| $Q(s,a)$ | 状态-动作价值 | Q(state=8, action=右) = 0.96 |
| $\|S\|$ | 状态空间大小 | GridWorld: 12 |
| $\|A\|$ | 动作空间大小 | 4 个方向 |

Q-table 大小 = $|S| \times |A|$。当状态空间很大时（如 Atari 游戏有 $\sim 10^{70}$ 种屏幕像素组合），表格方法不可行。

### 1.2 DQN 的核心思想

用神经网络 $Q_\theta(s,a)$ 近似 Q 函数，其中 $\theta$ 是网络参数：

$$Q_\theta(s,a) \approx Q^*(s,a)$$

DQN 的两个关键创新：
1. **Experience Replay** — 将转移 $(s, a, r, s')$ 存入 replay buffer，随机采样训练 → 打破数据相关性
2. **Target Network** — 用一个延迟更新的目标网络计算 TD target → 稳定训练

> ⚠️ **Slides 未强调：** DQN 只能处理**离散动作空间**，因为它需要对所有动作计算 Q 值然后取 argmax。

但要实际使用 DQN，还需要理解它与 Q-Learning 的关系。DQN 的损失函数本质上就是 TD error 的平方：

$$L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q_{\theta^-}(s', a') - Q_\theta(s, a)\right)^2\right]$$

其中 $\theta^-$ 是目标网络的参数。

---

## §2 Policy Gradient 方法：PPO 和 A2C

> 📚 Ref: Sutton & Barto §13.1-13.4 — Policy Gradient Methods

### 2.1 为什么需要 Policy Gradient？

DQN 通过学习 Q 函数间接得到策略（$\pi(s) = \arg\max_a Q(s,a)$）。但这有两个问题：

1. **连续动作空间** — 无法对无穷多个动作取 argmax
2. **随机策略** — 有时最优策略是随机的（如石头剪刀布）

Policy Gradient 直接参数化策略 $\pi_\theta(a|s)$，用梯度上升最大化期望回报。

### 2.2 REINFORCE 到 Actor-Critic

| 方法 | 更新目标 | 方差 | 偏差 |
|------|---------|------|------|
| REINFORCE | $G_t$（完整回报） | 高 | 无 |
| Actor-Critic (A2C) | $r + \gamma V(s') - V(s)$（TD error） | 低 | 有 |
| PPO | Clipped surrogate objective | 低 | 有 |

### 2.3 A2C (Advantage Actor-Critic)

A2C 用两个网络：
- **Actor** $\pi_\theta(a|s)$ — 输出动作概率
- **Critic** $V_\phi(s)$ — 估计状态价值

Advantage 函数：$A(s,a) = Q(s,a) - V(s) \approx r + \gamma V(s') - V(s)$

> ⚠️ **Slides 未解释：** `gae_lambda` 参数控制 GAE (Generalized Advantage Estimation)，是 bias-variance 的权衡：
> - `gae_lambda=1.0` → 等价于经典 advantage（高方差，低偏差）
> - `gae_lambda=0.0` → 只用一步 TD error（低方差，高偏差）

### 2.4 PPO (Proximal Policy Optimization)

PPO 是目前最流行的 RL 算法，核心思想是**限制策略更新幅度**：

$$L^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r_t(\theta) A_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t\right)\right]$$

其中 $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$ 是新旧策略的概率比。

直觉：如果新策略偏离旧策略太多，就裁剪掉，防止灾难性更新。

---

## §3 SAC (Soft Actor-Critic)

> 📚 Ref: Haarnoja et al. 2018 "Soft Actor-Critic"

SAC 是 off-policy actor-critic 方法，核心创新是**最大熵框架**：

$$\pi^* = \arg\max_\pi \mathbb{E}\left[\sum_t r_t + \alpha \mathcal{H}(\pi(\cdot|s_t))\right]$$

其中 $\mathcal{H}$ 是策略的熵，$\alpha$ 是温度参数。

直觉：不仅最大化奖励，还鼓励策略保持"随机性" → 更好的探索 + 更鲁棒。

> ⚠️ **Slides 未强调：** SAC 只支持**连续动作空间**。对于离散动作，用 DQN 或 PPO。

---

## §4 向量化环境的理论基础

> 📚 Ref: SB3 Documentation — Vectorized Environments

### 4.1 为什么并行收集数据？

On-policy 算法（PPO, A2C）每次更新后必须丢弃旧数据。如果每步只收集 1 个转移，效率极低。

向量化环境同时运行 $n$ 个环境，每步收集 $n$ 个转移：

$$\text{数据效率} \propto n \times \text{steps\_per\_update}$$

### 4.2 DummyVecEnv vs SubprocVecEnv

| 类型 | 实现 | 适用场景 |
|------|------|---------|
| `DummyVecEnv` | 单进程串行 | 简单环境（GridWorld） |
| `SubprocVecEnv` | 多进程并行 | 计算密集型环境（Atari） |

对于课程中的简单环境，`DummyVecEnv` 足够。SB3 会自动将单个环境包装为 `DummyVecEnv`。

---

## §5 超参数调优的理论依据

> 📚 Ref: SB3 RL Tips and Tricks

### 5.1 关键超参数解释

| 参数 | 含义 | 默认值 | 影响 |
|------|------|--------|------|
| `learning_rate` | 梯度更新步长 | 3e-4 | 太大→不稳定，太小→收敛慢 |
| `gamma` | 折扣因子 | 0.99 | 接近 1→重视长期，接近 0→重视短期 |
| `n_steps` | 每次更新收集的步数 | 2048 (PPO) | 大→更稳定但更慢 |
| `gae_lambda` | GAE bias-variance 权衡 | 0.95 | 1.0→高方差，0.0→高偏差 |
| `ent_coef` | 熵系数 | 0.0 | 大→更多探索 |
| `max_grad_norm` | 梯度裁剪阈值 | 0.5 | 防止梯度爆炸 |

### 5.2 网络架构 (`policy_kwargs`)

```python
policy_kwargs = dict(
    net_arch=[dict(vf=[64, 64], pi=[64, 64])],
    # vf = value function (critic) 网络
    # pi = policy (actor) 网络
    activation_fn=nn.Tanh,
    ortho_init=True,  # 正交初始化，有助于训练稳定性
)
```

> ⚠️ **Slides 未解释：** `net_arch` 中 `vf` 和 `pi` 分别是 critic 和 actor 的网络架构。如果只传一个列表（如 `[64, 64]`），则 actor 和 critic 共享网络。

---

## 📚 参考索引表

| 教程章节 | 来源 | 核心内容 | Slides 覆盖？ |
|---------|------|---------|-------------|
| §1 Q-Learning → DQN | Mnih 2015 | Experience Replay + Target Network | ❌ 未覆盖 |
| §2 Policy Gradient | Sutton §13 | REINFORCE → A2C → PPO | ❌ 未覆盖 |
| §3 SAC | Haarnoja 2018 | 最大熵框架 | ❌ 未覆盖 |
| §4 向量化环境 | SB3 Docs | DummyVecEnv vs SubprocVecEnv | ⚠️ 部分 |
| §5 超参数调优 | SB3 Docs | 参数含义和调优策略 | ⚠️ 部分（只展示了代码） |
