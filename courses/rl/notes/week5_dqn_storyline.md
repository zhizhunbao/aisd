# Week 5 故事线：从 Q-Table 到 DQN——当状态空间爆炸时怎么办？

> **Source:** `CST8509_05_DQN_Stable-Baselines3.pptx`
> **核心主题：** 当环境状态空间太大、Q-Table 装不下时，用神经网络替代表格来逼近 Q 值
> **故事线：** 从"查字典"到"训练大脑"——Q-Learning 的深度学习进化之路

---

## 🎬 序幕：我们要解决什么问题？

回顾 Week 2，我们学了 Q-Learning：用一张 Q-Table 记录每个 (state, action) 对的价值，然后查表选最优动作。

这在小环境（如 4×4 CliffWalking）中完美运行。但现在课程进入了 BlocksWorld 环境——积木数量从 2×4 到 10×10，状态空间呈指数增长：

| 环境规模 | 状态数量级 | Q-Table 可行？ |
|----------|-----------|---------------|
| 2×4      | ~几百     | ✅ 轻松       |
| 4×4      | ~几万     | ⚠️ 勉强       |
| 5×5      | ~几十万   | ❌ 内存爆炸   |
| 10×10    | ~天文数字 | ❌ 完全不可能 |

> 💡 **核心矛盾：** Q-Table 需要为每个状态分配一行，状态空间一大就存不下、学不完。

---

## 📚 第一章：Q-Learning 的瓶颈——表格方法的极限

### 1.1 Q-Table 回顾

Week 2 的 Q-Learning 核心公式：

$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$

这个公式的前提是：**Q(s,a) 存在一张表里**，每个 (s, a) 对有一个格子。

### 1.2 ❌ 表格方法的致命问题——维度灾难

当状态是连续的（如机器人关节角度）或组合爆炸的（如 10×10 积木排列），Q-Table 面临：

- **存储问题：** 表格太大，内存装不下
- **泛化问题：** 没见过的状态，Q 值为 0（没学过 = 不会）
- **收敛问题：** 需要访问每个状态足够多次才能收敛，状态太多根本访问不完

> 🔑 **故事转折点：** Q-Table 在大状态空间下彻底失效 → 我们需要一种方法，能从**有限的经验**中**泛化**到未见过的状态 → **函数逼近**登场！

---

## 🧠 第二章：DQN——用神经网络替代 Q-Table

### 2.1 核心思想：从"查表"到"预测"

DQN (Deep Q-Network) 的核心思想非常简单：

| 维度 | Q-Table | DQN |
|------|---------|-----|
| Q 值存储 | 一张大表格 | 一个神经网络 |
| 查询方式 | 查表 `Q[s][a]` | 前向传播 `Q_θ(s) → [q₁, q₂, ...]` |
| 泛化能力 | ❌ 没见过 = 不会 | ✅ 相似状态 → 相似 Q 值 |
| 内存需求 | O(|S| × |A|) | O(网络参数数) — 固定大小 |

> 💡 **类比：** Q-Table 像一本字典——每个词都要单独查。DQN 像一个"大脑"——见过足够多的例子后，能对新情况做出合理判断。

### 2.2 DQN 的四大组件

DQN 不只是"把 Q-Table 换成神经网络"这么简单。直接用神经网络替代会导致训练不稳定。DeepMind 在 2015 年的论文中引入了三个关键技巧：

| 组件 | 作用 | 解决什么问题 |
|------|------|-------------|
| **Q-Network** | 输入状态 → 输出所有动作的 Q 值 | 替代 Q-Table |
| **Target Network** | Q-Network 的缓慢更新副本 | 防止"追自己尾巴"（训练不稳定） |
| **Replay Buffer** | 存储过去的经验 (s, a, r, s') | 打破样本相关性 |
| **ε-Greedy** | 以概率 ε 随机探索 | 平衡探索与利用 |

### 2.3 DQN 训练 6 步流程

```
┌──────────────────────────────────────────────────────┐
│  DQN 训练循环                                         │
│                                                      │
│  Step 1: 交互收集                                     │
│    Agent ↔ Environment → (s, a, r, s') → Buffer      │
│                                                      │
│  Step 2: 预热 (learning_starts 步随机动作)             │
│    填充 Buffer，确保有足够多样的经验                    │
│                                                      │
│  Step 3: 采样                                         │
│    从 Buffer 随机抽取 mini-batch                       │
│                                                      │
│  Step 4: 计算目标                                     │
│    y = r + γ max_a' Q_target(s', a')                  │
│    ↑ 用 Target Network（不是主网络！）                 │
│                                                      │
│  Step 5: 更新主网络                                    │
│    Loss = MSE(Q_main(s,a), y)                         │
│    反向传播更新 Q_main 的权重                          │
│                                                      │
│  Step 6: 同步目标网络                                  │
│    每 target_update_interval 步：                      │
│    Q_target ← Q_main                                  │
└──────────────────────────────────────────────────────┘
```

### 2.4 为什么需要 Target Network？

如果用同一个网络既计算目标又更新自己：

- 目标 y 随着网络更新而变化 → "追自己的尾巴"
- 类似于考试时答案和评分标准同时在变 → 永远考不完

Target Network 的解决方案：**冻结一个副本**作为"评分标准"，每隔一段时间才同步一次。

### 2.5 为什么需要 Replay Buffer？

RL 的数据有一个特殊问题：**连续的经验高度相关**。

- 如果按时间顺序学习：Agent 在走廊里走了 100 步 → 网络只学会了"走廊"
- Replay Buffer 打乱顺序：随机抽取不同时间、不同位置的经验 → 学习更均衡

> 💡 **类比：** 像洗牌一样——不洗牌的话，连续抽到的牌都是同一花色。

---

## 🏰 第三章：实战——在 BlocksWorld 上训练 DQN

### 3.1 ⚠️ DQN 的限制：只支持 Discrete 动作空间

DQN 输出的是每个动作的 Q 值，所以动作数量必须是有限的（Discrete）。

但 BlocksWorld 环境使用 **MultiDiscrete** 动作空间（如 `MultiDiscrete([2, 3])` = 两个维度，分别有 2 和 3 个选择）。

> 🔑 **问题：** DQN 要求 Discrete，环境给的是 MultiDiscrete → 怎么办？

### 3.2 解决方案：DiscreteActionWrapper

核心思路：**把多维动作展平为一维**。

`MultiDiscrete([2, 3])` → 总共 2×3 = 6 种组合 → `Discrete(6)`

```
MultiDiscrete([2, 3]):        Discrete(6):
  (0,0) (0,1) (0,2)    →     0, 1, 2, 3, 4, 5
  (1,0) (1,1) (1,2)
```

- `np.prod(dims)` 计算总动作数
- `np.unravel_index(action, dims)` 将整数还原为多维索引

### 3.3 完整环境配置流程

```
原始环境 (MultiDiscrete)
    ↓ TimeLimit(max_episode_steps=200)
包装1: 限制每个 episode 最多 200 步
    ↓ DiscreteActionWrapper
包装2: MultiDiscrete → Discrete
    ↓ make_vec_env(n_envs=4)
向量化: 4 个并行环境加速训练
    ↓
最终环境 → 传给 DQN
```

---

## 📏 第四章：训练配置与监控

### 4.1 关键超参数

| 参数 | 值 | 含义 |
|------|-----|------|
| `policy` | `"MultiInputPolicy"` | 支持字典观测（current + target） |
| `learning_starts` | `100` | 前 100 步随机探索，填充 Buffer |
| `device` | `"cuda"` | 使用 GPU 加速 |
| `batch_size` | `512` | 每次更新采样 512 条经验 |
| `total_timesteps` | `1,000,000` | 总训练步数 |

### 4.2 TensorBoard 日志系统

SB3 的日志系统有两层粒度：

| 层级 | 频率 | 内容 |
|------|------|------|
| TensorBoard | 每 episode | `rollout/ep_rew_mean`, `train/loss` 等 |
| 终端/Callback | 每 10,000 步 | 自定义进度报告 |

- `log_interval=1` → TensorBoard 每 episode 记录一次（高分辨率）
- `check_freq=10000` → ProgressCallback 每 10,000 步触发一次（低频终端输出）
- 自定义指标通过 `self.logger.record("key", value)` 自动出现在 TensorBoard

### 4.3 模型保存与加载

```python
# 保存
model.save(f"{models_dir}/dqn_blocks_world")

# 加载并推理
model = DQN.load(f"{models_dir}/dqn_blocks_world", env)
action, _states = model.predict(obs, deterministic=True)
```

- `deterministic=True`：推理时使用确定性动作（不探索）
- VecEnv 的 `step()` 返回 4 个值（自动处理 terminated/truncated）

---

## 🗺️ 全局回顾：从 Q-Table 到 DQN 的技术演进

```
┌─────────────────────────────────────────────────────┐
│              技术演进路线图                            │
│                                                     │
│  Week 2: Q-Learning (Q-Table)                       │
│    ✅ 简单直观，保证收敛                              │
│    ❌ 状态空间大时内存爆炸、无法泛化                   │
│    │                                                │
│    ▼                                                │
│  Week 5: DQN (Deep Q-Network)                       │
│    ✅ 用神经网络逼近 Q 值，可处理大状态空间            │
│    ✅ Target Network + Replay Buffer 稳定训练         │
│    ❌ 只支持 Discrete 动作空间                        │
│    ❌ 可能高估 Q 值（overestimation）                 │
│    │                                                │
│    ▼                                                │
│  下一站：Double DQN / Dueling DQN / ...              │
│    解决 Q 值高估问题                                  │
└─────────────────────────────────────────────────────┘
```

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| Q-Table → DQN | 用神经网络替代表格，解决大状态空间下的存储和泛化问题 |
| 裸神经网络 → +Target Network | 冻结目标网络，防止训练目标不断漂移导致不稳定 |
| 顺序学习 → +Replay Buffer | 打乱经验顺序，打破样本相关性，提高学习效率 |
| MultiDiscrete → DiscreteActionWrapper | 展平多维动作空间，适配 DQN 的 Discrete 要求 |

---

## 🎓 考试/复习重点检查清单

- [ ] 能解释为什么 Q-Table 在大状态空间下失效
- [ ] 能说出 DQN 的四大组件及各自作用（Q-Network, Target Network, Replay Buffer, ε-Greedy）
- [ ] 能写出 DQN 的目标 Q 值公式：$y = r + \gamma \max_{a'} Q_{target}(s', a')$
- [ ] 能解释 Target Network 为什么能稳定训练（"追自己尾巴"问题）
- [ ] 能解释 Replay Buffer 为什么能提高学习效率（打破样本相关性）
- [ ] 能描述 DQN 训练的 6 步流程
- [ ] 能解释 DiscreteActionWrapper 的工作原理（MultiDiscrete → Discrete 展平）
- [ ] 能解释 `np.unravel_index()` 的作用
- [ ] 知道 DQN 的关键超参数：`learning_starts`, `batch_size`, `device`, `tensorboard_log`
- [ ] 能区分 `log_interval`（TensorBoard 频率）和 `check_freq`（Callback 频率）
- [ ] 知道 `deterministic=True` 在推理时的作用
- [ ] 知道 VecEnv 的 `step()` 返回 4 个值（不是 5 个）
