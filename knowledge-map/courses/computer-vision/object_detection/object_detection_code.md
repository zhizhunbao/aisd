---
topic: object_detection
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: torchvision Object Detection — https://pytorch.org/vision/stable/models.html#object-detection"
  - "📖 Docs: torchvision Faster R-CNN — https://pytorch.org/vision/stable/models/faster_rcnn.html"
  - "📖 Docs: Ultralytics YOLOv8 — https://docs.ultralytics.com/"
  - "📖 Paper: Ren et al., 'Faster R-CNN', NeurIPS 2015 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/object_detection/ren_2015_faster_rcnn.pdf"
expiry: 6m
status: current
---

# Object Detection 代码参考

> 📖 Docs: [torchvision Object Detection](https://pytorch.org/vision/stable/models.html#object-detection)
> 📖 Docs: [Ultralytics YOLOv8](https://docs.ultralytics.com/)

## 快速开始

### 最简示例 — 30 秒上手 Faster R-CNN 推理

```python
# ============================================================
# Faster R-CNN 推理示例 / Faster R-CNN Inference Example
# 用 torchvision 预训练模型对任意图片做目标检测
# ============================================================
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.io import read_image
from PIL import Image

# 加载预训练模型 / Load pretrained model
weights = FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1
model = fasterrcnn_resnet50_fpn_v2(weights=weights)
model.eval()  # 推理模式 / Inference mode

# 准备图片 / Prepare image
img = read_image("test.jpg")  # 读取图片为 tensor / Read image as tensor
preprocess = weights.transforms()  # 获取预处理 / Get preprocessing
batch = [preprocess(img)]  # 预处理 + 组成 batch / Preprocess + batch

# 推理 / Inference
with torch.no_grad():
    predictions = model(batch)

# 结果解析 / Parse results
pred = predictions[0]
# pred["boxes"]  → (N, 4) 检测框坐标 / Detection box coordinates
# pred["labels"] → (N,)   类别编号 / Category indices
# pred["scores"] → (N,)   置信度分数 / Confidence scores

# 过滤低置信度 / Filter low confidence
keep = pred["scores"] > 0.5
boxes = pred["boxes"][keep]
labels = pred["labels"][keep]
scores = pred["scores"][keep]

# 可视化 / Visualization
categories = weights.meta["categories"]
label_names = [f"{categories[l]}: {s:.2f}" for l, s in zip(labels, scores)]
result = draw_bounding_boxes(img, boxes, label_names, width=3)
Image.fromarray(result.permute(1, 2, 0).numpy()).save("result.jpg")

print(f"检测到 {len(boxes)} 个目标 / Detected {len(boxes)} objects")
```

**测试方法：** 用 `python detect.py` 运行，会在当前目录生成 `result.jpg`，打开查看检测框。

> 📖 Docs: [torchvision Faster R-CNN Tutorial](https://pytorch.org/vision/stable/models/faster_rcnn.html)

---

## 完整实现示例

### 示例 1: 使用 Ultralytics YOLOv8 检测

```python
# ============================================================
# 1. 安装与导入 / Installation & Import
# pip install ultralytics
# ============================================================
from ultralytics import YOLO

# ============================================================
# 2. 加载预训练模型 / Load Pretrained Model
# yolov8n = nano (最快), yolov8s = small, yolov8m = medium
# yolov8l = large, yolov8x = extra-large (最准)
# ============================================================
model = YOLO("yolov8n.pt")  # 自动下载预训练权重 / Auto-download weights

# ============================================================
# 3. 单张图片推理 / Single Image Inference
# ============================================================
results = model("test.jpg")  # 推理 / Inference
for result in results:
    boxes = result.boxes  # 检测框 / Detection boxes
    print(f"检测到 {len(boxes)} 个目标 / Detected {len(boxes)} objects")
    for box in boxes:
        cls_id = int(box.cls)          # 类别编号 / Class index
        conf = float(box.conf)         # 置信度 / Confidence
        xyxy = box.xyxy[0].tolist()    # (x1, y1, x2, y2) 坐标 / Coordinates
        cls_name = model.names[cls_id] # 类别名 / Class name
        print(f"  {cls_name}: {conf:.2f} at [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")

# ============================================================
# 4. 保存可视化结果 / Save Visualization
# ============================================================
results[0].save("result_yolo.jpg")  # 保存带标注的图片 / Save annotated image

# ============================================================
# 5. 视频推理 / Video Inference
# ============================================================
results = model("video.mp4", stream=True)  # stream=True 节省内存 / Save memory
for result in results:
    annotated = result.plot()  # 获取带标注的帧 / Get annotated frame
```

### 示例 2: 在 COCO 数据集上微调 Faster R-CNN

```python
# ============================================================
# 1. 数据集准备 / Dataset Preparation
# ============================================================
import torch
from torch.utils.data import DataLoader
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

# ============================================================
# 2. 自定义数据集 / Custom Dataset
# 每张图返回 image (Tensor) 和 target (dict)
# target = {"boxes": (N,4), "labels": (N,), "image_id": int}
# ============================================================
class CustomDetectionDataset(torch.utils.data.Dataset):
    def __init__(self, images, annotations, transforms=None):
        self.images = images       # 图片路径列表 / Image path list
        self.annotations = annotations  # 标注列表 / Annotation list
        self.transforms = transforms

    def __getitem__(self, idx):
        # 读取图片 / Read image
        img = read_image(self.images[idx]).float() / 255.0

        # 构建 target / Build target
        ann = self.annotations[idx]
        target = {
            "boxes": torch.tensor(ann["boxes"], dtype=torch.float32),   # (N, 4) xyxy
            "labels": torch.tensor(ann["labels"], dtype=torch.int64),   # (N,)
        }

        if self.transforms:
            img = self.transforms(img)

        return img, target

    def __len__(self):
        return len(self.images)

# ============================================================
# 3. 模型定义 / Model Definition
# 替换检测头适配自定义类别数
# ============================================================
def get_model(num_classes):
    # 加载预训练模型 / Load pretrained model
    model = fasterrcnn_resnet50_fpn_v2(weights="DEFAULT")

    # 替换分类头 / Replace classification head
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model

# ============================================================
# 4. 训练循环 / Training Loop
# ============================================================
def train_one_epoch(model, data_loader, optimizer, device):
    model.train()
    total_loss = 0
    for images, targets in data_loader:
        # 移到 GPU / Move to GPU
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        # 前向传播，自动计算损失 / Forward, auto compute loss
        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())

        # 反向传播 / Backward
        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        total_loss += losses.item()

    return total_loss / len(data_loader)

# ============================================================
# 5. 主程序 / Main
# ============================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = 3  # 背景 + 2 个自定义类 / Background + 2 custom classes

model = get_model(num_classes).to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

for epoch in range(10):
    loss = train_one_epoch(model, train_loader, optimizer, device)
    lr_scheduler.step()
    print(f"Epoch {epoch}: loss = {loss:.4f}")

# 保存模型 / Save model
torch.save(model.state_dict(), "fasterrcnn_custom.pth")
```

> 📖 Docs: [torchvision Detection Fine-Tuning](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)

---

## API 速查

### torchvision.models.detection

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `fasterrcnn_resnet50_fpn_v2()` | `weights` | `None` | 预训练的 Faster R-CNN |
| ↳ `num_classes` | `int` | 91 (COCO) | 类别数（含背景） |
| ↳ `min_size` | `int` | 800 | 输入图片最短边 |
| ↳ `max_size` | `int` | 1333 | 输入图片最长边 |
| `model(images)` | `List[Tensor]` | — | 推理模式：返回预测 |
| `model(images, targets)` | `List[Tensor], List[Dict]` | — | 训练模式：返回 loss_dict |
| `FastRCNNPredictor(in_ch, num_cls)` | `int, int` | — | 替换检测头 |

### torchvision.ops

| 函数 | 参数 | 默认值 | 说明 |
|------|------|--------|------|
| `nms(boxes, scores, iou_threshold)` | `Tensor, Tensor, float` | — | 非极大值抑制 |
| `box_iou(boxes1, boxes2)` | `Tensor, Tensor` | — | 计算 IoU 矩阵 |
| `roi_align(input, boxes, output_size)` | `Tensor, List[Tensor], Tuple` | — | RoI Align |
| `generalized_box_iou(boxes1, boxes2)` | `Tensor, Tensor` | — | GIoU |

### Ultralytics YOLO

| 函数 | 参数 | 默认值 | 说明 |
|------|------|--------|------|
| `YOLO(model)` | `str` | — | 加载模型 (yolov8n/s/m/l/x) |
| `model(source)` | `str/ndarray/Tensor` | — | 推理 |
| `model.train(data, epochs)` | `str, int` | — | 训练 |
| `model.val()` | — | — | 验证 |
| `model.export(format)` | `str` | — | 导出 (onnx/tflite/coreml) |

---

## 目录结构模板

### 简单结构

```
detection-project/
├── detect.py              ← 推理脚本 / Inference script
├── data/
│   ├── images/            ← 测试图片 / Test images
│   └── labels/            ← 标注文件 / Annotation files
└── results/               ← 输出结果 / Output results
```

### 标准结构

```
detection-project/
├── configs/
│   └── default.yaml       ← 超参数配置 / Hyperparameter config
├── data/
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── val/
│   │   ├── images/
│   │   └── labels/
│   └── data.yaml          ← 数据集定义 / Dataset definition
├── models/
│   └── detector.py        ← 模型定义 / Model definition
├── utils/
│   ├── dataset.py         ← 数据加载 / Data loading
│   ├── transforms.py      ← 数据增强 / Data augmentation
│   └── metrics.py         ← 评估指标 / Evaluation metrics
├── train.py               ← 训练脚本 / Training script
├── evaluate.py            ← 评估脚本 / Evaluation script
├── detect.py              ← 推理脚本 / Inference script
├── checkpoints/           ← 模型权重 / Model weights
└── logs/                  ← 训练日志 / Training logs
```
