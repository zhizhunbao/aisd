# Week 6: 聚类分析 (Clustering)

> Source: `Week6Clustering.pdf`
> Total slides: 50
> Instructor: Dr. Abbas Akkasi | Winter 2026
> Adapted from materials by Pang-Ning Tan (Data Mining Course)

---

## 1. 聚类分析概述 (What is Cluster Analysis?)

![Page 3](week6_clustering_slides_pages/page_003.png)

- Given a set of objects, place them in **groups** such that objects in a group are **similar** to one another and **different** from objects in other groups
- Goal: **minimize intra-cluster distances**, **maximize inter-cluster distances**

![Page 4](week6_clustering_slides_pages/page_004.png)

**Applications:**

- **Understanding:** Group related documents for browsing, group genes/proteins with similar functionality, group stocks with similar price fluctuations
- **Summarization:** Reduce the size of large data sets (e.g., clustering precipitation data in Australia)

> **📝 Notes:**
>
> **📌 What:**
> Clustering = unsupervised learning that groups data points by similarity without predefined labels. Unlike classification (supervised), there are no "correct answers" to learn from.
>
>> 聚类 = 无监督学习，根据相似性将数据点分组，没有预定义标签。与分类（监督学习）不同，没有"正确答案"可学习。
>>
>
> **🎯 Why:**
> Why not just classify? Because in many real-world scenarios, we don't KNOW the categories in advance. Customer segmentation, gene discovery, anomaly detection — the whole point is to discover hidden structure.
>
>> 为什么不直接分类？因为在很多现实场景中，我们事先不知道类别。客户分群、基因发现、异常检测 — 目的就是发现隐藏结构。
>>
>
> **💡 Intuition:**
> Like sorting a pile of unlabeled photos into groups: you'd naturally group by "people", "landscapes", "food" etc. You don't need someone to tell you the categories — you discover them from the data itself.
>
>> 像把一堆无标签照片分组：你自然会按"人物"、"风景"、"美食"等分。你不需要别人告诉你类别 — 你从数据本身发现它们。
>>
>
> **⚖️ Compare:**
> Clustering (unsupervised) vs Classification (supervised): Clustering discovers groups; Classification assigns to known groups. Clustering has no ground truth to evaluate against directly.
>
>> 聚类（无监督）vs 分类（监督）：聚类发现分组；分类分配到已知分组。聚类没有可直接评估的真实标签。
>>

---

## 2. 聚类类型 (Types of Clusterings)

### 2.1 划分聚类 vs 层次聚类 (Partitional vs Hierarchical)

![Page 5](week6_clustering_slides_pages/page_005.png)

- How many clusters? The notion of a cluster can be **ambiguous** — same data can have 2, 4, or 6 clusters depending on perspective

![Page 7](week6_clustering_slides_pages/page_007.png)

- **Partitional Clustering:** Divides data into **non-overlapping** subsets (clusters)

![Page 8](week6_clustering_slides_pages/page_008.png)

- **Hierarchical Clustering:** Creates **nested clusters** organized as a hierarchical tree (dendrogram)
- Traditional vs Non-traditional dendrograms

> **📝 Notes:**
>
> **⚖️ Compare:**
> Partitional vs Hierarchical: Partitional = one flat division (each point belongs to exactly one cluster). Hierarchical = tree structure showing all possible numbers of clusters at once. Partitional requires you to specify K upfront; Hierarchical lets you choose K after by cutting the dendrogram.
>
>> 划分 vs 层次：划分 = 一次平面划分（每个点恰好属于一个簇）。层次 = 树结构同时展示所有可能的聚类数。划分需要预先指定K；层次允许事后通过切割树状图选择K。
>>
>
> **🎯 Why:**
> Why two types? Because different problems have different needs. Customer segmentation → partitional (just need groups). Biological taxonomy → hierarchical (species → genus → family relationships matter).
>
>> 为什么有两种？因为不同问题有不同需求。客户分群→划分式（只需分组）。生物分类→层次式（种→属→科的关系很重要）。
>>
>
> **📝 Exam:**
> "What is the difference between partitional and hierarchical clustering?" Partitional = flat, non-overlapping groups. Hierarchical = nested, tree-structured clusters.
>
>> "划分聚类和层次聚类有什么区别？" 划分 = 平面的、不重叠的分组。层次 = 嵌套的、树形结构的聚类。
>>

### 2.2 簇的类型 (Types of Clusters)

![Page 10](week6_clustering_slides_pages/page_010.png)

**Well-separated:** Every point closer to its cluster than to any other cluster

![Page 11](week6_clustering_slides_pages/page_011.png)

**Prototype-based:** Each point closer to the centroid (mean/medoid) of its cluster than to any other centroid

![Page 12](week6_clustering_slides_pages/page_012.png)

**Contiguity-based (Nearest neighbor):** Each point closer to at least one point in its cluster than to any point outside

![Page 13](week6_clustering_slides_pages/page_013.png)

**Density-based:** Dense regions separated by low-density regions. Used for irregular or intertwined clusters with noise/outliers.

> **📝 Notes:**
>
> **🎯 Why:**
> Why does the type of cluster matter? Because your choice of clustering ALGORITHM depends on what type of clusters you expect. K-Means assumes prototype-based (spherical) clusters. DBSCAN assumes density-based clusters. Using the wrong algorithm for your data = garbage results.
>
>> 为什么簇的类型重要？因为你选择的聚类算法取决于你期望的簇类型。K-Means假设基于原型（球形）的簇。DBSCAN假设基于密度的簇。用错算法 = 垃圾结果。
>>
>
> **💡 Intuition:**
> Prototype-based = "everything gathers around a center" (like planets around stars). Density-based = "things clump together regardless of shape" (like clouds — they have no center but have clear boundaries).
>
>> 基于原型 = "一切围绕中心聚集"（像行星围绕恒星）。基于密度 = "事物聚在一起不管形状"（像云 — 没有中心但有清晰边界）。
>>
>
> **⚠️ Pitfall:**
> K-Means CANNOT find non-convex clusters (e.g., crescent shapes). If your data has irregular cluster shapes, use DBSCAN instead.
>
>> K-Means**无法**找到非凸形簇（如月牙形）。如果数据有不规则形状的簇，改用DBSCAN。
>>

---

## 3. K-Means 聚类 (K-Means Clustering)

### 3.1 基本算法 (Basic Algorithm)

![Page 15](week6_clustering_slides_pages/page_015.png)

- **Partitional** clustering approach
- Number of clusters **K must be specified**
- Each cluster is associated with a **centroid** (center point)
- Each point is assigned to the cluster with the **closest centroid**

**Algorithm:**

1. Choose K initial centroids (often randomly)
2. **Repeat:**
   - Assign each point to the nearest centroid
   - Recompute cluster centroids (mean of all points in cluster)
3. **Until** centroids stop changing (or few points change clusters)

![Page 16](week6_clustering_slides_pages/page_016.png)

K-Means iteration example (iteration 1–6): initial random centroids gradually move to the true cluster centers.

![Page 17](week6_clustering_slides_pages/page_017.png)

Continued iteration — centroids converge to stable positions.

> **📝 Notes:**
>
> **📌 What:**
> K-Means: First YOU decide how many clusters you want (K=3 means 3 groups). Then the algorithm randomly picks K data points as initial centroids → assigns all points to their nearest centroid → recomputes centroids → repeats until stable. K is not random — it's your choice; only the STARTING positions are random.
>
>> K-Means：首先你决定想要几个簇（K=3表示分3组）。然后算法从数据中随机选K个点作为初始质心→将所有点分配到最近的质心→重新计算质心→重复直到稳定。K不是随机的 — 是你的选择；只有起始位置是随机的。
>>
>
> **💡 Intuition:**
> Like placing K magnets on a table of scattered iron filings. Each filing goes to the nearest magnet. Then move each magnet to the center of its filings. Repeat. Eventually magnets settle into stable positions.
>
>> 像在散布铁屑的桌上放K块磁铁。每个铁屑被最近的磁铁吸引。然后把每块磁铁移到它吸引的铁屑的中心。重复。最终磁铁稳定在固定位置。
>>
>
> **⚠️ Pitfall:**
> Random initial centroids → different runs give different results! Bad initialization can converge to suboptimal clusters. Solution: K-Means++ for smarter initialization, or run multiple times and pick the best (lowest SSE).
>
>> 随机初始质心→不同运行给出不同结果！糟糕的初始化可能收敛到次优聚类。解决方案：K-Means++智能初始化，或多次运行选最佳（最低SSE）。
>>
>
> **📝 Exam:**
> "Describe the K-Means algorithm." Must include: (1) specify K, (2) initialize centroids, (3) assign points, (4) recompute centroids, (5) repeat until convergence.
>
>> "描述K-Means算法。" 必须包含：(1)指定K，(2)初始化质心，(3)分配点，(4)重新计算质心，(5)重复直到收敛。
>>

### 3.2 细节与复杂度 (Details & Complexity)

![Page 18](week6_clustering_slides_pages/page_018.png)

- **Convergence:** K-Means will converge for common distance measures
- Most convergence happens in the **first few iterations**
- **Complexity:** O(n × K × I × d)
  - n = number of points
  - K = number of clusters
  - I = number of iterations
  - d = number of attributes
- Initial centroids are often chosen **randomly** → clusters can vary from run to run
- The centroid is typically the **mean** of points in the cluster

> **📝 Notes:**
>
> **⚙️ How:**
> Complexity O(n × K × I × d) — linear in all factors! This is why K-Means is so fast. Typical runs converge in 10-20 iterations, and most of the "movement" happens in the first 3-5 iterations. So in practice it's nearly O(n × K × d).
>
>> 复杂度 O(n × K × I × d) — 对所有因素都是线性的！这就是K-Means快的原因。典型运行在10-20次迭代内收敛，大部分"移动"在前3-5次迭代就发生了。所以实际上接近 O(n × K × d)。
>>
>
> **⚠️ Pitfall:**
> "Converge" only means centroids stop moving — NOT that you found the best answer. K-Means ALWAYS converges, but may converge to a bad local minimum if initialization was unlucky. That's why `n_init=10` (run 10 times, pick best) is the default in sklearn.
>
>> "收敛"只意味着质心停止移动 — 不代表找到了最佳答案。K-Means总是会收敛，但如果初始化不幸运可能收敛到差的局部最小值。这就是为什么sklearn默认 `n_init=10`（运行10次，选最佳）。
>>

### 3.3 目标函数: SSE (Objective Function: Sum of Squared Error)

![Page 19](week6_clustering_slides_pages/page_019.png)

- **SSE** = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖²  = Σᵢ Σₓ∈Cᵢ Σⱼ (xⱼ - mᵢⱼ)²
  - x = data point in cluster Cᵢ
  - mᵢ = centroid (mean) of cluster Cᵢ
  - ‖x - mᵢ‖² = squared Euclidean distance = sum of squared differences across all d dimensions
- SSE improves in each iteration until it reaches a **local or global minimum**
- Goal: find the clustering that minimizes SSE

> **📝 Notes:**
>
> **🎯 Why:**
> Why SSE? It quantifies "how tight are the clusters?" Lower SSE = points closer to their centroids = better clustering. K-Means is essentially an optimization algorithm that minimizes SSE.
>
>> 为什么用SSE？它量化"聚类有多紧凑"。SSE越低 = 点离质心越近 = 聚类越好。K-Means本质上是最小化SSE的优化算法。
>>
>
> **💡 Intuition:**
> Like measuring how "scattered" iron filings are around magnets. Each filing's distance to its magnet is squared and summed. Tighter clusters = lower total.
>
>> 像测量铁屑围绕磁铁的"散布程度"。每个铁屑到磁铁的距离平方后求和。越紧凑 = 总和越小。
>>
>
> **📐 Formula:**
> Reading SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖² piece by piece:
>
> - Σᵢ: iterate over all K clusters (i = 1, 2, ..., K)
> - Σₓ∈Cᵢ: for each data point x that belongs to cluster i
> - ‖x - mᵢ‖²: compute the squared Euclidean distance from point x to centroid mᵢ
> - Sum it all up → one number measuring total "spread" of the clustering
>
>> 逐段读 SSE = Σᵢ Σₓ∈Cᵢ ‖x - mᵢ‖²：
>>
>> - Σᵢ：遍历所有K个簇（i = 1, 2, ..., K）
>> - Σₓ∈Cᵢ：对属于簇i的每个数据点x
>> - ‖x - mᵢ‖²：算x到质心mᵢ的平方欧氏距离
>> - 全部加起来 → 一个数字衡量聚类的总"散布程度"
>>
>
> **🔢 Example:**
> **Problem:** We have 4 data points in 1D: {1, 3, 7, 9}. They've been assigned to 2 clusters: C₁={1,3} and C₂={7,9}.
> **Question:** What is the SSE?
> **Solution:**
>
> - Centroid m₁ = (1+3)/2 = 2, centroid m₂ = (7+9)/2 = 8
> - Cluster 1: (1-2)² + (3-2)² = 1 + 1 = 2
> - Cluster 2: (7-8)² + (9-8)² = 1 + 1 = 2
> - SSE = 2 + 2 = **4**
>
>> **题目：** 4个1维数据点：{1, 3, 7, 9}。分为2个簇：C₁={1,3}，C₂={7,9}。
>> **问：** SSE是多少？
>> **解：**
>>
>> - 质心 m₁ = (1+3)/2 = 2，m₂ = (7+9)/2 = 8
>> - 簇1：(1-2)² + (3-2)² = 1 + 1 = 2
>> - 簇2：(7-8)² + (9-8)² = 1 + 1 = 2
>> - SSE = 2 + 2 = **4**
>>
>
> **📝 Exam:**
> "What is the objective function of K-Means?" Must write SSE formula + explain each symbol. "Does K-Means guarantee the global minimum?" No, only local minimum.
>
>> "K-Means的目标函数是什么？" 必须写SSE公式 + 解释每个符号。"K-Means能保证全局最优吗？" 不能，只保证局部最优。
>>

---

## 4. 层次聚类 (Hierarchical Clustering)

### 4.1 概述 (Overview)

![Page 20](week6_clustering_slides_pages/page_020.png)

- Produces **nested clusters** organized as a hierarchical tree
- Visualized as a **dendrogram** — a tree diagram recording sequences of merges or splits
- **No need to specify K** in advance — choose K by cutting the dendrogram at the desired level

![Page 21](week6_clustering_slides_pages/page_021.png)

**Strengths:**

- Do not have to assume any particular number of clusters — obtain any K by cutting dendrogram
- May correspond to meaningful taxonomies (e.g., biological sciences, phylogeny)

> **📝 Notes:**
>
> **🎯 Why:**
> K-Means forces you to pick K upfront — but what if you don't know how many clusters exist? Hierarchical clustering builds a full tree of all possible clusterings (K=1 to K=N). You can decide K AFTER seeing the structure, by cutting the dendrogram where the gaps are largest.
>
>> K-Means强制你提前选K — 但如果不知道有几个簇呢？层次聚类构建一棵包含所有可能聚类的完整树（K=1到K=N）。你可以在看到结构后再决定K，在间距最大的地方切割树状图。
>>
>
> **💡 Intuition:**
> Like organizing a bookshelf: first group similar books into small piles, then merge similar piles into sections, sections into shelves. The dendrogram is a record of this merging process — you can "cut" at any level to get the grouping you want.
>
>> 像整理书架：先把相似的书分成小堆，再把相似的小堆合成区域，区域合成书架。树状图是这个合并过程的记录 — 你可以在任意层"切割"得到想要的分组。
>>
>
> **⚖️ Compare:**
> K-Means vs Hierarchical: K-Means is fast (O(nKI)) but needs K upfront and gives flat clusters. Hierarchical is slower (O(n²) or O(n³)) but gives a full hierarchy, no K needed, and shows relationships between clusters.
>
>> K-Means vs 层次聚类：K-Means快（O(nKI)）但需要提前指定K且只给平面簇。层次聚类慢（O(n²)或O(n³)）但给出完整层级关系，不需要K，且展示簇之间的关系。
>>
>
> **⚠️ Pitfall:**
> Hierarchical clustering is NOT scalable to large datasets — O(n²) memory for the distance matrix. For 100K points, that's 10 billion entries. Use K-Means or DBSCAN for large data, hierarchical for small data where you want to explore structure.
>
>> 层次聚类不适合大数据集 — 距离矩阵需要O(n²)内存。10万个点就是100亿个条目。大数据用K-Means或DBSCAN，层次聚类适合小数据集且你想探索结构时。
>>

### 4.2 凝聚 vs 分裂 (Agglomerative vs Divisive)

![Page 22](week6_clustering_slides_pages/page_022.png)

- **Agglomerative (Bottom-up):**
  - Start with each point as an individual cluster
  - At each step, merge the **closest pair** of clusters
  - Continue until only one cluster (or K clusters) remains
- **Divisive (Top-down):**
  - Start with one all-inclusive cluster
  - At each step, **split** a cluster
  - Continue until each cluster contains an individual point (or K clusters)
- Traditional hierarchical algorithms use a **similarity or distance matrix**

> **📝 Notes:**
>
> **⚖️ Compare:**
> Agglomerative vs Divisive: Agglomerative = bottom-up (merge), more common, O(n²) space. Divisive = top-down (split), less common, computationally harder. In practice, agglomerative is used far more often.
>
>> 凝聚 vs 分裂：凝聚 = 自下而上（合并），更常见，O(n²)空间。分裂 = 自上而下（分裂），较少见，计算更难。实践中，凝聚式使用频率远高于分裂式。
>>
>
> **💡 Intuition:**
> Agglomerative = building a family tree from individuals. Start with each person, then find the most similar pair and merge them into a family, then merge families into clans, clans into tribes...
>
>> 凝聚式 = 从个人构建家族树。从每个人开始，找到最相似的一对合并成家庭，然后家庭合并成宗族，宗族合并成部落……
>>
>
> **📝 Exam:**
> "Explain agglomerative hierarchical clustering." Start with N clusters → compute distance matrix → merge closest pair → update matrix → repeat until 1 cluster.
>
>> "解释凝聚层次聚类。" 从N个簇开始→计算距离矩阵→合并最近的一对→更新矩阵→重复直到剩1个簇。
>>

### 4.3 凝聚算法 (Agglomerative Algorithm)

![Page 23](week6_clustering_slides_pages/page_023.png)

**Basic algorithm / 基本算法：**

1. Compute the **distance matrix** — 计算距离矩阵
2. Let each data point be a cluster — 每个数据点自成一个簇
3. **Repeat:** Merge the two closest clusters → Update the distance matrix — **重复：** 合并最近的两个簇 → 更新距离矩阵
4. **Until** only a single cluster remains — **直到** 只剩一个簇

**Key operation:** how to define the distance between two clusters — different definitions give different algorithms

**关键操作：** 如何定义两个簇之间的距离 — 不同的定义产生不同的算法变体（MIN / MAX / Average / Ward）

![Page 24](week6_clustering_slides_pages/page_024.png)

**Steps 1 & 2:** Start with individual points and a proximity matrix. Left: scatter plot where each point = one cluster. Right: N×N distance matrix (p1–p5…). Bottom: dendrogram with each point as a leaf node — no merges yet.

**步骤 1 和 2：** 从单个数据点开始，建立距离矩阵。左侧：散点图，每个点 = 一个簇。右侧：N×N 距离矩阵（p1–p5…）。底部：树状图初始状态，每个点各自为叶节点，尚未发生任何合并。

![Page 25](week6_clustering_slides_pages/page_025.png)

**Intermediate situation:** After some merging steps, individual points have formed 5 clusters (C1–C5, shown as "cloud" shapes). Distance matrix has shrunk to 5×5. The dendrogram records all previous merges (some points already connected).

**中间状态：** 经过若干次合并后，原始数据点已形成5个簇（C1–C5，用"云朵"形状表示）。距离矩阵缩小为 5×5。树状图已记录了之前的所有合并（部分点已经通过连线合并）。

![Page 26](week6_clustering_slides_pages/page_026.png)

**Merge step (Step 4):** Find minimum in 5×5 distance matrix → C2 and C5 are closest (yellow-highlighted rows/columns). Dotted oval on the left circles C2 and C5, indicating they will merge. Dendrogram will add a new connecting branch.

**合并步骤（第4步）：** 在 5×5 距离矩阵中找最小值 → C2 和 C5 距离最近（黄色高亮的行/列）。左侧虚线椭圆将 C2 和 C5 圈在一起，表示即将合并。树状图将画一条新的连接分支。

![Page 27](week6_clustering_slides_pages/page_027.png)

**After merge (Step 5):** C2 and C5 merged into "C2 ∪ C5". Matrix shrinks to 4×4, but new cluster's distances to C1, C3, C4 are marked **"?"** — must be recomputed. How to compute "?" depends on the **linkage method**: MIN (smallest), MAX (largest), Average (mean), Ward (SSE increase).

**合并后（第5步）：** C2 和 C5 合并为 "C2 ∪ C5"。矩阵缩小为 4×4，但新簇到 C1、C3、C4 的距离标为 **"?"** — 需要重新计算。"?" 怎么算取决于**链接方法**：MIN（取最小）、MAX（取最大）、Average（取平均）、Ward（取 SSE 增量）。

> **📝 Notes:**
>
> **📌 What:**
> Agglomerative clustering = a greedy, bottom-up algorithm. Start with N singleton clusters. At each step: (1) find the two closest clusters in the distance matrix, (2) merge them into one, (3) update the distance matrix (shrink by 1 row/col). Repeat N−1 times until everything is one cluster. The result is a dendrogram recording every merge.
>
>> 凝聚聚类 = 一种贪心的自下而上算法。从N个单点簇开始。每一步：(1) 从距离矩阵中找到最近的两个簇，(2) 合并它们，(3) 更新距离矩阵（减少1行/列）。重复N−1次直到所有点合为一个簇。结果是一棵记录每次合并的树状图。
>>
>
> **🎯 Why:**
> The key design decision is how you **update the distance matrix** after a merge — this is where Single/Complete/Average/Ward linkage differ. The algorithm skeleton is always the same; only the distance-update rule changes. This one rule completely determines the shape of your dendrogram.
>
>> 关键设计决策是合并后如何**更新距离矩阵** — 这正是单链接/完全链接/平均链接/Ward链接不同的地方。算法骨架始终一样；只有距离更新规则不同。这一个规则完全决定了树状图的形状。
>>
>
> **⚙️ How:**
> Complexity: O(n³) time in the naive implementation (n−1 merge steps × O(n²) to scan the matrix each time). With optimized priority queues it can be reduced to O(n² log n). Space: O(n²) for the distance matrix. This makes it impractical for n > ~10,000.
>
>> 复杂度：朴素实现O(n³)时间（n−1次合并步骤 × 每次O(n²)扫描矩阵）。用优化的优先队列可以降到O(n² log n)。空间：O(n²)用于距离矩阵。这使得n > ~10,000时不实用。
>>
>
> **💡 Intuition:**
> Like a tournament bracket in reverse: start with all players (data points) as individuals. Each round, the two most similar players are "merged" into a team. Teams keep merging until the entire tournament is one mega-team. The bracket diagram IS the dendrogram.
>
>> 像反向的淘汰赛对阵表：从所有选手（数据点）作为个人开始。每轮将最相似的两个选手"合并"成一队。队伍不断合并直到整个比赛成为一个超级队伍。对阵表图就是树状图。
>>
>
> **🔢 Example:**
> **Problem:** 5 points in 1D: A=1, B=2, C=6, D=7, E=10. Use Single Linkage (MIN).
> **Solution:**
>
> - Initial distances: d(A,B)=1, d(A,C)=5, d(B,C)=4, d(C,D)=1, d(D,E)=3, ...
> - Step 1: Merge {A,B} (distance=1) and merge {C,D} (distance=1, tie-break)
> - Step 2: d({A,B},{C,D})=MIN(d(B,C))=4, d({C,D},E)=MIN(d(D,E))=3 → merge {C,D,E}
> - Step 3: d({A,B},{C,D,E})=MIN(d(B,C))=4 → merge all → done
> - Dendrogram heights: 1, 1, 3, 4
>
>> **题目：** 1维5个点：A=1, B=2, C=6, D=7, E=10。使用单链接(MIN)。
>> **解：**
>>
>> - 初始距离：d(A,B)=1, d(A,C)=5, d(B,C)=4, d(C,D)=1, d(D,E)=3, ...
>> - 第1步：合并{A,B}（距离=1），合并{C,D}（距离=1，打破平局）
>> - 第2步：d({A,B},{C,D})=MIN(d(B,C))=4, d({C,D},E)=MIN(d(D,E))=3 → 合并{C,D,E}
>> - 第3步：d({A,B},{C,D,E})=MIN(d(B,C))=4 → 全部合并 → 完成
>> - 树状图高度：1, 1, 3, 4
>>
>
> **⚠️ Pitfall:**
> Agglomerative merges are **irreversible** — once two clusters are merged, they can never be separated. A bad early merge (caused by noise or outliers) will propagate all the way up the dendrogram. This is the fundamental weakness of greedy hierarchical methods.
>
>> 凝聚式合并是**不可逆的** — 一旦两个簇合并就无法再分开。由噪声或异常值导致的错误早期合并会一路传播到树状图顶部。这是贪心层次方法的根本弱点。
>>
>
> **📝 Exam:**
> "Walk through the agglomerative algorithm for a given distance matrix." Must show: (1) initial matrix, (2) find min distance, (3) merge, (4) recompute distances using specified linkage, (5) repeat. Also: "What is the time complexity?" O(n³) naive, O(n² log n) optimized.
>
>> "给定距离矩阵，走一遍凝聚算法。" 必须展示：(1) 初始矩阵，(2) 找最小距离，(3) 合并，(4) 用指定链接法重算距离，(5) 重复。另外："时间复杂度是什么？" 朴素O(n³)，优化O(n² log n)。
>>

### 4.4 簇间距离定义 (Inter-Cluster Distance Methods)

![Page 28](week6_clustering_slides_pages/page_028.png)

**Overview slide:** Title "How to Define Inter-Cluster Distance". Left: two "cloud" clusters with a double-arrow labeled "Similarity?" between them. Right: distance matrix (p1–p5…). Bottom: lists all 5 methods — MIN, MAX, Group Average, Distance Between Centroids, and Ward's Method (objective-function-driven, uses squared error). This slide frames the central question: after merging, how do you compute the new cluster's distances?

**概览幻灯片：** 标题"如何定义簇间距离"。左侧：两个"云朵"簇之间标注"Similarity?"的双向箭头。右侧：距离矩阵（p1–p5…）。底部：列出全部5种方法 — MIN、MAX、Group Average、质心距离和Ward方法（基于目标函数，使用平方误差）。本页提出核心问题：合并后，如何计算新簇的距离？

| Method                           | Definition                                                         | Also Called       |
| -------------------------------- | ------------------------------------------------------------------ | ----------------- |
| **MIN (Single Linkage)**   | Minimum distance between any two points in different clusters      | Nearest neighbor  |
| **MAX (Complete Linkage)** | Maximum distance between any two points in different clusters      | Farthest neighbor |
| **Group Average**          | Average distance between all pairs of points in different clusters | Average linkage   |
| **Centroid Distance**      | Distance between the centroids of two clusters                     | —                |
| **Ward's Method**          | Increase in total SSE after merging two clusters                   | Minimum variance  |

![Page 29](week6_clustering_slides_pages/page_029.png)

**MIN (Single Linkage):** Same two-cluster diagram, but now a single yellow line connects the two closest points (one from each cluster) — this shortest cross-cluster distance is used. "MIN" is highlighted in the method list. Intuition: only the nearest pair matters.

**MIN（单链接）：** 同样的两个簇图，但现在一条黄色线连接了两个最近的点（每个簇各一个）— 使用这个最短跨簇距离。方法列表中"MIN"被高亮。直觉理解：只有最近的那一对点有关系。

![Page 30](week6_clustering_slides_pages/page_030.png)

**MAX (Complete Linkage):** Same diagram, but the yellow line now connects the two farthest points (one from each cluster) — this longest cross-cluster distance is used. "MAX" is highlighted. Intuition: the worst-case pair determines the distance.

**MAX（完全链接）：** 同样的图，但黄色线现在连接两个最远的点（每个簇各一个）— 使用这个最长跨簇距离。"MAX"被高亮。直觉理解：最坏情况的那对点决定了距离。

![Page 31](week6_clustering_slides_pages/page_031.png)

**Group Average:** Same diagram, but now many yellow lines connect every pair of points across the two clusters — all pairwise distances are drawn. The cluster distance = average of all these pairwise distances. "Group Average" is highlighted. Intuition: considers ALL cross-cluster point pairs, not just extremes.

**组平均：** 同样的图，但现在多条黄色线连接了两个簇之间的所有点对 — 绘制了全部成对距离。簇间距离 = 所有这些成对距离的平均值。"Group Average"被高亮。直觉理解：考虑所有跨簇点对，不只是极端的。

![Page 32](week6_clustering_slides_pages/page_032.png)

**Distance Between Centroids:** Same diagram, but now each cluster has a centroid marked with "×" (red cross). A single yellow line connects the two centroids — their distance is used. "Distance Between Centroids" is highlighted. Intuition: represents each cluster by its center of mass.

**质心距离：** 同样的图，但现在每个簇用"×"（红色叉号）标注了质心。一条黄色线连接两个质心 — 用它们之间的距离。"Distance Between Centroids"被高亮。直觉理解：用质心（重心）代表整个簇。

![Page 33](week6_clustering_slides_pages/page_033.png)

**Group Average full example:** Left: 6 data points (labeled 1–6) shown with nested ellipses representing the hierarchical clustering result — innermost clusters {3,6} and {1,4} merge first, then larger clusters form (numbered 1–5 as merge order in red). Right: corresponding dendrogram with y-axis showing merge distance (0 to 0.25); merge order matches the nested structure.

**组平均完整示例：** 左侧：6个数据点（编号1–6），用嵌套椭圆表示层次聚类结果 — 最内层的簇{3,6}和{1,4}先合并，然后逐步形成更大的簇（红色数字1–5表示合并顺序）。右侧：对应的树状图，y轴显示合并距离（0到0.25）；合并顺序与嵌套结构一致。

![Page 34](week6_clustering_slides_pages/page_034.png)

**Comparison of linkage methods on the same data (6 points):** Three nested-cluster diagrams side by side — MIN, MAX, and Group Average. Each shows the same 6 points but with different merge orders (red numbers) and different final cluster shapes. MIN: produces elongated, chain-like clusters (points merge in sequence). MAX: produces compact, balanced clusters (distant points forced together later). Group Average: compromise between the two.

**同一数据（6个点）上不同链接方法的比较：** 三组嵌套簇图并排展示 — MIN、MAX 和 Group Average。每组使用相同的6个点，但合并顺序（红色数字）和最终簇形状不同。MIN：产生细长的链状簇（点按序号链式合并）。MAX：产生紧凑、均衡的簇（远距离的点被推迟合并）。Group Average：两者的折中。

> **📝 Notes:**
>
> **📌 What:**
> Five methods to compute the distance between two clusters in agglomerative clustering. They all answer the same question: "After merging clusters A and B into AB, what is d(AB, C)?" — but each answers it differently. The method you choose completely determines your dendrogram shape.
>
>> 凝聚聚类中计算两个簇间距离的五种方法。它们都回答同一个问题："把簇A和B合并成AB后，d(AB, C) 是多少？"— 但答案各不相同。你选择的方法完全决定了树状图的形状。
>>
>
> **🎯 Why:**
> Why so many methods? Because different data distributions need different assumptions. If clusters can be elongated (e.g., gene expression pathways), MIN works. If you want tight, globular clusters (e.g., customer segments), MAX or Ward is better. There's no universal best — the choice is a modeling decision, not a technical detail.
>
>> 为什么有这么多方法？因为不同的数据分布需要不同的假设。如果簇可以是细长的（如基因表达通路），MIN合适。如果你想要紧凑的球形簇（如客户分群），MAX 或 Ward 更好。没有普遍最优 — 选择是建模决策，不是技术细节。
>>
>
> **💡 Intuition:**
> Think of measuring the "distance" between two countries. MIN = the shortest border crossing (nearest points). MAX = the distance from the farthest city in country A to the farthest city in country B. Group Average = average distance between all pairs of cities. Centroid = distance between the two capitals. Ward = "if we merged these two countries, how much would the total population spread increase?"
>
>> 想象测量两个国家之间的"距离"。MIN = 最近的边境口岸（最近点）。MAX = 国家A最远城市到国家B最远城市的距离。Group Average = 所有城市对的平均距离。质心 = 两国首都之间的距离。Ward = "如果合并这两个国家，总人口散布程度会增加多少？"
>>
>
> **⚖️ Compare:**
> | Method | Tendency | Strength | Weakness |
> |---|---|---|---|
> | MIN | Chain-like, elongated | Handles non-globular shapes | Chaining effect from noise |
> | MAX | Compact, globular | Robust to noise | May break natural large clusters |
> | Average | Balanced compromise | Less extreme than MIN/MAX | No clear geometric meaning |
> | Centroid | Based on center of mass | Simple, intuitive | Can produce inversions in dendrogram |
> | Ward | Compact, minimizes SSE | Often the best default | Biased toward equal-sized clusters |
>
>> | 方法 | 倾向 | 优势 | 弱点 |
>> |---|---|---|---|
>> | MIN | 链状、细长 | 能处理非球形 | 噪声导致链接效应 |
>> | MAX | 紧凑、球形 | 抗噪声 | 可能拆分自然的大簇 |
>> | Average | 均衡折中 | 没有MIN/MAX那么极端 | 无几何直觉 |
>> | 质心 | 基于重心 | 简单直观 | 树状图可能出现反转 |
>> | Ward | 紧凑、最小化SSE | 通常是最好的默认选择 | 偏向大小相等的簇 |
>>
>
> **⚠️ Pitfall:**
> Single Linkage (MIN) is notorious for the **chaining effect** — one noisy point between two well-separated clusters can act as a "bridge" and cause them to merge incorrectly. Also, Centroid method can produce **dendrogram inversions** (a later merge happens at a lower distance than an earlier one), which makes the dendrogram hard to interpret.
>
>> 单链接（MIN）以**链接效应**闻名 — 两个本该分开的簇之间只要有一个噪声点当"桥梁"，就会导致错误合并。另外，质心方法可能产生**树状图反转**（后面的合并距离反而比前面的低），导致树状图难以解释。
>>
>
> **📝 Exam:**
> "Given a distance matrix, compute the inter-cluster distance using MIN / MAX / Average." Must know: MIN = smallest entry, MAX = largest entry, Average = sum of all entries ÷ count. Also: "Which method is prone to chaining?" → MIN. "Which method tends to produce compact clusters?" → MAX or Ward.
>
>> "给定距离矩阵，用 MIN / MAX / Average 计算簇间距离。" 必须知道：MIN = 最小值，MAX = 最大值，Average = 所有值之和 ÷ 个数。另外："哪种方法容易产生链接效应？" → MIN。"哪种方法倾向产生紧凑簇？" → MAX 或 Ward。
>>

---

## 5. DBSCAN (基于密度的聚类)

### 5.1 核心概念 (Core Concepts)

![Page 35](week6_clustering_slides_pages/page_035.png)

**Density-Based Clustering introduction:** Title "Density Based Clustering". Text: "Clusters are **regions of high density** separated from one another by **regions on low density**." Below: a scatter plot of blue dots forming block-letter shapes (resembling characters) — dense regions form the letter strokes, sparse/empty regions form the gaps. This motivates density-based methods: the "shape" of each character cluster is highly non-spherical, so K-Means would fail here.

**基于密度的聚类引入：** 标题"Density Based Clustering"。文字："簇是被**低密度区域**分隔的**高密度区域**。"下方：蓝色散点图呈方块字母形状 — 密集区域构成字母笔画，稀疏/空白区域构成间隔。这引出了基于密度方法的动机：每个字符簇的"形状"高度非球形，K-Means在这里会失败。

![Page 36](week6_clustering_slides_pages/page_036.png)

**DBSCAN definition slide:** Title "DBSCAN - Density-based spatial clustering of applications with noise". Defines: Density = number of points within radius ε. Three point types: **core point** (orange text, has ≥ MinPts neighbors within ε, "at least" is highlighted in yellow — note it counts the point itself), **border point** (orange text, not core but within ε of a core point), **noise point** (orange text, neither core nor border). Key detail on slide: "Counts the point itself" — this is a common exam trap.

**DBSCAN 定义幻灯片：** 标题"DBSCAN - 基于密度的带噪声空间聚类"。定义：密度 = 半径ε内的点数。三种点类型：**核心点**（橙色文字，ε内有≥MinPts个邻居，"at least"被黄色高亮 — 注意会把自身也算在内），**边界点**（橙色文字，不是核心点但在某个核心点的ε内），**噪声点**（橙色文字，既不是核心点也不是边界点）。幻灯片关键细节："Counts the point itself" — 这是常见的考试陷阱。

- **Density** = number of points within a specified radius (ε, epsilon) — 密度 = 指定半径ε内的点数
- **Two parameters:** ε (radius) and MinPts (minimum points) — 两个参数：ε（半径）和 MinPts（最小点数）
- **Core point:** has at least MinPts points within ε (**including itself**) — interior of cluster — 核心点：ε内至少有MinPts个点（**包括自身**）— 簇的内部
- **Border point:** not a core point, but in the neighborhood of a core point — 边界点：不是核心点，但在某个核心点的邻域内
- **Noise point:** neither core nor border — outlier — 噪声点：既不是核心也不是边界 — 异常值

![Page 37](week6_clustering_slides_pages/page_037.png)

**Diagram of three point types (MinPts = 7):** Three overlapping circles with radius Eps. Right circle (labeled "core point", point **A**): point A (black dot) has ≥ 7 points (gray dots) within its ε-circle → core. Middle circle (labeled "border point", point **B**): point B has < 7 points in its own ε-circle, but falls inside A's ε-circle → border. Left circle (labeled "noise point", point **C**): point C has < 7 points in its ε-circle and doesn't fall in any core point's circle → noise. The Eps arrows show the radius of each circle.

**三种点类型示意图（MinPts = 7）：** 三个半径为Eps的重叠圆。右侧圆（标注"core point"，点**A**）：点A（黑色实心点）在其ε圆内有≥7个点（灰色点）→ 核心点。中间圆（标注"border point"，点**B**）：点B自己的ε圆内不足7个点，但落入了A的ε圆内 → 边界点。左侧圆（标注"noise point"，点**C**）：点C的ε圆内不足7个点，也不在任何核心点的圆内 → 噪声点。Eps箭头标注了每个圆的半径。

![Page 38](week6_clustering_slides_pages/page_038.png)

**Real example (Eps = 10, MinPts = 4):** Left: original scatter plot (all blue dots), forming block-letter shapes — same data as page 35. Right: after DBSCAN classification — **green** = core points (dense interior of each letter stroke), **blue** = border points (edges of letter strokes), **red** = noise points (scattered outside the letters). The letter shapes are clearly preserved by core+border points, while isolated dots are correctly flagged as noise.

**实际示例（Eps = 10, MinPts = 4）：** 左图：原始散点图（全蓝色点），形成方块字母形状 — 与第35页相同的数据。右图：DBSCAN分类后 — **绿色** = 核心点（每个字母笔画的密集内部），**蓝色** = 边界点（字母笔画的边缘），**红色** = 噪声点（字母外部的孤立点）。核心+边界点清楚地保留了字母形状，而孤立的点被正确标记为噪声。

> **📝 Notes:**
>
> **📌 What:**
> DBSCAN classifies every point into exactly one of three types: **core** (interior of dense region, ≥ MinPts neighbors within ε including itself), **border** (within ε of a core point but not core itself), or **noise** (everything else). Two parameters: ε (neighborhood radius) and MinPts (density threshold). The key insight: DBSCAN does NOT require you to specify the number of clusters — it discovers them automatically from the density structure.
>
>> DBSCAN 将每个点严格归类为三种之一：**核心点**（密集区域内部，ε内含自身有≥MinPts个邻居）、**边界点**（在某核心点的ε内但自身不是核心点）、**噪声点**（其他所有点）。两个参数：ε（邻域半径）和 MinPts（密度阈值）。关键发现：DBSCAN **不需要**你指定簇的数量 — 它从密度结构中自动发现。
>>
>
> **🎯 Why:**
> Why DBSCAN over K-Means? Three fundamental reasons: (1) K-Means assumes **spherical** clusters — it cannot handle the letter-shaped clusters shown on page 35; (2) K-Means has **no concept of noise** — every point must belong to some cluster, so outliers distort centroids; (3) K-Means requires you to **specify K** in advance, but in many real-world problems you don't know how many clusters exist. DBSCAN solves all three: arbitrary shapes, built-in noise detection, automatic K.
>
>> 为什么用DBSCAN而不是K-Means？三个根本原因：(1) K-Means假设**球形**簇 — 无法处理第35页所示的字母形状簇；(2) K-Means**没有噪声概念** — 每个点必须属于某个簇，异常值会扭曲质心；(3) K-Means需要**提前指定K**，而很多实际问题中你不知道有多少个簇。DBSCAN三个都解决了：任意形状、内置噪声检测、自动确定K。
>>
>
> **💡 Intuition:**
> Like finding crowds in a park from an aerial photo: wherever people are **densely packed** = a "group" (cluster). People standing **alone far from any group** = noise. People at the **edge of a group** (close to the crowd but not in the thick of it) = border. The ε parameter = "how far can you reach to shake someone's hand?" MinPts = "how many people must be within handshake distance for this to count as a crowd?"
>
>> 像从航拍照片中找公园里的人群：人们**密集聚集**的地方 = 一个"群"（簇）。**远离任何群独自站着**的人 = 噪声。在**群的边缘**（靠近人群但不在最密处）的人 = 边界点。ε参数 = "你能伸手跟多远的人握手？" MinPts = "握手范围内必须有多少人才算一个人群？"
>>
>
> **⚙️ How:**
> Classification procedure: For each point p, count how many points fall within distance ε (including p itself). If count ≥ MinPts → p is **core**. If count < MinPts but p is within ε of some core point → p is **border**. Otherwise → p is **noise**. Important subtlety: a border point may be within ε of multiple core points from different clusters — it gets assigned to whichever core point is processed first (non-deterministic for border points).
>
>> 分类流程：对每个点p，计算距离ε内有多少个点（含p自身）。如果数量 ≥ MinPts → p是**核心点**。如果数量 < MinPts 但p在某个核心点的ε内 → p是**边界点**。否则 → p是**噪声点**。重要细节：一个边界点可能在不同簇的多个核心点的ε内 — 它会被分配给最先被处理的那个核心点（边界点的归属是非确定性的）。
>>
>
> **⚖️ Compare:**
> | Feature | K-Means | DBSCAN |
> |---|---|---|
> | Specify K? | Yes (required) | No (auto-detected) |
> | Cluster shape | Spherical only | Any shape |
> | Noise handling | None (all points assigned) | Built-in (noise = separate category) |
> | Parameters | K | ε, MinPts |
> | Varying density | OK (each cluster can have different spread) | Struggles (single ε for all) |
> | Deterministic? | No (random init) | Core+noise yes, border assignment no |
> | Scalability | O(NKt) — fast | O(N²) worst case, O(N log N) with spatial index |
>
>> | 特性 | K-Means | DBSCAN |
>> |---|---|---|
>> | 需要指定K？ | 是（必须） | 否（自动检测） |
>> | 簇形状 | 仅球形 | 任意形状 |
>> | 噪声处理 | 无（所有点必须分配） | 内置（噪声 = 单独类别） |
>> | 参数 | K | ε, MinPts |
>> | 密度不均 | OK（每个簇可以有不同的扩散） | 困难（所有簇用同一个ε） |
>> | 确定性？ | 否（随机初始化） | 核心+噪声确定，边界点分配不确定 |
>> | 可扩展性 | O(NKt) — 快 | O(N²)最坏，有空间索引时O(N log N) |
>>
>
> **⚠️ Pitfall:**
> (1) DBSCAN struggles with clusters of **varying densities** — if one cluster is dense and another is sparse, a single ε can't capture both (dense cluster's ε would merge sparse cluster into noise). (2) **"Including itself"** in the core point definition is a classic exam trap: with MinPts=4, a point with 3 neighbors (plus itself = 4) IS core. (3) Choosing ε and MinPts requires domain knowledge — the k-distance plot heuristic (plot sorted k-th nearest neighbor distances, look for the "elbow") can help choose ε but is not foolproof.
>
>> (1) DBSCAN在**密度不均**的簇上表现差 — 若一个簇密集一个稀疏，单一ε无法兼顾（密集簇的ε会把稀疏簇当成噪声）。(2) 核心点定义中的**"包括自身"**是经典考试陷阱：MinPts=4时，一个有3个邻居的点（加上自身=4）是核心点。(3) 选择ε和MinPts需要领域知识 — k-距离图启发法（画排序后的第k近邻距离曲线，找"肘部"）可以辅助选ε，但并非万能。
>>
>
> **📝 Exam:**
> "Given a set of points with pairwise distances, ε = X, MinPts = Y, classify each point as core/border/noise." Step-by-step: (1) for each point, count neighbors within ε (include itself!); (2) if count ≥ MinPts → core; (3) remaining points: if within ε of any core → border; (4) rest → noise. Also expect: "Why can't K-Means handle this data?" → non-spherical clusters / noise.
>
>> "给定一组点及其成对距离，ε = X，MinPts = Y，将每个点分类为核心/边界/噪声。" 步骤：(1) 对每个点，数ε内的邻居（包含自身！）；(2) 如果数量 ≥ MinPts → 核心；(3) 剩余的点：如果在任何核心点的ε内 → 边界；(4) 剩下的 → 噪声。还可能考："为什么K-Means无法处理这种数据？" → 非球形簇 / 噪声。
>>

### 5.2 算法步骤 (Algorithm Steps)

![Page 39](week6_clustering_slides_pages/page_039.png)

**DBSCAN Algorithm slide:** Title "DBSCAN Algorithm". Summary line: "Form clusters using core points, and assign border points to one of its neighboring clusters." Then 5 numbered steps listed in plain text. This is the complete pseudocode — note it is NOT iterative like K-Means; it runs in a single pass (label → eliminate → connect → cluster → assign).

**DBSCAN 算法幻灯片：** 标题"DBSCAN Algorithm"。摘要行："用核心点形成簇，将边界点分配到其相邻簇之一。"然后列出5个编号步骤。这是完整的伪代码 — 注意它不像K-Means那样迭代；它一次性完成（标记→去除→连接→成簇→分配）。

**Algorithm steps / 算法步骤：**

1. **Label** all points as core, border, or noise — **标记**所有点为核心、边界或噪声
2. **Eliminate** noise points — **去除**噪声点
3. Put an **edge** between all core points within distance ε of each other — 在所有距离ε内的核心点之间连**边**
4. Make each group of **connected core points** into a separate cluster — 每组**连通的核心点**构成一个独立的簇
5. **Assign** each border point to one of the clusters of its associated core points — 将每个边界点**分配**到其关联核心点所在的簇

![Page 40](week6_clustering_slides_pages/page_040.png)

**"When DBSCAN Works Well" slide:** Left: original scatter plot (all blue dots) forming block-letter shapes — same data as before. Right: DBSCAN result — each letter is assigned a different color (dark red, blue, red/orange, yellow, green, cyan), and **dark blue dots scattered around the letters = noise** (automatically excluded). Bottom text: "Can handle clusters of different shapes and sizes" and "Resistant to noise." This demonstrates that DBSCAN correctly separated each letter as a distinct cluster despite their non-convex shapes.

**"DBSCAN何时表现好"幻灯片：** 左图：原始散点图（全蓝色点），形成方块字母形状 — 与之前相同的数据。右图：DBSCAN结果 — 每个字母被分配不同颜色（深红、蓝、红/橙、黄、绿、青），**字母周围散布的深蓝色点 = 噪声**（被自动排除）。底部文字："Can handle clusters of different shapes and sizes"和"Resistant to noise"。这展示了DBSCAN正确地将每个字母分为独立的簇，尽管它们的形状是非凸的。

- Can handle clusters of **different shapes and sizes** — 能处理**不同形状和大小**的簇
- **Resistant to noise** (dark blue points = noise, automatically excluded) — **抗噪声**（深蓝色点 = 噪声，被自动排除）

> **📝 Notes:**
>
> **📌 What:**
> DBSCAN algorithm in 5 steps: (1) classify all points, (2) discard noise, (3) build a graph connecting core points within ε, (4) find connected components = clusters, (5) attach border points. Unlike K-Means, this is a **single-pass** algorithm — no iteration, no convergence criterion, no random initialization. The number of clusters is determined by the graph structure, not by a user parameter.
>
>> DBSCAN 算法5步：(1) 分类所有点，(2) 丢弃噪声，(3) 在ε内的核心点间建图连边，(4) 找连通分量 = 簇，(5) 附加边界点。与K-Means不同，这是**单遍**算法 — 没有迭代、没有收敛条件、没有随机初始化。簇的数量由图结构决定，不是用户参数。
>>
>
> **🎯 Why:**
> Why is step 3 (building edges between core points) the key? Because it transforms the clustering problem into a **graph connectivity** problem. Once you have the graph, connected components give you clusters for free. This is fundamentally different from K-Means which tries to optimize an objective function — DBSCAN makes a structural/topological argument about the data.
>
>> 为什么第3步（在核心点间连边）是关键？因为它把聚类问题转化为**图连通性**问题。有了图之后，连通分量就直接给出了簇。这与K-Means试图优化目标函数根本不同 — DBSCAN 对数据做的是结构/拓扑论证。
>>
>
> **💡 Intuition:**
> Think of it as a **"friendship chain"** algorithm: (1) Identify popular people (core = knows ≥ MinPts people nearby). (2) Ignore loners (noise). (3) If two popular people know each other → draw a friendship line. (4) Each connected friend group = one cluster. (5) Shy people (border) who know a popular person join that person's group. The clusters emerge from the social network structure, not from measuring everyone's distance to some "center."
>
>> 把它想象成**"朋友链"**算法：(1) 找出人缘好的人（核心 = 附近认识 ≥ MinPts 人）。(2) 忽略独行侠（噪声）。(3) 如果两个人缘好的人互相认识 → 画一条友谊线。(4) 每个连通的朋友圈 = 一个簇。(5) 认识某个人缘好的人的腼腆者（边界）加入那个人的圈子。簇从社交网络结构中涌现，而不是通过测量每个人到某个"中心"的距离。
>>
>
> **⚙️ How:**
> Key insight: DBSCAN is essentially a **graph-based** algorithm. Steps 3–4 convert the problem to: "build a graph where nodes = core points, edges = pairs within ε; find connected components." This can be done via BFS/DFS. Time complexity: O(N²) naive (check all pairs), but with a **spatial index** (e.g., KD-tree, R-tree), neighborhood queries become O(log N) each → total O(N log N). The page 40 result shows 6+ clusters discovered automatically — no K needed.
>
>> 关键洞察：DBSCAN本质上是**基于图**的算法。步骤3–4将问题转化为："构建核心点为节点、ε内的点对为边的图；找连通分量。"这可以用BFS/DFS完成。时间复杂度：朴素O(N²)（检查所有点对），但使用**空间索引**（如KD树、R树），邻域查询变为O(log N) → 总计O(N log N)。第40页的结果显示自动发现了6+个簇 — 不需要K。
>>
>
> **⚖️ Compare:**
> DBSCAN algorithm vs K-Means algorithm structure:
> | Aspect | K-Means | DBSCAN |
> |---|---|---|
> | Nature | Iterative optimization | Single-pass graph construction |
> | Steps | Assign → Update centroids → Repeat | Label → Remove noise → Connect → Components → Assign borders |
> | Convergence | May need many iterations | Always finishes in one pass |
> | Initialization | Random centroids (affects result) | None needed (deterministic for core/noise) |
> | Output | K clusters, every point assigned | Variable # clusters + noise category |
>
>> DBSCAN算法 vs K-Means算法结构：
>> | 方面 | K-Means | DBSCAN |
>> |---|---|---|
>> | 本质 | 迭代优化 | 单遍图构建 |
>> | 步骤 | 分配→更新质心→重复 | 标记→去噪→连接→连通分量→分配边界 |
>> | 收敛 | 可能需要多次迭代 | 一遍即完 |
>> | 初始化 | 随机质心（影响结果） | 不需要（核心/噪声结果确定） |
>> | 输出 | K个簇，每个点必须分配 | 不定数量的簇 + 噪声类别 |
>>
>
> **⚠️ Pitfall:**
> (1) **Border point ambiguity:** Step 5 says "assign each border point to one of the clusters of its associated core points" — but if a border point is near core points from two different clusters, which cluster wins? The answer: **whichever is processed first** → border assignments are non-deterministic and depend on processing order. (2) **"When DBSCAN works well"** (page 40) is a hint that there are cases when it does NOT work well — specifically: varying density clusters, high-dimensional data (ε becomes meaningless due to curse of dimensionality), and data where clusters are connected by thin bridges of points.
>
>> (1) **边界点歧义：** 第5步说"将边界点分配到其关联核心点的簇" — 但如果一个边界点靠近两个不同簇的核心点，哪个簇赢？答案：**先被处理到的那个** → 边界点分配是非确定性的，取决于处理顺序。(2) **"DBSCAN何时表现好"**（第40页）暗示了它表现**不好**的情况 — 具体是：密度不均的簇、高维数据（维度灾难使ε失去意义）、以及簇之间有细窄点桥连接的数据。
>>
>
> **📝 Exam:**
> "Describe the 5 steps of the DBSCAN algorithm." Must list: (1) Label core/border/noise, (2) Eliminate noise, (3) Connect core points within ε, (4) Connected components → clusters, (5) Assign borders. Follow-up: "Why can DBSCAN find non-spherical clusters?" → Because it uses graph connectivity (not centroid distance), so the cluster shape follows the density structure regardless of geometry.
>
>> "描述DBSCAN算法的5个步骤。" 必须列出：(1) 标记核心/边界/噪声，(2) 去除噪声，(3) 连接ε内的核心点，(4) 连通分量→簇，(5) 分配边界。追问："为什么DBSCAN能找到非球形簇？" → 因为它使用图连通性（不是质心距离），簇的形状跟随密度结构，与几何形状无关。
>>

---

## 6. 基于分布的聚类: EM (Distribution-based Clustering: EM)

![Page 41](week6_clustering_slides_pages/page_041.png)

**Distribution-based Clustering introduction:** Title "Distribution-based Clustering". Two bullet points: (1) "Idea is to model the set of data points as arising from a mixture of distributions" with sub-bullets noting Gaussian is typical but other distributions work too; (2) "Clusters are found by estimating the parameters of the statistical distributions using the Expectation-Maximization (EM) algorithm." This is a text-only overview slide — no diagrams.

**基于分布的聚类引入：** 标题"Distribution-based Clustering"。两个要点：(1) "将数据点集建模为来自混合分布" — 通常用高斯分布，但其他分布也可以；(2) "通过期望最大化（EM）算法估计统计分布的参数来发现簇。"这是纯文字概览页 — 没有图表。

> **📎 Background / 背景知识：**
> **Gaussian (Normal) Distribution** = the classic "bell curve" 🔔. Most natural phenomena cluster around an average value, with fewer observations far from the center — this shape is a Gaussian.
> - Defined by just **2 parameters**: **μ** (mean = where the bell is centered) and **σ** (standard deviation = how wide/narrow the bell is)
> - Example: human heights — most people are near average height, few are very tall or very short → bell-shaped histogram
> - Why use it for clustering? If each cluster's data roughly forms a bell shape, we can describe the entire cluster with just (μ, σ) instead of listing every point
>
>> **高斯（正态）分布** = 经典的"钟形曲线" 🔔。大多数自然现象围绕均值聚集，远离中心的观测更少 — 这个形状就是高斯分布。
>> - 仅由**2个参数**定义：**μ**（均值 = 钟形曲线中心位置）和 **σ**（标准差 = 钟形曲线宽窄）
>> - 示例：人的身高 — 大部分人接近平均身高，很高或很矮的人少 → 直方图呈钟形
>> - 为什么用它做聚类？如果每个簇的数据大致呈钟形，只需 (μ, σ) 就能描述整个簇，不用列出每个点

- Model data as arising from a **mixture of distributions** (typically Gaussian) — 将数据建模为**混合分布**（通常是高斯分布）
- Clusters are found by estimating distribution parameters using **Expectation-Maximization (EM)** algorithm — 通过**EM算法**估计分布参数来发现簇

![Page 42](week6_clustering_slides_pages/page_042.png)

**Distribution-based Clustering Example:** Title "Distribution-based Clustering: Example". Left: text labeled "Informal example" (orange highlighted) describing modeling points that generate a histogram. Right: a histogram (bar chart) with x-axis = x values (range −15 to 15), y-axis = "Number of Points" (up to 500). The histogram shows **two overlapping bell-shaped peaks** — one centered around −5 and another around +5. Below: three bullet points explaining that if we estimate each Gaussian's μ and σ, we completely describe the clusters, can compute membership probabilities, and assign points. Bottom: the Gaussian PDF formula: prob(xᵢ|Θ) = (1/√(2πσ)) · e^(−(x−μ)²/(2σ²)).

**基于分布的聚类示例：** 标题"Distribution-based Clustering: Example"。左侧："Informal example"（橙色高亮）文字描述。右侧：直方图（柱状图），x轴 = x值（范围−15到15），y轴 = "Number of Points"（最高500）。直方图显示**两个重叠的钟形峰** — 一个中心约在−5，另一个约在+5。下方：三个要点说明如果估计每个高斯的μ和σ，就能完全描述簇、计算隶属概率并分配点。底部：高斯PDF公式：prob(xᵢ|Θ) = (1/√(2πσ)) · e^(−(x−μ)²/(2σ²))。

- **Gaussian PDF (Probability Density Function / 概率密度函数):** prob(xᵢ|Θ) = (1/√(2πσ)) · e^(−(x−μ)²/(2σ²))
  - xᵢ = a data point — 一个数据点
  - Θ = parameters {μ, σ} — 参数集
  - μ = mean (center of the bell curve) — 均值（钟形曲线中心）
  - σ = standard deviation (width of the bell curve) — 标准差（钟形曲线宽度）
  - Overall: probability of observing xᵢ given this Gaussian — 在给定高斯下观察到xᵢ的概率

![Page 43](week6_clustering_slides_pages/page_043.png)

**EM algorithm motivation slide:** Title "EM…". Top: two side-by-side 1D scatter plots (number line 0–6). Left plot: points colored **blue and orange** showing known cluster membership — easy to estimate parameters. Right plot: same points but **all blue** (unknown membership) — can't estimate directly. Below: the chicken-and-egg problem text: "If we know the source → easy to estimate parameters. If we know the parameters → easy to assign points. If we know neither → ???" Then **EM algorithm** steps: start with k randomly placed Gaussians (k=2: (μₐ,σₐ²), (μᵦ,σᵦ²)); E-step: for each point xᵢ, compute P(b|xᵢ) = probability of belonging to blue group (soft clustering); M-step: calculate new (μₐ,σₐ²), (μᵦ,σᵦ²) to fit points weighted by their probabilities.

**EM算法动机幻灯片：** 标题"EM…"。顶部：两个并排的1D散点图（数轴0–6）。左图：点用**蓝色和橙色**着色表示已知簇归属 — 容易估计参数。右图：同样的点但**全是蓝色**（未知归属）— 无法直接估计。下方：鸡与蛋问题文字："知道来源→容易估参数。知道参数→容易分配点。两个都不知道→???" 然后是**EM算法**步骤：从k个随机放置的高斯开始（k=2: (μₐ,σₐ²), (μᵦ,σᵦ²)）；E步：对每个点xᵢ，计算P(b|xᵢ) = 属于蓝组的概率（软聚类）；M步：计算新的(μₐ,σₐ²), (μᵦ,σᵦ²)以拟合按概率加权的点。

![Page 44](week6_clustering_slides_pages/page_044.png)

**More Detailed EM Algorithm slide:** Title "More Detailed EM Algorithm". Left: plot showing the same 1D data points on number line 0–6, with two fitted Gaussian curves — **blue** (centered ~2) and **red** (centered ~3.5) — representing the two estimated components. Right: three formulas stacked vertically: (1) **P(xᵢ|b)** = Gaussian PDF for cluster b — likelihood of point xᵢ under cluster b; (2) **bᵢ = P(b|xᵢ)** = Bayes' rule: P(xᵢ|b)P(b) / [P(xᵢ|b)P(b) + P(xᵢ|a)P(a)] — posterior probability (E-step); (3) **μᵦ** = weighted mean = (b₁x₁+b₂x₂+…+bₙxₙ)/(b₁+b₂+…+bₙ) — M-step update for mean; (4) **σᵦ²** = weighted variance = Σbᵢ(xᵢ−μᵦ)²/Σbᵢ — M-step update for variance.

**更详细的EM算法幻灯片：** 标题"More Detailed EM Algorithm"。左侧：同样1D数据点在数轴0–6上，带两条拟合高斯曲线 — **蓝色**（中心~2）和**红色**（中心~3.5）— 代表两个估计分量。右侧：三个公式纵向排列：(1) **P(xᵢ|b)** = 簇b的高斯PDF — xᵢ在簇b下的似然；(2) **bᵢ = P(b|xᵢ)** = 贝叶斯公式：P(xᵢ|b)P(b) / [P(xᵢ|b)P(b) + P(xᵢ|a)P(a)] — 后验概率（E步）；(3) **μᵦ** = 加权均值 = (b₁x₁+b₂x₂+…+bₙxₙ)/(b₁+b₂+…+bₙ) — M步更新均值；(4) **σᵦ²** = 加权方差 = Σbᵢ(xᵢ−μᵦ)²/Σbᵢ — M步更新方差。

**Key formulas / 关键公式：**

- **E-step (Expectation):** Compute posterior probability using Bayes' rule — 用贝叶斯公式计算后验概率
  - bᵢ = P(b|xᵢ) = P(xᵢ|b)P(b) / [P(xᵢ|b)P(b) + P(xᵢ|a)P(a)]
  - bᵢ = probability that point xᵢ belongs to cluster b — 点xᵢ属于簇b的概率
  - P(xᵢ|b) = Gaussian PDF evaluated at xᵢ with parameters μᵦ, σᵦ — 用μᵦ, σᵦ参数在xᵢ处求高斯PDF值
  - P(b) = mixing weight (prior probability of cluster b) — 混合权重（簇b的先验概率）
- **M-step (Maximization):** Re-estimate parameters using weighted statistics — 用加权统计量重新估计参数
  - μᵦ = Σ(bᵢ · xᵢ) / Σbᵢ  (weighted mean) — 加权均值
  - σᵦ² = Σbᵢ(xᵢ − μᵦ)² / Σbᵢ  (weighted variance) — 加权方差
  - P(b) = Σbᵢ / N  (updated mixing weight) — 更新后的混合权重

> **📝 Notes:**
>
> **📌 What:**
> EM = **soft clustering** via probability distributions. Instead of assigning each point to exactly one cluster (hard assignment like K-Means), EM assigns **membership probabilities**: "Point xᵢ has 80% chance of being in Cluster 1 and 20% in Cluster 2." Each cluster is modeled as a Gaussian with parameters (μ, σ², mixing weight). The algorithm iterates E-step (compute probabilities) → M-step (update parameters) until convergence.
>
>> EM = 通过概率分布的**软聚类**。不像K-Means那样将每个点硬分配到一个簇，EM分配**隶属概率**："点xᵢ有80%概率在簇1，20%在簇2。"每个簇建模为高斯分布，参数为(μ, σ², 混合权重)。算法迭代 E步（计算概率）→ M步（更新参数）直到收敛。
>>
>
> **🎯 Why:**
> Why do we need EM? Because of the **chicken-and-egg problem** (page 43): if we knew which points belong to which cluster, we could easily estimate the Gaussian parameters (just compute mean and variance per group). If we knew the parameters, we could easily assign points (just evaluate the PDF). But we know **neither** — EM solves this by alternating between the two steps, gradually refining both assignments and parameters simultaneously.
>
>> 为什么需要EM？因为**鸡与蛋问题**（第43页）：如果知道哪些点属于哪个簇，就能轻松估计高斯参数（直接算每组的均值和方差）。如果知道参数，就能轻松分配点（直接算PDF值）。但我们**两个都不知道** — EM通过交替执行两步来解决，逐步同时优化分配和参数。
>>
>
> **💡 Intuition:**
> Imagine wearing **blurry glasses** looking at two overlapping crowds. Initially you guess where each crowd's center is (random init). E-step: squinting, you guess "this person is probably 70% in crowd A, 30% in crowd B" based on distance to each guessed center. M-step: you recompute each crowd's center using these soft assignments (person who's 70% in A contributes 70% of their position to A's center). Repeat: your vision "clears up" each round until the crowds stabilize. Unlike K-Means where you'd force each person into exactly one crowd, EM lets them straddle both.
>
>> 想象戴着**模糊眼镜**看两群重叠的人。一开始你猜测每群的中心在哪（随机初始化）。E步：眯着眼，你根据到每个猜测中心的距离判断"这个人70%概率在A群，30%在B群"。M步：你用这些软分配重新计算每群中心（70%属于A的人贡献70%的位置给A的中心）。重复：每轮视线都"更清晰"，直到人群稳定。与K-Means强制每人属于一个群不同，EM允许他们同时跨属两个群。
>>
>
> **🔗 Formula Chain / 公式链路图:**
> The formulas in EM form a dependency chain — each formula feeds into the next:
>
> ```
> ① Gaussian PDF: P(xᵢ|b) = (1/√2πσᵦ) · e^(-(xᵢ-μᵦ)²/2σᵦ²)
>        ↓ "How likely is xᵢ under cluster b?"
> ② Bayes' Rule (E-step): bᵢ = P(xᵢ|b)·P(b) / [P(xᵢ|b)·P(b) + P(xᵢ|a)·P(a)]
>        ↓ "What's the probability xᵢ belongs to b?"
> ③ Weighted Mean (M-step): μᵦ = Σ(bᵢ·xᵢ) / Σbᵢ
>        ↓ "New center of cluster b"
> ④ Weighted Variance (M-step): σᵦ² = Σbᵢ(xᵢ-μᵦ)² / Σbᵢ
>        ↓ "New width of cluster b"
> ⑤ Updated P(b) = Σbᵢ / N
>        ↓ "New mixing weight"
>   ↺ Back to ① with new μᵦ, σᵦ², P(b) → repeat until convergence
> ```
>
>> EM 的公式形成依赖链 — 每个公式的输出是下一个的输入：
>>
>> ```
>> ① 高斯PDF：P(xᵢ|b) → "xᵢ在簇b下有多可能？"
>>      ↓
>> ② 贝叶斯公式（E步）：bᵢ → "xᵢ属于b的概率是多少？"
>>      ↓
>> ③ 加权均值（M步）：μᵦ → "簇b的新中心"
>>      ↓
>> ④ 加权方差（M步）：σᵦ² → "簇b的新宽度"
>>      ↓
>> ⑤ 更新混合权重：P(b) → "簇b的新比例"
>>      ↓
>>   ↺ 用新的 μᵦ, σᵦ², P(b) 回到① → 重复直到收敛
>> ```
>>
>
> **⚙️ How:**
> The E-step uses **Bayes' rule** to compute posterior: P(b|xᵢ) = P(xᵢ|b)·P(b) / Σⱼ P(xᵢ|j)·P(j). This is the key formula — it converts the likelihood (how well does the Gaussian explain this point?) into a membership probability.  The M-step then computes **weighted statistics**: μᵦ and σᵦ² are just the regular mean and variance formulas, but each point xᵢ is weighted by its membership probability bᵢ instead of counting equally. This is why EM generalizes K-Means: in K-Means, bᵢ is either 0 or 1 (hard assignment), so the weighted mean reduces to a simple mean of assigned points.
>
>> E步使用**贝叶斯公式**计算后验：P(b|xᵢ) = P(xᵢ|b)·P(b) / Σⱼ P(xᵢ|j)·P(j)。这是关键公式 — 它将似然（这个高斯对这个点解释得多好？）转化为隶属概率。M步计算**加权统计量**：μᵦ和σᵦ²就是普通的均值和方差公式，但每个点xᵢ用其隶属概率bᵢ加权而非等权计数。这就是EM推广K-Means的原因：在K-Means中，bᵢ要么是0要么是1（硬分配），加权均值退化为分配点的简单均值。
>>
>
> **📐 Formula:**
> Reading bᵢ = P(b|xᵢ) = P(xᵢ|b)P(b) / [P(xᵢ|b)P(b) + P(xᵢ|a)P(a)] piece by piece:
> - P(xᵢ|b): plug xᵢ into Gaussian PDF with current μᵦ, σᵦ → how likely is this point under cluster b?
> - P(b): mixing weight = fraction of all points expected in cluster b (prior)
> - Numerator P(xᵢ|b)·P(b): "evidence for cluster b" for this point
> - Denominator: sum of evidence for ALL clusters → normalizes to a valid probability
> - Result bᵢ ∈ [0,1]: soft membership of point xᵢ in cluster b
>
>> 逐段读 bᵢ = P(b|xᵢ) = P(xᵢ|b)P(b) / [P(xᵢ|b)P(b) + P(xᵢ|a)P(a)]：
>> - P(xᵢ|b)：用当前μᵦ, σᵦ将xᵢ代入高斯PDF → 这个点在簇b下有多可能？
>> - P(b)：混合权重 = 预期属于簇b的点的比例（先验）
>> - 分子 P(xᵢ|b)·P(b)："簇b对这个点的证据"
>> - 分母：所有簇的证据之和 → 归一化为有效概率
>> - 结果 bᵢ ∈ [0,1]：点xᵢ在簇b中的软隶属度
>>
>
> **⚖️ Compare:**
> | Feature | K-Means | EM (GMM) |
> |---|---|---|
> | Assignment | Hard (0 or 1) | Soft (probabilities) |
> | Cluster model | Point (centroid only) | Full Gaussian (μ, σ², weight) |
> | Output | Cluster labels | Membership probabilities |
> | Cluster shape | Spherical, equal variance | Elliptical, different variances |
> | Relationship | Special case of EM | Generalization of K-Means |
> | Iteration | Assign → Update centroids | E-step (posteriors) → M-step (parameters) |
> | Convergence | Local optimum | Local optimum (same issue) |
>
>> | 特性 | K-Means | EM (GMM) |
>> |---|---|---|
>> | 分配方式 | 硬分配（0或1） | 软分配（概率） |
>> | 簇模型 | 点（仅质心） | 完整高斯（μ, σ², 权重） |
>> | 输出 | 簇标签 | 隶属概率 |
>> | 簇形状 | 球形、等方差 | 椭圆形、不同方差 |
>> | 关系 | EM的特殊情况 | K-Means的推广 |
>> | 迭代 | 分配→更新质心 | E步（后验）→ M步（参数） |
>> | 收敛 | 局部最优 | 局部最优（同样问题） |
>>
>
> **⚠️ Pitfall:**
> (1) **Local optima:** EM converges to local optima just like K-Means — different initializations → different results. Run multiple times and pick the best (highest log-likelihood). (2) **Number of components:** You must specify k (number of Gaussians) in advance — use **BIC/AIC** to select k (lower = better fit with parsimony). (3) **Singularity:** If a Gaussian collapses onto a single data point, σ → 0 and likelihood → ∞. Practical implementations add regularization or minimum variance constraints. (4) **Assumes Gaussian shape:** If the true clusters are not Gaussian (e.g., crescent-shaped), EM will fit poorly.
>
>> (1) **局部最优：** EM像K-Means一样收敛到局部最优 — 不同初始化→不同结果。运行多次，选最好的（最高对数似然）。(2) **分量数：** 必须提前指定k（高斯个数）— 用**BIC/AIC**选k（越低越好，兼顾拟合与简洁）。(3) **奇异性：** 如果一个高斯塌缩到单个数据点，σ→0且似然→∞。实际实现会加正则化或最小方差约束。(4) **假设高斯形状：** 如果真实簇不是高斯形的（如月牙形），EM拟合效果差。
>>
>
> **📝 Exam:**
> "What are the E-step and M-step in EM?" → E-step = compute posterior membership probabilities P(b|xᵢ) using Bayes' rule. M-step = re-estimate μ, σ², mixing weights using weighted statistics. "How is K-Means a special case of EM?" → When all clusters have equal, fixed variance, and membership probabilities are forced to 0 or 1 (hard assignment), EM reduces to K-Means. "Given current parameters, compute P(b|xᵢ)." → Plug into Bayes' formula with Gaussian PDFs.
>
>> "EM中E步和M步是什么？" → E步 = 用贝叶斯公式计算后验隶属概率P(b|xᵢ)。M步 = 用加权统计量重新估计μ, σ², 混合权重。"K-Means如何是EM的特殊情况？" → 当所有簇方差相等且固定，隶属概率被强制为0或1（硬分配），EM退化为K-Means。"给定当前参数，计算P(b|xᵢ)。" → 代入带高斯PDF的贝叶斯公式。
>>

---

## 7. 聚类有效性评估 (Cluster Validity)

### 7.1 评估指标分类 (Types of Measures)

![Page 45](week6_clustering_slides_pages/page_045.png)

**Measures of Cluster Validity slide:** Title "Measures of Cluster Validity". Text explains numerical measures for judging clustering quality, classified into two types: **Supervised** (orange text) — measures how well cluster labels match externally supplied class labels, often called ***external indices*** (yellow highlighted); **Unsupervised** (orange text) — measures goodness of clustering without external information (e.g., SSE), often called ***internal indices*** (yellow highlighted). Bottom bullet: "You can use supervised or unsupervised measures to compare clustering methods."

**聚类有效性度量幻灯片：** 标题"Measures of Cluster Validity"。文字解释评判聚类质量的数值指标，分为两类：**有监督**（橙色文字）— 衡量聚类标签与外部提供的类标签匹配程度，常称为***外部指标***（黄色高亮）；**无监督**（橙色文字）— 在没有外部信息的情况下衡量聚类的好坏（如SSE），常称为***内部指标***（黄色高亮）。底部要点："可以使用有监督或无监督指标来比较聚类方法。"

| Type | Description | Also Called |
| --- | --- | --- |
| **Supervised (External)** | Measures how well cluster labels match externally supplied class labels | External indices — 外部指标 |
| **Unsupervised (Internal)** | Measures goodness of clustering without external information (e.g., SSE) | Internal indices — 内部指标 |

> **📝 Notes:**
>
> **📌 What:**
> Two ways to evaluate clustering quality: (1) **External (supervised):** you have ground-truth labels and compare clusters against them — requires labeled data. (2) **Internal (unsupervised):** no ground truth — measure quality using only the data itself (e.g., how compact are clusters? how separated?). In practice, ground truth is rarely available (otherwise you'd use classification, not clustering), so internal measures are more commonly used.
>
>> 评估聚类质量的两种方式：(1) **外部（有监督）：** 有真实标签，将聚类结果与之对比 — 需要标注数据。(2) **内部（无监督）：** 没有真实标签 — 仅用数据本身衡量质量（如簇有多紧凑？多分离？）。实际中很少有真实标签（否则用分类而不是聚类），所以内部指标更常用。
>>

### 7.2 凝聚度与分离度 (Cohesion and Separation)

![Page 46](week6_clustering_slides_pages/page_046.png)

**Unsupervised Measures: Cohesion and Separation slide:** Title "Unsupervised Measures: Cohesion and Separation". Top: **Cluster Cohesion** (orange text) — "Measures how closely related are objects in a cluster", example = SSE. **Cluster Separation** (orange text) — "Measure how distinct or well-separated a cluster is from other clusters". Middle section titled "Example: Squared Error": cohesion measured by **within cluster sum of squares** (SSE), separation measured by **between cluster sum of squares** (SSB). Right side: two formulas — SSE = Σᵢ Σ_{x∈Cᵢ} (x − mᵢ)² and SSB = Σᵢ |Cᵢ|(m − mᵢ)². Bottom left: "|Cᵢ| is the size of cluster i, and m is the **global (grand) mean** of all data points."

**无监督度量：凝聚度与分离度幻灯片：** 标题"Unsupervised Measures: Cohesion and Separation"。顶部：**簇凝聚度**（橙色文字）— "衡量簇内对象有多紧密"，示例 = SSE。**簇分离度**（橙色文字）— "衡量一个簇与其他簇有多分离"。中间标题"Example: Squared Error"：凝聚度用**簇内平方和**（SSE）衡量，分离度用**簇间平方和**（SSB）衡量。右侧：两个公式 — SSE = Σᵢ Σ_{x∈Cᵢ} (x − mᵢ)² 和 SSB = Σᵢ |Cᵢ|(m − mᵢ)²。左下："|Cᵢ|是簇i的大小，m是所有数据点的**全局（总）均值**。"

- **Cohesion (SSE / SSW):** How closely related are objects within a cluster — 簇内对象有多紧密
  - SSE = Σᵢ Σ_{x∈Cᵢ} (x − mᵢ)² — 簇内平方和
  - mᵢ = centroid of cluster i — 簇i的质心
- **Separation (SSB):** How distinct a cluster is from other clusters — 簇与其他簇有多分离
  - SSB = Σᵢ |Cᵢ| · (m − mᵢ)² — 簇间平方和
  - m = global (grand) mean of all data points — 所有数据点的全局均值
  - |Cᵢ| = number of points in cluster i — 簇i中的点数

![Page 47](week6_clustering_slides_pages/page_047.png)

**Worked example slide — SSB + SSE = constant:** Title "Unsupervised Measures: Cohesion and Separation". Top: "Example SSE, SSB + SSE = constant". A 1D number line from 1 to 5 with four green dots at positions 1, 2, 4, 5. Red **×** marks show cluster centroids: m₁ ≈ 1.5, m₂ ≈ 4.5. A vertical arrow labeled **m** points to position 3 = grand mean. Below: two calculations — **K=1:** SSE=(1−3)²+(2−3)²+(4−3)²+(5−3)²=10, SSB=4×(3−3)²=0, Total=10. **K=2:** clusters {1,2} m₁=1.5, {4,5} m₂=4.5; SSE=(1−1.5)²+(2−1.5)²+(4−4.5)²+(5−4.5)²=1, SSB=2×(1.5−3)²+2×(4.5−3)²=9, Total=10 ✓.

**算例幻灯片 — SSB + SSE = 常数：** 标题"Unsupervised Measures: Cohesion and Separation"。顶部："Example SSE, SSB + SSE = constant"。1D数轴从1到5，四个绿色点在位置1、2、4、5。红色**×**标记为簇质心：m₁≈1.5, m₂≈4.5。垂直箭头标记**m**指向位置3 = 全局均值。下方两组计算 — **K=1：** SSE=10, SSB=0, 总计=10。**K=2：** 簇{1,2} m₁=1.5, {4,5} m₂=4.5; SSE=1, SSB=9, 总计=10 ✓。

**Worked Example / 算例** — SSB + SSE = TSS (constant / 常数):

- K=1 cluster: data = {1, 2, 4, 5}, grand mean m = 3
  - SSE = (1−3)² + (2−3)² + (4−3)² + (5−3)² = 4+1+1+4 = **10**
  - SSB = 4 × (3−3)² = **0**
  - Total = 10 + 0 = **10**
- K=2 clusters: {1,2} m₁=1.5, {4,5} m₂=4.5
  - SSE = (1−1.5)² + (2−1.5)² + (4−4.5)² + (5−4.5)² = 0.25×4 = **1**
  - SSB = 2×(1.5−3)² + 2×(4.5−3)² = 4.5+4.5 = **9**
  - Total = 1 + 9 = **10** ✓
- **Key insight / 关键发现:** SSE↓ + SSB↑ = constant. More clusters → lower SSE, higher SSB — 更多簇 → SSE更低、SSB更高

![Page 48](week6_clustering_slides_pages/page_048.png)

**Graph-based approach slide:** Title "Unsupervised Measures: Cohesion and Separation". Text: "A distance graph-based approach can also be used for cohesion and separation." Two diagrams: Left labeled **"cohesion"** — a single cloud-shaped cluster with 3 nodes, all internal edges drawn as yellow lines (sum of all intra-cluster link weights = cohesion). Right labeled **"separation"** — two cloud-shaped clusters (left with 4 nodes, right with 3 nodes), yellow lines connect nodes **between** the two clusters (sum of all inter-cluster link weights = separation). No internal edges shown on the right diagram.

**基于图的方法幻灯片：** 标题"Unsupervised Measures: Cohesion and Separation"。文字："也可以使用基于距离图的方法来计算凝聚度和分离度。"两张图：左图标记**"cohesion"** — 一个云状簇内有3个节点，所有内部边用黄色线画出（簇内链接权重之和 = 凝聚度）。右图标记**"separation"** — 两个云状簇（左4个节点，右3个节点），黄色线连接**两个簇之间**的节点（簇间链接权重之和 = 分离度）。右图不显示内部边。

- **Graph-based cohesion** = sum of weights of all links **within** a cluster — 簇**内部**所有链接权重之和
- **Graph-based separation** = sum of weights between nodes **in** the cluster and nodes **outside** — 簇内节点与簇**外**节点之间的权重之和

> **📝 Notes:**
>
> **📌 What:**
> Two complementary metrics for evaluating clustering quality without ground truth: **Cohesion (SSE)** = how tight are points within each cluster (lower = better). **Separation (SSB)** = how far apart are the cluster centroids from the overall center (higher = better). The fundamental identity: **SSE + SSB = TSS** (Total Sum of Squares), a constant that doesn't change with K. So improving one automatically improves the other.
>
>> 两个互补的聚类质量内部指标：**凝聚度（SSE）** = 每个簇内的点有多紧凑（越低越好）。**分离度（SSB）** = 簇质心离总中心有多远（越高越好）。基本恒等式：**SSE + SSB = TSS**（总平方和），不随K变化的常数。所以改善一个自动改善另一个。
>>
>
> **🎯 Why:**
> After running K-Means or any clustering algorithm, you need a way to **quantify** how good the result is — not just "it looks OK." SSE/SSB give you a number to compare: different K values, different initializations, different algorithms. Without these metrics, choosing K is purely subjective.
>
>> 运行K-Means或任何聚类算法后，需要一种方式来**量化**结果有多好 — 不只是"看起来还行"。SSE/SSB给你一个数字来比较：不同的K值、不同的初始化、不同的算法。没有这些指标，选K完全凭主观。
>>
>
> **💡 Intuition:**
> Think of SSE as **"how messy is each room?"** (each cluster = a room; distance from centroid = items scattered from center). SSB is **"how spread out are the rooms in the building?"** (centroids far from the grand mean = rooms are well-separated). The total mess (TSS) is fixed — you can either have one big messy room (K=1, high SSE, zero SSB) or many tidy rooms spread out (high K, low SSE, high SSB).
>
>> 把SSE想象为**"每个房间有多乱？"**（每个簇=一个房间；离质心的距离=物品散落离中心多远）。SSB是**"楼里的房间有多分散？"**（质心离总均值远=房间分布分散）。总乱度（TSS）是固定的 — 你可以有一个大乱房间（K=1，高SSE，零SSB）或很多整齐但分散的房间（高K，低SSE，高SSB）。
>>
>
> **📐 Formula:**
> - **SSE** = Σᵢ Σ_{x∈Cᵢ} (x − mᵢ)² → for each cluster i, sum the squared distance from every point x to its cluster centroid mᵢ, then sum across all clusters
> - **SSB** = Σᵢ |Cᵢ| · (m − mᵢ)² → for each cluster i, compute squared distance from cluster centroid mᵢ to grand mean m, weighted by cluster size |Cᵢ|
> - **TSS** = Σ (x − m)² = SSE + SSB → total variation in the data, constant regardless of clustering
>
>> - **SSE** = Σᵢ Σ_{x∈Cᵢ} (x − mᵢ)² → 对每个簇i，求所有点x到质心mᵢ的距离平方和，再对所有簇求和
>> - **SSB** = Σᵢ |Cᵢ| · (m − mᵢ)² → 对每个簇i，计算质心mᵢ到全局均值m的距离平方，乘以簇大小|Cᵢ|
>> - **TSS** = Σ (x − m)² = SSE + SSB → 数据的总变异，不随聚类方式变化
>>
>
> **🔢 Example:**
> Data = {1, 2, 4, 5}, grand mean m = 3, TSS = (1−3)²+(2−3)²+(4−3)²+(5−3)² = 10.
> K=2: {1,2} → m₁=1.5, {4,5} → m₂=4.5.
> SSE = (1−1.5)²+(2−1.5)²+(4−4.5)²+(5−4.5)² = 0.25×4 = 1.
> SSB = 2×(1.5−3)²+2×(4.5−3)² = 2×2.25+2×2.25 = 9.
> Check: 1 + 9 = 10 = TSS ✓
>
>> 数据 = {1, 2, 4, 5}，全局均值 m = 3，TSS = 10。
>> K=2：{1,2} → m₁=1.5，{4,5} → m₂=4.5。
>> SSE = 0.25×4 = 1。SSB = 2×2.25+2×2.25 = 9。
>> 验证：1 + 9 = 10 = TSS ✓
>>
>
> **⚠️ Pitfall:**
> (1) **SSE always decreases with more clusters** — at K=N (each point is its own cluster), SSE=0. So you can't just pick the K with lowest SSE; use the **elbow method** or silhouette instead. (2) **SSE is scale-dependent** — features with larger ranges dominate. Normalize your data first! (3) **SSB can be misleading** with unequal cluster sizes — a tiny outlier cluster far from the center inflates SSB without meaningful separation.
>
>> (1) **SSE随簇数增加始终下降** — 当K=N（每个点自成一簇），SSE=0。所以不能只选SSE最低的K；用**肘部法**或轮廓系数。(2) **SSE受量纲影响** — 范围大的特征占主导。先标准化数据！(3) **SSB在簇大小不等时可能误导** — 一个远离中心的小异常簇会膨胀SSB，但没有真正的分离意义。
>>
>
> **📝 Exam:**
> "Given data {1,2,4,5}, compute SSE and SSB for K=2 with clusters {1,2} and {4,5}." → m=3, m₁=1.5, m₂=4.5; SSE=1, SSB=9, Total=10. "Why does SSE+SSB=constant?" → Because TSS (total variance from grand mean) is a property of the data, not the clustering. Splitting variance into within (SSE) + between (SSB) is exhaustive.
>
>> "给定数据{1,2,4,5}，计算K=2聚类{1,2}和{4,5}的SSE和SSB。" → m=3, m₁=1.5, m₂=4.5; SSE=1, SSB=9, 总和=10。"为什么SSE+SSB=常数？" → 因为TSS（到全局均值的总方差）是数据的属性，不是聚类的。将方差分解为簇内(SSE)+簇间(SSB)是穷尽的。
>>

### 7.3 轮廓系数 (Silhouette Coefficient)

![Page 49](week6_clustering_slides_pages/page_049.png)

**Unsupervised Measures: Silhouette Coefficient slide:** Title "Unsupervised Measures: Silhouette Coefficient". Top: "Silhouette coefficient" (yellow highlighted) combines ideas of cohesion and separation for individual points. Steps listed: calculate **a** = average distance of point i to points in its cluster; calculate **b** = min(average distance of i to points in another cluster); s = (b−a)/max(a,b). Range [-1, 1], typically [0, 1], closer to 1 is better. Right side: diagram showing point **i** (white circle) at the boundary of two circular clusters — lines going left labeled "Distances used to calculate **a**" (to its own cluster), lines going right labeled "Distances used to calculate **b**" (to nearest other cluster). Bottom: "The **silhouette coefficient** tells you **how well each point fits in its cluster**."

**无监督度量：轮廓系数幻灯片：** 标题"Unsupervised Measures: Silhouette Coefficient"。顶部："轮廓系数"（黄色高亮）结合了凝聚度和分离度的概念，针对单个点。步骤：计算**a** = 点i到自己簇内其他点的平均距离；计算**b** = min(点i到其他簇中所有点的平均距离)；s = (b−a)/max(a,b)。范围[-1, 1]，通常[0, 1]，越接近1越好。右侧：点**i**（白色圆圈）在两个圆形簇的边界 — 左侧线条标记"计算**a**的距离"（到自己簇），右侧线条标记"计算**b**的距离"（到最近的其他簇）。底部："**轮廓系数**告诉你**每个点在其簇中有多合适**。"

Combines cohesion and separation for **individual points** — 结合凝聚度和分离度评估**单个点**：

1. Calculate **a** = average distance of point i to other points **in its cluster** — 点i到**自己簇内**其他点的平均距离
2. Calculate **b** = minimum (average distance of point i to points **in another cluster**) — 点i到**其他各簇**平均距离的最小值
3. **Silhouette coefficient:** s = (b − a) / max(a, b)
   - Range: [-1, 1] — 范围：[-1, 1]
   - Typically: [0, 1] — 通常在[0, 1]
   - **Closer to 1 = better** — 越接近1越好

> **📝 Notes:**
>
> **📌 What:**
> Silhouette coefficient: s = (b − a) / max(a, b). It evaluates **each individual point's** clustering quality, not just the cluster as a whole.
>
> - a = average distance from point i to all OTHER points **in its own cluster** (cohesion — lower is tighter)
> - b = minimum over all other clusters of: average distance from point i to all points in THAT cluster (separation — higher is better)
> - s ranges [-1, 1]: s ≈ 1 → well-clustered, s ≈ 0 → boundary, s ≈ -1 → misassigned
> - **Average silhouette** across all points = overall clustering quality score
>
>> 轮廓系数：s = (b − a) / max(a, b)。它评估**每个单独点**的聚类质量，而不仅是簇整体。
>>
>> - a = 点i到**自己簇内**其他所有点的平均距离（凝聚度 — 越小越紧凑）
>> - b = 对所有其他簇取最小值：点i到**该簇**所有点的平均距离（分离度 — 越大越好）
>> - s范围[-1, 1]：s ≈ 1 → 聚类好，s ≈ 0 → 边界，s ≈ -1 → 分配错误
>> - 所有点的**平均轮廓** = 整体聚类质量评分
>>
>
> **🎯 Why:**
> SSE only tells you about clusters as a whole. But what about individual points? A cluster might have low SSE overall but contain a few badly-placed points. Silhouette catches these — it asks each point individually: "Are you in the right cluster?" This makes it more diagnostic than SSE.
>
>> SSE只告诉你簇整体的情况。但单个点呢？一个簇可能整体SSE很低，但包含几个放置不当的点。轮廓系数能发现这些 — 它逐个问每个点："你在正确的簇里吗？"这使它比SSE更有诊断性。
>>
>
> **💡 Intuition:**
> Silhouette asks each point: "Am I **closer to my own team** (a) or the **nearest rival team** (b)?" If b >> a → the point is solidly in its team (s ≈ 1). If a >> b → the point should switch teams (s ≈ -1). If a ≈ b → the point is on the fence (s ≈ 0). Think of it like a player who practices with both teams — silhouette measures which team they fit better with.
>
>> 轮廓系数问每个点："我离**自己队**（a）更近还是离**最近的对手队**（b）更近？"如果b >> a → 该点稳固地在自己队（s ≈ 1）。如果a >> b → 该点应该换队（s ≈ -1）。如果a ≈ b → 该点在犹豫（s ≈ 0）。想象一个同时跟两队训练的球员 — 轮廓系数衡量他更适合哪队。
>>
>
> **📐 Formula:**
> Reading s = (b − a) / max(a, b) piece by piece:
> - Numerator (b − a): if positive → closer to own cluster (good); if negative → closer to another cluster (bad)
> - Denominator max(a, b): normalizes to [-1, 1] range regardless of absolute distances
> - Special case: if cluster has only 1 point → s = 0 (undefined cohesion)
>
>> 逐段读 s = (b − a) / max(a, b)：
>> - 分子(b − a)：正值→离自己簇更近（好）；负值→离其他簇更近（差）
>> - 分母max(a, b)：归一化到[-1, 1]范围，不受绝对距离影响
>> - 特殊情况：如果簇只有1个点 → s = 0（凝聚度未定义）
>>
>
> **⚙️ How:**
> To use silhouette for choosing K: run K-Means for K=2,3,4,..., compute average silhouette for each. Pick K with **highest average silhouette**. This is more robust than the "elbow method" which is subjective (where exactly is the "elbow"?). You can also plot per-point silhouette values sorted by cluster to visually identify problematic clusters.
>
>> 用轮廓系数选K：对K=2,3,4,...运行K-Means，计算每个K的平均轮廓。选**平均轮廓最高**的K。这比主观的"肘部法"更稳健（"肘部"到底在哪里？）。也可以绘制按簇排序的单点轮廓值，直观识别有问题的簇。
>>
>
> **⚖️ Compare:**
> | Metric | What it measures | Scope | Range | Better = |
> |---|---|---|---|---|
> | **SSE** | Within-cluster compactness | Per cluster / overall | [0, ∞) | Lower |
> | **SSB** | Between-cluster separation | Overall | [0, TSS] | Higher |
> | **Silhouette** | Per-point fit quality | Per point / overall | [-1, 1] | Closer to 1 |
>
>> | 指标 | 衡量内容 | 范围层级 | 值域 | 越好 = |
>> |---|---|---|---|---|
>> | **SSE** | 簇内紧凑度 | 每个簇 / 整体 | [0, ∞) | 越低 |
>> | **SSB** | 簇间分离度 | 整体 | [0, TSS] | 越高 |
>> | **轮廓系数** | 单点拟合质量 | 每个点 / 整体 | [-1, 1] | 越接近1 |
>>
>
> **⚠️ Pitfall:**
> (1) **Silhouette can be expensive:** computing all pairwise distances is O(N²) — problematic for large datasets. (2) **Silhouette favors convex clusters** — for non-convex shapes (e.g., crescent), silhouette may be low even if the clustering is correct. (3) **Don't blindly maximize:** in some cases, domain knowledge suggests a specific K even if silhouette is not highest.
>
>> (1) **轮廓系数可能很贵：** 计算所有成对距离是O(N²) — 对大数据集有问题。(2) **轮廓系数偏好凸形簇** — 对非凸形状（如月牙形），即使聚类正确轮廓系数也可能低。(3) **不要盲目最大化：** 有时领域知识指定了特定的K，即使轮廓系数不是最高。
>>
>
> **📝 Exam:**
> "Calculate the silhouette coefficient given a=2, b=5." → s = (5−2)/max(2,5) = 3/5 = **0.6**. "What does a negative silhouette mean?" → The point is closer to another cluster than its own — likely misassigned. "How do you use silhouette to choose K?" → Run clustering for each K, compute average silhouette, pick K with highest value.
>
>> "给定a=2, b=5计算轮廓系数。" → s = (5−2)/max(2,5) = 3/5 = **0.6**。"负轮廓系数意味着什么？" → 该点离其他簇比自己的簇更近 — 可能分配错误。"如何用轮廓系数选K？" → 对每个K运行聚类，计算平均轮廓，选最高值的K。
>>

---

## 8. 总结 (Summary)

![Page 50](week6_clustering_slides_pages/page_050.png)

| Category                     | Algorithm     | Key Property                                      |
| ---------------------------- | ------------- | ------------------------------------------------- |
| **Partition-based**    | K-Means       | Specify K, centroid-based, minimizes SSE          |
| **Density-based**      | DBSCAN        | ε + MinPts, arbitrary shapes, handles noise      |
| **Distribution-based** | EM            | Gaussian mixture, soft (probabilistic) assignment |
| **Hierarchical**       | Agglomerative | No K needed, dendrogram, various linkage methods  |

> **📝 Notes:**
>
> **⚖️ Compare:**
> The big picture — which algorithm to use when:
>
> - **K-Means:** Fast, scalable, spherical clusters, know K → default first choice
> - **DBSCAN:** Arbitrary shapes, noise present, don't know K → complex geometries
> - **EM:** Need soft assignments, data from mixture of Gaussians → probabilistic tasks
> - **Hierarchical:** Need to see structure at all levels, taxonomy → exploratory analysis
>
>> 全局比较 — 何时用哪个算法：
>>
>> - **K-Means：** 快速、可扩展、球形簇、知道K → 默认首选
>> - **DBSCAN：** 任意形状、有噪声、不知道K → 复杂几何
>> - **EM：** 需要软分配、数据来自混合高斯 → 概率任务
>> - **层次聚类：** 需要看所有层级结构、分类学 → 探索性分析
>>
>
> **📝 Exam:**
> "Compare 4 clustering algorithms covered in this lecture." Know: K-Means (partitional, SSE), DBSCAN (density, ε/MinPts), EM (distribution, soft), Hierarchical (dendrogram, linkage). Be ready to explain when each is appropriate.
>
>> "比较本讲涵盖的4种聚类算法。" 知道：K-Means（划分式、SSE）、DBSCAN（密度、ε/MinPts）、EM（分布、软分配）、层次聚类（树状图、链接法）。准备好解释每种何时适用。
>>

---
