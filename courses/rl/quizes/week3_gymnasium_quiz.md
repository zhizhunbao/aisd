# Week 3: Gymnasium 环境 — 测验 (Quiz)

> 基于 CST8509_03_Gymnasium slides + Lab 2

---

## 选择题 (Multiple Choice)

### Q1. Gymnasium 是哪个库的继任者？
- A) TensorFlow Gym
- B) OpenAI Gym
- C) PyTorch Gym
- D) Stable-Baselines Gym

### Q2. `env.step(action)` 返回几个值？
- A) 3 个：observation, reward, done
- B) 4 个：observation, reward, terminated, info
- C) 5 个：observation, reward, terminated, truncated, info
- D) 2 个：observation, reward

### Q3. 以下哪个是 Gymnasium `reset()` 方法的正确签名？
- A) `reset(self)`
- B) `reset(self, seed=None, options=None)`
- C) `reset(self, random_state=None)`
- D) `reset(self, initial_state=0)`

### Q4. 如果观测空间是 `spaces.Dict({...})`，Stable-Baselines3 应该使用哪个 Policy？
- A) MlpPolicy
- B) CnnPolicy
- C) MultiInputPolicy
- D) DictPolicy

### Q5. `terminated=True` 表示什么？
- A) 超过最大步数
- B) 任务自然结束（到达目标或掉入悬崖）
- C) 环境出错
- D) 智能体放弃

### Q6. 在 Gymnasium 环境的 `reset()` 方法中，为什么要调用 `super().reset(seed=seed)`？
- A) 初始化渲染引擎
- B) 设置 `self.np_random` 以确保随机操作可复现
- C) 注册环境到 Gymnasium
- D) 重置 Q-Table

### Q7. `spaces.Discrete(4)` 表示什么？
- A) 4 维连续空间
- B) 离散集合 {0, 1, 2, 3}
- C) 4×4 的网格
- D) 4 个浮点数

### Q8. 以下哪个 SB3 算法只支持离散动作空间？
- A) PPO
- B) A2C
- C) DQN
- D) SAC

### Q9. 自定义 Gymnasium 环境需要安装为 Python 包，正确的安装命令是？
- A) `pip install gymnasium`
- B) `pip install -e .`
- C) `python setup.py build`
- D) `conda install env`

### Q10. `truncated=True` 在 Q-Learning 中应该如何处理？
- A) 和 `terminated=True` 一样，设 Q(s) = 0
- B) 忽略，不更新 Q-Table
- C) 继续 bootstrap：target = reward + γ·max Q(s')
- D) 重新初始化 Q-Table

---

## 判断题 (True/False)

### T1. Gymnasium 的 `step()` 方法返回 4 个值。
### T2. `from gymnasium import spaces` 是正确的导入方式。
### T3. `spaces.Dict` 观测可以直接用 `MlpPolicy`。
### T4. `terminated` 和 `truncated` 不能同时为 True。
### T5. 环境中的随机操作应该使用 `self.np_random` 而不是 `np.random`。

---

## 简答题 (Short Answer)

### S1. 代码分析
给定以下代码，指出错误并修正：
```python
import gym
env = gym.make("my_env/GridWorld-v0")
obs = env.reset()
action = env.action_space.sample()
obs, reward, done, info = env.step(action)
```

### S2. 空间计算
一个 BlocksWorld 环境有 30 个合法状态和 6 个可能动作。
- Q-Table 的大小是多少？
- 如果用 Dict 观测 `Dict({"agent": Discrete(30), "target": Discrete(30)})`，总观测空间大小是多少？

---

## 答案 (Answers)

### 选择题
| 题号 | 答案 | 解释 |
|------|------|------|
| Q1 | B | Gymnasium 由 Farama Foundation 维护，是 OpenAI Gym 的继任者 |
| Q2 | C | observation, reward, terminated, truncated, info — 5 个值 |
| Q3 | B | `reset(self, seed=None, options=None)` 是 Gymnasium 标准签名 |
| Q4 | C | Dict 观测必须用 MultiInputPolicy |
| Q5 | B | terminated 表示 MDP 的终止状态（任务自然结束）|
| Q6 | B | 设置 self.np_random 确保随机操作可通过 seed 复现 |
| Q7 | B | Discrete(4) = {0, 1, 2, 3} |
| Q8 | C | DQN 只支持离散动作空间，PPO/A2C 支持连续和离散 |
| Q9 | B | `pip install -e .` 以 editable mode 安装本地包 |
| Q10 | C | truncated 不是终止状态，应继续 bootstrap |

### 判断题
| 题号 | 答案 | 解释 |
|------|------|------|
| T1 | False | 返回 5 个值（新增 truncated）|
| T2 | True | 正确的导入方式 |
| T3 | False | Dict 观测必须用 MultiInputPolicy |
| T4 | True | 两者互斥 |
| T5 | True | 确保可复现性 |

### 简答题

**S1 答案：** 3 个错误：
1. `import gym` → `import gymnasium as gym`
2. `obs = env.reset()` → `obs, info = env.reset()`（返回 2 个值）
3. `obs, reward, done, info = env.step(action)` → `obs, reward, terminated, truncated, info = env.step(action)`（返回 5 个值）

**S2 答案：**
- Q-Table 大小：30 × 6 = 180 个 Q 值
- Dict 观测空间大小：30 × 30 = 900 种组合
