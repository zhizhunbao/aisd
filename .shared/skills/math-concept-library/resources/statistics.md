# Statistics & Probability Concepts (统计与概率概念)

---

### Gaussian / Normal Distribution (高斯分布 / 正态分布)

**Tags:** `#statistics` `#distribution` `#ml-week6` `#mv-week2`

**📌 One-line Definition:**
> The Gaussian distribution is the classic "bell curve" — most data clusters near the mean, with exponentially fewer observations farther away.
>> 高斯分布是经典的"钟形曲线" — 大多数数据聚集在均值附近，越远的观测指数级减少。

**📐 Formula:**
```
P(x|μ,σ) = (1 / √(2πσ²)) × e^(-(x-μ)² / (2σ²))
```
- x = data point value
- μ (mu) = mean — center of the bell curve (where the peak is)
- σ (sigma) = standard deviation — width of the bell (larger σ = wider, flatter)
- σ² = variance = σ squared
- π ≈ 3.14159, e ≈ 2.71828
- Output = probability density at x (NOT probability; must integrate over a range)

**💡 Intuition (直觉理解):**
> **The dartboard analogy:**
> Imagine throwing darts at a target. Most darts land near the bullseye (μ). Some scatter a bit (within 1σ = 68%), fewer scatter more (within 2σ = 95%), and very few miss wildly (beyond 3σ = 0.3%). The bell curve describes this pattern. σ is how "shaky" your hand is — bigger σ = more scatter.
>
> **The 68-95-99.7 rule:**
> - 68% of data falls within μ ± 1σ
> - 95% within μ ± 2σ
> - 99.7% within μ ± 3σ
>> **飞镖靶类比：**
>> 想象向靶子扔飞镖。大部分飞镖落在靶心(μ)附近。一些偏离一点（1σ内 = 68%），更少偏离更多（2σ内 = 95%），极少数偏离很远（3σ外 = 0.3%）。钟形曲线描述了这个模式。σ是你手有多"抖" — σ越大 = 散布越大。
>>
>> **68-95-99.7法则：**
>> - 68%的数据在 μ ± 1σ 内
>> - 95%在 μ ± 2σ 内
>> - 99.7%在 μ ± 3σ 内

**🔢 Worked Example:**
```
μ = 170cm (average height), σ = 10cm

P(x=170) = (1/√(2π×100)) × e^0 = 1/25.07 ≈ 0.0399
P(x=180) = (1/25.07) × e^(-100/200) = 0.0399 × 0.607 ≈ 0.0242
P(x=190) = (1/25.07) × e^(-400/200) = 0.0399 × 0.135 ≈ 0.0054

→ At the mean (170cm): highest density
→ 1σ away (180cm): drops to ~60%
→ 2σ away (190cm): drops to ~14%
```

**⚙️ In Practice (实际使用):**
```python
import numpy as np
from scipy.stats import norm

# Create a Gaussian distribution
mu, sigma = 170, 10
dist = norm(loc=mu, scale=sigma)

# Probability density at a point
pdf_at_180 = dist.pdf(180)  # ≈ 0.0242

# Probability within a range
prob_160_to_180 = dist.cdf(180) - dist.cdf(160)  # ≈ 0.6827
```

**🔗 Related Concepts:**
→ see: Gaussian Filter (uses Gaussian shape as convolution weights)
→ see: EM Algorithm (fits mixtures of Gaussians to data)
→ see: Bayes' Theorem (used in EM's E-step with Gaussian likelihoods)

**📚 Appears In:**
- MV Week 2 §5 (Gaussian Blur — uses Gaussian as kernel weights)
- ML Week 6 §6 (EM clustering — models clusters as Gaussian distributions)

---

### Euclidean Distance (欧氏距离)

**Tags:** `#statistics` `#distance` `#ml-week6` `#mv-week2`

**📌 One-line Definition:**
> Euclidean distance is the "straight-line" distance between two points in any number of dimensions — the most common distance metric.
>> 欧氏距离是任意维度中两点之间的"直线"距离 — 最常用的距离度量。

**📐 Formula:**
```
d(x, y) = √( Σᵢ (xᵢ - yᵢ)² )

2D:  d = √((x₁-y₁)² + (x₂-y₂)²)
3D:  d = √((x₁-y₁)² + (x₂-y₂)² + (x₃-y₃)²)
```
- x, y = two data points (vectors)
- xᵢ, yᵢ = the i-th dimension/feature of each point
- Σᵢ = sum over all dimensions
- Always ≥ 0; d = 0 only when x = y

**💡 Intuition (直觉理解):**
> It's just the **Pythagorean theorem** extended to any number of dimensions. In 2D, it's how you measure distance with a ruler on a map. In 3D, it's the length of a string stretched between two points. In 100D, it's the same idea — just more dimensions in the sum.
>> 就是**勾股定理**扩展到任意维度。在2D中，就是用尺子在地图上量距离。在3D中，就是两点之间拉直的线的长度。在100D中，同样的思路 — 只是求和中有更多维度。

**🔢 Worked Example:**
```
Point A = (1, 3)
Point B = (4, 7)

d = √((4-1)² + (7-3)²) = √(9 + 16) = √25 = 5
```

**⚙️ In Practice (实际使用):**
```python
import numpy as np

a = np.array([1, 3])
b = np.array([4, 7])
d = np.linalg.norm(a - b)  # = 5.0
```

**⚠️ Common Mistake:**
> In high dimensions, Euclidean distance becomes **less meaningful** (curse of dimensionality). All points tend to become equally far from each other. At 100+ dimensions, consider cosine similarity or Manhattan distance instead.
>> 在高维空间中，欧氏距离变得**不太有意义**（维度灾难）。所有点趋向于彼此等距。100+维时，考虑余弦相似度或曼哈顿距离。

**🔗 Related Concepts:**
→ see: SSE (uses squared Euclidean distance)
→ see: K-Means (assigns points based on Euclidean distance to centroid)
→ see: Gradient Magnitude (√(Gx²+Gy²) is Euclidean norm of gradient vector)

**📚 Appears In:**
- ML Week 6 §3 (K-Means — distance to centroid)
- ML Week 6 §7 (Cluster validity metrics)
- MV Week 2 §8 (Canny — gradient magnitude)

---

### Bayes' Theorem (贝叶斯定理)

**Tags:** `#statistics` `#probability` `#ml-week6`

**📌 One-line Definition:**
> Bayes' theorem calculates the probability of a hypothesis given observed evidence — it "flips" the conditional probability using prior knowledge.
>> 贝叶斯定理计算给定观测证据下假设的概率 — 它利用先验知识"翻转"条件概率。

**📐 Formula:**
```
P(H|E) = P(E|H) × P(H) / P(E)
```
- P(H|E) = **posterior** — probability of hypothesis H given evidence E (what we want)
- P(E|H) = **likelihood** — probability of seeing evidence E if hypothesis H is true
- P(H) = **prior** — initial belief about H before seeing evidence
- P(E) = **evidence** — total probability of E (normalizing constant)

**In EM clustering:**
```
P(cluster_b | xᵢ) = P(xᵢ | cluster_b) × P(cluster_b) / P(xᵢ)
```
- "Given this data point, what's the probability it belongs to cluster b?"

**💡 Intuition (直觉理解):**
> **Medical test analogy:**
> A disease test is 99% accurate. You test positive. Are you sick?
> It depends on how **rare** the disease is (prior). If only 1 in 10,000 people have it, even with a positive test, the chance you're actually sick is only ~1%. Bayes' theorem accounts for this base rate.
>
> **In clustering:** "Given this point, which cluster does it belong to?" = "Given the test result, which disease do I have?" The prior P(cluster) is like the base rate of each disease.
>> **医学检测类比：**
>> 一个疾病测试准确率99%。你测试阳性。你生病了吗？
>> 取决于疾病有多**罕见**（先验）。如果只有万分之一的人患病，即使阳性，你实际生病的概率也只有~1%。贝叶斯定理考虑了这个基础率。
>>
>> **在聚类中：** "给定这个点，它属于哪个簇？" = "给定检测结果，我患的是哪种病？"先验P(簇)就像每种病的基础发病率。

**🔗 Related Concepts:**
→ see: EM Algorithm (E-step uses Bayes' theorem)
→ see: Gaussian Distribution (likelihood in EM is a Gaussian PDF)

**📚 Appears In:**
- ML Week 6 §6 (EM Algorithm — E-step posterior computation)

---

### SSE — Sum of Squared Error (误差平方和)

**Tags:** `#statistics` `#evaluation` `#clustering` `#ml-week6`

**📌 One-line Definition:**
> SSE measures the total "spread" of data points around their cluster centroids — lower SSE = tighter, more compact clusters.
>> SSE衡量数据点围绕各自簇质心的总"散布程度" — SSE越低 = 簇越紧凑。

**📐 Formula:**
```
SSE = Σᵢ Σ_{x∈Cᵢ} ‖x - mᵢ‖²
```
- Σᵢ = sum over all K clusters (i = 1 to K)
- Σ_{x∈Cᵢ} = sum over all points x in cluster i
- mᵢ = centroid (mean) of cluster i
- ‖x - mᵢ‖² = squared Euclidean distance from point x to its cluster center

**Related decomposition:**
```
TSS = SSE + SSB    (total = within-cluster + between-cluster)

SSB = Σᵢ |Cᵢ| × ‖mᵢ - m‖²
TSS = Σ ‖x - m‖²

where m = grand mean (mean of ALL data points)
```

**💡 Intuition (直觉理解):**
> **The messy room analogy:**
> Each cluster = a room. Each point's distance to the centroid = how far an item is from the center of the room. SSE = total messiness across all rooms. Lower SSE = tidier rooms = better clustering.
>
> **Key trap:** SSE ALWAYS decreases when you add more clusters. With K=N (every point is its own cluster), SSE=0. So "lowest SSE" doesn't mean "best K". Use the **elbow method** — plot SSE vs K and find where the curve "bends".
>> **凌乱房间类比：**
>> 每个簇 = 一个房间。每个点到质心的距离 = 物品离房间中心多远。SSE = 所有房间的总凌乱度。SSE越低 = 房间越整齐 = 聚类越好。
>>
>> **关键陷阱：** 增加簇数时SSE总是下降。当K=N（每个点自成一簇），SSE=0。所以"最低SSE"不等于"最优K"。用**肘部法** — 画SSE vs K的图，找曲线"弯折"的地方。

**🔢 Worked Example:**
```
Data: {1, 3, 7, 9}, K=2
Cluster 1: {1, 3} → m₁ = 2
Cluster 2: {7, 9} → m₂ = 8

SSE = (1-2)² + (3-2)² + (7-8)² + (9-8)² = 1+1+1+1 = 4
```

**🔗 Related Concepts:**
→ see: Euclidean Distance (SSE uses squared Euclidean)
→ see: K-Means (objective function is to minimize SSE)
→ see: Silhouette Coefficient (alternative quality metric)

**📚 Appears In:**
- ML Week 6 §3 (K-Means objective function)
- ML Week 6 §7 (Cluster validity — SSE, SSB, TSS)

---

### Silhouette Coefficient (轮廓系数)

**Tags:** `#statistics` `#evaluation` `#clustering` `#ml-week6`

**📌 One-line Definition:**
> The silhouette coefficient measures how well each individual point fits in its assigned cluster — ranging from -1 (wrong cluster) to +1 (perfect fit).
>> 轮廓系数衡量每个单独点在其分配簇中的拟合程度 — 从-1（分配错误）到+1（完美拟合）。

**📐 Formula:**
```
s(i) = (b - a) / max(a, b)
```
- a = average distance from point i to all OTHER points **in its own cluster** (cohesion)
- b = minimum (average distance from i to all points in EACH other cluster) (separation)
- s ∈ [-1, 1]
  - s ≈ 1: point is well inside its cluster (a << b)
  - s ≈ 0: point is on the boundary between clusters (a ≈ b)
  - s ≈ -1: point is probably in the wrong cluster (a >> b)

**💡 Intuition (直觉理解):**
> **The team player analogy:**
> Imagine a player who practices with two sports teams. a = how well they fit with their current team (avg distance to teammates). b = how well they'd fit with the nearest rival team (avg distance to rival players). If b >> a → great fit with current team (s ≈ 1). If a >> b → should switch teams (s ≈ -1).
>> **队员类比：**
>> 想象一个同时跟两支队训练的球员。a = 跟当前队的契合度（到队友的平均距离）。b = 跟最近对手队的契合度（到对手球员的平均距离）。如果b >> a → 跟当前队很合（s ≈ 1）。如果a >> b → 应该换队（s ≈ -1）。

**🔢 Worked Example:**
```
Point i in Cluster 1. Three clusters total.
Distances from i to Cluster 1 members: 1, 2, 3 → a = (1+2+3)/3 = 2
Distances from i to Cluster 2 members: 5, 6, 7 → avg = 6
Distances from i to Cluster 3 members: 8, 9, 10 → avg = 9
b = min(6, 9) = 6

s = (6 - 2) / max(2, 6) = 4/6 = 0.67 → good fit!
```

**🔗 Related Concepts:**
→ see: SSE (alternative cluster quality metric — per-cluster vs per-point)
→ see: Euclidean Distance (used to compute a and b)

**📚 Appears In:**
- ML Week 6 §7 (Cluster validity — Silhouette Coefficient)
