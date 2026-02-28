"""
Assignment 1: Image Classification Concepts Demo
CST8508 Machine Vision — mmpretrain 核心概念可视化演示

本脚本用合成数据演示 Assignment 1 中涉及的核心概念：
This script demonstrates core concepts from Assignment 1 using synthetic data:
  1. 数据增强效果 / Data augmentation effects
  2. 标准卷积 vs 深度可分离卷积参数量对比 / Standard vs depthwise separable conv
  3. 残差连接 vs 普通网络（退化问题）/ Residual vs plain (degradation)
  4. Softmax + CrossEntropy 损失 / Softmax + CE loss
  5. SGD vs Adam 收敛对比 / SGD vs Adam convergence
  6. 余弦退火学习率 / Cosine annealing LR
  7. 评估指标（混淆矩阵、Per-class Accuracy）/ Evaluation metrics
  8. 训练曲线（模拟 ResNet vs MobileNet）/ Training curves
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    SCRIPT_DIR, "assignment1_mmpretrain_complete_demo_pages"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FIG_WIDTH = 12
FIG_HEIGHT = 8
DPI = 150
RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)


# ============================================================
# 步骤 1：数据增强效果演示
# Step 1: Data Augmentation Effect Demo
# ============================================================

print("=" * 60)
print("Step 1: Data Augmentation — Why It Matters for Small Datasets")
print("=" * 60)

# 创建一张合成"花"图像
# Create a synthetic "flower" image
img_size = 64
flower_img = np.zeros((img_size, img_size, 3))

# 画一个简单的花（绿茎 + 黄色花瓣）
# Draw a simple flower (green stem + yellow petals)
y, x = np.ogrid[:img_size, :img_size]
center = img_size // 2
r = np.sqrt((x - center) ** 2 + (y - center) ** 2)

# 花瓣（黄色圆）/ Petals (yellow circle)
mask_petals = r < 18
flower_img[mask_petals] = [1.0, 0.85, 0.0]

# 花心（棕色小圆）/ Flower center (brown small circle)
mask_center = r < 7
flower_img[mask_center] = [0.55, 0.27, 0.07]

# 茎（绿色线）/ Stem (green line)
flower_img[center:, center - 2:center + 2] = [0.2, 0.7, 0.2]

fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH, FIG_HEIGHT))

# 原图 / Original
axes[0, 0].imshow(flower_img)
axes[0, 0].set_title("Original", fontsize=11, fontweight='bold')

# 模拟各种数据增强 / Simulate data augmentations
# 1. 水平翻转 / Horizontal flip
axes[0, 1].imshow(flower_img[:, ::-1, :])
axes[0, 1].set_title("RandomFlip", fontsize=11, fontweight='bold')

# 2. 随机裁剪 / Random crop
crop_y, crop_x = 8, 12
cropped = flower_img[crop_y:crop_y + 48, crop_x:crop_x + 48, :]
axes[0, 2].imshow(cropped)
axes[0, 2].set_title("RandomCrop", fontsize=11, fontweight='bold')

# 3. 随机旋转 / Random rotation (simulated)
from scipy.ndimage import rotate
rotated = rotate(flower_img, angle=15, reshape=False, mode='constant')
axes[0, 3].imshow(np.clip(rotated, 0, 1))
axes[0, 3].set_title("Rotation (15°)", fontsize=11, fontweight='bold')

# 4. 亮度变化 / Brightness change
axes[1, 0].imshow(np.clip(flower_img * 1.3, 0, 1))
axes[1, 0].set_title("Brighter (+30%)", fontsize=11, fontweight='bold')

axes[1, 1].imshow(np.clip(flower_img * 0.6, 0, 1))
axes[1, 1].set_title("Darker (-40%)", fontsize=11, fontweight='bold')

# 5. 组合增强 / Combined augmentation
combined = rotate(flower_img[:, ::-1, :], angle=-10, reshape=False)
axes[1, 2].imshow(np.clip(combined * 1.2, 0, 1))
axes[1, 2].set_title("Flip+Rotate+Bright", fontsize=11, fontweight='bold')

# 统计信息 / Stats
axes[1, 3].axis('off')
stats_text = (
    "Oxford Flowers 17:\n"
    "  17 categories\n"
    "  ~80 images/class\n"
    "  Train: ~62/class\n"
    "  Val: ~16/class\n\n"
    "Without augmentation:\n"
    "  62 images → high\n"
    "  overfitting risk!\n\n"
    "With augmentation:\n"
    "  Same 62 images look\n"
    "  different each epoch\n"
    "  → Much more diversity"
)
axes[1, 3].text(0.5, 0.5, stats_text, ha='center', va='center',
                fontsize=9, fontfamily='monospace',
                transform=axes[1, 3].transAxes,
                bbox=dict(boxstyle='round', facecolor='lightyellow'))

for ax in axes.flat:
    if ax.images:
        ax.set_xticks([])
        ax.set_yticks([])

plt.suptitle(
    "Data Augmentation: Same image → Many variations "
    "(critical for small datasets)",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step1_data_augmentation.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Oxford Flowers 17: only ~62 training images per class")
print("Data augmentation creates new views each epoch:")
print("  RandomResizedCrop(224) + RandomFlip(prob=0.5)")
print("\nSaved: step1_data_augmentation.png")


# ============================================================
# 步骤 2：标准卷积 vs 深度可分离卷积参数量对比
# Step 2: Standard vs Depthwise Separable Conv Parameter Count
# ============================================================

print("\n" + "=" * 60)
print("Step 2: Standard Conv vs Depthwise Separable Conv")
print("=" * 60)

configs = [
    {"K": 3, "C_in": 32, "C_out": 64},
    {"K": 3, "C_in": 64, "C_out": 128},
    {"K": 3, "C_in": 128, "C_out": 256},
    {"K": 3, "C_in": 256, "C_out": 512},
]

labels = []
standard_params = []
depthwise_params = []

for cfg in configs:
    K, Ci, Co = cfg["K"], cfg["C_in"], cfg["C_out"]
    std = K * K * Ci * Co
    dw = K * K * Ci + Ci * Co
    labels.append(f"{Ci}→{Co}")
    standard_params.append(std)
    depthwise_params.append(dw)

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# 柱状图对比 / Bar chart comparison
x = np.arange(len(labels))
width = 0.35
bars1 = axes[0].bar(x - width / 2, np.array(standard_params) / 1000,
                     width, label='Standard Conv', color='#E74C3C')
bars2 = axes[0].bar(x + width / 2, np.array(depthwise_params) / 1000,
                     width, label='Depthwise Sep.', color='#2ECC71')

axes[0].set_xlabel('Layer (C_in → C_out)', fontsize=11)
axes[0].set_ylabel('Parameters (×1000)', fontsize=11)
axes[0].set_title('Parameter Count Comparison', fontsize=12, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# 节省比例 / Savings ratio
savings = [1 - dw / std for std, dw in zip(standard_params, depthwise_params)]
axes[1].bar(labels, [s * 100 for s in savings], color='#3498DB')
axes[1].set_ylabel('Parameter Savings (%)', fontsize=11)
axes[1].set_title('MobileNet V2 Savings per Layer', fontsize=12,
                  fontweight='bold')
axes[1].set_ylim(0, 100)
for i, s in enumerate(savings):
    axes[1].text(i, s * 100 + 2, f"{s * 100:.1f}%", ha='center',
                 fontsize=10, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.suptitle(
    "ResNet uses Standard Conv | MobileNet V2 uses Depthwise Separable Conv",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step2_conv_comparison.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Parameter comparison (3×3 conv):")
for label, std, dw in zip(labels, standard_params, depthwise_params):
    print(f"  {label}: Standard={std:,} vs Depthwise={dw:,} "
          f"(saves {(1 - dw / std) * 100:.1f}%)")
print("\nSaved: step2_conv_comparison.png")


# ============================================================
# 步骤 3：Softmax + CrossEntropy 演示
# Step 3: Softmax + CrossEntropy Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 3: Softmax + CrossEntropy Loss")
print("=" * 60)


def softmax(z):
    """数值稳定的 Softmax / Numerically stable Softmax."""
    e_z = np.exp(z - np.max(z))
    return e_z / e_z.sum()


# 模拟 3 种预测场景 / Simulate 3 prediction scenarios
scenarios = [
    {"name": "Good prediction\n(high confidence correct)",
     "logits": [3.0, 0.5, -1.0], "true": 0},
    {"name": "Uncertain prediction\n(low confidence correct)",
     "logits": [1.2, 1.0, 0.8], "true": 0},
    {"name": "Wrong prediction\n(high confidence wrong!)",
     "logits": [-0.5, 3.0, 0.5], "true": 0},
]

fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))
colors = ['#2ECC71', '#F39C12', '#E74C3C']
class_names = ['Daisy', 'Tulip', 'Rose']

for i, sc in enumerate(scenarios):
    probs = softmax(np.array(sc["logits"]))
    loss = -np.log(probs[sc["true"]])

    bars = axes[i].bar(class_names, probs,
                       color=['#2ECC71' if j == sc["true"] else '#95A5A6'
                              for j in range(3)],
                       edgecolor='black')
    for bar, p in zip(bars, probs):
        axes[i].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.02,
                     f"{p:.3f}", ha='center', fontsize=10, fontweight='bold')

    axes[i].set_title(sc["name"], fontsize=10, fontweight='bold')
    axes[i].set_ylim(0, 1.1)
    axes[i].text(1, 0.95, f"Loss = {loss:.3f}",
                 ha='center', fontsize=12, fontweight='bold',
                 color=colors[i],
                 bbox=dict(boxstyle='round', facecolor='lightyellow'))

plt.suptitle(
    "CrossEntropy Loss = -log(p_correct)"
    " | Lower = Better | True class: Daisy",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step3_softmax_ce.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

for sc in scenarios:
    probs = softmax(np.array(sc["logits"]))
    loss = -np.log(probs[sc["true"]])
    print(f"  {sc['name'].split(chr(10))[0]}: "
          f"logits={sc['logits']} → probs={probs.round(3)} → loss={loss:.3f}")
print("\nSaved: step3_softmax_ce.png")


# ============================================================
# 步骤 4：SGD vs Adam 收敛对比（2D优化地形）
# Step 4: SGD vs Adam Convergence on 2D Loss Landscape
# ============================================================

print("\n" + "=" * 60)
print("Step 4: SGD vs Adam — Convergence Comparison")
print("=" * 60)

# 模拟一个椭圆形损失面 / Simulate an elliptical loss surface
# f(x,y) = 10*x^2 + y^2（x 方向陡峭，y 方向平缓）


def loss_fn(x, y):
    """椭圆形损失函数 / Elliptical loss function."""
    return 10 * x ** 2 + y ** 2


def grad_fn(x, y):
    """损失函数的梯度 / Gradient of loss function."""
    return np.array([20 * x, 2 * y])


# SGD + Momentum 优化轨迹 / SGD + Momentum trajectory
def sgd_momentum(x0, y0, lr, momentum, steps):
    """SGD 优化器路径 / SGD optimizer path."""
    path = [(x0, y0)]
    v = np.array([0.0, 0.0])
    pos = np.array([x0, y0])
    for _ in range(steps):
        g = grad_fn(pos[0], pos[1])
        v = momentum * v + g
        pos = pos - lr * v
        path.append((pos[0], pos[1]))
    return np.array(path)


# Adam 优化轨迹 / Adam trajectory
def adam(x0, y0, lr, steps):
    """Adam 优化器路径 / Adam optimizer path."""
    path = [(x0, y0)]
    m = np.array([0.0, 0.0])
    v = np.array([0.0, 0.0])
    pos = np.array([x0, y0])
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    for t in range(1, steps + 1):
        g = grad_fn(pos[0], pos[1])
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g ** 2
        m_hat = m / (1 - beta1 ** t)
        v_hat = v / (1 - beta2 ** t)
        pos = pos - lr * m_hat / (np.sqrt(v_hat) + eps)
        path.append((pos[0], pos[1]))
    return np.array(path)


n_steps = 50
sgd_path = sgd_momentum(3.0, 7.0, lr=0.02, momentum=0.9, steps=n_steps)
adam_path = adam(3.0, 7.0, lr=0.3, steps=n_steps)

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# 绘制等高线 / Draw contours
xx, yy = np.meshgrid(np.linspace(-4, 4, 100), np.linspace(-8, 8, 100))
zz = loss_fn(xx, yy)

for ax, path, name, color in [
    (axes[0], sgd_path, "SGD + Momentum\n(lr=0.02, μ=0.9)",
     '#E74C3C'),
    (axes[1], adam_path, "Adam\n(lr=0.3)", '#2ECC71')
]:
    ax.contour(xx, yy, zz, levels=20, cmap='Blues', alpha=0.5)
    ax.plot(path[:, 0], path[:, 1], '-o', color=color,
            markersize=3, linewidth=1.5, alpha=0.8)
    ax.plot(path[0, 0], path[0, 1], 'ko', markersize=8, label='Start')
    ax.plot(0, 0, 'r*', markersize=15, label='Optimum')
    ax.set_title(name, fontsize=11, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend(fontsize=8)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-8, 8)

plt.suptitle(
    "SGD oscillates on steep dimensions | "
    "Adam adapts step size per parameter",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step4_sgd_vs_adam.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print(f"SGD final position: ({sgd_path[-1, 0]:.4f}, {sgd_path[-1, 1]:.4f})")
print(f"Adam final position: ({adam_path[-1, 0]:.4f}, {adam_path[-1, 1]:.4f})")
print("Adam converges faster and more smoothly on asymmetric landscapes")
print("\nSaved: step4_sgd_vs_adam.png")


# ============================================================
# 步骤 5：余弦退火学习率
# Step 5: Cosine Annealing Learning Rate
# ============================================================

print("\n" + "=" * 60)
print("Step 5: Cosine Annealing Learning Rate Schedule")
print("=" * 60)

T_max = 100
epochs = np.arange(0, T_max + 1)

lr_cosine_sgd = 0.01 * 0.5 * (1 + np.cos(np.pi * epochs / T_max))
lr_cosine_adam = 0.001 * 0.5 * (1 + np.cos(np.pi * epochs / T_max))
lr_linear = 0.01 * (1 - epochs / T_max)
lr_step = 0.01 * np.where(epochs < 30, 1, np.where(epochs < 60, 0.1, 0.01))

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# 余弦 vs 其他策略 / Cosine vs other schedules
axes[0].plot(epochs, lr_cosine_sgd, 'r-', linewidth=2.5,
             label='Cosine (used in Assignment 1)')
axes[0].plot(epochs, lr_linear, 'b--', linewidth=1.5, label='Linear Decay')
axes[0].plot(epochs, lr_step, 'g:', linewidth=1.5, label='Step Decay')
axes[0].set_xlabel('Epoch', fontsize=11)
axes[0].set_ylabel('Learning Rate', fontsize=11)
axes[0].set_title('LR Schedules (SGD, initial=0.01)', fontsize=12,
                  fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# ResNet vs MobileNet 的学习率 / ResNet vs MobileNet LR
axes[1].plot(epochs, lr_cosine_sgd, 'r-', linewidth=2,
             label='ResNet-18 (SGD, lr=0.01)')
axes[1].plot(epochs, lr_cosine_adam, 'b-', linewidth=2,
             label='MobileNet V2 (Adam, lr=0.001)')
axes[1].set_xlabel('Epoch', fontsize=11)
axes[1].set_ylabel('Learning Rate', fontsize=11)
axes[1].set_title('Assignment 1: Both Models Use Cosine Annealing',
                  fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle(
    "Cosine Annealing: Start high (explore) → End low (fine-tune)",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step5_cosine_annealing.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Cosine Annealing: η(t) = η_min + 0.5*(η_max-η_min)*(1+cos(πt/T))")
print(f"  Epoch 0:  lr = {lr_cosine_sgd[0]:.4f}")
print(f"  Epoch 50: lr = {lr_cosine_sgd[50]:.4f}")
print(f"  Epoch 100: lr = {lr_cosine_sgd[100]:.6f}")
print("\nSaved: step5_cosine_annealing.png")


# ============================================================
# 步骤 6：训练曲线（模拟 Assignment 1 结果）
# Step 6: Training Curves (Simulating Assignment 1 Results)
# ============================================================

print("\n" + "=" * 60)
print("Step 6: Training Curves — ResNet-18 vs MobileNet V2")
print("=" * 60)

# 真实的 Assignment 1 验证准确率数据 / Actual Assignment 1 val accuracy
resnet_epochs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
resnet_acc = [38.97, 52.57, 60.66, 65.07, 69.49, 72.43, 72.79, 74.63,
              77.21, 76.47]

mobilenet_epochs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
mobilenet_acc = [55.88, 63.60, 70.22, 75.00, 84.93, 85.29, 88.24, 89.71,
                 90.07, 89.71]

fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT // 2 + 2))

# 训练曲线 / Training curves
axes[0].plot(resnet_epochs, resnet_acc, 'ro-', linewidth=2, markersize=6,
             label='ResNet-18 (SGD)')
axes[0].plot(mobilenet_epochs, mobilenet_acc, 'bs-', linewidth=2,
             markersize=6, label='MobileNet V2 (Adam)')
axes[0].set_xlabel('Epoch', fontsize=11)
axes[0].set_ylabel('Top-1 Accuracy (%)', fontsize=11)
axes[0].set_title('Validation Accuracy During Training', fontsize=12,
                  fontweight='bold')
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(30, 100)

# 差距演变 / Gap evolution
gap = [m - r for r, m in zip(resnet_acc, mobilenet_acc)]
axes[1].bar(resnet_epochs, gap, width=8, color='#9B59B6', alpha=0.8)
axes[1].set_xlabel('Epoch', fontsize=11)
axes[1].set_ylabel('MobileNet V2 - ResNet-18 (%)', fontsize=11)
axes[1].set_title('Accuracy Gap (MobileNet V2 Advantage)', fontsize=12,
                  fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

# 标注最大差距 / Annotate max gap
max_gap_idx = np.argmax(gap)
axes[1].text(resnet_epochs[max_gap_idx], gap[max_gap_idx] + 0.5,
             f"Max: +{gap[max_gap_idx]:.1f}%",
             ha='center', fontsize=10, fontweight='bold', color='#9B59B6')

plt.suptitle(
    "Surprising: MobileNet V2 (3.4M params) beats ResNet-18 (11.7M params)!",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step6_training_curves.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("Assignment 1 Results (Best @ Epoch 90):")
print(f"  ResNet-18:    {resnet_acc[-2]}% Top-1")
print(f"  MobileNet V2: {mobilenet_acc[-2]}% Top-1")
print(f"  Gap: +{mobilenet_acc[-2] - resnet_acc[-2]:.2f}% for MobileNet V2")
print("\nSaved: step6_training_curves.png")


# ============================================================
# 步骤 7：评估指标演示
# Step 7: Evaluation Metrics Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 7: Evaluation Metrics — Confusion Matrix & F1")
print("=" * 60)

# 模拟 5 类分类结果 / Simulate 5-class classification
np.random.seed(RANDOM_STATE)
n_classes = 5
class_names_eval = ['Daisy', 'Tulip', 'Rose', 'Sunflower', 'Lily']
n_samples_per_class = 20

# 创建一个"不完美"的混淆矩阵 / Create an imperfect confusion matrix
cm = np.array([
    [18, 1, 0, 1, 0],   # Daisy: 容易识别
    [2, 14, 3, 0, 1],   # Tulip: 常被误判为 Rose
    [0, 4, 15, 0, 1],   # Rose: 和 Tulip 互相混淆
    [1, 0, 0, 19, 0],   # Sunflower: 非常容易识别
    [0, 1, 2, 0, 17],   # Lily: 偶尔被误判
])

fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH + 2, FIG_HEIGHT // 2 + 2))

# 混淆矩阵热力图 / Confusion matrix heatmap
im = axes[0].imshow(cm, cmap='Blues', vmin=0, vmax=20)
axes[0].set_title('Confusion Matrix', fontsize=12, fontweight='bold')
for i in range(n_classes):
    for j in range(n_classes):
        color = 'white' if cm[i, j] > 10 else 'black'
        axes[0].text(j, i, str(cm[i, j]), ha='center', va='center',
                     fontsize=11, fontweight='bold', color=color)
axes[0].set_xticks(range(n_classes))
axes[0].set_yticks(range(n_classes))
axes[0].set_xticklabels(class_names_eval, rotation=45, ha='right')
axes[0].set_yticklabels(class_names_eval)
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('True')

# 每类 Precision, Recall, F1 / Per-class metrics
precisions = []
recalls = []
f1s = []
for i in range(n_classes):
    tp = cm[i, i]
    fp = cm[:, i].sum() - tp
    fn = cm[i, :].sum() - tp
    p = tp / (tp + fp) if (tp + fp) > 0 else 0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
    precisions.append(p)
    recalls.append(r)
    f1s.append(f1)

x = np.arange(n_classes)
width = 0.25
axes[1].bar(x - width, precisions, width, label='Precision', color='#3498DB')
axes[1].bar(x, recalls, width, label='Recall', color='#E74C3C')
axes[1].bar(x + width, f1s, width, label='F1', color='#2ECC71')
axes[1].set_title('Per-Class Metrics', fontsize=12, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(class_names_eval, rotation=45, ha='right')
axes[1].set_ylim(0, 1.15)
axes[1].legend(fontsize=9)
axes[1].grid(axis='y', alpha=0.3)

# 公式说明 / Formulas
axes[2].axis('off')
macro_p = np.mean(precisions)
macro_r = np.mean(recalls)
macro_f1 = np.mean(f1s)
overall_acc = np.trace(cm) / cm.sum()

formula_text = (
    f"Overall Accuracy:\n"
    f"  = {np.trace(cm)}/{cm.sum()} = {overall_acc:.3f}\n\n"
    f"Macro Avg Precision:\n"
    f"  = {macro_p:.3f}\n\n"
    f"Macro Avg Recall:\n"
    f"  = {macro_r:.3f}\n\n"
    f"Macro Avg F1-Score:\n"
    f"  = {macro_f1:.3f}\n\n"
    f"Worst: Tulip\n"
    f"  P={precisions[1]:.2f} R={recalls[1]:.2f}\n"
    f"  (confused with Rose)"
)
axes[2].text(0.5, 0.5, formula_text, ha='center', va='center',
             fontsize=10, fontfamily='monospace',
             transform=axes[2].transAxes,
             bbox=dict(boxstyle='round', facecolor='lightyellow'))

plt.suptitle(
    "Evaluation: Confusion Matrix reveals which classes are confused",
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step7_evaluation_metrics.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print(f"Overall Accuracy: {overall_acc:.3f}")
print(f"Macro Avg F1: {macro_f1:.3f}")
print("Per-class F1:")
for name, f1 in zip(class_names_eval, f1s):
    print(f"  {name}: {f1:.3f}")
print("\nSaved: step7_evaluation_metrics.png")


# ============================================================
# 步骤 8：mmpretrain 配置文件架构图
# Step 8: mmpretrain Config File Architecture
# ============================================================

print("\n" + "=" * 60)
print("Step 8: mmpretrain Config File Architecture")
print("=" * 60)

fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

# 配置文件组件 / Config components
components = [
    (2, 8.5, "model\ndict(backbone, neck, head)", '#3498DB'),
    (6, 8.5, "data_preprocessor\ndict(mean, std)", '#E74C3C'),
    (10, 8.5, "_base_\n(inheritance)", '#9B59B6'),
    (2, 6.5, "train_pipeline\n[Load, Crop, Flip, Pack]", '#2ECC71'),
    (6, 6.5, "val_pipeline\n[Load, Resize, CenterCrop]", '#F39C12'),
    (2, 4.5, "train_dataloader\ndict(batch=32, dataset)", '#E67E22'),
    (6, 4.5, "val_dataloader\ndict(batch=32, dataset)", '#1ABC9C'),
    (2, 2.5, "optim_wrapper\ndict(SGD/Adam, lr)", '#C0392B'),
    (6, 2.5, "param_scheduler\nCosineAnnealing(T=100)", '#8E44AD'),
    (10, 2.5, "train_cfg\nepochs=100, val_int=10", '#2C3E50'),
]

for x, y, text, color in components:
    rect = mpatches.FancyBboxPatch(
        (x - 1.7, y - 0.6), 3.4, 1.2,
        boxstyle="round,pad=0.1",
        facecolor=color, edgecolor='black', alpha=0.85
    )
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=8, fontweight='bold', color='white')

# 箭头连接 / Arrow connections
arrow_kw = dict(arrowstyle='->', color='#7F8C8D', lw=1.5)
# pipeline -> dataloader
ax.annotate('', xy=(2, 5.1), xytext=(2, 5.9),
            arrowprops=arrow_kw)
ax.annotate('', xy=(6, 5.1), xytext=(6, 5.9),
            arrowprops=arrow_kw)

# 标题和说明 / Title and notes
ax.text(6, 9.7, "mmpretrain Config File = Complete Experiment Definition",
        ha='center', fontsize=14, fontweight='bold')
ax.text(6, 1.0,
        "One .py file defines everything: model + data + optimizer + schedule\n"
        "Change model? Edit 'model' dict. Change optimizer? Edit 'optim_wrapper'.\n"
        "No training code to write!",
        ha='center', fontsize=10,
        bbox=dict(boxstyle='round', facecolor='lightyellow'))

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step8_config_architecture.png"),
            dpi=DPI, bbox_inches='tight')
plt.close()

print("mmpretrain config = one file defines the entire experiment:")
print("  model (ResNet/MobileNet) + data (pipeline, loader)")
print("  + optimizer (SGD/Adam) + scheduler (cosine)")
print("  + training (epochs, val interval)")
print("\nSaved: step8_config_architecture.png")


# ============================================================
# 最终总结
# Final Summary
# ============================================================

print("\n" + "=" * 60)
print("✓ All demos complete!")
print("=" * 60)
print(f"\nOutput directory: {OUTPUT_DIR}/")
print("\nFiles generated:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    print(f"  {f}")
