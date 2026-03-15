---
topic: max_pool_layer
dimension: math
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.9.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.MaxPool2d — https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html"
expiry: 12m
status: current
---

# Max Pool Layer 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $I$ | 输入特征图的空间尺寸（宽或高） | Input size | 正整数 |
| $K$ | 池化窗口大小 | Kernel size / Pool size | 通常 2 或 3 |
| $S$ | 步长 | Stride | 正整数，默认 = $K$ |
| $P$ | 边缘填充大小 | Padding | 非负整数，默认 0 |
| $D$ | 膨胀系数 | Dilation | 正整数，默认 1 |
| $O$ | 输出特征图的空间尺寸 | Output size | 正整数 |
| $C$ | 通道数 | Channels | 正整数 |
| $x_{i,j}^c$ | 第 $c$ 通道在 $(i,j)$ 位置的输入值 | Input activation | 实数 |
| $y_{m,n}^c$ | 第 $c$ 通道在 $(m,n)$ 位置的输出值 | Output activation | 实数 |
| $(i^*, j^*)$ | 窗口内取最大值的位置（argmax） | Argmax position | 整数坐标 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

---


## 核心公式

### 公式 1: Max Pooling 前向操作

**直觉：** 在每个池化窗口内找到最大值，作为该窗口的输出代表

$$
y_{m,n}^c = \max_{0 \le p < K, \; 0 \le q < K} \; x_{m \cdot S + p, \; n \cdot S + q}^{c}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $(m, n)$ | 输出特征图的空间坐标 | 输出的第 m 行第 n 列 |
| $(p, q)$ | 窗口内的相对偏移 | 从 0 到 K-1 遍历 |
| $S$ | 步长 | 决定窗口起始位置 |
| $c$ | 通道索引 | 每个通道独立池化 |

**推导过程：**

$$
\text{Step 1: 定位窗口左上角} \quad (i_0, j_0) = (m \cdot S, \; n \cdot S)
$$
$$
\text{Step 2: 遍历窗口内所有元素} \quad \{x_{i_0+p, \, j_0+q}^c \mid 0 \le p,q < K\}
$$
$$
\text{Step 3: 取最大值} \quad y_{m,n}^c = \max \text{ of the set above}
$$

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---

### 公式 2: 输出尺寸计算（无 dilation）

**直觉：** 用输入尺寸减去窗口大小，加上两侧填充，除以步长，再加 1

$$
O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1
$$

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $I$ | 输入尺寸 | 如 224 |
| $K$ | 窗口大小 | 如 2 |
| $P$ | 填充 | 如 0 |
| $S$ | 步长 | 如 2 |

**推导过程：**

$$
\text{Step 1: 有效输入长度（加填充）} \quad I_{eff} = I + 2P
$$
$$
\text{Step 2: 第一个窗口覆盖 K 个像素，剩余 } I_{eff} - K \text{ 个像素}
$$
$$
\text{Step 3: 每移动 S 步产生一个输出} \quad \text{额外窗口数} = \left\lfloor \frac{I_{eff} - K}{S} \right\rfloor
$$
$$
\text{Step 4: 总输出数 = 1（第一个窗口）+ 额外窗口数} = \left\lfloor \frac{I + 2P - K}{S} \right\rfloor + 1
$$

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---

### 公式 3: 输出尺寸计算（含 dilation）

**直觉：** dilation 让窗口"膨胀"，等效窗口大小变为 $K + (K-1)(D-1)$

$$
O = \left\lfloor \frac{I + 2P - D \cdot (K - 1) - 1}{S} \right\rfloor + 1
$$

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $D$ | 膨胀系数 | 如 2 |
| $D \cdot (K-1) + 1$ | 等效窗口大小 | $D=2, K=3 → 5$ |

**推导过程：**

$$
\text{Step 1: 膨胀后等效窗口大小} \quad K_{eff} = D \cdot (K - 1) + 1
$$
$$
\text{Step 2: 代入基本公式} \quad O = \left\lfloor \frac{I + 2P - K_{eff}}{S} \right\rfloor + 1
$$
$$
\text{Step 3: 展开} \quad O = \left\lfloor \frac{I + 2P - D(K-1) - 1}{S} \right\rfloor + 1
$$

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---

### 公式 4: 反向传播梯度

**直觉：** 梯度只流向窗口内最大值所在的位置，其余位置梯度为零

$$
\frac{\partial \mathcal{L}}{\partial x_{i,j}^c} = \sum_{(m,n) : (i,j) = \arg\max} \frac{\partial \mathcal{L}}{\partial y_{m,n}^c}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $\mathcal{L}$ | 损失函数 | 如交叉熵 |
| $\frac{\partial \mathcal{L}}{\partial y_{m,n}^c}$ | 上游梯度 | 来自下一层 |
| $(i,j) = \arg\max$ | 仅当 $(i,j)$ 是窗口最大值位置 | 记录在前向的 argmax 中 |

**推导过程：**

$$
\text{Step 1: } y_{m,n}^c = \max_{\text{window}} x \implies \frac{\partial y}{\partial x_{i,j}} = \begin{cases} 1 & \text{if } (i,j) = \arg\max \\ 0 & \text{otherwise} \end{cases}
$$
$$
\text{Step 2: 链式法则} \quad \frac{\partial \mathcal{L}}{\partial x_{i,j}^c} = \sum_{(m,n)} \frac{\partial \mathcal{L}}{\partial y_{m,n}^c} \cdot \frac{\partial y_{m,n}^c}{\partial x_{i,j}^c}
$$
$$
\text{Step 3: 仅 argmax 位置贡献} \implies \text{稀疏梯度，非最大值位置的权重得不到更新}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5 + Ch.9.3

---


## 公式关系图

```
公式 2 (输出尺寸-基本)
     │
     ├──扩展──→ 公式 3 (输出尺寸-含 dilation)
     │
公式 1 (前向操作 max)
     │
     └──反向──→ 公式 4 (梯度传播 argmax)
```

---


## 手算练习

### 练习 1: 2D Max Pooling 前向计算

**题目：** 输入 4×4 特征图（1个通道），kernel=2, stride=2, padding=0，求输出。

```
输入:
 1  3  2  4
 5  6  7  8
 9  2  1  0
 3  4  5  6
```

**解答步骤：**

1. 代入公式 2 求输出尺寸: $O = \lfloor(4 - 2 + 0) / 2\rfloor + 1 = 2$，输出为 2×2
2. 窗口 (0,0): max(1,3,5,6) = **6**
3. 窗口 (0,1): max(2,4,7,8) = **8**
4. 窗口 (1,0): max(9,2,3,4) = **9**
5. 窗口 (1,1): max(1,0,5,6) = **6**

```
输出:
 6  8
 9  6
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3

### 练习 2: 梯度反传

**题目：** 接练习 1，假设上游梯度 $\frac{\partial \mathcal{L}}{\partial y} = \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.4 \end{bmatrix}$，求输入的梯度。

**解答步骤：**

1. 记录前向的 argmax 位置: (1,1)=6, (0,3)=8, (2,0)=9, (3,3)=6
2. 梯度只传给 argmax 位置: 其余位置梯度=0

```
输入梯度:
 0    0    0    0
 0    0.1  0    0.2
 0.3  0    0    0
 0    0    0    0.4
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### 练习 3: 输出尺寸计算

**题目：** 输入 $I=112$，kernel=3, stride=2, padding=1，求输出尺寸。

**解答步骤：**

1. 代入公式 2: $O = \lfloor(112 - 3 + 2 \times 1) / 2\rfloor + 1$
2. 计算: $O = \lfloor 111 / 2 \rfloor + 1 = 55 + 1 = 56$
3. 输出尺寸为 56

> 📖 Docs: [PyTorch nn.MaxPool2d](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html)

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 前向操作 | $y_{m,n}^c = \max_{p,q \in [0,K)} x_{mS+p, nS+q}^c$ | 计算池化输出 | 无 |
| 输出尺寸（基本） | $O = \lfloor(I - K + 2P) / S\rfloor + 1$ | 计算输出维度 | 无 |
| 输出尺寸（含 dilation） | $O = \lfloor(I + 2P - D(K-1) - 1) / S\rfloor + 1$ | 含膨胀的输出维度 | 公式 2 |
| 梯度传播 | $\partial \mathcal{L}/\partial x_{i,j} = \mathbb{1}_{(i,j)=\arg\max} \cdot \partial \mathcal{L}/\partial y$ | 反向传播 | 公式 1 |
| 常用配置 | $K=2, S=2, P=0 \implies O = I/2$ | 尺寸减半 | 公式 2 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9.3
