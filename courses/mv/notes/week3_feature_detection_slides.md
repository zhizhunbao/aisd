# Week 3: 特征检测与描述 (Feature Detection and Description)

> Source: `Week. 3-Object_Feature Detection and Description.pptx`
> Total slides: 28
> Instructor: Stephin Rachel Thomas | 29-01-2026

---

## 1. 分割与二值图像 (Segmentation and Binary Images)

### 1.1 概念 (Concepts)

- **Segmentation** extracts objects from image for further processing
- Output is typically a **binary image** — values of 0 and 1 (black and white)
- 1 = the piece of image we want, 0 = everything else
- Binary image acts as a mask for the source image area
- **Thresholding** is a typical way to get a binary image — compares pixel values against a central value

![Picture 5](week3_feature_detection_slides_images/slide03_img1.png)
![Picture 3](week3_feature_detection_slides_images/slide04_img1.png)

> **📝 笔记:**
>
> **分割与二值图像:**
>
> - 分割 = 从图像中提取感兴趣对象, 输出为二值图像 (0和1)
> - 二值图像是许多算法的关键输入, 充当掩码 (mask) 的角色
> - 阈值化是获得二值图像最常用的方法

### 1.2 自适应阈值化 (Adaptive Thresholding)

- Binary thresholding is not ideal for uneven lighting
- **Adaptive thresholding** uses local neighborhood to determine threshold, counteracting uneven lighting
- Calculates threshold for each sub-region instead of the whole image
- Methods: `adaptive_mean` or `adaptive_gaussian`

> **📝 笔记:**
>
> **自适应阈值:** 解决光照不均问题, 为每个子区域计算独立阈值。方法: 均值法或高斯法。

---

## 2. 轮廓检测 (Contours)

### 2.1 轮廓概念 (Introduction to Contours)

- A **contour** is a curve joining points enclosing an area of same color/intensity
- Similar to edge detection but requires edges to form a **closed path**
- Defines boundaries of objects, useful for shape analysis, object detection and recognition
- Binary image (segmentation output) is used as input for contour detection (pre-processing)

![Picture 3](week3_feature_detection_slides_images/slide08_img1.png)

> **📝 笔记:**
>
> **轮廓 vs 边缘:** 边缘不一定封闭, 轮廓必须是封闭路径。轮廓检测的输入是二值图像。

### 2.2 OpenCV 轮廓函数 (Contour Functions)

- `cv2.findContours()` — Returns:
  - **Contours:** List of contours, each is a vector of boundary points
  - **Hierarchy:** Parent-child relationship information
- `cv2.drawContours()` — Draws contour outlines (thickness≥0) or fills area (thickness<0)

![Picture 7](week3_feature_detection_slides_images/slide09_img1.jpg)
![Picture 11](week3_feature_detection_slides_images/slide10_img1.png)

> **📝 笔记:**
>
> **关键函数:**
>
> - `findContours()`: 找轮廓, 返回轮廓列表和层级关系
> - `drawContours()`: 画轮廓, thickness≥0 画边线, <0 填充区域

---

## 3. 特征检测简介 (Introduction to Feature Detection)

### 3.1 定义与类型 (Definition)

- **Feature Detection:** Process of identifying and locating significant structures or patterns within an image
- Crucial for object recognition, motion tracking, and image classification
- Feature types: **Edges** (sharp intensity changes), **Corners** (intersection of two edges), **Blobs** (regions of similar texture/color), **Ridges** (lines of high intensity)

![Picture 4](week3_feature_detection_slides_images/slide11_img1.jpg)

> **📝 笔记:**
>
> **特征检测:** 识别和定位图像中的重要结构。四种特征类型: 边缘、角点、斑块、脊线。

### 3.2 图像梯度 (Image Gradient)

- Gradients measure **directional changes** in intensity or color
- Fundamental for identifying features
- Measure of change in Image function F(x,y) in X or Y direction
- Color changes = magnitude, arrows = direction

![Picture 2](week3_feature_detection_slides_images/slide13_img1.png)
![Picture 3](week3_feature_detection_slides_images/slide14_img1.png)
![Picture 9](week3_feature_detection_slides_images/slide14_img2.png)

> **📝 笔记:**
>
> **图像梯度:** 图像函数 F(x,y) 在 X/Y 方向的变化量。颜色变化=幅值, 箭头=方向。梯度是特征检测的数学基础。

---

## 4. SIFT 算法 (Scale-Invariant Feature Transform)

SIFT identifies and describes local features. Invariant to scaling, rotation, and partially invariant to illumination and 3D viewpoint. Detects corners, circles, blobs etc.

**Five steps:**

1. **Scale-space Extrema Detection** — Detect keypoints by searching local extrema in Difference of Gaussian (DoG) images across multiple scales (octaves)
2. **Keypoint Localization** — Refine keypoints by eliminating low-contrast points and edge points
3. **Orientation Assignment** — Assign orientations based on local gradient directions → rotation invariance
4. **Keypoint Descriptor Generation** — Region around keypoint divided into blocks, gradient orientation histograms computed → 128-dimensional feature vector
5. **Feature Matching (Optional)** — Compare descriptors using distance metrics (Euclidean distance)

![Picture 4](week3_feature_detection_slides_images/slide15_img1.png)
![Picture 7](week3_feature_detection_slides_images/slide16_img1.png)
![Picture 7](week3_feature_detection_slides_images/slide17_img1.png)

> **📝 笔记:**
>
> **SIFT 五步:**
>
> - 尺度空间极值检测(DoG) → 关键点定位(去低对比/边缘点) → 方向分配(旋转不变性) → 描述符生成(128维向量) → 特征匹配(欧氏距离)
>
> **💡 提示:** SIFT 的核心优势是对尺度和旋转不变, 但计算较慢

---

## 5. SURF 算法 (Speeded Up Robust Features)

- Faster alternative to SIFT, robust to scale, rotation, and illumination changes
- Uses integral images for faster convolutions, fewer features while maintaining accuracy
- More suitable for **real-time** applications

**Steps:**

1. **Interest Point Detection:** Hessian matrix-based detector, faster due to integral images and box filters
2. **Scale-space Representation:** Multi-scale feature detection (like SIFT)
3. **Orientation Assignment:** Haar wavelet responses, dominant orientation for rotation invariance
4. **Descriptor Generation:** 4×4 subregions with Haar wavelet responses → **64-dimensional** descriptor (vs SIFT's 128)

![Picture 6](week3_feature_detection_slides_images/slide18_img1.jpg)

> **📝 笔记:**
>
> **SURF vs SIFT:** SURF 更快 (积分图+盒式滤波器), 描述符 64 维 (SIFT 128 维), 更适合实时应用。

---

## 6. ORB 与高级技术 (ORB and Advanced Techniques)

**ORB (Oriented FAST and Rotated BRIEF):**

- Fusion of FAST keypoint detector and BRIEF descriptor
- **FAST** — Features from Accelerated Segment Test (intensity-based, fast)
- **BRIEF** — Binary Robust Independent Elementary Features (binary descriptors for efficient matching)
- `cv2.ORB_create()` — OpenCV function
- **Deep Learning** approaches (CNNs) surpass traditional methods in accuracy and robustness

![Picture 4](week3_feature_detection_slides_images/slide21_img1.png)

> **📝 笔记:**
>
> **ORB:** FAST(快速检测关键点) + BRIEF(二进制描述符) 的结合, 开源免费, 效率高。深度学习正在超越传统方法。

---

## 7. 特征描述符 (Feature Descriptors)

### HOG (Histogram of Oriented Gradients)

- Provides unique, robust representation of detected features
- Particularly effective for **human detection**
- Plots pixel orientations and gradients on histogram
- Analyzes gradients in localized image portions
- Applications: pedestrian detection in autonomous vehicles and surveillance

![Picture 4](week3_feature_detection_slides_images/slide22_img1.png)
![Picture 3](week3_feature_detection_slides_images/slide23_img1.png)

> **📝 笔记:**
>
> **HOG:** 在图像局部区域分析梯度方向, 生成方向直方图。特别适用于行人检测(自动驾驶/监控)。

---

## 8. 机器学习与特征检测 (Machine Learning in Feature Detection)

ML algorithms enhance feature detection accuracy and efficiency:

1. **Supervised learning:** Uses labeled data (e.g., Email Spam detection)
2. **Unsupervised learning:** Pattern discovery without labels (e.g., Customer Segmentation)
3. **Semi-supervised learning:** Combines both (e.g., Google Photos)

![Picture 2](week3_feature_detection_slides_images/slide25_img1.jpg)

> **📝 笔记:**
>
> **三种学习方式:** 监督(有标签)、无监督(无标签)、半监督(混合)。ML 提升了特征检测的精度和效率。

---

## 9. 实时特征检测 (Real-Time Feature Detection)

Challenges: balancing computation with accuracy (video surveillance, autonomous driving)

Common remedies:

- Algorithm optimizations
- Low-level programming languages (not Python)
- Hardware acceleration (GPUs and TPUs)

![Picture 4](week3_feature_detection_slides_images/slide26_img1.jpg)

> **📝 笔记:**
>
> **实时检测挑战:** 速度 vs 精度的平衡。解决方案: 算法优化、低级语言、GPU/TPU硬件加速。

---

## 10. 未来趋势 (Future Trends)

- Deep learning enhances capability to automatically and accurately detect features
- Departure from traditional handcrafted algorithms
- Enabling smarter systems that adapt and improve over time

---

## 11. 下周预告 (Next Week)

- Introduction to CNN
- Architecture of CNN
- How CNN resolves common computer vision problems

---
