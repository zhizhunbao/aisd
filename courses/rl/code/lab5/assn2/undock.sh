#!/bin/bash
# 终端2: 解除停靠（Gazebo 加载完后执行）
source /opt/ros/humble/setup.bash
source ~/create3_ws/install/setup.bash
echo "Undocking robot..."
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}
