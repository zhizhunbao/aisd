# Week 5: DQN Quiz

> 基于 CST8509_05_DQN_Stable-Baselines3 slides 生成

---

## 选择题 (Multiple Choice)

### Q1. DQN 中 Target Network 的主要作用是什么？

A. 加速训练过程
B. 减少内存使用
C. 稳定训练目标，防止目标 Q 值不断漂移
D. 增加探索能力

### Q2. Replay Buffer 解决了什么问题？

A. 状态空间太大
B. 动作空间不兼容
C. 连续样本之间的时间相关性
D. 神经网络过拟合

### Q3. DQN 的动作空间要求是什么？

A. 必须是 Continuous
B. 必须是 Discrete
C. 必须是 MultiDiscrete
D. 可以是任意类型

### Q4. `MultiDiscrete([3, 4])` 展平为 Discrete 后，总动作数是多少？

A. 7
B. 12
C. 34
D. 64

### Q5. `np.unravel_index(7, (3, 4))` 的结果是什么？

A. (0, 7)
B. (1, 3)
C. (2, 3)
D. (1, 2)

### Q6. DQN 目标 Q 值公式 $y = r + \gamma \max_{a'} Q(s', a')$ 中，Q 值由哪个网络计算？

A. 主 Q-Network
B. Target Network
C. 两个网络的平均
D. 随机选择一个

### Q7. 在 SB3 中，`learning_starts=100` 参数的含义是什么？

A. 学习率设为 100
B. 每 100 步更新一次
C. 前 100 步随机行动，不进行学习
D. 训练 100 个 episode

### Q8. VecEnv 的 `step()` 方法返回几个值？

A. 3
B. 4
C. 5
D. 6

### Q9. 在 SB3 DQN 中，`log_interval=1` 控制什么？

A. 每步打印一次日志
B. 每个 episode 向 TensorBoard 写入一次数据
C. 每步更新一次模型
D. 每个 episode 保存一次模型

### Q10. 当观测值是字典类型（Dict）时，应该使用哪个 Policy？

A. MlpPolicy
B. CnnPolicy
C. MultiInputPolicy
D. DictPolicy

---

## 判断题 (True/False)

### T1. DQN 可以处理连续动作空间。

### T2. Target Network 每一步都从主网络复制权重。

### T3. Replay Buffer 按时间顺序提供训练数据。

### T4. ε-Greedy 中的 ε 通常随训练逐渐衰减。

### T5. `deterministic=True` 在推理时让模型选择 Q 值最大的动作。

---

## 简答题 (Short Answer)

### S1. 已知 r = 2, γ = 0.95, Q_target(s', a₀) = 4.0, Q_target(s', a₁) = 6.0, Q_target(s', a₂) = 3.5。计算目标 Q 值 y。

### S2. 解释为什么 DQN 需要 Target Network。如果不用 Target Network 会发生什么？

---

## 答案 (Answers)

### 选择题

| 题号 | 答案 | 解释 |
|------|------|------|
| Q1 | C | Target Network 提供稳定的目标值，防止主网络"追自己的尾巴" |
| Q2 | C | Replay Buffer 随机采样打破连续经验的时间相关性 |
| Q3 | B | DQN 输出层为每个动作一个 Q 值节点，动作数必须有限 |
| Q4 | B | 3 × 4 = 12 |
| Q5 | B | 7 = 1×4 + 3，所以 (1, 3) |
| Q6 | B | 目标 Q 值由 Target Network 计算，不是主网络 |
| Q7 | C | learning_starts 是预热期，前 N 步随机行动填充 Buffer |
| Q8 | B | VecEnv 自动合并 terminated 和 truncated，返回 (obs, reward, done, info) |
| Q9 | B | log_interval=1 表示每个 episode 向 TensorBoard 写入一次 |
| Q10 | C | Dict 观测需要 MultiInputPolicy |

### 判断题

| 题号 | 答案 | 解释 |
|------|------|------|
| T1 | False | DQN 只支持 Discrete 动作空间，连续动作用 PPO 或 SAC |
| T2 | False | Target Network 每隔 target_update_interval 步才同步一次 |
| T3 | False | Replay Buffer 随机采样，打破时间顺序 |
| T4 | True | ε 通常从 1.0 线性衰减到 0.05 |
| T5 | True | deterministic=True 关闭探索，选择 argmax Q(s, a) |

### 简答题

**S1:**
$$y = r + \gamma \max_{a'} Q_{target}(s', a') = 2 + 0.95 \times 6.0 = 2 + 5.7 = 7.7$$

**S2:**
如果不用 Target Network，主网络同时用于计算目标值和更新自身。每次更新后，目标值也随之变化，导致"追自己的尾巴"——目标不断漂移，训练震荡不收敛。Target Network 通过冻结一个副本作为稳定的"评分标准"，每隔 N 步才同步一次，使训练目标在一段时间内保持不变，从而稳定训练过程。
