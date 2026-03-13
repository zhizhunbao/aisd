# Knowledge Map — Machine Learning (ML)

## 主题列表

| 主题 | 状态 | 最后更新 | 描述 |
|------|------|---------|------|
| [DBSCAN](dbscan/) | ✅ 8/8 维度完整 | 2026-03-13 | 密度聚类算法，发现任意形状簇并识别噪声 |
| [K-Means](kmeans/) | ✅ 8/8 维度完整 | 2026-03-13 | Lloyd 算法，最小化 WCSS，适合大规模球形簇聚类 |
| [SVM](svm/) | ✅ 8/8 维度完整 | 2026-03-13 | 支持向量机，最大间隔分类器 |

## 添加新主题

参考 `/generate-knowledge-map` 工作流：

```bash
/generate-knowledge-map ml <new-topic>
```

## 来源说明

本目录所有知识地图仅使用白名单来源：
- 📖 原始学术论文（arXiv, ACM, IEEE）
- 📚 出版教科书（`textbooks/` 目录）
- 📖 官方文档（scikit-learn, PyTorch...）
- 💻 开源代码（`.github/` 目录）
