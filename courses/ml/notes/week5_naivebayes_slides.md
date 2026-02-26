# Week 5: 朴素贝叶斯分类器 (Naïve Bayes Classifier)

> Source: `Week5_NaiveBayes.pdf`
> Total slides: 28
> Instructor: Dr. Abbas Akkasi | Winter 2026

---

## 1. 课程概览 (Course Overview)

![Page 1](week5_naivebayes_slides_pages/page_001.png)

**Title slide:** CST8506 – Advanced Machine Learning, Week 5: Bayesian Classifier - Naïve Bayes. Adapted from materials originally developed by Pang-Ning Tan on his Data Mining Course.

**标题页：** CST8506 – 高级机器学习，第5周：贝叶斯分类器 - 朴素贝叶斯。改编自 Pang-Ning Tan 的数据挖掘课程材料。

![Page 2](week5_naivebayes_slides_pages/page_002.png)

**Agenda slide:** Two main topics — Naïve Bayes Model and Bayesian Belief Network.

**议程页：** 两个主题 — 朴素贝叶斯模型和贝叶斯信念网络。

- **Naïve Bayes Model** — 朴素贝叶斯模型
- **Bayesian Belief Network** — 贝叶斯信念网络


---

## 2. 贝叶斯分类器基础 (Bayes Classifier Foundations)

### 2.1 条件概率与贝叶斯定理 (Conditional Probability & Bayes Theorem)

![Page 3](week5_naivebayes_slides_pages/page_003.png)

**Bayes Classifier slide:** Shows conditional probability formula and Bayes theorem with labeled components (Posterior, Prior, Evidence).

**贝叶斯分类器页：** 展示条件概率公式和贝叶斯定理，标注了各组成部分（后验、先验、证据）。

- A **probabilistic framework** for solving classification problems — 用于解决分类问题的**概率框架**
- **Conditional Probability:** P(Y|X) = P(X, Y) / P(X) — **条件概率：** P(Y|X) = P(X, Y) / P(X)
- **Bayes theorem:** P(Y|X) = P(X|Y) × P(Y) / P(X) — **贝叶斯定理：** P(Y|X) = P(X|Y) × P(Y) / P(X)
  - P(Y|X) = **Posterior** (后验概率)
  - P(X|Y) = **Likelihood** (似然)
  - P(Y) = **Prior** (先验概率)
  - P(X) = **Evidence** (证据)

### 2.2 条件概率示例 (Conditional Probability Example)

![Page 4](week5_naivebayes_slides_pages/page_004.png)

**Dice example:** When rolling 2 dice, find P(A|B) where A = sum is 8, B = first die shows 5.

**骰子示例：** 掷两个骰子，求 P(A|B)，其中 A = 两骰子之和为8，B = 第一个骰子为5。

- Possible outcomes for A: {(2,6), (3,5), (4,4), (5,3), (6,2)} → P(A) = 5/36
- Possible outcomes for B: {(5,1), (5,2), (5,3), (5,4), (5,5), (5,6)} → P(B) = 6/36
- P(A∩B) = 1/36 (only (5,3))
- P(A|B) = P(A∩B) / P(B) = (1/36) / (6/36) = **1/6**


---

## 3. 将贝叶斯定理用于分类 (Using Bayes Theorem for Classification)

### 3.1 分类问题的概率表述 (Probabilistic Formulation)

![Page 5](week5_naivebayes_slides_pages/page_005.png)

**Classification setup:** Shows a tax evasion dataset with attributes (Refund, Marital Status, Taxable Income, Evade).

**分类问题设定：** 展示一个税务逃税数据集，包含属性（退税、婚姻状况、应税收入、逃税）。

- Consider each attribute and class label as **random variables** — 将每个属性和类别标签视为**随机变量**
- Given a record with attributes (X₁, X₂, …, Xd), the goal is to predict class Y — 给定属性记录 (X₁, X₂, …, Xd)，目标是预测类别 Y
- Specifically, we want to find the value of Y that **maximizes P(Y| X₁, X₂, …, Xd)** — 找到使 **P(Y| X₁, X₂, …, Xd) 最大化**的 Y 值

### 3.2 后验概率计算 (Posterior Probability Computation)

![Page 6](week5_naivebayes_slides_pages/page_006.png)

**Approach slide:** Shows the mathematical formulation for computing posterior probability.

**方法页：** 展示计算后验概率的数学公式。

- Compute posterior probability using Bayes theorem: P(Y | X₁X₂…Xd) = P(X₁X₂…Xd |Y) × P(Y) / P(X₁X₂…Xd) — 用贝叶斯定理计算后验概率
- **Maximum a-posteriori (MAP):** Choose Y that maximizes P(Y | X₁, X₂, …, Xd) — **最大后验估计：** 选择使 P(Y | X₁, X₂, …, Xd) 最大的 Y
- Equivalent to choosing Y that maximizes **P(X₁, X₂, …, Xd |Y) × P(Y)** — 等价于最大化 **P(X₁, X₂, …, Xd |Y) × P(Y)**
- Key question: **How to estimate P(X₁, X₂, …, Xd | Y)?** — 关键问题：**如何估计 P(X₁, X₂, …, Xd | Y)？**


---

## 4. 条件独立性与朴素贝叶斯假设 (Conditional Independence & Naïve Bayes Assumption)

### 4.1 条件独立性 (Conditional Independence)

![Page 9](week5_naivebayes_slides_pages/page_009.png)

**Conditional Independence slide:** Defines conditional independence with the arm length / reading skills example.

**条件独立性页：** 用臂长/阅读能力的例子定义条件独立性。

- X and Y are **conditionally independent** given Z if **P(X|YZ) = P(X|Z)** — 如果 **P(X|YZ) = P(X|Z)**，则 X 和 Y 在给定 Z 下**条件独立**
- Example: **Arm length and reading skills** — 示例：**臂长和阅读能力**
  - Young child has shorter arm length and limited reading skills, compared to adults — 与成人相比，幼儿的臂长较短且阅读能力有限
  - If **age** is fixed, no apparent relationship between arm length and reading skills — 如果**年龄**固定，臂长和阅读能力之间没有明显关系
  - Arm length and reading skills are conditionally independent **given age** — 臂长和阅读能力在**给定年龄**下条件独立

### 4.2 朴素贝叶斯分类器定义 (Naïve Bayes Classifier Definition)

![Page 10](week5_naivebayes_slides_pages/page_010.png)

**Core assumption slide:** The Naïve Bayes independence assumption that simplifies the likelihood computation.

**核心假设页：** 朴素贝叶斯的独立性假设，简化了似然的计算。

- Assume **independence** among attributes Xᵢ when class is given — 假设在给定类别时属性 Xᵢ 之间**相互独立**
- P(X₁, X₂, …, Xd | Yⱼ) = P(X₁|Yⱼ) × P(X₂|Yⱼ) × … × P(Xd|Yⱼ) — 联合概率分解为各属性条件概率的乘积
- Now we can estimate P(Xᵢ|Yⱼ) for **all Xᵢ and Yⱼ combinations** from the training data — 可以从训练数据中估计**所有 Xᵢ 和 Yⱼ 组合**的条件概率
- New point is classified to Yⱼ if **P(Yⱼ) × Π P(Xᵢ|Yⱼ) is maximal** — 如果 **P(Yⱼ) × Π P(Xᵢ|Yⱼ) 最大**则分类为 Yⱼ


---

## 5. 朴素贝叶斯实例演练 (Naïve Bayes Worked Example)

### 5.1 示例数据与设置 (Example Data & Setup)

![Page 7](week5_naivebayes_slides_pages/page_007.png)

**Test record setup:** Given X = (Refund = No, Divorced, Income = 120K), estimate P(Evade = Yes|X) and P(Evade = No|X).

**测试记录设定：** 给定 X = (退税 = 否, 离婚, 收入 = 120K)，估计 P(逃税 = 是|X) 和 P(逃税 = 否|X)。

![Page 8](week5_naivebayes_slides_pages/page_008.png)

**Full dataset:** 10 records with attributes Refund, Marital Status, Taxable Income, and class label Evade (Yes/No).

**完整数据集：** 10条记录，包含退税、婚姻状况、应税收入和类别标签逃税（是/否）。

### 5.2 似然计算分解 (Likelihood Decomposition)

![Page 11](week5_naivebayes_slides_pages/page_011.png)

**Decomposition slide:** Shows how joint likelihood P(X|class) is decomposed into individual attribute likelihoods.

**分解页：** 展示联合似然 P(X|class) 如何分解为各属性的似然。

- P(X | Yes) = P(Refund=No | Yes) × P(Divorced | Yes) × P(Income=120K | Yes)
- P(X | No) = P(Refund=No | No) × P(Divorced | No) × P(Income=120K | No)

### 5.3 概率估计方法 (Probability Estimation Methods)

![Page 12](week5_naivebayes_slides_pages/page_012.png)

**Estimation from data:** Shows how to estimate probabilities for categorical and continuous attributes.

**从数据估计概率：** 展示如何估计分类属性和连续属性的概率。

- **P(y)** = fraction of instances of class y — e.g., P(No) = 7/10, P(Yes) = 3/10
- **For categorical attributes:** P(Xᵢ = c | y) = nc / n — nc为 Xᵢ=c 且 Y=y 的实例数
  - Example: P(Status=Married | No) = 4/7, P(Refund=Yes | Yes) = 0

![Page 13](week5_naivebayes_slides_pages/page_013.png)

**Continuous attributes:** Shows the Gaussian (Normal) distribution formula for estimating continuous attribute probabilities.

**连续属性：** 展示用于估计连续属性概率的高斯（正态）分布公式。

- **Normal distribution:** P(Xᵢ|Yⱼ) = (1/√(2πσ²ᵢⱼ)) × exp(-(Xᵢ - μᵢⱼ)² / (2σ²ᵢⱼ))
  - One distribution for each (Xᵢ, Yⱼ) pair — 每对 (Xᵢ, Yⱼ) 一个分布
- For (Income, Class=No): sample mean = 110, sample variance = 2975
- P(Income=120 | No) = (1/√(2π×2975)) × exp(-(120-110)²/(2×2975)) = **0.0072**

### 5.4 完整分类示例 (Complete Classification Example)

![Page 14](week5_naivebayes_slides_pages/page_014.png)

**Complete example:** Shows the full Naïve Bayes computation for the test record X = (Refund=No, Divorced, Income=120K).

**完整示例：** 展示测试记录 X = (退税=否, 离婚, 收入=120K) 的完整朴素贝叶斯计算。

- P(X | No) = 4/7 × 1/7 × 0.0072 = **0.0006**
- P(X | Yes) = 1 × 1/3 × 1.2×10⁻⁹ = **4×10⁻¹⁰**
- Since P(X|No)×P(No) > P(X|Yes)×P(Yes) → **Class = No**


---

## 6. 部分信息决策 (Decision with Partial Information)

![Page 15](week5_naivebayes_slides_pages/page_015.png)

**Partial information slide:** Shows that Naïve Bayes can make decisions even with incomplete attribute information.

**部分信息页：** 展示朴素贝叶斯即使在属性信息不完整时也能做出决策。

- Even in absence of information about any attributes, we can use P(Yes) = 3/10 — 即使没有任何属性信息，也可使用先验概率
- If we only know Marital Status = Divorced → P(Yes|Divorced) vs P(No|Divorced)
- As more attributes become known, the classification becomes more confident — 随着已知属性增多，分类更有信心


---

## 7. 朴素贝叶斯的问题 (Issues with Naïve Bayes)

### 7.1 零概率问题 (Zero Probability Problem)

![Page 16](week5_naivebayes_slides_pages/page_016.png)

**Zero probability issue:** Shows that P(Married|Yes) = 0 makes the entire posterior zero, regardless of other attributes.

**零概率问题：** 展示 P(已婚|是) = 0 会使整个后验概率为零，无论其他属性如何。

- Given X = (Married): P(Yes | Married) = **0** × 3/10 / P(Married) — 一个条件概率为0就使整个乘积为0

![Page 17](week5_naivebayes_slides_pages/page_017.png)

**Classification failure:** With Tid=7 deleted, P(Divorced|No) = 0 and P(Refund=Yes|Yes) = 0, making classification impossible.

**分类失败：** 删除 Tid=7 后，P(离婚|否) = 0 且 P(退税=是|是) = 0，导致无法分类。

- P(X|No) = 2/6 × **0** × 0.0083 = **0**
- P(X|Yes) = **0** × 1/3 × 1.2×10⁻⁹ = **0**
- Naïve Bayes will **not be able to classify** X as Yes or No! — 朴素贝叶斯**无法分类**！

### 7.2 拉普拉斯平滑 (Laplace Smoothing / m-estimate)

![Page 18](week5_naivebayes_slides_pages/page_018.png)

**Smoothing solutions:** Shows Laplace smoothing and m-estimate to handle zero probabilities.

**平滑方案：** 展示拉普拉斯平滑和 m-估计来处理零概率问题。

- **Original:** P(Xᵢ = c | y) = nc / n
- **Laplace smoothing:** P(Xᵢ = c | y) = (nc + 1) / (n + v)
  - v = total number of attribute values that Xᵢ can take — v = Xᵢ 可取值的总数
- **m-estimate:** P(Xᵢ = c | y) = (nc + m×p) / (n + m)
  - p = initial estimate of P(Xᵢ = c | y) known a priori — p = 先验初始估计
  - m = hyper-parameter for confidence in p — m = 对p置信度的超参数


---

## 8. 更多分类示例 (Additional Classification Example)

![Page 19](week5_naivebayes_slides_pages/page_019.png)

**Animal classification:** A larger example with 20 animal records, classifying as Mammals vs Non-mammals using attributes (Give Birth, Can Fly, Live in Water, Have Legs).

**动物分类：** 更大规模的示例，20条动物记录，用属性（产仔、能飞、水生、有腿）分类为哺乳动物 vs 非哺乳动物。

- Test record: (Give Birth = yes, Can Fly = no, Live in Water = yes, Have Legs = no)
- P(A|M) = 6/7 × 6/7 × 2/7 × ... = 0.06 → P(A|M)×P(M) = 0.021
- P(A|N) = 1/13 × 10/13 × 3/13 × ... = 0.0042 → P(A|N)×P(N) = 0.0027
- P(A|M)×P(M) > P(A|N)×P(N) → **Class = Mammals**


---

## 9. 朴素贝叶斯总结 (Naïve Bayes Summary)

![Page 20](week5_naivebayes_slides_pages/page_020.png)

**Summary slide:** Lists strengths and weaknesses of Naïve Bayes.

**总结页：** 列出朴素贝叶斯的优缺点。

- **Robust to isolated noise points** — 对孤立噪声点稳健
- **Handle missing values** by ignoring the instance during probability estimate calculations — 通过在概率估计中忽略该实例来**处理缺失值**
- **Robust to irrelevant attributes** — 对无关属性稳健
- **Redundant and correlated attributes** will violate class conditional assumption — **冗余和相关属性**会违反类条件独立假设
  - Use other techniques such as Bayesian Belief Networks (BBN) — 使用贝叶斯信念网络等其他技术

![Page 21](week5_naivebayes_slides_pages/page_021.png)

**Performance question:** How does Naïve Bayes perform when conditional independence of attributes is violated?

**性能问题：** 当属性的条件独立性被违反时，朴素贝叶斯表现如何？


---

## 10. 贝叶斯信念网络 (Bayesian Belief Networks)

### 10.1 BBN 定义与结构 (BBN Definition & Structure)

![Page 22](week5_naivebayes_slides_pages/page_022.png)

**BBN definition:** Provides graphical representation of probabilistic relationships among random variables.

**BBN 定义：** 提供随机变量之间概率关系的图形表示。

- A **directed acyclic graph (DAG)** — 一个**有向无环图 (DAG)**
  - **Node** corresponds to a variable — **节点**对应一个变量
  - **Arc** corresponds to dependence relationship between a pair of variables — **弧**对应变量对之间的依赖关系
- A **probability table** associating each node to its immediate parent — 将每个节点与其直接父节点关联的**概率表**

### 10.2 BBN 中的条件独立性 (Conditional Independence in BBN)

![Page 23](week5_naivebayes_slides_pages/page_023.png)

**BBN conditional independence:** Shows parent-child-descendant-ancestor relationships in the DAG.

**BBN 条件独立性：** 展示 DAG 中的父-子-后代-祖先关系。

- D is parent of C; A is child of C; B is descendant of D; D is ancestor of A
- A node in a Bayesian network is **conditionally independent of all of its non-descendants**, if its parents are known — 在贝叶斯网络中，如果父节点已知，则节点**与所有非后代节点条件独立**

![Page 24](week5_naivebayes_slides_pages/page_024.png)

**Naïve Bayes as BBN:** Shows Naïve Bayes assumption as a special BBN structure where Y is the parent of all attributes X₁, X₂, …, Xd.

**朴素贝叶斯作为 BBN：** 展示朴素贝叶斯假设作为特殊的 BBN 结构，其中 Y 是所有属性 X₁, X₂, …, Xd 的父节点。

### 10.3 概率表 (Probability Tables)

![Page 25](week5_naivebayes_slides_pages/page_025.png)

**Probability table rules:** Shows how probability tables work based on parent relationships.

**概率表规则：** 展示概率表如何根据父节点关系工作。

- If X **does not have any parents**, table contains **prior probability** P(X) — 无父节点则包含**先验概率**
- If X has **only one parent** (Y), table contains **conditional probability** P(X|Y) — 一个父节点则包含**条件概率**
- If X has **multiple parents** (Y₁, Y₂, …, Yk), table contains P(X|Y₁, Y₂, …, Yk) — 多个父节点则包含**联合条件概率**


---

## 11. BBN 推理实例 (BBN Inference Example)

### 11.1 心脏病网络 (Heart Disease Network)

![Page 26](week5_naivebayes_slides_pages/page_026.png)

**Heart disease BBN example:** A complete BBN with nodes Exercise, Diet, Heart Disease, Blood Pressure, Chest Pain, and their conditional probability tables.

**心脏病 BBN 示例：** 完整的 BBN，包含节点：运动、饮食、心脏病、血压、胸痛，及其条件概率表。

- **Root nodes (prior probabilities):**
  - P(Exercise=Yes) = 0.7, P(Exercise=No) = 0.3
  - P(Diet=Healthy) = 0.25, P(Diet=Unhealthy) = 0.75
- **Heart Disease (depends on Exercise & Diet):**
  - P(HD=Yes | E=Yes, D=Healthy) = 0.25
  - P(HD=Yes | E=No, D=Unhealthy) = 0.75
- **Chest Pain & Blood Pressure (depend on Heart Disease):**
  - P(CP=Yes | HD=Yes) = 0.8, P(BP=High | HD=Yes) = 0.85

### 11.2 BBN 推理计算 (BBN Inference Computation)

![Page 27](week5_naivebayes_slides_pages/page_027.png)

**Inference example:** Given X = (E=No, D=Yes, CP=Yes, BP=High), compute P(HD|X).

**推理示例：** 给定 X = (运动=否, 饮食=健康, 胸痛=是, 血压=高)，计算 P(HD|X)。

- P(HD=Yes | E=No, D=Yes) = 0.45 → × P(CP=Yes|HD=Yes) × P(BP=High|HD=Yes) = 0.45 × 0.8 × 0.85 = **0.306** (note: slide shows 0.55 for HD=Yes)
- P(HD=No | E=No, D=Yes) = 0.55 → × P(CP=Yes|HD=No) × P(BP=High|HD=No) = 0.55 × 0.01 × 0.2 = **0.0011** (note: slide shows 0.45 for HD=No)
- Since 0.306 ≫ 0.0011 → **Classify X as HD = Yes** — 分类为心脏病 = 是


---

## 12. 结语 (Conclusion)

![Page 28](week5_naivebayes_slides_pages/page_028.png)

**End slide.**

**结束页。**
