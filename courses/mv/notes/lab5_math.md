# Lab 5 — CNN (Convolutional Neural Network, 卷积神经网络) 数学公式

> **See also:** [lab5_cheatsheet.md](lab5_cheatsheet.md) · [lab5_code.md](lab5_code.md) · [Lab 文档](../labs/CST8508_Lab5.md)
>
> ❌ 本文件不含概念定义、不含代码 — 仅公式推导和手算练习

---

## 📐 公式汇总（Formulas）

### 1. 卷积输出尺寸（Convolution Output Size）

$$
W_{out} = \left\lfloor \frac{W_{in} - K + 2P}{S} \right\rfloor + 1
$$

| 符号 | 含义 | Lab 5 中的值 |
|------|------|-------------|
| $W_{out}$ | 输出特征图宽度 | 动态计算 |
| $W_{in}$ | 输入特征图宽度 | e.g., 128 |
| $K$ | 卷积核大小 (kernel size) | 3 |
| $P$ | 填充大小 (padding) | 1 (`padding=1`) |
| $S$ | 步长 (stride) | 1（默认）|

> 高度方向公式相同：$H_{out} = \lfloor (H_{in} - K + 2P) / S \rfloor + 1$

---

### 2. MaxPooling 输出尺寸

$$
W_{out} = \left\lfloor \frac{W_{in}}{K_{pool}} \right\rfloor
$$

| 符号 | 含义 | Lab 5 中的值 |
|------|------|-------------|
| $K_{pool}$ | 池化窗口大小 | 2 (`MaxPool2d(2, 2)`) |

> 步长默认等于窗口大小，所以尺寸减半。

---

### 3. 卷积层参数量

$$
\text{Params} = (K \times K \times C_{in} \times C_{out}) + C_{out}
$$

| 符号 | 含义 |
|------|------|
| $K$ | 卷积核大小 |
| $C_{in}$ | 输入通道数 |
| $C_{out}$ | 输出通道数（滤波器数量）|
| $+C_{out}$ | 偏置项（bias terms）|

---

### 4. 全连接层参数量

$$
\text{Params} = (n_{in} \times n_{out}) + n_{out}
$$

| 符号 | 含义 |
|------|------|
| $n_{in}$ | 输入节点数 |
| $n_{out}$ | 输出节点数 |
| $+n_{out}$ | 偏置项 |

---

### 5. ReLU 激活函数

$$
f(x) = \max(0, x) = \begin{cases} x & x > 0 \\ 0 & x \le 0 \end{cases}
$$

导数：

$$
f'(x) = \begin{cases} 1 & x > 0 \\ 0 & x \le 0 \end{cases}
$$

---

### 6. Softmax（模型内部使用）

$$
\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{C} e^{z_j}}
$$

| 符号 | 含义 |
|------|------|
| $z_i$ | 第 $i$ 个类别的原始 logit |
| $C$ | 类别总数（Lab 5 中 $C=2$）|

> ⚠️ Lab 5 的 `CrossEntropyLoss` 内部已包含 Softmax，不需要手动调用。

---

### 7. 交叉熵损失（Cross-Entropy Loss）

$$
\mathcal{L} = -\sum_{i=1}^{C} y_i \log(\hat{p}_i)
$$

对于二分类（$C=2$），真实标签为 one-hot 向量（如 $y=[1, 0]$ 表示猫）：

$$
\mathcal{L} = -\log(\hat{p}_{correct\_class})
$$

| 符号 | 含义 |
|------|------|
| $y_i$ | 真实标签（one-hot：正确类为 1，其余为 0）|
| $\hat{p}_i$ | 预测概率（Softmax 输出）|
| $C$ | 类别数 |

PyTorch 版本直接从 logits 计算：

$$
\mathcal{L} = -z_{correct} + \log\left(\sum_{j} e^{z_j}\right)
$$

---

### 8. Dropout

$$
\tilde{h}_i = \begin{cases} \frac{h_i}{1-p} & \text{以概率 } (1-p) \text{ 保留} \\ 0 & \text{以概率 } p \text{ 丢弃} \end{cases}
$$

| 符号 | 含义 |
|------|------|
| $h_i$ | 第 $i$ 个神经元的激活值 |
| $p$ | 丢弃概率（Lab 5 中 $p=0.5$）|
| $\frac{1}{1-p}$ | 缩放因子（保证期望值不变）|

---

### 9. Adam 优化器更新规则

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \quad \text{(一阶矩，动量)}
$$

$$
v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \quad \text{(二阶矩，方差)}
$$

$$
\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t} \quad \text{(偏差修正)}
$$

$$
\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t
$$

| 符号 | 含义 | 默认值 |
|------|------|--------|
| $g_t$ | 第 $t$ 步梯度 | — |
| $\beta_1$ | 一阶矩衰减系数 | 0.9 |
| $\beta_2$ | 二阶矩衰减系数 | 0.999 |
| $\alpha$ | 学习率 (lr) | 1e-3（Lab 5）|
| $\epsilon$ | 数值稳定项 | 1e-8 |

---

### 10. 分类评估指标

$$
\text{Precision} = \frac{TP}{TP + FP}
$$

$$
\text{Recall} = \frac{TP}{TP + FN}
$$

$$
\text{F1} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}
$$

$$
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
$$

| 缩写 | 含义 |
|------|------|
| TP (True Positive, 真阳性) | 预测为正类，实际也是正类 |
| FP (False Positive, 假阳性) | 预测为正类，实际是负类（误报）|
| FN (False Negative, 假阴性) | 预测为负类，实际是正类（漏报）|
| TN (True Negative, 真阴性) | 预测为负类，实际也是负类 |

---

## 📝 手算练习（Hand Calculations）

### 练习 1：计算 SimpleCNN 各层输出形状

**输入：** 3 × 128 × 128

**Step 1 — Conv2d(3, 32, kernel=3, padding=1) + MaxPool2d(2)**

卷积后：
$$W_{out} = \left\lfloor \frac{128 - 3 + 2 \times 1}{1} \right\rfloor + 1 = 128$$

池化后：
$$W_{out} = \left\lfloor \frac{128}{2} \right\rfloor = 64$$

形状：$32 \times 64 \times 64$

**Step 2 — Conv2d(32, 64, kernel=3, padding=1) + MaxPool2d(2)**

卷积后：$64$，池化后：$32$ → 形状：$64 \times 32 \times 32$

**Step 3 — Conv2d(64, 128, kernel=3, padding=1) + MaxPool2d(2)**

卷积后：$32$，池化后：$16$ → 形状：$128 \times 16 \times 16$

**Flatten：** $128 \times 16 \times 16 = \mathbf{32,768}$

---

### 练习 2：计算各层参数量

**Conv2d(3, 32, 3, padding=1)**

$$\text{Params} = (3 \times 3 \times 3 \times 32) + 32 = 864 + 32 = \mathbf{896}$$

**Conv2d(32, 64, 3, padding=1)**

$$\text{Params} = (3 \times 3 \times 32 \times 64) + 64 = 18{,}432 + 64 = \mathbf{18{,}496}$$

**Conv2d(64, 128, 3, padding=1)**

$$\text{Params} = (3 \times 3 \times 64 \times 128) + 128 = 73{,}728 + 128 = \mathbf{73{,}856}$$

**Linear(32768, 256)**

$$\text{Params} = (32{,}768 \times 256) + 256 = 8{,}388{,}608 + 256 = \mathbf{8{,}389{,}120}$$

**Linear(256, 2)**

$$\text{Params} = (256 \times 2) + 2 = 512 + 2 = \mathbf{514}$$

**Total:**

$$896 + 18{,}496 + 73{,}856 + 8{,}389{,}120 + 514 = \mathbf{8{,}482{,}882} \approx 8.48\text{M}$$

---

### 练习 3：手算 Cross-Entropy Loss（单样本）

**场景：** 模型对一张猫图输出 logits = $[2.1,\ 0.3]$（猫=0, 狗=1），真实标签 = 0（猫）

**Step 1 — Softmax**

$$e^{2.1} = 8.166, \quad e^{0.3} = 1.350, \quad \text{sum} = 9.516$$

$$\hat{p}_0 = \frac{8.166}{9.516} = 0.858, \quad \hat{p}_1 = \frac{1.350}{9.516} = 0.142$$

**Step 2 — Cross-Entropy**

$$\mathcal{L} = -\log(\hat{p}_0) = -\log(0.858) = \mathbf{0.153}$$

**直觉：** 损失越低，模型对正确类别越自信。若 $\hat{p}_0 \to 1$，则 $\mathcal{L} \to 0$。

---

### 练习 4：从混淆矩阵计算 Precision / Recall（猫类）

**场景（简化版）：**

|  | 预测猫 | 预测狗 |
|--|--------|--------|
| **真实猫** | TP = 2130 | FN = 348 |
| **真实狗** | FP = 228 | TN = 2294 |

$$\text{Precision}_{Cat} = \frac{2130}{2130 + 228} = \frac{2130}{2358} \approx 0.903$$

$$\text{Recall}_{Cat} = \frac{2130}{2130 + 348} = \frac{2130}{2478} \approx 0.860$$

$$\text{F1}_{Cat} = \frac{2 \times 0.903 \times 0.860}{0.903 + 0.860} = \frac{1.553}{1.763} \approx 0.881$$

> 与实际输出 `Cat: precision=0.90, recall=0.86, f1=0.88` 吻合。

---

## 📋 公式快速参考表（Quick Reference Table）

| 公式 | 用途 | 关键符号 |
|------|------|---------|
| $W_{out} = \lfloor(W_{in}-K+2P)/S\rfloor+1$ | 卷积输出尺寸 | $K$=核大小，$P$=填充，$S$=步长 |
| $W_{out} = \lfloor W_{in}/K_{pool} \rfloor$ | 池化输出尺寸 | $K_{pool}$=池化窗口 |
| $(K^2 \cdot C_{in} \cdot C_{out}) + C_{out}$ | 卷积层参数量 | 含 bias |
| $(n_{in} \cdot n_{out}) + n_{out}$ | 全连接层参数量 | 含 bias |
| $\max(0, x)$ | ReLU | 负值归零 |
| $-\log(\hat{p}_{correct})$ | 交叉熵（单样本）| logit → softmax → 取正确类 |
| $TP/(TP+FP)$ | Precision (精确率) | 预测为正中真正 |
| $TP/(TP+FN)$ | Recall (召回率) | 实际为正中被找到的 |
| $2PR/(P+R)$ | F1-Score | Precision 和 Recall 的调和均值 |
