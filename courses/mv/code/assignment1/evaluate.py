"""
CST8508 Machine Vision - Assignment 1: Model Evaluation
Author: Peng Wang
Student Number: 041107730

Evaluate trained ResNet-18 and MobileNet V2 models on the validation set.
Generate accuracy comparison charts, confusion matrices, and classification reports.
"""

import os
import glob
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# ============================================================
# 配置
# Configuration
# ============================================================
DATA_ROOT = "data/flowers17"
OUTPUT_DIR = "assignment1_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODELS = {
    "ResNet-18": {
        "config": "configs/resnet18_flowers17.py",
        "work_dir": "work_dirs/resnet18_flowers17",
    },
    "MobileNet V2": {
        "config": "configs/mobilenetv2_flowers17.py",
        "work_dir": "work_dirs/mobilenetv2_flowers17",
    },
}

# ============================================================
# 步骤 1: 获取类别和检查点
# Step 1: Get categories and checkpoints
# ============================================================
print("=" * 60)
print("CST8508 Assignment 1: Model Evaluation")
print("=" * 60)

# 获取类别名（从验证集目录）
# Get category names (from validation directory)
val_dir = os.path.join(DATA_ROOT, "val")
categories = sorted(os.listdir(val_dir))
print(f"\nCategories ({len(categories)}): {categories}")

# 查找检查点
# Find checkpoints
for name, info in MODELS.items():
    ckpts = sorted(glob.glob(os.path.join(info["work_dir"], "*.pth")))
    if ckpts:
        info["checkpoint"] = ckpts[-1]
        print(f"  {name}: {info['checkpoint']}")
    else:
        print(f"  {name}: No checkpoint found!")
        info["checkpoint"] = None

# ============================================================
# 步骤 2: 评估模型
# Step 2: Evaluate models
# ============================================================
from mmpretrain import ImageClassificationInferencer

results = {}

for model_name, info in MODELS.items():
    if info["checkpoint"] is None:
        print(f"\n[SKIP] {model_name} - no checkpoint")
        continue

    print(f"\n[EVAL] Evaluating {model_name}...")

    # 初始化推理器
    # Initialize inferencer
    inferencer = ImageClassificationInferencer(
        model=info["config"],
        pretrained=info["checkpoint"],
    )

    correct = defaultdict(int)
    total = defaultdict(int)
    all_preds = []
    all_labels = []

    for cat_idx, cat_name in enumerate(categories):
        cat_dir = os.path.join(val_dir, cat_name)
        for img_file in os.listdir(cat_dir):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            img_path = os.path.join(cat_dir, img_file)
            result = inferencer(img_path)[0]
            pred_label = result['pred_label']

            total[cat_name] += 1
            all_labels.append(cat_idx)
            all_preds.append(pred_label)

            if pred_label == cat_idx:
                correct[cat_name] += 1

    # 计算准确率
    # Calculate accuracy
    per_class_acc = {}
    for cat in categories:
        acc = correct[cat] / total[cat] * 100 if total[cat] > 0 else 0
        per_class_acc[cat] = acc

    overall_acc = sum(correct.values()) / sum(total.values()) * 100

    results[model_name] = {
        "per_class_acc": per_class_acc,
        "overall_acc": overall_acc,
        "preds": all_preds,
        "labels": all_labels,
    }
    print(f"  Overall Accuracy: {overall_acc:.2f}%")

# ============================================================
# 步骤 3: 可视化 - 准确率对比
# Step 3: Visualization - Accuracy comparison
# ============================================================
print(f"\n{'='*60}")
print("Generating visualizations...")

model_names = list(results.keys())
if len(model_names) >= 2:
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(categories))
    width = 0.35
    colors = ['#4285F4', '#EA4335']

    for i, name in enumerate(model_names):
        acc_vals = [results[name]["per_class_acc"][c] for c in categories]
        offset = (i - 0.5) * width
        ax.bar(x + offset, acc_vals, width,
               label=f'{name} ({results[name]["overall_acc"]:.1f}%)',
               color=colors[i])

    ax.set_xlabel('Flower Category', fontsize=12)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('Per-Category Classification Accuracy Comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "accuracy_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

# ============================================================
# 步骤 4: 混淆矩阵
# Step 4: Confusion matrices
# ============================================================
from sklearn.metrics import confusion_matrix, classification_report

if len(model_names) >= 2:
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    for i, name in enumerate(model_names):
        cm = confusion_matrix(results[name]["labels"], results[name]["preds"])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                    xticklabels=categories, yticklabels=categories)
        axes[i].set_title(f'{name} Confusion Matrix', fontsize=13)
        axes[i].set_xlabel('Predicted')
        axes[i].set_ylabel('True')
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "confusion_matrices.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

# ============================================================
# 步骤 5: 分类报告
# Step 5: Classification report
# ============================================================
print(f"\n{'='*60}")
for name in model_names:
    print(f"\n{name} Classification Report:")
    print("-" * 60)
    report = classification_report(
        results[name]["labels"], results[name]["preds"],
        target_names=categories
    )
    print(report)

    # 保存报告到文件
    # Save report to file
    report_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_').lower()}_report.txt")
    with open(report_path, 'w') as f:
        f.write(f"{name} Classification Report\n")
        f.write("=" * 60 + "\n")
        f.write(report)
    print(f"  Saved: {report_path}")

print(f"\n{'='*60}")
print("✓ Evaluation complete!")
print(f"  Results saved to: {OUTPUT_DIR}/")
print(f"{'='*60}")
