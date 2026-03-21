---
topic: aws_small_house
dimension: pitfalls
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Docs: AWS RoboMaker Small House World — https://github.com/aws-robotics/aws-robomaker-small-house-world"
  - "📖 Docs: CST8509 Lab 3 Gazebo — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/courses/rl/labs/CST8509_Lab3_Gazebo.md"
  - "🧪 经验: CST8509 Lab 3 常见构建问题"
expiry: 6m
status: current
---

# AWS Small House 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: Gazebo 加载后世界一片空白——模型路径没设对

**痛点类别：** 代码类 — 环境配置不知道怎么做

**场景：** 按照 Lab 3 指导执行了 `colcon build`，启动 Gazebo 后只看到灰色地面，没有任何家具和墙壁

**症状：** Gazebo GUI 打开了，但世界是空的。终端可能有 `Unable to find model` 警告

**根因：** `GAZEBO_MODEL_PATH` 环境变量没有包含 AWS Small House 的 `models/` 目录。Gazebo 在 `.world` 文件中看到 `<include><uri>model://aws_robomaker_residential_*</uri></include>`，但找不到对应模型文件

**解法：**

❌ 错误做法 — 直接启动 Gazebo 不设模型路径

```bash
# 没有设置模型路径就启动
gazebo worlds/small_house.world
```

✅ 正确做法 — 先设模型路径再启动

```bash
# 设置模型路径
export GAZEBO_MODEL_PATH=~/create3_ws/src/aws-robomaker-small-house-world/models:$GAZEBO_MODEL_PATH

# 然后启动
gazebo worlds/small_house.world
```

**教训：** Gazebo 不会自动在工作空间里搜索模型，必须手动告诉它去哪找

> 📖 Docs: [AWS Small House README](https://github.com/aws-robotics/aws-robomaker-small-house-world)

---

## 坑 2: 摄像头 Topic 不出现——忘了 source Gazebo setup.sh

**痛点类别：** 代码类 — 有一步遗漏但不知道少了哪步

**场景：** 添加了 `camera.urdf.xacro`，构建成功，启动后 `ros2 topic list` 里没有摄像头相关 Topic

**症状：** `ros2 topic list | grep custom` 无输出，但 Gazebo GUI 中 Create 3 上确实出现了红色方块（摄像头模型可见）

**根因：** `libgazebo_ros_camera.so` 插件需要 Gazebo 11 的环境变量才能正确加载。忘了执行 `source /usr/share/gazebo-11/setup.sh`

**解法：**

❌ 错误做法 — 只 source ROS 2 工作空间

```bash
source ~/create3_ws/install/setup.bash
ros2 launch ...   # 摄像头 Topic 不会出现！
```

✅ 正确做法 — 先 source Gazebo 11 再 source 工作空间

```bash
source /usr/share/gazebo-11/setup.sh    # ← 这一步关键！
source ~/create3_ws/install/setup.bash
ros2 launch ...   # 摄像头 Topic 正常出现
```

✅ 永久解决：加到 .bashrc

```bash
echo "source /usr/share/gazebo-11/setup.sh" >> ~/.bashrc
```

**教训：** Gazebo 插件需要 Gazebo 自己的环境变量，ROS 2 的 setup.bash 不包含这些变量

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 8

---

## 坑 3: RViz 中 Create 3 显示全白——启动太慢超时了

**痛点类别：** 代码类 — 程序行为不符合预期

**场景：** 启动仿真后，Gazebo GUI 正常，但 RViz 中 Create 3 模型全部是白色的，左侧面板有红色错误

**症状：** RViz 显示 Create 3 为白色轮廓，左侧面板显示 TF 或模型加载错误

**根因：** AWS Small House 有大量 3D 模型，首次加载时 Gazebo 需要较长时间下载/解析模型文件。RViz 在等待超时后显示错误

**解法：**

❌ 错误做法 — 看到白色就以为配置错误，开始改文件

✅ 正确做法 — 耐心等待 2-3 分钟，或 `^C` 终止后重新启动

```bash
# 在启动终端中 Ctrl+C 终止
# 然后重新启动
ros2 launch irobot_create_gazebo_bringup create3_gazebo.launch.py \
    world:=~/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world
```

**教训：** AWS Small House 模型数量多，第一次加载慢是正常的。GUI 显示 "Not Responding" 不要慌

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 6

---

## 坑 4: Gazebo 版本混淆——Classic Gazebo 11 vs Ignition Gazebo

**痛点类别：** 概念类 — 名词太多不知道选哪个

**场景：** 在 create3_sim 的 README 中看到两套指令（Classic Gazebo 和 Ignition Gazebo Fortress），不知道用哪个

**症状：** 按 Ignition 指令安装后，AWS Small House 加载失败，因为该世界只兼容 Classic Gazebo 11

**根因：** Classic Gazebo（版本号 11）和 Ignition Gazebo（后来更名为 Gazebo Sim）是**两个完全不同的软件**，共享"Gazebo"名字但架构不同。AWS Small House 只支持 Classic Gazebo 11

**解法：**

❌ 错误做法 — 安装 Ignition Gazebo Fortress

```bash
# 这是 Ignition Gazebo，不是 Classic Gazebo！
sudo apt install ros-humble-ros-gz
```

✅ 正确做法 — 安装 Classic Gazebo 11

```bash
# Classic Gazebo 11
curl -sSL http://get.gazebosim.org | sh
# 或者
sudo apt install gazebo
```

**教训：** Gazebo 生态有两个分叉，文档中看到 "Gazebo" 要先搞清楚是 Classic 还是 Ignition/Sim

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 2

---

## 坑 5: colcon build 报错——忘了 rosdep install

**痛点类别：** 代码类 — 构建失败不知道怎么修

**场景：** 克隆仓库后直接运行 `colcon build`，报了一堆找不到依赖包的错误

**症状：** 大量 `could not find package` 或 `CMake Error` 错误

**根因：** `colcon build` 假设所有 ROS 2 依赖包已安装。必须先用 `rosdep install` 自动安装依赖

**解法：**

❌ 错误做法 — 克隆后直接构建

```bash
cd ~/create3_ws
colcon build    # 报错！依赖没装！
```

✅ 正确做法 — 先安装依赖再构建

```bash
cd ~/create3_ws
rosdep install --from-paths src --ignore-src -r -y   # ← 先安装依赖
colcon build --symlink-install                         # ← 再构建
```

**教训：** ROS 2 项目的构建流程是 `clone → rosdep install → colcon build`，跳过中间步骤一定会报错

> 📖 Docs: [CST8509 Lab 3](../../../courses/rl/labs/CST8509_Lab3_Gazebo.md), Section 5

---

## 坑 6: 非静态家具导致仿真崩溃——改了 static 标记但没设质量

**痛点类别：** 代码类 — 改了配置但出了更大问题

**场景：** 想让机器人推开椅子，把 `<static>true</static>` 改成 `false`

**症状：** 家具飞向天空或穿过地板，仿真变得极不稳定

**根因：** AWS Small House 的家具模型默认质量和惯性值**不准确**（README Disclaimer 明确提到了这一点）。`static=true` 时这不是问题，但一旦改成 `false`，不准确的物理参数会导致物理引擎发散

**解法：**

❌ 错误做法 — 只改 static 状态

```xml
<!-- 只改了 static，没改质量 -->
<static>false</static>
```

✅ 正确做法 — 改 static 的同时校准质量和惯性

```xml
<static>false</static>
<link name="body">
    <inertial>
        <!-- 必须设置合理的质量和惯性矩 -->
        <mass>5.0</mass>
        <inertia>
            <ixx>0.1</ixx><ixy>0</ixy><ixz>0</ixz>
            <iyy>0.1</iyy><iyz>0</iyz>
            <izz>0.1</izz>
        </inertia>
    </inertial>
</link>
```

**教训：** 静态物体不需要准确的物理参数，但动态物体绝对需要。改 static 标记前先想清楚是否真的需要物体移动

> 📖 Docs: [AWS Small House README — Disclaimer](https://github.com/aws-robotics/aws-robomaker-small-house-world), [Gazebo Inertia Tutorial](http://gazebosim.org/tutorials?tut=inertia&cat=build_robot)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别把 Classic Gazebo 和 Ignition Gazebo 搞混** → 课程用 Classic Gazebo 11，不是 Ignition/Sim
2. [ ] **别忽略 README 的 Disclaimer** → 模型的质量/惯性不准确，改 static 之前先看
3. [ ] **别跳过 rosdep install** → 构建失败 90% 是因为少了这一步
4. [ ] **别被 GUI "Not Responding" 吓到** → 首次加载大世界就是慢，等 2-3 分钟

### 作业/项目避坑

1. [ ] **先验证世界加载** → 先不加摄像头，确认 Gazebo + AWS Small House 能正常运行
2. [ ] **再加摄像头** → 分步构建，每次只改一个东西
3. [ ] **camera.urdf.xacro 路径正确** → 必须放在 `urdf/` 目录下并在 `create3.urdf.xacro` 中引用
4. [ ] **提交 camera.urdf.xacro** → Lab 3 的提交物就是这个文件

### 调试清单（技术类）

1. [ ] **世界空白？** → 检查 `GAZEBO_MODEL_PATH` 是否包含 `models/` 目录
2. [ ] **摄像头 Topic 没出现？** → 检查是否执行了 `source /usr/share/gazebo-11/setup.sh`
3. [ ] **RViz 全白？** → `^C` 终止后重新启动，耐心等待
4. [ ] **colcon build 报错？** → 先运行 `rosdep install --from-paths src --ignore-src -r -y`
5. [ ] **Create 3 不动？** → 检查 `ros2 topic list` 确认 Topic 可用
6. [ ] **家具乱飞？** → 确认 `<static>true</static>` 或校准质量/惯性参数
