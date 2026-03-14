---
topic: naive_bayes
dimension: pitfalls
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Docs: scikit-learn Naive Bayes — https://scikit-learn.org/stable/modules/naive_bayes.html"
  - "💻 Source: scikit-learn/sklearn/naive_bayes.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/naive_bayes.py"
  - "📖 Paper: Vidhya & Aghila, 'A Survey of Naive Bayes in Text Document Classification', arXiv:1007.1669 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf"
  - "🧪 经验: scikit-learn 实践中的常见陷阱"
expiry: 6m
status: current
---

# Naive Bayes 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 用 MultinomialNB 处理含负数的特征

**场景：** 对 TF-IDF 矩阵使用 MultinomialNB，或使用了 `StandardScaler` 归一化后的词频特征

**症状：** `ValueError: Negative values in data passed to MultinomialNB (input X)`

**根因：** MultinomialNB 的数学假设是多项分布（计数），要求所有特征值**非负**。TF-IDF 本身非负，但 StandardScaler 会引入负值

**解法：**

❌ 错误写法 — StandardScaler 后用 MultinomialNB（引入负数）

```python
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import MultinomialNB

X_scaled = StandardScaler().fit_transform(X_tfidf)  # 产生负值！
clf = MultinomialNB()
clf.fit(X_scaled, y)  # ValueError!
```

✅ 正确写法 — 不对 TF-IDF 做 Standard 归一化，或用 GaussianNB/ComplementNB

```python
from sklearn.naive_bayes import MultinomialNB, ComplementNB

# 方案1: 直接用 TF-IDF（本身非负）
clf = MultinomialNB(alpha=0.1)
clf.fit(X_tfidf, y)  # ✅ TF-IDF 值已是非负

# 方案2: 若需要处理负值，改用 ComplementNB（效果通常更好）
clf = ComplementNB()
clf.fit(X_tfidf, y)
```

**教训：** MultinomialNB / CategoricalNB / BernoulliNB 均不支持负值；只有 GaussianNB 支持负实数

> 📖 Docs: [scikit-learn MultinomialNB 限制](https://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes)

---

## 坑 2: partial_fit 第一次调用忘记传 classes 参数

**场景：** 使用在线学习处理流式数据，第一批次调用 `partial_fit` 时没有传 `classes`

**症状：** `sklearn.utils.multiclass._check_partial_fit_first_call` 相关 `ValueError`，或者后续批次中出现的新类别无法被识别

**根因：** `partial_fit` 第一次调用时需要知道全部可能的类别，以正确初始化参数矩阵。后续批次可省略

**解法：**

❌ 错误写法 — 第一次调用漏掉 classes

```python
clf = GaussianNB()
for batch_X, batch_y in stream:
    clf.partial_fit(batch_X, batch_y)  # 第一次时 classes 未知！
```

✅ 正确写法 — 预先定义 classes，第一次显式传入

```python
import numpy as np
from sklearn.naive_bayes import GaussianNB

clf = GaussianNB()
all_classes = np.array([0, 1, 2])  # 提前定义全部类别 / define all classes upfront

for i, (batch_X, batch_y) in enumerate(stream):
    # 仅第一次需要传 classes；后续可省略
    # Pass classes only on first call; optional afterwards
    classes = all_classes if i == 0 else None
    clf.partial_fit(batch_X, batch_y, classes=classes)
```

**教训：** 永远在第一次 `partial_fit` 时传 `classes=np.unique(y_all)`

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `_check_partial_fit_first_call()` L31

---

## 坑 3: 依赖 predict_proba 输出作为真实概率

**场景：** 用 NB 输出的 `predict_proba` 做风控、医疗诊断等需要准确概率的场景

**症状：** 模型 predict 准确率高，但输出的概率极度趋向 0 或 1，Brier Score 或 Log Loss 很差

**根因：** NB 的条件独立假设使各特征的贡献被无限叠加，导致后验概率极端化（例如：100 个独立特征各给 0.6 的支持，最终后验接近 1.0）

**解法：**

❌ 错误写法 — 直接用 NB 概率做决策阈值

```python
clf = GaussianNB().fit(X_train, y_train)
proba = clf.predict_proba(X_test)  # 概率分布极端，不可信
threshold = 0.7
y_pred = (proba[:, 1] > threshold).astype(int)
```

✅ 正确写法 — 先做概率校准再用

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import GaussianNB

base_clf = GaussianNB()
calibrated_clf = CalibratedClassifierCV(base_clf, method='sigmoid', cv=5)
calibrated_clf.fit(X_train, y_train)

proba = calibrated_clf.predict_proba(X_test)  # 校准后更接近真实概率
y_pred = (proba[:, 1] > 0.7).astype(int)
```

**教训：** NB 的 predict 可信，但 predict_proba 的数值不可信；需要精确概率时必须做 Platt scaling 或 Isotonic regression 校准

> 📖 Docs: [scikit-learn Probability Calibration](https://scikit-learn.org/stable/modules/calibration.html)

---

## 坑 4: GaussianNB 遇到零方差特征崩溃

**场景：** 数据中某个类别的某个特征方差为 0（例如某类别所有样本的某特征值相同）

**症状：** `RuntimeWarning: divide by zero encountered in log` 或预测结果全为同一类别

**根因：** GaussianNB 计算 log N(x; μ, σ²) 时，σ²=0 导致分母为零和 log(0)

**解法：**

❌ 错误写法 — 不处理零方差（默认 var_smoothing 太小）

```python
clf = GaussianNB(var_smoothing=0)  # 关闭平滑，危险！
clf.fit(X_train, y_train)  # 若有零方差特征，预测会 NaN
```

✅ 正确写法 — 适当增大 var_smoothing，或预先删除零方差特征

```python
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import VarianceThreshold

# 方案1: 增大 var_smoothing（默认 1e-9 通常足够，但极端情况下调大）
clf = GaussianNB(var_smoothing=1e-3)

# 方案2: 预先删除零方差特征
selector = VarianceThreshold(threshold=0)  # 删除方差=0的特征
X_filtered = selector.fit_transform(X_train)
clf = GaussianNB().fit(X_filtered, y_train)
```

**教训：** `var_smoothing` 是 GaussianNB 的安全垫，遇到数值问题先调大它；数据预处理时检查 `VarianceThreshold`

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `_joint_log_likelihood()` L538：`var_[i, :]` 加 `epsilon_` 防零

---

## 坑 5: BernoulliNB 没有正确二值化输入

**场景：** 特征是整数词频（0, 1, 2, 3...），直接传给 BernoulliNB

**症状：** 模型可以运行，但准确率异常低，不如 MultinomialNB；BernoulliNB 的意义被破坏

**根因：** BernoulliNB 默认对输入做 `binarize=0.0` 的阈值处理（>0 视为 1），但如果用户已经期望传入 0/1 特征却传了词频，语义不符

**解法：**

❌ 错误写法 — 把 TF-IDF（非二值）直接传给 BernoulliNB

```python
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer

X = TfidfVectorizer().fit_transform(texts)
clf = BernoulliNB()
clf.fit(X, y)  # 语义混乱：BernoulliNB 假设二值输入
```

✅ 正确写法 — 明确用 CountVectorizer + binary=True，或设置 binarize 阈值

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

# 方案1: CountVectorizer 直接输出二值矩阵
X = CountVectorizer(binary=True).fit_transform(texts)  # 词是否出现，非词频
clf = BernoulliNB(alpha=1.0)
clf.fit(X, y)  # ✅ 符合 BernoulliNB 假设

# 方案2: 明确设置 binarize 参数（内部做阈值处理）
clf = BernoulliNB(alpha=1.0, binarize=0.5)  # >0.5 视为 1
```

**教训：** BernoulliNB 适合"词是否出现"；MultinomialNB 适合"词出现多少次"；场景不同，别混用

> 📖 Docs: [scikit-learn BernoulliNB](https://scikit-learn.org/stable/modules/naive_bayes.html#bernoulli-naive-bayes)

---

## 调试清单

1. [ ] **特征有负值？** → 只有 GaussianNB 支持负值；多项/伯努利/类别 NB 均不支持
2. [ ] **partial_fit 第一次传了 classes 参数？** → 未传会导致类别识别错误
3. [ ] **predict_proba 的值极端（0.999 或 0.001）？** → 需要 CalibratedClassifierCV 校准
4. [ ] **GaussianNB 出现 NaN 或 log 报错？** → 检查零方差特征，增大 var_smoothing
5. [ ] **BernoulliNB 效果差？** → 检查输入是否已二值化，或改用 MultinomialNB
6. [ ] **文本分类 MultinomialNB 效果差？** → 尝试 ComplementNB（对不平衡数据更好）
7. [ ] **alpha=0 时警告？** → 不推荐 alpha=0；会导致未见词概率为 0，使用 force_alpha=True 可强制忽略警告
8. [ ] **新类别在 partial_fit 中出现？** → 确保 classes 参数覆盖所有可能类别
9. [ ] **类别严重不平衡？** → 用 class_prior 手动调整先验或用 ComplementNB
10. [ ] **稀疏矩阵传给 GaussianNB？** → GaussianNB 不支持稀疏输入，需先 `.toarray()`

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) 各类的 `_check_X()` 方法
> 🧪 经验: scikit-learn 实践中整理
