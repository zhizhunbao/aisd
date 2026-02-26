# Week 6: Clustering — 教科书教程 (Textbook Tutorial)

> **Slide 来源:** `Week6Clustering.pdf`
> **教科书来源:** Murphy PML1 §21.1–§21.4, Bishop PRML §9.1–§9.2
> **目的:** 补充 Slides 未覆盖的数学推导和定理证明
> **See also:** [Storyline](week6_clustering_storyline.md) | [Cheatsheet](week6_clustering_cheatsheet.md) | [Math](week6_clustering_math.md) | [Code](week6_clustering_code.md)

---

## §0 前置知识 (Prerequisites)

> 本教程涉及以下前置概念，如果你不熟悉，请先复习。

### 0.1 距离度量 (Distance Metrics)

**欧几里得距离 (Euclidean Distance):** 两点之间的直线距离。

$$d(\mathbf{x}, \mathbf{y}) = \|\mathbf{x} - \mathbf{y}\|_2 = \sqrt{\sum_{d=1}^{D}(x_d - y_d)^2}$$

| 符号          | 含义              | 聚类中对应       |
| ------------- | ----------------- | ---------------- |
| $\mathbf{x}$  | 数据点（D维向量） | 一个样本         |
| $\mathbf{y}$  | 另一个数据点      | 另一个样本或质心 |
| $D$           | 维度数            | 特征数量         |
| $\|\cdot\|_2$ | L2 范数           | 到质心的距离     |

**平方欧式距离 (Squared Euclidean Distance):** 聚类中更常用，因为省去了开方运算：

$$d^2(\mathbf{x}, \mathbf{y}) = \|\mathbf{x} - \mathbf{y}\|_2^2 = \sum_{d=1}^{D}(x_d - y_d)^2$$

> ⚠️ **为什么用平方距离？** 平方距离与普通距离在"哪个点更近"的判断上等价（因为平方根是单调函数），但数学上更方便：(1) 对 μ 求导后整洁，(2) 避免开方运算。

### 0.2 贯穿例子 (Running Example)

本教程使用以下 1D 数据集贯穿所有推导：

```
数据集: X = {1, 2, 4, 5}  (4个1维数据点)
全局均值: m = (1+2+4+5)/4 = 3.0
```

当我们需要 2D 例子时，使用：

```
2D 数据集: {(1,1), (1.5,1.8), (5,8), (8,8), (1,0.6), (9,11)}  (6个2维点)
```

---

## §1 K-Means 目标函数的推导 (K-Means Objective Function)

> 📚 Ref: [Murphy §21.3.1](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_3_k_means_clustering.md) — Eq. 21.13–21.15

### ⚠️ Slides 未强调：K-Means 并不是"随便聚一聚"——它在优化一个明确的数学目标函数（distortion / 失真度）。

### 1.1 问题形式化

**直觉：** 我们有 N 个数据点 $\mathbf{x}_1, \ldots, \mathbf{x}_N \in \mathbb{R}^D$，想把它们分成 K 组，使得**每组内的点尽量紧凑**。

"紧凑"用数学表达就是**失真度 (distortion)**，也叫 SSE (Sum of Squared Errors)：

$$J(\mathbf{M}, \mathbf{Z}) = \sum_{n=1}^{N} \|\mathbf{x}_n - \boldsymbol{\mu}_{z_n}\|^2 = \|\mathbf{X} - \mathbf{Z}\mathbf{M}^T\|_F^2 \quad \text{(Murphy Eq. 21.15)}$$

| 符号                                     | 含义              | 贯穿例子中对应               |
| ---------------------------------------- | ----------------- | ---------------------------- |
| $N$                                      | 数据点总数        | 4                            |
| $K$                                      | 簇的数量          | 2                            |
| $\mathbf{x}_n$                           | 第 n 个数据点     | $x_1=1, x_2=2, x_3=4, x_4=5$ |
| $z_n \in \{1,\ldots,K\}$                 | 第 n 个点的簇分配 | $z_1=1, z_2=1, z_3=2, z_4=2$ |
| $\boldsymbol{\mu}_k$                     | 第 k 个簇的质心   | $\mu_1=1.5, \mu_2=4.5$       |
| $\mathbf{X} \in \mathbb{R}^{N \times D}$ | 数据矩阵          | 4×1 矩阵                     |
| $\mathbf{Z} \in \{0,1\}^{N \times K}$    | one-hot 分配矩阵  | 4×2 矩阵                     |
| $\mathbf{M} \in \mathbb{R}^{D \times K}$ | 质心矩阵          | 1×2 矩阵                     |
| $\|\cdot\|_F$                            | Frobenius 范数    | 矩阵元素平方和的平方根       |

### 1.2 交替最小化推导 (Alternating Minimization)

> 📐 推导（教科书原文，Murphy §21.3.1）

K-Means 通过**交替最小化 (alternating minimization)** 来优化 $J$：固定一个变量优化另一个。

**Step 1: 固定 μ，优化 z（分配步）**

当质心 $\boldsymbol{\mu}_k$ 固定时，每个点 $\mathbf{x}_n$ 应该被分配到最近的质心：

$$z_n^* = \arg\min_k \|\mathbf{x}_n - \boldsymbol{\mu}_k\|^2 \quad \text{(Murphy Eq. 21.13)}$$

> **为什么这是最优的？** 因为 $J = \sum_n \|\mathbf{x}_n - \boldsymbol{\mu}_{z_n}\|^2$ 是对每个 $n$ 独立求和的。每个 $z_n$ 的选择只影响它自己那一项，所以每个点独立选最近的质心就能使整体 J 最小。

**Step 2: 固定 z，优化 μ（更新步）**

当分配 $z_n$ 固定时，每个质心应该是其簇内所有点的均值：

$$\boldsymbol{\mu}_k^* = \frac{1}{N_k}\sum_{n: z_n = k} \mathbf{x}_n \quad \text{(Murphy Eq. 21.14)}$$

> 📐 **推导过程（tutorial 补充）：**
>
> 对 $\boldsymbol{\mu}_k$ 求 J 的偏导数并令其为 0：
>
> $$\frac{\partial J}{\partial \boldsymbol{\mu}_k} = \frac{\partial}{\partial \boldsymbol{\mu}_k} \sum_{n: z_n=k} \|\mathbf{x}_n - \boldsymbol{\mu}_k\|^2 = -2\sum_{n: z_n=k}(\mathbf{x}_n - \boldsymbol{\mu}_k) = 0$$
>
> 整理得：
>
> $$\sum_{n: z_n=k} \mathbf{x}_n = N_k \cdot \boldsymbol{\mu}_k$$
>
> $$\boldsymbol{\mu}_k^* = \frac{1}{N_k}\sum_{n: z_n=k} \mathbf{x}_n$$

### 1.3 收敛性证明

> ⚠️ **Slides 仅说"K-Means 总是收敛"，但没解释为什么。**

> 📐 推导（tutorial 补充，基于 Murphy §21.3.1 的描述）

**定理：K-Means 算法在有限步内收敛。**

**证明思路：**

1. **J 是有下界的：** $J \geq 0$（平方距离之和不可能为负）
2. **每一步 J 都不增：**
   - 分配步（固定 μ 优化 z）：每个点选最近质心 → J 不增
   - 更新步（固定 z 优化 μ）：均值是使平方距离和最小的点 → J 不增
3. **有限的可能分配：** N 个点分成 K 组的方式是有限的（最多 $K^N$ 种）
4. **由于 J 单调非增且有下界，且可能的分配方案有限 → 必在有限步内收敛**

> ⚠️ **但收敛不意味着最优！** K-Means 只保证收敛到**局部最小值 (local minimum)**，不保证全局最优。这就是为什么需要多次随机初始化。

### 1.4 贯穿例子验证

```
数据: {1, 2, 4, 5}，假设 K=2

初始化: μ₁=1, μ₂=5（随机选两个点）

迭代 1:
  分配步: d(1,μ₁)=0, d(1,μ₂)=16 → z₁=1
           d(2,μ₁)=1, d(2,μ₂)=9  → z₂=1
           d(4,μ₁)=9, d(4,μ₂)=1  → z₃=2
           d(5,μ₁)=16,d(5,μ₂)=0  → z₄=2
  C₁={1,2}, C₂={4,5}

  更新步: μ₁ = (1+2)/2 = 1.5
           μ₂ = (4+5)/2 = 4.5

  J = (1-1.5)² + (2-1.5)² + (4-4.5)² + (5-4.5)²
    = 0.25 + 0.25 + 0.25 + 0.25 = 1.0

迭代 2:
  分配步: d(1,1.5)=0.25, d(1,4.5)=12.25 → z₁=1
           d(2,1.5)=0.25, d(2,4.5)=6.25  → z₂=1
           d(4,1.5)=6.25, d(4,4.5)=0.25  → z₃=2
           d(5,1.5)=12.25,d(5,4.5)=0.25  → z₄=2
  分配未变 → 收敛！

最终: C₁={1,2} μ₁=1.5, C₂={4,5} μ₂=4.5, SSE=1.0
```

§1 推导了 K-Means 的分配步和更新步的最优性，并证明了收敛性。但 K-Means 只能找球形簇，遇到非球形数据怎么办？→ 我们需要更灵活的聚类方法。

---

## §2 K-Means++ 初始化的理论保证 (K-Means++ Initialization)

> 📚 Ref: [Murphy §21.3.4](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_3_k_means_clustering.md) — Eq. 21.18–21.19

### ⚠️ Slides 未覆盖：K-Means++ 是 sklearn 默认使用的初始化方法，有理论最优性保证。

### 2.1 动机

K-Means 对初始化敏感。随机初始化可能导致：

- 多个质心落在同一个真实簇内
- 某些真实簇没有质心覆盖
- 收敛到较差的局部最小值

### 2.2 K-Means++ 算法

**核心思想：** 顺序选择初始质心，让新质心**尽量远离**已有质心（"覆盖"数据空间）。

**算法步骤：**

1. 均匀随机选择第一个质心 $\boldsymbol{\mu}_1$
2. 对于 $t = 2, \ldots, K$，选择下一个质心 $\boldsymbol{\mu}_t = \mathbf{x}_n$，概率为：

$$p(\boldsymbol{\mu}_t = \mathbf{x}_n) = \frac{D_{t-1}(\mathbf{x}_n)}{\sum_{n'=1}^{N} D_{t-1}(\mathbf{x}_{n'})} \quad \text{(Murphy Eq. 21.18)}$$

其中：

$$D_{t-1}(\mathbf{x}) = \min_{k=1}^{t-1} \|\mathbf{x} - \boldsymbol{\mu}_k\|_2^2 \quad \text{(Murphy Eq. 21.19)}$$

| 符号                                   | 含义                                    | 直觉                             |
| -------------------------------------- | --------------------------------------- | -------------------------------- |
| $D_{t-1}(\mathbf{x})$                  | $\mathbf{x}$ 到已有质心的最短平方距离   | 离所有已选质心越远，D 越大       |
| $p(\boldsymbol{\mu}_t = \mathbf{x}_n)$ | 选 $\mathbf{x}_n$ 作为第 t 个质心的概率 | D 大 → 概率大 → 远的点更可能被选 |

### 2.3 理论保证

> 📚 Book §21.3.4: "this simple trick can be shown to guarantee that the reconstruction error is never more than $O(\log K)$ worse than optimal [AV07]."

**定理 (Arthur & Vassilvitskii 2007)：** K-Means++ 初始化后，期望的失真度满足：

$$\mathbb{E}[J_{\text{K-Means++}}] \leq 8(\ln K + 2) \cdot J_{\text{OPT}}$$

> **直觉：** K-Means++ 保证初始解就已经"不太差"——最多是最优解的 $O(\log K)$ 倍。再经过 K-Means 迭代优化，最终结果通常非常接近最优。

### 2.4 贯穿例子

```
数据: {1, 2, 4, 5}，K=2

Step 1: 随机选 μ₁ = 2（均匀随机）

Step 2: 计算每个点到 μ₁=2 的平方距离
  D(1) = (1-2)² = 1
  D(2) = (2-2)² = 0  ← 已选，概率为0
  D(4) = (4-2)² = 4
  D(5) = (5-2)² = 9
  总和 = 1+0+4+9 = 14

  选择概率:
  P(x=1) = 1/14 ≈ 7%
  P(x=4) = 4/14 ≈ 29%
  P(x=5) = 9/14 ≈ 64%  ← 最远的点最可能被选！

  → 很可能选 μ₂=5，这比随机初始化好得多
```

K-Means++ 解决了初始化问题。但 K-Means 的根本限制仍在——它只能处理球形簇。下一节我们看层次聚类如何绕过"必须指定 K"的限制。

---

## §3 层次聚类的链接距离公式 (Hierarchical Clustering Linkage Formulas)

> 📚 Ref: [Murphy §21.2.1](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_2_hierarchical_agglomerative_clusteri.md) — Eq. 21.9–21.12

### ⚠️ Slides 给出了四种链接方法的定义，但没有解释为什么 MIN 容易产生链接效应、MAX 倾向球形簇。教科书给出了数学解释。

### 3.1 三种链接距离的严格定义

**Single Link / MIN（最近邻，Murphy Eq. 21.9）：**

$$d_{\text{SL}}(G, H) = \min_{i \in G, \; i' \in H} d_{i,i'} \quad \text{(Murphy Eq. 21.9)}$$

**Complete Link / MAX（最远邻，Murphy Eq. 21.11）：**

$$d_{\text{CL}}(G, H) = \max_{i \in G, \; i' \in H} d_{i,i'} \quad \text{(Murphy Eq. 21.11)}$$

**Average Link（组平均，Murphy Eq. 21.12）：**

$$d_{\text{avg}}(G, H) = \frac{1}{n_G \cdot n_H}\sum_{i \in G}\sum_{i' \in H} d_{i,i'} \quad \text{(Murphy Eq. 21.12)}$$

| 符号       | 含义                  | 贯穿例子                 |
| ---------- | --------------------- | ------------------------ |
| $G, H$     | 两个簇                | $G=\{1,2\}$, $H=\{4,5\}$ |
| $d_{i,i'}$ | 点 i 和 i' 之间的距离 | $d(1,4)=3$, $d(2,5)=3$   |
| $n_G, n_H$ | 簇 G 和 H 中的点数    | $n_G=2, n_H=2$           |

### 3.2 为什么 MIN 产生链接效应 (Chaining Effect)

> 📚 Ref: Murphy §21.2.1.1: "single link clustering can overfit..."

> 📐 推导（tutorial 补充）

**链接效应 (Chaining Effect)** 的数学解释：

MIN 只看两簇之间**一对**最近的点。如果两个原本分离的簇之间有一串"桥接"噪声点：

```
簇A: ●●●    ·  ·  ·    ●●●  :簇B
         噪声桥 (每相邻两点距离很小)
```

设簇 A 和 B 的真实距离 = 10，但桥接噪声点每两相邻只差 0.5。

- **MIN 链接：** $d_{\text{SL}} = 0.5$（只看最近的一对噪声点）→ 合并！❌
- **MAX 链接：** $d_{\text{CL}} = 10+$（要看 A 最远点到 B 最远点）→ 不合并 ✅
- **Average：** $d_{\text{avg}} ≈ 5$（所有点对的平均）→ 可能不合并 ✅

**结论：** MIN 对单个异常点或噪声极度敏感，一个噪声点就能"桥接"两个应该分离的簇。这就是**链接效应**。

### 3.3 算法复杂度

> 📚 Book §21.2.1: "the total running time is $O(N^3)$. However, for single link clustering, this can be reduced to $O(N^2)$ using a minimum spanning tree algorithm."

| 链接方法      | 复杂度   | 原因                     |
| ------------- | -------- | ------------------------ |
| Single Link   | $O(N^2)$ | 可用最小生成树加速       |
| Complete Link | $O(N^3)$ | 每次合并后需重算距离矩阵 |
| Average Link  | $O(N^3)$ | 同上                     |

### 3.4 贯穿例子

```
1D 数据: {1, 2, 4, 5}

距离矩阵:
     1    2    4    5
1  [ 0    1    3    4 ]
2  [ 1    0    2    3 ]
4  [ 3    2    0    1 ]
5  [ 4    3    1    0 ]

Single Link 合并顺序:
  Step 1: d(1,2)=1, d(4,5)=1 → 合并 {1,2} 和 {4,5}（并列，选一个）
  Step 2: d_SL({1,2},{4,5}) = min(3,4,2,3) = 2 → 合并

Complete Link 合并顺序:
  Step 1: 同上 → {1,2} 和 {4,5}
  Step 2: d_CL({1,2},{4,5}) = max(3,4,2,3) = 4

Average Link:
  Step 2: d_avg({1,2},{4,5}) = (3+4+2+3)/4 = 3.0
```

层次聚类解决了"不需要指定 K"的问题。但所有点仍被分配到某个簇——没有噪声处理能力。DBSCAN 的理论基础是什么？

---

## §4 DBSCAN 的密度可达性理论 (DBSCAN Density Reachability)

> ⚠️ Slides 给了 DBSCAN 的使用步骤，但没有解释其理论基础——**密度可达性 (density reachability)** 和**密度连通性 (density connectivity)**。

### 4.1 核心定义链

> 📐 推导（tutorial 补充，整理自 Ester et al. 1996 经典论文）

DBSCAN 建立在一个严格的定义链上：

**定义 1: ε-邻域 (ε-neighborhood)**

$$N_\varepsilon(p) = \{q \in D \mid d(p, q) \leq \varepsilon\}$$

**定义 2: 核心点 (Core Point)**

$$p \text{ 是核心点} \iff |N_\varepsilon(p)| \geq \text{MinPts}$$

> ⚠️ **$|N_\varepsilon(p)|$ 包括 p 自身！** 这是 Slides 和考试中反复强调的重点。

**定义 3: 直接密度可达 (Directly Density-Reachable)**

点 q **直接密度可达**自 p，如果：

1. $q \in N_\varepsilon(p)$（q 在 p 的 ε 邻域内）
2. p 是核心点

> ⚠️ **不对称！** q 直接密度可达自 p，不意味着 p 直接密度可达自 q（因为 q 可能不是核心点）。

**定义 4: 密度可达 (Density-Reachable)**

点 q **密度可达**自 p，如果存在一条链 $p_1 = p, p_2, \ldots, p_m = q$，使得每个 $p_{i+1}$ 直接密度可达自 $p_i$。

```
核心点链: ● → ● → ● → ○
          p   p₂   p₃   q
(所有中间点必须是核心点，最后一个 q 可以不是)
```

**定义 5: 密度连通 (Density-Connected)**

点 p 和 q **密度连通**，如果存在一个核心点 o，使得 p 和 q 都密度可达自 o。

```
             o (核心点)
            / \
(密度可达) ↙   ↘ (密度可达)
          p       q
```

**定义 6: 簇 (Cluster)**

簇 $C$ 是满足以下条件的非空子集：

1. **最大性 (Maximality):** 如果 p ∈ C 且 q 密度可达自 p，则 q ∈ C
2. **连通性 (Connectivity):** C 中任意两点都密度连通

### 4.2 为什么这些定义很重要

这套定义保证了：

| 性质       | 保证                                    | 与 K-Means 对比        |
| ---------- | --------------------------------------- | ---------------------- |
| 任意形状   | 密度可达是沿任意路径的 → 月牙、环形都行 | K-Means 只能球形       |
| 噪声处理   | 不属于任何簇的点 = 噪声                 | K-Means 强制分配每个点 |
| 无需指定 K | 簇数由数据密度结构决定                  | K-Means 必须提前指定 K |
| 确定性     | 核心点的簇分配是确定的                  | K-Means 随初始化变化   |

> ⚠️ **边界点的分配不是确定的：** 一个边界点可能在多个核心点的 ε 邻域内，属于哪个核心点的簇取决于算法处理顺序。

---

## §5 SSE + SSB = TSS 恒等式的推导 (SSE-SSB-TSS Identity)

> ⚠️ Slides 给出了 SSE + SSB = TSS 这个结论和数值验证，但没有推导为什么。

### 5.1 三个指标的定义

$$\text{TSS} = \sum_{n=1}^{N}(\mathbf{x}_n - \bar{\mathbf{x}})^2 \quad \text{(Total Sum of Squares)}$$

$$\text{SSE} = \sum_{k=1}^{K}\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k)^2 \quad \text{(Within-Cluster / Error)}$$

$$\text{SSB} = \sum_{k=1}^{K}|C_k| \cdot (\boldsymbol{\mu}_k - \bar{\mathbf{x}})^2 \quad \text{(Between-Cluster)}$$

| 符号                 | 含义            | 贯穿例子                                 |
| -------------------- | --------------- | ---------------------------------------- |
| $\bar{\mathbf{x}}$   | 全局均值        | $\bar{x} = 3.0$                          |
| $\boldsymbol{\mu}_k$ | 第 k 个簇的均值 | $\mu_1=1.5, \mu_2=4.5$                   |
| $C_k$                | 第 k 个簇的点集 | $C_1=\{1,2\}, C_2=\{4,5\}$               |
| $\lvert C_k \rvert$  | 第 k 个簇的点数 | $\lvert C_1\rvert=2, \lvert C_2\rvert=2$ |

### 5.2 恒等式推导

> 📐 推导（tutorial 补充）

**要证：** $\text{TSS} = \text{SSE} + \text{SSB}$

**证明：** 对每个数据点 $\mathbf{x}_n \in C_k$，做一个"加零减零"的技巧：

$$(\mathbf{x}_n - \bar{\mathbf{x}}) = (\mathbf{x}_n - \boldsymbol{\mu}_k) + (\boldsymbol{\mu}_k - \bar{\mathbf{x}})$$

两边平方：

$$(\mathbf{x}_n - \bar{\mathbf{x}})^2 = (\mathbf{x}_n - \boldsymbol{\mu}_k)^2 + 2(\mathbf{x}_n - \boldsymbol{\mu}_k)(\boldsymbol{\mu}_k - \bar{\mathbf{x}}) + (\boldsymbol{\mu}_k - \bar{\mathbf{x}})^2$$

对簇 $C_k$ 内所有点求和：

$$\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \bar{\mathbf{x}})^2 = \sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k)^2 + 2(\boldsymbol{\mu}_k - \bar{\mathbf{x}})\underbrace{\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k)}_{= 0 \text{ (均值定义)}} + |C_k|(\boldsymbol{\mu}_k - \bar{\mathbf{x}})^2$$

> **关键步骤：** 交叉项为零！因为 $\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k) = 0$（$\boldsymbol{\mu}_k$ 是 $C_k$ 的均值，所以偏差之和为零）。

所以：

$$\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \bar{\mathbf{x}})^2 = \sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k)^2 + |C_k|(\boldsymbol{\mu}_k - \bar{\mathbf{x}})^2$$

对所有 K 个簇求和：

$$\underbrace{\sum_{k=1}^{K}\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \bar{\mathbf{x}})^2}_{\text{TSS}} = \underbrace{\sum_{k=1}^{K}\sum_{\mathbf{x} \in C_k}(\mathbf{x} - \boldsymbol{\mu}_k)^2}_{\text{SSE}} + \underbrace{\sum_{k=1}^{K}|C_k|(\boldsymbol{\mu}_k - \bar{\mathbf{x}})^2}_{\text{SSB}}$$

$$\boxed{\text{TSS} = \text{SSE} + \text{SSB}}$$

### 5.3 贯穿例子验证

```
数据: {1, 2, 4, 5}，全局均值 m = 3.0
分为 C₁={1,2} (μ₁=1.5), C₂={4,5} (μ₂=4.5)

TSS = (1-3)² + (2-3)² + (4-3)² + (5-3)²
    = 4 + 1 + 1 + 4 = 10

SSE = (1-1.5)² + (2-1.5)² + (4-4.5)² + (5-4.5)²
    = 0.25 + 0.25 + 0.25 + 0.25 = 1.0

SSB = 2×(1.5-3)² + 2×(4.5-3)²
    = 2×2.25 + 2×2.25 = 9.0

验证: SSE + SSB = 1.0 + 9.0 = 10.0 = TSS ✓
```

### 5.4 推导的意义

> **为什么交叉项为零如此重要？**
>
> 这个性质意味着：
>
> 1. **SSE 和 SSB 是互补的** — 降低 SSE 自动提升 SSB（此消彼长）
> 2. **只需要优化其中一个** — K-Means 优化 SSE 等价于同时优化 SSB
> 3. **TSS 是常数** — 不依赖聚类结果，只依赖数据本身

TSS = SSE + SSB 恒等式是理解聚类质量度量的基础。但我们还需要一个"跨簇"的质量指标——轮廓系数。

---

## §6 轮廓系数的推导与性质 (Silhouette Coefficient)

> 📚 Ref: [Murphy §21.3.7.3](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_3_k_means_clustering.md)

### 6.1 公式定义

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)} \quad \text{(Murphy §21.3.7.3)}$$

| 符号  | 含义                                            | 直觉                   |
| ----- | ----------------------------------------------- | ---------------------- |
| $a_i$ | 点 i 与**同簇**所有其他点的平均距离             | 簇内紧凑度（越小越好） |
| $b_i$ | 点 i 与**最近其他簇**所有点的平均距离中的最小值 | 簇间分离度（越大越好） |
| $s_i$ | 轮廓系数                                        | 综合评分 ∈ [-1, 1]     |

**$b_i$ 的精确定义：**

$$b_i = \min_{k \neq k_i} \frac{1}{|C_k|}\sum_{j \in C_k} d(i, j)$$

其中 $k_i$ 是点 i 所属的簇。

### 6.2 取值范围分析

> 📐 推导（tutorial 补充）

**Case 1: $s_i \approx +1$**

当 $a_i \ll b_i$（簇内紧凑，簇间远离）：

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)} = \frac{b_i - a_i}{b_i} = 1 - \frac{a_i}{b_i} \approx 1$$

> ✅ 良好聚类：点牢固地属于自己的簇。

**Case 2: $s_i \approx 0$**

当 $a_i \approx b_i$（点在两簇边界上）：

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)} \approx \frac{0}{\max(a_i, b_i)} \approx 0$$

> ⚠️ 边界点：分到哪个簇都差不多。

**Case 3: $s_i \approx -1$**

当 $a_i \gg b_i$（离自己的簇远，离其他簇近）：

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)} = \frac{b_i - a_i}{a_i} = \frac{b_i}{a_i} - 1 \approx -1$$

> ❌ 误分类：点可能分到了错误的簇。

### 6.3 为什么除以 max(a, b)

> 📐 推导（tutorial 补充）

除以 $\max(a_i, b_i)$ 是为了**归一化到 [-1, 1]**：

- 如果 $a_i > b_i$：$s_i = \frac{b_i - a_i}{a_i} \in [-1, 0)$
- 如果 $a_i < b_i$：$s_i = \frac{b_i - a_i}{b_i} \in (0, 1]$
- 如果 $a_i = b_i$：$s_i = 0$

任何情况下 $|s_i| \leq 1$，保证了不同数据集之间的可比性。

---

## §7 EM 算法与 GMM：从 K-Means 到概率模型 (EM Algorithm & GMM)

> 📚 Ref: [Murphy §21.4.1](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_4_clustering_using_mixture_models.md) — Eq. 21.22–21.24
> 📚 Ref: [Bishop §9.1–§9.2](../self-study/ml/_sources/bishop_sections/ch09/sec_9_1_k-means_clustering.md)

### ⚠️ Slides 给了 E 步和 M 步的公式，但没有推导它们。教科书展示了 EM 是如何从最大似然估计自然推导出来的。

### 7.1 高斯混合模型 (GMM) 的生成模型

**生成过程 (Generative Story)：** 每个数据点 $\mathbf{x}_n$ 是这样产生的：

1. 先掷一个有 K 面的骰子，以概率 $\pi_k$ 选中第 k 个高斯（$\sum_k \pi_k = 1$）
2. 从第 k 个高斯 $\mathcal{N}(\boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$ 中采样

**数学表达：**

$$p(\mathbf{x}_n | \boldsymbol{\theta}) = \sum_{k=1}^{K} \pi_k \cdot \mathcal{N}(\mathbf{x}_n | \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k) \quad \text{(Murphy Eq. 21.22)}$$

| 符号                    | 含义                                                                    | 命名来源                            |
| ----------------------- | ----------------------------------------------------------------------- | ----------------------------------- |
| $\pi_k$                 | 混合权重 (mixing weight)                                                | 先验概率 $P(z=k)$，像骰子每面的概率 |
| $\boldsymbol{\mu}_k$    | 第 k 个高斯的均值                                                       | 簇中心                              |
| $\boldsymbol{\Sigma}_k$ | 第 k 个高斯的协方差矩阵                                                 | 簇的"形状"和"大小"                  |
| $\boldsymbol{\theta}$   | 所有参数 $\{\pi_k, \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k\}_{k=1}^K$ | —                                   |

### 7.2 E 步的推导 (Responsibilities)

> 📐 推导（教科书原文，Murphy Eq. 21.23）

**E 步** 计算每个点属于每个簇的**后验概率** (responsibility)：

$$r_{nk} = p(z_n = k | \mathbf{x}_n, \boldsymbol{\theta}) = \frac{p(z_n = k | \boldsymbol{\theta}) \cdot p(\mathbf{x}_n | z_n = k, \boldsymbol{\theta})}{\sum_{k'=1}^{K} p(z_n = k' | \boldsymbol{\theta}) \cdot p(\mathbf{x}_n | z_n = k', \boldsymbol{\theta})} \quad \text{(Murphy Eq. 21.23)}$$

简写为：

$$r_{nk} = \frac{\pi_k \cdot \mathcal{N}(\mathbf{x}_n | \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)}{\sum_{k'=1}^{K} \pi_{k'} \cdot \mathcal{N}(\mathbf{x}_n | \boldsymbol{\mu}_{k'}, \boldsymbol{\Sigma}_{k'})}$$

> **这就是 Bayes 定理！** 分子 = 先验 × 似然，分母 = 边缘似然（归一化常数）。

| 符号                                                                       | Bayes 对应                             | 直觉                                 |
| -------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------ |
| $r_{nk}$                                                                   | 后验 $P(\text{簇} \mid \text{数据点})$ | "这个点有多大概率来自簇 k？"         |
| $\pi_k$                                                                    | 先验 $P(\text{簇})$                    | "簇 k 有多大？"                      |
| $\mathcal{N}(\mathbf{x}_n \mid \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)$ | 似然 $P(\text{数据点} \mid \text{簇})$ | "如果点来自簇 k，看到这个位置的概率" |

### 7.3 M 步的推导

> 📐 推导（教科书原文，Murphy §21.4.1 + Bishop §9.2）

给定 responsibilities $r_{nk}$，更新参数以最大化期望对数似然

**均值更新：**

$$\boldsymbol{\mu}_k^{\text{new}} = \frac{\sum_{n=1}^{N} r_{nk} \cdot \mathbf{x}_n}{\sum_{n=1}^{N} r_{nk}} = \frac{\sum_n r_{nk} \mathbf{x}_n}{N_k}$$

其中 $N_k = \sum_{n=1}^{N} r_{nk}$ 是簇 k 的"有效点数"（软计数）。

> **直觉：** 加权平均——每个点的权重就是它属于簇 k 的概率。

**协方差更新（1D 时为方差）：**

$$\sigma_k^2 = \frac{\sum_{n=1}^{N} r_{nk} (x_n - \mu_k)^2}{\sum_{n=1}^{N} r_{nk}} = \frac{\sum_n r_{nk} (x_n - \mu_k)^2}{N_k}$$

> **直觉：** 加权方差——偏差的加权平方和。

**混合权重更新：**

$$\pi_k^{\text{new}} = \frac{N_k}{N} = \frac{\sum_{n=1}^{N} r_{nk}}{N}$$

> **直觉：** 簇 k 的"有效点数"占总点数的比例。

### 7.4 K-Means 是 EM 的特殊情况

> 📚 Ref: Murphy §21.4.1.1: "K-means is a special case of EM"

> **这是 Slides 的核心考点之一。**

**定理：** K-Means 等价于 EM/GMM 加上两个约束：

| 约束 | K-Means                                            | EM/GMM                             |
| ---- | -------------------------------------------------- | ---------------------------------- |
| 方差 | 所有簇相同且固定 ($\sigma_k^2 = \sigma^2$, 不更新) | 每个簇独立学习 ($\sigma_k^2$ 更新) |
| 分配 | 硬分配 $r_{nk} \in \{0, 1\}$                       | 软分配 $r_{nk} \in [0, 1]$         |

> 📐 推导（tutorial 补充）

当 $\sigma_k^2 \to 0$（方差趋近于零），高斯 PDF 变成 delta 函数，responsibilities 变成：

$$r_{nk} = \begin{cases} 1 & \text{if } k = \arg\min_{k'} \|\mathbf{x}_n - \boldsymbol{\mu}_{k'}\|^2 \\ 0 & \text{otherwise} \end{cases}$$

这正是 K-Means 的分配步！此时 M 步的加权均值也变成简单均值：

$$\boldsymbol{\mu}_k = \frac{\sum_{n: r_{nk}=1} \mathbf{x}_n}{\sum_{n: r_{nk}=1} 1} = \frac{1}{|C_k|}\sum_{\mathbf{x} \in C_k} \mathbf{x}$$

这正是 K-Means 的更新步！

### 7.5 贯穿例子：1D EM 一次迭代

```
数据: X = {1, 2, 4, 5}
初始参数: μₐ=1.5, σₐ²=1.0, μᵦ=4.5, σᵦ²=1.0, πₐ=πᵦ=0.5

高斯 PDF: N(x; μ, σ²) = (1/√(2πσ²)) × exp(-(x-μ)²/(2σ²))

E 步（计算 responsibilities）:
  对 x=1:
    P(x=1|a) = N(1; 1.5, 1.0) = 0.3521   ← (1-1.5)²/2 = 0.125
    P(x=1|b) = N(1; 4.5, 1.0) = 0.0009   ← (1-4.5)²/2 = 6.125
    r(a|x=1) = 0.5×0.3521 / (0.5×0.3521 + 0.5×0.0009) = 0.9975  ← 几乎肯定属于 a

  对 x=2:
    P(x=2|a) = N(2; 1.5, 1.0) = 0.3521   ← (2-1.5)²/2 = 0.125
    P(x=2|b) = N(2; 4.5, 1.0) = 0.0175   ← (2-4.5)²/2 = 3.125
    r(a|x=2) = 0.5×0.3521 / (0.5×0.3521 + 0.5×0.0175) = 0.9526

  对 x=4:  （与 x=2 对称）
    P(x=4|a) = 0.0175, P(x=4|b) = 0.3521
    r(a|x=4) = 0.0474  ← 几乎肯定属于 b

  对 x=5:  （与 x=1 对称）
    P(x=5|a) = 0.0009, P(x=5|b) = 0.3521
    r(a|x=5) = 0.0025  ← 几乎肯定属于 b

M 步（更新参数）:
  Nₐ = 0.9975 + 0.9526 + 0.0474 + 0.0025 = 2.0
  Nᵦ = 0.0025 + 0.0474 + 0.9526 + 0.9975 = 2.0

  μₐ = (0.9975×1 + 0.9526×2 + 0.0474×4 + 0.0025×5) / 2.0 ≈ 1.55
  μᵦ = (0.0025×1 + 0.0474×2 + 0.9526×4 + 0.9975×5) / 2.0 ≈ 4.45

  πₐ = 2.0/4 = 0.5 (不变)

→ μ 向数据均值方向微调（1.5→1.55, 4.5→4.45），因为软分配让少量远处点有微小贡献
```

---

## §8 选择 K 的方法比较 (Choosing K)

> 📚 Ref: [Murphy §21.3.7](../self-study/ml/_sources/murphy_pml1_sections/ch21/sec_21_3_k_means_clustering.md) — Eq. 21.20–21.21

### ⚠️ Slides 介绍了 Elbow Method 和 Silhouette，但教科书还讨论了 BIC 和解释了为什么 Elbow Method 有时不可靠。

### 8.1 为什么 SSE 单调递减

> 📚 Book §21.3.7.1: "the distortion monotonically decreases with K."

**原因：** K-Means 模型本质上是 K 个 δ 函数（spike），不是真正的密度模型。增加 K 就增加了"覆盖"数据空间的 spike 数量，任何输入点都能找到更近的 prototype → 重建误差永远下降。

$$\text{当 } K = N \text{ 时，每个点一个簇，SSE} = 0 \text{（但毫无意义）}$$

> 这就是为什么不能简单地"选 SSE 最低的 K"。

### 8.2 BIC 方法

> 📚 Ref: Murphy Eq. 21.21

$$\text{BIC}(K) = \log p(\mathcal{D} | \hat{\boldsymbol{\theta}}_K) - \frac{D_K}{2}\log(N)$$

| 符号                                                   | 含义                        |
| ------------------------------------------------------ | --------------------------- |
| $\log p(\mathcal{D} \mid \hat{\boldsymbol{\theta}}_K)$ | K 个簇的 GMM 的最大对数似然 |
| $D_K$                                                  | K 个簇的模型参数个数        |
| $N$                                                    | 数据点数                    |

**直觉：** BIC = 拟合度 - 复杂度惩罚。它自动平衡模型的拟合能力和复杂度——太多簇会被惩罚。

> **与 Elbow Method 的区别：** Elbow 要人工判断"拐点"（主观），BIC 给出一个可计算的最优 K（客观）。但 BIC 需要用 GMM 而非 K-Means。

### 8.3 三种方法对比

| 方法         | 需要的模型 | 自动化程度      | 数学基础                       |
| ------------ | ---------- | --------------- | ------------------------------ |
| Elbow Method | K-Means    | ❌ 需要人工看图 | 无 — 启发式                    |
| Silhouette   | K-Means    | ✅ 取最大值     | 几何（簇内/簇间距离比）        |
| BIC          | GMM (EM)   | ✅ 取最大值     | 贝叶斯模型选择 (Occam's razor) |

---

## 参考索引表

| 教程章节             | 教科书来源                                       | 核心内容                                  | Slides 覆盖？                           |
| -------------------- | ------------------------------------------------ | ----------------------------------------- | --------------------------------------- |
| §0 前置知识          | —                                                | 距离度量、贯穿例子                        | ✅ 基本概念                             |
| §1 K-Means 目标函数  | Murphy §21.3.1, Eq. 21.13–21.15                  | 失真度推导、交替最小化、收敛证明          | ⚠️ 仅给了算法步骤，没推导               |
| §2 K-Means++         | Murphy §21.3.4, Eq. 21.18–21.19                  | 初始化概率、$O(\log K)$ 保证              | ❌ 未提及                               |
| §3 层次聚类链接公式  | Murphy §21.2.1, Eq. 21.9–21.12                   | 三种链接的公式和链接效应解释              | ⚠️ 给了公式，没解释链接效应的数学原因   |
| §4 DBSCAN 密度可达性 | Ester et al. 1996                                | 6 个定义的严格定义链                      | ⚠️ 仅给了核心/边界/噪声，没有密度可达性 |
| §5 SSE+SSB=TSS       | tutorial 补充                                    | 代数推导（交叉项为零）                    | ⚠️ 给了结论和数值验证，没推导           |
| §6 轮廓系数          | Murphy §21.3.7.3                                 | 取值范围分析、归一化原因                  | ⚠️ 给了公式，没分析取值含义             |
| §7 EM/GMM            | Murphy §21.4.1, Eq. 21.22–21.24; Bishop §9.1–9.2 | E步/M步推导、K-Means 是 EM 特殊情况的证明 | ⚠️ 给了公式，没推导                     |
| §8 选择 K            | Murphy §21.3.7, Eq. 21.20–21.21                  | BIC、Elbow 的数学基础和对比               | ⚠️ 只介绍了 Elbow 和 Silhouette         |
