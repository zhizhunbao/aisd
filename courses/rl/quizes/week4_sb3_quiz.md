# Week 4: Stable-Baselines3 — 测验 (Quiz)

> 基于 CST8509_04_Stable-Baselines3 slides + Demo

---

## 选择题 (Multiple Choice)

### Q1. Stable-Baselines3 基于哪个深度学习框架？
- A) TensorFlow
- B) JAX
- C) PyTorch
- D) Keras

### Q2. 以下哪个 SB3 算法仅支持离散动作空间？
- A) PPO
- B) A2C
- C) SAC
- D) DQN

### Q3. 以下哪个 SB3 算法仅支持连续动作空间？
- A) DQN
- B) PPO
- C) SAC
- D) A2C

### Q4. 如果观测空间是 `spaces.Dict({...})`，应该使用哪个 Policy？
- A) MlpPolicy
- B) CnnPolicy
- C) MultiInputPolicy
- D) DictPolicy

### Q5. `make_vec_env("CartPole-v1", n_envs=8)` 的作用是什么？
- A) 创建 8 个串行环境
- B) 创建 8 个并行环境，包装在 VecEnv 中
- C) 将环境的观测空间扩大 8 倍
- D) 训练 8 个不同的模型

### Q6. PPO 属于哪种类型的算法？
- A) Off-policy, Value-based
- B) On-policy, Policy Gradient
- C) Off-policy, Actor-Critic
- D) Model-based

### Q7. SB3 中 `evaluate_policy(model, env, n_eval_episodes=10)` 返回什么？
- A) 单个奖励值
- B) (mean_reward, std_reward) 元组
- C) 所有 episode 的奖励列表
- D) 最佳 episode 的奖励

### Q8. 以下哪个不是 PPO 的超参数？
- A) learning_rate
- B) gamma
- C) buffer_size
- D) clip_range

### Q9. On-policy 和 Off-policy 算法的主要区别是什么？
- A) On-policy 更快
- B) Off-policy 可以复用历史数据（Replay Buffer）
- C) On-policy 只能用于连续动作
- D) Off-policy 不需要神经网络

### Q10. 使用向量化环境时，PPO 默认 `n_steps=2048`，如果 `n_envs=8`，每个环境实际走多少步？
- A) 2048
- B) 256
- C) 16384
- D) 1024

---

## 判断题 (True/False)

### T1. SB3 中所有算法共享相同的 API（learn, predict, save, load）。
### T2. DQN 可以用于连续动作空间。
### T3. `MlpPolicy` 适用于 `Box(4,)` 类型的观测空间。
### T4. SAC 是 On-policy 算法。
### T5. `EvalCallback` 可以在训练过程中自动保存最佳模型。

---

## 简答题 (Short Answer)

### S1. 代码分析
给定以下代码，指出问题并修正：
```python
from stable_baselines3 import SAC
import gymnasium as gym

env = gym.make("CartPole-v1")  # Discrete action space
model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

### S2. 算法选择
你需要训练一个机器人手臂控制任务（连续动作空间），且训练样本获取成本很高。你会选择哪个 SB3 算法？为什么？

---

## 答案 (Answers)

### 选择题
| 题号 | 答案 | 解释 |
|------|------|------|
| Q1 | C | SB3 基于 PyTorch 构建 |
| Q2 | D | DQN 仅支持 Discrete 动作空间 |
| Q3 | C | SAC 仅支持 Continuous 动作空间 |
| Q4 | C | Dict 观测必须用 MultiInputPolicy |
| Q5 | B | 创建 8 个并行环境，包装在 DummyVecEnv 中 |
| Q6 | B | PPO 是 On-policy, Policy Gradient 算法 |
| Q7 | B | 返回 (mean_reward, std_reward) 元组 |
| Q8 | C | buffer_size 是 DQN/SAC 的参数（Replay Buffer），PPO 是 On-policy 不用 buffer |
| Q9 | B | Off-policy 算法使用 Replay Buffer 复用历史经验数据 |
| Q10 | B | 2048 / 8 = 256，每个环境走 256 步 |

### 判断题
| 题号 | 答案 | 解释 |
|------|------|------|
| T1 | True | SB3 的核心设计就是统一 API |
| T2 | False | DQN 仅支持 Discrete 动作空间 |
| T3 | True | Box(d,) 是平坦向量，适合 MlpPolicy |
| T4 | False | SAC 是 Off-policy 算法 |
| T5 | True | EvalCallback 定期评估并保存 best_model |

### 简答题

**S1 答案：**
CartPole-v1 的动作空间是 `Discrete(2)`，而 SAC 仅支持连续动作空间。应改用 DQN 或 PPO：
```python
from stable_baselines3 import PPO  # 或 DQN
model = PPO("MlpPolicy", env, verbose=1)
```

**S2 答案：**
选择 SAC（Soft Actor-Critic）。原因：
1. SAC 支持连续动作空间（机器人手臂控制需要）
2. SAC 是 Off-policy 算法，使用 Replay Buffer 复用历史数据，样本效率高
3. 训练样本获取成本高时，样本效率是关键考量
