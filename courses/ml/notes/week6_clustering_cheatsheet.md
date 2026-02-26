# Week 6: Clustering — 概念速查

> **Source:** slides `Week6Clustering.pdf` + storyline
> **Scope:** K-Means, Hierarchical Clustering, DBSCAN, EM/GMM, Cluster Validity (SSE, SSB, Silhouette)
> **See also:** [week6_clustering_math.md](week6_clustering_math.md) (公式+手算) | [week6_clustering_code.md](week6_clustering_code.md) (代码)

---

## Cluster Analysis Overview

### 📖 Definition

- **Cluster Analysis (聚类分析):** unsupervised learning that groups objects so objects in the same group are similar and objects in different groups are dissimilar
- **Unsupervised Learning (无监督学习):** learning from data without labels — no "teacher" tells you the correct groups
- **Intra-cluster Distance (簇内距离):** distance between points within the same cluster — want to MINIMIZE
- **Inter-cluster Distance (簇间距离):** distance between points in different clusters — want to MAXIMIZE
- **Partitional Clustering (划分聚类):** divides data into non-overlapping subsets (flat, no hierarchy)
- **Hierarchical Clustering (层次聚类):** creates nested clusters organized as a tree (dendrogram)

### 💡 Key Points

- 💡 Clustering = finding hidden structure in unlabeled data
- 💡 Core goal: minimize intra-cluster distance AND maximize inter-cluster distance
- 💡 Same data can have 2, 4, or 6 clusters — the "right" number is ambiguous
- 💡 Applications: document grouping, gene/protein analysis, stock price patterns, data summarization

### ⚠️ Traps

- ⚠️ Clustering is UNSUPERVISED (no labels) — NOT the same as classification (supervised, has labels)
- ⚠️ Number of clusters is inherently ambiguous — there is no single "correct" answer

---

## Types of Clusters

### 📖 Definition

- **Well-separated Cluster (分离良好的簇):** every point is closer to its own cluster than to any other cluster
- **Prototype-based Cluster (基于原型的簇):** each point is closer to the centroid (mean/medoid) of its cluster than to any other centroid — K-Means uses this
- **Contiguity-based Cluster (基于邻接的簇):** each point is closer to at least one point in its own cluster than to any point outside — also called nearest-neighbor clustering
- **Density-based Cluster (基于密度的簇):** dense regions of points separated by low-density regions — DBSCAN uses this
- **Centroid (质心):** the center point of a cluster, typically the mean of all points in the cluster
- **Medoid (中心点):** the actual data point closest to the center of a cluster (unlike centroid, medoid is a real data point)

### 💡 Key Points

- 💡 Different cluster definitions → different algorithms → different results on the same data
- 💡 K-Means = prototype-based, DBSCAN = density-based, Hierarchical with MIN = contiguity-based

### ⚠️ Traps

- ⚠️ Centroid ≠ Medoid: centroid = computed mean (may not be a real point), medoid = actual data point

---

## K-Means Clustering

### 📖 Definition

- **K-Means (K均值聚类):** partitional clustering that assigns each point to the nearest centroid, then recomputes centroids iteratively until convergence
- **K (簇数):** the number of clusters — MUST be specified in advance by the user
- **Centroid (质心):** the mean of all points assigned to a cluster
- **Convergence (收敛):** centroids stop moving (or very few points change cluster assignment)
- **SSE (Sum of Squared Error, 误差平方和):** objective function that K-Means minimizes — sum of squared distances from each point to its cluster centroid
- **Local Minimum (局部最小值):** SSE has converged but may NOT be the global best — different random starts can give different results

### 💡 Key Points

- 💡 Algorithm: (1) choose K initial centroids (randomly) → (2) assign points to nearest centroid → (3) recompute centroids as mean → (4) repeat until convergence
- 💡 Complexity: O(n × K × I × d) — n=points, K=clusters, I=iterations, d=dimensions
- 💡 Most convergence happens in the first few iterations
- 💡 K-Means always converges for common distance measures
- 💡 K-Means is extremely fast and simple — 5 lines in sklearn

### ⚠️ Traps

- ⚠️ K MUST be specified in advance — wrong K → entire clustering is wrong
- ⚠️ K-Means ALWAYS converges ≠ ALWAYS finds optimal solution — only guarantees LOCAL minimum of SSE
- ⚠️ K-Means can ONLY find spherical (ball-shaped) clusters — crescent/ring shapes → disaster
- ⚠️ K-Means has NO noise concept — every point MUST belong to some cluster, outliers distort centroids
- ⚠️ Random initialization → different runs can produce different results
- ⚠️ SSE ALWAYS decreases as K increases — cannot simply pick K with lowest SSE (K=N gives SSE=0)

---

## Hierarchical Clustering

### 📖 Definition

- **Hierarchical Clustering (层次聚类):** produces nested clusters organized as a tree — no need to specify K in advance
- **Dendrogram (树状图):** tree diagram that records the sequence of merges (or splits) — y-axis = merge distance
- **Agglomerative (凝聚式/自底向上):** start with each point as its own cluster → merge closest pair → repeat until one cluster remains
- **Divisive (分裂式/自顶向下):** start with one big cluster → split → repeat until each point is its own cluster
- **Linkage Method (链接方法):** defines how to compute distance between two clusters — determines merge behavior
- **Single Linkage / MIN (单链接):** distance = minimum distance between any pair of points across two clusters — nearest neighbor
- **Complete Linkage / MAX (完全链接):** distance = maximum distance between any pair of points across two clusters — farthest neighbor
- **Group Average (组平均):** distance = average of all pairwise distances between points in two clusters
- **Ward's Method (Ward方法):** distance = increase in total SSE after merging — minimum variance method
- **Proximity Matrix / Distance Matrix (距离矩阵):** N×N matrix storing pairwise distances between all points/clusters

### 💡 Key Points

- 💡 Algorithm: compute distance matrix → each point = one cluster → repeat: merge closest pair, update matrix → until one cluster
- 💡 Key advantage: no need to specify K — cut dendrogram at any height to get desired K
- 💡 Corresponds to meaningful taxonomies (e.g., biological classification)
- 💡 MIN → chain-like, elongated clusters; MAX → compact, spherical clusters; Average → compromise
- 💡 After merge, new cluster's distances marked "?" must be recomputed using chosen linkage method

### ⚠️ Traps

- ⚠️ O(n³) time + O(n²) space — NOT suitable for large datasets (100K points → 10 billion distance entries)
- ⚠️ Merges are IRREVERSIBLE — early wrong merge propagates errors to all subsequent levels
- ⚠️ MIN linkage is vulnerable to "chaining effect" — a single noise point can bridge two separate clusters
- ⚠️ Still assigns EVERY point to a cluster — no noise handling
- ⚠️ MAX and Ward still prefer spherical clusters

### 📊 Compare

| Feature           | MIN (Single)          | MAX (Complete)     | Group Average     | Ward             |
| ----------------- | --------------------- | ------------------ | ----------------- | ---------------- |
| Distance used     | Nearest pair          | Farthest pair      | All-pairs average | SSE increase     |
| Cluster shape     | Chain-like, elongated | Compact, spherical | Compromise        | Compact, min var |
| Noise sensitivity | HIGH (chaining)       | Low                | Medium            | Low              |
| Cluster size      | Uneven                | Balanced           | Medium            | Balanced         |

---

## DBSCAN

### 📖 Definition

- **DBSCAN (Density-Based Spatial Clustering of Applications with Noise, 基于密度的带噪声空间聚类):** density-based algorithm that finds clusters as regions of high density separated by regions of low density
- **ε (Epsilon, 半径):** radius parameter — defines the neighborhood around each point
- **MinPts (最小点数):** minimum number of points required within ε radius for a point to be a core point
- **Core Point (核心点):** a point with at least MinPts points within ε radius (**including itself**) — interior of cluster
- **Border Point (边界点):** NOT a core point, but within ε distance of at least one core point — edge of cluster
- **Noise Point (噪声点):** neither core nor border — outlier, excluded from all clusters
- **Density (密度):** number of points within ε radius of a point

### 💡 Key Points

- 💡 Algorithm: (1) label all points as core/border/noise → (2) eliminate noise → (3) connect core points within ε → (4) connected core points = one cluster → (5) assign border points to nearest core's cluster
- 💡 Does NOT require specifying K — number of clusters discovered automatically
- 💡 Can handle clusters of ANY shape (crescents, rings, letters)
- 💡 Built-in noise detection — outliers automatically excluded
- 💡 Single-pass algorithm — NOT iterative like K-Means
- 💡 Core/noise classification is deterministic; border point assignment may depend on processing order

### ⚠️ Traps

- ⚠️ **Core point counts ITSELF!** MinPts=4 means point + 3 neighbors = 4 → IS a core point
- ⚠️ Border point assignment is NON-DETERMINISTIC — depends on processing order
- ⚠️ Global single ε → fails when clusters have varying density (dense cluster + sparse cluster can't use same ε)
- ⚠️ High-dimensional data: ε distance becomes meaningless due to curse of dimensionality
- ⚠️ Sensitive to ε and MinPts choice: wrong parameters → everything is noise OR everything is one cluster

### 📊 Compare

| Feature        | K-Means           | DBSCAN                    |
| -------------- | ----------------- | ------------------------- |
| Specify K      | YES — required    | NO — auto-discovered      |
| Cluster shape  | Spherical only    | ANY shape                 |
| Noise handling | None              | Built-in (separate class) |
| Parameters     | K                 | ε, MinPts                 |
| Iterative      | YES — multi-round | NO — single pass          |
| Determinism    | NO — random init  | Core/noise: YES           |
| Assignment     | Hard (0 or 1)     | Hard (0 or 1)             |

---

## EM / Gaussian Mixture Model (GMM)

### 📖 Definition

- **EM (Expectation-Maximization, 期望最大化):** iterative algorithm that alternates between estimating cluster membership (E-step) and updating distribution parameters (M-step)
- **GMM (Gaussian Mixture Model, 高斯混合模型):** models data as arising from a mixture of multiple Gaussian distributions
- **Soft Assignment / Probabilistic Assignment (软分配/概率分配):** each point has a PROBABILITY of belonging to each cluster — NOT hard 0/1
- **Hard Assignment (硬分配):** each point belongs to exactly one cluster — K-Means style
- **Mixing Weight (混合权重):** P(b) — prior probability that a point comes from cluster b
- **E-step (Expectation步):** compute posterior probability P(cluster|point) for each point using Bayes' rule — "how much does each point belong to each cluster?"
- **M-step (Maximization步):** re-estimate parameters (μ, σ², mixing weight) using weighted statistics
- **Gaussian PDF (高斯概率密度函数):** bell curve defined by μ (mean) and σ (standard deviation)
- **Chicken-and-Egg Problem (鸡与蛋问题):** if we knew labels → easy to estimate params; if we knew params → easy to assign labels; EM alternates between the two

### 💡 Key Points

- 💡 EM is the generalization of K-Means: K-Means is EM with equal fixed variances and hard 0/1 assignments
- 💡 EM produces probability memberships (e.g., 80% cluster A, 20% cluster B)
- 💡 EM can fit elliptical clusters with different sizes (K-Means only fits equal spheres)
- 💡 Each Gaussian component is described by 3 parameters: μ (mean), σ² (variance), P(b) (weight)
- 💡 EM iterates E→M→E→M until convergence (parameters stabilize)

### ⚠️ Traps

- ⚠️ K-Means is a SPECIAL CASE of EM — when variances are equal+fixed and memberships are forced to 0/1
- ⚠️ EM still requires specifying K (number of Gaussian components) — same problem as K-Means
- ⚠️ EM assumes Gaussian distribution — non-Gaussian shaped clusters → poor fit
- ⚠️ EM can also get stuck in local optima (same as K-Means)

### 📊 Compare

| Feature       | K-Means            | EM (GMM)                      |
| ------------- | ------------------ | ----------------------------- |
| Assignment    | Hard (0 or 1)      | Soft (probability)            |
| Cluster model | Centroid only      | Full Gaussian (μ, σ², weight) |
| Cluster shape | Spherical, equal   | Elliptical, different sizes   |
| Relationship  | Special case of EM | Generalization of K-Means     |
| K required    | YES                | YES                           |

---

## Cluster Validity

### 📖 Definition

- **Cluster Validity (聚类有效性):** numerical measures to judge the quality of clustering results
- **External Index / Supervised Measure (外部指标):** compares cluster labels against externally supplied true class labels
- **Internal Index / Unsupervised Measure (内部指标):** evaluates clustering quality using only the data itself (no true labels)
- **Cohesion (凝聚度):** how closely related objects are within a cluster — lower SSE = higher cohesion
- **Separation (分离度):** how distinct a cluster is from other clusters — higher SSB = better separation
- **SSE / SSW (Sum of Squared Error / Within-Cluster Sum of Squares, 簇内平方和):** sum of squared distances from each point to its cluster centroid — measures cluster tightness
- **SSB (Between-Cluster Sum of Squares, 簇间平方和):** sum of weighted squared distances from each centroid to the global mean — measures cluster spread
- **TSS (Total Sum of Squares, 总平方和):** total squared distance of all points from the global mean — SSE + SSB = TSS (constant)
- **Silhouette Coefficient (轮廓系数):** per-point measure combining cohesion and separation — range [-1, 1]
- **a (within-cluster avg distance):** average distance from point i to all other points in its own cluster
- **b (nearest-cluster avg distance):** minimum average distance from point i to all points in any OTHER cluster
- **Grand Mean / Global Mean (全局均值):** mean of all data points across all clusters

### 💡 Key Points

- 💡 SSE + SSB = TSS (constant) — if SSE decreases, SSB increases by the same amount
- 💡 More clusters → lower SSE, higher SSB — but K=N gives SSE=0 (trivially useless)
- 💡 Silhouette s = (b − a) / max(a, b): closer to 1 = perfect, near 0 = boundary, near -1 = misclassified
- 💡 Use silhouette coefficient to select best K: try K=2,3,4,... and pick highest average silhouette
- 💡 Graph-based cohesion = sum of intra-cluster edge weights; graph-based separation = sum of inter-cluster edge weights

### ⚠️ Traps

- ⚠️ SSE ALWAYS decreases with more clusters — cannot just minimize SSE to pick K
- ⚠️ Silhouette coefficient prefers CONVEX cluster shapes — non-convex clusters may score low even when correctly clustered
- ⚠️ a = average distance to points in OWN cluster (not to centroid), b = minimum of averages to OTHER clusters (not just nearest point)

### 📊 Compare

| Measure       | What it measures   | Good value | Limitation                   |
| ------------- | ------------------ | ---------- | ---------------------------- |
| SSE (within)  | Cluster tightness  | Low        | Always decreases with more K |
| SSB (between) | Cluster separation | High       | Always increases with more K |
| Silhouette    | Per-point fit      | Close to 1 | Biased toward convex shapes  |

---

## Four Algorithms — Master Comparison

### 📊 Compare

| Feature         | K-Means         | Hierarchical        | DBSCAN                | EM/GMM                  |
| --------------- | --------------- | ------------------- | --------------------- | ----------------------- |
| Category        | Partition-based | Hierarchy-based     | Density-based         | Distribution-based      |
| Specify K       | YES             | NO (cut dendrogram) | NO (auto-discovered)  | YES                     |
| Cluster shape   | Spherical       | Depends on linkage  | ANY shape             | Elliptical              |
| Noise handling  | None            | None                | Built-in              | None                    |
| Assignment type | Hard            | Hard                | Hard                  | Soft (probability)      |
| Time complexity | O(nKId) — fast  | O(n³) — very slow   | O(n²) or O(n log n)   | O(nKId) — similar to KM |
| Space           | O(n)            | O(n²)               | O(n)                  | O(n)                    |
| Iterative       | Yes             | No (single pass)    | No (single pass)      | Yes                     |
| Deterministic   | No              | Yes                 | Core/noise: Yes       | No                      |
| Key weakness    | Must guess K    | Too slow for big N  | Varying density fails | Assumes Gaussian        |
