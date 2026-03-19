---
topic: imagenet
dimension: math
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Russakovsky et al., IJCV 2015 — https://arxiv.org/abs/1409.0575"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.3, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Krizhevsky et al., NeurIPS 2012 — https://arxiv.org/abs/1209.0270"
expiry: 12m
status: current
---

# ImageNet 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3, Ch.6
> 📖 Paper: Russakovsky et al., [ILSVRC](https://arxiv.org/abs/1409.0575), IJCV 2015

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $K$ | 总类别数 | Number of classes | ILSVRC: $K = 1000$ |
| $k$ | Top-k 中的 k 值 | Top-k parameter | 1 或 5（通常） |
| $y$ | 真实标签（整数） | Ground truth label | $y \in \{1, 2, ..., K\}$ |
| $\hat{y}$ | 模型预测标签 | Predicted label | $\hat{y} \in \{1, 2, ..., K\}$ |
| $z_i$ | 第 $i$ 类的 logit（未归一化分数） | Logit for class $i$ | $z_i \in \mathbb{R}$ |
| $p_i$ | 第 $i$ 类的预测概率 | Predicted probability for class $i$ | $p_i \in [0, 1]$, $\sum p_i = 1$ |
| $N$ | 评估样本总数 | Total evaluation samples | ILSVRC: $N = 50000$（验证集） |
| $\mathbb{1}[\cdot]$ | 指示函数，条件成立为 1 | Indicator function | $\{0, 1\}$ |
| $\mathcal{L}$ | 损失函数值 | Loss value | $\mathcal{L} \geq 0$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3 "Probability", Ch.6 "Deep Feedforward Networks"

---

## 核心公式

### 公式 1: Softmax 函数

**直觉：** 把 K 个任意实数（logits）变成 K 个概率值（0~1 之间，且和为 1），告诉你模型觉得每个类多"自信"。

$$
p_i = \text{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Eq. 6.29

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $z_i$ | 第 $i$ 类的原始分数 (logit) | 模型最后一层输出的第 $i$ 个值 |
| $K$ | 类别总数 | ImageNet 中 $K = 1000$ |
| $p_i$ | 第 $i$ 类的概率 | 0.85 表示模型 85% 认为是第 $i$ 类 |

**推导过程：**

1. 模型输出 logits $z = [z_1, z_2, ..., z_K]$（任意实数）
2. 为了变成概率，需要满足：(a) 非负 (b) 和为 1
3. 用指数 $e^{z_i}$ 保证非负（$e^x > 0$ 对所有 $x$）
4. 除以 $\sum e^{z_j}$ 保证和为 1
5. 结果：$p_i = e^{z_i} / \sum e^{z_j}$ 就是 softmax

**数值稳定性技巧：** 实际计算时用 $z_i - \max(z)$ 替代 $z_i$，避免 $e^{z_i}$ 溢出。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.4.1 "Numerical Stability"

---

### 公式 2: 交叉熵损失（分类任务）

**直觉：** 衡量模型的预测概率分布和真实标签之间"差多远"。真实类别的概率越高，损失越小。

$$
\mathcal{L}_{\text{CE}} = -\log(p_y) = -\log\left(\frac{e^{z_y}}{\sum_{j=1}^{K} e^{z_j}}\right)
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Eq. 6.30

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $p_y$ | 真实类别 $y$ 的预测概率 | 模型对正确答案给了多少概率 |
| $z_y$ | 真实类别 $y$ 的 logit | 模型最后一层对正确答案的原始分数 |

**推导过程：**

1. 目标：让模型对真实类别给高概率
2. 真实分布是 one-hot：$q = [0, ..., 1, ..., 0]$（只有第 $y$ 位是 1）
3. 交叉熵定义：$H(q, p) = -\sum_i q_i \log p_i$
4. 因为只有 $q_y = 1$，其余为 0，所以简化为 $-\log p_y$
5. 当 $p_y \to 1$ 时，$\mathcal{L} \to 0$（完美预测）
6. 当 $p_y \to 0$ 时，$\mathcal{L} \to +\infty$（完全错误，重罚）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3.13 "Information Theory"

---

### 公式 3: Top-1 准确率

**直觉：** 模型猜得最自信的那个答案对了吗？对的比例就是 Top-1 准确率。

$$
\text{Acc}_{\text{top-1}} = \frac{1}{N} \sum_{n=1}^{N} \mathbb{1}[\hat{y}_n = y_n]
$$

其中 $\hat{y}_n = \arg\max_i p_i^{(n)}$

> 📖 Paper: Russakovsky et al., [ILSVRC](https://arxiv.org/abs/1409.0575), Section 3.2 "Evaluation Metrics"

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $N$ | 测试样本总数 | ILSVRC 验证集 50,000 张 |
| $\hat{y}_n$ | 第 $n$ 张图的预测标签 | 概率最高的那个类 |
| $y_n$ | 第 $n$ 张图的真实标签 | 人工标注的类别 |
| $\mathbb{1}[\cdot]$ | 指示函数 | 猜对了=1，猜错了=0 |

---

### 公式 4: Top-5 准确率

**直觉：** 给模型 5 次机会猜，只要有一次猜对就算对。因为 ImageNet 有很多长得几乎一样的类（120 种狗），所以 ILSVRC 用 Top-5 作为主要指标。

$$
\text{Acc}_{\text{top-5}} = \frac{1}{N} \sum_{n=1}^{N} \mathbb{1}[y_n \in \text{Top5}(\mathbf{p}^{(n)})]
$$

其中 $\text{Top5}(\mathbf{p})$ 是概率最高的前 5 个类别的集合。

> 📖 Paper: Russakovsky et al., [ILSVRC](https://arxiv.org/abs/1409.0575), Section 3.2

**ILSVRC 排名指标：** Top-5 错误率 $= 1 - \text{Acc}_{\text{top-5}}$

---

### 公式 5: ImageNet 标准归一化

**直觉：** ImageNet 训练集的 RGB 通道均值和标准差，用于在训练/推理前统一图像的数值分布。不做归一化 = 模型看到的数值范围乱七八糟。

$$
x_{\text{norm}}^{(c)} = \frac{x^{(c)} - \mu^{(c)}}{\sigma^{(c)}}
$$

其中 ImageNet 统计值为：

$$
\mu = [0.485, 0.456, 0.406], \quad \sigma = [0.229, 0.224, 0.225]
$$

> 📖 Docs: [PyTorch torchvision transforms](https://pytorch.org/vision/stable/transforms.html) — `Normalize(mean, std)`

**参数解释：**

| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $x^{(c)}$ | 第 $c$ 通道原始像素值 (0~1) | R/G/B 通道 |
| $\mu^{(c)}$ | 第 $c$ 通道在 ImageNet 上的均值 | R=0.485, G=0.456, B=0.406 |
| $\sigma^{(c)}$ | 第 $c$ 通道在 ImageNet 上的标准差 | R=0.229, G=0.224, B=0.225 |

---

## 公式关系图

```
Logits z = [z_1, ..., z_K]
       │
       ▼
   Softmax (公式 1)
       │
       ▼
概率 p = [p_1, ..., p_K]  ──→  Top-1/Top-5 (公式 3, 4)  ──→  准确率
       │
       ▼
  交叉熵损失 (公式 2)  ──→  反向传播 ──→ 更新权重
       │
       └── 前提: 输入已用 ImageNet 均值/标准差归一化 (公式 5)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.2 "Gradient-Based Learning"

---

## 手算练习

### 练习 1: Softmax 计算

**题目：** 模型对 3 个类输出 logits $z = [2.0, 1.0, 0.1]$，计算 softmax 概率。

**解答步骤：**

1. 计算 $e^{z_i}$：$e^{2.0} = 7.389$, $e^{1.0} = 2.718$, $e^{0.1} = 1.105$
2. 求和：$\sum = 7.389 + 2.718 + 1.105 = 11.212$
3. 归一化：$p_1 = 7.389/11.212 = 0.659$, $p_2 = 2.718/11.212 = 0.242$, $p_3 = 1.105/11.212 = 0.099$
4. 验证：$0.659 + 0.242 + 0.099 = 1.000$ ✅

### 练习 2: 交叉熵损失

**题目：** 承接练习 1，真实标签是类别 1 ($y=1$)。计算交叉熵损失。

**解答步骤：**

1. 真实类别概率：$p_y = p_1 = 0.659$
2. 损失：$\mathcal{L} = -\log(0.659) = 0.417$
3. 如果纠正为 $p_y = 0.99$：$\mathcal{L} = -\log(0.99) = 0.010$（损失很小）
4. 如果 $p_y = 0.01$：$\mathcal{L} = -\log(0.01) = 4.605$（损失很大）

### 练习 3: Top-5 判断

**题目：** 模型预测的概率最高的 5 个类 = {猫, 狗, 虎, 豹, 狮}，真实标签是"虎"。Top-1 对吗？Top-5 对吗？

**解答步骤：**

1. Top-1 预测 = 猫（概率最高），真实 = 虎 → Top-1 ❌
2. Top-5 = {猫, 狗, 虎, 豹, 狮}，真实 = 虎 ∈ Top-5 → Top-5 ✅

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| Softmax | $p_i = e^{z_i} / \sum e^{z_j}$ | logit → 概率 | — |
| 交叉熵 | $\mathcal{L} = -\log(p_y)$ | 分类训练损失 | Softmax |
| Top-1 准确率 | $\frac{1}{N}\sum \mathbb{1}[\hat{y}=y]$ | 评估指标 | Softmax |
| Top-5 准确率 | $\frac{1}{N}\sum \mathbb{1}[y \in \text{Top5}]$ | ILSVRC 排名 | Softmax |
| ImageNet 归一化 | $(x - \mu) / \sigma$ | 输入预处理 | — |
