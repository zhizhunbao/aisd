# Week 11 故事线：从算法到部署——构建完整的 CV 技术栈

> **Source:** `Week 11 - OpenMMLab and CV Tech Stack.pptx`
> **核心主题：** 做计算机视觉不只是写算法——你还需要一整套工具链来管理环境、统一接口、容器化交付、云端训练，最终让模型从实验室走向生产
> **故事线：** 像盖房子一样搭建 CV 开发体系——OpenMMLab 是设计图纸和标准件仓库，Conda 是地基（环境），Docker 是集装箱（交付），VS Code 是工作台（开发），AWS EC2 是起重机（算力）

---

## 🎬 序幕：我们在解决什么问题？

### 真实场景：CV 研究者的日常噩梦

想象你是一个计算机视觉研究者，你的日常可能是这样的：

1. **周一**：想试试 Faster R-CNN 做目标检测 → 下载了 Facebook 的实现，Python 3.7 + PyTorch 1.6
2. **周二**：想跟 YOLO 比一下 → 下载了 Darknet 的实现，C 语言 + CUDA，得重新编译
3. **周三**：想加上语义分割 → 下载了 DeepLab 的实现，TensorFlow 1.x，跟 PyTorch 环境冲突
4. **周四**：跑通了一个模型，发给同事 → "在我的机器上跑不了"
5. **周五**：老板说要部署到生产环境 → 你发现训练代码根本没考虑过部署……

> 💡 **核心痛点：** CV 领域的算法源码来自不同团队、不同框架、不同编程语言，它们之间**没有统一的接口、没有统一的环境、没有统一的部署方式**。每换一个算法就像换一个宇宙。

**本讲要回答的问题：** 如何构建一套**从算法选型 → 环境管理 → 开发调试 → 容器交付 → 云端训练**的完整工具链，让 CV 开发像搭积木一样标准化？

---

## 📚 第一章：OpenMMLab——CV 的"标准件仓库"

### 1.1 问题：算法代码的碎片化灾难

在 OpenMMLab 出现之前，CV 领域面临的最大挑战是**代码的多样性和不一致性**：

| 问题 | 具体表现 |
|------|----------|
| **框架不统一** | Faster R-CNN 用 Caffe，YOLO 用 Darknet，DeepLab 用 TensorFlow |
| **接口不一致** | 每个算法的数据加载、训练循环、评估方式都不同 |
| **文档参差不齐** | 有的只有论文没有代码，有的代码没有文档 |
| **复现困难** | 论文里的结果，换个人跑可能差几个点 |

> 💡 **类比：** 想象你盖房子，但每个供应商的螺丝尺寸都不一样，电线接口也不兼容——这就是 CV 研究者面临的现状。

### 1.2 解决方案：OpenMMLab 的设计理念

OpenMMLab 的核心理念是：**为 CV 提供一套模块化 (Modular)、可复用 (Reusable)、可扩展 (Extendable) 的标准组件。**

- **一句话定义：** OpenMMLab = 一个用 PyTorch 统一实现各种 CV 算法的开源工具体系
- **设计原则：** 所有工具箱共享一个通用框架 (Common Framework)，数据加载、模型定义、训练循环、评估指标都有统一接口
- **核心价值：** 研究者只需关注算法创新本身，而不需要从零搭建训练流程

> 💡 **类比：** OpenMMLab 就像**乐高积木** (LEGO) ——每个工具箱是一套专题积木（检测套装、分割套装、跟踪套装），但所有积木的接口标准是一样的，你可以自由组合。

### 1.3 核心工具箱矩阵

OpenMMLab 按 CV 任务类型提供了一系列专用工具箱：

| 工具箱 | 任务 | 典型算法 | 应用场景 |
|--------|------|----------|----------|
| **MMPretrain** | 预训练 + 图像分类 | ResNet, ViT, CLIP | 迁移学习基础 |
| **MMDetection** | 2D 目标检测 + 实例分割 | Faster R-CNN, YOLO, SSD | 安防、自动驾驶 |
| **MMDetection3D** | 3D 目标检测 | PointPillars, SECOND | 自动驾驶、机器人 |
| **MMRotate** | 旋转目标检测 | Rotated Faster R-CNN | 航拍图像、文字检测 |
| **MMTracking** | 视频目标跟踪 | SORT, DeepSORT | 运动分析、监控 |
| **MMSegmentation** | 语义分割 | U-Net, DeepLab, PSPNet | 医学图像、地理信息 |
| **MMAction2** | 动作识别 | 3D CNN, TSN | 行为分析、体育 |
| **MMDeploy** | 模型部署 | ONNX, TensorRT, OpenVINO | 生产环境上线 |

> 💡 **记忆技巧：** "MM" = Multi-Media / Multi-Model。工具箱名称 = MM + 任务英文名。

### 1.4 MMDeploy：从实验到生产的桥梁

MMDeploy 值得单独强调，因为它解决了一个关键问题：**训练好的模型如何在实际设备上高效运行？**

```
训练模型 (PyTorch) 
    → Model Converter（模型转换器）
        → ONNX / TorchScript / TensorRT
    → MMDeploy Model（包含模型 + 元信息）
    → Inference SDK（C/C++，支持 Python/C#/Java）
        → 部署到 Linux / Windows / macOS / Android
```

支持的推理后端：ONNX Runtime、TensorRT、OpenVINO、ncnn 等

> 💡 **类比：** 如果训练模型是"原型车"，MMDeploy 就是"量产线"——它把实验室里的模型转换成可以在各种设备上跑的"成品"。

### 1.5 ❗ OpenMMLab 的局限——"有了工具箱，但房子还是盖不起来"

OpenMMLab 解决了**算法层面的统一性**问题，但一个完整的 CV 项目远不止算法：

| 已解决 ✅ | 未解决 ❌ |
|-----------|-----------|
| 算法接口统一 | 谁来管理 Python 环境和库依赖？ |
| 代码标准化 | 怎么保证"在我的机器上也能跑"？ |
| 模型可部署 | 去哪里找 GPU 算力？ |
| 文档完善 | 如何高效地写代码和调试？ |

> 🔑 **故事转折点：** OpenMMLab 给了你标准化的"建筑材料"，但你还需要**地基（环境管理）→ 搬运工具（容器化）→ 工作台（IDE）→ 起重机（云算力）** 才能真正盖起房子。接下来的故事就是：如何搭建这套完整的 CV 开发基础设施？

---

## 🎭 第二章：Conda——给 CV 项目打地基（环境管理）

### 2.1 问题：依赖地狱 (Dependency Hell)

CV 项目的依赖管理特别复杂：

- OpenMMLab 需要特定版本的 PyTorch
- PyTorch 需要特定版本的 CUDA
- CUDA 需要特定版本的 GPU 驱动
- 同时你可能还有另一个项目需要 TensorFlow（跟 PyTorch 的 CUDA 版本可能冲突）

> 💡 **类比：** 就像你在同一个厨房里同时做中餐和西餐——调料瓶混在一起、锅具互相占用、温度设置冲突。你需要**两个独立的厨房**。

### 2.2 解决方案：Conda 的隔离环境

Conda 的核心价值：**创建完全隔离的 Python 环境，每个环境有独立的 Python 版本和库。**

```bash
# 创建一个专用于 OpenMMLab 的环境
conda create -n mmlab python=3.9

# 激活环境
conda activate mmlab

# 安装依赖（互不干扰）
conda install numpy pandas matplotlib
conda install -c conda-forge opencv
conda install pytorch torchvision -c pytorch

# 导出环境（分享给同事）
conda env export > environment.yml

# 同事一键复现环境
conda env create -f environment.yml
```

### 2.3 Conda 的核心命令速查

| 命令 | 功能 |
|------|------|
| `conda create -n [名称] python=[版本]` | 创建新环境 |
| `conda activate [名称]` | 激活环境 |
| `conda install [包名]` | 安装包 |
| `conda list` | 查看已安装包 |
| `conda env list` | 查看所有环境 |
| `conda env export > environment.yml` | 导出环境配置 |
| `conda env create -f environment.yml` | 从配置文件创建环境 |

> 💡 **关键提示：** Conda 频道 (Channel) 扩展了包的可用性。`conda-forge` 是最大的社区频道。遇到依赖冲突时，可以通过指定包版本来解决：`conda install numpy=1.21`。

### 2.4 ❗ Conda 的局限——"环境隔离了，但换台电脑还是出问题"

Conda 解决了**同一台机器上**的环境隔离，但跨机器时仍有问题：

| Conda 已解决 ✅ | Conda 未解决 ❌ |
|-----------------|-----------------|
| Python 版本隔离 | 操作系统级依赖（如 CUDA 驱动） |
| 库版本管理 | 系统库版本差异（如 libstdc++） |
| 环境可复现（同 OS） | 跨 OS 的环境一致性 |

> 🔑 **故事转折点：** Conda 管住了 Python 层面的依赖，但操作系统级别的差异仍然导致"在我的机器上能跑，在你的机器上不行"。我们需要更彻底的隔离——**把整个操作系统也打包进去** → Docker 登场！

---

## 📖 第三章：Docker——把整个环境装进集装箱（容器化）

### 3.1 问题回顾：跨机器的环境不一致

即使用了 Conda，以下场景仍然会失败：
- 你的 Ubuntu 20.04 + CUDA 11.3 训练好的模型 → 同事的 Windows 10 跑不了
- 你的开发环境 → 公司的生产服务器配置不同
- 你的代码 → 云端 GPU 服务器的系统版本不同

### 3.2 解决方案：Docker 容器

Docker 的核心理念：**把应用 + 所有依赖 + 操作系统库 打包成一个标准化的"集装箱"（Container），在任何地方都能一致运行。**

- **一句话定义：** Docker 容器 = 轻量级的虚拟机，包含运行应用所需的一切
- **与虚拟机的区别：** Docker 共享宿主机内核，启动秒级、开销极小；虚拟机模拟完整 OS，启动分钟级、开销大

### 3.3 Docker 工作流

```
Dockerfile（定义环境的"食谱"）
    → docker build（按食谱"烹饪"出镜像）
        → Docker Image（可分发的标准化"成品菜"）
            → docker run（把成品放上"餐桌"运行）
                → Container（运行中的实例）
```

**实际操作命令：**

```bash
# 1. 编写 Dockerfile
FROM pytorch/pytorch:1.9-cuda11.1-cudnn8-devel
RUN pip install mmdet mmcv-full

# 2. 构建镜像
docker build -t my-mmlab .

# 3. 运行容器
docker run --gpus all -v /data:/data my-mmlab python train.py
```

### 3.4 Docker Hub：镜像的"应用商店"

- **Docker Hub** 是云端的镜像仓库，类似 GitHub 管理代码
- `docker pull` 拉取现成镜像，`docker push` 分享自己的镜像
- OpenMMLab 官方提供预构建的 Docker 镜像，开箱即用
- 支持私有仓库，保护商业项目

### 3.5 Conda + Docker 的协作关系

| 层次 | 工具 | 管什么 |
|------|------|--------|
| **Python 环境** | Conda | Python 版本 + pip/conda 包 |
| **系统环境** | Docker | OS + 系统库 + CUDA + Conda 环境 |

> 💡 **最佳实践：** Docker 容器内用 Conda 管理 Python 环境 → 实现从操作系统到 Python 包的**完全隔离和可复现**。

### 3.6 ❗ Docker 的局限——"环境一致了，但开发效率不高"

Docker 解决了环境一致性，但引入了新问题：

| Docker 已解决 ✅ | Docker 新问题 ❌ |
|-----------------|-----------------|
| 跨机器环境一致 | 在容器内编辑代码不方便 |
| 一键部署 | 调试容器内的程序很痛苦 |
| 隔离性好 | 缺少 IDE 级别的代码补全和导航 |

> 🔑 **故事转折点：** 环境问题解决了，但我们还需要一个**高效的开发工具**来在容器化环境中写代码、调试、协作 → VS Code 登场！

---

## 📖 第四章：VS Code——CV 开发者的瑞士军刀（开发工具）

### 4.1 问题回顾：容器内开发的不便

有了 Docker 之后，代码运行环境在容器内，但开发者需要：
- 代码编辑 + 智能补全
- 断点调试 + 变量查看
- Git 版本控制
- 还要能**直接连接到 Docker 容器或远程服务器**

### 4.2 解决方案：VS Code + 扩展生态

VS Code 是一个轻量但功能强大的代码编辑器，通过扩展 (Extension) 系统支持几乎所有开发需求：

| 扩展 | 功能 |
|------|------|
| **Python** | 代码补全 (IntelliSense)、Linting、测试、环境管理 |
| **Docker** | 管理容器、镜像、Compose |
| **Remote - Containers** | 直接在 Docker 容器内开发 |
| **Remote - SSH** | 远程连接云服务器开发 |
| **Live Share** | 实时协作编码 |
| **Git** | 版本控制集成 |

### 4.3 关键能力：在 Docker 中调试

VS Code 的 **Remote - Containers** 扩展打通了"本地 IDE + 容器环境"的鸿沟：

```
本地 VS Code（编辑器界面）
    ↕ Remote - Containers 扩展
Docker 容器（运行环境：Python + PyTorch + OpenMMLab）
```

- 在容器内设置断点、查看变量、执行代码
- 开发环境 = 运行环境 = 部署环境 → **零差异**
- 调用栈检查 (Call Stack Inspection)、变量探索 (Variable Exploration)、条件断点

> 💡 **核心价值：** 不再是"本地写代码 → 复制到容器 → 运行 → 看日志猜错误"的低效循环，而是**直接在生产级环境中交互式开发和调试**。

### 4.4 ❗ VS Code 的局限——"工具齐了，但笔记本跑不动大模型"

到目前为止我们有了：
- ✅ OpenMMLab（标准化算法）
- ✅ Conda（Python 环境管理）
- ✅ Docker（系统级环境隔离）
- ✅ VS Code（高效开发调试）

但还有一个致命问题：**算力在哪里？**

训练一个现代目标检测模型需要：
- 多块高端 GPU（如 V100、A100）
- 大量内存和高速存储
- 持续训练数天甚至数周

个人电脑或实验室服务器往往不够用。

> 🔑 **故事转折点：** 本地硬件不够用 → 我们需要**弹性的、按需的云端算力** → AWS EC2 登场！

---

## 🏆 第五章：AWS EC2——按需取用的云端算力（云计算）

### 5.1 问题回顾：算力瓶颈

| 本地计算 | 挑战 |
|----------|------|
| 单 GPU | 训练太慢，大模型放不下 |
| 固定配置 | 不同任务需要不同规格 |
| 7×24 运行 | 电费、散热、维护成本高 |
| 硬件升级 | 买新 GPU 成本高、折旧快 |

### 5.2 解决方案：EC2 弹性计算

AWS EC2 (Elastic Compute Cloud) 提供按需的云端计算资源：

- **一句话定义：** EC2 = 云端的虚拟服务器，按小时/秒计费，GPU/CPU/内存可自由配置
- **核心价值：** 训练时开大机器，训练完关掉，只花必要的钱

### 5.3 GPU 实例选型

| 实例系列 | GPU | 适用场景 |
|----------|-----|----------|
| **P3** | V100 (16GB) | 大规模深度学习训练 |
| **G4** | T4 (16GB) | 推理 + 轻量训练 |
| **P4** | A100 (40GB) | 超大模型训练 |

### 5.4 成本管理策略

| 策略 | 说明 | 节省幅度 |
|------|------|----------|
| **按需实例 (On-Demand)** | 随时启停，最灵活 | 基准价 |
| **Spot 实例** | 竞价使用闲置资源 | 最高节省 90% |
| **预留实例 (Reserved)** | 承诺使用 1-3 年 | 节省 30-60% |
| **Auto Scaling** | 自动调整实例数量 | 避免浪费 |

配合 **AWS Budgets** 和 **Cost Explorer** 监控支出，避免"云端烧钱"。

### 5.5 EC2 + Docker 的完美搭配

```
本地开发（VS Code + Docker）
    → 将 Docker 镜像推送到 Docker Hub / ECR
        → EC2 GPU 实例拉取镜像
            → 在云端容器中训练
                → 模型保存到 S3
                    → 训练完毕，关闭实例
```

> 💡 **关键洞察：** Docker 保证了"本地 → 云端"的环境一致性，EC2 提供了弹性算力，两者结合使得"本地开发 + 云端训练"的工作流无缝衔接。

---

## 📹 第六章：TensorFlow Object Detection API——另一个选择

虽然本讲以 OpenMMLab 为主线，但值得了解 TensorFlow 生态也提供了成熟的目标检测工具：

| 维度 | OpenMMLab (MMDetection) | TensorFlow Object Detection API |
|------|------------------------|--------------------------------|
| **框架** | PyTorch | TensorFlow |
| **覆盖任务** | 检测 + 分割 + 跟踪 + 动作 + ... | 主要聚焦目标检测 |
| **支持模型** | Faster R-CNN, YOLO, SSD, ... | SSD, Faster R-CNN, Mask R-CNN |
| **模块化程度** | 高（跨工具箱统一框架） | 中（API 内部统一） |
| **社区** | 中国研究群体活跃 | 全球广泛使用 |

> 💡 **选型建议：** 如果你的团队已经用 TensorFlow，可以继续使用 TF API；如果你做学术研究或需要覆盖更多 CV 任务，OpenMMLab 的生态更完整。

---

## 🗺️ 全局回顾：CV 技术栈演进路线图

```
┌──────────────────────────────────────────────────────┐
│ CV 技术栈演进路线图                                    │
│                                                      │
│ ❌ 问题：算法代码碎片化，每个模型实现不兼容             │
│         │                                            │
│         ▼                                            │
│ ① OpenMMLab（算法层）                                │
│ ✅ 统一接口、模块化复用、标准化训练流程               │
│ ❌ 但：Python 依赖冲突怎么办？                       │
│         │                                            │
│         ▼                                            │
│ ② Conda（Python 环境层）                             │
│ ✅ 隔离 Python 环境、一键复现依赖                    │
│ ❌ 但：操作系统级差异导致跨机器不兼容                 │
│         │                                            │
│         ▼                                            │
│ ③ Docker（系统环境层）                               │
│ ✅ 整个运行环境容器化、跨平台一致                    │
│ ❌ 但：容器内开发不方便、缺少 IDE                    │
│         │                                            │
│         ▼                                            │
│ ④ VS Code + Remote（开发工具层）                      │
│ ✅ 直接在容器/远程服务器内开发调试                    │
│ ❌ 但：本地硬件跑不动大模型                          │
│         │                                            │
│         ▼                                            │
│ ⑤ AWS EC2（算力层）                                  │
│ ✅ 弹性 GPU 算力、按需计费、Spot 实例降本            │
│                                                      │
│ 🏁 完整的 CV 开发到部署工具链：                       │
│    算法 → 环境 → 容器 → 开发 → 算力 → 部署           │
└──────────────────────────────────────────────────────┘
```

### 技术演进转折总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 碎片化代码 → OpenMMLab | 算法接口不统一、复现困难 |
| 原始 Python → Conda | 依赖冲突、环境不可复现 |
| Conda → Docker | 跨机器的操作系统级差异 |
| Docker → VS Code Remote | 容器内开发调试的效率问题 |
| 本地计算 → AWS EC2 | 算力不足、大模型训练瓶颈 |

### 五层技术栈对应关系

| 层次 | 工具 | 管什么 | 类比 |
|------|------|--------|------|
| 算法层 | OpenMMLab | 模型代码 | 设计图纸 + 标准件仓库 |
| 环境层 | Conda | Python + 库 | 地基 |
| 系统层 | Docker | OS + 系统库 | 集装箱 |
| 工具层 | VS Code | 编辑 + 调试 | 工作台 |
| 算力层 | AWS EC2 | GPU / CPU | 起重机 |

---

## 📝 考试/复习重点检查清单

### OpenMMLab 核心

- [ ] 能说出 OpenMMLab 的设计理念（模块化、可复用、可扩展）
- [ ] 能列出至少 5 个核心工具箱及其对应任务（MMDetection → 目标检测、MMSegmentation → 语义分割等）
- [ ] 理解 MMDeploy 的作用：模型转换 → 推理 SDK → 多平台部署
- [ ] 知道 OpenMMLab 解决的核心问题：CV 算法代码碎片化和接口不统一

### Conda 环境管理

- [ ] 能写出创建、激活、导出 Conda 环境的命令
- [ ] 理解 Conda 频道 (Channel) 的作用，特别是 `conda-forge`
- [ ] 知道 `environment.yml` 的用途：跨机器复现 Python 环境

### Docker 容器化

- [ ] 理解 Docker 与虚拟机的区别（共享内核 vs 完整 OS 模拟）
- [ ] 能描述 Dockerfile → Image → Container 的工作流
- [ ] 知道 Docker Hub 的用途：云端镜像仓库
- [ ] 理解 Docker 如何保证跨平台环境一致性

### VS Code 开发

- [ ] 知道 Remote - Containers 扩展的作用：在容器内直接开发调试
- [ ] 能列出 CV 开发常用的 VS Code 扩展（Python、Docker、Remote SSH、Live Share）
- [ ] 理解"开发环境 = 运行环境 = 部署环境"的理想状态

### AWS EC2 云计算

- [ ] 知道 EC2 GPU 实例系列（P3/G4/P4）及其适用场景
- [ ] 理解 Spot 实例的概念及其成本优势
- [ ] 能描述从本地开发到云端训练的完整工作流
- [ ] 知道 Auto Scaling、AWS Budgets 等成本管理工具

### 全局理解

- [ ] 能画出/描述五层 CV 技术栈的逻辑关系
- [ ] 理解每一层工具解决的核心问题和局限性
- [ ] 能说明为什么不能只用其中一个工具——每层解决不同层面的问题

---

## 📚 参考资料

- [week11_openmmlab_slides.md](week11_openmmlab_slides.md) — 原始双语讲义
- [OpenMMLab 官方文档](https://openmmlab.com/) — 工具箱详细文档
- [Conda 用户指南](https://docs.conda.io/) — 环境管理参考
- [Docker 官方文档](https://docs.docker.com/) — 容器化参考
- [AWS EC2 文档](https://docs.aws.amazon.com/ec2/) — 云计算参考
