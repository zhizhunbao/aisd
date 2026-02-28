# Week 4: Stable-Baselines3 — 数学公式 (Math Reference)

> See also: [概念速查](week4_sb3_cheatsheet.md) | [代码参考](week4_sb3_code.md)

---

## 📐 DQN 损失函数

$$L(\theta) = \mathbb{E}\left[\left(r + \gamma \max_{a'} Q_{\theta^-}(s', a') - Q_\theta(s, a)\right)^2\right]$$

| 符号 | 含义 | SB3 对应 |
|------|------|---------|
| $Q_\theta(s,a)$ | 当前网络的 Q 值估计 | 主网络 |
| $Q_{\theta^-}(s',a')$ | 目标网络的 Q 值估计 | 延迟更新的目标网络 |
| $\gamma$ | 折扣因子 | `gamma=0.99` |
| $r$ | 即时奖励 | `reward` |

---

## 📐 Policy Gradient (REINFORCE)

$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\left[\nabla_\theta \log \pi_\theta(a|s) \cdot G_t\right]$$

| 符号 | 含义 |
|------|------|
| $\pi_\theta(a\|s)$ | 参数化策略（给定状态 s 选择动作 a 的概率）|
| $G_t$ | 从时间步 t 开始的累积折扣回报 |
| $J(\theta)$ | 期望回报（要最大化的目标）|

---

## 📐 Advantage Function (A2C)

$$A(s,a) = Q(s,a) - V(s) \approx r + \gamma V(s') - V(s)$$

| 符号 | 含义 | 网络 |
|------|------|------|
| $V(s)$ | 状态价值函数 | Critic 网络 (`vf`) |
| $Q(s,a)$ | 状态-动作价值函数 | 通过 TD 估计 |
| $A(s,a)$ | 优势函数（动作比平均好多少）| 计算得到 |

---

## 📐 GAE (Generalized Advantage Estimation)

$$\hat{A}_t^{GAE(\gamma,\lambda)} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}$$

其中 TD error: $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$

| 符号 | 含义 | SB3 参数 |
|------|------|---------|
| $\lambda$ | bias-variance 权衡 | `gae_lambda` |
| $\lambda=1$ | 高方差，低偏差（= Monte Carlo） | |
| $\lambda=0$ | 低方差，高偏差（= 1-step TD） | |

---

## 📐 PPO Clipped Objective

$$L^{CLIP}(\theta) = \mathbb{E}\left[\min\left(r_t(\theta) \hat{A}_t,\ \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t\right)\right]$$

其中概率比: $r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$

| 符号 | 含义 | SB3 参数 |
|------|------|---------|
| $r_t(\theta)$ | 新旧策略的概率比 | 内部计算 |
| $\epsilon$ | 裁剪范围 | `clip_range=0.2` |
| $\hat{A}_t$ | GAE 估计的优势 | 由 `gae_lambda` 控制 |

---

## 📐 SAC 最大熵目标

$$\pi^* = \arg\max_\pi \mathbb{E}\left[\sum_t r_t + \alpha \mathcal{H}(\pi(\cdot|s_t))\right]$$

| 符号 | 含义 | SB3 参数 |
|------|------|---------|
| $\mathcal{H}(\pi)$ | 策略的熵 | 内部计算 |
| $\alpha$ | 温度参数（熵的权重）| `ent_coef="auto"` |

---

## 📝 手算练习

### 练习 1：TD Error 计算

给定 $V(s) = 0.5$, $V(s') = 0.8$, $r = 1.0$, $\gamma = 0.99$，计算 TD error $\delta$。

<details>
<summary>答案</summary>

$\delta = r + \gamma V(s') - V(s) = 1.0 + 0.99 \times 0.8 - 0.5 = 1.0 + 0.792 - 0.5 = 1.292$

</details>

### 练习 2：PPO 概率比

旧策略 $\pi_{old}(a|s) = 0.3$，新策略 $\pi_\theta(a|s) = 0.45$，计算概率比 $r_t(\theta)$。

<details>
<summary>答案</summary>

$r_t(\theta) = \frac{0.45}{0.3} = 1.5$

如果 $\epsilon = 0.2$，裁剪范围是 $[0.8, 1.2]$，所以 $r_t = 1.5$ 会被裁剪到 $1.2$。

</details>

### 练习 3：Q-Table vs DQN 参数量

4×3 GridWorld（12 状态，4 动作）：
- Q-Table 有多少参数？
- 一个 2 层全连接网络（输入 12，隐藏层 64，输出 4）有多少参数？

<details>
<summary>答案</summary>

- Q-Table: $12 \times 4 = 48$ 个参数
- DQN: $(12 \times 64 + 64) + (64 \times 4 + 4) = 768 + 64 + 256 + 4 = 1092$ 个参数
- DQN 参数量远大于 Q-Table，但可以泛化到未见过的状态

</details>
