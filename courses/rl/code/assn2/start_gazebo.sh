#!/bin/bash
# 终端1: 启动 Gazebo 仿真
source /opt/ros/humble/setup.bash
source ~/create3_ws/install/setup.bash
source /usr/share/gazebo-11/setup.sh
export IGNITION_VERSION=fortress
echo "Launching Gazebo... (wait for it to load)"
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
