"""
Generate 4 visualization charts for RL Final Review storyline.
生成 RL 期末复习故事线的 4 张可视化图表。

Charts:
1. State Space Explosion — Q-Table vs DQN scalability
2. Curriculum Learning — Difficulty progression & reward curve
3. DQN Network Architecture — [512,512,256] structure diagram
4. RL Evolution Roadmap — Technology progression comparison
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
plt.style.use("seaborn-v0_8-whitegrid")

# ============================================================
# Chart 1: State Space Explosion
# 图1：状态空间爆炸 — Q-Table 的致命缺陷
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
blocks = np.arange(1, 8)
positions = 12  # 6 ground + 6 on-top
state_counts = positions ** blocks

ax.bar(blocks, state_counts, color="#4C72B0", edgecolor="white", linewidth=0.8, alpha=0.85)
ax.set_xlabel("Number of Blocks", fontsize=12)
ax.set_ylabel("Number of States", fontsize=12)
ax.set_title("State Space Explosion in Block-Stacking\n(each block has 12 possible positions)", fontsize=13, fontweight="bold")
ax.set_xticks(blocks)
ax.set_xticklabels([f"{b} blocks" for b in blocks])

# Annotate key points
for i, (b, s) in enumerate(zip(blocks, state_counts)):
    if b <= 4:
        ax.annotate(f"{s:,}", (b, s), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9, color="#333")
    else:
        ax.annotate(f"{s:,.0f}", (b, s), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=9, color="#C44E52", fontweight="bold")

# Draw "Q-Table feasibility" line
ax.axhline(y=100000, color="#C44E52", linestyle="--", linewidth=1.5, alpha=0.7)
ax.text(1.2, 120000, "Q-Table practical limit (~100K states)", fontsize=9,
        color="#C44E52", fontstyle="italic")

ax.set_yscale("log")
ax.set_ylim(1, 1e10)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "state_space_explosion.png"), dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ Chart 1: state_space_explosion.png")

# ============================================================
# Chart 2: Curriculum Learning — Reward Curve
# 图2：课程学习 — 难度递进与奖励曲线
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: Without Curriculum Learning
episodes = np.arange(0, 500)
np.random.seed(42)
no_curriculum_reward = np.random.normal(0, 0.05, len(episodes))
no_curriculum_reward = np.clip(no_curriculum_reward, -0.1, 0.3)
# Smooth
from scipy.ndimage import uniform_filter1d
no_curriculum_smooth = uniform_filter1d(no_curriculum_reward, size=30)

ax1.plot(episodes, no_curriculum_smooth, color="#C44E52", linewidth=2, label="Avg Reward")
ax1.fill_between(episodes, no_curriculum_smooth - 0.03, no_curriculum_smooth + 0.03,
                  color="#C44E52", alpha=0.15)
ax1.set_xlabel("Training Episodes", fontsize=11)
ax1.set_ylabel("Average Reward", fontsize=11)
ax1.set_title("Without Curriculum Learning\n(sparse reward → no learning)", fontsize=12, fontweight="bold", color="#C44E52")
ax1.set_ylim(-0.2, 1.1)
ax1.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
ax1.legend(loc="upper right")

# Right: With Curriculum Learning (3 phases)
phases = [
    (0, 150, "Phase 1\ndifficulty=1\nstart_flat=True", "#55A868"),
    (150, 300, "Phase 2\ndifficulty=2", "#4C72B0"),
    (300, 500, "Phase 3\ndifficulty=5", "#8172B2"),
]

x_all = np.arange(0, 500)
y_all = np.zeros(500)

for start, end, label, color in phases:
    x = np.arange(start, end)
    progress = (x - start) / (end - start)
    y = 0.2 + 0.7 * (1 - np.exp(-3 * progress)) + np.random.normal(0, 0.03, len(x))
    y_all[start:end] = y
    ax2.axvspan(start, end, alpha=0.1, color=color)
    ax2.text((start + end) / 2, 0.05, label, ha="center", fontsize=8, color=color, fontweight="bold")

y_smooth = uniform_filter1d(y_all, size=20)
ax2.plot(x_all, y_smooth, color="#55A868", linewidth=2, label="Avg Reward")
ax2.fill_between(x_all, y_smooth - 0.05, y_smooth + 0.05, color="#55A868", alpha=0.15)
ax2.set_xlabel("Training Episodes", fontsize=11)
ax2.set_ylabel("Average Reward", fontsize=11)
ax2.set_title("With Curriculum Learning\n(progressive difficulty → converges!)", fontsize=12, fontweight="bold", color="#55A868")
ax2.set_ylim(-0.2, 1.1)
ax2.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
ax2.legend(loc="lower right")

fig.suptitle("Curriculum Learning Effect on Training", fontsize=14, fontweight="bold", y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "curriculum_learning_effect.png"), dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ Chart 2: curriculum_learning_effect.png")

# ============================================================
# Chart 3: DQN Network Architecture [512,512,256]
# 图3：DQN 网络架构可视化
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("DQN Q-Network Architecture: [512, 512, 256]\nfor 6-Block Stacking Task (144-dim input)", fontsize=13, fontweight="bold")

layers = [
    (1.5, "Input\n144 dims", 144, "#DCEDC8", "(6 blocks × 12 positions × 2)"),
    (3.5, "Hidden 1\n512 neurons", 512, "#FFE0B2", "Capacity: learn block\nposition patterns"),
    (5.5, "Hidden 2\n512 neurons", 512, "#FFCCBC", "Deeper: learn\ncombination patterns"),
    (7.5, "Hidden 3\n256 neurons", 256, "#D1C4E9", "Refinement:\nstacking logic"),
]

output_layer = (9.2, "Output\nQ-values", 36, "#B3E5FC", "One Q-value\nper action")

# Draw layers as rectangles with height proportional to neuron count
max_neurons = 512
bar_width = 1.2
for x, label, neurons, color, desc in layers:
    h = 4.5 * (neurons / max_neurons)
    y_bottom = 3.5 - h / 2
    rect = plt.Rectangle((x - bar_width/2, y_bottom), bar_width, h,
                          facecolor=color, edgecolor="#555", linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    ax.text(x, y_bottom + h + 0.3, label, ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.text(x, y_bottom - 0.2, desc, ha="center", va="top", fontsize=7.5, color="#666", style="italic")

# Output layer
x, label, neurons, color, desc = output_layer
h = 4.5 * (neurons / max_neurons)
y_bottom = 3.5 - h / 2
rect = plt.Rectangle((x - bar_width/2, y_bottom), bar_width, h,
                      facecolor=color, edgecolor="#555", linewidth=1.5, zorder=2)
ax.add_patch(rect)
ax.text(x, y_bottom + h + 0.3, label, ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.text(x, y_bottom - 0.2, desc, ha="center", va="top", fontsize=7.5, color="#666", style="italic")

# Draw arrows between layers
arrow_style = dict(arrowstyle="->", color="#888", lw=1.5)
for i in range(len(layers) - 1):
    x1 = layers[i][0] + bar_width/2
    x2 = layers[i+1][0] - bar_width/2
    ax.annotate("", xy=(x2, 3.5), xytext=(x1, 3.5), arrowprops=arrow_style)
# Last hidden to output
ax.annotate("", xy=(output_layer[0] - bar_width/2, 3.5),
            xytext=(layers[-1][0] + bar_width/2, 3.5), arrowprops=arrow_style)

# Comparison note
ax.text(5, 0.3, "Default: [64, 64] → Too small for 144-dim input → Cannot learn stacking patterns",
        ha="center", fontsize=9, color="#C44E52", style="italic",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF3E0", edgecolor="#C44E52", alpha=0.8))

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "dqn_network_architecture.png"), dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ Chart 3: dqn_network_architecture.png")

# ============================================================
# Chart 4: RL Methods Comparison — Q-Table vs DQN vs PPO
# 图4：三种方法对比 — 可扩展性与适用场景
# ============================================================
fig, ax = plt.subplots(figsize=(9, 5.5))

methods = ["Q-Table\n(Tabular)", "DQN\n(Value Approx.)", "PPO\n(Policy Gradient)"]
categories = ["Small State Space\n(< 1000)", "Medium State Space\n(1K - 100K)", "Large State Space\n(> 100K)",
              "Continuous Actions", "Training Stability"]

# Scores (0-10) for each method on each category
scores = np.array([
    [10, 4, 0, 0, 9],   # Q-Table
    [7, 9, 8, 3, 6],    # DQN
    [6, 8, 9, 10, 8],   # PPO
])

x = np.arange(len(categories))
width = 0.25
colors = ["#4C72B0", "#55A868", "#8172B2"]

for i, (method, color) in enumerate(zip(methods, colors)):
    bars = ax.bar(x + i * width, scores[i], width, label=method, color=color,
                  edgecolor="white", linewidth=0.8, alpha=0.85)
    for bar, score in zip(bars, scores[i]):
        if score > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                    str(score), ha="center", va="bottom", fontsize=8, fontweight="bold")

ax.set_xlabel("Evaluation Criteria", fontsize=11)
ax.set_ylabel("Score (0-10)", fontsize=11)
ax.set_title("RL Methods Comparison\nQ-Table vs DQN vs PPO", fontsize=13, fontweight="bold")
ax.set_xticks(x + width)
ax.set_xticklabels(categories, fontsize=8.5)
ax.set_ylim(0, 12)
ax.legend(loc="upper right", fontsize=9)

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "rl_methods_comparison.png"), dpi=150, bbox_inches="tight")
plt.close(fig)
print("✅ Chart 4: rl_methods_comparison.png")

print("\n🎉 All 4 charts generated successfully!")
