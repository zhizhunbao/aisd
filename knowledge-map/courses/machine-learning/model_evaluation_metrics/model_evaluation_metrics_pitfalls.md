---
topic: model_evaluation_metrics
dimension: pitfalls
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Chicco & Jurman, 'The advantages of the MCC over F1', BMC Genomics 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf"
  - "📖 Paper: Raschka, 'Model Evaluation, Model Selection, and Algorithm Selection in ML', arXiv 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf"
  - "📖 Docs: scikit-learn Model Evaluation — https://scikit-learn.org/stable/modules/model_evaluation.html"
  - "🧪 经验: 常见学生错误和调试模式"
expiry: 6m
status: current
---

# Model Evaluation & Metrics 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 不平衡数据上只看 Accuracy

**痛点类别：** 概念误解 — "为什么模型准确率很高但实际效果很差"

**场景：** 训练了一个欺诈检测模型，正常交易 99%、欺诈交易 1%，模型 Accuracy 达到 99%

**症状：** Accuracy = 0.99 看起来很好，但上线后一笔欺诈都没抓到

**根因：** 模型学会了"全部预测为正常"这个捷径。Accuracy 的分母是全部样本，被大量 TN 撑高了。在极端不平衡数据上，Accuracy 完全没有区分力

**解法：**

❌ 错误做法 — 只用 Accuracy 评估不平衡数据

```python
# 错误：只看 accuracy
from sklearn.metrics import accuracy_score
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")  # 0.99 → 误以为很好
```

✅ 正确做法 — 使用 F1、Recall、MCC 和 PR-AUC

```python
# 正确：用多个指标全面评估
from sklearn.metrics import classification_report, matthews_corrcoef, average_precision_score

print(classification_report(y_test, y_pred))  # 看少数类的 Recall 和 F1
print(f"MCC: {matthews_corrcoef(y_test, y_pred):.4f}")
print(f"PR-AUC: {average_precision_score(y_test, y_proba):.4f}")
```

**教训：** 不平衡数据上 Accuracy 是骗人的。用 F1（或 MCC）评估分类质量，用 PR-AUC 评估排序能力。

> 📖 Paper: Chicco & Jurman, [MCC vs F1](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf)

---

## 坑 2: 用训练数据评估模型

**痛点类别：** 流程错误 — "为什么训练效果好但新数据上不行"

**场景：** 用整个数据集训练模型，然后又用同一个数据集计算 Accuracy

**症状：** 训练 Accuracy = 0.99，但新数据上 Accuracy 骤降到 0.60

**根因：** 模型"记住"了训练数据（过拟合），你测量的是记忆力而不是泛化能力——这就像做完一套卷子后再考同一套作为考试成绩

**解法：**

❌ 错误做法 — 在训练数据上评估

```python
# 错误：用训练数据评估
model.fit(X, y)
y_pred = model.predict(X)    # 用同一份数据
print(accuracy_score(y, y_pred))  # 虚高！
```

✅ 正确做法 — Hold-out 或交叉验证

```python
# 正确：用交叉验证
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.4f} ± {scores.std():.4f}")
```

**教训：** 永远不要用训练数据评估模型。最低要求是 train/test split，推荐 K-Fold CV。

> 📖 Paper: Raschka, [Model Evaluation](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf), Section 2

---

## 坑 3: 交叉验证中的数据泄露

**痛点类别：** 流程错误 — "为什么 CV 分数很高但部署后很差"

**场景：** 先对整个数据集做了标准化/特征选择，然后再做 K-Fold CV

**症状：** CV Accuracy = 0.95，部署后发现新数据上只有 0.70

**根因：** 标准化的均值/标准差包含了测试折的信息（数据泄露 / Data Leakage）。相当于考试前偷看了答案

**解法：**

❌ 错误做法 — 先预处理再 CV

```python
# 错误：先标准化全部数据，再 CV
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # 泄露！测试折的统计量混入了
scores = cross_val_score(model, X_scaled, y, cv=5)
```

✅ 正确做法 — 用 Pipeline 把预处理包进 CV

```python
# 正确：Pipeline 确保每折独立预处理
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = make_pipeline(StandardScaler(), LogisticRegression())
scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')
# 每折内部独立 fit_transform，无泄露
```

**教训：** 数据预处理必须在 CV 的内部。用 Pipeline 是最简单的防泄露方法。

> 📖 Docs: [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline)

---

## 坑 4: 混淆 Precision 和 Recall 的业务含义

**痛点类别：** 概念误解 — "不知道该优化 Precision 还是 Recall"

**场景：** 做癌症筛查模型，努力提高了 Precision 到 0.98

**症状：** Precision 很高（预测为阳性的很准），但 Recall 只有 0.30——70% 的癌症患者被漏诊了

**根因：** 混淆了"模型说是的里面多少是对的"（Precision）和"实际的正例里找到了多少"（Recall）。癌症筛查的代价是漏诊 >> 误诊，应该优化 Recall

**解法：**

❌ 错误做法 — 不分场景盲目看 Precision

```python
# 错误：降低阈值只看 Precision
from sklearn.metrics import precision_score
print(f"Precision: {precision_score(y_test, y_pred):.4f}")  # 高但漏诊多
```

✅ 正确做法 — 根据业务场景选择主要指标

```python
# 正确：癌症筛查 → 用 Recall 或 F2
from sklearn.metrics import recall_score, fbeta_score

print(f"Recall: {recall_score(y_test, y_pred):.4f}")
print(f"F2 Score: {fbeta_score(y_test, y_pred, beta=2):.4f}")  # β=2 更重视 Recall
```

**教训：** 漏诊代价高 → 优化 Recall（或 F2）。误报代价高 → 优化 Precision（或 F0.5）。

> 📖 Paper: Powers, [Evaluation](../../../.documents/papers/model_evaluation_metrics/powers_2020_evaluation_precision_recall_fmeasure.pdf)

---

## 坑 5: 时间序列数据用随机 K-Fold CV

**痛点类别：** 流程错误 — "为什么股票预测模型 CV 效果好但实盘亏钱"

**场景：** 用过去 5 年的股价数据训练模型，用普通 K-Fold CV 评估

**症状：** CV Accuracy = 0.80，但实际交易全亏

**根因：** 随机 K-Fold 会把未来的数据混入训练集（look-ahead bias）。模型偷看了未来，当然"预测"很准

**解法：**

❌ 错误做法 — 时间序列用随机 CV

```python
# 错误：时间序列用随机 K-Fold
scores = cross_val_score(model, X, y, cv=5)  # 未来数据混入训练集
```

✅ 正确做法 — 用 TimeSeriesSplit

```python
# 正确：用时间序列专用划分
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(model, X, y, cv=tscv, scoring='accuracy')
# 每折都是：训练=过去，测试=未来
```

**教训：** 时间序列数据必须用 TimeSeriesSplit，确保"训练在前、测试在后"。

> 📖 Docs: [scikit-learn TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别只记公式** → 先理解每个指标"回答什么问题"（Precision: 模型说'是'靠不靠谱？Recall: 有多少正例被找到了？）
2. [ ] **别混淆 Accuracy 和 Precision** → 中文翻译"准确率"和"精确率"太像了，靠英文原名区分
3. [ ] **别盲目追求 AUC=1** → 测试集上 AUC=1 几乎肯定是数据泄露或过拟合
4. [ ] **别忽略标准差** → CV 分数报 `0.85 ± 0.12` 比只报 `0.85` 重要得多（0.12 说明不稳定）
5. [ ] **别把 Validation Set 和 Test Set 搞混** → Validation 用来调参，Test 用来最终评估，不能混用

### 作业/项目避坑

1. [ ] **先搞清楚评估指标再训练** → 不要训练完了才想"该用什么指标"
2. [ ] **用 Pipeline 防泄露** → 预处理 + 模型打包在一起
3. [ ] **报告多个指标** → 只报一个 Accuracy 是大忌
4. [ ] **画混淆矩阵** → 最直观看到模型在哪犯错

### 调试清单（技术类）

1. [ ] **F1 = 0 或 NaN？** → 检查是否 TP = 0（模型预测全负）。加 `zero_division=0` 参数
2. [ ] **AUC = 0.5？** → 模型等于随机猜测。检查特征是否有区分力
3. [ ] **训练 Accuracy 高，CV Accuracy 低？** → 过拟合。减少模型复杂度或增加正则化
4. [ ] **CV 分数波动很大？** → 数据太少或类别严重不平衡。用 StratifiedKFold 或增大 K
5. [ ] **PR-AUC 很低但 ROC-AUC 很高？** → 典型的不平衡数据陷阱。以 PR-AUC 为准
