---
topic: kmeans
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Lloyd S.P. 1957/1982 IEEE Transactions on Information Theory — https://ieeexplore.ieee.org/document/1056489"
  - "📖 Paper: MacQueen J. 1967 Proceedings 5th Berkeley Symposium — https://projecteuclid.org/euclid.bsmsp/1200512992"
  - "📚 Book: Murphy K.P., Probabilistic Machine Learning An Introduction, Ch.21 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie T. et al., The Elements of Statistical Learning, Ch.13 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📖 Docs: scikit-learn KMeans API — https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html"
expiry: 12m
status: current
---

# K-Means 知识地图

> 📚 Book: Murphy K.P., [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.21 §21.3
> 📖 Paper: Lloyd S.P., ["Least Squares Quantization in PCM"](https://ieeexplore.ieee.org/document/1056489), IEEE Trans. Inf. Theory 1982

## 1. 核心问题

- **K-Means 解决什么问题？** → 给定无标签数据集，将 N 个样本划分为 K 个紧凑簇，最小化簇内方差之和（WCSS）
- **K-Means 算法为什么能收敛？** → 每次迭代：分配步骤减少总距离，更新步骤取均值再次减少，目标函数单调递减，有界，必然收敛
- **如何选择 K？** → Elbow Method（WCSS 拐点）、Silhouette Score、BIC/AIC，或领域知识；无唯一正确答案
- **K-Means 的致命缺陷是什么？** → 对初始化敏感（局部最优）、假设簇为凸形且大小相近、对噪声/离群值敏感

> 📚 Murphy §21.3.7 "Choosing the number of clusters K"; 📖 Lloyd 1982 IEEE

---

## 2. 全景位置

```
机器学习
├── 监督学习
│   └── 分类、回归
└── 无监督学习              ← 你在这里
    ├── 聚类（Clustering）
    │   ├── 【K-Means】        (最小化簇内方差，硬分配，迭代)
    │   ├── 层次聚类 HAC       (树状图，不需要预设 K)
    │   ├── DBSCAN            (密度聚类，无需 K，能发现任意形状)
    │   ├── GMM + EM          (软分配，概率模型，是 K-Means 的概率推广)
    │   └── 谱聚类 Spectral    (图拉普拉斯，能处理非凸簇)
    ├── 降维 / 表征
    │   └── PCA, t-SNE, VAE
    └── 密度估计
```

> 📚 Hastie et al., ESL Ch.13 §13.2.1; Murphy §21.1

---

## 3. 依赖地图

```
前置知识                        本主题                          后续方向
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ 欧氏距离         │─────→│                  │─────→│ K-Means++ (更好初始化)│
│ 均值/方差        │─────→│   K-Means        │─────→│ Mini-Batch K-Means   │
│ 优化（坐标下降） │─────→│   (Lloyd算法)    │─────→│ GMM/EM (软分配推广)  │
│ 向量运算         │─────→│                  │─────→│ 向量量化 VQ / LVQ    │
└─────────────────┘      └──────────────────┘      └──────────────────────┘
```

> 📚 Murphy §21.3.1; 📖 Lloyd 1982

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [kmeans_map.md](kmeans_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [kmeans_concepts.md](kmeans_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [kmeans_math.md](kmeans_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [kmeans_tutorial.md](kmeans_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [kmeans_code.md](kmeans_code.md) | ⑤ 代码 | 快速上手实现 |
| [kmeans_pitfalls.md](kmeans_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [kmeans_history.md](kmeans_history.md) | ⑦ 历史 | 了解技术演进 |
| [kmeans_bridge.md](kmeans_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |

> 📖 当前目录：`knowledge-map/ml/kmeans/`

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [kmeans_map.md](kmeans_map.md) 了解全局位置
2. 读 [kmeans_tutorial.md](kmeans_tutorial.md) Section 1 理解动机
3. 读 [kmeans_concepts.md](kmeans_concepts.md) 掌握核心术语
4. 读 [kmeans_math.md](kmeans_math.md) 手算一次 Lloyd 步骤
5. 跟 [kmeans_code.md](kmeans_code.md) 快速开始跑一个示例
6. 读 [kmeans_history.md](kmeans_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [kmeans_code.md](kmeans_code.md) API 速查表（sklearn 参数）
2. 查 [kmeans_math.md](kmeans_math.md) WCSS 公式速查
3. 查 [kmeans_pitfalls.md](kmeans_pitfalls.md) 排查初始化/K 选择问题

### 深度研究 🔬

1. 读 [kmeans_history.md](kmeans_history.md) 完整演进线
2. 读 [kmeans_bridge.md](kmeans_bridge.md) 探索 GMM、DBSCAN 关系
3. 阅读原始论文：Lloyd 1957/1982, MacQueen 1967, Arthur & Vassilvitskii 2007 (K-Means++)

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-13 | 12m | ✅ current |
| Concepts | 2026-03-13 | 12m | ✅ current |
| Math | 2026-03-13 | 12m | ✅ current |
| Tutorial | 2026-03-13 | 12m | ✅ current |
| Code | 2026-03-13 | 6m | ✅ current |
| Pitfalls | 2026-03-13 | 6m | ✅ current |
| History | 2026-03-13 | never | ✅ current |
| Bridge | 2026-03-13 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Lloyd 1982, IEEE Trans. Inf. Theory](https://ieeexplore.ieee.org/document/1056489) | 📖 论文 | 算法原始来源 |
| [MacQueen 1967, Berkeley Symp.](https://projecteuclid.org/euclid.bsmsp/1200512992) | 📖 论文 | K-Means 命名来源，在线算法变体 |
| [Arthur & Vassilvitskii 2007, SODA](https://dl.acm.org/doi/10.5555/1283383.1283494) | 📖 论文 | K-Means++ 初始化 |
| [《PML1》Ch.21](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 算法、变体、选 K |
| [《ESL》Ch.13](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 原型方法视角、对比 LVQ/GMM |
| [scikit-learn KMeans docs](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html) | 📖 文档 | API 参数说明 |
| [sklearn/cluster/_kmeans.py](../../../.github/scikit-learn/sklearn/cluster/_kmeans.py) | 💻 源码 | 实现参考 |
