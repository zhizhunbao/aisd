---
topic: object_detection
dimension: tutorial
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Szeliski, 《Computer Vision: Algorithms and Applications》 2nd Ed. Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/szeliski_cv.pdf"
  - "📖 Paper: Girshick et al., 'R-CNN', CVPR 2014 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/girshick_2014_rcnn.pdf"
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
  - "📖 Paper: Redmon et al., 'YOLO', CVPR 2016 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/redmon_2016_yolo.pdf"
  - "📖 Paper: Lin et al., 'FPN', CVPR 2017 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/lin_2017_fpn.pdf"
  - "📖 Paper: Carion et al., 'DETR', ECCV 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/carion_2020_detr.pdf"
  - "📖 Docs: torchvision Object Detection — https://pytorch.org/vision/stable/models.html#object-detection"
expiry: 12m
status: current
---

# Object Detection 教程

> **前置知识：** CNN 基础（卷积/池化/特征图）、图像分类（ImageNet 预训练）、损失函数（交叉熵/回归损失）
> **参考来源：** [Szeliski《CV》](../../../textbooks/szeliski_cv.pdf) Ch.6, [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf)

---

## Section 0: 前置知识速查

1. **CNN 特征图**：卷积网络逐层提取越来越高级的特征，浅层是边缘/纹理，深层是语义部件/物体
2. **ImageNet 预训练**：在 120 万张图片上训练的分类网络（如 ResNet-50）可以作为通用特征提取器
3. **交叉熵损失**：衡量预测概率分布与真实标签之间的差距，$-\sum y_i \log p_i$
4. **回归损失**：衡量预测值与真实值之间的距离，如 L1、L2、Smooth L1
5. **迁移学习**：把在大数据集上学到的权重迁移到小数据集任务，只需微调少量参数

> 📖 Docs: [PyTorch Transfer Learning](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **自动驾驶系统无法工作** — 只知道"前方有车"不够，必须知道车在哪里、离我多远、有多大，才能做出制动/变道决策
- 🔥 **安防监控形同虚设** — 如果只能判断"视频里有人"，无法定位可疑人员在监控画面中的具体位置，安保人员依然需要盯着每一帧
- 🔥 **工业质检只能靠人眼** — 流水线上的缺陷检测必须同时知道"缺陷类型"和"缺陷位置"，才能自动标记或剔除不合格品
- 🔥 **医学影像辅助诊断无法落地** — 医生不只需要"这张 CT 里有肿瘤"，还需要知道肿瘤在哪个区域、有多大

### 它的核心价值

1. **从"是什么"到"在哪里"** — 图像分类只能给出整张图的标签，目标检测同时输出每个物体的类别 + 位置，信息量质的飞跃
2. **支撑下游任务** — 实例分割、目标跟踪、场景理解、动作识别等高级任务都依赖于先检测到物体
3. **自动化替代人工** — 一旦检测准确可靠，大量依赖人眼识别 + 定位的工作可以被自动化

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2
> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014, Section 1

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 目标检测的核心范式演进

```
传统方法（2001-2012）         Two-Stage（2014-2017）          One-Stage（2016-今）            Transformer（2020-今）
┌──────────────────┐      ┌──────────────────────┐      ┌────────────────────┐      ┌──────────────────┐
│ 滑动窗口          │      │ 候选区域 + 分类        │      │ 密集预测            │      │ 集合预测          │
│ + 手工特征        │      │ + CNN 特征            │      │ + CNN 特征          │      │ + Transformer     │
│ (Viola-Jones,     │ ──→  │ (R-CNN, Fast R-CNN,   │ ──→  │ (YOLO, SSD,        │ ──→  │ (DETR, DINO,      │
│  HOG+SVM, DPM)   │      │  Faster R-CNN)        │      │  RetinaNet)        │      │  RT-DETR)         │
└──────────────────┘      └──────────────────────┘      └────────────────────┘      └──────────────────┘
  手工特征，计算慢           CNN 自动学特征              一步出结果，速度快          去除 anchor/NMS
```

### 2.2 Two-Stage 检测器核心机制（以 Faster R-CNN 为例）

**设计决策：为什么要分两步？**

- 第一步（RPN）：快速筛选"这里可能有物体"的区域，从几万个 anchor 中筛选出 ~300 个高质量候选框
- 第二步（Head）：对每个候选框精细分类 + 精修边界框
- 好处：第一步大量丢弃背景，第二步只需处理少量候选，分类精度更高

```
输入图像 (H×W×3)
    │
    ▼
┌─────────────────────────────┐
│  Backbone (ResNet-50)       │  ← 在 ImageNet 上预训练
│  提取多尺度特征图            │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  Neck (FPN)                 │  ← 融合多尺度特征
│  {P2, P3, P4, P5}          │
└─────────────────────────────┘
    │
    ▼ (第一步)
┌─────────────────────────────┐
│  RPN (Region Proposal Net)  │
│  每个位置 k 个 anchor：      │
│  → 物体 vs 背景 (cls)       │
│  → 框偏移 (reg)             │
│  → NMS → ~300 个 proposals  │
└─────────────────────────────┘
    │
    ▼ (第二步)
┌─────────────────────────────┐
│  RoI Align                  │  ← 从特征图裁剪固定大小特征
│  + Detection Head           │
│  → N 类分类 + 框精修         │
│  → NMS → 最终检测结果       │
└─────────────────────────────┘
```

### 2.3 One-Stage 检测器核心机制（以 YOLO 为例）

**设计决策：为什么可以一步到位？**

- **关键洞察**：物体检测可以被看作对整张图的回归问题——把图像分成 S×S 网格，每个网格直接预测 B 个 box + C 个类别概率
- **代价**：取消了候选区域提议，在精度上（尤其是小物体和密集物体）有损失
- **收益**：速度极快，适合实时应用（YOLO v1 达到 45 FPS）

```
输入图像 (448×448×3)
    │
    ▼
┌─────────────────────────────┐
│  Backbone                   │
│  提取特征图                  │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  S×S 网格                   │  ← 例如 7×7 = 49 个格子
│  每个格子直接预测：          │
│  → B 个 bbox (x,y,w,h,conf)│  ← B=2，每格 2 个框
│  → C 个类别概率             │  ← C=20（VOC 20 类）
│  → 输出: S×S×(B×5+C)       │  ← 7×7×30
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  NMS 后处理                 │
│  → 最终检测结果             │
└─────────────────────────────┘
```

### 2.4 DETR 核心机制

**设计决策：为什么用 Transformer？**

- **痛点**：传统方法需要大量手工设计——anchor 的大小/比例、NMS 阈值、正负样本匹配策略
- **DETR 的做法**：把检测定义为**集合预测问题**，用 100 个可学习的 object queries 通过 Transformer 直接输出 100 个预测，用匈牙利算法做预测与 GT 一对一匹配
- **好处**：彻底去除 anchor 和 NMS，管线更简洁

> 📖 Paper: Carion et al., [DETR](../../../.documents/papers/object_detection/carion_2020_detr.pdf), ECCV 2020

---

## Section 3: 局限性

1. **小物体检测精度低** — 小物体在深层特征图上只有几个像素，特征分辨率不足 → 应对：FPN 多尺度特征融合、高分辨率训练
2. **密集遮挡场景困难** — 多个物体高度重叠时，(a) NMS 可能误删正确框，(b) anchor 匹配困难 → 应对：Soft-NMS、DETR 的集合预测
3. **类别不平衡严重** — 绝大多数 anchor 是背景（正负比可达 1:1000），导致训练被无意义的负样本主导 → 应对：Focal Loss、OHEM
4. **新类别需要重新标注** — 传统封闭集检测器只能检测训练时见过的类别 → 应对：Open-Vocabulary Detection (OWL-ViT, Grounding DINO)
5. **Bounding Box 表示受限** — 矩形框无法精确描述非矩形物体（如倾斜文本、弯曲物体）→ 应对：旋转框检测、实例分割

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2
> 📖 Paper: Lin et al., [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf), CVPR 2017

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Faster R-CNN** | 精度高，尤其小物体；成熟生态 | 速度较慢（~5-7 FPS） | 精度优先：医学影像、卫星图 |
| **YOLO (v8/v11)** | 极快（>100 FPS）；部署方便 | 小物体精度稍逊；版本迭代快 | 实时应用：视频监控、自动驾驶 |
| **SSD** | 速度快；多尺度检测 | 精度不如 Faster R-CNN | 嵌入式/移动端 |
| **RetinaNet** | 单阶段 + Focal Loss 解决类别不平衡 | 需要调 $\gamma$ 和 $\alpha$ | 高密度小物体 |
| **DETR** | 无 anchor/NMS，架构简洁 | 训练慢（需 500 epoch）；小物体弱 | 研究/定制场景 |
| **RT-DETR** | Transformer + 实时速度 | 较新，生态不如 YOLO | 需要 Transformer 优势的实时场景 |

> 📖 Paper: Redmon et al., [YOLO](../../../.documents/papers/object_detection/redmon_2016_yolo.pdf), CVPR 2016
> 📖 Paper: Carion et al., [DETR](../../../.documents/papers/object_detection/carion_2020_detr.pdf), ECCV 2020

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《CV》Ch.6](../../../textbooks/szeliski_cv.pdf) | 📚 教科书 | 全文核心参考 |
| [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf) | 📖 论文 | Section 1 痛点 + Section 2 范式演进 |
| [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf) | 📖 论文 | Section 2 Two-Stage 机制 |
| [YOLO](../../../.documents/papers/object_detection/redmon_2016_yolo.pdf) | 📖 论文 | Section 2 One-Stage 机制 + Section 4 对比 |
| [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf) | 📖 论文 | Section 3 多尺度 |
| [DETR](../../../.documents/papers/object_detection/carion_2020_detr.pdf) | 📖 论文 | Section 2 Transformer + Section 4 对比 |
| [torchvision Detection](https://pytorch.org/vision/stable/models.html#object-detection) | 📖 文档 | API 参考 |
