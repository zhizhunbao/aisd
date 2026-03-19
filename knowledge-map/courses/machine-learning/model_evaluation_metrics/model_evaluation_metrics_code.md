---
topic: model_evaluation_metrics
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: scikit-learn Model Evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html"
  - "📖 Docs: scikit-learn Cross-Validation — https://scikit-learn.org/stable/modules/cross_validation.html"
  - "💻 Source: scikit-learn/sklearn/metrics/ — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/"
expiry: 6m
status: current
---

# Model Evaluation & Metrics 代码参考

> 📖 Docs: [scikit-learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
X, y = load_iris(return_X_y=True)        # 加载数据 / Load data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)   # 按类别比例分层划分 / Stratified split

# ============================================================
# 2. 训练 + 评估 / Train + Evaluate
# ============================================================
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)                # 训练 / Train
y_pred = clf.predict(X_test)             # 预测 / Predict

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(classification_report(y_test, y_pred))

# ============================================================
# 3. 交叉验证 / Cross-Validation
# ============================================================
scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
print(f"5-Fold CV: {scores.mean():.4f} ± {scores.std():.4f}")
```

**测试方法：** 直接复制运行，无需额外安装（sklearn 自带 iris 数据集）

---

## 完整实现示例

### 示例 1: 二分类完整评估 — 混淆矩阵 + ROC + PR

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    classification_report,
    roc_curve, auc, RocCurveDisplay,
    precision_recall_curve, PrecisionRecallDisplay,
    f1_score, matthews_corrcoef
)

# ============================================================
# 1. 生成不平衡数据 / Generate imbalanced dataset
# ============================================================
X, y = make_classification(
    n_samples=1000,       # 样本数 / Number of samples
    n_features=20,        # 特征数 / Number of features
    weights=[0.9, 0.1],   # 类别比例 9:1 / Class ratio
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ============================================================
# 2. 训练模型 / Train model
# ============================================================
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)             # 硬标签 / Hard labels
y_proba = model.predict_proba(X_test)[:, 1]  # 正类概率 / Positive class probability

# ============================================================
# 3. 分类指标 / Classification Metrics
# ============================================================
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))
print(f"MCC: {matthews_corrcoef(y_test, y_pred):.4f}")

# ============================================================
# 4. 混淆矩阵可视化 / Confusion Matrix Visualization
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 4a. 混淆矩阵 / Confusion Matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=axes[0])
axes[0].set_title("Confusion Matrix")

# 4b. ROC 曲线 / ROC Curve
RocCurveDisplay.from_predictions(y_test, y_proba, ax=axes[1])
axes[1].set_title("ROC Curve")

# 4c. PR 曲线 / Precision-Recall Curve
PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=axes[2])
axes[2].set_title("Precision-Recall Curve")

plt.tight_layout()
plt.savefig("evaluation_plots.png", dpi=150)
plt.show()
```

### 示例 2: 交叉验证对比多个模型

```python
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification
import pandas as pd

# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
X, y = make_classification(
    n_samples=500, n_features=10, weights=[0.7, 0.3], random_state=42
)

# ============================================================
# 2. 定义模型和评估指标 / Define models and scoring
# ============================================================
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree":       DecisionTreeClassifier(max_depth=5),
    "Random Forest":       RandomForestClassifier(n_estimators=100),
    "SVM (RBF)":           SVC(kernel="rbf", probability=True),
}

scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

# ============================================================
# 3. 分层 5-Fold 交叉验证 / Stratified 5-Fold CV
# ============================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}
for name, model in models.items():
    cv_results = cross_validate(
        model, X, y, cv=cv, scoring=scoring, return_train_score=False
    )
    results[name] = {
        metric: f"{cv_results[f'test_{metric}'].mean():.4f} ± {cv_results[f'test_{metric}'].std():.4f}"
        for metric in scoring
    }

# ============================================================
# 4. 对比表格 / Comparison Table
# ============================================================
df = pd.DataFrame(results).T
print(df.to_string())
```

### 示例 3: 学习曲线诊断

```python
from sklearn.model_selection import learning_curve
from sklearn.svm import SVC
from sklearn.datasets import load_digits
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. 数据 + 模型 / Data + Model
# ============================================================
X, y = load_digits(return_X_y=True)
model = SVC(kernel="rbf", gamma=0.001)

# ============================================================
# 2. 计算学习曲线 / Compute learning curve
# ============================================================
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),  # 训练集比例 / Training set fractions
    cv=5,                                      # 5-fold CV
    scoring="accuracy",
    n_jobs=-1                                  # 并行 / Parallel
)

# ============================================================
# 3. 可视化 / Visualization
# ============================================================
train_mean = train_scores.mean(axis=1)  # 训练均值 / Train mean
train_std  = train_scores.std(axis=1)
val_mean   = val_scores.mean(axis=1)    # 验证均值 / Validation mean
val_std    = val_scores.std(axis=1)

plt.figure(figsize=(10, 6))
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color="blue")
plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color="orange")
plt.plot(train_sizes, train_mean, "o-", color="blue", label="Training Score")
plt.plot(train_sizes, val_mean, "o-", color="orange", label="Validation Score")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy")
plt.title("Learning Curve — SVM (RBF)")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("learning_curve.png", dpi=150)
plt.show()
```

---

## API 速查

### sklearn.metrics — 分类指标

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `accuracy_score()` | `y_true, y_pred` | — | 准确率 (TP+TN)/All |
| `precision_score()` | `y_true, y_pred` | — | 精确率 TP/(TP+FP) |
| ↳ `average` | str | `'binary'` | 多分类策略: 'micro'/'macro'/'weighted' |
| ↳ `zero_division` | int/str | `'warn'` | 分母为 0 时返回值 |
| `recall_score()` | `y_true, y_pred` | — | 召回率 TP/(TP+FN) |
| `f1_score()` | `y_true, y_pred` | — | F1 = 2PR/(P+R) |
| ↳ `average` | str | `'binary'` | 同 precision_score |
| `matthews_corrcoef()` | `y_true, y_pred` | — | MCC ∈ [-1, +1] |
| `confusion_matrix()` | `y_true, y_pred` | — | 返回 2×2 (或 n×n) 矩阵 |
| `classification_report()` | `y_true, y_pred` | — | 综合报告 (P/R/F1 per class) |
| `roc_curve()` | `y_true, y_score` | — | 返回 (fpr, tpr, thresholds) |
| `roc_auc_score()` | `y_true, y_score` | — | ROC-AUC 值 |
| `precision_recall_curve()` | `y_true, probas_pred` | — | 返回 (precision, recall, thresholds) |
| `average_precision_score()` | `y_true, y_score` | — | PR-AUC (平均精确率) |
| `brier_score_loss()` | `y_true, y_prob` | — | Brier 分数 (校准度) |

### sklearn.metrics — 回归指标

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `mean_squared_error()` | `y_true, y_pred` | — | MSE |
| ↳ `squared` | bool | `True` | 设为 False 返回 RMSE |
| `mean_absolute_error()` | `y_true, y_pred` | — | MAE |
| `r2_score()` | `y_true, y_pred` | — | R² 决定系数 |

### sklearn.model_selection — 交叉验证

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `cross_val_score()` | `estimator, X, y` | — | 返回 K 个分数的数组 |
| ↳ `cv` | int/splitter | `5` | 折数或自定义 splitter |
| ↳ `scoring` | str | `None` | 评分指标名 (如 'f1') |
| `cross_validate()` | `estimator, X, y` | — | 多指标版，返回 dict |
| ↳ `scoring` | list[str] | — | 可传多个指标名 |
| `StratifiedKFold()` | — | — | 分层 K 折（保持类别比例）|
| ↳ `n_splits` | int | `5` | 折数 |
| ↳ `shuffle` | bool | `False` | 是否打乱 |
| `learning_curve()` | `estimator, X, y` | — | 学习曲线数据 |
| ↳ `train_sizes` | array | `np.linspace(0.1,1,5)` | 训练集大小序列 |

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练 + 基本评估
├── data/
│   ├── train.csv
│   └── test.csv
└── results/
    └── metrics.txt
```

### 标准结构

```
project/
├── config.py             ← 超参数配置
├── dataset.py            ← 数据加载
├── model.py              ← 模型定义
├── train.py              ← 训练 + CV
├── evaluate.py           ← 评估脚本
├── visualize.py          ← 可视化 (ROC/PR/学习曲线)
├── data/
├── checkpoints/
├── results/
│   ├── figures/          ← 评估图
│   └── metrics.json      ← 评估指标
└── logs/
```
