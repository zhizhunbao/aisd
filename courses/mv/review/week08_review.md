# Week 8 Review — Object Detection Fundamentals

> 📋 Based on instructor's revision topics:
> **Limitation of traditional object detection, Object detection vs classification, Detection head types, SSD vs YOLO, Challenges in object detection**

---

## Q1: What are the limitations of traditional object detection?

Traditional pipeline: **SIFT/HOG feature extraction → Sliding window → SVM classifier**

| Limitation | Description |
|---|---|
| **Handcrafted features** | Requires manually designed features (SIFT, HOG), limited adaptability |
| **Scale/orientation/lighting** | Traditional methods perform poorly under scale, orientation, and lighting changes |
| **Computational inefficiency** | Sliding window is computationally expensive on high-resolution images, not suitable for real-time |
| **Poor generalization** | Handcrafted features cannot generalize well across diverse scenarios |

**Deep learning solved this:** CNN automatically learns features from data, eliminating the need for manual design.

---

## Q2: What is the difference between object detection and image classification?

| Aspect | Classification | Detection |
|---|---|---|
| **Task** | Categorize the **whole image** | Identify **what + where** |
| **Output** | Probability distribution across classes | Class probabilities + **bounding box coordinates** + confidence scores |
| **Objects** | One label per image | **Multiple objects** per image |
| **Localization** | ❌ No | ✅ Yes |

---

## Q3: What are the two types of detection heads?

| Type | Representatives | Mechanism | Pros | Cons |
|---|---|---|---|---|
| **Anchor-based** | Faster R-CNN | Uses predefined anchor boxes (various sizes/aspect ratios) to generate region proposals | High accuracy, suitable for different shapes | Computationally intensive (many proposals) |
| **Anchor-free** | CornerNet, CenterNet | Directly predicts object corner points or center points | Simplified pipeline, reduced computation | More complex training strategies |

---

## Q4: SSD vs YOLO Comparison

| Aspect | SSD | YOLO |
|---|---|---|
| **Full name** | Single Shot MultiBox Detector | You Only Look Once |
| **Approach** | Multi-scale feature maps + default boxes (anchor boxes) | Divides image into grid, each cell directly predicts |
| **Speed** | Fast | **Very fast** |
| **Multi-scale** | ✅ Uses multiple feature maps | Single pass through grid |
| **Default boxes** | Uses anchor boxes at each cell | Grid cell predictions |
| **NMS** | ✅ Yes | ✅ Yes |

**Both are single-shot detectors** — no region proposals needed, enabling real-time detection.

### Architecture Comparison:

| Component | SSD | YOLO |
|---|---|---|
| **Spatial division** | Multi-scale feature maps | Grid division |
| **Box generation** | Default (anchor) boxes at each cell | Each grid cell predicts boxes directly |
| **Multi-scale** | ✅ Built-in (different feature maps) | ⚠️ YOLOv1-v2 single scale; **YOLOv3+ uses FPN** |
| **Prediction** | Offsets + class confidence | Boxes + confidence + class probability |
| **Post-processing** | NMS to filter overlapping boxes | NMS to keep most confident boxes |

---

## Q5: What is IoU?

**IoU (Intersection over Union)** — measures the overlap between predicted box and ground truth box.

| IoU Value | Interpretation |
|---|---|
| IoU > **0.5** | Acceptable |
| Higher IoU | Better prediction |
| IoU = 1.0 | Perfect overlap |

---

## Q6: What are the challenges in object detection?

| Challenge | Description |
|---|---|
| **Small/occluded objects** | Small or occluded objects are difficult to detect |
| **Complex backgrounds** | Diverse complex backgrounds cause interference |
| **Varying lighting** | Changing lighting conditions |
| **Precision vs Recall** | Balancing precision and recall (especially in crowded scenes) |
| **Computational resources** | Training and deploying complex models requires significant compute |

---

## Q7: R-CNN Family Evolution

| Model | Method | Speed |
|---|---|---|
| **R-CNN** | Selective Search → CNN per region | Slow |
| **Fast R-CNN** | Shared CNN features + RoI Pooling | Medium |
| **Faster R-CNN** | Region Proposal Network (RPN) | Fast |
| **SSD / YOLO** | Single-shot, no region proposals | **Real-time** |
