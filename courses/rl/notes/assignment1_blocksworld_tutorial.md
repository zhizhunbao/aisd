# Assignment 1 教程：Blocks World — Prolog + Gymnasium + Q-Learning 集成

> 📚 Ref: Assignment 指导文档 + Sutton & Barto §3.1, §6.5 + [Gymnasium 环境创建教程](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/) + David Silver L5 (Model-Free Control)
> **核心问题：** Slides 和教科书从不同角度覆盖了 MDP、Q-Learning、Gymnasium——但都没有展示**如何将 Prolog 逻辑引擎与 Gymnasium 集成**。本教程补充这一集成部分，同时用教科书理论解释每一步设计选择的"为什么"。
> **数学前置：** [Week 2 MDP 数学](week2_mdp_math.md) — Q-Learning 更新公式 | [马尔可夫链与MDP](../../math/probability/markov_chains.md)
> **概念前置：** [Week 3 Gymnasium 教程](week3_gymnasium_tutorial.md) — 环境生命周期与空间定义 | [Week 5 DQN 故事线](week5_dqn_storyline.md) — SB3 集成模式
> **See also:** [故事线](assignment1_blocksworld_storyline.md) | [概念速查](assignment1_blocksworld_cheatsheet.md) | [数学公式](assignment1_blocksworld_math.md) | [代码参考](assignment1_blocksworld_code.md)

---

## §0 前置知识：贯穿例子 — 3-Block 积木世界

> 📚 Ref: Assignment 文档 §Prolog Blocks World + Sutton §3.1 (The Agent-Environment Interface, p.69-74)

在开始之前，我们先用 Sutton 的 Agent-Environment Interface 框架来定义积木世界的 MDP 五元组 $(S, A, P, R, \gamma)$。

### 0.1 MDP 五元组定义

> 📚 Ref: Sutton §3.1 Eq. 3.2-3.4 — Agent-Environment Interface; Week 2 MDP 教程 §5

| MDP 元素     | 符号        | BlocksWorld 中的含义                         | 具体规模                                      |
| ------------ | ----------- | -------------------------------------------- | --------------------------------------------- | ------------------ |
| **状态集**   | $S$         | 所有合法积木排列                             | ~13 个 (v0) / ~169 个 (v1)                    |
| **动作集**   | $A$         | 所有 `move(Block, From, To)`                 | ~N 个 (由 Prolog 枚举)                        |
| **转移概率** | $P(s'       | s,a)$                                        | **确定性的** — 每个动作在每个状态只有一个结果 | $P = 1$ 或 $P = 0$ |
| **奖励函数** | $R(s,a,s')$ | 合法移动 = -1, 不合法 = -10, 达到目标 = +100 | 3 种值                                        |
| **折扣因子** | $\gamma$    | 超参数，通常设 0.99                          | $0 \le \gamma < 1$                            |

> ⚠️ **Slides 未强调的关键点：** BlocksWorld 是**确定性环境**（deterministic）—— 与 Sutton §3.1 讨论的随机环境不同。这意味着 Bellman 方程简化为 $Q(s,a) = r + \gamma \max_{a'} Q(s', a')$，无需期望运算（📚 参见 `q_learning_final.md` 中 Omar Aflak 的推导）。

### 0.2 积木世界状态编码

> 📚 Ref: Assignment 文档 §4c + `blocks_world.pl` 源代码

- **积木：** A, B, C（3 块）
- **桌面位置：** 1, 2, 3（3 个位置）
- **编码规则：** 3 位字符串，每位表示对应积木的位置

| 位置 | 第1位 (A 的位置)                    | 第2位 (B 的位置) | 第3位 (C 的位置) |
| ---- | ----------------------------------- | ---------------- | ---------------- |
| 值域 | `1,2,3` (桌面) 或 `b,c` (在 B/C 上) | `1,2,3` 或 `a,c` | `1,2,3` 或 `a,b` |

```
状态 '123':          状态 'bc2':
  [A]  [B]  [C]        [A]
  ─1── ─2── ─3──       [B]
                        [C]
                   ─1── ─2── ─3──
  A在位置1            A在B上(b)
  B在位置2            B在C上(c)
  C在位置3            C在位置2
```

> ⚠️ **不合法状态不会被生成：** Prolog 的 `state(S)` 谓词只枚举物理上合法的排列（如不允许 A 在 B 上且 B 在 A 上），这正是使用 Prolog 的价值。

### 0.3 Q-Learning 适用条件检验

> 📚 Ref: Quiz 2 Q13 — "Q-learning 的应用条件是什么？" → 答案 D: 需要完整的状态集和动作集

BlocksWorld 满足 Q-Learning 的所有前提条件（📚 Sutton §6.5, p.153）：

| 条件                  | BlocksWorld 是否满足 | 如何满足                            |
| --------------------- | -------------------- | ----------------------------------- |
| ✅ 有限状态集 $S$     | 是                   | Prolog `state(S)` 枚举所有合法状态  |
| ✅ 有限动作集 $A$     | 是                   | Prolog `action(A)` 枚举所有可能动作 |
| ✅ 可以与环境交互     | 是                   | Prolog `step(Action)` 执行动作      |
| ✅ 可以获得奖励信号   | 是                   | Python 端根据执行结果计算奖励       |
| ✅ Episodic（有终止） | 是                   | 当前状态 = 目标状态时终止           |

> 💡 **这也是为什么 Q-Learning 在 BlocksWorld 中效果比 DQN/PPO 好的理论原因：** 状态空间小（13 或 169 个），表格方法可以精确覆盖每个状态，不需要神经网络的泛化能力（📚 Week 5 DQN 故事线 §1.2 "维度灾难"在此不成立）。

---

## §1 Prolog 情境演算与 Python 集成

> 📚 Ref: Assignment 文档 §4b-d + swiplserver 文档
> ⚠️ 这一节是 **Slides 完全未覆盖** 的内容 — Slides 只提到了 Prolog 的概念，没有展示 Python-Prolog 通信的细节。

### 1.1 为什么用 Prolog？

在 Week 3 的 Gymnasium 教程中（📚 `week3_gymnasium_tutorial.md` §3），环境的状态转移逻辑是用 Python 直接编写的（如 `if action == 0: x -= 1`）。但 BlocksWorld 的规则更复杂：

| 维度       | GridWorld (Lab 2) | BlocksWorld (Assn 1)               |
| ---------- | ----------------- | ---------------------------------- |
| 状态转移   | 简单坐标移动      | 需要检查前置条件（积木是否被压住） |
| 合法性检查 | 边界检查          | 复杂逻辑推理                       |
| 状态枚举   | 网格坐标          | 组合排列                           |
| 实现语言   | **Python**        | **Prolog**（更适合逻辑推理）       |

Prolog 天生适合描述规则（what），而不是过程（how）。`blocks_world.pl` 用情境演算定义了"什么情况下可以搬积木"和"搬了之后世界变成什么样"。

### 1.2 Python 调用 Prolog 的模式

```python
from swiplserver import PrologMQI, PrologThread

# 启动 Prolog 服务器 (Assignment §4b)
mqi = PrologMQI()
prolog_thread = mqi.create_thread()

# 加载模型文件 — 注意: 不加句号!
result = prolog_thread.query('[blocks_world]')  # result = True
```

> ⚠️ **Assignment §4b 强调：** 查询字符串**不以句号结尾**。这和 Prolog 交互式终端不同！

### 1.3 Prolog 返回值的 Python 结构

| Prolog 查询                  | Python 返回值                                              | 说明                |
| ---------------------------- | ---------------------------------------------------------- | ------------------- |
| `query('[blocks_world]')`    | `True`                                                     | 加载成功            |
| `query('state(S)')`          | `[{'S': 'bc2'}, {'S': 'bc3'}, ...]`                        | 字典列表            |
| `query('action(A)')`         | `[{'A': {'functor': 'move', 'args': ['a','b','c']}}, ...]` | 复合结构 → 嵌套字典 |
| `query('step(move(a,b,1))')` | `True` 或 `False`                                          | 动作是否可执行      |
| `query('current_state(S)')`  | `[{'S': 'bc2'}]`                                           | 当前状态            |

> ⚠️ **Slides 未强调：** Prolog 复合结构 `move(a,b,c)` 在 Python 中变成 `{'functor': 'move', 'args': ['a','b','c']}`。Assignment §4d 给出的拼接代码正是将它还原为字符串。

---

## §2 状态与动作映射（Assignment 核心难点）

> 📚 Ref: Assignment §4c-f + Week 3 Gymnasium 教程 §2 (Observation Space 设计哲学)

### 2.1 为什么需要两个字典？

Sutton §3.1 (p.69-74) 定义了 Agent-Environment 交互接口：Agent 发出动作整数，Environment 返回状态整数和奖励。但 Prolog 的世界使用字符串。

我们需要**翻译层**：

```
Agent (整数)     ←→    Gymnasium Env (翻译层)    ←→    Prolog (字符串)
action_int  ─→  actions_dict[int] = action_str  ─→  query(f"step({action_str})")
                 states_dict[state_str] = state_int  ←─  query("current_state(S)")
obs_int     ←─                                       ←─  result[0]['S']
```

> 📚 Week 3 Gymnasium 教程 §2.1: Gymnasium 的 `spaces` 模块要求状态和动作用**整数或张量**表示。这就是为什么需要映射。

### 2.2 状态字典构建 (Assignment §4c)

```python
# 从 Prolog 获取所有状态
result = self.prolog_thread.query("state(S)")
# result = [{'S': 'bc2'}, {'S': 'bc3'}, {'S': 'b2c'}, ...]

# 字典推导 + enumerate → 字符串→整数映射
self.states_dict = {s['S']: i for i, s in enumerate(result)}
# {'bc2': 0, 'bc3': 1, 'b2c': 2, ...}
```

> 📚 Quiz 2 Q13 陷阱回应: 这段代码正是在满足 Q-Learning "需要完整状态集" 的前提条件。

### 2.3 动作字典构建 (Assignment §4d)

```python
# 从 Prolog 获取所有动作 — 注意返回的是嵌套字典!
result = self.prolog_thread.query("action(A)")
# result = [{'A': {'functor': 'move', 'args': ['a', 'b', 'c']}}, ...]

# 需要手动拼接 functor + args → 动作字符串
self.actions_dict = {}
for i, A in enumerate(result):
    # A['A']['functor'] = 'move', A['A']['args'] = ['a', 'b', 'c']
    action_string = A['A']['functor']     # 'move'
    first = True
    for arg in A['A']['args']:
        if first:
            first = False
            action_string += '('          # 'move('
        else:
            action_string += ','           # 'move(a,'
        action_string += str(arg)          # 'move(a,b'
    action_string += ')'                  # 'move(a,b,c)'
    self.actions_dict[i] = action_string
# {0: 'move(a,b,c)', 1: 'move(a,b,1)', ...}
```

> ⚠️ **方向不同的设计意图：**
>
> - `states_dict`: **str→int** — 因为 Prolog 返回字符串，我们要转为 Gym 观测整数
> - `actions_dict`: **int→str** — 因为 Gym 给我们动作整数，我们要转为 Prolog 命令字符串

### 2.4 反向查找 (Assignment §4g)

```python
# 给定整数 state，找回字符串 (用于 render)
def state_int_to_str(self, state_int):
    return list(self.states_dict.keys())[
        list(self.states_dict.values()).index(state_int)
    ]
```

---

## §3 Gymnasium 环境的五个核心方法

> 📚 Ref: Week 3 Gymnasium 教程 §3 (环境生命周期) + Assignment §4-8 + Gymnasium 官方文档

这一节的核心贡献是：**将 Week 3 教程的通用模式与 Assignment 的具体要求对照**，展示 BlocksWorld 对每个方法的具体修改。

### 3.1 `__init__` — 初始化 (Assignment §4)

| 步骤          | Week 3 通用模式                            | BlocksWorld 具体实现                                                       |
| ------------- | ------------------------------------------ | -------------------------------------------------------------------------- |
| 1. 初始化后端 | —                                          | `PrologMQI()` + `create_thread()` + `query('[blocks_world]')`              |
| 2. 构建映射   | —                                          | `states_dict` + `actions_dict`                                             |
| 3. 定义空间   | `spaces.Discrete(n)` 或 `spaces.Dict(...)` | `spaces.Discrete(len(states_dict))` + `spaces.Discrete(len(actions_dict))` |
| 4. 初始状态   | `self._agent_location = ...`               | `self.state = 0` (第一个状态)                                              |
| 5. 渲染       | `pygame.display.set_mode(...)`             | `self.display = Display()`                                                 |

> 📚 Week 3 Gymnasium 教程 §2.2 (空间设计权衡):
>
> - 选择 `Discrete` 而非 `Dict` 是因为 **BlocksWorld 的状态已经被编码为单个整数**
> - 这意味着 SB3 应该用 `MlpPolicy` 而非 `MultiInputPolicy` (📚 Quiz W3 Q4: Dict → MultiInputPolicy)

### 3.2 `reset` — 重置环境 (Assignment §5)

> 📚 Ref: Sutton §3.1 — Episode 从 reset 开始; Week 3 Gymnasium 教程 §3.3 — seed 机制

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)  # 📚 Week 3 §3.3: 设置 self.np_random

    # 1. 随机目标状态 (Assignment §5a)
    self.target = self.np_random.integers(0, len(self.states_dict))
    if hasattr(self, 'display'):
        self.display.target = self.state_int_to_str(self.target)

    # 2. Prolog 重置 (Assignment §5b)
    self.prolog_thread.query("reset")

    # 3. 获取当前状态 (Assignment §5c)
    result = self.prolog_thread.query("current_state(S)")
    state_str = result[0]['S']  # Prolog 返回 [{'S': 'xxx'}]
    self.state = self.states_dict[state_str]

    return self.state, {}  # 📚 Week 3 Quiz T1: reset 返回 (obs, info)
```

> ⚠️ **Quiz W3 Q3 对应：** `reset(self, seed=None, options=None)` 是正确签名。

### 3.3 `step` — 执行一步 (Assignment §6)

> 📚 Ref: Sutton §6.5 Eq. 6.8 — Q-Learning 更新规则; Assignment §6a-d

```python
def step(self, action):
    # 1. 整数 → 动作字符串 (Assignment §6a)
    action_str = self.actions_dict[action]

    # 2. Prolog 执行 (Assignment §6a)
    result = self.prolog_thread.query(f"step({action_str})")

    if result:  # 动作合法 (Assignment §6b)
        state_result = self.prolog_thread.query("current_state(S)")
        state_str = state_result[0]['S']
        self.state = self.states_dict[state_str]
        reward = -1  # 📚 Sutton §3.2 (Goals and Rewards, p.75):
                      # 负奖励 → agent 学会用最少步数完成任务
    else:  # 动作不合法 (Assignment §6b)
        reward = -10  # 更大的负奖励 → 惩罚无效动作

    # 3. 终止检查 (Assignment §6c)
    terminated = (self.state == self.target)
    if terminated:
        reward = 100  # 大正奖励引导收敛

    # 4. 渲染
    if self.render_mode == "human":
        self.render()

    # 📚 Quiz W3 Q2: step 返回 5 个值
    # 📚 Quiz W3 Q5: terminated=True 表示任务自然结束
    return self.state, reward, terminated, False, {}
```

> 📚 **奖励设计的理论依据 (Sutton §3.2, p.75 + Quiz 4 Q8):**
>
> - Sutton: "The reward signal is your way of communicating to the agent **what** you want it to achieve, not **how** you want it to achieve it."
> - Quiz 4 Q8 (Antonin Raffin): "Start with a simple reward function... consider sparse rewards and shaped rewards"
> - Assignment 的 -1/-10/+100 奖励设计遵循了这一原则：
>   - -1 per step = sparse penalty → 鼓励最短路径 (📚 Week 2 MDP 故事线 §1.1: 负步数奖励是 CliffWalking 收敛的关键)
>   - -10 for invalid = shaped penalty → 明确告知"这个动作不好"
>   - +100 for goal = sparse reward → "完成任务"是唯一的正向目标

### 3.4 `render` 和 `close` (Assignment §7-8)

```python
def render(self):
    if self.render_mode == "human":
        state_str = self.state_int_to_str(self.state)
        self.display.step(state_str)  # PyGame 渲染

def close(self):
    self.mqi.stop()  # 📚 释放 Prolog 服务器资源 — 不关闭会导致后台线程残留
```

---

## §4 Q-Learning 适配

> 📚 Ref: Sutton §6.5 Eq. 6.8 (Q-Learning 更新) + Week 2 MDP 数学 §Q-Learning 更新 + Lab 2 Q-Learning 代码

### 4.1 对比 Lab 2 的变化

| 维度       | Lab 2 CliffWalking                                    | Assignment 1 BlocksWorld                            |
| ---------- | ----------------------------------------------------- | --------------------------------------------------- |
| 观测类型   | `Dict{"agent": Box, "target": Box}`                   | **`Discrete(n)` — 单个整数**                        |
| 状态计算   | `state = dict['agent'][1] * xsize + dict['agent'][0]` | **`state = obs` (直接用!)**                         |
| 动作数     | `numactions = env.action_space.n` (= 4)               | `numactions = env.action_space.n` (= N from Prolog) |
| 状态数     | `numstates = high_x * high_y`                         | `numstates = env.observation_space.n`               |
| SB3 Policy | `MultiInputPolicy` (因为 Dict)                        | **`MlpPolicy`** (因为 Discrete)                     |

> 📚 Quiz W3 Q4: Dict 观测 → `MultiInputPolicy`; Discrete 观测 → `MlpPolicy`
> 💡 **好消息：** BlocksWorld 的适配比 Lab 2 更简单！观测直接是整数，不需要字典解析。

### 4.2 Q-Learning 核心循环

> 📚 Ref: Sutton §6.5 Eq. 6.8; Week 2 MDP 数学 — Q-Learning 更新；`q_learning_final.md` Code Block 5

```python
import numpy as np

n_states = env.observation_space.n   # 📚 Quiz 2 Q13: 需要完整状态集
n_actions = env.action_space.n       # 📚 Quiz 2 Q13: 需要完整动作集
Q = np.zeros((n_states, n_actions))  # Q-Table: |S| × |A| (Week 3 Quiz S2)

# 超参数 (📚 Quiz 4 Q3: 保存记录所有参数以便复现)
EPISODES = 1000
alpha = 0.1        # 学习率 α (Sutton §6.5: step-size parameter)
gamma = 0.99       # 折扣因子 γ (📚 Quiz 2 Q7: 解决无穷累积回报)
epsilon = 1.0      # 初始探索率 ε
epsilon_decay = 0.995
epsilon_min = 0.01

episode_rewards = []  # 记录训练曲线
episode_steps = []

for episode in range(EPISODES):
    state, _ = env.reset()  # 📚 reset 返回 (obs, info)
    total_reward = 0
    steps = 0
    done = False

    while not done:
        # ε-greedy 策略 (📚 Week 2 MDP 故事线 §2: 平衡探索与利用)
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])  # 📚 Quiz 2 Q12: greedy = argmax Q

        # 执行动作
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # 📚 Sutton §6.5 Eq. 6.8 — Q-Learning 更新:
        # Q(S,A) ← Q(S,A) + α[R + γ max_a' Q(S',a') - Q(S,A)]
        #
        # 符号对照 (📚 Week 2 MDP 数学 — 符号表):
        # | 符号 | 本代码变量 | BlocksWorld 含义 |
        # |------|-----------|-----------------|
        # | S    | state     | 当前积木排列的整数编码 |
        # | A    | action    | move 动作的整数编码 |
        # | R    | reward    | -1/-10/+100 |
        # | S'   | next_state| 执行动作后的新排列 |
        # | α    | alpha     | 学习步长 |
        # | γ    | gamma     | 未来奖励折扣 |
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )

        state = next_state
        total_reward += reward
        steps += 1

    episode_rewards.append(total_reward)
    episode_steps.append(steps)
    epsilon = max(epsilon * epsilon_decay, epsilon_min)
```

> 📚 **手算验证 (参照 Week 2 MDP 数学 — 手算题):**
> 假设 α=0.5, γ=0.9, 当前 Q[s=3, a=2] = 0。Agent 在状态 3 执行动作 2, 得到 reward=-1, 到达 next_state=5, 其中 max Q[5,:] = 0 (初始)。
> TD target = -1 + 0.9 × 0 = -1
> TD error = -1 - 0 = -1
> 新 Q[3,2] = 0 + 0.5 × (-1) = -0.5

---

## §5 从 v0 到 v1：添加目标状态

> 📚 Ref: Assignment §6 "BlocksWorld-v1 with target as part of state" + Sutton §3.1 (状态的充分性)

### 5.1 为什么需要 v1？— 马尔可夫性的要求

> 📚 Ref: Quiz 2 Q3 — "马尔可夫状态的性质是什么？" → E: "后续状态不依赖于先前状态"
> 📚 Ref: Quiz 4 Q6 — "Don't break assumptions, especially the **Markov assumption**"

v0 的问题在于**违反了马尔可夫性**：

- v0 中，状态只包含当前积木排列（3 位）
- 但 Agent 的最优动作还取决于**目标是什么**（同一当前排列，不同目标需要不同策略）
- 目标信息没有编码到状态中 → Agent 看到的状态**不足以决定最优动作** → 违反马尔可夫性

v1 的解决方案：**把目标也编码到状态中**，让状态包含做决策所需的全部信息。

```
v0: 状态 = 当前3位               → 13 个状态   → 违反 Markov
v1: 状态 = 当前3位 + 目标3位      → 169 个状态  → 满足 Markov
```

> ⚠️ **Slides 未解释的设计理论：** 这是 Sutton §3.1 (p.72) 中"Agent-Environment boundary"设计选择的具体体现——目标状态应该是观测的一部分，而不是隐含的。Quiz 4 Q6 (Antonin Raffin) 也强调了这一点。

### 5.2 Prolog 端修改 (Assignment §6 Note 1)

```prolog
% 原来的 state/1 改名为 state_helper/1
state_helper(State):- ...  % 生成 3 位状态

% 新的 state/1 生成 6 位状态 (当前+目标)
state(State):-
    state_helper(Agent),   % 当前状态 (3位)
    state_helper(Target),  % 目标状态 (3位)
    atomics_to_string([Agent,Target], State).  % 拼接为 6 位
```

### 5.3 Python 端修改 (Assignment §6 Note 2)

核心变化在于 `reset()` 和 `step()` 中如何处理 6 位状态：

```python
# reset() 中:
# 1. 随机选目标 (取 6 位状态的后 3 位)
random_idx = self.np_random.integers(0, len(self.states_dict))
random_state_str = list(self.states_dict.keys())[random_idx]
self.target_str = random_state_str[-3:]  # 后 3 位作为目标

# 2. Prolog 返回 3 位当前状态
self.prolog_thread.query("reset")
result = self.prolog_thread.query("current_state(S)")
current_str = result[0]['S']  # 3 位, 如 'bc2'

# 3. 拼接为 6 位状态
full_state_str = current_str + self.target_str  # 如 'bc2123'
self.state = self.states_dict[full_state_str]

# step() 中: 类似, Prolog 返回 3 位当前 + 保存的 3 位目标 → 6 位
```

---

## §6 Stable-Baselines3 集成

> 📚 Ref: Week 4 SB3 故事线 + Week 5 DQN 故事线 §3 + Quiz 4 Q9

### 6.1 算法选择理论 (Quiz 4 Q9)

> 📚 Quiz 4 Q9 (Antonin Raffin): "Consider your actions and whether the algorithm is designed for continuous or discrete actions."

| 算法    | 动作空间要求          | BlocksWorld 适用？ | 原因                     |
| ------- | --------------------- | ------------------ | ------------------------ |
| **DQN** | Discrete only         | ✅                 | 我们用 `spaces.Discrete` |
| **PPO** | Discrete + Continuous | ✅                 | 通用                     |
| **A2C** | Discrete + Continuous | ✅                 | 通用                     |

> 📚 Week 3 Quiz Q8: DQN 只支持 Discrete 动作空间; PPO 支持连续和离散。

### 6.2 Policy 选择 (关键!)

> 📚 Week 3 Gymnasium 教程 §5.2 (Policy 与 Space 的对应关系):
>
> - `Discrete(n)` → `MlpPolicy` (one-hot 编码 → 全连接)
> - `Dict({...})` → `MultiInputPolicy` (Quiz W3 Q4)

```python
# BlocksWorld 用 Discrete 观测 → MlpPolicy
model = DQN("MlpPolicy", env, verbose=1)     # ✅
# model = DQN("MultiInputPolicy", env)        # ❌ 会报错!
```

### 6.3 代码模板

```python
import gymnasium as gym
import blocksworld_env
from stable_baselines3 import DQN, PPO

# DQN (📚 Week 5 DQN 故事线 §2: Q-Network + Target Network + Replay Buffer)
env = gym.make("blocksworld_env/BlocksWorld-v1")
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("dqn_blocks")

# PPO
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_blocks")
```

> 📚 **预期结果 (Week 5 DQN 故事线 §1):** 在 BlocksWorld 的小状态空间中，Q-Learning 的表现通常优于 DQN/PPO。这是正常的 — DQN/PPO 的优势在于大状态空间（如 Atari 游戏），而 BlocksWorld 只有 13/169 个状态，表格方法可以精确覆盖。

---

## 参考索引表

| 教程章节           | 教科书/课程来源                                    | 核心内容                                    | Slides 覆盖？                   |
| ------------------ | -------------------------------------------------- | ------------------------------------------- | ------------------------------- |
| §0 前置知识        | Sutton §3.1 (p.69-74) + Quiz 2 Q13                 | MDP 五元组定义 + Q-Learning 适用条件        | ✅ Week 2 讲了 MDP              |
| §1 Prolog 集成     | Assignment §4b-d + swiplserver 文档                | Python-Prolog 通信模式                      | ❌ **Slides 从未讲过**          |
| §2 状态动作映射    | Assignment §4c-f + Week 3 教程 §2                  | 两个字典的构建、方向与理论依据              | ❌ 细节未覆盖                   |
| §3 五个核心方法    | Sutton §3.1-3.2 + Week 3 教程 §3 + Assignment §4-8 | init/reset/step/render/close + 奖励设计理论 | ⚠️ 通用模式覆盖, 具体实现未覆盖 |
| §4 Q-Learning 适配 | Sutton §6.5 Eq. 6.8 + Week 2 MDP 数学 + Lab 2      | 从 Dict 到 Discrete 的简化 + 手算验证       | ✅ Q-Learning 公式覆盖          |
| §5 v0→v1           | Sutton §3.1 (Markov 性) + Quiz 2 Q3 + Quiz 4 Q6    | 马尔可夫性要求 → 目标编码到状态             | ❌ 设计理论未覆盖               |
| §6 SB3 集成        | Week 4/5 故事线 + Quiz 4 Q9 + Quiz W3 Q4/Q8        | Policy 选择 + 预期效果                      | ✅ SB3 基本使用覆盖             |

### 交叉引用的课程资料

| 资料                               | 引用位置         | 贡献                                      |
| ---------------------------------- | ---------------- | ----------------------------------------- |
| Sutton & Barto §3.1-3.2, §6.5      | §0, §3.3, §4.2   | MDP 定义、奖励设计理论、Q-Learning 公式   |
| `q_learning_final.md` (Omar Aflak) | §0.1             | 确定性环境下 Bellman 方程简化             |
| Quiz 2 (Q3, Q7, Q12, Q13)          | §0.3, §4.2, §5.1 | Q-Learning 条件、Markov 性、贪婪选择      |
| Quiz 4 (Q3, Q6, Q8, Q9)            | §3.3, §5.1, §6.1 | 实验记录、Markov 假设、奖励设计、算法选择 |
| Week 3 Quiz (Q2-Q5, Q8, S2)        | §3.2-3.3, §6.2   | 返回值、Policy 选择、Q-Table 大小         |
| Week 2 MDP 数学                    | §4.2             | Q-Learning 符号表和手算                   |
| Week 2 MDP 故事线 §1-2             | §3.3, §4.2       | 奖励设计影响、ε-greedy                    |
| Week 3 Gymnasium 教程 §2-3         | §2.1, §3.1       | 空间设计哲学、生命周期                    |
| Week 5 DQN 故事线 §1-2             | §0.3, §6.3       | 表格 vs 函数逼近、SB3 组件                |
| David Silver L5                    | 整体             | Model-Free Control 理论背景               |
