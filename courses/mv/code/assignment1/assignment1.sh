#!/bin/bash
# ============================================================
# CST8508 Assignment 1 - All-in-One Script (Conda 版)
# 完全对齐 mmpretrain 官方 get_started 教程
# https://mmpretrain.readthedocs.io/en/latest/get_started.html
#
# Usage:
#   bash assignment1.sh setup    # 搭建环境（首次运行）
#   bash assignment1.sh check    # 检查环境状态
#   bash assignment1.sh train    # 训练 + 评估
#   bash assignment1.sh all      # 全部执行
# ============================================================

set -e

WORK_DIR="$HOME/mv_assignment1"
WIN_PROJECT="/mnt/c/Users/40270/Desktop/workspace/aisd/courses/mv/code/assignment1"
CONDA_ENV="openmmlab"

show_usage() {
    echo "============================================================"
    echo "CST8508 Assignment 1 - All-in-One Script"
    echo "Author: Peng Wang (041107730)"
    echo "============================================================"
    echo ""
    echo "Usage: bash assignment1.sh <command>"
    echo ""
    echo "Commands:"
    echo "  setup   搭建 conda 环境（按官方教程）"
    echo "  check   检查环境是否就绪"
    echo "  train   训练两个模型并生成评估报告"
    echo "  all     全部执行（setup → check → train）"
    echo ""
}

# 激活 conda 环境的辅助函数
# Helper to activate conda environment
activate_conda() {
    # 尝试常见的 conda 安装路径
    for p in "$HOME/miniconda3" "$HOME/anaconda3" "/opt/conda" "$HOME/miniforge3"; do
        if [ -f "$p/etc/profile.d/conda.sh" ]; then
            source "$p/etc/profile.d/conda.sh"
            conda activate "$CONDA_ENV"
            return 0
        fi
    done
    echo "  ✗ conda not found! Please install Miniconda first:"
    echo "    https://docs.anaconda.com/miniconda/install/#quick-command-line-install"
    exit 1
}

# ============================================================
# do_setup: 按官方教程搭建 conda 环境
# ============================================================
do_setup() {
    echo "============================================================"
    echo "  Phase 1: Environment Setup (conda)"
    echo "============================================================"

    # --- 1.1 检查 GPU ---
    echo ""
    echo "[1/6] Checking GPU..."
    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
        echo "  ✓ GPU detected"
    else
        echo "  ✗ nvidia-smi not found"
        echo "    Install NVIDIA drivers on Windows (>= 470.76)"
        exit 1
    fi

    # --- 1.2 安装 Miniconda（如果没有）---
    echo ""
    echo "[2/6] Checking conda..."
    CONDA_FOUND=false
    for p in "$HOME/miniconda3" "$HOME/anaconda3" "/opt/conda" "$HOME/miniforge3"; do
        if [ -f "$p/etc/profile.d/conda.sh" ]; then
            source "$p/etc/profile.d/conda.sh"
            CONDA_FOUND=true
            break
        fi
    done

    if [ "$CONDA_FOUND" = false ]; then
        echo "  Installing Miniconda..."
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
        bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
        rm /tmp/miniconda.sh
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
        echo "  ✓ Miniconda installed"
    else
        echo "  ✓ conda found"
    fi

    # --- 1.3 创建 conda 环境（官方教程: python=3.8）---
    echo ""
    echo "[3/6] Creating conda environment '$CONDA_ENV' with Python 3.8..."
    if conda env list | grep -q "$CONDA_ENV"; then
        echo "  ✓ Environment already exists"
    else
        conda create --name "$CONDA_ENV" python=3.8 -y
        echo "  ✓ Environment created"
    fi
    conda activate "$CONDA_ENV"

    # --- 1.4 安装 PyTorch（官方教程: conda install pytorch torchvision -c pytorch）---
    echo ""
    echo "[4/6] Installing PyTorch with CUDA..."
    CURRENT_TORCH=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "none")
    if [ "$CURRENT_TORCH" != "none" ]; then
        echo "  ✓ PyTorch $CURRENT_TORCH already installed"
    else
        # 用 conda 安装 PyTorch + CUDA（conda 自动处理 CUDA toolkit 版本匹配）
        conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia -y
        echo "  ✓ PyTorch installed"
    fi

    # --- 1.5 安装 mmpretrain（官方教程: pip install -U openmim && mim install）---
    echo ""
    echo "[5/6] Installing OpenMMLab packages (official method)..."
    pip install -U openmim

    python -c "import mmengine" 2>/dev/null && echo "  ✓ mmengine already installed" || {
        mim install mmengine; echo "  ✓ mmengine installed"; }

    python -c "import mmcv" 2>/dev/null && echo "  ✓ mmcv already installed" || {
        mim install "mmcv>=2.0.0"; echo "  ✓ mmcv installed"; }

    python -c "import mmpretrain" 2>/dev/null && echo "  ✓ mmpretrain already installed" || {
        mim install "mmpretrain>=1.0.0"; echo "  ✓ mmpretrain installed"; }

    pip install scikit-learn seaborn matplotlib -q

    # --- 1.6 复制项目文件 + 准备数据集 ---
    echo ""
    echo "[6/6] Preparing project files and dataset..."
    mkdir -p "$WORK_DIR"
    cd "$WORK_DIR"

    if [ -d "$WIN_PROJECT" ]; then
        for f in prepare_dataset.py evaluate.py CST8508_Assignment1.py train_set.json val_set.json; do
            cp "$WIN_PROJECT/$f" . 2>/dev/null || true
        done
        cp -r "$WIN_PROJECT/configs" . 2>/dev/null || true
        echo "  ✓ Files copied from Windows"
    else
        echo "  ✗ Windows project not found: $WIN_PROJECT"
    fi

    if [ -d "data/flowers17/train" ]; then
        echo "  ✓ Dataset already exists"
    else
        python prepare_dataset.py
        echo "  ✓ Dataset prepared"
    fi

    # --- 验证安装（官方教程 verify 步骤）---
    echo ""
    echo "=== Verifying installation ==="
    python -c "
from mmpretrain import get_model, inference_model
print('mmpretrain import OK')
import torch
print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
"

    echo ""
    echo "============================================================"
    echo "  ✓ Setup complete!"
    echo "  To use: conda activate $CONDA_ENV"
    echo "============================================================"
}

# ============================================================
# do_check: 检查环境状态
# ============================================================
do_check() {
    echo "============================================================"
    echo "  Environment Check"
    echo "============================================================"

    activate_conda
    cd "$WORK_DIR"

    echo ""
    echo "=== GPU ==="
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader 2>/dev/null || echo "  ✗ N/A"

    echo ""
    echo "=== Packages ==="
    python -c "
import sys
print(f'  Python:     {sys.version.split()[0]}')
import torch
print(f'  PyTorch:    {torch.__version__}')
print(f'  CUDA:       {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'  GPU:        {torch.cuda.get_device_name(0)}')
import numpy; print(f'  numpy:      {numpy.__version__}')
import mmengine; print(f'  mmengine:   {mmengine.__version__}')
import mmcv; print(f'  mmcv:       {mmcv.__version__}')
import mmpretrain; print(f'  mmpretrain: {mmpretrain.__version__}')
"

    echo ""
    echo "=== Dataset ==="
    if [ -d "data/flowers17/train" ]; then
        echo "  ✓ train: $(ls data/flowers17/train/ | wc -l) categories"
        echo "  ✓ val:   $(ls data/flowers17/val/ 2>/dev/null | wc -l) categories"
    else
        echo "  ✗ Dataset NOT prepared"
    fi

    echo ""
    echo "=== Files ==="
    for f in prepare_dataset.py evaluate.py train_set.json val_set.json; do
        [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ $f"
    done
    [ -d "configs" ] && echo "  ✓ configs/ ($(ls configs/ | wc -l) files)" || echo "  ✗ configs/"
    echo ""
}

# ============================================================
# do_train: 训练 + 评估
# ============================================================
do_train() {
    echo "============================================================"
    echo "  Phase 2: Training & Evaluation"
    echo "============================================================"

    activate_conda
    cd "$WORK_DIR"

    echo ""
    echo "[1/4] Training ResNet-18..."
    mim train mmpretrain configs/resnet18_flowers17.py
    echo "  ✓ ResNet-18 done"

    echo ""
    echo "[2/4] Training MobileNet V2..."
    mim train mmpretrain configs/mobilenetv2_flowers17.py
    echo "  ✓ MobileNet V2 done"

    echo ""
    echo "[3/4] Evaluating..."
    python evaluate.py

    echo ""
    echo "[4/4] Copying results to Windows..."
    if [ -d "$WIN_PROJECT" ]; then
        cp -r work_dirs "$WIN_PROJECT/" 2>/dev/null || true
        cp -r assignment1_images "$WIN_PROJECT/" 2>/dev/null || true
        echo "  ✓ Results copied"
    fi

    echo ""
    echo "============================================================"
    echo "  ✓ All done!"
    echo "============================================================"
}

# ============================================================
# Main
# ============================================================
case "${1:-}" in
    setup) do_setup ;;
    check) do_check ;;
    train) do_train ;;
    all)   do_setup; do_check; do_train ;;
    *)     show_usage ;;
esac
