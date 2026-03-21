---
topic: irobot-create3
dimension: history
created: 2026-03-21
last_verified: 2026-03-21
source_versions:
  - "📖 Paper: Koenig & Howard, 'Design and Use Paradigms for Gazebo', IROS 2004 — https://doi.org/10.1109/IROS.2004.1389727"
  - "📖 Paper: Quigley et al., 'ROS: an open-source Robot Operating System', ICRA 2009 — https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf"
  - "📖 Paper: Soragna et al., 'Impact of ROS 2 Node Composition', IEEE RA-L 2023 — https://arxiv.org/abs/2305.09933"
  - "📖 Docs: iRobot Create 3 — https://iroboteducation.github.io/create3_docs/"
expiry: never
status: current
---

# iRobot Create 3 的故事线：从扫地机到 ROS 2 教育机器人

> **核心主题：** 一台扫地机器人如何用 20 年演变成一个完全 ROS 2 原生的 RL 训练平台
> **故事线：** 硬件不断进化，但真正的突破始终来自软件——从串行协议到 ROS 1 社区驱动，再到 ROS 2 原生集成

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> "我写了一个很酷的机器人算法——但没有真实机器人来验证它。"

2000 年代初，大学机器人课程面临一个尴尬：学生学了 SLAM、路径规划、避障算法，却只能在纯数学仿真里跑。真正的研究级机器人（PR2、Pioneer）要几万美元，实验室买得起但学生桌上放不下。

与此同时，iRobot 公司正在解决另一个完全不同的问题——把一台会自己扫地的机器人卖给普通家庭。他们不知道的是，这台扫地机器人的传感器套件（IR 接近、悬崖检测、差速驱动）恰好是机器人算法教学需要的一切。

> 🔑 **问题提出：** 能不能把一台便宜的扫地机器人变成一个教育平台？

---

## 📚 第一章：Roomba 与 Create 1 — 一台扫地机的教育化改造（2002-2007）

> **关键人物：** Colin Angle, Helen Greiner, Rodney Brooks — iRobot 三位联合创始人
> **关键论文：** 无（商业产品，非学术，但 Roomba 是世界上最成功的消费级移动机器人）

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Rodney Brooks 肖像 | Wikimedia Commons | `https://commons.wikimedia.org/wiki/File:Rodney_Brooks.jpg` | CC BY-SA |
| iRobot Create 1 照片 | iRobot 官网存档 | `https://web.archive.org/web/2010/https://www.irobot.com/create` | 公平使用 |

### 发生了什么？

2002 年，iRobot 发布了 Roomba——用 IR 传感器和碰撞传感器实现"随机碰撞式"扫地。它不够"聪明"，但够便宜（$200），够耐用。

2007 年，iRobot 做了一个聪明的决定：把 Roomba 400 系列底盘去掉吸尘模块，暴露一个 **串行端口（Serial/OI）**，命名为 **Create 1**。大学可以用 $130 买到一个有碰撞传感器、悬崖传感器、轮编码器的移动机器人。

### 为什么这很重要？

Create 1 让每个学生桌上都能放一台真实的移动机器人。它证明了"低成本传感器 + 开放接口 = 强大的教学工具"。

### 但还有一个问题……

Create 1 的接口是**串行协议**——你需要用 C 语言手写字节级别的通信代码来读传感器、发动作。没有标准化的消息格式，没有节点系统，代码完全不能复用。

> 🔑 **故事转折点：** 同一年（2007），Willow Garage 的一群人正在构思一个叫 "ROS" 的东西——一个标准化的机器人通信中间件。

---

## 📚 第二章：ROS + Gazebo — 标准化的力量（2004-2014）

> **关键人物：** Morgan Quigley（ROS 创造者），Nathan Koenig（Gazebo 创造者）
> **关键论文：** Koenig & Howard, [Gazebo IROS 2004](https://doi.org/10.1109/IROS.2004.1389727); Quigley et al., [ROS ICRA 2009](https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Gazebo 2004 论文首页 | IEEE IROS | `https://doi.org/10.1109/IROS.2004.1389727` | 学术引用 |
| ROS 2009 论文首页 | Stanford / ICRA | `https://www.willowgarage.com/sites/default/files/icraoss09-ROS.pdf` | 学术引用 |

### 发生了什么？

**2004 年**，Nathan Koenig 和 Andrew Howard 在 IROS 发表了 Gazebo——第一个支持 3D 物理+传感器噪声的开源多机器人仿真器。这意味着你可以在电脑上测试算法，再部署到真实机器人。

**2009 年**，Morgan Quigley 等人在 ICRA 发表了 ROS——不是操作系统，而是机器人通信的"中间件"。它定义了 Topic（发布/订阅）、Service（请求/响应）、TF（坐标系变换）等标准接口。

**2014 年**，iRobot 发布 Create 2（基于 Roomba 600），社区开发了 `create_autonomy` ROS 1 驱动包——但仍然是"串行协议 + 外部 ROS 桥接"的架构。

### 为什么这很重要？

ROS + Gazebo 创造了"先仿真后部署"的范式：你在 Gazebo 里写 `/cmd_vel`，在真实机器人上也用 `/cmd_vel`——代码一样。但 Create 2 是被迫通过第三方桥接加入 ROS 生态，不是原生支持。

### 但还有一个问题……

ROS 1 有一个致命弱点——它需要一个叫 `rosmaster` 的中央服务器。如果 `rosmaster` 挂了，所有节点都断开。而且 ROS 1 **不支持实时控制**，**不支持嵌入式处理器**——Create 2 这种资源受限设备无法直接运行 ROS 1。

> 🔑 **故事转折点：** Open Robotics 决定从零重写——这次叫 ROS 2，基于工业级 DDS 通信，去中心化，支持嵌入式。

---

## 📚 第三章：ROS 2 + Create 3 — ROS 在嵌入式上跑起来了（2017-2022）

> **关键人物：** Alberto Soragna（iRobot 工程师，ROS 2 Composition 核心作者）
> **关键论文：** Soragna et al., [Impact of ROS 2 Node Composition in Robotic Systems](https://arxiv.org/abs/2305.09933), IEEE RA-L 2023

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| ROS 2 Composition 论文首页 | arXiv | `https://arxiv.org/abs/2305.09933` | 学术引用 |
| Create 3 产品照片 | iRobot Education | `https://iroboteducation.github.io/create3_docs/` | 教育使用 |

### 发生了什么？

**2017 年**，ROS 2 正式发布——基于 DDS 的全新架构，去掉了 `rosmaster`，支持实时和嵌入式。但问题来了：嵌入式处理器的 CPU 和内存有限，能跑完整的 ROS 2 栈吗？

**2022 年**，iRobot 给出了答案：**Create 3**。这是第一台在嵌入式处理器上直接运行 ROS 2 的消费级机器人。关键技术是 **Node Composition**——把 `motion_control`、`robot_state`、`ui_mgr` 等节点合并到同一个进程，共享内存传递消息。

Soragna 等人的实验表明：Composition 节省了 **28% CPU** 和 **33% RAM**——没有这项技术，Create 3 根本跑不动 ROS 2。

### 为什么这很重要？

Create 3 不再是"串行协议 + 外部桥接"——它本身就是 ROS 2 节点。你插上 Wi-Fi，`ros2 topic list` 直接看到 `/cmd_vel`、`/odom`、`/imu`。而且官方 Gazebo 仿真暴露**完全相同**的 API——代码零修改从仿真迁移到真实。

### 但还有一个问题……

Create 3 仍然没有 LiDAR 和摄像头——纯依靠 IR 和里程计做 RL 会限制状态空间的丰富度。而且仿真 ≠ 真实（Sim-to-Real Gap）——物理引擎的近似误差在高精度任务中不可忽视。

> 🔑 **故事转折点：** TurtleBot 4 在 Create 3 底盘上加了 LiDAR + 深度摄像头 + Raspberry Pi 4，成为了完整的 SLAM 研究平台。而 Create 3 本身则作为"简洁版"专注于教学和 RL 入门。

---

## 🗺️ 全局回顾：技术演进路线图

    2002  Roomba 1        ──→  2007  Create 1       ──→  2014  Create 2
    (消费扫地机)                (教育平台 v1)              (硬件升级)
    IR + 碰撞 + 差速            + 串行协议 OI              + Roomba 600 底盘
                                                            + 社区 ROS 1 驱动

    2004  Gazebo           ──→  2009  ROS 1          ──→  2017  ROS 2
    (3D 物理仿真)               (中间件标准化)             (去中心化 + 嵌入式)
    Koenig & Howard              Quigley et al.

    2022 【Create 3】──→  未来  TurtleBot 4 / Create 4?
    ROS 2 原生!                + LiDAR + 深度相机
    Node Composition            + Nav2 内置
    Soragna et al.

### 每一步升级解决了什么核心问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| Roomba → Create 1 | 消费产品 → 教育平台（暴露串行接口） |
| 无标准 → ROS 1 | 各厂商协议不兼容 → Topic/Service/TF 标准化 |
| Player/Stage → Gazebo | 2D 仿真 → 3D 物理 + 传感器噪声 |
| Create 1 串行 → Create 2+ROS 1 | 字节级通信 → 标准化消息（但需要外部桥接） |
| ROS 1 → ROS 2 | rosmaster 单点故障 → DDS 去中心化 + 嵌入式支持 |
| Create 2+ROS 1 → **Create 3+ROS 2** | 外部桥接 → **原生 ROS 2**（Node Composition 让嵌入式可行） |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | Rodney Brooks | Wikimedia Commons: `File:Rodney_Brooks.jpg` | iRobot Create 1 存档照 | CC BY-SA / 公平使用 |
| 第二章 | Nathan Koenig, Morgan Quigley | 大学官网 | Gazebo IROS 2004 论文首页, ROS ICRA 2009 论文首页 | 学术引用 |
| 第三章 | Alberto Soragna | iRobot / LinkedIn | ROS 2 Composition 论文首页 arXiv:2305.09933 | 学术引用 |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选，多数科学家有公有领域肖像
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **Smithsonian Open Access** (`si.edu/openaccess`) — CC0 博物馆藏品
> 4. **Library of Congress** (`loc.gov/free-to-use`) — 美国历史公有领域
> 5. **Internet Archive** (`archive.org`) — 老书、老照片
> 6. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
