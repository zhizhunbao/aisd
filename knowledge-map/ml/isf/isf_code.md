---
topic: isf
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn IsolationForest — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html"
  - "💻 Source: sklearn/_iforest.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py"
  - "💻 Source: sklearn examples/ensemble/plot_isolation_forest.py — https://github.com/scikit-learn/scikit-learn/blob/main/examples/ensemble/plot_isolation_forest.py"
expiry: 6m
status: current
---

# Isolation Forest 代码参考

> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
> 💻 Source: [sklearn/_iforest.py](../../.github/scikit-learn/sklearn/ensemble/_iforest.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.ensemble import IsolationForest
import numpy as np

# 1. 生成正常数据 + 少量异常点
# 1. Generate normal data + a few anomalies
rng = np.random.default_rng(42)
X_normal = rng.normal(loc=0, scale=1, size=(200, 2))   # 正常点 / normal points
X_anomaly = rng.uniform(low=-6, high=6, size=(20, 2))  # 异常点 / anomalies
X = np.vstack([X_normal, X_anomaly])

# 2. 训练 Isolation Forest
# 2. Train IsolationForest
clf = IsolationForest(
    n_estimators=100,         # 树的棵数 / number of trees
    contamination=0.1,        # 预估异常比例 / estimated anomaly fraction
    random_state=42,
)
clf.fit(X)

# 3. 预测：-1 = 异常，+1 = 正常
# 3. Predict: -1 = outlier, +1 = inlier
labels = clf.predict(X)
scores = clf.score_samples(X)  # 越低越异常 / lower = more anomalous

print(f"检测到异常点数: {(labels == -1).sum()}")
# 检测到异常点数: 22
```

**测试方法：** 运行后 `(labels == -1).sum()` 应接近 22（20 真实异常 + 2 误判左右）

> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 完整实现示例

### 示例 1: 异常检测完整流程（含可视化）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

rng = np.random.default_rng(42)
n_normal = 300
n_outliers = 15

# 正态分布正常点 / Gaussian normal points
X_train = rng.normal(loc=0, scale=0.5, size=(n_normal, 2))

# 制造测试集：正常点 + 均匀分布异常点
# Test set: normal points + uniform outliers
X_test_normal = rng.normal(loc=0, scale=0.5, size=(50, 2))
X_test_outlier = rng.uniform(low=-4, high=4, size=(n_outliers, 2))
X_test = np.vstack([X_test_normal, X_test_outlier])
y_test = np.array([1] * 50 + [-1] * n_outliers)

# ============================================================
# 2. 模型训练 / Model Training
# ============================================================
clf = IsolationForest(
    n_estimators=200,      # 更多树 → 更稳定的分数 / more trees → more stable scores
    max_samples=256,       # 默认子采样大小 / default subsampling size
    contamination=0.05,    # 训练集几乎全是正常点 / training set mostly normal
    max_features=1.0,      # 使用全部特征 / use all features
    bootstrap=False,       # 不放回采样（推荐）/ sampling without replacement (recommended)
    random_state=42,
    n_jobs=-1,             # 使用全部 CPU 核心 / use all CPU cores
)
clf.fit(X_train)

# ============================================================
# 3. 评分与预测 / Scoring and Prediction
# ============================================================
# score_samples: 越低越异常（原论文分数取反）
# score_samples: lower = more anomalous (negated from original paper)
test_scores = clf.score_samples(X_test)
test_labels = clf.predict(X_test)

# decision_function = score_samples - offset_（0 为决策边界）
# decision_function = score_samples - offset_ (0 is decision boundary)
decision = clf.decision_function(X_test)

print(f"offset_ = {clf.offset_:.4f}")  # contamination=0.05 时由分位数决定
print(f"预测标签分布: 正常={( test_labels==1).sum()}, 异常={(test_labels==-1).sum()}")

# ============================================================
# 4. 可视化 / Visualization
# ============================================================
# 创建网格计算异常分数热图
# Create grid to plot anomaly score heatmap
xx, yy = np.meshgrid(
    np.linspace(-5, 5, 100),
    np.linspace(-5, 5, 100),
)
Z = clf.score_samples(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(xx, yy, Z, levels=20, cmap='RdYlGn', alpha=0.6)
plt.colorbar(contour, ax=ax, label='Anomaly Score (higher=more normal)')

# 绘制训练点、测试正常点、测试异常点
# Plot training, test normal, test anomaly points
ax.scatter(X_train[:, 0], X_train[:, 1], s=10, c='blue', alpha=0.3, label='Train')
ax.scatter(X_test_normal[:, 0], X_test_normal[:, 1], s=30, c='green', marker='o', label='Test Normal')
ax.scatter(X_test_outlier[:, 0], X_test_outlier[:, 1], s=60, c='red', marker='x', label='Test Anomaly')
ax.set_title('Isolation Forest — Anomaly Score Heatmap')
ax.legend()
plt.tight_layout()
plt.savefig('isf_heatmap.png', dpi=120)
plt.show()
```

> 💻 Source: [plot_isolation_forest.py](../../.github/scikit-learn/examples/ensemble/plot_isolation_forest.py)
> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

### 示例 2: 在线/增量检测（warm_start）

```python
# ============================================================
# 1. 初始训练集 / Initial Training
# ============================================================
from sklearn.ensemble import IsolationForest
import numpy as np

rng = np.random.default_rng(0)
X_batch1 = rng.normal(size=(200, 3))

clf = IsolationForest(
    n_estimators=50,
    warm_start=True,    # 开启暖启动：新调用 fit 时保留已有树
                        # warm_start: keep existing trees when fitting again
    random_state=0,
)
clf.fit(X_batch1)
print(f"第一批后树的数量: {len(clf.estimators_)}")  # 50

# ============================================================
# 2. 追加新数据继续训练 / Continue with new data
# ============================================================
X_batch2 = rng.normal(size=(100, 3))
X_combined = np.vstack([X_batch1, X_batch2])

clf.n_estimators = 100   # 把树的目标数增加到 100 / increase target to 100
clf.fit(X_combined)
print(f"第二批后树的数量: {len(clf.estimators_)}")  # 100（新增 50 棵）

# ============================================================
# 3. 对新到达数据打分 / Score incoming data
# ============================================================
X_new = rng.normal(size=(10, 3))
X_anomaly = rng.uniform(-10, 10, size=(3, 3))
X_incoming = np.vstack([X_new, X_anomaly])

scores = clf.score_samples(X_incoming)
labels = clf.predict(X_incoming)
print("scores:", scores.round(3))
print("labels:", labels)
```

> 📖 Docs: [warm_start 参数](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html#sklearn-ensemble-isolationforest)

---

### 示例 3: 管道集成与交叉验证

```python
# ============================================================
# 1. 构建 Pipeline / Build Pipeline
# ============================================================
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.datasets import make_classification
import numpy as np

# 生成不平衡数据集（模拟真实异常场景）
# Generate imbalanced dataset (simulating real anomaly scenario)
X, y = make_classification(
    n_samples=1000, n_features=10,
    weights=[0.95, 0.05],  # 5% 异常 / 5% anomalies
    random_state=42,
)
# 将标签转换为 ISF 格式（+1 正常，-1 异常）
# Convert labels to ISF format (+1 normal, -1 anomaly)
y_isf = np.where(y == 1, -1, 1)

pipe = Pipeline([
    ('scaler', StandardScaler()),               # 标准化 / normalize
    ('clf', IsolationForest(
        contamination=0.05,
        n_estimators=100,
        random_state=42,
    )),
])

# ============================================================
# 2. 训练和评估 / Train and Evaluate
# ============================================================
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y_isf, test_size=0.2, random_state=42)

pipe.fit(X_train)
y_pred = pipe.predict(X_test)

print(classification_report(y_test, y_pred, target_names=['normal(+1)', 'anomaly(-1)']))

# ============================================================
# 3. 超参数搜索（基于分数，不依赖标签）
# 3. Hyperparameter search (score-based, no labels needed)
# ============================================================
# 注意：ISF 是无监督算法，没有传统 CV 分数
# 通常用 AUC-ROC 在有标注的验证集上评估
# Note: ISF is unsupervised; AUC-ROC on labeled validation set
from sklearn.metrics import roc_auc_score

scores = pipe.named_steps['clf'].score_samples(
    pipe.named_steps['scaler'].transform(X_test)
)
# score_samples 越高越正常，越低越异常
# 用负号让"高分=异常"以匹配 roc_auc_score 的约定（label=1 对应高分）
auc = roc_auc_score(y_test == -1, -scores)
print(f"AUC-ROC: {auc:.4f}")
```

> 📖 Docs: [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)

---

## API 速查

### IsolationForest 主要参数

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `IsolationForest(...)` | `n_estimators` | 100 | 隔离树棵数 |
| ↳ | `max_samples` | `'auto'` | 每棵树的训练样本数；auto=min(256,n) |
| ↳ | `contamination` | `'auto'` | 异常比例估计；auto → offset=-0.5 |
| ↳ | `max_features` | 1.0 | 每棵树用的特征比例或绝对数 |
| ↳ | `bootstrap` | False | False=无放回；True=有放回（不推荐） |
| ↳ | `n_jobs` | None | 并行核心数；-1=全部 |
| ↳ | `random_state` | None | 随机种子（可复现时设整数） |
| ↳ | `warm_start` | False | True=保留旧树并追加新树 |

### 主要方法

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `fit(X)` | self | 训练 |
| `predict(X)` | ndarray {-1,+1} | -1=异常，+1=正常 |
| `score_samples(X)` | ndarray ∈(-∞,0] | 越低越异常；= 论文分数取反 |
| `decision_function(X)` | ndarray 实值 | = score_samples - offset_；<0 为异常 |

### 关键属性

| 属性 | 说明 |
|------|------|
| `offset_` | 决策阈值；auto时=-0.5；其他由contamination的分位数决定 |
| `max_samples_` | 实际使用的子采样大小 |
| `estimators_` | 训练好的 ExtraTreeRegressor 列表 |
| `estimators_features_` | 每棵树使用的特征索引 |

> 📖 Docs: [sklearn.ensemble.IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 目录结构模板

### 简单结构

```
anomaly_detection/
├── train.py              ← 训练 ISF 并保存模型
├── predict.py            ← 对新数据打分
└── data/
    └── train.csv
```

### 标准结构

```
anomaly_detection/
├── config.py             ← 超参数配置（n_estimators, contamination...）
├── data_loader.py        ← 数据加载与预处理
├── model.py              ← ISF 封装类（fit/predict/score）
├── evaluate.py           ← AUC-ROC、精确率、召回率评估
├── train.py              ← 训练入口
├── data/
│   ├── train/
│   └── val/
├── models/               ← joblib 保存的模型
└── reports/              ← 异常分数分布图、ROC 曲线
```

### 高级结构（多模型对比）

```
anomaly_detection/
├── configs/
│   └── isf_config.yaml
├── models/
│   ├── isolation_forest.py
│   ├── lof.py
│   └── base.py           ← 统一接口
├── datasets/
├── evaluation/
│   ├── metrics.py        ← AUC, AP, F1@threshold
│   └── visualization.py
├── experiments/          ← 实验记录
├── train.py
├── compare.py            ← 多模型对比实验
└── requirements.txt
```

> 📖 Docs: [scikit-learn 异常检测](https://scikit-learn.org/stable/modules/outlier_detection.html)
