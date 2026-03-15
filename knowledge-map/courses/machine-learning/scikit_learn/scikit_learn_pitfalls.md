---
topic: scikit_learn
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn Common Pitfalls — https://scikit-learn.org/stable/common_pitfalls.html"
  - "📖 Docs: scikit-learn FAQ — https://scikit-learn.org/stable/faq.html"
  - "💻 Source: scikit-learn/sklearn — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn"
  - "🧪 经验: ML 项目常见错误"
expiry: 6m
status: current
---

# Scikit-Learn 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 数据泄漏 — 先 fit_transform 全数据再 split

**场景：** 在整个数据集上做 StandardScaler / PCA，然后再拆分 train/test

**症状：** 测试分数虚高（0.95+），部署后泛化性能大幅下降

**根因：** StandardScaler 的 mean/std 是从全数据（包括测试集）计算的。测试集的信息泄漏到了训练过程中。

**解法：**

❌ 错误写法 — 全数据 fit

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)    # 泄漏！scaler 看到了测试数据
X_train, X_test = train_test_split(X_scaled, ...)
```

✅ 正确写法 — 只在 train 上 fit

```python
X_train, X_test = train_test_split(X, ...)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # 只在 train 上 fit
X_test = scaler.transform(X_test)        # 用 train 的参数 transform

# 或更好：用 Pipeline（自动处理）
pipe = Pipeline([('scaler', StandardScaler()), ('svm', SVC())])
pipe.fit(X_train, y_train)
```

**教训：** **永远用 Pipeline**—— 它自动确保预处理只在训练折上 fit

> 📖 Docs: [sklearn Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

---

## 坑 2: 未标准化导致距离/梯度类模型表现差

**场景：** 直接用原始特征喂给 SVM / KNN / 梯度下降类模型

**症状：** 模型准确率很低，或者训练不收敛

**根因：** 特征量纲差异巨大（如"年龄"0-100 vs "工资"10000-100000），距离和梯度被大数值特征主导。SVM、KNN、Logistic 回归对特征尺度敏感；决策树/随机森林不敏感。

**解法：**

❌ 错误写法 — 跳过标准化

```python
svc = SVC()
svc.fit(X_train_raw, y_train)   # X 有的列是 0-1，有的是 0-10000
```

✅ 正确写法 — Pipeline 中标准化

```python
pipe = Pipeline([
    ('scaler', StandardScaler()),  # 先标准化
    ('svc', SVC())
])
pipe.fit(X_train, y_train)
```

**教训：** 用距离/梯度的模型必须标准化；树模型可以不标准化但标准化也不会变差

> 📖 Docs: [sklearn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## 坑 3: 交叉验证中使用 accuracy 评估不平衡数据

**场景：** 正负样本比 95:5，用 accuracy 做 CV scoring

**症状：** 模型 accuracy = 0.95 看似很好，但实际全部预测为多数类

**根因：** 不平衡数据中，什么都不做全预测多数类也能得 95%。accuracy 无法反映少数类的识别能力。

**解法：**

❌ 错误写法 — 不平衡数据用 accuracy

```python
cross_val_score(clf, X, y, cv=5, scoring='accuracy')  # 虚高！
```

✅ 正确写法 — 用 F1 / ROC-AUC + 分层 CV

```python
from sklearn.model_selection import StratifiedKFold

cross_val_score(clf, X, y, cv=StratifiedKFold(5),
                scoring='f1')          # 或 'roc_auc'
```

**教训：** 不平衡数据用 `f1` / `roc_auc` / `f1_weighted`；用 `StratifiedKFold` 保证每折类别比例一致

> 📖 Docs: [sklearn Scoring](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## 坑 4: GridSearchCV 用了错误的 param 前缀

**场景：** Pipeline 中使用 GridSearchCV，超参数名称格式不对

**症状：** `ValueError: Invalid parameter C for estimator Pipeline`

**根因：** Pipeline 中的超参数名格式是 `步骤名__参数名`（双下划线），如 `svc__C`。直接写 `C` 会找 Pipeline 本身的参数。

**解法：**

❌ 错误写法 — 未加步骤前缀

```python
pipe = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])
GridSearchCV(pipe, {'C': [0.1, 1]})   # ValueError!
```

✅ 正确写法 — 双下划线前缀

```python
GridSearchCV(pipe, {'svc__C': [0.1, 1, 10]})   # ✅ 正确
```

**教训：** Pipeline 超参数格式 = `步骤名__参数名`

> 📖 Docs: [sklearn Pipeline and GridSearch](https://scikit-learn.org/stable/modules/compose.html#nested-parameters)

---

## 坑 5: fit_transform vs transform 搞混

**场景：** 在测试集上调用 `fit_transform()` 而非 `transform()`

**症状：** 模型在测试集上结果不一致，或评估分数不可靠

**根因：** `fit_transform(X_test)` 会用测试数据重新学习参数（如 PCA 重新计算主成分方向），导致训练和测试用了不同的变换。

**解法：**

❌ 错误写法 — 测试集也 fit_transform

```python
X_train_pca = pca.fit_transform(X_train)  # ✅ OK
X_test_pca = pca.fit_transform(X_test)    # ❌ 重新 fit 了！
```

✅ 正确写法 — 测试集只 transform

```python
X_train_pca = pca.fit_transform(X_train)  # 训练集: fit + transform
X_test_pca = pca.transform(X_test)        # 测试集: 只 transform, 用训练参数
```

**教训：** 训练集 `fit_transform()`，测试集永远只 `transform()`

> 📖 Docs: [sklearn Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)

---

## 坑 6: 忘记设置 random_state 导致结果不可复现

**场景：** 模型或 train_test_split 未设置 `random_state`

**症状：** 每次运行结果不同，无法复现之前的好成绩

**根因：** 很多 sklearn 操作涉及随机性（数据拆分、随机森林的特征子采样、KMeans 初始化）。不设种子则每次随机不同。

**解法：**

❌ 错误写法 — 不设种子

```python
X_train, X_test = train_test_split(X, y)             # 每次不同
rf = RandomForestClassifier(n_estimators=100)          # 每次不同
```

✅ 正确写法 — 全链路设种子

```python
X_train, X_test = train_test_split(X, y, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
```

**教训：** 在 `train_test_split`、模型构造、CV 中全部设置 `random_state`

> 📖 Docs: [sklearn FAQ](https://scikit-learn.org/stable/faq.html)

---

## 调试清单

1. [ ] **测试分数虚高？** → 检查数据泄漏（在 split 前是否 fit 了预处理器）
2. [ ] **SVM/KNN/LR 表现差？** → 是否标准化了？`StandardScaler` in Pipeline
3. [ ] **accuracy 高但少数类全错？** → 换 `f1` / `roc_auc`，加 `class_weight='balanced'`
4. [ ] **GridSearch ValueError？** → 超参数名用 `步骤名__参数名` 格式
5. [ ] **结果不可复现？** → 全链路设 `random_state`
6. [ ] **fit_transform on test？** → 测试集只 `transform()`
7. [ ] **内存不够？** → 用 `partial_fit()` 或 `n_jobs=1` 减少并行
8. [ ] **训练特别慢？** → 减少 `n_estimators` / `max_depth`，或用 `HistGradientBoosting`
9. [ ] **ConvergenceWarning？** → 增加 `max_iter`，检查是否标准化了
10. [ ] **模型部署后结果不同？** → 用 `joblib.dump/load` 保存整个 Pipeline
