"""
Week 4: Introduction to Convolutional Neural Networks (CNNs) - Complete Demo
Demonstrates ANN basics, CNN architecture (convolution, pooling, FC layers),
activation functions, softmax, backpropagation concepts, and performance
evaluation metrics using synthetic data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import ndimage
from scipy.signal import convolve2d
import os

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.path.abspath(".")
OUTPUT_DIR = os.path.join(
    SCRIPT_DIR, "week4_cnn_intro_complete_demo_pages"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FIG_WIDTH = 12
FIG_HEIGHT = 8
DPI = 150
RANDOM_STATE = 42

# CNN参数
# CNN parameters
CONV_FILTER_SIZE = 3
POOL_SIZE = 2
NUM_FILTERS = 4
NUM_CLASSES = 3
LEARNING_RATE = 0.01

# 评估指标
# Evaluation metrics
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 0

np.random.seed(RANDOM_STATE)


# ============================================================
# 辅助函数
# Helper Functions
# ============================================================

def create_simple_image(size=8):
    """Create a tiny image for step-by-step CNN demo."""
    img = np.array([
        [10, 10, 10, 0, 0, 0, 10, 10],
        [10, 80, 80, 0, 0, 80, 80, 10],
        [10, 80, 200, 200, 200, 200, 80, 10],
        [0, 0, 200, 255, 255, 200, 0, 0],
        [0, 0, 200, 255, 255, 200, 0, 0],
        [10, 80, 200, 200, 200, 200, 80, 10],
        [10, 80, 80, 0, 0, 80, 80, 10],
        [10, 10, 10, 0, 0, 0, 10, 10],
    ], dtype=np.float64)
    return img


def relu(x):
    """ReLU activation: max(0, x)."""
    return np.maximum(0, x)


def sigmoid(x):
    """Sigmoid activation: 1 / (1 + exp(-x))."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def softmax(x):
    """Softmax activation for classification output."""
    # 减去最大值防止溢出 / Subtract max to prevent overflow
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


# ============================================================
# 步骤 1：ANN vs CNN — 为什么图像需要CNN
# Step 1: ANN vs CNN — Why Images Need CNNs
# ============================================================

print("=" * 60)
print("Step 1: ANN vs CNN — Why Images Need CNNs")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# ANN示意图 / ANN diagram
ax = axes[0]
ax.set_xlim(0, 5)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title("ANN (Fully Connected)", fontsize=13, fontweight='bold')

# 输入层 / Input layer
ann_layers = [
    (1, [5, 4, 3, 2, 1], '#3498DB', "Input\n(flattened)"),
    (2.5, [4.5, 3.5, 2.5, 1.5], '#E74C3C', "Hidden"),
    (4, [4, 3, 2], '#2ECC71', "Output"),
]
for lx, ys, color, label in ann_layers:
    for y in ys:
        circle = plt.Circle((lx, y), 0.2, color=color, zorder=5)
        ax.add_patch(circle)
    ax.text(lx, 0.3, label, ha='center', fontsize=8)

# 连接线 / Connection lines
for y1 in ann_layers[0][1]:
    for y2 in ann_layers[1][1]:
        ax.plot([1.2, 2.3], [y1, y2], 'gray', alpha=0.2, lw=0.5)
for y1 in ann_layers[1][1]:
    for y2 in ann_layers[2][1]:
        ax.plot([2.7, 3.8], [y1, y2], 'gray', alpha=0.2, lw=0.5)

# 问题说明 / Problem note
ax.text(2.5, 5.8,
        "1000×1000 image = 1,000,000 inputs!\n"
        "→ Billions of weights → overfitting",
        ha='center', fontsize=9, color='red',
        bbox=dict(boxstyle='round', facecolor='#FFECEC'))

# CNN示意图 / CNN diagram
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title("CNN (Convolutional)", fontsize=13, fontweight='bold')

cnn_blocks = [
    (1, 3, 1.5, 2.5, '#3498DB', "Input\nImage"),
    (3, 3, 1.2, 2.0, '#E74C3C', "Conv\n+Pool"),
    (5, 3, 0.9, 1.5, '#E67E22', "Conv\n+Pool"),
    (7, 3, 0.3, 1.5, '#9B59B6', "FC"),
    (8.5, 3, 0.3, 1.0, '#2ECC71', "Out"),
]
for x, y, w, h, color, label in cnn_blocks:
    rect = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.05",
        facecolor=color, edgecolor='black', alpha=0.8
    )
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=8, color='white', fontweight='bold')

arrow_kw = dict(arrowstyle='->', color='#2C3E50', lw=1.5)
for i in range(len(cnn_blocks) - 1):
    x1 = cnn_blocks[i][0] + cnn_blocks[i][2] / 2
    x2 = cnn_blocks[i + 1][0] - cnn_blocks[i + 1][2] / 2
    ax.annotate('', xy=(x2, 3), xytext=(x1, 3),
                arrowprops=arrow_kw)

ax.text(5, 5.8,
        "Shared weights (filters) → few parameters\n"
        "→ Translation invariant → no overfitting",
        ha='center', fontsize=9, color='green',
        bbox=dict(boxstyle='round', facecolor='#ECFFF0'))

plt.suptitle(
    "ANN: Every pixel connects to every neuron (expensive) | "
    "CNN: Shared filters slide across image (efficient)",
    fontsize=11, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step1_ann_vs_cnn.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("ANN problem: 1000x1000 image = 1M inputs")
print("  With 1000 hidden neurons → 1 billion weights!")
print("CNN solution: shared filters, local connections")
print("  A 3x3 filter = only 9 weights, reused everywhere")
print("\nSaved: step1_ann_vs_cnn.png")

# ============================================================
# 步骤 2：卷积层 — 滤波器如何提取特征
# Step 2: Convolutional Layer — How Filters Extract Features
# ============================================================

print("\n" + "=" * 60)
print("Step 2: Convolutional Layer — Filter Feature Extraction")
print("=" * 60)

test_img = create_simple_image()

# 定义不同功能的滤波器 / Define filters with different purposes
filters = {
    "Horizontal\nEdge": np.array([[-1, -1, -1],
                                   [0, 0, 0],
                                   [1, 1, 1]], dtype=np.float64),
    "Vertical\nEdge": np.array([[-1, 0, 1],
                                 [-1, 0, 1],
                                 [-1, 0, 1]], dtype=np.float64),
    "Sharpen": np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]], dtype=np.float64),
    "Blur\n(Average)": np.ones((3, 3), dtype=np.float64) / 9.0,
}

fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH + 1, FIG_HEIGHT + 1))

# 上排：滤波器 / Top row: filters
for i, (name, kernel) in enumerate(filters.items()):
    axes[0, i].set_title(name, fontsize=10, fontweight='bold')
    axes[0, i].imshow(kernel, cmap='RdBu_r', vmin=-2, vmax=2)
    for r in range(3):
        for c in range(3):
            axes[0, i].text(c, r, f"{kernel[r, c]:.1f}",
                            ha='center', va='center', fontsize=8,
                            fontweight='bold')
    axes[0, i].set_xticks([])
    axes[0, i].set_yticks([])
axes[0, 0].set_ylabel("Filters (3×3)", fontsize=11)

# 下排：卷积结果（特征图）/ Bottom row: feature maps
for i, (name, kernel) in enumerate(filters.items()):
    feature_map = convolve2d(test_img, kernel, mode='valid')
    axes[1, i].set_title("Feature Map", fontsize=10, fontweight='bold')
    axes[1, i].imshow(feature_map, cmap='hot')
    axes[1, i].set_xticks([])
    axes[1, i].set_yticks([])
axes[1, 0].set_ylabel("Output", fontsize=11)

plt.suptitle(
    "Convolution: Each filter detects a different feature "
    "(edges, textures, patterns)",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step2_conv_filters.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Each 3×3 filter slides across the image")
print("Output = weighted sum of overlapping region")
print("Different filters → different features detected")
print("\nSaved: step2_conv_filters.png")

# ============================================================
# 步骤 3：步幅和填充对输出尺寸的影响
# Step 3: Stride and Padding — Output Size Formula
# ============================================================

print("\n" + "=" * 60)
print("Step 3: Stride and Padding — Output Size Formula")
print("=" * 60)

# 输出尺寸公式：O = (W - F + 2P) / S + 1
# Output size formula: O = (W - F + 2P) / S + 1
INPUT_SIZE = 8
configs = [
    {"name": "No pad, S=1", "F": 3, "P": 0, "S": 1},
    {"name": "Pad=1, S=1", "F": 3, "P": 1, "S": 1},
    {"name": "No pad, S=2", "F": 3, "P": 0, "S": 2},
    {"name": "F=5, Pad=2, S=1", "F": 5, "P": 2, "S": 1},
]

fig, axes = plt.subplots(1, 4, figsize=(FIG_WIDTH + 2, FIG_HEIGHT // 2 + 1))

for i, cfg in enumerate(configs):
    f = cfg["F"]
    p = cfg["P"]
    s = cfg["S"]
    out = (INPUT_SIZE - f + 2 * p) // s + 1

    ax = axes[i]
    ax.set_title(cfg["name"], fontsize=10, fontweight='bold')

    # 绘制输入网格 / Draw input grid
    padded = INPUT_SIZE + 2 * p
    grid = np.zeros((padded, padded))
    grid[p:p + INPUT_SIZE, p:p + INPUT_SIZE] = 0.5
    ax.imshow(grid, cmap='Blues', vmin=0, vmax=1,
              extent=[0, padded, padded, 0])

    # 绘制滤波器位置 / Draw filter position
    rect = mpatches.Rectangle(
        (p, p), f, f,
        linewidth=2, edgecolor='red', facecolor='red', alpha=0.3
    )
    ax.add_patch(rect)

    ax.text(padded / 2, padded + 0.8,
            f"In={INPUT_SIZE} F={f} P={p} S={s}\n"
            f"Out = ({INPUT_SIZE}-{f}+2×{p})/{s}+1 = {out}",
            ha='center', va='top', fontsize=8,
            bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.set_xlim(-0.5, padded + 0.5)
    ax.set_ylim(padded + 1.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle(
    "Output Size: O = (W − F + 2P) / S + 1",
    fontsize=14, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step3_stride_padding.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Output size formula: O = (W - F + 2P) / S + 1")
for cfg in configs:
    f, p, s = cfg["F"], cfg["P"], cfg["S"]
    out = (INPUT_SIZE - f + 2 * p) // s + 1
    print(f"  {cfg['name']}: ({INPUT_SIZE}-{f}+2*{p})/{s}+1"
          f" = {out}×{out}")
print("\nSaved: step3_stride_padding.png")

# ============================================================
# 步骤 4：池化层（最大池化 vs 平均池化）
# Step 4: Pooling Layers (Max vs Average Pooling)
# ============================================================

print("\n" + "=" * 60)
print("Step 4: Pooling Layers — Downsampling Feature Maps")
print("=" * 60)

# 创建一个特征图 / Create a feature map
feature_map = np.array([
    [1, 3, 2, 4],
    [5, 6, 8, 7],
    [3, 2, 1, 0],
    [9, 4, 7, 5],
], dtype=np.float64)

# 2x2 最大池化 / 2x2 max pooling
max_pooled = np.zeros((2, 2))
avg_pooled = np.zeros((2, 2))
for i in range(2):
    for j in range(2):
        block = feature_map[i * 2:(i + 1) * 2, j * 2:(j + 1) * 2]
        max_pooled[i, j] = block.max()
        avg_pooled[i, j] = block.mean()

fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 1))

# 原始 / Original
axes[0].set_title("Feature Map (4×4)", fontsize=12, fontweight='bold')
axes[0].imshow(feature_map, cmap='YlOrRd', vmin=0, vmax=9)
for r in range(4):
    for c in range(4):
        axes[0].text(c, r, f"{int(feature_map[r, c])}",
                     ha='center', va='center', fontsize=14,
                     fontweight='bold')
# 绘制2x2分块 / Draw 2x2 block boundaries
axes[0].axhline(1.5, color='blue', linewidth=2)
axes[0].axvline(1.5, color='blue', linewidth=2)

# 最大池化 / Max pooling
axes[1].set_title("Max Pool (2×2)", fontsize=12, fontweight='bold')
axes[1].imshow(max_pooled, cmap='YlOrRd', vmin=0, vmax=9)
for r in range(2):
    for c in range(2):
        axes[1].text(c, r, f"{int(max_pooled[r, c])}",
                     ha='center', va='center', fontsize=18,
                     fontweight='bold')

# 平均池化 / Average pooling
axes[2].set_title("Avg Pool (2×2)", fontsize=12, fontweight='bold')
axes[2].imshow(avg_pooled, cmap='YlOrRd', vmin=0, vmax=9)
for r in range(2):
    for c in range(2):
        axes[2].text(c, r, f"{avg_pooled[r, c]:.1f}",
                     ha='center', va='center', fontsize=18,
                     fontweight='bold')

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])

plt.suptitle(
    "Pooling: Reduces spatial size while keeping important info "
    "(Max = strongest signal, Avg = smooth summary)",
    fontsize=11, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step4_pooling.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Max Pooling: takes maximum value in each 2×2 block")
print("Avg Pooling: takes average value in each 2×2 block")
print(f"Input: 4×4 → Output: 2×2 (reduced by factor of {POOL_SIZE})")
print("\nSaved: step4_pooling.png")

# ============================================================
# 步骤 5：激活函数（ReLU, Sigmoid, Softmax）
# Step 5: Activation Functions (ReLU, Sigmoid, Softmax)
# ============================================================

print("\n" + "=" * 60)
print("Step 5: Activation Functions — Adding Nonlinearity")
print("=" * 60)

x = np.linspace(-5, 5, 200)

fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 1))

# ReLU
axes[0].set_title("ReLU: max(0, x)", fontsize=12, fontweight='bold')
axes[0].plot(x, relu(x), color='#E74C3C', linewidth=2.5)
axes[0].axhline(0, color='gray', linewidth=0.5)
axes[0].axvline(0, color='gray', linewidth=0.5)
axes[0].fill_between(x, relu(x), alpha=0.1, color='#E74C3C')
axes[0].set_xlabel("Input")
axes[0].set_ylabel("Output")
axes[0].text(2.5, 4.5, "Most used in\nhidden layers",
             fontsize=9, ha='center',
             bbox=dict(facecolor='lightyellow', alpha=0.9))
axes[0].grid(True, alpha=0.3)

# Sigmoid
axes[1].set_title("Sigmoid: 1/(1+e⁻ˣ)", fontsize=12, fontweight='bold')
axes[1].plot(x, sigmoid(x), color='#3498DB', linewidth=2.5)
axes[1].axhline(0.5, color='gray', linewidth=0.5, linestyle='--')
axes[1].axvline(0, color='gray', linewidth=0.5)
axes[1].fill_between(x, sigmoid(x), alpha=0.1, color='#3498DB')
axes[1].set_xlabel("Input")
axes[1].set_ylim(-0.1, 1.1)
axes[1].text(2.5, 0.2, "Output: [0, 1]\nBinary class.",
             fontsize=9, ha='center',
             bbox=dict(facecolor='lightyellow', alpha=0.9))
axes[1].grid(True, alpha=0.3)

# Softmax
logits = np.array([2.0, 1.0, 0.5])
probs = softmax(logits)
classes = ['Cat', 'Dog', 'Bird']
colors = ['#E74C3C', '#3498DB', '#2ECC71']
axes[2].set_title("Softmax (multi-class)", fontsize=12, fontweight='bold')
bars = axes[2].bar(classes, probs, color=colors, edgecolor='black')
for bar, p in zip(bars, probs):
    axes[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                 f"{p:.2f}", ha='center', fontsize=11, fontweight='bold')
axes[2].set_ylabel("Probability")
axes[2].set_ylim(0, 1.0)
axes[2].text(1, 0.85, f"logits: {logits.tolist()}\n→ sum=1.0",
             ha='center', fontsize=9,
             bbox=dict(facecolor='lightyellow', alpha=0.9))

plt.suptitle(
    "Activation Functions: Introduce nonlinearity "
    "so networks can learn complex patterns",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step5_activations.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("ReLU: max(0, x) — most common in hidden layers")
print("Sigmoid: 1/(1+e^-x) — output in [0,1], binary classification")
print(f"Softmax: logits {logits.tolist()} → probabilities "
      f"{[f'{p:.3f}' for p in probs]} (sum=1)")
print("\nSaved: step5_activations.png")

# ============================================================
# 步骤 6：完整CNN前向传播演示
# Step 6: Complete CNN Forward Pass Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 6: CNN Forward Pass — Input to Prediction")
print("=" * 60)

input_img = create_simple_image()

# 阶段1：卷积 / Stage 1: Convolution
edge_filter = np.array([[-1, -1, -1],
                         [0, 0, 0],
                         [1, 1, 1]], dtype=np.float64)
conv_output = convolve2d(input_img, edge_filter, mode='valid')

# 阶段2：ReLU / Stage 2: ReLU activation
relu_output = relu(conv_output)

# 阶段3：最大池化 / Stage 3: Max pooling
pool_h = relu_output.shape[0] // POOL_SIZE
pool_w = relu_output.shape[1] // POOL_SIZE
pool_output = np.zeros((pool_h, pool_w))
for i in range(pool_h):
    for j in range(pool_w):
        block = relu_output[
            i * POOL_SIZE:(i + 1) * POOL_SIZE,
            j * POOL_SIZE:(j + 1) * POOL_SIZE
        ]
        pool_output[i, j] = block.max()

# 阶段4：展平 / Stage 4: Flatten
flat = pool_output.flatten()

# 阶段5：全连接 + Softmax / Stage 5: FC + Softmax
np.random.seed(RANDOM_STATE)
fc_weights = np.random.randn(NUM_CLASSES, len(flat)) * 0.1
fc_bias = np.zeros(NUM_CLASSES)
fc_output = fc_weights @ flat + fc_bias
probs = softmax(fc_output)

fig, axes = plt.subplots(2, 3, figsize=(FIG_WIDTH, FIG_HEIGHT + 1))

axes[0, 0].set_title("1. Input (8×8)", fontsize=11, fontweight='bold')
axes[0, 0].imshow(input_img, cmap='gray', vmin=0, vmax=255)

axes[0, 1].set_title("2. Conv (6×6)", fontsize=11, fontweight='bold')
axes[0, 1].imshow(conv_output, cmap='RdBu_r')

axes[0, 2].set_title("3. ReLU (6×6)", fontsize=11, fontweight='bold')
axes[0, 2].imshow(relu_output, cmap='hot')

axes[1, 0].set_title("4. MaxPool (3×3)", fontsize=11, fontweight='bold')
axes[1, 0].imshow(pool_output, cmap='hot')
for r in range(pool_h):
    for c in range(pool_w):
        axes[1, 0].text(c, r, f"{pool_output[r, c]:.0f}",
                        ha='center', va='center', fontsize=10,
                        color='white', fontweight='bold')

axes[1, 1].set_title(f"5. Flatten ({len(flat)})", fontsize=11,
                     fontweight='bold')
axes[1, 1].barh(range(len(flat)), flat, color='#3498DB')
axes[1, 1].set_xlabel("Value")
axes[1, 1].set_ylabel("Index")
axes[1, 1].invert_yaxis()

axes[1, 2].set_title("6. Softmax Output", fontsize=11, fontweight='bold')
class_names = ['Class A', 'Class B', 'Class C']
bar_colors = ['#E74C3C', '#3498DB', '#2ECC71']
bars = axes[1, 2].bar(class_names, probs, color=bar_colors)
for bar, p in zip(bars, probs):
    axes[1, 2].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        f"{p:.3f}", ha='center', fontsize=10, fontweight='bold'
    )
axes[1, 2].set_ylim(0, 0.6)
axes[1, 2].set_ylabel("Probability")

for ax in axes.flat:
    if len(ax.images) > 0:
        ax.set_xticks([])
        ax.set_yticks([])

plt.suptitle(
    "CNN Forward Pass: "
    "Input → Conv → ReLU → Pool → Flatten → FC → Softmax",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step6_forward_pass.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Forward pass pipeline:")
print(f"  Input: {input_img.shape}")
print(f"  After Conv (3×3): {conv_output.shape}")
print(f"  After ReLU: {relu_output.shape} (negatives → 0)")
print(f"  After MaxPool (2×2): {pool_output.shape}")
print(f"  After Flatten: ({len(flat)},)")
print(f"  After FC + Softmax: {probs.round(3)}")
pred_class = class_names[np.argmax(probs)]
print(f"  Prediction: {pred_class} ({probs.max():.3f})")
print("\nSaved: step6_forward_pass.png")

# ============================================================
# 步骤 7：反向传播概念
# Step 7: Backpropagation Concept
# ============================================================

print("\n" + "=" * 60)
print("Step 7: Backpropagation — How CNNs Learn")
print("=" * 60)

fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

# 前向传播箭头 / Forward pass
fwd_boxes = [
    (1.5, 4.5, "Input", '#3498DB'),
    (4, 4.5, "Conv+Pool", '#E74C3C'),
    (6.5, 4.5, "FC Layer", '#9B59B6'),
    (9, 4.5, "Output", '#2ECC71'),
]
for x, y, text, color in fwd_boxes:
    rect = mpatches.FancyBboxPatch(
        (x - 0.9, y - 0.4), 1.8, 0.8,
        boxstyle="round,pad=0.1",
        facecolor=color, edgecolor='black', alpha=0.85
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

# 前向箭头 / Forward arrows
for i in range(3):
    ax.annotate('', xy=(fwd_boxes[i + 1][0] - 0.9, 4.5),
                xytext=(fwd_boxes[i][0] + 0.9, 4.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(6, 5.3, "Forward Pass →", fontsize=12,
        ha='center', fontweight='bold', color='#2C3E50')

# 损失计算 / Loss calculation
ax.text(10.5, 4.5, "Loss\n(error)", ha='center', va='center',
        fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#F39C12', alpha=0.9))
ax.annotate('', xy=(10, 4.5), xytext=(9.9, 4.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

# 反向传播箭头 / Backward arrows
for i in range(3, 0, -1):
    ax.annotate('', xy=(fwd_boxes[i - 1][0] + 0.9, 2.5),
                xytext=(fwd_boxes[i][0] - 0.9, 2.5),
                arrowprops=dict(arrowstyle='->',
                                color='red', lw=2, ls='--'))
ax.annotate('', xy=(fwd_boxes[3][0] + 0.9, 2.5),
            xytext=(10.5, 3.8),
            arrowprops=dict(arrowstyle='->',
                            color='red', lw=2, ls='--'))
ax.text(6, 2.0, "← Backpropagation (compute gradients)",
        fontsize=12, ha='center', fontweight='bold', color='red')

# 权重更新 / Weight update
ax.text(6, 1.0,
        "Weight Update: W_new = W_old − lr × ∂Loss/∂W\n"
        f"Learning Rate (lr) = {LEARNING_RATE}",
        ha='center', va='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightyellow'))

ax.set_title("Backpropagation: Compute gradients → Update weights "
             "→ Reduce loss", fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step7_backpropagation.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Backpropagation steps:")
print("  1. Forward pass: compute prediction")
print("  2. Compute loss (error between prediction and truth)")
print("  3. Backward pass: compute gradient of loss w.r.t. weights")
print("  4. Update weights: W_new = W_old - lr × gradient")
print(f"  Learning rate: {LEARNING_RATE}")
print("\nSaved: step7_backpropagation.png")

# ============================================================
# 步骤 8：混淆矩阵与评估指标
# Step 8: Confusion Matrix and Evaluation Metrics
# ============================================================

print("\n" + "=" * 60)
print("Step 8: Confusion Matrix & Evaluation Metrics")
print("=" * 60)

# 模拟分类结果 / Simulate classification results
y_true = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                   1, 1, 0, 0, 1, 0, 1, 0, 1, 0])
y_pred = np.array([1, 1, 1, 0, 1, 0, 0, 1, 0, 0,
                   1, 0, 0, 1, 1, 0, 1, 0, 0, 0])

# 手动计算混淆矩阵 / Manually compute confusion matrix
TP = np.sum((y_true == 1) & (y_pred == 1))
TN = np.sum((y_true == 0) & (y_pred == 0))
FP = np.sum((y_true == 0) & (y_pred == 1))
FN = np.sum((y_true == 1) & (y_pred == 0))

accuracy = (TP + TN) / len(y_true)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1 = (2 * precision * recall / (precision + recall)
      if (precision + recall) > 0 else 0)

cm = np.array([[TN, FP], [FN, TP]])

fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH + 1, FIG_HEIGHT // 2 + 2))

# 混淆矩阵 / Confusion matrix
axes[0].set_title("Confusion Matrix", fontsize=12, fontweight='bold')
im = axes[0].imshow(cm, cmap='Blues', vmin=0,
                    vmax=max(TP, TN, FP, FN) + 1)
labels = [['TN', 'FP'], ['FN', 'TP']]
cm_colors = [['#2ECC71', '#E74C3C'], ['#E74C3C', '#2ECC71']]
for i in range(2):
    for j in range(2):
        axes[0].text(j, i,
                     f"{labels[i][j]}\n{cm[i, j]}",
                     ha='center', va='center', fontsize=14,
                     fontweight='bold', color=cm_colors[i][j])
axes[0].set_xticks([0, 1])
axes[0].set_yticks([0, 1])
axes[0].set_xticklabels(['Pred Neg', 'Pred Pos'])
axes[0].set_yticklabels(['True Neg', 'True Pos'])

# 指标柱状图 / Metrics bar chart
metrics = {'Accuracy': accuracy, 'Precision': precision,
           'Recall': recall, 'F1 Score': f1}
m_colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
axes[1].set_title("Metric Values", fontsize=12, fontweight='bold')
bars = axes[1].bar(metrics.keys(), metrics.values(), color=m_colors)
for bar, v in zip(bars, metrics.values()):
    axes[1].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.02,
                 f"{v:.2f}", ha='center', fontsize=11,
                 fontweight='bold')
axes[1].set_ylim(0, 1.15)
axes[1].set_ylabel("Score")

# 公式说明 / Formulas
axes[2].set_title("Metric Formulas", fontsize=12, fontweight='bold')
axes[2].axis('off')
formula_text = (
    f"TP={TP}  TN={TN}  FP={FP}  FN={FN}\n"
    f"Total = {len(y_true)}\n\n"
    f"Accuracy = (TP+TN)/Total\n"
    f"  = ({TP}+{TN})/{len(y_true)} = {accuracy:.2f}\n\n"
    f"Precision = TP/(TP+FP)\n"
    f"  = {TP}/({TP}+{FP}) = {precision:.2f}\n\n"
    f"Recall = TP/(TP+FN)\n"
    f"  = {TP}/({TP}+{FN}) = {recall:.2f}\n\n"
    f"F1 = 2×P×R/(P+R)\n"
    f"  = {f1:.2f}"
)
axes[2].text(0.5, 0.5, formula_text, ha='center', va='center',
             fontsize=10, fontfamily='monospace',
             transform=axes[2].transAxes,
             bbox=dict(boxstyle='round', facecolor='lightyellow'))

plt.suptitle(
    "Performance Metrics: "
    "How to evaluate a CNN classifier",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step8_metrics.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print(f"TP={TP}, TN={TN}, FP={FP}, FN={FN}")
print(f"Accuracy:  {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall:    {recall:.2f}")
print(f"F1 Score:  {f1:.2f}")
print("\nSaved: step8_metrics.png")

# ============================================================
# 步骤 9：ROC曲线与AUC
# Step 9: ROC Curve and AUC
# ============================================================

print("\n" + "=" * 60)
print("Step 9: ROC Curve and AUC")
print("=" * 60)

# 模拟预测概率 / Simulate prediction probabilities
np.random.seed(RANDOM_STATE)
n_samples = 100
y_true_roc = np.concatenate([np.ones(50), np.zeros(50)])
# 正类概率更高，负类概率更低（模拟好的分类器）
# Positive class gets higher scores (simulating good classifier)
scores_pos = np.random.beta(5, 2, 50)
scores_neg = np.random.beta(2, 5, 50)
y_scores = np.concatenate([scores_pos, scores_neg])

# 手动计算ROC曲线 / Manually compute ROC curve
thresholds = np.linspace(1, 0, 200)
tpr_list = []
fpr_list = []
for t in thresholds:
    preds = (y_scores >= t).astype(int)
    tp = np.sum((preds == 1) & (y_true_roc == 1))
    fp = np.sum((preds == 1) & (y_true_roc == 0))
    fn = np.sum((preds == 0) & (y_true_roc == 1))
    tn = np.sum((preds == 0) & (y_true_roc == 0))
    tpr_list.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    fpr_list.append(fp / (fp + tn) if (fp + tn) > 0 else 0)

# AUC（梯形法）/ AUC (trapezoidal rule)
auc = np.trapz(tpr_list, fpr_list)
auc = abs(auc)

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# ROC曲线 / ROC curve
axes[0].set_title("ROC Curve", fontsize=13, fontweight='bold')
axes[0].plot(fpr_list, tpr_list, color='#E74C3C', linewidth=2.5,
             label=f'CNN (AUC = {auc:.2f})')
axes[0].plot([0, 1], [0, 1], 'k--', alpha=0.5,
             label='Random (AUC = 0.50)')
axes[0].fill_between(fpr_list, tpr_list, alpha=0.15,
                     color='#E74C3C')
axes[0].set_xlabel("False Positive Rate (FPR)", fontsize=11)
axes[0].set_ylabel("True Positive Rate (TPR)", fontsize=11)
axes[0].legend(fontsize=10, loc='lower right')
axes[0].grid(True, alpha=0.3)
axes[0].set_xlim(-0.02, 1.02)
axes[0].set_ylim(-0.02, 1.02)

# AUC解释 / AUC interpretation
axes[1].set_title("AUC Interpretation", fontsize=13, fontweight='bold')
axes[1].axis('off')
auc_text = (
    "ROC = Receiver Operating Characteristic\n"
    "AUC = Area Under the Curve\n\n"
    "X-axis: False Positive Rate\n"
    "  FPR = FP / (FP + TN)\n\n"
    "Y-axis: True Positive Rate\n"
    "  TPR = TP / (TP + FN) = Recall\n\n"
    "AUC Ranges:\n"
    "  0.90-1.00 = Excellent\n"
    "  0.80-0.90 = Good\n"
    "  0.70-0.80 = Fair\n"
    "  0.60-0.70 = Poor\n"
    "  0.50-0.60 = Random"
)
axes[1].text(0.5, 0.5, auc_text, ha='center', va='center',
             fontsize=10, fontfamily='monospace',
             transform=axes[1].transAxes,
             bbox=dict(boxstyle='round', facecolor='lightyellow'))

plt.suptitle(
    "ROC-AUC: Evaluate classifier performance across "
    "all thresholds",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step9_roc_auc.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print(f"ROC AUC: {auc:.2f}")
print("AUC = 1.0 → perfect classifier")
print("AUC = 0.5 → random guessing")
print("\nSaved: step9_roc_auc.png")

# ============================================================
# 步骤 10：CNN架构总览
# Step 10: CNN Architecture Overview
# ============================================================

print("\n" + "=" * 60)
print("Step 10: CNN Architecture Overview")
print("=" * 60)

fig, ax = plt.subplots(figsize=(FIG_WIDTH + 1, FIG_HEIGHT // 2 + 2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 5)
ax.axis('off')

# CNN流水线 / CNN pipeline
pipeline = [
    (1.0, 3.0, 1.4, 2.0, "Input\nImage", '#3498DB'),
    (3.0, 3.0, 1.4, 1.6, "Conv\nLayer", '#E74C3C'),
    (4.6, 3.0, 0.8, 0.6, "ReLU", '#E67E22'),
    (5.8, 3.0, 1.2, 1.2, "Pool\nLayer", '#9B59B6'),
    (7.4, 3.0, 1.4, 1.6, "Conv\nLayer", '#E74C3C'),
    (9.0, 3.0, 0.8, 0.6, "ReLU", '#E67E22'),
    (10.2, 3.0, 1.2, 0.8, "Pool\nLayer", '#9B59B6'),
    (11.6, 3.0, 0.6, 1.0, "Flat", '#1ABC9C'),
    (12.6, 3.0, 0.8, 1.2, "FC\n+ Softmax", '#2ECC71'),
]

for x, y, w, h, text, color in pipeline:
    rect = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.05",
        facecolor=color, edgecolor='black', alpha=0.85
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=8, fontweight='bold', color='white')

# 箭头 / Arrows
for i in range(len(pipeline) - 1):
    x1 = pipeline[i][0] + pipeline[i][2] / 2
    x2 = pipeline[i + 1][0] - pipeline[i + 1][2] / 2
    ax.annotate('', xy=(x2, 3.0), xytext=(x1, 3.0),
                arrowprops=dict(arrowstyle='->', color='#2C3E50',
                                lw=1.5))

# 标注层的功能 / Annotate layer purposes
annotations = [
    (2.0, 1.0, "Feature\nExtraction", '#E74C3C'),
    (7.0, 1.0, "Deeper\nFeatures", '#E74C3C'),
    (12.1, 1.0, "Classification", '#2ECC71'),
]
for x, y, text, color in annotations:
    ax.text(x, y, text, ha='center', va='center',
            fontsize=9, color=color, fontweight='bold')

ax.set_title(
    "Typical CNN Architecture: "
    "[Conv → ReLU → Pool] × N → Flatten → FC → Softmax",
    fontsize=13, fontweight='bold', pad=15
)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step10_cnn_architecture.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Typical CNN structure:")
print("  [Conv → ReLU → Pool] × N → Flatten → FC → Softmax")
print("  Conv: extract features (edges → textures → objects)")
print("  Pool: reduce size, keep important info")
print("  FC: combine all features for classification")
print("  Softmax: output probabilities for each class")
print("\nSaved: step10_cnn_architecture.png")

# ============================================================
# 完成
# Done
# ============================================================

print("\n" + "=" * 60)
print("All demos completed successfully!")
print(f"Output directory: {OUTPUT_DIR}")
print("=" * 60)
