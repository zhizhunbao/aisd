# Lab 3 安装文档：Gazebo Create3 仿真环境

> **平台**: Windows + WSL2 Ubuntu 22.04  
> **目标**: ROS 2 Humble + Classic Gazebo 11 + iRobot Create3 Simulator + AWS Small House

---

## 1. WSL2 安装 Ubuntu 22.04

```powershell
# 查看已有发行版
wsl --list --verbose

# 如需重装，先卸载旧的
wsl --unregister Ubuntu-22.04

# 安装 Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

安装完成后在弹出的终端中设置用户名和密码。

---

## 2. 系统更新 & 基础工具

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git software-properties-common \
    lsb-release gnupg2 build-essential cmake
```

---

## 3. 安装 ROS 2 Humble

```bash
# 添加 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

# 添加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update

# 安装 Desktop 版 (含 RViz)
sudo apt install -y ros-humble-desktop

# 安装开发工具
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool
```

---

## 4. 安装 Classic Gazebo 11

```bash
sudo apt install -y gazebo
sudo apt install -y ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros2-control
```

---

## 5. 初始化 rosdep

```bash
sudo rosdep init
rosdep update
```

---

## 6. 创建工作空间 & 克隆 Create3 Sim

```bash
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src

# 克隆 create3_sim 仓库
git clone https://github.com/iRobotEducation/create3_sim.git
cd create3_sim
git checkout humble
```

---

## 7. 安装依赖 & 构建

```bash
cd ~/create3_ws
source /opt/ros/humble/setup.bash
export IGNITION_VERSION=fortress

# 安装依赖
rosdep install --from-paths src -yi

# 构建
colcon build --symlink-install
```

---

## 8. 下载 AWS Small House World

```bash
cd ~/create3_ws/src
git clone https://github.com/aws-robotics/aws-robomaker-small-house-world.git -b ros2

cd ~/create3_ws
colcon build --symlink-install --packages-select aws_robomaker_small_house_world
```

---

## 9. 配置环境变量

将以下内容添加到 `~/.bashrc` 末尾：

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
echo 'source /usr/share/gazebo-11/setup.sh' >> ~/.bashrc
echo 'source ~/create3_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

---

## 10. 创建虚拟摄像头

### 10.1 创建 `camera.urdf.xacro`

在 `~/create3_ws/src/create3_sim/irobot_create_common/irobot_create_description/urdf/` 目录下创建 `camera.urdf.xacro`：

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" >

    <!-- Part 1: 关节和链接 -->
    <joint name="camera_joint" type="fixed">
        <parent link="base_link"/>
        <child link="camera_link"/>
        <origin xyz="0 0 0.2" rpy="0 0 0"/>
    </joint>

    <link name="camera_link">
        <visual>
            <geometry>
                <box size="0.010 0.03 0.03"/>
            </geometry>
            <material name="red"/>
        </visual>
    </link>

    <material name="red">
        <color rgba="1 0 0 1"/>
    </material>

    <!-- Part 2: 光学链接 (ROS→光学坐标转换) -->
    <joint name="camera_optical_joint" type="fixed">
        <parent link="camera_link"/>
        <child link="camera_link_optical"/>
        <origin xyz="0 0 0" rpy="${-pi/2} 0 ${-pi/2}"/>
    </joint>

    <link name="camera_link_optical"></link>

    <!-- Part 3: Gazebo 摄像头插件 -->
    <gazebo reference="camera_link">
        <material name="red"/>
        <sensor name="camera" type="camera">
            <pose> 0 0 0 0 0 0 </pose>
            <visualize>true</visualize>
            <update_rate>10</update_rate>
            <camera name="head">
                <horizontal_fov>1.089</horizontal_fov>
                <image>
                    <format>R8G8B8</format>
                    <width>640</width>
                    <height>480</height>
                </image>
                <clip>
                    <near>0.05</near>
                    <far>8.0</far>
                </clip>
            </camera>

            <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
                <ros>
                    <namespace>custom_ns</namespace>
                    <remapping>image_raw:=custom_img</remapping>
                    <remapping>camera_info:=custom_info</remapping>
                </ros>
                <camera_name>camera1</camera_name>
                <frame_name>camera_link_optical</frame_name>
                <hack_baseline>0.7</hack_baseline>
            </plugin>
        </sensor>
    </gazebo>

</robot>
```

### 10.2 修改 `create3.urdf.xacro`

在 `create3.urdf.xacro` 文件中 `wheel_with_wheeldrop.urdf.xacro` 的 include 行后面添加：

```xml
  <xacro:include filename="$(find irobot_create_description)/urdf/camera.urdf.xacro" />
```

### 10.3 重新构建

```bash
cd ~/create3_ws
colcon build --symlink-install --packages-select irobot_create_description
```

---

## 11. 启动仿真

```bash
source ~/.bashrc
ros2 launch irobot_create_gazebo_bringup create3_gazebo_aws_small.launch.py
```

> [!NOTE]
> 首次启动需要几分钟加载模型，GUI 可能会短暂显示 "Not Responding"，属正常现象。

---

## 12. 验证与操控

另开一个终端：

```bash
source ~/.bashrc

# 确认摄像头 topic
ros2 topic list | grep custom
# 应看到:
#   /custom_ns/camera1/custom_img
#   /custom_ns/camera1/custom_info

# 解除停靠
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}

# 前进
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.2}, angular: {z: 0.0}}'

# 转弯
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0}, angular: {z: 0.5}}'

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0}, angular: {z: 0.0}}'
```

在 RViz 中查看摄像头：**Add → By topic → /custom_ns/camera1/custom_img → Image**

---

## 常见问题

| 问题 | 解决方法 |
|------|----------|
| Gazebo GUI 黑屏/崩溃 | 在启动前设置 `export LIBGL_ALWAYS_SOFTWARE=1` |
| 摄像头 topic 不出现 | 确认已执行 `source /usr/share/gazebo-11/setup.sh` |
| RViz 中 Create3 全白 | 终端 `Ctrl+C` 后重新启动 launch |
| colcon build 失败 | 先 `rm -rf build install log` 再重新构建 |

---

## 目录结构

```
~/create3_ws/
├── src/
│   ├── create3_sim/                          # humble 分支
│   │   └── irobot_create_common/
│   │       └── irobot_create_description/
│   │           └── urdf/
│   │               ├── create3.urdf.xacro    # 已修改: 添加 camera include
│   │               └── camera.urdf.xacro     # 新建: 虚拟摄像头
│   └── aws-robomaker-small-house-world/      # ros2 分支
├── build/
├── install/
└── log/
```
