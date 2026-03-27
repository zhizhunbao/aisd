#!/bin/bash
# ============================================================
# Lab 3 - 启动 Gazebo Create3 + AWS Small House 仿真
# Usage: bash ~/start_gazebo.sh
# ============================================================

# ---------- 环境变量 ----------
source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash
source /usr/share/gazebo-11/setup.sh

export IGNITION_VERSION=fortress

# ---------- WSL2 显示配置 ----------
# WSLg (Windows 11) 自动支持 GUI，无需额外配置
# 如果用 VcXsrv 等外部 X Server，取消下面的注释：
# export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
# export LIBGL_ALWAYS_INDIRECT=0

# ---------- GPU 渲染回退 ----------
# WSL2 下 GPU 渲染可能有问题，使用软件渲染作为备选
# 如果 Gazebo 崩溃或黑屏，取消下面的注释：
# export LIBGL_ALWAYS_SOFTWARE=1
# export MESA_GL_VERSION_OVERRIDE=3.3

# ---------- 启动仿真 ----------
echo "============================================"
echo "  启动 Create3 + AWS Small House 仿真"
echo "  首次加载可能需要几分钟，请耐心等待..."
echo "============================================"
echo ""
echo "  摄像头 Topic: /custom_ns/camera1/custom_img"
echo "  摄像头 Info:  /custom_ns/camera1/custom_info"
echo ""
echo "  常用命令 (另开终端):"
echo "    ros2 topic list"
echo "    ros2 action send_goal /undock irobot_create_msgs/action/Undock {}"
echo "    ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \\"
echo "      '{linear: {x: 0.2}, angular: {z: 0.0}}'"
echo "============================================"
echo ""

ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
