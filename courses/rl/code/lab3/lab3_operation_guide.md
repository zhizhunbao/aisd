# Lab 3 操作手册：Gazebo Create3 仿真日常使用

> 前置条件：已按安装文档完成所有安装和配置

---

## 快速启动

```bash
# 在 WSL 终端中执行
bash ~/start_gazebo.sh
```

等待 Gazebo 和 RViz 窗口出现（首次约 1-3 分钟）。

---

## RViz 添加摄像头视图

1. 点击左下角 **Add** 按钮
2. 选择 **By topic** 标签
3. 展开 `/custom_ns` → `camera1` → `custom_img`
4. 选择 **Image**，点击 OK
5. 左下角出现 Image 面板，显示摄像头实时画面

---

## 机器人操控命令

> [!IMPORTANT]
> 所有操控命令需在**另一个终端**中执行，启动仿真的终端不要关。

```bash
# 先加载环境（每个新终端都要执行一次）
source ~/.bashrc
```

### 停靠 / 解除停靠

```bash
# 解除停靠（离开充电座）
ros2 action send_goal /undock irobot_create_msgs/action/Undock {}

# 重新停靠（回到充电座）
ros2 action send_goal /dock irobot_create_msgs/action/DockServo {}
```

### 移动控制

```bash
# 前进 (linear.x > 0)
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.2}, angular: {z: 0.0}}'

# 后退 (linear.x < 0)
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: -0.2}, angular: {z: 0.0}}'

# 左转 (angular.z > 0)
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0}, angular: {z: 0.5}}'

# 右转 (angular.z < 0)
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0}, angular: {z: -0.5}}'

# 边走边转
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.15}, angular: {z: 0.3}}'

# 停止
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.0}, angular: {z: 0.0}}'
```

### 持续移动（不加 --once）

```bash
# 持续前进，按 Ctrl+C 停止发送
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
    '{linear: {x: 0.2}, angular: {z: 0.0}}'
```

> [!TIP]
> `--once` 只发一次消息，机器人会因摩擦逐渐减速停下。不加 `--once` 会持续发送，机器人保持运动。

---

## ROS 2 话题监控

```bash
# 列出所有话题
ros2 topic list

# 查看摄像头话题是否存在
ros2 topic list | grep custom
# 期望输出:
#   /custom_ns/camera1/custom_img
#   /custom_ns/camera1/custom_info

# 查看话题发布频率
ros2 topic hz /custom_ns/camera1/custom_img

# 查看机器人里程计
ros2 topic echo /odom --once

# 查看所有可用 action
ros2 action list

# 查看所有 TF 坐标系
ros2 run tf2_tools view_frames
```

---

## Gazebo 界面操作

| 操作 | 方法 |
|------|------|
| 旋转视角 | 鼠标左键拖动 |
| 平移视角 | 鼠标中键拖动 |
| 缩放 | 鼠标滚轮 |
| 重置视角 | 菜单 Camera → Reset |
| 暂停/继续仿真 | 底部工具栏暂停按钮 |

---

## 关闭仿真

在启动仿真的终端按 **Ctrl+C**，等待所有节点关闭。

```bash
# 如果有残留进程
pkill -f gazebo
pkill -f ros2
pkill -f rviz
```

---

## 速查表

| 功能 | 命令 |
|------|------|
| 启动仿真 | `bash ~/start_gazebo.sh` |
| 解除停靠 | `ros2 action send_goal /undock irobot_create_msgs/action/Undock {}` |
| 停靠 | `ros2 action send_goal /dock irobot_create_msgs/action/DockServo {}` |
| 前进 | `ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'` |
| 停止 | `ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}'` |
| 查看话题 | `ros2 topic list` |
| 摄像头频率 | `ros2 topic hz /custom_ns/camera1/custom_img` |
| 关闭仿真 | 启动终端中按 `Ctrl+C` |

---

## 排错

| 问题 | 解决 |
|------|------|
| `bash: ros2: command not found` | 执行 `source ~/.bashrc` |
| 摄像头 topic 不存在 | 确认 `source /usr/share/gazebo-11/setup.sh` 已执行 |
| Gazebo 黑屏 | `export LIBGL_ALWAYS_SOFTWARE=1` 后重启 |
| undock 无响应 | 等 30 秒让控制器完全加载后再试 |
| RViz 模型全白 | `Ctrl+C` 后重新启动 launch |
| 端口冲突 | `pkill -f gazebo && pkill -f gzserver` 后重启 |
