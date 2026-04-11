#!/bin/bash
# ============================================================
# Assignment 2 一键安装脚本
# 安装依赖 + 安装环境包 + Git 初始化 + 验证
# Usage: bash setup_assn2.sh
# ============================================================
set -e

SCRIPT_DIR="/mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/assn2"
ASSN_DIR="$HOME/Assn2"

echo "=========================================="
echo "Assignment 2 Setup - 一键安装"
echo "=========================================="

# ---------- Step 1: 复制文件到 WSL ----------
echo ""
echo "[Step 1] Copying files to ~/Assn2..."
mkdir -p "$ASSN_DIR/screenshots"
cp "$SCRIPT_DIR"/*.py "$ASSN_DIR/"
cp "$SCRIPT_DIR"/.gitignore "$ASSN_DIR/"
cp "$SCRIPT_DIR"/README.md "$ASSN_DIR/"
cp "$SCRIPT_DIR"/start_gazebo.sh "$SCRIPT_DIR"/run_agent.sh "$SCRIPT_DIR"/undock.sh "$ASSN_DIR/" 2>/dev/null || true
# 修复 Windows 换行符并添加执行权限
sed -i 's/\r$//' "$ASSN_DIR"/*.sh "$ASSN_DIR"/*.py 2>/dev/null || true
chmod +x "$ASSN_DIR"/*.sh 2>/dev/null || true
# 用 rsync 避免重复运行时目录嵌套（cp -r 会嵌套已存在的目录）
rsync -a --delete "$SCRIPT_DIR/041107730_aisd_examples/" "$ASSN_DIR/041107730_aisd_examples/"
echo "  ✅ Files copied"

# ---------- Step 2: Source ROS 2 ----------
echo ""
echo "[Step 2] Sourcing ROS 2 environment..."
source /opt/ros/humble/setup.bash
source /usr/share/gazebo-11/setup.sh
source ~/create3_ws/install/setup.bash
echo "  ✅ ROS 2 Humble sourced"

# ---------- Step 3: 安装 pip（如果缺失）----------
echo ""
echo "[Step 3] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "  pip3 not found, installing..."
    sudo apt-get update -qq
    sudo apt-get install -y python3-pip
    echo "  ✅ pip3 installed"
else
    echo "  ✅ pip3 already installed"
fi

# ---------- Step 4: 安装 Python 依赖 ----------
echo ""
echo "[Step 4] Installing Python dependencies..."
pip3 install --upgrade pip "setuptools>=61,<80"
pip3 install "numpy<2" gymnasium matplotlib stable-baselines3
echo "  ✅ Python dependencies installed"

# ---------- Step 5: 安装 aisd_examples 环境包 ----------
echo ""
echo "[Step 5] Installing aisd_examples package..."
cd "$ASSN_DIR/041107730_aisd_examples"
pip3 install -e .
cd "$ASSN_DIR"
echo "  ✅ aisd_examples package installed"

# ---------- Step 6: Git 初始化 ----------
echo ""
echo "[Step 6] Initializing git..."
cd "$ASSN_DIR"
if [ ! -d ".git" ]; then
    git config --global user.name "Peng Wang"
    git config --global user.email "wang1059@algonquinlive.com"
    git init
    git add .gitignore README.md
    git commit -m "feat: initial project structure"
    git add 041107730_aisd_examples/
    git commit -m "feat: implement CreateRedBall-v0 gymnasium environment with RedBallNode"
    git add null.py
    git commit -m "feat: add null agent for environment testing"
    git add qlearning.py
    git commit -m "feat: implement Q-Learning agent with hyperparameter experiments"
    git add dqn.py ppo.py
    git commit -m "feat: integrate Stable-Baselines3 DQN and PPO agents"
    git add non-rl.py
    git commit -m "feat: add non-RL agent for comparison"
    # Note: test_imports.py and setup_assn2.sh are NOT committed to git
    # (they are helper scripts not listed in the assignment directory structure)
    echo "  ✅ Git initialized with commits"
else
    echo "  ✅ Git already initialized"
fi

# ---------- Step 7: 验证导入 ----------
echo ""
echo "[Step 7] Verifying imports..."
python3 "$ASSN_DIR/test_imports.py"

echo ""
echo "=========================================="
echo "✅ Assignment 2 安装完成！"
echo "=========================================="
echo ""
echo "运行命令（先启动 Gazebo 仿真）："
echo "  终端1: bash $SCRIPT_DIR/start_gazebo.sh   (或用你 Lab 4 的启动脚本)"
echo "  终端2: cd ~/Assn2"
echo ""
echo "  # 测试空代理"
echo "  python3 null.py"
echo ""
echo "  # Q-Learning 训练"
echo "  python3 qlearning.py"
echo ""
echo "  # DQN 训练"
echo "  python3 dqn.py"
echo ""
echo "  # PPO 训练"
echo "  python3 ppo.py"
echo ""
echo "  # 非 RL 对比"
echo "  python3 non-rl.py"
echo ""
