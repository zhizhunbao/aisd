# Lab 3: Gazebo — Create3 仿真环境搭建

> **课程**: CST8509 Reinforcement Learning  
> **平台**: Windows + WSL2 Ubuntu 22.04  
> **目标**: ROS 2 Humble + Classic Gazebo 11 + iRobot Create3 + AWS Small House

---

## WSL 目录结构

脚本执行后，WSL 中的工作空间结构如下：

```
/home/peng/create3_ws/
├── src/
│   ├── create3_sim/                                   # iRobot Create3 仿真器 (humble 分支)
│   │   └── irobot_create_common/
│   │       └── irobot_create_description/
│   │           └── urdf/
│   │               ├── create3.urdf.xacro             # ← 已修改: 添加 camera include
│   │               └── camera.urdf.xacro              # ← 新建: 虚拟摄像头
│   └── aws-robomaker-small-house-world/               # AWS 小房子世界 (ros2 分支)
├── build/
├── install/
└── log/
```

## 本地文件

```
code/lab3/
├── README.md                      # 本文件
├── lab3_installation_guide.md     # 安装文档（Step 1-12）
├── lab3_operation_guide.md        # 操作手册（日常使用、命令速查）
│
├── setup_env.sh                   # 🔧 一键安装（ROS 2 + Gazebo + Create3 + AWS House）
├── start_gazebo.sh                # 🚀 启动 Gazebo 仿真
├── camera.urdf.xacro              # 📷 虚拟摄像头 URDF 定义
├── fix_xacro.py                   # 🔨 修复 create3.urdf.xacro（添加 camera include）
├── auto_explore.py                # 🤖 自动探索脚本（ROS 2 节点）
│
├── CST8509_Lab3_Gazebo.md         # 实验文档（Markdown 格式）
└── CST8509_Lab3_Gazebo_pages/     # 实验文档截图
```

---

## 脚本说明

### `setup_env.sh` — 一键安装

自动完成全部环境搭建（约 20-30 分钟）：
- 系统更新 + 基础工具
- ROS 2 Humble Desktop 安装
- Classic Gazebo 11 安装
- create3_sim 克隆 + 构建
- AWS Small House World 下载 + 构建
- `.bashrc` 环境变量配置

> 安装目标用户: `peng`（顶部 `USER_HOME` 可配置）

### `start_gazebo.sh` — 启动仿真

加载环境变量并启动 Create3 + AWS Small House 仿真，自动打开 Gazebo GUI + RViz。

### `camera.urdf.xacro` — 虚拟摄像头

定义挂载在 Create3 上的虚拟摄像头：
- 话题: `custom_ns/camera1/custom_img`
- 分辨率: 640×480，10fps
- 高度: base_link 上方 0.2m

### `fix_xacro.py` — 修复 URDF

在 `create3.urdf.xacro` 中添加 `camera.urdf.xacro` 的 include 行。

### `auto_explore.py` — 自动探索

ROS 2 节点，随机发布 `cmd_vel` 控制机器人自动探索环境。

---

## 快速使用

### 1️⃣ 首次安装（一次性）

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/setup_env.sh
```

安装完成后，手动操作（参考 `lab3_installation_guide.md` Step 10）：
```bash
# 复制 camera.urdf.xacro
cp /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/camera.urdf.xacro \
   /home/peng/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/

# 修复 create3.urdf.xacro
python3 /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/fix_xacro.py

# 重新构建
cd /home/peng/create3_ws && colcon build --symlink-install --packages-select irobot_create_description
```

### 2️⃣ 启动仿真

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/code/lab3/start_gazebo.sh
```

### 3️⃣ 操控机器人（另开终端）

```powershell
# 解除停靠
wsl -d Ubuntu-22.04 -u peng -- bash -c "source /home/peng/.bashrc && ros2 action send_goal /undock irobot_create_msgs/action/Undock {}"

# 前进
wsl -d Ubuntu-22.04 -u peng -- bash -c "source /home/peng/.bashrc && ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'"
```

更多命令见 `lab3_operation_guide.md`。
