---
topic: knn
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cover & Hart, 'Nearest Neighbor Pattern Classification', IEEE Trans. Inform. Theory 1967 — ⚠️ 待下载 见 papers_index.md"
  - "📚 Book: Hastie, Tibshirani, Friedman, 《ESL》 Ch.2 §2.3, Ch.13 §13.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Murphy, 《PML1》 Ch.16 §16.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 12m
status: current
---

# KNN 数学基础

> 📚 Book: Hastie et al., [《The Elements of Statistical Learning》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3, Ch.13 §13.3
> 📖 Paper: Cover & Hart (1967) — Nearest Neighbor Pattern Classification ⚠️ 待下载

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $n$ | 训练样本总数 | sample count | $n \geq 1$ |
| $d$ | 特征维度 | feature dimension | $d \geq 1$ |
| $k$ | 邻居数量 | number of neighbors | $1 \leq k \leq n$ |
| $\mathbf{x}$ | 查询点特征向量 | query point | $\mathbf{x} \in \mathbb{R}^d$ |
| $\mathbf{x}_i$ | 第 $i$ 个训练点 | training point | $\mathbf{x}_i \in \mathbb{R}^d$ |
| $y_i$ | 第 $i$ 个训练点的标签 | label | 分类：离散，回归：连续 |
| $\mathcal{N}_k(\mathbf{x})$ | 距离 $\mathbf{x}$ 最近的 k 个邻居集合 | k-neighborhood | $|\mathcal{N}_k(\mathbf{x})| = k$ |
| $D(\mathbf{x}, \mathbf{x}_i)$ | 两点之间的距离 | distance | $D \geq 0$ |
| $p$ | Minkowski 距离的幂次 | Minkowski order | $p \geq 1$ |
| $w_i$ | 第 $i$ 个邻居的权重 | weight | $w_i \geq 0$ |
| $C$ | 分类类别数 | number of classes | $C \geq 2$ |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3

---

## 核心公式

### 公式 1: Minkowski 距离

**直觉：** 统一了欧氏距离和曼哈顿距离的通用距离公式，通过参数 $p$ 控制对大偏差分量的敏感程度

$$
D_p(\mathbf{x}, \mathbf{x}_i) = \left( \sum_{j=1}^{d} |x_j - x_{ij}|^p \right)^{1/p}
$$

> 📚 Book: Hastie et al., Eq. 2.25-2.28（ESL Ch.2）

**参数解释：**

| 参数 | 含义 | 特殊情况 |
|------|------|---------|
| $p=1$ | 曼哈顿距离（逐维度差值之和） | 稀疏/高维数据 |
| $p=2$ | 欧氏距离（几何直线距离） | sklearn 默认 |
| $p \to \infty$ | Chebyshev 距离（最大维度差值） | 棋盘距离 |

**推导过程（$p=2$ 欧氏距离展开）：**

$$
\text{Step 1: } D_2 = \left( \sum_{j=1}^{d} (x_j - x_{ij})^2 \right)^{1/2}
$$

$$
\text{Step 2: 展开向量内积} = \sqrt{(\mathbf{x} - \mathbf{x}_i)^\top (\mathbf{x} - \mathbf{x}_i)}
$$

$$
\text{Step 3: } = \sqrt{\|\mathbf{x}\|^2 - 2\mathbf{x}^\top \mathbf{x}_i + \|\mathbf{x}_i\|^2}
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3

---

### 公式 2: KNN 分类预测（多数投票）

**直觉：** 统计 k 个邻居中各类别出现次数，选出现最多的类别作为预测结果

$$
\hat{y} = \arg\max_{c \in \{1,\ldots,C\}} \sum_{i \in \mathcal{N}_k(\mathbf{x})} \mathbf{1}[y_i = c]
$$

> 📖 Paper: Cover & Hart (1967) — 原始定义 ⚠️ 待下载

**参数解释：**

| 参数 | 含义 |
|------|------|
| $\mathbf{1}[\cdot]$ | 指示函数，条件为真时取值 1 |
| $\mathcal{N}_k(\mathbf{x})$ | $k$ 个最近邻居的下标集合 |

**推导过程（从概率估计到决策）：**

$$
\text{Step 1: 估计类别条件概率 } \hat{P}(Y=c \mid \mathbf{x}) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x})} \mathbf{1}[y_i = c]
$$

$$
\text{Step 2: 贝叶斯最优决策 } \hat{y} = \arg\max_c \hat{P}(Y=c \mid \mathbf{x})
$$

$$
\text{Step 3: 等价于多数投票 } \hat{y} = \arg\max_c \sum_{i \in \mathcal{N}_k} \mathbf{1}[y_i = c]
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3, Eq. 2.1

---

### 公式 3: KNN 回归预测（均值）

**直觉：** 取 k 个最近邻居的目标值均值，作为稠密点集中该查询位置的期望值估计

$$
\hat{y} = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x})} y_i
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3 (Eq. 2.8 条件期望)

**推导过程（从条件期望出发）：**

$$
\text{Step 1: 真实目标 } f(\mathbf{x}) = E[Y \mid X = \mathbf{x}]
$$

$$
\text{Step 2: 用局部样本均值估计 } \hat{f}(\mathbf{x}) \approx \text{Average}(y_i \mid x_i \in \mathcal{N}_k(\mathbf{x}))
$$

$$
\text{Step 3: } \hat{f}(\mathbf{x}) = \frac{1}{k} \sum_{i \in \mathcal{N}_k(\mathbf{x})} y_i
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 2.8

---

### 公式 4: 距离加权 KNN（Weighted KNN）

**直觉：** 越近的邻居对预测贡献越大，用距离的倒数作权重

$$
\hat{y} = \frac{\sum_{i \in \mathcal{N}_k(\mathbf{x})} w_i \cdot y_i}{\sum_{i \in \mathcal{N}_k(\mathbf{x})} w_i}, \quad w_i = \frac{1}{D(\mathbf{x}, \mathbf{x}_i) + \epsilon}
$$

> 💻 Source: [sklearn/neighbors/_base.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_base.py) `_get_weights()`

**参数解释：**

| 参数 | 含义 |
|------|------|
| $w_i$ | 第 $i$ 个邻居的权重（距离倒数） |
| $\epsilon$ | 防止除零的小常数 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.16 §16.1

---

### 公式 5: Cover-Hart 误差界

**直觉：** 当数据量 $n \to \infty$、$k=1$ 时，1-NN 的误差率不超过贝叶斯最优错误率的两倍

$$
P^* \leq P_{\text{1-NN}} \leq 2P^* \left(1 - P^*\right) \leq 2P^*
$$

其中 $P^*$ 是贝叶斯错误率（理论最低误差）。

> 📖 Paper: Cover & Hart (1967) — Theorem 1 ⚠️ 待下载

**直觉解释：**
- $P^* = 0$（完全可分）→ 1-NN 也可以完美分类
- $P^* = 0.5$（随机猜测基线）→ 1-NN 最多错误率 50%
- 1-NN 的渐近误差最多是贝叶斯误差的 **2 倍**，这是非常强的理论保证

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.13 §13.3

---

## 公式关系图

```
Minkowski 距离 (公式 1)
        │
        ├──→ p=2  欧氏距离  ──→ 找到 k 个最近邻 N_k(x)
        ├──→ p=1  曼哈顿                │
        └──→ p=∞  Chebyshev            ├──→ 分类：多数投票 (公式 2)
                                        │       ↑ 加权版：距离加权 (公式 4)
                                        └──→ 回归：邻居均值 (公式 3)
                                                ↑ 加权版：距离加权 (公式 4)

理论保证：n→∞ 时，1-NN 误差 ≤ 2 × 贝叶斯误差 (公式 5)
```

---

## 手算练习

### 练习 1: 2D 平面 KNN 分类（k=3）

**题目：** 训练集有 5 个点，求查询点 $\mathbf{x}_q = (2, 3)$ 的 KNN 分类（k=3）

训练数据：

| 点 | 坐标 | 类别 |
|----|------|------|
| A | (1, 2) | 红 |
| B | (3, 4) | 红 |
| C | (5, 1) | 蓝 |
| D | (1, 4) | 蓝 |
| E | (4, 3) | 红 |

**解答步骤：**

1. 计算欧氏距离：
   - $D(q, A) = \sqrt{(2-1)^2 + (3-2)^2} = \sqrt{2} \approx 1.41$
   - $D(q, B) = \sqrt{(2-3)^2 + (3-4)^2} = \sqrt{2} \approx 1.41$
   - $D(q, C) = \sqrt{(2-5)^2 + (3-1)^2} = \sqrt{13} \approx 3.61$
   - $D(q, D) = \sqrt{(2-1)^2 + (3-4)^2} = \sqrt{2} \approx 1.41$
   - $D(q, E) = \sqrt{(2-4)^2 + (3-3)^2} = \sqrt{4} = 2.00$

2. 排序，取前 3 名：A (1.41), B (1.41), D (1.41)（平局按训练顺序）

3. 投票：红(A) + 红(B) + 蓝(D) → **红类胜 2:1**

4. 结果：$\hat{y} = \text{红}$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 Example

---

### 练习 2: 归一化对距离的影响

**题目：** 两个特征：$x_1 \in [0, 1000]$（年收入，元），$x_2 \in [0, 1]$（年龄归一化后）。不归一化时，KNN 距离由哪个特征主导？

**解答步骤：**

1. 不归一化：$D = \sqrt{(x_1^{(a)} - x_1^{(b)})^2 + (x_2^{(a)} - x_2^{(b)})^2}$
   - $x_1$ 差值量级：~100（元）
   - $x_2$ 差值量级：~0.01
   - $x_1$ 贡献：$100^2 = 10000$，$x_2$ 贡献：$0.01^2 = 0.0001$

2. 结论：$x_1$ 主导距离，$x_2$ 几乎不影响结果，KNN 实际上退化为仅按收入分类

3. 解法：StandardScaler 归一化后，两个特征均值为 0、方差为 1，贡献均等

> 📖 Docs: [scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| Minkowski 距离 | $\left(\sum_j \|x_j - x_{ij}\|^p\right)^{1/p}$ | 找 k 近邻 | 无 |
| KNN 分类 | $\arg\max_c \sum_{i \in \mathcal{N}_k} \mathbf{1}[y_i=c]$ | 分类预测 | 公式 1 |
| KNN 回归 | $\frac{1}{k}\sum_{i \in \mathcal{N}_k} y_i$ | 回归预测 | 公式 1 |
| 距离加权 | $w_i = 1/D(\mathbf{x}, \mathbf{x}_i)$ | 改进预测 | 公式 1 |
| Cover-Hart 界 | $P_{1\text{-NN}} \leq 2P^*$ | 理论保证 | 无 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 & Ch.13
