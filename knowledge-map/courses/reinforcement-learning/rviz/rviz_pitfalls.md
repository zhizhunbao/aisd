---
topic: rviz
dimension: pitfalls
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Docs: RViz2 User Guide — https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html"
  - "🧪 经验: 常见 RViz + ROS 2 初学者误区总结"
expiry: 6m
status: current
---

# RViz 可视化工具 踩坑记录

> ⚠️ **围绕学习痛点组织**，每次踩坑后请追加条目。

---

## 坑 1: Fixed Frame 设错导致什么都看不到

**痛点类别：** #1 只甩任务不教思路

**场景：** 启动 RViz，添加了 LaserScan Display，但 3D 视图中什么都没有

**症状：** Display 状态栏显示 `Status: Error` 或 `Transform [sender=...] For frame [...]: Fixed Frame [map] does not exist`

**根因：** RViz 需要知道"以哪个坐标系为参考画东西"。如果 Fixed Frame 设成了不存在的 frame，或者 TF 树中没有从 Fixed Frame 到数据 frame 的变换链，RViz 就不知道数据该画在哪

**解法：**

❌ 错误做法 — 不管 Fixed Frame 直接添加 Display

```
# ❌ Fixed Frame 保持默认 "map"，但机器人没有发布 map→odom 变换
# 所有 Display 都是红色错误状态
Global Options → Fixed Frame: map   ← 如果没有 SLAM，map frame 不存在！
```

✅ 正确做法 — 先检查有哪些 frame

```bash
# ✅ 先看 TF 树中有哪些 frame
ros2 run tf2_tools view_frames
# 会生成 frames.pdf，打开看 TF 树结构

# 或者命令行查看
ros2 topic echo /tf --once

# 然后在 RViz 中设置 Fixed Frame 为存在的 frame
# 常见选择：
#   odom        — 如果有里程计
#   base_link   — 以机器人为中心
#   map         — 如果有 SLAM/定位
```

**教训：** **RViz 打开后第一件事：设置 Fixed Frame**。不确定用什么？先 `ros2 run tf2_tools view_frames` 看一下有什么 frame。

---

## 坑 2: Display 的 Topic 没有设对

**痛点类别：** #2 上课念PPT

**场景：** 添加了 LaserScan Display，但没有数据出现

**症状：** Display 状态是 OK（绿色），但是 3D 视图中没有激光扫描点——因为默认 Topic 可能不对

**根因：** RViz 添加 Display 后，Topic 字段可能是空的或默认值。你需要手动选择正确的话题

**解法：**

❌ 错误做法 — 添加 Display 后不管 Topic

```
# ❌ 添加 LaserScan Display，Topic 为空
# 状态可能显示 OK（因为没有报错，只是没数据）
```

✅ 正确做法 — 先确认话题存在，再设置

```bash
# ✅ 先列出所有话题
ros2 topic list
# 找到激光话题，比如 /scan 或 /create3/scan

# 在 RViz 中：
# 1. 展开 LaserScan Display
# 2. 找到 Topic 字段
# 3. 从下拉菜单选择正确的话题（如 /scan）
# 4. 确认有数据：ros2 topic hz /scan  ← 检查频率
```

**教训：** 添加 Display 后一定要**手动选择 Topic**，并用 `ros2 topic hz` 确认数据在发。

---

## 坑 3: TF 变换链断裂

**痛点类别：** #1 只甩任务不教思路

**场景：** RobotModel 显示正常，但 LaserScan 或 Image 显示报错

**症状：** `Could not find a connection between 'odom' and 'lidar_link'` 或类似的 TF 错误

**根因：** RViz 需要一条完整的 TF 变换链从 Fixed Frame 到每个 Display 的数据 frame。如果某个环节的变换没被发布，链就断了

**解法：**

```bash
# ✅ 检查 TF 树完整性
ros2 run tf2_tools view_frames
# 打开生成的 PDF，看树有没有断开的地方

# 查看特定变换
ros2 run tf2_ros tf2_echo odom base_link
# 应该输出平移和旋转数据。如果报错 → 这段变换不存在

# 常见修复：确保 robot_state_publisher 在运行
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(xacro model.urdf.xacro)"
```

**教训：** TF 报错 → `view_frames` 看树，找到断裂的那段变换，确保对应的 publisher 在运行。

---

## 坑 4: RViz 性能很差 / 卡顿

**痛点类别：** #1 只甩任务不教思路

**场景：** 同时开 Gazebo + RViz，笔记本风扇狂转，RViz 帧率很低

**症状：** RViz 3D 视图卡顿、鼠标旋转不流畅、整个系统变慢

**根因：** Gazebo 已经很吃资源了，RViz 的 3D 渲染 + 订阅多个话题再加一层。特别是 PointCloud2 和 Image 是大数据量话题

**解法：**

```
# ✅ 性能优化列表：

# 1. 减少 Display 数量
#    - 只打开正在调试的 Display
#    - 不用时关闭 PointCloud2 和 Image

# 2. 降低 LaserScan 渲染量
#    - LaserScan Display → Decay Time 设为 0（不保留历史）
#    - Queue Size 设为 1

# 3. Image Display 降低分辨率
#    - 或改用 rqt_image_view（更轻量）

# 4. 在单独的机器上运行 RViz
#    - Gazebo 在一台电脑，RViz 在另一台
#    - 通过网络 ROS 2 DDS 自动发现

# 5. 降低 TF Display 复杂度
#    - 不用时关闭 TF Display
#    - 或只显示几个关键 frame
```

**教训：** RViz 不是免费的——它吃性能。**只打开你需要的 Display**。PointCloud2 和 Image 是大户。

---

## 坑 5: 配置每次都丢失

**痛点类别：** #2 上课念PPT

**场景：** 每次启动 RViz 都要重新添加 Display、设置 Fixed Frame、选话题

**症状：** 浪费大量时间反复配置

**根因：** RViz 默认不保存配置。关闭后所有设置丢失

**解法：**

```bash
# ✅ 保存配置
# RViz 中: File → Save Config As → 保存为 my_config.rviz

# ✅ 加载配置
rviz2 -d my_config.rviz

# ✅ 最佳做法：在 launch 文件中指定配置（见 code.md 示例）
# 这样每次 ros2 launch 自动加载正确配置
```

**教训：** **配置好 RViz 后立即 Save Config**。最好放到项目的 `rviz/` 目录下并通过 launch 文件加载。

---

## 超级避坑指南

### 启动避坑

1. [ ] **先设 Fixed Frame** → 这是第一步，不是最后一步
2. [ ] **检查 `ros2 topic list`** → 确认数据源在发布
3. [ ] **检查 `ros2 topic hz`** → 确认数据在持续更新
4. [ ] **加载保存的配置** → `rviz2 -d config.rviz`

### 使用避坑

1. [ ] **Display 没数据？** → 检查 Topic 字段是否正确
2. [ ] **TF 报错？** → `ros2 run tf2_tools view_frames` 看树
3. [ ] **性能差？** → 关掉不用的 Display，特别是 PointCloud2
4. [ ] **配置丢了？** → 记得 Save Config

### 考试/答辩避坑

1. [ ] **能解释 RViz vs Gazebo 区别** → RViz=看，Gazebo=仿真
2. [ ] **能解释 Fixed Frame 的作用** → 所有数据的参考坐标系
3. [ ] **能画出 RViz 数据流** → Gazebo → ROS 2 Topic → RViz Display
