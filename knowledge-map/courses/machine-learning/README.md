# Knowledge Map — Machine Learning (ML)

## 主题列表

| 主题 | 状态 | 最后更新 | 描述 |
|------|------|---------|------|
| [DBSCAN](dbscan/) | ✅ 8/8 维度完整 | 2026-03-13 | 密度聚类算法，发现任意形状簇并识别噪声 |
| [K-Means](kmeans/) | ✅ 8/8 维度完整 | 2026-03-13 | Lloyd 算法，最小化 WCSS，适合大规模球形聚类 |
| [SVM](svm/) | ✅ 8/8 维度完整 | 2026-03-13 | 支持向量机，最大间隔分类器 |
| [LOF](lof/) | ✅ 8/8 维度完整 | 2026-03-13 | 局部离群因子，密度估计异常检测 |
| [KNN](knn/) | ✅ 9/9 维度完整 | 2026-03-13 | K 近邻，非参数化分类/回归 |
| [ISF](isf/) | ✅ 9/9 维度完整 | 2026-03-13 | Isolation Forest，基于随机分割的异常检测 |
| [Naive Bayes](naive_bayes/) | ✅ 9/9 维度完整 | 2026-03-13 | 朴素贝叶斯，生成式概率分类器 |
| [Logistic Regression](logistic_regression/) | ✅ 9/9 维度完整 | 2026-03-14 | 逻辑回归，判别式线性分类器，GLM 成员 |
| [Decision Tree](decision_tree/) | ✅ 9/9 维度完整 | 2026-03-14 | 决策树 (CART)，非参数可解释模型，集成方法基石 |
| [Scikit-Learn](scikit_learn/) | ✅ 9/9 维度完整 | 2026-03-14 | Python ML 标准库，统一 Estimator API，Pipeline/CV/GridSearch |

## 添加新主题

参考 `/generate-knowledge-map` 工作流：

```bash
/generate-knowledge-map ml <new-topic>
```

## 来源说明

本目录所有知识地图仅使用白名单来源：
- 📖 原始学术论文（**arXiv 直接下载** `--url https://arxiv.org/abs/xxxx`，不用 Semantic Scholar Search）
- 📚 出版教科书（`textbooks/` 目录）
- 📖 官方文档（scikit-learn, PyTorch...）
- 💻 开源代码（`.github/` 目录）
