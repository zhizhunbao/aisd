# Lab 4 操作手册：添加行走红球 Actor + 红球检测

> 前置条件：已按 Lab 3 安装文档完成 Gazebo + Create3 仿真环境搭建

---

## 快速概览

本实验分 3 个任务：
1. 在 `small_house.world` 中添加人类 actor（验证后注释掉）
2. 添加行走红球 actor（修改为红色球体 + 直线来回轨迹）
3. 添加 `redball.py` ROS 2 节点，检测红球并在 RViz 中显示

---

## Step 1: 找到 small_house.world 文件

```bash
# 在 WSL 终端中执行
find /home/peng/create3_ws/src -name "small_house.world"
# 预期路径:
# /home/peng/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world
```

---

## Step 2: 添加人类 Actor（验证用）

在 `small_house.world` 文件的 `</world>` 标签前添加以下 XML：

```xml
<!-- Lab 4 Step 2: Human actor (comment out after verification) -->
<actor name="human_actor">
  <skin>
    <filename>walk.dae</filename>
  </skin>
  <animation name="walking">
    <filename>walk.dae</filename>
    <interpolate_x>true</interpolate_x>
  </animation>
  <script>
    <loop>true</loop>
    <delay_start>0.000000</delay_start>
    <auto_start>true</auto_start>
    <trajectory id="0" type="walking">
      <waypoint>
        <time>0</time>
        <pose>0 2 0 0 0 -1.57</pose>
      </waypoint>
      <waypoint>
        <time>2</time>
        <pose>0 -2 0 0 0 -1.57</pose>
      </waypoint>
      <waypoint>
        <time>2.5</time>
        <pose>0 -2 0 0 0 1.57</pose>
      </waypoint>
      <waypoint>
        <time>7</time>
        <pose>0 2 0 0 0 1.57</pose>
      </waypoint>
      <waypoint>
        <time>7.5</time>
        <pose>0 2 0 0 0 -1.57</pose>
      </waypoint>
    </trajectory>
  </script>
</actor>
```

### 验证

```bash
# 重新构建
cd /home/peng/create3_ws
colcon build --symlink-install --packages-select aws_robomaker_small_house_world

# 启动仿真
bash /home/peng/start_gazebo.sh
```

在 Gazebo 中应看到一个人在房子里走来走去。

### 验证成功后注释掉

```xml
<!-- <actor name="human_actor"> ... </actor> -->
```

---

## Step 3: 添加行走红球 Actor

在 `small_house.world` 中（同样在 `</world>` 前）添加：

```xml
<!-- Lab 4 Step 3: Travelling red ball actor -->
<actor name="red_ball_actor">
  <link name="link">
    <visual name="visual">
      <geometry>
        <sphere>
          <radius>.2</radius>
        </sphere>
      </geometry>
      <material name="red">
        <ambient>1 0 0 1</ambient>
        <diffuse>1 0 0 1</diffuse>
        <specular>0 0 0 0</specular>
        <emissive>0 0 0 1</emissive>
      </material>
    </visual>
  </link>
  <script>
    <loop>true</loop>
    <delay_start>0.000000</delay_start>
    <auto_start>true</auto_start>
    <trajectory id="0" type="line">
      <waypoint>
        <time>0.0</time>
        <pose>-1 0 1 0 0 0</pose>
      </waypoint>
      <waypoint>
        <time>2.0</time>
        <pose>1 0 1 0 0 0</pose>
      </waypoint>
      <waypoint>
        <time>4.0</time>
        <pose>-1 0 1 0 0 0</pose>
      </waypoint>
    </trajectory>
  </script>
</actor>
```

> **说明**: 轨迹是直线来回（x 轴 -1 到 1），高度 z=1，不走正方形。如果红球在房子外面，调整坐标使其出现在机器人可视范围内。

### 重新构建并验证

```bash
cd /home/peng/create3_ws
colcon build --symlink-install --packages-select aws_robomaker_small_house_world
bash /home/peng/start_gazebo.sh
```

应看到红球在房子里直线来回移动。

---

## Step 4: 创建 redball.py 节点

### 4.1 创建文件

将 `redball.py` 文件复制到 `aisd_vision` 包中：

```bash
# 找到 hands.py 所在位置
find /home/peng/create3_ws/src -name "hands.py"
# 假设路径为: /home/peng/create3_ws/src/<your_package>/aisd_vision/hands.py

# 将 redball.py 复制到同一目录
cp /home/peng/lab4_files/redball.py <同一目录>/redball.py
```

或直接创建文件（代码见本目录中的 `redball.py`）。

### 4.2 注册入口点

在 `aisd_vision` 包的 `setup.py` 中，找到 `console_scripts` 部分，添加 `redball`：

```python
entry_points={
    'console_scripts': [
        'hands = aisd_vision.hands:main',
        'redball = aisd_vision.redball:main',   # <-- 添加这行
    ],
},
```

### 4.3 重新构建

```bash
cd /home/peng/create3_ws
colcon build --symlink-install --packages-select <your_aisd_vision_package>
source install/setup.bash
```

---

## Step 5: 运行红球检测

### 启动仿真（终端 1）

```bash
bash /home/peng/start_gazebo.sh
```

### 运行 redball 节点（终端 2）

```bash
source /home/peng/.bashrc
ros2 run <your_package> redball
```

### 在 RViz 中查看检测结果（终端 1 的 RViz）

1. 点击 **Add** 按钮
2. 选择 **By topic** 标签
3. 展开 `target_redball`
4. 选择 **Image**，点击 OK
5. 应看到红球被绿色圆圈标注

> **注意**: `redball.py` 订阅的是 `custom_ns/camera1/image_raw`。如果你的摄像头话题名不同（如 Lab 3 中使用的 `custom_img`），需要修改代码中的话题名。

---

## Step 6: 提交

```bash
# 提交 small_house.world 文件到 Brightspace
# 文件路径:
# ~/create3_ws/src/aws-robomaker-small-house-world/worlds/small_house.world
```

---

## 演示准备

向实验老师展示：
1. ✅ 红球在 Gazebo 中来回移动
2. ✅ RViz 中 `target_redball` 话题显示检测后的图像（红球被绿圈标注）
3. ✅ 准备好回答代码相关问题

---

## 排错

| 问题 | 解决 |
|------|------|
| 红球不出现 | 确认 XML 加在 `</world>` 前且不在其他元素内部 |
| 红球位置不对 | 调整 `<pose>` 中的 x, y 坐标 |
| `redball` 节点找不到 | 确认 `setup.py` 中已注册，重新 `colcon build` |
| 相机话题对不上 | 检查 `ros2 topic list | grep camera` 确认实际话题名 |
| `no ball detected` 持续输出 | 调整机器人位置使摄像头能看到红球 |
| cv_bridge 报错 | `sudo apt install ros-humble-cv-bridge` |
