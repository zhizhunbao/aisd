# Lab 4: Actor — 添加行走红球 + 红球检测

> **课程**: CST8509 Reinforcement Learning  
> **平台**: Ubuntu 22.04 (WSL2 或 Loaner Laptop)  
> **前置**: Lab 3 Gazebo 环境已安装完成

---

## WSL 目录结构

脚本执行后，WSL 中的工作空间结构如下：

```
/home/peng/create3_ws/
├── src/
│   ├── aws-robomaker-small-house-world/
│   │   └── worlds/
│   │       └── small_house.world          # ← 已注入 red_ball_actor
│   ├── create3_sim/                       # Lab 3 已有
│   │   └── .../urdf/
│   │       ├── create3.urdf.xacro         # Lab 3 已添加 camera include
│   │       └── camera.urdf.xacro          # Lab 3 已创建
│   └── aisd_vision/                       # ← 新建
│       ├── aisd_vision/
│       │   ├── __init__.py
│       │   └── redball.py                 # 红球检测节点
│       ├── resource/aisd_vision
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── build/
├── install/
└── log/
```

---

## 本地文件

```
code/lab4/
├── README.md                      # 本文件
├── lab4_operation_guide.md        # 手动操作手册
│
├── setup_lab4.sh                  # 🔧 一键安装（调用下面 4 个子脚本）
├── step1_add_human_actor.py       #    ├─ 添加人类 actor（验证用）
├── step2_add_red_ball.py          #    ├─ 注释人类 actor，添加红球
├── step3_check_camera.py          #    ├─ 检查 Lab 3 摄像头配置
├── step4_setup_package.py         #    └─ 创建 aisd_vision ROS 2 包
│
├── step6_start_gazebo.sh          # 🚀 启动 Gazebo（终端 1）
├── step7_run_redball.sh           # 🔴 启动红球检测（终端 2）
├── step8_undock.sh                # 🤖 解除停靠 + 移动命令（终端 3）
│
├── redball.py                     # 老师原版红球检测代码
└── actor_snippets.xml             # 3 段 actor XML（参考用）
```

---

## 快速使用

### Windows PowerShell 端

#### 1️⃣ 安装（一次性）

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/setup_lab4.sh
```

#### 2️⃣ 启动仿真（终端 1）

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/step6_start_gazebo.sh
```

#### 3️⃣ 启动红球检测（终端 2）

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/step7_run_redball.sh
```

#### 4️⃣ 解除停靠 + 移动（终端 3）

```powershell
wsl -d Ubuntu-22.04 -u peng -- bash /mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/step8_undock.sh
```

---

### Linux 端直接执行（在 WSL Ubuntu 终端中）

> ⚠️ **必须先设置** `export DISPLAY=:0`，否则 Gazebo/RViz 窗口无法显示

#### 1️⃣ 安装（一次性）

```bash
bash /mnt/c/Users/40270/Desktop/workspace/aisd/courses/rl/code/lab4/setup_lab4.sh
```

#### 2️⃣ 启动仿真（终端 1）

```bash
export DISPLAY=:0
source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash
source /usr/share/gazebo-11/setup.sh
export IGNITION_VERSION=fortress
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
```

#### 3️⃣ 启动红球检测（终端 2）

```bash
export DISPLAY=:0
source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash
ros2 run aisd_vision redball
```

#### 4️⃣ 解除停靠 + 移动（终端 3）

```bash
source /opt/ros/humble/setup.bash
source /home/peng/create3_ws/install/setup.bash

# 脱离充电座
ros2 action send_goal /undock irobot_create_msgs/action/Undock '{}'

# 移动命令
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'   # 前进
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.5}}'   # 左转
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}'   # 停止
```

#### 5️⃣ RViz 中查看检测结果

Add → By topic → `target_redball` → Image

---

## 提交

- 提交 `small_house.world` 到 Brightspace
- 路径: `/home/peng/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world`

## 演示

1. ✅ Gazebo 中红球来回移动
2. ✅ RViz 中 `target_redball` 显示绿圈标注
3. ✅ 准备回答代码问题
