# CST8509 Final: 强化学习期末总复习 (Reinforcement Learning Final Review)

## 1. Definitions (定义)

### RL 核心概念 (Core RL Concepts)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Reinforcement Learning (强化学习) | 机器学习的第三种类型，智能体通过与环境的试错交互来学习最大化累积奖励的策略 (Third type of ML; agent learns by trial-and-error interaction) | AlphaGo 下围棋、Atari 游戏 |
| Agent (智能体) | 学习和做决策的主体，根据状态选择动作以最大化奖励 (The decision-making entity) | Q-Learning 代码、SB3 的 DQN/PPO 模型 |
| Environment (环境) | 智能体交互的外部世界，接收动作并返回新状态和奖励 (The world the agent interacts with) | Gymnasium 迷宫、Gazebo 3D 仿真房子 |
| State ($S_t$) (状态) | 环境在某一时刻的描述信息，用于决定下一步行动 (Description of current situation) | 积木A在位置3、CartPole 的角度和速度 |
| Action ($A_t$) (动作) | 智能体在某一时刻执行的决策 (Choice made by agent) | 把积木A搬到位置2、向左/向右推杆 |
| Reward ($R_t$) (奖励) | 环境对智能体动作的标量反馈信号，表示"做得好不好" (Scalar feedback signal) | 堆对积木 +1、掉入悬崖 -100、每步 -1 |
| Policy ($\pi$) (策略) | 从状态到动作的映射规则，是 RL 的最终产出——"在每个状态下选什么动作" (Mapping from states to actions; the final output of RL) | 确定性：$a = \pi(s)$；随机性：$\pi(a|s) = P[A=a|S=s]$ |
| Deterministic Policy (确定性策略) | 每个状态只映射到一个确定的动作 $a = \pi(s)$ (One state → one fixed action) | 看到红灯 → 必定踩刹车 |
| Stochastic Policy (随机性策略) | 给出每个动作的选择概率 $\pi(a|s) = P[A=a|S=s]$ (One state → probability distribution over actions) | 状态X下：80%选动作1, 20%选动作2 |
| Value Function ($v_\pi(s)$) (价值函数) | 在策略 $\pi$ 下，从状态 $s$ 开始能获得的期望累积未来奖励 (Expected future cumulative reward from state $s$) | $v_\pi(s) = \mathbb{E}_\pi[G_t | S_t = s]$ |
| Action-Value Function ($q_\pi(s,a)$) (动作价值函数) | 在策略 $\pi$ 下，在状态 $s$ 执行动作 $a$ 后能获得的期望累积未来奖励 (Expected future reward after taking action $a$ in state $s$) | $q_\pi(s,a) = \mathbb{E}_\pi[G_t | S_t=s, A_t=a]$ |
| Model (模型) | 智能体对环境的内部表征，用于预测下一个状态和奖励，支持规划 (Agent's internal representation of environment dynamics) | 转移模型预测状态，奖励模型预测奖励 |
| Return ($G_t$) (回报) | 从时间步 $t$ 开始的累积折扣奖励总和 (Cumulative discounted reward from step $t$) | $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots$ |
| Discount Factor ($\gamma$) (折扣因子) | 控制未来奖励的衰减程度，$\gamma$ 越接近 1 智能体越有远见 (Controls importance of future rewards; 0→myopic, 1→farsighted) | $\gamma=0.99$：重视长远；$\gamma=0.1$：只看眼前 |
| Episode (回合) | 从初始状态到终止状态的一次完整交互序列 (One complete sequence from start to terminal state) | 一局棋、走完一次迷宫、泡一杯咖啡 |
| Episodic Task (回合制任务) | 有终止状态的任务，每次运行是一个独立回合 (Task with terminal state) | 下棋、走迷宫 |
| Continuing Task (持续任务) | 永不结束的任务 $T=\infty$，必须用折扣防止回报发散 (Never-ending task; needs discounting) | 控制发电厂、家用恒温器 |
| Reward Hypothesis (奖励假说) | 所有目标都可以用期望累积奖励的最大化来描述 (All goals = maximization of expected cumulative reward) | Sutton 教科书核心公理 |

### 马尔可夫与 MDP (Markov & MDP)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Markov Property (马尔可夫性质) | "给定当前状态，未来与过去无关"——$S_t$ 和 $R_t$ 的概率只取决于 $S_{t-1}$ 和 $A_{t-1}$ (Future is independent of past given present) | 位置+速度可构成马尔可夫状态；仅位置不行 |
| MDP (马尔可夫决策过程) | 满足马尔可夫性质的顺序决策问题的数学框架，包含 $(S, A, P, R, \gamma)$ (Mathematical framework for sequential decision-making) | 所有 RL 问题的数学基础 |
| Agent-Environment Boundary (智能体-环境边界) | 智能体不能任意改变的一切都属于环境；这个边界是设计者的选择("art not science") (Anything agent can't arbitrarily change = environment) | AlphaGo 不包含放棋子的物理动作 |

### Q-Learning 与 SARSA

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Q-Table (Q值表) | 记录每个"状态×动作"组合的长期价值的表格，策略 = "查表选最大Q值的动作" (Table storing Q-values for every state-action pair) | 4个状态×3个动作的小迷宫表格 |
| Q-Learning | 一种 Off-policy TD 控制算法，用最大Q值更新：$Q(S,A) \leftarrow Q(S,A) + \alpha[R + \gamma \max_{a'} Q(S',a') - Q(S,A)]$ (Off-policy: updates with max Q-value) | CliffWalking 实验中收敛到最短路径 |
| SARSA | 一种 On-policy TD 控制算法，用实际选的下一个动作的Q值更新：$Q(S,A) \leftarrow Q(S,A) + \alpha[R + \gamma Q(S',A') - Q(S,A)]$ (On-policy: updates with actual next action's Q-value) | 如果 $\epsilon$=1 (完全随机)，差异最大 |
| Epsilon-Greedy ($\epsilon$-贪心) | 以概率 $\epsilon$ 随机探索，以 $1-\epsilon$ 选最优动作，平衡探索与利用 (With prob ε: random; else: best action) | `epsilon=0.1`：90%利用+10%探索 |

### 动态规划与蒙特卡洛 (DP & MC)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Dynamic Programming (动态规划) | 在已知完美模型的前提下，用 Bellman 方程迭代计算最优策略的方法 (Requires perfect model; iterates Bellman equation) | `dynamic.ipynb` 实现值迭代 |
| Policy Evaluation (策略评估) | 给定一个策略 $\pi$，计算其状态值函数 $v_\pi$ (Compute value function for given policy) | 迭代更新直到差异足够小 |
| Policy Iteration (策略迭代) | 交替进行策略评估和策略改进的方法 (Alternate between evaluation and improvement) | 每次迭代都要做完整的策略评估 |
| Value Iteration (值迭代) | 类似策略迭代，但策略评估只迭代一次就停止 (Like Policy Iteration but evaluation stops after 1 sweep) | 比策略迭代更高效 |
| Monte Carlo (蒙特卡洛) | 不需要模型，通过完成完整回合后计算实际回报的平均值来学习 (Model-free; learns from complete episodes by averaging returns) | `monte_carlo.ipynb`, Sutton 第111页算法 |
| First-Visit MC (首次访问 MC) | 只统计每个回合中第一次访问某状态时的回报 (Count return only for first visit to a state in episode) | 同一状态被多次访问时只取第一次 |
| Every-Visit MC (每次访问 MC) | 统计回合中每次访问某状态时的回报 (Count return for every visit to a state) | 所有访问都计入平均 |
| Exploring Starts (探索起始) | 每个回合开始时随机选择初始状态/动作对，确保所有动作都被尝试 (Random start state/action each episode) | 无法用于真实环境，只能用于仿真 |

### DQN 核心组件 (DQN Components)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| DQN (深度Q网络) | 用神经网络替代 Q-Table 来近似 Q 值函数，能处理海量状态空间——"学规律"而非"背答案" (Neural network approximates Q-function instead of table) | 方块堆叠中 ~300万种状态用 `[512,512,256]` 网络处理 |
| Value Function Approximation (值函数近似) | 用参数化函数（如神经网络）来估算 Q 值，而非精确存储每个状态的值 (Use parameterized function to estimate Q-values instead of exact storage) | DQN 中的 Q-Network |
| Q-Network (Q网络) | DQN 中的主神经网络，输入状态，输出每个离散动作的 Q 值 (Main NN; input=state, output=Q-values for all actions) | `MlpPolicy` / `MultiInputPolicy` |
| Target Network (目标网络) | Q 网络的缓慢更新副本，用于计算目标 Q 值，防止训练过程中"追自己尾巴"导致不稳定 (Slowly updated copy of Q-network for stable target computation) | 每隔 `target_update_interval` 步同步一次 |
| Replay Buffer (经验回放缓冲区) | 存储过去经历 $(s, a, r, s')$ 的"经验池"，随机抽样训练以打破数据相关性 (Memory storing past transitions; randomly sampled to break correlation) | `learning_starts=2000`：先攒数据再学习 |
| `learning_starts` (预热步数) | 预热阶段的步数，智能体先随机行动填充 Replay Buffer 后才开始训练网络 (Number of random steps before training begins) | =2000 → 先随机执行2000步攒经验 |
| One-hot Vector (独热向量) | 一种编码方式：用一串数字表示分类信息，只有一位是1其余全0 (Encoding: one position=1, rest=0) | 积木A在位置3 → `[0,0,1,0,0,0, 0,0,0,0,0,0]` |
| `MultiInputPolicy` | SB3 策略类型，用于观测值是字典（Dict space）的情况 (SB3 policy for Dict observation spaces) | 当前+目标配置都是字典 → 用 MultiInputPolicy |
| `MlpPolicy` | SB3 策略类型，用于观测值是单个离散/连续值的情况 (SB3 policy for simple Discrete/Box observations) | 3 字母离散状态 → 用 MlpPolicy |
| Sparse Reward (稀疏奖励) | 智能体在绝大多数步骤中得到零奖励，只有极少数步骤得到非零奖励，导致学习信号极弱 (Most steps give 0 reward; learning signal extremely weak) | 方块堆叠中随机搬200步全部 reward=0 |

### PPO

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| PPO (Proximal Policy Optimization) | 直接优化策略的算法，输出每个动作的概率，更新方式保守平滑，不容易训练崩溃 (Directly learns action probabilities; conservative updates prevent training collapse) | 跳过Q值估算，直接学"该选哪个动作" |

### 课程学习 (Curriculum Learning)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Curriculum Learning (课程学习) | "先简单后困难"的训练策略：先降低难度让智能体获得正向奖励学到基本规律，再逐步增加难度 (Train from easy→hard so agent gets early positive rewards) | 像教小孩搭乐高：先留最后2块，再5块、10块… |
| `start_flat` (平铺启动) | 每个积木从自己"对应"的位置开始，使起点离目标很近，容易成功获得奖励 (Each block starts at its corresponding position; easy to reach target) | `start_flat=True` → 起点已经很接近目标 |
| `difficulty_level` (难度级别) | 控制起始状态与目标状态之间差几步：数值越小越容易 (Number of steps between start and target state) | `difficulty_level=2` → 只差2步 |
| `net_arch` (网络结构) | 定义神经网络隐藏层的宽度和深度 (Defines hidden layer sizes of the neural network) | `[64,64]`=默认; `[512,512,256]`=方块堆叠任务 |
| Capacity (容量) | 网络层的宽度，神经元越多能记住和学习的模式越多 (Width of layers; more neurons = more patterns learned) | 512 个神经元 vs 64 个神经元处理 144 维输入 |
| Separation (分离性) | 网络的深度，层越深能发现越复杂的"联合模式" (Depth of layers; deeper = more complex joint patterns discovered) | 3层网络可以学到"积木A在位置1 且 积木B在A上" |

### 工具与基础设施 (Tools & Infrastructure)

| Term (术语) | Definition (定义) | Example (示例) |
|---|---|---|
| Gymnasium | OpenAI Gym 的继任者，提供标准化的 RL 环境接口（reset/step/render） (Successor to Gym; standard RL environment API) | `import gymnasium as gym; env = gym.make(...)` |
| Stable-Baselines3 (SB3) | RL 算法的 Python 库，提供 DQN/PPO/A2C/SAC 等现成实现 (Library of ready-made RL algorithm implementations) | `model = DQN("MlpPolicy", env).learn(10000)` |
| Gazebo (仿真器) | 3D 物理仿真引擎，模拟环境和机器人，遵循物理定律——代替真机训练 (3D physics simulator; replaces real robot training) | 模拟 AWS 小屋中的 Create3 机器人 |
| ROS 2 (通信系统) | 机器人通信框架，在传感器/算法/控制器之间传递消息 (Communication framework between robot components) | `cmd_vel`(速度指令)、`image_raw`(图像)、`stop_status` |
| Vectorized Environment (向量化环境) | 将多个独立环境堆叠为单一环境，每步同时训练 n 个环境以加速 (Stack n independent envs; train all simultaneously) | `make_vec_env(make_custom_env, n_envs=4)` |
| Wrapper (包装器) | 修改环境行为的包装类，如改变动作空间、限制步数等 (Modifies env behavior: action space, step limit, etc.) | `DiscreteActionWrapper`: MultiDiscrete → Discrete |
| Callback (回调函数) | 训练过程中特定阶段调用的函数，用于监控、自动保存、评估 (Functions called at training stages; monitoring/saving/eval) | `EvalCallback`, `CheckpointCallback` |
| TensorBoard | 训练可视化工具，绘制 `ep_rew_mean`、`loss` 等指标曲线 (Training visualization; plots reward/loss curves) | `tensorboard_log=logs_dir` |
| Docker | 解决 Python 虚拟环境和 ROS 2 工作空间隔离问题的容器化方案 (Containerization for Python/ROS2 workspace isolation) | 保证依赖一致、可复现 |
| PyGame | Gymnasium 环境常用的 2D 渲染库 (2D rendering library often used with Gymnasium) | 可视化积木世界、CliffWalking |
| Prolog / Swiplserver | 用于积木世界的逻辑编程语言和 Python 接口 (Logic programming language for blocks world) | Assignment 1: 情境演算积木世界 |
| URDF (统一机器人描述格式) | ROS 中描述机器人模型的文件格式 (File format for describing robots in ROS) | Create3 仿真器使用 URDF |

---

## 2. Comparisons (对比)

### Q-Table vs DQN vs PPO

| Dimension (维度) | Q-Table (Q表) | DQN (深度Q网络) | PPO (近端策略优化) | Example (示例) |
|---|---|---|---|---|
| 核心思路 | 背答案：记录每个状态-动作的值 | 学规律：用神经网络估算Q值 | 直接学"该选哪个动作的概率" | Q-Table=乘法表; DQN=学乘法规则; PPO=直觉选答案 |
| 得到策略的方式 | 间接：查表→选Q值最大的动作 | 间接：算Q值→选最大的 | 直接：网络直接输出动作概率 | — |
| 动作空间 | 仅 Discrete | 仅 Discrete | Discrete 和 Continuous 都可 | PPO更通用 |
| 状态空间 | 小（表格存得下） | 大（网络可泛化到没见过的状态） | 大（同样用网络） | Q-Table: 几百种; DQN/PPO: 几百万种 |
| 可解释性 | 100% 透明，可查每个决策理由 | 黑盒，不知道内部学了什么 | 黑盒 | Q-Table最透明 |
| 致命缺陷 | 状态多→表格存不下、填不满 | 需要Replay Buffer和Target Network稳定训练 | — | 方块堆叠 $12^6 \approx$ 300万种状态 |

### On-policy vs Off-policy

| Dimension (维度) | On-policy (同策略) | Off-policy (异策略) | Example (示例) |
|---|---|---|---|
| 代表算法 | SARSA | Q-Learning | — |
| Q值更新依据 | 用实际选的下一个动作 $A'$ 的 Q 值 | 用下一状态中最大 Q 值 $\max_{a'} Q(S',a')$ | — |
| 当 $\epsilon$=1 时 | 用随机动作的值更新 | 用最大值动作更新 | 差异被放大 |
| 学习的策略 vs 执行的策略 | 相同（学什么用什么） | 不同（学最优，执行可以是探索性的） | Q-Learning 学的是贪心策略，执行的是 ε-贪心 |

### DP vs MC vs TD (Q-Learning)

| Dimension (维度) | Dynamic Programming | Monte Carlo | TD / Q-Learning | Example (示例) |
|---|---|---|---|---|
| 是否需要模型 | ✅ 需要完美模型 | ❌ 不需要 | ❌ 不需要 | DP = model-based; MC/TD = model-free |
| 是否需要回合结束 | ❌ 不需要 | ✅ 必须等回合结束 | ❌ 每步更新 | MC必须走完整个episode |
| 更新时机 | 迭代同步更新所有状态 | 回合结束后回溯更新 | 每步都更新 | TD最高效 |

### Agent 分类 (Agent Taxonomy)

| Dimension (维度) | Value-Based (基于价值) | Policy-Based (基于策略) | Actor-Critic (演员-评论家) | Example (示例) |
|---|---|---|---|---|
| 有无策略 | ✗ 隐含在 V 中 | ✓ 显式策略 | ✓ 策略(Actor) | — |
| 有无价值函数 | ✓ V/Q | ✗ | ✓ V(Critic) | — |
| 代表算法 | DQN, Q-Learning | REINFORCE | PPO, A2C, SAC | — |

### Model-Free vs Model-Based

| Dimension (维度) | Model-Free (无模型) | Model-Based (基于模型) | Example (示例) |
|---|---|---|---|
| 有无环境模型 | ✗ 不建模 | ✓ 有转移/奖励模型 | Q-Learning = Model-Free |
| 学习方式 | 直接从交互经验学 | 可以用模型规划 (Planning) | DP需要完美模型 |

### Exploration vs Exploitation

| Dimension (维度) | Exploration (探索) | Exploitation (利用) | Example (示例) |
|---|---|---|---|
| 含义 | 尝试未知动作，可能更好也可能更差 | 选择已知最优动作 | 随机选新餐厅 vs 总去熟悉的好餐厅 |
| 风险 | 可能发现更好方案，但有失败风险 | 安全稳定但可能错过更好选择 | $\epsilon$-greedy平衡两者 |

### MlpPolicy vs MultiInputPolicy

| Dimension (维度) | MlpPolicy | MultiInputPolicy | Example (示例) |
|---|---|---|---|
| 适用观测空间 | `Discrete` 或 `Box` | `Dict` (字典) | — |
| 典型场景 | 单一整数或向量表示的状态 | 当前配置+目标配置分别编码 | 字典含 `current` 和 `target` 用 MultiInputPolicy |

---

## 3. Formulas (公式)

### 核心公式 (Core Formulas)

| Formula (公式) | Description (说明) | Example (示例) |
|---|---|---|
| $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = R_{t+1} + \gamma G_{t+1}$ | 折扣回报：未来奖励的加权和，$\gamma$ 越大越重视远期 (Discounted return; recursive form) | $\gamma=0.99$, 奖励序列[+1,+1,+1] → $G=1+0.99+0.98$ |
| $v_\pi(s) = \mathbb{E}_\pi[G_t \| S_t = s]$ | 状态价值函数：从状态 $s$ 开始遵循策略 $\pi$ 的期望回报 (State-value function) | 在走廊状态的价值 = 4.7 |
| $q_\pi(s, a) = \mathbb{E}_\pi[G_t \| S_t = s, A_t = a]$ | 动作价值函数：状态 $s$ 下选动作 $a$ 的期望回报 (Action-value function) | Q-Table 中每个格子的值 |
| $Q(S,A) \leftarrow Q(S,A) + \alpha[R + \gamma \max_{a'} Q(S',a') - Q(S,A)]$ | Q-Learning 更新规则：Off-policy，用下一状态的最大Q值 (Q-Learning update; off-policy with max) | Lab 1 CliffWalking 实现 |
| $Q(S,A) \leftarrow Q(S,A) + \alpha[R + \gamma Q(S',A') - Q(S,A)]$ | SARSA 更新规则：On-policy，用实际选的下一动作的Q值 (SARSA update; on-policy with actual next action) | $A'$ 通过 $\epsilon$-greedy 从 $S'$ 选出 |
| $y = r + \gamma \max_{a'} Q_{target}(s', a')$ | DQN 目标值：用**目标网络**计算 (DQN target Q-value computed by target network) | 主网络最小化 $\text{MSE}(Q(s,a), y)$ |
| 输入向量长度 = $N_{blocks} \times N_{positions+blocks} \times 2$ | DQN方块堆叠的输入编码：每个积木用one-hot编码，当前+目标各一组 (One-hot encoding for block-stacking) | 6积木 × 12位 × 2(当前+目标) = 144维 |

---

## 4. Practical / Lab (实战结论)

### 📊 Lab/Assignment Conclusions (实验/作业结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|---|---|---|
| CliffWalking 中 Q-Learning 收敛到最短路径 | 因为 Q-Learning 是 off-policy，用最优Q值更新，所以即使探索时走弯路，最终学到的是贪心最短路径 (Q-Learning finds shortest path due to off-policy max update) | Lab 1 实验验证 |
| 负奖励促使更短路径 | 每步 -1 奖励会让智能体尽快找到终点以减少总惩罚 (Per-step negative reward incentivizes faster completion) | CliffWalking 每步 reward=-1 |
| Q-Table 初始化影响收敛 | 随机初始化 vs 全零初始化会影响收敛速度和路径 (Initialization method affects convergence) | 全零初始化可能导致初期过度探索 |
| `[64,64]` 网络学不会方块堆叠 | 默认小网络处理 144 维输入时容量不足，只有 `[512,512,256]` 才成功 (Default network too small for 144-dim input) | 实验调参结果，非理论推导 |
| 三件套缺一不可 | 大网络 + 课程学习 + 经验回放必须同时使用：缺大网络→学不会复杂模式；缺课程学习→永远拿不到奖励；缺经验回放→学习不稳定 (All three needed: big net + curriculum + replay) | Assignment 2 方块堆叠 DQN |
| DiscreteActionWrapper 展平 MultiDiscrete | DQN 只接受 Discrete 动作空间，用 `np.unravel_index` 将单整数还原为多维索引 (Flatten MultiDiscrete for DQN compatibility) | `np.prod(dims)` → 新 Discrete 空间 |
| VecEnv 的 step() 返回 4 个值 | 不是 5 个！VecEnv 自动处理 terminated 和 truncated (VecEnv auto-handles terminated/truncated) | `obs, reward, terminated, info = env.step(action)` |
| Gazebo 替代真机训练 | 真机训练太慢太贵太危险(3天训练+可能撞坏)，Gazebo 几小时完成+Reset 即可 (Simulation training is faster, cheaper, safer) | AWS Small House + Create3 仿真 |

---

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|---|---|---|
| 混淆 Q-Learning 和 SARSA 的更新规则 | Q-Learning 用 $\max Q(S',a')$（off-policy）；SARSA 用实际选的 $Q(S',A')$（on-policy） (Q-Learning=max; SARSA=actual next action) | 设 $\epsilon$=1 差异最明显 |
| 认为 Policy = Algorithm | Policy 是最终产出物（状态→动作的规则），不是算法本身。DQN/PPO 是产生策略的**方法** (Policy = final output mapping; DQN/PPO = methods to produce it) | 策略像"驾驶习惯"，DQN/PPO像"驾校教学方法" |
| 认为 DQN 的神经网络"存储"了状态 | 神经网络存的是**权重**（计算规律），不是状态本身。它能对没见过的状态也算出Q值 (NN stores weights/patterns, not states themselves) | 300万种状态不可能存下，但能泛化 |
| 认为 `[512,512,256]` 是理论计算的 | 这些数字是**实验调参**的结果，不是数学推导出来的 (Network architecture is empirically tuned, not theoretically derived) | 先试默认 `[64,64]` 效果差→调大→效果好 |
| 认为 One-hot 里每个积木只有 11 位 | 实际是 12 位——"自身槽位"虽然永远是0，但为了统一长度而保留 (12 bits not 11; self-slot always 0 but kept for uniform length) | 积木A的one-hot中"在A上"这一位永远=0 |
| 混淆 Value Function 的方向 | Value Function 只看**未来**奖励，不包含已经获得的奖励。好事发生后V值反而下降 (V only counts future rewards; drops after receiving a reward) | Atari中得分后V值降低因为那个奖励已经"过去了" |
| 忘记终止状态 Q=0 | 在 Q-Table 中终止状态的所有动作值必须初始化为0 (Terminal state Q-values must be 0) | $Q(\text{terminal}, \cdot) = 0$ |
| 认为 PPO 和 DQN 做同一件事 | DQN 学 Q 值函数（间接得到策略）；PPO 直接学策略本身（跳过Q值）。方法论完全不同 (DQN=value-based indirect; PPO=policy-based direct) | DQN选max Q值; PPO按概率选动作 |
| 奖励设计围绕子目标 | Sutton 明确说不要围绕子目标设计奖励。奖励应传达"要实现什么"而非"怎么实现" (Don't reward subgoals; reward the WHAT not the HOW) | 正确：到达终点+100; 错误：每走对一步+1 |
| VecEnv step() 返回 5 个值 | VecEnv 返回 4 个值 `(obs, reward, terminated, info)`，不是 Gymnasium 标准的 5 个 (VecEnv returns 4 values, not 5) | 忘记 VecEnv 自动合并 truncated |
| 认为 DP 不需要模型 | DP **必须知道**完美模型（转移概率和奖励）。MC 和 Q-Learning 才是 model-free (DP requires a perfect model; MC/Q-Learning are model-free) | DP: 已知所有转移概率 → 可以计算 |
| 混淆 Episode 和 Epoch | Episode 是 RL 中一次完整回合(起点→终点)；Epoch 是监督学习中对数据集的一次遍历——RL 没有固定数据集！ (Episode=one RL run; Epoch=one pass through SL dataset; RL has no fixed dataset) | RL 说 episode 不说 epoch |
| 改善效果不好时只想到调超参 | 应考虑 5 个方向：① 奖励是否太稀疏 ② 网络是否太小 ③ 是否需要课程学习 ④ 探索率衰减是否合理 ⑤ learning_starts/batch_size 是否合适 | 笔试题"效果不好怎么调？" |
