---
topic: knn
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn KNeighborsClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html"
  - "📖 Docs: scikit-learn KNeighborsRegressor — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html"
  - "💻 Source: sklearn/neighbors/_classification.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py"
  - "💻 Source: sklearn/neighbors/_base.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_base.py"
expiry: 6m
status: current
---

# KNN 代码参考

> 📖 Docs: [scikit-learn Neighbors User Guide](https://scikit-learn.org/stable/modules/neighbors.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# 加载数据 / Load dataset
X, y = load_iris(return_X_y=True)

# 归一化（KNN 必须！）/ Feature scaling (mandatory for KNN)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 创建并训练 KNN 分类器 / Create and fit KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_scaled, y)

# 预测 / Predict
print(knn.predict(scaler.transform([[5.1, 3.5, 1.4, 0.2]])))  # [0]
print(knn.predict_proba(scaler.transform([[5.1, 3.5, 1.4, 0.2]])))
```

**测试方法：** 运行后 `predict` 输出类别标签（0/1/2），`predict_proba` 输出概率向量，三值之和为 1.0

> 📖 Docs: [KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

---

## 完整实现示例

### 示例 1: 分类 + 超参数调优（GridSearchCV）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import numpy as np

# 加载二分类数据集 / Load binary classification dataset
X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# 2. 构建 Pipeline（归一化 + KNN）/ Build Pipeline
# ============================================================
# 用 Pipeline 防止数据泄露 / Use Pipeline to prevent data leakage
pipe = Pipeline([
    ('scaler', StandardScaler()),           # 归一化 / Standardization
    ('knn', KNeighborsClassifier()),        # K 近邻分类器 / KNN classifier
])

# ============================================================
# 3. 超参数搜索 / Hyperparameter Search
# ============================================================
param_grid = {
    'knn__n_neighbors': [3, 5, 7, 9, 11, 15, 21],   # k 候选值 / candidate k values
    'knn__weights': ['uniform', 'distance'],           # 权重策略 / weighting strategy
    'knn__metric': ['euclidean', 'manhattan'],         # 距离度量 / distance metric
}

grid_search = GridSearchCV(
    pipe,
    param_grid,
    cv=5,                   # 5 折交叉验证 / 5-fold cross-validation
    scoring='f1_weighted',  # 评估指标 / scoring metric
    n_jobs=-1,              # 并行加速 / parallel acceleration
    verbose=1,
)
grid_search.fit(X_train, y_train)

print(f"最优参数 / Best params: {grid_search.best_params_}")
print(f"CV 最优 F1 / Best CV F1: {grid_search.best_score_:.4f}")

# ============================================================
# 4. 测试评估 / Evaluation
# ============================================================
y_pred = grid_search.predict(X_test)
print("\n分类报告 / Classification Report:")
print(classification_report(y_test, y_pred,
                             target_names=['malignant', 'benign']))
```

> 📖 Docs: [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
> 💻 Source: [sklearn/neighbors/_classification.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py)

---

### 示例 2: KNN 回归（房价预测）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# 2. 归一化 + 模型训练 / Scaling + Training
# ============================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit on train only
X_test_scaled = scaler.transform(X_test)         # transform test with train stats

# 距离加权 KNN 回归 / Distance-weighted KNN regression
knn_reg = KNeighborsRegressor(
    n_neighbors=10,
    weights='distance',   # 距离加权：近邻影响更大 / closer neighbors have more influence
    algorithm='kd_tree',  # 低维数据用 KD-Tree / use KD-Tree for low-dim data
    metric='euclidean',
)
knn_reg.fit(X_train_scaled, y_train)

# ============================================================
# 3. 评估 / Evaluation
# ============================================================
y_pred = knn_reg.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"R²:   {r2:.4f}")

# 交叉验证 / Cross-validation
cv_scores = cross_val_score(knn_reg, X_train_scaled, y_train, cv=5, scoring='r2')
print(f"CV R² (mean±std): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

> 📖 Docs: [KNeighborsRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html)

---

### 示例 3: 可视化决策边界（2D）

```python
# ============================================================
# 决策边界可视化 / Decision boundary visualization
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler

# 生成非线性数据 / Generate non-linear dataset
X, y = make_moons(n_samples=300, noise=0.3, random_state=42)
X = StandardScaler().fit_transform(X)

# 画不同 k 的决策边界 / Plot decision boundaries for different k
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, k in zip(axes, [1, 5, 20]):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, y)

    # 生成网格 / Create mesh grid
    h = 0.05
    xx, yy = np.meshgrid(
        np.arange(X[:, 0].min() - 1, X[:, 0].max() + 1, h),
        np.arange(X[:, 1].min() - 1, X[:, 1].max() + 1, h)
    )
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.4)     # 决策区域 / decision regions
    ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', s=20)
    ax.set_title(f'k={k}')
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

plt.tight_layout()
plt.savefig('knn_decision_boundary.png', dpi=100)
plt.show()
```

> 💻 Source: [sklearn examples/neighbors](https://github.com/scikit-learn/scikit-learn/tree/main/examples/neighbors)

---

## API 速查

### KNeighborsClassifier

| 参数/方法 | 类型/签名 | 默认值 | 说明 |
|---------|----------|--------|------|
| `n_neighbors` | `int` | `5` | k 值，近邻数量 |
| `weights` | `'uniform'/'distance'/callable` | `'uniform'` | `'distance'` = 距离倒数加权 |
| `algorithm` | `'auto'/'kd_tree'/'ball_tree'/'brute'` | `'auto'` | 索引算法；auto 自动选 |
| `leaf_size` | `int` | `30` | KD-Tree/Ball-Tree 叶节点大小 |
| `metric` | `str/callable` | `'minkowski'` | 距离度量；p=2 时即欧氏 |
| `p` | `float` | `2` | Minkowski 距离的幂次 |
| `n_jobs` | `int/None` | `None` | 并行线程数；-1 = 全核 |
| ↳ `.fit(X, y)` | method | — | 存储训练数据 |
| ↳ `.predict(X)` | method | — | 返回类别标签 |
| ↳ `.predict_proba(X)` | method | — | 返回各类概率 |
| ↳ `.kneighbors(X, k)` | method | — | 返回 (距离, 下标) |
| ↳ `.score(X, y)` | method | — | 返回准确率 |

### KNeighborsRegressor

| 参数/方法 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `n_neighbors` | `int` | `5` | k 值 |
| `weights` | `str/callable` | `'uniform'` | 权重计算方式 |
| `algorithm` | `str` | `'auto'` | 索引算法 |
| ↳ `.predict(X)` | method | — | 返回连续预测值 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `sklearn.pipeline.Pipeline` | 推荐：Scaler + KNN 封装为一体，防数据泄露 |
| `GridSearchCV(pipe, param_grid, cv=5)` | 超参数网格搜索 |
| `StandardScaler()` | KNN 必须先归一化 |
| `knn.kneighbors(X)` | 返回 k 个近邻的距离和索引，用于调试 |

> 📖 Docs: [scikit-learn API Reference](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.neighbors)

---

## 目录结构模板

### 简单结构

```
knn_project/
├── data/
│   ├── train.csv
│   └── test.csv
├── knn_classifier.py     ← 核心脚本
└── requirements.txt
```

### 标准结构

```
knn_project/
├── data/
│   ├── raw/              ← 原始数据
│   └── processed/        ← 归一化后数据
├── notebooks/
│   ├── 01_eda.ipynb      ← 探索性分析
│   └── 02_knn_train.ipynb← 模型训练与可视化
├── src/
│   ├── preprocess.py     ← 特征缩放
│   ├── train.py          ← 训练 + GridSearchCV
│   └── evaluate.py       ← 评估 + 可视化
├── models/
│   └── knn_best.pkl      ← 保存最优模型
└── requirements.txt
```

> 💻 Source: [sklearn examples](https://github.com/scikit-learn/scikit-learn/tree/main/examples/neighbors)
