---
topic: lof
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Breunig et al. SIGMOD 2000 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/lof/breunig_2000_lof.pdf"
expiry: 12m
status: current
---

# LOF 数学基础

> 📖 Paper: Breunig et al., [《LOF: Identifying Density-Based Local Outliers》](../../../.documents/papers/lof/breunig_2000_lof.pdf), SIGMOD 2000, Def. 1-6, Theorem 1

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|------------|------|---------|
| $D$ | 数据集 | Dataset | 有限点集 |
| $p, q, o$ | 数据点 | Data point | $\in D$ |
| $k$ | 邻域大小（超参数） | MinPts / n_neighbors | $\mathbb{Z}^+$ |
| $\text{dist}(p,q)$ | 点对间的距离（如欧氏距离） | Distance | $\geq 0$ |
| $k\text{-dist}(p)$ | p 到其第 k 个最近邻的距离 | k-distance | $\geq 0$ |
| $N_k(p)$ | p 的 k-距离邻域（所有在 k-dist 球内的点） | k-distance neighborhood | $|N_k(p)| \geq k$ |
| $\text{reach-dist}_k(o,p)$ | o 相对于 p 的可达距离 | Reachability distance | $\geq 0$ |
| $\text{lrd}_k(p)$ | p 的局部可达密度 | Local Reachability Density | $> 0$ |
| $\text{LOF}_k(p)$ | p 的局部离群因子 | Local Outlier Factor | $\geq 0$ |

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Def. 1 (p. 94)

---

## 核心公式

### 公式 1: k-distance

**直觉：** 定义点 p 的"邻域半径"——到第 k 个邻居有多远

$$
k\text{-dist}(p) = \text{dist}(p,\ o^{(k)})
$$

其中 $o^{(k)}$ 是距 $p$ 第 $k$ 近的点（按距离升序排列的第 $k$ 个）。

> 📖 Paper: Breunig et al., Def. 1 (p. 94)

**参数解释：**
| 参数 | 含义 |
|------|------|
| $o^{(k)}$ | p 的第 k 个最近邻 |

**推导过程：**

$$
\text{Step 1: 对所有 } q \in D \setminus \{p\},\ \text{按 dist}(p,q) \text{ 升序排列}
$$

$$
\text{Step 2: 取排名第 } k \text{ 的点 } o^{(k)}
$$

$$
\text{Step 3: } k\text{-dist}(p) = \text{dist}(p, o^{(k)})
$$

> 📖 Paper: Breunig et al., Def. 1

---

### 公式 2: k-distance 邻域

**直觉：** 把所有"不比第 k 个邻居更远"的点都纳入邻域

$$
N_k(p) = \bigl\{q \in D \setminus \{p\} \mid \text{dist}(p, q) \leq k\text{-dist}(p)\bigr\}
$$

> 📖 Paper: Breunig et al., Def. 2 (p. 94)

**推导（为何 $|N_k(p)| \geq k$）：**

$$
\text{Step 1: 按定义，第 k 个邻居 } o^{(k)} \in N_k(p)，\text{因此 } |N_k(p)| \geq k
$$

$$
\text{Step 2: 若距离等于 } k\text{-dist}(p) \text{ 的点不止一个（tie），则 } |N_k(p)| > k
$$

> 📖 Paper: Breunig et al., Def. 2

---

### 公式 3: 可达距离 (Reachability Distance)

**直觉：** 对近距离点对用 k-dist(p) 替换真实距离，防止密集核心区内极小距离带来的统计噪声

$$
\text{reach-dist}_k(o, p) = \max\bigl\{k\text{-dist}(p),\ \text{dist}(o, p)\bigr\}
$$

> 📖 Paper: Breunig et al., Def. 3 (p. 95)

**参数解释：**
| 参数 | 含义 |
|------|------|
| $o$ | 目标点（从 o 出发） |
| $p$ | 参考点（用 p 的 k-dist 作为下界） |

**推导（为什么非对称）：**

$$
\text{Step 1: reach-dist}_k(o,p) \text{ 以 } k\text{-dist}(p) \text{ 为下界（p 的视角）}
$$

$$
\text{Step 2: reach-dist}_k(p,o) \text{ 以 } k\text{-dist}(o) \text{ 为下界（o 的视角）}
$$

$$
\text{Step 3: } k\text{-dist}(p) \neq k\text{-dist}(o) \Rightarrow \text{ 非对称}
$$

> 📖 Paper: Breunig et al., Def. 3, Note after Def. 3

---

### 公式 4: 局部可达密度 (LRD)

**直觉：** p 周围区域的"密度"——邻居到 p 的平均可达距离的倒数；距离越短 → 密度越高

$$
\text{lrd}_k(p) = \left(\frac{\displaystyle\sum_{o \in N_k(p)} \text{reach-dist}_k(o,\ p)}{|N_k(p)|}\right)^{-1}
$$

> 📖 Paper: Breunig et al., Def. 4 (p. 95)

**推导过程：**

$$
\text{Step 1: 计算 p 的所有邻居 } o \in N_k(p) \text{ 到 p 的可达距离 reach-dist}_k(o,p)
$$

$$
\text{Step 2: 求平均可达距离} = \frac{1}{|N_k(p)|}\sum_{o \in N_k(p)} \text{reach-dist}_k(o,p)
$$

$$
\text{Step 3: LRD} = \text{（平均可达距离）}^{-1}
$$

> 📖 Paper: Breunig et al., Def. 4

---

### 公式 5: 局部离群因子 (LOF)

**直觉：** p 有多"孤立"——邻居们的平均密度 / p 自身密度；比值 >> 1 → p 异常

$$
\text{LOF}_k(p) = \frac{\displaystyle\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}
= \frac{1}{|N_k(p)|} \sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}
$$

> 📖 Paper: Breunig et al., Def. 5 (p. 95)

**推导过程：**

$$
\text{Step 1: 对 p 的每个邻居 } o \text{ 计算 lrd}_k(o) / \text{lrd}_k(p)
$$

$$
\text{Step 2: 若 o 比 p 密度高，则比值 > 1（o 所在区域比 p 稠密）}
$$

$$
\text{Step 3: } \text{LOF}_k(p) = \text{所有比值的均值}
$$

$$
\text{Step 4: LOF} \approx 1 \Leftrightarrow p \text{ 与邻居密度相当（内点）}
$$

$$
\text{Step 5: LOF} \gg 1 \Leftrightarrow \text{邻居远比 } p \text{ 稠密（外点）}
$$

> 📖 Paper: Breunig et al., Def. 5, Theorem 1

---

## 公式关系图

```
k-dist(p)              ──→  N_k(p)
    │                            │
    │                            ▼
    └──────────────→  reach-dist_k(o, p) = max{k-dist(p), dist(o,p)}
                                 │
                                 ▼
                        lrd_k(p) = 1 / mean(reach-dist)
                                 │
                                 ▼
                        LOF_k(p) = mean( lrd(neighbors) / lrd(p) )
```

---

## 手算练习

### 练习 1: 三点数据集

**题目：** 数据集 $D = \{A(0), B(1), C(10)\}$，用欧氏距离，$k=1$。计算 $\text{LOF}_1(C)$。

**解答步骤：**

1. **计算 k-dist**：
   - $1\text{-dist}(A) = \text{dist}(A,B) = 1$
   - $1\text{-dist}(B) = \text{dist}(B,A) = 1$
   - $1\text{-dist}(C) = \text{dist}(C,B) = 9$

2. **邻域**：
   - $N_1(C) = \{B\}$

3. **计算 reach-dist**：
   - $\text{reach-dist}_1(B, C) = \max\{1\text{-dist}(C), \text{dist}(B,C)\} = \max\{9, 9\} = 9$

4. **计算 LRD**：
   - $\text{lrd}_1(C) = 1/9 \approx 0.111$
   - $\text{lrd}_1(B)$：$N_1(B)=\{A\}$，$\text{reach-dist}_1(A,B) = \max\{1,1\}=1$，$\text{lrd}_1(B) = 1$

5. **计算 LOF**：
   - $\text{LOF}_1(C) = \text{lrd}_1(B) / \text{lrd}_1(C) = 1 / 0.111 = 9.0$

**结果：** LOF = 9 >> 1，C 是明显的异常点。✅

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Example in Sec. 3

### 练习 2: sklearn 数值验证

**题目：** 用 sklearn 验证：`X = [[-1.1], [0.2], [101.1], [0.3]]`，$k=2$，预期 `101.1` 的 LOF 最大。

**解答步骤：**

1. 代入公式，`101.1` 距离最近邻 `0.3` 约 100.8
2. 相较于 `[-1.1, 0.2, 0.3]` 三点密集区，LRD(101.1) 极小
3. sklearn 输出 `negative_outlier_factor_` ≈ `[-0.98, -1.04, -73.37, -0.98]`
4. `101.1` 的 `-LOF = -73.37`，即 `LOF ≈ 73.37`，远大于 1 → 确认为异常点

> 💻 Source: [sklearn/_lof.py](../../../.github/scikit-learn/sklearn/neighbors/_lof.py) `lines 178-185` (docstring example)

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| k-distance | $\text{dist}(p, o^{(k)})$ | 定义邻域半径 | 无 |
| 邻域 $N_k(p)$ | $\{q : \text{dist}(p,q) \leq k\text{-dist}(p)\}$ | 确定邻居集合 | 公式 1 |
| reach-dist | $\max\{k\text{-dist}(p), \text{dist}(o,p)\}$ | 平滑距离，减少噪声 | 公式 1,2 |
| LRD | $1 / \text{mean}(\text{reach-dist})$ | 局部密度估计 | 公式 3 |
| LOF | $\text{mean}(\text{lrd}(\text{neighbors})) / \text{lrd}(p)$ | 最终异常分数 | 公式 4 |

> 📖 Paper: Breunig et al., [LOF](../../../.documents/papers/lof/breunig_2000_lof.pdf), Def. 1-5 (pp. 94-95)
