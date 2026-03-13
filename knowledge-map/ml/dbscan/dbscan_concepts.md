---
topic: dbscan
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Ester et al. KDD 1996 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/dbscan/ester_1996_dbscan.pdf"
  - "📖 Paper: Schubert et al. TODS 2017 — https://doi.org/10.1145/3068335"
  - "📖 Docs: scikit-learn DBSCAN — https://scikit-learn.org/stable/modules/clustering.html#dbscan"
expiry: 12m
status: current
---

# DBSCAN 核心概念

> 📖 Paper: Ester et al., [A Density-Based Algorithm...](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf), KDD 1996, Sec. 2

---

## 术语定义

### ε-邻域 (ε-Neighborhood)

给定点 p 和半径 ε，p 的邻域是数据集中所有到 p 距离不超过 ε 的点的集合：$N_\varepsilon(p) = \{q \in D \mid dist(p, q) \leq \varepsilon\}$。这是 DBSCAN 判断"密集"的基本单位——用一个半径为 ε 的圆套住 p，圆内的点就是邻域。

> 易混淆：**邻域大小 vs ε** — ε 是半径（距离阈值），$|N_\varepsilon(p)|$ 才是邻域内点的数量

### 核心点 (Core Point)

如果点 p 的 ε 邻域内（含 p 自身）至少有 `min_samples` 个点，则 p 是核心点。核心点是"人口密集区的居民"——自身的邻域满足密度条件，能作为簇扩展的出发点。

> 易混淆：**核心点 vs 边界点** — 两者都在簇内，区别在于核心点自身邻域密度达标，边界点不达标但落在某核心点的邻域内

### 边界点 (Border Point)

不是核心点，但落在某个核心点的 ε 邻域内的点。边界点处于簇的"边缘地带"——自己不够密集，但依附于核心点而属于同一个簇。

> 易混淆：**边界点 vs 噪声点** — 边界点有归属（在某核心点邻域内），噪声点完全孤立无归属

### 噪声点 (Noise Point / Outlier)

既不是核心点，又不在任何核心点邻域内的点。DBSCAN 将噪声点的标签设为 `-1`。这是 DBSCAN 相对 K-Means 的关键能力：显式地识别并排除异常值，不强制归入任何簇。

> 易混淆：**噪声点 vs 边界点** — 两者都不是核心点，但边界点可归入某簇，噪声点无法归入任何簇

### 直接密度可达 (Directly Density-Reachable)

从核心点 p 出发，如果点 q 在 p 的 ε 邻域内（$q \in N_\varepsilon(p)$），则称 q 从 p 直接密度可达。**非对称关系**：q 从 p 可达，若 q 不是核心点则 p 不一定从 q 可达。

> 易混淆：**直接可达 vs 密度可达** — 直接可达是一步（q 在 p 邻域），密度可达是多步链式传播

### 密度可达 (Density-Reachable)

从点 p 到点 q 存在一条链 $p_1, p_2, \ldots, p_n$（$p_1=p, p_n=q$），且每个 $p_{i+1}$ 都从 $p_i$ 直接密度可达，则 q 从 p 密度可达。这是 DBSCAN 扩展簇的传播机制，允许跨越多条核心点的"接力链"。

### 密度相连 (Density-Connected)

如果存在点 o，使得 p 和 q 都从 o 密度可达，则 p 和 q 密度相连。密度相连是**对称关系**，是 DBSCAN 定义簇的最终标准——同一簇内任意两点必须密度相连。

> 📖 Paper: Ester et al., KDD 1996, Definitions 1–6 (Sec. 2)

---

## 概念辨析

### 核心点 vs 边界点 vs 噪声点

| 维度 | 核心点 (Core) | 边界点 (Border) | 噪声点 (Noise) |
|------|-------------|----------------|--------------|
| **自身邻域密度** | ≥ min_samples | < min_samples | < min_samples |
| **在某核心点邻域内** | 可能是 | ✅ 是 | ❌ 否 |
| **输出标签** | 非负整数（簇ID） | 非负整数（簇ID） | -1 |
| **能扩展簇？** | ✅ 可以 | ❌ 不能 | ❌ 不能 |
| **典型角色** | 簇的核心 | 簇的边界 | 离群值 |

> 📖 Paper: Ester et al., KDD 1996, Definitions 1–3

### DBSCAN vs K-Means

| 维度 | DBSCAN | K-Means |
|------|--------|---------|
| **是否需要预设 K** | ❌ 不需要 | ✅ 需要 |
| **簇的形状** | 任意形状 | 球形（凸形）|
| **噪声处理** | 显式标记 -1 | 强制归入最近簇 |
| **参数** | ε, min_samples | K |
| **时间复杂度** | O(n log n)（有索引）| O(nKt) |
| **适用场景** | 地理/空间数据，含噪声，形状不规则 | 均匀球形簇 |

> 📖 Paper: Ester et al., KDD 1996, Sec. 5 (Experiments)

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────┐
│  DBSCAN 算法架构                                  │
├──────────────────────────────────────────────────┤
│ 输入                                              │
│  ├─ 数据集 D（n 个点）                           │
│  ├─ ε（邻域半径）                                │
│  └─ min_samples（核心点最少邻居数，含自身）        │
├──────────────────────────────────────────────────┤
│ 执行流程                                          │
│  ├─ Step 1: 为每个点计算 ε 邻域（KD-Tree 加速）  │
│  ├─ Step 2: 判断是否为核心点（|Nε| ≥ min_samples）│
│  ├─ Step 3: 从未访问核心点出发，BFS 扩展簇        │
│  └─ Step 4: 未归入任何簇的点 → 噪声（标签 -1）   │
├──────────────────────────────────────────────────┤
│ 输出                                              │
│  ├─ labels_：每点的簇 ID（-1 = 噪声）            │
│  └─ core_sample_indices_：核心点在原始数据中的索引  │
└──────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn _dbscan.py](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py) `fit()` 方法

### 适用场景 ✅

- 地理/空间数据聚类（GPS 轨迹、地图兴趣点 POI）
- 数据中存在异常值（噪声），需要显式识别与剔除
- 簇的形状不规则（月牙形、环形、狭长形）
- 预先不知道簇的数量 K
- 簇内密度大致均匀

### 不适用场景 ❌

- 不同簇的密度差异很大（单一 ε 无法同时适配稀疏和密集簇）
- 高维稀疏数据（维度诅咒：所有点距离趋同，ε 邻域失去意义）
- 需要严格可重现的边界点分配（边界点归属具有固有不确定性）
- 超大数据集（朴素实现 O(n²)；sklearn 改善但内存仍有成本）

> 📖 Paper: Schubert et al., TODS 2017, Sec. 2 (Common Misconceptions)
> 📖 Docs: [sklearn 聚类算法对比](https://scikit-learn.org/stable/modules/clustering.html#overview-of-clustering-methods)

---

## 速查表

| 项 | 说明 | 典型值/示例 |
|-----|------|-----------|
| `eps` | ε 邻域半径 | 用 k-NN 距离图的"肘部"选取 |
| `min_samples` | 成为核心点的最少邻居数（含自身）| 通常 ≥ 维度数 + 1；2D 数据用 3~5 |
| `labels_` | 输出标签，-1 表示噪声 | `[0, 0, 1, 1, -1]` |
| `core_sample_indices_` | 核心点在原始数据中的索引 | `ndarray of int` |
| `components_` | 所有核心点的特征向量副本 | shape `(n_core, n_features)` |
| 时间复杂度 | 有空间索引时 O(n log n) | 朴素实现 O(n²) |
| 空间复杂度 | sklearn 实现约 O(n·d)，d = 平均邻居数 | — |

> 📖 Docs: [sklearn DBSCAN API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
> 💻 Source: [sklearn _dbscan.py L201-L513](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)
