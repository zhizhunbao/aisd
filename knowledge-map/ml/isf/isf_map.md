---
topic: isf
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Liu et al., 'Isolation Forest', ICDM 2008 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Paper: Liu et al., 'Isolation-Based Anomaly Detection', TKDD 2012 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Docs: scikit-learn IsolationForest — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html"
  - "💻 Source: scikit-learn _iforest.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py"
expiry: 12m
status: current
---

# Isolation Forest (ISF) 知识地图

> 📖 Paper: Liu et al., [Isolation Forest](https://doi.org/10.1109/ICDM.2008.17), ICDM 2008
> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

## 1. 核心问题

- **什么是 Isolation Forest？** → 一种基于随机分割树的无监督异常检测算法；异常点因特征稀疏而被"隔离"得更快（路径更短）
- **它和 LOF 的根本区别是什么？** → LOF 基于局部密度比较（测距离），ISF 基于路径长度（测隔离难度）；ISF 线性时间，LOF 平方时间
- **为什么路径短 = 异常？** → 异常点在特征空间中孤立、稀疏，随机切割很快就能将其单独隔离；正常点紧密聚集，需要更多切割
- **如何量化"异常分数"？** → 对所有 iTree 的路径长度取均值，再用 BST 期望路径长度 c(n) 做归一化，输出 [0,1] 分数，越接近 1 越异常
- **什么时候用 ISF，什么时候用其他方法？** → 数据量大（>10k）、高维、无标签时首选 ISF；低维密度异常用 LOF；已知分布用 EllipticEnvelope

> 📖 Paper: Liu et al., [Isolation Forest](https://doi.org/10.1109/ICDM.2008.17), ICDM 2008

---

## 2. 全景位置

```
机器学习
├── 监督学习
│   └── 分类、回归
├── 无监督学习
│   ├── 聚类
│   │   ├── K-Means
│   │   ├── DBSCAN
│   │   └── 层次聚类
│   └── 异常检测 ← 你在这里
│       ├── 【Isolation Forest (ISF)】 (基于路径长度，线性，高维友好)
│       ├── LOF (基于局部密度，适合低维复杂形状)
│       ├── One-Class SVM (基于支持向量，适合中等规模)
│       └── EllipticEnvelope (基于协方差，假设高斯分布)
└── 半监督学习
```

> 📖 Docs: [scikit-learn 异常检测对比](https://scikit-learn.org/stable/modules/outlier_detection.html)

---

## 3. 依赖地图

```

前置知识                    Isolation Forest                后续方向
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│ 决策树/随机分割  │──────→│                      │──────→│ Extended Isolation    │
│ 随机采样        │──────→│ Isolation Forest     │──────→│ Forest (EIF)         │
│ BST 期望路径长度 │──────→│                      │──────→│ SCiForest            │
│ 集成学习思想    │──────→│                      │──────→│ 流式/在线异常检测    │
└─────────────────┘       └──────────────────────┘       └──────────────────────┘

```

> 📖 Paper: Liu et al., ICDM 2008

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [isf_map.md](isf_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [isf_concepts.md](isf_concepts.md) | ② 概念 | 理解术语定义（iTree, 路径长度, 归一化分数） |
| [isf_math.md](isf_math.md) | ③ 公式 | 推导异常分数公式、理解 c(n) 归一化 |
| [isf_tutorial.md](isf_tutorial.md) | ④ 教程 | Why-First 理解设计动机与核心机制 |
| [isf_code.md](isf_code.md) | ⑤ 代码 | 快速上手 sklearn IsolationForest |
| [isf_pitfalls.md](isf_pitfalls.md) | ⑥ 踩坑 | 调试异常分数异常、参数不当等问题 |
| [isf_history.md](isf_history.md) | ⑦ 历史 | 了解从朴素树隔离到 ISF 的演进 |
| [isf_bridge.md](isf_bridge.md) | ⑧ 衔接 | 找相关主题（LOF/DBSCAN/EIF）、扩展阅读 |
| [isf_first_principles.md](isf_first_principles.md) | ⑨ 第一性原理 | 从公理推导为什么路径长度能检测异常 |

> 📖 Docs: [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [isf_map.md](isf_map.md) 了解全局位置
2. 读 [isf_tutorial.md](isf_tutorial.md) Section 1 理解动机（为什么用路径长度？）
3. 读 [isf_concepts.md](isf_concepts.md) 掌握核心术语（iTree, path length, c(n)）
4. 读 [isf_math.md](isf_math.md) 手算一次异常分数
5. 跟 [isf_code.md](isf_code.md) 快速开始跑一个检测示例
6. 读 [isf_history.md](isf_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [isf_code.md](isf_code.md) API 速查表（参数含义）
2. 查 [isf_math.md](isf_math.md) 公式速查（score 计算方式）
3. 查 [isf_pitfalls.md](isf_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [isf_history.md](isf_history.md) 完整演进线
2. 读 [isf_bridge.md](isf_bridge.md) 探索 EIF/SCiForest 等后继
3. 阅读原始论文 Liu et al. ICDM 2008 + TKDD 2012

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
| [Liu et al. ICDM 2008](https://doi.org/10.1109/ICDM.2008.17) | 📖 论文 | 全文核心参考（原始算法） |
| [Liu et al. TKDD 2012](https://doi.org/10.1145/2133360.2133363) | 📖 论文 | Math, History（改进版，详细分析） |
| [scikit-learn IsolationForest docs](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) | 📖 文档 | Code, Pitfalls |
| [sklearn._iforest.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py) | 💻 源码 | Code（实现细节） |
