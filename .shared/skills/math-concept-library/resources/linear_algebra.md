# Linear Algebra Concepts (线性代数概念)

---

### Affine Transformation (仿射变换)

**Tags:** `#linear-algebra` `#transformation` `#mv-week2`

**📌 One-line Definition:**
> An affine transformation is any geometric operation expressible as **y = Ax + b** (matrix multiplication + translation) — it can translate, rotate, scale, shear, or any combination, while preserving parallel lines and ratios.
>> 仿射变换是任何可以表示为**y = Ax + b**（矩阵乘法+平移）的几何操作 — 可以平移、旋转、缩放、剪切或任意组合，同时保持平行线和比例。

**📐 Formula:**
```
General form: y = Ax + b

In 2D with homogeneous coordinates:
[x']   [a₁₁  a₁₂  tx] [x]
[y'] = [a₂₁  a₂₂  ty] [y]
[1 ]   [ 0    0    1 ] [1]

OpenCV uses 2×3 matrix M:
M = [[a₁₁, a₁₂, tx],
     [a₂₁, a₂₂, ty]]
```
- A = 2×2 linear transformation matrix (rotation, scale, shear)
- b = (tx, ty) = translation vector
- M = combined 2×3 matrix used by `cv2.warpAffine()`

**Common transformation matrices:**

| Transform | Matrix M |
|---|---|
| Translation by (tx, ty) | `[[1, 0, tx], [0, 1, ty]]` |
| Scaling by (sx, sy) | `[[sx, 0, 0], [0, sy, 0]]` |
| Rotation by θ around origin | `[[cosθ, -sinθ, 0], [sinθ, cosθ, 0]]` |

**💡 Intuition (直觉理解):**
> **The rubber sheet analogy:**
>
> Imagine your image is printed on a rubber sheet pinned to a board:
> - **Translation** = slide the whole sheet (all pins move the same distance)
> - **Rotation** = pin one corner and spin
> - **Scaling** = stretch/compress the rubber
> - **Shearing** = push one edge sideways while holding the opposite edge
>
> **What's preserved:** Parallel lines stay parallel. Points on a straight line stay on a straight line. Distance ratios along a line stay the same.
>
> **What's NOT preserved:** Angles can change. Distances can change. Circles can become ellipses.
>> **橡胶片类比：**
>>
>> 想象你的图像印在一块钉在板上的橡胶片上：
>> - **平移** = 滑动整块橡胶（所有钉子移动相同距离）
>> - **旋转** = 钉住一个角，旋转
>> - **缩放** = 拉伸/压缩橡胶
>> - **剪切** = 推一个边，同时固定对面的边
>>
>> **保持的：** 平行线保持平行。直线上的点保持在直线上。沿直线的距离比保持不变。
>>
>> **不保持的：** 角度可能改变。距离可能改变。圆可能变成椭圆。

**⚙️ In Practice (实际使用):**
```python
import cv2
import numpy as np

h, w = img.shape[:2]

# Translation: shift right 50px, down 30px
M_translate = np.float32([[1, 0, 50], [0, 1, 30]])
translated = cv2.warpAffine(img, M_translate, (w, h))

# Rotation: 45° around center, scale 1.0
center = (w // 2, h // 2)
M_rotate = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(img, M_rotate, (w, h))

# Scaling: simpler to use cv2.resize()
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)
```

**🔗 Related Concepts:**
→ see: Matrix Multiplication (the core operation)

**📚 Appears In:**
- MV Week 2 §12 (Image Transformation Techniques)
