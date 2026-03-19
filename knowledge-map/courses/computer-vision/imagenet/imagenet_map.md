---
topic: imagenet
dimension: map
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Russakovsky et al., IJCV 2015 — https://arxiv.org/abs/1409.0575"
  - "📖 Paper: Deng et al., CVPR 2009 — https://doi.org/10.1109/CVPR.2009.5206848"
  - "📖 Paper: Krizhevsky et al., NeurIPS 2012 — https://arxiv.org/abs/1209.0270"
  - "📚 Book: Szeliski, 《Computer Vision: Algorithms and Applications》 2nd Ed. Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/szeliski_cv.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.1, Ch.12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch torchvision.datasets.ImageNet — https://pytorch.org/vision/stable/datasets.html"
expiry: 12m
status: current
---

# ImageNet 知识地图

> 📖 Paper: Russakovsky et al., [ImageNet Large Scale Visual Recognition Challenge](https://arxiv.org/abs/1409.0575), IJCV 2015
> 📖 Paper: Deng et al., [ImageNet: A Large-Scale Hierarchical Image Database](https://doi.org/10.1109/CVPR.2009.5206848), CVPR 2009
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1, Ch.12

## 1. 核心问题

- **ImageNet 是什么？** → 一个按 WordNet 层级结构组织的超大规模图像数据库，包含 1400 万+ 张标注图像、2.1 万+ 个类别
- **ILSVRC 竞赛为什么重要？** → 它是 2010-2017 年的深度学习「奥运会」，直接推动了 AlexNet、VGGNet、GoogLeNet、ResNet 等架构的诞生，定义了现代 CV 基准
- **ImageNet 如何改变了整个 AI 领域？** → 它证明了大规模有标注数据 + 深度网络 = 超人性能，从根本上改变了 AI 研究从「手工特征」到「端到端学习」的范式
- **ImageNet 的 1000 类子集（ILSVRC）和完整数据集有什么区别？** → ILSVRC 用 1000 类、120 万训练图像的子集做竞赛；完整 ImageNet 有 2.1 万类、1400 万图像
- **ImageNet 预训练权重为什么成为迁移学习的通用起点？** → 1000 类覆盖了足够丰富的视觉特征（纹理、形状、语义），使预训练特征可以迁移到几乎所有下游视觉任务

> 📖 Paper: Russakovsky et al., [ILSVRC](https://arxiv.org/abs/1409.0575), IJCV 2015, Section 1-2
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1.2.1 "The increasing size of datasets"

---

## 2. 全景位置

```
计算机视觉 Computer Vision
├── 图像形成与表示 Image Formation
├── 图像滤波与特征 Image Filtering & Features
├── 几何变换与配准 Geometric Transforms
├── 图像识别与分类 Image Recognition & Classification ← 你在这里
│   ├── 【ImageNet】 (大规模层级图像数据库 + ILSVRC 竞赛基准)
│   ├── CIFAR-10/100 (小规模学术基准)
│   ├── COCO (检测/分割多任务基准)
│   ├── Pascal VOC (经典检测/分割基准)
│   └── Open Images (Google 开放标注数据集)
├── CNN 架构演进 CNN Architecture Evolution
├── 目标检测 Object Detection
├── 图像分割 Image Segmentation
├── 视觉 Transformer Vision Transformer
└── 视觉语言模型 Vision-Language Models
```

> 📖 Paper: Russakovsky et al., [ILSVRC](https://arxiv.org/abs/1409.0575), Section 2 "Dataset"
> 📚 Book: Szeliski, [《Computer Vision》](../../../textbooks/szeliski_cv.pdf), Ch.6.3 "Object Recognition"

---

## 3. 依赖地图

```
前置知识                     本主题                       后续方向
┌─────────────────────┐     ┌──────────────────────┐     ┌──────────────────────────┐
│ WordNet 层级分类     │────→│                      │────→│ 迁移学习 Transfer Learn. │
│ 图像标注方法论       │────→│     ImageNet         │────→│ CNN 架构演进             │
│ 基本图像处理         │────→│  (数据集 + ILSVRC)   │────→│ 目标检测 Object Detection│
│ CNN 基础 (Conv/Pool) │────→│                      │────→│ 图像分割 Segmentation    │
│ 交叉熵损失函数       │────→│                      │────→│ 预训练范式 Pre-training   │
└─────────────────────┘     └──────────────────────┘     └──────────────────────────┘
```

> 📖 Paper: Deng et al., [ImageNet CVPR 2009](https://doi.org/10.1109/CVPR.2009.5206848), Section 2 "ImageNet construction"
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.12.2 "Computer Vision"

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [imagenet_map.md](imagenet_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [imagenet_concepts.md](imagenet_concepts.md) | ② 概念 | 理解 ILSVRC/Top-5/synset 等术语 |
| [imagenet_math.md](imagenet_math.md) | ③ 公式 | 理解 Top-k 准确率、交叉熵、softmax |
| [imagenet_tutorial.md](imagenet_tutorial.md) | ④ 教程 | Why-First 理解 ImageNet 设计动机 |
| [imagenet_code.md](imagenet_code.md) | ⑤ 代码 | 用 torchvision 加载 ImageNet 预训练模型 |
| [imagenet_pitfalls.md](imagenet_pitfalls.md) | ⑥ 踩坑 | 数据下载、标签映射、评估指标常见错误 |
| [imagenet_history.md](imagenet_history.md) | ⑦ 历史 | 从 Fei-Fei Li 到 ILSVRC 的演进故事 |
| [imagenet_bridge.md](imagenet_bridge.md) | ⑧ 衔接 | 找相关数据集、预训练、下游任务 |
| [imagenet_first_principles.md](imagenet_first_principles.md) | ⑨ 第一性原理 | 追问「为什么大数据+深度网络就能学会」 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1.2 "The increasing role of data"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [imagenet_map.md](imagenet_map.md) 了解全局位置
2. 读 [imagenet_tutorial.md](imagenet_tutorial.md) Section 1 理解为什么需要 ImageNet
3. 读 [imagenet_concepts.md](imagenet_concepts.md) 掌握 synset/ILSVRC/Top-5 等核心术语
4. 读 [imagenet_math.md](imagenet_math.md) 理解 Top-k 准确率和 softmax 公式
5. 跟 [imagenet_code.md](imagenet_code.md) 快速开始用预训练模型做推理
6. 读 [imagenet_history.md](imagenet_history.md) 了解从 Fei-Fei Li 到 ResNet 的故事
7. 读 [imagenet_first_principles.md](imagenet_first_principles.md) 追问大数据+深度学习的底层逻辑

### 日常参考 🔧

1. 查 [imagenet_code.md](imagenet_code.md) 预训练模型加载和推理 API
2. 查 [imagenet_math.md](imagenet_math.md) Top-1/Top-5 计算公式
3. 查 [imagenet_pitfalls.md](imagenet_pitfalls.md) 排查标签映射和数据加载问题

### 深度研究 🔬

1. 读 [imagenet_history.md](imagenet_history.md) 完整 ILSVRC 竞赛演进线
2. 读 [imagenet_first_principles.md](imagenet_first_principles.md) 追问数据规模定律
3. 读 [imagenet_bridge.md](imagenet_bridge.md) 探索 COCO/Open Images 等下游数据集
4. 阅读原始论文：Deng et al. CVPR 2009 + Russakovsky et al. IJCV 2015

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-18 | 12m | ✅ current |
| Concepts | 2026-03-18 | 12m | ✅ current |
| Math | 2026-03-18 | 12m | ✅ current |
| Tutorial | 2026-03-18 | 12m | ✅ current |
| Code | 2026-03-18 | 6m | ✅ current |
| Pitfalls | 2026-03-18 | 6m | ✅ current |
| History | 2026-03-18 | never | ✅ current |
| Bridge | 2026-03-18 | 12m | ✅ current |
| First Principles | 2026-03-18 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Russakovsky et al., ILSVRC, IJCV 2015](https://arxiv.org/abs/1409.0575) | 📖 论文 | 全文核心参考——竞赛规则、数据集规模、评估标准 |
| [Deng et al., ImageNet CVPR 2009](https://doi.org/10.1109/CVPR.2009.5206848) | 📖 论文 | Concepts/History——数据集构建方法、WordNet 映射 |
| [Krizhevsky et al., AlexNet NeurIPS 2012](https://arxiv.org/abs/1209.0270) | 📖 论文 | History——ILSVRC 2012 革命性突破 |
| [Simonyan & Zisserman, VGGNet ICLR 2015](https://arxiv.org/abs/1409.1556) | 📖 论文 | History——深度网络可行性验证 |
| [Szegedy et al., GoogLeNet CVPR 2015](https://arxiv.org/abs/1409.4842) | 📖 论文 | History——Inception 模块的效率革命 |
| [He et al., ResNet CVPR 2016](https://arxiv.org/abs/1512.03385) | 📖 论文 | History——残差学习突破深度限制 |
| [《Computer Vision》Ch.6](../../../textbooks/szeliski_cv.pdf) | 📚 教科书 | Tutorial/Concepts——图像识别背景 |
| [《Deep Learning》Ch.1, Ch.12](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Tutorial/First Principles——数据规模与深度学习 |
| [PyTorch torchvision.datasets.ImageNet](https://pytorch.org/vision/stable/datasets.html) | 📖 文档 | Code——数据加载和预训练模型 API |
| [PyTorch torchvision.models](https://pytorch.org/vision/stable/models.html) | 📖 文档 | Code——预训练权重使用 |
