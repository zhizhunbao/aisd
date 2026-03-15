---
topic: lof
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn LocalOutlierFactor — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html"
  - "💻 Source: scikit-learn _lof.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_lof.py"
  - "💻 Source: sklearn plot_lof_outlier_detection.py — https://github.com/scikit-learn/scikit-learn/blob/main/examples/neighbors/plot_lof_outlier_detection.py"
expiry: 6m
status: current
---

# LOF 代码参考

> 📖 Docs: [scikit-learn LocalOutlierFactor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)
> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

# 构造一个含明显异常点的数据集  / Dataset with an obvious outlier
X = np.array([[-1.1], [0.2], [101.1], [0.3]])

# 创建模型，k=2 个邻居                / Create model with 2 neighbors
clf = LocalOutlierFactor(n_neighbors=2)

# fit_predict：-1 为异常，1 为正常   / fit_predict: -1 outlier, 1 inlier
labels = clf.fit_predict(X)           # array([ 1,  1, -1,  1])

# 查看原始 LOF 分数（负数，越小越异常）/ Raw LOF scores (more negative = more anomalous)
scores = clf.negative_outlier_factor_ # array([-0.98, -1.04, -73.37, -0.98])

print("Labels:", labels)
print("LOF scores (negative):", scores.round(2))
```

**测试方法：** 运行后 `labels[2]` 应为 `-1`（101.1 是异常）；`scores[2]` 应约为 `-73.37`。

> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 178-185`

---

## 完整实现示例

### 示例 1: 多密度簇异常检测（核心场景）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

np.random.seed(42)

# 密集簇（正常内点）     / Dense cluster (inliers)
X_inliers_dense  = 0.3 * np.random.randn(100, 2)
# 稀疏簇（也是正常内点）/ Sparse cluster (also inliers, different density)
X_inliers_sparse = 0.3 * np.random.randn(20, 2) + [5, 5]
# 真正的异常点          / True outliers
X_outliers       = np.random.uniform(low=-6, high=6, size=(20, 2))

X = np.concatenate([X_inliers_dense, X_inliers_sparse, X_outliers])

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
# n_neighbors=20：邻域大小；contamination=0.15：预期异常比例
# n_neighbors=20: neighborhood size; contamination=0.15: expected outlier rate
clf = LocalOutlierFactor(
    n_neighbors=20,
    contamination=0.15,   # 告知模型约 15% 为异常  / ~15% expected outliers
    algorithm='auto',     # 自动选择 kd-tree/ball-tree / Auto-select index
    metric='euclidean',   # 欧氏距离                  / Euclidean distance
)

# ============================================================
# 3. 训练与预测 / Training & Prediction
# ============================================================
# novelty=False (默认)：只能对训练集检测
# novelty=False (default): outlier detection on training set only
labels = clf.fit_predict(X)              # 1 = inlier, -1 = outlier
scores = clf.negative_outlier_factor_    # raw LOF scores (negative)

# ============================================================
# 4. 可视化 / Visualization
# ============================================================
# 圆圈半径代表异常程度（越大越异常）/ Circle radius = degree of anomaly
radius = (scores.max() - scores) / (scores.max() - scores.min())
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1],
            c=['red' if l == -1 else 'blue' for l in labels],
            s=10, label='Inlier/Outlier')
plt.scatter(X[:, 0], X[:, 1],
            s=1000 * radius,
            edgecolors='orange', facecolors='none',
            label='LOF score (circle size)')
plt.title("LOF Outlier Detection — Multi-density Clusters")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig("lof_detection.png", dpi=100)

print(f"Total outliers detected: {(labels == -1).sum()}")
print(f"Threshold (offset_): {clf.offset_:.3f}")
```

> 💻 Source: [plot_lof_outlier_detection.py](../../../.github/scikit-learn/examples/neighbors/plot_lof_outlier_detection.py)

---

### 示例 2: Novelty Detection（新数据预测）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

np.random.seed(0)
X_train = np.random.randn(100, 2)              # 正常训练数据 / Normal train data
X_test_normal  = np.random.randn(20, 2)        # 正常测试数据 / Normal test data
X_test_outlier = np.random.uniform(-6, 6, (5, 2))  # 异常测试数据 / Outlier test data

# ============================================================
# 2. 模型定义（novelty=True）/ Model with novelty=True
# ============================================================
# ⚠️ 关键：novelty=True 才能对新数据调用 predict/score_samples
# ⚠️ KEY: novelty=True is REQUIRED to call predict on new data
clf = LocalOutlierFactor(n_neighbors=20, novelty=True, contamination=0.1)
clf.fit(X_train)

# ============================================================
# 3. 对新数据预测 / Predict on new data
# ============================================================
print("Normal test:", clf.predict(X_test_normal))       # 大部分应为 1
print("Outlier test:", clf.predict(X_test_outlier))     # 大部分应为 -1

# score_samples 返回 -LOF（越大越正常）
# score_samples returns -LOF (higher = more normal)
scores = clf.score_samples(X_test_outlier)
print("Outlier scores:", scores.round(3))               # 应远小于 -1
```

> 💻 Source: [plot_lof_novelty_detection.py](../../../.github/scikit-learn/examples/neighbors/plot_lof_novelty_detection.py)

---

### 示例 3: 使用预计算距离矩阵（自定义距离）

```python
# ============================================================
# 1~2. 自定义距离 / Custom distance (e.g., cosine)
# ============================================================
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics.pairwise import cosine_distances

X = np.random.randn(50, 10)  # 高维数据 / High-dimensional data

# 预计算余弦距离矩阵    / Pre-compute cosine distance matrix
dist_matrix = cosine_distances(X)

# ============================================================
# 3. 使用预计算矩阵训练 / Train with precomputed matrix
# ============================================================
# metric='precomputed'：接受距离矩阵而非原始特征
# metric='precomputed': accepts distance matrix instead of raw features
clf = LocalOutlierFactor(
    n_neighbors=10,
    metric='precomputed',   # 关键参数 / Key parameter
    contamination=0.1,
)
labels = clf.fit_predict(dist_matrix)
print("Detected outliers:", (labels == -1).sum())
```

> 📖 Docs: [scikit-learn LOF metric parameter](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)

---

## API 速查

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `n_neighbors` | int | 20 | k 邻域大小（= 论文的 MinPts） |
| `algorithm` | str | `'auto'` | kNN 索引：`'auto'`/`'ball_tree'`/`'kd_tree'`/`'brute'` |
| `leaf_size` | int | 30 | BallTree/KDTree 的叶节点大小，影响速度和内存 |
| `metric` | str/callable | `'minkowski'` | 距离度量；p=2 时等于欧氏距离 |
| `p` | float | 2 | Minkowski 的 p 参数（p=1 Manhattan, p=2 Euclidean） |
| `contamination` | float/'auto' | `'auto'` | 预期异常比例；'auto' 时 offset=-1.5 |
| `novelty` | bool | False | True = 支持对新数据预测 |
| `n_jobs` | int | None | 并行 job 数，-1 用全部 CPU |

### 主要方法

| 方法 | novelty 要求 | 说明 |
|------|-------------|------|
| `fit(X)` | — | 训练模型，计算训练集 LOF 分数 |
| `fit_predict(X)` | `novelty=False` | 训练 + 对训练集预测（1/-1） |
| `predict(X)` | `novelty=True` | 对新数据预测标签（1/-1） |
| `decision_function(X)` | `novelty=True` | 返回 shifted -LOF；< 0 为异常 |
| `score_samples(X)` | `novelty=True` | 返回 -LOF；越小越异常 |
| `kneighbors(X, n_neighbors)` | — | 返回 kNN 距离和索引 |

### 主要属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `negative_outlier_factor_` | ndarray (n,) | 训练集每个点的 -LOF；接近 -1 为正常 |
| `offset_` | float | 判定阈值；< offset 则为异常 |
| `n_neighbors_` | int | 实际使用的邻居数（可能 < n_neighbors） |
| `n_samples_fit_` | int | 训练集样本数 |

> 📖 Docs: [scikit-learn LocalOutlierFactor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)

---

## 目录结构模板

### 简单结构

```
lof_project/
├── detect.py           ← 异常检测主脚本
├── data/
│   └── train.csv       ← 训练数据
└── outputs/
    └── lof_scores.csv  ← 输出分数
```

### 标准结构

```
lof_project/
├── config.py           ← n_neighbors, contamination 等参数配置
├── data_loader.py      ← 数据加载与预处理
├── lof_detector.py     ← LocalOutlierFactor 封装
├── evaluate.py         ← 精确率/召回率评估（有标签时）
├── visualize.py        ← LOF 分数可视化
├── data/
│   ├── train.csv
│   └── test.csv
├── outputs/
│   ├── lof_scores.csv
│   └── lof_plot.png
└── requirements.txt    ← scikit-learn>=1.0, numpy, matplotlib
```

> 💻 Source: [sklearn/plot_lof_outlier_detection.py](../../../.github/scikit-learn/examples/neighbors/plot_lof_outlier_detection.py)
