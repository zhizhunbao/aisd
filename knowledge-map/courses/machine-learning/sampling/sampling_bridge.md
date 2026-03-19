---
topic: sampling
dimension: bridge
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.7-8,15 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., 《An Introduction to Statistical Learning》 Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
expiry: 12m
status: current
---

# Sampling & Resampling 衔接与扩展

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7-8, 15
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.5

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 过拟合 Overfitting | CV 是检测和对抗过拟合的核心工具 | [overfitting/](../overfitting/overfitting_map.md) |
| ← 前置 | 模型评估指标 Model Evaluation Metrics | 采样方法产出数据，评估指标衡量性能 | [model_evaluation_metrics/](../model_evaluation_metrics/model_evaluation_metrics_map.md) |
| → 后续 | 决策树 Decision Tree | 决策树 + Bootstrap → Bagging/Random Forest | [decision_tree/](../decision_tree/decision_tree_map.md) |
| → 后续 | SVM | SVM 在小样本上依赖 CV 选参 | [svm/](../svm/svm_map.md) |
| → 后续 | KNN | KNN 选择 K 依赖 CV | [knn/](../knn/knn_map.md) |

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 概率论 | 独立同分布 (i.i.d.) | CV 和 Bootstrap 都假设数据 i.i.d.；违反时需用 TimeSeriesSplit |
| [过拟合](../overfitting/overfitting_concepts.md) | 偏差-方差权衡 | K-Fold CV 的 K 选择本质是偏差-方差权衡 |
| [过拟合](../overfitting/overfitting_concepts.md) | 泛化误差 | CV 估计的就是泛化误差 |
| 损失函数 | MSE, 0-1 loss | CV 公式中的 $L(y, \hat{y})$ 就是损失函数 |
| [KNN](../knn/knn_concepts.md) | K 近邻距离 | SMOTE 用 K-NN 找近邻来插值生成合成样本 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.1-7.3

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| [决策树](../decision_tree/decision_tree_map.md) | Bootstrap 采样 | Bagging = Bootstrap + 决策树投票 |
| Random Forest | Bootstrap + 特征子采样 | 每棵树用 Bootstrap 样本 + 随机特征子集 |
| GridSearchCV / RandomizedSearchCV | K-Fold CV | 用 CV 评估每组超参数配置 |
| [模型评估](../model_evaluation_metrics/model_evaluation_metrics_map.md) | Stratified CV | 确保各折类别比例一致 |
| 统计推断 | Bootstrap 置信区间 | 对任意统计量估计标准误差和 CI |
| 不平衡学习 | SMOTE, 欠采样 | 在训练前平衡类别分布 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.8, 15

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 泛化评估 | Holdout (单次划分) | K-Fold CV (多次划分取平均) | 单次划分方差太大，尤其在小数据集 |
| 标准误差估计 | Jackknife (去1个样本) | Bootstrap (有放回全重抽) | 计算机普及使暴力重复计算可行 |
| 不平衡处理 | 简单复制少数类 | SMOTE (特征空间插值) | 复制导致过拟合，插值增加多样性 |
| SMOTE | 全特征空间 K-NN 插值 | Borderline-SMOTE / ADASYN | 只在决策边界附近插值，避免生成噪声 |
| CV 选超参 | 手动尝试 | GridSearchCV + Pipeline | 自动化 + 防数据泄露 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.7.10-7.11

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Efron & Tibshirani "An Introduction to the Bootstrap" (1993)](https://doi.org/10.1007/978-1-4899-4541-9) | 📚 教科书 | Bootstrap 最权威的教科书，覆盖理论和应用 | ⭐⭐⭐ |
| [Efron 1979 原始论文](https://doi.org/10.1214/aos/1176344552) | 📖 论文 | 了解 Bootstrap 的原始思想和与 Jackknife 的关系 | ⭐⭐⭐ |
| [ESL Ch.7.10-7.12](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | CV 和 Bootstrap 的理论分析，.632+ 估计器 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [模型评估指标](../model_evaluation_metrics/model_evaluation_metrics_map.md) | CV 产出数据 + 指标衡量性能 | 想了解 CV 之后用什么指标 |
| [过拟合](../overfitting/overfitting_map.md) | CV 是检测过拟合的工具 | 想了解为什么需要 CV |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [scikit-learn model_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.model_selection) | 所有 CV/Split 工具的 API | 需要查 API |
| [imbalanced-learn User Guide](https://imbalanced-learn.org/stable/user_guide.html) | 不平衡学习全景 | 需要选择不平衡处理方法 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 分类器 | 5+ | [KNN](../knn/), [SVM](../svm/), [Decision Tree](../decision_tree/), [Naive Bayes](../naive_bayes/), [Logistic Regression](../logistic_regression/) | 所有分类器都用 CV 选参和评估 |
| 聚类 | 2 | [K-Means](../kmeans/), [DBSCAN](../dbscan/) | 聚类评估也可用 CV（内部指标） |
| 异常检测 | 2 | [LOF](../lof/), [ISF](../isf/) | 异常检测天然面对类别不平衡 |
| 框架 | 1 | [scikit-learn](../scikit_learn/) | Pipeline + CV 是 sklearn 核心工作流 |
