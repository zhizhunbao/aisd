---
topic: gazebo
dimension: code
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo Simulator — https://gazebosim.org/home"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "💻 Source: create3_sim — https://github.com/iRobotEducation/create3_sim"
expiry: 6m
status: current
---

# Gazebo 仿真器 代码参考

> 📖 Docs: [Gazebo](https://gazebosim.org/home), [Create 3 Sim](https://iroboteducation.github.io/create3_docs/sim/setup/), [create3_sim GitHub](https://github.com/iRobotEducation/create3_sim)

## 快速开始

### 最简示例 — 安装并启动 Gazebo + Create 3 仿真

```bash
# ============================================================
# 1. 安装 Classic Gazebo 11 (Ubuntu 22.04)
# ============================================================
sudo apt update && sudo apt upgrade -y
curl -sSL http://get.gazebosim.org | sh

# 验证安装 / Verify installation
gazebo --version
# 输出应显示: Gazebo multi-robot simulator, version 11.x.x

# ============================================================
# 2. 启动空世界测试 / Launch empty world test
# ============================================================
gazebo
# 应弹出 Gazebo GUI 窗口，显示空的仿真世界
# Ctrl+C 退出
```

> 📖 Slides: CST8509 Week 7 Slide 5

---

## 完整实现示例

### 示例 1: 安装 Create 3 仿真器（ROS 2 Humble + Classic Gazebo 11）

```bash
# ============================================================
# 前置条件：已安装 ROS 2 Humble 和 Classic Gazebo 11
# ============================================================

# 1. 创建工作空间 / Create workspace
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src

# 2. 克隆 Create 3 仿真包 / Clone Create 3 sim packages
git clone https://github.com/iRobotEducation/create3_sim.git -b humble

# 3. 安装依赖 / Install dependencies
cd ~/create3_ws
rosdep install --from-paths src --ignore-src -r -y

# 4. 编译 / Build
colcon build --symlink-install

# 5. Source 工作空间 / Source workspace
source install/setup.bash

# 6. 启动 Create 3 仿真 / Launch Create 3 simulation
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py
# 应看到 Gazebo 窗口中出现 Create 3 机器人
```

> 📖 Docs: [Create 3 Sim Setup](https://iroboteducation.github.io/create3_docs/sim/setup/); 📖 Slides: CST8509 Week 7 Slide 13

### 示例 2: 通过 ROS 2 控制仿真 Create 3

```bash
# ============================================================
# 在另一个终端中（已 source 工作空间）
# ============================================================

# 查看所有可用话题 / List available topics
ros2 topic list
# 应看到 /cmd_vel, /odom, /scan 等话题

# 发送速度命令让机器人前进 / Send velocity command
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" \
  --rate 10
# 机器人应该开始前进

# 让机器人转圈 / Make robot spin
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}" \
  --rate 10
```

> 📖 Slides: CST8509 Week 7 Slide 6 (Twist Messages from Move Module)

### 示例 3: Python 中通过 ROS 2 控制 Create 3

```python
# ============================================================
# create3_controller.py — 用 Python/ROS 2 控制仿真 Create 3
# ============================================================
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Create3Controller(Node):
    """简单的 Create 3 控制器 / Simple Create 3 Controller"""
    def __init__(self):
        super().__init__('create3_controller')
        # 创建速度命令发布者 / Create velocity publisher
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        # 每 0.1 秒发布一次 / Publish every 0.1 seconds
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.step = 0

    def timer_callback(self):
        msg = Twist()
        if self.step < 50:
            # 前进 5 秒 / Move forward for 5 seconds
            msg.linear.x = 0.3   # 0.3 m/s 前进
            msg.angular.z = 0.0
            self.get_logger().info(f'前进 / Moving forward: step {self.step}')
        elif self.step < 80:
            # 左转 3 秒 / Turn left for 3 seconds
            msg.linear.x = 0.0
            msg.angular.z = 1.0  # 1.0 rad/s 左转
            self.get_logger().info(f'左转 / Turning left: step {self.step}')
        else:
            # 停止 / Stop
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('停止 / Stopped')

        self.publisher.publish(msg)
        self.step += 1

def main():
    rclpy.init()
    controller = Create3Controller()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

> 📖 Slides: CST8509 Week 7 Slides 6, 12

### 示例 4: 给 Create 3 添加虚拟摄像头的 URDF 片段

```xml
<!-- ============================================================
     camera.urdf.xacro — 给 Create 3 添加虚拟摄像头
     ============================================================ -->
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- 摄像头链接 / Camera Link -->
  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.02 0.02 0.02"/>  <!-- 2cm 方块代表摄像头 -->
      </geometry>
    </visual>
  </link>

  <!-- 把摄像头固定到机器人顶部 / Attach camera to robot top -->
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.1 0 0.15" rpy="0 0 0"/>  <!-- 前方 10cm, 高 15cm -->
  </joint>

  <!-- Gazebo 摄像头插件 / Gazebo camera plugin -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="gazebo_camera">
      <update_rate>30</update_rate>
      <camera>
        <horizontal_fov>1.3962634</horizontal_fov>  <!-- 80° 视场角 -->
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.02</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <namespace>/create3</namespace>
          <remapping>image_raw:=camera/image</remapping>
        </ros>
        <camera_name>camera</camera_name>
      </plugin>
    </sensor>
  </gazebo>

</robot>
```

> 📖 Slides: CST8509 Week 7 Slides 14-15; Lab 4 涉及添加虚拟摄像头

---

## API 速查

### ROS 2 CLI 常用命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `ros2 topic list` | 列出所有话题 | 查看 Gazebo 发布了什么 |
| `ros2 topic echo <topic>` | 查看话题消息 | `ros2 topic echo /odom` |
| `ros2 topic pub <topic> <type> <data>` | 发布消息 | 发送 Twist 控制命令 |
| `ros2 node list` | 列出所有节点 | 确认 Gazebo 节点在运行 |
| `ros2 launch <pkg> <file>` | 启动 launch 文件 | 启动 Create 3 仿真 |

### Gazebo CLI 常用命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `gazebo` | 启动空世界 | 测试安装 |
| `gazebo --verbose` | 带详细日志启动 | 排查启动问题 |
| `gzserver` | 无头模式 (无 GUI) | 加速训练 |
| `gzclient` | 单独启动 GUI | 连接到已运行的 gzserver |

### Create 3 常用 ROS 2 话题

| 话题 | 消息类型 | 方向 | 用途 |
|------|---------|------|------|
| `/cmd_vel` | `geometry_msgs/Twist` | Agent → Robot | 速度控制 |
| `/odom` | `nav_msgs/Odometry` | Robot → Agent | 位置和速度 |
| `/scan` | `sensor_msgs/LaserScan` | Robot → Agent | 激光雷达扫描 |
| `/camera/image` | `sensor_msgs/Image` | Robot → Agent | 摄像头图像 |
| `/imu` | `sensor_msgs/Imu` | Robot → Agent | 惯性测量 |

---

## 目录结构模板

### Lab 4 项目结构

```
create3_rl_lab/
├── create3_ws/                    ← ROS 2 工作空间
│   └── src/
│       ├── create3_sim/           ← iRobot 提供的仿真包
│       └── create3_rl/            ← 你的 RL 包
│           ├── create3_rl/
│           │   ├── __init__.py
│           │   ├── env.py         ← Gymnasium 环境（包装 ROS 2）
│           │   ├── agent.py       ← RL Agent
│           │   └── controller.py  ← Create 3 控制器
│           ├── launch/
│           │   └── rl_training.launch.py
│           ├── urdf/
│           │   └── camera.urdf.xacro  ← 虚拟摄像头
│           ├── package.xml
│           └── setup.py
└── README.md
```
