---
topic: object_detection
dimension: pitfalls
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
  - "📖 Paper: Lin et al., 'Focal Loss (RetinaNet)', ICCV 2017 — https://arxiv.org/abs/1708.02002"
  - "📖 Docs: torchvision Detection — https://pytorch.org/vision/stable/models.html#object-detection"
  - "🧪 经验: 目标检测模型训练与调试常见问题"
expiry: 6m
status: current
---

# Object Detection 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: IoU 和 mAP 到底怎么算

**痛点类别：** 概念理解类 — "看了公式但不知道怎么用"

**场景：** 初学者计算 mAP 时把所有类别的预测框混在一起排序，得到的结果远低于预期。

**症状：** mAP 值异常低（如 0.01），但从可视化来看检测效果还不错。

**根因：** mAP 必须**逐类别**计算 AP 再取均值，不能把不同类别混在一起算。每个类别有自己独立的 Precision-Recall 曲线。

**解法：**

❌ 错误做法 — 把所有类别的预测混在一起排序

```python
# 错误：所有类别混在一起
all_preds = sorted(all_preds, key=lambda x: x["score"], reverse=True)
ap = compute_ap(all_preds, all_gts)  # 这不是 mAP！
```

✅ 正确做法 — 逐类别计算 AP 再取均值

```python
# 正确：每个类别单独算 AP
aps = []
for class_id in range(num_classes):
    class_preds = [p for p in all_preds if p["class"] == class_id]
    class_gts = [g for g in all_gts if g["class"] == class_id]
    ap = compute_ap(class_preds, class_gts, iou_threshold=0.5)
    aps.append(ap)
mAP = sum(aps) / len(aps)
```

**教训：** mAP 的 "mean" 是对**类别**取均值，不是对所有预测取均值。

> 📖 Docs: [COCO Detection Evaluation](https://cocodataset.org/#detection-eval)

---

## 坑 2: NMS 阈值选错导致漏检或重复检测

**痛点类别：** 代码调参类 — "参数选错效果天差地别"

**场景：** 使用 NMS 后处理时，不知道 IoU 阈值该设多少。

**症状：** 阈值设太低（如 0.3）→ 同一物体只保留一个框但相邻物体被误删；阈值设太高（如 0.9）→ 同一物体保留多个重复框。

**根因：** NMS 的 IoU 阈值决定"多重叠的框才算是同一个物体的重复检测"。太低误删相邻物体，太高不能去重。

**解法：**

❌ 错误做法 — 使用极端阈值

```python
# 错误：阈值太低，密集场景下相邻物体被误删
keep = torchvision.ops.nms(boxes, scores, iou_threshold=0.2)

# 错误：阈值太高，同一物体有多个框
keep = torchvision.ops.nms(boxes, scores, iou_threshold=0.9)
```

✅ 正确做法 — 使用标准阈值 + 针对场景微调

```python
# 推荐：标准阈值 0.5，密集场景可适当提高
keep = torchvision.ops.nms(boxes, scores, iou_threshold=0.5)

# 如果场景密集（人群、车流），可以尝试 0.6-0.7
# 或者使用 Soft-NMS 避免硬删除
from torchvision.ops import batched_nms
keep = batched_nms(boxes, scores, labels, iou_threshold=0.5)  # 按类别分别 NMS
```

**教训：** NMS 阈值 0.5 是一个好的起点。密集场景用 Soft-NMS 或按类别分别做 NMS。

> 📖 Paper: Ren et al., [Faster R-CNN](../../../.documents/papers/object_detection/ren_2015_faster_rcnn.pdf), NeurIPS 2015

---

## 坑 3: 训练时 loss 为 NaN 或不收敛

**痛点类别：** 代码调试类 — "程序能跑但结果全错"

**场景：** 自定义数据集微调 Faster R-CNN / YOLO，loss 从第一个 epoch 就是 NaN，或 loss 始终在很高的值震荡不下降。

**症状：** loss = NaN / loss 不下降 / 模型输出全是乱框

**根因：** (1) 标注坐标格式错误（如把 (x, y, w, h) 当成 (x1, y1, x2, y2)），(2) 学习率太大，(3) bbox 坐标超出图片范围，(4) 标注中有面积为 0 的框。

**解法：**

❌ 错误做法 — 不做数据验证直接训练

```python
# 错误：不检查标注格式
target = {"boxes": torch.tensor(annotations["bbox"]), "labels": torch.tensor(labels)}
# 如果 bbox 格式是 (x, y, w, h) 但模型期望 (x1, y1, x2, y2)，会训练失败
```

✅ 正确做法 — 训练前验证标注数据

```python
# 正确：先验证标注数据
def validate_annotations(boxes, labels, img_w, img_h):
    """训练前检查标注数据 / Validate annotations before training"""
    assert boxes.shape[1] == 4, "boxes 需要 4 列 / boxes need 4 columns"
    assert (boxes[:, 2] > boxes[:, 0]).all(), "x2 必须 > x1 / x2 must > x1"
    assert (boxes[:, 3] > boxes[:, 1]).all(), "y2 必须 > y1 / y2 must > y1"
    assert (boxes[:, 0] >= 0).all(), "x1 不能为负 / x1 must >= 0"
    assert (boxes[:, 2] <= img_w).all(), f"x2 不能超过图片宽 {img_w} / x2 must <= {img_w}"
    assert (boxes[:, 3] <= img_h).all(), f"y2 不能超过图片高 {img_h} / y2 must <= {img_h}"
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    assert (areas > 0).all(), "框面积不能为 0 / Box area must > 0"

# COCO 格式 (x, y, w, h) → torchvision 格式 (x1, y1, x2, y2)
def coco_to_xyxy(bbox):
    x, y, w, h = bbox
    return [x, y, x + w, y + h]
```

**教训：** 数据验证放在训练循环之前。90% 的训练失败来自标注格式问题。

> 📖 Docs: [torchvision Detection Fine-Tuning](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)

---

## 坑 4: 小物体检测精度极低

**痛点类别：** 概念理解类 — "知道结果不好但不知道为什么"

**场景：** 在 COCO 数据集上训练好的检测器，AP_small（面积 < 32²）远低于 AP_large。

**症状：** 大物体检测正常（AP_large > 0.5），但小物体几乎漏检（AP_small < 0.1）。

**根因：** 深层特征图（如 C5）的空间分辨率很低（原图的 1/32），小物体在这个尺度上只有 1-2 个像素的特征，信息不足以支撑检测。

**解法：**

❌ 错误做法 — 只用最高层特征做检测

```python
# 错误：只用 C5 特征做检测
features = backbone(image)["layer4"]  # C5, stride=32
predictions = head(features)  # 小物体在这里基本看不见
```

✅ 正确做法 — 使用 FPN 多尺度检测

```python
# 正确：使用 FPN，在多个尺度上检测
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2

# FPN 自动构建 P2-P5 多尺度特征
model = fasterrcnn_resnet50_fpn_v2(weights="DEFAULT")
# P2 (stride=4) → 检测小物体
# P3 (stride=8) → 检测中等物体
# P4 (stride=16) → 检测中大物体
# P5 (stride=32) → 检测大物体

# 额外技巧：提高输入分辨率
model = fasterrcnn_resnet50_fpn_v2(
    weights="DEFAULT",
    min_size=1024,  # 提高最短边，让小物体更大
    max_size=2048,
)
```

**教训：** 小物体检测三板斧：(1) FPN 多尺度特征，(2) 提高输入分辨率，(3) 在小尺度特征图上用更密集的 anchor。

> 📖 Paper: Lin et al., [FPN](../../../.documents/papers/object_detection/lin_2017_fpn.pdf), CVPR 2017

---

## 坑 5: 混淆 "检测" 和 "分类" 的评估指标

**痛点类别：** 概念理解类 — "概念看着像，分不清区别"

**场景：** 用分类指标（准确率 Accuracy）评估检测模型效果，数值看起来很高但实际效果很差。

**症状：** Accuracy 显示 99% 但可视化发现大量漏检。

**根因：** 检测器的绝大多数预测是"背景"（负样本），如果用 Accuracy 评估，即使模型把一切都预测为背景，Accuracy 也会很高（因为背景确实占绝大多数）。检测必须用 mAP 评估。

**解法：**

❌ 错误做法 — 用分类的 Accuracy 评估检测器

```python
# 错误：用 Accuracy
correct = (pred_labels == gt_labels).sum()
accuracy = correct / total  # 99%，但全是背景贡献的
```

✅ 正确做法 — 用 mAP 评估

```python
# 正确：用 COCO 评估工具
from pycocotools.cocoeval import COCOeval

coco_eval = COCOeval(coco_gt, coco_dt, "bbox")
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()
# 输出 mAP@[.5:.95], mAP@.5, mAP@.75, AP_small, AP_medium, AP_large
```

**教训：** 检测用 mAP，分类用 Accuracy/F1。用错指标会得出完全错误的结论。

> 📖 Docs: [COCO Detection Evaluation](https://cocodataset.org/#detection-eval)

---

## 超级避坑指南

### 学习避坑

1. [ ] **先跑推理再学原理** → 先用 `torchvision` 或 `ultralytics` 跑一个推理 demo，看到框了再学理论
2. [ ] **搞清三种框** → Anchor (预设参考框) ≠ Proposal (RPN 输出) ≠ Prediction (最终输出)
3. [ ] **理解 mAP 的 "mean"** → 是对类别取均值，不是对所有预测取均值
4. [ ] **两大范式先搞清** → Two-Stage (Faster R-CNN) 和 One-Stage (YOLO) 是两条路线
5. [ ] **NMS 不是可选的** → 几乎所有传统检测器都需要 NMS，只有 DETR 不需要

### 作业/项目避坑

1. [ ] **标注格式确认** → torchvision 用 (x1,y1,x2,y2)，YOLO 用 (cx,cy,w,h) 归一化，COCO 用 (x,y,w,h)
2. [ ] **先验证数据再训练** → 检查 bbox 是否超出图片范围、面积是否为 0
3. [ ] **Backbone 用预训练权重** → 从头训 CNN 需要海量数据，目标检测通常用 ImageNet 预训练的 backbone
4. [ ] **学习率从小开始** → 微调时 lr=0.001-0.005，不要用分类任务的 lr=0.1

### 考试/答辩避坑

1. [ ] **被问 Anchor 回到设计目的** → "用预设框把绝对坐标预测简化为相对偏移预测，降低学习难度"
2. [ ] **被问 NMS 讲四步** → 排序→取最高→删重叠→重复
3. [ ] **被问 mAP 分三步** → 逐类别→P-R 曲线→取面积→类别均值

### 调试清单（技术类）

1. [ ] **Loss = NaN？** → 检查 bbox 坐标是否合法（x2>x1, y2>y1, 不超出图片）
2. [ ] **mAP 极低？** → 检查标注格式是否和模型匹配（xyxy vs xywh）
3. [ ] **小物体漏检？** → 是否使用了 FPN？输入分辨率够不够？
4. [ ] **检测重复框？** → NMS 阈值是否合理？是否对每个类别分别做 NMS？
5. [ ] **训练不收敛？** → 学习率是否太大？数据增强是否过度？
