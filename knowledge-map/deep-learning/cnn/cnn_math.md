---
topic: cnn
dimension: math
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)"
expiry: 12m
status: current
---

# CNN 数学基础

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
> 📖 Paper: LeCun et al., [Gradient-Based Learning Applied to Document Recognition (1998)](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $n$ | 输入图像的边长 | input size | 正整数 |
| $f$ | 滤波器/卷积核的边长 | filter/kernel size | 奇数：1, 3, 5, 7 |
| $p$ | 填充的像素数 | padding | 非负整数 |
| $s$ | 步长 | stride | 正整数，常取 1 或 2 |
| $C_{in}$ | 输入通道数 | input channels | RGB=3, 灰度=1 |
| $C_{out}$ | 输出通道数（滤波器个数） | output channels | 正整数：32, 64, 128... |
| $W$ | 滤波器权重矩阵 | weight / kernel | $f \times f \times C_{in}$ |
| $b$ | 偏置 | bias | 每个滤波器一个标量 |
| $X$ | 输入特征图 | input feature map | $C_{in} \times H \times W$ |
| $Y$ | 输出特征图 | output feature map | $C_{out} \times H' \times W'$ |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 核心公式

### 公式 1: 2D 卷积操作（单通道）

**直觉：** 滤波器"盖"在输入的一个位置上，逐元素相乘再求和，得到输出的一个像素值

$$
Y(i, j) = \sum_{m=0}^{f-1} \sum_{n=0}^{f-1} X(i \cdot s + m, \; j \cdot s + n) \cdot W(m, n) + b
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $(i, j)$ | 输出特征图的位置索引 | 第 i 行第 j 列 |
| $s$ | 步长，控制滤波器每次移动几格 | stride=1 |
| $(m, n)$ | 滤波器内部的位置索引 | 0 到 f-1 |

**推导过程：**

$$
\text{Step 1: 确定输出位置 } (i, j) \text{ 对应输入的起始位置 } (i \cdot s, \; j \cdot s)
$$

$$
\text{Step 2: 取输入中以 } (i \cdot s, \; j \cdot s) \text{ 为左上角、大小为 } f \times f \text{ 的区域}
$$

$$
\text{Step 3: 将该区域与滤波器 } W \text{ 逐元素相乘，求和，加偏置 } b
$$

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)

---

### 公式 2: 多通道卷积操作

**直觉：** RGB 图像有 3 个通道，滤波器也是 3 个通道的，每个通道分别做 2D 卷积后全部加起来

$$
Y_k(i, j) = \sum_{c=0}^{C_{in}-1} \sum_{m=0}^{f-1} \sum_{n=0}^{f-1} X_c(i \cdot s + m, \; j \cdot s + n) \cdot W_{k,c}(m, n) + b_k
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $k$ | 第 k 个滤波器（输出通道索引） | 0 到 $C_{out}-1$ |
| $c$ | 输入通道索引 | RGB: c=0(R), 1(G), 2(B) |
| $W_{k,c}$ | 第 k 个滤波器的第 c 个通道 | 3D 权重张量的一个 2D 切片 |

**推导过程：**

$$
\text{Step 1: 对每个输入通道 } c, \text{ 用 } W_{k,c} \text{ 做 2D 卷积}
$$

$$
\text{Step 2: 将 } C_{in} \text{ 个通道的卷积结果逐元素相加}
$$

$$
\text{Step 3: 加上第 } k \text{ 个滤波器的偏置 } b_k
$$

$$
\text{Step 4: 重复 } C_{out} \text{ 次，得到 } C_{out} \text{ 张特征图}
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

### 公式 3: 输出尺寸公式

**直觉：** 卷积后输出多大？用输入尺寸、滤波器大小、填充和步长就能算出来

$$
H_{out} = \left\lfloor \frac{n + 2p - f}{s} + 1 \right\rfloor
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $n$ | 输入边长 | 6 |
| $p$ | 填充像素数 | 0 (valid) 或 1 (same) |
| $f$ | 滤波器边长 | 3 |
| $s$ | 步长 | 1 |
| $\lfloor \cdot \rfloor$ | 向下取整 | 不足一步就丢弃 |

**推导过程：**

$$
\text{Step 1: 填充后的有效输入大小 = } n + 2p
$$

$$
\text{Step 2: 滤波器第一次放置后，剩余可滑动距离 = } (n + 2p) - f
$$

$$
\text{Step 3: 每步移动 } s \text{ 格，可移动次数 = } \frac{(n + 2p) - f}{s}
$$

$$
\text{Step 4: 加上第一次放置 = } \frac{n + 2p - f}{s} + 1
$$

$$
\text{Step 5: 向下取整（不够一步的丢弃）}
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

### 公式 4: Same Padding 的 p 值

**直觉：** 想让输出和输入一样大，需要补多少零？

$$
p = \frac{f - 1}{2}
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

**推导过程：**

$$
\text{Step 1: Same 要求 } H_{out} = n, \; s = 1
$$

$$
\text{Step 2: 代入输出尺寸公式: } n = n + 2p - f + 1
$$

$$
\text{Step 3: 化简: } 2p = f - 1
$$

$$
\text{Step 4: } p = \frac{f - 1}{2} \text{ （所以 } f \text{ 取奇数才能整除）}
$$

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---

### 公式 5: 卷积层参数量

**直觉：** 一个卷积层有多少个可训练参数？

$$
\text{Params} = (f \times f \times C_{in} + 1) \times C_{out}
$$

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $f \times f \times C_{in}$ | 一个滤波器的权重数 | 3×3×3 = 27 |
| $+1$ | 偏置（每个滤波器一个） | 1 |
| $\times C_{out}$ | 滤波器个数 | 64 |

**推导过程：**

$$
\text{Step 1: 每个滤波器的权重数 = } f \times f \times C_{in} = 3 \times 3 \times 3 = 27
$$

$$
\text{Step 2: 加偏置 = } 27 + 1 = 28
$$

$$
\text{Step 3: 共 } C_{out} = 64 \text{ 个滤波器: } 28 \times 64 = 1792
$$

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---


## 公式关系图

```
公式 1 (单通道卷积) ──→ 公式 2 (多通道卷积)
        │                       │
        └───→ 公式 3 (输出尺寸) ←───┘
                    │
              公式 4 (Same Padding p 值)
                    
公式 5 (参数量) ← 独立，但使用 f, C_in, C_out
```

---


## 手算练习

### 练习 1: 6×6 图像卷积

**题目：** 6×6 灰度图像，用 3×3 滤波器，stride=1，padding=0，计算输出尺寸

**解答步骤：**

1. 代入公式 3: $H_{out} = \lfloor \frac{6 + 2 \times 0 - 3}{1} + 1 \rfloor$
2. 计算: $= \lfloor \frac{3}{1} + 1 \rfloor = \lfloor 4 \rfloor = 4$
3. 结果: 输出为 **4×4**

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

### 练习 2: Same Padding 计算

**题目：** 输入 32×32，滤波器 5×5，stride=1，求 Same Padding 的 p 值和输出尺寸

**解答步骤：**

1. 代入公式 4: $p = \frac{5 - 1}{2} = 2$
2. 验证公式 3: $H_{out} = \lfloor \frac{32 + 2 \times 2 - 5}{1} + 1 \rfloor = \lfloor 32 \rfloor = 32$
3. 结果: p=2，输出为 **32×32**（与输入相同 ✅）

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) — LeNet-5 使用 5×5 滤波器

### 练习 3: 多层参数量计算

**题目：** 输入 3 通道 (RGB)，Conv1: 64 个 3×3 滤波器，Conv2: 128 个 3×3 滤波器。求每层参数量

**解答步骤：**

1. Conv1: $(3 \times 3 \times 3 + 1) \times 64 = 28 \times 64 = 1,792$
2. Conv2: $(3 \times 3 \times 64 + 1) \times 128 = 577 \times 128 = 73,856$
3. 结果: Conv1 = **1,792**，Conv2 = **73,856**

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

### 练习 4: LeNet-5 第一层

**题目：** LeNet-5 输入 32×32×1（灰度），C1 层: 6 个 5×5 滤波器，stride=1，padding=0。求输出尺寸和参数量

**解答步骤：**

1. 尺寸: $H_{out} = \lfloor \frac{32 + 0 - 5}{1} + 1 \rfloor = 28$, 输出为 **28×28×6**
2. 参数: $(5 \times 5 \times 1 + 1) \times 6 = 26 \times 6 = 156$
3. 结果: 输出 28×28×6，参数量 **156**

> 📖 Paper: [LeCun et al. 1998](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf) — LeNet-5 C1 layer

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 2D 卷积 | $Y(i,j) = \sum_m \sum_n X(is+m, js+n) \cdot W(m,n) + b$ | 理解卷积操作 | 无 |
| 多通道卷积 | $Y_k = \sum_c \text{Conv2D}(X_c, W_{k,c}) + b_k$ | RGB 图像卷积 | 公式 1 |
| 输出尺寸 | $\lfloor \frac{n+2p-f}{s} + 1 \rfloor$ | 计算特征图大小 | 无 |
| Same Padding | $p = \frac{f-1}{2}$ | 保持输入输出同尺寸 | 公式 3 |
| 参数量 | $(f^2 \cdot C_{in} + 1) \times C_{out}$ | 评估模型大小 | 无 |

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8
