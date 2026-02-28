# Week 5: DQN — 概念速查 (Concept Cheatsheet)

> See also: [数学公式](week5_dqn_math.md) | [代码参考](week5_dqn_code.md)

---

## 📖 核心定义

### DQN (Deep Q-Network, 深度 Q 网络)
- 用**神经网络**替代 Q-Table 来逼近 Q 函数
- 输入：状态 s → 输出：每个离散动作的 Q 值
- 仅支持 **Discrete** 动作空间
- DeepMind 2015 年提出，首次在 Atari 游戏上达到人类水平

### Q-Network (Q 网络 / 策略网络)
- 主神经网络，通常是 MlpPolicy（全连接）或 CnnPolicy（卷积）
- 输入状态 → 输出所有动作的 Q 值向量
- 训练时不断更新权重

### Target Network (目标网络)
- Q-Network 的**缓慢更新副本**
- 用于计算目标 Q 值 y，**不参与梯度更新**
- 每隔 `target_update_interval` 步从主网络复制权重
- 作用：稳定训练，防止"追自己尾巴"

### Replay Buffer (经验回放缓冲区)
- 存储过去的经验元组 (s, a, r, s')
- 训练时从中**随机采样** mini-batch
- 作用：打破连续样本的时间相关性

### Epsilon-Greedy Exploration (ε-贪心探索)
- 以概率 ε 选择随机动作（探索）
- 以概率 1-ε 选择 Q 值最大的动作（利用）
- ε 通常随训练逐渐衰减

### DiscreteActionWrapper (离散动作包装器)
- 将 MultiDiscrete 动作空间展平为 Discrete
- `MultiDiscrete([2, 3])` → `Discrete(6)`
- 使用 `np.prod()` 计算总动作数，`np.unravel_index()` 还原

### Warm-up Period (预热期)
- 训练开始前的 `learning_starts` 步
- Agent 随机行动，只收集经验不学习
- 目的：确保 Replay Buffer 有足够多样的数据

---

## 💡 关键要点

1. **DQN vs Q-Table：** Q-Table 在大状态空间下内存爆炸且无法泛化；DQN 用固定大小的神经网络逼近 Q 值，可处理大/连续状态空间
2. **Target Network 必要性：** 如果用同一网络计算目标和更新，目标会不断漂移 → 训练不稳定
3. **Replay Buffer 必要性：** RL 数据时间相关 → 顺序学习会偏向最近经验 → 随机采样打破相关性
4. **DQN 只支持 Discrete：** 因为输出层是每个动作一个 Q 值节点，动作数必须有限
5. **MultiDiscrete → Discrete：** 用 Wrapper 展平，`np.prod(dims)` 个组合
6. **VecEnv step() 返回 4 值：** `obs, reward, terminated, info`（不是 5 个），VecEnv 自动处理 truncated
7. **log_interval vs check_freq：** `log_interval=1` 控制 TensorBoard 写入频率（每 episode），`check_freq` 控制 Callback 触发频率

---

## ⚠️ 常见陷阱

| 陷阱 | 正确做法 | 来源 |
|------|---------|------|
| 连续动作空间用 DQN | DQN 仅支持 Discrete，连续用 PPO/SAC | Slide 4 |
| MultiDiscrete 环境直接传给 DQN | 必须用 DiscreteActionWrapper 包装 | Slide 4-5 |
| VecEnv step() 解包 5 个值 | VecEnv 返回 4 个值 (obs, reward, done, info) | Slide 12 |
| 不设 learning_starts | 应设置预热期让 Buffer 先积累经验 | Slide 8 |
| 混淆 log_interval 和 check_freq | log_interval = TensorBoard 频率，check_freq = Callback 频率 | Slide 11 |
| 推理时不设 deterministic=True | 推理/评估时应用确定性动作，避免随机探索 | Slide 12 |

---

## 📊 对比表

### Q-Table vs DQN

| 维度 | Q-Table | DQN |
|------|---------|-----|
| Q 值存储 | 表格 (每个 state-action 一格) | 神经网络参数 |
| 状态空间 | 仅小型离散 | 大型离散/连续 |
| 泛化能力 | ❌ 没见过 = 不会 | ✅ 相似状态 → 相似 Q 值 |
| 内存 | O(\|S\| × \|A\|) | O(网络参数数) — 固定 |
| 训练稳定性 | ✅ 保证收敛 | ⚠️ 需要 Target Network + Replay Buffer |

### DQN 四大组件作用

| 组件 | 解决什么问题 | 如果没有会怎样 |
|------|-------------|---------------|
| Q-Network | 替代 Q-Table，处理大状态空间 | 无法处理大环境 |
| Target Network | 稳定训练目标 | 目标漂移，训练震荡不收敛 |
| Replay Buffer | 打破样本相关性 | 学习偏向最近经验，效率低 |
| ε-Greedy | 平衡探索与利用 | 陷入局部最优，不探索新策略 |

### DQN 训练 6 步流程

| 步骤 | 操作 | 关键细节 |
|------|------|---------|
| 1. 交互收集 | Agent ↔ Env → Buffer | 存储 (s, a, r, s') |
| 2. 预热 | 随机动作 × learning_starts 步 | 填充 Buffer |
| 3. 采样 | 从 Buffer 随机抽 mini-batch | batch_size=512 |
| 4. 计算目标 | y = r + γ max Q_target(s',a') | 用 Target Network |
| 5. 更新主网络 | MSE(Q_main(s,a), y) | 反向传播 |
| 6. 同步目标网络 | Q_target ← Q_main | 每 N 步一次 |

### Week 4 SB3 基础 vs Week 5 DQN 实战

| 维度 | Week 4 | Week 5 |
|------|--------|--------|
| 重点 | SB3 统一 API + 算法选择 | DQN 原理 + BlocksWorld 实战 |
| 环境 | 标准 Gym 环境 | 自定义 BlocksWorld + Wrapper |
| 动作空间 | 直接使用 | 需要 DiscreteActionWrapper |
| 监控 | EvalCallback | TensorBoard + ProgressCallback |
| 超参数 | 通用 (net_arch, lr, gamma) | DQN 专属 (learning_starts, batch_size) |
