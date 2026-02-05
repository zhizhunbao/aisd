---
description: Complete RL assignment - specialized workflow for Reinforcement Learning assignments with Gymnasium environments
---

# 🤖 RL 作业完成工作流 (RL Assignment Workflow)

## ⚖️ 执行协议 (Execution Protocol)

为保证执行的确定性，Agent 必须严格遵守以下串行流程，禁止跨阶段执行。

## 📋 适用场景

- Gymnasium 自定义环境开发
- Q-Learning / SARSA 等表格型算法实现
- Stable-Baselines3 (DQN, PPO, A2C) 算法集成
- 含 Prolog/外部系统集成的复杂环境
- 超参数实验与结果可视化

## 🛠️ 所需 Skills

| 阶段 | 核心 Skill | 辅助 Skill |
|------|-----------|-----------|
| Phase 1 | `ai_learning-rl`, `learning-code_generation` | `dev-code_comment` |
| Phase 2 | `ai_learning-rl`, `learning-code_generation` | `dev-code_style` |
| Phase 3 | `ai_learning-rl`, `learning-code_screenshot` | - |
| Phase 4 | `dev-git`, `learning-lab_submission` | - |

---

## Phase 1: 环境构建协议 (Environment Construction)

**核心指令**: 通过 `learning-code_generation` 与 `dev-code_comment` 技能构建 Gymnasium 兼容环境。

### 1.1 环境脚手架

1. **复制模板**: 从现有环境（如 GridWorld）复制基础结构
2. **目录结构**: 
   ```
   <userid>_<env_name>/
   ├── <env_name>/
   │   ├── __init__.py          # 注册环境
   │   ├── envs/
   │   │   ├── __init__.py
   │   │   └── <env_file>.py    # 核心环境类
   │   └── wrappers/            # 可选的包装器
   ├── pyproject.toml           # 包定义
   └── README.md
   ```
3. **重命名**: 更新所有类名、环境 ID、包名

### 1.2 外部系统集成（如 Prolog）

```python
# Prolog 集成示例
from swiplserver import PrologMQI, PrologThread

self.mqi = PrologMQI()
self.prolog_thread = self.mqi.create_thread()
result = self.prolog_thread.query('[model_file]')  # 加载模型
```

### 1.3 状态与动作映射

```python
# 状态映射: 字符串 -> 整数
result = self.prolog_thread.query("state(S)")
self.states_dict = {s['S']: i for i, s in enumerate(result)}

# 动作映射: 整数 -> 字符串
result = self.prolog_thread.query("action(A)")
self.actions_dict = {i: build_action_string(a) for i, a in enumerate(result)}

# 反向查找: 整数 -> 字符串
def state_int_to_str(self, state_int):
    return list(self.states_dict.keys())[
        list(self.states_dict.values()).index(state_int)
    ]
```

### 1.4 空间定义

```python
from gymnasium import spaces

self.observation_space = spaces.Discrete(len(self.states_dict))
self.action_space = spaces.Discrete(len(self.actions_dict))
```

### 1.5 核心方法实现

| 方法 | 职责 | 关键点 |
|------|------|--------|
| `__init__` | 初始化环境 | 加载外部系统、构建映射、定义空间 |
| `reset` | 重置环境 | 随机目标状态、查询初始状态、返回观测 |
| `step` | 执行动作 | 动作转换、状态更新、奖励计算、终止判断 |
| `render` | 可视化 | PyGame/matplotlib 渲染 |
| `close` | 清理资源 | 关闭外部连接、释放资源 |

### 1.6 奖励设计

```python
# 典型奖励结构
REWARD_STEP = -1        # 每步惩罚（鼓励快速完成）
REWARD_INVALID = -10    # 无效动作惩罚
REWARD_GOAL = 100       # 达到目标奖励
```

### 1.7 验证检查点

- [ ] `pip install -e .` 成功执行
- [ ] `gym.make("<package>/<EnvName>-v0")` 能够加载
- [ ] Null Agent 随机测试通过
- [ ] `render_mode="human"` 可视化正常

**状态准入**: 只有环境能被成功初始化并通过 Null Agent 测试后，方可进入 Phase 2。

---

## Phase 2: 智能体演化协议 (Agent Evolution)

**核心指令**: 调用 `ai_learning-rl` 技能实现目标算法。

### 2.1 Q-Learning 实现

```python
# Q-Table 初始化
Q = np.zeros((n_states, n_actions))

# 核心更新公式
# Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]
Q[state, action] += alpha * (
    reward + gamma * np.max(Q[next_state]) - Q[state, action]
)
```

**超参数模板**:
```python
# 可调超参数
EPISODES = 1000
ALPHA = 0.1           # 学习率
GAMMA = 0.99          # 折扣因子
EPSILON = 1.0         # 初始探索率
EPSILON_DECAY = 0.995 # 探索衰减
EPSILON_MIN = 0.01    # 最小探索率
```

### 2.2 Stable-Baselines3 集成

```python
from stable_baselines3 import DQN, PPO, A2C

# DQN 示例
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# PPO 示例
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
```

### 2.3 训练记录

```python
# 记录指标
episode_rewards = []
episode_steps = []

for episode in range(EPISODES):
    total_reward = 0
    steps = 0
    # ... 训练循环 ...
    episode_rewards.append(total_reward)
    episode_steps.append(steps)
```

### 2.4 验证检查点

- [ ] Q-Learning 能正常收敛
- [ ] 训练指标被正确记录
- [ ] SB3 算法能成功运行（不要求收敛）

**状态准入**: Agent 能完成训练流程后，方可进入 Phase 3。

---

## Phase 3: 观测与分析协议 (Experimentation & Analysis)

**核心指令**: 运行实验并捕获可视化成果。

### 3.1 绘图模板

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Episode Rewards
axes[0].plot(episode_rewards)
axes[0].set_xlabel('Episode')
axes[0].set_ylabel('Total Reward')
axes[0].set_title('Episode Rewards')

# Episode Steps
axes[1].plot(episode_steps)
axes[1].set_xlabel('Episode')
axes[1].set_ylabel('Steps')
axes[1].set_title('Steps per Episode')

plt.suptitle('Q-Learning: α=0.1, γ=0.99, ε-decay=0.995')
plt.tight_layout()
plt.savefig('screenshots/qlearning_original_hyperparams.png', dpi=150)
plt.show()
```

### 3.2 超参数实验矩阵

| 实验 | Alpha | Gamma | Epsilon Decay | 备注 |
|------|-------|-------|---------------|------|
| Original | 0.1 | 0.99 | 0.995 | 基线 |
| Exp 1 | 0.2 | 0.99 | 0.995 | 高学习率 |
| Exp 2 | 0.1 | 0.9 | 0.995 | 低折扣 |
| Exp 3 | 0.1 | 0.99 | 0.99 | 快衰减 |
| Exp 4 | 0.05 | 0.999 | 0.999 | 保守设置 |

### 3.3 截图规范

- **目录**: `screenshots/`
- **命名**: `<algorithm>_<description>.png`
  - 例: `qlearning_original_hyperparams.png`
  - 例: `qlearning_high_alpha.png`
  - 例: `dqn_baseline.png`
- **标题**: 必须标注超参数值

### 3.4 验证检查点

- [ ] 基线实验截图已保存
- [ ] 至少 3 组超参数对比截图
- [ ] 图表标题清晰标注参数

**状态准入**: 所有实验截图完成后，方可进入 Phase 4。

---

## Phase 4: 交割与打包协议 (Delivery & Submission)

**核心指令**: 调用 `dev-git` 与 `learning-lab_submission` 技能。

### 4.1 代码清理

```bash
# 清理缓存
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# 确认不含虚拟环境
ls -la  # 检查无 venv, pvenv, .venv 目录
```

### 4.2 Git 提交规范

```bash
# 提交信息格式
git commit -m "feat: implement BlocksWorld-v0 environment"
git commit -m "feat: add Q-Learning agent with training plots"
git commit -m "feat: extend to BlocksWorld-v1 with target state"
git commit -m "feat: integrate Stable-Baselines3 DQN/PPO"
git commit -m "docs: add hyperparameter experiment screenshots"
```

### 4.3 最终目录结构检查

```
repository/
├── <userid>_blocksworld_env/      # 环境包
│   ├── blocksworld_env/
│   │   ├── envs/
│   │   │   ├── blocks_world.py    # v0 环境
│   │   │   └── blocks_world_target.py  # v1 环境
│   │   └── __init__.py
│   └── pyproject.toml
├── <userid>_assn1_qlearning_agent.py
├── <userid>_assn1_dqn_agent.py
├── <userid>_assn1_ppo_agent.py
├── screenshots/
│   ├── qlearning_original_hyperparams.png
│   ├── qlearning_exp1_high_alpha.png
│   ├── qlearning_exp2_low_gamma.png
│   └── qlearning_exp3_fast_decay.png
├── blocks_world.pl                # Prolog 模型
├── screen.py                      # 显示类
└── README.md
```

### 4.4 演示准备清单

- [ ] `BlocksWorld-v0` + Q-Learning 可运行演示
- [ ] 训练曲线截图准备完毕
- [ ] `BlocksWorld-v1` + Q-Learning 可运行演示
- [ ] Stable-Baselines3 算法可运行演示
- [ ] 熟悉代码核心逻辑，准备回答问题

### 4.5 最终断言

- [ ] 所有 Python 文件无语法错误
- [ ] 虚拟环境未被提交
- [ ] 所有截图在 `screenshots/` 目录
- [ ] Git 历史包含有意义的 commit message

---

## 📚 参考资源

### Gymnasium 环境创建
- [Environment Creation Tutorial](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

### Stable-Baselines3
- [SB3 Documentation](https://stable-baselines3.readthedocs.io/)
- [DQN](https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html)
- [PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)

### Prolog 集成
- [swiplserver Documentation](https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/mqi.html%27))

---

## 🚨 常见问题

| 问题 | 解决方案 |
|------|----------|
| `gym.make` 找不到环境 | 检查 `__init__.py` 注册、确认 `pip install -e .` |
| Prolog 查询返回空 | 检查查询语法（无句号）、确认模型已加载 |
| Q-Table 不收敛 | 调整学习率、检查奖励设计、增加探索 |
| SB3 训练崩溃 | 检查 observation_space/action_space 类型匹配 |
| 渲染窗口不显示 | 确认 `render_mode="human"`、检查 PyGame 安装 |
