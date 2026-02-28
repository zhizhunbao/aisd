# Week 2: 图像处理基础 — 数学公式速查 (Math Quick Reference)

> 📐 See also: [概念速查](week2_image_processing_cheatsheet.md) | [代码参考](week2_image_processing_code.md)
> 📄 Source: slides + demo code

---

## 📐 公式与计算

### 1. 2D 卷积 (Convolution)

图像滤波的核心操作 — 核（kernel）在图像上滑动，对邻域做加权求和：

$$G(x, y) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} K(i, j) \cdot I(x+i, y+j)$$

| 符号     | 含义           | 说明                        |
| -------- | -------------- | --------------------------- |
| $I(x,y)$ | 输入图像像素值 | 位置 $(x,y)$ 处             |
| $K(i,j)$ | 卷积核/滤波器  | 大小 $(2k+1) \times (2k+1)$ |
| $G(x,y)$ | 输出图像像素值 | 滤波后的结果                |
| $k$      | 核的半径       | 3×3核 → k=1; 5×5核 → k=2    |

---

### 2. 均值滤波核 (Average Filter Kernel)

3×3 均值核：

$$K_{\text{avg}} = \frac{1}{9} \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

📝 **手算练习 1：**

> 对中心像素 100，邻域为 `[[80,90,85],[95,100,110],[105,115,120]]`，用 3×3 均值核求结果？
>
> 答：$(80+90+85+95+100+110+105+115+120) / 9 = 900/9 = 100$

---

### 3. 高斯滤波核 (Gaussian Filter Kernel)

高斯权重公式（2D）：

$$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$$

| 符号     | 含义               | 说明            |
| -------- | ------------------ | --------------- |
| $\sigma$ | 标准差             | 越大 → 模糊越强 |
| $(x, y)$ | 相对于核中心的距离 | 中心 = (0,0)    |

近似 3×3 高斯核 (σ ≈ 1)：

$$K_{\text{gauss}} \approx \frac{1}{16} \begin{bmatrix} 1 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 1 \end{bmatrix}$$

> 💡 中心权重(4)是角落权重(1)的4倍 → 更自然的平滑

---

### 4. 锐化核 (Sharpening Kernel)

$$K_{\text{sharpen}} = \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$

> 原理：中心权重大(5)，周围为负(-1) → 放大中心与邻域的差值 → 增强边缘

---

### 5. Sobel 梯度算子

**水平梯度核 $G_x$：**

$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

**垂直梯度核 $G_y$：**

$$G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

**梯度幅值：**

$$|G| = \sqrt{G_x^2 + G_y^2}$$

**梯度方向：**

$$\theta = \arctan\left(\frac{G_y}{G_x}\right)$$

| 符号     | 含义         | 说明         |
| -------- | ------------ | ------------ |
| $G_x$    | 水平方向梯度 | 检测垂直边缘 |
| $G_y$    | 垂直方向梯度 | 检测水平边缘 |
| $\|G\|$  | 梯度幅值     | 边缘强度     |
| $\theta$ | 梯度方向     | 边缘法线方向 |

📝 **手算练习 2：**

> 一个3×3邻域为 `[[10,10,10],[10,10,50],[10,10,50]]`，用 Sobel $G_x$ 求梯度？
>
> 答：$G_x = (-1)(10)+0(10)+1(10)+(-2)(10)+0(10)+2(50)+(-1)(10)+0(10)+1(50)$
> $= -10+0+10-20+0+100-10+0+50 = 120$
> 水平梯度为 120（右侧有强垂直边缘）

---

### 6. 简单阈值化 (Simple Thresholding)

$$g(x, y) = \begin{cases} \text{maxVal} & \text{if } I(x,y) > T \\ 0 & \text{otherwise} \end{cases}$$

| 符号   | 含义   | 典型值        |
| ------ | ------ | ------------- |
| $T$    | 阈值   | 127（中间值） |
| maxVal | 最大值 | 255           |

📝 **手算练习 3：**

> 像素值序列: [100, 150, 80, 200, 127, 130]，阈值 T=127，结果？
>
> 答：[0, 255, 0, 255, 0, 255]
> (注：127 ≤ T → 0)

---

### 7. 仿射变换 (Affine Transformation)

$$\mathbf{y} = A\mathbf{x} + \mathbf{b}$$

**平移矩阵：**

$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$

**旋转矩阵：**

$$A_{\text{rot}} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$$

**缩放矩阵：**

$$A_{\text{scale}} = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix}$$

**剪切矩阵（水平）：**

$$A_{\text{shear}} = \begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$$

| 符号       | 含义     |
| ---------- | -------- |
| $t_x, t_y$ | 平移距离 |
| $\theta$   | 旋转角度 |
| $s_x, s_y$ | 缩放因子 |
| $k$        | 剪切系数 |

📝 **手算练习 4：**

> 点 (3, 4) 绕原点逆时针旋转 90°，结果坐标？
>
> 答：$\cos 90° = 0, \sin 90° = 1$
> $x' = 0 \times 3 + (-1) \times 4 = -4$
> $y' = 1 \times 3 + 0 \times 4 = 3$
> 结果：**(-4, 3)**

📝 **手算练习 5：**

> 点 (10, 20) 缩放 $s_x = 0.5, s_y = 2$，结果？
>
> 答：$x' = 0.5 \times 10 = 5, \quad y' = 2 \times 20 = 40$
> 结果：**(5, 40)**

---

### 8. 形态学操作逻辑

**腐蚀 (Erosion):** 输出像素 = 1 当且仅当核下**所有**输入像素 = 1

$$E(x,y) = \begin{cases} 1 & \text{if } \forall (i,j) \in K: I(x+i, y+j) = 1 \\ 0 & \text{otherwise} \end{cases}$$

**膨胀 (Dilation):** 输出像素 = 1 当且仅当核下**至少一个**输入像素 = 1

$$D(x,y) = \begin{cases} 1 & \text{if } \exists (i,j) \in K: I(x+i, y+j) = 1 \\ 0 & \text{otherwise} \end{cases}$$

**组合操作：**

- **开运算** = $D(E(I))$ = 膨胀(腐蚀(图像))
- **闭运算** = $E(D(I))$ = 腐蚀(膨胀(图像))

---

## 🔢 核速查表

| 核名称      | 矩阵                                    | 用途     |
| ----------- | --------------------------------------- | -------- |
| 均值 3×3    | $\frac{1}{9}[[1,1,1],[1,1,1],[1,1,1]]$  | 平均模糊 |
| 高斯 3×3    | $\frac{1}{16}[[1,2,1],[2,4,2],[1,2,1]]$ | 自然模糊 |
| 锐化        | $[[0,-1,0],[-1,5,-1],[0,-1,0]]$         | 增强边缘 |
| Sobel $G_x$ | $[[-1,0,1],[-2,0,2],[-1,0,1]]$          | 水平梯度 |
| Sobel $G_y$ | $[[-1,-2,-1],[0,0,0],[1,2,1]]$          | 垂直梯度 |

---

## 🔗 相关文件

- 📖 [概念速查](week2_image_processing_cheatsheet.md) — 定义、要点、陷阱
- 🔧 [代码参考](week2_image_processing_code.md) — OpenCV 实现
