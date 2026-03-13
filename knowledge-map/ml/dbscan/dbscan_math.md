---
topic: dbscan
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Ester et al. KDD 1996 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/dbscan/ester_1996_dbscan.pdf"
  - "📖 Paper: Schubert et al. TODS 2017 — https://doi.org/10.1145/3068335"
expiry: 12m
status: current
---

# DBSCAN 数学基础

> 📖 Paper: Ester et al., [A Density-Based Algorithm...](../../../.documents/papers/dbscan/ester_1996_dbscan.pdf), KDD 1996, Sec. 2 (Definitions 1–6)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $D$ | 数据集 | Dataset | 所有样本点的集合 |
| $p, q, o$ | 数据点（单个样本） | Point | $p \in D$ |
| $\varepsilon$ | 邻域半径（eps 参数） | Epsilon / radius | $\varepsilon > 0$ |
| $MinPts$ | 核心点的最少邻居数（min_samples 参数） | Minimum points | $MinPts \geq 1$，含 $p$ 本身 |
| $N_\varepsilon(p)$ | p 的 ε 邻域（距离 p 不超过 ε 的点集）| ε-Neighborhood | $N_\varepsilon(p) \subseteq D$ |
| $dist(p, q)$ | p 和 q 之间的距离 | Distance function | $dist \geq 0$ |
| $C_k$ | 第 k 个簇 | Cluster k | $C_k \subseteq D$ |

> 📖 Paper: Ester et al., KDD 1996, Sec. 2 (Definitions 1–6)

---

## 核心公式

### 公式 1: ε-邻域 (ε-Neighborhood)

**直觉：** 以 p 为圆心、ε 为半径画一个球，球内所有点就是 p 的邻域

$$
N_\varepsilon(p) = \{ q \in D \mid dist(p, q) \leq \varepsilon \}
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 1

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------|
| $p$ | 待查询点 | 数据集中的任一点 |
| $\varepsilon$ | 邻域半径（用户指定的 `eps`）| 如 0.5 |
| $D$ | 全体数据集 | 所有训练点 |

**推导说明（核心点判断）：**

$$
\text{Step 1: } |N_\varepsilon(p)| = \sum_{q \in D} \mathbf{1}[dist(p, q) \leq \varepsilon]
$$

$$
\text{Step 2: 若 } |N_\varepsilon(p)| \geq MinPts \Rightarrow p \text{ 是核心点}
$$

$$
\text{Step 3: 否则 } p \text{ 为边界点或噪声点}
$$

> 📖 Paper: Ester et al., KDD 1996, Definitions 2–3

---

### 公式 2: 直接密度可达 (Directly Density-Reachable)

**直觉：** "q 直接可从 p 到达" = p 是核心点，且 q 就在 p 的邻域内——一步就够了

$$
q \text{ 直接密度可达自 } p \iff \begin{cases} q \in N_\varepsilon(p) \\ |N_\varepsilon(p)| \geq MinPts \end{cases}
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 3

**推导过程（从核心点判断到可达性）：**

$$
\text{Step 1: } p \text{ 是核心点} \iff |N_\varepsilon(p)| \geq MinPts
$$

$$
\text{Step 2: 若 } q \in N_\varepsilon(p) \Rightarrow dist(p, q) \leq \varepsilon
$$

$$
\text{Step 3 (非对称性): } q \text{ 从 } p \text{ 可达} \not\Rightarrow p \text{ 从 } q \text{ 可达（除非 } q \text{ 也是核心点）}
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 3, Note after

---

### 公式 3: 密度可达 (Density-Reachable, 传递闭包)

**直觉：** "q 密度可达自 p" = 存在一条核心点链，从 p 跳跃到 q——像接力赛一样

$$
q \text{ 密度可达自 } p \iff \exists p_1, \ldots, p_n \in D, \quad p_1 = p,\; p_n = q
$$

$$
\text{s.t. } \forall i \in \{1, \ldots, n-1\}: p_{i+1} \text{ 直接密度可达自 } p_i
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 4

**推导说明：**

$$
\text{Step 1: } p_1 = p \text{ 必须是核心点，才能开始链}
$$

$$
\text{Step 2: 中间每个 } p_i \text{（除最后一步）必须是核心点}
$$

$$
\text{Step 3: 最后一个点 } p_n = q \text{ 可以是边界点}
$$

> 📖 Paper: Ester et al., KDD 1996, Note after Definition 4（non-symmetric）

---

### 公式 4: 密度相连 (Density-Connected, 对称关系)

**直觉：** "p 和 q 密度相连" = 它们有共同的"祖先"核心点 o，从 o 都能到达两者

$$
p \text{ 和 } q \text{ 密度相连} \iff \exists o \in D \text{ s.t. } \begin{cases} p \text{ 密度可达自 } o \\ q \text{ 密度可达自 } o \end{cases}
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 5

**簇的正式定义（由密度相连导出）：**

$$
\text{Step 1: } \forall p \in C, \; \forall q \in D: q \text{ 密度可达自 } p \Rightarrow q \in C \quad \text{（最大化）}
$$

$$
\text{Step 2: } \forall p, q \in C: p \text{ 与 } q \text{ 密度相连} \quad \text{（连通性）}
$$

> 📖 Paper: Ester et al., KDD 1996, Definition 6 (Cluster)

---

## 公式关系图

```
ε-邻域 N_ε(p)  ──────→  核心点判断 (|N_ε(p)| ≥ MinPts)
        │                         │
        │                         ▼
        └─────────────→  直接密度可达 (1 步)
                                  │
                                  ▼ 传递闭包（链式）
                         密度可达 (多步)
                                  │
                                  ▼ 对称化（共同祖先）
                         密度相连 ──────→ 簇（Cluster）定义
                                                │
                                                ▼
                                        噪声点（不在任何簇内）
```

---

## 手算练习

### 练习 1: 判断核心点、边界点、噪声点

**题目：** 设 $\varepsilon = 1.5$，$MinPts = 3$（含自身）。数据点：
- A = (0, 0)，邻域内有 A, B, C → $|N_\varepsilon(A)| = 3$
- B = (1, 0)，邻域内有 A, B, C, D → $|N_\varepsilon(B)| = 4$
- C = (0, 1)，邻域内有 A, B, C → $|N_\varepsilon(C)| = 3$
- D = (1, 1)，邻域内有 B, D → $|N_\varepsilon(D)| = 2$
- E = (5, 5)，邻域内仅有 E → $|N_\varepsilon(E)| = 1$

**解答步骤：**

1. A: $|N_\varepsilon(A)| = 3 \geq 3$ → **核心点**
2. B: $|N_\varepsilon(B)| = 4 \geq 3$ → **核心点**
3. C: $|N_\varepsilon(C)| = 3 \geq 3$ → **核心点**
4. D: $|N_\varepsilon(D)| = 2 < 3$，但 $D \in N_\varepsilon(B)$（B 是核心点）→ **边界点**
5. E: $|N_\varepsilon(E)| = 1 < 3$，且不在任何核心点邻域 → **噪声点（-1）**

> 📖 Paper: Ester et al., KDD 1996, Definitions 2–3

### 练习 2: 验证密度相连

**题目：** 在练习 1 中，A 和 D 是否密度相连？

**解答步骤：**

1. 取中间点 o = B（B 是核心点）
2. A 密度可达自 B？→ A ∈ N_ε(B) 且 B 是核心点 → ✅ 直接可达
3. D 密度可达自 B？→ D ∈ N_ε(B) 且 B 是核心点 → ✅ 直接可达
4. 存在 o=B 使得 A 和 D 都从 o 密度可达 → **A 和 D 密度相连** → 同一簇

> 📖 Paper: Ester et al., KDD 1996, Definition 5

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| ε-邻域 | $N_\varepsilon(p) = \{q \mid dist(p,q) \leq \varepsilon\}$ | 计算每点的邻域 | 无 |
| 核心点 | $\|N_\varepsilon(p)\| \geq MinPts$ | 判断是否为核心点 | 公式 1 |
| 直接密度可达 | $q \in N_\varepsilon(p)$ 且 p 是核心点 | 一步扩展 | 公式 1, 核心点 |
| 密度可达 | 存在直接可达链 $p_1 \to \cdots \to p_n$ | 多步传播 | 公式 2 |
| 密度相连 | $\exists o$: p 和 q 都从 o 密度可达 | 定义簇内连通性 | 公式 3 |
| 簇 $C$ | 最大密度相连点集 | 输出簇定义 | 公式 4 |

> 📖 Paper: Ester et al., KDD 1996, Sec. 2 (Definitions 1–6)
