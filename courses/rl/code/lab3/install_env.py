"""
CST8509 Lab 3: Gazebo Environment Install Script
Author: Peng Wang
Student Number: 041107730

Automates the installation of ROS 2 Humble, Gazebo 11, and the
iRobot Create 3 simulator with AWS Small House in WSL2 Ubuntu 22.04.

Run from Windows: python install_env.py
Prerequisites: WSL2 + Ubuntu 22.04 (run check_env.py first)
"""

import subprocess
import sys
import os
import time
import argparse


# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 当前脚本所在目录（用于定位 camera.urdf.xacro）
# Current script directory (to locate camera.urdf.xacro)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# camera.urdf.xacro 文件路径（Windows 路径）
# Path to camera.urdf.xacro file (Windows path)
CAMERA_XACRO_FILE = os.path.join(SCRIPT_DIR, "camera.urdf.xacro")

# 安装步骤定义
# Installation step definitions
STEPS = [
    "wsl_setup",        # 0: 基础 WSL 设置
    "ros2_keys",        # 1: ROS 2 密钥和源
    "ros2_install",     # 2: 安装 ROS 2 Humble Desktop
    "ros2_deps",        # 3: ROS 2 依赖工具
    "gazebo_install",   # 4: 安装 Gazebo 11
    "workspace_create", # 5: 创建工作空间
    "clone_create3",    # 6: 克隆 create3_sim
    "clone_aws_house",  # 7: 克隆 AWS Small House
    "rosdep_install",   # 8: 安装 ROS 依赖
    "build_workspace",  # 9: 构建工作空间
    "copy_camera",      # 10: 复制 camera.urdf.xacro
    "build_camera",     # 11: 重建 description 包
    "setup_bashrc",     # 12: 配置 bashrc
]


# ============================================================
# 辅助函数
# Helper Functions
# ============================================================

def run_wsl(cmd, timeout=600, interactive=False):
    """
    在 WSL 中运行命令，实时输出
    Run a command inside WSL with real-time output
    """
    full_cmd = f'wsl -e bash -c "{cmd}"'

    if interactive:
        # 交互模式：直接执行，用户可以看到输出并输入
        # Interactive mode: direct execution
        result = subprocess.run(full_cmd, shell=True, timeout=timeout)
        return result.returncode == 0
    else:
        # 非交互模式：捕获输出
        # Non-interactive mode: capture output
        try:
            process = subprocess.Popen(
                full_cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            output_lines = []
            for line in iter(process.stdout.readline, ''):
                print(f"    {line}", end='')
                output_lines.append(line)
            process.wait(timeout=timeout)
            return process.returncode == 0
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"  ⚠️  Command timed out after {timeout}s")
            return False
        except Exception as e:
            print(f"  ⚠️  Error: {e}")
            return False


def run_wsl_sudo(cmd, timeout=600):
    """
    在 WSL 中以 sudo 运行命令（可能需要密码）
    Run a sudo command inside WSL (may need password)
    """
    print(f"  📌 Running: sudo {cmd[:80]}...")
    return run_wsl(f"sudo {cmd}", timeout=timeout, interactive=True)


def print_step(step_num, total, title_en, title_cn):
    """打印步骤标题 / Print step header"""
    print(f"\n{'='*60}")
    print(f"  Step {step_num}/{total}: {title_en}")
    print(f"  步骤 {step_num}/{total}: {title_cn}")
    print(f"{'='*60}\n")


def confirm(msg):
    """请求用户确认 / Ask user for confirmation"""
    response = input(f"  ❓ {msg} (y/n): ").strip().lower()
    return response in ('y', 'yes', '')


def check_wsl_exists():
    """
    检查 WSL 是否可用
    Check if WSL is available
    """
    try:
        result = subprocess.run(
            "wsl echo OK", shell=True,
            capture_output=True, text=True, timeout=10
        )
        return "OK" in result.stdout
    except:
        return False


def wsl_path(windows_path):
    """
    将 Windows 路径转换为 WSL 路径
    Convert Windows path to WSL path
    Example: C:\\Users\\foo -> /mnt/c/Users/foo
    """
    # 替换反斜杠为正斜杠
    path = windows_path.replace('\\', '/')
    # 处理驱动器盘符
    if len(path) >= 2 and path[1] == ':':
        drive = path[0].lower()
        path = f"/mnt/{drive}{path[2:]}"
    return path


# ============================================================
# 安装步骤
# Installation Steps
# ============================================================

def step_wsl_setup():
    """
    基础 WSL 设置：更新包列表
    Basic WSL setup: update package lists
    """
    print("  Updating package lists...")
    print("  更新包列表...\n")
    return run_wsl_sudo("apt update -y", timeout=120)


def step_ros2_keys():
    """
    配置 ROS 2 仓库密钥和源
    Configure ROS 2 repository keys and sources
    """
    cmds = [
        # 安装必要工具
        # Install required tools
        "sudo apt install -y software-properties-common curl gnupg lsb-release",
        # 添加 ROS 2 GPG 密钥
        # Add ROS 2 GPG key
        "sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg",
        # 添加 ROS 2 源
        # Add ROS 2 source
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null',
        # 更新包列表
        # Update package lists
        "sudo apt update -y",
    ]

    for cmd in cmds:
        print(f"  📌 Running: {cmd[:80]}...")
        if not run_wsl(cmd, interactive=True):
            print(f"  ⚠️  Command may have had issues, continuing...")
    return True


def step_ros2_install():
    """
    安装 ROS 2 Humble Desktop
    Install ROS 2 Humble Desktop
    """
    print("  This may take 10-20 minutes...")
    print("  可能需要 10-20 分钟...\n")
    return run_wsl_sudo(
        "DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop",
        timeout=1800
    )


def step_ros2_deps():
    """
    安装 ROS 2 依赖工具（colcon, rosdep 等）
    Install ROS 2 dependency tools (colcon, rosdep, etc.)
    """
    cmds = [
        # 安装 colcon 构建工具
        # Install colcon build tools
        "sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool",
        # 初始化 rosdep（如果尚未初始化）
        # Initialize rosdep (if not already done)
        "sudo rosdep init 2>/dev/null || echo 'rosdep already initialized'",
        # 更新 rosdep
        # Update rosdep
        "rosdep update",
    ]

    for cmd in cmds:
        print(f"  📌 Running: {cmd[:80]}...")
        if not run_wsl(cmd, interactive=True):
            print(f"  ⚠️  Command may have had issues, continuing...")
    return True


def step_gazebo_install():
    """
    安装 Classic Gazebo 11
    Install Classic Gazebo 11
    """
    print("  Installing Gazebo 11...")
    print("  安装 Gazebo 11...\n")
    return run_wsl_sudo(
        "DEBIAN_FRONTEND=noninteractive apt install -y gazebo libgazebo-dev ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control",
        timeout=600
    )


def step_workspace_create():
    """
    创建 ROS 2 工作空间目录
    Create ROS 2 workspace directory
    """
    print("  Creating ~/create3_ws/src directory...")
    print("  创建 ~/create3_ws/src 目录...\n")
    return run_wsl("mkdir -p ~/create3_ws/src")


def step_clone_create3():
    """
    克隆 iRobot Create 3 模拟器仓库
    Clone the iRobot Create 3 simulator repository
    """
    # 先检查是否已克隆
    # Check if already cloned
    result = subprocess.run(
        'wsl -e bash -c "test -d ~/create3_ws/src/create3_sim && echo EXISTS"',
        shell=True, capture_output=True, text=True
    )
    if "EXISTS" in result.stdout:
        print("  ℹ️  create3_sim already exists, pulling latest...")
        print("     create3_sim 已存在，拉取最新代码...\n")
        return run_wsl("cd ~/create3_ws/src/create3_sim && git checkout humble && git pull")

    print("  Cloning create3_sim (humble branch)...")
    print("  克隆 create3_sim（humble 分支）...\n")
    return run_wsl(
        "cd ~/create3_ws/src && git clone -b humble https://github.com/iRobotEducation/create3_sim.git",
        timeout=120
    )


def step_clone_aws_house():
    """
    克隆 AWS Small House World
    Clone the AWS Small House World
    """
    result = subprocess.run(
        'wsl -e bash -c "test -d ~/create3_ws/src/aws-robomaker-small-house-world && echo EXISTS"',
        shell=True, capture_output=True, text=True
    )
    if "EXISTS" in result.stdout:
        print("  ℹ️  AWS Small House already exists, pulling latest...")
        print("     AWS Small House 已存在，拉取最新代码...\n")
        return run_wsl("cd ~/create3_ws/src/aws-robomaker-small-house-world && git pull")

    print("  Cloning AWS Small House World...")
    print("  克隆 AWS 小房子世界...\n")
    return run_wsl(
        "cd ~/create3_ws/src && git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git",
        timeout=120
    )


def step_rosdep_install():
    """
    使用 rosdep 安装依赖
    Install dependencies using rosdep
    """
    print("  Installing ROS dependencies with rosdep...")
    print("  使用 rosdep 安装 ROS 依赖...\n")
    cmd = (
        "source /opt/ros/humble/setup.bash && "
        "cd ~/create3_ws && "
        "export IGNITION_VERSION=fortress && "
        "rosdep install --from-paths src -y --ignore-src --skip-keys catkin"
    )
    return run_wsl(cmd, timeout=300, interactive=True)


def step_build_workspace():
    """
    构建整个工作空间
    Build the entire workspace
    """
    # 先跳过 AWS Small House 构建（ROS 1 catkin 包）
    # Skip AWS Small House build first (ROS 1 catkin package)
    print("  Adding COLCON_IGNORE for aws_robomaker_small_house_world...")
    print("  跳过 AWS 包构建（ROS 1 catkin 包，只需模型文件）...\n")
    run_wsl("touch ~/create3_ws/src/aws-robomaker-small-house-world/COLCON_IGNORE")

    print("  Building workspace (this may take 10-30 minutes)...")
    print("  构建工作空间（可能需要 10-30 分钟）...\n")
    cmd = (
        "source /opt/ros/humble/setup.bash && "
        "cd ~/create3_ws && "
        "export IGNITION_VERSION=fortress && "
        "colcon build --symlink-install"
    )
    return run_wsl(cmd, timeout=1800, interactive=True)


def step_copy_camera():
    """
    复制 camera.urdf.xacro 到工作空间
    Copy camera.urdf.xacro to the workspace
    """
    if not os.path.exists(CAMERA_XACRO_FILE):
        print(f"  ❌ camera.urdf.xacro not found at: {CAMERA_XACRO_FILE}")
        return False

    # 转换路径
    # Convert path
    wsl_src = wsl_path(CAMERA_XACRO_FILE)
    wsl_dst = "~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/camera.urdf.xacro"

    print(f"  Copying camera.urdf.xacro to workspace...")
    print(f"  复制 camera.urdf.xacro 到工作空间...\n")

    # 复制文件
    # Copy file
    ok = run_wsl(f"cp '{wsl_src}' {wsl_dst}")
    if not ok:
        return False

    # 修改 create3.urdf.xacro 添加 camera include（如果尚未添加）
    # Modify create3.urdf.xacro to add camera include (if not already)
    xacro_file = "~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/create3.urdf.xacro"

    # 检查是否已添加
    # Check if already included
    result = subprocess.run(
        f'wsl -e bash -c "grep -l camera.urdf.xacro {xacro_file} 2>/dev/null"',
        shell=True, capture_output=True, text=True
    )

    if result.stdout.strip():
        print("  ℹ️  camera.urdf.xacro already included in create3.urdf.xacro")
        return True

    # 在 </robot> 前添加 include 行
    # Add include line before </robot>
    print("  Adding camera include to create3.urdf.xacro...")
    print("  在 create3.urdf.xacro 中添加摄像头引用...")

    include_line = '    <xacro:include filename=\\"$(find irobot_create_description)/urdf/camera.urdf.xacro\\" />'
    cmd = f"sed -i '/<\\/robot>/i {include_line}' {xacro_file}"
    return run_wsl(cmd)


def step_build_camera():
    """
    重建 description 包以包含摄像头
    Rebuild the description package to include the camera
    """
    print("  Rebuilding irobot_create_description package...")
    print("  重建 irobot_create_description 包...\n")
    cmd = (
        "source /opt/ros/humble/setup.bash && "
        "cd ~/create3_ws && "
        "colcon build --symlink-install --packages-select irobot_create_description"
    )
    return run_wsl(cmd, timeout=300, interactive=True)


def step_setup_bashrc():
    """
    配置 ~/.bashrc 文件
    Configure ~/.bashrc file
    """
    lines_to_add = [
        "source /opt/ros/humble/setup.bash",
        "source ~/create3_ws/install/setup.bash",
        "source /usr/share/gazebo-11/setup.sh",
        "export IGNITION_VERSION=fortress",
    ]

    print("  Configuring ~/.bashrc...")
    print("  配置 ~/.bashrc...\n")

    for line in lines_to_add:
        # 检查是否已存在
        # Check if line already exists
        result = subprocess.run(
            f'wsl -e bash -c "grep -Fq \'{line}\' ~/.bashrc && echo EXISTS || echo MISSING"',
            shell=True, capture_output=True, text=True
        )
        if "MISSING" in result.stdout:
            run_wsl(f"echo '{line}' >> ~/.bashrc")
            print(f"    ✅ Added: {line}")
        else:
            print(f"    ℹ️  Already exists: {line}")

    return True


# ============================================================
# 步骤映射
# Step Mapping
# ============================================================

STEP_FUNCTIONS = {
    "wsl_setup":        (step_wsl_setup,        "Update packages",           "更新包列表"),
    "ros2_keys":        (step_ros2_keys,         "ROS 2 repository keys",     "ROS 2 仓库密钥"),
    "ros2_install":     (step_ros2_install,      "Install ROS 2 Humble",      "安装 ROS 2 Humble"),
    "ros2_deps":        (step_ros2_deps,         "ROS 2 build tools",         "ROS 2 构建工具"),
    "gazebo_install":   (step_gazebo_install,    "Install Gazebo 11",         "安装 Gazebo 11"),
    "workspace_create": (step_workspace_create,  "Create workspace",          "创建工作空间"),
    "clone_create3":    (step_clone_create3,     "Clone Create 3 simulator",  "克隆 Create 3 模拟器"),
    "clone_aws_house":  (step_clone_aws_house,   "Clone AWS Small House",     "克隆 AWS 小房子"),
    "rosdep_install":   (step_rosdep_install,    "Install ROS dependencies",  "安装 ROS 依赖"),
    "build_workspace":  (step_build_workspace,   "Build workspace",           "构建工作空间"),
    "copy_camera":      (step_copy_camera,       "Copy camera URDF",          "复制摄像头 URDF"),
    "build_camera":     (step_build_camera,      "Rebuild with camera",       "重建摄像头包"),
    "setup_bashrc":     (step_setup_bashrc,      "Configure bashrc",          "配置 bashrc"),
}


# ============================================================
# 主程序
# Main Program
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Install Gazebo + ROS 2 environment for CST8509 Lab 3"
    )
    parser.add_argument(
        "--from-step", type=int, default=0,
        help="Start from step N (0-indexed). Use to resume after failure."
    )
    parser.add_argument(
        "--step", type=int, default=None,
        help="Run only step N (0-indexed)."
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all steps and exit."
    )
    args = parser.parse_args()

    # 列出所有步骤
    # List all steps
    if args.list:
        print("\nInstallation Steps:")
        print("-" * 50)
        for i, step_name in enumerate(STEPS):
            func, en, cn = STEP_FUNCTIONS[step_name]
            print(f"  {i:2d}. {en} / {cn}")
        print()
        return

    # 打印欢迎信息
    # Print welcome message
    print("\n" + "=" * 60)
    print("  🚀 CST8509 Lab 3 — Gazebo Environment Installer")
    print("  安装 ROS 2 Humble + Gazebo 11 + Create 3 模拟器")
    print("=" * 60)

    # 检查 WSL 是否可用
    # Check if WSL is available
    if not check_wsl_exists():
        print("\n  ❌ WSL is not available.")
        print("     WSL 不可用。请先安装 WSL2 + Ubuntu 22.04:")
        print("     wsl --install -d Ubuntu-22.04")
        return

    # 确定运行范围
    # Determine run range
    if args.step is not None:
        step_range = [args.step]
    else:
        step_range = range(args.from_step, len(STEPS))

    # 显示将要执行的步骤
    # Show steps to be executed
    print(f"\n  Steps to execute: / 即将执行的步骤:")
    for i in step_range:
        func, en, cn = STEP_FUNCTIONS[STEPS[i]]
        print(f"    {i:2d}. {en} / {cn}")

    print()
    if not confirm("Proceed with installation? / 开始安装？"):
        print("  Cancelled. / 已取消。")
        return

    # 执行安装步骤
    # Execute installation steps
    total = len(step_range)
    failed_step = None

    for idx, step_idx in enumerate(step_range):
        step_name = STEPS[step_idx]
        func, en, cn = STEP_FUNCTIONS[step_name]

        print_step(idx + 1, total, en, cn)

        success = func()

        if success:
            print(f"\n  ✅ Step {step_idx} completed successfully!")
            print(f"     步骤 {step_idx} 完成！")
        else:
            print(f"\n  ❌ Step {step_idx} failed!")
            print(f"     步骤 {step_idx} 失败！")
            if confirm("Continue anyway? / 仍然继续？"):
                continue
            else:
                failed_step = step_idx
                break

    # 完成总结
    # Completion summary
    print("\n" + "=" * 60)
    if failed_step is None:
        print("  🎉 Installation complete!")
        print("     安装完成！")
        print()
        print("  Next steps: / 后续步骤：")
        print("  1. Open WSL terminal: wsl")
        print("     打开 WSL 终端: wsl")
        print("  2. Launch simulation: / 启动仿真：")
        print("     ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py")
        print("  3. Verify camera topics: / 验证摄像头 topics：")
        print("     ros2 topic list | grep camera")
    else:
        print(f"  ⚠️  Installation stopped at step {failed_step}.")
        print(f"     安装在步骤 {failed_step} 停止。")
        print(f"     To resume: python install_env.py --from-step {failed_step}")
        print(f"     恢复安装: python install_env.py --from-step {failed_step}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
