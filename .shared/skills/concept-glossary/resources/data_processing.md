# Data Processing (数据处理)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

### CRISP-DM (跨行业数据挖掘标准流程)

**Tags:** `#data_processing` `#methodology` `#ml-week1`

**📌 Definition (定义):**

> CRoss-Industry Standard Process for Data Mining. An industry-proven methodology providing a structured, iterative approach to planning and executing data mining/ML projects through six phases.
>
> > 跨行业数据挖掘标准流程。一种经过行业验证的方法论，通过六个阶段为规划和执行数据挖掘/机器学习项目提供结构化的迭代方法。

**💡 Analogy (类比):**

> Like a recipe for cooking: Business Understanding (decide what to cook), Data Understanding (check ingredients), Data Preparation (wash/chop), Modeling (cook), Evaluation (taste), Deployment (serve). You often go back to adjust.
>
> > 像做菜的食谱：业务理解（决定做什么菜）、数据理解（检查食材）、数据准备（洗切）、建模（烹饪）、评估（品尝）、部署（上菜）。经常需要回头调整。

**⚠️ Common Mistake (常见错误):**

> Jumping straight to Modeling without proper Data Preparation — this is the #1 reason data science projects fail. 70-80% of time should be spent on data preparation.
>
> > 没有充分的数据准备就直接跳到建模——这是数据科学项目失败的首要原因。70-80%的时间应该花在数据准备上。

**📚 Appears In (出现课程):**

> - ML Week 1: Data Preprocessing and Dimensionality Reduction

---

### Normalization / Min-Max Scaling (归一化 / 最小-最大缩放)

**Tags:** `#data_processing` `#scaling` `#ml-week1`

**📌 Definition (定义):**

> A scaling technique that transforms continuous features to fall within a fixed range, typically [0, 1], by subtracting the minimum and dividing by the range.
>
> > 一种将连续特征值缩放到固定范围（通常是 [0, 1]）的技术，方法是减去最小值再除以全距。

**📐 Formula:**

> `x' = (x - x_min) / (x_max - x_min)`

**⚖️ Contrast (易混淆对比):**

> | Aspect         | Normalization (Min-Max)             | Standardization (Z-score)            |
> | -------------- | ----------------------------------- | ------------------------------------ |
> | Output range   | Fixed [0, 1]                        | Unbounded                            |
> | Outlier impact | ❌ Very sensitive                   | ✅ Robust                            |
> | When to use    | Neural network inputs, pixel values | Distance-based algorithms (kNN, PCA) |

**🔗 Related Concepts (关联概念):**

> → see: Standardization (Z-score) — alternative scaling method
> → see: Data Leakage (数据泄露) — must fit on train set only

**📚 Appears In (出现课程):**

> - ML Week 1: Data Preprocessing — Scaling

---

### Standardization / Z-score (标准化 / Z分数)

**Tags:** `#data_processing` `#scaling` `#ml-week1`

**📌 Definition (定义):**

> A scaling technique that transforms features to have mean 0 and standard deviation 1, expressing each value as "how many standard deviations from the mean."
>
> > 一种使特征均值为0、标准差为1的缩放方法，将每个值表示为"距离均值多少个标准差"。

**📐 Formula:**

> `z = (x - μ) / σ`

**⚠️ Common Mistake (常见错误):**

> Must fit on TRAINING set only, then transform both train and test. Fitting on the entire dataset causes data leakage.
>
> > 必须仅在训练集上 fit，然后 transform 训练集和测试集。在全部数据上 fit 会导致数据泄露。

**🔗 Related Concepts (关联概念):**

> → see: Normalization (归一化) — alternative scaling method
> → see: PCA (主成分分析) — requires standardization before applying

**📚 Appears In (出现课程):**

> - ML Week 1: Data Preprocessing — Scaling

---

### Curse of Dimensionality (维度灾难)

**Tags:** `#data_processing` `#dimensionality_reduction` `#ml-week1`

**📌 Definition (定义):**

> As the number of dimensions increases, the volume of the space increases exponentially, making data sparse and distance metrics meaningless — all points appear equidistant.
>
> > 随着维度数增加，空间体积呈指数级增长，导致数据稀疏且距离度量失去意义——所有点看起来等距。

**💡 Analogy (类比):**

> Placing 10 people in a 10m hallway — crowded. In a 10×10 room — some space. In a 10-dimensional hypercube (volume = 10 billion) — everyone is completely isolated and can't find each other.
>
> > 把10个人放在10米长走廊——挤。放在10×10的房间——有些空间。放在10维超立方体（体积100亿）——每个人完全孤立，找不到彼此。

**🔗 Related Concepts (关联概念):**

> → see: PCA (解决方案之一 — 无监督降维)
> → see: LDA (解决方案之一 — 有监督降维)
> → see: Euclidean Distance (在高维中失效)

**📚 Appears In (出现课程):**

> - ML Week 1: Dimensionality Reduction Overview

---

### PCA / Principal Component Analysis (主成分分析)

**Tags:** `#data_processing` `#dimensionality_reduction` `#ml-week1`

**📌 Definition (定义):**

> An unsupervised dimensionality reduction technique that finds orthogonal directions of maximum variance and projects data onto them, creating new synthetic features (principal components) as linear combinations of the original features.
>
> > 一种无监督降维技术，找到数据方差最大的正交方向，将数据投影上去，创建新的合成特征（主成分）作为原始特征的线性组合。

**📜 History (历史背景):**

> Invented by Karl Pearson in 1901 and independently developed by Harold Hotelling in 1933.
>
> > 由Karl Pearson在1901年发明，Harold Hotelling在1933年独立发展。

**💡 Analogy (类比):**

> Like photographing a UFO (flat saucer). From above (PC1), you see the big circular shape (most variance/info). From the side (PC2), just a thin line (less info). PCA rotates the camera to find the angle showing the most features.
>
> > 像拍飞碟（扁平碟形物体）。从正上方拍（PC1），看到大圆形轮廓（最大方差/信息量）。从侧面拍（PC2），只看到一条线（信息量少）。PCA就是旋转相机找到最能展现特征的角度。

**⚖️ Contrast (易混淆对比):**

> | Aspect         | PCA                     | LDA                       |
> | -------------- | ----------------------- | ------------------------- |
> | Supervised?    | ❌ No (ignores labels)  | ✅ Yes (requires labels)  |
> | Objective      | Maximize total variance | Maximize class separation |
> | Max components | min(samples, features)  | min(classes-1, features)  |
> | Type           | Feature Extraction      | Feature Extraction        |

**⚠️ Common Mistake (常见错误):**

> 1. Forgetting to standardize before PCA — features with large numeric values dominate
> 2. Confusing PCA with feature selection — PCA is feature extraction (creates new features)
>
> > 1. PCA前忘记标准化——数值大的特征会主导方向选择
> > 2. 把PCA和特征选择混淆——PCA是特征提取（创建新特征）

**🔗 Related Concepts (关联概念):**

> → see: LDA (有监督对应物)
> → see: Scree Plot (碎石图 — 确定保留主成分数)
> → see: Eigenvalues/Eigenvectors (PCA的核心数学工具)
> → see: Covariance Matrix (PCA的Step 2)

**📚 Appears In (出现课程):**

> - ML Week 1: Principal Component Analysis

---

### LDA / Linear Discriminant Analysis (线性判别分析)

**Tags:** `#data_processing` `#dimensionality_reduction` `#ml-week1`

**📌 Definition (定义):**

> A supervised dimensionality reduction technique that projects data onto a lower-dimensional space by maximizing class separability — maximizing between-class distance while minimizing within-class scatter.
>
> > 一种有监督降维技术，通过最大化类别可分性——最大化类间距离同时最小化类内分散——将数据投影到低维空间。

**💡 Analogy (类比):**

> Like sorting exam scores into "pass" and "fail" groups — you want the group averages as far apart as possible (maximize between-class), and each group's scores as similar as possible (minimize within-class).
>
> > 像把考试成绩分成"及格"和"不及格"两组——你希望两组的平均分尽可能远（最大化类间），同时每组内部的分数尽可能集中（最小化类内）。

**⚠️ Common Mistake (常见错误):**

> LDA can only reduce to at most (number_of_classes - 1) dimensions. For binary classification: only 1 dimension, regardless of input features.
>
> > LDA最多只能降到（类别数 - 1）维。二分类情况：无论输入多少特征，只能降到1维。

**🔗 Related Concepts (关联概念):**

> → see: PCA (无监督对应物)
> → see: Scatter Matrix (散布矩阵 — LDA的关键数学工具)

**📚 Appears In (出现课程):**

> - ML Week 1: Linear Discriminant Analysis

---
