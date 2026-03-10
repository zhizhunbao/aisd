# Assignment 1 故事线：Blocks World — 从 Prolog 逻辑到 RL 智能体

> **Source:** `CST8509_Assn1_BlocksWorld.docx` + Week 1-5 slides
> **核心问题：** 如何将一个 Prolog 逻辑模型包装成 Gymnasium 环境，然后用 Q-Learning 和 Stable-Baselines3 训练智能体来学会搭积木？
> **前置知识：** [Week 1 RL 入门](week1_rl_intro_storyline.md) | [Week 2 MDP](week2_mdp_storyline.md) | [Week 3 Gymnasium](week3_gymnasium_storyline.md) | [Week 4 SB3](week4_sb3_storyline.md)

---

## 🗺️ 路线图 (Roadmap)

```
Lab 1: 手写环境          Lab 2: Gymnasium          Assignment 1: 完整系统
┌────────────────┐    ┌────────────────────┐    ┌──────────────────────────┐
│ 手写 CliffEnv   │ →  │ gym.Env 标准接口    │ →  │ Prolog 后端 + Gym 前端    │
│ 手写 Q-table    │    │ 手写 Q-Learning     │    │ Q-Learning + SB3(DQN/PPO)│
│ 无渲染          │    │ PyGame 渲染         │    │ PyGame 渲染              │
│ 4×12 网格       │    │ 12×4 CliffWalking   │    │ 3-block 积木世界         │
└────────────────┘    └────────────────────┘    └──────────────────────────┘
```

---

## 📖 因果叙事 (Causal Narrative)

### 第一章：为什么需要 Blocks World？

**问题起点：** Lab 1 和 Lab 2 的 CliffWalking 是一个简单的网格世界——状态是坐标 (x, y)，动作是上下左右，状态转移是确定性的坐标移动。这太简单了。

**真实世界的问题：**

- 状态不是简单的坐标，而是**组合状态**（如"A 在 B 上，B 在桌子上，C 在 A 上"）
- 动作有**前置条件**（不能搬被压着的积木）
- 状态转移需要**逻辑推理**（Prolog 情境演算）
- 目标状态是**动态的**（每次 episode 随机一个目标）

**Blocks World** 就是这样一个经典 AI 问题：3 块积木 A, B, C，放在 3 个位置（1, 2, 3）上，可以互相叠放。目标是从初始状态移动到目标状态。

> 💡 **为什么用 Prolog？** Prolog 天生适合描述规则和逻辑推理。`blocks_world.pl` 用情境演算（situation calculus）定义了所有合法状态、合法动作和状态转移。Python 负责 RL 框架，Prolog 负责"游戏规则"。

---

### 第二章：系统架构——四个组件如何协作

```
┌─────────────────────────────────────────────────────────────┐
│                    Assignment 1 系统架构                      │
│                                                              │
│  ┌──────────┐     ┌─────────────────────┐     ┌──────────┐  │
│  │  Agent    │     │  Gymnasium Env      │     │  Prolog   │  │
│  │          │     │  (blocks_world.py)   │     │  Server   │  │
│  │ Q-Learn  │──→  │                     │──→  │          │  │
│  │ or SB3   │  ①  │ step(action_int)    │  ②  │ step(A)  │  │
│  │          │     │ → action_dict[int]   │     │ → 状态   │  │
│  │          │  ⑤  │ → query Prolog      │  ③  │ 转移     │  │
│  │          │←──  │ → state_dict[str]    │←──  │          │  │
│  │          │     │ → return obs, rew    │  ④  │          │  │
│  └──────────┘     └─────────────────────┘     └──────────┘  │
│       │                    │                                 │
│       │              ┌─────────┐                             │
│       │              │ PyGame  │                             │
│       └──────────────│ Display │                             │
│         render()     │ screen  │                             │
│                      └─────────┘                             │
└─────────────────────────────────────────────────────────────┘

数据流:
① Agent 发出 action (整数)
② Gym Env 将整数转为 Prolog 动作字符串, 发送查询
③ Prolog 执行状态转移, 返回新状态字符串
④ Gym Env 将状态字符串转为整数 observation
⑤ 返回 (observation, reward, terminated, truncated, info)
```

### 关键映射（作业的核心难点）

| 层级         | Prolog 表示              | Python 表示                               | 转换方式                                  |
| ------------ | ------------------------ | ----------------------------------------- | ----------------------------------------- |
| **状态**     | `'bc2'` (字符串)         | `0, 1, 2, ...` (整数)                     | `states_dict = {'bc2': 0, 'bc3': 1, ...}` |
| **动作**     | `'move(a,b,c)'` (字符串) | `0, 1, 2, ...` (整数)                     | `actions_dict = {0: 'move(a,b,c)', ...}`  |
| **反向查找** | 整数 → 字符串            | `list(keys())[list(values()).index(int)]` | 用于 render 和 target 显示                |

> ⚠️ **这是整个作业最容易出错的地方！** 两个字典方向不同：
>
> - `states_dict`: 字符串 → 整数（查询状态用）
> - `actions_dict`: 整数 → 字符串（执行动作用）

---

### 第三章：BlocksWorld-v0 — 不含目标状态

**为什么先做 v0？** 降低复杂度——先搞定 Prolog 集成和基本 Q-Learning，再添加目标状态。

#### 3.1 状态空间

积木世界有 13 个合法状态（3 块积木 A, B, C 的所有合法排列）。每个状态用 3 位字符串表示：

```
状态编码规则 (三位字符串, 每位表示对应积木的位置):
- 位置 1: A 的位置
- 位置 2: B 的位置
- 位置 3: C 的位置

位置值可以是: 1, 2, 3 (桌面位置) 或 a, b, c (在某块积木上)

示例:
  'bc2' → A 在 B 上(b), B 在 C 上(c), C 在位置 2
  '123' → A 在位置 1, B 在位置 2, C 在位置 3 (全在桌面上)
```

> 💡 **关键理解：** Prolog 的 `state(S)` 谓词会生成所有 13 个合法状态。不合法的组合（如 A 在 B 上且 B 在 A 上）不会被生成。

#### 3.2 动作空间

`action(A)` 查询返回所有可能的 `move(X, From, To)` 动作。不是所有动作在所有状态下都合法——Prolog 的 `step/1` 谓词负责判断。

#### 3.3 奖励设计

| 情况       | 奖励 | 原因               |
| ---------- | ---- | ------------------ |
| 合法移动   | -1   | 鼓励用最少步数完成 |
| 不合法移动 | -10  | 惩罚无效动作       |
| 到达目标   | +100 | 大正奖励引导收敛   |

> ⚠️ **v0 的"目标"是硬编码的**——目标状态是构造器中选定的一个固定状态。Q-Learning 可以在这个固定目标上收敛。

---

### 第四章：Q-Learning 适配

从 Lab 2 迁移 Q-Learning 代码，核心变化：

| Lab 2 (CliffWalking)                       | Assignment 1 (BlocksWorld) |
| ------------------------------------------ | -------------------------- |
| 观测是 `Dict{"agent": ..., "target": ...}` | 观测是**单个整数**         |
| 状态需要计算 `y * xsize + x`               | 状态**直接就是整数**       |
| 4 个动作 (上下左右)                        | **N 个动作** (来自 Prolog) |
| 简单网格环境                               | **Prolog 后端**            |

> 💡 **好消息：** BlocksWorld 的观测直接是整数，比 Lab 2 的字典观测更简单！Q-table 直接用 `Q[state][action]` 索引。

#### 4.1 训练记录与可视化

```python
# 每个 episode 记录:
episode_rewards = []  # 总回报
episode_steps = []    # 总步数

# 绘图要求:
# 1. "Original Hyperparameters" 标题 → 基线截图
# 2. 至少 3 组不同超参数 → 对比截图
# 3. 截图保存到 screenshots/ 文件夹
```

---

### 第五章：BlocksWorld-v1 — 包含目标状态

**问题：** v0 的目标是固定的。真正的 RL 应该能处理不同目标——"我告诉你要搭成什么样，你来学怎么搭"。

**解决方案：** 把目标状态也编码到观测中！

```
v0: 状态 = 3位 (当前状态)     → 13 个状态
v1: 状态 = 6位 (当前+目标)    → 13 × 13 = 169 个状态
```

#### 5.1 Prolog 端修改

```prolog
% 原来的 state/1 改名为 state_helper/1
state_helper(State):- ...  % 生成 3 位状态

% 新的 state/1 生成 6 位状态
state(State):-
  state_helper(Agent),   % 当前状态 (3位)
  state_helper(Target),  % 目标状态 (3位)
  atomics_to_string([Agent,Target],State).  % 拼接为 6 位
```

#### 5.2 Python 端修改

```
reset() 时:
  1. 随机选一个 6 位状态
  2. 取后 3 位作为目标
  3. Prolog reset 后获取当前 3 位状态
  4. 当前3位 + 目标3位 = 6位状态 → 查 states_dict 得整数

step() 时:
  1. Prolog 返回 3 位当前状态
  2. 拼接保存的 3 位目标 → 6 位状态
  3. 查 states_dict 得整数观测
```

---

### 第六章：Stable-Baselines3 集成

有了 Gymnasium 标准接口，SB3 集成非常简单：

```python
from stable_baselines3 import DQN, PPO

# DQN (Deep Q-Network)
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# PPO (Proximal Policy Optimization)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

> ⚠️ **关键：** 使用 `MlpPolicy` 而非 `MultiInputPolicy`！因为 BlocksWorld 的观测是单个 `Discrete` 整数，不是 `Dict`。

> ⚠️ **预期结果：** 在这个小状态空间（13 或 169 个状态），SB3 的 DQN/PPO **不会比手写 Q-Learning 更好**。这是正常的——DQN/PPO 设计用于大规模状态空间。这里只是验证集成正确性。

---

## 📊 对比表 (Comparison Table)

| 维度   | Lab 1 手写   | Lab 2 Gymnasium    | **Assn1 v0**        | **Assn1 v1**      |
| ------ | ------------ | ------------------ | ------------------- | ----------------- |
| 环境   | CliffWalking | CliffWalking       | BlocksWorld         | BlocksWorld       |
| 后端   | Python       | Python             | **Prolog**          | **Prolog**        |
| 状态   | (x,y) 坐标   | Dict{agent,target} | **Discrete 整数**   | **Discrete 整数** |
| 状态数 | 48           | 48                 | **13**              | **169**           |
| 动作   | 4 (上下左右) | 4                  | **N (from Prolog)** | **N**             |
| 目标   | 固定         | 固定               | **固定**            | **随机**          |
| 算法   | Q-Learning   | Q-Learning + SB3   | Q-Learning          | Q-Learning + SB3  |
| 可视化 | 无           | PyGame             | **PyGame**          | **PyGame**        |

---

## ✅ 作业完成检查清单

### Phase 1: 环境构建

- [ ] 从 GridWorld 复制并重命名为 BlocksWorld
- [ ] `pip install -e .` 成功
- [ ] Prolog (`swiplserver`) 集成正常
- [ ] 状态映射字典 (`states_dict`) 构建正确
- [ ] 动作映射字典 (`actions_dict`) 构建正确
- [ ] 观测空间 = `Discrete(len(states_dict))`
- [ ] 动作空间 = `Discrete(len(actions_dict))`
- [ ] Null Agent 随机测试通过
- [ ] PyGame 渲染正常

### Phase 2: Q-Learning

- [ ] 从 Lab 2 复制并适配 Q-Learning 代码
- [ ] 观测处理：直接用整数（无需字典解析）
- [ ] 训练记录：episode_rewards 和 episode_steps
- [ ] "Original Hyperparameters" 基线截图
- [ ] 至少 3 组超参数对比截图
- [ ] 截图保存到 `screenshots/` 文件夹

### Phase 3: BlocksWorld-v1

- [ ] Prolog: `state/1` 生成 6 位状态
- [ ] Python: reset 时随机目标（取后 3 位）
- [ ] Python: step 时拼接 当前+目标 为 6 位状态
- [ ] 状态空间扩大到 169

### Phase 4: Stable-Baselines3

- [ ] `pip install stable-baselines3`
- [ ] DQN agent 可运行
- [ ] PPO agent 可运行
- [ ] 使用 `MlpPolicy`（不是 `MultiInputPolicy`）

### Phase 5: 提交

- [ ] 有意义的 commit messages
- [ ] `screenshots/` 文件夹包含所有截图
- [ ] 虚拟环境未提交
- [ ] 代码有注释（证明理解）

---

## 📚 参考资料

| 资源                  | 链接                                                                                       | 用途                |
| --------------------- | ------------------------------------------------------------------------------------------ | ------------------- |
| Gymnasium 环境创建    | [官方教程](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)  | 环境包结构与注册    |
| Stable-Baselines3     | [SB3 文档](https://stable-baselines3.readthedocs.io/)                                      | DQN/PPO 使用        |
| swiplserver           | [文档](<https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/mqi.html%27)>) | Python-Prolog 通信  |
| Week 3 Gymnasium 笔记 | [week3_gymnasium_storyline.md](week3_gymnasium_storyline.md)                               | 环境创建模式        |
| Week 2 MDP 笔记       | [week2_mdp_storyline.md](week2_mdp_storyline.md)                                           | Q-Learning 数学基础 |
| Lab 2 Gymnasium       | [CST8509_Lab2_Gymnasium.md](../labs/CST8509_Lab2_Gymnasium.md)                             | 环境创建实例        |
