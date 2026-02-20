# Signal Processing Concepts (信号处理概念)

---

### Convolution (卷积)

**Tags:** `#signal-processing` `#filtering` `#mv-week2`

**📌 One-line Definition:**
> Convolution is a mathematical operation that slides a small matrix (kernel) across an image, computing a weighted sum at each position to produce a new output image.
>> 卷积是一种数学运算，将一个小矩阵（核）在图像上滑动，在每个位置计算加权和，生成新的输出图像。

**📐 Formula:**
```
output(x,y) = Σᵢ Σⱼ input(x+i, y+j) × kernel(i,j)
```
- output(x,y) = the new pixel value at position (x,y)
- input(x+i, y+j) = neighboring pixel value at offset (i,j)
- kernel(i,j) = weight at offset (i,j) in the kernel
- Σᵢ Σⱼ = sum over all kernel positions (e.g., 3×3 → 9 positions)
- Note: this is technically **correlation**. True convolution flips the kernel 180°, but OpenCV and CNNs use correlation.

**💡 Intuition (直觉理解):**
> Imagine you have a magnifying glass with colored zones (the kernel). You place it over each spot in a photo. Each zone has a number saying "how much do I care about this pixel?" You multiply each pixel by its zone's number, add them all up, and that's your new pixel value. Slide the magnifying glass to the next spot and repeat.
>
> **Key insight:** Convolution = "look at neighbors, take a weighted vote, and replace the pixel with the vote result."
>> 想象你有一个带有彩色区域的放大镜（核）。你把它放在照片的每个位置上。每个区域有一个数字说"我多在乎这个像素？"你把每个像素乘以其区域的数字，全部加起来，这就是你的新像素值。将放大镜滑到下一个位置，重复。
>>
>> **关键理解：** 卷积 = "看邻居，做加权投票，用投票结果替换像素。"

**🔢 Worked Example:**
```
Image region (3×3):        Kernel (averaging):
[10, 20, 30]               [1/9, 1/9, 1/9]
[40, 50, 60]               [1/9, 1/9, 1/9]
[70, 80, 90]               [1/9, 1/9, 1/9]

output = (10+20+30+40+50+60+70+80+90) / 9 = 450/9 = 50
→ The center pixel (50) stays 50 because all values are symmetric around it.
```

**⚙️ In Practice (实际使用):**
```python
import cv2
import numpy as np

# Define a custom kernel
kernel = np.ones((3,3), dtype=np.float32) / 9  # averaging kernel

# Apply convolution
output = cv2.filter2D(img, -1, kernel)
```

**🔗 Related Concepts:**
→ see: Gaussian Filter, Sobel Kernel, Kernel/Filter

**📚 Appears In:**
- MV Week 2 §4 (Image Filtering)
- MV Week 2 §8 (Canny Edge Detection — Stage 2)

---

### Gaussian Filter / Gaussian Blur (高斯滤波 / 高斯模糊)

**Tags:** `#signal-processing` `#filtering` `#noise-reduction` `#mv-week2`

**📌 One-line Definition:**
> A Gaussian filter is a convolution kernel whose weights follow a bell-curve (Gaussian distribution) — center pixels get the highest weight, farther pixels get exponentially less.
>> 高斯滤波器是一个权重遵循钟形曲线（高斯分布）的卷积核 — 中心像素权重最高，越远的像素权重指数递减。

**📐 Formula:**
```
G(x,y) = (1 / 2πσ²) × e^(-(x² + y²) / 2σ²)
```
- G(x,y) = weight at offset (x,y) from kernel center
- σ (sigma) = standard deviation — controls blur strength
  - σ = 1: gentle blur
  - σ = 3: strong blur
  - σ = 5: very strong blur
- π ≈ 3.14159
- e ≈ 2.71828
- (x² + y²) = squared distance from kernel center — farther = smaller weight
- **Rule of thumb:** kernel size ≈ 6σ + 1 (captures 99.7% of the Gaussian)

**💡 Intuition (直觉理解):**
> Think of dropping an ink drop on wet paper. The ink is darkest at the center and gradually fades out — that's the Gaussian shape. When blurring an image, each pixel "asks its neighbors for opinions" but trusts **nearby neighbors more** (high weight) and **distant neighbors less** (low weight). This produces a natural-looking blur without the harsh box-like artifacts of an averaging filter.
>
> **Why Gaussian instead of uniform averaging?**
> - Uniform average: every neighbor votes equally → creates "boxy" artifacts at edges
> - Gaussian: nearby votes count more → smooth, natural transition → no ringing artifacts
>> 想象在湿纸上滴一滴墨水。墨水在中心最浓，逐渐向外淡化 — 这就是高斯形状。模糊图像时，每个像素"向邻居征求意见"，但更信任**近邻**（高权重），不太信任**远邻**（低权重）。这产生自然的模糊，没有均值滤波器的方块状伪影。
>>
>> **为什么用高斯而不是均匀平均？**
>> - 均匀平均：所有邻居投票权相同 → 在边缘产生"方块"伪影
>> - 高斯：近邻投票权更大 → 平滑自然过渡 → 无振铃伪影

**🔢 Worked Example:**
```
σ = 1, 3×3 Gaussian kernel (approximate):

[0.075, 0.124, 0.075]    Center (0,0): e^0 = 1.0 → highest
[0.124, 0.204, 0.124]    Edge (1,0):   e^(-0.5) ≈ 0.607
[0.075, 0.124, 0.075]    Corner (1,1): e^(-1) ≈ 0.368

All weights sum to 1.0 (normalized) → true weighted average.

For pixel with neighbors:
[100, 100, 100]
[100, 200, 100]    ← center pixel is bright spike (noise?)
[100, 100, 100]

output = 0.075×100×4 + 0.124×100×4 + 0.204×200
       = 30 + 49.6 + 40.8 = 120.4

→ The noisy spike (200) is smoothed down to ~120. Noise reduced!
```

**⚙️ In Practice (实际使用):**
```python
import cv2

# Apply Gaussian blur
# (5,5) = kernel size, 0 = auto-compute sigma from kernel size
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# With explicit sigma
blurred = cv2.GaussianBlur(img, (5, 5), sigmaX=1.5)
```

**🔗 Related Concepts:**
→ see: Convolution (the operation used to apply this filter)
→ see: Sobel Kernel (often applied AFTER Gaussian to compute gradients)
→ see: Canny Edge Detection (uses Gaussian as Stage 1)

**📚 Appears In:**
- MV Week 2 §5 (Image Blurring)
- MV Week 2 §8 (Canny Edge Detection — Stage 1: Noise Reduction)

---

### Sobel Kernel / Sobel Operator (Sobel核 / Sobel算子)

**Tags:** `#signal-processing` `#edge-detection` `#gradient` `#mv-week2`

**📌 One-line Definition:**
> The Sobel operator is a pair of 3×3 convolution kernels that compute the **first derivative** (rate of change) of image intensity in the horizontal and vertical directions — detecting edges.
>> Sobel算子是一对3×3卷积核，计算图像强度在水平和垂直方向上的**一阶导数**（变化率）— 检测边缘。

**📐 Formula:**
```
Horizontal (Gx — detects VERTICAL edges):
[[-1, 0, 1],
 [-2, 0, 2],
 [-1, 0, 1]]

Vertical (Gy — detects HORIZONTAL edges):
[[-1, -2, -1],
 [ 0,  0,  0],
 [ 1,  2,  1]]
```
- Gx = result of convolving with horizontal kernel → large |Gx| = strong vertical edge
- Gy = result of convolving with vertical kernel → large |Gy| = strong horizontal edge
- **Counterintuitive:** horizontal kernel detects VERTICAL edges (because it measures horizontal change)

**💡 Intuition (直觉理解):**
> The Sobel kernel is like a **balance scale** placed on the image:
>
> **Horizontal kernel Gx:** Place the scale left-to-right. Left side has negative weights (-1, -2, -1), right side has positive weights (1, 2, 1). If left pixels are dark and right pixels are bright → the scale tips hard → big Gx → there's a **vertical edge** here (intensity changes from left to right).
>
> **Why -2 and +2 in the center row?** The center row gets double weight because it's closest to the pixel we're computing. This makes Sobel **smoother** than a simple [-1, 0, 1] difference — it also does a bit of vertical averaging, reducing noise.
>
> **Why does Gx detect VERTICAL edges?** Because Gx measures the rate of change in the **x-direction** (horizontal). If intensity changes rapidly from left to right, that means there's an edge running vertically (perpendicular to the change direction).
>> Sobel核就像放在图像上的**天平**：
>>
>> **水平核Gx：** 天平左右放置。左侧有负权重(-1, -2, -1)，右侧有正权重(1, 2, 1)。如果左边像素暗，右边像素亮 → 天平倾斜严重 → Gx很大 → 这里有**垂直边缘**（强度从左到右变化）。
>>
>> **为什么中间行是-2和+2？** 中间行得到双倍权重，因为它最靠近我们计算的像素。这使Sobel比简单的[-1, 0, 1]差分更**平滑** — 它同时做一点垂直平均，减少噪声。
>>
>> **为什么Gx检测垂直边缘？** 因为Gx测量**x方向**（水平）的变化率。如果强度从左到右快速变化，说明有一条垂直于变化方向的边缘。

**🔢 Worked Example:**
```
Image region:              Horizontal Sobel kernel:
[10, 10, 100]              [[-1, 0, 1],
[10, 10, 100]               [-2, 0, 2],
[10, 10, 100]               [-1, 0, 1]]

Gx = (-1×10 + 0×10 + 1×100) +
     (-2×10 + 0×10 + 2×100) +
     (-1×10 + 0×10 + 1×100)
   = (90) + (180) + (90) = 360

→ Large positive Gx → strong vertical edge (dark on left, bright on right)
```

**⚙️ In Practice (实际使用):**
```python
import cv2

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Compute Sobel derivatives
Gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)  # horizontal
Gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)  # vertical

# Gradient magnitude
magnitude = cv2.magnitude(Gx, Gy)

# Gradient direction
direction = cv2.phase(Gx, Gy, angleInDegrees=True)
```

**🔗 Related Concepts:**
→ see: Convolution (the operation that applies the Sobel kernel)
→ see: Gradient (the result of applying Sobel)
→ see: Canny Edge Detection (uses Sobel in Stage 2)

**📚 Appears In:**
- MV Week 2 §8 (Canny Edge Detection — Stage 2)
- MV Week 3 §6 (Image Gradient)
