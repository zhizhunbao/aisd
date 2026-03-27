#!/bin/bash
# Step 6: 启动 Gazebo 仿真
# Usage: bash step6_start_gazebo.sh

source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash
source /usr/share/gazebo-11/setup.sh
export IGNITION_VERSION=fortress

echo "=========================================="
echo "  Lab 4: Launching Gazebo + Red Ball"
echo "=========================================="
echo ""
echo "  After Gazebo loads, in another terminal:"
echo "    bash step7_run_redball.sh"
echo ""
echo "  To undock robot:"
echo "    bash step8_undock.sh"
echo "=========================================="
echo ""

ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
