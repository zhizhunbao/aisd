# Week 5: Naive Bayes & BBN — 教科书教程

> **Purpose:** 提供课堂 slides 未覆盖的**数学推导和定理证明**，作为深度参考。
> **与 Storyline 的区别：** Storyline 讲"**为什么**需要这个概念"；Tutorial 讲"**教科书怎么推导的**"。
> **阅读建议：** 先读 Storyline 建立直觉，再来这里看数学细节。

---

## §0 概率基础 — 四个核心概念

> 📚 Ref: [MML §6.2 Discrete and Continuous Probabilities](../../self-study/math/_sources/mml_sections/ch06/sec_6.2_discrete_and_continuous_probabilities.md) — Eq. 6.9–6.14

后面所有公式都建立在四个概念上。MML §6.2 Example 6.2 用抽象的 $n_{ij}$ 符号定义它们，这里用一个具体例子让概念更直观。

### 🎲 贯穿例子：一个班级30个学生

|                     | 男生 (x=男) | 女生 (x=女) | 合计   |
| ------------------- | ----------- | ----------- | ------ |
| **戴眼镜 (y=是)**   | 6           | 9           | 15     |
| **不戴眼镜 (y=否)** | 4           | 11          | 15     |
| **合计**            | 10          | 20          | **30** |

> 这个例子会在后面所有章节中反复使用，让新公式有具体数字可以代入验证。

### 0.1 概率 — "一件事发生的可能性"

> "随机抽一个学生，是男生的概率？"

$$P(x = 男) = \frac{10}{30} = \frac{1}{3}$$

最基本的概率：**满足条件的数量** ÷ **总数量**。

### 0.2 联合概率 P(x, y) — "两件事同时发生"

> 📚 MML Eq. 6.9: $P(X = x_i, Y = y_j) = \frac{n_{ij}}{N}$
> 其中 $n_{ij}$ 是同时满足 $X = x_i$ 和 $Y = y_j$ 的个数，$N$ 是总数。

> "随机抽一个学生，**既是男生又戴眼镜**的概率？"

$$P(x = 男,\ y = 是) = \frac{n_{ij}}{N} = \frac{6}{30} = 0.2$$

关键词是"**同时**" — 要同时满足两个条件。在表格里就是找到**对应的那一格**（$n_{ij}$）。

### 0.3 边缘概率 P(x) — "把另一个变量加掉"

> 📚 MML Eq. 6.10: $P(X = x_i) = \frac{c_i}{N} = \frac{\sum_j n_{ij}}{N}$
> 其中 $c_i$ 是第 $i$ 列所有行的合计。MML 原文："the probability distribution of each random variable can be seen as the sum over a row or column"。

> "不管戴不戴眼镜，是男生的概率？"

$$P(x = 男) = P(x=男, y=是) + P(x=男, y=否) = \frac{6}{30} + \frac{4}{30} = \frac{10}{30}$$

边缘概率就是**把你不关心的变量求和**（$c_i = \sum_j n_{ij}$）。在表格里就是看**行/列的合计**。

> 📝 "边缘"这个名字来自历史习惯：手算时，行列合计写在表格的**边缘**（margin）处，所以叫 marginal probability。

### 0.4 条件概率 P(y | x) — "已知一件事后，另一件事的概率"

> 📚 MML Eq. 6.13: $P(Y = y_j \mid X = x_i) = \frac{n_{ij}}{c_i}$
> MML 原文："if we consider only the instances where $X = x$, then the fraction of instances for which $Y = y$ is written as $p(y \mid x)$"。

> "**已知是男生**，他戴眼镜的概率？"

$$P(y = 是 \mid x = 男) = \frac{n_{ij}}{c_i} = \frac{6}{10} = 0.6$$

注意分母变了！不再是全班30人（$N$），而是**只看男生那10人**（$c_i$）。竖线 "|" 读作"**给定**"（given）— 给定了 x=男，世界缩小到了10个人。

**定义公式：** 条件概率也可以写成联合概率除以边缘概率：

$$P(y \mid x) = \frac{P(x, y)}{P(x)} = \frac{6/30}{10/30} = \frac{6}{10} = 0.6$$

> ⚠️ **为什么条件概率是一切的起点：** 把这个公式两边乘以 $P(x)$，就得到 $P(x, y) = P(y \mid x) \cdot P(x)$ — 这就是下面 §1 的**乘法法则**。整个 Bayes 定理都是从这一个定义推出来的。

### 0.5 对数 log — "把乘法变成加法的工具"

后面 §3 会用到对数（$\log$），这里先讲清楚它是什么、为什么有用。

**对数是什么：** 对数是指数（幂）的**反操作**，就像减法是加法的反操作一样。

$$2^3 = 8 \quad \Longleftrightarrow \quad \log_2 8 = 3$$

白话："2 的几次方等于 8？答：3次。" 对数回答的是"**几次方**"这个问题。

ML 中通常用**自然对数** $\ln$（以 $e \approx 2.718$ 为底），写作 $\log$ 时默认就是 $\ln$。

**对数最重要的一条性质：把乘法变成加法。**

$$\log(a \times b) = \log(a) + \log(b)$$

验证：$\log(2 \times 8) = \log(16) \approx 2.77$，$\log(2) + \log(8) \approx 0.69 + 2.08 = 2.77$ ✅

**为什么 ML 中要取对数？** 两个原因：

**原因1：数字太小会"下溢"。** NB 要把很多概率乘起来（§2 的连乘 $\prod$）。比如10个特征各自概率都是 0.1：

$0.1 \times 0.1 \times \cdots \times 0.1 = 0.1^{10} = 0.0000000001$

计算机存不了这么小的数（浮点数精度有限），会变成0。但取对数后：

$\log(0.1) + \log(0.1) + \cdots + \log(0.1) = 10 \times (-2.3) = -23$

$-23$ 是个正常的数字，计算机轻松存储。

**原因2：加法比乘法更容易优化。** §3 MLE 要找"使概率最大的参数"。对乘积求导很复杂，但取对数变成求和后，求导就简单了。而且 $\log$ 是单调递增函数 — **使乘积最大的参数，也使对数和最大**，所以优化结果不变。

> 📝 这就是为什么 §3 叫"对数似然"— 不是因为数学上必须取对数，而是取了之后**计算更方便、数值更稳定**，结果完全等价。

---

## §1 从乘法法则推导 Bayes 定理

> 📚 Ref: [MML §6.3 Sum Rule, Product Rule, and Bayes' Theorem](../../self-study/math/_sources/mml_sections/ch06/sec_6.3_sum_rule_product_rule_and_bayes_theorem.md)

Slides 直接给出 Bayes 公式，但没有展示它是怎么来的。教科书的推导只需要两步。

### 1.1 乘法法则（Product Rule）

> 📚 MML §6.3: "p(x, y) = p(y | x) · p(x)" 和 "also: p(x, y) = p(x | y) · p(y)"

就是 §0.4 的条件概率定义移项后得到的。联合概率可以用两种方式分解：

$$p(x, y) = p(y \mid x) \cdot p(x) \tag{写法1：先确定x，再看y}$$

$$p(x, y) = p(x \mid y) \cdot p(y) \tag{写法2：先确定y，再看x}$$

用班级例子验证写法1：$p(男, 眼镜) = p(眼镜 \mid 男) \cdot p(男) = \frac{6}{10} \times \frac{10}{30} = \frac{6}{30}$ ✅

用班级例子验证写法2：$p(男, 眼镜) = p(男 \mid 眼镜) \cdot p(眼镜) = \frac{6}{15} \times \frac{15}{30} = \frac{6}{30}$ ✅

两种写法结果一样，因为它们描述的是**同一件事**（同时是男生且戴眼镜），只是分解的顺序不同。

### 1.2 推导 Bayes 定理

既然两种写法都等于 $p(x, y)$，令它们相等：

$$p(y \mid x) \cdot p(x) = p(x \mid y) \cdot p(y)$$

两边除以 $p(y)$：

$$p(x \mid y) = \frac{p(y \mid x) \cdot p(x)}{p(y)} \qquad \blacksquare$$

> 📝 $\blacksquare$ 是数学中的"证毕"符号（Q.E.D.），表示推导到此结束。

这个公式以 **Thomas Bayes**（1701–1761，英国牧师和数学家）命名。Bayes 在遗作中提出了这个思想，后来由 **Pierre-Simon Laplace**（1749–1827，法国数学家）在 1812 年的《概率分析理论》中正式表述和推广。

### 1.3 四个术语的命名

> 📚 MML §6.3 对 Bayes 公式四个位置的标注（原文 p.178）

公式里的四个位置有专门的名字：

$$\underbrace{p(x \mid y)}_{\text{后验 Posterior}} = \frac{\overbrace{p(y \mid x)}^{\text{似然 Likelihood}} \cdot \overbrace{p(x)}^{\text{先验 Prior}}}{\underbrace{p(y)}_{\text{证据 Evidence}}}$$

用班级例子（根据"戴不戴眼镜"来猜"是男是女"，$x$=性别，$y$=眼镜）：

| 术语                | 符号          | 白话                               | 班级例子     |
| ------------------- | ------------- | ---------------------------------- | ------------ |
| **先验** Prior      | $p(x)$        | **还没看眼镜之前**，猜是男生的概率 | 10/30 = 1/3  |
| **似然** Likelihood | $p(y \mid x)$ | **如果是男生**，戴眼镜的概率有多大 | 6/10 = 0.6   |
| **证据** Evidence   | $p(y)$        | **不管男女**，戴眼镜的整体概率     | 15/30 = 0.5  |
| **后验** Posterior  | $p(x \mid y)$ | **看到戴眼镜之后**，猜是男生的概率 | **= 要算的** |

这些名字的来源：

- **Prior**（先验）和 **Posterior**（后验）— **Laplace** (1812) 正式使用。"先"于观察 / "后"于观察的信念
- **Likelihood**（似然）— **R.A. Fisher** (1921) 正式定义，刻意区分 "probability"（给定参数预测数据）和 "likelihood"（给定数据反推参数）。MML 原文："how likely the data $y$ is, given the latent variable $x$"
- **Evidence**（证据）— 现代贝叶斯统计的通用术语，也叫 marginal likelihood。MML 原文："the total probability of the observed data"

代入验证：$p(男 \mid 眼镜) = \frac{0.6 \times \frac{1}{3}}{0.5} = \frac{0.2}{0.5} = 0.4$ ✅（和直接数表格 6/15 = 0.4 一致）

### 1.4 证据项 P(y) 的计算

现在要**真的用 Bayes 公式**，右边三项你都得知道。**先验** $p(x)$ 和**似然** $p(y \mid x)$ 可以从训练数据直接"数"出来，但**证据** $p(y)$ 怎么算？

> 📚 MML §6.3 Sum Rule: "p(x) = Σ_y p(x, y)"（离散）/ "p(x) = ∫ p(x, y) dy"（连续）

$p(y)$ 通过**求和法则**（Sum Rule，也叫边缘化 Marginalization）计算 — 就是 §0.3 边缘概率的推广：

$$p(y) = \sum_x p(y \mid x) \cdot p(x) \quad \text{（离散）}$$

$$p(y) = \int p(y \mid x) \cdot p(x) \, dx \quad \text{（连续）}$$

班级例子验证：$p(眼镜) = p(眼镜 \mid 男) \cdot p(男) + p(眼镜 \mid 女) \cdot p(女) = 0.6 \times \frac{1}{3} + \frac{9}{20} \times \frac{2}{3} = 0.2 + 0.3 = 0.5$ ✅

> 📝 MML 的直觉："把不关心的变量加掉"— 把二维联合分布投影到一个轴上。

> ⚠️ **Slides 未强调的实用技巧：** 在分类问题中，如果只需要比较哪个类别的后验更大（而不需要精确概率值），可以跳过 $p(y)$ 的计算 — 因为它对所有类别都一样。这叫做 **MAP 决策**（Maximum A Posteriori，最大后验）：$\hat{y} = \arg\max_x\ p(y \mid x) \cdot p(x)$。但如果需要实际概率值，就必须计算 $p(y)$。

---

到此为止，我们有了 Bayes 定理的完整推导和所有工具。但要把它用于**分类**（多个特征预测类别），会遇到一个严重问题：特征太多时，似然 $p(\mathbf{x} \mid y)$ 无法直接估计。下一节解释这个问题和 Murphy 教科书的解决方案。

---

## §2 朴素假设的数学根基 — 从联合到乘积

> 📚 Ref: [Murphy PML1 §9.3 Naive Bayes Classifiers](../../self-study/ml/_sources/murphy_pml1_sections/ch09/sec_9_3_naive_bayes_classifiers.md) — Eq. 9.46–9.47

Murphy 的公式用了很多符号。先列一个对照表，后面看公式时随时回来查：

| 符号                  | 含义                           | 逃税例子中对应                                               |
| --------------------- | ------------------------------ | ------------------------------------------------------------ |
| $y$                   | 类别标签                       | 逃税？（Yes / No）                                           |
| $c$                   | 类别的某个具体取值             | Yes 或 No                                                    |
| $C$                   | 类别总数                       | 2（Yes 和 No）                                               |
| $\mathbf{x}$          | 所有特征的组合                 | (已婚, 有退税, 低收入)                                       |
| $x_d$                 | 第 $d$ 个特征                  | $x_1$=婚姻, $x_2$=退税, $x_3$=收入                           |
| $D$                   | 特征总数                       | 3                                                            |
| $v$                   | 每个特征的取值数               | 2（如：已婚/未婚）                                           |
| $\pi_c$               | 类别先验 $P(y=c)$              | $\pi_{\text{Yes}}=0.3$，$\pi_{\text{No}}=0.7$                |
| $\theta_{dc}$         | 第 $d$ 个特征在类 $c$ 下的参数 | $\theta_{1,\text{Yes}} = P(\text{已婚}\mid\text{Yes}) = 0.3$ |
| $\boldsymbol{\theta}$ | 所有参数的总称                 | 上面所有概率值打包在一起                                     |
| $N$                   | 训练数据总数                   | 比如 100 条记录                                              |
| $N_c$                 | 类 $c$ 的样本数                | $N_{\text{Yes}}=30$，$N_{\text{No}}=70$                      |

### 2.1 问题：全联合分布的参数爆炸

在分类问题中，我们有 $D$ 个特征 $x_1, x_2, \ldots, x_D$ 和一个类别标签 $y$。根据 §1 的 Bayes 定理，我们需要估计**似然** $p(x_1, x_2, \ldots, x_D \mid y = c)$ — 这是一个**联合条件分布**（给定类别$c$后，所有特征同时取某组值的概率）。

Murphy 指出朴素假设后参数量是 $O(CD)$，但没有推导假设前需要多少参数。下面从组合计数推导：

> 📐 **推导（tutorial 补充，非教科书原文）：**
>
> 如果每个特征有 $v$ 种取值，那么 $D$ 个特征的所有可能**组合数** = $v \times v \times \cdots \times v = v^D$。
>
> 联合分布需要给每种组合一个概率值。这些概率之和必须=1，所以知道 $v^D - 1$ 个就能算出最后一个。因此：
>
> $$\text{无朴素假设的参数数} = v^D - 1 \quad \text{（指数级增长）}$$
>
> 例如 $D = 10$ 个二值特征 → $2^{10} - 1 = 1023$ 个参数（每个类别！）。

### 2.2 解决方案：条件独立假设

> 📚 Murphy §9.3 Eq. 9.46

Murphy 教科书引入了一个简化假设来解决上述参数爆炸问题。

先解释两个概念：

- **独立**（Independence）：两件事互不影响。$P(A, B) = P(A) \cdot P(B)$。例如：抛两次硬币，第一次的结果不影响第二次。
- **条件独立**（Conditional Independence）：**在知道某件事之后**，两件事互不影响。$P(A, B \mid C) = P(A \mid C) \cdot P(B \mid C)$。例如：知道年龄后，臂长和阅读能力不再相关（因为年龄同时影响了两者）。

**朴素贝叶斯假设**就是：所有特征在**给定类别后**彼此条件独立。Murphy 原文："we assume the features are conditionally independent given the class label. This is called the naive Bayes assumption."

数学表达（Murphy 引入符号 $\boldsymbol{\theta}$ 表示模型的所有参数——就是那些需要从数据中学出来的概率值，$\theta_{dc}$ 表示第 $d$ 个特征在类别 $c$ 下的参数）：

$$p(\mathbf{x} \mid y = c, \boldsymbol{\theta}) = \prod_{d=1}^{D} p(x_d \mid y = c, \theta_{dc}) \tag{Murphy Eq. 9.46}$$

**逃税例子代入 Eq. 9.46：** 假设3个特征：婚姻($x_1$)、退税($x_2$)、收入($x_3$)，已知从训练数据中数出来的概率是：

| 特征          | $P(x_d \mid \text{Yes})$ | $P(x_d \mid \text{No})$ |
| ------------- | ------------------------ | ----------------------- |
| $x_1$: 已婚   | 0.3                      | 0.5                     |
| $x_2$: 有退税 | 0.6                      | 0.2                     |
| $x_3$: 低收入 | 0.4                      | 0.8                     |

那么 Eq. 9.46 展开就是：

$p(\text{已婚,有退税,低收入} \mid \text{Yes}) = 0.3 \times 0.6 \times 0.4 = 0.072$

$p(\text{已婚,有退税,低收入} \mid \text{No}) = 0.5 \times 0.2 \times 0.8 = 0.08$

> 📐 **参数量验证（tutorial 补充）：**
>
> 上面的例子中，3个特征各2种取值。不用朴素假设需要 $2^3 - 1 = 7$ 个参数（每类）。
> 用了朴素假设只需要 $3 \times (2-1) = 3$ 个参数（每类）——就是表格里的3个数字。
>
> 这与 Murphy 原文的 $O(CD)$ 一致（$C$ 个类别 × $D$ 个特征）。

> Murphy 原文对"朴素"的解释："The model is called 'naive' since we do not expect the features to be independent, even conditional on the class label. However, even if the naive Bayes assumption is not true, it often results in classifiers that work well... One reason for this is that the model is quite simple (it only has $O(CD)$ parameters) and hence it is relatively immune to overfitting."

### 2.3 后验分类公式

> 📚 Murphy §9.3 Eq. 9.47

将朴素假设（Eq. 9.46）代入 §1 的 Bayes 定理，就得到**朴素贝叶斯分类器**（NBC）的完整公式。其中 $\pi_c$ 是 Murphy 对**类别先验** $P(y = c)$ 的简写符号：

$$p(y = c \mid \mathbf{x}, \boldsymbol{\theta}) = \frac{p(y = c \mid \pi) \prod_{d=1}^{D} p(x_d \mid y = c, \theta_{dc})}{\sum_{c'} p(y = c' \mid \pi) \prod_{d=1}^{D} p(x_d \mid y = c', \theta_{dc'})} \tag{Murphy Eq. 9.47}$$

白话：**后验 = 该类别的得分 ÷ 所有类别得分之和**

**逃税例子代入 Eq. 9.47：** 假设先验 $P(\text{Yes}) = 0.3$，$P(\text{No}) = 0.7$。

**分子（Yes 的得分）：** 先验 × Eq. 9.46 的连乘结果

$P(\text{Yes}) \times p(\text{已婚,有退税,低收入} \mid \text{Yes}) = 0.3 \times 0.072 = 0.0216$

**分母（所有类别得分之和）：**

$\text{Yes的得分} + \text{No的得分} = 0.0216 + (0.7 \times 0.08) = 0.0216 + 0.056 = 0.0776$

**后验：**

$P(\text{Yes} \mid \text{已婚,有退税,低收入}) = \frac{0.0216}{0.0776} = 0.278 \quad (27.8\%)$

$P(\text{No} \mid \text{已婚,有退税,低收入}) = \frac{0.056}{0.0776} = 0.722 \quad (72.2\%)$

**分类结果：No（不逃税）**，因为 72.2% > 27.8%。注意两个后验加起来 = 100%（分母的作用就是保证这一点）。

---

公式有了，但里面的参数 $\theta_{dc}$（每个特征在每个类别下的概率分布）和 $\pi_c$（类别先验）具体怎么从训练数据估计出来？下一节讲 Murphy 的 MLE 方法。

---

## §3 MLE 参数估计 — 对数似然的分解

> 📚 Ref: [Murphy PML1 §9.3.2 Model Fitting](../../self-study/ml/_sources/murphy_pml1_sections/ch09/sec_9_3_naive_bayes_classifiers.md) — Eq. 9.48–9.55

Slides 只说"数记录"来估计参数，但没展示为什么"数记录"是对的。Murphy 用 **MLE**（Maximum Likelihood Estimation，最大似然估计）给出了数学证明。

**MLE 是什么：** 给定观测数据 $\mathcal{D}$（训练集），找到一组参数 $\boldsymbol{\theta}$，使得这组参数下数据出现的概率**最大**。这个方法由 **R.A. Fisher**（1890–1962，英国统计学家）在 1920 年代提出。

### 3.1 对数似然的分解

> 📚 Murphy §9.3.2 Eq. 9.50–9.51

Murphy 首先写出整个训练集的似然函数（所有样本概率的乘积），然后取对数得到**对数似然**（取对数是因为乘积变成求和，更容易优化）。

这个公式引入的新符号：

| 新符号                | 含义                         | 逃税例子                                                              |
| --------------------- | ---------------------------- | --------------------------------------------------------------------- |
| $\mathcal{D}$         | 训练数据集                   | 100条逃税记录                                                         |
| $\log$                | 对数（通常自然对数 ln）      | 把连乘变成连加                                                        |
| $n$                   | 第 $n$ 条数据                | 第1条、第2条…第100条                                                  |
| $y_n$                 | 第 $n$ 条数据的类别          | 第3个人逃税了 → $y_3 = \text{Yes}$                                    |
| $x_{nd}$              | 第 $n$ 条数据的第 $d$ 个特征 | 第3个人的婚姻状态 → $x_{3,1} = \text{已婚}$                           |
| $\mathbb{1}(y_n = c)$ | 指示函数：条件成立=1，否则=0 | $\mathbb{1}(y_3 = \text{Yes}) = 1$；$\mathbb{1}(y_3 = \text{No}) = 0$ |

$$\log p(\mathcal{D} \mid \boldsymbol{\theta}) = \underbrace{\sum_{n=1}^{N} \sum_{c=1}^{C} \mathbb{1}(y_n = c) \log \pi_c}_{\text{类别先验项}} + \sum_{c=1}^{C} \sum_{d=1}^{D} \underbrace{\sum_{n: y_n = c} \log p(x_{nd} \mid \theta_{dc})}_{\text{特征似然项}} \tag{Murphy Eq. 9.50}$$

> 📝 **关键性质：** 由于朴素假设（§2.2），对数似然**自然分解**为 $\pi$ 项和 $C \times D$ 个 $\theta_{dc}$ 项（Murphy Eq. 9.51）。这意味着可以**独立地**估计每个参数 — 这就是为什么 NB 的训练如此高效。

### 3.2 各类型特征的 MLE 结果

> 📚 Murphy §9.3.2 Eq. 9.52–9.55

对上面的对数似然分别求导、令导数为零，就得到各种特征类型的 MLE 公式。结果都是直观的"数记录"：

**离散特征（Categorical）：**

| 新符号               | 含义                                        | 逃税例子                                |
| -------------------- | ------------------------------------------- | --------------------------------------- |
| $\hat{\theta}_{dck}$ | MLE 估计出的参数值（$\hat{}$ 表示"估计值"） | $P(\text{已婚} \mid \text{Yes})$ 的估计 |
| $k$                  | 特征的某个取值                              | 婚姻的取值：已婚 或 未婚                |
| $N_{dck}$            | 类 $c$ 中特征 $d$ 取值 $k$ 的**计数**       | Yes类中已婚的人数 = 3                   |

$$\hat{\theta}_{dck} = \frac{N_{dck}}{N_c} \tag{Murphy Eq. 9.52}$$

白话：**该取值的计数 / 该类别的总数**。Murphy 原文："the number of times that feature $d$ had value $k$ in examples of class $c$"。

逃税例子：$P(\text{已婚} \mid \text{Yes}) = \frac{3}{30} = 0.1$ — 在逃税者中数一下已婚的有几个，除以逃税者总数。

**连续特征（Gaussian）：**

| 新符号                | 含义                             | 逃税例子               |
| --------------------- | -------------------------------- | ---------------------- |
| $\hat{\mu}_{dc}$      | 特征 $d$ 在类 $c$ 中的**平均值** | Yes类的平均收入 = 110K |
| $\hat{\sigma}^2_{dc}$ | 特征 $d$ 在类 $c$ 中的**方差**   | Yes类收入的方差 = 2975 |
| $\sum_{n: y_n = c}$   | "对所有属于类 $c$ 的样本求和"    | 对所有逃税者的收入求和 |

$$\hat{\mu}_{dc} = \frac{1}{N_c} \sum_{n: y_n = c} x_{nd} \tag{Murphy Eq. 9.54}$$

$$\hat{\sigma}^2_{dc} = \frac{1}{N_c} \sum_{n: y_n = c} (x_{nd} - \hat{\mu}_{dc})^2 \tag{Murphy Eq. 9.55}$$

白话：Eq. 9.54 就是**算平均值**，Eq. 9.55 就是**算方差**。Murphy 原文总结："Thus we see that fitting a naive Bayes classifier is extremely simple and efficient."

> ⚠️ **Murphy vs 课程的差异：** Murphy 用 $\frac{1}{N_c}$ 分母（MLE），课程 slides 用 $\frac{1}{N_c - 1}$（无偏样本方差，即 Python 中 `ddof=1`）。**考试按 slides 用 $N_c - 1$。** 这个差异不在教科书中讨论，是 tutorial 基于课程实际情况补充的注释。

---

MLE 解决了参数估计问题，但有一个致命缺陷：如果某个特征值在训练数据中**从未出现**过（$N_{dck} = 0$），MLE 会给出 $\hat{\theta}_{dck} = 0$，导致整个乘积为零。下一节看 Murphy 如何用贝叶斯方法解决这个问题。

---

## §4 Laplace 平滑的贝叶斯解释

> 📚 Ref: [Murphy PML1 §9.3.3 Bayesian Naive Bayes](../../self-study/ml/_sources/murphy_pml1_sections/ch09/sec_9_3_naive_bayes_classifiers.md) — Eq. 9.56–9.59

Slides 只给了 Laplace 平滑公式 $(n_c + 1)/(n + v)$，但没解释它的**概率论来源**。Murphy 揭示了本质：Laplace 平滑不是 ad-hoc 的"加1技巧"，而是有严格的贝叶斯理论基础。

### 4.1 共轭先验

> 📚 Murphy §9.3.3

要理解这一节，需要先知道两个概念：

- **先验分布**（Prior distribution）：在看到数据之前，对参数 $\theta$ 的初始信念。在 §1.3 中我们讲了"先验"是对类别的初始信念 $P(y=c)$；这里的先验是对**参数本身**的信念 $p(\theta)$ — 层次更高了一层
- **共轭先验**（Conjugate prior）：一种特殊的先验分布，使得**后验分布和先验分布是同一类型**。这大大简化了计算（由 **Raiffa & Schlaifer**, 1961 提出的概念）

对于分类似然 $\text{Cat}(x_d \mid \theta_{dc})$，共轭先验是 **Dirichlet 分布**（以德国数学家 **Peter Gustav Lejeune Dirichlet**, 1805–1859 命名）：

| 新符号                         | 含义                                   | 逃税例子                    |
| ------------------------------ | -------------------------------------- | --------------------------- |
| $\text{Dir}(\cdot \mid \beta)$ | Dirichlet 分布（一种"概率的概率"分布） | —                           |
| $\beta_{dck}$                  | **伪计数**：假装已经见过的次数         | "假装已经见过1个已婚逃税者" |
| $\hat{\beta}_{dck}$            | 更新后的计数 = 伪计数 + 实际计数       | $1 + 3 = 4$                 |
| $K$                            | 特征 $d$ 的取值种类数                  | 婚姻有2种取值（已婚/未婚）  |

$$p(\theta_{dc}) = \text{Dir}(\theta_{dc} \mid \beta_{dc})$$

$$\text{其中 } \beta_{dck} \text{ 是"伪计数"— Murphy 原文:"pseudo counts, corresponding to counts } N_{dck} \text{ that come from prior data"}$$

白话说：$\beta_{dck}$ 就是"在看到真实数据之前，我们假装已经见过多少次特征 $d$ 在类 $c$ 中取值 $k$"。

### 4.2 后验分布

> 📚 Murphy §9.3.3 Eq. 9.56

由于共轭性，后验分布也是 Dirichlet（先验和后验同类型，所以叫"共轭"）：

$$p(\boldsymbol{\theta} \mid \mathcal{D}) = \text{Dir}(\pi \mid \hat{\alpha}) \prod_{d=1}^{D} \prod_{c=1}^{C} \text{Dir}(\theta_{dc} \mid \hat{\beta}_{dc}) \tag{Murphy Eq. 9.56}$$

其中 $\hat{\beta}_{dck} = \beta_{dck} + N_{dck}$（先验伪计数 + 实际计数）。

### 4.3 后验预测

> 📚 Murphy §9.3.3 Eq. 9.57

Murphy 用**后验均值**（posterior mean，即后验分布的期望值）作为参数的点估计：

$$\bar{\theta}_{dck} = \frac{\beta_{dck} + N_{dck}}{\sum_{k'} (\beta_{dk'c} + N_{dk'c})} \tag{Murphy Eq. 9.57}$$

Murphy 原文："the posterior mean of the parameters"。

**三种特殊的 $\beta$ 设置：**

| 设置                        | 含义             | 公式                            | 教科书来源                 |
| --------------------------- | ---------------- | ------------------------------- | -------------------------- |
| $\beta_{dck} = 0$           | MLE（无先验）    | $\frac{N_{dck}}{N_c}$           | = Murphy Eq. 9.52          |
| $\beta_{dck} = 1$           | **Laplace 平滑** | $\frac{N_{dck} + 1}{N_c + K}$   | Murphy "add-one smoothing" |
| $\beta_{dck} = \frac{1}{K}$ | Jeffreys 先验    | $\frac{N_{dck} + 1/K}{N_c + 1}$ | —                          |

> 📝 **Laplace 平滑**以 Laplace 本人命名（他在 1814 年首先提出"把所有计数加1"的想法）。Murphy 揭示了其本质：**Laplace 平滑 = 设 Dirichlet 先验 $\beta = 1$ 后的后验均值**。

> ⚠️ **用词说明：** Murphy 原文说这是 "posterior mean"（后验均值），不是 "MAP estimate"（最大后验估计）。对于 Dirichlet 分布，这两者的公式不同（MAP 用的是 mode，不是 mean）。

---

到目前为止我们已经有了 NB 分类器的完整理论：Bayes 定理（§1）→ 朴素假设（§2）→ MLE 训练（§3）→ 平滑（§4）。下面两节是教科书中的**进阶内容**，Slides 完全没有覆盖。

---

## §5 NB 与逻辑回归的等价性

> 📚 Ref: [Murphy PML1 §9.3.4 The Connection Between Naive Bayes and Logistic Regression](../../self-study/ml/_sources/murphy_pml1_sections/ch09/sec_9_3_naive_bayes_classifiers.md) — Eq. 9.60–9.62

Slides 完全没有提到这个联系。Murphy 证明了一个令人惊讶的结果：NB 的后验形式等价于**逻辑回归**的 softmax。

### 5.1 推导

> 📚 Murphy §9.3.4 Eq. 9.60–9.62

Murphy 原文："we show that the class posterior $p(y \mid x, \theta)$ for a NBC model has the same form as multinomial logistic regression."

这一节引入的新符号：

| 新符号                  | 含义                                                      | 逃税例子                                               |
| ----------------------- | --------------------------------------------------------- | ------------------------------------------------------ |
| $x_{dk}$                | one-hot 编码：特征 $d$ 取值 $k$ 时=1，否则=0              | 婚姻=已婚 → $x_{1,\text{已婚}}=1, x_{1,\text{未婚}}=0$ |
| $\theta_{dck}^{x_{dk}}$ | 如果 $x_{dk}=1$ 则=参数值；如果=0 则=1（任何数的0次方=1） | —                                                      |
| $\boldsymbol{\beta}_c$  | 取 log 后的参数向量：$\beta_{cdk} = \log \theta_{dck}$    | —                                                      |
| $\gamma_c$              | 取 log 后的先验：$\gamma_c = \log \pi_c$                  | $\log 0.3 = -1.2$                                      |
| $\exp(\cdot)$           | 指数函数 $e^{(\cdot)}$，是 $\log$ 的反操作                | —                                                      |

先解释一个编码技巧：**one-hot 编码**是把分类值变成二进制向量的方法。例如颜色{红,绿,蓝} → 红=[1,0,0], 绿=[0,1,0], 蓝=[0,0,1]。Murphy 用 $x_{dk} = \mathbb{1}(x_d = k)$ 表示特征 $d$ 的 one-hot 编码。

代入后，NB 的类条件分布可以写成：

$$p(\mathbf{x} \mid y = c, \boldsymbol{\theta}) = \prod_{d=1}^{D} \prod_{k=1}^{K} \theta_{dck}^{x_{dk}} \tag{Murphy Eq. 9.60}$$

将这个代入 Bayes 定理的后验公式：

$$p(y = c \mid \mathbf{x}, \boldsymbol{\theta}) = \frac{\pi_c \prod_d \prod_k \theta_{dck}^{x_{dk}}}{\sum_{c'} \pi_{c'} \prod_d \prod_k \theta_{dc'k}^{x_{dk}}} \tag{Murphy Eq. 9.61}$$

取对数（利用 $a^b = \exp(b \log a)$）：

$$p(y = c \mid \mathbf{x}, \boldsymbol{\theta}) = \frac{\exp(\boldsymbol{\beta}_c^\top \mathbf{x} + \gamma_c)}{\sum_{c'} \exp(\boldsymbol{\beta}_{c'}^\top \mathbf{x} + \gamma_{c'})} \tag{Murphy Eq. 9.62}$$

其中 $\beta_{cdk} = \log \theta_{dck}$，$\gamma_c = \log \pi_c$。

**这就是 softmax 函数 — 多项逻辑回归的标准形式！**

### 5.2 意义

这个结果揭示了两种看似不同的分类方法之间的深层联系：

- **生成式模型**（Generative）：先建模数据是怎么生成的 $p(\mathbf{x} \mid y)$，再用 Bayes 定理"翻转"→ NB 就是这种
- **判别式模型**（Discriminative）：直接建模分类边界 $p(y \mid \mathbf{x})$ → 逻辑回归就是这种

Murphy 的推导证明了：NB 和逻辑回归给出**相同形式的决策边界**。区别在于**参数怎么估计** — NB 用 MLE 估计生成模型参数（§3），逻辑回归直接优化条件似然。NB 收敛更快（参数更少），但逻辑回归在大数据时渐近更好。

---

## §6 NB 的信念网络表示

> 📚 Ref: [Barber §10.1 Naive Bayes and Conditional Independence](../../self-study/ml/_sources/barber_sections/ch10/sec_10_1_naive_bayes_and_conditional_independence.md) — Eq. 10.1.1–10.1.2

### 6.1 NB 作为 DAG

> 📚 Barber §10.1 Eq. 10.1.1

**DAG**（Directed Acyclic Graph，有向无环图）是一种用箭头表示变量之间因果/依赖关系的图，且箭头不能形成环路。在概率论中，将联合分布表示为 DAG 的模型叫做**贝叶斯信念网络**（Bayesian Belief Network, BBN），也叫 Bayesian Network。

Barber 将 NB 的联合模型显式写为信念网络：

$$p(\mathbf{x}, c) = p(c) \prod_{i=1}^{D} p(x_i \mid c) \tag{Barber Eq. 10.1.1}$$

对应的 DAG 是**星形结构**：类别 $c$ 是唯一的父节点，所有特征 $x_i$ 都是叶子（子节点）。$c$ 直接指向每个 $x_i$，但 $x_i$ 之间没有任何边 — 这正是条件独立假设的图形化表达。

> Barber 原文："Coupled with a suitable choice for each conditional distribution $p(x_i \mid c)$, we can then use Bayes' rule to form a classifier for a novel attribute vector $x^*$"（Eq. 10.1.2）。

### 6.2 从 NB 到一般 BBN 的推广

> ⚠️ 以下内容是 tutorial 基于 Slides 中的 BBN 部分补充的总结，不直接来自 Barber §10.1（该章节仅49行，只讲了 NB 作为 BBN 特例）。

当朴素假设不成立时（特征之间确实有依赖），NB 的星形 DAG 不够用。一般的 BBN 允许：

- 特征之间有直接边（如 $\text{Exercise} \to \text{HD} \gets \text{Diet}$）
- 每个节点给定其**父节点**后，与所有**非后代节点**条件独立
- 条件概率表的大小取决于父节点数量

---

## 📚 参考索引

| 教程章节               | 教科书来源                  | 核心内容                              | Slides 覆盖？          |
| ---------------------- | --------------------------- | ------------------------------------- | ---------------------- |
| §0 概率基础            | MML §6.2 Eq. 6.9–6.14       | 联合/边缘/条件概率的定义              | ⚠️ Slides 假设已知     |
| §1 Bayes 推导          | MML §6.3                    | 从 Product Rule 推导 Bayes + 四术语   | ❌ Slides 直接给公式   |
| §2 朴素假设            | Murphy §9.3 Eq. 9.46–9.47   | 参数爆炸 → CI 假设 → 后验公式         | ⚠️ Slides 有结论无推导 |
| §3 MLE 分解            | Murphy §9.3.2 Eq. 9.48–9.55 | 对数似然自然分解 → "数记录"的数学证明 | ❌ Slides 只说"数记录" |
| §4 Laplace = Dirichlet | Murphy §9.3.3 Eq. 9.56–9.59 | Laplace 本质是 Dir(β=1) 的后验均值    | ❌ Slides 只给公式     |
| §5 NB = Softmax        | Murphy §9.3.4 Eq. 9.60–9.62 | NB 后验等价于逻辑回归 softmax 形式    | ❌ Slides 完全未提     |
| §6 NB 的 DAG           | Barber §10.1 Eq. 10.1.1     | NB = 特殊的星形 BBN                   | ⚠️ Slides 有图无公式   |
