---
topic: knn
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Cover & Hart, 'Nearest Neighbor Pattern Classification', IEEE Trans. Inform. Theory 1967 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/knn/cover_hart_1967_nearest_neighbor.pdf"
  - "📚 Book: Hastie, Tibshirani, Friedman, 《ESL》 Ch.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Murphy, 《PML1》 Ch.16 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn Neighbors — https://scikit-learn.org/stable/modules/neighbors.html"
expiry: 12m
status: current
---

# KNN 核心概念

> 📚 Book: Hastie et al., [《The Elements of Statistical Learning》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.3
> 📖 Paper: Cover & Hart (1967), [Nearest Neighbor Pattern Classification](../../../../.documents/papers/knn/cover_hart_1967_nearest_neighbor.pdf)

---

## 术语定义

### K 近邻（K-Nearest Neighbors, KNN）

KNN 是一种基于实例的非参数惰性学习算法。它的核心思想极为直观：**预测一个新点的标签，就看它周围 k 个最近邻居怎么说**。分类时取多数票，回归时取平均值。"惰性"意味着它在训练阶段不做任何数学建模，训练集本身就是模型。

> 易混淆：**KNN vs K-Means** — KNN 是有监督学习（需要标签），K-Means 是无监督聚类（不需要标签）；两者都用 "k" 和距离，但目的完全不同

### k（邻居数量）

查询时选取的最近邻居数量，是 KNN 最关键的超参数。

- **k=1**：完全记住训练数据，泛化能力差（高方差）
- **k=N**（训练集大小）：退化为全局多数类预测（高偏差）
- **最优 k**：通过交叉验证选择，通常取奇数（避免平票）

> 易混淆：**k in KNN vs k in K-Means** — KNN 的 k 是查询邻居数，K-Means 的 k 是聚类中心数，含义不同

### 距离度量（Distance Metric）

衡量两个样本点之间相似性的函数。KNN 的性能高度依赖距离度量的选择。

常用距离：
- **Minkowski 距离** ($p$ 参数控制)：$L_p$ 范数的通用形式
- **欧氏距离 (Euclidean)**：$p=2$，几何直线距离，适合连续特征
- **曼哈顿距离 (Manhattan)**：$p=1$，适合高维稀疏数据
- **余弦相似度**：适合文本/向量方向相似性

> 易混淆：**欧氏距离 vs 余弦相似度** — 欧氏度量绝对位置差异，余弦度量向量方向差异；同一数据集两者结果可以完全不同

### 惰性学习（Lazy Learning）

与"积极学习"（Eager Learning，如决策树、SVM）对立的学习范式。惰性学习**在训练时不构建显式判别函数**，而是将所有计算推迟到预测时。

- **优点**：训练极快（O(1)），能自然适应数据分布局部变化
- **缺点**：预测慢（需遍历/查询所有训练点），内存消耗大

> 📚 Book: Murphy, [《Probabilistic Machine Learning》](../../../textbooks/murphy_pml1.pdf), Ch.16

### 维度灾难（Curse of Dimensionality）

随着特征维度 $d$ 增加，数据点在空间中变得极度稀疏，"最近邻"在几何上不再有意义——在高维空间中，所有点的距离趋向相等。

直觉：在 $d$ 维超立方体中，要覆盖 $r$ 比例的体积，需要边长 $r^{1/d}$ 的超正方体。当 $d=10, r=0.01$ 时，需要边长 80% 的正方体——"局部"变得不局部了。

> 易混淆：**维度灾难 vs 过拟合** — 维度灾难是几何问题（距离失效），过拟合是统计问题（模型太复杂）；两者都随维度增加恶化，但机制不同

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.5

---

## 概念辨析

### KNN 分类 vs KNN 回归

| 维度 | KNN 分类 | KNN 回归 |
|------|---------|---------|
| **输出** | 离散类别标签 | 连续数值 |
| **聚合方式** | 多数投票（uniform）或加权投票（distance） | k 邻居目标值的均值或加权均值 |
| **评估指标** | 准确率、F1、AUC | MSE、MAE、R² |
| **典型应用** | 手写数字识别、医学诊断 | 房价预测、年龄估计 |

> 📖 Docs: [scikit-learn KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

### KD-Tree vs Ball Tree vs Brute Force

| 维度 | Brute Force | KD-Tree | Ball Tree |
|------|-------------|---------|-----------|
| **查询复杂度** | $O(n \cdot d)$ | $O(d \log n)$ 低维时 | $O(d \log n)$ 高维更好 |
| **构建复杂度** | $O(1)$ | $O(n \log n)$ | $O(n \log n)$ |
| **适用维度** | 任意（少量数据） | $d \leq 20$ | $d > 20$ |
| **数据形状** | 任意 | 轴对齐切割 | 球体划分 |
| **sklearn 默认** | metric=precomputed 或稀疏 | auto 低维 | auto 高维 |

> 💻 Source: [sklearn/neighbors/_classification.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_classification.py) line 71-78

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────────┐
│                        KNN 算法架构                               │
├──────────────────────────────────────────────────────────────────┤
│  超参数                                                           │
│  ├─ k（邻居数）        — 控制偏差-方差权衡                         │
│  ├─ 距离度量           — Minkowski/Euclidean/Manhattan/Cosine     │
│  ├─ weights           — uniform / distance（距离加权）            │
│  └─ algorithm        — auto / kd_tree / ball_tree / brute        │
├──────────────────────────────────────────────────────────────────┤
│  训练阶段（惰性）                                                  │
│  └─ 存储所有训练样本 (X_train, y_train)                            │
├──────────────────────────────────────────────────────────────────┤
│  预测阶段                                                         │
│  ├─ Step 1: 计算查询点与所有训练点的距离                            │
│  ├─ Step 2: 选取最近的 k 个邻居                                    │
│  ├─ Step 3: 分类→多数投票 / 回归→均值                              │
│  └─ Step 4: 返回预测结果                                           │
└──────────────────────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn/neighbors/_base.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_base.py)

### 适用场景 ✅

- 数据量较小（n < 10万），特征维度不高（d < 30）
- 决策边界非线性、复杂，不适合线性模型
- 需要快速原型验证，或作为其他模型的基线
- 数据局部结构明显（同类样本聚集）
- 多分类问题，类别数量多

### 不适用场景 ❌

- 高维数据（d > 50）——维度灾难导致距离失效
- 大数据集（n > 100万）——预测时间 O(n·d) 不可接受
- 数据有大量噪声特征——所有特征等权重对距离的负面影响
- 类别严重不平衡——多数类主导投票
- 需要模型可解释性——KNN 无法提供特征重要性

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.2 §2.5

---

## 速查表

| 属性 | 值 |
|------|----|
| 算法类型 | 非参数、惰性学习、基于实例 |
| 训练时间复杂度 | $O(1)$（仅存储数据） |
| 预测时间复杂度 | $O(n \cdot d)$ brute force，$O(d \log n)$ 有索引 |
| 空间复杂度 | $O(n \cdot d)$ |
| 关键超参数 | k, metric, weights, algorithm |
| 需要特征缩放？ | ✅ 必须（StandardScaler / MinMaxScaler） |
| 处理缺失值？ | ❌ 不直接支持，需预处理 |
| 多输出支持？ | ✅ |
| sklearn 类 | `KNeighborsClassifier`, `KNeighborsRegressor` |

> 📖 Docs: [scikit-learn Neighbors](https://scikit-learn.org/stable/modules/neighbors.html)
