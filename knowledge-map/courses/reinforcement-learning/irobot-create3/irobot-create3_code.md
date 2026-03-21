---
topic: irobot-create3
dimension: code
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: iRobot Create 3 — Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "📖 Docs: iRobot Create 3 — ROS 2 API — https://iroboteducation.github.io/create3_docs/api/ros2/"
  - "📖 Docs: iRobot Create 3 — Actuators CLI — https://iroboteducation.github.io/create3_docs/examples/actuators-cli/"
  - "💻 Source: create3_sim — https://github.com/iRobotEducation/create3_sim"
  - "💻 Source: create3_examples — https://github.com/iRobotEducation/create3_examples"
  - "📖 Docs: Gazebo URDF Tutorial — https://classic.gazebosim.org/tutorials?tut=ros_urdf"
expiry: 6m
status: current
---

# iRobot Create 3 代码参考

> 📖 Docs: [Simulator](https://iroboteducation.github.io/create3_docs/sim/setup/), [ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/), [Actuators CLI](https://iroboteducation.github.io/create3_docs/examples/actuators-cli/)
> 💻 Source: [create3_sim](https://github.com/iRobotEducation/create3_sim), [create3_examples](https://github.com/iRobotEducation/create3_examples)

## 快速开始

### 最简示例 — 部署 Create 3 仿真器并发送控制命令

```bash
# ============================================================
# 1. 安装 Classic Gazebo 11 (Ubuntu 22.04)
# ============================================================
sudo apt update && sudo apt upgrade -y
curl -sSL http://get.gazebosim.org | sh

# 验证安装
gazebo --version
# 输出应显示: Gazebo multi-robot simulator, version 11.x.x

# ============================================================
# 2. 安装 ROS 2 Humble Desktop
# ============================================================
sudo apt install ros-humble-desktop

# ============================================================
# 3. 克隆 Create 3 仿真器
# ============================================================
mkdir -p ~/create3_ws/src
cd ~/create3_ws/src
git clone https://github.com/iRobotEducation/create3_sim.git -b humble

# ============================================================
# 4. 安装依赖 + 编译
# ============================================================
cd ~/create3_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash

# ============================================================
# 5. 启动 Create 3 仿真
# ============================================================
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py
```

> 💻 Source: [create3_sim README](https://github.com/iRobotEducation/create3_sim)

---

## 完整实现示例

### 示例 1: ROS 2 CLI 控制 Create 3

```bash
# 在另一个终端（已 source 工作空间）

# 查看所有可用话题
ros2 topic list
# 应看到 /cmd_vel, /odom, /ir_intensity, /dock_status 等

# 解除对接（从充电站出发）
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}

# 前进 0.5 m/s
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" \
  --rate 10

# 左转 1 rad/s
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}" \
  --rate 10

# 前进 0.5 米然后停
ros2 action send_goal /drive_distance irobot_create_msgs/action/DriveDistance \
  "{distance: 0.5, max_translation_speed: 0.3}"

# 左转 90 度
ros2 action send_goal /rotate_angle irobot_create_msgs/action/RotateAngle \
  "{angle: 1.5708, max_rotation_speed: 1.0}"

# 回充电站
ros2 action send_goal /dock irobot_create_msgs/action/Dock {}
```

> 📖 Docs: [Actuators CLI](https://iroboteducation.github.io/create3_docs/examples/actuators-cli/), [Drive Goals](https://iroboteducation.github.io/create3_docs/api/drive-goals/)

### 示例 2: Python ROS 2 节点控制 Create 3

```python
# ============================================================
# create3_controller.py — 用 Python/ROS 2 控制 Create 3
# ============================================================
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from irobot_create_msgs.msg import HazardDetectionVector

class Create3Controller(Node):
    """Create 3 控制器: 前进并在碰到障碍物时转向"""
    def __init__(self):
        super().__init__('create3_controller')
        # 发布速度命令
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # 订阅里程计
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        # 订阅危险检测
        self.hazard_sub = self.create_subscription(
            HazardDetectionVector, '/hazard_detection',
            self.hazard_callback, 10)
        # 控制循环 10Hz
        self.timer = self.create_timer(0.1, self.control_loop)
        self.obstacle_detected = False

    def odom_callback(self, msg):
        """处理里程计数据"""
        pos = msg.pose.pose.position
        self.get_logger().info(f'位置: x={pos.x:.2f}, y={pos.y:.2f}')

    def hazard_callback(self, msg):
        """检测障碍物"""
        self.obstacle_detected = len(msg.detections) > 0
        if self.obstacle_detected:
            self.get_logger().warn('⚠️ 检测到障碍物!')

    def control_loop(self):
        """简单的避障策略"""
        twist = Twist()
        if self.obstacle_detected:
            twist.linear.x = 0.0
            twist.angular.z = 1.0  # 左转避障
        else:
            twist.linear.x = 0.3  # 前进
            twist.angular.z = 0.0
        self.cmd_pub.publish(twist)

def main():
    rclpy.init()
    node = Create3Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

> 💻 Source: [create3_examples](https://github.com/iRobotEducation/create3_examples)

### 示例 3: 添加虚拟摄像头 URDF (camera.urdf.xacro)

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" >

    <!-- 关节: 把摄像头固定到 Create 3 顶部 -->
    <joint name="camera_joint" type="fixed">
        <parent link="base_link"/>
        <child link="camera_link"/>
        <origin xyz="0 0 0.2" rpy="0 0 0"/>
    </joint>

    <!-- 摄像头链接 -->
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

    <!-- 光学坐标系 (z-forward) -->
    <joint name="camera_optical_joint" type="fixed">
        <parent link="camera_link"/>
        <child link="camera_link_optical"/>
        <origin xyz="0 0 0" rpy="${-pi/2} 0 ${-pi/2}"/>
    </joint>
    <link name="camera_link_optical"></link>

    <!-- Gazebo 摄像头插件 -->
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
            </plugin>
        </sensor>
    </gazebo>

</robot>
```

> 📖 Docs: [Gazebo URDF Tutorial](https://classic.gazebosim.org/tutorials?tut=ros_urdf), [Articulated Robotics Camera](https://articulatedrobotics.xyz/mobile-robot-9-camera)

---

## API 速查

### Create 3 ROS 2 Topics

| 话题 | 消息类型 | 方向 | 用途 |
|------|---------|------|------|
| `/cmd_vel` | `geometry_msgs/Twist` | Agent → Robot | 速度控制 |
| `/cmd_lightring` | `irobot_create_msgs/LightringLeds` | Agent → Robot | LED |
| `/cmd_audio` | `irobot_create_msgs/AudioNoteVector` | Agent → Robot | 声音 |
| `/odom` | `nav_msgs/Odometry` | Robot → Agent | 融合里程计 |
| `/imu` | `sensor_msgs/Imu` | Robot → Agent | IMU |
| `/ir_intensity` | `irobot_create_msgs/IrIntensityVector` | Robot → Agent | IR 接近 |
| `/hazard_detection` | `irobot_create_msgs/HazardDetectionVector` | Robot → Agent | 碰撞+悬崖 |
| `/dock_status` | `irobot_create_msgs/DockStatus` | Robot → Agent | 对接状态 |
| `/wheel_ticks` | `irobot_create_msgs/WheelTicks` | Robot → Agent | 编码器 |
| `/tf` | `tf2_msgs/TFMessage` | Robot → Agent | 坐标变换 |

### Create 3 ROS 2 Actions

| 动作 | 消息类型 | 用途 |
|------|---------|------|
| `/dock` | `irobot_create_msgs/Dock` | 自动对接充电站 |
| `/undock` | `irobot_create_msgs/Undock` | 从充电站脱离 |
| `/drive_distance` | `irobot_create_msgs/DriveDistance` | 前进指定距离 |
| `/rotate_angle` | `irobot_create_msgs/RotateAngle` | 旋转指定角度 |
| `/navigate_to_position` | `irobot_create_msgs/NavigateToPosition` | 导航到位置 |
| `/wall_follow` | `irobot_create_msgs/WallFollow` | 沿墙行走 |

### Create 3 关键参数

| 参数 | 节点 | 说明 |
|------|------|------|
| `max_speed` | motion_control | 最大速度限制 |
| `safety_override` | motion_control | 安全模式: none/backup_only/full |
| `wheel_base` | static_transform | 轮距（只读） |
| `wheels_radius` | static_transform | 轮半径（只读） |
| `wheels_encoder_resolution` | static_transform | 编码器分辨率（只读） |
| `publish_odom_tfs` | robot_state | 是否发布 odom→base TF |

> 📖 Docs: [ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/)
