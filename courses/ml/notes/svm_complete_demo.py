"""
SVM Complete Demo: From Linear Separators to Kernel Tricks
CST8506 Advanced Machine Learning - Week 2

Demonstrates all key SVM concepts from the lecture:
1. Linear separation and maximum margin
2. Support vectors visualization
3. Effect of C parameter (soft margin)
4. Kernel comparison (Linear vs RBF vs Polynomial)
5. Effect of gamma parameter
6. MMC vs SVC vs SVM progression
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# 输出目录（相对于脚本位置）
# Output directory (relative to script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "svm_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 可视化配色
# Visualization color scheme
COLORS_LIGHT = ListedColormap(["#FFAAAA", "#AAAAFF"])
COLORS_BOLD = ["#FF4444", "#4444FF"]
FIGSIZE = (10, 6)
DPI = 150


def plot_decision_boundary(clf, X, y, ax, title, show_margin=True, show_sv=True):
    """Plot SVM decision boundary with optional margin lines and support vectors."""
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.3, cmap=COLORS_LIGHT)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], c=COLORS_BOLD[0],
               edgecolors="k", s=50, label="Class 0")
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c=COLORS_BOLD[1],
               edgecolors="k", s=50, label="Class 1")

    # 间隔边界线 (margin lines): 决策函数值为 -1 和 +1 的等高线
    # Margin lines: contours where decision function equals -1 and +1
    if show_margin:
        Z_decision = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        Z_decision = Z_decision.reshape(xx.shape)
        ax.contour(xx, yy, Z_decision, levels=[-1, 0, 1],
                   linestyles=["--", "-", "--"], colors="k", linewidths=[1, 2, 1])

    # 标记支持向量
    # Highlight support vectors
    if show_sv and hasattr(clf, "support_vectors_"):
        ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
                   s=200, facecolors="none", edgecolors="lime", linewidths=2,
                   label=f"Support Vectors (n={len(clf.support_vectors_)})")

    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(loc="best", fontsize=8)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)


# ============================================================
# 演示 1：线性分类器与最大间隔
# Demo 1: Linear Separator and Maximum Margin
# ============================================================
print("=" * 60)
print("Demo 1: Linear Separator and Maximum Margin")
print("=" * 60)

# 生成线性可分数据
# Generate linearly separable data
X_linear, y_linear = make_blobs(n_samples=100, centers=2,
                                random_state=RANDOM_STATE, cluster_std=1.2)

clf_linear = SVC(kernel="linear", C=1.0)
clf_linear.fit(X_linear, y_linear)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：无间隔线（普通分类器视角）
# Left: without margin lines (generic classifier view)
plot_decision_boundary(clf_linear, X_linear, y_linear, axes[0],
                       "Any Linear Classifier", show_margin=False, show_sv=False)

# 右图：带间隔线和支持向量（SVM 视角）
# Right: with margin lines and support vectors (SVM view)
plot_decision_boundary(clf_linear, X_linear, y_linear, axes[1],
                       "SVM: Maximum Margin Classifier")

w = clf_linear.coef_[0]
margin = 2 / np.linalg.norm(w)
axes[1].text(0.02, 0.02, f"Margin width = 2/||w|| = {margin:.3f}",
             transform=axes[1].transAxes, fontsize=10,
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

plt.suptitle("Why SVM? — Finding the Widest Gap Between Classes",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "01_linear_separator_margin.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()

print(f"  Support vectors: {len(clf_linear.support_vectors_)}")
print(f"  Margin width: {margin:.4f}")
print(f"  w = {w}")
print(f"  b = {clf_linear.intercept_[0]:.4f}")
print()


# ============================================================
# 演示 2：C 参数的影响（软间隔 vs 硬间隔）
# Demo 2: Effect of C Parameter (Soft Margin vs Hard Margin)
# ============================================================
print("=" * 60)
print("Demo 2: Effect of C Parameter (Soft vs Hard Margin)")
print("=" * 60)

# 生成有重叠的数据
# Generate overlapping data
X_overlap, y_overlap = make_blobs(n_samples=150, centers=2,
                                  random_state=RANDOM_STATE, cluster_std=2.5)

# C 值越大惩罚越严，间隔越窄；C 值越小允许更多误分类，间隔越宽
# Larger C = stricter penalty, narrower margin; Smaller C = more tolerant, wider margin
c_values = [0.01, 0.1, 1.0, 100.0]
fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))

for ax, c_val in zip(axes, c_values):
    clf = SVC(kernel="linear", C=c_val)
    clf.fit(X_overlap, y_overlap)
    w = clf.coef_[0]
    margin = 2 / np.linalg.norm(w)
    n_sv = len(clf.support_vectors_)
    plot_decision_boundary(clf, X_overlap, y_overlap, ax,
                           f"C = {c_val}\nmargin={margin:.2f}, SVs={n_sv}")
    print(f"  C={c_val:>6}: margin={margin:.3f}, support_vectors={n_sv}")

plt.suptitle("C Parameter: Trading Off Margin Width vs Classification Errors",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "02_c_parameter_effect.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()
print()


# ============================================================
# 演示 3：为什么需要核函数——线性 SVM 的局限
# Demo 3: Why Kernels? — Limitations of Linear SVM
# ============================================================
print("=" * 60)
print("Demo 3: Why Kernels? Linear SVM Cannot Handle This")
print("=" * 60)

# 环形数据：线性不可分
# Circular data: not linearly separable
X_circles, y_circles = make_circles(n_samples=200, noise=0.1,
                                     factor=0.4, random_state=RANDOM_STATE)

# 月牙形数据：也不线性可分
# Moon-shaped data: also not linearly separable
X_moons, y_moons = make_moons(n_samples=200, noise=0.15,
                               random_state=RANDOM_STATE)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

datasets = [(X_circles, y_circles, "Circles"), (X_moons, y_moons, "Moons")]
for row, (X, y, name) in enumerate(datasets):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 线性核失败
    # Linear kernel fails
    clf_lin = SVC(kernel="linear", C=1.0)
    clf_lin.fit(X_scaled, y)
    plot_decision_boundary(clf_lin, X_scaled, y, axes[row, 0],
                           f"{name}: Linear Kernel (Fails!)", show_margin=False)

    # RBF 核成功
    # RBF kernel succeeds
    clf_rbf = SVC(kernel="rbf", C=1.0, gamma="scale")
    clf_rbf.fit(X_scaled, y)
    plot_decision_boundary(clf_rbf, X_scaled, y, axes[row, 1],
                           f"{name}: RBF Kernel (Works!)", show_margin=False)

    acc_lin = clf_lin.score(X_scaled, y)
    acc_rbf = clf_rbf.score(X_scaled, y)
    print(f"  {name}: Linear acc={acc_lin:.3f}, RBF acc={acc_rbf:.3f}")

plt.suptitle("Why Kernels? — Linear SVM Cannot Separate Non-Linear Data",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "03_why_kernels.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()
print()


# ============================================================
# 演示 4：核函数对比（Linear vs Polynomial vs RBF）
# Demo 4: Kernel Comparison (Linear vs Polynomial vs RBF)
# ============================================================
print("=" * 60)
print("Demo 4: Kernel Comparison on Moon Dataset")
print("=" * 60)

scaler = StandardScaler()
X_moons_scaled = scaler.fit_transform(X_moons)

kernels = [
    ("linear", {"C": 1.0}, "Linear Kernel"),
    ("poly", {"C": 1.0, "degree": 3, "gamma": "scale"}, "Polynomial (degree=3)"),
    ("rbf", {"C": 1.0, "gamma": "scale"}, "RBF (Gaussian)"),
    ("sigmoid", {"C": 1.0, "gamma": "scale"}, "Sigmoid"),
]

fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))
for ax, (kernel, params, title) in zip(axes, kernels):
    clf = SVC(kernel=kernel, **params)
    clf.fit(X_moons_scaled, y_moons)
    acc = clf.score(X_moons_scaled, y_moons)
    plot_decision_boundary(clf, X_moons_scaled, y_moons, ax,
                           f"{title}\nacc={acc:.3f}", show_margin=False)
    print(f"  {title}: accuracy={acc:.3f}, SVs={len(clf.support_vectors_)}")

plt.suptitle("Kernel Comparison: How Different Kernels Shape the Decision Boundary",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "04_kernel_comparison.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()
print()


# ============================================================
# 演示 5：Gamma 参数的影响（RBF 核）
# Demo 5: Effect of Gamma Parameter (RBF Kernel)
# ============================================================
print("=" * 60)
print("Demo 5: Effect of Gamma Parameter (RBF Kernel)")
print("=" * 60)

# gamma 越小决策边界越平滑（欠拟合风险），gamma 越大决策边界越复杂（过拟合风险）
# Smaller gamma = smoother boundary (underfitting risk)
# Larger gamma = more complex boundary (overfitting risk)
gamma_values = [0.1, 0.5, 1.0, 10.0]
fig, axes = plt.subplots(1, 4, figsize=(20, 4.5))

for ax, gamma_val in zip(axes, gamma_values):
    clf = SVC(kernel="rbf", C=1.0, gamma=gamma_val)
    clf.fit(X_moons_scaled, y_moons)
    acc = clf.score(X_moons_scaled, y_moons)
    plot_decision_boundary(clf, X_moons_scaled, y_moons, ax,
                           f"gamma={gamma_val}\nacc={acc:.3f}", show_margin=False)
    print(f"  gamma={gamma_val}: accuracy={acc:.3f}, SVs={len(clf.support_vectors_)}")

plt.suptitle("Gamma Parameter: From Underfitting (smooth) to Overfitting (wiggly)",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "05_gamma_effect.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()
print()


# ============================================================
# 演示 6：MMC → SVC → SVM 演进
# Demo 6: MMC → SVC → SVM Progression
# ============================================================
print("=" * 60)
print("Demo 6: MMC -> SVC -> SVM Progression")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# MMC: 硬间隔线性分类（仅适用于完美可分数据）
# MMC: Hard margin linear classification (only for perfectly separable data)
X_clean, y_clean = make_blobs(n_samples=80, centers=2,
                              random_state=RANDOM_STATE, cluster_std=0.8)
clf_mmc = SVC(kernel="linear", C=1e6)
clf_mmc.fit(X_clean, y_clean)
plot_decision_boundary(clf_mmc, X_clean, y_clean, axes[0],
                       "MMC\n(Hard Margin, Linear)")
axes[0].text(0.02, 0.02, "C → ∞: no misclassification allowed",
             transform=axes[0].transAxes, fontsize=9,
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))
print(f"  MMC: SVs={len(clf_mmc.support_vectors_)}")

# SVC: 软间隔线性分类（允许误分类）
# SVC: Soft margin linear classification (allows misclassification)
clf_svc = SVC(kernel="linear", C=1.0)
clf_svc.fit(X_overlap, y_overlap)
plot_decision_boundary(clf_svc, X_overlap, y_overlap, axes[1],
                       "SVC\n(Soft Margin, Linear)")
axes[1].text(0.02, 0.02, "C=1.0: allows some errors",
             transform=axes[1].transAxes, fontsize=9,
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))
print(f"  SVC: SVs={len(clf_svc.support_vectors_)}")

# SVM: 软间隔 + 核函数（处理非线性数据）
# SVM: Soft margin + kernel (handles non-linear data)
clf_svm = SVC(kernel="rbf", C=1.0, gamma="scale")
clf_svm.fit(X_moons_scaled, y_moons)
plot_decision_boundary(clf_svm, X_moons_scaled, y_moons, axes[2],
                       "SVM\n(Soft Margin, RBF Kernel)", show_margin=False)
axes[2].text(0.02, 0.02, "RBF kernel: non-linear boundary",
             transform=axes[2].transAxes, fontsize=9,
             bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))
print(f"  SVM: SVs={len(clf_svm.support_vectors_)}")

plt.suptitle("Evolution: MMC → SVC → SVM",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "06_mmc_svc_svm.png"),
            dpi=DPI, bbox_inches="tight")
plt.close()
print()

print("=" * 60)
print(f"All plots saved to: {OUTPUT_DIR}")
print("=" * 60)
