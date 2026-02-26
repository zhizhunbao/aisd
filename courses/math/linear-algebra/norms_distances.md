# Norms & Distances | 范数与距离度量

> **Purpose:** Define norms, distance metrics, and cosine similarity — the geometric building blocks for K-Means, KNN, DBSCAN, and hierarchical clustering.
> **Primary Source:** MML §3.1, §3.3, §3.4 (Deisenroth et al.)
> **See also:** [inner_product.md](inner_product.md) (prerequisite)
> **Prerequisites:** Basic vector operations (dot product, vector addition)

---

## Notation (符号约定)

| Symbol | Meaning (EN) | 含义 (中文) |
| --- | --- | --- |
| $\mathbb{R}$ | set of all real numbers | 实数集 |
| $\mathbb{R}^n$ | set of all $n$-dimensional real vectors | $n$ 维实数向量集 |

---

## §1 Norm (范数)

> 📚 Source: MML §3.1, p. 71 — Definition 3.1

### 1.1 What IS a Norm? (范数到底是什么)

A norm is a way to measure the length (size) of a vector — how far the tip of the arrow is from the origin.

范数就是衡量向量有多长（有多大）的方法——箭头的尖端离原点有多远。

**Concrete example:** You stand at the origin (0, 0) on a city map. Your friend is at (3, 4). How far away are they?
- Walk straight (ℓ₂ norm): $\sqrt{3^2 + 4^2} = 5$ — Pythagorean theorem
- Walk along streets (ℓ₁ norm): $|3| + |4| = 7$ — Manhattan grid

Both are valid "lengths" — they just measure differently. Different norms = different rulers.

两种都是合法的"长度"——只是测量方式不同。不同的范数 = 不同的尺子。

> 🔑 K-Means asks "which centroid is this point closest to?" — the answer depends on which norm you use. Default is ℓ₂.
> K-Means 问"这个点离哪个质心最近？"——答案取决于你用哪个范数。默认用 ℓ₂。

### 1.2 Three Rules a Norm Must Follow (范数的三条规则)

> 📚 MML §3.1, p. 71 — Definition 3.1

| Rule | Plain Language | Formula |
| --- | --- | --- |
| Scaling | 缩放向量 = 缩放长度 | $\|\lambda \mathbf{x}\| = |\lambda| \|\mathbf{x}\|$ |
| Triangle ineq. | 抄近路不能更远 | $\|\mathbf{x} + \mathbf{y}\| \leq \|\mathbf{x}\| + \|\mathbf{y}\|$ |
| Positive definite | 只有零向量长度为零 | $\|\mathbf{x}\| \geq 0$; $\|\mathbf{x}\| = 0 \iff \mathbf{x} = \mathbf{0}$ |

> 📖 $\|\mathbf{x}\|$ (double vertical bars) means "the norm (length) of vector $\mathbf{x}$."

### 1.3 Common Norms (常用范数)

> 📚 Source: MML §3.1, pp. 71–72

**ℓ₁ norm (Manhattan norm / 曼哈顿范数):**

Add up the absolute value of each component — like counting blocks on a city grid.

把每个分量的绝对值加起来——像在城市街道上数走了几个街区。

$\|\mathbf{x}\|_1 := \sum_{i=1}^{n} |x_i|$

> 📚 MML §3.1, Eq. 3.3

**Example:** $\mathbf{x} = [3, -4, 2]$ → $\|\mathbf{x}\|_1 = |3| + |-4| + |2| = 9$

---

**ℓ₂ norm (Euclidean norm / 欧几里得范数):**

Square each component, sum them, then take the square root — Pythagorean theorem.

把每个分量平方，加起来，再开根号——勾股定理。

$\|\mathbf{x}\|_2 := \sqrt{\sum_{i=1}^{n} x_i^2} = \sqrt{\mathbf{x}^\top \mathbf{x}}$

> 📚 MML §3.1, Eq. 3.4 — This is the default norm used throughout MML.

**Example:** $\mathbf{x} = [3, -4]$ → $\|\mathbf{x}\|_2 = \sqrt{9+16} = 5$

---

**General ℓₚ norm (通用 ℓₚ 范数):**

$\|\mathbf{x}\|_p := \left( \sum_{i=1}^{n} |x_i|^p \right)^{1/p}$

Unit ball shapes: ℓ₁ = diamond (菱形), ℓ₂ = circle (圆), ℓ∞ = square (正方形).

> 📚 MML §3.1, Figure 3.3

> 🔗 **Course Connection:**
> - **ML W6 K-Means:** SSE uses ℓ₂ norm squared: $SSE = \sum \|\mathbf{x} - \mathbf{m}_i\|_2^2$
> - **ML W6 DBSCAN:** ε-neighborhood uses ℓ₂ norm: $\|\mathbf{p} - \mathbf{q}\| \leq \varepsilon$
> - **ML W2 SVM:** ℓ₂ norm of weights $\|\mathbf{w}\|_2$ appears in the margin $\frac{2}{\|\mathbf{w}\|}$

---

## §2 Distance (距离)

> 📚 Source: MML §3.3, p. 75 — Definition 3.6

### 2.1 What IS Distance? (距离到底是什么)

Norm measures how long one vector is (from origin). Distance measures how far two vectors are from each other.

范数量的是一个向量有多长（离原点多远）。距离量的是两个向量之间有多远。

How to get distance from norm: subtract → then measure length. Distance = norm of the difference.

从范数得到距离：减 → 再量长度。距离 = 差向量的范数。

| Symbol | Meaning (EN) | 含义 (中文) | Type |
| --- | --- | --- | --- |
| $\mathbf{x}, \mathbf{y}$ | two vectors | 两个向量 | $\in \mathbb{R}^n$ |
| $d(\mathbf{x}, \mathbf{y})$ | distance | 距离 | $\geq 0$ |

$d(\mathbf{x}, \mathbf{y}) := \|\mathbf{x} - \mathbf{y}\|$

> 📚 MML §3.3, Eq. 3.21

### 2.2 Three Rules Distance Must Follow (距离的三条规则)

> 📚 Source: MML §3.4, p. 76

| Rule | Plain Language | Formula |
| --- | --- | --- |
| Identity | 距离为零 = 同一个点 | $d(\mathbf{x}, \mathbf{y}) = 0 \iff \mathbf{x} = \mathbf{y}$ |
| Symmetric | 从 A 到 B = 从 B 到 A | $d(\mathbf{x}, \mathbf{y}) = d(\mathbf{y}, \mathbf{x})$ |
| Triangle ineq. | 直达 ≤ 绕路 | $d(\mathbf{x}, \mathbf{z}) \leq d(\mathbf{x}, \mathbf{y}) + d(\mathbf{y}, \mathbf{z})$ |

> 🔑 Inner products and distances behave oppositely: similar vectors → large inner product, small distance.
> 内积与距离行为相反：相似的向量 → 大内积、小距离。

### 2.3 Squared Euclidean Distance (平方欧几里得距离)

In ML, we often skip the square root and use squared distance. Why? (1) Faster to compute. (2) `argmin` doesn't change (if A < B then A² < B²).

ML 中经常省掉开根号，用平方距离。(1) 算得更快 (2) 谁最小不变。

$d^2(\mathbf{x}, \mathbf{y}) = \|\mathbf{x} - \mathbf{y}\|_2^2 = \sum_{i=1}^{n} (x_i - y_i)^2$

Expansion:

$\|\mathbf{x} - \mathbf{y}\|_2^2 = \|\mathbf{x}\|^2 + \|\mathbf{y}\|^2 - 2\langle \mathbf{x}, \mathbf{y} \rangle$

> 🔑 This shows: minimizing distance ≈ maximizing inner product (when norms are fixed). K-Means and SVM both exploit this.
> 最小化距离 ≈ 最大化内积（范数固定时）。

### 2.4 Worked Example (手算例题)

> 📚 Adapted from MML Example 3.5, p. 75

**Problem:** Compute the Euclidean distance between $\mathbf{x} = [1, 2, 3]$ and $\mathbf{y} = [4, 0, 1]$.

**Solution:**

Step 1 — Subtract: $\mathbf{x} - \mathbf{y} = [-3, 2, 2]$

Step 2 — Square each: $9, 4, 4$

Step 3 — Sum and square-root: $d = \sqrt{9 + 4 + 4} = \sqrt{17} \approx 4.12$

> 🔗 **Course Connection:**
> - **ML W6 K-Means:** Assignment step — assign each $\mathbf{x}$ to nearest centroid: $\arg\min_i \|\mathbf{x} - \mathbf{m}_i\|^2$
> - **ML W6 Hierarchical:** All linkage methods compare pairwise distances
> - **ML W6 DBSCAN:** Core point definition — count neighbors with $d(\mathbf{p}, \mathbf{q}) \leq \varepsilon$

### 2.5 Practice Problems (练习题)

#### 🟢 Easy | 基础题

**P1.** Compute ℓ₁ and ℓ₂ norms for $\mathbf{x} = [3, -4]$, then find the Euclidean distance from $\mathbf{x}$ to the origin.

计算 $\mathbf{x} = [3, -4]$ 的 ℓ₁ 和 ℓ₂ 范数，然后求到原点的欧几里得距离。

> 📐 Original — based on MML §3.1

<details><summary>💡 Hint</summary>

ℓ₁ = sum of absolute values. ℓ₂ = square root of sum of squares. Distance to origin = norm of the vector itself.

</details>

<details><summary>✅ Solution</summary>

$\|\mathbf{x}\|_1 = |3| + |-4| = 7$

$\|\mathbf{x}\|_2 = \sqrt{9 + 16} = 5$

Distance to origin: $d(\mathbf{x}, \mathbf{0}) = \|\mathbf{x}\|_2 = 5$

Note: ℓ₁ ≠ ℓ₂ in general (7 ≠ 5). Always $\|\mathbf{x}\|_2 \leq \|\mathbf{x}\|_1$.

</details>

#### 🟡 Medium | 中等题

**P2.** K-Means with K=2. Data: $\{[0,0], [1,1], [5,5], [6,6]\}$. Initial centroids: $\mathbf{m}_1 = [0, 0]$, $\mathbf{m}_2 = [6, 6]$. Perform one iteration: (a) assign points, (b) update centroids, (c) compute SSE.

K-Means，K=2，4 个点，初始质心 $[0,0]$ 和 $[6,6]$。执行一次迭代。

> 📐 Original — applies MML §3.3 distance to K-Means SSE

<details><summary>💡 Hint</summary>

Assign each point to the nearest centroid using Euclidean distance. New centroid = mean of assigned points. SSE = sum of squared distances.

</details>

<details><summary>✅ Solution</summary>

**(a) Assign:**

| Point | $d$ to $[0,0]$ | $d$ to $[6,6]$ | Cluster |
| --- | --- | --- | --- |
| [0,0] | 0 | $\sqrt{72} \approx 8.49$ | C₁ |
| [1,1] | $\sqrt{2} \approx 1.41$ | $\sqrt{50} \approx 7.07$ | C₁ |
| [5,5] | $\sqrt{50} \approx 7.07$ | $\sqrt{2} \approx 1.41$ | C₂ |
| [6,6] | $\sqrt{72} \approx 8.49$ | 0 | C₂ |

**(b) Update centroids:**

$\mathbf{m}_1 = \frac{[0,0]+[1,1]}{2} = [0.5, 0.5], \quad \mathbf{m}_2 = \frac{[5,5]+[6,6]}{2} = [5.5, 5.5]$

**(c) SSE:**

$SSE = 0.5 + 0.5 + 0.5 + 0.5 = 2.0$

</details>

#### 🔴 Hard | 挑战题

**P3.** (a) Prove: $\|\mathbf{x} - \mathbf{y}\|_2^2 = \|\mathbf{x}\|^2 + \|\mathbf{y}\|^2 - 2\mathbf{x}^\top\mathbf{y}$. (b) Why does K-Means use squared distance instead of plain distance? Give two reasons.

(a) 证明平方距离展开公式。(b) 为什么 K-Means 用平方距离？

> 📐 Original — based on MML §3.3

<details><summary>💡 Hint</summary>

(a) Expand $(\mathbf{x} - \mathbf{y})^\top(\mathbf{x} - \mathbf{y})$. (b) Think about differentiability and computational cost.

</details>

<details><summary>✅ Solution</summary>

**(a) Proof:**

$\|\mathbf{x} - \mathbf{y}\|_2^2 = (\mathbf{x} - \mathbf{y})^\top(\mathbf{x} - \mathbf{y}) = \mathbf{x}^\top\mathbf{x} - 2\mathbf{x}^\top\mathbf{y} + \mathbf{y}^\top\mathbf{y} = \|\mathbf{x}\|^2 - 2\mathbf{x}^\top\mathbf{y} + \|\mathbf{y}\|^2 \quad \blacksquare$

**(b) Two reasons:**

**Reason 1 (Differentiable):** $\sqrt{\cdot}$ is not differentiable at 0. Squared distance is smooth everywhere, so setting $\frac{\partial SSE}{\partial \mathbf{m}} = 0$ cleanly gives centroid = mean.

**Reason 2 (Same winner):** $\sqrt{\cdot}$ is monotonically increasing, so $\arg\min d = \arg\min d^2$. Skipping the square root saves computation without changing which centroid wins.

</details>

---

## §3 Cosine Similarity (余弦相似度)

> 📚 Source: MML §3.4, pp. 76–77 — Eq. 3.25

### 3.1 What IS Cosine Similarity? (余弦相似度是什么)

Euclidean distance cares about position — how far apart two points are. Cosine similarity cares about direction — are two arrows pointing the same way?

欧几里得距离关心位置——两个点有多远。余弦相似度关心方向——两个箭头是不是指向同一个方向？

When to use which:
- Euclidean: data where magnitude matters (height, weight) → K-Means
- Cosine: data where only direction matters (document word counts) → text clustering, NLP

什么时候用哪个：
- 欧几里得：大小有意义时（身高体重）→ K-Means
- 余弦：只有方向有意义时（文档词频）→ 文本聚类、NLP

### 3.2 Definition (定义)

| Symbol | Meaning (EN) | 含义 (中文) | Range |
| --- | --- | --- | --- |
| $\omega$ | angle between vectors | 夹角 | $[0, \pi]$ |
| $\cos \omega$ | cosine similarity | 余弦相似度 | $[-1, 1]$ |

$\cos \omega = \frac{\mathbf{x}^\top \mathbf{y}}{\|\mathbf{x}\|_2 \; \|\mathbf{y}\|_2}$

> 📚 MML §3.4, Eq. 3.25

| Value | Direction | 含义 |
| --- | --- | --- |
| $\cos \omega = 1$ | Same direction | 方向完全相同 |
| $\cos \omega = 0$ | Perpendicular | 正交（无关） |
| $\cos \omega = -1$ | Opposite | 方向完全相反 |

### 3.3 Cosine Distance (余弦距离)

$d_{\cos}(\mathbf{x}, \mathbf{y}) = 1 - \cos \omega$

> ⚠️ Cosine distance is not a true metric (fails triangle inequality). But it is widely used in NLP and text clustering.
> 余弦距离不是严格的度量（不满足三角不等式），但在 NLP 和文本聚类中广泛使用。

> 🔗 **Course Connection:**
> - **ML W6 Clustering:** Text/document clustering often uses cosine similarity instead of Euclidean distance
> - **NLP:** Word embedding similarity (Word2Vec, BERT) uses cosine similarity

---

## Quick Reference (速查表)

| Concept | What It Does (干什么的) | Formula | Source |
| --- | --- | --- | --- |
| ℓ₁ norm | 绝对值加起来 | $\sum |x_i|$ | MML §3.1, Eq. 3.3 |
| ℓ₂ norm | 勾股定理算长度 | $\sqrt{\sum x_i^2}$ | MML §3.1, Eq. 3.4 |
| Euclidean dist. | 两点直线距离 | $\|\mathbf{x} - \mathbf{y}\|_2$ | MML §3.3, Eq. 3.21 |
| Squared dist. | 省掉开根号 | $\sum (x_i - y_i)^2$ | MML §3.3 |
| Cosine sim. | 方向像不像 | $\frac{\mathbf{x}^\top\mathbf{y}}{\|\mathbf{x}\|\|\mathbf{y}\|}$ | MML §3.4, Eq. 3.25 |

---

## Source Index (来源索引)

| Section | Textbook | Chapter/Equation | Pages |
| --- | --- | --- | --- |
| §1 | MML | §3.1, Def. 3.1, Eq. 3.1–3.4 | pp. 71–72 |
| §2 | MML | §3.3, Def. 3.6, Eq. 3.16–3.21 | pp. 75–76 |
| §2 | MML | §3.4, metric properties | p. 76 |
| §3 | MML | §3.4, Eq. 3.24–3.25 | pp. 76–77 |