# Week 5: DQN — 操作教程 (Hands-On Tutorial)

> See also: [幻灯片笔记](week5_dqn_slides.md) | [数学公式](week5_dqn_math.md) | [代码参考](week5_dqn_code.md)

---

## §0 前置知识 (Prerequisites)

在开始本教程前，确保你已理解：

| 概念 | 来源 |
|------|------|
| Q-Learning 更新公式 | [week2_mdp_math.md](week2_mdp_math.md) |
| Q-Table 的工作原理 | [week2_mdp_tutorial.md](week2_mdp_tutorial.md) |
| Gymnasium 环境 / Wrapper | [week3_gymnasium_tutorial.md](week3_gymnasium_tutorial.md) |
| SB3 使用基础（PPO/A2C） | [week4_sb3_tutorial.md](week4_sb3_tutorial.md) |

---

## §1 为什么需要 DQN？Q-Table 的局限

> 📚 Ref: Mnih et al. 2015 "Human-level control through deep reinforcement learning" (Google DeepMind)

### 1.1 Q-Table 的根本问题

Q-Table 是一个二维数组：`Q[state][action]`。它的大小 = **状态数 × 动作数**。

对于 CliffWalking（4×12 格子），Q-Table 只有 48 × 4 = 192 个格子，完全可行。

但对于 BlocksWorld（4 个积木，4 个位置）：

$$|\text{States}| = 4^4 = 256, \quad |\text{Actions}| = 4 \times 4 = 16$$

Q-Table 有 256 × 16 = 4096 个格子，还算可以。

再扩展一点（8 个积木，8 个位置）：

$$|\text{States}| = 8^8 = 16{,}777{,}216, \quad |\text{Actions}| = 64$$

Q-Table 需要 10 亿格子。这就是**维度诅咒 (Curse of Dimensionality)**。

### 1.2 DQN 的解决思路

DQN (Deep Q-Network) 用一个**神经网络**代替 Q-Table：

$$\text{Q-Table: } Q[s][a] \quad \rightarrow \quad \text{DQN: } Q_\theta(s, a)$$

神经网络以状态 $s$ 为输入，对所有动作输出 Q 值。参数 $\theta$ 的数量固定，不随状态空间增大。

> ⚠️ **关键限制：** DQN 只支持**离散动作空间**（`Discrete`）。对于 MultiDiscrete（如 BlocksWorld 中"选哪个积木 + 放哪个位置"），需要用 `DiscreteActionWrapper` 展平。

---

## §2 DQN 的三大创新

> 📚 Ref: Mnih et al. 2015

原始 Q-Learning 如果直接用神经网络会非常不稳定。DQN 引入 3 个关键技术解决这个问题：

### 2.1 Q-Network（主网络）

用神经网络 $Q_\theta(s, a)$ 近似 Q 值。输入状态 $s$，输出每个动作的 Q 值向量。

SB3 DQN 使用 `MultiInputPolicy`（因为观测是 Dict 格式包含当前状态 + 目标状态）。

### 2.2 Target Network（目标网络）

问题：如果用同一个网络同时计算"预测值"和"目标值"，目标一直在动，训练极其不稳定——就像追一个不断移动的标靶。

解决：用一个**延迟更新的副本**（Target Network）来计算目标 Q 值：

$$y = r + \gamma \max_{a'} Q_{target}(s', a')$$

Target Network 每隔 `target_update_interval` 步才同步一次主网络参数。

| 网络 | 更新频率 | 用途 |
|------|---------|------|
| 主网络 $Q_\theta$ | 每次训练步 | 预测当前 Q 值 |
| 目标网络 $Q_{target}$ | 每 N 步同步 | 计算训练目标 |

### 2.3 Replay Buffer（经验回放）

问题：连续采样的数据高度相关（$s_0→s_1→s_2$ 是时间序列），违反了神经网络训练假设的"数据独立同分布"，导致训练不稳定。

解决：将所有历史转移 $(s, a, r, s')$ 存入一个大缓冲区，训练时**随机采样** mini-batch：

$$\text{Buffer: } \{(s_0, a_0, r_0, s'_0), (s_1, a_1, r_1, s'_1), \ldots\}$$

每次训练从中随机取 `batch_size` 个样本，打破时间相关性。

> ⚠️ **Slides 未强调：** `learning_starts=100` 确保缓冲区至少有 100 条随机数据后才开始训练，避免用几乎为空的缓冲区进行无意义更新。

---

## §3 ε-Greedy 探索策略

在 Q-Table 时代我们已经用过 ε-Greedy。DQN 中它的工作原理完全相同，但 SB3 自动管理 ε 衰减：

$$a = \begin{cases} \text{random} & \text{with prob } \varepsilon \\ \arg\max_a Q_\theta(s, a) & \text{with prob } 1 - \varepsilon \end{cases}$$

SB3 DQN 中 ε 的衰减由 `exploration_fraction` 控制：

```python
model = DQN(..., exploration_fraction=0.1, exploration_final_eps=0.05)
```

- `exploration_fraction=0.1`：在前 10% 的总训练步内，ε 从 1.0 线性衰减到 `exploration_final_eps`
- `exploration_final_eps=0.05`：之后保持 ε = 0.05（5% 的时间随机探索）

---

## §4 DiscreteActionWrapper — 适配 DQN

DQN 只支持 `Discrete` 动作空间，但 BlocksWorld 的动作空间是 `MultiDiscrete([4, 4])`（选积木 + 选位置，各 4 种选择）。

### 4.1 展平逻辑

```python
class DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.dims = env.action_space.nvec          # [4, 4]
        self.action_space = gym.spaces.Discrete(np.prod(self.dims))  # Discrete(16)

    def action(self, action):
        # DQN 输出: 整数 0-15
        # 环境期待: (block_idx, position_idx) 元组
        return np.unravel_index(action, self.dims)
```

### 4.2 映射示意

| DQN 输出（整数） | 环境收到（元组） | 含义 |
|----------------|----------------|------|
| 0 | (0, 0) | 积木0 → 位置0 |
| 1 | (0, 1) | 积木0 → 位置1 |
| 5 | (1, 1) | 积木1 → 位置1 |
| 15 | (3, 3) | 积木3 → 位置3 |

`np.unravel_index(5, [4, 4])` = `(1, 1)` — 就像把一个展平的数组索引还原成行列索引。

### 4.3 Wrapper 堆叠顺序

```python
def make_custom_env():
    env = gym.make("blocks_env/BlocksTargetPython-v0", num_blocks=4, num_positions=4)
    env = TimeLimit(env, max_episode_steps=200)    # 先限制步数
    env = DiscreteActionWrapper(env)                # 再展平动作空间
    return env

env = make_vec_env(make_custom_env, n_envs=4)       # 最后向量化
```

> ⚠️ **顺序很重要：** `DiscreteActionWrapper` 必须在 `TimeLimit` 之后，这样 TimeLimit 看到的还是原始 MultiDiscrete 空间，避免混乱。

---

## §5 DQN 超参数配置

```python
model = DQN(
    "MultiInputPolicy",
    env,
    learning_starts=100,
    device="cuda",           # Mac 用 "mps"，通用用 "auto"
    batch_size=512,
    verbose=1,
    tensorboard_log=logs_dir
)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| `"MultiInputPolicy"` | — | Dict 观测（包含 current + target 两个 key） |
| `learning_starts` | 100 | 先随机采集 100 步填充 Replay Buffer，再开始更新 |
| `batch_size` | 512 | 每次梯度更新使用的样本数，越大越稳定但越慢 |
| `device` | `"cuda"` | GPU 加速；CPU 训练设 `"cpu"` |
| `tensorboard_log` | `logs_dir` | TensorBoard 日志目录 |

**SB3 DQN 其他常用参数（默认值）：**

| 参数 | 默认 | 说明 |
|------|------|------|
| `learning_rate` | 1e-4 | 神经网络学习率 |
| `buffer_size` | 1,000,000 | Replay Buffer 最大容量 |
| `gamma` | 0.99 | 折扣因子 |
| `target_update_interval` | 10,000 | Target Network 同步间隔（步数） |
| `exploration_fraction` | 0.1 | ε 线性衰减至终值的时间比例 |

> 📚 Ref: https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

---

## §6 完整训练流程

### 6.1 目录创建

```python
models_dir = "models/dqn"
logs_dir = "logs/dqn"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)
```

### 6.2 训练与保存

```python
callback = ProgressCallback(check_freq=10000)       # 每 10000 步报告
model.learn(
    total_timesteps=1_000_000,
    log_interval=1,                                  # 每 episode 写一次 TensorBoard
    callback=callback
)
model.save(f"{models_dir}/dqn_blocks_world")
```

**理解 `log_interval` vs `check_freq`：**

| 参数 | 触发频率 | 输出目标 |
|------|---------|---------|
| `log_interval=1` | 每个 episode | TensorBoard（高分辨率） |
| `check_freq=10000` | 每 10,000 步 | 终端 / 自定义逻辑（低频报告） |

### 6.3 启动 TensorBoard

```bash
# 在项目根目录运行
tensorboard --logdir logs/dqn
# 浏览器访问 http://localhost:6006
```

关注指标：
- `rollout/ep_rew_mean` — 平均每 episode 总奖励（主要训练信号）
- `train/loss` — 神经网络损失（应下降）
- `rollout/exploration_rate` — ε 值（应从 1.0 下降到 0.05）

### 6.4 运行已训练模型

```python
model = DQN.load(f"{models_dir}/dqn_blocks_world", env)
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, info = env.step(action)
    # VecEnv 返回 4 个值（已自动处理 terminated/truncated）
```

> ⚠️ **VecEnv 注意：** 使用向量化环境时 `step()` 返回 4 个值，而非 Gymnasium 标准的 5 个（`terminated` 和 `truncated` 被合并处理）。

---

## §7 DQN vs Q-Table vs PPO 对比

| 维度 | Q-Table | DQN | PPO |
|------|---------|-----|-----|
| 状态空间 | 小型离散 | 大型/连续 | 任意 |
| 动作空间 | 离散 | 离散 | 离散/连续 |
| On/Off-Policy | Off-policy | Off-policy | On-policy |
| 数据效率 | 高（可复用） | 高（Replay Buffer） | 低（数据一次性） |
| 训练稳定性 | 高 | 中（需调参） | 高 |
| 适用课程场景 | CliffWalking | BlocksWorld | BlocksWorld |

---

## 📋 学习检查清单

- [ ] 能解释为什么 Q-Table 在大状态空间下失效
- [ ] 能说出 DQN 三大创新并解释各自解决了什么问题
- [ ] 知道 Target Network 更新频率由哪个参数控制
- [ ] 能解释 `DiscreteActionWrapper` 的 `action()` 方法里 `np.unravel_index` 做了什么
- [ ] 知道 `learning_starts` 和 `batch_size` 的含义
- [ ] 能区分 `log_interval` 和 `check_freq` 的作用
