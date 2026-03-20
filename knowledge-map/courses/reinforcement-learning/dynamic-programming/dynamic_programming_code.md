---
topic: dynamic-programming
dimension: code
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.4 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: Gymnasium — https://gymnasium.farama.org/"
  - "📖 Docs: NumPy — https://numpy.org/doc/stable/"
expiry: 6m
status: current
---

# 动态规划 代码参考

> 📖 Docs: [Gymnasium](https://gymnasium.farama.org/), [NumPy](https://numpy.org/doc/stable/)

## 快速开始

### 最简示例 — 30 秒上手策略评估

```python
import numpy as np

# ============================================================
# 4x4 GridWorld 策略评估 / Policy Evaluation on 4x4 GridWorld
# ============================================================
# 终止状态: (0,0) 和 (3,3), 奖励: 每步 -1, γ=1
# Terminal: (0,0) & (3,3), Reward: -1 per step, γ=1

grid_size = 4
gamma = 1.0
theta = 1e-4  # 收敛阈值 / Convergence threshold

V = np.zeros((grid_size, grid_size))  # 值函数初始化 / Initialize V
actions = [(-1,0), (1,0), (0,-1), (0,1)]  # 上下左右 / Up Down Left Right

while True:
    delta = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in [(0, 0), (3, 3)]:  # 终止状态 / Terminal
                continue
            v_old = V[i, j]
            v_new = 0
            for di, dj in actions:
                ni, nj = max(0, min(3, i+di)), max(0, min(3, j+dj))
                v_new += 0.25 * (-1 + gamma * V[ni, nj])  # 等概率策略 π=1/4
            V[i, j] = v_new
            delta = max(delta, abs(v_new - v_old))
    if delta < theta:
        break

print("V^π (随机策略 / Random policy):")
print(np.round(V, 1))
```

**测试方法：** 直接 `python gridworld_pe.py`，结果应与 Sutton & Barto Example 4.1 Figure 4.1 一致

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 Example 4.1

---

## 完整实现示例

### 示例 1: 策略迭代 (Policy Iteration)

```python
import numpy as np

# ============================================================
# 1. 环境定义 / GridWorld Environment
# ============================================================
class GridWorld:
    """4x4 GridWorld 环境 / 4x4 GridWorld Environment"""
    def __init__(self, size=4):
        self.size = size
        self.n_states = size * size
        self.n_actions = 4  # 上下左右 / Up Down Left Right
        self.terminal = {0, size * size - 1}  # (0,0) 和 (3,3)
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_transitions(self, state, action):
        """返回 (next_state, reward, prob) / Returns (s', r, p)"""
        if state in self.terminal:
            return [(state, 0.0, 1.0)]
        i, j = state // self.size, state % self.size
        di, dj = self.actions[action]
        ni, nj = max(0, min(self.size-1, i+di)), max(0, min(self.size-1, j+dj))
        next_state = ni * self.size + nj
        return [(next_state, -1.0, 1.0)]  # 确定性转移 / Deterministic

# ============================================================
# 2. 策略评估 / Policy Evaluation
# ============================================================
def policy_evaluation(env, policy, gamma=1.0, theta=1e-8):
    """迭代策略评估 / Iterative Policy Evaluation"""
    V = np.zeros(env.n_states)
    while True:
        delta = 0
        for s in range(env.n_states):
            if s in env.terminal:
                continue
            v_old = V[s]
            v_new = 0
            for a in range(env.n_actions):
                for s_next, r, p in env.get_transitions(s, a):
                    v_new += policy[s, a] * p * (r + gamma * V[s_next])
            V[s] = v_new
            delta = max(delta, abs(v_new - v_old))
        if delta < theta:
            break
    return V

# ============================================================
# 3. 策略改进 / Policy Improvement
# ============================================================
def policy_improvement(env, V, gamma=1.0):
    """贪心策略改进 / Greedy Policy Improvement"""
    policy = np.zeros((env.n_states, env.n_actions))
    for s in range(env.n_states):
        if s in env.terminal:
            policy[s] = 1.0 / env.n_actions  # 终止状态无所谓
            continue
        q_values = np.zeros(env.n_actions)
        for a in range(env.n_actions):
            for s_next, r, p in env.get_transitions(s, a):
                q_values[a] += p * (r + gamma * V[s_next])
        best_actions = np.where(q_values == q_values.max())[0]
        policy[s, best_actions] = 1.0 / len(best_actions)
    return policy

# ============================================================
# 4. 策略迭代主循环 / Policy Iteration Main Loop
# ============================================================
def policy_iteration(env, gamma=1.0):
    """策略迭代算法 / Policy Iteration Algorithm"""
    # 初始化：随机策略 / Initialize: random policy
    policy = np.ones((env.n_states, env.n_actions)) / env.n_actions

    for iteration in range(100):
        # 评估 / Evaluate
        V = policy_evaluation(env, policy, gamma)
        # 改进 / Improve
        new_policy = policy_improvement(env, V, gamma)
        # 检查收敛 / Check convergence
        if np.allclose(policy, new_policy):
            print(f"策略迭代在第 {iteration+1} 轮收敛 / Converged at iteration {iteration+1}")
            break
        policy = new_policy

    return policy, V

# ============================================================
# 5. 运行 / Run
# ============================================================
env = GridWorld(4)
policy, V = policy_iteration(env)

print("\n最优值函数 V* / Optimal Value Function:")
print(np.round(V.reshape(4, 4), 1))

print("\n最优策略 π* / Optimal Policy (↑=0 ↓=1 ←=2 →=3):")
directions = ['↑', '↓', '←', '→']
for i in range(4):
    row = []
    for j in range(4):
        s = i * 4 + j
        if s in env.terminal:
            row.append('■')
        else:
            best = np.argmax(policy[s])
            row.append(directions[best])
    print(' '.join(row))
```

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.3

### 示例 2: 值迭代 (Value Iteration)

```python
import numpy as np

# ============================================================
# 值迭代算法 / Value Iteration Algorithm
# ============================================================
def value_iteration(env, gamma=1.0, theta=1e-8):
    """值迭代 / Value Iteration"""
    V = np.zeros(env.n_states)

    iteration = 0
    while True:
        delta = 0
        for s in range(env.n_states):
            if s in env.terminal:
                continue
            v_old = V[s]
            q_values = np.zeros(env.n_actions)
            for a in range(env.n_actions):
                for s_next, r, p in env.get_transitions(s, a):
                    q_values[a] += p * (r + gamma * V[s_next])
            V[s] = q_values.max()  # max 操作 / max operation
            delta = max(delta, abs(V[s] - v_old))
        iteration += 1
        if delta < theta:
            print(f"值迭代在第 {iteration} 轮收敛 / Converged at iteration {iteration}")
            break

    # 从 V* 提取策略 / Extract policy from V*
    policy = np.zeros((env.n_states, env.n_actions))
    for s in range(env.n_states):
        if s in env.terminal:
            policy[s] = 1.0 / env.n_actions
            continue
        q_values = np.zeros(env.n_actions)
        for a in range(env.n_actions):
            for s_next, r, p in env.get_transitions(s, a):
                q_values[a] += p * (r + gamma * V[s_next])
        best_actions = np.where(q_values == q_values.max())[0]
        policy[s, best_actions] = 1.0 / len(best_actions)

    return policy, V

# 运行 / Run
env = GridWorld(4)  # 复用上面的 GridWorld 类
policy, V = value_iteration(env)

print("\nV* (值迭代 / Value Iteration):")
print(np.round(V.reshape(4, 4), 1))
```

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.4 §4.4

### 示例 3: 策略迭代 vs 值迭代对比实验

```python
import numpy as np
import time

# ============================================================
# 对比实验 / Comparison Experiment
# ============================================================
env = GridWorld(4)

# 策略迭代 / Policy Iteration
t0 = time.time()
pi_policy, pi_V = policy_iteration(env)
t_pi = time.time() - t0

# 值迭代 / Value Iteration
t0 = time.time()
vi_policy, vi_V = value_iteration(env)
t_vi = time.time() - t0

# 对比结果 / Compare results
print(f"\n策略迭代耗时 / PI time: {t_pi:.4f}s")
print(f"值迭代耗时 / VI time: {t_vi:.4f}s")
print(f"值函数一致？/ V match? {np.allclose(pi_V, vi_V)}")
print(f"策略一致？/ Policy match? {np.allclose(pi_policy, vi_policy)}")
```

---

## API 速查

### GridWorld 环境 API（自定义）

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `GridWorld(size)` | `size` | `4` | 创建 size×size 网格 |
| `env.get_transitions(s, a)` | `s`, `a` | — | 返回 `[(s', r, p)]` 转移列表 |
| `env.n_states` | — | — | 状态总数 |
| `env.n_actions` | — | — | 动作总数 |
| `env.terminal` | — | — | 终止状态集合 |

### NumPy 常用函数

| 函数 | 用途 | 说明 |
|------|------|------|
| `np.zeros(n)` | 全零数组 | 初始化值函数 |
| `np.ones((n,m))/m` | 均匀概率矩阵 | 初始化随机策略 |
| `np.argmax(a)` | 最大值索引 | 贪心选择动作 |
| `np.where(cond)` | 满足条件的索引 | 找所有最优动作（处理 tie） |
| `np.allclose(a, b)` | 近似相等判断 | 策略收敛检测 |
| `np.round(a, d)` | 四舍五入到 d 位 | 打印值函数 |

---

## 目录结构模板

### 简单结构

```
rl-dynamic-programming/
├── gridworld_pe.py        ← 策略评估
├── policy_iteration.py    ← 策略迭代
├── value_iteration.py     ← 值迭代
└── results/
    └── gridworld_values.txt
```

### 标准结构

```
rl-dynamic-programming/
├── config.py              ← 实验配置（grid_size, gamma, theta）
├── envs/
│   ├── gridworld.py       ← GridWorld 环境类
│   └── frozen_lake.py     ← FrozenLake 环境
├── algorithms/
│   ├── policy_evaluation.py
│   ├── policy_iteration.py
│   └── value_iteration.py
├── experiments/
│   └── compare_pi_vi.py   ← 策略迭代 vs 值迭代实验
├── utils.py               ← 可视化、值函数打印
├── results/               ← 实验结果
└── requirements.txt
```
