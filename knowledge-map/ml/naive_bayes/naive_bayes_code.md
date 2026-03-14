---
topic: naive_bayes
dimension: code
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn Naive Bayes — https://scikit-learn.org/stable/modules/naive_bayes.html"
  - "💻 Source: scikit-learn/sklearn/naive_bayes.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/naive_bayes.py"
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv:1410.5329 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
expiry: 6m
status: current
---

# Naive Bayes 代码参考

> 📖 Docs: [scikit-learn Naive Bayes User Guide](https://scikit-learn.org/stable/modules/naive_bayes.html)
> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py)


## 快速开始

### 最简示例 — 30 秒上手

```python
from sklearn.naive_bayes import GaussianNB  # 导入高斯朴素贝叶斯 / Import Gaussian NB
from sklearn.datasets import load_iris       # 鸢尾花数据集 / Iris dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. 加载数据 / Load data
X, y = load_iris(return_X_y=True)

# 2. 划分训练/测试集 / Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 训练模型 (极快，O(nd)) / Train — extremely fast
clf = GaussianNB()
clf.fit(X_train, y_train)

# 4. 预测 / Predict
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")  # 通常 ~0.97

# 5. 输出概率 / Probability estimates
proba = clf.predict_proba(X_test[:3])
print(f"Probabilities:\n{proba}")
```

**测试方法：** 直接运行，accuracy 应在 0.95 以上为正常。

> 📖 Docs: [scikit-learn GaussianNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html)

---

## 完整实现示例

### 示例 1: MultinomialNB 文本分类（垃圾邮件）

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# 只用两个类别做二分类演示 / Use 2 categories for binary demo
categories = ['sci.space', 'talk.religion.misc']
train = fetch_20newsgroups(subset='train', categories=categories)
test  = fetch_20newsgroups(subset='test',  categories=categories)

# ============================================================
# 2. 特征提取 Pipeline / Feature Extraction Pipeline
# ============================================================
# Pipeline: 文本 → 词频矩阵 → TF-IDF → MultinomialNB
# Pipeline: text → count matrix → TF-IDF → MultinomialNB
text_clf = Pipeline([
    ('vect', CountVectorizer()),           # 词袋模型 / Bag of words
    ('tfidf', TfidfTransformer()),         # TF-IDF 权重 / TF-IDF weighting
    ('clf', MultinomialNB(alpha=0.1)),     # NB 分类器，alpha=平滑系数 / smoothing
])

# ============================================================
# 3. 训练 / Training
# ============================================================
text_clf.fit(train.data, train.target)

# ============================================================
# 4. 评估 / Evaluation
# ============================================================
y_pred = text_clf.predict(test.data)
print(classification_report(test.target, y_pred,
                             target_names=test.target_names))
```

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.3
> 📖 Docs: [scikit-learn Text Feature Extraction](https://scikit-learn.org/stable/modules/feature_extraction.html)

---

### 示例 2: GaussianNB 增量在线学习（partial_fit）

```python
# ============================================================
# 1. 模拟流式数据 / Simulate streaming data
# ============================================================
import numpy as np
from sklearn.naive_bayes import GaussianNB

# 生成数据 / Generate data
rng = np.random.RandomState(42)
X = rng.randn(1000, 4)            # 1000 样本，4 特征 / 1000 samples, 4 features
y = (X[:, 0] + X[:, 1] > 0).astype(int)  # 简单线性规则 / simple linear rule

# ============================================================
# 2. 增量训练(模拟每批 100 条) / Incremental fit (100 per batch)
# ============================================================
clf = GaussianNB()
classes = np.array([0, 1])

BATCH_SIZE = 100
for i in range(0, 800, BATCH_SIZE):
    # partial_fit 无需重读历史数据，仅更新充分统计量
    # partial_fit only updates sufficient statistics, no re-reading history
    clf.partial_fit(X[i:i+BATCH_SIZE], y[i:i+BATCH_SIZE],
                    classes=classes)  # 第一次调用时需传 classes / required on 1st call

# ============================================================
# 3. 评估 (最后 200 条作为测试集) / Evaluate
# ============================================================
from sklearn.metrics import accuracy_score
y_pred = clf.predict(X[800:])
print(f"Online learning accuracy: {accuracy_score(y[800:], y_pred):.3f}")
print(f"Class priors learned: {clf.class_prior_}")  # 先验 / class priors
```

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `partial_fit()` L362-L405

---

### 示例 3: BernoulliNB + 交叉验证 + 概率校准

```python
# ============================================================
# 1. BernoulliNB 适合二值特征 / BernoulliNB for binary features
# ============================================================
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.calibration import CalibratedClassifierCV  # 概率校准 / probability calibration
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification

# 生成二值特征数据 / Generate binary feature data
X, y = make_classification(n_samples=500, n_features=20,
                            n_informative=10, random_state=42)
X_binary = (X > 0).astype(int)  # 二值化 / binarize

# ============================================================
# 2. 基础 BernoulliNB / Base BernoulliNB
# ============================================================
bnb = BernoulliNB(alpha=1.0)  # alpha=1 即 Laplace 平滑 / Laplace smoothing

# 5 折交叉验证 / 5-fold cross validation
scores = cross_val_score(bnb, X_binary, y, cv=5, scoring='accuracy')
print(f"BernoulliNB CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

# ============================================================
# 3. 概率校准(NB 输出概率通常过于极端)
# Probability calibration (NB tends to output overconfident probs)
# ============================================================
calibrated = CalibratedClassifierCV(bnb, method='isotonic', cv=5)
calibrated.fit(X_binary, y)

# 对比未校准 vs 校准后的概率分布
raw_proba = bnb.fit(X_binary, y).predict_proba(X_binary[:5])
cal_proba  = calibrated.predict_proba(X_binary[:5])
print(f"原始概率 / Raw probabilities:\n{raw_proba}")
print(f"校准概率 / Calibrated probabilities:\n{cal_proba}")
```

> 📖 Docs: [scikit-learn Calibration](https://scikit-learn.org/stable/modules/calibration.html)
> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `BernoulliNB` class

---

## API 速查

### 分类器类

| 函数/类 | 主要参数 | 默认值 | 说明 |
|---------|---------|--------|------|
| `GaussianNB()` | `priors` | `None` | 高斯朴素贝叶斯（连续特征） |
| ↳ | `var_smoothing` | `1e-9` | 方差下限（防止数值问题） |
| `MultinomialNB()` | `alpha` | `1.0` | Laplace/Lidstone 平滑系数 |
| ↳ | `fit_prior` | `True` | 是否从数据估计先验 |
| ↳ | `class_prior` | `None` | 手动指定先验概率 |
| `BernoulliNB()` | `alpha` | `1.0` | 平滑系数 |
| ↳ | `binarize` | `0.0` | 二值化阈值，None 表示已是二值 |
| `CategoricalNB()` | `alpha` | `1.0` | 平滑系数 |
| `ComplementNB()` | `alpha` | `1.0` | 针对不平衡文本的改进版 |
| ↳ | `norm` | `False` | 是否对权重归一化 |

### 公共方法

| 方法 | 参数 | 说明 |
|------|------|------|
| `fit(X, y)` | X: 特征矩阵, y: 标签 | 训练模型 |
| `partial_fit(X, y, classes)` | classes: 首次调用必传 | 增量训练（流式数据） |
| `predict(X)` | X: 测试特征矩阵 | 返回预测类别 |
| `predict_proba(X)` | X: 测试特征矩阵 | 返回归一化后验概率 |
| `predict_log_proba(X)` | X: 测试特征矩阵 | 返回对数后验（更稳定） |
| `score(X, y)` | X, y | 返回 accuracy |

### 常用工具

| 函数 | 说明 |
|------|------|
| `CountVectorizer()` | 文本 → 词频矩阵（配合 MultinomialNB） |
| `TfidfVectorizer()` | 文本 → TF-IDF 矩阵 |
| `CalibratedClassifierCV()` | 概率校准（NB 输出过于极端时使用） |
| `Pipeline([...])` | 链式封装特征提取 + NB |

> 📖 Docs: [scikit-learn Naive Bayes API](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.naive_bayes)

---

## 目录结构模板

### 简单结构

```
nb_classifier/
├── train.py              ← 训练脚本
├── predict.py            ← 预测脚本
└── data/
    ├── train.csv
    └── test.csv
```

### 标准结构

```
nb_classifier/
├── config.py             ← 超参数配置 (alpha, var_smoothing 等)
├── data_loader.py        ← 数据加载与特征提取
├── model.py              ← NB 模型封装
├── train.py              ← 训练 + 保存模型
├── evaluate.py           ← 评估 + 混淆矩阵
├── data/
│   ├── raw/              ← 原始文本/CSV
│   └── processed/        ← 向量化后的特征
└── models/
    └── nb_model.pkl      ← joblib 保存的模型
```

> 📖 Docs: [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/pipeline.html)
