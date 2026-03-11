# Note-Taking — Templates & Examples

## Page N

![Page N](path/page_NNN.png)

**Document Title — 文档标题**

**Section Heading — 章节标题**

- Original text from PDF — 中文翻译
- Another point from PDF — 另一个要点的中文翻译
  1. Sub-step from PDF — 子步骤翻译
  2. Another sub-step — 另一个子步骤

| Column — 列名 | Description — 描述                |
| ------------- | --------------------------------- |
| value1        | Meaning of value1 — value1 的含义 |
```

**示例（Lab PDF）：**

```markdown

## Page 1

![Page 1](CST8507_Lab_3_W26_pages/page_001.png)

**CST8507: Natural Language Processing — CST8507：自然语言处理**

**Lab 3: Word Embedding — 实验 3：词嵌入**

**Objective — 目标**

- Load pre-trained word vectors. — 加载预训练词向量。
- Evaluate embeddings using intrinsic metrics — 使用内在评价指标评估词嵌入
```


## Examples

### Example 1: Math/Algorithm Concept (Eigenvalues)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Reveal natural axes (揭示本质方向):**
>
> Eigenvectors reveal the "natural axes" of a transformation.
> A complex matrix transformation, viewed along eigenvector directions, becomes simple scaling.
>
> > 特征向量揭示了变换的"本质方向"。
> > 复杂的矩阵变换，沿特征向量方向看就变成了简单的缩放。
>
> **(2) Foundation for PCA (PCA的基础):**
>
> PCA uses eigenvectors for dimensionality reduction — finding directions of maximum variance.
> Without eigenvectors, there's no principled way to choose which dimensions to keep.
>
> > PCA 用特征向量降维 — 找到数据方差最大的方向。
> > 没有特征向量，就无法有原则地选择保留哪些维度。
>
> **💡 Intuition:**
> **(1) Revolving door analogy (旋转门类比):**
>
> Imagine pushing a revolving door. Most directions make it spin.
> But one direction only pushes it forward/backward without rotation —
> that direction is the "eigenvector", the displacement magnitude is the "eigenvalue".
>
> > 想象推旋转门。大部分方向推会让门转动。
> > 但有一个方向推只会让门前后移动不转 —
> > 那个方向就是"特征向量"，移动幅度就是"特征值"。
>
> **(2) Stretching rubber sheet (拉伸橡胶布):**
>
> A matrix is like stretching a rubber sheet. Most points move in complex ways.
> Eigenvectors are the directions that only get stretched (or compressed), never rotated.
>
> > 矩阵就像拉伸橡胶布。大部分点移动方式复杂。
> > 特征向量是只被拉伸（或压缩）而不被旋转的方向。
>
> **⚙️ How:**
> **(1) Derivation of characteristic equation (特征方程推导):**
>
> Why det(A-λI) = 0? Because Av = λv rearranges to (A-λI)v = 0.
> For non-zero v to exist, (A-λI) must be singular, meaning its determinant is 0.
>
> > 为什么 det(A-λI) = 0？因为 Av = λv 移项得 (A-λI)v = 0。
> > 要有非零解 v，(A-λI) 必须不可逆，即行列式为 0。
>
> **⚖️ Compare:**
> **(1) Eigendecomposition vs SVD:**
>
> Eigen requires square matrices; SVD works for any matrix.
> SVD is essentially eigendecomposition applied to AᵀA.
>
> > 特征分解要求方阵，SVD 对任意矩阵都有效。
> > SVD 本质是对 AᵀA 做特征分解。
>
> **⚠️ Pitfall:**
> **(1) Complex eigenvalues (复数特征值):**
>
> Not all matrices have real eigenvalues. Rotation matrices have complex eigenvalues —
> because no direction stays unchanged after rotation.
>
> > 不是所有矩阵都有实数特征值。旋转矩阵的特征值是复数 —
> > 因为旋转后没有方向保持不变。
>
> **(2) Confusing eigenvalue with eigenvector (混淆特征值和特征向量):**
>
> The eigenvalue λ is the scaling factor; the eigenvector v is the direction.
> Students often swap which is which in exam answers.
>
> > 特征值 λ 是缩放因子；特征向量 v 是方向。
> > 学生在考试中经常搞混哪个是哪个。
```

### Example 2: CV/ML Concept (Max Pooling)

```markdown
> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Reduce computational cost (降低计算成本):**
>
> After convolution, feature maps are too large — expensive to compute and store.
>
> > 卷积后特征图太大，计算和存储成本高。
>
> **(2) Add positional tolerance (增加位置容忍度):**
>
> We care about WHETHER a feature exists, not its exact pixel location.
> Pooling adds spatial invariance — a cat shifted by 2 pixels still gets detected.
>
> > 我们关心特征"有没有"，而不是"在哪个精确像素"。
> > 池化增加空间不变性 — 猫移动2像素仍然能被检测到。
>
> **💡 Intuition:**
> **(1) Map zoom analogy (地图缩放类比):**
>
> Like zooming out on a map — you lose street-level detail but still see city shapes.
>
> > 像缩小地图 — 丢失街道细节但保留城市轮廓。
>
> **(2) Strongest signal wins (最强信号胜出):**
>
> Max pooling keeps the strongest signal in each region, like picking the loudest voice in each room.
>
> > 最大池化保留每个区域中最强的信号，像从每个房间里挑出最大声的声音。
>
> **⚠️ Pitfall:**
> **(1) No learnable parameters (无可学习参数):**
>
> Pooling has NO learnable parameters — don't confuse it with convolution.
> Convolution learns filters; pooling just applies a fixed rule (max or average).
>
> > 池化没有可学习参数 — 不要跟卷积层混淆。
> > 卷积学习滤波器；池化只是应用固定规则（取最大值或平均值）。
>
> **(2) Information loss (信息损失):**
>
> Aggressive pooling (large kernel or stride) can destroy fine-grained spatial details needed for tasks like segmentation.
>
> > 激进的池化（大核或大步长）会破坏分割等任务需要的精细空间细节。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> Given input size 4×4 with 2×2 pooling and stride 2, output is 2×2.
> Formula: output = (input - pool_size) / stride + 1.
>
> > 给定 4×4 输入，2×2 池化，stride=2，输出为 2×2。
> > 公式：output = (input - pool_size) / stride + 1。
>
> **(2) 对比题 (Comparison):**
>
> "Max pooling vs average pooling — when to use which?" → Max for feature detection (keep strongest), average for smooth downsampling.
>
> > "最大池化 vs 平均池化 — 什么时候用哪个？" → 最大用于特征检测（保留最强），平均用于平滑下采样。
```

### Example 3: Math Formula (SSE in K-Means)

```markdown
- **SSE** = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² = Σᵢ Σₓ∈Cᵢ Σⱼ (xⱼ - mᵢⱼ)²
  - Cᵢ = the i-th cluster (a set of data points)
  - x = a data point in cluster Cᵢ (a d-dimensional vector)
  - mᵢ = centroid (mean) of cluster Cᵢ (a d-dimensional vector)
  - ‖x - mᵢ‖² = squared Euclidean distance between x and its centroid
  - Overall: total "spread" of all clusters — lower SSE = tighter clusters

> **📝 Notes:**
>
> **💡 Intuition:**
> **(1) Iron filings analogy (铁屑类比):**
>
> Like measuring how "scattered" iron filings are around magnets. Each filing's distance to its magnet is squared and summed. Tighter clusters = lower total.
>
> > 像测量铁屑围绕磁铁的"散布程度"。每个铁屑到磁铁的距离平方后求和。越紧凑 = 总和越小。
>
> **(2) Why squared? (为什么平方？):**
>
> Squaring penalizes outliers more heavily — a point 10 units away contributes 100, not 10. This makes SSE sensitive to distant points.
>
> > 平方会更重地惩罚离群点 — 距离10的点贡献100而不是10。这使SSE对远距离点敏感。
>
> **📐 Formula:**
> **(1) SSE breakdown (SSE逐段拆解):**
>
> Reading SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² piece by piece:
>
> - Σᵢ: iterate over all K clusters (i = 1, 2, ..., K)
> - Σₓ∈Cᵢ: for each data point x that belongs to cluster i
> - ‖x - mᵢ‖²: compute the squared Euclidean distance from x to its centroid mᵢ
> - Overall: sum up ALL these squared distances across ALL clusters = total "spread"
>
> > 逐段读 SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖²：
> >
> > - Σᵢ：遍历所有K个簇（i = 1, 2, ..., K）
> > - Σₓ∈Cᵢ：对属于簇i的每个数据点x
> > - ‖x - mᵢ‖²：算x到它的质心mᵢ的平方欧氏距离
> > - 整体：把所有簇中所有点的平方距离加起来 = 总"散布程度"
>
> **🔢 Example:**
> **(1) 1D SSE calculation (一维SSE计算):**
>
> **Problem:** We have 4 data points in 1D: {1, 3, 7, 9}. They've been assigned to 2 clusters: C₁={1,3} and C₂={7,9}.
> **Question:** What is the SSE?
> **Solution:**
>
> - Centroid m₁ = (1+3)/2 = 2, centroid m₂ = (7+9)/2 = 8
> - Cluster 1: (1-2)² + (3-2)² = 1 + 1 = 2
> - Cluster 2: (7-8)² + (9-8)² = 1 + 1 = 2
> - SSE = 2 + 2 = **4**
>
> > **题目：** 4个1维数据点：{1, 3, 7, 9}。分为2个簇：C₁={1,3}，C₂={7,9}。
> > **问：** SSE是多少？
> > **解：**
> >
> > - 质心 m₁ = (1+3)/2 = 2，m₂ = (7+9)/2 = 8
> > - 簇1：(1-2)² + (3-2)² = 1 + 1 = 2
> > - 簇2：(7-8)² + (9-8)² = 1 + 1 = 2
> > - SSE = 2 + 2 = **4**
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Given these clusters, compute SSE." Must show: formula → plug in each point → sum.
>
> > "给定这些簇，计算SSE。" 必须展示：公式 → 代入每个点 → 求和。
>
> **(2) 概念题 (Conceptual):**
>
> "What happens to SSE as K increases?" → SSE always decreases (more clusters = tighter fit), but eventually overfits.
>
> > "K增大时SSE会怎样？" → SSE总是下降（更多簇 = 更紧密），但最终过拟合。
```

### Example 4: Concept Comparison Section (Inter-Cluster Distance Methods)

```markdown
### 4.4 簇间距离定义 (Inter-Cluster Distance Methods)

![Page 29](week6_clustering_slides_pages/page_029.png)

**MIN (Single Linkage):** Same two-cluster diagram, but now a single yellow line connects the two closest points (one from each cluster) — this shortest cross-cluster distance is used. "MIN" is highlighted. Intuition: only the nearest pair matters.

**MIN（单链接）：** 同样的两个簇图，但现在一条黄色线连接了两个最近的点（每个簇各一个）— 使用最短跨簇距离。"MIN"被高亮。直觉：只有最近的那一对点有关系。

| Method  | Definition                          | Also Called       |
| ------- | ----------------------------------- | ----------------- |
| **MIN** | Min distance between any two points | Nearest neighbor  |
| **MAX** | Max distance between any two points | Farthest neighbor |

> **📝 Notes:**
>
> **📌 What:**
> **(1) Five linkage methods (五种链接方法):**
>
> Five methods to compute d(AB, C) after merging A and B: MIN, MAX, Average, Centroid, Ward.
>
> > 合并A和B后计算d(AB, C)的五种方法：MIN、MAX、Average、Centroid、Ward。
>
> **(2) Shape determinism (形状决定性):**
>
> The choice of linkage method completely determines the dendrogram shape — same data, different method → completely different tree.
>
> > 链接方法的选择完全决定树状图形状 — 同一数据、不同方法 → 完全不同的树。
>
> **💡 Intuition:**
> **(1) Country distance analogy (国家距离类比):**
>
> Measuring "distance" between two countries: MIN = nearest border crossing, MAX = farthest cities, Average = all city pairs, Centroid = capitals, Ward = population spread increase.
>
> > 测量两国"距离"：MIN = 最近边境，MAX = 最远城市，Average = 所有城市对，质心 = 首都，Ward = 人口扩散增量。
>
> **⚖️ Compare:**
> **(1) Method comparison table (方法对比表):**
>
> | Method | Tendency         | Weakness              |
> | ------ | ---------------- | --------------------- |
> | MIN    | Chain-like       | Chaining from noise   |
> | MAX    | Compact          | Breaks large clusters |
> | Ward   | Compact, min SSE | Biased to equal sizes |
>
> > | 方法 | 倾向          | 弱点         |
> > | ---- | ------------- | ------------ |
> > | MIN  | 链状          | 噪声导致链接 |
> > | MAX  | 紧凑          | 拆分大簇     |
> > | Ward | 紧凑、最小SSE | 偏向等大小   |
>
> **⚠️ Pitfall:**
> **(1) Chaining effect (链接效应):**
>
> MIN merges through noise bridges — a few stray points between distant clusters can chain them together.
>
> > MIN通过噪声桥合并 — 远距离簇之间的几个散点可以把它们串联起来。
>
> **(2) Dendrogram inversions (树状图反转):**
>
> Centroid method can produce later merges at lower distances — the dendrogram "goes backward", which is confusing.
>
> > 质心方法可能后续合并距离反而更低 — 树状图"倒退"，令人困惑。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Compute inter-cluster distance using MIN/MAX/Average." → MIN = smallest entry, MAX = largest, Average = sum ÷ count.
>
> > "用MIN/MAX/Average计算簇间距离。" → MIN = 最小值，MAX = 最大值，Average = 总和 ÷ 个数。
>
> **(2) 推理题 (Reasoning):**
>
> "Which method is most sensitive to outliers?" → MIN, because a single outlier point can bridge two clusters.
>
> > "哪种方法对离群值最敏感？" → MIN，因为一个离群点就能桥接两个簇。
```

