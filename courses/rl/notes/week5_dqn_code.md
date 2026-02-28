# Week 5: DQN — 代码参考 (Code Reference)

> See also: [概念速查](week5_dqn_cheatsheet.md) | [数学公式](week5_dqn_math.md)

---

## 🔧 Imports

```python
import os
import numpy as np
import gymnasium as gym
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback
```

---

## 🔧 DiscreteActionWrapper — MultiDiscrete → Discrete

```python
class DiscreteActionWrapper(gym.ActionWrapper):
    """将 MultiDiscrete 动作空间展平为 Discrete，适配 DQN"""
    def __init__(self, env):
        super().__init__(env)
        # 获取各维度大小，如 [2, 3]
        self.dims = env.action_space.nvec
        # 总动作数 = 各维度乘积，如 2*3=6
        self.action_space = gym.spaces.Discrete(np.prod(self.dims))

    def action(self, action):
        # 整数 → 多维索引，如 5 → (1, 2)
        return np.unravel_index(action, self.dims)
```

**使用场景：** DQN 只接受 `Discrete` 动作空间，但 BlocksWorld 环境是 `MultiDiscrete`

---

## 🔧 环境创建与包装

```python
def make_custom_env():
    """创建带 Wrapper 的自定义环境"""
    import gymnasium as gym
    # 创建 BlocksWorld 环境：4 个积木，4 个位置
    env = gym.make("blocks_env/BlocksTargetPython-v0",
                    num_blocks=4, num_positions=4)
    # Wrapper 1: 限制每个 episode 最多 200 步
    env = TimeLimit(env, max_episode_steps=200)
    # Wrapper 2: MultiDiscrete → Discrete（DQN 要求）
    env = DiscreteActionWrapper(env)
    return env

# 创建 4 个并行环境（向量化）
env = make_vec_env(make_custom_env, n_envs=4)
```

**Wrapper 顺序：** 原始环境 → TimeLimit → DiscreteActionWrapper → VecEnv

---

## 🔧 目录设置

```python
models_dir = "models/dqn"
logs_dir = "logs/dqn"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)
```

---

## 🔧 DQN 模型创建

```python
model = DQN(
    "MultiInputPolicy",     # Dict 观测 → MultiInputPolicy
    env,                     # 包装后的向量化环境
    learning_starts=100,     # 前 100 步随机探索（预热）
    device="cuda",           # GPU 加速（Mac: "mps", CPU: "cpu", 自动: "auto"）
    batch_size=512,          # 每次更新采样 512 条经验
    verbose=1,               # 打印训练信息
    tensorboard_log=logs_dir # TensorBoard 日志目录
)
```

**Policy 选择：**

| 观测类型 | Policy |
|---------|--------|
| 向量 (Box/Discrete) | `"MlpPolicy"` |
| 字典 (Dict) | `"MultiInputPolicy"` |
| 图像 (Box with shape HxWxC) | `"CnnPolicy"` |

**DQN 关键参数：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `learning_rate` | 1e-4 | 学习率 |
| `buffer_size` | 1,000,000 | Replay Buffer 大小 |
| `learning_starts` | 50,000 | 预热步数 |
| `batch_size` | 32 | Mini-batch 大小 |
| `tau` | 1.0 | Target Network 软更新系数 |
| `gamma` | 0.99 | 折扣因子 |
| `target_update_interval` | 10,000 | Target Network 更新间隔 |
| `exploration_fraction` | 0.1 | ε 衰减占总步数的比例 |
| `exploration_final_eps` | 0.05 | ε 最终值 |

Ref: https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

---

## 🔧 训练与回调

```python
# 自定义进度回调
callback = ProgressCallback(check_freq=10000)

# 训练 1,000,000 步
model.learn(
    total_timesteps=1_000_000,
    log_interval=1,        # TensorBoard: 每 episode 记录
    callback=callback      # 终端: 每 10,000 步报告
)

# 保存模型
model.save(f"{models_dir}/dqn_blocks_world")
```

**日志频率对比：**

| 参数 | 控制什么 | 频率 |
|------|---------|------|
| `log_interval=1` | TensorBoard 写入 | 每 episode |
| `check_freq=10000` | Callback 触发 | 每 10,000 步 |

**自定义 Callback 中记录指标：**
```python
self.logger.record("custom/metric_name", value)
# → 自动出现在 TensorBoard 图表中
```

---

## 🔧 加载与推理

```python
# 加载训练好的模型
model = DQN.load(f"{models_dir}/dqn_blocks_world", env)

# 推理循环
obs = env.reset()
for _ in range(1000):
    # deterministic=True: 不探索，选 Q 值最大的动作
    action, _states = model.predict(obs, deterministic=True)
    # ⚠️ VecEnv 返回 4 个值（不是 5 个）
    obs, reward, terminated, info = env.step(action)
```

**⚠️ 注意：** 标准 Gymnasium `step()` 返回 5 个值 `(obs, reward, terminated, truncated, info)`，但 VecEnv 自动合并 `terminated` 和 `truncated` 为 `done`，只返回 4 个值。

---

## 🔧 TensorBoard 查看训练曲线

```bash
# 启动 TensorBoard
tensorboard --logdir logs/dqn

# 浏览器打开 http://localhost:6006
```

**常用指标：**
- `rollout/ep_rew_mean` — 平均 episode 奖励
- `rollout/ep_len_mean` — 平均 episode 长度
- `train/loss` — 训练损失

---

## 🔧 完整训练流程模板

```python
import os
import numpy as np
import gymnasium as gym
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env

# 1. 定义 Wrapper
class DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.dims = env.action_space.nvec
        self.action_space = gym.spaces.Discrete(np.prod(self.dims))
    def action(self, action):
        return np.unravel_index(action, self.dims)

# 2. 创建环境
def make_custom_env():
    env = gym.make("blocks_env/BlocksTargetPython-v0",
                    num_blocks=4, num_positions=4)
    env = TimeLimit(env, max_episode_steps=200)
    env = DiscreteActionWrapper(env)
    return env

env = make_vec_env(make_custom_env, n_envs=4)

# 3. 创建目录
models_dir, logs_dir = "models/dqn", "logs/dqn"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

# 4. 创建并训练模型
model = DQN("MultiInputPolicy", env,
            learning_starts=100, device="cuda",
            batch_size=512, verbose=1,
            tensorboard_log=logs_dir)
model.learn(total_timesteps=1_000_000, log_interval=1)
model.save(f"{models_dir}/dqn_blocks_world")

# 5. 加载并推理
model = DQN.load(f"{models_dir}/dqn_blocks_world", env)
obs = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
```
