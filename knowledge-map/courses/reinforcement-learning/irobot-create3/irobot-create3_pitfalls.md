---
topic: irobot-create3
dimension: pitfalls
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: iRobot Create 3 — Network Config — https://iroboteducation.github.io/create3_docs/setup/xml-config/"
  - "📖 Docs: iRobot Create 3 — ROS 2 API — https://iroboteducation.github.io/create3_docs/api/ros2/"
  - "📖 Docs: iRobot Create 3 — Safety — https://iroboteducation.github.io/create3_docs/api/safety/"
  - "💻 Source: create3_sim — https://github.com/iRobotEducation/create3_sim"
  - "🧪 经验: 常见 Create 3 + Gazebo 初学者误区总结"
expiry: 6m
status: current
---

# iRobot Create 3 踩坑记录

> ⚠️ **围绕学习痛点组织**，每次踩坑后请追加条目。

---

## 坑 1: 仿真器话题看不到

**场景：** 启动 Create 3 仿真后，`ros2 topic list` 只显示 `/rosout` 和 `/parameter_events`

**症状：** 看不到 `/cmd_vel`、`/odom` 等 Create 3 话题

**根因：** ROS 2 的 DDS 中间件需要节点在同一个 Domain 中。`RMW_IMPLEMENTATION` 不匹配也会导致不可见。

**解法：**

❌ 错误做法 — 以为直接 `gazebo` 就有 ROS 2

```bash
# ❌ 直接启动 Gazebo，没有 ROS 2 桥接
gazebo
ros2 topic list  # 空的！
```

✅ 正确做法 — 用 ros2 launch 文件启动

```bash
# ✅ 用 launch 文件（包含 ROS 2 插件）
source ~/create3_ws/install/setup.bash
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py

# ✅ 另一个终端也要 source
source ~/create3_ws/install/setup.bash
ros2 topic list  # 应该能看到 /cmd_vel, /odom 等

# ✅ 如果还是看不到，检查 RMW 和 Domain
echo $RMW_IMPLEMENTATION
echo $ROS_DOMAIN_ID
# 两个终端必须一致
```

> 📖 Docs: [Network Configuration](https://iroboteducation.github.io/create3_docs/setup/xml-config/)

---

## 坑 2: 忘记 source install/setup.bash

**场景：** `colcon build` 编译完成后直接 `ros2 launch`

**症状：** `Package 'irobot_create_gazebo_bringup' not found`

**根因：** ROS 2 用环境变量查找包。每次打开新终端或编译后，必须 `source` 工作空间的 `setup.bash`

**解法：**

❌ 错误做法 — 编译后直接 launch

```bash
colcon build --symlink-install
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py
# Package not found!!!
```

✅ 正确做法 — 每次都 source

```bash
colcon build --symlink-install
source install/setup.bash  # ← 关键！

# 或加到 .bashrc 一劳永逸
echo "source ~/create3_ws/install/setup.bash" >> ~/.bashrc
```

> 📖 Docs: [ROS 2 Humble Tutorials](https://docs.ros.org/en/humble/Tutorials.html)

---

## 坑 3: 虚拟摄像头话题不出现

**场景：** 添加了 `camera.urdf.xacro` 并重新编译，但 `ros2 topic list` 看不到摄像头话题

**症状：** 没有 `/custom_ns/camera1/custom_img` 话题

**根因：** Gazebo 摄像头插件需要 Gazebo 的环境变量才能加载 `libgazebo_ros_camera.so`

**解法：**

❌ 错误做法 — 只 source ROS 2 工作空间

```bash
source install/setup.bash
ros2 launch ...  # 摄像头话题不出现
```

✅ 正确做法 — 同时 source Gazebo 环境

```bash
# ✅ 必须先 source Gazebo 11 的 setup
source /usr/share/gazebo-11/setup.sh
source ~/create3_ws/install/setup.bash
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py

# 加到 .bashrc
echo "source /usr/share/gazebo-11/setup.sh" >> ~/.bashrc
```

> 📖 Docs: [Gazebo URDF Tutorial](https://classic.gazebosim.org/tutorials?tut=ros_urdf)

---

## 坑 4: 安全反射干扰 RL 训练

**场景：** RL Agent 想探索"撞墙后怎么办"，但 Create 3 的 `REFLEX_BUMP` 自动让机器人后退了

**症状：** Agent 发送了"前进"动作，但机器人自己后退了——奖励信号不一致

**根因：** Create 3 默认开启所有安全反射，会自动对碰撞/悬崖做出保护性响应

**解法：**

❌ 错误做法 — 不知道反射的存在

```python
# ❌ Agent 以为自己在控制，其实反射在"抢方向盘"
env.step(action=FORWARD)  # 撞到障碍物
# 期望: 机器人继续前进(学习碰撞惩罚)
# 实际: 反射让机器人后退了, Agent 困惑
```

✅ 正确做法 — 仿真中禁用反射（仅仿真！）

```bash
# ✅ 在仿真中设置 safety_override=full
ros2 param set /motion_control safety_override full
# 现在 RL Agent 完全控制，不会被反射干扰

# ⚠️ 真实机器人上不要这样做！保留反射保护
```

> 📖 Docs: [Safety](https://iroboteducation.github.io/create3_docs/api/safety/) — `safety_override` 参数说明

---

## 坑 5: `ros2 topic list` 显示旧的缓存数据

**场景：** 之前启动过仿真，关掉后重新启动，但 `ros2 topic list` 显示的话题可能不准确

**症状：** 话题列表不对——多了旧话题或少了新话题

**根因：** `ros2 topic list` 使用 daemon 缓存的发现信息

**解法：**

✅ 正确做法 — 绕过缓存

```bash
# ✅ 跳过 daemon 缓存，直接扫描
ros2 topic list --no-daemon --spin-time 10
```

> 📖 Docs: [Create 3 ROS 2 API](https://iroboteducation.github.io/create3_docs/api/ros2/) — "the command line ros2 topic utility could use stale cached discovery information"

---

## 超级避坑指南

### 安装避坑

1. [ ] **Gazebo 版本确认** → Classic Gazebo 11，不是 Gazebo Sim
2. [ ] **ROS 2 Desktop 版** → `ros-humble-desktop`，不是 `ros-humble-ros-base`
3. [ ] **create3_sim 分支** → `humble` 分支，不是 main
4. [ ] **rosdep 别忘了** → `rosdep install --from-paths src --ignore-src -r -y`

### 运行避坑

1. [ ] **每个终端都 source** → `source install/setup.bash`
2. [ ] **Gazebo 环境也 source** → `source /usr/share/gazebo-11/setup.sh`（摄像头需要）
3. [ ] **用 `ros2 launch` 不用 `gazebo`** → launch 文件加载 ROS 2 桥接
4. [ ] **`ros2 topic list` 先验证** → 确认话题存在再发命令

### 调试清单

1. [ ] **话题找不到？** → 检查 `ROS_DOMAIN_ID` 和 `RMW_IMPLEMENTATION`
2. [ ] **机器人不动？** → `ros2 topic echo /cmd_vel` 确认命令在发
3. [ ] **摄像头没有？** → `source /usr/share/gazebo-11/setup.sh` 了吗？
4. [ ] **反射抢控制？** → `ros2 param set /motion_control safety_override full`
5. [ ] **缓存不准？** → `ros2 topic list --no-daemon --spin-time 10`
