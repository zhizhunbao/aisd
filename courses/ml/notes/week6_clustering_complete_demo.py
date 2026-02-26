"""
Week 6: Clustering — Complete Demo
Demonstrates K-Means, Hierarchical/Agglomerative, DBSCAN, EM/GMM clustering,
and cluster validity measures (SSE, SSB, Silhouette) from lecture slides.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import norm
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'week6_clustering_complete_demo_pages')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 图表全局设置
# Global plot settings
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})


# ============================================================
# 步骤 1：K-Means 基本算法 — 手动实现
# Step 1: K-Means Basic Algorithm — Manual Implementation
# ============================================================

print("=" * 60)
print("Step 1: K-Means Algorithm — Manual Implementation")
print("=" * 60)

# 生成简单的2D数据（3个球形簇）
# Generate simple 2D data (3 spherical clusters)
from sklearn.datasets import make_blobs
X_blobs, y_true = make_blobs(n_samples=300, centers=3, cluster_std=0.8,
                              random_state=RANDOM_STATE)


def kmeans_manual(X, K, max_iter=20, random_state=42):
    """
    手动实现K-Means
    Manual K-Means implementation

    参数 / Parameters:
        X: 数据矩阵 (n, d) / Data matrix
        K: 簇数 / Number of clusters
        max_iter: 最大迭代次数 / Max iterations
    返回 / Returns:
        centroids: 最终质心 / Final centroids
        labels: 每个点的簇标签 / Cluster labels for each point
        history: 迭代历史 / Iteration history
    """
    rng = np.random.RandomState(random_state)
    n, d = X.shape

    # 步骤 1：随机选择 K 个初始质心
    # Step 1: Randomly choose K initial centroids
    indices = rng.choice(n, K, replace=False)
    centroids = X[indices].copy()

    history = [centroids.copy()]
    labels = np.zeros(n, dtype=int)

    for iteration in range(max_iter):
        # 步骤 2：分配——每个点到最近质心
        # Step 2: Assign — each point to nearest centroid
        # 距离矩阵: (n, K) — 每行是一个点到K个质心的距离
        # Distance matrix: (n, K) — each row = distances from one point to K centroids
        distances = np.sqrt(((X[:, np.newaxis] - centroids[np.newaxis, :]) ** 2).sum(axis=2))
        new_labels = distances.argmin(axis=1)

        # 步骤 3：更新——质心移到簇的平均位置
        # Step 3: Update — centroid moves to mean of assigned points
        new_centroids = np.array([X[new_labels == k].mean(axis=0) for k in range(K)])

        # 检查收敛（质心不再移动）
        # Check convergence (centroids stop moving)
        if np.allclose(centroids, new_centroids):
            print(f"  Converged at iteration {iteration + 1}")
            centroids = new_centroids
            labels = new_labels
            history.append(centroids.copy())
            break

        centroids = new_centroids
        labels = new_labels
        history.append(centroids.copy())

    return centroids, labels, history


centroids, labels, history = kmeans_manual(X_blobs, K=3)

# 计算 SSE
# Compute SSE
# SSE = Σᵢ Σ_{x∈Cᵢ} ‖x - mᵢ‖²
# For each cluster, sum squared distances from points to centroid
sse = sum(np.sum((X_blobs[labels == k] - centroids[k]) ** 2) for k in range(3))
print(f"\nFinal SSE = {sse:.2f}")
print(f"Number of iterations: {len(history) - 1}")

# 可视化：K-Means 迭代过程
# Visualization: K-Means iteration process
n_show = min(4, len(history))
fig, axes = plt.subplots(1, n_show, figsize=(5 * n_show, 5))

for idx, ax in enumerate(axes):
    # 分配颜色基于当前质心
    # Color assignment based on current centroids
    if idx == 0:
        # 初始状态：用最终标签着色但标记初始质心
        # Initial state: color by final labels but mark initial centroids
        ax.scatter(X_blobs[:, 0], X_blobs[:, 1], c='gray', s=20, alpha=0.5)
        c = history[idx]
        ax.scatter(c[:, 0], c[:, 1], c='red', marker='X', s=200,
                   edgecolors='black', linewidths=2, zorder=5)
        ax.set_title(f'Iteration 0\n(Random centroids)')
    else:
        step_idx = min(idx, len(history) - 1)
        c = history[step_idx]
        # 用当前质心分配标签
        # Assign labels using current centroids
        dists = np.sqrt(((X_blobs[:, np.newaxis] - c[np.newaxis, :]) ** 2).sum(axis=2))
        step_labels = dists.argmin(axis=1)
        ax.scatter(X_blobs[:, 0], X_blobs[:, 1], c=step_labels,
                   cmap='viridis', s=20, alpha=0.7)
        ax.scatter(c[:, 0], c[:, 1], c='red', marker='X', s=200,
                   edgecolors='black', linewidths=2, zorder=5)
        if step_idx == len(history) - 1:
            ax.set_title(f'Final (iter {step_idx})\nSSE = {sse:.1f}')
        else:
            ax.set_title(f'Iteration {step_idx}')
    ax.set_xlabel('X₁')
    ax.set_ylabel('X₂')

plt.suptitle("K-Means: Centroids Converge to Cluster Centers",
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step1_kmeans_iterations.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 2：K-Means 的缺陷 — 非球形数据
# Step 2: K-Means Limitations — Non-Spherical Data
# ============================================================

print("\n" + "=" * 60)
print("Step 2: K-Means Limitations — Non-Spherical Data")
print("=" * 60)

from sklearn.datasets import make_moons, make_circles
from sklearn.cluster import KMeans

# 生成月牙形和同心圆数据
# Generate crescent and concentric circles data
X_moons, y_moons = make_moons(n_samples=300, noise=0.05, random_state=RANDOM_STATE)
X_circles, y_circles = make_circles(n_samples=300, noise=0.05, factor=0.5,
                                     random_state=RANDOM_STATE)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 上排：K-Means 在月牙形数据上（失败）
# Top row: K-Means on crescent data (fails)
km_moons = KMeans(n_clusters=2, random_state=RANDOM_STATE, n_init=10)
labels_moons = km_moons.fit_predict(X_moons)

axes[0, 0].scatter(X_moons[:, 0], X_moons[:, 1], c=y_moons, cmap='Set1', s=30, alpha=0.7)
axes[0, 0].set_title('Moon Data: True Labels')

axes[0, 1].scatter(X_moons[:, 0], X_moons[:, 1], c=labels_moons, cmap='Set1', s=30, alpha=0.7)
axes[0, 1].scatter(km_moons.cluster_centers_[:, 0], km_moons.cluster_centers_[:, 1],
                   c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[0, 1].set_title('K-Means K=2: ❌ FAILS!\n(Can only find spherical clusters)')

# 下排：K-Means 在同心圆数据上（失败）
# Bottom row: K-Means on concentric circles (fails)
km_circles = KMeans(n_clusters=2, random_state=RANDOM_STATE, n_init=10)
labels_circles = km_circles.fit_predict(X_circles)

axes[1, 0].scatter(X_circles[:, 0], X_circles[:, 1], c=y_circles, cmap='Set1', s=30, alpha=0.7)
axes[1, 0].set_title('Circle Data: True Labels')

axes[1, 1].scatter(X_circles[:, 0], X_circles[:, 1], c=labels_circles, cmap='Set1', s=30, alpha=0.7)
axes[1, 1].scatter(km_circles.cluster_centers_[:, 0], km_circles.cluster_centers_[:, 1],
                   c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[1, 1].set_title('K-Means K=2: ❌ FAILS!\n(Spherical assumption violated)')

for ax in axes.flat:
    ax.set_xlabel('X₁')
    ax.set_ylabel('X₂')

plt.suptitle("K-Means ONLY Works on Spherical Clusters\n"
             "Crescent/Ring shapes → complete failure",
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step2_kmeans_limitations.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("K-Means fails on non-spherical data:")
print("  • Moon-shaped clusters → wrong boundary")
print("  • Concentric circles → splits each circle in half")


# ============================================================
# 步骤 3：SSE 肘部法 — 选择最优 K
# Step 3: SSE Elbow Method — Choosing Optimal K
# ============================================================

print("\n" + "=" * 60)
print("Step 3: Elbow Method for Choosing K")
print("=" * 60)

# 对球形数据尝试 K=1..10
# Try K=1..10 on spherical data
K_range = range(1, 11)
sse_list = []
for k in K_range:
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    km.fit(X_blobs)
    sse_list.append(km.inertia_)
    print(f"  K={k}: SSE = {km.inertia_:.2f}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(K_range, sse_list, 'bo-', linewidth=2, markersize=8)
ax.axvline(x=3, color='red', linestyle='--', alpha=0.7, label='Elbow at K=3')
ax.annotate('Elbow ← best K', xy=(3, sse_list[2]),
            xytext=(5, sse_list[2] + 200), fontsize=12,
            arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax.set_xlabel('Number of Clusters K')
ax.set_ylabel('SSE (Inertia)')
ax.set_title('Elbow Method: SSE Always Decreases with K\n'
             '⚠️ Cannot just pick min SSE — look for the "elbow" bend')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step3_elbow_method.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print(f"\n⚠️ SSE ALWAYS decreases → K=N gives SSE=0 (trivially useless)")
print(f"  Look for the 'elbow' where adding more K gives diminishing returns")


# ============================================================
# 步骤 4：层次聚类 — 树状图 + 不同链接方法
# Step 4: Hierarchical Clustering — Dendrogram + Linkage Methods
# ============================================================

print("\n" + "=" * 60)
print("Step 4: Hierarchical Clustering — Linkage Methods")
print("=" * 60)

# 用小数据集演示（6个点，与slides一致）
# Use small dataset (6 points, matching slides)
X_small = np.array([[1.0, 1.0], [1.5, 1.8], [5.0, 8.0],
                     [8.0, 8.0], [1.0, 0.6], [9.0, 11.0]])

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

linkage_methods = ['single', 'complete', 'average', 'ward']
linkage_labels = ['MIN (Single Linkage)\n→ Chain-like clusters',
                  'MAX (Complete Linkage)\n→ Compact, spherical clusters',
                  'Group Average\n→ Compromise',
                  'Ward (Min Variance)\n→ Compact, balanced clusters']

for idx, (method, label) in enumerate(zip(linkage_methods, linkage_labels)):
    ax = axes[idx // 2][idx % 2]

    # 计算链接矩阵
    # Compute linkage matrix
    Z = linkage(X_small, method=method)

    # 画树状图
    # Plot dendrogram
    dendrogram(Z, ax=ax, labels=[f'P{i+1}' for i in range(len(X_small))],
               leaf_font_size=11)
    ax.set_title(label, fontsize=12, fontweight='bold')
    ax.set_ylabel('Distance')

    print(f"\n{method.upper()} linkage:")
    print(f"  Merge order: {Z[:, :2].astype(int).tolist()}")
    print(f"  Merge distances: {Z[:, 2].round(2).tolist()}")

plt.suptitle("Hierarchical Clustering: Same Data, Different Linkage → Different Trees\n"
             "Choose linkage based on expected cluster shape",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step4_dendrograms.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 5：DBSCAN — 核心/边界/噪声分类
# Step 5: DBSCAN — Core/Border/Noise Classification
# ============================================================

print("\n" + "=" * 60)
print("Step 5: DBSCAN — Core/Border/Noise Point Classification")
print("=" * 60)

from sklearn.cluster import DBSCAN

# DBSCAN 在月牙形数据上（K-Means失败的数据）
# DBSCAN on crescent data (where K-Means failed)
db = DBSCAN(eps=0.3, min_samples=5)
db_labels = db.fit_predict(X_moons)

# 识别核心、边界、噪声
# Identify core, border, noise
core_mask = np.zeros_like(db_labels, dtype=bool)
core_mask[db.core_sample_indices_] = True
border_mask = ~core_mask & (db_labels != -1)
noise_mask = (db_labels == -1)

n_clusters = len(set(db_labels)) - (1 if -1 in db_labels else 0)
n_noise = noise_mask.sum()

print(f"\nDBSCAN on Moon data (eps=0.3, min_samples=5):")
print(f"  Clusters found: {n_clusters}")
print(f"  Core points: {core_mask.sum()}")
print(f"  Border points: {border_mask.sum()}")
print(f"  Noise points: {n_noise}")

# 可视化：DBSCAN 结果 vs K-Means
# Visualization: DBSCAN results vs K-Means
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 真实标签
# True labels
axes[0].scatter(X_moons[:, 0], X_moons[:, 1], c=y_moons, cmap='Set1', s=30, alpha=0.7)
axes[0].set_title('True Labels')

# K-Means（失败）
# K-Means (fails)
axes[1].scatter(X_moons[:, 0], X_moons[:, 1], c=labels_moons, cmap='Set1', s=30, alpha=0.7)
axes[1].scatter(km_moons.cluster_centers_[:, 0], km_moons.cluster_centers_[:, 1],
                c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[1].set_title('K-Means K=2: ❌ Wrong!')

# DBSCAN（成功！）
# DBSCAN (succeeds!)
# 核心点用大点，边界小点，噪声用×
# Core = large dots, border = small dots, noise = ×
axes[2].scatter(X_moons[core_mask, 0], X_moons[core_mask, 1],
                c=db_labels[core_mask], cmap='Set1', s=50, alpha=0.8, label='Core')
axes[2].scatter(X_moons[border_mask, 0], X_moons[border_mask, 1],
                c=db_labels[border_mask], cmap='Set1', s=20, alpha=0.5,
                edgecolors='black', linewidths=0.5, label='Border')
if noise_mask.any():
    axes[2].scatter(X_moons[noise_mask, 0], X_moons[noise_mask, 1],
                    c='black', marker='x', s=50, label='Noise')
axes[2].set_title(f'DBSCAN: ✅ Correct!\n({n_clusters} clusters, {n_noise} noise)')
axes[2].legend(fontsize=9)

for ax in axes:
    ax.set_xlabel('X₁')
    ax.set_ylabel('X₂')

plt.suptitle("DBSCAN Handles Non-Spherical Clusters + Noise\n"
             "K-Means fails on moon-shaped data, DBSCAN succeeds!",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step5_dbscan_vs_kmeans.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 6：DBSCAN 核心/边界/噪声 — 详细可视化
# Step 6: DBSCAN Core/Border/Noise — Detailed Visualization
# ============================================================

print("\n" + "=" * 60)
print("Step 6: DBSCAN Point Classification — Detailed View")
print("=" * 60)

# 小数据集手动演示 DBSCAN
# Small dataset for manual DBSCAN demo
X_dbscan_demo = np.array([
    [1, 2], [1.5, 1.8], [1.2, 2.3], [1.8, 2.1], [1.3, 1.5],  # 簇1核心区域
    [0.5, 2.8],   # 簇1边界点
    [5, 5], [5.2, 5.3], [4.8, 5.1], [5.5, 4.8], [5.1, 5.5],  # 簇2核心区域
    [4.2, 4.5],   # 簇2边界点
    [8, 1],       # 噪声点
])

db_demo = DBSCAN(eps=1.0, min_samples=4)
demo_labels = db_demo.fit_predict(X_dbscan_demo)

core_demo = np.zeros(len(X_dbscan_demo), dtype=bool)
core_demo[db_demo.core_sample_indices_] = True
border_demo = ~core_demo & (demo_labels != -1)
noise_demo = demo_labels == -1

print(f"\nDBSCAN demo (eps=1.0, MinPts=4):")
print(f"  ⚠️ MinPts includes the point itself!")
for i, (x, label) in enumerate(zip(X_dbscan_demo, demo_labels)):
    ptype = 'Core' if core_demo[i] else ('Border' if border_demo[i] else 'Noise')
    print(f"  Point {i} {x}: cluster={label}, type={ptype}")

fig, ax = plt.subplots(figsize=(10, 8))

# 画 ε 邻域圆
# Draw ε neighborhood circles
for i in range(len(X_dbscan_demo)):
    if core_demo[i]:
        circle = plt.Circle(X_dbscan_demo[i], 1.0, fill=False,
                            color='green', linestyle='--', alpha=0.3)
        ax.add_patch(circle)

# 核心点（大绿色）
# Core points (large green)
ax.scatter(X_dbscan_demo[core_demo, 0], X_dbscan_demo[core_demo, 1],
           c='green', s=150, marker='o', edgecolors='darkgreen', linewidths=2,
           label='Core (≥MinPts in ε)', zorder=5)

# 边界点（蓝色三角）
# Border points (blue triangles)
ax.scatter(X_dbscan_demo[border_demo, 0], X_dbscan_demo[border_demo, 1],
           c='blue', s=120, marker='^', edgecolors='darkblue', linewidths=2,
           label='Border (in core\'s ε)', zorder=5)

# 噪声点（红色×）
# Noise points (red X)
ax.scatter(X_dbscan_demo[noise_demo, 0], X_dbscan_demo[noise_demo, 1],
           c='red', s=120, marker='X', edgecolors='darkred', linewidths=2,
           label='Noise (isolated)', zorder=5)

# 标注每个点
# Label each point
for i, (x, y) in enumerate(X_dbscan_demo):
    ptype = 'C' if core_demo[i] else ('B' if border_demo[i] else 'N')
    ax.annotate(f'P{i}({ptype})', (x, y), textcoords="offset points",
                xytext=(10, 5), fontsize=9)

ax.set_xlabel('X₁')
ax.set_ylabel('X₂')
ax.set_title('DBSCAN Point Classification (eps=1.0, MinPts=4)\n'
             '⚠️ MinPts counts the point ITSELF!\n'
             'Green circles = ε neighborhoods of core points')
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step6_dbscan_point_types.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 7：EM / GMM — 软分配 vs K-Means 硬分配
# Step 7: EM / GMM — Soft Assignment vs K-Means Hard Assignment
# ============================================================

print("\n" + "=" * 60)
print("Step 7: EM (GMM) — Soft vs Hard Assignment")
print("=" * 60)

from sklearn.mixture import GaussianMixture

# 在球形数据上比较 K-Means 和 GMM
# Compare K-Means and GMM on spherical data
gmm = GaussianMixture(n_components=3, random_state=RANDOM_STATE)
gmm.fit(X_blobs)

gmm_labels = gmm.predict(X_blobs)
gmm_probs = gmm.predict_proba(X_blobs)

print(f"\nGMM Parameters (3 components):")
for k in range(3):
    print(f"\n  Component {k}:")
    print(f"    μ = {gmm.means_[k].round(2)}")
    print(f"    Weight P(k) = {gmm.weights_[k]:.4f}")

# 找到不确定的点（最大概率 < 0.9）
# Find uncertain points (max probability < 0.9)
max_probs = gmm_probs.max(axis=1)
uncertain_mask = max_probs < 0.9
n_uncertain = uncertain_mask.sum()
print(f"\nUncertain points (max_prob < 0.9): {n_uncertain}/{len(X_blobs)}")

# 可视化
# Visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# K-Means 硬分配
# K-Means hard assignment
km_blobs = KMeans(n_clusters=3, random_state=RANDOM_STATE, n_init=10)
km_labels_blobs = km_blobs.fit_predict(X_blobs)
axes[0].scatter(X_blobs[:, 0], X_blobs[:, 1], c=km_labels_blobs,
                cmap='viridis', s=30, alpha=0.7)
axes[0].scatter(km_blobs.cluster_centers_[:, 0], km_blobs.cluster_centers_[:, 1],
                c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[0].set_title('K-Means: Hard Assignment\n(Each point → exactly 1 cluster)')

# GMM 硬标签（与K-Means类似）
# GMM hard labels (similar to K-Means)
axes[1].scatter(X_blobs[:, 0], X_blobs[:, 1], c=gmm_labels,
                cmap='viridis', s=30, alpha=0.7)
axes[1].scatter(gmm.means_[:, 0], gmm.means_[:, 1],
                c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[1].set_title('GMM: Hard Assignment (predict)\n(Similar to K-Means)')

# GMM 软分配（颜色深浅表示确定性）
# GMM soft assignment (color intensity = certainty)
scatter = axes[2].scatter(X_blobs[:, 0], X_blobs[:, 1], c=max_probs,
                          cmap='RdYlGn', s=30, alpha=0.8,
                          vmin=0.3, vmax=1.0)
# 标记不确定的点
# Mark uncertain points
if uncertain_mask.any():
    axes[2].scatter(X_blobs[uncertain_mask, 0], X_blobs[uncertain_mask, 1],
                    facecolors='none', edgecolors='red', s=100, linewidths=2,
                    label=f'Uncertain ({n_uncertain} pts)')
    axes[2].legend(fontsize=10)
plt.colorbar(scatter, ax=axes[2], label='Max P(cluster|point)')
axes[2].set_title('GMM: Soft Assignment (predict_proba)\n'
                  'Red circles = uncertain (on cluster boundaries)')

for ax in axes:
    ax.set_xlabel('X₁')
    ax.set_ylabel('X₂')

plt.suptitle("K-Means is a Special Case of EM/GMM\n"
             "EM adds: probability memberships + different cluster sizes/shapes",
             fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step7_gmm_soft_assignment.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 8：EM 手动迭代 — 1D 示例
# Step 8: EM Manual Iteration — 1D Example
# ============================================================

print("\n" + "=" * 60)
print("Step 8: EM Algorithm — Manual 1D Iteration")
print("=" * 60)

# 1D 数据
# 1D data
X_1d = np.array([1.0, 2.0, 4.0, 5.0])

# 初始参数
# Initial parameters
mu_a, sigma_a = 1.5, 1.0
mu_b, sigma_b = 4.5, 1.0
pi_a, pi_b = 0.5, 0.5  # 混合权重 / mixing weights

print(f"\nData: {X_1d}")
print(f"Initial: μ_a={mu_a}, σ_a={sigma_a}, μ_b={mu_b}, σ_b={sigma_b}")
print(f"Weights: P(a)={pi_a}, P(b)={pi_b}")

em_history = {'mu_a': [mu_a], 'mu_b': [mu_b], 'sigma_a': [sigma_a], 'sigma_b': [sigma_b]}

for iteration in range(5):
    print(f"\n--- EM Iteration {iteration + 1} ---")

    # E步：计算后验概率 P(cluster | xᵢ)
    # E-step: Compute posterior P(cluster | xᵢ)
    # P(a|xᵢ) = P(xᵢ|a)P(a) / [P(xᵢ|a)P(a) + P(xᵢ|b)P(b)]
    p_x_given_a = norm.pdf(X_1d, mu_a, sigma_a)
    p_x_given_b = norm.pdf(X_1d, mu_b, sigma_b)

    # 后验概率（每个点属于 cluster a 的概率）
    # Posterior probability (prob each point belongs to cluster a)
    r_a = (p_x_given_a * pi_a) / (p_x_given_a * pi_a + p_x_given_b * pi_b)
    r_b = 1 - r_a

    print(f"  E-step posteriors P(a|x):")
    for i, x in enumerate(X_1d):
        print(f"    x={x}: P(a|x)={r_a[i]:.4f}, P(b|x)={r_b[i]:.4f}")

    # M步：用加权统计量更新参数
    # M-step: Update parameters with weighted statistics
    # μ_a = Σ(r_a × x) / Σr_a
    mu_a_new = np.sum(r_a * X_1d) / np.sum(r_a)
    mu_b_new = np.sum(r_b * X_1d) / np.sum(r_b)

    # σ²_a = Σ r_a (x - μ_a)² / Σr_a
    sigma_a_new = np.sqrt(np.sum(r_a * (X_1d - mu_a_new) ** 2) / np.sum(r_a))
    sigma_b_new = np.sqrt(np.sum(r_b * (X_1d - mu_b_new) ** 2) / np.sum(r_b))

    # 更新混合权重
    # Update mixing weights
    pi_a_new = np.sum(r_a) / len(X_1d)
    pi_b_new = np.sum(r_b) / len(X_1d)

    print(f"  M-step updates:")
    print(f"    μ_a: {mu_a:.4f} → {mu_a_new:.4f}")
    print(f"    μ_b: {mu_b:.4f} → {mu_b_new:.4f}")
    print(f"    σ_a: {sigma_a:.4f} → {sigma_a_new:.4f}")
    print(f"    σ_b: {sigma_b:.4f} → {sigma_b_new:.4f}")
    print(f"    P(a): {pi_a:.4f} → {pi_a_new:.4f}")

    mu_a, mu_b = mu_a_new, mu_b_new
    sigma_a, sigma_b = sigma_a_new, sigma_b_new
    pi_a, pi_b = pi_a_new, pi_b_new

    em_history['mu_a'].append(mu_a)
    em_history['mu_b'].append(mu_b)
    em_history['sigma_a'].append(sigma_a)
    em_history['sigma_b'].append(sigma_b)

# 可视化：EM 迭代过程
# Visualization: EM iteration process
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for idx in range(6):
    ax = axes[idx // 3][idx % 3]
    iter_idx = min(idx, len(em_history['mu_a']) - 1)

    m_a = em_history['mu_a'][iter_idx]
    m_b = em_history['mu_b'][iter_idx]
    s_a = em_history['sigma_a'][iter_idx]
    s_b = em_history['sigma_b'][iter_idx]

    x_range = np.linspace(-1, 7, 300)
    pdf_a = norm.pdf(x_range, m_a, s_a)
    pdf_b = norm.pdf(x_range, m_b, s_b)

    ax.plot(x_range, pdf_a, 'b-', linewidth=2, label=f'Cluster A (μ={m_a:.2f})')
    ax.plot(x_range, pdf_b, 'r-', linewidth=2, label=f'Cluster B (μ={m_b:.2f})')
    ax.fill_between(x_range, pdf_a, alpha=0.2, color='blue')
    ax.fill_between(x_range, pdf_b, alpha=0.2, color='red')

    # 画数据点
    # Plot data points
    ax.scatter(X_1d, np.zeros_like(X_1d), c='black', s=100, zorder=5, marker='|')
    for x in X_1d:
        ax.annotate(f'{x}', (x, 0.01), ha='center', fontsize=9)

    ax.set_title(f'Iteration {iter_idx}' if iter_idx < len(em_history['mu_a']) - 1
                 else f'Final (iter {iter_idx})')
    ax.legend(fontsize=8)
    ax.set_xlim(-1, 7)
    ax.set_ylim(-0.05, 0.7)

plt.suptitle("EM Algorithm: Two Gaussians Gradually Separate\n"
             "E-step: soft assign points to clusters | M-step: update μ, σ",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step8_em_iterations_1d.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 9：SSE + SSB = TSS — 恒等式验证
# Step 9: SSE + SSB = TSS — Identity Verification
# ============================================================

print("\n" + "=" * 60)
print("Step 9: SSE + SSB = TSS Identity")
print("=" * 60)

# 使用 slides 中的数据: {1, 2, 4, 5}
# Use data from slides: {1, 2, 4, 5}
data_1d = np.array([1, 2, 4, 5], dtype=float)
grand_mean = data_1d.mean()

print(f"\nData: {data_1d}")
print(f"Grand mean m = {grand_mean}")

# TSS = Σ(x - m)²
# TSS (Total Sum of Squares) = sum of squared distances from global mean
tss = np.sum((data_1d - grand_mean) ** 2)
print(f"TSS = Σ(x - m)² = {tss}")

results = []
for K in [1, 2, 4]:
    if K == 1:
        clusters = [data_1d]
        centroids_1d = [grand_mean]
    elif K == 2:
        clusters = [data_1d[:2], data_1d[2:]]
        centroids_1d = [c.mean() for c in clusters]
    else:
        clusters = [[x] for x in data_1d]
        centroids_1d = [x for x in data_1d]

    # SSE = Σᵢ Σ_{x∈Cᵢ} (x - mᵢ)²
    sse_val = sum(np.sum((np.array(c) - m) ** 2) for c, m in zip(clusters, centroids_1d))
    # SSB = Σᵢ |Cᵢ| (m - mᵢ)²
    ssb_val = sum(len(c) * (grand_mean - m) ** 2 for c, m in zip(clusters, centroids_1d))

    total = sse_val + ssb_val
    results.append((K, sse_val, ssb_val, total))

    print(f"\nK={K}:")
    print(f"  Centroids: {[round(m, 1) for m in centroids_1d]}")
    print(f"  SSE = {sse_val:.1f}")
    print(f"  SSB = {ssb_val:.1f}")
    print(f"  SSE + SSB = {total:.1f} {'✓' if abs(total - tss) < 0.01 else '✗'}")

# 可视化
# Visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
colors = ['#e74c3c', '#3498db', '#2ecc71']

for idx, (K, sse_val, ssb_val, total) in enumerate(results):
    ax = axes[idx]
    bar_data = [sse_val, ssb_val]
    bar_labels = ['SSE\n(Within)', 'SSB\n(Between)']
    bar_colors = ['#e74c3c', '#3498db']

    bars = ax.bar(bar_labels, bar_data, color=bar_colors, alpha=0.8, edgecolor='black')
    for bar, val in zip(bars, bar_data):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f'{val:.1f}', ha='center', va='bottom', fontsize=14, fontweight='bold')
    ax.axhline(y=tss, color='gray', linestyle='--', alpha=0.5, label=f'TSS={tss:.0f}')
    ax.set_ylim(0, tss + 2)
    ax.set_title(f'K={K}\nSSE={sse_val:.0f} + SSB={ssb_val:.0f} = {total:.0f}')
    ax.legend()

plt.suptitle("SSE + SSB = TSS (Constant = 10)\n"
             "More clusters → SSE↓, SSB↑, but total stays the same!",
             fontsize=14, fontweight='bold', y=1.05)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step9_sse_ssb_identity.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 10：轮廓系数 — 选择最佳 K
# Step 10: Silhouette Coefficient — Choosing Best K
# ============================================================

print("\n" + "=" * 60)
print("Step 10: Silhouette Coefficient for Choosing K")
print("=" * 60)

from sklearn.metrics import silhouette_score, silhouette_samples

# 手动计算一个点的轮廓系数
# Manually compute silhouette for one point
print("\nManual silhouette computation for one point:")
print("  Suppose point P in cluster A, with 3 other points in A")
a_val = 3.0  # avg distance to own cluster
b_val = 6.0  # min avg distance to other clusters
s_val = (b_val - a_val) / max(a_val, b_val)
print(f"  a (within-cluster avg dist) = {a_val}")
print(f"  b (nearest-cluster avg dist) = {b_val}")
print(f"  s = (b - a) / max(a, b) = ({b_val} - {a_val}) / {max(a_val, b_val)} = {s_val:.4f}")

# 用 sklearn 计算不同 K 的轮廓系数
# Compute silhouette score for different K using sklearn
sil_scores = []
K_range_sil = range(2, 8)
for k in K_range_sil:
    km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
    km_labels = km.fit_predict(X_blobs)
    score = silhouette_score(X_blobs, km_labels)
    sil_scores.append(score)
    print(f"  K={k}: Silhouette = {score:.4f}")

best_k = list(K_range_sil)[np.argmax(sil_scores)]
print(f"\nBest K by Silhouette: K={best_k} (score={max(sil_scores):.4f})")

# 可视化：轮廓计数图 + 最佳 K
# Visualization: Silhouette plot + best K selection
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：轮廓分数 vs K
# Left: Silhouette score vs K
axes[0].plot(list(K_range_sil), sil_scores, 'go-', linewidth=2, markersize=10)
axes[0].axvline(x=best_k, color='red', linestyle='--', alpha=0.7, label=f'Best K={best_k}')
axes[0].set_xlabel('Number of Clusters K')
axes[0].set_ylabel('Silhouette Score')
axes[0].set_title('Silhouette Method: Higher = Better\n'
                  'Pick K with highest average silhouette')
axes[0].legend(fontsize=12)
axes[0].grid(True, alpha=0.3)

# 右图：K=3 的逐点轮廓图
# Right: Per-point silhouette plot for K=3
km3 = KMeans(n_clusters=3, random_state=RANDOM_STATE, n_init=10)
labels_3 = km3.fit_predict(X_blobs)
sample_sil = silhouette_samples(X_blobs, labels_3)

y_lower = 0
for k in range(3):
    cluster_sil = sample_sil[labels_3 == k]
    cluster_sil.sort()
    y_upper = y_lower + len(cluster_sil)

    color = plt.cm.viridis(k / 3)
    axes[1].fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_sil,
                          facecolor=color, edgecolor=color, alpha=0.7)
    axes[1].text(-0.05, y_lower + 0.5 * len(cluster_sil), f'Cluster {k}',
                fontsize=10, fontweight='bold')
    y_lower = y_upper

axes[1].axvline(x=silhouette_score(X_blobs, labels_3), color='red',
                linestyle='--', linewidth=2,
                label=f'Mean = {silhouette_score(X_blobs, labels_3):.3f}')
axes[1].set_xlabel('Silhouette Coefficient')
axes[1].set_ylabel('Points (sorted within cluster)')
axes[1].set_title('Per-Point Silhouette for K=3\n'
                  's ≈ 1: well-clustered | s ≈ 0: boundary | s < 0: misclassified')
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.suptitle("Silhouette Analysis: Per-Point Cluster Quality Assessment",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step10_silhouette_analysis.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 步骤 11：四大算法大比拼
# Step 11: Four Algorithms Head-to-Head Comparison
# ============================================================

print("\n" + "=" * 60)
print("Step 11: Four Algorithms — Head-to-Head Comparison")
print("=" * 60)

# 生成不同类型的数据
# Generate different types of data
datasets = {
    'Blobs (spherical)': make_blobs(n_samples=300, centers=3, cluster_std=0.8,
                                     random_state=RANDOM_STATE),
    'Moons (crescent)': make_moons(n_samples=300, noise=0.05, random_state=RANDOM_STATE),
    'Circles (ring)': make_circles(n_samples=300, noise=0.05, factor=0.5,
                                    random_state=RANDOM_STATE),
}

# 应用四种算法
# Apply four algorithms
from sklearn.cluster import AgglomerativeClustering

fig, axes = plt.subplots(3, 5, figsize=(25, 15))

for row, (name, (X, y_true_data)) in enumerate(datasets.items()):
    # 真实标签
    # True labels
    axes[row, 0].scatter(X[:, 0], X[:, 1], c=y_true_data, cmap='Set1', s=20, alpha=0.7)
    axes[row, 0].set_title(f'{name}\nTrue Labels')

    # K-Means
    n_c = len(set(y_true_data))
    km = KMeans(n_clusters=n_c, random_state=RANDOM_STATE, n_init=10)
    axes[row, 1].scatter(X[:, 0], X[:, 1], c=km.fit_predict(X),
                         cmap='Set1', s=20, alpha=0.7)
    axes[row, 1].set_title('K-Means')

    # Hierarchical
    agg = AgglomerativeClustering(n_clusters=n_c, linkage='ward')
    axes[row, 2].scatter(X[:, 0], X[:, 1], c=agg.fit_predict(X),
                         cmap='Set1', s=20, alpha=0.7)
    axes[row, 2].set_title('Hierarchical\n(Ward)')

    # DBSCAN
    db = DBSCAN(eps=0.3, min_samples=5)
    db_l = db.fit_predict(X)
    noise_m = db_l == -1
    axes[row, 3].scatter(X[~noise_m, 0], X[~noise_m, 1], c=db_l[~noise_m],
                         cmap='Set1', s=20, alpha=0.7)
    if noise_m.any():
        axes[row, 3].scatter(X[noise_m, 0], X[noise_m, 1],
                             c='black', marker='x', s=30, alpha=0.5)
    axes[row, 3].set_title(f'DBSCAN\n(eps=0.3, noise={noise_m.sum()})')

    # GMM
    gmm = GaussianMixture(n_components=n_c, random_state=RANDOM_STATE)
    axes[row, 4].scatter(X[:, 0], X[:, 1], c=gmm.fit_predict(X),
                         cmap='Set1', s=20, alpha=0.7)
    axes[row, 4].set_title('GMM (EM)')

    for ax in axes[row]:
        ax.set_xlabel('X₁')
        ax.set_ylabel('X₂')

# 添加行标注
# Add row annotations
for row, name in enumerate(['✅ ✅ ✅ ✅', '❌ ❌ ✅ ❌', '❌ ❌ ✅ ❌']):
    axes[row, 0].set_ylabel(list(datasets.keys())[row], fontsize=13, fontweight='bold')

plt.suptitle("Four Clustering Algorithms on Three Dataset Types\n"
             "Only DBSCAN handles non-spherical shapes correctly!",
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step11_four_algorithms_comparison.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print("\nAlgorithm Performance Summary:")
print("  Blobs (spherical):  ALL algorithms work ✅")
print("  Moons (crescent):   Only DBSCAN works ✅")
print("  Circles (ring):     Only DBSCAN works ✅")


# ============================================================
# 步骤 12：K-Means vs EM — 数学关系
# Step 12: K-Means is a Special Case of EM
# ============================================================

print("\n" + "=" * 60)
print("Step 12: K-Means is a Special Case of EM")
print("=" * 60)

print("""
K-Means vs EM/GMM Relationship:

  K-Means is EM with two constraints:
  1. All cluster variances are equal and FIXED
  2. Membership probabilities are forced to 0 or 1 (hard assignment)

  Remove these constraints → you get EM/GMM:
  - Different cluster variances → elliptical clusters
  - Probability memberships → soft assignment

  ┌─────────────────────────────────────────────────────┐
  │  K-Means (Special Case)  →  EM/GMM (General Case)  │
  │                                                     │
  │  Hard: P(k|x) ∈ {0, 1}  →  Soft: P(k|x) ∈ [0, 1] │
  │  Equal σ² (fixed)        →  Different σ² (learned)  │
  │  Spherical only          →  Elliptical shapes       │
  │  Only centroids          →  Full Gaussian params    │
  └─────────────────────────────────────────────────────┘
""")

# 可视化：不同方差的2D数据
# Visualization: 2D data with different variances
X_unequal, _ = make_blobs(n_samples=300, centers=[[0, 0], [4, 4], [8, 0]],
                            cluster_std=[0.5, 2.0, 0.8], random_state=RANDOM_STATE)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# K-Means（假设等方差，球形）
# K-Means (assumes equal variance, spherical)
km_un = KMeans(n_clusters=3, random_state=RANDOM_STATE, n_init=10)
axes[0].scatter(X_unequal[:, 0], X_unequal[:, 1], c=km_un.fit_predict(X_unequal),
                cmap='viridis', s=20, alpha=0.7)
axes[0].scatter(km_un.cluster_centers_[:, 0], km_un.cluster_centers_[:, 1],
                c='red', marker='X', s=200, edgecolors='black', linewidths=2)
axes[0].set_title('K-Means: Assumes Equal Spherical Clusters\n'
                  '(Struggles with different-sized clusters)')

# GMM（学习不同方差，椭圆形）
# GMM (learns different variances, elliptical)
gmm_un = GaussianMixture(n_components=3, random_state=RANDOM_STATE)
gmm_un.fit(X_unequal)
axes[1].scatter(X_unequal[:, 0], X_unequal[:, 1], c=gmm_un.predict(X_unequal),
                cmap='viridis', s=20, alpha=0.7)
axes[1].scatter(gmm_un.means_[:, 0], gmm_un.means_[:, 1],
                c='red', marker='X', s=200, edgecolors='black', linewidths=2)

# 画协方差椭圆
# Draw covariance ellipses
from matplotlib.patches import Ellipse
for k in range(3):
    cov = gmm_un.covariances_[k]
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    for n_std in [1, 2]:
        ellipse = Ellipse(xy=gmm_un.means_[k], width=2 * n_std * np.sqrt(eigenvalues[0]),
                          height=2 * n_std * np.sqrt(eigenvalues[1]), angle=angle,
                          fill=False, color='red', linewidth=1.5, linestyle='--', alpha=0.5)
        axes[1].add_patch(ellipse)

axes[1].set_title('GMM (EM): Learns Different Sizes + Shapes\n'
                  '(Ellipses = 1σ, 2σ contours)')

for ax in axes:
    ax.set_xlabel('X₁')
    ax.set_ylabel('X₂')

plt.suptitle("K-Means = EM with Equal Fixed Variances + Hard Assignment\n"
             "EM relaxes both constraints → better fit on unequal clusters",
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'step12_kmeans_vs_em.png'),
            dpi=150, bbox_inches='tight')
plt.close()


# ============================================================
# 总结
# Summary
# ============================================================

print("\n" + "=" * 60)
print("Summary: Clustering Algorithm Evolution")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│  K-Means  ──► Simple, fast, but: must specify K,           │
│               spherical only, no noise handling             │
│      │                                                      │
│      ▼                                                      │
│  Hierarchical ──► No K needed! Dendrogram shows structure   │
│      │            but: O(n³) too slow, still spherical      │
│      ▼                                                      │
│  DBSCAN  ──► Any shape! Built-in noise detection!           │
│      │        but: single ε, varying density fails          │
│      ▼                                                      │
│  EM/GMM  ──► Soft assignment (probability memberships)      │
│               K-Means is its special case!                  │
│               but: still needs K, assumes Gaussian          │
└─────────────────────────────────────────────────────────────┘

No perfect algorithm — choose based on your data!
""")

print(f"\nAll visualizations saved to: {OUTPUT_DIR}")
print(f"Files generated:")
for f in sorted(os.listdir(OUTPUT_DIR)):
    fpath = os.path.join(OUTPUT_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {f} ({size_kb:.1f} KB)")
