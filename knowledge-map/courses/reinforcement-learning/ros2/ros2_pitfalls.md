---
topic: ros2
dimension: pitfalls
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: ROS 2 Humble Troubleshooting — https://docs.ros.org/en/humble/How-To-Guides/Installation-Troubleshooting.html"
  - "📖 Paper: Macenski et al., 'Robot Operating System 2', Science Robotics 2022 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf"
  - "🧪 经验: CST8509 Lab 3 Gazebo + ROS 2 实践"
expiry: 6m
status: current
---

# ROS 2 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: source 了环境但命令还是找不到

**痛点类别：** 环境配置类 — "明明装了但用不了"

**场景：** 安装了 ROS 2 Humble，打开新终端执行 `ros2 topic list` 报 `command not found`

**症状：** `ros2: command not found` 或 `No module named 'rclpy'`

**根因：** ROS 2 的环境变量需要在**每个**新终端里 source 一次。安装不会自动修改 PATH。

**解法：**

❌ 错误做法 — 只在当前终端 source 了一次

```bash
source /opt/ros/humble/setup.bash
# 关掉终端，开新终端，又找不到了
```

✅ 正确做法 — 加到 .bashrc 自动加载

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
# 同时 source 工作空间（如果有）
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**教训：** ROS 2 的 setup.bash 必须在每个终端 session 加载，最好写进 .bashrc。

> 📖 Docs: [Configuring Environment](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)

---

## 坑 2: Topic 发了但 Subscriber 收不到

**痛点类别：** 通信调试类 — "发了但对面没反应"

**场景：** Publisher 正常发布消息，Subscriber 已启动，但回调从不触发

**症状：** `ros2 topic echo` 能看到消息，但自己的 Subscriber 节点无输出

**根因：** **QoS 不匹配**。Publisher 和 Subscriber 的 QoS 策略不兼容时，DDS 层会静默拒绝连接。最常见的是 Reliability 不匹配（一个 Reliable，一个 Best Effort）。

**解法：**

❌ 错误做法 — 不指定 QoS，默认不一定兼容

```python
# Publisher 用了 sensor_data profile (Best Effort)
from rclpy.qos import qos_profile_sensor_data
self.pub = self.create_publisher(Image, '/camera', qos_profile_sensor_data)

# Subscriber 用默认 (Reliable) — QoS 不匹配！
self.sub = self.create_subscription(Image, '/camera', self.callback, 10)
```

✅ 正确做法 — 显式匹配 QoS

```python
from rclpy.qos import qos_profile_sensor_data

# Publisher 和 Subscriber 用同一个 QoS profile
self.pub = self.create_publisher(Image, '/camera', qos_profile_sensor_data)
self.sub = self.create_subscription(Image, '/camera', self.callback, qos_profile_sensor_data)
```

**教训：** Topic 通不了先查 QoS。用 `ros2 topic info -v /topic_name` 查看双方 QoS 设置。

> 📖 Paper: Macenski et al. 2022, Section II-B "Quality of Service"

---

## 坑 3: colcon build 成功但 ros2 run 找不到节点

**痛点类别：** 构建部署类 — "编译过了但跑不了"

**场景：** `colcon build` 成功无报错，但 `ros2 run my_package my_node` 报 `Package 'my_package' not found`

**症状：** `ros2 pkg list` 里看不到自己的包

**根因：** 忘了 source 工作空间的 install/setup.bash。`colcon build` 生成的可执行文件在 `install/` 目录下，需要 source 才能让 ROS 2 找到。

**解法：**

❌ 错误做法 — build 完直接 run

```bash
cd ~/ros2_ws
colcon build
ros2 run my_package my_node  # ❌ Package not found
```

✅ 正确做法 — build 后 source install

```bash
cd ~/ros2_ws
colcon build --symlink-install  # --symlink-install 避免每次 rebuild
source install/setup.bash       # 关键步骤！
ros2 run my_package my_node     # ✅ 找到了
```

**教训：** `colcon build` 之后**永远**要 `source install/setup.bash`。

> 📖 Docs: [Building Packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)

---

## 坑 4: 多台机器看不到对方的 Topic

**痛点类别：** 网络通信类 — "两台机器连不上"

**场景：** 两台 Ubuntu 机器在同一网络，各自的节点能跑，但互相看不到对方的 Topic

**症状：** 本机 `ros2 topic list` 看不到对方发布的话题

**根因：** **ROS_DOMAIN_ID 不一致**或**网络多播被阻断**。ROS 2 通过 DDS 多播发现节点，需要相同 Domain ID 且网络允许多播。

**解法：**

❌ 错误做法 — 不设 DOMAIN_ID，两台机器默认值可能不同

```bash
# 机器 A: ROS_DOMAIN_ID 没设，默认 0
# 机器 B: 之前设成了 42
export ROS_DOMAIN_ID=42  # 只有 B 设了！
```

✅ 正确做法 — 两台机器设成一样

```bash
# 机器 A 和 B 都执行:
export ROS_DOMAIN_ID=0

# 验证:
ros2 topic list  # 应该能看到对方的 topic
```

**教训：** 多机通信先确认 (1) DOMAIN_ID 一致 (2) 网络允许 UDP 多播 (3) 防火墙放行。

> 📖 Docs: [ROS 2 Domain ID](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Domain-ID.html)

---

## 坑 5: 混淆了 ROS 1 和 ROS 2 的教程

**痛点类别：** 概念混淆类 — "照着教程做但命令不对"

**场景：** Google 搜到的教程是 ROS 1 的，照着做各种报错

**症状：** `roscore` 找不到、`catkin_make` 找不到、`import rospy` 报错

**根因：** ROS 1 和 ROS 2 的命令、包名、API 完全不同，但搜索引擎经常排 ROS 1 教程在前面

**解法：**

❌ ROS 1 写法（常见于老教程）

```python
import rospy                          # ROS 1
rospy.init_node('my_node')            # ROS 1 初始化
pub = rospy.Publisher('/topic', String, queue_size=10)  # ROS 1
```

✅ ROS 2 写法

```python
import rclpy                          # ROS 2
from rclpy.node import Node           # ROS 2
rclpy.init()                          # ROS 2 初始化

class MyNode(Node):                   # ROS 2: 必须继承 Node
    def __init__(self):
        super().__init__('my_node')
        self.pub = self.create_publisher(String, '/topic', 10)
```

**教训：** 搜教程时加"ROS 2 Humble"关键词。看到 `rospy`/`roscore`/`catkin` 就是 ROS 1，立即换教程。

> 📖 Docs: [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

---

## 超级避坑指南

### 学习避坑

1. [ ] **先跑 `ros2 topic list` 再写代码** → 确认环境正常
2. [ ] **搜教程加 "ROS 2 Humble"** → 避免误入 ROS 1 教程
3. [ ] **先 Topic 后 Service 最后 Action** → 不要一上来就学 Action
4. [ ] **用 `rqt_graph` 看连接** → 比脑补强 100 倍

### 作业/项目避坑

1. [ ] **每次 build 后 source** → `source install/setup.bash`
2. [ ] **用 `--symlink-install`** → 避免每次改代码都 rebuild
3. [ ] **先用 CLI 验证** → `ros2 topic pub` 手动发消息测试
4. [ ] **Topic 名别打错** → 大小写敏感，`/cmd_vel` ≠ `/Cmd_Vel`

### 调试清单（技术类）

1. [ ] **`ros2` 命令找不到？** → `source /opt/ros/humble/setup.bash`
2. [ ] **Package 找不到？** → `source install/setup.bash`
3. [ ] **Topic 收不到？** → `ros2 topic info -v` 查 QoS 匹配
4. [ ] **多机看不到？** → 检查 `ROS_DOMAIN_ID` 和网络多播
5. [ ] **消息类型错误？** → `ros2 interface show <type>` 查看定义
6. [ ] **Launch 启动失败？** → 检查 `package.xml` 的 `<exec_depend>`
