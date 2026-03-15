---
topic: kmeans
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Murphy K.P., Probabilistic Machine Learning An Introduction, Ch.21 §21.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie T. et al., The Elements of Statistical Learning, Ch.13 §13.2.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Lloyd 1982 IEEE; Arthur & Vassilvitskii 2007 SODA"
  - "📖 Docs: scikit-learn Clustering User Guide — https://scikit-learn.org/stable/modules/clustering.html#k-means"
expiry: 12m
status: current
---

# K-Means 教程

> **前置知识：** 欧氏距离、向量均值、基本优化（梯度置 0）
> **参考来源：** [Murphy PML1 §21.3](../../../textbooks/murphy_pml1.pdf) | [Hastie ESL §13.2.1](../../../textbooks/hastie_esl.pdf) | [sklearn 聚类指南](https://scikit-learn.org/stable/modules/clustering.html#k-means)

---


## Section 0: 前置知识速查

1. **欧氏距离**：$\|\boldsymbol{x} - \boldsymbol{y}\|_2 = \sqrt{\sum_{d=1}^D (x_d - y_d)^2}$，衡量两点之间的直线距离
2. **向量均值**：$D$ 维 $N$ 个向量的均值 = 逐维求均值，即 $\bar{\boldsymbol{x}} = \frac{1}{N}\sum_{i=1}^N \boldsymbol{x}_i$
3. **坐标下降**：固定部分变量，逐步优化另一个变量；K-Means 的 E/M 步骤正是坐标下降
4. **局部最优 vs 全局最优**：K-Means 的目标函数非凸，Lloyd 算法只保证收敛到局部最优，多次随机重启能提高找到全局最优的概率

> 📚 Murphy §8 Optimization (coordinate descent); §21.3.1

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：数据探索无标签**：真实世界的数据大多没有标签（用户行为、基因序列、图像像素），监督学习根本无法使用。我们需要一种方法能自动发现数据中"自然分组"的结构
- 🔥 **痛点 2：数据规模庞大**：真实场景动辄百万、千万级数据点，需要一个计算效率高（线性或接近线性复杂度）的聚类算法
- 🔥 **痛点 3：下游任务需要离散化**：推荐系统的用户分群、图像压缩的颜色量化、RAG 系统的语义聚簇——很多场景需要将连续特征空间离散化为有限个代表点

### 它的核心价值

1. **极简的算法原理**：只需两步交替迭代——"分配"和"更新"——就能收敛，无需梯度计算，易于实现和并行化
2. **高效的计算复杂度**：O(NKDt)（t 为迭代次数），远优于穷举方法，能处理大规模数据
3. **广泛的应用基础**：向量量化（VQ）、图像分割、文档聚类、客户分群、语义索引——K-Means 是众多系统的核心组件

> 📚 Hastie §13.2.1 "K-Means Clustering"; Murphy §21.3

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌──────────────────────────────────────────────────────────────────────┐
│                     K-Means 完整流程                                  │
├──────────────────────────────────────────────────────────────────────┤
│  输入: X (N×D 矩阵), K (簇数)                                        │
│    │                                                                  │
│    ▼                                                                  │
│  ┌─────────────────────────────┐                                     │
│  │  Step 0: 初始化质心          │                                     │
│  │  随机选 K 个点，或 K-Means++ │                                     │
│  └─────────────────────────────┘                                     │
│    │                                                                  │
│    ▼     ◄──────────────────────────────────────┐                   │
│  ┌─────────────────────────────┐                │                   │
│  │  E 步: 分配（Assignment）    │                │                   │
│  │  每点 → 最近质心             │                │ 未收敛             │
│  └─────────────────────────────┘                │                   │
│    │                                             │                   │
│    ▼                                             │                   │
│  ┌─────────────────────────────┐                │                   │
│  │  M 步: 更新（Update）        │                │                   │
│  │  每簇质心 → 簇内均值         │────────────────┘                   │
│  └─────────────────────────────┘                                     │
│    │ 收敛（质心不动 或 达到最大迭代）                                  │
│    ▼                                                                  │
│  输出: labels_, cluster_centers_, inertia_                           │
└──────────────────────────────────────────────────────────────────────┘
```

> 📖 Lloyd 1982 §II; 📚 Murphy §21.3.1

### 2.2 核心机制 1: 为什么 WCSS 单调递减？

**为什么 E 步减小 WCSS？**

固定质心 $\{\boldsymbol{\mu}_k\}$，对每个点 $\boldsymbol{x}_i$，我们选最小距离的簇，这必然使 $\sum_i \min_k \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$ 最小或不变。

**为什么 M 步减小 WCSS？**

固定分配，对每个簇 $k$，最小化 $\sum_{i \in \mathcal{C}_k} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$ 的最优解就是均值（见数学文件证明），所以更新后 WCSS 不增大。

由于 WCSS 下界为 0，且每步不增大，所以**必然收敛**。

> 📚 Murphy §21.3.1; 📖 Lloyd 1982

### 2.3 核心机制 2: 为什么 K-Means 是 EM 算法的特例？

GMM 的 EM 算法中：
- **E 步**：计算每个点对每个高斯的"软分配"概率（responsibility）
- **M 步**：用加权均值更新参数

当 GMM 的方差 $\sigma^2 \rightarrow 0$ 时，软分配趋向硬分配（winner-take-all），加权均值退化为普通均值，整个算法退化为 K-Means。

这说明 K-Means 是高斯混合模型的极端情况，理解 GMM 能获得对 K-Means 的深层洞见。

> 📚 Hastie §13.2.3 "Gaussian Mixtures"; Murphy §21.4.1

### 2.4 层次化说明

```
K-Means 扩展体系
            简单                   中等                    复杂
┌──────────────┐    ┌───────────────────┐    ┌────────────────────────┐
│ K-Means      │──→ │ Mini-Batch K-Means │──→ │ GMM + EM               │
│ (Lloyd 硬分配)│    │ (随机子批量更新)    │    │ (软分配+协方差估计)     │
└──────────────┘    └───────────────────┘    └────────────────────────┘
      │
      ├── K-Means++ (改进初始化)
      └── K-Medoids (中心点=真实样本，鲁棒性更强)
```

> 📚 Murphy §21.3.4-21.3.5

---


## Section 3: 局限性

1. **局部最优** → 对初始化敏感，不同初始质心往往得到不同结果。应对：多次随机重启（`n_init=10`），或使用 K-Means++ 初始化
2. **必须预设 K** → 需要提前知道簇数，但现实中往往未知。应对：用 Elbow Method 或 Silhouette Score 扫描不同 K 值
3. **只适合凸形球状簇** → 月牙形、环形等非凸分布无法正确聚类。应对：改用 DBSCAN 或谱聚类
4. **对离群值敏感** → 一个远离质心的离群值会把整个质心拉偏。应对：改用 K-Medoids（中心点=真实样本），更鲁棒
5. **各维度权重相同** → 不会自动区分重要和不重要的特征，高维时性能下降（维度灾难）。应对：先做特征选择或降维（PCA），或对特征标准化

> 📚 Murphy §21.3; Hastie §13.2.1

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **K-Means** | 快速、简单、可扩展 | 需预设 K，只处理球形簇，对初始化敏感 | 大规模数值数据，簇近似球形 |
| **K-Means++** | 初始化更好，收敛快，局部最优更少 | 额外 O(NK) 初始化开销 | K-Means 的默认更好替代 |
| **K-Medoids** | 更鲁棒（质心是真实样本），能处理非数值型 | 计算复杂度更高 O(K(N-K)²) | 数据含离群值，或非欧氏距离 |
| **GMM + EM** | 软分配，能建模椭圆形簇，提供概率输出 | 计算更重，需估计协方差 | 需要概率输出，或簇有不同形状/大小 |
| **DBSCAN** | 不需要预设 K，能发现任意形状，处理噪声 | 高维效果差，需调 eps 和 min_samples | 任意形状簇，含噪声，中小规模数据 |

> 📚 Murphy §21; Hastie §13.2, §14.3

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [《PML1》Ch.21 §21.3](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | Section 1, 2, 3, 4 全文参考 |
| [《ESL》Ch.13 §13.2.1](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | Section 1 动机, Section 4 方案对比 |
| [Lloyd 1982 IEEE](https://ieeexplore.ieee.org/document/1056489) | 📖 论文 | Section 2.1 流程，收敛分析 |
| [Arthur & Vassilvitskii 2007 SODA](https://dl.acm.org/doi/10.5555/1283383.1283494) | 📖 论文 | Section 2.3 K-Means++ |
| [sklearn 聚类指南](https://scikit-learn.org/stable/modules/clustering.html#k-means) | 📖 文档 | Section 0 前置，Section 4 对比 |
