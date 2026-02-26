# Week 6: Clustering — 代码参考

> **Source:** slides `Week6Clustering.pdf` + sklearn documentation
> **Scope:** K-Means, Hierarchical/Agglomerative, DBSCAN, GMM (EM), Silhouette, visualization
> **See also:** [week6_clustering_cheatsheet.md](week6_clustering_cheatsheet.md) (概念速查) | [week6_clustering_math.md](week6_clustering_math.md) (公式+手算)

---

## K-Means Clustering

### 🔧 Code

- 🔧 **K-Means basic pipeline:**

```python
from sklearn.cluster import KMeans
import numpy as np

# K-Means clustering — specify K, fit, predict
# K均值聚类 — 指定K, 训练, 预测
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)                    # Fit to data
labels = kmeans.labels_          # Cluster assignments (0, 1, 2, ...)
centroids = kmeans.cluster_centers_  # Centroid coordinates
sse = kmeans.inertia_            # SSE (sum of squared distances to centroids)
```

- 🔧 **Elbow method — find optimal K by plotting SSE vs K:**

```python
import matplotlib.pyplot as plt

# Elbow method: plot SSE for K=1..10, look for "elbow" bend
# 肘部法：画出K=1..10的SSE，找拐点
sse_list = []
K_range = range(1, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    sse_list.append(km.inertia_)

plt.plot(K_range, sse_list, 'bo-')
plt.xlabel('Number of clusters K')
plt.ylabel('SSE (Inertia)')
plt.title('Elbow Method')
plt.show()
```

- 🔧 **Visualize K-Means clusters (2D):**

```python
import matplotlib.pyplot as plt

# Plot clusters with different colors + centroids as red X
# 画出聚类结果（不同颜色）+ 质心（红色X）
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=30, alpha=0.7)
plt.scatter(centroids[:, 0], centroids[:, 1],
            c='red', marker='X', s=200, edgecolors='black', linewidths=2)
plt.title('K-Means Clustering')
plt.show()
```

---

## Hierarchical / Agglomerative Clustering

### 🔧 Code

- 🔧 **Agglomerative clustering pipeline:**

```python
from sklearn.cluster import AgglomerativeClustering

# Agglomerative clustering — specify n_clusters and linkage
# 凝聚式层次聚类 — 指定簇数和链接方法
agg = AgglomerativeClustering(
    n_clusters=3,         # Number of clusters (or set to None + distance_threshold)
    linkage='ward'        # 'ward' | 'single' (MIN) | 'complete' (MAX) | 'average'
)
labels = agg.fit_predict(X)
```

- 🔧 **Dendrogram visualization:**

```python
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# Compute linkage matrix and plot dendrogram
# 计算链接矩阵并画树状图
Z = linkage(X, method='ward')  # 'single' | 'complete' | 'average' | 'ward'

plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode='level', p=5)  # p = depth to display
plt.xlabel('Sample index or cluster size')
plt.ylabel('Distance')
plt.title('Dendrogram (Ward Linkage)')
plt.show()
```

- 🔧 **Cut dendrogram at specific number of clusters:**

```python
from scipy.cluster.hierarchy import fcluster

# Cut dendrogram to get exactly K clusters
# 在树状图上切割得到K个簇
labels = fcluster(Z, t=3, criterion='maxclust')  # t = desired number of clusters
```

- 🔧 **Linkage method mapping:**

```python
# sklearn linkage parameter values:
# sklearn 链接方法参数值:
# 'single'   → MIN (nearest pair)        — 单链接（最近点对）
# 'complete' → MAX (farthest pair)        — 完全链接（最远点对）
# 'average'  → Group Average (mean pair)  — 组平均（平均距离）
# 'ward'     → Ward (minimize SSE increase) — Ward法（最小化SSE增量）
```

---

## DBSCAN

### 🔧 Code

- 🔧 **DBSCAN pipeline:**

```python
from sklearn.cluster import DBSCAN

# DBSCAN — specify eps (radius) and min_samples (MinPts)
# DBSCAN — 指定eps（半径）和min_samples（最小点数）
db = DBSCAN(eps=0.5, min_samples=5)  # ⚠️ min_samples includes the point itself
db.fit(X)

labels = db.labels_           # -1 = noise, 0,1,2... = cluster IDs
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)  # Count clusters (exclude noise)
n_noise = list(labels).count(-1)  # Count noise points

# Identify core, border, noise
# 识别核心点、边界点、噪声点
core_mask = np.zeros_like(labels, dtype=bool)
core_mask[db.core_sample_indices_] = True  # Core points
# Border = not core but labeled (not -1)
# Noise = labeled -1
```

- 🔧 **Visualize DBSCAN results with noise:**

```python
import matplotlib.pyplot as plt

# Color clusters, mark noise as black
# 簇用颜色区分，噪声点用黑色标记
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

for label, color in zip(unique_labels, colors):
    if label == -1:
        color = 'black'  # Noise = black / 噪声 = 黑色
    mask = (labels == label)
    is_core = core_mask & mask
    plt.scatter(X[is_core, 0], X[is_core, 1], c=[color], s=50, label=f'Core {label}')
    plt.scatter(X[~is_core & mask, 0], X[~is_core & mask, 1],
                c=[color], s=20, marker='o', alpha=0.5, label=f'Border {label}')

plt.title(f'DBSCAN: {n_clusters} clusters, {n_noise} noise points')
plt.legend()
plt.show()
```

---

## Gaussian Mixture Model (EM)

### 🔧 Code

- 🔧 **GMM / EM pipeline:**

```python
from sklearn.mixture import GaussianMixture

# GMM (EM algorithm) — specify n_components (= K)
# 高斯混合模型（EM算法）— 指定分量数（= K）
gmm = GaussianMixture(n_components=3, random_state=42)
gmm.fit(X)

# Hard assignment (like K-Means)
# 硬分配（类似K-Means）
labels = gmm.predict(X)

# Soft assignment — probability of each point belonging to each cluster
# 软分配 — 每个点属于每个簇的概率
probs = gmm.predict_proba(X)  # Shape: (n_samples, n_components)
# probs[i] = [P(cluster_0|x_i), P(cluster_1|x_i), P(cluster_2|x_i)]
```

- 🔧 **Access learned GMM parameters:**

```python
gmm.means_           # μ per component: shape (K, d)     — 每个分量的均值
gmm.covariances_     # σ² per component: shape depends on cov_type — 每个分量的协方差
gmm.weights_         # P(k) mixing weights: shape (K,)   — 混合权重（先验概率）
```

- 🔧 **BIC/AIC for choosing K:**

```python
# BIC (Bayesian Information Criterion) — lower = better model
# AIC (Akaike Information Criterion) — lower = better model
# 用BIC/AIC选择最佳K
bic_scores = []
for k in range(1, 11):
    gmm = GaussianMixture(n_components=k, random_state=42)
    gmm.fit(X)
    bic_scores.append(gmm.bic(X))

plt.plot(range(1, 11), bic_scores, 'bo-')
plt.xlabel('Number of components K')
plt.ylabel('BIC Score')
plt.title('BIC for GMM')
plt.show()
```

---

## Silhouette Analysis

### 🔧 Code

- 🔧 **Silhouette score computation:**

```python
from sklearn.metrics import silhouette_score, silhouette_samples

# Overall silhouette score (average across all points)
# 整体轮廓系数（所有点的平均值）
score = silhouette_score(X, labels)  # Range: [-1, 1], higher = better

# Per-point silhouette values
# 每个点的轮廓系数
sample_scores = silhouette_samples(X, labels)  # Array of s_i for each point
```

- 🔧 **Silhouette method for choosing K:**

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Try K=2..10, pick K with highest silhouette score
# 尝试K=2..10，选轮廓系数最高的K
sil_scores = []
K_range = range(2, 11)  # ⚠️ Start from 2 (silhouette undefined for K=1)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    sil_scores.append(silhouette_score(X, labels))

best_k = K_range[np.argmax(sil_scores)]  # K with highest silhouette
```

---

## Common Data Generation for Testing

### 🔧 Code

- 🔧 **Generate synthetic clustering data:**

```python
from sklearn.datasets import make_blobs, make_moons, make_circles

# Spherical clusters (good for K-Means)
# 球形簇（适合K-Means）
X_blobs, y_blobs = make_blobs(n_samples=300, centers=3, random_state=42)

# Crescent/moon shapes (good for DBSCAN, bad for K-Means)
# 月牙形（适合DBSCAN，K-Means会失败）
X_moons, y_moons = make_moons(n_samples=300, noise=0.05, random_state=42)

# Concentric circles (good for DBSCAN, bad for K-Means)
# 同心圆（适合DBSCAN，K-Means会失败）
X_circles, y_circles = make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)
```

---

## Distance/Proximity Matrix

### 🔧 Code

- 🔧 **Compute pairwise distance matrix:**

```python
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import pdist, squareform

# Full N×N distance matrix (for hierarchical clustering)
# 完整的N×N距离矩阵（用于层次聚类）
dist_matrix = pairwise_distances(X, metric='euclidean')

# Condensed form (upper triangle, for scipy linkage)
# 压缩形式（上三角，用于scipy linkage函数）
dist_condensed = pdist(X, metric='euclidean')
dist_full = squareform(dist_condensed)  # Convert back to square
```
