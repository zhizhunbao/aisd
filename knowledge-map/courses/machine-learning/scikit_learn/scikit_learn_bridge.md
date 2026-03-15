---
topic: scikit_learn
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: scikit-learn Related Projects — https://scikit-learn.org/stable/related_projects.html"
  - "📖 Docs: scikit-learn User Guide — https://scikit-learn.org/stable/user_guide.html"
  - "📚 Book: Hastie et al., ESL — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
expiry: 6m
status: current
---

# Scikit-Learn 衔接与扩展

> 📖 Docs: [scikit-learn Related Projects](https://scikit-learn.org/stable/related_projects.html)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Python + NumPy/Pandas | sklearn 的数据结构基础 | — |
| ← 前置 | 线性代数 + 统计学 | 算法的数学基础 | [differentiation_map.md](../../math/differentiation/differentiation_map.md) |
| ← 前置 | ML 基础概念 | 分类/回归/聚类/降维的理论基础 | — |
| → 后续 | XGBoost / LightGBM | 更强的梯度提升（sklearn API 兼容） | — |
| → 后续 | PyTorch / TensorFlow | 深度学习（sklearn 不覆盖的领域） | — |
| → 后续 | 模型部署 (ONNX, MLflow) | 将 sklearn Pipeline 导出部署 | — |
| → 后续 | AutoML (TPOT, auto-sklearn) | 自动化 sklearn Pipeline 构建 | — |

> 📖 Docs: [sklearn Related Projects](https://scikit-learn.org/stable/related_projects.html)

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 sklearn 中如何使用 |
|---------|-----------|---------------------|
| NumPy | ndarray、矩阵运算 | 所有输入/输出的数据结构 |
| SciPy | 稀疏矩阵、优化器、距离度量 | KNN 距离、SVM 优化、稀疏特征 |
| Pandas | DataFrame | `set_output('pandas')` 支持 |
| 线性代数 | SVD、特征分解 | PCA、Ridge 的核心实现 |
| 概率论 | 贝叶斯定理、概率分布 | NaiveBayes、GMM |
| 优化 | 梯度下降、坐标下降 | Logistic/Lasso 的求解器 |

> 📖 Docs: [sklearn Computing](https://scikit-learn.org/stable/computing.html)

---

## 下游影响

| 去向主题 | sklearn 提供的概念 | 在下游如何被使用 |
|---------|------------------|----------------|
| XGBoost / LightGBM | 兼容 API、Pipeline | `xgb.XGBClassifier` 可直接放入 Pipeline |
| PyTorch | 预处理/评估 | 用 sklearn 做特征工程 + metrics 评估 |
| MLflow | Pipeline 序列化 | `mlflow.sklearn.log_model(pipeline)` |
| ONNX | 模型导出 | `skl2onnx` 将 Pipeline 转为 ONNX 格式 |
| auto-sklearn / TPOT | AutoML | 自动搜索最优 sklearn Pipeline |
| cuML (RAPIDS) | API 兼容 | GPU 版 sklearn，API 几乎相同 |

> 📖 Docs: [sklearn Related Projects](https://scikit-learn.org/stable/related_projects.html)

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 数据输入 | 只支持 NumPy 数组 | 支持 Pandas DataFrame + `set_output` | 用户友好性提升 |
| 梯度提升 | `GradientBoostingClassifier`（慢） | `HistGradientBoostingClassifier`（快） | 追赶 XGBoost 性能 |
| 类别编码 | 只有 `LabelEncoder`/`OrdinalEncoder` | 新增 `TargetEncoder` | 更丰富的编码选择 |
| 聚类 | KMeans / DBSCAN | 新增 `HDBSCAN` (v1.3) | 更强的密度聚类 |
| 超参数搜索 | `GridSearchCV`（穷举） | + `HalvingGridSearchCV`（淘汰式） | 搜索效率提升 |
| 元数据路由 | 不支持 | `set_*_request()` 元数据路由 (v1.3+) | Pipeline 中传递样本权重等元数据 |

> 📖 Docs: [sklearn Changelog](https://scikit-learn.org/stable/whats_new.html)

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [《ESL》](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | sklearn 所有算法的数学基础 | ⭐⭐⭐⭐ |
| [《ISLR》](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | 统计学习入门 | ⭐⭐ |
| [sklearn 源码](../../../.github/scikit-learn/sklearn/) | 💻 源码 | 理解实现细节 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| XGBoost 文档 | GBDT 实现对比 | 需要更快的 GBDT 时 |
| PyTorch 文档 | 深度学习 vs 传统 ML | 任务需要 DL 时 |
| cuML 文档 | GPU 加速 sklearn | 数据量太大 CPU 太慢时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| MLflow 文档 | 模型实验追踪 + 部署 | 项目进入工业化时 |
| TPOT/auto-sklearn | AutoML 管道 | 想自动化 Pipeline 搜索时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| ML 算法 | 9 | [knn](../knn/), [svm](../svm/), [decision_tree](../decision_tree/), [logistic_regression](../logistic_regression/) | 这些都使用 sklearn 实现 |
| ML 算法 | 3 | [kmeans](../kmeans/), [dbscan](../dbscan/), [naive_bayes](../naive_bayes/) | 聚类/分类的 sklearn 实现 |
| ML 算法 | 2 | [lof](../lof/), [isf](../isf/) | 异常检测的 sklearn 实现 |
| 数学基础 | 3 | [differentiation](../../math/differentiation/), [integration_summation](../../math/integration_summation/) | sklearn 算法的数学依赖 |
