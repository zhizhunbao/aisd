# Week 2: 支持向量机 (Support Vector Machines)

> Source: `02_CST8506_SVM4.pdf`
> Total slides: 25
> Instructor: Dr. Anu Thomas

---

## 1. 线性分离器与分类间隔 (Linear Separators and Classification Margin)

### 1.1 线性分离器示例 (Linear Separator Examples)

![Page 2](week2_svm_slides_pages/page_002.png)

**Linear Separator Examples:** Scatter plot showing three different linear lines (red, green, blue) that all successfully separate blue from red dots in 2D space.

**线性分离器示例：** 散点图显示了三条不同的直线（红、绿、蓝），它们都在2D空间中成功地将蓝点与红点分开了。

### 1.2 最佳分离器 (Optimal Separator)

![Page 3](week2_svm_slides_pages/page_003.png)

**Optimal Separator:** The green line is highlighted as the optimal separator because it runs exactly down the middle of the empty space between the two classes.

**最佳分离器：** 绿线被突出显示为最佳分离器，因为它恰好穿过两个类别之间空白区域的正中间。

### 1.3 分类间隔概念 (Classification Margin Idea)

![Page 4](week2_svm_slides_pages/page_004.png)

**Classification Margin Idea:** Shows the empty "street" or margin space between the classes, bounded by dashed lines parallel to the decision boundary.

**分类间隔概念：** 展示了类别之间空白的"街道"或边界空间，由平行于决策边界的虚线限定。

### 1.4 支持向量 (Support Vectors)

![Page 5](week2_svm_slides_pages/page_005.png)

**Support Vectors marked:** Specific data points touching the dashed boundary lines are circled. These points dictate the width of the margin.

**标记支持向量：** 接触虚线边界的特定数据点被圈出。这些点决定了间隔的宽度。

- Support vectors marked in circle — 圈出的点即为支持向量

### 1.5 间隔定义 (Margin Definition)

![Page 6](week2_svm_slides_pages/page_006.png)

**Margin Definition:** Visual representation of distance $d$ from the hyperplane to the nearest support vectors on both sides.

**间隔定义：** 直观展示了从超平面到两侧最近支持向量的距离 $d$。

- **Classification Margin:** Distance between the hyperplane and the vectors closest to the hyperplane (support vectors) — **分类间隔：** 超平面与距离超平面最近的向量（支持向量）之间的距离


---

## 2. 支持向量与 SVM 简介 (Support Vectors and Introduction to SVM)

### 2.1 支持向量总结 (Support Vector Summary)

![Page 7](week2_svm_slides_pages/page_007.png)

**Support Vector Summary:** Slide providing the text definition of support vectors and their role in margin maximization.

**支持向量总结：** 幻灯片提供了支持向量的文本定义及其在最大化间隔中的作用。

- Vectors (data points) that : — 向量（数据点）：
  - Are closer to the hyperplane — 更靠近超平面
  - Can influence the position and the orientation of the hyperplane — 能够影响超平面的位置和方向
- Using the support vectors, we maximize the classification margin — 利用支持向量，我们最大化分类间隔

### 2.2 SVM 算法定义 (SVM Algorithm Definitions)

![Page 8](week2_svm_slides_pages/page_008.png)

**SVM Algorithm Definitions:** Slide detailing SVM's goal to find a distinct hyperplane in n-dimensional space. Mentions shape based on dimension.

**SVM算法定义：** 幻灯片详细说明了SVM试图在n维空间中寻找清晰的超平面的目标。提到了基于形状的维度。

- **Objective:** find a hyperplane in an n-dimensional space (n is the number of features) that has the maximum margin (that can distinctly classify the instances) — **目标：** 在n维空间（n是特征数量）中找到一个具有最大间隔的超平面（能够清晰地分类实例）
- If n is 1, classifier will be a dot — 如果 n 是 1，分类器将是一个点
- If n is 2, classifier will be a line — 如果 n 是 2，分类器将是一条线
- If n is 3, classifier will be a 2d plane — 如果 n 是 3，分类器将是一个2D平面
- If n>3, classifier will be a hyperplane in the n-dimensional space — 如果 n > 3，分类器将是n维空间中的超平面
- SVM is a supervised algorithm that works best on small complex datasets. — SVM 是一种监督学习算法，在小型复杂数据集上效果最好。
- SVM can be used for classification and regression tasks but generally used more for classification. — SVM 可用于分类和回归任务，但通常更多用于分类。


---

## 3. 数学基础与优化目标 (Math Foundation and Optimization Function)

### 3.1 预测新点图示 (Predicting a New Point Diagram)

![Page 9](week2_svm_slides_pages/page_009.png)

**Predicting a New Point Diagram:** A question showing the established hyperplane and asking how to algorithmically classify a new, unknown black point (vector $u$).

**预测新点图示：** 提出了一个问题，展示已建立的超平面，并询问如何用算法对一个新出现的、未知的黑点（向量 $u$）进行分类。

### 3.2 点积投影 (Dot Product Projection)

![Page 10](week2_svm_slides_pages/page_010.png)

**Dot Product Projection:** Shows mathematically how classifying a new vector $x$ works by taking the dot product with the weight vector $w$ (which is perpendicular to the boundary) and checking if the value exceeds a threshold.

**点积投影：** 从数学上展示了如何对新向量 $x$ 进行分类，即通过将其与权重向量 $w$（垂直于边界）做点积，并检查结果是否超过某个阈值。

- Vector **w** is perpendicular to the green line. The projection of any vector or another vector is called **dot-product**. — 向量 $w$ 垂直于绿线。投影或两个向量的运算被称为**点积**。
- Vector **x** is projected on vector **w**. — 向量 $x$ 被投影到向量 $w$ 上。
- If $w \cdot x \geq c$, it falls on the right of the line (positive class, $y=+1$) — 如果 $w \cdot x \geq c$，它落在直线的右侧（正类，$y=+1$）
- If $w \cdot x < c$, it falls on the left of the line (negative class, $y=-1$) — 如果 $w \cdot x < c$，它落在直线的左侧（负类，$y=-1$）

### 3.3 超平面方程 (Hyperplane Equation)

![Page 11](week2_svm_slides_pages/page_011.png)

**Hyperplane Equation:** Derives the functional margin and defines the canonical hyperplane using a bias term $b$.

**超平面方程：** 推导了函数间隔，并使用偏置项 $b$ 定义了规范超平面。

- We need to find a w and b for the hyperplane such that the margin d is maximum. — 我们需要为超平面找到 $w$ 和 $b$，以使得间隔 $d$ 最大。
- Let rule be $w \cdot x + b \ge 0$ (for positive) and $w \cdot x + b < 0$ (for negative). — 设规则为 $w \cdot x + b \ge 0$ (正类) 以及 $w \cdot x + b < 0$ (负类)。

### 3.4 正负间隔 (Positive and Negative Margins)

![Page 12](week2_svm_slides_pages/page_012.png)

**Positive and Negative Margins:** Shows how the margin boundary constraints are set to +1 and -1.

**正负间隔：** 展示了如何将间隔边界约束设定为 +1 和 -1。

- Let's consider blue points as +1 and red points as -1. — 设蓝点标号为 +1，红点为 -1。
- For blue points: $w \cdot x + b \ge 1$ — 对于蓝点：$w \cdot x + b \ge 1$
- For red points: $w \cdot x + b \le -1$ — 对于红点：$w \cdot x + b \le -1$
- Combined constraint: $y_i (w \cdot x_i + b) \ge 1$ — 综合约束条件：$y_i (w \cdot x_i + b) \ge 1$

### 3.5 超平面之间的距离 (Distance Between Hyperplanes)

![Page 13](week2_svm_slides_pages/page_013.png)

**Distance Between Hyperplanes:** The mathematical calculation of total margin distance is shown to be $2 / ||w||$.

**超平面之间的距离：** 总间隔距离的数学计算过程显示为 $2 / ||w||$。

- Distance between two parallel hyperplanes is $2/||w||$. — 两个平行超平面之间的距离是 $2/|w|$。
- Euclidean norm (||w||) measures the "length" or "magnitude" of a vector in Euclidean space. — 欧几里德范数 ($||w||$) 衡量了向量在欧氏空间中的"长度"或"幅度"。

### 3.6 MMC 优化约束 (MMC Optimization Constraints)

![Page 14](week2_svm_slides_pages/page_014.png)

**MMC Optimization constraints:** States the formal goal of Maximum Margin Classifier: maximize margin size subject to no misclassifications.

**MMC优化约束：** 声明了最大间隔分类器的正式目标：在不允许错分的前提下最大化间隔大小。

- The goal when training an SVM is: — 训练SVM时的目标是：
  - Maximize $\frac{2}{||w||}$ — 最大化 $\frac{2}{||w||}$
  - Subject to the constraint: $y_i (w \cdot x_i + b) \ge 1$ — 满足约束条件：$y_i (w \cdot x_i + b) \ge 1$
- This method is called Maximum Margin Classifier (MMC). — 这种方法称为最大间隔分类器（MMC）。


---

## 4. 软间隔与支持向量分类器 (Soft Margin and Support Vector Classifier)

### 4.1 SVM 类型 (Types of SVM)

![Page 15](week2_svm_slides_pages/page_015.png)

**Types of SVM:** Briefly differentiates Linear SVMs (hard data split) from Non-linear SVMs (where straight lines fail).

**SVM 类型：** 简要区分了线性SVM（硬分离数据）和非线性SVM（直线无法分离时）。

- **Linear SVM (LSVM)** – when the data is linearly separable — **线性SVM (LSVM)** – 当数据是线性可分的
- **Non-linear SVM** – data cannot be separated into 2 classes using a straight line. — **非线性SVM** – 数据无法用一条直线被分成两个类别。

### 4.2 不可分数据 (Inseparable Classes)

![Page 16](week2_svm_slides_pages/page_016.png)

**Inseparable Classes (SVC):** Demonstrates real-world overlapping data and the need for a Soft Margin approach.

**不可分数据 (SVC)：** 展示了现实世界中重叠交叉的数据，引出对软间隔方法的需求。

- When the data is not separable we cannot separate them with linear classifiers. — 当数据不可分离时，我们无法用线性分类器将它们分开。
- We need to use **soft-margin** instead of hard margin – by allowing a few misclassifications. — 我们需要使用**软间隔**而不是硬间隔——即允许少量的错误分类。
- This method is called **Support Vector Classifier (SVC)**. — 这种方法称为**支持向量分类器 (SVC)**。


---

## 5. 核函数与非线性 SVM (Kernels and Non-linear SVM)

### 5.1 低维数据转换 (Transforming low-dimensional data)

![Page 17](week2_svm_slides_pages/page_017.png)

**Transforming low-dimensional data:** Shows concentric circle data projected up into a 3D bowl shape to make a flat 2D plane cut through them perfectly.

**低维数据转换：** 展示了原本呈同心圆分布的不可分集被向上投影成3D碗状形态，使得一个平坦的2D切面可以完美地将两类数据分开。

- When the data is not separable like this, we cannot separate them with linear classifiers. — 当数据像这样不可分时，我们无法用线性分类器分开。
- We need to transform the low-dimensional data into a higher dimensional space, but this is computationally expensive. — 我们需要将低维数据转换到更高维的空间，但这在计算上非常昂贵。
- We can achieve similar results using **kernels**. — 我们可以使用**核函数**实现类似结果。

### 5.2 核函数定义 (Kernel Definition)

![Page 18](week2_svm_slides_pages/page_018.png)

**Kernel Definition:** Defines Kernels as shortcut equations computing similarities, and lists Polynomial, RBF, and Sigmoid.

**核函数定义：** 将核函数定义为计算相似度的捷径公式，列出了多项式、RBF和Sigmoid核。

- **Kernel** is a function that quantifies the similarities between observations by summarizing the relationship between every instance in the dataset. — **核** 是一个函数，它通过总结数据集中每个实例之间的关系来量化观测值之间的相似性。
- This will transform data into higher dimensions without going into higher dimensions by **computing dot products** in a high-dimensional feature space without explicitly mapping the data to that space. — 它能在不升维的情况下降数据转换为高维关系。它通过在高维特征空间中直接**计算点积**来实现，而无需隐式或显式地将数据真正映射上去。
- 1. **Polynomial:** generalized form of linear kernel. Useful for non-linear hyperplane. — **1. 多项式核：** 线性核的推广形式。对非线性超平面有用。
- 2. **Radial Basis Function (Gaussian):** can map an input space to infinite dimensional space (widely used) — **2. 径向基函数 (RBF)：** 能将输入空间映射到无限维空间（非常常用）
- 3. **Sigmoid:** rarely used, sometimes, works for specific datasets — **3. Sigmoid核：** 很少使用，有时在特定数据集上有效

### 5.3 线性核 vs RBF核 示例 (Linear vs RBF Example)

![Page 19](week2_svm_slides_pages/page_019.png)

**Linear vs RBF Example:** Comparing a straight-line cut (Linear Kernel) failing on concentric data vs a circular blob cut (RBF Kernel) succeeding.

**线性核 vs RBF核 示例：** 在同心圆数据上，对比了一条直线切割（线性核）失败，而RBF核能成功切出环状面。

### 5.4 线性核 vs 多项式核 示例1 (Linear vs Polynomial Example 1)

![Page 20](week2_svm_slides_pages/page_020.png)

**Linear vs Polynomial (Left image):** Another plot demonstrating how a Polynomial curve can contour around data that a straight linear cut entirely misses.

**线性核 vs 多项式核 (示例1)：** 进一步图解多项式曲线可以如何包裹紧贴直切线根本覆盖不到的数据。

### 5.5 线性核 vs 多项式核 示例2 (Linear vs Polynomial Example 2)

![Page 21](week2_svm_slides_pages/page_021.png)

**Linear vs Polynomial Example (Right image):** Further proof of non-linear flexibility.

**线性核 vs 多项式核 (示例2)：** 进一步验证非线性灵活度的例子。


---

## 6. SVM 变体与重要超参数 (SVM Types and Important Parameters)

### 6.1 MMC vs SVC vs SVM 总结 (MMC vs SVC vs SVM Summary)

![Page 22](week2_svm_slides_pages/page_022.png)

**MMC vs SVC vs SVM Summary:** A cheat-sheet list summarizing what separates the 3 naming conventions based on margin rules and kernels.

**MMC vs SVC vs SVM 总结：** 速查清单，根据间隔宽容规则和核的使用，区分了三大名称的不同之处。

- **Maximum margin Classifier (MMC)** – with **hard** margin — 最大间隔分类器（MMC）– 使用**硬**间隔（不允许错误）
- **Support Vector Classifier (SVC)** – with **soft** margin and linear kernel — 支持向量分类器（SVC）– 使用**软**间隔（允许错误） + 线性核
- **Support Vector Machine (SVM)** – SVC + **non-linear** kernel — 支持向量机（SVM）– SVC + **非线性**核函数（终极完全体）

### 6.2 C 和 Gamma 的参数意义 (C and Gamma Parameters)

![Page 23](week2_svm_slides_pages/page_023.png)

**C and Gamma Parameters:** Explains the impact of tuning Regularization $C$ and the area of influence Gamma ($\gamma$).

**C 和 Gamma 的参数意义：** 解释了调节正则化系数 $C$ 和影响范围参数 $\gamma$ 所带来的表现变化。

- **C** – (inversely proportional to the Regularization parameter) — **C** – （与正则化参数成反比）
  - represents the acceptable amount of misclassification or error. — 表示可接受的错误分类或误差数量。
  - A **smaller C** value (high regularization) creates a wider margin hyperplane, allows more misclassifications (large margin - high misclassifications) — 较小的 **C** 值（强正则化）产生更宽间隔的超平面，允许更多的误分类。
  - **larger value** creates small-margin hyperplane (forcing the algorithm to classify every training point correctly. Larger value of C can cause overfitting). — 较大值会产生极窄的硬边界（迫使算法将每个训练点正确分类。C 值过大容易导致极度过拟合）。
- **Gamma** – factor that control how the model fit on the training data. — **Gamma** – 控制模型拟合训练数据程度的因素。
  - **Lower value:** loosely fit the train data, more data points will influence the decision boundary. decision boundary will be more generic (may cause underfitting) — 较小值：松散拟合数据，较多数据点影响边界，可能欠拟合。
  - **Higher value:** fewer data points will influence the decision boundary. So, this may cause overfitting — 较高值：少数孤立点会极大地影响决策边界收缩（就像高斯孤岛）。极易过拟合。


---

## 7. 优缺点概览 (Advantages & Disadvantages)

![Page 24](week2_svm_slides_pages/page_024.png)

**Advantages & Disadvantages:** Final summary showing why SVM is still used today (high dimensional spaces) and why it's avoided on big data.

**优缺点综述：** 结尾总结，展示了为何SVM至今仍在高维空间中有使用价值，以及为什么在大数据时代我们要避开它。

- **Advantages** — **优点**
  - High accuracy, faster prediction — 高准确度，预测快（推理阶段）
  - **Memory efficient** — 在内存中非常高效
  - Works well if the dataset is small, classes separable — 如果数据集很小，类别可分，效果特别好
  - **Effective in high-dimensional space** — 处理极高维空间非常有效
  - Effective when number of dimensions greater than the number of instances — 甚至在特征维度比实际可用样本数据还要多的时候仍然非常有效！
  - Variety of kernel functions — 可切换多种核函数来应对各种复杂的分布
- **Disadvantages** — **缺点**
  - **Not suitable for larger datasets** — 完全不适合大规模或百万级数据集
  - Poor performance on overlapping classes — 如果类分布严重重叠交融无边界，效果极差
  - Highly sensitive to the type of kernel — 极其依赖你选择对了哪个核并调优好了其专属超参数


---

## 8. 参考文献 (References)

![Page 25](week2_svm_slides_pages/page_025.png)

- https://towardsdatascience.com/support-vector-machine-introduction-to-machine-learning-algorithms-934a444fca47
- https://www.analyticsvidhya.com/blog/2021/10/support-vector-machinessvm-a-complete-guide-for-beginners/
- https://towardsdatascience.com/hyperparameter-tuning-for-support-vector-machines-c-and-gamma-parameters-6a5097416167/
- https://www.geeksforgeeks.org/machine-learning/gamma-parameter-in-svm/
