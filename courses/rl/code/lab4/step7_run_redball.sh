#!/bin/bash
# Step 7: 启动红球检测节点
# Usage: bash step7_run_redball.sh

source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash

echo "=========================================="
echo "  Starting redball detection node"
echo "  Publishing to: target_redball"
echo "  In RViz: Add -> By topic -> target_redball -> Image"
echo "=========================================="
echo ""

ros2 run aisd_vision redball
