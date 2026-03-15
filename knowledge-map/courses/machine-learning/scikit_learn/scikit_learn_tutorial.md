---
topic: scikit_learn
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn User Guide — https://scikit-learn.org/stable/user_guide.html"
  - "📖 Docs: scikit-learn API Design — https://scikit-learn.org/stable/developers/develop.html"
  - "💻 Source: scikit-learn/sklearn — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.github/scikit-learn/sklearn"
  - "📚 Book: James et al., ISLR — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
expiry: 6m
status: current
---

# Scikit-Learn 教程

> **前置知识：** Python 基础、NumPy/Pandas、ML 基本概念（分类/回归/聚类）
> **参考来源：** [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html) | [sklearn API Design](https://scikit-learn.org/stable/developers/develop.html)

---


## Section 0: 前置知识速查

1. **NumPy 数组**：`np.array([[1,2],[3,4]])`，sklearn 的输入/输出都是 NumPy 数组
2. **Pandas DataFrame**：`pd.DataFrame(data)`，sklearn 现在也支持 DataFrame 输入
3. **ML 基本概念**：监督学习 = 有标签 (X, y)；无监督学习 = 只有 X；过拟合 = 模型太复杂
4. **训练/测试拆分**：训练集训练模型，测试集评估泛化能力

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.2

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **每个算法自己写接口：** 不同 ML 库 API 不统一。KNN 用 `.classify()`，SVM 用 `.run()`，随机森林用 `.build()` → 切换算法需要大量改代码
- 🔥 **数据预处理与模型脱耦：** 先写 scaler，再写编码器，再写模型，每步手动传数据。稍不注意就数据泄漏（在全数据上 fit scaler 后再 split）
- 🔥 **交叉验证自己写循环：** 手动写 K-fold 循环、收集分数、计算均值标准差 → 枯燥且易出错
- 🔥 **超参数调优手动尝试：** 没有 GridSearch，需要手动嵌套 for 循环遍历 C=[0.01, 0.1, 1, 10] × gamma=[0.001, 0.01, 0.1]

### 它的核心价值

1. **统一 API（一学百通）：** 所有模型 `fit() → predict() / transform()`，切换算法只需换一行
2. **Pipeline（防泄漏+可复用）：** 自动确保预处理只在训练集上 fit，整个流程可序列化/部署
3. **内置 CV + 调参：** `cross_val_score()` 一行搞定；`GridSearchCV()` 自动搜索最优超参数
4. **丰富的模型生态：** 30+ 分类器、20+ 回归器、10+ 聚类器、10+ 降维器，统一在一个库中

> 📖 Docs: [sklearn API Design Principles](https://scikit-learn.org/stable/developers/develop.html)

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 Estimator API 设计哲学

```
                        BaseEstimator
                        ├── get_params()
                        └── set_params()
                              │
                ┌─────────────┼─────────────┐
                │             │             │
          ClassifierMixin  RegressorMixin  TransformerMixin
          ├── predict()   ├── predict()    ├── transform()
          └── score()     └── score()      └── fit_transform()
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                 SVC      Ridge      PCA
```

**五大设计原则（sklearn 论文明确提出）：**

1. **一致性 (Consistency)**：所有 Estimator 有相同的接口
2. **可检视 (Inspection)**：超参数通过构造函数传入，可通过 `get_params()` 检查
3. **非扩展 (Non-proliferation)**：尽量用 NumPy/SciPy 的数据结构
4. **组合性 (Composition)**：Pipeline 和 ColumnTransformer 组合简单模块
5. **合理默认值 (Sensible defaults)**：大部分超参数有经过测试的默认值

> 📖 Docs: [sklearn API Design](https://scikit-learn.org/stable/developers/develop.html)
> 💻 Source: [sklearn/base.py](../../../.github/scikit-learn/sklearn/base.py)

### 2.2 Pipeline 内部工作流

```
Pipeline([('scaler', StandardScaler()),
          ('pca',    PCA(n_components=10)),
          ('svm',    SVC(C=1.0))])

调用 pipeline.fit(X_train, y_train):
    Step 1: scaler.fit_transform(X_train)    → X_scaled
    Step 2: pca.fit_transform(X_scaled)      → X_pca
    Step 3: svm.fit(X_pca, y_train)          (最后一步只 fit)

调用 pipeline.predict(X_test):
    Step 1: scaler.transform(X_test)         → X_scaled  (注意: 只 transform!)
    Step 2: pca.transform(X_scaled)          → X_pca     (只 transform!)
    Step 3: svm.predict(X_pca)               → y_pred
```

**为什么 Pipeline 能防止数据泄漏？** 因为 `.fit()` 只在训练数据上调用，`.transform()` 用训练时学到的参数变换新数据。如果你手动先 `scaler.fit_transform(全数据)`，然后 `train_test_split()`，scaler 已经"看过"测试数据了。

> 📖 Docs: [sklearn Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline)

### 2.3 交叉验证+超参数搜索

```
GridSearchCV(SVC(), param_grid={'C': [0.1,1,10], 'kernel': ['rbf','linear']}, cv=5)

内部执行:
    for C in [0.1, 1, 10]:
        for kernel in ['rbf', 'linear']:
            for fold in range(5):
                model = SVC(C=C, kernel=kernel)
                model.fit(X_train_fold, y_train_fold)
                score = model.score(X_val_fold, y_val_fold)
    
    best_params_ = (C=1, kernel='rbf')  ← 平均得分最高的组合
    best_estimator_ = SVC(C=1, kernel='rbf').fit(X_all_train, y_all_train)
```

> 📖 Docs: [sklearn Grid Search](https://scikit-learn.org/stable/modules/grid_search.html)

---


## Section 3: 局限性

1. **不支持 GPU：** 所有计算在 CPU 上。大数据集训练慢 → 用 cuML (RAPIDS) 或 XGBoost GPU
2. **不支持深度学习：** 没有神经网络层、自动微分 → 用 PyTorch / TensorFlow
3. **内存瓶颈：** 数据必须完全载入内存（不支持 out-of-core 大多数模型）→ 用 Dask-ML / Spark
4. **增量学习有限：** 只有 `partial_fit()` 的模型支持（SGDClassifier, MiniBatchKMeans 等），大部分不支持
5. **梯度提升不如专用库：** `GradientBoostingClassifier` 比 XGBoost/LightGBM 慢得多 → sklearn 1.0 引入 `HistGradientBoosting` 算是追赶

> 📖 Docs: [sklearn Computing](https://scikit-learn.org/stable/computing.html)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **Scikit-Learn** | 统一API、文档极佳、Pipeline | 无GPU、无DL、规模受限 | 表格数据、原型、教学 |
| **XGBoost/LightGBM** | GBDT 极快、GPU支持 | 只做树模型、API 较散 | 竞赛、工业表格数据 |
| **PyTorch** | GPU、自动微分、灵活 | 学习曲线陡、无ML工具 | 深度学习 |
| **Spark MLlib** | 分布式、大数据 | API 不如sklearn、模型种类少 | TB级数据 |
| **cuML (RAPIDS)** | sklearn兼容API + GPU | 需NVIDIA GPU、模型少 | GPU加速传统ML |
| **statsmodels** | 统计推断、p值、置信区间 | 预测能力弱 | 统计分析/假设检验 |

> 📖 Docs: [sklearn Related Projects](https://scikit-learn.org/stable/related_projects.html)

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [sklearn User Guide](https://scikit-learn.org/stable/user_guide.html) | 📖 文档 | 全文（API 设计、Pipeline、CV） |
| [sklearn API Design](https://scikit-learn.org/stable/developers/develop.html) | 📖 文档 | Section 2（设计哲学） |
| [sklearn/base.py 源码](../../../.github/scikit-learn/sklearn/base.py) | 💻 源码 | Section 2（Estimator 继承体系） |
| [《ISLR》Ch.2](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | Section 0（ML 基础概念） |
