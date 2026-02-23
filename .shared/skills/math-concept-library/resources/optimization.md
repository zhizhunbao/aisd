# Optimization (优化方法)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

### Maximum Margin Classifier Optimization (最大间隔分类器优化)

**Tags:** `#optimization` `#svm` `#ml-week2`

**📌 One-line Definition:**

> The quadratic optimization problem formulating the SVM objective: to maximize the margin width without misclassifying any points (Hard Margin).
>
> > 描述SVM目标的二次优化问题：在不造成任何误分类的情况下最大化间隔宽度(硬间隔)。

**📐 Formula:**

```
Maximize:    2 / ||w||
Subject to:  y_i (w · x_i + b) >= 1   for all i = 1, ..., n
```

- ||w|| = Euclidean norm of the weight vector (weights determining hyperplane orientation)
- y_i = Class label of the i-th training instance (+1 or -1)
- x_i = Feature vector of the i-th training instance
- b = Bias term (shifts hyperplane offset from origin)

**💡 Intuition (直觉理解):**

> Since margin width is 2/||w||, maximizing the margin is mathematically identical to minimizing ||w||. The constraint says that every single data point must lie perfectly outside the "street" margin on the correct side (defined by >= 1 or <= -1 mapped elegantly via y_i).
>
> > 由于间隔宽度是 2/||w||，从数学上讲最大化间隔等同于最小化 ||w||。约束条件表示，每一个数据点都必须完美地落在正确类别一侧的间隔"街道"之外（通过 y_i 优雅地映射在一起的 >= 1 约束）。

**⚙️ In Practice (实际使用):**

> Solved under the hood in implementations like `sklearn.svm.SVC` using quadratic programming (specifically SMO algorithm), optimized via Lagrange multipliers.
>
> > 在诸如 `sklearn.svm.SVC` 等实现底层中通过二次规划（确切说是SMO算法）利用拉格朗日乘子求解。

**🔗 Related Concepts:**

> → concept: Support Vector Machine in concept-glossary
> → concept: Hard/Soft Margin in concept-glossary

**📚 Appears In:**

> - ML Week 2: Support Vector Machines

---

### RBF / Gaussian Kernel (径向基函数 / 高斯核)

**Tags:** `#optimization` `#svm` `#kernel` `#ml-week2`

**📌 One-line Definition:**

> The Radial Basis Function kernel maps data to infinite-dimensional space by computing similarity as an exponentially decaying function of squared Euclidean distance between two points.
>
> > 径向基函数核通过计算两点之间欧氏距离平方的指数衰减函数来将数据映射到无限维空间。

**📐 Formula:**

```
K(x, z) = exp(-γ × ||x - z||²)

where:
  x, z = two data points (vectors)
  ||x - z||² = squared Euclidean distance
  γ (gamma) = 1 / (2σ²), controls influence radius

Output range: (0, 1]
  K = 1 when x = z (identical points)
  K → 0 as distance → ∞ (very different points)
```

**💡 Intuition (直觉理解):**

> **The campfire analogy:** Each support vector is a campfire. γ controls how quickly the warmth fades with distance. Low γ = bonfire (warmth reaches far, smooth boundary). High γ = candle (warmth only near the flame, tight "islands").
>
> > **篝火类比：** 每个支持向量是一堆篝火。γ 控制温暖随距离衰减的速度。低 γ = 大篝火（温暖传很远，平滑边界）。高 γ = 蜡烛（只有靠近才暖，形成紧凑"孤岛"）。

**⚠️ Common Mistake:**

> High γ does NOT mean "better fit." It means each support vector creates a tiny island of influence, leading to severe overfitting. Always tune γ with cross-validation.
>
> > 高 γ 不代表"更好的拟合"。它意味着每个支持向量只创建一个微小的影响孤岛，导致严重过拟合。必须用交叉验证来调优 γ。

**🔗 Related Concepts:**

> → concept: Support Vector Machine in concept-glossary
> → concept: Kernel Trick in concept-glossary
> → formula: Maximum Margin Classifier Optimization (the optimization this kernel plugs into)

**📚 Appears In:**

> - ML Week 2: Kernels and Non-linear SVM

---

### Soft Margin SVC Optimization (软间隔SVC优化)

**Tags:** `#optimization` `#svm` `#ml-week2`

**📌 One-line Definition:**

> The soft margin formulation allows some training points to violate the margin constraint by introducing slack variables ξᵢ and a penalty parameter C that controls the trade-off between margin width and misclassification.
>
> > 软间隔公式允许部分训练点违反间隔约束，通过引入松弛变量 ξᵢ 和惩罚参数 C 来控制间隔宽度与错误分类之间的权衡。

**📐 Formula:**

```
Minimize:    (1/2)||w||² + C × Σᵢ ξᵢ
Subject to:  yᵢ(w · xᵢ + b) ≥ 1 - ξᵢ,  ξᵢ ≥ 0

where:
  ||w||² = squared norm (controls margin width)
  C = penalty for violations (misclassification cost)
  ξᵢ = slack variable (how much point i violates the margin)
    ξᵢ = 0: point is correctly outside margin
    0 < ξᵢ < 1: inside margin but on correct side
    ξᵢ ≥ 1: misclassified (wrong side of boundary)
```

**💡 Intuition (直觉理解):**

> **The traffic fine analogy:** C is the fine amount for crossing the double line. Small C = ¥10 fine → everyone jaywalks (wide margin, many violations). Large C = ¥100,000 fine → nobody dares cross (narrow margin, near-zero violations, but the road bends wildly to accommodate everyone).
>
> > **交通罚款类比：** C 是越过双黄线的罚款金额。小 C = 10元罚款 → 大家随便越线（宽间隔，很多违规）。大 C = 10万元罚款 → 没人敢越线（窄间隔，几乎零违规，但道路为了迁就所有人而剧烈弯曲）。

**🔗 Related Concepts:**

> → formula: Maximum Margin Classifier Optimization (the hard-margin predecessor)
> → concept: Hard/Soft Margin in concept-glossary

**📚 Appears In:**

> - ML Week 2: Soft Margin and Support Vector Classifier
