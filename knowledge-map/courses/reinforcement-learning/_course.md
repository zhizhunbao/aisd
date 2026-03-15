# 强化学习 Reinforcement Learning

> 名词总表 · 来源：Sutton & Barto《Reinforcement Learning: An Introduction》· Stanford CS234 · CMU 10-703 · 原始论文
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 基础概念 Foundations

| 名词 | 英文 |
|------|------|
| 强化学习 | Reinforcement Learning (RL) |
| 智能体 | Agent |
| 环境 | Environment |
| 状态 | State (s) |
| 动作 | Action (a) |
| 奖励 | Reward (r) |
| 策略 | Policy (π) |
| 轨迹 | Trajectory / Episode |
| 时间步 | Time Step |
| 折扣因子 | Discount Factor (γ) |
| 回报 | Return (G) |
| 探索 vs 利用 | Exploration vs Exploitation |
| ε-贪心 | ε-Greedy |
| 多臂赌博机 | Multi-Armed Bandit |
| 上置信界 | UCB (Upper Confidence Bound) |

---

### 马尔可夫决策过程 Markov Decision Process

| 名词 | 英文 |
|------|------|
| 马尔可夫性质 | Markov Property |
| 马尔可夫决策过程 | MDP (Markov Decision Process) |
| 状态转移概率 | Transition Probability P(s'|s,a) |
| 奖励函数 | Reward Function R(s,a) |
| 状态值函数 | State-Value Function V(s) |
| 动作值函数 | Action-Value Function Q(s,a) |
| 贝尔曼期望方程 | Bellman Expectation Equation |
| 贝尔曼最优方程 | Bellman Optimality Equation |
| 最优策略 | Optimal Policy (π*) |
| 最优值函数 | Optimal Value Function (V*, Q*) |
| POMDP | Partially Observable MDP |

---

### 动态规划 Dynamic Programming

| 名词 | 英文 |
|------|------|
| 动态规划 | Dynamic Programming (DP) |
| 策略评估 | Policy Evaluation |
| 策略改进 | Policy Improvement |
| 策略迭代 | Policy Iteration |
| 值迭代 | Value Iteration |
| 收敛性 | Convergence |
| 完备模型 | Model-Based (Full Model) |
| 同步更新 | Synchronous Update |
| 异步更新 | Asynchronous Update |

---

### 蒙特卡洛方法 Monte Carlo Methods

| 名词 | 英文 |
|------|------|
| 蒙特卡洛方法 | Monte Carlo (MC) Methods |
| 首次访问 MC | First-Visit MC |
| 每次访问 MC | Every-Visit MC |
| MC 控制 | MC Control |
| 重要性采样 | Importance Sampling |
| 离线策略 | Off-Policy |
| 在线策略 | On-Policy |
| 加权重要性采样 | Weighted Importance Sampling |
| 回报估计 | Return Estimation |

---

### 时序差分学习 Temporal Difference Learning

| 名词 | 英文 |
|------|------|
| 时序差分 | TD (Temporal Difference) |
| TD(0) | TD(0) |
| TD 误差 | TD Error (δ) |
| 自举 | Bootstrapping |
| SARSA | State-Action-Reward-State-Action |
| Q-Learning | Q-Learning |
| 期望 SARSA | Expected SARSA |
| n 步 TD | n-step TD |
| TD(λ) | TD(λ) |
| 资格迹 | Eligibility Trace |
| 前向视图 / 后向视图 | Forward / Backward View |

---

### 函数近似 Function Approximation

| 名词 | 英文 |
|------|------|
| 函数近似 | Function Approximation |
| 线性函数近似 | Linear Function Approximation |
| 特征向量 | Feature Vector |
| 基函数 | Basis Functions |
| 梯度蒙特卡洛 | Gradient MC |
| 半梯度 TD | Semi-Gradient TD |
| 致命三角 | Deadly Triad |
| 经验回放 | Experience Replay |
| 目标网络 | Target Network |
| DQN | Deep Q-Network |
| 优先级经验回放 | Prioritized Experience Replay |
| 双重 DQN | Double DQN |
| 决斗 DQN | Dueling DQN |

---

### 策略梯度 Policy Gradient

| 名词 | 英文 |
|------|------|
| 策略梯度 | Policy Gradient |
| 策略梯度定理 | Policy Gradient Theorem |
| REINFORCE | REINFORCE (Monte Carlo Policy Gradient) |
| 基线 | Baseline |
| 优势函数 | Advantage Function A(s,a) |
| 方差缩减 | Variance Reduction |
| 随机策略 | Stochastic Policy |
| 确定性策略 | Deterministic Policy |
| 对数概率技巧 | Log-Probability Trick |
| 得分函数 | Score Function |

---

### Actor-Critic 方法 Actor-Critic Methods

| 名词 | 英文 |
|------|------|
| Actor-Critic | Actor-Critic |
| Actor（策略网络） | Actor (Policy Network) |
| Critic（值网络） | Critic (Value Network) |
| A2C | Advantage Actor-Critic |
| A3C | Asynchronous Advantage Actor-Critic |
| GAE | Generalized Advantage Estimation |
| PPO | Proximal Policy Optimization |
| TRPO | Trust Region Policy Optimization |
| 剪断目标 | Clipped Objective |
| KL 散度约束 | KL Divergence Constraint |
| SAC | Soft Actor-Critic |
| 最大熵 RL | Maximum Entropy RL |
| DDPG | Deep Deterministic Policy Gradient |
| TD3 | Twin Delayed DDPG |

---

### 基于模型的 RL Model-Based RL

| 名词 | 英文 |
|------|------|
| 基于模型的 RL | Model-Based RL |
| 世界模型 | World Model |
| Dyna | Dyna Architecture |
| 模型预测控制 | MPC (Model Predictive Control) |
| 学习动力学模型 | Learned Dynamics Model |
| 规划 | Planning |
| 蒙特卡洛树搜索 | MCTS (Monte Carlo Tree Search) |
| AlphaGo / AlphaZero | AlphaGo / AlphaZero |
| MuZero | MuZero |
| 模型误差 | Model Error / Model Bias |

---

### 逆强化学习与模仿学习 Inverse RL & Imitation Learning

| 名词 | 英文 |
|------|------|
| 模仿学习 | Imitation Learning |
| 行为克隆 | Behavior Cloning |
| DAgger | Dataset Aggregation |
| 逆强化学习 | Inverse RL (IRL) |
| 最大熵 IRL | Maximum Entropy IRL |
| GAIL | Generative Adversarial Imitation Learning |
| 示范 | Demonstration |
| 专家策略 | Expert Policy |

---

### 多智能体 RL Multi-Agent RL

| 名词 | 英文 |
|------|------|
| 多智能体 RL | Multi-Agent RL (MARL) |
| 纳什均衡 | Nash Equilibrium |
| 合作博弈 | Cooperative Game |
| 竞争博弈 | Competitive Game |
| 混合博弈 | Mixed Game |
| 通信学习 | Communication Learning |
| 集中训练分散执行 | CTDE (Centralized Training, Decentralized Execution) |
| 自我博弈 | Self-Play |
| 独立学习 | Independent Learning |

---

### RLHF 与对齐 RLHF & Alignment

| 名词 | 英文 |
|------|------|
| 人类反馈强化学习 | RLHF (RL from Human Feedback) |
| 奖励模型 | Reward Model |
| 偏好学习 | Preference Learning |
| DPO | Direct Preference Optimization |
| 对齐 | Alignment |
| 安全 RL | Safe RL |
| 约束 MDP | Constrained MDP |
| 价值对齐 | Value Alignment |

---

### RL 环境与工具 RL Environments & Tools

| 名词 | 英文 |
|------|------|
| Gymnasium | Gymnasium (OpenAI Gym) |
| Atari 游戏 | Atari Games |
| MuJoCo | MuJoCo |
| DeepMind Control Suite | DM Control Suite |
| PettingZoo | PettingZoo (Multi-Agent) |
| Stable Baselines3 | Stable Baselines3 |
| RLlib | RLlib (Ray) |
| CleanRL | CleanRL |
| TRL | Transformer Reinforcement Learning (TRL) |
