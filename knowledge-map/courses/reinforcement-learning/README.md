# Reinforcement Learning Knowledge Map

> 来源课程：Stanford CS234 · CMU 10-703 · Sutton & Barto《RL: An Introduction》
> 级别：研究生 Master · 角色：ML 工程师
> 前置课程：`machine-learning` (研究生级) · `deep-learning` (研究生级)

## 课程定位

RL 是研究生级别独立课程，关注序贯决策与最优控制：

| 维度 | Deep Learning (研究生) | Reinforcement Learning (研究生) |
|------|----------------------|-------------------------------|
| 重点 | 监督学习 / 表示学习 | 序贯决策 / 试错学习 |
| 核心框架 | 输入→模型→输出 | 状态→动作→奖励→状态 |
| 数学基础 | 线性代数 + 微积分 + 概率 | MDP + 动态规划 + 最优控制 |
| 核心挑战 | 泛化 / 过拟合 | 探索vs利用 / 延迟奖励 / 信用分配 |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| foundations | 0 | 🔲 planned | RL 基础：Agent/环境/奖励/策略/探索vs利用/多臂赌博机 |
| mdp | 0 | 🔲 planned | MDP：状态转移/贝尔曼方程/最优策略/POMDP |
| dynamic_programming | 0 | 🔲 planned | 动态规划：策略评估/策略迭代/值迭代 |
| monte_carlo | 0 | 🔲 planned | 蒙特卡洛方法：首次访问/每次访问/重要性采样/离线策略 |
| temporal_difference | 0 | 🔲 planned | 时序差分：TD(0)/SARSA/Q-Learning/资格迹/TD(λ) |
| function_approx | 0 | 🔲 planned | 函数近似：线性近似/DQN/经验回放/目标网络/致命三角 |
| policy_gradient | 0 | 🔲 planned | 策略梯度：REINFORCE/基线/优势函数/方差缩减 |
| actor_critic | 0 | 🔲 planned | Actor-Critic：A2C/A3C/GAE/PPO/TRPO/SAC/DDPG/TD3 |
| model_based_rl | 0 | 🔲 planned | 基于模型RL：Dyna/MPC/MCTS/AlphaZero/MuZero |
| irl_imitation | 0 | 🔲 planned | 逆RL与模仿学习：行为克隆/DAgger/GAIL/最大熵IRL |
| multi_agent | 0 | 🔲 planned | 多智能体RL：纳什均衡/CTDE/自我博弈/合作vs竞争 |
| rlhf_alignment | 0 | 🔲 planned | RLHF与对齐：奖励模型/偏好学习/DPO/安全RL |
| rl_tools | 0 | 🔲 planned | RL工具：Gymnasium/MuJoCo/Stable Baselines3/CleanRL/TRL |
