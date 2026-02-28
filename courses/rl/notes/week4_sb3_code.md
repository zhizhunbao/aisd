# Week 4: Stable-Baselines3 — 代码参考 (Code Reference)

> See also: [概念速查](week4_sb3_cheatsheet.md) | [数学公式](week4_sb3_math.md)

---

## 🔧 安装

```bash
pip install stable-baselines3[extra]
# extra 包含 TensorBoard, OpenCV 等
```

---

## 🔧 基本用法（统一 API）

```python
import gymnasium as gym
from stable_baselines3 import DQN, PPO, A2C, SAC

# 1. 创建环境
env = gym.make("CartPole-v1")

# 2. 创建模型
model = PPO("MlpPolicy", env, verbose=1)

# 3. 训练
model.learn(total_timesteps=10000)

# 4. 保存/加载
model.save("ppo_cartpole")
model = PPO.load("ppo_cartpole")

# 5. 预测
obs, info = env.reset()
action, _states = model.predict(obs, deterministic=True)
```

---

## 🔧 算法选择速查

```python
# 离散动作 + 小状态空间
model = DQN("MlpPolicy", env)

# 离散或连续动作（默认首选）
model = PPO("MlpPolicy", env)

# 简单问题，快速训练
model = A2C("MlpPolicy", env)

# 连续动作 + 需要样本效率
model = SAC("MlpPolicy", env)
```

---

## 🔧 Policy 选择

```python
# Discrete / Box 观测 → MlpPolicy
model = DQN("MlpPolicy", env)

# Dict 观测 → MultiInputPolicy
model = DQN("MultiInputPolicy", env)

# 图像观测 Box(H,W,C) → CnnPolicy
model = PPO("CnnPolicy", env)
```

---

## 🔧 向量化环境

```python
from stable_baselines3.common.env_util import make_vec_env

# 创建 16 个并行环境
vec_env = make_vec_env("CartPole-v1", n_envs=16)
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=25000)

# 注意：n_steps 应除以 n_envs
# PPO 默认 n_steps=2048，16 个环境时每个环境只走 128 步
```

---

## 🔧 回调函数

```python
from stable_baselines3.common.callbacks import (
    EvalCallback, CheckpointCallback, CallbackList
)

# 评估回调：定期评估并保存最佳模型
eval_env = gym.make("CartPole-v1")
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./logs/best/",
    log_path="./logs/eval/",
    eval_freq=1000,
    deterministic=True,
)

# 检查点回调：定期保存模型
checkpoint_callback = CheckpointCallback(
    save_freq=5000,
    save_path="./logs/checkpoints/",
)

# 组合多个回调
callbacks = CallbackList([eval_callback, checkpoint_callback])
model.learn(total_timesteps=50000, callback=callbacks)
```

---

## 🔧 超参数配置

```python
import torch.nn as nn

# 网络架构
policy_kwargs = dict(
    net_arch=[dict(vf=[64, 64], pi=[64, 64])],
    activation_fn=nn.Tanh,
    ortho_init=True,
)

# 训练超参数
model = PPO(
    "MlpPolicy", env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.0,
    max_grad_norm=0.5,
    policy_kwargs=policy_kwargs,
    verbose=1,
)
```

---

## 🔧 评估模型

```python
from stable_baselines3.common.evaluation import evaluate_policy

# 评估 10 个 episode
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
```

---

## 🔧 完整训练循环

```python
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy

# 环境
vec_env = make_vec_env("CartPole-v1", n_envs=4)
eval_env = gym.make("CartPole-v1")

# 回调
eval_callback = EvalCallback(
    eval_env, eval_freq=2000,
    best_model_save_path="./best_model/",
    deterministic=True,
)

# 训练
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=50000, callback=eval_callback)

# 评估
mean_reward, std = evaluate_policy(model, eval_env, n_eval_episodes=20)
print(f"Final: {mean_reward:.2f} +/- {std:.2f}")

# 保存
model.save("ppo_cartpole_final")
```

---

## 🔧 自定义环境 + SB3

```python
import my_env  # 注册自定义环境
import gymnasium as gym
from stable_baselines3 import DQN

# Discrete 观测
env = gym.make("my_env/GridWorld-v0")
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Dict 观测
env = gym.make("my_env/BlocksWorld-v0")
model = DQN("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```
