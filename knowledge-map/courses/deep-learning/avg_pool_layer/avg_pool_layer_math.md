---
topic: avg_pool_layer
dimension: math
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.AvgPool2d — https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html"
expiry: 12m
status: current
---

# Avg Pool Layer 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $I$ | 输入特征图的空间尺寸 | Input size | 正整数 |
| $K$ | 池化窗口大小 | Kernel size | 通常 2 或 3 |
| $S$ | 步长 | Stride | 正整数，默认 = $K$ |
| $P$ | 边缘填充大小 | Padding | 非负整数，默认 0 |
| $O$ | 输出特征图的空间尺寸 | Output size | 正整数 |
| $C$ | 通道数 | Channels | 正整数 |
| $H, W$ | 特征图高度、宽度 | Height, Width | 正整数 |
| $x_{i,j}^c$ | 第 $c$ 通道在 $(i,j)$ 位置的输入值 | Input activation | 实数 |
| $y_{m,n}^c$ | 第 $c$ 通道在 $(m,n)$ 位置的输出值 | Output activation | 实数 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---


## 核心公式

### 公式 1: Average Pooling 前向操作

**直觉：** 在每个池化窗口内把所有值加起来再除以窗口大小，得到该区域的"平均强度"

$$
y_{m,n}^c = \frac{1}{K^2} \sum_{p=0}^{K-1} \sum_{q=0}^{K-1} x_{m \cdot S + p, \; n \cdot S + q}^{c}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $(m, n)$ | 输出特征图的空间坐标 | 输出的第 m 行第 n 列 |
| $(p, q)$ | 窗口内的相对偏移 | 从 0 到 K-1 遍历 |
| $K^2$ | 窗口内元素总数 | K=2 → 4 个元素 |

**推导过程：**

$$
\text{Step 1: 定位窗口左上角} \quad (i_0, j_0) = (m \cdot S, \; n \cdot S)
$$
$$
\text{Step 2: 求窗口内所有元素的和} \quad \text{sum} = \sum_{p=0}^{K-1} \sum_{q=0}^{K-1} x_{i_0+p, \, j_0+q}^c
$$
$$
\text{Step 3: 除以窗口大小} \quad y_{m,n}^c = \frac{\text{sum}}{K \times K}
$$

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

---

### 公式 2: Global Average Pooling

**直觉：** 对整个特征图取平均——每个通道压缩为一个标量

$$
y^c = \frac{1}{H \times W} \sum_{i=0}^{H-1} \sum_{j=0}^{W-1} x_{i,j}^{c}
$$

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $H, W$ | 输入特征图的空间尺寸 | 如 7×7 |
| $y^c$ | 第 $c$ 通道的输出标量 | 1 个浮点数 |

**推导过程：**

$$
\text{Step 1: 公式 1 中令 } K = H = W, \; S = 1, \; m = n = 0
$$
$$
\text{Step 2: 窗口覆盖整个特征图} \implies y^c = \frac{1}{HW} \sum_{\text{all } (i,j)} x_{i,j}^c
$$

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

---

### 公式 3: 输出尺寸计算

**直觉：** 与 Max Pooling 公式完全相同

$$
O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1
$$

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $I$ | 输入尺寸 | 如 28 |
| $K$ | 窗口大小 | 如 2 |
| $P$ | 填充 | 如 0 |
| $S$ | 步长 | 如 2 |

**推导过程：** 与 Max Pooling 相同，仅聚合函数不同（avg 替代 max），不影响输出尺寸计算。

> 📖 参考: [max_pool_layer_math.md](../max_pool_layer/max_pool_layer_math.md) 公式 2

---

### 公式 4: 反向传播梯度

**直觉：** 梯度均匀分配给窗口内的每个位置——每个位置贡献 $1/K^2$ 的权重

$$
\frac{\partial \mathcal{L}}{\partial x_{i,j}^c} = \sum_{(m,n) : (i,j) \in \text{window}_{m,n}} \frac{1}{K^2} \cdot \frac{\partial \mathcal{L}}{\partial y_{m,n}^c}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5 + Ch.9.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\frac{1}{K^2}$ | 每个位置的均等贡献系数 | K=2 → 0.25 |
| $(m,n)$ 范围 | 所有包含 $(i,j)$ 的池化窗口 | 重叠池化时可能有多个 |

**推导过程：**

$$
\text{Step 1: } y_{m,n}^c = \frac{1}{K^2} \sum x \implies \frac{\partial y}{\partial x_{i,j}} = \frac{1}{K^2} \quad \text{(对窗口内每个 } x \text{)}
$$
$$
\text{Step 2: 链式法则} \quad \frac{\partial \mathcal{L}}{\partial x_{i,j}^c} = \sum_{(m,n)} \frac{\partial \mathcal{L}}{\partial y_{m,n}^c} \cdot \frac{1}{K^2}
$$
$$
\text{Step 3: 关键区别 — 所有位置都收到梯度}
$$
$$
\text{vs Max Pooling: 仅 argmax 位置收到梯度（其余 = 0）}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 公式关系图

```
公式 1 (局部 AvgPool) ──特例──→ 公式 2 (GAP, K=H=W)
     │
     ├──尺寸──→ 公式 3 (输出大小，与 MaxPool 相同)
     │
     └──反向──→ 公式 4 (梯度均匀分配 1/K²)
```

---


## 手算练习

### 练习 1: 2D Average Pooling 前向计算

**题目：** 输入 4×4 特征图（1个通道），kernel=2, stride=2, padding=0，求输出。

```
输入:
 1  3  2  4
 5  6  7  8
 9  2  1  0
 3  4  5  6
```

**解答步骤：**

1. 代入公式 3 求输出尺寸: $O = \lfloor(4-2)/2\rfloor + 1 = 2$，输出为 2×2
2. 窗口 (0,0): avg(1,3,5,6) = 15/4 = **3.75**
3. 窗口 (0,1): avg(2,4,7,8) = 21/4 = **5.25**
4. 窗口 (1,0): avg(9,2,3,4) = 18/4 = **4.50**
5. 窗口 (1,1): avg(1,0,5,6) = 12/4 = **3.00**

```
输出:
 3.75  5.25
 4.50  3.00
```

**对比 Max Pooling 的同一输入: [[6, 8], [9, 6]]** — Average 更平滑，极值被平均掉了。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

### 练习 2: Global Average Pooling

**题目：** 输入 2×2 特征图，2个通道，求 GAP 输出。

```
通道 0:          通道 1:
 4  6            1  3
 2  8            5  7
```

**解答步骤：**

1. 通道 0: GAP = (4+6+2+8) / 4 = **5.0**
2. 通道 1: GAP = (1+3+5+7) / 4 = **4.0**
3. 输出: [5.0, 4.0]（形状从 2×2×2 变为 2）

> 📖 Paper: Lin et al., [Network in Network](https://arxiv.org/abs/1312.4400), ICLR 2014

### 练习 3: 梯度反传

**题目：** 接练习 1，假设上游梯度 $\frac{\partial \mathcal{L}}{\partial y} = \begin{bmatrix} 0.4 & 0.8 \\ 1.2 & 1.6 \end{bmatrix}$，求输入的梯度。

**解答步骤：**

1. 每个窗口的梯度均匀分成 4 份（$1/K^2 = 1/4 = 0.25$）
2. 窗口 (0,0): 0.4 × 0.25 = 0.1 分配给 4 个位置
3. 窗口 (0,1): 0.8 × 0.25 = 0.2 分配给 4 个位置
4. 窗口 (1,0): 1.2 × 0.25 = 0.3 分配给 4 个位置
5. 窗口 (1,1): 1.6 × 0.25 = 0.4 分配给 4 个位置

```
输入梯度:
 0.1  0.1  0.2  0.2
 0.1  0.1  0.2  0.2
 0.3  0.3  0.4  0.4
 0.3  0.3  0.4  0.4
```

**对比 Max Pooling: 梯度是稀疏的（仅 argmax 位置非零）**；Average Pooling 梯度是密集的（所有位置均有梯度）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 局部 AvgPool | $y_{m,n}^c = \frac{1}{K^2}\sum_{p,q} x_{mS+p,nS+q}^c$ | 空间下采样 | 无 |
| Global Avg Pool | $y^c = \frac{1}{HW}\sum_{i,j} x_{i,j}^c$ | 替代 FC 层 | 公式 1 特例 |
| 输出尺寸 | $O = \lfloor(I-K+2P)/S\rfloor + 1$ | 计算输出维度 | 无 |
| 梯度传播 | $\partial\mathcal{L}/\partial x_{i,j} = (1/K^2) \cdot \partial\mathcal{L}/\partial y$ | 反向传播 | 公式 1 |

> 📖 Docs: [PyTorch nn.AvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html)
