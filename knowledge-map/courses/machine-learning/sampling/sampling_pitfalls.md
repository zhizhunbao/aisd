---
topic: sampling
dimension: pitfalls
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Chawla et al., 'SMOTE', JAIR 2002 — https://arxiv.org/abs/1106.1813"
  - "📖 Docs: scikit-learn model_selection — https://scikit-learn.org/stable/modules/cross_validation.html"
  - "🧪 经验: 常见 CV 和 SMOTE 使用错误"
expiry: 6m
status: current
---

# Sampling & Resampling 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: SMOTE 在 CV 外面做导致数据泄露

**痛点类别：** 代码类 — 不知道操作的正确顺序

**场景：** 先对整个数据集做 SMOTE，再用 cross_val_score 做交叉验证

**症状：** 验证分数异常地高（比如 recall 从 0.6 跳到 0.95），觉得 SMOTE "效果太好了"

**根因：** SMOTE 在划分前就接触了所有数据，合成的样本可能基于验证集中的真实样本插值。验证集中的样本信息泄露到了训练集。这不是 SMOTE 的功劳，而是**数据泄露**

**解法：**

❌ 错误做法 — 先 SMOTE 再 CV（数据泄露）

```python
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_val_score

# ❌ 整体 SMOTE 后再 CV → 验证集已被污染
X_res, y_res = SMOTE().fit_resample(X, y)
scores = cross_val_score(clf, X_res, y_res, cv=5)  # 分数虚高！
```

✅ 正确做法 — SMOTE 放在 Pipeline 内（每折独立）

```python
from imblearn.pipeline import Pipeline  # ⚠️ 用 imblearn 的 Pipeline
from sklearn.model_selection import cross_val_score

# ✅ Pipeline 保证 SMOTE 只作用于训练折
pipe = Pipeline([('smote', SMOTE()), ('clf', clf)])
scores = cross_val_score(pipe, X, y, cv=5)  # 真实分数
```

**教训：** 任何涉及数据变换的操作（SMOTE、特征选择、标准化）都必须放在 CV 的循环内部，不能提前做

> 📖 Docs: [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline)
> 📖 Docs: [imbalanced-learn Pipeline](https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html)

---

## 坑 2: 用 sklearn.pipeline.Pipeline 代替 imblearn.pipeline.Pipeline

**痛点类别：** 代码类 — 两个库名字一样但行为不同

**场景：** 把 SMOTE 放进了 `sklearn.pipeline.Pipeline`

**症状：** `TypeError: All intermediate steps should be transformers and implement fit and transform or be the string 'passthrough'`

**根因：** scikit-learn 的 Pipeline 要求中间步骤实现 `transform()`，但 SMOTE 实现的是 `fit_resample()`。imbalanced-learn 的 Pipeline 专门支持 sampler

**解法：**

❌ 错误做法 — 用 sklearn 的 Pipeline

```python
from sklearn.pipeline import Pipeline  # ❌ 错了！
pipe = Pipeline([('smote', SMOTE()), ('clf', clf)])  # 报错
```

✅ 正确做法 — 用 imblearn 的 Pipeline

```python
from imblearn.pipeline import Pipeline  # ✅ 对了！
pipe = Pipeline([('smote', SMOTE()), ('clf', clf)])  # 正常
```

**教训：** 只要 Pipeline 里有采样器（SMOTE/ADASYN/Undersampler），就必须用 `imblearn.pipeline.Pipeline`

> 📖 Docs: [imblearn Pipeline](https://imbalanced-learn.org/stable/references/generated/imblearn.pipeline.Pipeline.html)

---

## 坑 3: 用 accuracy 评估不平衡数据

**痛点类别：** 概念类 — 不理解为什么 accuracy 不行

**场景：** 类别不平衡（99:1），模型全预测多数类，accuracy=99%

**症状：** 觉得模型表现很好，但实际上少数类全部漏检

**根因：** Accuracy = 正确数/总数，在不平衡数据中，全预测多数类就能获得很高的值。Accuracy 对少数类的性能完全不敏感

**解法：**

❌ 错误做法 — 只看 accuracy

```python
# ❌ 不平衡数据只看 accuracy 没有意义
scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f}")  # 0.990 但少数类全漏
```

✅ 正确做法 — 用 precision/recall/F1/AUC

```python
# ✅ 用多个指标全面评估
from sklearn.model_selection import cross_validate
results = cross_validate(clf, X, y, cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'])
for m in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']:
    print(f"{m}: {results[f'test_{m}'].mean():.3f}")
```

**教训：** 不平衡数据必须用 Recall（少数类有没有被找到）+ Precision（找到的准不准）+ F1（两者的调和平均）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.2

---

## 坑 4: 时间序列数据用标准 K-Fold CV

**痛点类别：** 概念类 — 不理解 i.i.d. 假设

**场景：** 股票价格预测任务，用标准 K-Fold CV 评估

**症状：** CV 分数很高，但实盘部署后性能暴跌

**根因：** 标准 K-Fold 随机打乱数据，导致**未来数据泄露到训练集**。比如用 2025 年的数据训练，却测试 2024 年的预测

**解法：**

❌ 错误做法 — 时间序列用 K-Fold

```python
# ❌ 随机打乱破坏了时序性
from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)  # 未来数据泄露！
```

✅ 正确做法 — 用 TimeSeriesSplit

```python
# ✅ 只用过去的数据训练，预测未来
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X, y, cv=tscv)
```

**教训：** K-Fold CV 假设数据 i.i.d.（独立同分布），时间序列违反这个假设

> 📖 Docs: [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

---

## 坑 5: Bootstrap 用来估计泛化误差时偏差大

**痛点类别：** 概念类 — 混淆了 Bootstrap 的用途

**场景：** 用 Bootstrap 估计模型的泛化误差

**症状：** Bootstrap 估计的误差远低于真实泛化误差

**根因：** 有放回抽样使得约 63.2% 的样本出现在训练集中，而 OOB 样本只有 36.8%。训练集和"测试集"(OOB) 之间存在重叠：有些训练样本在 Bootstrap 样本中出现了多次，但原始样本和 OOB 样本之间有信息相关性

**解法：**

❌ 错误做法 — 直接用 Bootstrap 估计泛化误差

```python
# ❌ 简单 Bootstrap 对泛化误差有下偏
# 不推荐用来代替 CV
```

✅ 正确做法 — 用 CV 估计泛化误差，用 Bootstrap 估计置信区间

```python
# ✅ 各用其所长
# CV：估计泛化误差
cv_score = cross_val_score(clf, X, y, cv=5).mean()
# Bootstrap：估计 CV score 的置信区间
# （见 code.md 示例 2）
```

**教训：** Bootstrap 的长处是估计统计量的不确定性（标准误差、置信区间），不是估计泛化误差

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.11 ".632 Bootstrap"

---

## 超级避坑指南

### 学习避坑

1. [ ] **别混淆 CV 和 Bootstrap 的用途** → CV 估计泛化误差, Bootstrap 估计不确定性
2. [ ] **别忘了 i.i.d. 假设** → 时间序列不能用标准 K-Fold
3. [ ] **别用 accuracy 评估不平衡数据** → 用 F1/AUC/Recall
4. [ ] **别以为 SMOTE 总是好的** → 高维/噪声数据可能生成坏样本

### 作业/项目避坑

1. [ ] **SMOTE 必须在 Pipeline 内** → 不能提前做
2. [ ] **用 imblearn.pipeline 不是 sklearn.pipeline** → 名字一样行为不同
3. [ ] **Stratified CV 用于不平衡数据** → 保持每折类别比例
4. [ ] **设置 random_state** → 保证结果可复现

### 考试/答辩避坑

1. [ ] **被问 "CV 和 Bootstrap 有什么区别"** → CV=泛化估计, Bootstrap=不确定性估计
2. [ ] **被问 "为什么不用 LOOCV"** → 方差高 + 计算贵，K=5/10 是更好的折中
3. [ ] **被问 "SMOTE 怎么工作"** → K-NN 找近邻 → 连线上随机插值

### 调试清单（技术类）

1. [ ] **CV 分数异常高？** → 检查是否有数据泄露（SMOTE/标准化在 CV 外面做了）
2. [ ] **SMOTE Pipeline 报错？** → 检查是否用了 `imblearn.pipeline.Pipeline`
3. [ ] **CV 分数波动大？** → 增加 K（从 5 到 10），或用 RepeatedKFold
4. [ ] **少数类 recall 低？** → 加 SMOTE 或用 `class_weight='balanced'`
5. [ ] **时间序列 CV 偏高？** → 改用 `TimeSeriesSplit`
