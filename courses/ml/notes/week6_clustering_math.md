# Week 6: Clustering — 数学公式 + 手算

> **Source:** slides `Week6Clustering.pdf` + storyline
> **Scope:** K-Means SSE, Hierarchical linkage calculations, DBSCAN point classification, EM formulas, Silhouette Coefficient
> **See also:** [week6_clustering_cheatsheet.md](week6_clustering_cheatsheet.md) (概念速查) | [week6_clustering_code.md](week6_clustering_code.md) (代码)

---

## K-Means Objective Function

### 📐 Formula

- **SSE (Sum of Squared Error):**

$$SSE = \sum_{i=1}^{K} \sum_{x \in C_i} \|x - m_i\|^2$$

$K$ = number of clusters, $C_i$ = set of points in cluster $i$, $x$ = data point, $m_i$ = centroid (mean) of cluster $i$, $\|x - m_i\|^2$ = squared Euclidean distance

- **Centroid update:**

$$m_i = \frac{1}{|C_i|} \sum_{x \in C_i} x$$

$|C_i|$ = number of points in cluster $i$

- **K-Means Complexity:**

$$O(n \times K \times I \times d)$$

$n$ = number of data points, $K$ = number of clusters, $I$ = number of iterations, $d$ = number of dimensions/attributes

### 📝 Hand Calc

- **SSE computation:** Data = {1, 2, 4, 5}, K=2, clusters {1,2} and {4,5}

  **Step 1: Compute centroids**

$$m_1 = \frac{1+2}{2} = 1.5, \quad m_2 = \frac{4+5}{2} = 4.5$$

**Step 2: Compute SSE per cluster**

$$SSE_1 = (1-1.5)^2 + (2-1.5)^2 = 0.25 + 0.25 = 0.5$$

$$SSE_2 = (4-4.5)^2 + (5-4.5)^2 = 0.25 + 0.25 = 0.5$$

**Step 3: Total SSE**

$$SSE = 0.5 + 0.5 = \mathbf{1.0}$$

---

## Cluster Validity: SSE, SSB, TSS

### 📐 Formula

- **SSE (Within-Cluster Sum of Squares / Cohesion):**

$$SSE = \sum_{i=1}^{K} \sum_{x \in C_i} (x - m_i)^2$$

$m_i$ = centroid of cluster $i$

- **SSB (Between-Cluster Sum of Squares / Separation):**

$$SSB = \sum_{i=1}^{K} |C_i| \cdot (m - m_i)^2$$

$|C_i|$ = number of points in cluster $i$, $m$ = global (grand) mean of all data points, $m_i$ = centroid of cluster $i$

- **TSS (Total Sum of Squares):**

$$TSS = \sum_{\text{all } x} (x - m)^2$$

- **Identity:**

$$SSE + SSB = TSS = \text{constant}$$

### 📝 Hand Calc

- **Verify SSE + SSB = TSS:** Data = {1, 2, 4, 5}, grand mean $m = 3$

  **Case K=1** (one big cluster):

$$SSE = (1-3)^2 + (2-3)^2 + (4-3)^2 + (5-3)^2 = 4+1+1+4 = \mathbf{10}$$

$$SSB = 4 \times (3-3)^2 = \mathbf{0}$$

$$\text{Total} = 10 + 0 = \mathbf{10} \quad \checkmark$$

**Case K=2** (clusters {1,2} m₁=1.5, {4,5} m₂=4.5):

$$SSE = (1-1.5)^2 + (2-1.5)^2 + (4-4.5)^2 + (5-4.5)^2 = 4 \times 0.25 = \mathbf{1}$$

$$SSB = 2 \times (1.5-3)^2 + 2 \times (4.5-3)^2 = 2(2.25) + 2(2.25) = \mathbf{9}$$

$$\text{Total} = 1 + 9 = \mathbf{10} \quad \checkmark$$

**Key insight:** More clusters → SSE↓, SSB↑, but total is always 10.

---

## Silhouette Coefficient

### 📐 Formula

- **Per-point silhouette:**

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)}$$

$a_i$ = average distance from point $i$ to all other points in **its own cluster** (cohesion), $b_i$ = minimum of (average distance from point $i$ to all points in **each other cluster**) (separation)

- **Range:** $s_i \in [-1, 1]$
  - $s \approx 1$: well-clustered (far from other clusters, close to own)
  - $s \approx 0$: on boundary between two clusters
  - $s \approx -1$: misclassified (closer to another cluster)

### 📝 Hand Calc

- **Example:** 3 clusters, point P in cluster A

  **Step 1: Compute a (within-cluster)**

$$a = \text{avg distance of P to all other points in cluster A}$$

Suppose distances to 3 other points in A: 2, 3, 4

$$a = \frac{2+3+4}{3} = 3.0$$

**Step 2: Compute b (nearest-cluster)**

Avg distance of P to all points in cluster B: $\frac{5+6+7}{3} = 6.0$

Avg distance of P to all points in cluster C: $\frac{8+9+10}{3} = 9.0$

$$b = \min(6.0, 9.0) = 6.0$$

**Step 3: Compute silhouette**

$$s = \frac{b - a}{\max(a, b)} = \frac{6.0 - 3.0}{\max(3.0, 6.0)} = \frac{3.0}{6.0} = \mathbf{0.5}$$

Interpretation: reasonably well-clustered but not perfect.

---

## Hierarchical Clustering: Linkage Distances

### 📐 Formula

- **MIN (Single Linkage):**

$$d(C_i, C_j) = \min_{x \in C_i, \; y \in C_j} \|x - y\|$$

Minimum distance between any pair of points across two clusters

- **MAX (Complete Linkage):**

$$d(C_i, C_j) = \max_{x \in C_i, \; y \in C_j} \|x - y\|$$

Maximum distance between any pair of points across two clusters

- **Group Average:**

$$d(C_i, C_j) = \frac{1}{|C_i| \cdot |C_j|} \sum_{x \in C_i} \sum_{y \in C_j} \|x - y\|$$

Average of all pairwise distances between the two clusters

- **Ward's Method:**

$$d(C_i, C_j) = SSE(C_i \cup C_j) - SSE(C_i) - SSE(C_j)$$

Increase in total SSE caused by merging the two clusters

### 📝 Hand Calc

- **Agglomerative clustering with MIN linkage:** 5 points, initial distance matrix

  Given: points p1–p5 with distance matrix. Find the two closest points → merge → update matrix → repeat.

  **Step 1:** Find minimum in distance matrix → e.g., d(p2, p5) = 1.2 → merge into C₁={p2, p5}

  **Step 2:** Recompute distances using MIN:

$$d(C_1, p_1) = \min(d(p_2, p_1), \; d(p_5, p_1))$$

**Step 3:** Repeat until one cluster remains. Dendrogram y-axis shows merge distance.

---

## DBSCAN Point Classification

### 📐 Formula

- **Core point condition:**

$$|\{q : \|p - q\| \leq \varepsilon\}| \geq \text{MinPts}$$

Point $p$ is core if at least MinPts points (including $p$ itself) are within radius $\varepsilon$

- **Border point condition:** NOT core, but $\exists$ core point $q$ such that $\|p - q\| \leq \varepsilon$

- **Noise point condition:** NOT core AND NOT border

### 📝 Hand Calc

- **Classify points:** ε = 1.5, MinPts = 4

  Given points with pairwise distances:

  | Point | Neighbors within ε=1.5 (including self) | Count | Classification |
  | ----- | --------------------------------------- | ----- | -------------- |
  | A     | {A, B, C, D, E}                         | 5 ≥ 4 | **Core**       |
  | B     | {A, B, C, D}                            | 4 ≥ 4 | **Core**       |
  | C     | {A, B, C}                               | 3 < 4 | → check below  |
  | D     | {A, B, D}                               | 3 < 4 | → check below  |
  | E     | {A, E}                                  | 2 < 4 | → check below  |
  | F     | {F}                                     | 1 < 4 | → check below  |

  C and D are not core, but within ε of core point A → **Border**

  E is not core, but within ε of core point A → **Border**

  F is not core and not within ε of any core → **Noise**

---

## EM Algorithm Formulas

### 📐 Formula

- **Gaussian PDF:**

$$P(x_i | \Theta) = \frac{1}{\sqrt{2\pi\sigma^2}} \cdot \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

$x_i$ = data point, $\mu$ = mean of the Gaussian, $\sigma^2$ = variance, $\Theta = \{\mu, \sigma^2\}$

- **E-step (compute posterior / soft assignment):**

$$b_i = P(b|x_i) = \frac{P(x_i|b) \cdot P(b)}{P(x_i|b) \cdot P(b) + P(x_i|a) \cdot P(a)}$$

$b_i$ = posterior probability that point $x_i$ belongs to cluster $b$, $P(x_i|b)$ = Gaussian PDF of cluster $b$ evaluated at $x_i$, $P(b)$ = mixing weight (prior) of cluster $b$

- **M-step (re-estimate parameters):**

$$\mu_b = \frac{\sum_{i} b_i \cdot x_i}{\sum_{i} b_i} \quad \text{(weighted mean)}$$

$$\sigma_b^2 = \frac{\sum_{i} b_i (x_i - \mu_b)^2}{\sum_{i} b_i} \quad \text{(weighted variance)}$$

$$P(b) = \frac{\sum_{i} b_i}{N} \quad \text{(updated mixing weight)}$$

$b_i$ = posterior from E-step, $N$ = total number of data points

### 📝 Hand Calc

- **One iteration of EM (1D, 2 clusters):** data = {1, 2, 4, 5}, initial: $\mu_a=1.5$, $\sigma_a=1$, $\mu_b=4.5$, $\sigma_b=1$, $P(a)=P(b)=0.5$

  **E-step for point x=2:**

  **Step 1:** Compute likelihoods

$$P(x=2|a) = \frac{1}{\sqrt{2\pi(1)}} \exp\left(-\frac{(2-1.5)^2}{2(1)}\right) = 0.3521$$

$$P(x=2|b) = \frac{1}{\sqrt{2\pi(1)}} \exp\left(-\frac{(2-4.5)^2}{2(1)}\right) = 0.0175$$

**Step 2:** Compute posterior

$$P(a|x=2) = \frac{0.3521 \times 0.5}{0.3521 \times 0.5 + 0.0175 \times 0.5} = \frac{0.1761}{0.1848} = \mathbf{0.953}$$

$$P(b|x=2) = 1 - 0.953 = \mathbf{0.047}$$

Point x=2 has 95.3% probability of belonging to cluster a → soft assignment.

---

## Quick Formula Reference

| Name             | Formula                                                    | Key Params                           |
| ---------------- | ---------------------------------------------------------- | ------------------------------------ | ---------------------- | ------------------------------ | --- | -------------- |
| K-Means SSE      | $SSE = \sum_i \sum_{x \in C_i} \|x - m_i\|^2$              | $m_i$=centroid, $C_i$=cluster        |
| Centroid update  | $m_i = \frac{1}{                                           | C_i                                  | } \sum\_{x \in C_i} x$ | Mean of points in cluster      |
| SSB              | $\sum_i                                                    | C_i                                  | \cdot (m - m_i)^2$     | $m$=global mean, $             | C_i | $=cluster size |
| SSE+SSB identity | $SSE + SSB = TSS$                                          | TSS is constant for given data       |
| Silhouette       | $s = \frac{b-a}{\max(a,b)}$                                | $a$=intra avg, $b$=nearest-inter avg |
| MIN linkage      | $\min_{x \in C_i, y \in C_j} \|x-y\|$                      | Nearest pair across clusters         |
| MAX linkage      | $\max_{x \in C_i, y \in C_j} \|x-y\|$                      | Farthest pair across clusters        |
| Core point       | $\|\{q: \|p-q\| \leq \varepsilon\}\| \geq \text{MinPts}$   | Includes point itself                |
| Gaussian PDF     | $\frac{1}{\sqrt{2\pi\sigma^2}} e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$=mean, $\sigma^2$=variance      |
| EM E-step        | $b_i = \frac{P(x_i                                         | b)P(b)}{\sum_j P(x_i                 | j)P(j)}$               | Posterior = Lik×Prior/Evidence |
| EM M-step μ      | $\mu_b = \frac{\sum b_i x_i}{\sum b_i}$                    | Weighted mean                        |
| EM M-step σ²     | $\sigma_b^2 = \frac{\sum b_i(x_i - \mu_b)^2}{\sum b_i}$    | Weighted variance                    |
| EM M-step P(b)   | $P(b) = \frac{\sum b_i}{N}$                                | Updated mixing weight                |
