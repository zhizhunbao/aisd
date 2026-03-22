#!/bin/bash
# ============================================================
# Lab 3 一键环境安装脚本
# Ubuntu 22.04 WSL2 - ROS2 Humble + Gazebo 11 + Create3 Sim
# ============================================================
set -e

echo "=========================================="
echo "Step 1: 基础系统更新"
echo "=========================================="
sudo apt update && sudo apt upgrade -y

echo "=========================================="
echo "Step 2: 安装基础工具"
echo "=========================================="
sudo apt install -y curl wget git software-properties-common lsb-release gnupg2 build-essential cmake

echo "=========================================="
echo "Step 3: 安装 ROS 2 Humble"
echo "=========================================="
# 添加 ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 添加 ROS 2 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

# 安装 ROS 2 Humble Desktop (包含 RViz)
sudo apt install -y ros-humble-desktop

# 安装开发工具
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool

echo "=========================================="
echo "Step 4: 安装 Classic Gazebo 11"
echo "=========================================="
sudo apt install -y gazebo
sudo apt install -y ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control

echo "=========================================="
echo "Step 5: 初始化 rosdep"
echo "=========================================="
if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then
    sudo rosdep init
fi
rosdep update

echo "=========================================="
echo "Step 6: 配置 .bashrc"
echo "=========================================="
# 添加 ROS 2 环境
if ! grep -q "source /opt/ros/humble/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
fi

# 添加 Gazebo 环境
if ! grep -q "source /usr/share/gazebo-11/setup.sh" ~/.bashrc; then
    echo "source /usr/share/gazebo-11/setup.sh" >> ~/.bashrc
fi

# 立即加载
source /opt/ros/humble/setup.bash

echo "=========================================="
echo "Step 7: 创建工作空间并克隆 create3_sim"
echo "=========================================="
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src

if [ ! -d "create3_sim" ]; then
    git clone https://github.com/iRobotEducation/create3_sim.git
fi

cd create3_sim
git checkout humble

echo "=========================================="
echo "Step 8: 安装 create3_sim 依赖"
echo "=========================================="
cd ~/create3_ws
export IGNITION_VERSION=fortress
rosdep install --from-paths src -yi

echo "=========================================="
echo "Step 9: 构建 create3_ws"
echo "=========================================="
cd ~/create3_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install

echo "=========================================="
echo "Step 10: 下载 AWS Small House World"
echo "=========================================="
cd ~/create3_ws/src
if [ ! -d "aws-robomaker-small-house-world" ]; then
    git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git -b ros2
fi

cd ~/create3_ws
colcon build --symlink-install --packages-select aws_robomaker_small_house_world

echo "=========================================="
echo "Step 11: 添加工作空间到 .bashrc"
echo "=========================================="
if ! grep -q "source ~/create3_ws/install/setup.bash" ~/.bashrc; then
    echo "source ~/create3_ws/install/setup.bash" >> ~/.bashrc
fi

echo "=========================================="
echo "✅ 全部安装完成！"
echo "=========================================="
echo ""
echo "请执行以下命令加载环境："
echo "  source ~/.bashrc"
echo ""
echo "启动模拟器命令："
echo "  ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py"
echo ""
