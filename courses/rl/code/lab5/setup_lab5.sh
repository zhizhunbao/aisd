#!/bin/bash
# ============================================================
# Lab 5 一键部署脚本
# 准备 Docker 构建上下文 + 构建 + 运行
# Usage: bash setup_lab5.sh
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSN2_SRC="/mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/assn2"

echo "=========================================="
echo "Lab 5: Docker Setup - 一键部署"
echo "=========================================="

# ---------- Step 1: 准备构建上下文 ----------
echo ""
echo "[Step 1] Preparing build context..."

# Copy Assignment 2 code into the Docker build context
if [ -d "$SCRIPT_DIR/assn2" ]; then
    echo "  Removing old assn2 directory..."
    rm -rf "$SCRIPT_DIR/assn2"
fi

mkdir -p "$SCRIPT_DIR/assn2"

# If running from WSL, copy from Windows path
if [ -d "$ASSN2_SRC" ]; then
    echo "  Copying from WSL mount: $ASSN2_SRC"
    cp -r "$ASSN2_SRC/041107730_aisd_examples" "$SCRIPT_DIR/assn2/"
    cp "$ASSN2_SRC"/*.py "$SCRIPT_DIR/assn2/" 2>/dev/null || true
    cp "$ASSN2_SRC"/*.sh "$SCRIPT_DIR/assn2/" 2>/dev/null || true
    cp "$ASSN2_SRC"/README.md "$SCRIPT_DIR/assn2/" 2>/dev/null || true
    cp "$ASSN2_SRC"/.gitignore "$SCRIPT_DIR/assn2/" 2>/dev/null || true
elif [ -d "$HOME/Assn2" ]; then
    echo "  Copying from ~/Assn2"
    cp -r "$HOME/Assn2/"* "$SCRIPT_DIR/assn2/"
else
    echo "  ⚠️  Cannot find Assignment 2 code. Please copy manually:"
    echo "     Place your Assn2 files into: $SCRIPT_DIR/assn2/"
    exit 1
fi

# Fix Windows line endings
find "$SCRIPT_DIR/assn2" -type f \( -name "*.py" -o -name "*.sh" \) -exec sed -i 's/\r$//' {} \; 2>/dev/null || true

echo "  ✅ Build context prepared"

# ---------- Step 2: 允许 X11 转发 ----------
echo ""
echo "[Step 2] Configuring X11 access..."
xhost +local:docker 2>/dev/null || echo "  (xhost not available, skipping)"
echo "  ✅ X11 configured"

# ---------- Step 3: 构建 Docker 镜像 ----------
echo ""
echo "[Step 3] Building Docker image..."
cd "$SCRIPT_DIR"
docker compose build
echo "  ✅ Docker image built"

# ---------- Step 4: 启动容器 ----------
echo ""
echo "=========================================="
echo "✅ Lab 5 Docker 环境已就绪！"
echo "=========================================="
echo ""
echo "运行容器："
echo "  docker compose run ros2-create3"
echo ""
echo "容器内启动 Gazebo："
echo "  ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py"
echo ""
echo "容器内运行 Agent（另一个 shell）："
echo "  docker compose exec ros2-create3 bash"
echo "  cd /ros2_ws/assn2"
echo "  python3 null.py"
echo ""
