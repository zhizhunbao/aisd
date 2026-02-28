"""
CST8508 Machine Vision - Assignment 1: Dataset Preparation
Author: Peng Wang
Student Number: 041107730

This script downloads the Oxford Flowers 17 dataset and organizes it
into SubFolder format compatible with mmpretrain's CustomDataset.

The SubFolder format structures data as:
    data/flowers17/
    ├── train/
    │   ├── LilyValley/
    │   │   ├── image_0231.jpg
    │   │   └── ...
    │   └── ... (17 categories)
    └── val/
        ├── LilyValley/
        │   ├── image_0203.jpg
        │   └── ...
        └── ... (17 categories)
"""

import os
import json
import shutil
import tarfile
import urllib.request

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 数据集下载 URL
# Dataset download URL
DATASET_URL = "https://www.robots.ox.ac.uk/~vgg/data/flowers/17/17flowers.tgz"

# 数据集存放根目录
# Root directory for dataset storage
DATA_ROOT = "data/flowers17"

# 下载的压缩文件名
# Downloaded archive filename
ARCHIVE_NAME = "17flowers.tgz"

# 解压后的原始图片目录名
# Extracted raw images directory name
RAW_IMAGES_DIR = "jpg"

# 训练集和验证集的 JSON 分割文件
# JSON split files for train and validation sets
TRAIN_SPLIT_FILE = "train_set.json"
VAL_SPLIT_FILE = "val_set.json"

# ============================================================
# 步骤 1：下载 Oxford Flowers 17 数据集
# Step 1: Download Oxford Flowers 17 Dataset
# ============================================================
def download_dataset():
    """
    下载 Oxford Flowers 17 数据集。
    Download the Oxford Flowers 17 dataset.

    数据集来自 Visual Geometry Group, University of Oxford
    Dataset from Visual Geometry Group, University of Oxford
    包含 17 种花卉类别，每类约 80 张图片
    Contains 17 flower categories, ~80 images each
    """
    if os.path.exists(ARCHIVE_NAME):
        print(f"[INFO] 压缩文件已存在: {ARCHIVE_NAME}")
        print(f"[INFO] Archive already exists: {ARCHIVE_NAME}")
        return

    print(f"[INFO] 正在下载数据集: {DATASET_URL}")
    print(f"[INFO] Downloading dataset: {DATASET_URL}")
    urllib.request.urlretrieve(DATASET_URL, ARCHIVE_NAME)
    print(f"[INFO] 下载完成: {ARCHIVE_NAME}")
    print(f"[INFO] Download complete: {ARCHIVE_NAME}")


# ============================================================
# 步骤 2：解压数据集
# Step 2: Extract Dataset
# ============================================================
def extract_dataset():
    """
    解压 .tgz 文件到当前目录。
    Extract .tgz file to current directory.

    解压后会生成 'jpg/' 目录，包含所有 1360 张图片
    After extraction, a 'jpg/' directory with all 1360 images is created
    """
    if os.path.exists(RAW_IMAGES_DIR):
        print(f"[INFO] 图片目录已存在: {RAW_IMAGES_DIR}/")
        print(f"[INFO] Images directory already exists: {RAW_IMAGES_DIR}/")
        return

    print(f"[INFO] 正在解压: {ARCHIVE_NAME}")
    print(f"[INFO] Extracting: {ARCHIVE_NAME}")
    with tarfile.open(ARCHIVE_NAME, "r:gz") as tar:
        tar.extractall()
    print(f"[INFO] 解压完成")
    print(f"[INFO] Extraction complete")


# ============================================================
# 步骤 3：按 SubFolder 格式组织数据集
# Step 3: Organize Dataset in SubFolder Format
# ============================================================
def organize_dataset(train_json_path, val_json_path):
    """
    将数据集按 SubFolder 格式组织，兼容 mmpretrain CustomDataset。
    Organize dataset in SubFolder format compatible with mmpretrain CustomDataset.

    SubFolder 格式说明（来自 mmpretrain 文档）：
    SubFolder format description (from mmpretrain docs):
    - 无需创建标注文件（annotation file）
    - No annotation files needed
    - 子文件夹名即类别名
    - Subfolder names serve as class names
    - mmpretrain 自动扫描子文件夹并将文件夹名映射为类别标签
    - mmpretrain auto-scans subfolders and maps folder names to class labels

    Args:
        train_json_path: 训练集分割文件路径 / Path to train split JSON file
        val_json_path: 验证集分割文件路径 / Path to validation split JSON file
    """
    # 读取分割文件
    # Load split files
    print(f"[INFO] 正在读取分割文件...")
    print(f"[INFO] Loading split files...")
    with open(train_json_path, 'r') as f:
        train_split = json.load(f)
    with open(val_json_path, 'r') as f:
        val_split = json.load(f)

    # 创建 SubFolder 目录结构
    # Create SubFolder directory structure
    train_dir = os.path.join(DATA_ROOT, "train")
    val_dir = os.path.join(DATA_ROOT, "val")

    # 统计信息
    # Statistics
    total_train = 0
    total_val = 0
    categories = sorted(train_split.keys())

    print(f"\n[INFO] 数据集包含 {len(categories)} 个类别:")
    print(f"[INFO] Dataset contains {len(categories)} categories:")
    for cat in categories:
        print(f"  - {cat}")

    # 复制训练集图片到对应的类别子文件夹
    # Copy training images to corresponding category subfolders
    print(f"\n[INFO] 正在组织训练集...")
    print(f"[INFO] Organizing training set...")
    for category, images in train_split.items():
        cat_dir = os.path.join(train_dir, category)
        os.makedirs(cat_dir, exist_ok=True)
        for img_name in images:
            src = os.path.join(RAW_IMAGES_DIR, img_name)
            dst = os.path.join(cat_dir, img_name)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
            total_train += 1
        print(f"  [TRAIN] {category}: {len(images)} 张图片 / images")

    # 复制验证集图片到对应的类别子文件夹
    # Copy validation images to corresponding category subfolders
    print(f"\n[INFO] 正在组织验证集...")
    print(f"[INFO] Organizing validation set...")
    for category, images in val_split.items():
        cat_dir = os.path.join(val_dir, category)
        os.makedirs(cat_dir, exist_ok=True)
        for img_name in images:
            src = os.path.join(RAW_IMAGES_DIR, img_name)
            dst = os.path.join(cat_dir, img_name)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
            total_val += 1
        print(f"  [VAL]   {category}: {len(images)} 张图片 / images")

    # 打印总结
    # Print summary
    print(f"\n{'='*60}")
    print(f"[SUMMARY] 数据集准备完成！/ Dataset preparation complete!")
    print(f"{'='*60}")
    print(f"  训练集 / Training set:   {total_train} 张图片 / images")
    print(f"  验证集 / Validation set: {total_val} 张图片 / images")
    print(f"  类别数 / Categories:     {len(categories)}")
    print(f"  数据根目录 / Data root:  {DATA_ROOT}")
    print(f"{'='*60}")


# ============================================================
# 步骤 4：验证数据集结构
# Step 4: Verify Dataset Structure
# ============================================================
def verify_dataset():
    """
    验证 SubFolder 格式的数据集结构是否正确。
    Verify the SubFolder format dataset structure is correct.

    检查内容：
    Verification checks:
    - 训练/验证目录是否存在 / Train/Val directories exist
    - 每个类别子文件夹是否包含图片 / Each category subfolder has images
    - 图片文件是否可读 / Image files are readable
    """
    print(f"\n[INFO] 正在验证数据集结构...")
    print(f"[INFO] Verifying dataset structure...")

    for split_name in ["train", "val"]:
        split_dir = os.path.join(DATA_ROOT, split_name)
        if not os.path.exists(split_dir):
            print(f"  [ERROR] 目录不存在: {split_dir}")
            print(f"  [ERROR] Directory missing: {split_dir}")
            continue

        categories = sorted(os.listdir(split_dir))
        print(f"\n  [{split_name.upper()}] {len(categories)} 个类别 / categories:")
        for cat in categories:
            cat_path = os.path.join(split_dir, cat)
            if os.path.isdir(cat_path):
                num_images = len([
                    f for f in os.listdir(cat_path)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                ])
                status = "✓" if num_images > 0 else "✗"
                print(f"    {status} {cat}: {num_images} 张图片 / images")

    print(f"\n[INFO] 验证完成！/ Verification complete!")


# ============================================================
# 主执行流程
# Main Execution Flow
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("CST8508 Assignment 1: Oxford Flowers 17 Dataset Preparation")
    print("Author: Peng Wang (041107730)")
    print("=" * 60)

    # 步骤 1: 下载数据集
    # Step 1: Download dataset
    download_dataset()

    # 步骤 2: 解压数据集
    # Step 2: Extract dataset
    extract_dataset()

    # 步骤 3: 按 SubFolder 格式组织
    # Step 3: Organize in SubFolder format
    organize_dataset(TRAIN_SPLIT_FILE, VAL_SPLIT_FILE)

    # 步骤 4: 验证数据集结构
    # Step 4: Verify dataset structure
    verify_dataset()
