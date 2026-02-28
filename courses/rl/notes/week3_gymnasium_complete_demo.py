"""
Week 3: Gymnasium 环境完整演示
Week 3: Gymnasium Environments Complete Demo

演示 Gymnasium 的核心 API、自定义环境创建、Spaces 系统和 Q-Learning 集成。
Demonstrates Gymnasium core API, custom environment creation, Spaces system, and Q-Learning integration.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 输出目录 (Output directory)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week3_gymnasium_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# ============================================================
# 步骤 1：Gymnasium Spaces 系统演示
# Step 1: Gymnasium Spaces System Demo
# ============================================================

import gymnasium as gym
from gymnasium import spaces

print("=" * 60)
print("步骤 1: Gymnasium Spaces 系统 (Spaces System)")
print("=" * 60)

# --- Discrete Space ---
# 离散空间：{0, 1, ..., n-1}
# Discrete space: {0, 1, ..., n-1}
discrete_space = spaces.Discrete(4)
print(f"\n[Discrete(4)]")
print(f"  n = {discrete_space.n}")
print(f"  sample = {discrete_space.sample()}")
print(f"  contains(3) = {discrete_space.contains(3)}")
print(f"  contains(5) = {discrete_space.contains(5)}")

# --- Box Space ---
# 连续空间：指定范围和形状
# Continuous space: specified range and shape
box_space = spaces.Box(low=0, high=10, shape=(2,), dtype=np.float32)
print(f"\n[Box(0, 10, shape=(2,))]")
print(f"  shape = {box_space.shape}")
print(f"  low = {box_space.low}, high = {box_space.high}")
print(f"  sample = {box_space.sample()}")

# --- Dict Space ---
# 字典空间：组合多个子空间
# Dict space: combine multiple sub-spaces
dict_space = spaces.Dict({
    "agent": spaces.Discrete(12),
    "target": spaces.Discrete(12),
})
print(f"\n[Dict(agent=Discrete(12), target=Discrete(12))]")
sample = dict_space.sample()
print(f"  sample = {sample}")

# --- MultiDiscrete Space ---
# 多维离散空间
# Multi-dimensional discrete space
multi_space = spaces.MultiDiscrete([4, 3])
print(f"\n[MultiDiscrete([4, 3])]")
print(f"  nvec = {multi_space.nvec}")
print(f"  sample = {multi_space.sample()}")

# 可视化 Spaces 类型对比
# Visualize Spaces type comparison
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Discrete
ax = axes[0]
ax.bar(range(4), [1]*4, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'], alpha=0.8)
ax.set_title("Discrete(4)\n离散空间", fontsize=12)
ax.set_xlabel("Value")
ax.set_xticks(range(4))
ax.set_xticklabels(["Right(0)", "Up(1)", "Left(2)", "Down(3)"], rotation=30, fontsize=8)

# Box
ax = axes[1]
samples = np.array([box_space.sample() for _ in range(200)])
ax.scatter(samples[:, 0], samples[:, 1], alpha=0.3, s=10, c='#3498db')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Box(0, 10, shape=(2,))\n连续空间", fontsize=12)
ax.set_xlabel("dim 0")
ax.set_ylabel("dim 1")

# Dict
ax = axes[2]
agent_samples = [dict_space.sample()["agent"] for _ in range(500)]
target_samples = [dict_space.sample()["target"] for _ in range(500)]
ax.hist2d(agent_samples, target_samples, bins=12, cmap='Blues')
ax.set_title("Dict(agent, target)\n字典空间", fontsize=12)
ax.set_xlabel("agent state")
ax.set_ylabel("target state")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step1_spaces.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n✅ 图表已保存: step1_spaces.png")


# ============================================================
# 步骤 2：自定义 Gymnasium 环境 — 4x3 GridWorld
# Step 2: Custom Gymnasium Environment — 4x3 GridWorld
# ============================================================

print("\n" + "=" * 60)
print("步骤 2: 自定义 Gymnasium 环境 (Custom Environment)")
print("=" * 60)


class SimpleGridWorldEnv(gym.Env):
    """
    简单的 4x3 GridWorld 环境
    Simple 4x3 GridWorld environment

    网格布局 (Grid layout):
    ┌───┬───┬───┬───┐
    │ 0 │ 1 │ 2 │+1 │  row 0: 目标在 (0,3)
    ├───┼───┼───┼───┤
    │ 4 │ W │ 6 │-1 │  row 1: 墙在 (1,1), 悬崖在 (1,3)
    ├───┼───┼───┼───┤
    │ 8 │ 9 │10 │11 │  row 2: 起点在 (2,0)=state 8
    └───┴───┴───┴───┘
    动作: 0=右, 1=上, 2=左, 3=下
    """

    metadata = {"render_modes": ["ansi"]}

    def __init__(self, render_mode=None):
        super().__init__()
        self.rows = 3
        self.cols = 4
        self.observation_space = spaces.Discrete(self.rows * self.cols)
        self.action_space = spaces.Discrete(4)  # 右上左下 (right, up, left, down)
        self.render_mode = render_mode

        # 特殊状态 (Special states)
        self.start = 8       # 起点 (start)
        self.goal = 3        # 目标 +1 (goal)
        self.cliff = 7       # 悬崖 -1 (cliff)
        self.wall = 5        # 墙壁 (wall)

        # 动作映射: 右上左下 (Action mapping: right, up, left, down)
        self._action_to_delta = {
            0: (0, 1),   # 右 (right)
            1: (-1, 0),  # 上 (up)
            2: (0, -1),  # 左 (left)
            3: (1, 0),   # 下 (down)
        }

    def _state_to_rc(self, state):
        return state // self.cols, state % self.cols

    def _rc_to_state(self, row, col):
        return row * self.cols + col

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._agent_pos = self.start
        return self._agent_pos, {}

    def step(self, action):
        row, col = self._state_to_rc(self._agent_pos)
        dr, dc = self._action_to_delta[action]
        new_row = max(0, min(self.rows - 1, row + dr))
        new_col = max(0, min(self.cols - 1, col + dc))
        new_state = self._rc_to_state(new_row, new_col)

        # 撞墙则不动 (Hit wall: stay)
        if new_state == self.wall:
            new_state = self._agent_pos

        self._agent_pos = new_state

        # 奖励和终止 (Reward and termination)
        if new_state == self.goal:
            return new_state, 1.0, True, False, {}
        elif new_state == self.cliff:
            return new_state, -1.0, True, False, {}
        else:
            return new_state, -0.01, False, False, {}

    def render(self):
        if self.render_mode == "ansi":
            grid = []
            for r in range(self.rows):
                row_str = []
                for c in range(self.cols):
                    s = self._rc_to_state(r, c)
                    if s == self._agent_pos:
                        row_str.append(" A ")
                    elif s == self.goal:
                        row_str.append("+1 ")
                    elif s == self.cliff:
                        row_str.append("-1 ")
                    elif s == self.wall:
                        row_str.append(" ▓ ")
                    else:
                        row_str.append(" . ")
                grid.append("|".join(row_str))
            return "\n".join(grid)


# 测试环境 (Test environment)
env = SimpleGridWorldEnv(render_mode="ansi")
obs, info = env.reset(seed=42)
print(f"\n初始状态 (Initial state): {obs}")
print(f"观测空间 (Observation space): {env.observation_space}")
print(f"动作空间 (Action space): {env.action_space}")
print(f"\n初始网格 (Initial grid):")
print(env.render())

# 执行几步 (Take a few steps)
actions = [1, 1, 0, 0, 0]  # 上上右右右 → 到达目标
action_names = ["Right", "Up", "Left", "Down"]
print(f"\n执行动作序列 (Execute action sequence):")
for a in actions:
    obs, reward, terminated, truncated, info = env.step(a)
    print(f"  Action: {action_names[a]:5s} → State: {obs:2d}, Reward: {reward:+.2f}, "
          f"Terminated: {terminated}, Truncated: {truncated}")
    if terminated:
        print(f"  🎯 Episode 结束!")
        break


# ============================================================
# 步骤 3：Q-Learning 在自定义 Gymnasium 环境中训练
# Step 3: Q-Learning Training in Custom Gymnasium Environment
# ============================================================

print("\n" + "=" * 60)
print("步骤 3: Q-Learning 训练 (Q-Learning Training)")
print("=" * 60)

# 超参数 (Hyperparameters)
alpha = 0.1      # 学习率 (learning rate)
gamma = 0.99     # 折扣因子 (discount factor)
epsilon = 1.0    # 初始探索率 (initial exploration rate)
epsilon_min = 0.01
epsilon_decay = 0.995
num_episodes = 500

env = SimpleGridWorldEnv()
n_states = env.observation_space.n
n_actions = env.action_space.n
qtable = np.zeros((n_states, n_actions))

# 训练记录 (Training records)
rewards_per_episode = []
steps_per_episode = []

for episode in range(num_episodes):
    obs, _ = env.reset(seed=episode)
    total_reward = 0
    steps = 0

    for step in range(100):  # 最大步数 (max steps)
        # Epsilon-greedy 策略 (Epsilon-greedy policy)
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = int(np.argmax(qtable[obs]))

        next_obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # Q-Learning 更新 (Q-Learning update)
        # Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') - Q(s,a)]
        best_next = np.max(qtable[next_obs]) if not terminated else 0
        qtable[obs, action] += alpha * (reward + gamma * best_next - qtable[obs, action])

        obs = next_obs
        total_reward += reward
        steps += 1

        if done:
            break

    rewards_per_episode.append(total_reward)
    steps_per_episode.append(steps)
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

print(f"\n训练完成 (Training complete): {num_episodes} episodes")
print(f"最后 50 episodes 平均奖励: {np.mean(rewards_per_episode[-50:]):.3f}")
print(f"最后 50 episodes 平均步数: {np.mean(steps_per_episode[-50:]):.1f}")

# 可视化训练曲线 (Visualize training curves)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# 奖励曲线 (Reward curve)
window = 20
rewards_smooth = np.convolve(rewards_per_episode, np.ones(window)/window, mode='valid')
ax1.plot(rewards_smooth, color='#3498db', linewidth=1.5)
ax1.set_title("训练奖励曲线 (Training Reward)", fontsize=12)
ax1.set_xlabel("Episode")
ax1.set_ylabel("Total Reward (smoothed)")
ax1.axhline(y=0.9, color='#2ecc71', linestyle='--', alpha=0.5, label='Target')
ax1.legend()

# 步数曲线 (Steps curve)
steps_smooth = np.convolve(steps_per_episode, np.ones(window)/window, mode='valid')
ax2.plot(steps_smooth, color='#e74c3c', linewidth=1.5)
ax2.set_title("每 Episode 步数 (Steps per Episode)", fontsize=12)
ax2.set_xlabel("Episode")
ax2.set_ylabel("Steps (smoothed)")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step3_training_curves.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"✅ 图表已保存: step3_training_curves.png")


# ============================================================
# 步骤 4：Q-Table 可视化与最优策略
# Step 4: Q-Table Visualization and Optimal Policy
# ============================================================

print("\n" + "=" * 60)
print("步骤 4: Q-Table 可视化 (Q-Table Visualization)")
print("=" * 60)

action_symbols = ['→', '↑', '←', '↓']
action_names_cn = ['右', '上', '左', '下']

print("\n学到的 Q-Table (Learned Q-Table):")
print(f"{'State':>6} | {'Right':>8} {'Up':>8} {'Left':>8} {'Down':>8} | Best Action")
print("-" * 70)
for s in range(n_states):
    if s == 5:  # 墙壁 (wall)
        print(f"  {s:>3}  |   WALL                                  |   ▓")
        continue
    q_vals = qtable[s]
    best_a = int(np.argmax(q_vals))
    q_str = " ".join(f"{q:>8.3f}" for q in q_vals)
    print(f"  {s:>3}  | {q_str} | {action_symbols[best_a]} ({action_names_cn[best_a]})")

# 可视化 Q-Table 热力图和策略箭头
# Visualize Q-Table heatmap and policy arrows
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Q-Table 热力图 (Q-Table heatmap)
q_max = np.max(qtable, axis=1).reshape(3, 4)
q_max[1, 1] = np.nan  # 墙壁 (wall)

im = ax1.imshow(q_max, cmap='RdYlGn', aspect='equal')
ax1.set_title("V(s) = max_a Q(s,a)\n状态价值函数", fontsize=12)
for r in range(3):
    for c in range(4):
        s = r * 4 + c
        if s == 5:
            ax1.text(c, r, "WALL", ha='center', va='center', fontsize=10, fontweight='bold')
        elif s == 3:
            ax1.text(c, r, f"GOAL\n{q_max[r,c]:.2f}", ha='center', va='center', fontsize=9)
        elif s == 7:
            ax1.text(c, r, f"CLIFF\n{q_max[r,c]:.2f}", ha='center', va='center', fontsize=9)
        else:
            ax1.text(c, r, f"s={s}\n{q_max[r,c]:.2f}", ha='center', va='center', fontsize=9)
ax1.set_xticks(range(4))
ax1.set_yticks(range(3))
plt.colorbar(im, ax=ax1, shrink=0.8)

# 策略箭头图 (Policy arrow map)
arrow_dx = {0: 0.3, 1: 0, 2: -0.3, 3: 0}
arrow_dy = {0: 0, 1: -0.3, 2: 0, 3: 0.3}

ax2.set_xlim(-0.5, 3.5)
ax2.set_ylim(-0.5, 2.5)
ax2.set_aspect('equal')
ax2.invert_yaxis()
ax2.set_title("最优策略 (Optimal Policy)\n箭头 = argmax_a Q(s,a)", fontsize=12)

for r in range(3):
    for c in range(4):
        s = r * 4 + c
        if s == 5:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='gray', alpha=0.5))
            ax2.text(c, r, "▓", ha='center', va='center', fontsize=16)
        elif s == 3:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#2ecc71', alpha=0.3))
            ax2.text(c, r, "+1", ha='center', va='center', fontsize=14, fontweight='bold', color='green')
        elif s == 7:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#e74c3c', alpha=0.3))
            ax2.text(c, r, "-1", ha='center', va='center', fontsize=14, fontweight='bold', color='red')
        else:
            best_a = int(np.argmax(qtable[s]))
            ax2.arrow(c, r, arrow_dx[best_a], arrow_dy[best_a],
                      head_width=0.12, head_length=0.06, fc='#3498db', ec='#2c3e50', linewidth=1.5)

# 画网格线 (Draw grid lines)
for i in range(5):
    ax2.axvline(x=i-0.5, color='gray', linewidth=0.5, alpha=0.5)
for i in range(4):
    ax2.axhline(y=i-0.5, color='gray', linewidth=0.5, alpha=0.5)
ax2.set_xticks(range(4))
ax2.set_yticks(range(3))

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step4_qtable_policy.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n✅ 图表已保存: step4_qtable_policy.png")


# ============================================================
# 步骤 5：terminated vs truncated 演示
# Step 5: terminated vs truncated Demo
# ============================================================

print("\n" + "=" * 60)
print("步骤 5: terminated vs truncated 区别")
print("=" * 60)

print("""
Gymnasium 的 step() 返回 5 个值:
  observation, reward, terminated, truncated, info

terminated vs truncated 的区别:
┌─────────────┬──────────────────────────────┬──────────────────────────────┐
│             │ terminated                   │ truncated                    │
├─────────────┼──────────────────────────────┼──────────────────────────────┤
│ 含义        │ 任务自然结束                 │ 人为截断                     │
│ 触发条件    │ 到达目标/掉入悬崖            │ 超过 max_episode_steps       │
│ MDP 意义    │ 终止状态 (terminal state)    │ 非 MDP 概念，工程需要        │
│ Q-Learning  │ Q(s_terminal) = 0            │ Q(s) ≠ 0 (状态仍有价值)     │
│ Bootstrap   │ 不需要 (no bootstrap)        │ 需要 (should bootstrap)      │
└─────────────┴──────────────────────────────┴──────────────────────────────┘
""")

# 演示 terminated 场景 (Demo terminated scenario)
env = SimpleGridWorldEnv()
obs, _ = env.reset(seed=0)
print("场景 1: terminated (到达目标)")
# 手动走到目标: 上上右右右
for a in [1, 1, 0, 0, 0]:
    obs, reward, terminated, truncated, _ = env.step(a)
    if terminated:
        print(f"  → State {obs}: terminated={terminated}, truncated={truncated}, reward={reward:+.2f}")
        print(f"  → 任务自然结束: 到达目标!")
        break

# 演示 truncated 概念 (Demo truncated concept)
print("\n场景 2: truncated (超时截断)")
print("  → 当 register() 中设置 max_episode_steps=50 时,")
print("  → 如果 50 步内未到达目标, Gymnasium 自动设置 truncated=True")
print("  → 注意: truncated 由 Gymnasium wrapper 处理, 不需要在 env.step() 中实现")

# 可视化对比 (Visualize comparison)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# terminated 场景
ax1.set_xlim(-0.5, 3.5)
ax1.set_ylim(-0.5, 2.5)
ax1.set_aspect('equal')
ax1.invert_yaxis()
ax1.set_title("terminated=True\n任务自然结束", fontsize=12)

# 画路径
path = [(2,0), (1,0), (0,0), (0,1), (0,2), (0,3)]
for i in range(len(path)-1):
    r1, c1 = path[i]
    r2, c2 = path[i+1]
    ax1.annotate("", xy=(c2, r2), xytext=(c1, r1),
                arrowprops=dict(arrowstyle="->", color='#3498db', lw=2))

# 画网格
for r in range(3):
    for c in range(4):
        s = r * 4 + c
        if s == 5:
            ax1.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='gray', alpha=0.5))
        elif s == 3:
            ax1.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#2ecc71', alpha=0.3))
            ax1.text(c, r, "GOAL", ha='center', va='center', fontsize=10, color='green')
        elif s == 7:
            ax1.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#e74c3c', alpha=0.3))
            ax1.text(c, r, "CLIFF", ha='center', va='center', fontsize=10, color='red')
        elif s == 8:
            ax1.text(c, r, "START", ha='center', va='center', fontsize=10, color='blue')
for i in range(5):
    ax1.axvline(x=i-0.5, color='gray', linewidth=0.5, alpha=0.5)
for i in range(4):
    ax1.axhline(y=i-0.5, color='gray', linewidth=0.5, alpha=0.5)

# truncated 场景
ax2.set_xlim(-0.5, 3.5)
ax2.set_ylim(-0.5, 2.5)
ax2.set_aspect('equal')
ax2.invert_yaxis()
ax2.set_title("truncated=True\n超时截断 (max_episode_steps)", fontsize=12)

# 画随机游走路径
np.random.seed(42)
pos = (2, 0)
random_path = [pos]
for _ in range(8):
    dr, dc = [(0,1),(-1,0),(0,-1),(1,0)][np.random.randint(4)]
    nr, nc = max(0, min(2, pos[0]+dr)), max(0, min(3, pos[1]+dc))
    if nr * 4 + nc != 5:
        pos = (nr, nc)
    random_path.append(pos)

for i in range(len(random_path)-1):
    r1, c1 = random_path[i]
    r2, c2 = random_path[i+1]
    alpha_val = 0.3 + 0.7 * i / len(random_path)
    ax2.annotate("", xy=(c2, r2), xytext=(c1, r1),
                arrowprops=dict(arrowstyle="->", color='#e67e22', lw=1.5, alpha=alpha_val))

ax2.text(1.5, -0.3, "⏰ max_steps reached!", ha='center', fontsize=10, color='#e67e22', fontweight='bold')

for r in range(3):
    for c in range(4):
        s = r * 4 + c
        if s == 5:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='gray', alpha=0.5))
        elif s == 3:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#2ecc71', alpha=0.3))
            ax2.text(c, r, "GOAL", ha='center', va='center', fontsize=10, color='green')
        elif s == 7:
            ax2.add_patch(plt.Rectangle((c-0.4, r-0.4), 0.8, 0.8, color='#e74c3c', alpha=0.3))
            ax2.text(c, r, "CLIFF", ha='center', va='center', fontsize=10, color='red')
        elif s == 8:
            ax2.text(c, r, "START", ha='center', va='center', fontsize=10, color='blue')
for i in range(5):
    ax2.axvline(x=i-0.5, color='gray', linewidth=0.5, alpha=0.5)
for i in range(4):
    ax2.axhline(y=i-0.5, color='gray', linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step5_terminated_vs_truncated.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n✅ 图表已保存: step5_terminated_vs_truncated.png")


# ============================================================
# 步骤 6：观测空间设计对比 — Dict vs Discrete
# Step 6: Observation Space Design — Dict vs Discrete
# ============================================================

print("\n" + "=" * 60)
print("步骤 6: 观测空间设计对比 (Observation Space Design)")
print("=" * 60)

# Dict 观测空间 (Dict observation space)
dict_obs_space = spaces.Dict({
    "agent": spaces.Discrete(12),
    "target": spaces.Discrete(12),
})

# Discrete 观测空间 (Discrete observation space)
# 将 (agent, target) 编码为单一整数: state = agent * 12 + target
discrete_obs_space = spaces.Discrete(12 * 12)  # 144

print(f"\n方式 1: Dict 观测空间")
print(f"  observation_space = Dict(agent=Discrete(12), target=Discrete(12))")
print(f"  总组合数: 12 × 12 = 144")
print(f"  SB3 Policy: MultiInputPolicy")
sample = dict_obs_space.sample()
print(f"  示例: {sample}")

print(f"\n方式 2: Discrete 观测空间")
print(f"  observation_space = Discrete(144)")
print(f"  编码: state = agent_pos * 12 + target_pos")
print(f"  SB3 Policy: MlpPolicy")
agent_pos, target_pos = sample["agent"], sample["target"]
encoded = agent_pos * 12 + target_pos
print(f"  示例: agent={agent_pos}, target={target_pos} → encoded={encoded}")

print(f"\n对比:")
print(f"  ┌──────────────┬─────────────────┬──────────────────┐")
print(f"  │              │ Dict            │ Discrete         │")
print(f"  ├──────────────┼─────────────────┼──────────────────┤")
print(f"  │ 可读性       │ ✅ 高           │ ❌ 低            │")
print(f"  │ Q-Table 兼容 │ ❌ 不直接兼容   │ ✅ 直接索引      │")
print(f"  │ SB3 Policy   │ MultiInputPolicy│ MlpPolicy        │")
print(f"  │ 灵活性       │ ✅ 高           │ ❌ 低            │")
print(f"  └──────────────┴─────────────────┴──────────────────┘")

# 可视化编码对比 (Visualize encoding comparison)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Dict 空间可视化
ax1.set_title("Dict Observation Space\n字典观测空间", fontsize=12)
ax1.set_xlabel("agent position")
ax1.set_ylabel("target position")
# 画一个 12x12 的网格，标注几个示例
grid_data = np.zeros((12, 12))
examples = [(0, 3), (8, 3), (4, 11)]
for a, t in examples:
    grid_data[t, a] = 1
ax1.imshow(grid_data, cmap='Blues', aspect='equal', alpha=0.3)
for a, t in examples:
    ax1.plot(a, t, 'ro', markersize=10)
    ax1.annotate(f"agent={a}\ntarget={t}", (a, t), textcoords="offset points",
                xytext=(15, 5), fontsize=8, color='red')
ax1.set_xticks(range(0, 12, 2))
ax1.set_yticks(range(0, 12, 2))

# Discrete 空间可视化
ax2.set_title("Discrete Observation Space\n离散观测空间 (encoded)", fontsize=12)
encoded_values = []
labels = []
for a, t in examples:
    enc = a * 12 + t
    encoded_values.append(enc)
    labels.append(f"({a},{t})→{enc}")

ax2.barh(range(len(encoded_values)), encoded_values, color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7)
ax2.set_yticks(range(len(labels)))
ax2.set_yticklabels(labels, fontsize=10)
ax2.set_xlabel("Encoded state value")
ax2.set_xlim(0, 144)
ax2.axvline(x=144, color='gray', linestyle='--', alpha=0.5, label='max=143')
ax2.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step6_obs_space_comparison.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n✅ 图表已保存: step6_obs_space_comparison.png")


# ============================================================
# 步骤 7：环境注册与 Wrappers 概念
# Step 7: Environment Registration and Wrappers
# ============================================================

print("\n" + "=" * 60)
print("步骤 7: 环境注册与 Wrappers")
print("=" * 60)

print("""
环境注册流程 (Environment Registration Flow):

1. 创建包目录结构:
   my_env/
   ├── pyproject.toml
   └── my_env/
       ├── __init__.py          ← register() 在这里
       └── envs/
           ├── __init__.py
           └── grid_world.py    ← 环境类在这里

2. __init__.py 中注册:
   from gymnasium.envs.registration import register
   register(
       id="my_env/GridWorld-v0",
       entry_point="my_env.envs:GridWorldEnv",
       max_episode_steps=200,
   )

3. 安装并使用:
   pip install -e .
   env = gym.make("my_env/GridWorld-v0")
""")

# 演示 Gymnasium 内置 Wrappers
# Demo Gymnasium built-in Wrappers
print("常用 Gymnasium Wrappers:")
print("┌────────────────────────┬──────────────────────────────────────┐")
print("│ Wrapper                │ 功能                                 │")
print("├────────────────────────┼──────────────────────────────────────┤")
print("│ TimeLimit              │ 限制最大步数 (max_episode_steps)     │")
print("│ FlattenObservation     │ 将 Dict/Tuple 观测展平为 Box        │")
print("│ RecordVideo            │ 录制环境渲染视频                     │")
print("│ RecordEpisodeStatistics│ 记录 episode 统计信息               │")
print("│ NormalizeObservation   │ 标准化观测值                         │")
print("│ NormalizeReward        │ 标准化奖励值                         │")
print("└────────────────────────┴──────────────────────────────────────┘")

print("""
Wrapper 使用示例:
  env = gym.make("my_env/GridWorld-v0", max_episode_steps=200)
  # ↑ 这会自动包裹 TimeLimit wrapper
  # 当步数超过 200 时, truncated=True
""")


# ============================================================
# 步骤 8：完整 Agent-Environment 交互循环可视化
# Step 8: Complete Agent-Environment Interaction Loop Visualization
# ============================================================

print("\n" + "=" * 60)
print("步骤 8: Agent-Environment 交互循环可视化")
print("=" * 60)

# 用训练好的 Q-table 运行一个完整 episode 并记录轨迹
# Run a complete episode with trained Q-table and record trajectory
env = SimpleGridWorldEnv()
obs, _ = env.reset(seed=0)
trajectory = [(obs, None, None)]

for step in range(20):
    action = int(np.argmax(qtable[obs]))
    next_obs, reward, terminated, truncated, _ = env.step(action)
    trajectory.append((next_obs, action, reward))
    obs = next_obs
    if terminated or truncated:
        break

print(f"\n最优策略轨迹 (Optimal policy trajectory):")
print(f"  起点 → ", end="")
for i, (s, a, r) in enumerate(trajectory):
    if a is not None:
        print(f"[{action_symbols[a]}]→ s{s}(r={r:+.2f}) ", end="")
    if s == 3:
        print("→ 🎯 目标!")
        break
    elif s == 7:
        print("→ 💀 悬崖!")
        break

# 可视化交互循环 (Visualize interaction loop)
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# 画 Agent-Environment 交互图
# Draw Agent-Environment interaction diagram
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Agent-Environment Interaction Loop\n智能体-环境交互循环 (Sutton §3.1)", fontsize=14)

# Agent 框
agent_rect = plt.Rectangle((0.5, 2.5), 3, 2, fill=True, facecolor='#3498db', alpha=0.2, edgecolor='#2c3e50', linewidth=2)
ax.add_patch(agent_rect)
ax.text(2, 3.5, "Agent\n智能体", ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(2, 2.8, "Q-Learning / DQN / PPO", ha='center', va='center', fontsize=9, style='italic', color='gray')

# Environment 框
env_rect = plt.Rectangle((6.5, 2.5), 3, 2, fill=True, facecolor='#2ecc71', alpha=0.2, edgecolor='#2c3e50', linewidth=2)
ax.add_patch(env_rect)
ax.text(8, 3.5, "Environment\n环境", ha='center', va='center', fontsize=13, fontweight='bold')
ax.text(8, 2.8, "gymnasium.Env", ha='center', va='center', fontsize=9, style='italic', color='gray')

# 箭头: action (Agent → Env)
ax.annotate("", xy=(6.5, 4.0), xytext=(3.5, 4.0),
           arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=2.5))
ax.text(5, 4.3, "action $A_t$", ha='center', va='bottom', fontsize=11, color='#e74c3c', fontweight='bold')
ax.text(5, 4.7, "env.step(action)", ha='center', va='bottom', fontsize=9, color='gray', style='italic')

# 箭头: observation, reward (Env → Agent)
ax.annotate("", xy=(3.5, 3.0), xytext=(6.5, 3.0),
           arrowprops=dict(arrowstyle="-|>", color='#8e44ad', lw=2.5))
ax.text(5, 2.3, "$S_{t+1}, R_{t+1}$, terminated, truncated, info", ha='center', va='top', fontsize=10, color='#8e44ad', fontweight='bold')

# 时间步标注
ax.text(5, 1.2, "每个时间步 t 重复此循环\nRepeat this loop at each timestep t", ha='center', va='center',
       fontsize=10, style='italic', color='gray',
       bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='gray', alpha=0.5))

# reset 箭头
ax.annotate("", xy=(8, 5.2), xytext=(8, 4.5),
           arrowprops=dict(arrowstyle="-|>", color='#f39c12', lw=2))
ax.text(8, 5.5, "env.reset(seed=42)", ha='center', va='bottom', fontsize=9, color='#f39c12')
ax.text(8, 6.0, "→ (obs, info)", ha='center', va='bottom', fontsize=9, color='#f39c12')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step8_interaction_loop.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n✅ 图表已保存: step8_interaction_loop.png")

print("\n" + "=" * 60)
print("演示完成! (Demo Complete!)")
print("=" * 60)
print(f"\n所有图表保存在: {OUTPUT_DIR}")
print(f"共 6 张图表:")
print(f"  1. step1_spaces.png — Spaces 类型对比")
print(f"  2. step3_training_curves.png — Q-Learning 训练曲线")
print(f"  3. step4_qtable_policy.png — Q-Table 热力图和最优策略")
print(f"  4. step5_terminated_vs_truncated.png — terminated vs truncated")
print(f"  5. step6_obs_space_comparison.png — 观测空间设计对比")
print(f"  6. step8_interaction_loop.png — Agent-Environment 交互循环")
