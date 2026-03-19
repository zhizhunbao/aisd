---
topic: object_detection
dimension: bridge
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Szeliski, 《Computer Vision: Algorithms and Applications》 2nd Ed. Ch.6-7 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/szeliski_cv.pdf"
  - "📚 Book: Goodfellow, Bengio & Courville, 《Deep Learning》 Ch.9 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: He et al., 'Mask R-CNN', ICCV 2017 — https://arxiv.org/abs/1703.06870"
expiry: 12m
status: current
---

# Object Detection 衔接与扩展

> 📚 Book: Szeliski, [《Computer Vision: Algorithms and Applications》](../../../textbooks/szeliski_cv.pdf), Ch.6 "Recognition"

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | CNN 基础（卷积/池化） | Backbone 的构建基础 | ../../deep-learning/conv_layer/ |
| ← 前置 | 图像分类 | 检测 = 分类 + 定位 | — |
| ← 前置 | 迁移学习 | Backbone 预训练策略 | ../../deep-learning/transfer_learning/ |
| → 后续 | 实例分割 | 在检测框内加像素级掩码 (Mask R-CNN) | — |
| → 后续 | 全景分割 | 统一语义分割 + 实例分割 | — |
| → 后续 | 目标跟踪 | 在视频中跨帧追踪检测到的物体 | — |
| → 后续 | 3D 目标检测 | 从 2D bbox 扩展到 3D bbox | — |
| → 后续 | Open-Vocabulary Detection | 检测训练时未见过的类别 | — |

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6-7

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| CNN 基础 | 卷积层、池化层、特征图 | 作为 Backbone 的构建模块，逐层提取从边缘到语义的多级特征 |
| 图像分类 | ImageNet 预训练权重 | Backbone 使用分类网络的预训练权重做迁移学习 |
| 迁移学习 | 微调策略 | 冻结浅层、微调深层，或全部微调 |
| 损失函数 | 交叉熵、L1/L2 回归损失 | 检测的分类头用 CE/Focal Loss，回归头用 Smooth L1 |
| 概率论 | 条件概率、贝叶斯 | 理解检测置信度、后验概率 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| 实例分割 | Backbone-Neck-Head 架构 + RoI Align | Mask R-CNN = Faster R-CNN + 语义分割分支 |
| 全景分割 | 检测框 + 类别预测 | Panoptic FPN = FPN 检测 + 语义分割统一 |
| 目标跟踪 | 逐帧检测结果 | SORT/DeepSORT 在检测框基础上做跨帧关联 |
| 姿态估计 | 人体检测框 | 先检测人体 bbox，再在框内做关键点检测 |
| 3D 检测 | 2D 检测框范式 | 3D bbox 回归 = 在 2D 基础上增加深度/旋转预测维度 |
| 视频理解 | 时空检测 | 动作检测 = 空间上检测人 + 时间上识别动作 |
| Open-Vocabulary Detection | 检测管线 + CLIP | 用语言-视觉模型替代固定类别分类头 |

> 📖 Paper: He et al., Mask R-CNN, ICCV 2017

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 候选区域生成 | Selective Search（手工算法） | RPN（可学习网络）/ 无候选区域 (YOLO) | 端到端训练需求 |
| 特征提取 | HOG、Haar（手工设计） | CNN / Vision Transformer（自动学习） | 深度学习的表达能力远超手工特征 |
| 多尺度检测 | 图像金字塔（多次缩放输入） | FPN（单次前向 + 特征金字塔） | 图像金字塔计算量太大 |
| 后处理 | NMS（贪心删除重叠框） | 无 NMS（DETR 一对一匹配） | NMS 是不可微操作，不能端到端学习 |
| 正负样本匹配 | IoU 阈值硬匹配 | 匈牙利算法（DETR） / 动态匹配 | 固定阈值不够灵活 |
| 损失函数 | 交叉熵 + L2 | Focal Loss + Smooth L1 / GIoU / CIoU | 类别不平衡 + 框回归需要更好的度量 |

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Faster R-CNN 原文](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf) | 📖 论文 | Two-Stage 检测器的集大成之作，理解 RPN 的设计动机 | ⭐⭐⭐ |
| [DETR 原文](../../../.documents/papers/object_detection/carion_2020_detr.pdf) | 📖 论文 | 理解为什么 Transformer 能去除 anchor 和 NMS | ⭐⭐⭐⭐ |
| [Focal Loss (RetinaNet)](https://arxiv.org/abs/1708.02002) | 📖 论文 | 类别不平衡问题的深入分析和优雅解决方案 | ⭐⭐⭐ |
| [DINO: DETR with Improved DeNoising](https://arxiv.org/abs/2203.03605) | 📖 论文 | DETR 系列最新进展 | ⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [YOLOv8 Documentation](https://docs.ultralytics.com/) | YOLO 系列最新迭代 vs Faster R-CNN | 需要选型时 |
| [mmdetection 模型库](https://github.com/open-mmlab/mmdetection) | 多种检测器统一实现和对比 | 需要横向对比不同检测器时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [COCO 数据集和竞赛](https://cocodataset.org/) | 检测领域最权威的基准 | 评估模型性能时 |
| [Grounding DINO](https://arxiv.org/abs/2303.05499) | 文本引导的开放词汇检测 | 对 VLM + 检测融合感兴趣时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| deep-learning 课程 | 15 主题 | conv_layer, transfer_learning | CNN 和迁移学习是 Object Detection 的基底 |
| machine-learning 课程 | 10+ 主题 | overfitting, model_evaluation_metrics | 模型评估方法论跨领域适用 |
| computer-vision 课程 | 本主题 | object_detection | 首个 CV 知识地图主题 |
