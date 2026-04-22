"""
Week 6 Clustering Storyline — Visualization Generator
=====================================================
Generates 6 plots for the clustering storyline:
  1. K-Means iteration demo (centroid movement)
  2. K-Means failure on non-spherical data (moons & circles)
  3. Hierarchical clustering dendrogram
  4. DBSCAN core/border/noise classification
  5. GMM soft assignment (overlapping Gaussians)
  6. Silhouette coefficient comparison

Usage:
  cd aisd/
  uv run python courses/ml/notes/week6_clustering_generated_images/generate_clustering_plots.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import os

# ── 输出目录 / Output directory ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150

# ── 全局样式 / Global style ──
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#fafafa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.size': 11,
})


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 1: K-Means Iteration Demo                             ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_kmeans_iteration():
    """Show K-Means convergence: initial random centroids → final stable centroids."""
    np.random.seed(42)

    # 生成3个簇 / Generate 3 clusters
    c1 = np.random.randn(30, 2) * 0.6 + [2, 2]
    c2 = np.random.randn(30, 2) * 0.6 + [6, 2]
    c3 = np.random.randn(30, 2) * 0.6 + [4, 6]
    X = np.vstack([c1, c2, c3])

    # 手动K-Means迭代 / Manual K-Means iterations
    centroids = np.array([[3.0, 5.0], [5.0, 1.0], [7.0, 5.0]])  # bad initial
    colors_map = ['#e74c3c', '#3498db', '#2ecc71']

    fig, axes = plt.subplots(1, 4, figsize=(18, 4.2))
    titles = ['Iter 0: Random Init', 'Iter 1: Reassign', 'Iter 2: Update', 'Iter 3: Converged']

    for step in range(4):
        ax = axes[step]

        # 分配步骤 / Assignment step
        dists = np.array([np.sum((X - c)**2, axis=1) for c in centroids])
        labels = np.argmin(dists, axis=0)

        # 画数据点 / Plot data points
        for k in range(3):
            mask = labels == k
            ax.scatter(X[mask, 0], X[mask, 1], c=colors_map[k], s=25, alpha=0.6, edgecolors='none')

        # 画质心 / Plot centroids
        for k in range(3):
            ax.scatter(*centroids[k], c=colors_map[k], s=200, marker='*',
                       edgecolors='black', linewidths=1.2, zorder=5)
            if step > 0:
                ax.scatter(*prev_centroids[k], c=colors_map[k], s=100, marker='x',
                           linewidths=1.5, alpha=0.4, zorder=4)
                ax.annotate('', xy=centroids[k], xytext=prev_centroids[k],
                            arrowprops=dict(arrowstyle='->', color=colors_map[k],
                                            lw=1.5, alpha=0.6))

        ax.set_title(titles[step], fontsize=11, fontweight='bold')
        ax.set_xlim(-0.5, 9)
        ax.set_ylim(-1, 9)
        ax.set_aspect('equal')
        ax.tick_params(labelsize=8)

        # 更新步骤 / Update step
        prev_centroids = centroids.copy()
        new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(3)])
        centroids = new_centroids

    fig.suptitle('K-Means Iteration: Centroids (★) Move Toward Cluster Centers',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_KMeans_Iteration.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 1: Week6_KMeans_Iteration.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 2: K-Means Failure on Non-Spherical Data              ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_kmeans_failure():
    """Show K-Means fails on moons and concentric circles."""
    from sklearn.datasets import make_moons, make_circles
    from sklearn.cluster import KMeans

    np.random.seed(42)

    fig, axes = plt.subplots(2, 2, figsize=(10, 9))

    # ── Moons ──
    X_moon, y_moon = make_moons(n_samples=300, noise=0.08, random_state=42)
    km_moon = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X_moon)

    axes[0, 0].scatter(X_moon[:, 0], X_moon[:, 1], c=y_moon, cmap='RdBu', s=15, alpha=0.7)
    axes[0, 0].set_title('Moons: Ground Truth', fontweight='bold')

    axes[0, 1].scatter(X_moon[:, 0], X_moon[:, 1], c=km_moon.labels_, cmap='RdBu', s=15, alpha=0.7)
    axes[0, 1].scatter(*km_moon.cluster_centers_.T, c='gold', s=200, marker='*',
                         edgecolors='black', linewidths=1.2, zorder=5)
    axes[0, 1].set_title('Moons: K-Means (K=2) ❌', fontweight='bold', color='#c0392b')

    # ── Circles ──
    X_circ, y_circ = make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)
    km_circ = KMeans(n_clusters=2, random_state=0, n_init=10).fit(X_circ)

    axes[1, 0].scatter(X_circ[:, 0], X_circ[:, 1], c=y_circ, cmap='RdBu', s=15, alpha=0.7)
    axes[1, 0].set_title('Circles: Ground Truth', fontweight='bold')

    axes[1, 1].scatter(X_circ[:, 0], X_circ[:, 1], c=km_circ.labels_, cmap='RdBu', s=15, alpha=0.7)
    axes[1, 1].scatter(*km_circ.cluster_centers_.T, c='gold', s=200, marker='*',
                         edgecolors='black', linewidths=1.2, zorder=5)
    axes[1, 1].set_title('Circles: K-Means (K=2) ❌', fontweight='bold', color='#c0392b')

    for ax in axes.flat:
        ax.set_aspect('equal')
        ax.tick_params(labelsize=8)

    fig.suptitle('K-Means Fails on Non-Spherical Data\n'
                 'K-Means assumes spherical clusters → catastrophic on moons & rings',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_KMeans_Failure.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 2: Week6_KMeans_Failure.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 3: Hierarchical Clustering Dendrogram                 ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_dendrogram():
    """Show dendrogram with different linkage methods and a cut line."""
    np.random.seed(42)

    # 小数据集便于观察 / Small dataset for clarity
    X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6],
                  [9, 11], [8, 2], [10, 2], [9, 3]])
    labels = [f'P{i}' for i in range(len(X))]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    methods = ['single', 'complete', 'ward']
    titles = ['MIN (Single) Linkage\nTends to chain-like clusters',
              'MAX (Complete) Linkage\nTends to compact clusters',
              'Ward Linkage\nMinimizes variance increase']
    cut_colors = ['#e74c3c', '#3498db', '#2ecc71']

    for i, (method, title) in enumerate(zip(methods, titles)):
        Z = linkage(X, method=method)
        ax = axes[i]
        dendrogram(Z, labels=labels, ax=ax, leaf_font_size=10,
                   color_threshold=0.7 * max(Z[:, 2]))
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_ylabel('Distance')

        # 切割线 / Cut line for K=3
        cut_height = 0.6 * max(Z[:, 2])
        ax.axhline(y=cut_height, color=cut_colors[i], linestyle='--',
                   linewidth=2, alpha=0.7, label=f'Cut → K=3')
        ax.legend(fontsize=9)
        ax.tick_params(labelsize=9)

    fig.suptitle('Hierarchical Clustering: Dendrogram Comparison\n'
                 'Cut the tree at any height to get K clusters',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_Dendrogram.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 3: Week6_Dendrogram.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 4: DBSCAN Core / Border / Noise Classification        ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_dbscan():
    """Visualize DBSCAN point types: core, border, noise with ε-neighborhoods."""
    np.random.seed(42)

    # 两个密度不同的簇 + 噪声 / Two clusters + noise
    c1 = np.random.randn(40, 2) * 0.4 + [2, 2]
    c2 = np.random.randn(30, 2) * 0.5 + [5, 5]
    noise = np.random.uniform(0, 7, size=(8, 2))
    X = np.vstack([c1, c2, noise])

    from sklearn.cluster import DBSCAN

    eps = 0.8
    min_samples = 5
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_
    core_mask = np.zeros(len(X), dtype=bool)
    core_mask[db.core_sample_indices_] = True

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # ── Left: Point classification ──
    ax = axes[0]
    # Noise
    noise_mask = labels == -1
    ax.scatter(X[noise_mask, 0], X[noise_mask, 1], c='gray', marker='x',
               s=60, linewidths=2, label='Noise', zorder=3)
    # Border
    border_mask = ~core_mask & ~noise_mask
    ax.scatter(X[border_mask, 0], X[border_mask, 1], c='#f39c12', s=40,
               edgecolors='black', linewidths=0.5, label='Border', zorder=3)
    # Core
    ax.scatter(X[core_mask, 0], X[core_mask, 1], c='#e74c3c', s=60,
               edgecolors='black', linewidths=0.5, label='Core', zorder=3)

    # Draw a few ε-circles for core points
    for idx in db.core_sample_indices_[:6]:
        circle = plt.Circle(X[idx], eps, fill=False, color='#e74c3c',
                            linestyle='--', linewidth=0.8, alpha=0.4)
        ax.add_patch(circle)

    ax.set_title(f'DBSCAN Point Classification\nε={eps}, MinPts={min_samples}',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.set_aspect('equal')
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 8)

    # ── Right: Final clusters ──
    ax = axes[1]
    unique_labels = set(labels)
    cmap_list = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']
    for k in sorted(unique_labels):
        mask = labels == k
        if k == -1:
            ax.scatter(X[mask, 0], X[mask, 1], c='gray', marker='x',
                       s=60, linewidths=2, label='Noise')
        else:
            color = cmap_list[k % len(cmap_list)]
            ax.scatter(X[mask, 0], X[mask, 1], c=color, s=40,
                       edgecolors='black', linewidths=0.5, label=f'Cluster {k}')

    ax.set_title('DBSCAN Final Clusters\nArbitrary shape + noise auto-removed',
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='upper left')
    ax.set_aspect('equal')
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 8)

    fig.suptitle('DBSCAN: Density-Based Clustering\n'
                 'Core points (≥MinPts neighbors) form cluster cores; '
                 'Border points attach; isolated points = Noise',
                 fontsize=12, fontweight='bold', y=1.04)
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_DBSCAN.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 4: Week6_DBSCAN.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 5: GMM Soft Assignment (Overlapping Gaussians)        ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_gmm():
    """Show GMM soft assignment vs K-Means hard assignment."""
    np.random.seed(42)

    from sklearn.mixture import GaussianMixture
    from sklearn.cluster import KMeans

    # 生成两个重叠的高斯 / Two overlapping Gaussians
    c1 = np.random.randn(100, 2) * 0.8 + [2, 2]
    c2 = np.random.randn(100, 2) * np.array([1.2, 0.5]) + [4.5, 2.5]
    X = np.vstack([c1, c2])

    gmm = GaussianMixture(n_components=2, random_state=42).fit(X)
    km = KMeans(n_clusters=2, random_state=42, n_init=10).fit(X)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # ── Left: K-Means hard assignment ──
    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], c=km.labels_, cmap='RdBu', s=25, alpha=0.7)
    ax.scatter(*km.cluster_centers_.T, c='gold', s=200, marker='*',
               edgecolors='black', linewidths=1.2, zorder=5)
    ax.set_title('K-Means: Hard Assignment\nEvery point is 100% in one cluster',
                 fontsize=11, fontweight='bold')
    ax.set_aspect('equal')

    # ── Right: GMM soft assignment ──
    ax = axes[1]
    probs = gmm.predict_proba(X)  # shape (n, 2)
    # 用概率着色 / Color by probability
    ax.scatter(X[:, 0], X[:, 1], c=probs[:, 0], cmap='RdBu', s=25, alpha=0.7,
               vmin=0, vmax=1)

    # Draw confidence ellipses
    for k in range(2):
        mean = gmm.means_[k]
        cov = gmm.covariances_[k]
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
        for n_std in [1, 2]:
            width, height = 2 * n_std * np.sqrt(eigenvalues)
            ellipse = mpatches.Ellipse(mean, width, height, angle=angle,
                                        fill=False, linewidth=1.5,
                                        color=['#e74c3c', '#3498db'][k],
                                        linestyle=['--', '-'][n_std-1],
                                        alpha=0.7)
            ax.add_patch(ellipse)

    ax.set_title('GMM: Soft Assignment (Probability)\nPoints in overlap zone → partial membership',
                 fontsize=11, fontweight='bold')
    ax.set_aspect('equal')

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='RdBu', norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes[1], shrink=0.7)
    cbar.set_label('P(Cluster 0 | x)', fontsize=10)

    fig.suptitle('Hard Assignment (K-Means) vs Soft Assignment (GMM)\n'
                 'GMM: each point has a probability of belonging to each cluster',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_GMM_SoftAssignment.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 5: Week6_GMM_SoftAssignment.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Plot 6: Silhouette Coefficient — Choosing K                ║
# ╚══════════════════════════════════════════════════════════════╝
def plot_silhouette():
    """Show silhouette analysis for different K values + SSE elbow plot."""
    np.random.seed(42)

    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score, silhouette_samples

    # 生成3个簇 / Generate 3 true clusters
    c1 = np.random.randn(60, 2) * 0.5 + [1, 1]
    c2 = np.random.randn(60, 2) * 0.5 + [5, 1]
    c3 = np.random.randn(60, 2) * 0.5 + [3, 5]
    X = np.vstack([c1, c2, c3])

    K_range = range(2, 7)
    sse_list = []
    sil_list = []

    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X)
        sse_list.append(km.inertia_)
        sil_list.append(silhouette_score(X, km.labels_))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # ── Left: SSE Elbow ──
    ax = axes[0]
    ax.plot(list(K_range), sse_list, 'o-', color='#e74c3c', linewidth=2, markersize=8)
    ax.axvline(x=3, color='#2ecc71', linestyle='--', linewidth=2, alpha=0.7, label='Elbow at K=3')
    ax.set_xlabel('K (Number of Clusters)', fontsize=11)
    ax.set_ylabel('SSE (Intra-cluster Sum of Squares)', fontsize=11)
    ax.set_title('SSE Elbow Method\nSSE always decreases — look for the "elbow"',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_xticks(list(K_range))

    # ── Right: Silhouette Score ──
    ax = axes[1]
    bars = ax.bar(list(K_range), sil_list, color=['#3498db' if k != 3 else '#2ecc71' for k in K_range],
                  edgecolor='black', linewidth=0.5)
    ax.set_xlabel('K (Number of Clusters)', fontsize=11)
    ax.set_ylabel('Avg Silhouette Score', fontsize=11)
    ax.set_title('Silhouette Analysis\nHighest score → best K (here K=3)',
                 fontsize=11, fontweight='bold')
    ax.set_xticks(list(K_range))

    # 标注最高分 / Annotate best
    best_idx = np.argmax(sil_list)
    best_k = list(K_range)[best_idx]
    ax.annotate(f'Best: K={best_k}\n(s={sil_list[best_idx]:.3f})',
                xy=(best_k, sil_list[best_idx]),
                xytext=(best_k + 1, sil_list[best_idx]),
                fontsize=10, fontweight='bold', color='#27ae60',
                arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1.5))

    fig.suptitle('How to Choose K: Elbow Method (SSE) vs Silhouette Score',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'Week6_Silhouette_Elbow.png'),
                dpi=DPI, bbox_inches='tight')
    plt.close()
    print("✅ Plot 6: Week6_Silhouette_Elbow.png")


# ╔══════════════════════════════════════════════════════════════╗
# ║  Main: Run all plots                                        ║
# ╚══════════════════════════════════════════════════════════════╝
if __name__ == '__main__':
    print("=" * 60)
    print("Week 6 Clustering — Generating Storyline Plots")
    print("=" * 60)

    plot_kmeans_iteration()
    plot_kmeans_failure()
    plot_dendrogram()
    plot_dbscan()
    plot_gmm()
    plot_silhouette()

    print("\n" + "=" * 60)
    print(f"All 6 plots saved to: {SCRIPT_DIR}")
    print("=" * 60)
