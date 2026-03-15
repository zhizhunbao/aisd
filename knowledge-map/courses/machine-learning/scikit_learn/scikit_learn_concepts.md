---
topic: scikit_learn
dimension: concepts
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn Glossary — https://scikit-learn.org/stable/glossary.html"
  - "📖 Docs: scikit-learn API Design — https://scikit-learn.org/stable/developers/develop.html"
  - "💻 Source: scikit-learn/sklearn/base.py — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn/base.py"
  - "📚 Book: Hastie et al., ESL — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
expiry: 6m
status: current
---

# Scikit-Learn 核心概念

> 📖 Docs: [scikit-learn Glossary](https://scikit-learn.org/stable/glossary.html)
> 💻 Source: [sklearn/base.py](../../../.github/scikit-learn/sklearn/base.py)

---


## 术语定义

### 估计器 (Estimator)

sklearn 的核心抽象。任何能从数据中"学习"的对象都是 Estimator，必须实现 `fit(X, y)` 方法。所有分类器、回归器、聚类器、降维器都是 Estimator。构造时通过超参数 `__init__(hyperparams)` 配置，`fit()` 后内部状态变化（产生带下划线后缀的属性如 `coef_`）。

> 易混淆：**Estimator vs Model** — 在 sklearn 中，Estimator 是 API 层面的概念（实现了 fit）；Model 是 fit 之后的 Estimator（已学到参数）

### 预测器 (Predictor)

能做预测的 Estimator，实现 `predict(X)` 方法。分类器和回归器都是 Predictor。分类器还通常实现 `predict_proba(X)` 返回类别概率。调用 `predict` 前必须先 `fit`。

### 转换器 (Transformer)

能做数据变换的 Estimator，实现 `transform(X)` 方法。典型如 `StandardScaler`（标准化）、`PCA`（降维）、`OneHotEncoder`（编码）。大多数 Transformer 同时实现 `fit_transform(X)` = `fit(X).transform(X)` 的快捷方式。

> 易混淆：**Transformer vs Deep Learning 的 Transformer** — sklearn 的 Transformer 是数据预处理/特征变换器（实现 transform 接口）；DL 的 Transformer 是注意力机制架构，完全不同

### 管道 (Pipeline)

将多个 Transformer 和一个最终 Estimator 串联为一个统一的 Estimator。`Pipeline([('scaler', StandardScaler()), ('svm', SVC())])`。Pipeline 的 `fit()` 依次调用每一步的 `fit_transform()`，最后调用最终估计器的 `fit()`。防止数据泄漏、简化代码。

### 交叉验证 (Cross-Validation)

将数据集分为 $K$ 折，轮流用其中一折做验证、其余做训练。`cross_val_score(model, X, y, cv=5)` 自动执行 5 折 CV 并返回每折得分。用于可靠地估计模型泛化性能，避免过拟合到特定的 train/test 分割。

### 网格搜索 (Grid Search / Hyperparameter Tuning)

对超参数的所有组合做交叉验证，找到最优组合。`GridSearchCV(model, param_grid, cv=5)` 穷举所有超参数组合。`RandomizedSearchCV` 随机采样，效率更高。调参是 ML 工作流的关键步骤。

### 特征矩阵 X 与目标向量 y

sklearn 的输入约定：`X` 是 $n \times p$ 的特征矩阵（NumPy 数组或 Pandas DataFrame），$n$ = 样本数，$p$ = 特征数；`y` 是长度为 $n$ 的目标向量。监督学习用 `(X, y)`，无监督学习只用 `X`。

### 数据泄漏 (Data Leakage)

训练过程中不当地使用了验证/测试集的信息，导致评估指标虚高。典型情况：先对全部数据做 StandardScaler `fit_transform`，再划分 train/test。正确做法是用 Pipeline 或只在 train 上 fit。

> 易混淆：**数据泄漏 vs 过拟合** — 数据泄漏是信息违规（测试信息混入训练）；过拟合是模型复杂度过高（对训练数据记忆而非泛化），两者导致的症状相似但原因不同

### 评分函数 (Scoring / Metrics)

衡量模型性能的函数。分类：`accuracy_score`、`f1_score`、`roc_auc_score`；回归：`mean_squared_error`、`r2_score`。`cross_val_score` 的 `scoring` 参数接受字符串或自定义 scorer。

### 稀疏矩阵 (Sparse Matrix)

当特征矩阵大部分元素为 0 时（如文本的 TF-IDF、独热编码），使用 `scipy.sparse` 格式存储可节省内存。sklearn 大多数模型支持稀疏输入。

> 📖 Docs: [sklearn Glossary](https://scikit-learn.org/stable/glossary.html)
> 📖 Docs: [sklearn API Design](https://scikit-learn.org/stable/developers/develop.html)
> 💻 Source: [sklearn/base.py](../../../.github/scikit-learn/sklearn/base.py)

---


## 概念辨析

### fit() vs transform() vs predict()

| 维度 | `fit(X, y)` | `transform(X)` | `predict(X)` |
|------|---|---|---|
| **谁用** | 所有 Estimator | Transformer | Predictor |
| **做什么** | 从数据学习参数 | 用学到的参数变换数据 | 用学到的参数做预测 |
| **返回** | `self` | 变换后的 $X'$ | 预测值 $\hat{y}$ |
| **示例** | `scaler.fit(X_train)` | `scaler.transform(X_test)` | `svm.predict(X_test)` |

> 📖 Docs: [sklearn API](https://scikit-learn.org/stable/developers/develop.html)

### GridSearchCV vs RandomizedSearchCV vs Bayesian Optimization

| 维度 | GridSearchCV | RandomizedSearchCV | Bayesian (Optuna) |
|------|---|---|---|
| **搜索方式** | 穷举所有组合 | 随机采样 $n$ 组 | 基于历史智能选择 |
| **效率** | $O(\prod |p_i|)$ | $O(n)$，$n$ 自定 | $O(n)$，收敛更快 |
| **适合** | 超参数少（<4） | 超参数多、范围大 | 超参数多、计算贵 |
| **sklearn** | ✅ 内置 | ✅ 内置 | ❌ 需要 Optuna/Hyperopt |

> 📖 Docs: [sklearn Model Selection](https://scikit-learn.org/stable/modules/grid_search.html)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────┐
│                 Scikit-Learn 核心模块                       │
├──────────────────────────────────────────────────────────┤
│  数据准备                                                  │
│  ├─ preprocessing: 标准化/编码/缺失值                       │
│  ├─ feature_extraction: TF-IDF / 图像特征                  │
│  └─ feature_selection: 特征选择                             │
├──────────────────────────────────────────────────────────┤
│  监督学习模型                                               │
│  ├─ linear_model: 线性/Logistic/Ridge/Lasso               │
│  ├─ svm: SVC / SVR                                        │
│  ├─ tree: DecisionTree                                     │
│  ├─ ensemble: RandomForest / GradientBoosting / AdaBoost  │
│  ├─ neighbors: KNN                                         │
│  └─ naive_bayes: GaussianNB / MultinomialNB               │
├──────────────────────────────────────────────────────────┤
│  无监督学习模型                                             │
│  ├─ cluster: KMeans / DBSCAN / AgglomerativeClustering    │
│  ├─ decomposition: PCA / NMF / TruncatedSVD              │
│  └─ manifold: t-SNE / UMAP (via umap-learn)              │
├──────────────────────────────────────────────────────────┤
│  模型选择与评估                                             │
│  ├─ model_selection: train_test_split / CV / GridSearch   │
│  ├─ metrics: accuracy / F1 / ROC-AUC / MSE / R²          │
│  └─ pipeline: Pipeline / ColumnTransformer                │
└──────────────────────────────────────────────────────────┘
```

> 📖 Docs: [sklearn API Reference](https://scikit-learn.org/stable/modules/classes.html)

### 适用场景 ✅

- 表格数据（结构化数据）的分类、回归、聚类
- 中小规模数据（万~百万级样本）
- 快速原型和实验（统一 API 降低切换成本）
- 特征工程 Pipeline 构建
- 模型选择、交叉验证、超参数调优

### 不适用场景 ❌

- 深度学习任务（图像、NLP、语音）→ 用 PyTorch / TensorFlow
- 大规模分布式训练 → 用 Spark MLlib / Dask-ML
- GPU 加速计算 → 用 cuML (RAPIDS)
- 在线/增量学习（sklearn 部分支持，但不是强项）→ 用 River
- 超大规模梯度提升 → 用 XGBoost / LightGBM（更快更强）

> 📖 Docs: [sklearn Choosing the right estimator](https://scikit-learn.org/stable/machine_learning_map.html)

---


## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| `fit(X, y)` | 训练模型 | `clf.fit(X_train, y_train)` |
| `predict(X)` | 预测 | `clf.predict(X_test)` |
| `predict_proba(X)` | 预测概率 | `clf.predict_proba(X_test)` |
| `transform(X)` | 变换数据 | `scaler.transform(X_test)` |
| `fit_transform(X)` | 训练+变换 | `scaler.fit_transform(X_train)` |
| `score(X, y)` | 评估得分 | `clf.score(X_test, y_test)` |
| `get_params()` | 获取超参数 | `clf.get_params()` |
| `set_params(**p)` | 设置超参数 | `clf.set_params(C=10)` |
| `model.coef_` | 训练后的系数 | 带下划线后缀 = 学到的参数 |
| `Pipeline([...])` | 组合工作流 | `Pipeline([('s', Scaler()), ('m', SVC())])` |

> 📖 Docs: [sklearn API Reference](https://scikit-learn.org/stable/modules/classes.html)
