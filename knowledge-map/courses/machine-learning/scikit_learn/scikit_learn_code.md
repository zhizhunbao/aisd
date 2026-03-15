---
topic: scikit_learn
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn API — https://scikit-learn.org/stable/modules/classes.html"
  - "📖 Docs: scikit-learn Examples — https://scikit-learn.org/stable/auto_examples/index.html"
  - "💻 Source: scikit-learn/sklearn — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn"
expiry: 3m
status: current
---

# Scikit-Learn 代码参考

> 📖 Docs: [sklearn API Reference](https://scikit-learn.org/stable/modules/classes.html)
> 📖 Docs: [sklearn Examples](https://scikit-learn.org/stable/auto_examples/index.html)


## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ============================================================
# 1. 加载数据 / Load Data
# ============================================================
X, y = load_iris(return_X_y=True)                  # 鸢尾花数据集 / Iris dataset

# ============================================================
# 2. 拆分数据 / Split Data
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42           # 80/20 拆分 / 80/20 split
)

# ============================================================
# 3. 训练 + 预测 / Train + Predict
# ============================================================
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)                           # 训练 / Fit
y_pred = clf.predict(X_test)                        # 预测 / Predict

# ============================================================
# 4. 评估 / Evaluate
# ============================================================
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")  # ≈ 1.0
```

**测试方法：** 运行后 accuracy ≈ 1.0（鸢尾花对 RF 很简单）

> 📖 Docs: [sklearn Getting Started](https://scikit-learn.org/stable/getting_started.html)

---

## 完整实现示例

### 示例 1: 完整 ML 工作流 (Pipeline + GridSearchCV)

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# ============================================================
# 1. 加载数据 / Load Data
# ============================================================
X, y = load_breast_cancer(return_X_y=True)         # 乳腺癌二分类 / Breast cancer
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y  # 分层抽样 / Stratified
)

# ============================================================
# 2. 构建 Pipeline / Build Pipeline
# ============================================================
pipe = Pipeline([
    ('scaler', StandardScaler()),                   # 标准化 / Standardization
    ('svc', SVC(probability=True))                  # SVM 分类器 / SVM classifier
])

# ============================================================
# 3. 超参数搜索 / Hyperparameter Search
# ============================================================
param_grid = {
    'svc__C': [0.1, 1, 10, 100],                   # 正则化 / Regularization
    'svc__kernel': ['rbf', 'linear'],               # 核函数 / Kernel
    'svc__gamma': ['scale', 'auto']                 # RBF gamma
}

grid = GridSearchCV(
    pipe, param_grid,
    cv=5,                                           # 5 折交叉验证 / 5-fold CV
    scoring='f1',                                   # F1 分数 / F1 score
    n_jobs=-1,                                      # 并行 / Parallel
    verbose=1
)
grid.fit(X_train, y_train)

# ============================================================
# 4. 结果 / Results
# ============================================================
print(f"最优参数: {grid.best_params_}")
print(f"最优 F1 (CV): {grid.best_score_:.4f}")
print(f"\n测试集报告:")
y_pred = grid.predict(X_test)
print(classification_report(y_test, y_pred))
```

> 📖 Docs: [sklearn Pipeline](https://scikit-learn.org/stable/modules/compose.html)
> 📖 Docs: [sklearn GridSearchCV](https://scikit-learn.org/stable/modules/grid_search.html)

---

### 示例 2: ColumnTransformer 处理混合特征

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# ============================================================
# 1. 构造混合数据 / Create Mixed-type Data
# ============================================================
df = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 50, 55, 60],         # 数值 / Numeric
    'salary': [30, 50, 60, 80, 90, 100, 110, 120],    # 数值 / Numeric
    'department': ['A','B','A','B','A','B','A','B'],   # 类别 / Categorical
    'city': ['NY','SF','NY','SF','LA','SF','NY','LA']  # 类别 / Categorical
})
y = [0, 1, 0, 1, 0, 1, 0, 1]

# ============================================================
# 2. ColumnTransformer 分别处理 / Process Separately
# ============================================================
num_features = ['age', 'salary']                      # 数值列 / Numeric columns
cat_features = ['department', 'city']                  # 类别列 / Categorical columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),       # 数值→标准化 / Numeric→Scale
        ('cat', OneHotEncoder(drop='first'), cat_features)  # 类别→独热 / Cat→OHE
    ]
)

# ============================================================
# 3. 完整 Pipeline / Full Pipeline
# ============================================================
pipe = Pipeline([
    ('prep', preprocessor),                            # 预处理 / Preprocessing
    ('clf', GradientBoostingClassifier(n_estimators=50))  # 模型 / Model
])

scores = cross_val_score(pipe, df, y, cv=3)
print(f"CV scores: {scores}")
```

> 📖 Docs: [sklearn ColumnTransformer](https://scikit-learn.org/stable/modules/compose.html#columntransformer)

---

### 示例 3: 无监督学习 (KMeans + PCA 可视化)

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# ============================================================
# 1. 生成数据 / Generate Data
# ============================================================
X, y_true = make_blobs(n_samples=300, centers=4, random_state=42)

# ============================================================
# 2. KMeans 聚类 / KMeans Clustering
# ============================================================
kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
y_pred = kmeans.fit_predict(X)                            # 训练+预测 / Fit+Predict
print(f"Silhouette Score: {silhouette_score(X, y_pred):.3f}")  # 轮廓系数

# ============================================================
# 3. PCA 降维可视化 / PCA Visualization
# ============================================================
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(X_2d[:, 0], X_2d[:, 1], c=y_true, cmap='Set1', s=20)
axes[0].set_title('真实标签 / True Labels')
axes[1].scatter(X_2d[:, 0], X_2d[:, 1], c=y_pred, cmap='Set1', s=20)
axes[1].scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
                c='red', marker='X', s=200, label='中心')
axes[1].set_title('KMeans 聚类 / KMeans Clustering')
axes[1].legend()
plt.tight_layout()
plt.savefig('kmeans_pca.png', dpi=150)
plt.show()
```

> 📖 Docs: [sklearn KMeans](https://scikit-learn.org/stable/modules/clustering.html#k-means)
> 📖 Docs: [sklearn PCA](https://scikit-learn.org/stable/modules/decomposition.html#pca)

---

## API 速查

### 数据准备

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `train_test_split(X, y)` | `test_size, random_state, stratify` | 拆分数据 |
| `StandardScaler()` | — | 零均值单位方差标准化 |
| `MinMaxScaler()` | `feature_range` | 缩放到 [0, 1] |
| `OneHotEncoder()` | `drop, sparse_output` | 类别→独热编码 |
| `LabelEncoder()` | — | 标签→整数 |
| `SimpleImputer()` | `strategy='mean/median/most_frequent'` | 填充缺失值 |

### 监督学习

| 类 | 关键参数 | 任务 |
|----|---------|------|
| `LinearRegression()` | — | 回归 |
| `Ridge(alpha=)` | `alpha` | 回归 (L2) |
| `Lasso(alpha=)` | `alpha` | 回归 (L1) |
| `LogisticRegression(C=)` | `C, penalty, solver` | 分类 |
| `SVC(C=, kernel=)` | `C, kernel, gamma` | 分类 |
| `KNeighborsClassifier(n_neighbors=)` | `n_neighbors, weights` | 分类 |
| `DecisionTreeClassifier()` | `max_depth, min_samples_split` | 分类 |
| `RandomForestClassifier()` | `n_estimators, max_depth` | 分类 |
| `GradientBoostingClassifier()` | `n_estimators, learning_rate` | 分类 |
| `GaussianNB()` | — | 分类 |

### 无监督学习

| 类 | 关键参数 | 任务 |
|----|---------|------|
| `KMeans(n_clusters=)` | `n_clusters, n_init` | 聚类 |
| `DBSCAN(eps=, min_samples=)` | `eps, min_samples` | 聚类（密度） |
| `PCA(n_components=)` | `n_components` | 降维 |
| `TSNE(n_components=)` | `n_components, perplexity` | 降维（可视化） |

### 模型选择

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `cross_val_score(model, X, y)` | `cv, scoring` | 交叉验证得分 |
| `GridSearchCV(model, params)` | `param_grid, cv, scoring` | 网格搜索 |
| `RandomizedSearchCV()` | `param_distributions, n_iter` | 随机搜索 |

### 评估指标

| 函数 | 任务 | 说明 |
|------|------|------|
| `accuracy_score(y, y_pred)` | 分类 | 准确率 |
| `f1_score(y, y_pred)` | 分类 | F1 分数 |
| `roc_auc_score(y, y_proba)` | 分类 | ROC AUC |
| `confusion_matrix(y, y_pred)` | 分类 | 混淆矩阵 |
| `classification_report(y, y_pred)` | 分类 | 综合报告 |
| `mean_squared_error(y, y_pred)` | 回归 | MSE |
| `r2_score(y, y_pred)` | 回归 | R² |
| `silhouette_score(X, labels)` | 聚类 | 轮廓系数 |

> 📖 Docs: [sklearn API Reference](https://scikit-learn.org/stable/modules/classes.html)

---

## 目录结构模板

### 简单结构

```
ml_project/
├── data/
│   └── dataset.csv
├── train.py              ← Pipeline + GridSearch + 评估
└── requirements.txt
```

### 标准结构

```
ml_project/
├── data/
│   ├── raw/              ← 原始数据
│   └── processed/        ← 预处理后数据
├── src/
│   ├── data_loader.py    ← 数据加载
│   ├── features.py       ← ColumnTransformer 定义
│   ├── model.py          ← Pipeline 构建
│   ├── train.py          ← 训练+调参
│   └── evaluate.py       ← 评估+报告
├── models/
│   └── best_model.pkl    ← joblib.dump 保存的模型
├── notebooks/
│   └── EDA.ipynb         ← 数据探索
├── tests/
│   └── test_pipeline.py
└── requirements.txt
```

> 📖 Docs: [sklearn Persistence](https://scikit-learn.org/stable/model_persistence.html)
