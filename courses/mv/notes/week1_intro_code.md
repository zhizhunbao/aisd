# Week 1: 机器视觉导论 — 代码参考 (Code Quick Reference)

> 🔧 See also: [概念速查](week1_intro_cheatsheet.md) | [数学公式](week1_intro_math.md)
> 📄 Source: slides + demo code + lab1

---

## 🔧 环境与导入

```python
# 核心库导入 / Core imports
import numpy as np               # 数值计算 / Numerical computation
import cv2                        # OpenCV — 图像处理 / Image processing
import matplotlib.pyplot as plt   # 可视化 / Visualization
from matplotlib.colors import hsv_to_rgb  # HSV→RGB转换 / Color conversion
```

---

## 🔧 图像读取与显示

### 读取图像 (Read Image)

```python
# OpenCV 读取图像（默认 BGR 顺序）
# Read image with OpenCV (default: BGR order)
img_bgr = cv2.imread('image.jpg')            # 彩色图 / Color
img_gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)  # 灰度图 / Grayscale

# 检查是否读取成功 / Check if read successfully
if img_bgr is None:
    print("Error: Image not found!")
```

### BGR ↔ RGB 转换 (Color Conversion)

```python
# ⚠️ OpenCV 默认 BGR，matplotlib 需要 RGB
# ⚠️ OpenCV uses BGR, matplotlib needs RGB
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# BGR → HSV
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# BGR → 灰度 / BGR → Grayscale
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
```

### 用 Matplotlib 显示 (Display with Matplotlib)

```python
# 显示彩色图（必须先转 RGB！）
# Display color image (must convert to RGB first!)
plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
plt.title("Color Image")
plt.axis('off')
plt.show()

# 显示灰度图（需指定 cmap='gray'）
# Display grayscale (must set cmap='gray')
plt.imshow(img_gray, cmap='gray')
plt.title("Grayscale Image")
plt.axis('off')
plt.show()
```

---

## 🔧 像素操作

### 访问像素 (Access Pixel)

```python
# ⚠️ 注意：OpenCV 用 [y, x]（行, 列），不是 [x, y]!
# ⚠️ Note: OpenCV uses [y, x] (row, col), NOT [x, y]!

# 灰度图 — 单个值 / Grayscale — single value
pixel_value = img_gray[100, 200]  # y=100, x=200

# 彩色图 — BGR 三元组 / Color — BGR tuple
b, g, r = img_bgr[100, 200]      # y=100, x=200
```

### 修改像素 (Modify Pixel)

```python
# 设置单个像素为白色 / Set pixel to white
img_gray[100, 200] = 255                    # 灰度
img_bgr[100, 200] = [255, 255, 255]         # BGR — 白色

# 设置区域为红色 / Set region to red (BGR order!)
img_bgr[0:50, 0:50] = [0, 0, 255]           # BGR: B=0, G=0, R=255
```

### 图像属性 (Image Properties)

```python
print(f"Shape: {img_bgr.shape}")     # (Height, Width, Channels) 例: (480, 640, 3)
print(f"Size: {img_bgr.size}")       # 总像素数×通道数 例: 921600
print(f"Dtype: {img_bgr.dtype}")     # 数据类型 例: uint8
print(f"H×W: {img_bgr.shape[0]}×{img_bgr.shape[1]}")  # 高×宽
```

---

## 🔧 图像创建

### 用 NumPy 创建图像 (Create with NumPy)

```python
# 创建黑色图像 / Create black image
black = np.zeros((480, 640, 3), dtype=np.uint8)

# 创建白色图像 / Create white image
white = np.ones((480, 640, 3), dtype=np.uint8) * 255

# 创建灰度渐变 / Create grayscale gradient
gradient = np.tile(np.arange(256, dtype=np.uint8), (100, 1))  # 100行×256列

# 创建 RGB 彩色方块 / Create RGB color patch
red_patch = np.zeros((100, 100, 3), dtype=np.uint8)
red_patch[:, :, 2] = 255  # BGR 中 R 是通道 2 / R is channel 2 in BGR
```

---

## 🔧 色彩空间操作

### RGB ↔ HSV (Color Space Conversion)

```python
# BGR → HSV
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
# ⚠️ OpenCV 中 H: 0-179, S: 0-255, V: 0-255
# ⚠️ In OpenCV: H: 0-179, S: 0-255, V: 0-255

# 分离 HSV 通道 / Split HSV channels
h, s, v = cv2.split(hsv)

# 基于颜色的物体检测（例：检测红色）
# Color-based detection (e.g., detect red)
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)
result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
```

### 通道分离与合并 (Split & Merge)

```python
# 分离 BGR 通道 / Split BGR channels
b, g, r = cv2.split(img_bgr)

# 合并通道 / Merge channels
merged = cv2.merge([b, g, r])

# 可视化单通道（用彩色映射）
# Visualize single channel (with color map)
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, ch, name in zip(axes, [r, g, b], ['Red', 'Green', 'Blue']):
    ax.imshow(ch, cmap='gray')
    ax.set_title(name)
    ax.axis('off')
plt.show()
```

---

## 🔧 图像保存

```python
# 保存图像 / Save image
cv2.imwrite('output.jpg', img_bgr)              # JPEG（有损）
cv2.imwrite('output.png', img_bgr)              # PNG（无损）
cv2.imwrite('output.jpg', img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])  # JPEG 质量参数
```

---

## 🔧 常用可视化模式

### 并排对比 (Side-by-Side Comparison)

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(img_rgb)
axes[0].set_title("Original")
axes[0].axis('off')

axes[1].imshow(processed_rgb)
axes[1].set_title("Processed")
axes[1].axis('off')

plt.tight_layout()
plt.show()
```

### 矩阵数值可视化 (Matrix Value Visualization)

```python
# 显示小矩阵的数值和图像
# Display both values and image for a small matrix
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# 左：数值表格 / Left: value table
axes[0].imshow(small_gray, cmap='gray', vmin=0, vmax=255)
for i in range(small_gray.shape[0]):
    for j in range(small_gray.shape[1]):
        axes[0].text(j, i, str(small_gray[i, j]),
                     ha='center', va='center', fontsize=8)

# 右：渲染图 / Right: rendered image
axes[1].imshow(small_gray, cmap='gray', vmin=0, vmax=255)
```

---

## ⚠️ 常见代码错误

| #   | 错误                        | 正确                                                   | 说明                         |
| --- | --------------------------- | ------------------------------------------------------ | ---------------------------- |
| 1   | `img[x, y]`                 | `img[y, x]`                                            | OpenCV 用 (行, 列) 即 (y, x) |
| 2   | `plt.imshow(img_bgr)`       | `plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))` | 必须转 RGB 再显示            |
| 3   | `img_bgr[:,:,0]` 认为是 Red | `img_bgr[:,:,0]` 是 **Blue**                           | BGR 顺序: B=0, G=1, R=2      |
| 4   | HSV 的 H 范围 0-360         | OpenCV 中 H 范围 **0-179**                             | 因为 uint8 最大 255          |
| 5   | 灰度图 `plt.imshow(gray)`   | `plt.imshow(gray, cmap='gray')`                        | 不指定 cmap 会用彩色映射     |

---

## 🔗 相关文件

- 📖 [概念速查](week1_intro_cheatsheet.md) — 定义、要点、陷阱
- 📐 [数学公式](week1_intro_math.md) — 公式与手算题
- 💻 [完整 Demo](week1_intro_complete_demo.py) — 可运行的完整演示脚本
