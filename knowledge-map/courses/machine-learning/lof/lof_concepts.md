---
topic: lof
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Breunig et al. SIGMOD 2000 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/lof/breunig_2000_lof.pdf"
  - "📖 Docs: scikit-learn LocalOutlierFactor — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html"
  - "💻 Source: scikit-learn _lof.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_lof.py"
expiry: 12m
status: current
---

# LOF 核心概念

> 📖 Paper: Breunig et al., [《LOF: Identifying Density-Based Local Outliers》](../../../.documents/papers/lof/breunig_2000_lof.pdf), SIGMOD 2000, Def. 1-6

---

## 术语定义

### k-distance — k距离

一个点 $p$ 的 k-distance（记作 $k\text{-dist}(p)$）是 $p$ 到它第 $k$ 个最近邻居的距离。这个距离定义了以 $p$ 为圆心、包含至少 $k$ 个其他点的最小球半径。

> 易混淆：**k-distance vs k-NN 距离** — k-distance 是到第 k 个邻居的距离（标量）；k-NN 距离通常泛指到所有 k 个邻居的距离集合（向量）

### k-distance 邻域 (k-distance Neighborhood)

$N_k(p) = \{q \neq p \mid \text{dist}(p,q) \leq k\text{-dist}(p)\}$。由于可能存在距离相等的点（ties），$|N_k(p)|$ 可能大于 $k$。

> 易混淆：**邻域大小 vs k** — $|N_k(p)| \geq k$ 恒成立，但可能 $|N_k(p)| > k$（存在距离相等的第 $k$ 和第 $k+1$ 个邻居时）

### 可达距离 (Reachability Distance)

点 $o$ 相对于点 $p$ 的可达距离：$\text{reach-dist}_k(o, p) = \max\{k\text{-dist}(p),\ \text{dist}(o, p)\}$。

这是一种"平滑"后的距离：对于处于密集核心区域内的点对，可达距离替换为 $k\text{-dist}(p)$，避免核心区内部距离因量化误差或极小值而产生噪声。

> 易混淆：**reach-dist(o,p) vs reach-dist(p,o)** — 非对称！$\text{reach-dist}(o,p)$ 与 $\text{reach-dist}(p,o)$ 通常不等

### 局部可达密度 (Local Reachability Density, LRD)

$$\text{lrd}_k(p) = \left(\frac{\sum_{o \in N_k(p)} \text{reach-dist}_k(o, p)}{|N_k(p)|}\right)^{-1}$$

LRD 是 $p$ 的邻居到 $p$ 的平均可达距离的倒数。数值越高 → $p$ 所处区域密度越高；数值越低 → 越稀疏。

> 易混淆：**LRD vs 核密度估计 KDE** — LRD 是非参数、基于 k 近邻的密度估计，只使用离散的 k 个邻居；KDE 使用全局带宽核函数

### 局部离群因子 (Local Outlier Factor, LOF)

$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$

LOF 是 $p$ 的邻居们的 LRD 与 $p$ 自身 LRD 的比值均值。比值 >> 1 说明邻居区域比 $p$ 稠密得多 → $p$ 是异常点。

> 易混淆：**LOF score vs negative_outlier_factor_** — sklearn 存储的是负 LOF 值（`negative_outlier_factor_`），数值越接近 -1 越正常，越小（如 -10）越异常

### MinPts / n_neighbors

LOF 的超参数，控制邻域大小。论文中记为 MinPts，sklearn 中为 `n_neighbors`（默认 20）。MinPts 越大，邻域越大，LOF 越平滑；MinPts 越小，越敏感但方差也更大。

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Def. 1-6 (pp. 94-96)
> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 496-521`

---

## 概念辨析

### LOF vs Isolation Forest

| 维度 | LOF | Isolation Forest |
|------|-----|-----------------|
| **本质** | 局部密度比较 | 随机分割隔离效率 |
| **输出** | 连续异常分数（软判断） | 连续异常分数（软判断） |
| **复杂度** | $O(n^2)$ 朴素；近似 $O(n \log n)$ | $O(n \log n)$ |
| **假设** | 无分布假设，仅依赖密度差异 | 异常点在随机树中更容易被隔离 |
| **适合场景** | 局部密度不均匀的数据 | 高维、大规模数据 |
| **典型应用** | 欺诈检测、网络入侵（低维） | 大规模工业异常检测 |

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 5 (Experiments)

### LOF vs DBSCAN 噪声点

| 维度 | LOF 异常 | DBSCAN 噪声点 |
|------|---------|--------------|
| **判断方式** | LOF 分数阈值 | 密度不足，无法成为核心点 |
| **输出** | 连续分数（程度） | 二值标签（是/否） |
| **对 MinPts 的依赖** | 强（k 影响 LRD） | 强（MinPts 决定核心点） |
| **多密度簇** | ✅ 支持（局部比较） | ❌ 困难（全局 ε 参数） |

> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 19-35`

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│  LOF 计算流水线                                               │
├──────────────────────────────────────────────────────────────┤
│ 输入层                                                        │
│  └─ 数据集 D，超参数 MinPts                                  │
├──────────────────────────────────────────────────────────────┤
│ 第一层：邻域                                                  │
│  ├─ k-dist(p)   ← 到第 k 邻居的距离                         │
│  └─ N_k(p)      ← k 邻域集合（可能 > k 个点）               │
├──────────────────────────────────────────────────────────────┤
│ 第二层：平滑距离                                              │
│  └─ reach-dist_k(o, p) = max{k-dist(p), dist(o,p)}         │
├──────────────────────────────────────────────────────────────┤
│ 第三层：局部密度                                              │
│  └─ LRD_k(p)   ← 平均可达距离的倒数                         │
├──────────────────────────────────────────────────────────────┤
│ 第四层：异常分数                                              │
│  └─ LOF_k(p)   ← 邻居 LRD 均值 / 自身 LRD                  │
└──────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Fig. 1

### 适用场景 ✅

- 数据集中存在**密度不均匀的簇**（不同区域稀疏程度差异大）
- 需要**连续异常分数**（而非二值标签），用于排序或置信度评估
- 低到中等维度的特征空间（< 50 维效果较好）
- 欺诈检测、网络入侵检测、医疗异常诊断等领域

### 不适用场景 ❌

- 超高维数据（维度灾难导致距离度量失效）
- 超大规模数据集（朴素实现 $O(n^2)$，百万级别时开销大）
- 需要在线/流式更新的场景（LOF 必须重新训练）
- 数据完全服从单一高斯分布（此时简单 Z-score 即可）

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 6 (Conclusions)

---

## 速查表

| 概念 | 公式/定义 | 典型值 |
|------|----------|--------|
| k-distance(p) | 到第 k 个邻居的距离 | 取决于数据 |
| N_k(p) | k-dist 球内所有邻居 | ≥ k 个点 |
| reach-dist_k(o,p) | max{k-dist(p), dist(o,p)} | ≥ 0 |
| LRD_k(p) | 1 / 平均 reach-dist | > 0 |
| LOF_k(p) | 邻居平均 LRD / 自身 LRD | ≈1 正常，>>1 异常 |
| n_neighbors (sklearn) | MinPts 的实现参数 | 默认 20 |
| contamination | 预期异常比例 | 默认 "auto" (offset=-1.5) |
| negative_outlier_factor_ | -LOF（sklearn 存储） | 接近 -1 为正常 |

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Def. 1-6
> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 116-140`
