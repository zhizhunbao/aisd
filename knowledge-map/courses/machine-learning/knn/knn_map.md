---
topic: knn
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cover & Hart, 'Nearest Neighbor Pattern Classification', IEEE Trans. Inform. Theory 1967 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/knn/cover_hart_1967_nearest_neighbor.pdf"
  - "📚 Book: Hastie, Tibshirani, Friedman, 《The Elements of Statistical Learning》 Ch.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: James et al., 《ISLR》 Ch.2,3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/james_ISLR.pdf"
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.16 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn Neighbors User Guide — https://scikit-learn.org/stable/modules/neighbors.html"
  - "💻 Source: sklearn/neighbors/_classification.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py"
expiry: 12m
status: current
---

# KNN 知识地图

> 📚 Book: Hastie et al., [《The Elements of Statistical Learning》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3
> 📖 Paper: Cover & Hart (1967), [Nearest Neighbor Pattern Classification](../../../../.documents/papers/knn/cover_hart_1967_nearest_neighbor.pdf)

## 1. 核心问题

- **KNN 的预测逻辑是什么？** → 找到训练集中距离最近的 k 个点，按多数投票（分类）或均值（回归）输出结果
- **k 怎么选？** → 通过交叉验证；k 小→低偏差高方差，k 大→高偏差低方差
- **距离用什么度量？** → 默认 Minkowski (p=2 即欧氏距离)，需根据数据特征选择
- **KNN 有模型参数吗？** → 没有显式参数，是惰性学习（lazy learning）——训练即存储数据
- **什么情况 KNN 会失效？** → 高维诅咒（维度灾难）、类不平衡、噪声大的特征

> 📚 Book: Hastie et al., [《The Elements of Statistical Learning》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3

---

## 2. 全景位置

```
机器学习
├── 有监督学习 ← 你在这里
│   ├── 参数模型（Parametric）
│   │   ├── 线性回归 / 逻辑回归
│   │   └── SVM, 朴素贝叶斯
│   └── 非参数模型（Non-parametric）
│       ├── 【KNN】 (基于实例、惰性学习)
│       ├── 决策树 (基于规则)
│       └── 核方法 (基于相似度)
├── 无监督学习
│   ├── K-Means (聚类，与KNN同名不同物)
│   ├── DBSCAN (密度聚类)
│   └── LOF (异常检测)
└── 强化学习
```

> 📚 Book: Murphy, [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.16

---

## 3. 依赖地图

```
前置知识                本主题                 后续方向
┌─────────────────┐    ┌──────────────────┐   ┌──────────────────────┐
│ 距离度量         │───→│                  │──→│ 核方法 / SVM         │
│ 欧氏/曼哈顿/余弦 │    │   KNN            │──→│ 决策树/随机森林      │
│ 特征缩放 (归一化)│───→│ (K近邻分类/回归)  │──→│ Approximate NN (ANN) │
│ 偏差-方差权衡    │───→│                  │──→│ LOF 异常检测         │
│ 交叉验证 (CV)   │───→│                  │──→│ KD-Tree / Ball Tree  │
└─────────────────┘    └──────────────────┘   └──────────────────────┘
```

> 📖 Docs: [scikit-learn Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [knn_map.md](knn_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [knn_concepts.md](knn_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [knn_math.md](knn_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [knn_tutorial.md](knn_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [knn_code.md](knn_code.md) | ⑤ 代码 | 快速上手实现 |
| [knn_pitfalls.md](knn_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [knn_history.md](knn_history.md) | ⑦ 历史 | 了解技术演进 |
| [knn_bridge.md](knn_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [knn_first_principles.md](knn_first_principles.md) | ⑨ 第一性 | 理解底层公理 |

> 📖 Docs: [scikit-learn API](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.neighbors)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [knn_map.md](knn_map.md) 了解全局位置
2. 读 [knn_tutorial.md](knn_tutorial.md) Section 1 理解动机
3. 读 [knn_concepts.md](knn_concepts.md) 掌握核心术语
4. 读 [knn_math.md](knn_math.md) 手算一次核心公式
5. 跟 [knn_code.md](knn_code.md) 快速开始跑一个示例
6. 读 [knn_history.md](knn_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [knn_code.md](knn_code.md) API 速查表
2. 查 [knn_math.md](knn_math.md) 公式速查
3. 查 [knn_pitfalls.md](knn_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [knn_history.md](knn_history.md) 完整演进线
2. 读 [knn_bridge.md](knn_bridge.md) 探索下游任务
3. 读 [knn_first_principles.md](knn_first_principles.md) 理解底层公理
4. 阅读原始论文：Cover & Hart (1967)

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
| First Principles | ✅ 已完成 |

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
| First Principles | 2026-03-13 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《The Elements of Statistical Learning》Ch.2](../../../textbooks/hastie_esl.pdf) | 📚 教科书 | 全文核心参考，维度灾难 |
| [《ISLR》Ch.2,3](../../../textbooks/james_ISLR.pdf) | 📚 教科书 | KNN 回归、分类示例 |
| [《Probabilistic Machine Learning》Ch.16](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 非参数方法理论 |
| Cover & Hart (1967), [Nearest Neighbor Pattern Classification](../../../../.documents/papers/knn/cover_hart_1967_nearest_neighbor.pdf) | 📖 论文 | 原始论文，误差界定理 |
| [scikit-learn Neighbors Docs](https://scikit-learn.org/stable/modules/neighbors.html) | 📖 文档 | 算法选择、API 参考 |
| [sklearn/neighbors/_classification.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py) | 💻 源码 | 分类实现 |
