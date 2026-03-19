---
topic: sampling
dimension: code
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Docs: scikit-learn model_selection — https://scikit-learn.org/stable/modules/cross_validation.html"
  - "📖 Docs: imbalanced-learn — https://imbalanced-learn.org/stable/"
  - "📖 Docs: scikit-learn StratifiedKFold — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html"
expiry: 6m
status: current
---

# Sampling & Resampling 代码参考

> 📖 Docs: [scikit-learn model_selection](https://scikit-learn.org/stable/modules/cross_validation.html)
> 📖 Docs: [imbalanced-learn](https://imbalanced-learn.org/stable/)

## 快速开始

### 最简示例 — 30 秒上手 K-Fold CV

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

# 加载数据 / Load dataset
X, y = load_iris(return_X_y=True)

# 5-Fold 交叉验证 / 5-Fold cross-validation
scores = cross_val_score(DecisionTreeClassifier(), X, y, cv=5, scoring='accuracy')

# 输出结果 / Print results
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
# 预期输出 / Expected: CV Accuracy: 0.960 ± 0.022
```

**测试方法：** 复制粘贴直接运行，需要 `pip install scikit-learn`

---

## 完整实现示例

### 示例 1: K-Fold CV + 分层 + 多指标评估

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# 创建不平衡二分类数据 / Create imbalanced binary dataset
X, y = make_classification(
    n_samples=1000,         # 总样本数 / Total samples
    n_features=20,          # 特征数 / Number of features
    n_informative=10,       # 有用特征数 / Informative features
    weights=[0.9, 0.1],     # 类别比例 9:1 / Class ratio 9:1
    random_state=42
)
print(f"类别分布 / Class distribution: {np.bincount(y)}")

# ============================================================
# 2. 分层 K-Fold 交叉验证 / Stratified K-Fold CV
# ============================================================
# 分层确保每折保持 9:1 比例 / Stratified keeps 9:1 ratio in each fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 多指标评估 / Multi-metric evaluation
scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

results = cross_validate(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y,
    cv=skf,
    scoring=scoring,
    return_train_score=True  # 同时记录训练分数 / Also record train scores
)

# ============================================================
# 3. 结果展示 / Display Results
# ============================================================
for metric in scoring:
    train_key = f'train_{metric}'
    test_key = f'test_{metric}'
    print(f"{metric:>12}: "
          f"Train={results[train_key].mean():.3f}±{results[train_key].std():.3f}  "
          f"Test={results[test_key].mean():.3f}±{results[test_key].std():.3f}")
```

### 示例 2: Bootstrap 置信区间估计

```python
# ============================================================
# 1. Bootstrap 实现 / Bootstrap Implementation
# ============================================================
import numpy as np
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)

def bootstrap_ci(X, y, model, B=1000, alpha=0.05, random_state=42):
    """
    Bootstrap 置信区间估计 / Bootstrap confidence interval estimation
    Args:
        B: Bootstrap 重复次数 / Number of bootstrap replicates
        alpha: 显著性水平 / Significance level (0.05 → 95% CI)
    """
    rng = np.random.RandomState(random_state)
    n = len(X)
    scores = np.zeros(B)

    for b in range(B):
        # 有放回抽样 / Sample with replacement
        idx = rng.choice(n, size=n, replace=True)
        X_boot, y_boot = X[idx], y[idx]

        # OOB 样本做测试 / Use OOB samples as test
        oob_idx = np.array(list(set(range(n)) - set(idx)))
        if len(oob_idx) == 0:
            continue  # 极少发生 / Rarely happens

        model.fit(X_boot, y_boot)
        scores[b] = accuracy_score(y[oob_idx], model.predict(X[oob_idx]))

    # ============================================================
    # 2. 计算置信区间 / Compute Confidence Interval
    # ============================================================
    lower = np.percentile(scores, 100 * alpha / 2)
    upper = np.percentile(scores, 100 * (1 - alpha / 2))
    return scores.mean(), lower, upper

mean_acc, ci_low, ci_high = bootstrap_ci(
    X, y, DecisionTreeClassifier(random_state=42), B=1000
)
print(f"Bootstrap Accuracy: {mean_acc:.3f}")
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")
```

### 示例 3: SMOTE + Pipeline + CV

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline  # 注意用 imblearn 的 Pipeline！
import numpy as np

# 创建严重不平衡数据 / Create heavily imbalanced data
X, y = make_classification(
    n_samples=1000, n_features=20,
    weights=[0.95, 0.05],  # 95:5 不平衡 / 95:5 imbalance
    random_state=42
)
print(f"原始分布 / Original: {np.bincount(y)}")

# ============================================================
# 2. 构建 Pipeline / Build Pipeline
# ============================================================
# ⚠️ 关键：SMOTE 必须放在 Pipeline 内！
# ⚠️ KEY: SMOTE must be inside the Pipeline!
# 否则 CV 会在划分前就做 SMOTE → 数据泄露 / Otherwise CV leaks data
pipeline = Pipeline([
    ('smote', SMOTE(k_neighbors=5, random_state=42)),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
])

# ============================================================
# 3. 分层 CV 评估 / Stratified CV Evaluation
# ============================================================
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

results = cross_validate(pipeline, X, y, cv=skf, scoring=scoring)

# ============================================================
# 4. 对比：无 SMOTE / Comparison: Without SMOTE
# ============================================================
results_no_smote = cross_validate(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y, cv=skf, scoring=scoring
)

print("\n指标对比 / Metric Comparison:")
for metric in scoring:
    key = f'test_{metric}'
    print(f"{metric:>12}: "
          f"No SMOTE={results_no_smote[key].mean():.3f}  "
          f"SMOTE={results[key].mean():.3f}")
```

---

## API 速查

### 交叉验证 Cross-Validation

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `cross_val_score()` | `estimator` | — | 模型 / Model |
| ↳ | `cv` | 5 | 折数或 CV 对象 / Number of folds or CV object |
| ↳ | `scoring` | None | 评估指标 / Scoring metric |
| `cross_validate()` | `return_train_score` | False | 是否返回训练分数 / Return train scores |
| ↳ | `scoring` | None | 可传列表做多指标 / Can pass list for multi-metric |
| `StratifiedKFold()` | `n_splits` | 5 | 折数 / Number of splits |
| ↳ | `shuffle` | False | 是否打乱 / Shuffle before splitting |
| ↳ | `random_state` | None | 可复现的随机种子 / Reproducibility seed |
| `LeaveOneOut()` | — | — | LOOCV，等价于 K=N / LOOCV, equivalent to K=N |
| `TimeSeriesSplit()` | `n_splits` | 5 | 时间序列专用 / For time series data |
| ↳ | `max_train_size` | None | 限制训练集大小 / Cap training size |

### 不平衡采样 Imbalanced Sampling

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `SMOTE()` | `k_neighbors` | 5 | 插值用的近邻数 / K for interpolation |
| ↳ | `sampling_strategy` | 'auto' | 目标比例 / Target ratio |
| `BorderlineSMOTE()` | `kind` | 'borderline-1' | 只对边界少数类插值 / Borderline samples only |
| `ADASYN()` | `n_neighbors` | 5 | 自适应合成 / Adaptive synthesis |
| `RandomUnderSampler()` | `sampling_strategy` | 'auto' | 随机欠采样 / Random undersampling |
| `TomekLinks()` | — | — | 删除 Tomek link 对中的多数类 / Remove majority in Tomek links |
| `SMOTEENN()` | — | — | SMOTE + ENN 混合 / SMOTE + Edited Nearest Neighbors |
| `imblearn.pipeline.Pipeline` | — | — | ⚠️ 必须用 imblearn 的 Pipeline / Must use imblearn's Pipeline |

---

## 目录结构模板

### 简单结构

```
project/
├── evaluate.py           ← CV 评估脚本 / CV evaluation script
├── model.py              ← 模型定义 / Model definition
└── data/
    └── raw/              ← 原始数据 / Raw data
```

### 标准结构

```
project/
├── config.py             ← 超参数配置 / Hyperparameter config
├── dataset.py            ← 数据加载与预处理 / Data loading & preprocessing
├── model.py              ← 模型定义 / Model definition
├── train.py              ← 训练脚本 / Training script
├── evaluate.py           ← CV + Bootstrap 评估 / CV + Bootstrap evaluation
├── sampling.py           ← SMOTE 等采样逻辑 / Sampling logic (SMOTE etc.)
├── utils.py              ← 工具函数 / Utility functions
├── data/
│   ├── raw/              ← 原始数据 / Raw data
│   └── processed/        ← 预处理后数据 / Processed data
├── results/              ← 交叉验证结果 / CV results
└── logs/                 ← 日志 / Logs
```
