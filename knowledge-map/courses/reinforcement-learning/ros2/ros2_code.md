---
topic: ros2
dimension: code
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: ROS 2 Humble Tutorials — https://docs.ros.org/en/humble/Tutorials.html"
  - "📖 Docs: rclpy API — https://docs.ros2.org/latest/api/rclpy/"
  - "📖 Paper: Macenski et al., 'Robot Operating System 2', Science Robotics 2022 — file:///C:/Users/40270/OneDrive/Desktop/workspace/.documents/papers/ros2/macenski_2022_ros2_design.pdf"
expiry: 6m
status: current
---

# ROS 2 代码参考

> 📖 Docs: [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html), [rclpy API](https://docs.ros2.org/latest/api/rclpy/)

## 快速开始

### 最简示例 — 30 秒上手 Publisher

```python
# ============================================================
# ROS 2 最简 Publisher / Minimal ROS 2 Publisher
# ============================================================
import rclpy                           # ROS 2 Python 客户端库 / ROS 2 Python client library
from rclpy.node import Node            # 节点基类 / Node base class
from std_msgs.msg import String        # 标准字符串消息 / Standard string message

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')  # 节点名称 / Node name
        # 创建 Publisher: 话题名, 消息类型, 队列深度
        # Create Publisher: topic name, message type, queue depth
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        # 每 0.5 秒发布一次 / Publish every 0.5 seconds
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)              # 初始化 ROS 2 / Initialize ROS 2
    node = MinimalPublisher()
    rclpy.spin(node)                   # 保持节点运行 / Keep node running
    node.destroy_node()
    rclpy.shutdown()                   # 关闭 ROS 2 / Shutdown ROS 2

if __name__ == '__main__':
    main()
```

**测试方法：**
```bash
# 终端 1: 运行 Publisher / Terminal 1: Run Publisher
ros2 run my_package minimal_publisher

# 终端 2: 查看消息 / Terminal 2: View messages
ros2 topic echo /topic
```

> 📖 Docs: [Writing a Simple Publisher](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

---

## 完整实现示例

### 示例 1: Publisher + Subscriber（发布/订阅）

```python
# ============================================================
# 1. Subscriber 节点 / Subscriber Node
# ============================================================
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        # 创建 Subscriber: 话题名, 消息类型, 回调函数, 队列深度
        # Create Subscriber: topic, msg type, callback, queue depth
        self.subscription = self.create_subscription(
            String,                    # 消息类型 / Message type
            'topic',                   # 话题名 / Topic name
            self.listener_callback,    # 收到消息时调用 / Called on message
            10)                        # 队列深度 / Queue depth

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

> 📖 Docs: [Writing a Simple Subscriber](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

### 示例 2: Twist 消息控制机器人（RL Agent 动作）

```python
# ============================================================
# RL Agent 发送 Twist 动作到机器人 / RL Agent sends Twist action
# ============================================================
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist   # 速度命令消息 / Velocity command message

class RLAgentNode(Node):
    def __init__(self):
        super().__init__('rl_agent')
        # 发布到 /cmd_vel 话题控制机器人 / Publish to /cmd_vel to control robot
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.step)  # 10 Hz 控制频率 / 10 Hz control rate

    def step(self):
        # ============================================================
        # 2. 构建动作 / Build action
        # ============================================================
        cmd = Twist()
        cmd.linear.x = 0.2             # 前进 0.2 m/s / Move forward 0.2 m/s
        cmd.angular.z = 0.0             # 不旋转 / No rotation
        self.cmd_pub.publish(cmd)
        self.get_logger().info(f'Sent: linear={cmd.linear.x}, angular={cmd.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = RLAgentNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

> 📖 Docs: [geometry_msgs/Twist](https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html)

### 示例 3: Service 客户端（查询状态）

```python
# ============================================================
# Service 客户端示例 / Service Client Example
# ============================================================
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts  # 示例服务 / Example service

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        # 创建 Service 客户端 / Create Service client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        # 等待服务可用 / Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        # 异步调用 / Async call
        self.future = self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    client = AddTwoIntsClient()
    client.send_request(2, 3)
    # 等待结果 / Wait for result
    rclpy.spin_until_future_complete(client, client.future)
    result = client.future.result()
    client.get_logger().info(f'Result: {result.sum}')
    client.destroy_node()
    rclpy.shutdown()
```

> 📖 Docs: [Writing a Simple Service](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)

---

## API 速查

### CLI 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `ros2 node list` | 列出所有活跃节点 | |
| `ros2 node info <node>` | 查看节点详情 | `ros2 node info /minimal_publisher` |
| `ros2 topic list` | 列出所有活跃话题 | |
| `ros2 topic echo <topic>` | 实时查看话题消息 | `ros2 topic echo /cmd_vel` |
| `ros2 topic info <topic>` | 查看话题类型和连接数 | `ros2 topic info /scan` |
| `ros2 topic pub <topic> <type> <data>` | 手动发布消息 | `ros2 topic pub /cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}}"` |
| `ros2 topic hz <topic>` | 查看话题发布频率 | `ros2 topic hz /camera/image` |
| `ros2 service list` | 列出所有服务 | |
| `ros2 service call <srv> <type> <data>` | 调用服务 | |
| `ros2 param list` | 列出节点参数 | |
| `ros2 param get <node> <param>` | 获取参数值 | |
| `ros2 launch <pkg> <launch>` | 启动 Launch 文件 | `ros2 launch my_pkg robot.launch.py` |
| `ros2 bag record <topics>` | 录制话题数据 | `ros2 bag record /scan /cmd_vel` |
| `ros2 bag play <bag>` | 回放录制数据 | `ros2 bag play rosbag2_*/` |

### rclpy 核心 API

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `rclpy.init()` | `args=None` | 初始化 ROS 2 / Initialize |
| `rclpy.spin(node)` | `node` | 阻塞运行节点 / Block & run node |
| `rclpy.shutdown()` | | 关闭 ROS 2 / Shutdown |
| `Node(name)` | `name: str` | 创建节点 / Create node |
| ↳ `.create_publisher(type, topic, qos)` | `type, topic, qos` | 创建 Publisher |
| ↳ `.create_subscription(type, topic, cb, qos)` | `type, topic, callback, qos` | 创建 Subscriber |
| ↳ `.create_timer(period, cb)` | `period_sec, callback` | 创建定时器 |
| ↳ `.create_client(type, name)` | `srv_type, srv_name` | 创建 Service 客户端 |
| ↳ `.create_service(type, name, cb)` | `srv_type, srv_name, callback` | 创建 Service 服务端 |
| ↳ `.get_logger()` | | 获取日志器 / Get logger |

> 📖 Docs: [rclpy API](https://docs.ros2.org/latest/api/rclpy/)

---

## 目录结构模板

### 简单结构（单节点）

```
my_ros2_ws/
├── src/
│   └── my_package/
│       ├── my_package/
│       │   ├── __init__.py
│       │   └── my_node.py        ← 节点代码
│       ├── package.xml           ← 包依赖声明
│       ├── setup.py              ← Python 包安装
│       └── setup.cfg
├── build/                        ← colcon 构建产物（自动生成）
├── install/                      ← 安装产物（自动生成）
└── log/                          ← 构建日志（自动生成）
```

### 标准结构（RL + Gazebo）

```
ros2_rl_ws/
├── src/
│   ├── rl_agent_pkg/             ← RL Agent 节点
│   │   ├── rl_agent_pkg/
│   │   │   ├── __init__.py
│   │   │   ├── agent_node.py     ← Agent 主节点
│   │   │   └── gym_wrapper.py    ← Gymnasium 桥接
│   │   ├── package.xml
│   │   └── setup.py
│   ├── robot_description/        ← 机器人模型
│   │   ├── urdf/
│   │   ├── launch/
│   │   └── config/
│   └── simulation_bringup/       ← 仿真启动
│       ├── launch/
│       │   └── sim.launch.py     ← 一键启动 Gazebo + Robot + Agent
│       └── worlds/
│           └── training.world
├── build/
├── install/
└── log/
```
