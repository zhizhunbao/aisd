"""
Generate 6 separate anomaly detection method images for Week 9 storyline.
每个方法单独一张图，嵌入对应章节
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.use('Agg')
np.random.seed(42)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {path}")
    plt.close(fig)

# ── Common data ──
normal_x = np.random.normal(0.5, 0.12, 60)
normal_y = np.random.normal(0.5, 0.12, 60)

# ============================================================
# 1. Statistical
# ============================================================
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_title('1. Statistical (Probability-based)', fontsize=13, fontweight='bold', color='#1565C0')

from scipy.stats import norm
x_range = np.linspace(-0.1, 1.1, 200)
pdf = norm.pdf(x_range, 0.5, 0.12)
ax.fill_between(x_range, pdf, alpha=0.2, color='#2196F3')
ax.plot(x_range, pdf, 'b-', linewidth=2)
for xi in normal_x[:20]:
    ax.plot(xi, 0.15, 'o', color='#2196F3', markersize=5, alpha=0.6)
ax.plot(0.95, 0.15, 'o', color='red', markersize=10, zorder=5)
ax.annotate('Outlier (low prob)', (0.95, 0.15), textcoords="offset points",
            xytext=(0, 20), fontsize=9, color='red', ha='center',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.axvline(x=0.82, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(0.84, 2.5, 'threshold', fontsize=9, color='orange', rotation=90)
ax.text(0.5, 3.0, 'P(x) < threshold = Anomaly', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(-0.1, 1.1); ax.set_ylim(-0.2, 4)
ax.set_xlabel('Value', fontsize=10); ax.set_ylabel('Probability Density', fontsize=10)
plt.tight_layout()
save(fig, 'Week9_AD1_Statistical.png')

# ============================================================
# 2. Proximity / Distance
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_title('2. Proximity / Distance (kNN distance)', fontsize=13, fontweight='bold', color='#1565C0')
ax.scatter(normal_x, normal_y, c='#2196F3', s=30, alpha=0.6, zorder=3)
ox, oy = 0.92, 0.88
ax.plot(ox, oy, 'o', color='red', markersize=12, zorder=5)
dists = np.sqrt((normal_x - ox)**2 + (normal_y - oy)**2)
k_idx = np.argsort(dists)[:3]
for ki in k_idx:
    ax.plot([ox, normal_x[ki]], [oy, normal_y[ki]], 'r--', alpha=0.5, linewidth=1.2)
ax.annotate('Outlier (far from kNN)', (ox, oy), textcoords="offset points",
            xytext=(-20, -25), fontsize=9, color='red', ha='center',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.text(0.5, 0.05, 'dist(x, kth-NN) > threshold = Anomaly', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(0, 1.1); ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('Feature 1', fontsize=10); ax.set_ylabel('Feature 2', fontsize=10)
plt.tight_layout()
save(fig, 'Week9_AD2_Proximity.png')

# ============================================================
# 3. Density / LOF
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_title('3. Density / LOF (Relative density)', fontsize=13, fontweight='bold', color='#1565C0')
dense_x = np.random.normal(0.3, 0.06, 40)
dense_y = np.random.normal(0.3, 0.06, 40)
ax.scatter(dense_x, dense_y, c='#2196F3', s=25, alpha=0.6, zorder=3)
sparse_x = np.random.normal(0.75, 0.1, 15)
sparse_y = np.random.normal(0.75, 0.1, 15)
ax.scatter(sparse_x, sparse_y, c='#4CAF50', s=25, alpha=0.6, zorder=3)
ox, oy = 0.55, 0.52
ax.plot(ox, oy, 'o', color='red', markersize=12, zorder=5)
ax.annotate('Outlier\n(sparse vs dense neighbors)', (ox, oy),
            textcoords="offset points", xytext=(12, 18), fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
circle1 = plt.Circle((0.3, 0.3), 0.12, fill=False, color='#2196F3', linestyle='--', linewidth=1.5)
circle2 = plt.Circle((0.75, 0.75), 0.2, fill=False, color='#4CAF50', linestyle='--', linewidth=1.5)
ax.add_patch(circle1); ax.add_patch(circle2)
ax.text(0.3, 0.12, 'Dense', fontsize=9, ha='center', color='#1565C0', fontweight='bold')
ax.text(0.75, 0.48, 'Sparse', fontsize=9, ha='center', color='#388E3C', fontweight='bold')
ax.text(0.5, 0.02, 'relative density >> 1 = Anomaly', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(0, 1.05); ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('Feature 1', fontsize=10); ax.set_ylabel('Feature 2', fontsize=10)
plt.tight_layout()
save(fig, 'Week9_AD3_LOF.png')

# ============================================================
# 4. Clustering
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_title('4. Clustering (Far from cluster center)', fontsize=13, fontweight='bold', color='#1565C0')
ca_x = np.random.normal(0.3, 0.08, 30)
ca_y = np.random.normal(0.3, 0.08, 30)
ax.scatter(ca_x, ca_y, c='#2196F3', s=25, alpha=0.6, zorder=3)
ax.plot(0.3, 0.3, '+', color='#0D47A1', markersize=15, markeredgewidth=3, zorder=4)
cb_x = np.random.normal(0.7, 0.08, 30)
cb_y = np.random.normal(0.7, 0.08, 30)
ax.scatter(cb_x, cb_y, c='#4CAF50', s=25, alpha=0.6, zorder=3)
ax.plot(0.7, 0.7, '+', color='#1B5E20', markersize=15, markeredgewidth=3, zorder=4)
ax.plot(0.15, 0.85, 'o', color='red', markersize=12, zorder=5)
ax.annotate('Outlier (no cluster)', (0.15, 0.85), textcoords="offset points",
            xytext=(15, -15), fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.scatter([0.9, 0.92, 0.91], [0.15, 0.17, 0.13], c='orange', s=30, alpha=0.8,
           zorder=3, edgecolors='red', linewidths=1)
ax.annotate('Tiny cluster = Outlier', (0.91, 0.15), textcoords="offset points",
            xytext=(-30, -25), fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.text(0.5, 0.02, 'Far from centers OR tiny cluster = Anomaly', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(0, 1.05); ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('Feature 1', fontsize=10); ax.set_ylabel('Feature 2', fontsize=10)
plt.tight_layout()
save(fig, 'Week9_AD4_Clustering.png')

# ============================================================
# 5. Reconstruction (PCA / Autoencoder)
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_title('5. Reconstruction (PCA / Autoencoder)', fontsize=13, fontweight='bold', color='#1565C0')
t = np.random.uniform(0.1, 0.9, 30)
rx = t + np.random.normal(0, 0.02, 30)
ry = t + np.random.normal(0, 0.02, 30)
ax.scatter(rx, ry, c='#2196F3', s=30, alpha=0.6, zorder=3)
ax.plot([0, 1], [0, 1], 'b--', alpha=0.3, linewidth=2, label='Low-dim subspace')
ni = 15
ax.plot([rx[ni], (rx[ni]+ry[ni])/2], [ry[ni], (rx[ni]+ry[ni])/2], 'g-', linewidth=1.5, alpha=0.7)
ax.plot((rx[ni]+ry[ni])/2, (rx[ni]+ry[ni])/2, 's', color='green', markersize=6)
ax.text(rx[ni]+0.03, ry[ni]+0.05, 'small error', fontsize=8, color='green')
ox, oy = 0.2, 0.8
proj = (ox + oy) / 2
ax.plot(ox, oy, 'o', color='red', markersize=12, zorder=5)
ax.plot(proj, proj, 's', color='red', markersize=8, zorder=5)
ax.plot([ox, proj], [oy, proj], 'r-', linewidth=2.5, zorder=4)
ax.annotate('Outlier (large error)', (ox, oy), textcoords="offset points",
            xytext=(-10, 15), fontsize=9, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.text(0.15, 0.6, '||x - x_hat||', fontsize=11, color='red', fontweight='bold', rotation=-45)
ax.text(0.6, 0.08, '||x - x_hat|| > threshold = Anomaly', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)
ax.set_xlabel('Feature 1', fontsize=10); ax.set_ylabel('Feature 2', fontsize=10)
ax.set_aspect('equal')
plt.tight_layout()
save(fig, 'Week9_AD5_Reconstruction.png')

# ============================================================
# 6. One-Class SVM (OCSVM)
# ============================================================
fig, ax = plt.subplots(figsize=(6, 5))
ax.set_title('6. One-Class SVM (OCSVM)', fontsize=13, fontweight='bold', color='#1565C0')
oc_x = np.random.normal(0.5, 0.1, 50)
oc_y = np.random.normal(0.5, 0.1, 50)
ax.scatter(oc_x, oc_y, c='#2196F3', s=25, alpha=0.6, zorder=3)
theta = np.linspace(0, 2*np.pi, 100)
bx = 0.5 + 0.3 * np.cos(theta)
by = 0.5 + 0.3 * np.sin(theta)
ax.plot(bx, by, 'b-', linewidth=2.5, label='f(x) = 0 boundary')
ax.fill(bx, by, alpha=0.08, color='#2196F3')
ax.plot(0, 0, 'k^', markersize=12, zorder=5)
ax.text(0.02, 0.05, 'Origin', fontsize=10, fontweight='bold')
ax.text(0.5, 0.5, 'f(x) >= 0\nNormal', fontsize=11, ha='center', va='center',
        color='#1565C0', fontweight='bold')
ax.plot(0.9, 0.85, 'o', color='red', markersize=12, zorder=5)
ax.annotate('f(x) < 0 = Outlier', (0.9, 0.85), textcoords="offset points",
            xytext=(-20, 15), fontsize=10, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.2))
ax.plot(0.08, 0.85, 'o', color='red', markersize=10, zorder=5)
ax.text(0.5, 0.02, 'v=0.05 tight boundary, v=0.2 loose boundary', fontsize=9, ha='center',
        bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#FFD54F'))
ax.set_xlim(-0.1, 1.05); ax.set_ylim(-0.1, 1.05)
ax.set_xlabel('Feature 1', fontsize=10); ax.set_ylabel('Feature 2', fontsize=10)
plt.tight_layout()
save(fig, 'Week9_AD6_OCSVM.png')

print("\nAll 6 images generated!")
