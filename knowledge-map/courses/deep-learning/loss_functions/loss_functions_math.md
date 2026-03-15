---
topic: loss_functions
dimension: math
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.2, Ch.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.4 §4.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
expiry: 12m
status: current
---

# Loss Functions 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $y$ | 真实标签 | ground truth | 回归: $\mathbb{R}$; 分类: $\{0,1\}$ |
| $\hat{y}$ | 模型预测值 | prediction | 回归: $\mathbb{R}$; 分类: $(0,1)$ |
| $n$ | 样本数量 | number of samples | $\mathbb{Z}^+$ |
| $K$ | 类别数 | number of classes | $\mathbb{Z}^+, K \geq 2$ |
| $L$ | 损失值（标量） | loss value | $\mathbb{R}^+_0$ |
| $p$ | 真实概率分布 | true distribution | $[0,1]$ |
| $q$ | 模型预测分布 | predicted distribution | $(0,1)$ |
| $\sigma$ | Sigmoid 函数 | Sigmoid | $(0,1)$ |
| $z$ | 线性输出 (logits) | pre-activation output | $\mathbb{R}$ |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3, Ch.6

---


## 核心公式

### 公式 1: MSE (均方误差)

**直觉：** 把每个预测误差平方后取平均。平方让正负误差都变正，且放大大误差。

$$L_{\text{MSE}} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

**梯度推导：**

$$\frac{\partial L}{\partial \hat{y}_i} = \frac{2}{n}(\hat{y}_i - y_i)$$

**MLE 视角推导：** 假设 $y \sim \mathcal{N}(\hat{y}, \sigma^2)$：

$$
\text{Step 1: } p(y|\hat{y}) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(y-\hat{y})^2}{2\sigma^2}\right)
$$
$$
\text{Step 2: } \log p = -\frac{(y-\hat{y})^2}{2\sigma^2} + \text{const}
$$
$$
\text{Step 3: 最大化 } \log p \Leftrightarrow \text{最小化 } (y-\hat{y})^2 = \text{MSE}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.1
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1 §1.2.5

---

### 公式 2: Binary Cross-Entropy (二分类交叉熵)

**直觉：** 当模型"自信地"犯错时给出巨大惩罚——预测 0.01 但真实是 1 时，$-\log(0.01)=4.6$，而预测 0.99 时 $-\log(0.99)=0.01$。

$$L_{\text{BCE}} = -\frac{1}{n}\sum_{i=1}^{n}\left[y_i\log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)\right]$$

**梯度推导（对 Sigmoid 输出 $\hat{y} = \sigma(z)$）：**

$$
\text{Step 1: } \frac{\partial L}{\partial \hat{y}} = -\frac{y}{\hat{y}} + \frac{1-y}{1-\hat{y}}
$$
$$
\text{Step 2: } \frac{\partial \hat{y}}{\partial z} = \hat{y}(1-\hat{y}) \quad \text{(Sigmoid 导数)}
$$
$$
\text{Step 3: } \frac{\partial L}{\partial z} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} = \hat{y} - y
$$

**关键发现：** BCE + Sigmoid 的梯度简化为 $\hat{y} - y$——没有 Sigmoid 导数的 $\hat{y}(1-\hat{y})$ 项！**饱和问题被完全消除。** 这就是为什么二分类用 BCE 而不是 MSE。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

---

### 公式 3: Categorical Cross-Entropy (多分类交叉熵)

**直觉：** 只看真实类别那一项的概率。真实类别的预测概率越高，损失越低。

$$L_{\text{CCE}} = -\frac{1}{n}\sum_{i=1}^{n}\sum_{k=1}^{K} y_{i,k}\log(\hat{y}_{i,k})$$

由于 $y$ 是 one-hot，只有一项非零：

$$L_i = -\log(\hat{y}_{i,k^*}) \quad \text{其中 } k^* = \text{argmax}(y_i)$$

**梯度推导（对 Softmax 输出, 结合 logits $z$）：**

$$\frac{\partial L}{\partial z_k} = \hat{y}_k - y_k$$

**关键发现：** CCE + Softmax 的梯度也简化为 $\hat{y}_k - y_k$，与 BCE + Sigmoid 结构一致。这不是巧合——两者都源自 MLE。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4 §4.3.4

---

### 公式 4: Cross-Entropy 的信息论推导

**直觉：** 交叉熵衡量"用预测分布 $q$ 来编码服从真实分布 $p$ 的数据，平均需要多少比特"。$q$ 越接近 $p$，编码越短，交叉熵越小。

$$H(p, q) = -\sum_{k} p(k) \log q(k)$$

**与 KL 散度的关系：**

$$
H(p, q) = H(p) + D_{KL}(p \| q)
$$

- $H(p)$：真实分布的熵（常数，与模型无关）
- $D_{KL}(p \| q) \geq 0$：KL 散度（$p=q$ 时为 0）
- 因此：**最小化交叉熵 $\Leftrightarrow$ 最小化 KL 散度 $\Leftrightarrow$ 让 $q$ 逼近 $p$**

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3 §3.13

---

### 公式 5: Huber Loss

**直觉：** 误差小时像 MSE（光滑梯度），误差大时像 MAE（不被异常值带偏）。$\delta$ 是切换阈值。

$$L_\delta = \begin{cases} \frac{1}{2}(y-\hat{y})^2 & \text{if } |y-\hat{y}| \leq \delta \\ \delta|y-\hat{y}| - \frac{1}{2}\delta^2 & \text{otherwise} \end{cases}$$

**梯度：**

$$\frac{\partial L}{\partial \hat{y}} = \begin{cases} \hat{y}-y & \text{if } |y-\hat{y}| \leq \delta \\ \delta \cdot \text{sign}(\hat{y}-y) & \text{otherwise} \end{cases}$$

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.5

---


## 公式关系图

```
                  MLE (最大似然估计)
                       │
              ┌────────┼────────┐
              ▼                 ▼
     高斯似然 → MSE      Bernoulli/Categorical 似然
                              → Cross-Entropy
                       │
              ┌────────┼────────┐
              ▼                 ▼
     Binary CE               Categorical CE
     (二分类)                (多分类)
        │                       │
        ▼                       ▼
   + Sigmoid              + Softmax
   梯度 = ŷ - y           梯度 = ŷ - y
   (饱和被消除！)          (饱和被消除！)
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---


## 手算练习

### 练习 1: MSE 计算

**题目：** 真实值 $y = [3, 5, 7]$，预测值 $\hat{y} = [2.5, 5.5, 6]$。计算 MSE。

**解答：**
1. 误差：$(3-2.5)^2 = 0.25$, $(5-5.5)^2 = 0.25$, $(7-6)^2 = 1.0$
2. $\text{MSE} = \frac{0.25 + 0.25 + 1.0}{3} = \frac{1.5}{3} = 0.5$

### 练习 2: BCE 计算

**题目：** 真实标签 $y = 1$，模型预测 $\hat{y} = 0.8$。计算 BCE loss。

**解答：**
1. $L = -[1 \cdot \log(0.8) + 0 \cdot \log(0.2)]$
2. $L = -\log(0.8) = -(-0.2231) = 0.2231$
3. 如果预测 $\hat{y} = 0.2$：$L = -\log(0.2) = 1.6094$ → 错误预测的惩罚大 7 倍！

### 练习 3: CCE 计算

**题目：** 3 类分类。真实标签 $y = [0, 1, 0]$（第 2 类），Softmax 输出 $\hat{y} = [0.1, 0.7, 0.2]$。

**解答：**
1. $L = -[0 \cdot \log(0.1) + 1 \cdot \log(0.7) + 0 \cdot \log(0.2)]$
2. $L = -\log(0.7) = 0.3567$
3. 只有真实类别那一项有贡献：$-\log(0.7)$

### 练习 4: 为什么分类不用 MSE？

**题目：** 二分类, Sigmoid 输出 $\hat{y} = 0.99$，真实 $y = 0$（模型自信地预测错了）。比较 MSE 和 BCE 的梯度。

**解答：**
1. MSE 梯度 $\frac{\partial L}{\partial z}$：包含 $\sigma'(z) = \hat{y}(1-\hat{y}) = 0.99 \times 0.01 = 0.0099$ → 梯度极小！Sigmoid 饱和使梯度消失
2. BCE 梯度 $\frac{\partial L}{\partial z}$：$\hat{y} - y = 0.99 - 0 = 0.99$ → 梯度正常！
3. **结论：** BCE 消除了 Sigmoid 饱和导致的梯度消失，分类任务必须用交叉熵

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

---


## 公式速查表

| 名称 | 公式 | 梯度 $\partial L/\partial z$ | 配套激活 |
|------|------|-----|---------|
| MSE | $\frac{1}{n}\sum(y-\hat{y})^2$ | $\frac{2}{n}(\hat{y}-y)$ | Linear |
| MAE | $\frac{1}{n}\sum\|y-\hat{y}\|$ | $\text{sign}(\hat{y}-y)$ | Linear |
| BCE | $-[y\log\hat{y}+(1-y)\log(1-\hat{y})]$ | $\hat{y}-y$ (with Sigmoid) | Sigmoid |
| CCE | $-\sum y_k\log\hat{y}_k$ | $\hat{y}_k-y_k$ (with Softmax) | Softmax |
| Huber | MSE/MAE 混合 | 分段线性 | Linear |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
