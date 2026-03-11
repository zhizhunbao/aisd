# Week 4: Stable-Baselines3 — 核心概念 (Core Concepts)

> See also: [幻灯片笔记](week4_sb3_slides.md) | [操作教程](week4_sb3_tutorial.md) | [历史背景](week4_sb3_history.md)

---

## 核心术语速查

### Stable-Baselines3（SB3）

一套可靠的强化学习算法实现库，基于 PyTorch，提供：
- 统一接口（所有算法共用 `learn()` / `predict()` / `save()` / `load()`）
- 向量化环境支持
- 回调函数机制

> "可靠"的含义：每个算法有单元测试和性能基准验证，避免了研究代码中常见的 Bug。

---

### SB3 支持的算法

| 算法 | 类型 | 动作空间 | 适用场景 |
|------|------|---------|---------|
| DQN | Off-policy | 离散 | 离散控制（Atari, BlocksWorld） |
| PPO | On-policy | 离散/连续 | 通用，最常用 |
| A2C | On-policy | 离散/连续 | PPO 的简化版 |
| SAC | Off-policy | **连续** | 机器人、物理仿真 |
| TD3 | Off-policy | **连续** | 机器人、物理仿真 |

> ⚠️ **SAC 和 TD3 只支持连续动作空间。** BlocksWorld 是离散的，用 DQN 或 PPO。

---

### On-Policy vs Off-Policy（SB3 选择的关键）

| 维度 | On-Policy（PPO/A2C） | Off-Policy（DQN/SAC） |
|------|--------------------|--------------------|
| 数据使用 | 一次性（更新后丢弃） | 可复用（Replay Buffer） |
| 样本效率 | 低 | 高 |
| 训练稳定性 | 高 | 中（需调参） |
| 并行环境效果 | 显著提升（n_envs） | 有限提升 |

---

### Vectorized Environments（向量化环境）

同时运行 $n$ 个独立环境副本，每步收集 $n$ 个转移：

```python
env = make_vec_env("CartPole-v1", n_envs=4)
```

| VecEnv 类型 | 实现 | 适用场景 |
|------------|------|---------|
| `DummyVecEnv` | 单进程串行 | 简单环境（GridWorld, BlocksWorld） |
| `SubprocVecEnv` | 多进程并行 | 计算密集型（Atari, MuJoCo） |

> SB3 会自动将单个环境包装为 `DummyVecEnv`。

**对 On-policy 的特别意义：** PPO/A2C 每次更新要丢弃旧数据，并行 $n$ 个环境意味着每步收集 $n$ 倍数据，数据效率线性提升。

---

### Callbacks（回调函数）

在训练特定阶段执行自定义代码的机制：

```python
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback

eval_callback = EvalCallback(eval_env, eval_freq=500, best_model_save_path="./logs/")
model.learn(total_timesteps=100000, callback=eval_callback)
```

| 内置 Callback | 用途 |
|--------------|------|
| `EvalCallback` | 定期评估并保存最佳模型 |
| `CheckpointCallback` | 定期保存检查点 |
| `StopTrainingOnRewardThreshold` | 达到目标奖励后停止 |
| 自定义 `BaseCallback` | 任意自定义逻辑 |

---

### 核心 API

```python
# 创建
model = PPO("MlpPolicy", env, verbose=1)
model = DQN("MultiInputPolicy", env, learning_starts=100, batch_size=512)

# 训练
model.learn(total_timesteps=100_000)

# 推理
obs, _ = env.reset()
action, _states = model.predict(obs, deterministic=True)

# 保存/加载
model.save("my_model")
model = PPO.load("my_model", env=env)
```

- `deterministic=True`：推理时关闭随机探索，使用贪婪策略

---

### Policy 类型

| Policy | 适用观测 | 网络 |
|--------|---------|------|
| `MlpPolicy` | 单一向量/Discrete | MLP（多层感知机） |
| `MultiInputPolicy` | Dict 观测 | 分支 MLP，各 key 独立编码后合并 |
| `CnnPolicy` | 图像 (Box with uint8) | CNN |

---

## 概念辨析

### `learn()` 的 `total_timesteps` vs `n_steps`

- `total_timesteps`：总训练步数（整个训练过程）
- `n_steps`（PPO 参数）：每次策略更新前收集的步数

```
总更新次数 ≈ total_timesteps / (n_steps × n_envs)
```

### `log_interval` vs `check_freq`（Callback）

| 参数 | 位置 | 触发频率 | 输出目标 |
|------|------|---------|---------|
| `log_interval=1` | `learn()` 参数 | 每 episode | TensorBoard（高分辨率） |
| `check_freq=10000` | 自定义 Callback | 每 N 步 | 终端/自定义逻辑 |

### `save()` 保存什么？

保存：模型权重 + 超参数 + 策略配置。  
**不保存：** Replay Buffer（DQN）、VecEnv 的归一化统计。  
加载后调用 `set_env()` 可换一个新环境继续训练。

---

## 易错点速查

| 错误 | 正确理解 |
|------|---------|
| SAC 用于离散动作 | SAC 只支持连续动作空间，离散用 DQN/PPO |
| `predict()` 不传 `env` 就加载 | `PPO.load("path")` 不传 env 可以，但之后必须用 `set_env()` 才能训练 |
| VecEnv `step()` 返回 5 个值 | VecEnv 的 `step()` 返回 4 个（`terminated`/`truncated` 被合并处理） |
| `n_envs=4` 会让训练快 4 倍 | 数据收集快 4 倍，但更新计算量不变；实际加速比 < 4 |
| 每次 `learn()` 都从头开始 | 可以多次调用 `learn()`，会在上次基础上继续训练 |
