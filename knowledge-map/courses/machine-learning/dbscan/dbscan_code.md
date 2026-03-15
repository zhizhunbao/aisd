---
topic: dbscan
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn DBSCAN API — https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html"
  - "💻 Source: scikit-learn _dbscan.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_dbscan.py"
  - "💻 Source: sklearn plot_dbscan.py example — https://github.com/scikit-learn/scikit-learn/blob/main/examples/cluster/plot_dbscan.py"
expiry: 6m
status: current
---

# DBSCAN 代码参考

> 📖 Docs: [scikit-learn DBSCAN API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
> 💻 Source: [sklearn _dbscan.py](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np
from sklearn.cluster import DBSCAN

# 示例数据：6 个点，其中 [25, 80] 应为噪声
# Sample data: 6 points, [25, 80] should be noise
X = np.array([[1, 2], [2, 2], [2, 3],
              [8, 7], [8, 8], [25, 80]])

# 创建并拟合 DBSCAN 模型
# Create and fit the DBSCAN model
db = DBSCAN(eps=3, min_samples=2).fit(X)

# 输出结果
# Output results
print(db.labels_)           # [ 0  0  0  1  1 -1]  （-1 = 噪声）
print(db.core_sample_indices_)  # [0 1 2 3 4]  （索引 5 即 [25,80] 不是核心点）
```

**测试方法：** 直接运行，`labels_` 中出现 `-1` 即噪声，非负整数为簇 ID

> 💻 Source: [sklearn _dbscan.py L339-L353](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)

---

## 完整实现示例

### 示例 1: 含可视化的完整 DBSCAN 流程（基于 sklearn 官方示例）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics

# 生成合成数据（3 个簇，共 750 点）
# Generate synthetic data (3 clusters, 750 points)
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(
    n_samples=750,
    centers=centers,
    cluster_std=0.4,
    random_state=0
)
# 标准化（DBSCAN 对尺度敏感，建议归一化）
# Standardize (DBSCAN is scale-sensitive, normalization recommended)
X = StandardScaler().fit_transform(X)

# ============================================================
# 2. DBSCAN 聚类 / DBSCAN Clustering
# ============================================================
db = DBSCAN(
    eps=0.3,           # 邻域半径 / neighborhood radius
    min_samples=10,    # 核心点最少邻居数 / min neighbors for core point
    metric='euclidean',# 距离度量 / distance metric
    n_jobs=-1          # 使用全部 CPU / use all CPUs
).fit(X)

labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)

print(f"簇数量 / Estimated clusters: {n_clusters}")
print(f"噪声点 / Noise points: {n_noise}")

# ============================================================
# 3. 评估指标 / Evaluation (需要真实标签)
# ============================================================
print(f"Homogeneity:  {metrics.homogeneity_score(labels_true, labels):.3f}")
print(f"Completeness: {metrics.completeness_score(labels_true, labels):.3f}")
print(f"V-measure:    {metrics.v_measure_score(labels_true, labels):.3f}")
print(f"Adjusted Rand Index: {metrics.adjusted_rand_score(labels_true, labels):.3f}")
# 无真实标签时用 Silhouette（-1 表示噪声点，需过滤）
# Without ground truth, use Silhouette (filter -1 noise first)
mask = labels != -1
if mask.sum() > 1:
    print(f"Silhouette (non-noise): {metrics.silhouette_score(X[mask], labels[mask]):.3f}")

# ============================================================
# 4. 可视化 / Visualization
# ============================================================
unique_labels = set(labels)
core_mask = np.zeros_like(labels, dtype=bool)
core_mask[db.core_sample_indices_] = True
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]

for k, col in zip(unique_labels, colors):
    if k == -1:
        col = [0, 0, 0, 1]  # 噪声用黑色 / noise in black
    class_mask = labels == k
    # 核心点：大圆 / Core points: large dots
    xy = X[class_mask & core_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)
    # 边界点：小圆 / Border points: small dots
    xy = X[class_mask & ~core_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title(f"DBSCAN — {n_clusters} clusters, {n_noise} noise points")
plt.tight_layout()
plt.savefig("dbscan_result.png", dpi=150)
plt.show()
```

> 💻 Source: [sklearn plot_dbscan.py](../../../.github/scikit-learn/examples/cluster/plot_dbscan.py)
> 📖 Docs: [sklearn DBSCAN User Guide](https://scikit-learn.org/stable/modules/clustering.html#dbscan)

---

### 示例 2: 使用预计算距离矩阵（适合自定义距离函数）

```python
# ============================================================
# 1. 构造自定义距离矩阵 / Build custom distance matrix
# ============================================================
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import pairwise_distances

X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])

# 计算距离矩阵（可替换为自定义距离函数）
# Compute distance matrix (replace with custom distance function if needed)
dist_matrix = pairwise_distances(X, metric='euclidean')

# ============================================================
# 2. 使用 metric='precomputed' / Use precomputed distance matrix
# ============================================================
db = DBSCAN(
    eps=3,
    min_samples=2,
    metric='precomputed'  # 告知 sklearn 直接使用距离矩阵 / tell sklearn to use distance matrix
).fit(dist_matrix)

print(f"Labels: {db.labels_}")   # [ 0  0  0  1  1 -1]
```

> 💻 Source: [sklearn _dbscan.py L57-L62](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)

---

### 示例 3: ε 参数选择（k-NN 距离图法）

```python
# ============================================================
# 选择最优 ε：k-NN 距离图 / Choosing optimal ε: k-NN distance plot
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# 假设已有数据 X，min_samples=5
# Assume X is available, min_samples=5
def plot_knn_distances(X, min_samples=5):
    k = min_samples - 1                    # k = min_samples - 1（含自身则 -1）
    nbrs = NearestNeighbors(n_neighbors=k).fit(X)
    distances, _ = nbrs.kneighbors(X)
    
    # 取第 k 近邻距离（最后一列），排序
    # Take k-th neighbor distance (last column), sort descending
    kth_distances = np.sort(distances[:, -1])[::-1]
    
    plt.figure(figsize=(8, 4))
    plt.plot(kth_distances)
    plt.xlabel("Points sorted by distance")
    plt.ylabel(f"{k}-NN Distance")
    plt.title("k-NN Distance Plot — Look for the 'Elbow'")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("knn_distance_plot.png", dpi=150)
    plt.show()
    print("选肘部对应的距离值作为 ε")
    print("Choose the distance at the 'elbow' as ε")

# 生成示例数据后调用
# Call after generating sample data
from sklearn.datasets import make_blobs
X, _ = make_blobs(n_samples=300, centers=3, random_state=42)
plot_knn_distances(X, min_samples=5)
```

> 📖 Paper: Ester et al., KDD 1996, Sec. 4 (Determining ε and MinPts)

---

## API 速查

### DBSCAN 类

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `DBSCAN(...)` | `eps` | `0.5` | 邻域半径（最重要参数）|
| ↳ | `min_samples` | `5` | 核心点的最少邻居数（含自身）|
| ↳ | `metric` | `'euclidean'` | 距离度量；`'precomputed'` 接受距离矩阵 |
| ↳ | `algorithm` | `'auto'` | 邻域搜索算法：auto/ball_tree/kd_tree/brute |
| ↳ | `leaf_size` | `30` | BallTree/KDTree 叶节点大小 |
| ↳ | `p` | `None` | Minkowski metric 的 p 值（None = 2 = 欧氏）|
| ↳ | `n_jobs` | `None` | 并行数（-1=全核）|

### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `.labels_` | `ndarray (n,)` | 簇标签，-1 表示噪声 |
| `.core_sample_indices_` | `ndarray` | 核心点的索引（在原始 X 中）|
| `.components_` | `ndarray (n_core, n_feat)` | 核心点的特征向量副本 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `db.fit(X)` | 拟合并聚类 |
| `db.fit_predict(X)` | 拟合并返回标签（等价于 fit 后取 labels_）|
| `set(labels) - {-1}` | 获得所有非噪声簇 ID |
| `(labels != -1).sum()` | 非噪声点数量 |
| `metrics.silhouette_score(X[mask], labels[mask])` | 轮廓系数（过滤噪声后）|

> 📖 Docs: [sklearn DBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
> 💻 Source: [sklearn _dbscan.py](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py)

---

## 目录结构模板

### 简单结构

```
dbscan_project/
├── run_dbscan.py          ← 入口脚本（数据加载+聚类+评估）
├── data/
│   └── points.csv         ← 输入数据
└── output/
    └── dbscan_result.png  ← 可视化图
```

### 标准结构

```
dbscan_project/
├── config.py              ← eps, min_samples, metric 等参数
├── preprocess.py          ← 数据加载 + 标准化
├── cluster.py             ← DBSCAN 聚类封装
├── evaluate.py            ← 聚类评估指标
├── visualize.py           ← 结果可视化
├── main.py                ← 主入口
├── data/
│   ├── raw/
│   └── processed/
└── output/
    ├── plots/
    └── labels.npy         ← 保存聚类结果
```

> 📖 Docs: [sklearn 聚类文档](https://scikit-learn.org/stable/modules/clustering.html)
