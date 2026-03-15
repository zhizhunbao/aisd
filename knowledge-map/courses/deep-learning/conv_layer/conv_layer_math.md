---
topic: conv_layer
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5.5.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Dumoulin & Visin, 'A guide to convolution arithmetic', 2016 — https://arxiv.org/abs/1603.07285"
  - "📖 Docs: PyTorch nn.Conv2d — https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html"
expiry: 12m
status: current
---

# Conv Layer (卷积层) 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
> 📖 Paper: Dumoulin & Visin, [A guide to convolution arithmetic](https://arxiv.org/abs/1603.07285), 2016

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $I$ 或 $H, W$ | 输入的空间尺寸（高/宽） | Input height/width | 正整数 |
| $K$ 或 $f$ | 卷积核大小（正方形边长） | Kernel size | 通常 1, 3, 5, 7 |
| $S$ | 步长 | Stride | 正整数，通常 1 或 2 |
| $P$ | 填充大小（每边补零数） | Padding | 非负整数 |
| $d$ | 膨胀率（空洞卷积） | Dilation rate | 正整数，默认 1 |
| $C_{in}$ | 输入通道数 | Input channels | 正整数 (RGB=3) |
| $C_{out}$ | 输出通道数 = 滤波器个数 | Output channels | 正整数 |
| $O$ 或 $H_{out}, W_{out}$ | 输出空间尺寸 | Output height/width | 正整数 |
| $\mathbf{X}$ | 输入张量 | Input tensor | $\mathbb{R}^{C_{in} \times H \times W}$ |
| $\mathbf{W}$ | 滤波器权重张量 | Filter weights | $\mathbb{R}^{C_{out} \times C_{in} \times K \times K}$ |
| $\mathbf{b}$ | 偏置向量 | Bias vector | $\mathbb{R}^{C_{out}}$ |
| $\mathbf{Y}$ | 输出张量 | Output tensor | $\mathbb{R}^{C_{out} \times H_{out} \times W_{out}}$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---


## 核心公式

### 公式 1: 2D 卷积操作（单滤波器）

**直觉：** 一个滤波器在输入上滑动，每个位置做"覆盖区域 × 滤波器权重 → 求和 + 偏置"，产生输出特征图上的一个值。

$$
Y[m][i][j] = b[m] + \sum_{c=0}^{C_{in}-1} \sum_{p=0}^{K-1} \sum_{q=0}^{K-1} W[m][c][p][q] \cdot X[c][i \cdot S + p][j \cdot S + q]
$$

> 📚 Book: Goodfellow et al., Eq.9.6–9.8

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $m$ | 第 $m$ 个滤波器（输出通道索引） | $m = 0, \ldots, C_{out}-1$ |
| $(i, j)$ | 输出特征图的空间位置 | $(0,0)$ 到 $(H_{out}-1, W_{out}-1)$ |
| $(p, q)$ | 滤波器内部的位置 | $(0,0)$ 到 $(K-1, K-1)$ |
| $c$ | 输入通道索引 | RGB: $c = 0,1,2$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.1

---

### 公式 2: 输出尺寸公式 ⭐

**直觉：** 输入有多大、核有多大、走几步、边上补了多少——这四个因素决定输出有多大。

**标准卷积：**

$$
O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1
$$

**空洞/膨胀卷积** ($d > 1$)：

$$
K_{\text{eff}} = K + (K-1)(d-1)
$$

$$
O = \left\lfloor \frac{I - K_{\text{eff}} + 2P}{S} \right\rfloor + 1
$$

**转置卷积（上采样）：**

$$
O = (I - 1) \times S - 2P + K + \text{output\_padding}
$$

> 📖 Paper: Dumoulin & Visin, [Convolution Arithmetic](https://arxiv.org/abs/1603.07285), 2016

**常用速记：**

| 配置 | 公式简化 | 效果 |
|------|---------|------|
| $K=3, P=1, S=1$ | $O = I$ | 保持尺寸 |
| $K=3, P=1, S=2$ | $O = \lceil I/2 \rceil$ | 尺寸减半 |
| $K=1, P=0, S=1$ | $O = I$ | 仅通道变换 |
| $K=5, P=2, S=1$ | $O = I$ | 保持尺寸 |
| $K=7, P=3, S=2$ | $O = \lceil I/2 \rceil$ | ResNet 第一层 |

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

---

### 公式 3: 参数量公式 ⭐

**直觉：** 每个滤波器是 $K \times K \times C_{in}$ 的 3D 权重 + 1 个偏置，总共有 $C_{out}$ 个滤波器。

$$
\text{Params} = (K \times K \times C_{in} + 1) \times C_{out}
$$

不含偏置时（`bias=False`）：

$$
\text{Params} = K \times K \times C_{in} \times C_{out}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.2

**变体参数量对比：**

| 卷积类型 | 参数量 | $K=3, C_{in}=64, C_{out}=128$ |
|---------|--------|------|
| 标准卷积 | $K^2 \cdot C_{in} \cdot C_{out}$ | $9 \times 64 \times 128 = 73{,}728$ |
| 深度可分离 | $K^2 \cdot C_{in} + C_{in} \cdot C_{out}$ | $9 \times 64 + 64 \times 128 = 8{,}768$ |
| 1×1 卷积 | $C_{in} \cdot C_{out}$ | $64 \times 128 = 8{,}192$ |

> 📖 Paper: Chollet, [Xception](https://arxiv.org/abs/1610.02357), 2017

---

### 公式 4: 计算量 (FLOPs)

**直觉：** 每个输出像素需要 $K \times K \times C_{in}$ 次乘加，总共有 $H_{out} \times W_{out} \times C_{out}$ 个输出像素。

$$
\text{FLOPs} = 2 \times K^2 \times C_{in} \times C_{out} \times H_{out} \times W_{out}
$$

（乘 2 因为每次乘加 = 1 乘法 + 1 加法）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

---

### 公式 5: 感受野递推公式

**直觉：** 深层神经元"看到"的原始输入区域有多大？每多一层卷积，感受野增长取决于核大小和步长。

$$
RF_l = RF_{l-1} + (K_l - 1) \times \prod_{i=1}^{l-1} S_i
$$

初始条件：$RF_0 = 1$（输入层一个像素对应自身）

**两层 3×3 卷积 ($S=1$) 的感受野：**

$$
RF_1 = 1 + (3-1) \times 1 = 3
$$
$$
RF_2 = 3 + (3-1) \times 1 = 5
$$

→ 两层 $3 \times 3$ 等效一层 $5 \times 5$，但参数更少！

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.4

---


## 公式关系图

```
输入 X ∈ ℝ^{C_in × H × W}
│
├─ 公式 2: 输出尺寸 O = ⌊(I-K+2P)/S⌋ + 1
│
├─ 公式 1: 卷积操作 Y[m][i][j] = Σ W·X + b
│   │
│   ├── 需要: 公式 3 (参数量 = K²·C_in·C_out)
│   └── 需要: 公式 4 (FLOPs = 2·K²·C_in·C_out·H_out·W_out)
│
└─ 公式 5: 感受野 RF_l = RF_{l-1} + (K-1)·∏S_i
           （多层堆叠时累积）
```

---


## 手算练习

### 练习 1: 计算 Conv2d 输出尺寸和参数量

**题目：** 输入 $32 \times 32 \times 3$ (CIFAR-10)，经过 `Conv2d(3, 16, kernel_size=5, stride=1, padding=2)`，求输出尺寸和参数量。

**解答步骤：**

1. 输出空间尺寸：$O = \lfloor(32 - 5 + 2 \times 2) / 1\rfloor + 1 = \lfloor 31/1 \rfloor + 1 = 32$
2. 输出形状：$16 \times 32 \times 32$（16 个通道，空间尺寸保持）
3. 参数量：$(5 \times 5 \times 3 + 1) \times 16 = 76 \times 16 = 1{,}216$

> 📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

### 练习 2: 多层 CNN 的输出尺寸追踪

**题目：** 输入 $224 \times 224 \times 3$，依次经过：
1. `Conv2d(3, 64, 7, stride=2, padding=3)` — 7×7 大核
2. `MaxPool2d(3, stride=2, padding=1)` — 池化
3. `Conv2d(64, 128, 3, stride=1, padding=1)` — 标准 3×3

求每层输出尺寸和总参数量。

**解答步骤：**

1. **Conv 7×7**：$O = \lfloor(224 - 7 + 2 \times 3) / 2\rfloor + 1 = \lfloor 223/2 \rfloor + 1 = 112$
   - 输出：$64 \times 112 \times 112$
   - 参数：$(7 \times 7 \times 3 + 1) \times 64 = 148 \times 64 = 9{,}472$

2. **MaxPool 3×3**：$O = \lfloor(112 - 3 + 2 \times 1) / 2\rfloor + 1 = \lfloor 111/2 \rfloor + 1 = 56$
   - 输出：$64 \times 56 \times 56$
   - 参数：$0$（池化无可学习参数）

3. **Conv 3×3**：$O = \lfloor(56 - 3 + 2 \times 1) / 1\rfloor + 1 = 56$
   - 输出：$128 \times 56 \times 56$
   - 参数：$(3 \times 3 \times 64 + 1) \times 128 = 577 \times 128 = 73{,}856$

4. **总参数量**：$9{,}472 + 0 + 73{,}856 = 83{,}328$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9

### 练习 3: 深度可分离卷积的参数节省

**题目：** 标准 Conv2d(64, 128, 3) vs 深度可分离卷积，计算参数量和压缩比。

**解答步骤：**

1. 标准卷积：$3 \times 3 \times 64 \times 128 = 73{,}728$
2. 深度可分离：
   - Depthwise：$3 \times 3 \times 64 = 576$
   - Pointwise：$1 \times 1 \times 64 \times 128 = 8{,}192$
   - 总计：$576 + 8{,}192 = 8{,}768$
3. 压缩比：$73{,}728 / 8{,}768 \approx 8.4 \times$（约 $K^2 = 9$ 倍）

> 📖 Paper: Chollet, [Xception](https://arxiv.org/abs/1610.02357), 2017

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 输出尺寸 | $\lfloor(I-K+2P)/S\rfloor+1$ | 设计网络时确定各层尺寸 | 无 |
| 膨胀卷积有效核 | $K + (K-1)(d-1)$ | 空洞卷积输出尺寸 | 输出尺寸 |
| 转置卷积输出 | $(I-1) \times S - 2P + K$ | 上采样后的尺寸 | 无 |
| 参数量 | $(K^2 \cdot C_{in}+1) \times C_{out}$ | 模型大小估算 | 无 |
| 深度可分离参数 | $K^2 C_{in} + C_{in} C_{out}$ | 轻量模型参数 | 参数量 |
| FLOPs | $2 K^2 C_{in} C_{out} H_o W_o$ | 计算量估算 | 输出尺寸 |
| 感受野 | $RF_l = RF_{l-1} + (K-1)\prod S_i$ | 确定感受野大小 | 无 |
| 同尺寸填充 | $P = \lfloor K/2 \rfloor$ | 保持空间尺寸 | 输出尺寸 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9
> 📖 Paper: Dumoulin & Visin, [Convolution Arithmetic](https://arxiv.org/abs/1603.07285), 2016
