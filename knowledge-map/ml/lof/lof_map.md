---
topic: lof
dimension: map
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Breunig et al. SIGMOD 2000 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/lof/breunig_2000_lof.pdf"
  - "📖 Docs: scikit-learn LocalOutlierFactor — https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html"
  - "💻 Source: scikit-learn _lof.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/neighbors/_lof.py"
expiry: 12m
status: current
---

# LOF 知识地图

> 📖 Paper: Breunig et al., [《LOF: Identifying Density-Based Local Outliers》](../../../.documents/papers/lof/breunig_2000_lof.pdf), SIGMOD 2000
> 📖 Docs: [scikit-learn LocalOutlierFactor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)

## 1. 核心问题

- **LOF 是如何定义"异常"的？** → 通过对比一个点与其邻居的局部密度之比；比值远大于 1 则为异常
- **为什么要用"局部"密度而不是全局密度？** → 不同区域密度差异悬殊，全局阈值会漏判或误判处于稀疏簇边缘的点
- **k-distance、reach-dist、LRD、LOF 这四个量是什么关系？** → 逐层递进：k-distance 定义邻域 → reach-dist 平滑距离 → LRD 估计密度 → LOF 对比密度比
- **LOF ≈ 1 / >> 1 / << 1 分别意味着什么？** → ≈1 正常内点；>>1 局部异常值；<<1 处于比邻居更密集的核心区域
- **novelty=False vs novelty=True 有何区别？** → False 只能对训练集检测；True 支持对新数据预测，但训练集结果可能差异

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 3-4

---

## 2. 全景位置

```
异常检测 (Anomaly Detection)
├── 统计方法 (Statistical)
│   ├── Z-Score / 3σ
│   └── Grubbs Test
├── 基于距离的方法 (Distance-based)
│   ├── kNN 距离异常
│   └── 基于隔离的 (Isolation Forest)
├── 基于密度的方法 (Density-based)  ← 你在这里
│   ├── 【LOF】                      (局部密度比，软分数)
│   ├── LOCI                         (多粒度 LOF 变体)
│   ├── COF                          (连通性 LOF 变体)
│   └── HDBSCAN outlier score        (基于聚类的异常)
├── 基于重建的方法 (Reconstruction)
│   ├── Autoencoder
│   └── PCA 重建误差
└── 基于模型/分类 (Model-based)
    └── One-Class SVM
```

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 1 (Introduction)

---

## 3. 依赖地图

```
前置知识                        本主题                          后续方向
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ k-NN 邻域搜索   │─────→│                  │─────→│ COF / LoOP 变体      │
│ 距离度量         │─────→│   LOF (局部离群  │─────→│ HDBSCAN 异常分数     │
│ 密度估计概念     │─────→│   因子)           │─────→│ 流式/增量异常检测    │
│ DBSCAN 密度思想 │─────→│                  │─────→│ 高维异常检测         │
└─────────────────┘      └──────────────────┘      └──────────────────────┘
```

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Sec. 2 (Related Work)

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [lof_map.md](lof_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [lof_concepts.md](lof_concepts.md) | ② 概念 | 理解 k-distance / LRD / LOF score 等术语 |
| [lof_math.md](lof_math.md) | ③ 公式 | 推导 LOF 公式、手算一轮 |
| [lof_tutorial.md](lof_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [lof_code.md](lof_code.md) | ⑤ 代码 | 快速上手 sklearn 实现 |
| [lof_pitfalls.md](lof_pitfalls.md) | ⑥ 踩坑 | 调试 LOF 异常结果 |
| [lof_history.md](lof_history.md) | ⑦ 历史 | 了解密度异常检测演进 |
| [lof_bridge.md](lof_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [lof_first_principles.md](lof_first_principles.md) | ⑨ 第一性原理 | 理解 LOF 为什么必须是这样？割裂公理搜索边界 |

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [lof_map.md](lof_map.md) 了解全局位置
2. 读 [lof_tutorial.md](lof_tutorial.md) Section 1 理解动机（为什么全局方法不够）
3. 读 [lof_concepts.md](lof_concepts.md) 掌握 k-distance / LRD / LOF 四层核心术语
4. 读 [lof_math.md](lof_math.md) 手算一次 LOF 得分
5. 跟 [lof_code.md](lof_code.md) 快速开始跑一个示例
6. 读 [lof_history.md](lof_history.md) 了解技术演进

### 日常参考 🔧

1. 查 [lof_code.md](lof_code.md) API 速查表 (`n_neighbors`, `contamination`, `novelty`)
2. 查 [lof_math.md](lof_math.md) 公式速查（reach-dist / LRD / LOF）
3. 查 [lof_pitfalls.md](lof_pitfalls.md) 排查异常得分不合理问题

### 深度研究 🔬

1. 读 [lof_history.md](lof_history.md) 完整演进（LOF → COF → LoOP → HDBSCAN）
2. 读 [lof_bridge.md](lof_bridge.md) 探索下游任务及变体
3. 阅读原始论文: [Breunig 2000](../../../.documents/papers/lof/breunig_2000_lof.pdf)

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 2026-03-13 |
| Code | ✅ 已完成 2026-03-13 |
| Pitfalls | ✅ 已完成 2026-03-13 |
| History | ✅ 已完成 2026-03-13 |
| Bridge | ✅ 已完成 2026-03-13 |
| First Principles | ✅ 已完成 2026-03-13 |

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
| [Breunig et al. SIGMOD 2000](../../../.documents/papers/lof/breunig_2000_lof.pdf) | 📖 论文 | 全文核心：Map/Concepts/Math/Tutorial/History |
| [scikit-learn LocalOutlierFactor Docs](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html) | 📖 文档 | Code API 速查、Pitfalls 参数说明、Bridge 扩展阅读 |
| [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) | 💻 源码 | Code 示例、Pitfalls 根因分析（lines 232/312/521） |
| [plot_lof_outlier_detection.py](../../../.github/scikit-learn/examples/neighbors/plot_lof_outlier_detection.py) | 💻 源码 | Code 示例 1（多密度簇可视化） |
| [plot_lof_novelty_detection.py](../../../.github/scikit-learn/examples/neighbors/plot_lof_novelty_detection.py) | 💻 源码 | Code 示例 2（Novelty Detection） |
| [scikit-learn Outlier Detection Overview](https://scikit-learn.org/stable/modules/outlier_detection.html) | 📖 文档 | Tutorial Section 4（方案对比）、Bridge 横向对比 |
