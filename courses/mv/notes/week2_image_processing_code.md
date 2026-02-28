# Week 2: 图像处理基础 — 代码参考 (Code Quick Reference)

> 🔧 See also: [概念速查](week2_image_processing_cheatsheet.md) | [数学公式](week2_image_processing_math.md)
> 📄 Source: slides + demo code + lab2

---

## 🔧 图像模糊/滤波 (Blurring/Filtering)

### 均值模糊 (Average Blur)

```python
# 均值模糊 — 所有权重相等 / Average blur — equal weights
blurred_avg = cv2.blur(img, ksize=(5, 5))
# ksize: 核大小，越大越模糊 / Kernel size, larger = more blur
```

### 高斯模糊 (Gaussian Blur)

```python
# 高斯模糊 — 中心权重大 / Gaussian blur — center-weighted
blurred_gauss = cv2.GaussianBlur(img, ksize=(5, 5), sigmaX=0)
# sigmaX=0: 从ksize自动计算sigma / Auto-compute sigma from ksize
```

### 中值模糊 (Median Blur)

```python
# 中值模糊 — 取中位数，对椒盐噪声效果最好
# Median blur — takes median, best for salt-and-pepper noise
blurred_median = cv2.medianBlur(img, ksize=5)
# ⚠️ ksize 必须是奇数 / ksize must be odd
```

### 双边滤波 (Bilateral Filter)

```python
# 双边滤波 — 去噪同时保边 / Bilateral — denoise while preserving edges
blurred_bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
# d: 邻域直径 / Neighborhood diameter
# sigmaColor: 颜色相似性范围 / Color similarity range
# sigmaSpace: 空间接近度范围 / Spatial proximity range
```

### 自定义核卷积 (Custom Kernel Convolution)

```python
# 自定义核 / Custom kernel
kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]], dtype=np.float32) / 9.0

filtered = cv2.filter2D(img, ddepth=-1, kernel=kernel)
# ddepth=-1: 输出与输入相同深度 / Output same depth as input
```

---

## 🔧 图像锐化 (Sharpening)

```python
# 锐化核 / Sharpening kernel
sharpen_kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)

sharpened = cv2.filter2D(img, -1, sharpen_kernel)
```

---

## 🔧 边缘检测 (Edge Detection)

### Canny 边缘检测

```python
# Canny 边缘检测 — 5步自动完成 / Canny — 5-step pipeline
edges = cv2.Canny(img_gray, threshold1=50, threshold2=150)
# threshold1: 低阈值 (弱边缘下限) / Low threshold
# threshold2: 高阈值 (强边缘下限) / High threshold
# ⚠️ 输入必须是灰度图! / Input must be grayscale!
```

### Sobel 梯度

```python
# Sobel 梯度 / Sobel gradient
sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, dx=1, dy=0, ksize=3)  # 水平
sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, dx=0, dy=1, ksize=3)  # 垂直

# 梯度幅值 / Gradient magnitude
magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
magnitude = np.uint8(np.clip(magnitude, 0, 255))
```

---

## 🔧 直方图 (Histogram)

### 计算与绘制直方图

```python
# 计算直方图 / Calculate histogram
hist = cv2.calcHist([img_gray], channels=[0], mask=None,
                    histSize=[256], ranges=[0, 256])
# channels: 通道索引 / Channel index
# histSize: bin 数量 / Number of bins
# ranges: 像素值范围 / Pixel value range

# 用 matplotlib 绘制 / Plot with matplotlib
plt.plot(hist, color='gray')
plt.xlabel('Pixel Value (0-255)')
plt.ylabel('Pixel Count')
plt.title('Image Histogram')
plt.show()
```

### 直方图均衡化

```python
# 全局直方图均衡化 — 增强对比度
# Global histogram equalization — enhance contrast
equalized = cv2.equalizeHist(img_gray)
# ⚠️ 输入必须是灰度图! / Input must be grayscale!

# CLAHE — 局部自适应均衡化（更好）
# CLAHE — locally adaptive equalization (better)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_result = clahe.apply(img_gray)
```

---

## 🔧 阈值化 (Thresholding)

### 简单阈值

```python
# 简单阈值 / Simple threshold
ret, binary = cv2.threshold(img_gray, thresh=127, maxval=255,
                            type=cv2.THRESH_BINARY)
# ret: 使用的阈值 / Threshold used
# binary: 二值化结果 / Binary result

# 反转二值化 / Inverted binary
ret, binary_inv = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
```

### 自适应阈值

```python
# 自适应阈值 — 局部计算阈值 / Adaptive — local threshold
adaptive = cv2.adaptiveThreshold(
    img_gray,
    maxValue=255,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # 或 MEAN_C
    thresholdType=cv2.THRESH_BINARY,
    blockSize=11,     # 邻域大小（必须奇数）/ Block size (must be odd)
    C=2               # 从均值减去的常数 / Constant subtracted from mean
)
```

### Otsu 自动阈值

```python
# Otsu — 自动从直方图找最优阈值 / Auto-find optimal threshold
ret, otsu = cv2.threshold(img_gray, 0, 255,
                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# ⚠️ thresh参数设为0，由Otsu自动计算 / thresh=0, Otsu auto-computes
print(f"Otsu's threshold: {ret}")
```

---

## 🔧 形态学操作 (Morphological Operations)

```python
# 创建结构元素/核 / Create structuring element/kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# 形状选项: MORPH_RECT, MORPH_CROSS, MORPH_ELLIPSE

# 腐蚀 — 缩小白色区域 / Erosion — shrink white regions
eroded = cv2.erode(binary, kernel, iterations=1)

# 膨胀 — 扩大白色区域 / Dilation — expand white regions
dilated = cv2.dilate(binary, kernel, iterations=1)

# 开运算 — 先腐蚀后膨胀（去白噪点）
# Opening — erosion then dilation (remove white noise)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# 闭运算 — 先膨胀后腐蚀（填黑孔洞）
# Closing — dilation then erosion (fill black holes)
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

---

## 🔧 基本图像操作 (Basic Manipulations)

### 缩放 (Resize)

```python
# 缩放 / Resize
resized = cv2.resize(img, dsize=(new_width, new_height))
# 或使用缩放因子 / Or use scale factor
resized = cv2.resize(img, None, fx=0.5, fy=0.5)  # 缩小一半
```

### 裁剪 (Crop)

```python
# 裁剪 — 用 NumPy 切片 / Crop — use NumPy slicing
# ⚠️ 注意 [y1:y2, x1:x2] 不是 [x1:x2, y1:y2]!
cropped = img[y1:y2, x1:x2]
```

### 旋转 (Rotate)

```python
# 旋转 / Rotate
(h, w) = img.shape[:2]
center = (w // 2, h // 2)

# 获取旋转矩阵 / Get rotation matrix
M = cv2.getRotationMatrix2D(center, angle=45, scale=1.0)
# angle: 逆时针角度 / Counter-clockwise degrees

# 应用旋转 / Apply rotation
rotated = cv2.warpAffine(img, M, (w, h))
```

### 仿射变换 (Affine Transform)

```python
# 通用仿射变换 / General affine transform
# 需要3对对应点 / Needs 3 pairs of corresponding points
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

M = cv2.getAffineTransform(pts1, pts2)
warped = cv2.warpAffine(img, M, (w, h))
```

---

## ⚠️ 常见代码错误

| #   | 错误                                                  | 正确                           | 说明                     |
| --- | ----------------------------------------------------- | ------------------------------ | ------------------------ |
| 1   | `cv2.Canny(img_bgr, ...)`                             | `cv2.Canny(img_gray, ...)`     | Canny 输入必须是灰度图   |
| 2   | `cv2.medianBlur(img, 4)`                              | `cv2.medianBlur(img, 5)`       | ksize 必须是**奇数**     |
| 3   | `cv2.morphologyEx(img, cv2.MORPH_OPEN, ...)` 期待填孔 | 用 `MORPH_CLOSE` 填孔          | OPEN 去噪点, CLOSE 填孔  |
| 4   | `cv2.threshold(img_bgr, ...)`                         | `cv2.threshold(img_gray, ...)` | 阈值化输入必须是灰度图   |
| 5   | 裁剪用 `img[x1:x2, y1:y2]`                            | `img[y1:y2, x1:x2]`            | NumPy 是 [行,列] = [y,x] |
| 6   | `cv2.equalizeHist(img_bgr)`                           | `cv2.equalizeHist(img_gray)`   | 均衡化只支持灰度图       |

---

## 🔗 相关文件

- 📖 [概念速查](week2_image_processing_cheatsheet.md) — 定义、要点、陷阱
- 📐 [数学公式](week2_image_processing_math.md) — 公式与手算题
- 💻 [完整 Demo](week2_image_processing_complete_demo.py) — 可运行的完整演示脚本
