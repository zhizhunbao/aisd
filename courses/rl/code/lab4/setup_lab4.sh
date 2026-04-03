#!/bin/bash
# ============================================================
# Lab 4 一键安装脚本
# 添加红球 actor + 检查摄像头 + 创建 aisd_vision 包 + 构建
# Usage: bash setup_lab4.sh
# ============================================================
set -e

SCRIPT_DIR="/mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4"
WS="/home/peng/create3_ws"

echo "=========================================="
echo "Lab 4 Setup - 一键安装"
echo "=========================================="

# ---------- Step 1: 添加红球 actor ----------
echo ""
echo "[Step 1] Adding red ball actor to small_house.world..."
python3 "$SCRIPT_DIR/step1_add_human_actor.py"
python3 "$SCRIPT_DIR/step2_add_red_ball.py"

# ---------- Step 2: 检查摄像头 ----------
echo ""
echo "[Step 2] Checking camera setup..."
python3 "$SCRIPT_DIR/step3_check_camera.py"

# ---------- Step 3: 创建 aisd_vision 包 ----------
echo ""
echo "[Step 3] Setting up aisd_vision package..."
python3 "$SCRIPT_DIR/step4_setup_package.py"

# ---------- Step 4: 构建 ----------
echo ""
echo "[Step 4] Building..."
cd "$WS"
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select aws_robomaker_small_house_world aisd_vision
source install/setup.bash

echo ""
echo "=========================================="
echo "✅ Lab 4 安装完成！"
echo "=========================================="
echo ""
echo "启动命令（各开一个终端）："
echo "  终端1: bash $SCRIPT_DIR/step6_start_gazebo.sh"
echo "  终端2: bash $SCRIPT_DIR/step7_run_redball.sh"
echo "  终端3: bash $SCRIPT_DIR/step8_undock.sh"
echo ""
