---
description: Complete RL course lab - follow teacher's coding style strictly
---

# 🤖 RL 课程实验完成工作流 (RL Lab Workflow)

## 核心原则 (Core Principles)

在编写所有代码时，必须严格遵守以下原则：

1. **匹配老师风格**: 代码风格必须与老师在实验文档和教程中给出的示例一致。代码应简洁直接，不要过度封装。
2. **禁止魔术数字**: 所有数字字面量必须提取为文件顶部的命名常量。
3. **禁止过度设计**: 不要添加老师没要求的东西（如 class 封装、dotenv、bilingual 注释、复杂的工具函数等）。
4. **保持简单**: 如果老师给的示例是平铺脚本，就写平铺脚本；如果老师给的是一个 class，就写一个 class。

---

## Phase 1: 阅读实验文档 (Read Lab Document)

1. **找到实验文档**: 在 `courses/rl/labs/` 目录下找到对应的 Lab markdown 文件。
2. **通读全文**: 理解老师的具体要求，特别注意：
   - 老师给出的代码示例（必须严格参照）
   - 文件命名要求（如 `<userid>_lab[n]_xxx.py`）
   - 目录结构要求
   - 提交清单 (Submission Checklist)

---

## Phase 2: 环境构建 (Environment Construction)

**适用于需要自定义 Gymnasium 环境的实验。**

1. **创建环境包目录**: `src/<userid>_<env_name>/`
2. **grid_world.py**: 从 Gymnasium 教程 (https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/) 直接复制原版 GridWorldEnv 代码。保留教程原有的英文注释，不要添加额外注释。
3. **自定义环境文件** (如 cliff_walking.py): 在 grid_world.py 基础上复制并修改：
   - 重命名 class
   - 按老师要求修改网格尺寸、奖励机制等
   - 所有数字提取为模块顶部常量
4. **__init__.py 文件**: 保持最简，只写注册和导出代码。
5. **pyproject.toml**: 按教程格式配置。
// turbo
6. **安装验证**: `pip install -e .`
// turbo
7. **功能验证**: 用 Python 一行命令验证 `gymnasium.make()` 能正常加载环境。

---

## Phase 3: 编写 Agent (Agent Implementation)

1. **null_agent.py**: 老师的模板风格 — 导入环境 → `gymnasium.make()` → `env.reset()` → 循环 `env.action_space.sample()` + `env.step()` → `env.close()`。常量提取到顶部。
2. **Q-Learning Agent** (`<userid>_lab[n]_qlearning_agent.py`):
   - 平铺脚本风格（除非老师明确要求 class）
   - 使用老师指定的接口代码（如 `numstates` 计算方式、`state_dict['agent']` 提取方式）
   - 超参数全部提取为顶部常量
   - 包含 matplotlib 绘图（episode returns 和 steps per episode）
3. **DQN Agent** (`<userid>_lab[n]_dqn_agent.py`):
   - 直接参照老师给的 DQN 示例代码
   - 使用 `stable_baselines3.DQN`
   - 常量提取到顶部（ENV_ID, TOTAL_TIMESTEPS, LOG_INTERVAL 等）
4. **PPO Agent** (`<userid>_lab[n]_ppo_agent.py`):
   - 与 DQN 相同结构，换成 `stable_baselines3.PPO`

---

## Phase 4: 验证运行 (Verification)

// turbo
1. 运行 `null_agent.py` 验证环境能正常工作。
2. 运行各 agent 脚本确认无报错。
3. 验证图表文件已保存（如有）。

---

## Phase 5: 打包提交 (Packaging)

1. **清理**: 删除 `__pycache__`、`.egg-info`、`venv` 等目录。
2. **打包**: 压缩 `src` 文件夹为 `<userid>_lab[n]_submission.zip`。
3. **验证**: 检查压缩包内容是否包含所有要求的文件。

---

## 代码风格参考 (Code Style Reference)

### null_agent.py 范例:
```python
import gymnasium
import cliffwalking_env

ENV_ID = "cliffwalking_env/CliffWalking-v0"
RENDER_MODE = "human"
TEST_STEPS = 1000

env = gymnasium.make(ENV_ID, render_mode=RENDER_MODE)
observation, info = env.reset()

for _ in range(TEST_STEPS):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

### DQN Agent 范例 (老师原版):
```python
import gymnasium
import cliffwalking_env
from stable_baselines3 import DQN

ENV_ID = "cliffwalking_env/CliffWalking-v0"
RENDER_MODE = "human"
POLICY = "MultiInputPolicy"
TOTAL_TIMESTEPS = 10000
LOG_INTERVAL = 4
MODEL_NAME = "dqn_cliff"

env = gymnasium.make(ENV_ID, render_mode=RENDER_MODE)
model = DQN(POLICY, env, verbose=1)
model.learn(total_timesteps=TOTAL_TIMESTEPS, log_interval=LOG_INTERVAL)
model.save(MODEL_NAME)

del model
model = DQN.load(MODEL_NAME)

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
```
