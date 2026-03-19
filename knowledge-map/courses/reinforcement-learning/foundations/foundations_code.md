---
topic: foundations
dimension: code
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📚 Book: Sutton & Barto, 《Reinforcement Learning: An Introduction》 2nd Ed. Ch.2 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/sutton_barto_rl_intro.pdf"
  - "📖 Docs: Gymnasium — https://gymnasium.farama.org/"
  - "📖 Docs: NumPy — https://numpy.org/doc/stable/"
expiry: 6m
status: current
---

# RL 基础 代码参考

> 📖 Docs: [Gymnasium](https://gymnasium.farama.org/), [NumPy](https://numpy.org/doc/stable/)

## 快速开始

### 最简示例 — 30 秒上手 ε-Greedy 多臂赌博机

```python
import numpy as np

# ============================================================
# 10-Arm Bandit with ε-Greedy / 10 臂赌博机 ε-贪心策略
# ============================================================

k = 10          # 臂数 / Number of arms
steps = 1000    # 交互步数 / Number of steps
epsilon = 0.1   # 探索率 / Exploration rate

# 真实奖励均值 (Agent 不知道) / True reward means (unknown to agent)
q_star = np.random.randn(k)

# Agent 的估计值和计数 / Agent's estimates and counts
Q = np.zeros(k)
N = np.zeros(k)

rewards = []
for t in range(1, steps + 1):
    # ε-Greedy 选动作 / ε-Greedy action selection
    if np.random.rand() < epsilon:
        a = np.random.randint(k)       # 探索 / Explore
    else:
        a = np.argmax(Q)               # 利用 / Exploit

    # 环境返回奖励 / Environment returns reward
    r = np.random.randn() + q_star[a]

    # 增量更新 / Incremental update
    N[a] += 1
    Q[a] += (1 / N[a]) * (r - Q[a])   # Q ← Q + (1/n)[r - Q]

    rewards.append(r)

print(f"平均奖励 / Average reward: {np.mean(rewards):.2f}")
print(f"最优臂 / Best arm: {np.argmax(q_star)}, Agent 选最多的 / Most selected: {np.argmax(N)}")
```

**测试方法：** 直接 `python bandit.py`，观察 Agent 是否收敛到最优臂

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 §2.3-2.4

---

## 完整实现示例

### 示例 1: 多策略对比实验（ε-Greedy vs UCB）

```python
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. 实验配置 / Experiment Configuration
# ============================================================
k = 10              # 臂数 / Number of arms
steps = 1000         # 每轮步数 / Steps per run
runs = 2000          # 独立实验次数 / Number of independent runs

# ============================================================
# 2. Bandit 环境 / Bandit Environment
# ============================================================
class KArmedBandit:
    """k 臂赌博机环境 / k-Armed Bandit Environment"""
    def __init__(self, k=10):
        self.k = k
        self.reset()

    def reset(self):
        # 每次 reset 重新采样真实值 / Resample true values
        self.q_star = np.random.randn(self.k)
        return self

    def step(self, action):
        # 奖励 = 真实值 + 噪声 / Reward = true value + noise
        reward = np.random.randn() + self.q_star[action]
        return reward

    @property
    def optimal_action(self):
        return np.argmax(self.q_star)

# ============================================================
# 3. Agent 实现 / Agent Implementations
# ============================================================
class EpsilonGreedyAgent:
    """ε-Greedy 策略 / ε-Greedy Strategy"""
    def __init__(self, k, epsilon=0.1):
        self.k = k
        self.epsilon = epsilon
        self.Q = np.zeros(k)   # 值估计 / Value estimates
        self.N = np.zeros(k)   # 动作计数 / Action counts

    def select_action(self, t):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.k)   # 探索 / Explore
        return np.argmax(self.Q)                # 利用 / Exploit

    def update(self, action, reward):
        self.N[action] += 1
        self.Q[action] += (1 / self.N[action]) * (reward - self.Q[action])

class UCBAgent:
    """UCB 策略 / UCB Strategy"""
    def __init__(self, k, c=2):
        self.k = k
        self.c = c
        self.Q = np.zeros(k)
        self.N = np.zeros(k)

    def select_action(self, t):
        # 未尝试的动作优先 / Untried actions first
        untried = np.where(self.N == 0)[0]
        if len(untried) > 0:
            return untried[0]
        # UCB 公式 / UCB formula
        ucb_values = self.Q + self.c * np.sqrt(np.log(t) / self.N)
        return np.argmax(ucb_values)

    def update(self, action, reward):
        self.N[action] += 1
        self.Q[action] += (1 / self.N[action]) * (reward - self.Q[action])

# ============================================================
# 4. 实验运行 / Run Experiments
# ============================================================
def run_experiment(AgentClass, bandit_k, steps, runs, **agent_kwargs):
    """运行多次独立实验 / Run multiple independent experiments"""
    avg_rewards = np.zeros(steps)
    optimal_pct = np.zeros(steps)

    for run in range(runs):
        env = KArmedBandit(bandit_k)
        agent = AgentClass(bandit_k, **agent_kwargs)

        for t in range(1, steps + 1):
            action = agent.select_action(t)
            reward = env.step(action)
            agent.update(action, reward)

            avg_rewards[t - 1] += reward
            if action == env.optimal_action:
                optimal_pct[t - 1] += 1

    avg_rewards /= runs
    optimal_pct /= runs
    return avg_rewards, optimal_pct

# 运行三个策略 / Run three strategies
results = {}
for label, Agent, kwargs in [
    ("ε=0 (Greedy)", EpsilonGreedyAgent, {"epsilon": 0}),
    ("ε=0.1", EpsilonGreedyAgent, {"epsilon": 0.1}),
    ("UCB c=2", UCBAgent, {"c": 2}),
]:
    results[label] = run_experiment(Agent, k, steps, runs, **kwargs)

# ============================================================
# 5. 可视化 / Visualization
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

for label, (avg_r, opt_pct) in results.items():
    ax1.plot(avg_r, label=label)
    ax2.plot(opt_pct * 100, label=label)

ax1.set_xlabel("Steps")
ax1.set_ylabel("Average Reward / 平均奖励")
ax1.legend()
ax1.set_title("10-Armed Bandit: Average Reward / 10 臂赌博机：平均奖励")

ax2.set_xlabel("Steps")
ax2.set_ylabel("% Optimal Action / 最优动作选择率")
ax2.legend()
ax2.set_title("10-Armed Bandit: % Optimal Action / 10 臂赌博机：最优动作比例")

plt.tight_layout()
plt.savefig("bandit_comparison.png", dpi=150)
plt.show()
```

> 📚 Book: Sutton & Barto, [《Reinforcement Learning: An Introduction》](../../../textbooks/sutton_barto_rl_intro.pdf), Ch.2 Figure 2.2, 2.4

### 示例 2: Gymnasium 环境入门

```python
import gymnasium as gym

# ============================================================
# 1. 创建环境 / Create Environment
# ============================================================
env = gym.make("CartPole-v1", render_mode="human")

# ============================================================
# 2. 随机策略运行一个 Episode / Run one episode with random policy
# ============================================================
observation, info = env.reset()

total_reward = 0
for step in range(200):
    action = env.action_space.sample()  # 随机选动作 / Random action
    observation, reward, terminated, truncated, info = env.step(action)
    total_reward += reward

    if terminated or truncated:
        break

print(f"Episode 结束 / Episode ended at step {step + 1}")
print(f"总奖励 / Total reward: {total_reward}")
print(f"观察空间 / Observation space: {env.observation_space}")
print(f"动作空间 / Action space: {env.action_space}")

env.close()
```

> 📖 Docs: [Gymnasium Getting Started](https://gymnasium.farama.org/content/basic_usage/)

---

## API 速查

### Gymnasium 环境 API

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `gym.make()` | `id` | — | 创建环境 / Create environment |
| ↳ `render_mode` | `str` | `None` | `"human"` 可视化 / `"rgb_array"` 返回图像 |
| `env.reset()` | — | — | 重置环境，返回 `(obs, info)` |
| ↳ `seed` | `int` | `None` | 随机种子 / Random seed |
| `env.step(action)` | `action` | — | 执行动作，返回 `(obs, reward, terminated, truncated, info)` |
| `env.action_space` | — | — | 动作空间对象 / Action space object |
| `env.observation_space` | — | — | 观察空间对象 / Observation space object |
| `env.action_space.sample()` | — | — | 随机采样动作 / Sample random action |
| `env.close()` | — | — | 关闭环境 / Close environment |

### NumPy 常用函数

| 函数 | 用途 | 说明 |
|------|------|------|
| `np.argmax(a)` | 返回最大值索引 / Index of max | 贪心选择用 |
| `np.random.rand()` | [0,1) 均匀随机数 | 用于 ε-greedy 判断 |
| `np.random.randint(k)` | [0,k) 随机整数 | 随机探索选动作 |
| `np.random.randn()` | 标准正态随机数 | 模拟奖励噪声 |
| `np.zeros(k)` | 全零数组 | 初始化 Q 值和计数 |

---

## 目录结构模板

### 简单结构

```
rl-foundations/
├── bandit.py              ← 多臂赌博机实验
├── utils.py               ← 工具函数
└── results/
    └── bandit_comparison.png
```

### 标准结构

```
rl-foundations/
├── config.py              ← 实验配置（k, steps, runs, ε, c）
├── envs/
│   └── bandit.py          ← Bandit 环境类
├── agents/
│   ├── epsilon_greedy.py  ← ε-Greedy Agent
│   ├── ucb.py             ← UCB Agent
│   └── base.py            ← Agent 基类
├── experiments/
│   └── run_bandit.py      ← 实验运行脚本
├── utils.py               ← 可视化、数据处理
├── results/               ← 实验结果图表
└── requirements.txt
```
