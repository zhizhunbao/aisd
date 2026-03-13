"""
CST8508 Machine Vision - Assignment 1: Model Evaluation
模型评估脚本
Author: Peng Wang
Student Number: 041107730

评估训练好的 ResNet-18 和 MobileNet V2 模型，在验证集上生成准确率对比图、混淆矩阵和分类报告。
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
# 配置 / Configuration
# ============================================================

# DATA_ROOT: 数据集根目录，包含 train/ 和 val/ 子目录
# DATA_ROOT: Dataset root directory, contains train/ and val/ subdirectories
DATA_ROOT = "data/flowers17"

# OUTPUT_DIR: 评估结果输出目录（图表和报告保存位置）
# OUTPUT_DIR: Evaluation output directory (charts and reports saved here)
OUTPUT_DIR = "assignment1_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# MODELS: 要评估的模型配置; config=训练配置文件路径, work_dir=权重文件目录
# MODELS: Models to evaluate; config=training config path, work_dir=checkpoint directory
MODELS = {
    "ResNet-18": {
        "config": "configs/resnet18_flowers17.py",       # 训练配置文件 / Training config file
        "work_dir": "work_dirs/resnet18_flowers17",      # 权重保存目录 / Checkpoint directory
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

# 从验证集目录自动获取类别名（按字母排序，与训练时 CustomDataset 的标签顺序一致）
# Auto-detect category names from validation directory (sorted alphabetically, matches CustomDataset label order)
val_dir = os.path.join(DATA_ROOT, "val")
categories = sorted(os.listdir(val_dir))
print(f"\nCategories ({len(categories)}): {categories}")

# 查找最新的检查点文件（按文件名排序，最后一个通常是最新/最佳的）
# Find latest checkpoint file (sorted by name, last one is usually the newest/best)
for name, info in MODELS.items():
    # glob 匹配 work_dir 下所有 .pth 文件
    # glob matches all .pth files in work_dir
    ckpts = sorted(glob.glob(os.path.join(info["work_dir"], "*.pth")))
    if ckpts:
        info["checkpoint"] = ckpts[-1]                   # 取最后一个（最新的）/ Take the last one (newest)
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

    # 初始化推理器: model=配置文件, pretrained=权重文件
    # Initialize inferencer: model=config file, pretrained=checkpoint file
    inferencer = ImageClassificationInferencer(
        model=info["config"],            # 配置文件路径（包含模型结构和数据管道定义）
                                         # Config file path (contains model architecture and data pipeline)
        pretrained=info["checkpoint"],   # 训练好的权重文件路径
                                         # Trained checkpoint file path
    )

    # defaultdict(int): 自动初始化为 0，方便计数
    # defaultdict(int): Auto-initializes to 0, convenient for counting
    correct = defaultdict(int)           # 每类正确预测数 / Correct predictions per class
    total = defaultdict(int)             # 每类总图片数 / Total images per class
    all_preds = []                       # 所有预测标签（用于混淆矩阵）/ All predicted labels (for confusion matrix)
    all_labels = []                      # 所有真实标签 / All ground truth labels

    # 遍历验证集每个类别的每张图片
    # Iterate through every image in every category of validation set
    for cat_idx, cat_name in enumerate(categories):
        cat_dir = os.path.join(val_dir, cat_name)
        for img_file in os.listdir(cat_dir):
            # 过滤非图片文件
            # Filter non-image files
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            img_path = os.path.join(cat_dir, img_file)

            # 推理: 返回列表，取第一个结果
            # Inference: returns a list, take the first result
            result = inferencer(img_path)[0]
            # pred_label: 模型预测的类别索引（0~16）
            # pred_label: Model's predicted class index (0~16)
            pred_label = result['pred_label']

            total[cat_name] += 1
            all_labels.append(cat_idx)           # 真实标签 = 类别索引 / Ground truth = category index
            all_preds.append(pred_label)          # 预测标签 / Predicted label

            # 判断预测是否正确
            # Check if prediction is correct
            if pred_label == cat_idx:
                correct[cat_name] += 1

    # 计算每类准确率和整体准确率
    # Calculate per-class accuracy and overall accuracy
    per_class_acc = {}
    for cat in categories:
        # 每类准确率 = 正确数 / 总数 × 100%
        # Per-class accuracy = correct / total × 100%
        acc = correct[cat] / total[cat] * 100 if total[cat] > 0 else 0
        per_class_acc[cat] = acc

    # 整体准确率 = 所有正确预测 / 所有图片
    # Overall accuracy = all correct predictions / all images
    overall_acc = sum(correct.values()) / sum(total.values()) * 100

    results[model_name] = {
        "per_class_acc": per_class_acc,   # 每类准确率 / Per-class accuracy
        "overall_acc": overall_acc,       # 整体准确率 / Overall accuracy
        "preds": all_preds,               # 预测列表（混淆矩阵用）/ Predictions (for confusion matrix)
        "labels": all_labels,             # 真实标签列表 / Ground truth labels
    }
    print(f"  Overall Accuracy: {overall_acc:.2f}%")

# ============================================================
# 步骤 3: 可视化 - 准确率对比柱状图
# Step 3: Visualization - Accuracy comparison bar chart
# ============================================================
print(f"\n{'='*60}")
print("Generating visualizations...")

model_names = list(results.keys())
if len(model_names) >= 2:
    # figsize=(14, 6): 图表宽 14 英寸高 6 英寸，横向长图适合多类别柱状图
    # figsize=(14, 6): Chart width 14 inches, height 6 inches, landscape suits multi-category bar chart
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(categories))     # 类别位置数组 / Category position array
    width = 0.35                       # 柱子宽度; 两个模型并排 / Bar width; two models side by side
    colors = ['#4285F4', '#EA4335']    # Google 蓝和红 / Google blue and red

    for i, name in enumerate(model_names):
        acc_vals = [results[name]["per_class_acc"][c] for c in categories]
        offset = (i - 0.5) * width     # 柱子偏移，两个模型一左一右 / Bar offset, two models left and right
        ax.bar(x + offset, acc_vals, width,
               label=f'{name} ({results[name]["overall_acc"]:.1f}%)',
               color=colors[i])

    ax.set_xlabel('Flower Category', fontsize=12)       # X 轴标签 / X axis label
    ax.set_ylabel('Accuracy (%)', fontsize=12)          # Y 轴标签 / Y axis label
    ax.set_title('Per-Category Classification Accuracy Comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')  # 旋转 45° 防止重叠 / Rotate 45° to prevent overlap
    ax.legend(fontsize=11)                               # 图例显示模型名和总准确率 / Legend with model name and overall accuracy
    ax.set_ylim(0, 105)                                  # Y 轴范围 0-105% / Y axis range 0-105%
    ax.grid(axis='y', alpha=0.3)                         # 水平网格线辅助阅读 / Horizontal grid lines for readability
    plt.tight_layout()

    # dpi=150: 分辨率 150 像素/英寸，报告中清晰度足够
    # dpi=150: 150 pixels/inch resolution, sufficient clarity for reports
    path = os.path.join(OUTPUT_DIR, "accuracy_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')      # bbox_inches='tight' 去除多余白边 / Remove excess whitespace
    plt.close()
    print(f"  Saved: {path}")

# ============================================================
# 步骤 4: 混淆矩阵
# Step 4: Confusion matrices
# ============================================================
from sklearn.metrics import confusion_matrix, classification_report

if len(model_names) >= 2:
    # 两个模型的混淆矩阵并排显示: 1 行 2 列
    # Two confusion matrices side by side: 1 row, 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    for i, name in enumerate(model_names):
        # confusion_matrix: 行=真实标签, 列=预测标签; 对角线=正确预测
        # confusion_matrix: rows=true labels, cols=predicted labels; diagonal=correct predictions
        cm = confusion_matrix(results[name]["labels"], results[name]["preds"])
        # heatmap: annot=True 在格子里显示数字; fmt='d' 整数格式; cmap='Blues' 蓝色渐变
        # heatmap: annot=True shows numbers in cells; fmt='d' integer format; cmap='Blues' blue gradient
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i],
                    xticklabels=categories, yticklabels=categories)
        axes[i].set_title(f'{name} Confusion Matrix', fontsize=13)
        axes[i].set_xlabel('Predicted')                  # 预测标签 / Predicted label
        axes[i].set_ylabel('True')                       # 真实标签 / True label
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "confusion_matrices.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")

# ============================================================
# 步骤 5: 分类报告
# Step 5: Classification report
# ============================================================
# classification_report 输出: precision(精确率), recall(召回率), f1-score, support(样本数)
# classification_report output: precision, recall, f1-score, support (sample count)
print(f"\n{'='*60}")
for name in model_names:
    print(f"\n{name} Classification Report:")
    print("-" * 60)
    # target_names: 用类别名替代数字索引，报告更可读
    # target_names: Replace numeric indices with category names for readability
    report = classification_report(
        results[name]["labels"], results[name]["preds"],
        target_names=categories
    )
    print(report)

    # 保存报告到文本文件
    # Save report to text file
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
