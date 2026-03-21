#!/bin/bash
# ============================================================
# CST8509 Lab 3: Gazebo Environment Install Script (Bash)
# Author: Peng Wang | Student Number: 041107730
#
# 在 WSL2 Ubuntu 22.04 中安装 ROS 2 Humble + Gazebo 11
# Run: wsl bash /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/install_gazebo.sh
# ============================================================

set -e  # 遇到错误立即退出 / Exit on error

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

step_num=0
total_steps=13

print_step() {
    step_num=$((step_num + 1))
    echo ""
    echo "============================================================"
    echo -e "  ${GREEN}Step ${step_num}/${total_steps}: $1${NC}"
    echo -e "  步骤 ${step_num}/${total_steps}: $2"
    echo "============================================================"
    echo ""
}

# ============================================================
# Step 1: 更新包列表 / Update packages
# ============================================================
print_step "Update packages" "更新包列表"
sudo apt update -y

# ============================================================
# Step 2: ROS 2 仓库密钥 / ROS 2 repository keys
# ============================================================
print_step "ROS 2 repository keys" "ROS 2 仓库密钥"
sudo apt install -y software-properties-common curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
    sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update -y

# ============================================================
# Step 3: 安装 ROS 2 Humble Desktop / Install ROS 2 Humble
# ============================================================
print_step "Install ROS 2 Humble Desktop" "安装 ROS 2 Humble Desktop（约 10-20 分钟）"
sudo DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop

# ============================================================
# Step 4: ROS 2 构建工具 / ROS 2 build tools
# ============================================================
print_step "ROS 2 build tools" "ROS 2 构建工具"
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool
sudo rosdep init 2>/dev/null || echo "rosdep already initialized"
rosdep update

# ============================================================
# Step 5: 安装 Gazebo 11 / Install Gazebo 11
# ============================================================
print_step "Install Gazebo 11" "安装 Gazebo 11"
sudo DEBIAN_FRONTEND=noninteractive apt install -y \
    gazebo libgazebo-dev \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control

# ============================================================
# Step 6: 创建工作空间 / Create workspace
# ============================================================
print_step "Create workspace" "创建工作空间"
mkdir -p ~/create3_ws/src

# ============================================================
# Step 7: 克隆 Create 3 模拟器 / Clone Create 3 simulator
# ============================================================
print_step "Clone Create 3 simulator" "克隆 Create 3 模拟器"
if [ -d ~/create3_ws/src/create3_sim ]; then
    echo "  create3_sim already exists, pulling latest..."
    cd ~/create3_ws/src/create3_sim
    git checkout humble
    git pull
else
    cd ~/create3_ws/src
    git clone -b humble https://github.com/iRobotEducation/create3_sim.git
fi

# ============================================================
# Step 8: 克隆 AWS Small House / Clone AWS Small House
# ============================================================
print_step "Clone AWS Small House" "克隆 AWS 小房子"
if [ -d ~/create3_ws/src/aws-robomaker-small-house-world ]; then
    echo "  AWS Small House already exists, pulling latest..."
    cd ~/create3_ws/src/aws-robomaker-small-house-world
    git pull
else
    cd ~/create3_ws/src
    git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git
fi

# ============================================================
# Step 9: 安装 ROS 依赖 / Install ROS dependencies
# ============================================================
print_step "Install ROS dependencies" "安装 ROS 依赖"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
export IGNITION_VERSION=fortress
rosdep install --from-paths src -y --ignore-src --skip-keys catkin

# ============================================================
# Step 10: 跳过 AWS 包构建 / Skip AWS Small House build
# ============================================================
print_step "Skip AWS Small House build" "跳过 AWS 包构建（ROS 1 catkin 包）"
touch ~/create3_ws/src/aws-robomaker-small-house-world/COLCON_IGNORE
echo "  ✅ COLCON_IGNORE added — only model files needed"

# ============================================================
# Step 11: 构建工作空间 / Build workspace
# ============================================================
print_step "Build workspace" "构建工作空间（约 10-30 分钟）"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
export IGNITION_VERSION=fortress
colcon build --symlink-install

# ============================================================
# Step 11: 复制 camera.urdf.xacro / Copy camera URDF
# ============================================================
print_step "Copy camera URDF" "复制摄像头 URDF"

CAMERA_SRC="/mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/camera.urdf.xacro"
CAMERA_DST=~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/camera.urdf.xacro
XACRO_FILE=~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro

if [ -f "$CAMERA_SRC" ]; then
    cp "$CAMERA_SRC" "$CAMERA_DST"
    echo "  ✅ Copied camera.urdf.xacro"
else
    echo -e "  ${RED}❌ camera.urdf.xacro not found at: $CAMERA_SRC${NC}"
    echo "  Please copy it manually."
fi

# 在 create3.urdf.xacro 中添加 camera include
# Add camera include to create3.urdf.xacro
if grep -q "camera.urdf.xacro" "$XACRO_FILE" 2>/dev/null; then
    echo "  ℹ️  camera.urdf.xacro already included"
else
    sed -i '/<\/robot>/i \    <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />' "$XACRO_FILE"
    echo "  ✅ Added camera include to create3.urdf.xacro"
fi

# ============================================================
# Step 12: 重建 description 包 / Rebuild description package
# ============================================================
print_step "Rebuild with camera" "重建摄像头包"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description

# ============================================================
# Step 13: 配置 bashrc / Configure bashrc
# ============================================================
print_step "Configure bashrc" "配置 bashrc"

LINES_TO_ADD=(
    "source /opt/ros/humble/setup.bash"
    "source ~/create3_ws/install/setup.bash"
    "source /usr/share/gazebo-11/setup.sh"
    "export IGNITION_VERSION=fortress"
)

for line in "${LINES_TO_ADD[@]}"; do
    if grep -Fq "$line" ~/.bashrc 2>/dev/null; then
        echo "  ℹ️  Already exists: $line"
    else
        echo "$line" >> ~/.bashrc
        echo "  ✅ Added: $line"
    fi
done

# ============================================================
# 完成 / Done
# ============================================================
echo ""
echo "============================================================"
echo -e "  ${GREEN}🎉 Installation complete! / 安装完成！${NC}"
echo "============================================================"
echo ""
echo "  Next steps / 后续步骤："
echo "  1. Close and reopen WSL terminal / 关闭并重新打开 WSL 终端"
echo "  2. Launch simulation / 启动仿真："
echo "     ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py"
echo "  3. Verify camera topics / 验证摄像头 topics："
echo "     ros2 topic list | grep camera"
echo ""
