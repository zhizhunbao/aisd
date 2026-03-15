# 机器视觉 Machine Vision

> 名词总表 · 来源：Gonzalez《Digital Image Processing》· Szeliski《Computer Vision》· OpenCV 官方文档

---

### 图像基础 Image Fundamentals

| 名词 | 英文 |
|------|------|
| 像素 | Pixel |
| 分辨率 | Resolution |
| 灰度图像 | Grayscale Image |
| 彩色图像 | Color Image |
| 颜色空间 | Color Space (RGB / HSV / Lab / YCbCr) |
| 通道 | Channel |
| 位深度 | Bit Depth |
| 直方图 | Histogram |
| 图像坐标系 | Image Coordinate System |
| 采样与量化 | Sampling & Quantization |
| 空间分辨率 | Spatial Resolution |
| 灰度级分辨率 | Intensity Resolution |

---

### 图像增强 Image Enhancement

| 名词 | 英文 |
|------|------|
| 点运算 | Point Operations |
| 对比度拉伸 | Contrast Stretching |
| 直方图均衡化 | Histogram Equalization |
| 自适应直方图均衡化 | CLAHE (Adaptive Histogram Equalization) |
| 伽马校正 | Gamma Correction |
| 对数变换 | Log Transform |
| 图像反转 | Image Negation |
| 分段线性变换 | Piecewise Linear Transform |

---

### 空间滤波 Spatial Filtering

| 名词 | 英文 |
|------|------|
| 卷积 | Convolution |
| 相关 | Correlation |
| 均值滤波 | Mean Filter (Box Filter) |
| 高斯滤波 | Gaussian Filter |
| 中值滤波 | Median Filter |
| 双边滤波 | Bilateral Filter |
| 锐化 | Sharpening |
| 拉普拉斯算子 | Laplacian Operator |
| Sobel 算子 | Sobel Operator |
| Prewitt 算子 | Prewitt Operator |
| 非锐化掩蔽 | Unsharp Masking |

---

### 频域滤波 Frequency Domain Filtering

| 名词 | 英文 |
|------|------|
| 傅里叶变换 | Fourier Transform (DFT) |
| 频谱 | Frequency Spectrum |
| 低通滤波 | Low-Pass Filter |
| 高通滤波 | High-Pass Filter |
| 带通/带阻滤波 | Band-Pass / Band-Reject Filter |
| 理想滤波器 | Ideal Filter |
| 巴特沃斯滤波器 | Butterworth Filter |
| 高斯滤波器（频域） | Gaussian Filter (Frequency) |
| 逆傅里叶变换 | Inverse DFT (IDFT) |

---

### 边缘检测 Edge Detection

| 名词 | 英文 |
|------|------|
| 边缘 | Edge |
| 梯度 | Gradient |
| 梯度幅值 | Gradient Magnitude |
| 梯度方向 | Gradient Direction |
| Canny 边缘检测 | Canny Edge Detection |
| 非极大值抑制 | Non-Maximum Suppression |
| 双阈值 | Double Thresholding |
| 滞后阈值 | Hysteresis Thresholding |
| Scharr 算子 | Scharr Operator |
| LoG 算子 | Laplacian of Gaussian |
| 零交叉 | Zero Crossing |

---

### 图像分割 Image Segmentation

| 名词 | 英文 |
|------|------|
| 阈值分割 | Thresholding |
| Otsu 方法 | Otsu's Method |
| 自适应阈值 | Adaptive Thresholding |
| 区域生长 | Region Growing |
| 分水岭算法 | Watershed Algorithm |
| 轮廓检测 | Contour Detection |
| 连通域分析 | Connected Component Analysis |
| 语义分割 | [Semantic Segmentation](../deep-learning/) |
| GrabCut | GrabCut |
| 均值漂移 | Mean Shift |

---

### 形态学处理 Morphological Operations

| 名词 | 英文 |
|------|------|
| 结构元素 | Structuring Element |
| 腐蚀 | Erosion |
| 膨胀 | Dilation |
| 开运算 | Opening |
| 闭运算 | Closing |
| 形态梯度 | Morphological Gradient |
| 顶帽变换 | Top-Hat Transform |
| 底帽变换 | Bottom-Hat (Black-Hat) Transform |
| 骨架化 | Skeletonization |
| 重建 | Reconstruction |

---

### 特征提取 Feature Extraction

| 名词 | 英文 |
|------|------|
| 角点检测 | Corner Detection |
| Harris 角点 | Harris Corner |
| Shi-Tomasi 角点 | Shi-Tomasi (Good Features to Track) |
| SIFT | Scale-Invariant Feature Transform |
| SURF | Speeded Up Robust Features |
| ORB | Oriented FAST and Rotated BRIEF |
| FAST | Features from Accelerated Segment Test |
| BRIEF | Binary Robust Independent Elementary Features |
| 特征描述子 | Feature Descriptor |
| 关键点 | Keypoint |
| 尺度空间 | Scale Space |
| 高斯金字塔 | Gaussian Pyramid |
| 特征匹配 | Feature Matching |
| BFMatcher | Brute-Force Matcher |
| FLANN | Fast Library for Approximate Nearest Neighbors |
| 单应性矩阵 | Homography Matrix |
| RANSAC | Random Sample Consensus |

---

### 几何变换 Geometric Transformations

| 名词 | 英文 |
|------|------|
| 平移 | Translation |
| 旋转 | Rotation |
| 缩放 | Scaling |
| 仿射变换 | Affine Transformation |
| 透视变换 | Perspective Transformation |
| 插值 | Interpolation (Bilinear / Bicubic) |
| 图像配准 | Image Registration |
| 图像拼接 | Image Stitching |
| 畸变校正 | Distortion Correction |

---

### 相机模型与标定 Camera Model & Calibration

| 名词 | 英文 |
|------|------|
| 针孔模型 | Pinhole Camera Model |
| 内参矩阵 | Intrinsic Matrix |
| 外参矩阵 | Extrinsic Matrix |
| 焦距 | Focal Length |
| 主点 | Principal Point |
| 径向畸变 | Radial Distortion |
| 切向畸变 | Tangential Distortion |
| 相机标定 | Camera Calibration |
| 棋盘格标定 | Checkerboard Calibration |
| 立体视觉 | Stereo Vision |
| 视差图 | Disparity Map |
| 对极几何 | Epipolar Geometry |
| 基础矩阵 | Fundamental Matrix |
| 本质矩阵 | Essential Matrix |

---

### 目标检测与识别 Object Detection & Recognition

| 名词 | 英文 |
|------|------|
| 模板匹配 | Template Matching |
| 霍夫变换 | Hough Transform |
| 霍夫直线检测 | Hough Line Transform |
| 霍夫圆检测 | Hough Circle Transform |
| 级联分类器 | Cascade Classifier |
| Haar 特征 | Haar Features |
| HOG 特征 | Histogram of Oriented Gradients |
| 滑动窗口 | Sliding Window |
| 背景建模 | Background Modeling |
| 帧差法 | Frame Differencing |
| 光流 | Optical Flow |
| Lucas-Kanade | Lucas-Kanade Method |
| [深度学习检测](../deep-learning/) | Deep Learning-Based Detection |

---

### 工业视觉应用 Industrial Vision Applications

| 名词 | 英文 |
|------|------|
| 缺陷检测 | Defect Detection |
| 尺寸测量 | Dimensional Measurement |
| 字符识别 | OCR (Optical Character Recognition) |
| 条码 / 二维码识别 | Barcode / QR Code Recognition |
| 颜色分选 | Color Sorting |
| 表面检测 | Surface Inspection |
| 定位引导 | Vision-Guided Positioning |
| 视觉伺服 | Visual Servoing |
| 机器人抓取 | Robotic Grasping |
| 3D 视觉 | 3D Vision |
| 结构光 | Structured Light |
| 线扫描相机 | Line Scan Camera |
| 面阵相机 | Area Scan Camera |

---

### OpenCV 核心 API OpenCV Core API

| 名词 | 英文 |
|------|------|
| cv2.imread / imwrite | Image I/O |
| cv2.cvtColor | Color Space Conversion |
| cv2.GaussianBlur | Gaussian Blur |
| cv2.Canny | Canny Edge Detection |
| cv2.threshold | Thresholding |
| cv2.findContours | Contour Detection |
| cv2.drawContours | Contour Drawing |
| cv2.warpAffine | Affine Transformation |
| cv2.warpPerspective | Perspective Transformation |
| cv2.calibrateCamera | Camera Calibration |
| cv2.matchTemplate | Template Matching |
| cv2.HoughLines | Hough Line Detection |
| cv2.goodFeaturesToTrack | Feature Detection |
