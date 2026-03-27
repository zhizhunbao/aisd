#!/bin/bash
# Step 8: 解除停靠 + 移动机器人
# Usage: bash step8_undock.sh

source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash

echo "Undocking robot..."
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}

echo ""
echo "Robot undocked. Move commands:"
echo "  Forward:  ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'"
echo "  Turn:     ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.5}}'"
echo "  Stop:     ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}'"
