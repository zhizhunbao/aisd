# Image Processing Concepts (图像处理概念)

---

### Histogram Equalization (直方图均衡化)

**Tags:** `#image-processing` `#contrast` `#mv-week2`

**📌 One-line Definition:**

> Histogram equalization remaps pixel intensities so that the histogram becomes approximately uniform — maximizing contrast by spreading intensities across the full [0, 255] range.
>
> > 直方图均衡化重新映射像素强度，使直方图近似均匀分布 — 通过将强度扩展到完整的[0, 255]范围来最大化对比度。

**📐 Formula:**

```
new_value(v) = round( (CDF(v) - CDF_min) / (N - CDF_min) × (L-1) )
```

- v = original pixel intensity (0-255)
- CDF(v) = cumulative count of pixels with intensity ≤ v
- CDF_min = smallest non-zero CDF value
- N = total number of pixels in the image
- L = number of intensity levels (typically 256)
- new_value(v) = remapped intensity (0-255)

**💡 Intuition (直觉理解):**

> **The grade curve analogy:**
> Imagine a class where everyone scored between 60-70 on a test (clustered, no spread). Histogram equalization is like "curving the grades" — mapping the scores to fill the entire 0-100 range. The student with the lowest score gets 0, the highest gets 100, and everyone else is spread evenly in between.
>
> **In images:** A low-contrast image has all pixels bunched in a narrow intensity range (e.g., all grayish). Equalization spreads them across 0-255 → visible contrast.
>
> > **成绩曲线类比：**
> > 想象一个班级考试分数都在60-70之间。直方图均衡化就像"调整分数" — 把分数映射到填满0-100的范围。最低分得0，最高分得100，其他人均匀分布。
> >
> > **在图像中：** 低对比度图像的像素集中在窄强度范围。均衡化扩展到0-255 → 可见对比度。

**🔢 Worked Example:**

```
Simple 4×1 image: [50, 50, 100, 150], L=256

Histogram: h(50)=2, h(100)=1, h(150)=1
CDF: CDF(50)=2, CDF(100)=3, CDF(150)=4
CDF_min=2, N=4

new(50)  = round((2-2)/(4-2) × 255) = 0
new(100) = round((3-2)/(4-2) × 255) = 128
new(150) = round((4-2)/(4-2) × 255) = 255

Result: [0, 0, 128, 255] → full range utilized!
```

**⚙️ In Practice (实际使用):**

```python
import cv2

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
equalized = cv2.equalizeHist(gray)

# CLAHE (adaptive, often better):
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
adaptive_eq = clahe.apply(gray)
```

**🔗 Related Concepts:**
→ see: Thresholding (often applied after equalization)

**📚 Appears In:**

- MV Week 2 §9 (Image Histograms)

---

### Unsharp Masking (反锐化掩模)

**Tags:** `#image-processing` `#sharpening` `#mv-week2`

**📌 One-line Definition:**

> Unsharp masking sharpens an image by adding back the high-frequency details (edges) that were removed by blurring.
>
> > 反锐化掩模通过将模糊去除的高频细节（边缘）加回来实现图像锐化。

**📐 Formula:**

```
sharpened = original + α × (original - GaussianBlur(original))
```

- original = input image
- GaussianBlur(original) = blurred version (low-frequency only)
- (original - blurred) = high-frequency details (edges, noise)
- α = sharpening strength: 0.5 (subtle), 1.0 (standard), 2.0 (aggressive)

**Equivalent kernel form:**

```
Sharpening kernel:
[[0,  -1,  0],
[-1,  5, -1],         center 5 = 1 (identity) + 4 (enhancement)
[ 0, -1,  0]]
```

**💡 Intuition (直觉理解):**

> **The photo editing analogy:**
>
> 1. Make a blurry copy of your photo (removes detail)
> 2. Subtract the blurry from the original → you get ONLY the edges
> 3. Add those edges back to the original with amplification
>
> It's called "unsharp" because you USE an unsharp (blurred) version to FIND what to sharpen. Counterintuitive name!
>
> > **照片编辑类比：**
> >
> > 1.  做一份模糊的照片副本（去除细节）
> > 2.  从原片减去模糊版 → 只剩边缘和细节
> > 3.  把边缘放大后加回原片
> >
> > 叫"反锐化"掩模是因为你用了不锐利（模糊）的版本来找到需要锐化的东西。名字反直觉！

**⚠️ Common Mistake:**

> Sharpening amplifies ALL high-frequency content, including **noise**. Always denoise first!
>
> > 锐化放大所有高频内容，包括**噪声**。总是先去噪！

**🔗 Related Concepts:**
→ see: Gaussian Filter (used to create the blurred version)
→ see: Convolution (the sharpening kernel is applied via convolution)

**📚 Appears In:**

- MV Week 2 §6 (Image Sharpening)

---

### Morphological Operations: Erosion & Dilation (形态学操作：腐蚀与膨胀)

**Tags:** `#image-processing` `#binary-image` `#mv-week2`

**📌 One-line Definition:**

> Erosion shrinks white regions (all neighbors must be white). Dilation expands white regions (any white neighbor triggers expansion). Used to clean binary/mask images.
>
> > 腐蚀缩小白色区域（核内全白才保留）。膨胀扩大白色区域（任何白色邻居即扩展）。

**📐 Operations:**

```
Erosion:  output(x,y) = MIN of all pixels under the kernel → shrinks white
Dilation: output(x,y) = MAX of all pixels under the kernel → expands white

Opening  = Erosion → Dilation   (removes small white noise)
Closing  = Dilation → Erosion   (fills small black holes)
```

**💡 Intuition (直觉理解):**

> **Erosion = coastline erosion.** Water eats edges. Small islands vanish entirely. Large landmasses shrink slightly.
> **Dilation = land expansion.** Land grows outward. Small gaps fill up.
> **Opening:** "Remove sand specks, then restore coastline."
> **Closing:** "Fill puddles, then trim growth."
>
> > **腐蚀 = 海岸线侵蚀。** 水侵蚀边缘。小岛消失。大陆缩小。
> > **膨胀 = 陆地扩张。** 陆地向外生长。小间隙填满。
> > **开运算：** "去除沙粒，然后恢复海岸线。"
> > **闭运算：** "填平水洼，然后修剪生长。"

**⚙️ In Practice (实际使用):**

```python
import cv2
import numpy as np

kernel = np.ones((5,5), np.uint8)
eroded  = cv2.erode(binary_img, kernel, iterations=1)
dilated = cv2.dilate(binary_img, kernel, iterations=1)
opened  = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
closed  = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
```

**⚠️ Common Mistake:**

> **Order matters!** Opening ≠ Closing. Wrong order = opposite effect.
>
> > **顺序很重要！** 开运算 ≠ 闭运算。顺序搞反效果相反。

**🔗 Related Concepts:**
→ see: Thresholding (creates the binary image that morphology operates on)

**📚 Appears In:**

- MV Week 2 §11 (Morphological Operations)

---

### Thresholding (阈值化)

**Tags:** `#image-processing` `#segmentation` `#mv-week2` `#mv-week3`

**📌 One-line Definition:**

> Thresholding converts a grayscale image to binary by setting pixels above a threshold to white and below to black.
>
> > 阈值化通过将高于阈值的像素设为白色、低于阈值的设为黑色，将灰度图转换为二值图。

**📐 Formula:**

```
Simple:    output(x,y) = 255 if input(x,y) > T, else 0
Adaptive:  T(x,y) varies per pixel based on local neighborhood
```

**💡 Intuition (直觉理解):**

> **Pass/fail:** One cutoff for all (simple) vs per-class cutoff (adaptive).
>
> > **及格/不及格：** 所有人一个分数线（简单）vs 每班一个分数线（自适应）。

**⚙️ In Practice (实际使用):**

```python
import cv2

_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
adaptive = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
```

**🔗 Related Concepts:**
→ see: Histogram (visualize distribution to choose T)
→ see: Morphological Operations (clean binary image after thresholding)
→ see: Double Thresholding (Canny Stage 4)

**📚 Appears In:**

- MV Week 2 §10, MV Week 3 §2

---

### Interpolation (插值)

**Tags:** `#image-processing` `#resizing` `#mv-week2`

**📌 One-line Definition:**

> Interpolation estimates pixel values at non-integer positions when resizing/transforming — trading quality vs speed.
>
> > 插值在调整大小/变换时估计非整数位置的像素值 — 在质量和速度间权衡。

**📐 Methods:**

```
Nearest Neighbor: closest pixel (fastest, blocky)
Bilinear:         4 nearest pixels (good balance)
Bicubic:          16 nearest pixels (best quality, slowest)
```

**💡 Intuition (直觉理解):**

> **Zooming into a mosaic:** Nearest = bigger blocks. Bilinear = smooth blending of 4 tiles. Bicubic = smoothest blending of 16 tiles.
>
> > **放大马赛克：** 最近邻 = 更大方块。双线性 = 4块砖混合。双三次 = 16块砖最平滑混合。

**⚙️ In Practice (实际使用):**

```python
import cv2

small = cv2.resize(img, (100, 100), interpolation=cv2.INTER_NEAREST)
medium = cv2.resize(img, (100, 100), interpolation=cv2.INTER_LINEAR)  # default
best = cv2.resize(img, (100, 100), interpolation=cv2.INTER_CUBIC)
shrunk = cv2.resize(img, (50, 50), interpolation=cv2.INTER_AREA)     # for shrinking
```

**🔗 Related Concepts:**
→ see: Affine Transformation (interpolation needed when warping)

**📚 Appears In:**

- MV Week 2 §7 (Basic Image Manipulations)

---

### CNN Convolution Output Size (卷积输出尺寸公式)

**Tags:** `#image-processing` `#cnn` `#ml-week3`

**📌 One-line Definition:**

> The formula to calculate the spatial dimensions of a feature map after applying a convolution or pooling operation with given filter size, padding, and stride.
>
> > 给定滤波器大小、填充和步长后，计算卷积或池化操作后特征图空间维度的公式。

**📐 Formula:**

```
Output = ⌊(n + 2p - f) / s + 1⌋

where:
  n = input size (height or width)
  p = padding (number of zero pixels added per side)
  f = filter/kernel size
  s = stride (step size)
  ⌊·⌋ = floor (round down)

Special cases:
  No padding, stride 1:   out = n - f + 1
  Same padding, stride 1: p = (f-1)/2, out = n
```

**💡 Intuition (直觉理解):**

> Think of it as: "How many times can the filter slide across the input?" The numerator (n + 2p - f) is the "remaining space" after the first filter placement. Dividing by stride tells you how many steps you can take. Add 1 for the initial position.
>
> > 可以理解为："滤波器能在输入上滑动多少次？"分子 (n + 2p - f) 是放下第一个滤波器后的"剩余空间"。除以步长告诉你能走多少步。加 1 是因为初始位置。

**🔢 Worked Example:**

```
Input: 32×32, Filter: 3×3, Padding: 1, Stride: 2

Output = ⌊(32 + 2×1 - 3) / 2 + 1⌋
       = ⌊(32 + 2 - 3) / 2 + 1⌋
       = ⌊31/2 + 1⌋
       = ⌊15.5 + 1⌋
       = ⌊16.5⌋ = 16

→ Output: 16×16
```

**🔗 Related Concepts:**
→ see: Convolution in concept-glossary
→ see: Pooling in concept-glossary (uses same formula)

**📚 Appears In:**

- ML Week 3 §5 (Convolution Parameters — Padding and Stride)
