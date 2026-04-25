# %%
# ============================================================
# Cell 0: 工具函数（唯一共享单元）
# Cell 0: Utility Functions (only shared cell)
# ============================================================
import math
import tabulate as _tabulate_mod
_tabulate_mod.WIDE_CHARS_MODE = True  # 修复中文对齐 / Fix CJK alignment
from tabulate import tabulate as _tabulate_fn

def ptable(rows, **kwargs):
    """格式化表格输出 / Formatted table output"""
    print(_tabulate_fn(rows, **kwargs, tablefmt="simple_grid"))

# %%
# ============================================================
# 概念01：强化学习交互循环
# Concept 01: RL Interaction Cycle (Agent-Environment Loop)
# ============================================================
# 强化学习的核心是智能体与环境的交互循环：状态→动作→奖励→新状态
# The core of RL is the agent-environment interaction loop: state→action→reward→next state
# ============================================================

# 状态集合：机器人可能的位置 / State set: possible robot positions
states = ["door", "hallway", "room", "exit"]
# 动作集合：可选的移动方式 / Action set: possible moves
actions = ["left", "right", "stay"]
# 奖励函数示例：到达出口得+10 / Reward example: +10 for reaching exit
rewards = {"door": 0, "hallway": 0, "room": 0, "exit": 10}

# 模拟一个回合 / Simulate one episode
def simulate_episode(start, policy_map, transitions, max_steps=5):
    """模拟智能体按策略执行一个回合 / Simulate agent following policy for one episode"""
    state = start
    total_reward = 0
    trajectory = []
    for step in range(max_steps):
        action = policy_map.get(state, "stay")
        reward = rewards.get(state, 0)
        total_reward += reward
        next_state = transitions.get((state, action), state)
        trajectory.append([step + 1, state, action, reward, next_state])
        state = next_state
        if state == "exit":
            total_reward += rewards["exit"]
            trajectory.append([step + 2, state, "done", rewards["exit"], "-"])
            break
    return trajectory, total_reward

# 简单策略：在每个状态选什么动作 / Simple policy: which action at each state
policy = {"door": "right", "hallway": "right", "room": "right", "exit": "stay"}
# 状态转移表 / Transition table
trans = {
    ("door", "right"): "hallway",
    ("hallway", "right"): "room",
    ("room", "right"): "exit",
}

traj, total = simulate_episode("door", policy, trans)
print("概念01: RL Interaction Cycle / 强化学习交互循环")
ptable(traj, headers=["Step", "State (St)", "Action (At)", "Reward (Rt)", "Next State (St+1)"])
print(f"Total reward = {total}\n")

# %%
# ============================================================
# 概念02：策略
# Concept 02: Policy (π)
# ============================================================
# 策略是从状态到动作的映射，是RL的最终产出
# Policy is a mapping from state to action — the ultimate output of RL
# ============================================================

# 三种策略对比 / Three policies comparison
# 策略A：总是往右 / Policy A: always go right
policy_a = {"door": "right", "hallway": "right", "room": "right"}
# 策略B：总是往左 / Policy B: always go left
policy_b = {"door": "left", "hallway": "left", "room": "left"}
# 策略C：随机策略 / Policy C: random (stay)
policy_c = {"door": "stay", "hallway": "stay", "room": "stay"}

rows = []
for name, pol, desc in [
    ("Policy A", policy_a, "Always Right → reaches exit"),
    ("Policy B", policy_b, "Always Left → stuck at door"),
    ("Policy C", policy_c, "Always Stay → no progress"),
]:
    actions_str = ", ".join(f"{s}→{a}" for s, a in pol.items())
    rows.append([name, actions_str, desc])

print("概念02: Policy / 策略")
ptable(rows, headers=["Policy", "State→Action Mapping", "Outcome"])
print("Best policy = Policy A (maximizes cumulative reward)\n")

# %%
# ============================================================
# 概念03：Q-Table（Q值表格）
# Concept 03: Q-Table (State-Action Value Table)
# ============================================================
# Q-Table记录每个状态-动作对的长期预期回报，策略=查表选最大Q值
# Q-Table stores expected long-term return for each state-action pair
# ============================================================

# Q-Table 数据：4状态×3动作 / Q-Table data: 4 states × 3 actions
q_table = {
    "door":    {"left": 0.0, "right": 3.2, "stay": 0.0},
    "hallway": {"left": 0.1, "right": 4.7, "stay": 0.0},
    "room":    {"left": 2.0, "right": 0.3, "stay": 5.1},
    "exit":    {"left": 0.0, "right": 0.0, "stay": 0.0},
}

rows = []
for state, actions_dict in q_table.items():
    best_action = max(actions_dict, key=actions_dict.get)
    best_q = actions_dict[best_action]
    row = [state] + [f"{v:.1f}" for v in actions_dict.values()]
    row.append(f"{best_action} (Q={best_q:.1f})")
    rows.append(row)

print("概念03: Q-Table / Q值表格")
ptable(rows, headers=["State", "Q(left)", "Q(right)", "Q(stay)", "Best Action"])
print("Policy derived from Q-Table: always pick action with max Q-value\n")

# %%
# ============================================================
# 概念04：Q-Learning 更新规则
# Concept 04: Q-Learning Update Rule
# ============================================================
# Q(s,a) ← Q(s,a) + α[R + γ·max Q(s',a') - Q(s,a)]
# Alpha=学习率, Gamma=折扣因子
# ============================================================

# 学习率 / Learning rate
alpha = 0.1
# 折扣因子 / Discount factor
gamma = 0.9

# 当前Q值 / Current Q-value
q_old = 1.0
# 获得的即时奖励 / Immediate reward received
reward = 5.0
# 下一状态的最大Q值 / Max Q-value of next state
max_q_next = 3.0

# TD目标 / TD target
td_target = reward + gamma * max_q_next
# TD误差 / TD error
td_error = td_target - q_old
# 更新后的Q值 / Updated Q-value
q_new = q_old + alpha * td_error

rows = [
    ["Q_old(s, a)", f"{q_old:.2f}", "Current estimate"],
    ["Reward R", f"{reward:.2f}", "Immediate reward"],
    ["max Q(s', a')", f"{max_q_next:.2f}", "Best future value"],
    ["TD Target", f"{td_target:.2f}", f"R + γ·max Q = {reward} + {gamma}×{max_q_next}"],
    ["TD Error", f"{td_error:.2f}", f"Target - Q_old = {td_target:.2f} - {q_old:.2f}"],
    ["Q_new(s, a)", f"{q_new:.2f}", f"Q_old + α·error = {q_old} + {alpha}×{td_error:.2f}"],
]

print("概念04: Q-Learning Update Rule / Q-Learning 更新规则")
print(f"Formula: Q(s,a) ← Q(s,a) + α[R + γ·maxQ(s',a') - Q(s,a)]")
print(f"Parameters: α={alpha}, γ={gamma}")
ptable(rows, headers=["Variable", "Value", "Meaning"])
print()

# %%
# ============================================================
# 概念05：状态空间爆炸
# Concept 05: State Space Explosion
# ============================================================
# 当方块数增加时，状态数呈指数增长，Q-Table不可行
# As blocks increase, state count grows exponentially → Q-Table infeasible
# ============================================================

# 每个方块的可能位置数 / Possible positions per block
positions_per_block = 12  # 6 ground + 6 on-top

rows = []
for num_blocks in range(1, 8):
    # 状态总数 / Total states
    total_states = positions_per_block ** num_blocks
    # Q-Table大小（假设36个动作）/ Q-Table size (assume 36 actions)
    num_actions = num_blocks * (num_blocks + 5)
    table_size = total_states * num_actions
    feasible = "YES" if total_states < 100000 else "NO"
    rows.append([num_blocks, f"{total_states:,}", f"{num_actions}", f"{table_size:,}", feasible])

print("概念05: State Space Explosion / 状态空间爆炸")
ptable(rows, headers=["Blocks", "States (12^n)", "Actions", "Q-Table Cells", "Feasible?"])
print("Conclusion: 6+ blocks → Q-Table is impractical (millions of cells)\n")

# %%
# ============================================================
# 概念06：One-Hot 编码
# Concept 06: One-Hot Encoding for Block States
# ============================================================
# 每个方块用12维one-hot向量表示位置，6方块×2组(当前+目标)=144维输入
# Each block: 12-dim one-hot vector; 6 blocks × 2 sets = 144-dim input
# ============================================================

def one_hot_encode(position_index, total_positions=12):
    """将位置索引编码为one-hot向量 / Encode position index as one-hot vector"""
    vec = [0] * total_positions
    vec[position_index] = 1
    return vec

# 示例：方块A在地面位置3 / Example: Block A at ground position 3
block_a_pos = one_hot_encode(2)  # index 2 = position 3
# 示例：方块B在方块A上方 / Example: Block B on top of Block A
block_b_pos = one_hot_encode(6)  # index 6 = "on block A"

rows = [
    ["Block A", "Ground Pos 3", str(block_a_pos), "Index 2 = 1"],
    ["Block B", "On Block A", str(block_b_pos), "Index 6 = 1"],
]
print("概念06: One-Hot Encoding / One-Hot 编码")
ptable(rows, headers=["Block", "Position", "One-Hot (12 dims)", "Note"])

# 计算总输入维度 / Calculate total input dimensions
num_blocks = 6
dims_per_block = 12
current_dims = num_blocks * dims_per_block  # 72
target_dims = num_blocks * dims_per_block   # 72
total_input = current_dims + target_dims    # 144

print(f"\nTotal input = {num_blocks} blocks × {dims_per_block} dims × 2 (current+target) = {total_input} dims")
print("This is the MultiInputPolicy input vector of length 144\n")

# %%
# ============================================================
# 概念07：值函数近似
# Concept 07: Value Function Approximation (VFA)
# ============================================================
# 用神经网络近似Q值函数，不再逐个记忆，而是学习状态→Q值的映射规律
# Use neural network to approximate Q-function: learn patterns instead of memorizing
# ============================================================

def simple_linear_q(state_features, weights, bias):
    """最简单的线性值函数近似 / Simplest linear value function approximation"""
    q_value = sum(s * w for s, w in zip(state_features, weights)) + bias
    return q_value

# 状态特征：[距离目标, 已完成步数比例, 方块正确率] / State features
state = [0.3, 0.5, 0.7]
# 权重（学习得到）/ Weights (learned)
weights = [2.0, -0.5, 3.0]
# 偏置 / Bias
bias = 0.1

q_approx = simple_linear_q(state, weights, bias)

# 展示计算过程 / Show calculation
terms = [f"{s}×{w}" for s, w in zip(state, weights)]
calc_str = " + ".join(terms) + f" + {bias}"

rows = [
    ["Q-Table", "Look up exact value from table", "Fails when states > 100K"],
    ["Linear VFA", f"Q = {calc_str} = {q_approx:.2f}", "Fast but limited patterns"],
    ["DQN (Deep)", "Q = NeuralNet(state)", "Handles complex patterns"],
]

print("概念07: Value Function Approximation / 值函数近似")
ptable(rows, headers=["Method", "How Q-value is computed", "Limitation"])
print()

# %%
# ============================================================
# 概念08：DQN 网络结构
# Concept 08: DQN Q-Network Architecture [512,512,256]
# ============================================================
# 默认[64,64]太小，6x6方块堆叠需要[512,512,256]的更大容量
# Default [64,64] too small; 6x6 block-stacking needs [512,512,256]
# ============================================================

def count_parameters(layer_sizes):
    """计算全连接网络的参数总数 / Count total parameters of FC network"""
    total_params = 0
    param_details = []
    for i in range(len(layer_sizes) - 1):
        # 权重 / Weights
        w_params = layer_sizes[i] * layer_sizes[i + 1]
        # 偏置 / Biases
        b_params = layer_sizes[i + 1]
        layer_total = w_params + b_params
        total_params += layer_total
        param_details.append([
            f"Layer {i}→{i+1}",
            f"{layer_sizes[i]}→{layer_sizes[i+1]}",
            f"{w_params:,}",
            f"{b_params:,}",
            f"{layer_total:,}",
        ])
    return total_params, param_details

# 输入维度 / Input dimension
input_dim = 144
# 输出维度（动作数）/ Output dimension (number of actions)
output_dim = 36

# 默认架构 / Default architecture
default_arch = [input_dim, 64, 64, output_dim]
default_total, default_details = count_parameters(default_arch)

# 增强架构 / Enhanced architecture
enhanced_arch = [input_dim, 512, 512, 256, output_dim]
enhanced_total, enhanced_details = count_parameters(enhanced_arch)

print("概念08: DQN Network Architecture / DQN 网络结构")
print(f"\nDefault [64,64] — Total params: {default_total:,}")
ptable(default_details, headers=["Connection", "Shape", "Weights", "Biases", "Total"])

print(f"\nEnhanced [512,512,256] — Total params: {enhanced_total:,}")
ptable(enhanced_details, headers=["Connection", "Shape", "Weights", "Biases", "Total"])

ratio = enhanced_total / default_total
print(f"\nEnhanced has {ratio:.1f}x more parameters → much greater capacity\n")

# %%
# ============================================================
# 概念09：经验回放缓冲区
# Concept 09: Experience Replay Buffer
# ============================================================
# 存储(s, a, r, s')经验四元组，随机采样训练，打破时序相关性
# Store (s, a, r, s') tuples, random sample for training, break temporal correlation
# ============================================================

# 模拟经验回放缓冲区 / Simulate replay buffer
class ReplayBuffer:
    """经验回放缓冲区 / Experience Replay Buffer"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state):
        """存储一条经验 / Store one experience"""
        experience = (state, action, reward, next_state)
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.position % self.capacity] = experience
        self.position += 1

    def sample(self, batch_size):
        """随机采样一批经验 / Random sample a batch"""
        import random
        random.seed(42)
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))

# 模拟填充缓冲区 / Simulate filling buffer
buffer = ReplayBuffer(capacity=2000)
sample_experiences = [
    ("pos_A", "move_right", 0, "pos_B"),
    ("pos_B", "move_left", 0, "pos_A"),
    ("pos_B", "move_right", 0, "pos_C"),
    ("pos_C", "stack_block", 1, "pos_D"),
    ("pos_D", "move_left", -1, "pos_C"),
]

for exp in sample_experiences:
    buffer.push(*exp)

print("概念09: Experience Replay Buffer / 经验回放缓冲区")
rows = []
for i, (s, a, r, ns) in enumerate(buffer.buffer):
    rows.append([i + 1, s, a, r, ns])
ptable(rows, headers=["#", "State", "Action", "Reward", "Next State"])

# 采样演示 / Sampling demo
batch = buffer.sample(3)
print("\nRandom batch of 3 experiences for training:")
batch_rows = [[s, a, r, ns] for s, a, r, ns in batch]
ptable(batch_rows, headers=["State", "Action", "Reward", "Next State"])
print(f"learning_starts=2000 means: collect 2000 experiences BEFORE training begins\n")

# %%
# ============================================================
# 概念10：课程学习
# Concept 10: Curriculum Learning
# ============================================================
# 从简单到困难逐步训练：start_flat + difficulty_level递增
# Train progressively from easy to hard: start_flat + increasing difficulty_level
# ============================================================

# 课程学习的训练阶段 / Curriculum learning training phases
phases = [
    ["DQN_1", True, 1, "Easiest: blocks already near target, 1 step away", "~80%"],
    ["DQN_2", True, 2, "Easy: blocks 2 steps from target", "~70%"],
    ["DQN_3", False, 3, "Medium: random start, 3 steps from target", "~55%"],
    ["DQN_4", False, 5, "Hard: random start, 5 steps from target", "~40%"],
    ["DQN_5", False, -1, "Full difficulty: completely random", "~25%"],
]

print("概念10: Curriculum Learning / 课程学习")
ptable(phases, headers=["Run", "start_flat", "difficulty", "Description", "Success Rate"])

# 对比：无课程学习 / Comparison: without curriculum
print("\nWithout Curriculum Learning:")
print("  → Start at full difficulty → near-zero reward → no learning signal")
print("  → Agent never discovers what 'correct stacking' looks like")
print("\nWith Curriculum Learning:")
print("  → Phase 1: easy wins build basic understanding")
print("  → Each phase loads previous model weights and increases difficulty")
print("  → Gradual progression → stable convergence\n")

# %%
# ============================================================
# 概念11：奖励稀疏问题
# Concept 11: Sparse Reward Problem
# ============================================================
# 任务太难时智能体几乎永远拿不到正向奖励，导致学习信号为零
# When task is too hard, agent almost never gets positive reward → zero learning signal
# ============================================================

import random
random.seed(42)

def simulate_random_agent(num_episodes, success_prob):
    """模拟随机智能体获得奖励的情况 / Simulate random agent reward collection"""
    total_reward = 0
    successes = 0
    for _ in range(num_episodes):
        if random.random() < success_prob:
            total_reward += 1
            successes += 1
    return total_reward, successes

# 不同难度下随机智能体的成功概率 / Success probability at different difficulties
scenarios = [
    ["2 blocks, 2 pos", 100, 0.25, "Simple task"],
    ["4 blocks, 4 pos", 100, 0.001, "Medium task"],
    ["6 blocks, 6 pos", 100, 0.000001, "Full task (Assignment)"],
]

rows = []
for name, episodes, prob, desc in scenarios:
    reward, successes = simulate_random_agent(episodes, prob)
    rows.append([name, f"{prob:.6f}", episodes, successes, reward, desc])

print("概念11: Sparse Reward / 奖励稀疏问题")
ptable(rows, headers=["Task", "P(success)", "Episodes", "Successes", "Total Reward", "Note"])
print("With 6 blocks: random agent gets ~0 reward → neural network has nothing to learn from\n")

# %%
# ============================================================
# 概念12：DQN vs PPO 对比
# Concept 12: DQN vs PPO Comparison
# ============================================================
# DQN间接学策略（先学Q值→选max），PPO直接学策略（输出动作概率）
# DQN learns policy indirectly (Q→argmax), PPO learns policy directly (output probabilities)
# ============================================================

rows = [
    ["What it learns", "Q-value function Q(s,a)", "Policy π(a|s) directly"],
    ["Network output", "Q-value for each action", "Probability of each action"],
    ["Action selection", "argmax Q(s,a) (greedy)", "Sample from probability distribution"],
    ["Approach type", "Value-based (indirect)", "Policy gradient (direct)"],
    ["Action space", "Discrete only", "Discrete + Continuous"],
    ["Update style", "Off-policy (replay buffer)", "On-policy (recent experience)"],
    ["Stability", "Can be unstable (overestimation)", "More stable (clipped updates)"],
    ["Key technique", "Experience Replay + Target Net", "Clipped Surrogate Objective"],
    ["SB3 default net", "[64, 64]", "[64, 64]"],
]

print("概念12: DQN vs PPO / DQN与PPO对比")
ptable(rows, headers=["Dimension", "DQN", "PPO"])
print()

# %%
# ============================================================
# 概念13：Gazebo + ROS2 仿真架构
# Concept 13: Gazebo + ROS 2 Simulation Architecture
# ============================================================
# Gazebo=3D物理仿真器，ROS2=通信框架，Agent=算法大脑
# Gazebo=3D physics sim, ROS2=communication framework, Agent=algorithm brain
# ============================================================

# 仿真系统组件 / Simulation system components
components = [
    ["Gazebo", "3D Physics Simulator", "Simulates house, robot, collisions", "AWS Small House world"],
    ["ROS 2", "Communication Framework", "Passes messages between nodes", "Topics: cmd_vel, image_raw"],
    ["Agent (SB3)", "Algorithm Brain", "Decides actions from observations", "DQN or PPO algorithm"],
    ["Gymnasium", "Environment Interface", "Wraps simulation as RL env", "step(), reset(), observation"],
]

print("概念13: Gazebo + ROS2 Architecture / 仿真架构")
ptable(components, headers=["Component", "Role", "What it does", "Example"])

# ROS2 消息流 / ROS2 message flow
print("\nROS 2 Message Flow:")
print("  Agent → publish cmd_vel → Robot moves in Gazebo")
print("  Gazebo → image_raw → Agent processes camera image")
print("  Gazebo → stop_status → Agent knows when robot stopped")
print("  Environment → (observation, reward) → Agent decides next action\n")

# %%
# ============================================================
# 概念14：SB3 关键配置参数
# Concept 14: Stable-Baselines3 Key Hyperparameters
# ============================================================
# SB3中影响训练效果的核心超参数
# Key hyperparameters in SB3 that affect training performance
# ============================================================

params = [
    ["learning_starts", "2000", "Steps before training begins", "Fill replay buffer first"],
    ["learning_rate", "1e-4", "Step size for weight updates", "Too high=unstable, too low=slow"],
    ["batch_size", "32", "Experiences per training step", "Larger=more stable, slower"],
    ["gamma (γ)", "0.99", "Discount factor for future rewards", "0=myopic, 1=far-sighted"],
    ["buffer_size", "100000", "Replay buffer capacity", "Stores past experiences"],
    ["exploration_fraction", "0.1", "% of training for exploration decay", "ε-greedy exploration"],
    ["policy_kwargs", "dict(net_arch=[512,512,256])", "Network architecture", "More neurons=more capacity"],
    ["total_timesteps", "500000", "Total training steps", "More=better but slower"],
]

print("概念14: SB3 Key Hyperparameters / SB3关键超参数")
ptable(params, headers=["Parameter", "Typical Value", "Meaning", "Tuning Tip"])
print()

# %%
# ============================================================
# 概念15：期末复习全局总结
# Concept 15: Final Review — Complete RL Evolution Summary
# ============================================================
# 整学期技术演进：Q-Table→DQN→仿真环境→课程学习
# Full-semester tech evolution: Q-Table→DQN→Simulation→Curriculum Learning
# ============================================================

evolution = [
    ["Stage 1", "Q-Table", "Simple lookup table", "100% transparent", "Cannot scale to large state spaces"],
    ["Stage 2", "DQN", "Neural net approximates Q", "Handles millions of states", "Black box; needs lots of data"],
    ["Stage 3", "Gazebo+ROS2", "3D physics simulation", "Safe & fast training", "Sparse reward in complex tasks"],
    ["Stage 4", "Curriculum", "Easy→hard progression", "Solves sparse reward", "Requires manual difficulty design"],
]

print("概念15: RL Evolution Summary / 强化学习演进总结")
ptable(evolution, headers=["Stage", "Method", "What", "Strength", "Weakness"])

# 三要素缺一不可 / Three essentials — all required
print("\nSuccess Recipe for Block-Stacking (all three required):")
essentials = [
    ["Large Network [512,512,256]", "Enough capacity to learn complex patterns"],
    ["Curriculum Learning", "Progressive difficulty ensures positive reward signal"],
    ["Experience Replay + learning_starts", "Stable and diverse training data"],
]
ptable(essentials, headers=["Component", "Why It's Essential"])
print("\nRemove any one → training fails!\n")
