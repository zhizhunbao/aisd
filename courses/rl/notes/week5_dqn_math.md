# Week 5: DQN — 数学公式 (Math Reference)

> See also: [概念速查](week5_dqn_cheatsheet.md) | [代码参考](week5_dqn_code.md)

---

## 📐 核心公式

### 1. Q-Learning 更新公式（Q-Table 版，Week 2 回顾）

| 符号 | 含义 |
|------|------|
| $Q(s,a)$ | 状态 s 下执行动作 a 的价值 |
| $\alpha$ | 学习率 (learning rate) |
| $r$ | 即时奖励 (immediate reward) |
| $\gamma$ | 折扣因子 (discount factor) |
| $s'$ | 下一个状态 (next state) |

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

- 这是表格版 Q-Learning，直接更新表格中的值

### 2. DQN 目标 Q 值公式

| 符号 | 含义 |
|------|------|
| $y$ | 目标 Q 值 (target Q-value) |
| $r$ | 即时奖励 |
| $\gamma$ | 折扣因子 |
| $Q_{target}(s', a')$ | **目标网络**对下一状态的 Q 值估计 |

$$y = r + \gamma \max_{a'} Q_{target}(s', a')$$

- ⚠️ 注意：用的是 **Target Network**（不是主网络）来计算目标
- 如果 $s'$ 是终止状态，则 $y = r$（没有未来奖励）

### 3. DQN 损失函数

| 符号 | 含义 |
|------|------|
| $Q_\theta(s, a)$ | 主网络对当前 (s, a) 的 Q 值预测 |
| $y$ | 目标 Q 值（由公式 2 计算） |
| $N$ | mini-batch 大小 |

$$L(\theta) = \frac{1}{N} \sum_{i=1}^{N} \left( Q_\theta(s_i, a_i) - y_i \right)^2$$

- 均方误差 (MSE) 损失
- 通过反向传播更新主网络参数 $\theta$

### 4. ε-Greedy 动作选择

$$a = \begin{cases} \text{random action} & \text{with probability } \varepsilon \\ \arg\max_a Q_\theta(s, a) & \text{with probability } 1 - \varepsilon \end{cases}$$

- $\varepsilon$ 通常从 1.0 线性衰减到 0.05
- 训练初期多探索，后期多利用

### 5. MultiDiscrete → Discrete 展平

| 符号 | 含义 |
|------|------|
| $d_1, d_2, \ldots, d_k$ | 各维度的动作数 |
| $a_{flat}$ | 展平后的单一整数动作 |

$$|\text{Discrete}| = \prod_{i=1}^{k} d_i$$

- 例：`MultiDiscrete([2, 3])` → $2 \times 3 = 6$ → `Discrete(6)`
- 还原：`np.unravel_index(a_flat, dims)` 将整数映射回多维索引

---

## 📝 手算练习

### 练习 1：计算目标 Q 值

已知：
- 即时奖励 $r = 1$
- 折扣因子 $\gamma = 0.99$
- Target Network 对下一状态的 Q 值：$Q_{target}(s', a_0) = 2.5$, $Q_{target}(s', a_1) = 3.0$, $Q_{target}(s', a_2) = 1.8$

求目标 Q 值 $y$：

$$y = r + \gamma \max_{a'} Q_{target}(s', a') = 1 + 0.99 \times 3.0 = 1 + 2.97 = \mathbf{3.97}$$

### 练习 2：计算 MSE 损失

已知 mini-batch (N=3)：

| 样本 | $Q_\theta(s, a)$ | $y$ |
|------|-----------------|-----|
| 1 | 3.5 | 3.97 |
| 2 | 2.0 | 2.5 |
| 3 | 4.1 | 3.8 |

$$L = \frac{1}{3} \left[ (3.5 - 3.97)^2 + (2.0 - 2.5)^2 + (4.1 - 3.8)^2 \right]$$
$$= \frac{1}{3} \left[ 0.2209 + 0.25 + 0.09 \right] = \frac{0.5609}{3} = \mathbf{0.187}$$

### 练习 3：MultiDiscrete 展平

环境动作空间：`MultiDiscrete([3, 4])`

1. 总动作数 = $3 \times 4 = 12$ → `Discrete(12)`
2. 动作 7 对应的多维索引：`np.unravel_index(7, (3, 4))` = $(1, 3)$
   - 验证：$1 \times 4 + 3 = 7$ ✅
3. 多维动作 $(2, 1)$ 对应的整数：$2 \times 4 + 1 = 9$

### 练习 4：ε-Greedy 动作选择

已知：
- $\varepsilon = 0.1$
- $Q_\theta(s, a_0) = 2.3$, $Q_\theta(s, a_1) = 5.1$, $Q_\theta(s, a_2) = 3.7$

- 90% 概率选择 $a_1$（Q 值最大 = 5.1）
- 10% 概率随机选择 $a_0$, $a_1$, $a_2$ 之一（各 $\frac{0.1}{3} \approx 3.3\%$）

---

## 📋 公式速查表

| 公式 | 用途 | 关键点 |
|------|------|--------|
| $y = r + \gamma \max_{a'} Q_{target}(s', a')$ | DQN 目标值 | 用 Target Network |
| $L = \frac{1}{N}\sum(Q_\theta - y)^2$ | MSE 损失 | 更新主网络 |
| $\varepsilon$-greedy | 动作选择 | ε 衰减：探索→利用 |
| $\prod d_i$ | MultiDiscrete 展平 | `np.unravel_index` 还原 |
