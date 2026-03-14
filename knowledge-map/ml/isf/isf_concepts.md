---
topic: isf
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Liu et al., 'Isolation Forest', ICDM 2008 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Paper: Liu et al., 'Isolation-Based Anomaly Detection', TKDD 2012 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Docs: scikit-learn IsolationForest — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html"
  - "💻 Source: sklearn/_iforest.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py"
expiry: 12m
status: current
---

# Isolation Forest 核心概念

> 📖 Paper: Liu et al., [Isolation Forest](https://doi.org/10.1109/ICDM.2008.17), ICDM 2008
> 📖 Docs: [scikit-learn IsolationForest User Guide](https://scikit-learn.org/stable/modules/outlier_detection.html#isolation-forest)

---

## 术语定义

### 隔离树 (Isolation Tree / iTree)

一棵随机构建的二叉树：每次随机选一个特征，再随机选一个分割值（在该特征的 min–max 范围内），将样本递归分割，直到每个叶节点只剩一个样本或树达到最大深度。

> 易混淆：**iTree vs 决策树** — 决策树用信息增益最大化来选分割点（有监督）；iTree 完全随机选分割（无监督），目的是测量"隔离一个点需要多少步"，而不是学分类边界。

### 路径长度 (Path Length / h(x))

给定样本 x，从 iTree 根节点到包含 x 的叶节点所经历的边数（加上到达叶节点时的调整项）。路径越短 → 越难被"周围点包围" → 越异常。

> 易混淆：**路径长度 vs 树深度** — 树深度是树的全局属性（最大层数）；路径长度是针对**某个样本**在某棵树中的层数，是样本级的指标。

### 期望路径长度归一化因子 (c(n))

`c(n)` 是用 n 个样本构建的二叉搜索树（BST）中一次**不成功搜索**的平均路径长度，公式为 `c(n) = 2H(n-1) - 2(n-1)/n`，其中 H 是调和数。用于将各棵树的路径长度归一化到 [0,1]，消除子样本数量的影响。

> 易混淆：**c(n) vs n** — c(n) 是期望路径长度（理论值），n 是子样本数量（`max_samples`）；归一化除以 c(n) 而不是直接除以 n 是因为随机树的路径分布服从 BST 的期望路径。

### 异常分数 (Anomaly Score / s(x, n))

对 T 棵 iTree 的路径长度取均值后，通过公式 `s(x,n) = 2^{-E[h(x)]/c(n)}` 映射到 [0,1]：
- 分数接近 1：路径极短 → **高度异常**
- 分数接近 0.5：路径与均值相近 → **无法区分**
- 分数接近 0：路径极长 → **正常点**

> 易混淆：**score_samples vs decision_function** — `score_samples` 是原始异常分数（越低越异常，与论文相反符号）；`decision_function = score_samples - offset_`，以 0 为阈值，负值 = 异常。

### 污染率 (Contamination)

用户提供的先验估计：数据集中异常点所占比例。在 `contamination='auto'` 时，threshold 设为 -0.5（对应论文原定义）。若设具体浮点数，则按该比例取分位数作为阈值。

> 易混淆：**contamination vs threshold** — contamination 是**输入参数**（你对数据中异常比例的估计）；threshold 是内部计算的分数阈值，由 contamination 决定。

### 子采样 (Subsampling / max_samples)

训练每棵 iTree 时只使用 `max_samples` 个样本（默认 `min(256, n)`）。论文证明 256 已足够：异常点在小样本下就能被快速隔离，过多样本反而引入"遮蔽效应"（inlier masking），让正常点"保护"了异常点。

> 易混淆：**max_samples vs bootstrap** — max_samples 是每棵树用多少样本（**不放回**抽样，默认）；bootstrap=True 时改为**放回**抽样（类似随机森林），会导致异常检测能力下降，一般不推荐开启。

> 📖 Paper: Liu et al., ICDM 2008, Section 2.1–2.3
> 💻 Source: [sklearn/_iforest.py](../../.github/scikit-learn/sklearn/ensemble/_iforest.py) `L55-L227`

---

## 概念辨析

### Isolation Forest vs LOF

| 维度 | Isolation Forest | LOF |
|------|-----------------|-----|
| **核心思路** | 随机分割树，测路径长度 | 计算局部密度与邻居密度之比 |
| **数据假设** | 无分布假设 | 假设局部密度可比 |
| **时间复杂度** | O(n log n) 训练 | O(n²) 训练 |
| **高维性能** | 友好（随机特征选择自然降维） | 高维时密度估计崩溃（维度灾难） |
| **局部/全局** | 全局检测（路径长度全局比较） | 局部检测（与邻居相比） |
| **典型适用** | 大数据、高维、实时评分 | 小数据、低维、局部簇内异常 |

> 📖 Paper: Liu et al., TKDD 2012, Section 6（对比实验）

### score_samples vs decision_function vs predict

| 方法 | 输出含义 | 范围 | 正负含义 |
|------|---------|------|---------|
| `score_samples(X)` | 原始异常分数的负值 | (-∞, 0] | 越负越异常 |
| `decision_function(X)` | `score_samples - offset_` | 实值 | <0 异常，>0 正常 |
| `predict(X)` | 标签 | {-1, +1} | -1 异常，+1 正常 |

> 💻 Source: [sklearn/_iforest.py](../../.github/scikit-learn/sklearn/ensemble/_iforest.py) `L393-L431`

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────┐
│              Isolation Forest                    │
├──────────────────────────────────────────────────┤
│ 训练阶段                                          │
│  └─ 构建 T 棵 iTree（每棵用 max_samples 子采样）  │
│      └─ 每棵树：随机选特征 → 随机选分割值 → 递归    │
│         直到叶节点=1个样本 或 达到 max_depth       │
├──────────────────────────────────────────────────┤
│ 评分阶段                                          │
│  └─ 样本 x 在每棵 iTree 中走到叶节点              │
│      ├─ 记录路径长度 h(x)                         │
│      └─ 加上叶节点调整项 c(叶节点样本数)           │
│  └─ T 棵树平均路径长度 E[h(x)]                   │
│  └─ 归一化: s = 2^{-E[h(x)]/c(n)}               │
├──────────────────────────────────────────────────┤
│ 判决阶段                                          │
│  └─ s - offset_ 与 0 比较 → predict {-1, +1}    │
└──────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn/_iforest.py](../../.github/scikit-learn/sklearn/ensemble/_iforest.py) `L550-L640`

### 适用场景 ✅

- 数据量大（>10k 样本），需要高效异常检测
- 高维特征空间（图像特征、日志向量、网络特征）
- 无标签数据，需要完全无监督
- 需要实时或批量为新样本打分
- 全局稀疏异常（异常点在全局特征空间中孤立）

### 不适用场景 ❌

- 低维数据中的局部簇内异常（用 LOF 更合适）
- 已知数据服从高斯分布（用 EllipticEnvelope）
- 需要可解释性（ISF 分数难以直接解释"为什么是异常"）
- 数据中异常点极密集成群（群体异常）

> 📖 Paper: Liu et al., TKDD 2012, Section 5–6

---

## 速查表

| 项 | 说明 | 默认值/示例 |
|-----|------|------------|
| `n_estimators` | 隔离树数量 | 100 |
| `max_samples` | 每棵树的子采样大小 | `min(256, n_samples)` |
| `contamination` | 异常比例先验估计 | `'auto'`（等价 offset=-0.5） |
| `max_features` | 每棵树使用的特征数 | 1.0（全特征） |
| `bootstrap` | 是否有放回抽样 | False |
| `random_state` | 随机种子 | None |
| 异常输出 | `predict` 返回 | -1（异常）/ +1（正常） |
| 分数范围 | `score_samples` | 越负越异常 |

> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
