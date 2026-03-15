---
topic: kmeans
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn KMeans API — https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html"
  - "💻 Source: sklearn/cluster/_kmeans.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/cluster/_kmeans.py"
  - "📚 Book: Murphy K.P., PML1 Ch.21 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
expiry: 6m
status: current
---

# K-Means 代码参考

> 📖 Docs: [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)
> 💻 Source: [sklearn/cluster/_kmeans.py](../../../.github/scikit-learn/sklearn/cluster/_kmeans.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.cluster import KMeans
import numpy as np

# ============================================================
# 生成示例数据 / Generate sample data
# ============================================================
np.random.seed(42)
X = np.vstack([
    np.random.randn(100, 2) + np.array([0, 0]),   # 簇 1 / Cluster 1
    np.random.randn(100, 2) + np.array([5, 5]),   # 簇 2 / Cluster 2
    np.random.randn(100, 2) + np.array([10, 0]),  # 簇 3 / Cluster 3
])

# ============================================================
# 拟合 K-Means 模型 / Fit K-Means model
# ============================================================
kmeans = KMeans(
    n_clusters=3,        # 簇数 K / Number of clusters
    init='k-means++',    # K-Means++ 初始化（推荐）/ K-Means++ init (recommended)
    n_init=10,           # 随机重启 10 次，取最优 / 10 random restarts
    random_state=42      # 可复现 / Reproducibility
)
kmeans.fit(X)

# ============================================================
# 查看结果 / View results
# ============================================================
print("簇标签 Labels:", kmeans.labels_[:5])          # 每点的簇编号
print("质心 Centers:", kmeans.cluster_centers_)      # K 个质心坐标
print("WCSS (Inertia):", kmeans.inertia_)            # 越小越好
```

**测试方法：** 运行后应看到 3 个质心坐标分别接近 (0,0), (5,5), (10,0)，inertia 约 600

> 📖 scikit-learn [KMeans docs](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

---


## 完整实现示例

### 示例 1: 用 Elbow Method 选最优 K（标准化 + 可视化）

```python
# ============================================================
# 1. 导入 / Imports
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs

# ============================================================
# 2. 数据准备 / Data Preparation
# ============================================================
# 生成 4 个 blob 的合成数据 / Generate synthetic 4-blob data
X, y_true = make_blobs(
    n_samples=400,
    centers=4,           # 真实簇数（用于对比验证）/ True cluster count
    random_state=42
)

# 标准化（重要！K-Means 对量纲敏感）/ Standardize (critical! K-Means is scale-sensitive)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================================
# 3. Elbow Method — 扫描不同 K / Sweep different K values
# ============================================================
inertias = []           # 记录每个 K 的 WCSS / Record WCSS for each K
k_range = range(1, 11)  # 测试 K=1…10 / Test K=1 to 10

for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)  # 收集 WCSS / Collect WCSS

# ============================================================
# 4. 可视化 Elbow 曲线 / Visualize Elbow curve
# ============================================================
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(k_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (WCSS)')
plt.title('Elbow Method — 选 WCSS 下降开始变缓的 K')  # Select K where WCSS drop slows

# ============================================================
# 5. 拟合最优模型并可视化聚类结果 / Fit best model & visualize
# ============================================================
best_k = 4
km_best = KMeans(n_clusters=best_k, init='k-means++', n_init=10, random_state=42)
km_best.fit(X_scaled)

plt.subplot(1, 2, 2)
scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=km_best.labels_, cmap='tab10', alpha=0.6)
centers_scaled = km_best.cluster_centers_
plt.scatter(centers_scaled[:, 0], centers_scaled[:, 1],
            c='red', marker='x', s=200, linewidths=3,  # 质心标红 X / Mark centers with red X
            label='Centroids')
plt.title(f'K-Means Clustering (K={best_k})')
plt.legend()
plt.tight_layout()
plt.savefig('kmeans_result.png', dpi=150)
plt.show()

print(f"\n最终 WCSS: {km_best.inertia_:.2f}")        # Final WCSS
print(f"质心数组 shape: {km_best.cluster_centers_.shape}")  # (K, D) shape
```

> 📖 scikit-learn [Examples](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html)

---

### 示例 2: Silhouette Score 选 K（更准确的评估）

```python
# ============================================================
# Silhouette 分析 — 衡量聚类"凝聚度"和"分离度" / Silhouette analysis
# ============================================================
from sklearn.metrics import silhouette_score

sil_scores = []  # 越接近 1 越好 / Closer to 1 is better
k_range = range(2, 11)  # Silhouette 从 K=2 开始 / Silhouette starts at K=2

for k in k_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)            # 直接返回标签 / Return labels directly
    score = silhouette_score(X_scaled, labels)   # 计算 Silhouette / Compute score
    sil_scores.append(score)
    print(f"K={k}: Silhouette={score:.4f}")

# 选 Silhouette 最大的 K / Select K with max Silhouette
best_k = k_range[np.argmax(sil_scores)]
print(f"\n最优 K: {best_k}")  # Best K
```

> 📖 scikit-learn [Silhouette analysis](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html)

---

### 示例 3: Mini-Batch K-Means — 超大规模数据

```python
# ============================================================
# Mini-Batch K-Means — 大数据场景 / Large-scale scenario
# ============================================================
from sklearn.cluster import MiniBatchKMeans

# 适合 N 很大时（100万+）/ Suitable when N is very large (1M+)
mbkm = MiniBatchKMeans(
    n_clusters=4,
    batch_size=1024,     # 每次迭代的批量大小 / Batch size per iteration
    init='k-means++',
    n_init=3,
    max_iter=100,
    random_state=42
)
mbkm.fit(X_scaled)
print(f"Mini-Batch WCSS: {mbkm.inertia_:.2f}")  # 略高于标准 K-Means，但快很多
```

> 💻 sklearn [MiniBatchKMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html)

---


## API 速查

### KMeans 主要参数

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `KMeans(...)` | `n_clusters` | 8 | 簇数 K，**必须指定** |
| ↳ | `init` | 'k-means++' | 初始化方式：'k-means++' 或 'random' |
| ↳ | `n_init` | 10 | 随机重启次数，取 WCSS 最小 |
| ↳ | `max_iter` | 300 | 最大迭代次数 |
| ↳ | `tol` | 1e-4 | 收敛阈值（质心移动量） |
| ↳ | `random_state` | None | 随机种子，用于复现 |
| ↳ | `algorithm` | 'lloyd' | 'lloyd' 或 'elkan'（对稠密数据更快） |

### KMeans 输出属性

| 属性 | 说明 | Shape |
|------|------|-------|
| `labels_` | 每个点的簇编号 (0~K-1) | (N,) |
| `cluster_centers_` | K 个质心的坐标 | (K, D) |
| `inertia_` | 最终 WCSS 值 | scalar |
| `n_iter_` | 实际迭代次数 | int |

### 常用工具

| 函数 | 说明 |
|------|------|
| `km.fit(X)` | 拟合模型 |
| `km.predict(X_new)` | 预测新点所属簇 |
| `km.fit_predict(X)` | 拟合并返回标签（等同 fit+labels_） |
| `silhouette_score(X, labels)` | Silhouette 评估 |
| `silhouette_samples(X, labels)` | 每点的 Silhouette 值 |

> 📖 scikit-learn [KMeans API](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

---


## 目录结构模板

### 简单结构

```
kmeans_project/
├── cluster.py            ← 聚类主脚本 / Main clustering script
├── select_k.py           ← K 选择（Elbow/Silhouette）/ K selection
└── data/
    └── dataset.csv
```

### 标准结构

```
kmeans_project/
├── config.py             ← 超参数配置 / Hyperparameters
├── data_loader.py        ← 数据加载和预处理 / Data loading & preprocessing
├── cluster.py            ← K-Means 聚类主逻辑 / Main K-Means logic
├── evaluate.py           ← 评估（Silhouette, WCSS）/ Evaluation metrics
├── visualize.py          ← 可视化聚类结果 / Visualization
├── data/
└── outputs/
    ├── cluster_results.csv
    └── plots/
```

> 💻 参考 [handson-ml3/09_unsupervised_learning.ipynb](../../../.github/handson-ml3/09_unsupervised_learning.ipynb)
