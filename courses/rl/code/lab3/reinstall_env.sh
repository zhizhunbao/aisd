#!/bin/bash
# ============================================================
# CST8509 Lab 3: Gazebo Environment Reinstall Script
# Author: Peng Wang | Student Number: 041107730
#
# 在 WSL2 Ubuntu 22.04 中 **彻底清除** 并重新安装
# ROS 2 Humble + Gazebo 11 + Create 3 模拟器 + AWS Small House
#
# Run:
#   wsl bash /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/reinstall_env.sh
#
# Options:
#   --yes       跳过确认提示 / Skip confirmation prompts
#   --keep-ros  保留 ROS 2（只清除 workspace）/ Keep ROS 2 (only clean workspace)
# ============================================================

set -e  # 遇到错误立即退出 / Exit on error

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================
# 参数解析 / Parse Arguments
# ============================================================
AUTO_YES=false
KEEP_ROS=false

for arg in "$@"; do
    case $arg in
        --yes)   AUTO_YES=true ;;
        --keep-ros) KEEP_ROS=true ;;
        *)       echo -e "${RED}Unknown option: $arg${NC}"; exit 1 ;;
    esac
done

# ============================================================
# 辅助函数 / Helper Functions
# ============================================================
step_num=0
total_steps=0  # 会在后面动态设置 / Set dynamically below

print_step() {
    step_num=$((step_num + 1))
    echo ""
    echo "============================================================"
    echo -e "  ${GREEN}Step ${step_num}/${total_steps}: $1${NC}"
    echo -e "  步骤 ${step_num}/${total_steps}: $2"
    echo "============================================================"
    echo ""
}

confirm() {
    if [ "$AUTO_YES" = true ]; then
        return 0
    fi
    read -p "  ❓ $1 (y/n): " response
    case "$response" in
        y|Y|yes|YES|"") return 0 ;;
        *) return 1 ;;
    esac
}

# ============================================================
# 欢迎信息 / Welcome
# ============================================================
echo ""
echo "============================================================"
echo -e "  ${CYAN}🔄 CST8509 Lab 3 — Gazebo Environment REINSTALLER${NC}"
echo "  彻底清除并重新安装 ROS 2 + Gazebo + Create 3 仿真环境"
echo "============================================================"
echo ""

if [ "$KEEP_ROS" = true ]; then
    echo -e "  ${YELLOW}Mode: --keep-ros — 仅清除工作空间，保留 ROS 2 和 Gazebo${NC}"
    echo "  Will only clean workspace and rebuild. ROS 2 / Gazebo stay."
    total_steps=8
else
    echo -e "  ${RED}Mode: FULL REINSTALL — 清除全部并重装${NC}"
    echo "  Will purge ROS 2, Gazebo, workspace, and reinstall everything."
    total_steps=15
fi

echo ""
echo "  This script will:"
echo "  此脚本将："
if [ "$KEEP_ROS" = false ]; then
    echo "    1. 杀死所有 ROS/Gazebo 进程 / Kill all ROS/Gazebo processes"
    echo "    2. 删除 ~/create3_ws 工作空间 / Remove workspace"
    echo "    3. 卸载 ROS 2 Humble / Purge ROS 2 Humble"
    echo "    4. 卸载 Gazebo 11 / Purge Gazebo 11"
    echo "    5. 清理 bashrc 中的相关配置 / Clean bashrc entries"
    echo "    6. 重新安装全部环境 / Reinstall everything from scratch"
else
    echo "    1. 杀死所有 ROS/Gazebo 进程 / Kill all ROS/Gazebo processes"
    echo "    2. 删除 ~/create3_ws 工作空间 / Remove workspace"
    echo "    3. 重新克隆并构建 / Re-clone and rebuild"
fi

echo ""
if ! confirm "Proceed with reinstallation? / 确认重新安装？"; then
    echo -e "  ${YELLOW}Cancelled. / 已取消。${NC}"
    exit 0
fi

echo ""
echo -e "  ${GREEN}Starting reinstallation...${NC}"
echo "  开始重新安装..."

# ============================================================
# Phase 1: 清理 / Cleanup
# ============================================================

# --- Kill running processes / 杀死运行中的进程 ---
print_step "Kill ROS/Gazebo processes" "终止 ROS/Gazebo 进程"

echo "  Killing gzserver, gzclient, ros2, rviz2..."
echo "  终止 gzserver, gzclient, ros2, rviz2..."
killall -9 gzserver gzclient ros2 rviz2 2>/dev/null || echo "  ℹ️  No processes to kill / 没有需要终止的进程"
sleep 1

# --- Remove workspace / 删除工作空间 ---
print_step "Remove workspace" "删除工作空间"

if [ -d ~/create3_ws ]; then
    echo "  Removing ~/create3_ws..."
    echo "  删除 ~/create3_ws..."
    rm -rf ~/create3_ws
    echo -e "  ${GREEN}✅ Workspace removed${NC}"
else
    echo "  ℹ️  ~/create3_ws does not exist, skipping / 工作空间不存在，跳过"
fi

if [ "$KEEP_ROS" = false ]; then
    # --- Clean bashrc / 清理 bashrc ---
    print_step "Clean bashrc" "清理 bashrc 配置"

    LINES_TO_REMOVE=(
        "source /opt/ros/humble/setup.bash"
        "source ~/create3_ws/install/setup.bash"
        "source /usr/share/gazebo-11/setup.sh"
        "export IGNITION_VERSION=fortress"
    )

    for line in "${LINES_TO_REMOVE[@]}"; do
        if grep -Fq "$line" ~/.bashrc 2>/dev/null; then
            # 使用 sed 删除该行（转义特殊字符）
            escaped=$(printf '%s\n' "$line" | sed 's/[\/&]/\\&/g')
            sed -i "/$escaped/d" ~/.bashrc
            echo "  ✅ Removed: $line"
        else
            echo "  ℹ️  Not found: $line"
        fi
    done

    # --- Purge ROS 2 / 卸载 ROS 2 ---
    print_step "Purge ROS 2 Humble" "卸载 ROS 2 Humble"

    echo "  Purging ros-humble-* packages..."
    echo "  卸载 ros-humble-* 包..."
    sudo apt purge -y 'ros-humble-*' 2>/dev/null || echo "  ℹ️  No ROS 2 packages found"

    echo "  Removing ROS 2 apt source..."
    echo "  删除 ROS 2 apt 源..."
    sudo rm -f /etc/apt/sources.list.d/ros2.list
    sudo rm -f /usr/share/keyrings/ros-archive-keyring.gpg

    echo "  Removing rosdep cache..."
    echo "  删除 rosdep 缓存..."
    sudo rm -rf /etc/ros/rosdep/sources.list.d/20-default.list 2>/dev/null || true
    rm -rf ~/.ros/rosdep 2>/dev/null || true

    # --- Purge Gazebo / 卸载 Gazebo ---
    print_step "Purge Gazebo 11" "卸载 Gazebo 11"

    echo "  Purging gazebo packages..."
    echo "  卸载 gazebo 包..."
    sudo apt purge -y gazebo libgazebo-dev 2>/dev/null || echo "  ℹ️  No Gazebo packages found"

    # --- Autoremove & clean / 清理残留 ---
    print_step "Autoremove & clean" "清理残留包"

    echo "  Running apt autoremove..."
    echo "  运行 apt autoremove..."
    sudo apt autoremove -y
    sudo apt autoclean -y

    echo -e "  ${GREEN}✅ Cleanup complete!${NC}"
    echo "  清理完成！"
fi

# ============================================================
# Phase 2: 重新安装 / Reinstall
# ============================================================

if [ "$KEEP_ROS" = false ]; then
    # --- Update packages / 更新包列表 ---
    print_step "Update packages" "更新包列表"
    sudo apt update -y

    # --- ROS 2 keys / ROS 2 密钥 ---
    print_step "ROS 2 repository keys" "ROS 2 仓库密钥"
    sudo apt install -y software-properties-common curl gnupg lsb-release
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
        -o /usr/share/keyrings/ros-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
    http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
        sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    sudo apt update -y

    # --- Install ROS 2 / 安装 ROS 2 ---
    print_step "Install ROS 2 Humble Desktop" "安装 ROS 2 Humble Desktop（约 10-20 分钟）"
    sudo DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop

    # --- ROS 2 build tools / ROS 2 构建工具 ---
    print_step "ROS 2 build tools" "ROS 2 构建工具"
    sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool
    sudo rosdep init 2>/dev/null || echo "rosdep already initialized"
    rosdep update

    # --- Install Gazebo 11 / 安装 Gazebo ---
    print_step "Install Gazebo 11" "安装 Gazebo 11"
    sudo DEBIAN_FRONTEND=noninteractive apt install -y \
        gazebo libgazebo-dev \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-gazebo-ros2-control
fi

# --- Create workspace / 创建工作空间 ---
print_step "Create workspace" "创建工作空间"
mkdir -p ~/create3_ws/src

# --- Clone Create 3 / 克隆 Create 3 ---
print_step "Clone Create 3 simulator" "克隆 Create 3 模拟器"
cd ~/create3_ws/src
git clone -b humble https://github.com/iRobotEducation/create3_sim.git
echo -e "  ${GREEN}✅ create3_sim cloned (humble branch)${NC}"

# --- Clone AWS Small House / 克隆 AWS 小房子 ---
print_step "Clone AWS Small House" "克隆 AWS 小房子"
cd ~/create3_ws/src
git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git
echo -e "  ${GREEN}✅ AWS Small House cloned${NC}"

# --- Install ROS deps / 安装 ROS 依赖 ---
print_step "Install ROS dependencies" "安装 ROS 依赖"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
export IGNITION_VERSION=fortress
rosdep install --from-paths src -y --ignore-src --skip-keys catkin

# --- Skip AWS Small House build / 跳过 AWS 包构建 ---
# AWS Small House 是 ROS 1 catkin 包，不能用 colcon 编译
# 只需要它的模型文件（SDF/worlds），不需要编译
# It's a ROS 1 catkin package — only model files are needed, not compilation
touch ~/create3_ws/src/aws-robomaker-small-house-world/COLCON_IGNORE
echo -e "  ${GREEN}✅ COLCON_IGNORE added for aws_robomaker_small_house_world${NC}"

# --- Build workspace / 构建工作空间 ---
print_step "Build workspace" "构建工作空间（约 10-30 分钟）"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
export IGNITION_VERSION=fortress
colcon build --symlink-install

# --- Copy camera URDF / 复制摄像头 URDF ---
print_step "Copy camera URDF" "复制摄像头 URDF"

CAMERA_SRC="/mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/camera.urdf.xacro"
CAMERA_DST=~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/camera.urdf.xacro
XACRO_FILE=~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro

if [ -f "$CAMERA_SRC" ]; then
    cp "$CAMERA_SRC" "$CAMERA_DST"
    echo -e "  ${GREEN}✅ Copied camera.urdf.xacro${NC}"
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
    echo -e "  ${GREEN}✅ Added camera include to create3.urdf.xacro${NC}"
fi

# --- Rebuild description / 重建 description 包 ---
print_step "Rebuild with camera" "重建摄像头包"
source /opt/ros/humble/setup.bash
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description

# --- Configure bashrc / 配置 bashrc ---
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
echo -e "  ${GREEN}🎉 Reinstallation complete! / 重新安装完成！${NC}"
echo "============================================================"
echo ""
echo "  Next steps / 后续步骤："
echo "  1. Close and reopen WSL terminal / 关闭并重新打开 WSL 终端"
echo "  2. Verify environment / 验证环境："
echo "     python /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/check_env.py"
echo "  3. Launch simulation / 启动仿真："
echo "     ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py"
echo "  4. Verify camera topics / 验证摄像头 topics："
echo "     ros2 topic list | grep camera"
echo ""
