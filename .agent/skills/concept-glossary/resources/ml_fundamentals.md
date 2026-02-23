# ML Fundamentals (机器学习基础)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

### Hard/Soft Margin (硬/软间隔)

**Tags:** `#ml_fundamentals` `#svm` `#ml-week2`

**📌 Definition (定义):**

> A margin rule in Support Vector Machines; "Hard" allows zero misclassifications in the training data, while "Soft" introduces slack variables allowing some errors to achieve a more robust overall boundary.
>
> > 支持向量机中的间隔规则；"硬"间隔不允许训练数据有任何误分类，而"软"间隔引入松弛变量允许部分错误，以获得更具鲁棒性的整体边界。

**📜 History (历史背景):**

> Soft margin was introduced by Corinna Cortes and Vladimir Vapnik in 1995 to handle real-world datasets inseparable by a strict linear hyperplane.
>
> > 软间隔由 Corinna Cortes 和 Vladimir Vapnik 在1995年提出，旨在处理现实世界中无法被严格线性超平面分离的数据集。

**💡 Analogy (类比):**

> Hard Margin is a referee who immediately disqualifies a team if anyone steps an inch over the line. Soft Margin is a referee who gives a yellow card (penalty cost) for minor steps over the line, keeping the game robust and flowing rather than ending it over noise.
>
> > 硬间隔就像一个裁判在任何人越界哪怕一英寸时立即剥夺队伍资格。软间隔是给轻微越界一张黄牌（惩罚代价），保持比赛稳健流畅，而不是因为一点噪声就结束比赛。

**🔗 Related Concepts (关联概念):**

> → see: Support Vector Machine (支持向量机) — context of the margin
> → see: Regularization Parameter C (惩罚系数 C) — controls how "soft" the margin is

**📚 Appears In (出现课程):**

> - ML Week 2: Support Vector Machines

---

### Bayesian Belief Network / BBN (贝叶斯信念网络)

**Tags:** `#ml_fundamentals` `#probabilistic` `#ml-week5`

**📌 Definition (定义):**

> A probabilistic graphical model using a directed acyclic graph (DAG) to represent conditional dependencies among a set of random variables, with each node having a conditional probability table (CPT).
>
> > 一种概率图模型，使用有向无环图 (DAG) 表示一组随机变量之间的条件依赖关系，每个节点有一个条件概率表 (CPT)。

**💡 Analogy (类比):**

> Like a family tree for variables. Parents directly influence children. If you know your parents' traits, knowing your grandparents' gives no additional info (conditional independence given parents).
>
> > 像变量的家族树。父母直接影响子女。如果你知道父母的特征，知道祖父母不会提供额外信息（给定父母的条件独立）。

**🔗 Related Concepts (关联概念):**

> → see: Naïve Bayes (朴素贝叶斯) — special case of BBN with star-shaped DAG
> → see: Bayes' Theorem (贝叶斯定理) — foundation for BBN inference

**📚 Appears In (出现课程):**

> - ML Week 5: Bayesian Classifier — Naïve Bayes & BBN

---

### Kernel Trick (核技巧)

**Tags:** `#ml_fundamentals` `#svm` `#ml-week2`

**📌 Definition (定义):**

> A mathematical shortcut that computes the dot product of two vectors in a high-dimensional feature space directly from their original low-dimensional coordinates, allowing non-linear classification without the computational cost of explicit mapping.
>
> > 一种数学捷径，直接利用原始低维坐标计算两个向量在高维特征空间中的点积，在不产生显式映射计算成本的情况下实现非线性分类。

**📜 History (历史背景):**

> First applied to Support Vector Machines by Bernhard Boser, Isabelle Guyon and Vladimir Vapnik in 1992.
>
> > 在1992年由 Bernhard Boser, Isabelle Guyon 和 Vladimir Vapnik 首次应用于支持向量机中。

**💡 Analogy (类比):**

> Imagine trying to compute how far apart two cities are in a 3D globe coordinate system using only flat 2D maps. The Kernel Trick is like a magic formula giving you the exact 3D distance purely by doing math on their 2D flat-map coordinates, saving the effort of building a 3D globe.
>
> > 想象仅凭平面2D地图来计算两座城市在3D地球上的距离。核技巧就像一个能在2D地图上计算并直接给出准确3D距离的神奇公式，省了造一个立体地球仪的麻烦。

**🔗 Related Concepts (关联概念):**

> → see: Support Vector Machine (支持向量机) — primary algorithm using kernels

**📚 Appears In (出现课程):**

> - ML Week 2: Non-linear SVM

---

### Naïve Bayes Classifier (朴素贝叶斯分类器)

**Tags:** `#ml_fundamentals` `#probabilistic` `#ml-week5`

**📌 Definition (定义):**

> A probabilistic classifier based on Bayes' theorem with the "naïve" assumption that all attributes are conditionally independent given the class label. Despite this unrealistic assumption, it performs surprisingly well in practice, especially for text classification.
>
> > 基于贝叶斯定理的概率分类器，带有"朴素"假设：给定类别标签后所有属性条件独立。尽管这个假设不现实，但实际表现出奇地好，尤其在文本分类中。

**💡 Analogy (类比):**

> Like independent dice rolls. Once you know the class (which "game" you're playing), each attribute is like rolling its own dice — the results don't affect each other.
>
> > 像独立骰子投掷。一旦知道类别（在玩哪个"游戏"），每个属性就像掷自己的骰子——结果互不影响。

**🔗 Related Concepts (关联概念):**

> → see: Bayes' Theorem (贝叶斯定理) — theoretical foundation
> → see: Laplace Smoothing (拉普拉斯平滑) — fixes zero probability issue
> → see: Bayesian Belief Network (贝叶斯信念网络) — general case allowing dependencies

**⚖️ Contrast (易混淆对比):**

> | Aspect        | Naïve Bayes   | BBN           | SVM         |
> | ------------- | ------------- | ------------- | ----------- |
> | Approach      | Probabilistic | Probabilistic | Geometric   |
> | Independence? | ✅ Full       | Partial       | N/A         |
> | Output        | Probabilities | Probabilities | Hard labels |
> | Speed         | ✅ Very fast  | Moderate      | Slow        |

**📚 Appears In (出现课程):**

> - ML Week 5: Bayesian Classifier — Naïve Bayes

---

### Recurrent Neural Network / RNN (循环神经网络)

**Tags:** `#ml_fundamentals` `#deep_learning` `#rnn`

**📌 Definition (定义):**

> A type of artificial neural network where connections between nodes can create a cycle, allowing output from some nodes to affect subsequent input to the same nodes, thus maintaining an internal state (memory).
>
> > 一种人工神经网络，其中节点之间的连接可以形成循环，允许某些节点的输出影响同一节点的后续输入，从而维持内部状态（记忆）。

**💡 Analogy (类比):**

> FNN is like a camera taking snapshots; RNN is like a video camera. You understand the current scene because you remember the previous frames.
>
> > FNN 就像相机拍摄快照；RNN 就像摄像机。你理解当前的场景是因为你记住了之前的画面。

**🔗 Related Concepts (关联概念):**

> → see: LSTM (长短期记忆网络) — advanced variant solving vanishing gradients
> → see: BPTT (随时间反向传播) — training algorithm

---

### Support Vector Classifier / SVC (支持向量分类器)

**Tags:** `#ml_fundamentals` `#svm` `#ml-week2`

**📌 Definition (定义):**

> An extension of the Maximum Margin Classifier that uses a soft margin and linear kernel, allowing some misclassifications to better generalize on overlapping data.
>
> > 最大间隔分类器的扩展，它使用软间隔和线性核，通过允许小部分误分类来在重叠数据上获得更好的泛化能力。

**💡 Analogy (类比):**

> It's an MMC but with a tolerance for noisy outliers trying to cross the street.
>
> > 它是具有对横穿街道的噪声孤立点具备容忍度的纯线性限制版本MMC。

**🔗 Related Concepts (关联概念):**

> → see: Maximum Margin Classifier (最大间隔分类器) — strict predecessor
> → see: Support Vector Machine (支持向量机) — non-linear successor

**📚 Appears In (出现课程):**

> - ML Week 2: Support Vector Machines

---

### Support Vector Machine / SVM (支持向量机)

**Tags:** `#ml_fundamentals` `#svm` `#ml-week2`

**📌 Definition (定义):**

> A supervised machine learning algorithm that finds an optimal hyperplane with the maximum margin between classes, utilizing a combination of soft margins and the kernel trick for non-linear decision boundaries.
>
> > 一种在类别之间找到具有最大间隔的最优超平面的监督学习算法，它综合利用了软间隔和核技巧来处理非线性决策边界。

**📜 History (历史背景):**

> Originally invented by Vladimir Vapnik and Alexey Chervonenkis in 1963 (linear MMC); the modern standard Soft-Margin + Kernel SVM was published in 1995 (Cortes & Vapnik). It dominated ML until Deep Learning took over around 2012.
>
> > 最初由 Vladimir Vapnik 和 Alexey Chervonenkis 于1963年发明(线性MMC)；现代标准的软间隔+核技巧SVM发表于1995年(Cortes & Vapnik)。在深度学习(2012年左右)崛起前统治了机器学习领域。

**💡 Analogy (类比):**

> Imagine trying to lay down a multi-lane highway between two different species of trees in a forest. You want to build the widest possible road without knocking any trees down, even if the forest is curved or hilly.
>
> > 想象你要在森林里的两种不同树木之间铺设多车道高速公路。即使森林地形弯曲崎岖，你也想在不撞倒任何一棵树的前提下修筑最宽的马路。

**🔗 Related Concepts (关联概念):**

> → see: Kernel Trick (核技巧) — key part of SVM for non-linear data
> → formula: Maximum Margin Classifier Optimization in math-concept-library

**⚖️ Contrast (易混淆对比):**

> | Term | Margin Rules | Kernel Used |
> | ---- | ------------ | ----------- |
> | MMC  | Hard Margin  | Linear      |
> | SVC  | Soft Margin  | Linear      |
> | SVM  | Soft Margin  | Non-linear  |

**📚 Appears In (出现课程):**

> - ML Week 2: Support Vector Machines

---

### Support Vectors (支持向量)

**Tags:** `#ml_fundamentals` `#svm` `#ml-week2`

**📌 Definition (定义):**

> The subset of training data points that lie closest to the decision boundary and alone dictate its position and orientation; moving them shifts the margin entirely.
>
> > 训练数据中最靠近决策边界的一个子集，它们全权决定了边界的位置和方向；移动这些点会导致整个间隔偏移。

**💡 Analogy (类比):**

> Like pillars supporting a roof or walls bounding a street. The houses far away from the street don't influence where the street borders are drawn. You can tear them down and the street remains perfectly identical.
>
> > 就像支撑屋顶的柱子或界定街道边界的墙壁。远离街道的房子并不影响街道边界的画法。你把遥远的房子拆了，街道也保持完全一致。

**🔗 Related Concepts (关联概念):**

> → see: Support Vector Machine (支持向量机) — algorithm based on them
> → see: Hard/Soft Margin (硬/软间隔) — what they support

**📚 Appears In (出现课程):**

> - ML Week 2: Support Vector Machines

---

### Time Series (时间序列)

**Tags:** `#ml_fundamentals` `#forecasting`

**📌 Definition (定义):**

> A series of data points indexed (or listed or graphed) in time order, typically consisting of four components: Trend, Seasonal, Cycle, and Noise.
>
> > 按时间顺序索引（或列出或绘图）的一系列数据点，通常由四个部分组成：趋势、季节性、周期和噪声。

**💡 Analogy (类比):**

> Like a physical diary. Each entry's meaning depends heavily on what was written the day before.
>
> > 就像一本实体日记。每一条记录的含义很大程度取决于前一天写了什么。

**🔗 Related Concepts (关联概念):**

> → see: Trend (趋势) — long-term direction
> → see: Seasonal (季节性) — repeating patterns in fixed intervals

**📚 Appears In (出现课程):**

> - ML Week 4: Time Series Forecasting

---

### K-Means Clustering (K-Means 聚类)

**Tags:** `#ml_fundamentals` `#clustering` `#unsupervised` `#ml-week6`

**📌 Definition (定义):**

> A partitional clustering algorithm that divides data into K non-overlapping groups by iteratively assigning points to the nearest centroid and recomputing centroids until convergence. Minimizes SSE (Sum of Squared Errors).
>
> > 一种划分式聚类算法，通过迭代地将点分配到最近的质心并重新计算质心直到收敛，将数据分为K个不重叠的组。最小化SSE（误差平方和）。

**💡 Analogy (类比):**

> Like placing K magnets on a table of iron filings. Each filing goes to the nearest magnet. Then move each magnet to the center of its filings. Repeat until magnets stabilize.
>
> > 像在铁屑桌上放K块磁铁。每个铁屑被最近的磁铁吸引。然后把磁铁移到铁屑中心。重复直到磁铁稳定。

**⚠️ Common Mistake (常见错误):**

> "Convergence" only means centroids stopped moving — NOT that you found the global optimum. K-Means always converges, but may converge to a bad local minimum. Run multiple times (n_init=10) and pick the lowest SSE.
>
> > "收敛"只意味着质心停止移动——不意味着找到了全局最优。K-Means总是收敛，但可能收敛到差的局部最小值。运行多次(n_init=10)，选最低SSE。

**📚 Appears In (出现课程):**

> - ML Week 6: K-Means Clustering

---

### DBSCAN (基于密度的聚类)

**Tags:** `#ml_fundamentals` `#clustering` `#unsupervised` `#ml-week6`

**📌 Definition (定义):**

> Density-Based Spatial Clustering of Applications with Noise. Discovers clusters as dense regions separated by sparse regions. Uses two parameters: ε (neighborhood radius) and MinPts (density threshold). Automatically detects number of clusters and identifies noise points.
>
> > 带噪声的基于密度的空间聚类。将密集区域发现为簇，被稀疏区域分隔。使用两个参数：ε（邻域半径）和MinPts（密度阈值）。自动检测簇数并识别噪声点。

**⚖️ Contrast (易混淆对比):**

> | Feature        | K-Means        | DBSCAN             |
> | -------------- | -------------- | ------------------ |
> | Specify K?     | Yes (required) | No (auto-detected) |
> | Cluster shape  | Spherical only | Any shape          |
> | Noise handling | None           | Built-in           |

**⚠️ Common Mistake (常见错误):**

> Core point definition "includes itself": with MinPts=4, a point with 3 neighbors (plus itself = 4) IS a core point. Exam trap!
>
> > 核心点定义"包括自身"：MinPts=4时，有3个邻居的点（加上自身=4）是核心点。考试陷阱！

**📚 Appears In (出现课程):**

> - ML Week 6: DBSCAN

---

### Hierarchical Clustering (层次聚类)

**Tags:** `#ml_fundamentals` `#clustering` `#unsupervised` `#ml-week6`

**📌 Definition (定义):**

> Creates nested clusters organized as a tree (dendrogram). Agglomerative (bottom-up) starts with each point as its own cluster and merges the closest pairs. No need to specify K in advance — choose K by cutting the dendrogram at the desired level.
>
> > 创建组织为树（树状图）的嵌套簇。凝聚式（自底向上）从每个点自成一簇开始，合并最近的对。不需要预先指定K——通过在所需层级切割树状图来选择K。

**💡 Analogy (类比):**

> Like building a family tree from individuals. Find the most similar pair → merge into a family → families into clans → clans into tribes. The dendrogram records this entire process.
>
> > 像从个人构建家族树。找到最相似的一对→合并成家庭→家庭合并为宗族→宗族合并为部落。树状图记录整个过程。

**📚 Appears In (出现课程):**

> - ML Week 6: Hierarchical Clustering

---

### EM / Gaussian Mixture Model (EM / 高斯混合模型)

**Tags:** `#ml_fundamentals` `#clustering` `#unsupervised` `#ml-week6`

**📌 Definition (定义):**

> The Expectation-Maximization algorithm for Gaussian Mixture Models performs soft clustering by modeling data as a mixture of Gaussian distributions. E-step computes posterior membership probabilities; M-step re-estimates parameters (μ, σ², mixing weights). K-Means is its special case (hard assignment with equal fixed variances).
>
> > 高斯混合模型的期望最大化算法通过将数据建模为高斯分布的混合来执行软聚类。E步计算后验隶属概率；M步重新估计参数(μ, σ², 混合权重)。K-Means是其特殊情况（等方差固定时的硬分配）。

**⚖️ Contrast (易混淆对比):**

> | Feature       | K-Means                   | EM (GMM)                        |
> | ------------- | ------------------------- | ------------------------------- |
> | Assignment    | Hard (0 or 1)             | Soft (probabilities)            |
> | Cluster model | Centroid only             | Full Gaussian (μ, σ², weight)   |
> | Cluster shape | Spherical, equal variance | Elliptical, different variances |
> | Relationship  | Special case of EM        | Generalization of K-Means       |

**📚 Appears In (出现课程):**

> - ML Week 6: Distribution-based Clustering (EM)

---
