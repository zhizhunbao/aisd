---
topic: kmeans
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Murphy K.P., Probabilistic Machine Learning An Introduction, Ch.21 §21.3.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie T. et al., The Elements of Statistical Learning, Ch.13 §13.2.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Lloyd S.P. 1982 IEEE Trans. Inf. Theory — https://ieeexplore.ieee.org/document/1056489"
  - "📖 Paper: Arthur & Vassilvitskii 2007 SODA — https://dl.acm.org/doi/10.5555/1283383.1283494"
expiry: 12m
status: current
---

# K-Means 数学基础

> 📚 Book: Murphy K.P., [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.21 §21.3.1
> 📖 Paper: Lloyd, ["Least Squares Quantization in PCM"](https://ieeexplore.ieee.org/document/1056489), IEEE Trans. 1982

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| $N$ | 数据集样本数 | Number of samples | $N \in \mathbb{Z}^+$ |
| $D$ | 特征（维度）数 | Feature dimension | $D \in \mathbb{Z}^+$ |
| $K$ | 簇数（超参数） | Number of clusters | $K \in \mathbb{Z}^+, K \leq N$ |
| $\boldsymbol{x}_i$ | 第 $i$ 个数据点，D 维向量 | Data point | $\boldsymbol{x}_i \in \mathbb{R}^D$ |
| $c_i$ | 第 $i$ 个点的簇标签 | Cluster assignment | $c_i \in \{1, \ldots, K\}$ |
| $\boldsymbol{\mu}_k$ | 第 $k$ 个簇的质心（均值向量） | Centroid / mean | $\boldsymbol{\mu}_k \in \mathbb{R}^D$ |
| $\mathcal{C}_k$ | 第 $k$ 个簇包含的点的集合 | Cluster set | $\mathcal{C}_k \subseteq \{1, \ldots, N\}$ |
| $r_{ik}$ | 指示变量，第 $i$ 点是否属于第 $k$ 簇 | Responsibility | $r_{ik} \in \{0, 1\}$ |
| $J$ | 总目标函数（WCSS） | Within-Cluster Sum of Squares | $J \geq 0$ |

> 📚 Murphy §21.3.1 Eq.(21.14) - Eq.(21.17)

---


## 核心公式

### 公式 1: WCSS 目标函数

**直觉：** 把所有数据点到其所属质心的平方距离加起来，越小说明簇越紧凑

$$
J(\{r_{ik}\}, \{\boldsymbol{\mu}_k\}) = \sum_{i=1}^{N} \sum_{k=1}^{K} r_{ik} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2
$$

> 📚 Murphy §21.3.1, Eq.(21.14); Hastie §13.2.1

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $r_{ik}$ | 若点 $i$ 属于簇 $k$ 则为 1，否则为 0 | 硬分配的指示变量 |
| $\|\cdot\|^2$ | 欧氏距离的平方 | $\sum_{d=1}^D (x_{id} - \mu_{kd})^2$ |

**推导说明：** K-Means 是一个 NP-Hard 问题（精确最优化），Lloyd 算法通过坐标下降交替优化 $\{r_{ik}\}$ 和 $\{\boldsymbol{\mu}_k\}$ 来找局部最优解。

> 📚 Murphy §21.3.1

---

### 公式 2: E 步（分配步骤）

**直觉：** 固定质心，把每个样本分配给距离最近的那个质心

$$
r_{ik} = \mathbb{1}\left[k = \arg\min_{k'} \|\boldsymbol{x}_i - \boldsymbol{\mu}_{k'}\|^2 \right]
$$

等价写法（每次只让一个 $k$ 为 1）：

$$
c_i = \arg\min_{k \in \{1,\ldots,K\}} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2
$$

> 📖 Lloyd 1982, §II Encoding step

**推导过程：**

$$
\text{Step 1: 固定 } \{\boldsymbol{\mu}_k\}，\text{对每个 } i \text{ 独立优化 } r_{ik}
$$
$$
\text{Step 2: 目标函数对 } r_{ik} \text{ 是线性的（加和形式）}
$$
$$
\text{Step 3: 最小化 → 选最小 } \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2 \text{ 对应的 } k，令 } r_{ik}=1
$$

> 📚 Murphy §21.3.1

---

### 公式 3: M 步（更新步骤）

**直觉：** 固定分配，把每个质心移到它所包含的所有点的均值位置

$$
\boldsymbol{\mu}_k = \frac{\sum_{i=1}^{N} r_{ik} \boldsymbol{x}_i}{\sum_{i=1}^{N} r_{ik}} = \frac{1}{|\mathcal{C}_k|} \sum_{i \in \mathcal{C}_k} \boldsymbol{x}_i
$$

> 📚 Murphy §21.3.1, Eq.(21.17); 📖 Lloyd 1982

**推导过程：**

$$
\text{Step 1: 固定 } \{r_{ik}\}，\text{对 } \boldsymbol{\mu}_k \text{ 求偏导}
$$
$$
\frac{\partial J}{\partial \boldsymbol{\mu}_k} = -2 \sum_{i=1}^{N} r_{ik} (\boldsymbol{x}_i - \boldsymbol{\mu}_k) = 0
$$
$$
\text{Step 2: 解方程 } \Rightarrow \boldsymbol{\mu}_k = \frac{\sum_i r_{ik} \boldsymbol{x}_i}{\sum_i r_{ik}}
$$

> 📚 Murphy §21.3.1

---

### 公式 4: K-Means++ 初始化概率

**直觉：** 第一个质心随机选，之后每个新质心的选取概率正比于该点到已有质心的最远距离平方，目的是让初始质心"分散开"

$$
P(\boldsymbol{x}_i \text{ 被选为第}(t+1)\text{个质心}) = \frac{D(\boldsymbol{x}_i)^2}{\sum_{j=1}^N D(\boldsymbol{x}_j)^2}
$$

其中 $D(\boldsymbol{x}_i) = \min_{k \in \text{已选}} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|$ 是点 $i$ 到已选质心的最短距离。

> 📖 Arthur & Vassilvitskii, ["k-means++: The Advantages of Careful Seeding"](https://dl.acm.org/doi/10.5555/1283383.1283494), SODA 2007

---


## 公式关系图

```
目标函数 J (WCSS)
       │
       ├─→ E 步（最小化 J 对 r_ik）：分配 → 公式 2
       │       使 J 单调递减
       │
       └─→ M 步（最小化 J 对 μ_k）：更新 → 公式 3
               使 J 单调递减（取均值最小化均方距离）

K-Means++ → 更好的初始 μ_k → 更少迭代次数 → 公式 4
```

> 📚 Murphy §21.3.1; 📖 Arthur & Vassilvitskii 2007

---


## 手算练习

### 练习 1: 2 维, K=2 的 Lloyd 迭代

**题目：** 数据点 $\boldsymbol{x}_1=(0,0), \boldsymbol{x}_2=(1,0), \boldsymbol{x}_3=(5,0), \boldsymbol{x}_4=(6,0)$，初始质心 $\boldsymbol{\mu}_1=(0,0), \boldsymbol{\mu}_2=(6,0)$

**解答步骤：**

1. **E 步（分配）：**
   - $d(\boldsymbol{x}_1, \boldsymbol{\mu}_1)=0, d(\boldsymbol{x}_1, \boldsymbol{\mu}_2)=6$ → $c_1=1$
   - $d(\boldsymbol{x}_2, \boldsymbol{\mu}_1)=1, d(\boldsymbol{x}_2, \boldsymbol{\mu}_2)=5$ → $c_2=1$
   - $d(\boldsymbol{x}_3, \boldsymbol{\mu}_1)=5, d(\boldsymbol{x}_3, \boldsymbol{\mu}_2)=1$ → $c_3=2$
   - $d(\boldsymbol{x}_4, \boldsymbol{\mu}_1)=6, d(\boldsymbol{x}_4, \boldsymbol{\mu}_2)=0$ → $c_4=2$

2. **M 步（更新质心）：**
   - $\boldsymbol{\mu}_1 = \frac{(0,0)+(1,0)}{2} = (0.5, 0)$
   - $\boldsymbol{\mu}_2 = \frac{(5,0)+(6,0)}{2} = (5.5, 0)$

3. **验证收敛：** 再做一次 E 步，分配不变 → **收敛！**

4. **WCSS 结果：**
   - $J = (0-0.5)^2 + (1-0.5)^2 + (5-5.5)^2 + (6-5.5)^2 = 0.25+0.25+0.25+0.25 = 1.0$

> 📚 根据 Murphy §21.3.1 算法步骤手算

### 练习 2: 验证 M 步公式

**题目：** 证明取均值能最小化簇 $k$ 内的 WCSS

**解答步骤：**

1. 对固定分配，簇 $k$ 的局部目标：$J_k = \sum_{i \in \mathcal{C}_k} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$

2. 对 $\boldsymbol{\mu}_k$ 求梯度：$\nabla_{\boldsymbol{\mu}_k} J_k = -2\sum_{i \in \mathcal{C}_k}(\boldsymbol{x}_i - \boldsymbol{\mu}_k)$

3. 令梯度为 0：$\sum_{i \in \mathcal{C}_k} \boldsymbol{x}_i = |\mathcal{C}_k| \cdot \boldsymbol{\mu}_k \Rightarrow \boldsymbol{\mu}_k = \frac{1}{|\mathcal{C}_k|}\sum_{i \in \mathcal{C}_k}\boldsymbol{x}_i$ ✓

> 📚 Murphy §21.3.1 推导

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| WCSS 目标 | $J = \sum_i \sum_k r_{ik} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$ | 评估聚类质量，越小越好 | — |
| E 步（分配） | $c_i = \arg\min_k \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$ | 把点分给最近质心 | 公式 1 |
| M 步（更新） | $\boldsymbol{\mu}_k = \frac{1}{|\mathcal{C}_k|}\sum_{i\in\mathcal{C}_k}\boldsymbol{x}_i$ | 重新计算质心 | 公式 2 |
| K-Means++ 概率 | $P(i) \propto D(\boldsymbol{x}_i)^2$ | 改进初始化，减少迭代 | 公式 1 |

> 📚 Murphy §21.3.1; 📖 Arthur & Vassilvitskii 2007
