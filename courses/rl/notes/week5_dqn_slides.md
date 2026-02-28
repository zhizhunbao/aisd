# Week 5: DQN 与 Stable-Baselines3 (DQN with Stable-Baselines3)

> Source: `CST8509_05_DQN_Stable-Baselines3.pptx`
> Total slides: 12
> Instructor: Todd Kelley (Lectures) / Ali Mohamed Ali (Labs) | Winter 2026

---

## 1. DQN 简介与动机 (DQN Introduction & Motivation)

![Page 1](week5_dqn_slides_pages/page_001.png)

- Stable-Baselines3 DQN — Stable-Baselines3 中的 DQN 算法

![Page 2](week5_dqn_slides_pages/page_002.png)

- **Blocks with Target 2x4, 4x4, 5x5, …. 10x10** — 积木目标环境（不同规模）

- **Which Algorithm?** — **应该使用哪个算法？**
  - DQN working better than PPO in early experiments — DQN 在早期实验中比 PPO 表现更好
  - DQN is a popular choice for this type of problem (e.g. Rubik's Cube) — DQN 是此类问题的热门选择（如魔方）

- **Basics of DQN** — **DQN 基础概念：**
  - **Q-Network (Policy):** A neural network (often MlpPolicy or CnnPolicy) that takes the state as input and outputs Q-values for each possible discrete action — **Q 网络（策略）：** 一个神经网络（通常是 MlpPolicy 或 CnnPolicy），以状态为输入，输出每个离散动作的 Q 值
  - **Target Network:** A slowly updated, identical copy of the Q-network used to compute the target Q-value, which helps stabilize training by preventing the network from chasing its own tail — **目标网络：** Q 网络的一个缓慢更新的副本，用于计算目标 Q 值，通过防止网络"追自己的尾巴"来稳定训练
  - **Replay Buffer:** Stores past experiences to break the correlation between consecutive samples, allowing the agent to learn from a diverse, random batch of past data — **经验回放缓冲区：** 存储过去的经验，打破连续样本之间的相关性，让智能体从多样化的随机批次中学习
  - **Epsilon-Greedy Exploration:** The agent balances exploration and exploitation by choosing a random action with probability (epsilon) or the best-predicted action — **ε-贪心探索：** 智能体以概率 ε 选择随机动作（探索），否则选择最优预测动作（利用），平衡探索与利用

> **📝 Notes:**
>
> _(To be added)_

---

## 2. DQN 训练流程 (DQN Training Process)

![Page 3](week5_dqn_slides_pages/page_003.png)

- **DQN 训练 6 步流程：**

1. **Interaction & Collection:** The agent interacts with the environment, taking actions and storing transitions in the ReplayBuffer — **交互与收集：** 智能体与环境交互，执行动作并将转移存储到经验回放缓冲区
2. **Warm-up:** For a specified number of steps (`learning_starts`), the agent acts randomly to fill the buffer before learning begins — **预热：** 在指定步数（`learning_starts`）内，智能体随机行动以填充缓冲区
3. **Sampling:** After the warm-up, the algorithm samples a random mini-batch of experiences from the replay buffer — **采样：** 预热后，算法从回放缓冲区中随机采样一个 mini-batch
4. **Target Calculation:** The target network computes the target Q-value: $y = r + \gamma \max_{a'} Q(s', a')$ — **目标计算：** 目标网络计算目标 Q 值
5. **Loss Calculation & Update:** The main Q-network computes the current Q(s,a) and updates its weights by minimizing the Mean Squared Error between Q(s,a) and y — **损失计算与更新：** 主 Q 网络计算当前 Q(s,a)，通过最小化 Q(s,a) 与 y 之间的均方误差来更新权重
6. **Target Network Update:** Every `target_update_interval` steps, the main network weights are copied to the target network — **目标网络更新：** 每隔 `target_update_interval` 步，将主网络权重复制到目标网络

> **📝 Notes:**
>
> _(To be added)_

---

## 3. 动作空间适配 (Action Space Adaptation)

### 3.1 DQN 的离散动作限制 (DQN Discrete Action Constraint)

![Page 4](week5_dqn_slides_pages/page_004.png)

- **DQN action space must be Discrete** — **DQN 的动作空间必须是 Discrete（离散的）**
- The Python-based environment, blocks with target, uses **MultiDiscrete** actions — 基于 Python 的积木目标环境使用 **MultiDiscrete** 动作空间
- **Q: How can we train DQN on this environment?** — **问：如何在此环境上训练 DQN？**
- **A: wrap it!** — **答：用 Wrapper 包装它！**

### 3.2 DiscreteActionWrapper 实现 (DiscreteActionWrapper Implementation)

![Page 5](week5_dqn_slides_pages/page_005.png)

```python
class DiscreteActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        # Assume env.action_space is MultiDiscrete([2, 3])
        # 假设环境动作空间是 MultiDiscrete([2, 3])
        self.dims = env.action_space.nvec
        self.action_space = gym.spaces.Discrete(np.prod(self.dims))

    def action(self, action):
        # Convert single integer back to tuple for the inner env
        # 将单个整数转换回元组给内部环境
        return np.unravel_index(action, self.dims)
```

- 核心思路：将 MultiDiscrete 动作空间展平为单个 Discrete 空间
- `np.prod(self.dims)` 计算所有维度的乘积作为新的离散动作数
- `np.unravel_index()` 将单个整数索引还原为多维索引

> **📝 Notes:**
>
> _(To be added)_

---

## 4. 环境配置与包装 (Environment Setup & Wrapping)

![Page 6](week5_dqn_slides_pages/page_006.png)

- **Applying wrappers to an environment** — **将 Wrapper 应用到环境**

```python
# Define a function that applies all your wrappers
# 定义一个应用所有 Wrapper 的函数
def make_custom_env():
    import gymnasium as gym
    # using 4 blocks and 4 positions right now
    # 当前使用 4 个积木和 4 个位置
    env = gym.make("blocks_env/BlocksTargetPython-v0",
                    num_blocks=4, num_positions=4)
    # Manually pass kwargs to each wrapper here
    # 手动将参数传递给每个 Wrapper
    env = TimeLimit(env, max_episode_steps=200)
    env = DiscreteActionWrapper(env)
    return env

# Use the function as the env_id, and create 4 parallel copies
# 使用该函数作为 env_id，创建 4 个并行副本
env = make_vec_env(make_custom_env, n_envs=4)
```

- `TimeLimit` wrapper 限制每个 episode 最多 200 步
- `DiscreteActionWrapper` 将 MultiDiscrete 转为 Discrete（DQN 要求）
- `make_vec_env` 创建向量化环境，4 个并行副本加速训练

> **📝 Notes:**
>
> _(To be added)_

---

## 5. 模型存储与日志 (Model Storage & Logging)

![Page 7](week5_dqn_slides_pages/page_007.png)

- **Logs and trained model storage** — **日志和训练模型存储**

```python
# Create directories for models and logs
# 创建模型和日志目录
models_dir = "models/dqn"
logs_dir = "logs/dqn"
os.makedirs(models_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)
```

- 模型保存到 `models/dqn/` 目录
- TensorBoard 日志保存到 `logs/dqn/` 目录

> **📝 Notes:**
>
> _(To be added)_

---

## 6. DQN 超参数配置 (DQN Hyperparameters)

![Page 8](week5_dqn_slides_pages/page_008.png)

- **DQN hyperparameters** — **DQN 超参数配置**

```python
model = DQN("MultiInputPolicy", env, learning_starts=100, device="cuda",
            batch_size=512, verbose=1, tensorboard_log=logs_dir)
```

Ref: https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

- **`MultiInputPolicy`**: observations are a dictionary with current and target — 观测值是包含当前状态和目标状态的字典
- **`env`**: our wrapped environment — 我们包装后的环境
- **`learning_starts=100`**: number of random actions before learning starts — 学习开始前的随机动作数
- **`device="cuda"`**: use CUDA GPU (would be `"mps"` on a Mac, or `"auto"`, or `"cpu"`) — 使用 CUDA GPU（Mac 上用 `"mps"`，或 `"auto"`、`"cpu"`）
- **`batch_size=512`**: batch size for update — 更新时的批量大小
- **`tensorboard_log=logs_dir`**: log training progress to the specified directory for viewing with TensorBoard — 将训练进度记录到指定目录，用 TensorBoard 查看

> **📝 Notes:**
>
> _(To be added)_

---

## 7. TensorBoard 可视化 (TensorBoard Visualization)

![Page 9](week5_dqn_slides_pages/page_009.png)

- **TensorBoard** can plot information stored in the appropriate format — **TensorBoard** 可以绘制以适当格式存储的信息
- Can view graphs of training progress, comparing several runs — 可以查看训练进度图表，比较多次运行

> **📝 Notes:**
>
> _(To be added)_

---

## 8. 模型训练与回调 (Model Training & Callbacks)

### 8.1 训练模型 (Training the Model)

![Page 10](week5_dqn_slides_pages/page_010.png)

- **Training the model** — **训练模型**

```python
# Train for 1,000,000 timesteps with progress reports every 10,000 steps
# 训练 1,000,000 步，每 10,000 步报告一次进度
callback = ProgressCallback(check_freq=10000)
model.learn(total_timesteps=1000000, log_interval=1, callback=callback)
model.save(f"{models_dir}/dqn_blocks_world")
```

### 8.2 日志机制详解 (Logging Mechanism Details)

![Page 11](week5_dqn_slides_pages/page_011.png)

- **Logging** — **日志机制**
  - With `tensorboard_log=logs_dir`, SB3 initializes a global logger that handles multiple output formats simultaneously: terminal (stdout) and TensorBoard binary files — 设置 `tensorboard_log=logs_dir` 后，SB3 初始化一个全局 logger，同时处理终端输出和 TensorBoard 二进制文件
  - `ProgressCallback` has access to this same logger via `self.logger`. Any custom metrics recorded in the callback using `self.logger.record("key", value)` will automatically appear in TensorBoard graphs — `ProgressCallback` 通过 `self.logger` 访问同一个 logger，回调中记录的自定义指标会自动出现在 TensorBoard 图表中
  - **`log_interval=1`**: For DQN, this tells SB3 to write a data point to TensorBoard every episode. This includes standard metrics like `rollout/ep_rew_mean` and `train/loss` — 对于 DQN，每个 episode 写入一个数据点到 TensorBoard，包括 `rollout/ep_rew_mean` 和 `train/loss` 等标准指标
  - **`check_freq=10000`**: callback only triggers its logic every 10,000 timesteps — 回调每 10,000 步触发一次
  - **The Result:** high-resolution data in TensorBoard (every episode), while terminal/callback reports will only update in massive 10,000-step jumps — **结果：** TensorBoard 中有高分辨率数据（每 episode），而终端/回调报告每 10,000 步才更新一次

> **📝 Notes:**
>
> _(To be added)_

---

## 9. 运行训练好的模型 (Running Trained Models)

![Page 12](week5_dqn_slides_pages/page_012.png)

- **Running trained models** — **运行训练好的模型**

```python
model = DQN.load(f"{models_dir}/dqn_blocks_world", env)
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    # obs, reward, terminated, truncated, info = env.step(action)
    obs, reward, terminated, info = env.step(action)
```

- `DQN.load()` 加载保存的模型
- `deterministic=True` 使用确定性动作（不探索）
- 注意：VecEnv 的 `step()` 返回 4 个值（不是 5 个），因为 VecEnv 自动处理 `terminated` 和 `truncated`

> **📝 Notes:**
>
> _(To be added)_

---
