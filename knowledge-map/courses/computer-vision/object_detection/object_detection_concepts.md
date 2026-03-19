---
topic: object_detection
dimension: concepts
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Szeliski, 《Computer Vision: Algorithms and Applications》 2nd Ed. Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/szeliski_cv.pdf"
  - "📖 Paper: Girshick et al., 'R-CNN', CVPR 2014 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/girshick_2014_rcnn.pdf"
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
  - "📖 Paper: Redmon et al., 'YOLO', CVPR 2016 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/redmon_2016_yolo.pdf"
  - "📖 Paper: Lin et al., 'FPN', CVPR 2017 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/lin_2017_fpn.pdf"
  - "📖 Paper: Carion et al., 'DETR', ECCV 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/carion_2020_detr.pdf"
expiry: 12m
status: current
---

# Object Detection 核心概念

> 📚 Book: Szeliski, [《Computer Vision: Algorithms and Applications》](../../../textbooks/szeliski_cv.pdf), Ch.6 "Recognition"
> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015

---

## 术语定义

### 目标检测 (Object Detection)

给定一张图像，找出图中**所有**属于预定义类别的物体，并为每个物体输出：(1) 一个包围框 (bounding box) 标注物体位置，(2) 一个类别标签标注物体是什么，(3) 一个置信度分数表示预测有多确定。与图像分类不同，目标检测同时解决"是什么"和"在哪里"两个问题。

> 易混淆：**图像分类 (Image Classification)** — 分类只输出整张图的类别标签，不定位；检测要输出每个物体的位置 + 类别

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2

### 包围框 (Bounding Box)

一个轴对齐的矩形框，用来框住目标物体的位置。通常表示为 (x, y, w, h) 或 (x₁, y₁, x₂, y₂)。前者是中心点坐标 + 宽高，后者是左上角和右下角坐标。几乎所有检测器的输出都是 bounding box 形式。

> 别名：**边界框**（中文直译）/ **bbox**（代码缩写）/ **detection box**（检测文献）— 都指同一个矩形框，bbox 是最常用的代码写法

> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014, Section 2

### 锚框 (Anchor Box)

检测器在特征图的每个位置预先放置的一组**固定大小和比例的参考框**。模型不直接预测 box 坐标，而是预测**相对于锚框的偏移量**（δx, δy, δw, δh），这样学习任务从"从零预测坐标"变成"微调已有框"，收敛更快更稳定。

> 别名：**先验框 (Prior Box)**（SSD 论文用语）/ **Default Box**（SSD 论文用语）— 概念完全相同，只是不同论文的不同叫法
> 易混淆：**Ground Truth Box** — anchor 是模型预设的参考框，GT box 是人工标注的真实框

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015, Section 3.1

### 交并比 (Intersection over Union, IoU)

衡量两个框重叠程度的指标。计算方式是两个框的交集面积除以并集面积，取值 [0, 1]。IoU = 1 表示完全重合，IoU = 0 表示完全不重叠。在目标检测中用于：(1) 训练时匹配 anchor 与 GT，(2) NMS 后处理，(3) 评估 mAP 时判断预测是否正确。

> 别名：**Jaccard 指数 (Jaccard Index)**（数学领域）— IoU 本质上就是集合论中的 Jaccard 相似系数，只是在检测领域换了名字

> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014, Section 3

### 非极大值抑制 (Non-Maximum Suppression, NMS)

目标检测的**后处理步骤**。检测器通常会对同一个真实物体产生多个重叠的预测框。NMS 的目的是只保留最好的那一个：(1) 按置信度排序所有框，(2) 取最高分的框，(3) 删除与它 IoU 超过阈值的其他框，(4) 重复直到处理完所有框。

> 易混淆：**Soft-NMS** — 标准 NMS 直接删除重叠框（硬删除），Soft-NMS 不删除而是降低置信度分数，更温和

> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014, Section C

### 区域提议网络 (Region Proposal Network, RPN)

Faster R-CNN 提出的一个**轻量级网络**，用来在特征图上生成候选区域（region proposals）。它在每个特征图位置放置 k 个 anchor，对每个 anchor 预测"是否包含物体"（二分类）和"框的偏移量"（回归）。RPN 取代了之前用手工方法（如 Selective Search）生成候选区域的步骤，使整个检测管线可以端到端训练。

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015, Section 3

### 骨干网络 (Backbone)

目标检测器的**特征提取部分**，通常是一个在 ImageNet 上预训练过的分类网络（如 ResNet-50、VGG-16），去掉最后的全连接层和 softmax。Backbone 的输出是多尺度的特征图（feature maps），后续的检测头在这些特征图上进行预测。

> 📖 Paper: Lin et al., [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf), CVPR 2017, Section 3

### 颈部网络 (Neck)

连接 Backbone 和 Head 的中间结构，负责将 Backbone 输出的**多尺度特征图进行融合和增强**。最经典的 Neck 是 FPN（Feature Pyramid Network），它通过自顶向下路径和横向连接，把高层语义信息传递给低层高分辨率特征图，使小物体也能获得丰富的语义信息。

> 📖 Paper: Lin et al., [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf), CVPR 2017, Section 3

### 检测头 (Detection Head)

检测器的**最终预测部分**，接收 Neck 输出的特征图，对每个位置/anchor 预测两件事：(1) 类别概率（分类头），(2) bounding box 坐标偏移（回归头）。在 Two-Stage 检测器中，Head 的输入还包括 RoI Pooling/RoI Align 提取的固定尺寸特征。

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015, Section 3.1

### 特征金字塔网络 (Feature Pyramid Network, FPN)

解决目标检测中**多尺度问题**的经典结构。传统方法要么只用最高层特征（丢失小物体信息），要么用图像金字塔（计算量爆炸）。FPN 用一个自底向上路径（Backbone 前向传播）+ 一个自顶向下路径（上采样 + 横向连接），在所有尺度上都构建语义丰富的特征图。

> 📖 Paper: Lin et al., [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf), CVPR 2017

### 平均精度均值 (Mean Average Precision, mAP)

目标检测最常用的评估指标。计算方法：(1) 对每个类别，按置信度排序所有预测框，(2) 逐个判断是否为 TP（IoU > 阈值且类别正确），(3) 画 Precision-Recall 曲线并计算曲线下面积 = AP，(4) 对所有类别的 AP 取均值 = mAP。PASCAL VOC 用 IoU=0.5，COCO 用 IoU 从 0.5 到 0.95 取均值。

> 别名：**AP**（只有一个类别的时候）/ **mAP@0.5**（PASCAL VOC 标准）/ **mAP@[.5:.95]**（COCO 标准）— mAP 后跟的数字是 IoU 阈值

> 📖 Docs: [COCO Detection Evaluation](https://cocodataset.org/#detection-eval)

### RoI Pooling / RoI Align

从特征图上裁剪出**对应候选区域的固定大小特征**的操作。RoI Pooling 用量化（取整）来对齐网格，这会引入位移误差。RoI Align 改用双线性插值消除量化误差，对小物体和分割任务来说精度提升显著。

> 易混淆：**RoI Pooling vs RoI Align** — Pooling 有量化误差（坐标取整），Align 用插值消除误差，Mask R-CNN 之后 Align 成为标准

> 📖 Paper: Girshick, [Fast R-CNN](../../../.documents/papers/object_detection/girshick_2015_fast_rcnn.pdf), ICCV 2015, Section 2.1

### DETR (Detection Transformer)

第一个把 **Transformer** 应用到目标检测的工作。核心想法是把检测重新定义为一个集合预测问题：输入一组可学习的 object queries，通过 Transformer decoder 与图像特征交互，直接输出一组预测。使用**匈牙利算法**做预测与 GT 的一对一匹配，完全去除了 anchor、NMS 等手工设计组件。

> 📖 Paper: Carion et al., [DETR](../../../.documents/papers/object_detection/carion_2020_detr.pdf), ECCV 2020

---

## 概念辨析

### Two-Stage vs One-Stage 检测器

| 维度 | Two-Stage | One-Stage |
|------|-----------|-----------|
| **本质** | 先提议候选区域，再对每个区域分类 + 精修 | 直接在特征图上密集预测 box + class |
| **代表** | R-CNN → Fast R-CNN → Faster R-CNN | YOLO → SSD → RetinaNet |
| **精度** | 通常更高，尤其在小物体上 | 早期较低，RetinaNet/YOLOv3+ 已追上 |
| **速度** | 较慢（两步计算） | 更快（一步到位） |
| **设计复杂度** | 较高（RPN + RoI Pooling + 两阶段损失） | 较低（单一网络 + 密集预测） |
| **典型应用** | 精度优先场景（医学影像、卫星图） | 速度优先场景（实时视频、自动驾驶） |

> 📖 Paper: Redmon et al., [YOLO](../../../.documents/papers/object_detection/redmon_2016_yolo.pdf), CVPR 2016, Section 1
> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015

### Anchor-Based vs Anchor-Free

| 维度 | Anchor-Based | Anchor-Free |
|------|-------------|-------------|
| **本质** | 在每个位置预设固定 anchor，预测偏移量 | 直接预测目标中心/角点/边距 |
| **代表** | Faster R-CNN, SSD, RetinaNet | FCOS, CenterNet, CornerNet |
| **超参数** | 需要调 anchor 大小、比例、数量 | 不需要 anchor 相关超参数 |
| **小物体** | 需要合理的 anchor 设计才能覆盖 | 天然不受 anchor 匹配问题影响 |
| **设计哲学** | "微调参考框" | "从零预测位置" |

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2

---

## 核心属性

### 信息架构

```
目标检测系统
├── 输入：RGB 图像 (H × W × 3)
├── Backbone：CNN/Transformer 特征提取
│   └── 输出：多尺度特征图 {C2, C3, C4, C5}
├── Neck：特征融合（如 FPN）
│   └── 输出：增强特征图 {P2, P3, P4, P5}
├── Head：分类 + 回归
│   ├── 分类分支：预测每个 anchor/位置的类别概率
│   └── 回归分支：预测 bbox 偏移 (δx, δy, δw, δh)
├── 后处理：NMS 去重
└── 输出：[{bbox, class, score}, ...]
```

### 适用场景 ✅

- 自动驾驶中的行人/车辆检测
- 安防监控中的异常物体检测
- 工业质检中的缺陷检测
- 医学影像中的病灶检测
- 零售场景中的商品识别

### 不适用场景 ❌

- 只需要知道"图里有没有猫"不需要位置 → 用图像分类
- 需要像素级轮廓而非矩形框 → 用实例分割
- 目标极度密集且互相遮挡（如细胞计数） → 用密度估计
- 非预定义类别的开放世界检测（早期方法） → 需要 Open-Vocabulary Detection

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 输入 | RGB 图像 | (800, 1333, 3) |
| 输出 | (bbox, class, score) 列表 | [([100,200,300,400], "car", 0.95)] |
| 评估指标 | mAP (mean Average Precision) | mAP@0.5 = 0.85 |
| IoU 阈值 | 判断预测正确的交并比阈值 | VOC: 0.5, COCO: 0.5:0.95 |
| 常见 Backbone | ResNet-50, ResNet-101, Swin-T | torchvision.models.resnet50 |
| 常见 Neck | FPN, PANet, BiFPN | torchvision FPN |
| NMS 阈值 | 两框 IoU 超过此值则删除低分框 | 0.5 (常用) |
| 典型数据集 | PASCAL VOC (20 类)、COCO (80 类) | COCO: 118k 训练图 |
