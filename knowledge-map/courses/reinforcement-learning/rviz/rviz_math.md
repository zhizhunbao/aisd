---
topic: rviz
dimension: math
created: 2026-03-19
last_verified: 2026-03-19
source_versions:
  - "📖 Docs: ROS 2 TF2 — https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html"
expiry: 12m
status: current
---

# RViz 可视化工具 数学基础

> 📖 Docs: [ROS 2 TF2](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| T | 齐次变换矩阵 | Homogeneous Transform | SE(3) |
| R | 旋转矩阵 | Rotation Matrix | SO(3), 3×3 |
| t | 平移向量 | Translation Vector | ℝ³ |
| q | 四元数 | Quaternion | (w, x, y, z), ‖q‖=1 |
| θ | 旋转角度 | Rotation Angle | [0, 2π] (rad) |
| frame_id | 坐标系名称 | Frame ID | 字符串 |

---

## 核心公式

### 公式 1: 齐次变换（坐标系间的位姿关系）

**直觉：** TF 系统的核心——描述一个坐标系相对于另一个坐标系的位置和朝向。RViz 用这些变换来正确放置每个 Display 的数据。

$$
T_{parent}^{child} = \begin{bmatrix} R & t \\ 0 & 1 \end{bmatrix}
= \begin{bmatrix} r_{11} & r_{12} & r_{13} & t_x \\ r_{21} & r_{22} & r_{23} & t_y \\ r_{31} & r_{32} & r_{33} & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

**参数解释：**

| 参数 | 含义 | 例子 |
|------|------|------|
| R (3×3) | 旋转矩阵 | child 坐标系相对于 parent 的旋转 |
| t (3×1) | 平移向量 (tₓ, tᵧ, t_z) | child 原点在 parent 中的位置 |

### 公式 2: 四元数（ROS 2 中表示旋转的方式）

**直觉：** ROS 2 的 TF 用四元数而不是欧拉角表示旋转（避免万向锁问题）。四元数是 4 个数 (w, x, y, z)。

$$
q = w + xi + yj + zk, \quad \|q\| = 1
$$

绕轴 (aₓ, aᵧ, a_z) 旋转 θ 角的四元数：

$$
q = \left(\cos\frac{\theta}{2},\; a_x\sin\frac{\theta}{2},\; a_y\sin\frac{\theta}{2},\; a_z\sin\frac{\theta}{2}\right)
$$

**常用四元数：**

| 旋转 | 四元数 (w, x, y, z) |
|------|---------------------|
| 无旋转 | (1, 0, 0, 0) |
| 绕 Z 轴 90° | (0.707, 0, 0, 0.707) |
| 绕 Z 轴 180° | (0, 0, 0, 1) |

### 公式 3: 坐标变换链

**直觉：** 如果你知道 `map→odom` 的变换和 `odom→base_link` 的变换，可以链式相乘得到 `map→base_link` 的变换。RViz 需要这条链完整才能正确显示。

$$
T_{map}^{base\_link} = T_{map}^{odom} \times T_{odom}^{base\_link}
$$

**TF 树示例：**

```
map
 └── odom
      └── base_link
           ├── camera_link
           ├── lidar_link
           └── wheel_left_link
```

RViz 要显示 `camera_link` 的数据，需要 `map → odom → base_link → camera_link` 整条链存在。**任何一节断了，RViz 就显示不出来。**

---

## 手算练习

### 练习 1: 简单平移变换

**题目：** `base_link` 在 `odom` 坐标系中位于 (3, 2, 0)，无旋转。`camera_link` 在 `base_link` 前方 0.1m、高0.15m。camera_link 在 odom 中的位置是什么？

**解答：**

1. T_odom^base = 平移 (3, 2, 0)
2. T_base^camera = 平移 (0.1, 0, 0.15)
3. T_odom^camera = T_odom^base × T_base^camera
4. camera 在 odom 中的位置 = (3+0.1, 2+0, 0+0.15) = **(3.1, 2, 0.15)** ✅

---

## 公式速查表

| 名称 | 公式 | 用途 |
|------|------|------|
| 齐次变换 | T = [R, t; 0, 1] | 描述坐标系之间的位姿 |
| 四元数旋转 | q = (cos θ/2, aₓ sin θ/2, …) | 无万向锁旋转表示 |
| 变换链 | T_A^C = T_A^B × T_B^C | 链式计算坐标变换 |
| 逆变换 | T⁻¹ = [Rᵀ, -Rᵀt; 0, 1] | 反向坐标变换 |
