---
topic: kmeans
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Murphy K.P., Probabilistic Machine Learning An Introduction, Ch.21 §21.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie T. et al., The Elements of Statistical Learning, Ch.13 §13.2.1 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Lloyd S.P. 1982 IEEE Trans. Inf. Theory — https://ieeexplore.ieee.org/document/1056489"
expiry: 12m
status: current
---

# K-Means 核心概念

> 📚 Book: Murphy K.P., [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.21 §21.3
> 📖 Paper: Lloyd, ["Least Squares Quantization in PCM"](https://ieeexplore.ieee.org/document/1056489)

---


## 术语定义

### 簇（Cluster）

簇是数据空间中一组"相似"数据点的集合。在 K-Means 中，相似性由欧氏距离定义——同一个簇内的点离自己的"簇中心（质心）"比离其他簇中心更近。每个数据点只属于一个簇（硬分配）。

> 易混淆：**簇 vs 类（Class）** — 簇是无监督发现的结构，无需任何标签；类是有监督学习中预先定义的分类。K-Means 找到的是数据的自然分组，不对应任何已知标签

### 质心（Centroid）

质心是簇内所有数据点的均值向量（mean vector）。在 K-Means 的每次迭代中，质心先固定用于分配数据点，然后根据当前分配重新计算。K 个质心是算法的核心参数，记为 $\boldsymbol{\mu}_k, k=1,\ldots,K$。

> 易混淆：**质心 vs 中心点（Medoid）** — 质心是均值，不一定是真实数据点；中心点（K-Medoids 算法中使用）必须是数据集中实际存在的点，对离群值更鲁棒

### 簇内方差和（WCSS, Within-Cluster Sum of Squares）

WCSS 是 K-Means 的优化目标，定义为所有数据点到其所属质心的平方欧氏距离之和。公式：
$$\text{WCSS} = \sum_{k=1}^{K} \sum_{i: c_i = k} \|\boldsymbol{x}_i - \boldsymbol{\mu}_k\|^2$$
WCSS 越小，表示簇越紧凑，聚类效果越好。

> 易混淆：**WCSS vs Inertia** — scikit-learn 中 `inertia_` 属性就是 WCSS；两者完全等价，只是不同语境下的叫法

### 硬分配（Hard Assignment）

K-Means 的每个数据点被明确地、排他地分配给恰好一个簇，这叫硬分配。与之对比的是高斯混合模型（GMM）的"软分配"——GMM 中每个数据点对每个簇有一个归属概率（隶属度），值在 [0,1] 之间且加和为 1。

> 易混淆：**硬分配 vs 软分配** — K-Means 是硬聚类，每点只属于一个簇；GMM+EM 是软聚类，每点有多个簇的归属概率。当 GMM 的高斯方差趋向 0 时，GMM 退化为 K-Means

> 📚 Murphy §21.3 "K-means Clustering"; Hastie §13.2.1

---


## 概念辨析

### K-Means vs GMM（高斯混合模型）

| 维度 | K-Means | GMM |
|------|---------|-----|
| **分配方式** | 硬分配（每点唯一属于一簇） | 软分配（每点有归属概率） |
| **目标函数** | 最小化 WCSS（欧氏距离） | 最大化数据似然（EM 算法） |
| **假设** | 簇为球形且大小相近 | 每个簇为椭圆形高斯分布 |
| **计算复杂度** | 低，迭代快 | 较高，需要估计协方差矩阵 |
| **关系** | GMM 当方差→0 退化为 K-Means | GMM 是 K-Means 的概率推广 |
| **典型应用** | 大规模快速聚类、向量量化 | 概率建模、生成模型 |

> 📚 Hastie §13.2.3 "Gaussian Mixtures"; Murphy §21.4.1

### K-Means vs DBSCAN

| 维度 | K-Means | DBSCAN |
|------|---------|--------|
| **需要预设 K** | 是，必须指定簇数 | 否，自动发现簇数 |
| **簇的形状** | 只能处理凸形球状簇 | 任意形状（月牙、环形等） |
| **噪声处理** | 所有点必须归入某个簇 | 可识别噪声点（离群值） |
| **复杂度** | O(NKd·iter)，快 | O(N log N)，需要空间索引 |
| **适用场景** | 大规模、球状、非噪声数据 | 任意形状、含噪声的中等规模数据 |

> 📚 Murphy §21 Clustering overview

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────┐
│  K-Means 算法架构                                 │
├──────────────────────────────────────────────────┤
│ 输入                                              │
│  └─ X: N×D 数据矩阵，K: 指定的簇数              │
├──────────────────────────────────────────────────┤
│ 初始化                                            │
│  ├─ 随机选 K 个数据点作为初始质心               │
│  └─ K-Means++ (改进版) 用加权概率选初始中心      │
├──────────────────────────────────────────────────┤
│ 迭代（Lloyd 算法）                                │
│  ├─ E 步：分配 — 每点分给最近质心               │
│  └─ M 步：更新 — 重新计算每簇均值               │
├──────────────────────────────────────────────────┤
│ 收敛条件                                          │
│  ├─ 质心不再移动，或移动量小于阈值 tol           │
│  └─ 达到最大迭代次数 max_iter                    │
├──────────────────────────────────────────────────┤
│ 输出                                              │
│  ├─ labels_: N 维向量，每点的簇编号 (0~K-1)     │
│  ├─ cluster_centers_: K×D 质心矩阵              │
│  └─ inertia_: WCSS 值（评估聚类质量）           │
└──────────────────────────────────────────────────┘
```

> 📖 Lloyd 1982; 📖 scikit-learn [KMeans文档](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

### 适用场景 ✅

- 数据量大（N 很大），需要快速聚类
- 簇的形状近似球形（各向同性）
- 各簇大小相近（点数量差异不大）
- 已知或可以估计出 K 的合理范围
- 作为其他算法的前处理步骤（如 GMM 初始化）
- 向量量化（图像压缩、编码本生成）

### 不适用场景 ❌

- 数据中含有大量噪声/离群值（K-Means 对它们敏感）
- 簇形状非凸（月牙形、环形等），需要用 DBSCAN 或谱聚类
- 各簇密度/大小差异极大（大簇会"吃掉"小簇）
- 特征尺度差异很大且未标准化（距离计算失效）
- 样本为分类型（非数值型）数据，需先编码处理
- 没有先验知识，不知道 K 值时（K-Medoids 或 DBSCAN 更鲁棒）

> 📚 Hastie §13.2.1; Murphy §21.3

---


## 速查表

| 项 | 说明 | 值/范围 |
|-----|------|---------|
| 时间复杂度 | 每次迭代 | O(N·K·D·iter) |
| 空间复杂度 | 存储质心和标签 | O(K·D + N) |
| 收敛保证 | 单调递减，有限步收敛 | 收敛到局部最优 |
| sklearn 主要参数 | `n_clusters` | 簇数 K，必须指定 |
| sklearn 主要参数 | `init` | 'k-means++' (默认) 或 'random' |
| sklearn 主要参数 | `n_init` | 随机重启次数，默认 10 |
| sklearn 输出 | `inertia_` | WCSS 值 |
| sklearn 输出 | `labels_` | 每点的簇标签 |
| sklearn 输出 | `cluster_centers_` | 质心坐标 |

> 📖 scikit-learn [KMeans API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
