---
topic: object_detection
dimension: history
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Viola & Jones, 'Rapid Object Detection using a Boosted Cascade', CVPR 2001 — https://doi.org/10.1109/CVPR.2001.990517"
  - "📖 Paper: Dalal & Triggs, 'HOG for Human Detection', CVPR 2005 — https://doi.org/10.1109/CVPR.2005.177"
  - "📖 Paper: Felzenszwalb et al., 'Object Detection with DPM', PAMI 2010 — https://doi.org/10.1109/TPAMI.2009.167"
  - "📖 Paper: Girshick et al., 'R-CNN', CVPR 2014 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/girshick_2014_rcnn.pdf"
  - "📖 Paper: Girshick, 'Fast R-CNN', ICCV 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/girshick_2015_fast_rcnn.pdf"
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
  - "📖 Paper: Redmon et al., 'YOLO', CVPR 2016 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/redmon_2016_yolo.pdf"
  - "📖 Paper: Liu et al., 'SSD', ECCV 2016 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/liu_2016_ssd.pdf"
  - "📖 Paper: Lin et al., 'FPN', CVPR 2017 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/lin_2017_fpn.pdf"
  - "📖 Paper: Carion et al., 'DETR', ECCV 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/carion_2020_detr.pdf"
expiry: never
status: current
---

# Object Detection 的故事线：从滑动窗口到 Transformer

> **核心主题：** 目标检测技术的每一次飞跃，都是在回答同一个问题——"如何更快、更准地找到图片中的物体"
> **故事线：** 从手工特征到深度学习、从两步走到一步到位、从工程技巧到端到端学习的三次范式革命

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 计算机如何像人一样，看一眼照片就知道里面有什么东西、在哪里？

20 世纪 90 年代末，计算机视觉领域面临一个巨大挑战：虽然已经有了一些图像分类的初步成果，但"找到物体在哪里"比"判断物体是什么"难得多——因为物体可以出现在任意位置、任意大小、任意角度，搜索空间是爆炸性的。

> 🔑 **问题提出：** 如何在一张图的海量位置和尺度中高效搜索物体？这个问题引出了第一代方法——滑动窗口。

---

## 📚 第一章：滑动窗口与手工特征（2001-2012）

> **关键人物：** Paul Viola, Michael Jones, Navneet Dalal, Bill Triggs, Pedro Felzenszwalb
> **关键论文：** Viola & Jones 2001, Dalal & Triggs 2005, Felzenszwalb et al. 2010

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Viola-Jones 人脸检测级联图 | 原论文 Figure | CVPR 2001 | 学术引用 |
| HOG 可视化特征 | 原论文 Figure | CVPR 2005 | 学术引用 |

### 发生了什么？

2001 年，Viola 和 Jones 发表了实时人脸检测方法：用 Haar-like 特征 + AdaBoost 级联分类器，在每个滑动窗口位置判断"是不是人脸"。这个方法首次实现了实时检测（15 FPS），被嵌入了几乎所有数码相机。

2005 年，Dalal 和 Triggs 提出了 HOG（方向梯度直方图），结合线性 SVM 实现行人检测。HOG 特征对光照变化鲁棒，精度远超 Haar 特征。

2010 年，Felzenszwalb 等人提出 DPM（可变形部件模型），用"根模型 + 部件模型"的思路处理物体的形变和遮挡，三次获得 PASCAL VOC 竞赛冠军。

### 为什么这很重要？

- Viola-Jones 证明了实时目标检测是可行的——这一点在 2001 年意义重大
- HOG+SVM 建立了"特征提取 + 分类器"的经典管线，成为后续十年的标准范式
- DPM 引入了"部件"概念，为后来的 attention 和 multi-scale 思路埋下种子

### 但还有一个问题……

手工设计的特征（Haar、HOG）表达能力有限，无法捕捉复杂的语义信息。而且滑动窗口方法需要在所有位置和尺度上密集搜索，计算量巨大。

> 🔑 **故事转折点：** 2012 年 AlexNet 在 ImageNet 上的突破证明——CNN 学到的特征比所有手工特征都好。如果把 CNN 用到检测上，会怎样？

---

## 📚 第二章：R-CNN 家族——让 CNN 做检测（2014-2015）

> **关键人物：** Ross Girshick, Jeff Donahue, Trevor Darrell, Jian Sun, Shaoqing Ren, Kaiming He
> **关键论文：** R-CNN (CVPR 2014), Fast R-CNN (ICCV 2015), Faster R-CNN (NeurIPS 2015)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Ross Girshick 肖像 | UC Berkeley / Meta AI | 大学官网 | 学术引用 |
| R-CNN 系统图 | 原论文 Figure 1 | `https://arxiv.org/abs/1311.2524` | 学术引用 |
| Faster R-CNN 架构图 | 原论文 Figure 2 | `https://arxiv.org/abs/1506.01497` | 学术引用 |

### 发生了什么？

**2014 年 R-CNN**：Girshick 的想法很直接——用 Selective Search 提取 ~2000 个候选区域，把每个区域缩放到固定大小送入 CNN 提取特征，再用 SVM 分类。简单粗暴但有效：在 PASCAL VOC 2012 上 mAP 从 34% 暴涨到 53%。

**2015 年 Fast R-CNN**：R-CNN 最大的问题是太慢——每张图要跑 2000 次 CNN。Girshick 的改进：先对整张图跑一次 CNN 得到特征图，然后用 RoI Pooling 从特征图上裁剪每个候选区域的特征。速度提升了 200 多倍。

**2015 年 Faster R-CNN**：Fast R-CNN 还有一个瓶颈——Selective Search 是外挂的手工方法。Ren、He 和 Girshick 提出 RPN（Region Proposal Network），用一个轻量 CNN 在特征图上生成候选区域，完全替代 Selective Search。至此，整个检测管线第一次实现了端到端训练。

### 为什么这很重要？

- R-CNN 证明了 CNN 特征在检测任务上远超手工特征——mAP 提升 56% 是碾压级
- Faster R-CNN 建立了 "Backbone + Neck + RPN + Head" 的标准架构，成为后续 5 年几乎所有检测器的基础
- "共享计算"思想（整张图跑一次 CNN，而非每个区域跑一次）成为效率优化的核心原则

### 但还有一个问题……

Faster R-CNN 虽然是当时最先进的方法，但 Two-Stage 管线仍然不够快——在 GPU 上只有 5-7 FPS，离实时应用还有距离。能不能把两步合成一步？

> 🔑 **故事转折点：** 如果不做候选区域提议，直接在特征图上预测框和类别，速度能快多少？

---

## 📚 第三章：YOLO 和 SSD——一步到位的革命（2016）

> **关键人物：** Joseph Redmon, Ali Farhadi, Wei Liu, Dragomir Anguelov, Christian Szegedy
> **关键论文：** YOLO (CVPR 2016), SSD (ECCV 2016)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Joseph Redmon 肖像 | 个人网站 pjreddie.com | `https://pjreddie.com` | 个人网站 |
| YOLO 系统图 | 原论文 Figure 1 | `https://arxiv.org/abs/1506.02640` | 学术引用 |
| SSD 多尺度检测图 | 原论文 Figure 2 | `https://arxiv.org/abs/1512.02325` | 学术引用 |

### 发生了什么？

**2016 年 YOLO**：Redmon 把目标检测重新定义为一个回归问题。把图像分成 S×S 网格，每个网格直接预测 B 个框和 C 个类别概率。一次前向传播就得到所有检测结果——"You Only Look Once"，达到 45 FPS。

**2016 年 SSD**：Liu 等人在 YOLO 的基础上做了关键改进——在多个尺度的特征图上做预测（而不是只在最后一层），这让 SSD 在保持 YOLO 速度优势的同时，大幅提升了小物体检测精度。

### 为什么这很重要？

- YOLO 开创了 One-Stage 检测范式，证明"检测 = 回归"是可行的
- SSD 的多尺度检测思路直接启发了后来的 FPN
- One-Stage 方法让实时目标检测成为现实，自动驾驶、安防监控等应用场景真正可落地

### 但还有一个问题……

早期 One-Stage 方法的精度明显低于 Faster R-CNN，尤其是在小物体和密集场景上。原因是 One-Stage 在高分辨率特征图上密集预测，正负样本比例极不平衡（1:1000），大量容易的背景样本主导了训练过程。

> 🔑 **故事转折点：** 一个简单的损失函数改动——Focal Loss——就解决了类别不平衡问题，让 One-Stage 方法的精度追上了 Two-Stage。

---

## 📚 第四章：FPN 与 Focal Loss——补齐短板（2017）

> **关键人物：** Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He
> **关键论文：** FPN (CVPR 2017), RetinaNet / Focal Loss (ICCV 2017)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| FPN 架构图 | 原论文 Figure 1 | `https://arxiv.org/abs/1612.03144` | 学术引用 |
| Focal Loss vs CE 曲线 | RetinaNet 原论文 Figure 1 | `https://arxiv.org/abs/1708.02002` | 学术引用 |

### 发生了什么？

**2017 年 FPN**：Lin 等人提出特征金字塔网络，通过自顶向下路径和横向连接，在所有尺度上构建语义丰富的特征图。FPN 成为几乎所有现代检测器的标配 Neck 结构。

**2017 年 Focal Loss / RetinaNet**：同样是 Lin 等人，分析发现 One-Stage 方法精度低的根因不是架构问题，而是**类别不平衡**。他们设计了 Focal Loss：给容易分类的样本降低权重，让网络专注于难样本。RetinaNet 使用 Focal Loss + FPN 的组合，首次让 One-Stage 方法在精度上追上甚至超过 Faster R-CNN。

### 为什么这很重要？

- FPN 优雅地解决了多尺度检测问题，成为行业标准
- Focal Loss 揭示了密集检测中类别不平衡的本质，一个损失函数的改动抵过复杂的架构设计
- RetinaNet 终结了"Two-Stage 更准、One-Stage 更快"的二分法

### 但还有一个问题……

即使有了 FPN 和 Focal Loss，检测器仍然依赖大量的手工设计组件：anchor 的大小 / 比例需要人工调优，NMS 阈值需要搜索，正负样本匹配策略需要精心设计。能不能让网络自己学会这些？

> 🔑 **故事转折点：** 2020 年 Transformer 登陆视觉领域，DETR 证明——可以彻底去除 anchor 和 NMS。

---

## 📚 第五章：DETR 与 Transformer——去除手工设计（2020-今）

> **关键人物：** Nicolas Carion, Francisco Massa, Alexander Kirillov
> **关键论文：** DETR (ECCV 2020)

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| DETR 架构图 | 原论文 Figure 2 | `https://arxiv.org/abs/2005.12872` | 学术引用 |

### 发生了什么？

**2020 年 DETR**：Carion 等人（来自 Facebook AI Research）做了一件颠覆性的事——把目标检测定义为**集合预测问题**。核心设计：100 个可学习的 object queries 通过 Transformer decoder 与图像特征交互，直接输出 100 个预测。预测与 GT 之间使用**匈牙利算法**做一对一匹配，不需要 anchor，不需要 NMS。

后续改进包括 Deformable DETR（加速训练收敛）、DINO（提升精度）和 RT-DETR（实时速度），Transformer 检测范式迅速成熟。

### 为什么这很重要？

- DETR 证明了 "端到端 = 更简洁"的设计哲学——去掉 anchor 和 NMS 后管线大幅简化
- Transformer 的全局注意力天然适合处理物体间的关系（如遮挡推理）
- 开启了检测领域从 CNN 到 Transformer 的范式转移

### 但还有一个问题……

DETR 训练非常慢（需要 500 epoch vs Faster R-CNN 的 36 epoch），且在小物体上表现不佳。这些问题正在被后续工作逐步解决。

> 🔑 **未来方向：** Open-Vocabulary Detection（检测训练时没见过的类别）、大语言模型与检测的融合（Grounding DINO）、3D 检测。

---

## 🗺️ 全局回顾：技术演进路线图

```
2001          2005           2010          2014         2015          2016         2017          2020         2023+
 │             │              │             │            │             │            │             │            │
 Viola-Jones   HOG+SVM        DPM           R-CNN        Faster R-CNN  YOLO/SSD     FPN/Focal     DETR         RT-DETR
 (Haar+Cascade)(手工特征巅峰)  (部件模型)     (CNN+检测)    (端到端)      (实时检测)   (多尺度/平衡)  (Transformer)  (实时Transformer)
 │                                          │                         │                          │
 └── 手工特征时代 ──────────────────────────── └── CNN Two-Stage ──────── └── CNN One-Stage ──────── └── Transformer ──→
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| 手工特征 → CNN 特征 | 特征表达能力不足 → 自动学习高级语义特征 |
| R-CNN → Fast R-CNN | 每个区域单独跑 CNN 太慢 → 共享计算，只跑一次 |
| Fast R-CNN → Faster R-CNN | Selective Search 是瓶颈 → RPN 端到端学习候选区域 |
| Two-Stage → One-Stage | 两步太慢 → 一步回归，实时检测 |
| 单尺度 → FPN | 小物体检测差 → 多尺度特征融合 |
| CE → Focal Loss | 正负样本不平衡 → 聚焦难样本 |
| Anchor-Based → DETR | 手工设计组件多 → 端到端集合预测 |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | Viola & Jones | — | CVPR 2001 原论文 | 学术引用 |
| 第一章 | Dalal & Triggs | — | CVPR 2005 原论文 | 学术引用 |
| 第二章 | Ross Girshick | UC Berkeley / Meta AI | arXiv: `1311.2524` | 学术引用 |
| 第二章 | Kaiming He | Meta AI | arXiv: `1506.01497` | 学术引用 |
| 第三章 | Joseph Redmon | pjreddie.com | arXiv: `1506.02640` | 个人网站 |
| 第四章 | Tsung-Yi Lin | Google Research | arXiv: `1612.03144` | 学术引用 |
| 第五章 | Nicolas Carion | FAIR | arXiv: `2005.12872` | 学术引用 |

> ⚠️ **素材查找优先级：**
> 1. **Wikimedia Commons** — 首选，多数科学家有公有领域肖像
> 2. **大学官网/档案馆** — 本校教授的官方照片
> 3. **论文首页截图** — arXiv / Google Scholar
>
> ❌ **禁止：** AI 生成肖像、库存图片网站、无版权标注的图片
