---
topic: dbscan
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Ester et al. KDD 1996 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/dbscan/ester_1996_dbscan.pdf"
  - "📖 Paper: Schubert et al. TODS 2017 — https://doi.org/10.1145/3068335"
  - "📖 Docs: scikit-learn DBSCAN — https://scikit-learn.org/stable/modules/clustering.html#dbscan"
expiry: 12m
status: current
---

# DBSCAN 知识地图

> 📖 Paper: Ester et al., [A Density-Based Algorithm...](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf), KDD 1996
> 📖 Docs: [scikit-learn DBSCAN](https://scikit-learn.org/stable/modules/clustering.html#dbscan)

---

## 1. 核心问题

- **DBSCAN 解决什么问题？** → 在没有预设簇数量的情况下，发现任意形状的密度连通簇，并显式识别噪声点
- **为什么用密度而不是距离？** → 基于距离的中心（K-Means）只能找球形簇；密度传播可以"爬过"任意弯曲形状
- **ε 和 min_samples 如何选？** → 用 k-NN 距离图找"肘部"确定 ε；min_samples 通常 ≥ 维度数 + 1
- **DBSCAN 什么情况下失效？** → 不同密度的簇（单一 ε 无法适配）、高维数据（维度诅咒）

> 📖 Paper: Ester et al., KDD 1996, Sec. 1 (Introduction) + Sec. 4 (Parameter Selection)

---

## 2. 全景位置

```
无监督学习
├── 聚类 (Clustering)
│   ├── 基于划分
│   │   ├── K-Means         (需预设 K，仅球形簇)
│   │   └── K-Medoids
│   ├── 基于层次
│   │   └── Agglomerative   (树状结构，O(n²))
│   ├── 基于密度                        ← 你在这里
│   │   ├── 【DBSCAN】      (ε+MinPts，任意形状，噪声识别)
│   │   ├── OPTICS          (DBSCAN 的有序点版本)
│   │   └── HDBSCAN         (层次密度，自适应)
│   └── 基于模型
│       └── GMM             (软分配，概率输出)
└── 降维 (Dimensionality Reduction)
    └── UMAP / PCA          (常与 DBSCAN 组合使用)
```

> 📖 Docs: [sklearn 聚类概览](https://scikit-learn.org/stable/modules/clustering.html#overview-of-clustering-methods)

---

## 3. 依赖地图

```
前置知识                          DBSCAN                        后续方向
┌──────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│ 距离度量          │──────→│                     │──────→│ HDBSCAN (变密度)    │
│ (欧氏/余弦)      │       │   DBSCAN            │──────→│ OPTICS (有序点)     │
│ 邻域搜索结构      │──────→│   ε-邻域 + MinPts   │──────→│ 异常检测            │
│ (KD-Tree)        │       │   密度可达链传播      │──────→│ 地理空间分析        │
│ StandardScaler   │──────→│                     │──────→│ GPS 轨迹聚类        │
└──────────────────┘       └─────────────────────┘       └─────────────────────┘
```

> 📖 Paper: Ester et al., KDD 1996, Sec. 2 (Definitions)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [dbscan_map.md](dbscan_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [dbscan_concepts.md](dbscan_concepts.md) | ② 概念 | 理解核心点/边界点/噪声点/密度可达等术语 |
| [dbscan_math.md](dbscan_math.md) | ③ 公式 | 推导 ε-邻域/密度可达/密度相连公式 |
| [dbscan_tutorial.md](dbscan_tutorial.md) | ④ 教程 | 理解为什么用密度、ε 怎么选、和 K-Means 比较 |
| [dbscan_code.md](dbscan_code.md) | ⑤ 代码 | sklearn DBSCAN 快速上手、k-NN 距离图、可视化 |
| [dbscan_pitfalls.md](dbscan_pitfalls.md) | ⑥ 踩坑 | 忘记标准化、Silhouette 计算错、eps 选错 |
| [dbscan_history.md](dbscan_history.md) | ⑦ 历史 | K-Means 局限 → DBSCAN 诞生 → OPTICS → HDBSCAN |
| [dbscan_bridge.md](dbscan_bridge.md) | ⑧ 衔接 | 上游 K-Means、下游 HDBSCAN、扩展阅读 |

> 📖 Paper: Ester et al., KDD 1996

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [dbscan_map.md](dbscan_map.md) 了解全局位置
2. 读 [dbscan_tutorial.md](dbscan_tutorial.md) Section 1 理解动机（DBSCAN 解决了什么）
3. 读 [dbscan_concepts.md](dbscan_concepts.md) 掌握核心术语（核心点/边界点/噪声点/密度可达）
4. 读 [dbscan_math.md](dbscan_math.md) 手算一次 ε-邻域与密度相连
5. 跟 [dbscan_code.md](dbscan_code.md) 快速开始跑一个示例
6. 读 [dbscan_history.md](dbscan_history.md) 了解技术演进（1996 → HDBSCAN）

### 日常参考 🔧

1. 查 [dbscan_code.md](dbscan_code.md) API 速查表（eps/min_samples/labels_）
2. 查 [dbscan_math.md](dbscan_math.md) 公式速查
3. 查 [dbscan_pitfalls.md](dbscan_pitfalls.md) 排查问题（标准化、评估指标、大数据内存）

### 深度研究 🔬

1. 读 [dbscan_history.md](dbscan_history.md) 完整演进线
2. 读 [dbscan_bridge.md](dbscan_bridge.md) 探索 HDBSCAN、OPTICS 等下游方向
3. 阅读原始论文: [Ester et al. KDD 1996](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf) + [Schubert et al. TODS 2017](https://doi.org/10.1145/3068335)

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
| [Ester et al. KDD 1996](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf) | 📖 论文 | 全文核心参考（算法定义、参数选择、实验） |
| [Schubert et al. TODS 2017](https://doi.org/10.1145/3068335) | 📖 论文 | Pitfalls + Code（实现差异、常见误用） |
| [Campello et al. 2013 HDBSCAN](../../../.documents/papers/dbscan/campello_2013_hdbscan.pdf) | 📖 论文 | History + Bridge（后续演进） |
| [sklearn DBSCAN](https://scikit-learn.org/stable/modules/clustering.html#dbscan) | 📖 文档 | Code + Pitfalls（API 用法、注意事项） |
| [sklearn _dbscan.py](../../../.github/scikit-learn/sklearn/cluster/_dbscan.py) | 💻 源码 | Code（实现细节、参数默认值） |
