"""
Week 4 — Three Parallelism Strategies & NAS Methods Comparison
生成两张图:
  1. 数据并行 / 模型并行 / 流水线并行 对比
  2. NAS 三种方法 (RL / Evolutionary / DARTS) 雷达对比
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── 公共设置 ──
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
})
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ====================================================================
# 图 1: 三种并行化策略对比
# ====================================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
fig.suptitle("Three Parallelism Strategies\n三种并行化策略", fontsize=15, fontweight="bold", y=1.02)

colors = {
    "data":   ["#4FC3F7", "#29B6F6", "#039BE5"],
    "model":  ["#81C784", "#66BB6A", "#43A047"],
    "pipe":   ["#FFB74D", "#FFA726", "#FB8C00"],
    "gpu":    "#E0E0E0",
}

# --- 1a) Data Parallelism ---
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title("① Data Parallelism\n数据并行", fontsize=12, fontweight="bold")
ax.axis("off")

# Data splits
for i, (y, label) in enumerate([(7.5, "Batch 1"), (5.0, "Batch 2"), (2.5, "Batch 3")]):
    ax.add_patch(mpatches.FancyBboxPatch((0.5, y - 0.6), 3, 1.2, 
                 boxstyle="round,pad=0.1", facecolor=colors["data"][i], edgecolor="none", alpha=0.85))
    ax.text(2, y, label, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    # Arrow
    ax.annotate("", xy=(5.5, y), xytext=(3.8, y),
                arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))
    # GPU box with same model
    ax.add_patch(mpatches.FancyBboxPatch((5.5, y - 0.6), 3.5, 1.2,
                 boxstyle="round,pad=0.1", facecolor=colors["gpu"], edgecolor="#999"))
    ax.text(7.25, y + 0.15, f"GPU {i+1}", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(7.25, y - 0.25, "Model Copy", ha="center", va="center", fontsize=7.5, color="#555")

ax.text(5, 0.7, "All-Reduce 梯度汇总", ha="center", va="center", fontsize=8, 
        style="italic", color="#D32F2F", fontweight="bold")

# --- 1b) Model Parallelism ---
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title("② Model Parallelism\n模型并行", fontsize=12, fontweight="bold")
ax.axis("off")

layers = [("Layer 1-2", 7.5), ("Layer 3-4", 5.0), ("Layer 5-6", 2.5)]
for i, (label, y) in enumerate(layers):
    ax.add_patch(mpatches.FancyBboxPatch((1, y - 0.6), 8, 1.2,
                 boxstyle="round,pad=0.1", facecolor=colors["model"][i], edgecolor="none", alpha=0.85))
    ax.text(5, y + 0.15, f"GPU {i+1}: {label}", ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    ax.text(5, y - 0.25, "模型的不同层", ha="center", va="center", fontsize=7.5, color="white")
    if i < len(layers) - 1:
        ax.annotate("", xy=(5, y - 0.8), xytext=(5, y - 1.4),
                    arrowprops=dict(arrowstyle="->", color="#555", lw=1.5))

ax.text(5, 0.7, "相同数据，不同模型层", ha="center", va="center", fontsize=8,
        style="italic", color="#D32F2F", fontweight="bold")

# --- 1c) Pipeline Parallelism ---
ax = axes[2]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title("③ Pipeline Parallelism\n流水线并行", fontsize=12, fontweight="bold")
ax.axis("off")

pipe_colors = ["#E1BEE7", "#CE93D8", "#AB47BC", "#7B1FA2"]
# Time steps along x, GPUs along y
gpu_labels = ["GPU 1", "GPU 2", "GPU 3", "GPU 4"]
time_labels = ["t₁", "t₂", "t₃", "t₄"]

for gi in range(4):
    y = 8 - gi * 2
    ax.text(0.5, y, gpu_labels[gi], ha="center", va="center", fontsize=8, fontweight="bold")
    for ti in range(4):
        if ti >= gi:
            batch_id = ti - gi
            x = 2 + ti * 1.9
            ax.add_patch(mpatches.FancyBboxPatch((x - 0.7, y - 0.45), 1.5, 0.9,
                         boxstyle="round,pad=0.05", facecolor=pipe_colors[batch_id], 
                         edgecolor="white", alpha=0.85))
            ax.text(x + 0.05, y, f"B{batch_id+1}", ha="center", va="center", fontsize=8, 
                    fontweight="bold", color="white")

for ti in range(4):
    x = 2 + ti * 1.9 + 0.05
    ax.text(x, 0.7, time_labels[ti], ha="center", va="center", fontsize=9, color="#555")

ax.text(5, 0.1, "微批次交错，消除气泡", ha="center", va="center", fontsize=8,
        style="italic", color="#D32F2F", fontweight="bold")

plt.tight_layout()
out1 = os.path.join(OUT_DIR, "Week4_parallelism_strategies.png")
plt.savefig(out1, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"[OK] Saved: {out1}")

# ====================================================================
# 图 2: NAS 三种方法雷达对比
# ====================================================================
categories = [
    "Search Speed\n搜索速度",
    "Performance\n最终性能", 
    "Resource Cost\n资源成本(低=好)",
    "Flexibility\n灵活性",
    "Ease of Use\n易用性",
]
N = len(categories)

# Scores (1-5 scale)
scores = {
    "RL-Based NAS\n(NASNet)":        [1, 5, 1, 4, 2],
    "Evolutionary NAS\n(AmoebaNet)":  [2, 4, 2, 5, 3],
    "DARTS\n(Differentiable)":        [5, 4, 5, 3, 4],
}

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # close polygon

fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(polar=True))
fig.suptitle("NAS Methods Comparison — Radar Chart\nNAS 方法雷达对比", 
             fontsize=14, fontweight="bold", y=1.0)

radar_colors = ["#E53935", "#1E88E5", "#43A047"]
for idx, (name, vals) in enumerate(scores.items()):
    vals_closed = vals + vals[:1]
    ax.plot(angles, vals_closed, linewidth=2, label=name, color=radar_colors[idx])
    ax.fill(angles, vals_closed, alpha=0.12, color=radar_colors[idx])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=9)
ax.set_ylim(0, 5.5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=7, color="#888")
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=9)

out2 = os.path.join(OUT_DIR, "Week4_nas_comparison.png")
plt.savefig(out2, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"[OK] Saved: {out2}")

# ====================================================================
# 图 3: DDP vs FSDP 对比示意
# ====================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("DDP vs FSDP — PyTorch Distributed Training\nPyTorch 分布式训练对比", 
             fontsize=14, fontweight="bold", y=1.02)

# --- DDP ---
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title("DDP (Distributed Data Parallel)\n分布式数据并行", fontsize=11, fontweight="bold")
ax.axis("off")

for i, x in enumerate([1.2, 4.2, 7.2]):
    # GPU box
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.8, 1.5), 2.8, 6.5,
                 boxstyle="round,pad=0.15", facecolor="#E3F2FD", edgecolor="#1565C0", lw=1.5))
    ax.text(x + 0.6, 8.5, f"GPU {i+1}", ha="center", va="center", fontsize=10, fontweight="bold", color="#1565C0")
    # Full model copy
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 5.5), 2.2, 2,
                 boxstyle="round,pad=0.1", facecolor="#42A5F5", edgecolor="none", alpha=0.8))
    ax.text(x + 0.6, 6.5, "Full Model\n完整模型副本", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    # Optimizer state
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 3.5), 2.2, 1.5,
                 boxstyle="round,pad=0.1", facecolor="#66BB6A", edgecolor="none", alpha=0.8))
    ax.text(x + 0.6, 4.25, "Optimizer\n优化器状态", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    # Data shard
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 2), 2.2, 1,
                 boxstyle="round,pad=0.1", facecolor="#FFB74D", edgecolor="none", alpha=0.8))
    ax.text(x + 0.6, 2.5, f"Data {i+1}", ha="center", va="center", fontsize=8, color="white", fontweight="bold")

ax.text(5, 0.5, "⚠️ 模型权重在每个 GPU 上完整复制（冗余）", ha="center", va="center", fontsize=8.5,
        color="#D32F2F", fontweight="bold")

# --- FSDP ---
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.set_title("FSDP (Fully Sharded Data Parallel)\n全分片数据并行", fontsize=11, fontweight="bold")
ax.axis("off")

shard_colors = ["#E1BEE7", "#CE93D8", "#AB47BC"]
for i, x in enumerate([1.2, 4.2, 7.2]):
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.8, 1.5), 2.8, 6.5,
                 boxstyle="round,pad=0.15", facecolor="#F3E5F5", edgecolor="#7B1FA2", lw=1.5))
    ax.text(x + 0.6, 8.5, f"GPU {i+1}", ha="center", va="center", fontsize=10, fontweight="bold", color="#7B1FA2")
    # Model shard
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 5.5), 2.2, 2,
                 boxstyle="round,pad=0.1", facecolor=shard_colors[i], edgecolor="none", alpha=0.8))
    ax.text(x + 0.6, 6.5, f"Model Shard {i+1}\n模型分片 {i+1}", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    # Optimizer shard
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 3.5), 2.2, 1.5,
                 boxstyle="round,pad=0.1", facecolor="#66BB6A", edgecolor="none", alpha=0.6))
    ax.text(x + 0.6, 4.25, f"Opt Shard {i+1}\n优化器分片", ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    # Data shard
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.5, 2), 2.2, 1,
                 boxstyle="round,pad=0.1", facecolor="#FFB74D", edgecolor="none", alpha=0.8))
    ax.text(x + 0.6, 2.5, f"Data {i+1}", ha="center", va="center", fontsize=8, color="white", fontweight="bold")

ax.text(5, 0.5, "✅ 参数+优化器+梯度均分片，内存效率极高", ha="center", va="center", fontsize=8.5,
        color="#2E7D32", fontweight="bold")

plt.tight_layout()
out3 = os.path.join(OUT_DIR, "Week4_ddp_vs_fsdp.png")
plt.savefig(out3, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"[OK] Saved: {out3}")

print("\n[ALL DONE] Generated 3 images for Week 4 storyline.")
