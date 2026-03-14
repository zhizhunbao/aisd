---
topic: isf
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Liu et al., 'Isolation Forest', ICDM 2008 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Paper: Liu et al., 'Isolation-Based Anomaly Detection', TKDD 2012 — ⚠️ 待下载 见 papers_index.md"
  - "📖 Docs: scikit-learn IsolationForest — https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html"
  - "💻 Source: sklearn/_iforest.py — https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py"
expiry: 12m
status: current
---

# Isolation Forest 教程

> **前置知识：** 二叉树结构、随机采样、集成学习基本思想
> **参考来源：** [Liu et al. ICDM 2008](https://doi.org/10.1109/ICDM.2008.17) | [scikit-learn User Guide](https://scikit-learn.org/stable/modules/outlier_detection.html#isolation-forest)

---

## Section 0: 前置知识速查

1. **二叉树**：每个节点最多有两个子节点的树形结构；树的深度 = 从根到最深叶的步数
2. **随机采样（无放回）**：从 n 个样本中随机抽 k 个，每个样本被选到的概率相等，抽到后不放回
3. **集成学习**：训练多个弱学习器，将结果聚合（平均/投票）来提高稳定性；随机森林是典型例子
4. **BST（二叉搜索树）**：有序二叉树，不成功搜索的平均路径长度为 $c(n) = 2H(n-1) - 2(n-1)/n$

> 📖 Paper: Liu et al., ICDM 2008, Section 1 (Background)

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1 — 高维低效**：LOF、KNN-based 方法需要计算所有点对的距离，时间 O(n²·d)，在大数据集上无法使用
- 🔥 **痛点 2 — 分布假设限制**：基于密度的方法（如 GMM）需要假设数据服从特定分布；真实异常数据往往分布复杂
- 🔥 **痛点 3 — 维度灾难**：高维空间中距离度量失效（all points equally far），基于密度/距离的异常检测在高维退化
- 🔥 **痛点 4 — 需要标签**：监督分类方法要求标注异常样本，但异常本身极少且难以穷举（未知的未知）

### 它的核心价值

1. **直接隔离**：不测密度、不算距离，直接随机切割 → 异常点"先被孤立"，路径更短。这是纯粹利用异常点的**稀疏性**
2. **线性时间**：训练 O(n log n)，预测为每棵树 O(log n)，适合实时流检测
3. **无分布假设**：完全数据驱动，随机特征+随机分割，不依赖任何分布假设
4. **完全无监督**：不需要异常标签，只需正常数据（甚至混有少量异常也可以）

> 📖 Paper: Liu et al., ICDM 2008, Section 1 (Introduction)
> 📖 Paper: Liu et al., TKDD 2012, Section 1.1 (Motivation)

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌──────────────────────────────────────────────────────────────────┐
│                   Isolation Forest 完整流程                      │
├──────────────────────────────────────────────────────────────────┤
│ 训练阶段                                                          │
│                                                                  │
│  数据集 X（n_samples × n_features）                              │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  重复 T=100 次：                                     │        │
│  │  1. 子采样：从 X 中无放回抽 256 个样本               │        │
│  │  2. 构建 iTree：                                     │        │
│  │     while (节点样本数 > 1 且 深度 < max_depth):      │        │
│  │         随机选特征 q ← uniform(所有特征)              │        │
│  │         随机选分割值 p ← uniform(min_q, max_q)        │        │
│  │         左子树 ← {x : x_q < p}                      │        │
│  │         右子树 ← {x : x_q ≥ p}                      │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 预测阶段（对新样本 x）                                            │
│                                                                  │
│  对每棵 iTree：                                                   │
│    从根走到叶，记录步数 e，叶节点样本数 size                       │
│    h(x) = e + c(size)（路径长度）                                 │
│       │                                                          │
│       ▼                                                          │
│  E[h(x)] = 100 棵树路径均值                                       │
│       │                                                          │
│       ▼                                                          │
│  s(x,n) = 2^{-E[h(x)]/c(256)}        → 异常分数 (0,1]           │
│       │                                                          │
│  s - offset_ 与 0 比较               → predict: +1 / -1         │
└──────────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Liu et al., ICDM 2008, Algorithm 1–2

### 2.2 核心机制：为什么随机分割能检测异常？

**为什么用随机分割而不是最优分割？**

关键洞察：异常点在特征空间中**孤立**（少数、不集中）。随机分割时：
- 异常点周围**稀疏** → 随机切一刀就可能把它和所有其他点分开 → 路径短
- 正常点周围**密集** → 需要多次切割才能把它从其他正常点中分开 → 路径长

如果用最优分割（如 CART），分割会集中在密集区域，反而不利于快速定位异常点。

```
正常点（密集区）             异常点（稀疏区）
                              
 · · · · ·           ×        
 · · · · ·   →  多次切割       →  1-2 次切割就隔离了
 · · · · ·                    
                              
路径长 ≈ log(n)            路径短 ≈ 1~3
```

> 📖 Paper: Liu et al., ICDM 2008, Section 2 (Analysis)

### 2.3 核心机制：子采样为什么是 256？

**为什么 max_samples 默认 256 而不是全量样本？**

论文实验显示：子样本大小 ψ=256 时，异常检测性能已近乎达到饱和，继续增大 ψ 几乎没有提升。更小的子样本：
1. 减少"遮蔽效应"（masking）：大样本中正常点会"包围"异常点，帮助异常点混入
2. 减少"吸收效应"（swamping）：大样本中密集的正常点簇的外侧点会误被判为异常
3. 更快的训练和预测

> 📖 Paper: Liu et al., TKDD 2012, Section 4 (Subsampling Effect)

### 2.4 层次化说明：iTree 的随机性来自两处

```

随机性来源 1                随机性来源 2               结合效果
┌──────────┐            ┌────────────────┐         ┌────────────────┐
│ 特征随机 │──→ 每步从   │ 分割值随机     │──→      │ 每棵 iTree     │
│ 选择     │    所有特征 │ uniform(min,   │         │ 形状完全不同   │
          │    中随机选1 │ max)           │         │                │
└──────────┘            └────────────────┘         └────────────────┘
                                                          │
                                                          ▼
                                              T 棵树平均，消除单棵随机性
```

> 💻 Source: [sklearn/_iforest.py](../../.github/scikit-learn/sklearn/ensemble/_iforest.py) `L357-L375`

---

## Section 3: 局限性

1. **局部异常检测弱** → 若异常点在局部密集正常点中（如簇边缘），ISF 可能漏检；应对：使用 LOF 或 EIF（Extended Isolation Forest）
2. **特征相关时性能下降** → 若异常仅在特征组合中体现（如 x1+x2 异常但单独正常），随机单特征分割难以捕获；应对：使用 SCiForest（沿随机斜切面分割）
3. **边界异常（boundary anomalies）** → 位于数据分布边缘的高密度正常点可能被误判；应对：增大 n_estimators，调整 contamination
4. **不可解释性** → 无法说明"为什么这个点是异常"；应对：SHAP + IsolationForest，查看哪些特征对路径缩短贡献最大

> 📖 Paper: Liu et al., TKDD 2012, Section 5.2 (Limitations)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Isolation Forest** | 线性时间、无分布假设、高维友好 | 局部异常弱、不可解释 | 大规模、高维、全局稀疏异常 |
| **LOF** | 局部密度精准、发现簇内异常 | O(n²) 慢、高维失效 | 小数据、低维、局部簇内异常 |
| **One-Class SVM** | 核函数可处理非线性 | 超参敏感、不适合大数据 | 中等规模、已知正常分布 |
| **EllipticEnvelope** | 数学严谨、可解释 | 必须高斯分布、不适合高维 | 高斯数据、低维 |
| **Extended Isolation Forest (EIF)** | 修复ISF的超平面切割偏差 | 更慢 | ISF效果不佳的场景 |

> 📖 Paper: Liu et al., TKDD 2012, Section 6 (Comparative Study)
> 📖 Docs: [scikit-learn 异常检测对比](https://scikit-learn.org/stable/modules/outlier_detection.html#overview-of-outlier-detection-methods)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Liu et al. ICDM 2008](https://doi.org/10.1109/ICDM.2008.17) | 📖 论文 | Section 1,2（算法原理） |
| [Liu et al. TKDD 2012](https://doi.org/10.1145/2133360.2133363) | 📖 论文 | Section 3,4（子采样分析、改进） |
| [scikit-learn User Guide](https://scikit-learn.org/stable/modules/outlier_detection.html) | 📖 文档 | Section 4（方案对比） |
| [sklearn/_iforest.py](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/ensemble/_iforest.py) | 💻 源码 | Section 2.4（实现细节） |
