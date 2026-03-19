---
topic: rviz
dimension: code
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Docs: RViz2 User Guide — https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html"
  - "📖 Docs: ROS 2 Humble — https://docs.ros.org/en/humble/"
expiry: 6m
status: current
---

# RViz 可视化工具 代码参考

> 📖 Docs: [RViz2 User Guide](https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

## 快速开始

### 最简示例 — 启动 RViz2

```bash
# ============================================================
# 1. 启动 RViz2 (ROS 2 Humble 已安装)
# ============================================================
source /opt/ros/humble/setup.bash
rviz2
# 弹出 RViz2 窗口，默认只有 Grid Display

# ============================================================
# 2. 带配置文件启动
# ============================================================
rviz2 -d my_config.rviz
```

---

## 完整实现示例

### 示例 1: 在 launch 文件中集成 RViz

```python
# ============================================================
# rl_rviz.launch.py — 启动 Gazebo + RViz 的 launch 文件
# ============================================================
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Create 3 Gazebo 仿真 / Create 3 Gazebo simulation
    create3_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('irobot_create_gazebo_bringup'),
                'launch',
                'create3_gazebo.launch.py'
            )
        )
    )

    # RViz2 配置文件路径 / RViz2 config file path
    rviz_config = os.path.join(
        get_package_share_directory('create3_rl'),
        'rviz',
        'rl_debug.rviz'
    )

    # RViz2 节点 / RViz2 node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        create3_launch,
        rviz_node,
    ])
```

### 示例 2: 用 Python 发布 Marker 标注 RL 目标点

```python
# ============================================================
# rl_markers.py — 在 RViz 中标注 RL 训练的目标和奖励区域
# ============================================================
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class RLMarkerPublisher(Node):
    """发布 RL 调试用的 Marker / Publish RL debug markers"""
    def __init__(self):
        super().__init__('rl_marker_publisher')
        self.marker_pub = self.create_publisher(Marker, '/rl_markers', 10)
        self.timer = self.create_timer(1.0, self.publish_markers)

    def publish_markers(self):
        # === 目标点标记（绿色球） / Goal marker (green sphere) ===
        goal = Marker()
        goal.header.frame_id = 'map'
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.ns = 'rl_goal'
        goal.id = 0
        goal.type = Marker.SPHERE        # 球形
        goal.action = Marker.ADD
        goal.pose.position.x = 5.0       # 目标位置
        goal.pose.position.y = 3.0
        goal.pose.position.z = 0.2
        goal.pose.orientation.w = 1.0
        goal.scale.x = 0.5               # 直径 0.5m
        goal.scale.y = 0.5
        goal.scale.z = 0.5
        goal.color.g = 1.0               # 绿色
        goal.color.a = 0.8               # 80% 不透明
        self.marker_pub.publish(goal)

        # === 奖励区域标记（蓝色半透明圆柱） / Reward zone ===
        zone = Marker()
        zone.header.frame_id = 'map'
        zone.header.stamp = self.get_clock().now().to_msg()
        zone.ns = 'rl_reward_zone'
        zone.id = 1
        zone.type = Marker.CYLINDER      # 圆柱形
        zone.action = Marker.ADD
        zone.pose.position.x = 5.0
        zone.pose.position.y = 3.0
        zone.pose.position.z = 0.0
        zone.pose.orientation.w = 1.0
        zone.scale.x = 2.0               # 半径 1m
        zone.scale.y = 2.0
        zone.scale.z = 0.01              # 很薄
        zone.color.b = 1.0               # 蓝色
        zone.color.a = 0.3               # 30% 不透明
        self.marker_pub.publish(zone)

        # === Agent 轨迹标记（红色线） / Agent trajectory ===
        traj = Marker()
        traj.header.frame_id = 'map'
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.ns = 'rl_trajectory'
        traj.id = 2
        traj.type = Marker.LINE_STRIP    # 线段
        traj.action = Marker.ADD
        traj.scale.x = 0.05              # 线宽 5cm
        traj.color.r = 1.0               # 红色
        traj.color.a = 1.0
        # 添加轨迹点 / Add trajectory points
        for i in range(20):
            p = Point()
            p.x = float(i) * 0.25
            p.y = float(i) * 0.15
            p.z = 0.05
            traj.points.append(p)
        self.marker_pub.publish(traj)

        self.get_logger().info('Published RL markers')

def main():
    rclpy.init()
    node = RLMarkerPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

在 RViz 中添加 **Marker** Display，Topic 设为 `/rl_markers` 即可看到标注。

---

## API 速查

### RViz2 CLI

| 命令 | 用途 |
|------|------|
| `rviz2` | 启动空配置的 RViz2 |
| `rviz2 -d <file>.rviz` | 加载配置文件启动 |
| `rviz2 --help` | 查看所有选项 |

### RViz2 GUI 操作

| 操作 | 方法 |
|------|------|
| 添加 Display | 左下角 **Add** 按钮 → 选择 Display 类型 |
| 设置 Fixed Frame | 左侧 **Global Options → Fixed Frame** |
| 设置话题 | 展开 Display → **Topic** 下拉选择 |
| 保存配置 | File → Save Config As |
| 加载配置 | File → Open Config |
| 旋转视角 | 鼠标左键拖拽 |
| 平移视角 | 鼠标中键拖拽 |
| 缩放视角 | 鼠标滚轮 |

### Marker 类型速查

| Marker.Type | 常量值 | 形状 | 典型 RL 用途 |
|-------------|--------|------|------------|
| `ARROW` | 0 | 箭头 | 标注动作方向 |
| `CUBE` | 1 | 方块 | 标注障碍物 |
| `SPHERE` | 2 | 球 | 标注目标点 |
| `CYLINDER` | 3 | 圆柱 | 标注奖励区域 |
| `LINE_STRIP` | 4 | 连续线 | 标注轨迹 |
| `LINE_LIST` | 5 | 线段列表 | 标注激光射线 |
| `CUBE_LIST` | 6 | 方块列表 | 标注栅格 |
| `SPHERE_LIST` | 7 | 球列表 | 标注多个点 |
| `TEXT_VIEW_FACING` | 9 | 文字 | 标注数值/标签 |

---

## 目录结构模板

### RViz 配置在项目中的位置

```
create3_rl/
├── launch/
│   └── rl_rviz.launch.py      ← 同时启动 Gazebo + RViz
├── rviz/
│   ├── rl_debug.rviz           ← RL 调试用配置
│   └── sensor_check.rviz       ← 传感器验证用配置
├── src/
│   └── rl_markers.py           ← Marker 发布节点
└── package.xml
```
