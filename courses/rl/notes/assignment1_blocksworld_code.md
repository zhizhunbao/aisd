# Assignment 1 Blocks World — 代码参考 (Code)

> **See also:** [概念速查](assignment1_blocksworld_cheatsheet.md) | [数学公式](assignment1_blocksworld_math.md)
> **Source:** Assignment 文档 + Lab 2 代码 + Week 3/4/5 code notes

---

## 🔧 环境包结构 (Assignment 目录结构)

```
<userid>_blocksworld_env/
├── blocksworld_env/
│   ├── __init__.py          # 注册 BlocksWorld-v0 和 v1
│   ├── envs/
│   │   ├── __init__.py      # 导出环境类
│   │   ├── blocks_world.py  # v0: 3位状态, 无目标
│   │   └── blocks_world_target.py  # v1: 6位状态, 含目标
│   └── wrappers/            # 可选包装器
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## 🔧 环境注册 (`__init__.py`)

```python
# blocksworld_env/__init__.py
from gymnasium.envs.registration import register

register(
    id="blocksworld_env/BlocksWorld-v0",
    entry_point="blocksworld_env.envs:BlocksWorldEnv",
)

register(
    id="blocksworld_env/BlocksWorld-v1",
    entry_point="blocksworld_env.envs:BlocksWorldTargetEnv",
)
```

```python
# blocksworld_env/envs/__init__.py
from blocksworld_env.envs.blocks_world import BlocksWorldEnv
from blocksworld_env.envs.blocks_world_target import BlocksWorldTargetEnv
```

---

## 🔧 Prolog 集成模式

```python
# 启动
from swiplserver import PrologMQI, PrologThread
self.mqi = PrologMQI()
self.prolog_thread = self.mqi.create_thread()
self.prolog_thread.query('[blocks_world]')  # 不加句号!

# 查询状态
result = self.prolog_thread.query("state(S)")
# → [{'S': 'bc2'}, {'S': 'bc3'}, ...]

# 查询动作
result = self.prolog_thread.query("action(A)")
# → [{'A': {'functor': 'move', 'args': ['a', 'b', 'c']}}, ...]

# 执行动作
result = self.prolog_thread.query(f"step({action_str})")
# → True (合法) / False (不合法)

# 查询当前状态
result = self.prolog_thread.query("current_state(S)")
# → [{'S': 'bc2'}]
state_str = result[0]['S']

# 重置
self.prolog_thread.query("reset")

# 关闭
self.mqi.stop()
```

---

## 🔧 状态/动作映射

```python
# 状态映射: 字符串 → 整数
self.states_dict = {s['S']: i for i, s in enumerate(result)}

# 动作映射: 整数 → 字符串 (Assignment §4d 给的代码)
self.actions_dict = {}
for i, A in enumerate(result):
    action_string = A['A']['functor']
    first = True
    for arg in A['A']['args']:
        if first:
            first = False
            action_string += '('
        else:
            action_string += ','
        action_string += str(arg)
    action_string += ')'
    self.actions_dict[i] = action_string

# 反向查找: 整数 → 字符串
state_str = list(self.states_dict.keys())[
    list(self.states_dict.values()).index(state_int)
]
```

---

## 🔧 空间定义

```python
from gymnasium import spaces

# v0 和 v1 相同模式, 只是 states_dict 大小不同
self.observation_space = spaces.Discrete(len(self.states_dict))
self.action_space = spaces.Discrete(len(self.actions_dict))
```

---

## 🔧 Null Agent 测试

```python
import gymnasium as gym
import blocksworld_env

env = gym.make("blocksworld_env/BlocksWorld-v0", render_mode="human")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

---

## 🔧 Q-Learning Agent (从 Lab 2 适配)

```python
import gymnasium as gym
import blocksworld_env
import numpy as np
import matplotlib.pyplot as plt

env = gym.make("blocksworld_env/BlocksWorld-v0")

# 空间大小
n_states = env.observation_space.n
n_actions = env.action_space.n
Q = np.zeros((n_states, n_actions))

# 超参数
EPISODES = 1000
alpha = 0.1
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01

episode_rewards = []
episode_steps = []

for episode in range(EPISODES):
    state, _ = env.reset()
    total_reward = 0
    steps = 0
    done = False

    while not done:
        # ε-greedy
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state])

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # Q-Learning 更新 (Sutton Eq. 6.8)
        Q[state, action] += alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )

        state = next_state
        total_reward += reward
        steps += 1

    episode_rewards.append(total_reward)
    episode_steps.append(steps)
    epsilon = max(epsilon * epsilon_decay, epsilon_min)

env.close()
```

---

## 🔧 绘图模板 (Assignment 截图要求)

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(episode_rewards)
axes[0].set_xlabel('Episode')
axes[0].set_ylabel('Total Reward')
axes[0].set_title('Episode Rewards')

axes[1].plot(episode_steps)
axes[1].set_xlabel('Episode')
axes[1].set_ylabel('Steps')
axes[1].set_title('Steps per Episode')

plt.suptitle(f'Q-Learning: α={alpha}, γ={gamma}, ε-decay={epsilon_decay}')
plt.tight_layout()
plt.savefig('screenshots/qlearning_original_hyperparams.png', dpi=150)
plt.show()
```

---

## 🔧 SB3 DQN Agent

```python
import gymnasium as gym
import blocksworld_env
from stable_baselines3 import DQN

env = gym.make("blocksworld_env/BlocksWorld-v1")
model = DQN("MlpPolicy", env, verbose=1)  # MlpPolicy, 不是 MultiInputPolicy!
model.learn(total_timesteps=10000)
model.save("dqn_blocks")

# 测试
model = DQN.load("dqn_blocks")
obs, info = env.reset()
for _ in range(200):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
env.close()
```

---

## 🔧 SB3 PPO Agent

```python
from stable_baselines3 import PPO

env = gym.make("blocksworld_env/BlocksWorld-v1")
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("ppo_blocks")
```

---

## 🔧 v1 Prolog 修改

```prolog
% blocks_world_target.pl — 6位状态

state_helper(State):- ...  % 原来的 state/1 改名

state(State):-
    state_helper(Agent),
    state_helper(Target),
    atomics_to_string([Agent,Target], State).
```

---

## 🔧 v1 Python: reset 中的 6 位状态拼接

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    # 随机选目标 (取后3位)
    random_idx = self.np_random.integers(0, len(self.states_dict))
    random_key = list(self.states_dict.keys())[random_idx]
    self.target_str = random_key[-3:]

    if hasattr(self, 'display'):
        self.display.target = self.target_str

    # Prolog 重置 + 获取当前3位状态
    self.prolog_thread.query("reset")
    result = self.prolog_thread.query("current_state(S)")
    current_str = result[0]['S']

    # 拼接6位 → 查字典
    full_str = current_str + self.target_str
    self.state = self.states_dict[full_str]

    return self.state, {}
```

---

## 🔧 安装命令

```bash
# 在包含 pyproject.toml 的目录下
pip install -e .

# 安装 SB3
pip install stable-baselines3

# 安装 Prolog
sudo apt install swi-prolog
```

---

## 🔧 Git 提交规范

```bash
git commit -m "feat: implement BlocksWorld-v0 environment"
git commit -m "feat: add Q-Learning agent with training plots"
git commit -m "feat: extend to BlocksWorld-v1 with target state"
git commit -m "feat: integrate Stable-Baselines3 DQN/PPO"
git commit -m "docs: add hyperparameter experiment screenshots"
```
