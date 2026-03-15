---
topic: decision_tree
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Murphy, PML1 Ch.18 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: James et al., ISLR Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
expiry: 12m
status: current
---

# Decision Tree 衔接与扩展

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9-10
> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.8

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 信息论 (Entropy) | 信息增益是 DT 的分割准则 | — |
| ← 前置 | Logistic Regression | 对比：线性 vs 非线性决策边界 | [logistic_regression_bridge.md](../logistic_regression/logistic_regression_bridge.md) |
| → 后续 | **Random Forest** | Bagging + 随机特征子集的 DT 集成 | — |
| → 后续 | **Gradient Boosting** | 依次拟合残差的 DT 序列 | — |
| → 后续 | **XGBoost / LightGBM** | 工程化 GBDT | — |
| → 后续 | **AdaBoost** | 加权 DT 序列 | — |
| ↔ 平行 | SVM | 比较最大间隔 vs 不纯度下降 | [svm_bridge.md](../svm/svm_bridge.md) |
| ↔ 平行 | KNN | 比较参数 vs 非参数模型 | [knn_bridge.md](../knn/knn_bridge.md) |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9-10

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|----------|-----------|-------------------|
| 信息论 | Shannon 信息熵 $H=-\sum p\log p$ | 作为分割准则（ID3/C4.5 用信息增益） |
| 概率论 | 条件概率、频率估计 | 叶子节点的类别比例估计 + predict_proba |
| 贪心算法 | 局部最优选择 | 每个节点选择当前最优分割 |
| 交叉验证 | k-fold CV | 选择最优剪枝参数 $\alpha$ |
| 偏差-方差理论 | 方差分解 | 解释 DT 为什么高方差 → 集成降方差 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2.9, Ch.7

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|----------|-----------------|-----------------|
| **Random Forest** | DT 作为基学习器 | 多棵 DT + Bootstrap + 随机特征子集 |
| **Gradient Boosting** | DT 拟合残差 | 序列 DT, 每棵修正前面的误差 |
| **XGBoost** | CART 分割 + 正则化 | 加入二阶梯度 + 列采样 + 正则化剪枝 |
| **LightGBM** | 直方图近似分割 | 用 histogram 加速分割点搜索 |
| **AdaBoost** | 加权误分类的 DT | 提高难样本权重 → 集中学习 |
| **SHAP** | 树结构 → 精确 Shapley 值 | Tree SHAP 算法：$O(TLD)$ 精确归因 |
| **特征工程** | 特征重要性 (MDI) | 快速筛选重要特征 |
| **规则提取** | 根到叶路径 → if-then 规则 | 模型可解释性、业务规则生成 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.10, Ch.15

---

## 概念演变追踪

| 概念 | 在早期/经典中 | 在现代/实践中 | 变化原因 |
|------|-------------|-------------|---------|
| 分割准则 | 信息增益 (ID3) | Gini 不纯度 (CART/sklearn) | Gini 计算更快，效果相当 |
| 多路 vs 二叉 | ID3/C4.5 多路分割 | CART 二叉分割 (sklearn) | 二叉更简单且可处理连续特征 |
| 剪枝 | 无 (ID3) / MDL (C4.5) | CCP (CART/sklearn) | CCP 用 CV 选择，更系统化 |
| 定位 | 独立的分类/回归模型 | 集成方法的基学习器 | 单棵树太弱，但作为集成组件极强 |
| 缺失值 | 不支持 (ID3) | 原生支持 (sklearn ≥1.4) | 实际数据总有缺失值 |
| 特征重要性 | MDI (树内部) | Permutation / SHAP | MDI 对高基数有偏 |
| 解释方式 | 看树结构 | SHAP 精确归因 | 需要定量而非定性的解释 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.18

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [《ESL》Ch.9](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | CART 完整理论、剪枝、变量重要性 | ⭐⭐⭐ |
| [《ISLR》Ch.8](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | 最友好的入门、R 代码示例 | ⭐⭐ |
| Quinlan 1986 原始 ID3 论文 | 📖 论文 | 信息增益的起源 | ⭐⭐⭐ |
| Breiman 1984 CART 书 | 📖 论文/书 | CART 完整算法 + 统计分析 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|-------|
| [Logistic Regression](../logistic_regression/logistic_regression_map.md) | 线性 vs 非线性边界 | 理解模型假设的影响 |
| [SVM](../svm/svm_map.md) | 间隔最大化 vs 不纯度下降 | 对比判别式模型 |
| [KNN](../knn/knn_map.md) | 两种非参数方法的特点 | 对比非参数模型 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|-------|
| [《ESL》Ch.10](../../../textbooks/hastie_esl.pdf) | Boosting | 学完 DT 后理解 GBDT |
| [《ESL》Ch.15](../../../textbooks/hastie_esl.pdf) | Random Forest | 学完 DT 后理解 RF |
| [XGBoost docs](https://xgboost.readthedocs.io) | 工程化 GBDT | 需要高性能树模型时 |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.9-10

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 线性分类器 | 2 | [Logistic Regression](../logistic_regression/logistic_regression_map.md), [SVM](../svm/svm_map.md) | DT 的非线性优势 vs 线性模型的稳定性 |
| 生成式分类器 | 1 | [Naive Bayes](../naive_bayes/naive_bayes_map.md) | 判别式(DT) vs 生成式(NB)：两种建模哲学 |
| 非参数方法 | 1 | [KNN](../knn/knn_map.md) | 两种非参数模型各有特色：DT 快、KNN 简单 |
| 异常检测 | 2 | [ISF](../isf/isf_map.md), [LOF](../lof/lof_map.md) | ISF 内部就是用的隔离树（DT 的变体） |
| 聚类 | 2 | [K-Means](../kmeans/kmeans_map.md), [DBSCAN](../dbscan/dbscan_map.md) | DT 可做监督特征发现，与聚类互补 |
