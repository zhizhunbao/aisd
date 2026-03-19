---
topic: model_evaluation_metrics
dimension: bridge
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Paper: Raschka, 'Model Evaluation, Model Selection, and Algorithm Selection in ML', arXiv 2020 — file:///C:/Users/40270/Desktop/workspace/aisd/.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf"
expiry: 12m
status: current
---

# Model Evaluation & Metrics 衔接与扩展

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | SVM | 分类器训练后需要评估 | [svm/](../svm/) |
| ← 前置 | Naive Bayes | 分类器训练后需要评估 | [naive_bayes/](../naive_bayes/) |
| ← 前置 | Decision Tree | 分类器训练后需要评估 | [decision_tree/](../decision_tree/) |
| ← 前置 | Logistic Regression | 分类器训练后需要评估 | [logistic_regression/](../logistic_regression/) |
| ← 前置 | KNN | 分类器训练后需要评估 | [knn/](../knn/) |
| → 后续 | 超参数调优 | 用 CV + 指标做参数搜索 | — |
| → 后续 | 不平衡学习 | 用 F1/Recall 评估重采样效果 | — |
| → 后续 | 模型可解释性 | 评估 SHAP 解释的可靠性 | — |
| → 后续 | scikit-learn | Pipeline + GridSearchCV 实现 | [scikit_learn/](../scikit_learn/) |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 概率论 | 条件概率 P(A\|B)、贝叶斯定理 | ROC 曲线的 TPR/FPR 定义、校准曲线的概率解释 |
| 线性代数 | 矩阵表示 | 混淆矩阵本质是一个 2×2（或 n×n）矩阵 |
| 统计学 | 均值、方差、偏差-方差分解 | CV 估计的期望和方差分析、泛化误差分解 |
| 各分类算法 | `predict()` 和 `predict_proba()` 输出 | 评估指标的输入是模型的预测结果 |

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| 超参数调优 | K-Fold CV + scoring 函数 | GridSearchCV 的内层用 CV 做参数搜索 |
| 不平衡学习 | F1、Recall、PR-AUC | 评估 SMOTE/重采样效果时选用正确指标 |
| 集成学习 | OOB error、CV 分数 | Bagging 的 OOB 估计 ≈ LOOCV |
| 神经网络 | Loss curve (训练+验证) | 早停法基于验证集 loss |
| AutoML | 嵌套 CV、多指标排名 | 自动选择最佳模型 |
| 论文写作 | 标准评估流程 | 论文中的实验评估 section |

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 评估方式 | Hold-out 一次划分 | K-Fold CV + 重复 CV | 单次划分方差太大 |
| 分类指标 | 只看 Accuracy | 多指标: F1 + MCC + AUC | 不平衡数据上 Accuracy 不可靠 |
| 阈值选择 | 固定阈值 | ROC/PR 曲线全局分析 | 单一阈值太武断 |
| AUC 选择 | ROC-AUC | ROC-AUC + PR-AUC | ROC-AUC 在不平衡数据上过度乐观 |
| F1 地位 | 标准推荐 | MCC 逐渐被推荐替代 | F1 忽略 TN |

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Raschka 2020](../../../.documents/papers/model_evaluation_metrics/raschka_2020_model_evaluation.pdf) | 📖 论文 | 最全面的评估综述：评估、选择、算法比较三位一体 | ⭐⭐⭐ |
| [ESL Ch.7](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 偏差-方差分解与模型选择的数学基础 | ⭐⭐⭐⭐ |
| [Arlot & Celisse 2010](../../../.documents/papers/model_evaluation_metrics/arlot_celisse_2010_cross_validation.pdf) | 📖 论文 | 交叉验证方法综述：V-fold、LOO、corrected CV | ⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Chicco & Jurman 2020](../../../.documents/papers/model_evaluation_metrics/chicco_jurman_2020_mcc_vs_f1.pdf) | MCC vs F1 系统对比 | 想知道到底该用 F1 还是 MCC |
| [Flach 2020](../../../.documents/papers/model_evaluation_metrics/flach_2020_precision_recall.pdf) | PR 曲线 vs ROC 曲线深度分析 | 想理解两种曲线的数学关系 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [scikit-learn Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) | 完整 API 参考 + 使用指南 | 日常查阅 |
| [Kaggle Evaluation Metrics](https://www.kaggle.com/competitions) | 各比赛使用的评估指标 | 了解业界实际选择 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 分类算法 | 6 | [svm/](../svm/), [naive_bayes/](../naive_bayes/), [knn/](../knn/) | 每个分类器的输出都需要用本主题的指标来评估 |
| 聚类算法 | 2 | [kmeans/](../kmeans/), [dbscan/](../dbscan/) | 聚类用不同的指标（Silhouette），但方法论相通 |
| 异常检测 | 2 | [lof/](../lof/), [isf/](../isf/) | 异常检测评估也用 Precision/Recall/F1，因为类别极度不平衡 |
| sklearn 框架 | 1 | [scikit_learn/](../scikit_learn/) | Pipeline + GridSearchCV 整合了评估流程 |
