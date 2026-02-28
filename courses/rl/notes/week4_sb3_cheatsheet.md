# Week 4: Stable-Baselines3 — 概念速查 (Concept Cheatsheet)

> See also: [数学公式](week4_sb3_math.md) | [代码参考](week4_sb3_code.md)

---

## 📖 核心定义

### Stable-Baselines3 (SB3)
- 基于 PyTorch 的 RL 算法库，提供统一 API
- 所有算法继承同一基类，共享 `learn()`, `predict()`, `save()`, `load()` 接口

### DQN (Deep Q-Network)
- Off-policy, Value-based 算法
- 用神经网络近似 Q 函数
- 仅支持离散动作空间

### PPO (Proximal Policy Optimization)
- On-policy, Policy Gradient 算法
- 通过裁剪策略更新幅度保证稳定性
- 支持离散和连续动作空间，默认首选

### A2C (Advantage Actor-Critic)
- On-policy, Actor-Critic 算法
- Actor 输出动作概率，Critic 估计状态价值
- 支持离散和连续动作空间

### SAC (Soft Actor-Critic)
- Off-policy, Actor-Critic + 最大熵
- 仅支持连续动作空间

### Vectorized Environment (向量化环境)
- 将多个独立环境堆叠为单一环境
- 每步并行收集 n 个转移，提高数据效率

---

## 💡 关键要点

1. **统一 API：** `model = Algorithm(policy, env)` → `model.learn()` → `model.predict()`
2. **算法选择：** 离散动作 → DQN/PPO，连续动作 → PPO/SAC
3. **PPO 是默认首选** — 稳定、通用、适合大多数问题
4. **Policy 匹配：** Discrete/Box → `MlpPolicy`，Dict → `MultiInputPolicy`，Image → `CnnPolicy`
5. **向量化环境：** `make_vec_env(env_id, n_envs=16)` 并行收集数据

---

## ⚠️ 常见陷阱

| 陷阱 | 正确做法 | 来源 |
|------|---------|------|
| 连续动作空间用 DQN | DQN 仅支持 Discrete，用 PPO 或 SAC | Slide 5 |
| 离散动作空间用 SAC | SAC 仅支持 Continuous，用 DQN 或 PPO | SB3 Docs |
| Dict 观测用 MlpPolicy | Dict 观测必须用 MultiInputPolicy | Slide 4 |
| 忘记 `model.save()` | 训练后保存模型，或用 CheckpointCallback | Slide 9 |
| 向量化环境忘记调整 n_steps | `n_steps` 应除以 `n_envs` 以保持总步数一致 | Slide 8 |
| 不用 EvalCallback | 用 EvalCallback 自动保存最佳模型 | Slide 10 |

---

## 📊 对比表

### SB3 算法对比

| 算法 | 类型 | 动作空间 | On/Off-policy | 样本效率 | 稳定性 |
|------|------|---------|--------------|---------|--------|
| DQN | Value-based | Discrete | Off-policy | 中 | 中 |
| PPO | Policy Gradient | Both | On-policy | 低 | 高 |
| A2C | Actor-Critic | Both | On-policy | 低 | 中 |
| SAC | Actor-Critic + Entropy | Continuous | Off-policy | 高 | 高 |

### On-policy vs Off-policy

| 维度 | On-policy (PPO, A2C) | Off-policy (DQN, SAC) |
|------|---------------------|----------------------|
| 数据复用 | ❌ 每次更新后丢弃 | ✅ Replay Buffer 复用 |
| 样本效率 | 低 | 高 |
| 稳定性 | 高 | 中 |
| 向量化环境 | 非常有用（补偿低效率） | 可选 |

### 手写 Q-Learning vs SB3

| 维度 | 手写 Q-Learning | SB3 |
|------|----------------|-----|
| 代码量 | ~50 行 | ~5 行 |
| 算法 | 仅 Q-Learning | DQN/PPO/A2C/SAC |
| 状态空间 | 仅离散 | 离散 + 连续 |
| 训练工具 | 无 | Callbacks + Logging |
| 并行训练 | ❌ | ✅ VecEnv |
