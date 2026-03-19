---
topic: gazebo
dimension: pitfalls
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Slides: CST8509 Week 7 — file:///C:/Users/40270/Desktop/workspace/aisd/courses/rl/slides/CST8509_07_Gazebo_DynamicP_MC.pdf"
  - "📖 Docs: Gazebo Simulator — https://gazebosim.org/home"
  - "📖 Docs: iRobot Create 3 Simulator — https://iroboteducation.github.io/create3_docs/sim/setup/"
  - "🧪 经验: 常见 Gazebo + ROS 2 初学者误区总结"
expiry: 6m
status: current
---

# Gazebo 仿真器 踩坑记录

> ⚠️ **围绕学习痛点组织**，每次踩坑后请追加条目。

---

## 坑 1: Classic Gazebo 和 Ignition Gazebo 搞混

**痛点类别：** #5 名词多黑话多

**场景：** 安装 Gazebo 时搜到的教程既有 Classic 又有 Ignition，装错了版本

**症状：** `ros2 launch` Create 3 时报错找不到 Gazebo 插件，或者 `gazebo` 命令启动了错的版本

**根因：** Gazebo 有两个完全不同的代码库但用了同样的名字。Ignition Gazebo 后来更名为"Gazebo"让情况更混乱。课程要的是 Classic Gazebo 11，但如果你搜"install gazebo"很可能装上了新版

**解法：**

❌ 错误做法 — 直接搜"install gazebo"

```bash
# ❌ 这可能安装了新版 Gazebo Sim 而不是 Classic
sudo apt install gazebo       # 不明确是哪个版本！
# 或者按新版教程安装了 Ignition
sudo apt install ignition-fortress
```

✅ 正确做法 — 明确安装 Classic Gazebo 11

```bash
# ✅ 使用官方一键安装脚本，它会安装 Classic Gazebo 11
curl -sSL http://get.gazebosim.org | sh

# ✅ 或者明确指定包名
sudo apt install gazebo11 libgazebo11-dev

# 验证版本
gazebo --version
# 期望输出: Gazebo multi-robot simulator, version 11.x.x
```

**教训：** 安装任何 Gazebo 前，先确认你需要的是**哪个 Gazebo**。课程 = Classic Gazebo 11。

> 📖 Slides: CST8509 Week 7 Slide 5

---

## 坑 2: ROS 2 环境没有 source

**痛点类别：** #2 上课念PPT（老师不讲的重要细节）

**场景：** 编译完 Create 3 包后直接 `ros2 launch`

**症状：** `Package 'irobot_create_gazebo_bringup' not found`——明明刚编译完，但 ROS 2 找不到包

**根因：** ROS 2 用环境变量找包。每次打开新终端或编译后，必须 `source` 工作空间的 `setup.bash`

**解法：**

❌ 错误做法 — 忘记 source

```bash
# ❌ 编译后直接 launch
colcon build
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py
# 报错: Package not found!!!
```

✅ 正确做法 — 每次都 source

```bash
# ✅ 编译后必须 source
colcon build --symlink-install
source install/setup.bash   # ← 关键步骤！

# 或者加到 .bashrc 一劳永逸
echo "source ~/create3_ws/install/setup.bash" >> ~/.bashrc

# 验证
ros2 pkg list | grep create3
# 应该能看到 irobot_create_* 包
```

**教训：** **每开一个新终端、每编译一次，都要 `source install/setup.bash`**。没有例外。

---

## 坑 3: Gazebo 启动后黑屏或崩溃

**痛点类别：** #1 只甩任务不教思路

**场景：** 运行 `gazebo` 命令后窗口闪一下就关了，或者显示黑屏

**症状：** GUI 窗口不显示、启动时看到 `[Err] [RenderEngine.cc]` 错误、或者整个进程 segfault

**根因：** GPU 驱动问题、虚拟机中没有 GPU 加速、或者环境变量冲突

**解法：**

❌ 错误做法 — 不看日志直接重试

```bash
# ❌ 反复运行 gazebo 但不看错误信息
gazebo  # 崩了
gazebo  # 又崩了
```

✅ 正确做法 — 用 verbose 模式诊断

```bash
# ✅ 带日志启动
gazebo --verbose 2>&1 | tee gazebo_log.txt
# 检查日志中的 [Err] 和 [Wrn]

# 如果是 GPU 问题，尝试软件渲染
export LIBGL_ALWAYS_SOFTWARE=1
gazebo

# 如果在 VirtualBox/VMware 中
# → 方案 1: 启用 3D 加速
# → 方案 2: 用无头模式
gzserver  # 只运行物理引擎，不渲染

# 如果是多个 Gazebo 进程冲突
killall -9 gazebo gzserver gzclient
gazebo
```

**教训：** Gazebo 启动问题 90% 是 GPU 驱动相关。**先用 `--verbose` 看日志**。虚拟机里用 `gzserver` 无头模式最稳。

---

## 坑 4: ROS 2 话题找不到 / 消息收不到

**痛点类别：** #1 只甩任务不教思路

**场景：** Gazebo 仿真已启动，但 `ros2 topic list` 看不到 `/cmd_vel` 等话题

**症状：** `ros2 topic list` 显示为空或只有 `/rosout`、`/parameter_events`

**根因：** ROS 2 的 DDS 中间件需要节点在同一个 Domain 中。或者 Gazebo 的 ROS 2 插件没有正确加载

**解法：**

❌ 错误做法 — 以为 Gazebo 自动就有 ROS 2

```bash
# ❌ 只启动 gazebo 但没有 ROS 2 桥接插件
gazebo  # 这是纯 Gazebo，没有 ROS 2 话题！
```

✅ 正确做法 — 通过 ROS 2 launch 文件启动

```bash
# ✅ 用 launch 文件启动（包含 ROS 2 插件）
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py

# 在另一个终端验证
ros2 topic list
# 应该能看到 /cmd_vel, /odom, /scan 等

# 如果还是看不到，检查 ROS_DOMAIN_ID
echo $ROS_DOMAIN_ID
# 两个终端的 DOMAIN_ID 必须一样（默认是 0）
```

**教训：** Gazebo 本身不说"ROS 2 语"——需要通过 `gazebo_ros_pkgs` 插件桥接。用 `ros2 launch` 而不是直接 `gazebo`。

---

## 坑 5: URDF 修改后没有重新编译

**痛点类别：** #2 上课念PPT

**场景：** 修改了 Create 3 的 URDF（比如添加摄像头），但启动后看不到变化

**症状：** Gazebo 中的机器人模型和修改前一样，新加的传感器不存在

**根因：** Xacro 文件需要重新编译（`colcon build`），而且需要重新 source

**解法：**

❌ 错误做法 — 改完 URDF 直接 launch

```bash
# ❌ 修改了 camera.urdf.xacro 但没重新编译
vim src/create3_rl/urdf/camera.urdf.xacro
ros2 launch ...  # 还是旧的模型！
```

✅ 正确做法 — 改 → 编译 → source → 启动

```bash
# ✅ 完整流程
vim src/create3_rl/urdf/camera.urdf.xacro  # 修改
colcon build --packages-select create3_rl   # 重新编译
source install/setup.bash                    # 重新 source
ros2 launch ...                              # 启动
```

**教训：** URDF/Xacro 改了 → **必须重新 `colcon build` + `source`**。没有快捷方式。

> 📖 Slides: CST8509 Week 7 Slides 14-15

---

## 超级避坑指南

### 安装避坑

1. [ ] **确认 Gazebo 版本** → 课程用 Classic Gazebo 11，不是 Gazebo Sim
2. [ ] **确认 ROS 2 版本** → Ubuntu 22.04 + ROS 2 Humble
3. [ ] **先跑空世界** → `gazebo --verbose` 确认基础安装没问题
4. [ ] **再装 Create 3 仿真包** → 按官方文档一步步来

### 运行避坑

1. [ ] **每个终端都 source** → `source install/setup.bash`
2. [ ] **用 `ros2 launch` 不用 `gazebo`** → launch 文件会加载 ROS 2 桥接
3. [ ] **检查 `ros2 topic list`** → 确认话题存在后再发命令
4. [ ] **虚拟机用无头模式** → `gzserver` 代替 `gazebo`

### 调试清单

1. [ ] **Gazebo 崩溃？** → `gazebo --verbose` 看日志
2. [ ] **话题找不到？** → 检查 ROS_DOMAIN_ID 是否一致
3. [ ] **机器人不动？** → `ros2 topic echo /cmd_vel` 确认命令在发
4. [ ] **模型没更新？** → `colcon build` + `source` 了吗？
5. [ ] **仿真太慢？** → 用 `gzserver`（无头模式）关掉渲染

### 考试/答辩避坑

1. [ ] **能解释为什么 RL 需要仿真** → 安全+速度+成本+可重复性
2. [ ] **能区分 Gazebo vs Gymnasium** → Gazebo=物理仿真，Gymnasium=RL API
3. [ ] **能画出 Agent-Gymnasium-ROS2-Gazebo 架构图** → 见 Tutorial 中的架构图
