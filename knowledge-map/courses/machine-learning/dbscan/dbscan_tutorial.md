---
topic: dbscan
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Ester et al. KDD 1996 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/dbscan/ester_1996_dbscan.pdf"
  - "📖 Paper: Schubert et al. TODS 2017 — https://doi.org/10.1145/3068335"
  - "📖 Docs: scikit-learn DBSCAN User Guide — https://scikit-learn.org/stable/modules/clustering.html#dbscan"
  - "💻 Source: scikit-learn _dbscan.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_dbscan.py"
expiry: 12m
status: current
---

# DBSCAN 教程

> **前置知识：** 距离度量（欧氏距离）、无监督聚类基本概念、KD-Tree/Ball-Tree 邻域搜索
> **参考来源：** [Ester et al. KDD 1996](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf) | [Schubert et al. TODS 2017](https://doi.org/10.1145/3068335) | [sklearn DBSCAN 文档](https://scikit-learn.org/stable/modules/clustering.html#dbscan)

---

## Section 0: 前置知识速查

1. **距离度量（Distance Metric）**：能计算两点之间的"远近"，如欧氏距离 $\sqrt{\sum(p_i-q_i)^2}$
2. **无监督聚类**：没有标签，靠数据本身的结构划分类别
3. **邻域搜索（Neighborhood Query）**：给定点 p 和半径 r，找到所有距 p ≤ r 的点；sklearn 用 KD-Tree 或 Ball-Tree 加速
4. **K-Means 的局限**：需预设 K，假设簇为球形，无法处理噪声——DBSCAN 正是为解决这些问题而生

> 📖 Paper: Ester et al., KDD 1996, Sec. 1 (Introduction)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **K-Means 需要预设簇数量 K**：真实数据中你往往不知道 K 是多少，盲猜 K 会导致错误划分
- 🔥 **K-Means 无法发现非球形簇**：月牙形、环形、S 形数据，K-Means 会把它切割成球状的错误簇
- 🔥 **K-Means 把所有点都强制归入某个簇**：异常值（噪声）会被错误地拉进某个簇，污染聚类结果
- 🔥 **层次聚类计算复杂度高**：全量数据时 O(n²) 甚至 O(n³)，对大规模空间数据库（GPS、地图数据）无法使用

### 它的核心价值

1. **无需预设 K**：由 ε 和 min_samples 两个直觉可解释的参数自动确定簇数量
2. **任意形状的簇**：基于密度传播，可以"爬过"任意形状的数据分布
3. **噪声识别**：显式地把低密度区域的点标为噪声（标签 -1），不强制归类
4. **大规模空间数据效率**：借助空间索引（KD-Tree、Ball-Tree、R*-Tree），达到 O(n log n)

> 📖 Paper: Ester et al., KDD 1996, Sec. 1 (Motivation) + Sec. 5 (Experiments)
> 📖 Paper: Schubert et al., TODS 2017, Sec. 1 (Introduction)

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 DBSCAN 完整执行流程

```
┌───────────────────────────────────────────────────────────────┐
│                    DBSCAN 执行流程                             │
├───────────────────────────────────────────────────────────────┤
│  输入: D（数据集）, ε（邻域半径）, MinPts（最少邻居）           │
│        labels[] 初始化为 -1（噪声）                            │
│                        │                                      │
│                        ▼                                      │
│  ┌─────────────────────────────────────┐                     │
│  │ Step 1: 枚举每个未访问点 p           │                     │
│  └────────────────┬────────────────────┘                     │
│                   │                                           │
│                   ▼                                           │
│  ┌─────────────────────────────────────┐                     │
│  │ Step 2: 计算 N_ε(p)                 │                     │
│  │         若 |N_ε(p)| < MinPts:       │                     │
│  │           → 标记为噪声（暂时）       │                     │
│  │         若 |N_ε(p)| ≥ MinPts:       │                     │
│  │           → p 是核心点，开始扩展簇   │                     │
│  └────────────────┬────────────────────┘                     │
│                   │                                           │
│                   ▼                                           │
│  ┌─────────────────────────────────────┐                     │
│  │ Step 3: 扩展簇（BFS/队列）           │                     │
│  │  队列 Q = N_ε(p)                    │                     │
│  │  While Q 不空:                       │                     │
│  │    取出 q                            │                     │
│  │    若 q 是噪声 → 改为当前簇（边界点）│                     │
│  │    若 q 未访问 且 |N_ε(q)| ≥ MinPts │                     │
│  │      → 将 N_ε(q) 加入 Q             │                     │
│  └────────────────┬────────────────────┘                     │
│                   │                                           │
│                   ▼                                           │
│  重复 Step 1–3 直到所有点被访问                                │
│  输出: labels[] 数组（簇 ID 或 -1）                           │
└───────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Ester et al., KDD 1996, Sec. 3 (Algorithm DBSCAN)

### 2.2 为什么用"密度可达"而不是"直接距离"？

**为什么不直接用阈值距离划分？**

如果只用"两点距离 ≤ ε 则同簇"，会出现月牙形等复杂形状被切断的问题——只有相互直接相邻才算同簇，稍微弯曲的链就断了。

DBSCAN 的设计决策：**用传递性的密度可达链**。只要存在一条核心点接力链，两点就属于同一簇。这使得算法能"爬过"任意形状的密集区域，同时在稀疏区域（密度低于阈值）自动断开。

> 📖 Paper: Ester et al., KDD 1996, Definitions 4–6 + Lemma 1

### 2.3 ε 参数如何选择？（k-NN 距离图法）

**实证方法（Ester 1996 原论文提出）：**

1. 对每个点，计算到其第 k 近邻的距离（k = min_samples - 1）
2. 按距离从大到小排序，绘制"k-NN 距离图"
3. 找到图中**曲率最大的"肘部"（elbow）** → 这就是合适的 ε

**直觉**：ε 设太小 → 大多数点变噪声；ε 设太大 → 所有点并入一个大簇。肘部是分水岭。

> 📖 Paper: Ester et al., KDD 1996, Sec. 4 (Determining the Parameters ε and MinPts)

### 2.4 sklearn 实现与原始论文的差异

```
原始论文             sklearn 实现
─────────────────    ─────────────────────────────────
O(n) 内存           O(n·d)（d=平均邻居数）
R*-Tree 索引        KD-Tree / Ball-Tree / brute-force
Sequential scan      批量邻域查询（radius_neighbors）
```

**为什么 sklearn 内存更大？** sklearn 批量计算所有点的邻域并存储，牺牲内存换取向量化计算速度。

> 💻 Source: [sklearn _dbscan.py L427-L463](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)
> 📖 Paper: Schubert et al., TODS 2017, Sec. 3 (Implementation Details)

---

## Section 3: 局限性

1. **变密度簇问题** → 不同簇密度差异大时，单一 ε 无法同时适配；应对策略：改用 HDBSCAN（自动选择多尺度密度）
2. **高维数据失效** → 维度诅咒导致所有点的距离趋同，ε 邻域要么空要么全；应对策略：降维（PCA/UMAP）再聚类，或用余弦距离
3. **边界点不唯一分配** → 边界点可能同时属于多个核心点的邻域，分配结果依赖处理顺序；应对策略：接受不确定性，或改用 HDBSCAN（有明确的边界处理）
4. **参数敏感性** → ε 和 min_samples 的选取对结果影响很大；应对策略：用 k-NN 距离图 + 领域知识选取

> 📖 Paper: Schubert et al., TODS 2017, Sec. 2 (Common Misconceptions about DBSCAN)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **K-Means** | 快、简单、可扩展 | 需预设 K，只支持球形簇，不处理噪声 | 均匀球形簇 |
| **DBSCAN** | 不需 K，任意形状，噪声识别 | 变密度失效，高维失效 | 空间数据，含噪声 |
| **HDBSCAN** | 处理变密度，层次结构 | 实现复杂，参数更多 | 复杂密度分布 |
| **OPTICS** | 可视化有序性图，处理变密度 | 不直接输出簇，需后处理 | 探索性分析 |
| **Agglomerative** | 层次树可视化 | O(n²)，不处理噪声 | 小数据集 |
| **Spectral** | 可发现非凸簇 | 需预设 K，计算昂贵 | 图/网络数据 |

> 📖 Paper: Ester et al., KDD 1996, Sec. 5 (Comparison with CLARANS)
> 📖 Docs: [sklearn 聚类算法对比](https://scikit-learn.org/stable/modules/clustering.html#overview-of-clustering-methods)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Ester et al. KDD 1996](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf) | 📖 论文 | Section 0-3（核心算法+参数选择+与 CLARANS 对比） |
| [Schubert et al. TODS 2017](https://doi.org/10.1145/3068335) | 📖 论文 | Section 2-4（实现细节+局限性+常见误解） |
| [sklearn DBSCAN 文档](https://scikit-learn.org/stable/modules/clustering.html#dbscan) | 📖 文档 | Section 4（算法对比表） |
| [sklearn _dbscan.py](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py) | 💻 源码 | Section 2.4（sklearn 实现差异） |
