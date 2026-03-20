"""
CST8508 Assignment 2: Object Detection with YOLO26 (Transfer Learning)
Author: Peng Wang
Student Number: 041107730

All-in-one script: dataset preparation, model fine-tuning, and evaluation.
Uses Ultralytics YOLO26 as alternative to MMDetection (EOL since 2025).
Approach: Transfer Learning — load COCO pretrained weights, fine-tune on Oxford Pet.
Models: YOLO26-s vs YOLO26-m on Oxford-IIIT Pet Dataset.
Runs on Windows: uv run python assignment2.py
"""

import os
import json
import tarfile
import shutil
import random
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 数据集下载地址
# Dataset download URLs
IMAGES_URL = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz"
ANNOTATIONS_URL = "https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz"

# 项目路径
# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datasets" / "oxford_pet"
RAW_DIR = DATA_DIR / "raw"
YOLO_DIR = DATA_DIR / "yolo"
WORK_DIR = BASE_DIR / "work_dirs"
OUTPUT_DIR = BASE_DIR / "assignment2_images"

# 数据集配置文件路径
# Dataset config file path
DATA_CONFIG = BASE_DIR / "pet.yaml"

# 数据集划分比例：80% 训练, 20% 验证
# Dataset split ratio: 80% train, 20% val
TRAIN_RATIO = 0.8
RANDOM_STATE = 42

# 训练超参数（作业要求不超过 20 个 epoch）
# Training hyperparameters (assignment requires no more than 20 epochs)
MAX_EPOCHS = 20
IMAGE_SIZE = 640
BATCH_SIZE = 16

# 迁移学习：两个 YOLO26 预训练模型用于 fine-tune（替代 TOOD 和 VFNET）
# Transfer Learning: Two YOLO26 pretrained models for fine-tuning (alternative to TOOD and VFNET)
# yolo26n: 纳米模型 (2.7M 参数) — COCO 预训练，最轻量
# yolo26n: Nano model (2.7M params) — COCO pretrained, lightest
# yolo26s: 小型模型 (10.0M 参数) — COCO 预训练，比 nano 大 3.7x
# yolo26s: Small model (10.0M params) — COCO pretrained, 3.7x larger than nano
MODELS = {
    "yolo26n": "yolo26n.pt",
    "yolo26s": "yolo26s.pt",
}

# IoU 阈值（用于判断检测是否正确）
# IoU threshold (for determining if detection is correct)
IOU_THRESHOLD = 0.5

# 图表设置
# Plot settings
FIGURE_DPI = 150
FONT_SIZE = 12


# ============================================================
# 辅助函数
# Helper Functions
# ============================================================

def download_file(url, dest_path):
    """Download file from URL with progress display.
    从 URL 下载文件并显示进度"""
    if dest_path.exists():
        print(f"  Already exists: {dest_path.name}")
        return
    print(f"  Downloading: {url}")

    def progress_hook(count, block_size, total_size):
        percent = count * block_size * 100 / total_size
        print(f"\r  Progress: {min(percent, 100):.1f}%", end="", flush=True)

    urlretrieve(url, dest_path, reporthook=progress_hook)
    print()


def parse_xml_annotation(xml_path):
    """Parse Pascal VOC XML annotation file.
    解析 Pascal VOC 格式的 XML 标注文件"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    boxes = []
    for obj in root.findall("object"):
        name = obj.find("name").text
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        boxes.append((name, xmin, ymin, xmax, ymax))

    return img_width, img_height, boxes


def voc_to_yolo(img_w, img_h, xmin, ymin, xmax, ymax):
    """Convert VOC box to YOLO normalized format.
    将 VOC 格式边界框转换为 YOLO 归一化格式"""
    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(img_w, xmax)
    ymax = min(img_h, ymax)

    x_center = (xmin + xmax) / 2.0 / img_w
    y_center = (ymin + ymax) / 2.0 / img_h
    width = (xmax - xmin) / img_w
    height = (ymax - ymin) / img_h
    return x_center, y_center, width, height


def compute_iou(box1, box2):
    """Compute IoU between two boxes in xyxy format.
    计算两个 xyxy 格式边界框的 IoU"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0


def load_yolo_labels(label_path, img_w, img_h):
    """Load YOLO format labels and convert to xyxy pixel coordinates.
    加载 YOLO 格式标签并转换为 xyxy 像素坐标"""
    boxes = []
    if not label_path.exists():
        return boxes
    with open(label_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                cls_id = int(parts[0])
                x_c = float(parts[1]) * img_w
                y_c = float(parts[2]) * img_h
                w = float(parts[3]) * img_w
                h = float(parts[4]) * img_h
                boxes.append((cls_id, x_c - w / 2, y_c - h / 2, x_c + w / 2, y_c + h / 2))
    return boxes


# ============================================================
# Windows 多进程保护：所有执行代码必须在 __main__ 内
# Windows multiprocessing guard: all executable code must be inside __main__
# 原因：Windows 使用 spawn（而非 fork）启动子进程，会重新导入整个模块
# Reason: Windows uses spawn (not fork) to start child processes, re-importing the entire module
# ============================================================

if __name__ == "__main__":

    # ################################################################
    #
    #  PHASE 2: 数据准备 (40%)
    #  PHASE 2: Data Preparation (40%)
    #
    # ################################################################

    # ============================================================
    # 步骤 1：下载数据集
    # Step 1: Download dataset
    # ============================================================

    print("=" * 60)
    print("Step 1: Download Oxford-IIIT Pet Dataset")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    images_tar = RAW_DIR / "images.tar.gz"
    annotations_tar = RAW_DIR / "annotations.tar.gz"

    download_file(IMAGES_URL, images_tar)
    download_file(ANNOTATIONS_URL, annotations_tar)

    # ============================================================
    # 步骤 2：解压数据集
    # Step 2: Extract dataset
    # ============================================================

    print()
    print("=" * 60)
    print("Step 2: Extract dataset")
    print("=" * 60)

    for tar_path, name in [(images_tar, "images"), (annotations_tar, "annotations")]:
        extract_dir = RAW_DIR / name
        if extract_dir.exists() and len(list(extract_dir.iterdir())) > 0:
            print(f"  Already extracted: {name}")
        else:
            print(f"  Extracting: {tar_path.name}")
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(RAW_DIR)
            print(f"  Done: {name}")

    images_dir = RAW_DIR / "images"
    xmls_dir = RAW_DIR / "annotations" / "xmls"
    list_file = RAW_DIR / "annotations" / "list.txt"

    print(f"  Images: {images_dir}")
    print(f"  XMLs: {xmls_dir}")

    # ============================================================
    # 步骤 3：解析类别映射
    # Step 3: Parse class mapping
    # ============================================================

    print()
    print("=" * 60)
    print("Step 3: Parse class mapping")
    print("=" * 60)

    breed_names = set()
    image_class_map = {}

    with open(list_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            parts = line.split()
            if len(parts) >= 4:
                image_name = parts[0]
                breed = "_".join(image_name.split("_")[:-1])
                breed_names.add(breed)
                image_class_map[image_name] = breed

    breed_list = sorted(breed_names)
    breed_to_id = {breed: idx for idx, breed in enumerate(breed_list)}

    print(f"  Total breeds (classes): {len(breed_list)}")
    print(f"  Total images: {len(image_class_map)}")
    print(f"  First 5: {breed_list[:5]}")

    # ============================================================
    # 步骤 4：XML → YOLO 格式转换
    # Step 4: Convert XML to YOLO format
    # ============================================================

    print()
    print("=" * 60)
    print("Step 4: Convert XML to YOLO format")
    print("=" * 60)

    converted = 0
    skipped = 0
    all_samples = []

    xml_files = sorted(xmls_dir.glob("*.xml"))
    print(f"  Found {len(xml_files)} XML files")

    for xml_path in xml_files:
        image_name = xml_path.stem

        img_path = None
        for ext in [".jpg", ".png", ".jpeg"]:
            candidate = images_dir / (image_name + ext)
            if candidate.exists():
                img_path = candidate
                break

        if img_path is None:
            skipped += 1
            continue

        breed = "_".join(image_name.split("_")[:-1])
        if breed not in breed_to_id:
            skipped += 1
            continue
        breed_id = breed_to_id[breed]

        try:
            img_w, img_h, boxes = parse_xml_annotation(xml_path)
        except Exception as e:
            print(f"  Warning: {xml_path.name}: {e}")
            skipped += 1
            continue

        label_lines = []
        for _, xmin, ymin, xmax, ymax in boxes:
            x_c, y_c, w, h = voc_to_yolo(img_w, img_h, xmin, ymin, xmax, ymax)
            label_lines.append(f"{breed_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}")

        all_samples.append((img_path, "\n".join(label_lines), breed_id))
        converted += 1

    print(f"  Converted: {converted}, Skipped: {skipped}")

    # ============================================================
    # 步骤 5：划分 Train / Val 并写入文件
    # Step 5: Split Train / Val and write files
    # ============================================================

    print()
    print("=" * 60)
    print("Step 5: Split train/val and create YOLO dataset")
    print("=" * 60)

    random.seed(RANDOM_STATE)
    random.shuffle(all_samples)

    split_idx = int(len(all_samples) * TRAIN_RATIO)
    splits = {"train": all_samples[:split_idx], "val": all_samples[split_idx:]}

    for split_name, samples in splits.items():
        img_dir = YOLO_DIR / split_name / "images"
        lbl_dir = YOLO_DIR / split_name / "labels"
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)

        for img_path, label_content, _ in samples:
            dest_img = img_dir / img_path.name
            if not dest_img.exists():
                shutil.copy2(img_path, dest_img)
            with open(lbl_dir / (img_path.stem + ".txt"), "w") as f:
                f.write(label_content)

        print(f"  {split_name}: {len(samples)} samples")

    # ============================================================
    # 步骤 6：生成 pet.yaml
    # Step 6: Generate pet.yaml
    # ============================================================

    print()
    print("=" * 60)
    print("Step 6: Generate pet.yaml")
    print("=" * 60)

    yaml_content = f"# Oxford-IIIT Pet Dataset - YOLO Format\n"
    yaml_content += f"path: {YOLO_DIR.resolve()}\n"
    yaml_content += f"train: train/images\nval: val/images\n"
    yaml_content += f"nc: {len(breed_list)}\nnames:\n"
    for idx, breed in enumerate(breed_list):
        yaml_content += f"  {idx}: {breed}\n"

    for yaml_path in [YOLO_DIR / "pet.yaml", DATA_CONFIG]:
        with open(yaml_path, "w") as f:
            f.write(yaml_content)

    print(f"  Config: {DATA_CONFIG}")
    print(f"  Classes: {len(breed_list)}")

    # ################################################################
    #
    #  PHASE 4: 迁移学习 Fine-tune (20%)
    #  PHASE 4: Transfer Learning Fine-tune (20%)
    #
    # ################################################################

    # ============================================================
    # 步骤 7：Fine-tune YOLO26 模型（Transfer Learning）
    # Step 7: Fine-tune YOLO26 models (Transfer Learning)
    # ============================================================

    from ultralytics import YOLO

    for model_name, pretrained_weights in MODELS.items():
        print()
        print("=" * 60)
        print(f"Step 7: Fine-tune {model_name} (Transfer Learning)")
        print("=" * 60)

        # 跳过已训练的模型（避免重复训练浪费时间）
        # Skip already trained models (avoid wasting time on re-training)
        best_ckpt = WORK_DIR / model_name / "weights" / "best.pt"
        if best_ckpt.exists():
            print(f"  SKIP: {model_name} already trained -> {best_ckpt}")
            continue

        # 迁移学习：加载 COCO 预训练权重，然后在 Pet 数据集上 fine-tune
        # Transfer Learning: load COCO pretrained weights, then fine-tune on Pet dataset
        model = YOLO(pretrained_weights)

        # 训练参数:
        # Training parameters:
        # - epochs: 最大 20（作业限制） / max 20 (assignment limit)
        # - imgsz: 640（YOLO 标准输入尺寸） / 640 (YOLO standard input size)
        # - batch: 16（平衡 GPU 内存和训练速度） / 16 (balance GPU memory and training speed)
        # - workers: 0（Windows 不支持 fork 多进程，必须单进程加载数据）
        # - workers: 0 (Windows doesn't support fork, must use single-process data loading)
        # - pretrained: True（启用迁移学习） / True (enable transfer learning)
        model.train(
            data=str(DATA_CONFIG),
            epochs=MAX_EPOCHS,
            imgsz=IMAGE_SIZE,
            batch=BATCH_SIZE,
            workers=0,
            project=str(WORK_DIR),
            name=model_name,
            pretrained=True,
            plots=True,
            save=True,
            exist_ok=True,
            verbose=True,
        )

        print(f"  Done: {model_name} → {WORK_DIR / model_name}")

    # ################################################################
    #
    #  PHASE 5: 评估分析 (30%)
    #  PHASE 5: Evaluation & Analysis (30%)
    #
    # ################################################################

    # ============================================================
    # 步骤 8：加载最佳检查点并推理
    # Step 8: Load best checkpoints and run inference
    # ============================================================

    print()
    print("=" * 60)
    print("Step 8: Evaluate models -- ROC curve & AUC")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    val_images_dir = YOLO_DIR / "val" / "images"
    val_labels_dir = YOLO_DIR / "val" / "labels"

    model_results = {}

    for model_name in MODELS:
        best_path = WORK_DIR / model_name / "weights" / "best.pt"
        if not best_path.exists():
            best_path = WORK_DIR / model_name / "weights" / "last.pt"
        if not best_path.exists():
            print(f"  ERROR: No checkpoint for {model_name}")
            continue

        print(f"\n  Evaluating: {model_name} ({best_path})")
        model = YOLO(str(best_path))

        all_confidences = []
        all_matches = []
        total_gt = 0

        # 批量推理
        # Batch inference
        results = model.predict(
            source=str(val_images_dir),
            conf=0.001,
            iou=IOU_THRESHOLD,
            save=False,
            verbose=False,
            stream=True,
        )

        for result in results:
            img_path = Path(result.path)
            img_h, img_w = result.orig_shape

            label_path = val_labels_dir / (img_path.stem + ".txt")
            gt_boxes = load_yolo_labels(label_path, img_w, img_h)
            total_gt += len(gt_boxes)

            if result.boxes is not None and len(result.boxes) > 0:
                pred_boxes = result.boxes.xyxy.cpu().numpy()
                pred_confs = result.boxes.conf.cpu().numpy()
                pred_classes = result.boxes.cls.cpu().numpy().astype(int)

                matched_gt = set()
                sorted_indices = np.argsort(-pred_confs)

                for idx in sorted_indices:
                    conf = pred_confs[idx]
                    pred_box = pred_boxes[idx]
                    pred_cls = pred_classes[idx]

                    best_iou = 0
                    best_gt_idx = -1
                    for gt_idx, (gt_cls, gx1, gy1, gx2, gy2) in enumerate(gt_boxes):
                        if gt_idx in matched_gt or gt_cls != pred_cls:
                            continue
                        iou_val = compute_iou(pred_box, [gx1, gy1, gx2, gy2])
                        if iou_val > best_iou:
                            best_iou = iou_val
                            best_gt_idx = gt_idx

                    all_confidences.append(conf)
                    if best_iou >= IOU_THRESHOLD and best_gt_idx >= 0:
                        all_matches.append(1)
                        matched_gt.add(best_gt_idx)
                    else:
                        all_matches.append(0)

        model_results[model_name] = {
            "confidences": np.array(all_confidences),
            "matches": np.array(all_matches),
            "total_gt": total_gt,
        }

        tp = sum(all_matches)
        fp = len(all_matches) - tp
        print(f"    Detections: {len(all_confidences)}, TP: {tp}, FP: {fp}, GT: {total_gt}")

    # ============================================================
    # 步骤 9：计算 ROC 曲线和 AUC
    # Step 9: Compute ROC curves and AUC
    # ============================================================

    print()
    print("=" * 60)
    print("Step 9: Compute ROC curves and AUC")
    print("=" * 60)

    roc_data = {}

    for model_name, data in model_results.items():
        confs = data["confidences"]
        matches = data["matches"]
        total_gt = data["total_gt"]

        if len(confs) == 0:
            roc_data[model_name] = {"fpr": np.array([0, 1]), "tpr": np.array([0, 1]), "auc": 0.5}
            continue

        sorted_idx = np.argsort(-confs)
        sorted_matches = matches[sorted_idx]

        tp_cum = np.cumsum(sorted_matches)
        fp_cum = np.cumsum(1 - sorted_matches)

        # TPR = 累积 TP / 真实目标总数 (召回率)
        # TPR = cumulative TP / total ground truth (recall)
        tpr = tp_cum / total_gt if total_gt > 0 else tp_cum

        # FPR = 累积 FP / 最大 FP (归一化到 0-1)
        # FPR = cumulative FP / max FP (normalized to 0-1)
        max_fp = fp_cum[-1] if fp_cum[-1] > 0 else 1
        fpr = fp_cum / max_fp

        fpr = np.concatenate([[0], fpr, [1]])
        tpr = np.concatenate([[0], tpr, [1]])

        roc_auc = auc(fpr, tpr)
        roc_data[model_name] = {"fpr": fpr, "tpr": tpr, "auc": roc_auc}
        print(f"  {model_name}: AUC = {roc_auc:.4f}")

    # ============================================================
    # 步骤 10：绘制 ROC 曲线
    # Step 10: Plot ROC curves
    # ============================================================

    print()
    print("=" * 60)
    print("Step 10: Plot ROC curves")
    print("=" * 60)

    colors = {"yolo26n": "#2196F3", "yolo26s": "#FF5722"}

    plt.figure(figsize=(10, 8))
    for name, data in roc_data.items():
        plt.plot(data["fpr"], data["tpr"], color=colors.get(name, "gray"),
                 linewidth=2.5, label=f"{name} (AUC = {data['auc']:.4f})")

    plt.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Random (AUC = 0.5)")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate", fontsize=FONT_SIZE)
    plt.ylabel("True Positive Rate", fontsize=FONT_SIZE)
    plt.title("ROC Curve -- YOLO26 Model Comparison\nOxford-IIIT Pet Dataset (Transfer Learning)", fontsize=FONT_SIZE + 2)
    plt.legend(loc="lower right", fontsize=FONT_SIZE)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    roc_path = OUTPUT_DIR / "roc_curve.png"
    plt.savefig(roc_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {roc_path}")

    # ============================================================
    # 步骤 11：绘制模型对比图
    # Step 11: Plot model comparison chart
    # ============================================================

    print()
    print("=" * 60)
    print("Step 11: Plot model comparison")
    print("=" * 60)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    names_list = list(roc_data.keys())
    auc_vals = [roc_data[m]["auc"] for m in names_list]
    bar_colors = [colors.get(m, "gray") for m in names_list]

    axes[0].bar(names_list, auc_vals, color=bar_colors, width=0.5, alpha=0.85)
    axes[0].set_ylabel("AUC Score", fontsize=FONT_SIZE)
    axes[0].set_title("AUC Comparison", fontsize=FONT_SIZE + 1)
    axes[0].set_ylim([0, 1.0])
    axes[0].grid(axis="y", alpha=0.3)
    for i, v in enumerate(auc_vals):
        axes[0].text(i, v + 0.02, f"{v:.4f}", ha="center", fontsize=FONT_SIZE, fontweight="bold")

    tp_list = [int(model_results[m]["matches"].sum()) for m in names_list]
    fp_list = [int(len(model_results[m]["matches"]) - model_results[m]["matches"].sum()) for m in names_list]
    x = np.arange(len(names_list))
    w = 0.35
    axes[1].bar(x - w / 2, tp_list, w, label="True Positives", color="#4CAF50", alpha=0.85)
    axes[1].bar(x + w / 2, fp_list, w, label="False Positives", color="#f44336", alpha=0.85)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names_list)
    axes[1].set_ylabel("Count", fontsize=FONT_SIZE)
    axes[1].set_title("Detection Results", fontsize=FONT_SIZE + 1)
    axes[1].legend(fontsize=FONT_SIZE - 1)
    axes[1].grid(axis="y", alpha=0.3)

    plt.suptitle("YOLO26 Model Comparison -- Oxford-IIIT Pet Dataset", fontsize=FONT_SIZE + 3, y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "model_comparison.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {OUTPUT_DIR / 'model_comparison.png'}")

    # ============================================================
    # 步骤 12：输出评估总结
    # Step 12: Evaluation summary
    # ============================================================

    print()
    print("=" * 60)
    print("Step 12: Evaluation summary")
    print("=" * 60)

    print()
    print(f"  {'Model':<12} {'AUC':<10} {'TP':<8} {'FP':<8} {'GT':<8}")
    print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*8} {'-'*8}")

    eval_json = {}
    for name in MODELS:
        if name in roc_data:
            a = roc_data[name]["auc"]
            tp = int(model_results[name]["matches"].sum())
            fp = int(len(model_results[name]["matches"]) - tp)
            gt = model_results[name]["total_gt"]
            print(f"  {name:<12} {a:<10.4f} {tp:<8} {fp:<8} {gt:<8}")
            eval_json[name] = {"auc": float(a), "tp": tp, "fp": fp, "gt": gt}

    best = max(roc_data.keys(), key=lambda m: roc_data[m]["auc"])
    print(f"\n  Best model: {best} (AUC = {roc_data[best]['auc']:.4f})")

    with open(OUTPUT_DIR / "eval_results.json", "w") as f:
        json.dump(eval_json, f, indent=2)

    print()
    print("=" * 60)
    print("Assignment 2 Complete!")
    print("=" * 60)
    print(f"  Checkpoints: {WORK_DIR}")
    print(f"  Plots: {OUTPUT_DIR}")
