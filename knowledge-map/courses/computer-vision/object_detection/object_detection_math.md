---
topic: object_detection
dimension: math
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Szeliski, 《Computer Vision: Algorithms and Applications》 2nd Ed. Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/szeliski_cv.pdf"
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
  - "📖 Paper: Redmon et al., 'YOLO', CVPR 2016 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/redmon_2016_yolo.pdf"
  - "📖 Paper: Lin et al., 'Focal Loss for Dense Object Detection (RetinaNet)', ICCV 2017 — https://arxiv.org/abs/1708.02002"
expiry: 12m
status: current
---

# Object Detection 数学基础

> 📚 Book: Szeliski, [《Computer Vision: Algorithms and Applications》](../../../textbooks/szeliski_cv.pdf), Ch.6
> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $B^{pred}$ | 预测框 | Predicted bounding box | $(x, y, w, h) \in \mathbb{R}^4$ |
| $B^{gt}$ | 真实标注框 | Ground truth box | $(x, y, w, h) \in \mathbb{R}^4$ |
| $A$ | 锚框 | Anchor box | 预设的参考框 |
| $t_x, t_y, t_w, t_h$ | 预测的偏移量 | Predicted offsets | $\mathbb{R}$ |
| $t_x^*, t_y^*, t_w^*, t_h^*$ | 真实的偏移量（训练目标） | Target offsets | $\mathbb{R}$ |
| $p_i$ | 第 i 个 anchor 的物体概率 | Objectness probability | $[0, 1]$ |
| $p_i^*$ | 第 i 个 anchor 的 GT 标签 | Ground truth label | $\{0, 1\}$ |
| $\text{IoU}$ | 交并比 | Intersection over Union | $[0, 1]$ |
| $\text{AP}$ | 单类平均精度 | Average Precision | $[0, 1]$ |
| $\text{mAP}$ | 所有类别 AP 均值 | Mean Average Precision | $[0, 1]$ |
| $\lambda$ | 分类与回归损失的平衡系数 | Balancing weight | $\mathbb{R}^+$ |
| $\alpha_t$ | Focal Loss 类别权重 | Class-balancing weight | $[0, 1]$ |
| $\gamma$ | Focal Loss 聚焦参数 | Focusing parameter | $\mathbb{R}^+$, 通常 2 |

> 📚 Book: Szeliski, [《CV》](../../../textbooks/szeliski_cv.pdf), Ch.6.2

---

## 核心公式

### 公式 1: IoU（交并比）

**直觉：** 两个框重叠面积占它们合并面积的比例，越大说明越重合。

$$
\text{IoU}(B^{pred}, B^{gt}) = \frac{|B^{pred} \cap B^{gt}|}{|B^{pred} \cup B^{gt}|} = \frac{\text{交集面积}}{\text{并集面积}}
$$

> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $B^{pred} \cap B^{gt}$ | 两框重叠区域面积 | 两个矩形交集 |
| $B^{pred} \cup B^{gt}$ | 两框合并区域面积 | 交集 + 各自独有部分 |

**推导过程：**

给定两个框 $B_1 = (x_1^{min}, y_1^{min}, x_1^{max}, y_1^{max})$ 和 $B_2 = (x_2^{min}, y_2^{min}, x_2^{max}, y_2^{max})$：

1. 交集左上角：$(x_{inter}^{min}, y_{inter}^{min}) = (\max(x_1^{min}, x_2^{min}), \max(y_1^{min}, y_2^{min}))$
2. 交集右下角：$(x_{inter}^{max}, y_{inter}^{max}) = (\min(x_1^{max}, x_2^{max}), \min(y_1^{max}, y_2^{max}))$
3. 交集面积：$A_{inter} = \max(0, x_{inter}^{max} - x_{inter}^{min}) \times \max(0, y_{inter}^{max} - y_{inter}^{min})$
4. 并集面积：$A_{union} = A_1 + A_2 - A_{inter}$
5. IoU = $A_{inter} / A_{union}$

> 📖 Paper: Girshick et al., [R-CNN](../../../.documents/papers/object_detection/girshick_2014_rcnn.pdf), CVPR 2014

### 公式 2: Bounding Box 回归（偏移量参数化）

**直觉：** 不直接预测框坐标，而是预测"锚框需要平移和缩放多少"，这让学习目标更小、更稳定。

$$
t_x = \frac{x - x_a}{w_a}, \quad t_y = \frac{y - y_a}{h_a}, \quad t_w = \ln\frac{w}{w_a}, \quad t_h = \ln\frac{h}{h_a}
$$

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015, Eq. (1)-(4)

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $(x, y, w, h)$ | 预测框中心坐标和宽高 | 模型输出 |
| $(x_a, y_a, w_a, h_a)$ | 锚框中心坐标和宽高 | 预设值 |
| $t_x, t_y$ | 中心点偏移（归一化） | 相对 anchor 宽高的比例 |
| $t_w, t_h$ | 尺度缩放（对数空间） | 用 ln 防止负宽高 |

**推导过程：**

1. **为什么不直接预测 $(x, y, w, h)$？** → 不同大小的物体坐标值差异巨大（小物体 x=50，大物体 x=500），直接回归让网络难以学习
2. **为什么用相对偏移？** → 归一化到 anchor 的尺度后，学习目标变为"偏移几个 anchor 宽度"，量级一致
3. **为什么宽高用 log？** → 宽高必须为正数，$w = w_a \cdot e^{t_w}$ 保证了 $w > 0$；log 让 0.5 倍缩小和 2 倍放大的回归目标对称

**从偏移还原到坐标：**

$$
x = t_x \cdot w_a + x_a, \quad y = t_y \cdot h_a + y_a, \quad w = w_a \cdot e^{t_w}, \quad h = h_a \cdot e^{t_h}
$$

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015

### 公式 3: Faster R-CNN 多任务损失

**直觉：** 检测器同时做两件事（分类 + 定位），所以损失函数也是两部分之和。

$$
L(\{p_i\}, \{t_i\}) = \frac{1}{N_{cls}} \sum_i L_{cls}(p_i, p_i^*) + \lambda \frac{1}{N_{reg}} \sum_i p_i^* \cdot L_{reg}(t_i, t_i^*)
$$

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015, Eq. (1)

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $L_{cls}$ | 分类损失（交叉熵） | "这个 anchor 是物体还是背景" |
| $L_{reg}$ | 回归损失（Smooth L1） | "框偏移量离真实值多远" |
| $p_i^*$ | GT 标签（只有正样本才算回归损失） | 1 = 正样本，0 = 负样本 |
| $N_{cls}$ | mini-batch 大小 | 256 |
| $N_{reg}$ | anchor 位置数 | ~2400 |
| $\lambda$ | 平衡系数 | 10（使两项量级相当） |

**推导过程：**

1. **分类损失**：$L_{cls}(p_i, p_i^*) = -[p_i^* \log p_i + (1 - p_i^*) \log(1 - p_i)]$（二分类交叉熵）
2. **回归损失**：$L_{reg} = \text{Smooth}_{L1}(t_i - t_i^*)$，只对正样本 ($p_i^* = 1$) 计算
3. **Smooth L1**：

$$
\text{Smooth}_{L1}(x) = \begin{cases} 0.5x^2 & \text{if } |x| < 1 \\ |x| - 0.5 & \text{otherwise} \end{cases}
$$

4. **为什么用 Smooth L1 不用 L2？** → L2 对大偏差的梯度太大容易梯度爆炸，Smooth L1 对大偏差只有线性梯度更稳定

> 📖 Paper: Girshick, [Fast R-CNN](../../../.documents/papers/object_detection/girshick_2015_fast_rcnn.pdf), ICCV 2015

### 公式 4: Focal Loss

**直觉：** 密集检测器中绝大多数是容易分类的背景（负样本），它们虽然单个损失小但数量压倒性地多，会淹没有意义的前景损失。Focal Loss 给容易样本降权，让网络专注于难样本。

$$
FL(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)
$$

> 📖 Paper: Lin et al., Focal Loss (RetinaNet), ICCV 2017

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $p_t$ | 正确类别的预测概率 | 正样本取 $p$，负样本取 $1-p$ |
| $\gamma$ | 聚焦参数，越大越聚焦难样本 | $\gamma = 2$（论文最佳） |
| $\alpha_t$ | 类别平衡权重 | $\alpha = 0.25$ |
| $(1-p_t)^\gamma$ | 调制因子：易样本 $p_t$ 大，此项趋近 0 | 让易样本损失接近 0 |

**推导过程：**

1. 标准交叉熵：$CE(p_t) = -\log(p_t)$
2. 加入调制因子：$FL(p_t) = -(1-p_t)^\gamma \log(p_t)$
3. 当 $p_t = 0.9$（容易样本）：$(1-0.9)^2 = 0.01$，损失缩小 100 倍
4. 当 $p_t = 0.1$（困难样本）：$(1-0.1)^2 = 0.81$，损失基本不变
5. 加入 $\alpha_t$ 平衡正负样本数量

> 📖 Paper: Lin et al., Focal Loss (RetinaNet), ICCV 2017

---

## 公式关系图

```
IoU (交并比)
  │
  ├──→ NMS 后处理（IoU 阈值判断是否抑制）
  ├──→ Anchor 匹配（IoU > 0.7 = 正样本，IoU < 0.3 = 负样本）
  └──→ mAP 评估（IoU 阈值判断 TP/FP）

BBox 回归参数化 (tx, ty, tw, th)
  │
  └──→ 多任务损失 L_reg（Smooth L1 Loss）
         │
         └──→ Faster R-CNN 总损失 = L_cls + λ·L_reg

交叉熵损失
  │
  ├──→ 多任务损失 L_cls
  └──→ Focal Loss（加调制因子 → RetinaNet）
```

---

## 手算练习

### 练习 1: 计算 IoU

**题目：** 框 A = (100, 100, 300, 300)，框 B = (200, 200, 400, 400)，坐标格式为 (x_min, y_min, x_max, y_max)。计算 IoU。

**解答步骤：**

1. 交集左上角 = (max(100,200), max(100,200)) = (200, 200)
2. 交集右下角 = (min(300,400), min(300,400)) = (300, 300)
3. 交集面积 = (300-200) × (300-200) = 100 × 100 = **10000**
4. 框 A 面积 = (300-100) × (300-100) = 200 × 200 = 40000
5. 框 B 面积 = (400-200) × (400-200) = 200 × 200 = 40000
6. 并集面积 = 40000 + 40000 - 10000 = **70000**
7. IoU = 10000 / 70000 = **1/7 ≈ 0.143**

### 练习 2: BBox 偏移编码

**题目：** Anchor = (50, 50, 100, 80)（中心 x, y, 宽, 高），GT bbox = (60, 55, 120, 90)。计算偏移量 $(t_x, t_y, t_w, t_h)$。

**解答步骤：**

1. $t_x = (60 - 50) / 100 = 0.1$
2. $t_y = (55 - 50) / 80 = 0.0625$
3. $t_w = \ln(120 / 100) = \ln(1.2) ≈ 0.182$
4. $t_h = \ln(90 / 80) = \ln(1.125) ≈ 0.118$

### 练习 3: Focal Loss vs Cross-Entropy

**题目：** 一个容易的背景样本 $p_t = 0.9$，一个困难的前景样本 $p_t = 0.2$，$\gamma = 2$。比较 Focal Loss 和 Cross-Entropy 对两者的损失大小。

**解答步骤：**

1. 容易样本 CE = $-\log(0.9) ≈ 0.105$，FL = $(1-0.9)^2 \times 0.105 = 0.01 \times 0.105 ≈ 0.00105$
2. 困难样本 CE = $-\log(0.2) ≈ 1.609$，FL = $(1-0.2)^2 \times 1.609 = 0.64 \times 1.609 ≈ 1.030$
3. **CE 比值** = 1.609 / 0.105 ≈ **15.3 倍**
4. **FL 比值** = 1.030 / 0.00105 ≈ **981 倍** → Focal Loss 让难样本的相对重要性增加了 ~64 倍

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| IoU | $\frac{\|A \cap B\|}{\|A \cup B\|}$ | 框重叠度量、NMS、mAP 评估 | — |
| BBox 偏移 | $t_x = (x - x_a)/w_a$ | Anchor 到预测框的参数化 | — |
| BBox 解码 | $x = t_x \cdot w_a + x_a$ | 偏移量还原为坐标 | BBox 偏移 |
| Smooth L1 | $0.5x^2$ if $\|x\|<1$ else $\|x\|-0.5$ | 回归损失 | — |
| 多任务损失 | $L_{cls} + \lambda L_{reg}$ | Faster R-CNN 训练目标 | Smooth L1, CE |
| Focal Loss | $-\alpha_t(1-p_t)^\gamma \log(p_t)$ | 解决类别不平衡 | CE |
| AP | P-R 曲线下面积 | 单类评估 | IoU |
| mAP | $\frac{1}{C}\sum_{c=1}^C AP_c$ | 多类评估 | AP |
