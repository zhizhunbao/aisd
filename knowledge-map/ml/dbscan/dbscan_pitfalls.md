---
topic: dbscan
dimension: pitfalls
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Schubert et al. TODS 2017 — https://doi.org/10.1145/3068335"
  - "📖 Docs: scikit-learn DBSCAN — https://scikit-learn.org/stable/modules/clustering.html#dbscan"
  - "💻 Source: scikit-learn _dbscan.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_dbscan.py"
  - "🧪 经验: 工程实践中常见 DBSCAN 使用错误总结"
expiry: 6m
status: current
---

# DBSCAN 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 忘记标准化数据（最常见错误）

**场景：** 数据有多列特征，各列量纲不同（如身高 cm + 体重 kg + 年龄 year）

**症状：** DBSCAN 把所有点聚成一个大簇，或把几乎所有点标为噪声；调整 eps 完全没规律

**根因：** DBSCAN 直接用欧氏距离，量纲大的特征（如体重 0-100 kg）主导了距离计算，量纲小的特征（如年龄 0-80 year）几乎没有影响，导致距离计算失真

**解法：**

❌ 错误写法 — 直接用原始特征

```python
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=5).fit(X_raw)  # X_raw 直接含不同量纲的特征
```

✅ 正确写法 — 先标准化再聚类

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

X_scaled = StandardScaler().fit_transform(X_raw)
db = DBSCAN(eps=0.5).fit(X_scaled)  # eps 在标准化空间是 0.5
```

**教训：** DBSCAN 对尺度高度敏感，标准化是强制要求（除非你的距离函数本身处理量纲）

> 📖 Docs: [sklearn DBSCAN User Guide](https://scikit-learn.org/stable/modules/clustering.html#dbscan) (Note on Preprocessing)

---

## 坑 2: Silhouette 分数计算时未过滤噪声点

**场景：** 聚类完成后，用 Silhouette Coefficient 评估聚类质量

**症状：** `ValueError: Number of labels is 1`，或 Silhouette 值异常低/高（-1 标签的噪声点干扰了计算）

**根因：** `silhouette_score` 要求所有传入点都有有效标签（非负整数），而 DBSCAN 的噪声点标签是 -1，导致计算错误

**解法：**

❌ 错误写法 — 直接计算（含噪声点）

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, db.labels_)  # 若有 -1 标签则报错或结果不准
```

✅ 正确写法 — 过滤噪声点后计算

```python
from sklearn.metrics import silhouette_score
import numpy as np

mask = db.labels_ != -1              # 过滤噪声点 / Filter noise points
if len(set(db.labels_[mask])) > 1:   # 至少 2 个簇才能计算
    score = silhouette_score(X[mask], db.labels_[mask])
    print(f"Silhouette (non-noise): {score:.3f}")
else:
    print("只有一个有效簇，无法计算 Silhouette / Only 1 valid cluster")
```

**教训：** DBSCAN 的评估需要特殊处理噪声点，不能直接套用 K-Means 的评估代码

> 📖 Docs: [sklearn silhouette_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)

---

## 坑 3: eps 选太大，所有点并入一个簇

**场景：** DBSCAN 运行完，`labels_` 中只有 0（一个大簇），簇数 = 1，噪声点 = 0

**症状：** 聚类结果无意义，所有点都在同一个簇里

**根因：** eps 太大，导致每个点的邻域覆盖了整个数据集，所有点都密度可达，扩展成一个超级大簇

**解法：**

❌ 错误做法 — 随意设 eps

```python
db = DBSCAN(eps=100, min_samples=5).fit(X_scaled)  # eps=100 远大于数据范围
```

✅ 正确做法 — 用 k-NN 距离图选 eps（肘部法）

```python
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt

k = 4  # = min_samples - 1（推荐：min_samples = 维度数 + 1）
nbrs = NearestNeighbors(n_neighbors=k).fit(X_scaled)
dist, _ = nbrs.kneighbors(X_scaled)
kth_dist = np.sort(dist[:, -1])[::-1]  # 排序后的 k 近邻距离

plt.plot(kth_dist)
plt.ylabel(f"{k}-NN Distance")
plt.title("Find the elbow for ε (eps)")
plt.show()
# 选"肘部"对应的距离值作为 eps
```

**教训：** 先画 k-NN 距离图，eps 必须用数据驱动的方式选取，不能拍脑袋

> 📖 Paper: Ester et al., KDD 1996, Sec. 4 (Determining ε)

---

## 坑 4: 边界点分配不唯一，结果不可重现

**场景：** 同样的数据多次运行 DBSCAN，某些边界点（Border Points）的簇标签不同

**症状：** 结果在不同 sklearn 版本或数据顺序下略有不同（特别是数据点顺序改变后）

**根因：** 当一个边界点同时在多个核心点的 ε 邻域内时，它被分配到先处理的核心点所在的簇——这是 DBSCAN 的理论设计，原始论文定义的边界点归属本就不唯一

**解法：**

❌ 错误预期 — 依赖边界点标签做精确稳定计算

```python
# 不要把边界点的簇 ID 作为稳定特征传给下游系统
border_cluster_ids = db.labels_[border_indices]  # 结果可能随顺序变化
```

✅ 正确做法 — 只依赖核心点标签（稳定），边界点单独处理

```python
import numpy as np

# 以核心点为基础分析 / Base analysis on core points (stable)
core_mask = np.zeros_like(db.labels_, dtype=bool)
core_mask[db.core_sample_indices_] = True

stable_labels = db.labels_.copy()
stable_labels[~core_mask & (db.labels_ != -1)] = -2  # 边界点另行标记

# 或换用 HDBSCAN（提供 soft clustering，明确处理边界点）
# from hdbscan import HDBSCAN
# db2 = HDBSCAN(min_cluster_size=5).fit(X_scaled)
```

**教训：** 边界点归属是 DBSCAN 的固有不确定性，不是 bug；需要确定性时用核心点或改用 HDBSCAN

> 📖 Paper: Schubert et al., TODS 2017, Sec. 2.3 (Border Points Ambiguity)

---

## 坑 5: 高维数据用欧氏距离，聚类全失效

**场景：** 文本嵌入（768 维 BERT）或图像特征（2048 维 ResNet）使用 DBSCAN

**症状：** 几乎所有点变噪声，或全部并入一个大簇，调啥 eps 都没用

**根因：** 维度诅咒（Curse of Dimensionality）：高维空间中随机向量之间的距离趋于相等，欧氏距离失去区分能力，导致"邻域"失去意义

**解法：**

❌ 错误写法 — 高维特征直接 DBSCAN + 欧氏距离

```python
db = DBSCAN(eps=0.5, metric='euclidean').fit(X_high_dim)
# X_high_dim: shape (n, 768)，所有点距离趋同 → 聚类结果无意义
```

✅ 正确写法 A — 先用 UMAP 降维

```python
import umap
from sklearn.cluster import DBSCAN

X_2d = umap.UMAP(n_components=2, random_state=42).fit_transform(X_high_dim)
db = DBSCAN(eps=0.5, min_samples=5).fit(X_2d)
```

✅ 正确写法 B — 改用余弦距离（文本嵌入更适合）

```python
from sklearn.cluster import DBSCAN

# 余弦距离 = 1 - cosine_similarity，range [0, 2]
db = DBSCAN(eps=0.3, min_samples=5, metric='cosine').fit(X_high_dim)
```

**教训：** DBSCAN 在高维空间应先降维；文本/图像特征用余弦距离比欧氏距离更合适

> 📖 Paper: Schubert et al., TODS 2017, Sec. 2.2 (High-dimensional data)

---

## 坑 6: sklearn 大数据集内存爆炸

**场景：** 数据集超过 10 万点，运行 DBSCAN 时内存溢出

**症状：** `MemoryError` 或进程被系统 kill

**根因：** sklearn 的 DBSCAN 批量计算所有点的 ε 邻域并存储，内存复杂度 $O(n \cdot d)$（$d$ = 平均邻居数），当数据量大且 eps 稍大时，$d$ 会很大

**解法：**

❌ 错误写法 — 直接跑大数据集

```python
db = DBSCAN(eps=0.5, min_samples=10).fit(X_large)  # n > 100k → OOM
```

✅ 正确写法 — 预计算稀疏邻域图，节省内存

```python
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

# 预计算稀疏邻域（只存 eps 内的邻居）/ Precompute sparse neighborhoods
nbrs = NearestNeighbors(radius=0.5, algorithm='ball_tree', n_jobs=-1)
nbrs.fit(X_large)
sparse_graph = nbrs.radius_neighbors_graph(X_large, mode='distance')

# 使用预计算距离矩阵 / Use precomputed sparse matrix
db = DBSCAN(eps=0.5, min_samples=10, metric='precomputed').fit(sparse_graph)
print(f"簇数 / n_clusters: {len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)}")
```

**教训：** 大数据集必须用 `radius_neighbors_graph` + `metric='precomputed'`；或改用 HDBSCAN（内存更友好）

> 💻 Source: [sklearn _dbscan.py L144-L162](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)
> 📖 Paper: Schubert et al., TODS 2017, Sec. 3 (Efficient DBSCAN Implementations)

---

## 调试清单

1. [ ] **数据是否标准化？** → `StandardScaler().fit_transform(X)` 必须在 DBSCAN 之前
2. [ ] **eps 是否用 k-NN 距离图选取？** → 肘部法，不能随意猜测
3. [ ] **min_samples 是否合理？** → 通常 ≥ 维度数 + 1（2D 数据最少 3）
4. [ ] **结果只有一个簇？** → eps 太大，按 k-NN 图减小 eps
5. [ ] **结果全是噪声？** → eps 太小，或 min_samples 太大；按 k-NN 图增大 eps
6. [ ] **Silhouette 计算报错？** → 过滤 `labels_ != -1` 的点再计算
7. [ ] **边界点标签不稳定？** → 属于算法固有性质，设计时避免依赖边界点
8. [ ] **高维数据 DBSCAN 失效？** → 先 UMAP 降维，或改用余弦距离
9. [ ] **大数据集内存溢出？** → 用 `radius_neighbors_graph` 预计算稀疏图
10. [ ] **不同数据密度差异大？** → 考虑改用 HDBSCAN（自适应密度阈值）
