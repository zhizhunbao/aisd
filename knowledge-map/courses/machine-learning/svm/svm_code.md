---
topic: svm
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: sklearn SVM User Guide — https://scikit-learn.org/stable/modules/svm.html"
  - "💻 Source: sklearn svm/_classes.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/svm/_classes.py"
  - "💻 Source: sklearn examples/svm/ — https://github.com/scikit-learn/scikit-learn/tree/main/examples/svm"
  - "📖 Paper: Chang & Lin TIST 2011 (LIBSVM) — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/svm/chang_lin_2011_libsvm.pdf"
expiry: 6m
status: current
---

# SVM 代码参考

> 📖 Docs: [sklearn SVM 用户指南](https://scikit-learn.org/stable/modules/svm.html)
> 💻 Source: [sklearn examples/svm/](../../../.github/scikit-learn/examples/svm/)

---

## 快速开始

### 最简示例 — 60 秒上手分类

```python
# ============================================================
# SVM 最简分类示例 / Minimal SVM Classification Example
# ============================================================
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. 生成示例数据 / Generate sample data
X, y = make_classification(n_samples=200, n_features=2,
                            n_informative=2, n_redundant=0,
                            random_state=42)

# 2. 划分训练/测试集 / Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 3. 标准化（SVM 对尺度敏感，必须！）/ Scale features (critical for SVM)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # fit 在训练集上 / fit on train only
X_test  = scaler.transform(X_test)       # transform 测试集 / transform test

# 4. 训练 SVM / Train SVM
clf = SVC(kernel='rbf', C=1.0, gamma='scale')
clf.fit(X_train, y_train)

# 5. 预测与评估 / Predict and evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print(f"支持向量数 / n_support_vectors: {clf.support_vectors_.shape[0]}")
```

**测试方法：** 运行后 `classification_report` 输出各类精确率/召回率/F1；支持向量数通常是训练集的 10%~40%

> 📖 Docs: [sklearn SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)

---

## 完整实现示例

### 示例 1: C/γ 参数搜索 + 决策边界可视化（2D）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons
from sklearn.model_selection import GridSearchCV, train_test_split

# 月牙形数据（非线性，测试核 SVM）/ Moon-shaped data (non-linear)
X, y = make_moons(n_samples=300, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# ============================================================
# 2. 模型定义 + 参数搜索 / Model + Hyperparameter Search
# ============================================================
param_grid = {
    'C':     [0.1, 1, 10, 100],       # 正则化强度 / regularization
    'gamma': [0.01, 0.1, 1, 'scale'], # RBF 核宽度 / kernel bandwidth
}
grid = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5,
                    scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

best = grid.best_estimator_
print(f"最优参数 / Best params: {grid.best_params_}")
print(f"测试集准确率 / Test accuracy: {best.score(X_test, y_test):.3f}")

# ============================================================
# 3. 可视化决策边界 / Visualize Decision Boundary
# ============================================================
h = 0.02  # 网格步长 / grid step
x_min, x_max = X_train[:, 0].min() - 0.5, X_train[:, 0].max() + 0.5
y_min, y_max = X_train[:, 1].min() - 0.5, X_train[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

Z = best.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.4, cmap='RdBu')  # 决策区域 / decision regions
plt.scatter(X_train[:, 0], X_train[:, 1],
            c=y_train, cmap='RdBu', edgecolors='k', label='Train')
# 支持向量圈起来 / Mark support vectors
plt.scatter(best.support_vectors_[:, 0],
            best.support_vectors_[:, 1],
            s=100, facecolors='none', edgecolors='k', linewidths=2,
            label='Support Vectors')
plt.title(f"RBF SVM | C={grid.best_params_['C']}, γ={grid.best_params_['gamma']}")
plt.legend(); plt.tight_layout(); plt.show()

# ============================================================
# 4. 评估 / Evaluation
# ============================================================
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
print(classification_report(y_test, best.predict(X_test)))
ConfusionMatrixDisplay.from_estimator(best, X_test, y_test)
plt.show()
```

> 💻 Source: [sklearn plot_svm_margin.py](../../../.github/scikit-learn/examples/svm/plot_svm_margin.py)
> 📖 Docs: [sklearn GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)

---

### 示例 2: 多核对比（linear / poly / rbf / sigmoid）

```python
# ============================================================
# 1. 数据 / Data
# ============================================================
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = make_classification(n_samples=500, n_features=20,
                            n_informative=10, random_state=0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================================
# 2. 对比四种核 / Compare four kernels
# ============================================================
kernels = {
    'linear':  SVC(kernel='linear',  C=1.0),
    'poly d=3': SVC(kernel='poly',   C=1.0, degree=3, gamma='scale'),
    'rbf':     SVC(kernel='rbf',     C=1.0, gamma='scale'),
    'sigmoid': SVC(kernel='sigmoid', C=1.0, gamma='scale'),
}

print("核函数对比 / Kernel Comparison (5-fold CV):")
for name, clf in kernels.items():
    scores = cross_val_score(clf, X_scaled, y, cv=5, scoring='accuracy')
    print(f"  {name:12s}: {scores.mean():.3f} ± {scores.std():.3f}")
```

> 💻 Source: [sklearn plot_svm_kernels.py](../../../.github/scikit-learn/examples/svm/plot_svm_kernels.py)

---

### 示例 3: SVR — ε-不敏感回归

```python
# ============================================================
# 1. 数据 / Data
# ============================================================
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

np.random.seed(42)
X = np.sort(5 * np.random.rand(100, 1), axis=0)
y = np.sin(X).ravel() + 0.1 * np.random.randn(100)  # 带噪声的 sin

scaler_X = StandardScaler(); scaler_y = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1,1)).ravel()

# ============================================================
# 2. 模型 / Model
# ============================================================
svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
# epsilon: 忽略残差 < ε 的样本 / ignore residuals smaller than epsilon
svr_rbf.fit(X_scaled, y_scaled)

# ============================================================
# 3. 预测 / Predict
# ============================================================
y_pred_scaled = svr_rbf.predict(X_scaled)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1,1)).ravel()
print(f"MSE: {mean_squared_error(y, y_pred):.4f}")
print(f"支持向量数 / n_sv: {len(svr_rbf.support_)}")

# ============================================================
# 4. 可视化 / Visualization
# ============================================================
import matplotlib.pyplot as plt
X_plot = scaler_X.inverse_transform(X_scaled)
plt.scatter(X_plot, y, c='k', s=10, label='Data')
plt.plot(X_plot, y_pred, c='r', label='SVR (RBF)')
plt.legend(); plt.title("SVR with RBF Kernel"); plt.show()
```

> 💻 Source: [sklearn plot_svm_regression.py](../../../.github/scikit-learn/examples/svm/plot_svm_regression.py)
> 📖 Docs: [sklearn SVR](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html)

---

## API 速查

### 分类器

| 类/参数 | 默认值 | 说明 |
|---------|--------|------|
| `SVC(C, kernel, gamma, degree, coef0)` | — | 通用 SVM 分类器（libsvm） |
| ↳ `C` | `1.0` | 正则化参数，越大间隔越窄 |
| ↳ `kernel` | `'rbf'` | `'linear'/'poly'/'rbf'/'sigmoid'/'precomputed'` |
| ↳ `gamma` | `'scale'` | `'scale'`=1/(n\_feat·var); `'auto'`=1/n\_feat |
| ↳ `degree` | `3` | 仅 poly 核使用 |
| ↳ `probability` | `False` | True 时启用 Platt scaling（训练慢 5x）|
| ↳ `class_weight` | `None` | `'balanced'` 处理类不平衡 |
| `LinearSVC(C, max_iter)` | — | 线性核，liblinear 优化，大数据集用 |
| `NuSVC(nu)` | — | 用 $\nu$ 代替 C，$\nu$ ≈ 支持向量比例 |

### 回归器

| 类/参数 | 默认值 | 说明 |
|---------|--------|------|
| `SVR(C, kernel, gamma, epsilon)` | — | SVM 回归（ε-insensitive loss）|
| ↳ `epsilon` | `0.1` | 不惩罚区间宽度（残差 < ε 不计入损失）|
| `LinearSVR(C, epsilon)` | — | 线性 SVR，大数据集用 |

### 关键属性（训练后）

| 属性 | 说明 |
|------|------|
| `support_vectors_` | 支持向量特征矩阵，shape: (n_sv, n_features) |
| `support_` | 支持向量在训练集中的索引 |
| `dual_coef_` | $\alpha_i y_i$，shape: (n_class-1, n_sv) |
| `intercept_` | 偏置 $\beta_0$，shape: (n_class*(n_class-1)/2,) |
| `n_support_` | 每类的支持向量数 |
| `decision_function(X)` | 返回有符号距离 $f(x)$（非概率）|
| `predict_proba(X)` | 需 `probability=True`，Platt scaling |

> 📖 Docs: [sklearn SVC API](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)

### 常用工具

| 函数 | 说明 |
|------|------|
| `GridSearchCV(SVC(), param_grid, cv=5)` | C/γ 网格搜索 |
| `RandomizedSearchCV(SVC(), dist, n_iter=50)` | 随机搜索（更快）|
| `StandardScaler()` | **必须**在 SVC 前做标准化 |
| `make_pipeline(StandardScaler(), SVC())` | 防止数据泄露的 Pipeline |

> 📖 Docs: [sklearn GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)

---

## 目录结构模板

### 简单结构

```
svm_project/
├── train.py              ← 训练 + 参数搜索
├── predict.py            ← 加载模型推理
├── data/
│   ├── train.csv
│   └── test.csv
└── models/
    └── svm_best.pkl      ← joblib.dump 保存
```

### 标准结构

```
svm_project/
├── config.py             ← 参数配置（C, gamma, kernel）
├── preprocess.py         ← 数据加载 + StandardScaler
├── train.py              ← GridSearchCV + 训练
├── evaluate.py           ← 分类报告 + 混淆矩阵
├── predict.py            ← 加载 Pipeline 推理
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── pipeline.pkl      ← make_pipeline(scaler, svc)
└── requirements.txt      ← scikit-learn, joblib, numpy
```

> 📖 Docs: [sklearn Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
