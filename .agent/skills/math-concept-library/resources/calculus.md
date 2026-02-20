# Calculus Concepts (微积分概念)

---

### Gradient / Image Gradient (梯度 / 图像梯度)

**Tags:** `#calculus` `#derivative` `#edge-detection` `#mv-week2` `#mv-week3`

**📌 One-line Definition:**
> The gradient of an image is a 2D vector at each pixel showing the **direction** and **rate** of the fastest intensity change — it points perpendicular to edges.
>> 图像梯度是每个像素处的二维向量，显示最快强度变化的**方向**和**速率** — 它垂直于边缘方向。

**📐 Formula:**
```
∇F = (∂F/∂x, ∂F/∂y) = (Gx, Gy)

Magnitude: |G| = √(Gx² + Gy²)      → edge strength (边缘强度)
Direction: θ = arctan(Gy / Gx)      → edge orientation (边缘方向)
```
- ∇F = gradient vector at pixel (x,y)
- ∂F/∂x = rate of intensity change in x-direction (horizontal) = Gx
- ∂F/∂y = rate of intensity change in y-direction (vertical) = Gy
- |G| = gradient magnitude — how strong the edge is (0 = flat, 255 = sharp edge)
- θ = gradient direction — which way the edge faces (perpendicular to the edge line)

**💡 Intuition (直觉理解):**
> **The hillside analogy:**
>
> Imagine a grayscale image as a 3D terrain where **bright = high** and **dark = low**. The gradient at any point tells you:
> 1. **Magnitude** = how steep the slope is. Flat area → gradient ≈ 0. Cliff → gradient is huge.
> 2. **Direction** = which way is "uphill" (toward brighter). It always points **perpendicular to the edge** (the edge is the contour line, and the gradient points away from it).
>
> **Why does this detect edges?** An edge in an image is where brightness changes suddenly (dark → bright). That's exactly a steep slope on our terrain → high gradient magnitude → "there's an edge here!"
>
> **Why 2 components (Gx, Gy)?** Because slopes can go in any 2D direction. Gx catches left-right changes (vertical edges). Gy catches up-down changes (horizontal edges). Together they capture edges at any angle.
>> **山坡类比：**
>>
>> 想象灰度图像是一个3D地形，**亮 = 高**，**暗 = 低**。每个点的梯度告诉你：
>> 1. **幅值** = 坡度有多陡。平地 → 梯度 ≈ 0。悬崖 → 梯度很大。
>> 2. **方向** = 哪个方向是"上坡"（朝更亮的方向）。它总是**垂直于边缘**（边缘是等高线，梯度指向远离它的方向）。
>>
>> **为什么能检测边缘？** 图像中的边缘是亮度突然变化的地方（暗→亮）。在我们的地形上这就是陡坡 → 高梯度幅值 → "这里有边缘！"
>>
>> **为什么需要2个分量(Gx, Gy)？** 因为坡度可以朝2D的任何方向。Gx捕捉左右变化（垂直边缘）。Gy捕捉上下变化（水平边缘）。合在一起能捕捉任意角度的边缘。

**🔢 Worked Example:**
```
Image patch around pixel (2,2):
[50,  50,  50]
[50,  50, 200]     ← sharp brightness jump to the right
[50,  50, 200]

After Sobel:
Gx = 360 (big horizontal change → vertical edge on the right)
Gy = 0   (no vertical change)

Magnitude = √(360² + 0²) = 360   → strong edge!
Direction = arctan(0/360) = 0°    → edge is horizontal (gradient points right)

Interpretation: There's a vertical edge with the gradient pointing to the right
(from dark to bright).
```

**⚙️ In Practice (实际使用):**
```python
import cv2
import numpy as np

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)  # ALWAYS blur first!

Gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
Gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

magnitude = np.sqrt(Gx**2 + Gy**2)
direction = np.arctan2(Gy, Gx) * 180 / np.pi  # in degrees
```

**⚠️ Common Mistake:**
> **ALWAYS blur before computing gradients.** Gradient = differentiation = amplifies noise. Without blurring, noise pixels create false edges everywhere.
>> **必须先模糊再计算梯度。** 梯度 = 求导 = 放大噪声。不先模糊，噪声像素会到处产生假边缘。

**🔗 Related Concepts:**
→ see: Sobel Kernel (the tool used to compute Gx and Gy)
→ see: Gaussian Filter (used to smooth before gradient computation)
→ see: Derivative (the mathematical foundation)

**📚 Appears In:**
- MV Week 2 §8 (Canny Edge Detection — Stage 2)
- MV Week 3 §6 (Image Gradient)

---

### Derivative / Differentiation (导数 / 微分)

**Tags:** `#calculus` `#fundamental` `#mv-week2`

**📌 One-line Definition:**
> A derivative measures the **instantaneous rate of change** of a function — in images, it tells you how fast pixel brightness is changing at each point.
>> 导数测量函数的**瞬时变化率** — 在图像中，它告诉你每个点的像素亮度变化有多快。

**📐 Formula:**
```
Continuous:  f'(x) = lim(h→0) [f(x+h) - f(x)] / h
Discrete:    f'(x) ≈ f(x+1) - f(x)           (forward difference)
             f'(x) ≈ [f(x+1) - f(x-1)] / 2   (central difference)
```
- f(x) = pixel intensity at position x
- f'(x) = rate of change at position x
- h = step size (in discrete images, h = 1 pixel)
- Central difference is more accurate (used by Sobel)

**💡 Intuition (直觉理解):**
> **The speedometer analogy:**
>
> If position is f(x), then the derivative f'(x) is the **speedometer** — it tells you how fast you're moving at this instant.
>
> **In images:** Picture a row of pixel values: `[50, 50, 50, 200, 200, 200]`. The derivative at each position:
> - At pixels 1,2: derivative ≈ 0 (flat, no change)
> - At pixel 3→4: derivative ≈ 150 (huge jump! = edge!)
> - At pixels 4,5: derivative ≈ 0 (flat again)
>
> **Key insight:** Derivative = 0 means "no change" (flat region). Large derivative means "fast change" (edge). That's why derivatives detect edges!
>
> **The noise problem:** Taking a derivative amplifies small fluctuations. If your signal has tiny random bumps (noise), the derivative turns them into spikes. That's why we smooth (blur) first.
>> **速度计类比：**
>>
>> 如果位置是f(x)，那导数f'(x)就是**速度计** — 它告诉你这一刻移动有多快。
>>
>> **在图像中：** 想象一行像素值：`[50, 50, 50, 200, 200, 200]`。每个位置的导数：
>> - 像素1,2处：导数 ≈ 0（平坦，无变化）
>> - 像素3→4处：导数 ≈ 150（巨大跳跃！= 边缘！）
>> - 像素4,5处：导数 ≈ 0（又平坦了）
>>
>> **关键理解：** 导数 = 0 表示"无变化"（平坦区域）。大导数表示"快速变化"（边缘）。这就是导数检测边缘的原理！
>>
>> **噪声问题：** 求导会放大小的波动。如果信号有微小的随机凸起（噪声），导数会把它们变成尖峰。这就是为什么我们先平滑（模糊）。

**🔢 Worked Example:**
```
1D pixel row: [100, 100, 102, 200, 200, 198]

Forward difference derivative:
f'(0) = 100-100 = 0    (flat)
f'(1) = 102-100 = 2    (tiny noise)
f'(2) = 200-102 = 98   (EDGE!)
f'(3) = 200-200 = 0    (flat)
f'(4) = 198-200 = -2   (tiny noise)

The derivative clearly shows the edge at position 2→3.
The noise at positions 1 and 4 produces small spikes (2 and -2).
```

**🔗 Related Concepts:**
→ see: Gradient (2D version of derivative applied to images)
→ see: Sobel Kernel (computes discrete derivatives efficiently)
→ see: Gaussian Filter (smooths before differentiation to reduce noise)

**📚 Appears In:**
- MV Week 2 §8 (Canny Edge Detection — why Gaussian smoothing is needed)
- MV Week 3 §6 (Image Gradient)

---

### Non-maximum Suppression, NMS (非极大值抑制)

**Tags:** `#calculus` `#local-maximum` `#edge-thinning` `#mv-week2`

**📌 One-line Definition:**
> Non-maximum Suppression keeps only the **local maximum** gradient values along the gradient direction, thinning thick gradient edges down to 1-pixel wide lines.
>> 非极大值抑制只保留沿梯度方向上的**局部最大值**，将粗的梯度边缘细化为1像素宽的线。

**📐 Formula:**
```
For each pixel p with gradient magnitude M(p) and direction θ(p):
    1. Find the two neighbors (n₁, n₂) along the gradient direction θ
    2. If M(p) ≥ M(n₁) AND M(p) ≥ M(n₂):
         keep p (it's the local max)
       Else:
         suppress p to 0
```
- M(p) = gradient magnitude at pixel p
- θ(p) = gradient direction at pixel p (from arctan(Gy/Gx))
- n₁, n₂ = the two neighbors in the direction of θ (perpendicular to the edge)

**💡 Intuition (直觉理解):**
> **The mountain ridge analogy:**
>
> After computing the gradient, edges look like thick, blurry ridges on a mountain. NMS is like walking across the ridge and asking at each point: "Am I the highest point if I look left and right (perpendicular to the ridge direction)?" If yes → keep. If no → suppress to zero.
>
> **Why "along the gradient direction"?** The gradient direction is perpendicular to the edge. By comparing values perpendicular to the edge, we find the exact peak of the edge. It's like finding the exact top of a hill by looking at the slope on both sides.
>
> **NMS ≠ thresholding!** Thresholding asks "is this value above X?" NMS asks "is this value the biggest among its neighbors in a specific direction?" Completely different operations.
>> **山脊类比：**
>>
>> 计算梯度后，边缘看起来像山上粗的、模糊的山脊。NMS就像沿山脊走，在每个点问："如果我向左右看（垂直于山脊方向），我是最高点吗？"如果是 → 保留。如果不是 → 抑制为零。
>>
>> **为什么是"沿梯度方向"？** 梯度方向垂直于边缘。通过比较垂直于边缘方向的值，我们找到边缘的精确峰值。就像通过看两侧的坡度来找到山顶的确切位置。
>>
>> **NMS ≠ 阈值化！** 阈值化问"这个值是否超过X？"NMS问"这个值是否是某个特定方向上邻居中最大的？"完全不同的操作。

**🔗 Related Concepts:**
→ see: Gradient (NMS operates on gradient magnitude and direction)
→ see: Canny Edge Detection (NMS is Stage 3)

**📚 Appears In:**
- MV Week 2 §8 (Canny Edge Detection — Stage 3)
