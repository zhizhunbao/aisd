# Lab 1 CliffWalking — 教程 (Tutorial)

> 📚 Ref: Sutton & Barto §6.1 (TD Learning), §6.5 (Q-Learning), p.132 (CliffWalking Example)
> **核心问题：** Lab 指导文档展示了"做什么"，但没解释 Q-Learning 每一行代码背后的"为什么"。本教程补充理论-代码对应关系，并解释 CliffWalking 作为 Q-Learning 经典示例的设计意图。
> **数学前置：** [lab1_cliffwalking_math.md](lab1_cliffwalking_math.md) — Q-Learning 公式与手算
> **概念前置：** [week2_mdp_tutorial.md](week2_mdp_tutorial.md) — MDP 五元组 | [week2_mdp_math.md](week2_mdp_math.md) — 折扣回报
> **See also:** [故事线](lab1_cliffwalking_storyline.md) | [代码速查](lab1_cliffwalking_code.md)

---

## §0 前置知识：CliffWalking 问题定义

> 📚 Sutton §6.5, p.132 — "The Cliff Walking Example"

### 0.1 MDP 五元组

| MDP 元素 | 符号 | CliffWalking 中的含义 |
|---------|------|----------------------|
| **状态集** | $S$ | 4×12 网格上的 48 个位置（整数 0–47） |
| **动作集** | $A$ | \{左(0), 右(1), 上(2), 下(3)\} |
| **转移概率** | $P(s'\|s,a)$ | **确定性的**——$P=1$（边界处保持原位） |
| **奖励函数** | $R$ | 普通=-1, 悬崖=-100, (目标结束) |
| **折扣因子** | $\gamma$ | 通常接近 1（如 0.99） |

### 0.2 网格布局

```
         列: 0    1    2    3   ...   10   11
行 0:   [ ]  [ ]  [ ]  [ ]  ...  [ ]  [ ]
行 1:   [ ]  [ ]  [ ]  [ ]  ...  [ ]  [ ]
行 2:   [ ]  [ ]  [ ]  [ ]  ...  [ ]  [ ]
行 3:  [S]  [X]  [X]  [X]  ...  [X]  [G]
             ←———————— 悬崖（X）—————————→
S = 起点 (0,3), G = 目标 (11,3), X = 悬崖
```

> ⚠️ **Sutton 的设计意图：** CliffWalking 专门用来演示 Q-Learning 与 SARSA 的行为差异。Q-Learning 学到最优路径（沿崖边走），而 SARSA 学到更保守的路径（绕远路避开悬崖边缘）。这一差异来自 **off-policy vs on-policy** 的本质区别。

---

## §1 Hybrid Activity 1 教程解析

> 📚 Ref: [Omar Aflak 的 Medium 教程](https://medium.com/data-science/math-of-q-learning-python-code-5dcbdc49b6f6) + Lab 1 指导文档

### 1.1 原始 GridWorld 结构

Hybrid Activity 1 提供了一个简单的 3×4 GridWorld 和对应的 Q-Learning 实现。Lab 1 的任务是：**理解并修改这个代码来解决 CliffWalking 问题。**

核心文件：

| 文件 | 职责 |
|------|------|
| `medium_qlearning_env.py` → 重命名为 `<id>_lab2_environment.py` | 环境类，定义网格、奖励、转移 |
| `medium_qlearning_rl.py` → 重命名为 `<id>_lab2_qlearning_agent.py` | Q-Learning 主循环 |

> ⚠️ **常见错误：** 重命名后忘记同步更新 `import` 语句。在 `qlearning_agent.py` 的顶部找到 `import medium_qlearning_env`，改为 `import <id>_lab2_environment`。

### 1.2 Bellman 方程的代码体现

Omar Aflak 教程的核心是 Bellman 方程：

$$Q(s,a) \leftarrow Q(s,a) + \alpha \left[ R + \gamma \max_{a'} Q(s', a') - Q(s,a) \right]$$

在代码中体现为：

```python
# Q-Learning 更新（对应 Bellman 公式）
td_target = reward + gamma * np.max(Q[next_state])   # R + γ max Q(s',a')
td_error  = td_target - Q[state, action]              # TD 误差
Q[state, action] += alpha * td_error                  # Q ← Q + α * TD误差
```

---

## §2 修改环境类：从 GridWorld 到 CliffWalking

### 2.1 修改网格形状

**原始 GridWorld：** 任意小网格（如 3×4）
**CliffWalking：** 固定 4 行 × 12 列

```python
# 修改 __init__：
self.height, self.width = 4, 12   # 4行×12列（原来可能是3×4）
self.x, self.y = 0, 3             # 起点：左下角
self.end_x, self.end_y = 11, 3    # 目标：右下角
```

> 📚 Sutton p.132: "The cliff is a region of cells along the bottom of the grid"

### 2.2 添加 cliff 属性

```python
# 在 __init__ 中添加：
self.cliff = False  # 记录上一步是否掉入悬崖（布尔值）
```

**为什么需要 cliff 属性？**

- 用于渲染时显示悬崖标记（X）
- 用于演示时讨论智能体行为

### 2.3 修改 step() 方法

**关键逻辑：悬崖检测**

```python
def step(self, action: int) -> tuple[int, int, bool]:
    # 1. 执行移动（带边界检查）
    if action == 0: self.x = max(0, self.x - 1)              # 左
    if action == 1: self.x = min(self.width - 1, self.x + 1) # 右
    if action == 2: self.y = max(0, self.y - 1)              # 上
    if action == 3: self.y = min(self.height - 1, self.y + 1)# 下

    # 2. 悬崖检测（底行 x 在 1-10 之间）
    if self.y == 3 and 1 <= self.x <= 10:
        self.cliff = True
        reward = -100
        self.x, self.y = 0, 3   # 返回起点
        done = False             # ← 重要！掉崖后 episode 不结束
    else:
        self.cliff = False
        reward = -1
        done = (self.x == self.end_x and self.y == self.end_y)

    next_state = self.y * self.width + self.x
    return next_state, reward, done
```

> ⚠️ **关键设计：** 掉崖后 `done=False`，agent 返回起点继续训练。这意味着一个 episode 可以包含多次掉崖。这与 Gymnasium 的 `terminated=True` 不同（见 Lab 2）。

### 2.4 修改 reward() 方法（如果独立）

如果原始代码有独立的 `reward()` 方法：

```python
def reward(self) -> int:
    if self.cliff:
        return -100  # 悬崖惩罚
    elif self.x == self.end_x and self.y == self.end_y:
        return 0     # 到达目标（已结束，不再执行 step）
    else:
        return -1    # 普通移动
```

### 2.5 修改 render() 方法

```python
def render(self):
    for y in range(self.height):
        row = ""
        for x in range(self.width):
            if x == self.x and y == self.y:
                row += "A"               # Agent 当前位置
            elif x == self.end_x and y == self.end_y:
                row += "G"               # 目标
            elif y == 3 and 1 <= x <= 10:
                row += "X"               # 悬崖（之前可能是其他字符）
            else:
                row += "."
        print(row)
    print()
```

---

## §3 Q-Learning 主循环解析

```python
# 初始化 Q-Table
Q = np.zeros((env.states(), env.actions()))  # shape: (48, 4)

for episode in range(num_episodes):          # "epoch" → 改为 "episode"
    state, _, done = env.reset()
    total_return = 0                          # 累计回报（Return）

    while not done:
        # ε-greedy 策略选择动作
        if np.random.random() < epsilon:
            action = np.random.randint(env.actions())   # 探索
        else:
            action = np.argmax(Q[state])                # 利用

        # 执行动作
        next_state, reward, done = env.step(action)
        total_return += reward

        # Q-Learning 更新
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )

        state = next_state

    if done:
        print(f"Episode {episode}: steps={..., return={total_return}")
```

> 📚 **"epoch" → "episode" 的重要性：** Lab 指导文档特别要求改变这个术语。Epoch 来自监督学习（遍历一次数据集），而 Episode 是 RL 专用术语（从初始状态到终止状态的完整交互序列，对应 Quiz 2 Q6 的定义）。

---

## §4 alpha=1 的演示讨论

Lab 要求在超参数部分添加 `alpha=1` 并在演示时讨论：

| alpha 值 | 效果 | 何时用？ |
|----------|------|---------|
| $\alpha = 1$ | 每次直接用新目标覆盖旧 Q 值——最激进 | 确定性环境（如 CliffWalking） |
| $\alpha = 0.1$ | 缓慢学习，保留过去经验 | 随机环境，稳定收敛 |
| $\alpha \to 0$ | 永不学习 | — |

**为什么确定性环境可以用 alpha=1？**

在确定性环境中，$P(s'\|s,a) = 1$，每次从相同的 $(s,a)$ 出发总会到达同一个 $s'$。因此 TD target 不带噪声，$\alpha=1$ 相当于直接设置 Q 值而非平均，收敛更快。

> 📚 Sutton §6.5 p.133: "Q-Learning with $\alpha=1$" 在确定性环境中等价于值迭代（Value Iteration）。

---

## §5 提交与演示准备

**提交内容：**

```
zip 文件包含：
├── <id>_lab2_qlearning_agent.py   (主 Q-Learning 循环)
├── <id>_lab2_environment.py       (原始 GridWorld 环境，已改名)
└── <id>_lab2_cliff_env.py         (CliffWalking 修改版)
```

**演示讨论要点：**

1. 解释 `cliff` 属性的作用
2. 解释为什么掉崖后 `done=False`（episode 不结束）
3. 讨论 `alpha=1` 在确定性环境中的意义
4. 展示渲染输出中 X 标记悬崖的效果
5. 说明 `epoch` → `episode` 的术语意义
