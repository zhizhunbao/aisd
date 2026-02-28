# Week 4: Stable-Baselines3 — 故事线 (Storyline)

> 基于 CST8509_04_Stable-Baselines3 slides
> 核心问题：如何用工业级 RL 算法库替代手写 Q-Learning？

---

## 🗺️ 路线图 (Roadmap)

```
Week 2: 手写 Q-Learning        Week 3: Gymnasium 标准化        Week 4: SB3 算法库
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────────┐
│ 手写 Q-table 更新 │ ──升级→ │ 标准 Env 接口     │ ──集成→ │ DQN / PPO / A2C / SAC│
│ 只能处理离散状态  │          │ spaces API        │          │ 向量化环境           │
│ 无法扩展          │          │ 可复用            │          │ 回调 + 超参数调优    │
└──────────────────┘          └──────────────────┘          └──────────────────────┘
```

---

## 📖 因果叙事 (Causal Narrative)

### 问题起点：手写 Q-Learning 的局限

Week 2-3 我们手写了 Q-Learning，它能解决 CliffWalking 和 GridWorld，但有致命局限：

1. **只能处理离散状态** — Q-table 大小 = |S| × |A|，状态空间大了就爆炸
2. **只有一种算法** — Q-Learning 是 off-policy value-based，不适合所有问题
3. **没有训练工具** — 没有日志、回调、模型保存、评估等工程功能
4. **单环境训练** — 每步只从一个环境收集一个转移，效率低

### 解决方案：Stable-Baselines3

SB3 提供了一套**统一接口**的工业级 RL 算法实现：

```python
from stable_baselines3 import DQN, PPO, A2C, SAC

# 所有算法共享相同 API
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("model")
model = DQN.load("model")
action, _ = model.predict(obs)
```

### 核心概念 1：算法选择

SB3 提供多种算法，选择取决于**动作空间类型**和**问题特性**：

| 算法 | 类型 | 动作空间 | 特点 | 适用场景 |
|------|------|---------|------|---------|
| DQN | Off-policy, Value-based | 仅 Discrete | 经典，简单 | 小离散动作空间 |
| PPO | On-policy, Policy Gradient | Discrete + Continuous | 稳定，通用 | 默认首选 |
| A2C | On-policy, Actor-Critic | Discrete + Continuous | 快速，简单 | 简单问题 |
| SAC | Off-policy, Actor-Critic | 仅 Continuous | 样本效率高 | 连续控制 |

⚠️ **关键决策树：**
```
动作空间是离散的？
├── 是 → 状态空间小？
│        ├── 是 → DQN（或手写 Q-Learning）
│        └── 否 → PPO
└── 否（连续）→ 需要样本效率？
                 ├── 是 → SAC
                 └── 否 → PPO
```

### 核心概念 2：Policy 选择

Policy 必须匹配观测空间类型（Week 3 已介绍）：

| 观测空间 | Policy | 内部处理 |
|---------|--------|---------|
| `Discrete(n)` / `Box(shape=(d,))` | `MlpPolicy` | 全连接网络 |
| `Dict({...})` | `MultiInputPolicy` | 每个 key 单独编码后拼接 |
| `Box(shape=(H,W,C))` | `CnnPolicy` | CNN 提取特征 |

### 核心概念 3：向量化环境 (Vectorized Environments)

手写 Q-Learning 每步只从 1 个环境收集 1 个转移。SB3 的向量化环境可以**并行收集 n 个转移**：

```python
from stable_baselines3.common.env_util import make_vec_env

# 16 个环境并行运行
vec_env = make_vec_env("Pendulum-v1", n_envs=16)
model = PPO("MlpPolicy", vec_env).learn(20000)
```

两种实现：
- `DummyVecEnv` — 串行执行（单进程），简单环境默认使用
- `SubprocVecEnv` — 并行执行（多进程），计算密集型环境使用

### 核心概念 4：回调函数 (Callbacks)

回调函数在训练的特定阶段被调用，提供工程级功能：

| Callback | 功能 | 用途 |
|----------|------|------|
| `CheckpointCallback` | 定期保存模型 | 防止训练中断丢失进度 |
| `EvalCallback` | 定期评估并保存最佳模型 | 选择最优模型 |
| `StopTrainingOnRewardThreshold` | 达到目标奖励时停止 | 避免过度训练 |
| `ProgressBarCallback` | 显示进度条 | 监控训练进度 |

### 核心概念 5：超参数调优

SB3 的超参数分为两类：

**算法超参数：**
- `learning_rate` — 学习率
- `gamma` — 折扣因子
- `n_steps` — 每次更新收集的步数
- `gae_lambda` — GAE 参数（bias-variance 权衡）
- `ent_coef` — 熵系数（鼓励探索）
- `max_grad_norm` — 梯度裁剪

**网络架构超参数（`policy_kwargs`）：**
- `net_arch` — 网络层数和宽度
- `activation_fn` — 激活函数
- `ortho_init` — 正交初始化

---

## 📊 对比表 (Comparison Table)

| 维度 | 手写 Q-Learning | SB3 |
|------|----------------|-----|
| 算法 | 只有 Q-Learning | DQN, PPO, A2C, SAC 等 |
| 状态空间 | 仅离散（Q-table） | 离散 + 连续（神经网络） |
| 动作空间 | 仅离散 | 离散 + 连续 |
| 并行训练 | ❌ | ✅ 向量化环境 |
| 模型保存/加载 | 手动 | `save()` / `load()` |
| 训练监控 | 手动 | Callbacks |
| 超参数调优 | 手动 | `policy_kwargs` + `hyperparams` |
| 代码量 | ~50 行 | ~5 行 |

---

## ✅ 考试 Checklist

- [ ] SB3 所有算法共享统一 API：`model = Algorithm(policy, env)`
- [ ] DQN 只支持离散动作空间
- [ ] PPO 是默认首选算法（稳定、通用）
- [ ] SAC 只支持连续动作空间
- [ ] `MlpPolicy` 用于 Discrete/Box 观测，`MultiInputPolicy` 用于 Dict 观测
- [ ] `make_vec_env()` 创建向量化环境，`n_envs` 控制并行数
- [ ] `DummyVecEnv` 串行，`SubprocVecEnv` 并行
- [ ] `EvalCallback` 定期评估并保存最佳模型
- [ ] `policy_kwargs` 配置网络架构，`hyperparams` 配置训练参数
- [ ] `gamma` 是折扣因子，`gae_lambda` 是 GAE 参数

---

## 📚 参考资料

- [SB3 官方文档](https://stable-baselines3.readthedocs.io/)
- [SB3 算法选择指南](https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html)
- [SB3 Hands-on Tutorial](https://github.com/araffin/rl-handson-rlvs21)
- Week 4 Tutorial: `week4_sb3_tutorial.md`
