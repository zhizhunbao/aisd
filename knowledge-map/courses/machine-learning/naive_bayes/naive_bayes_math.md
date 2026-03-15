---
topic: naive_bayes
dimension: math
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv:1410.5329 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Hastie et al., 《The Elements of Statistical Learning》 Ch.6.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
expiry: 12m
status: current
---

# Naive Bayes 数学基础

> 📚 Book: Murphy, [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.9
> 📖 Paper: Raschka, [Naive Bayes and Text Classification I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $x$ | 输入特征向量 | feature vector | $\mathbb{R}^d$ |
| $x_i$ | 第 $i$ 个特征 | $i$-th feature | $\mathbb{R}$ 或离散值 |
| $y$ | 类别标签 | class label | $\{1, 2, \ldots, C\}$ |
| $C$ | 类别总数 | number of classes | 正整数 |
| $d$ | 特征维度 | feature dimension | 正整数 |
| $N$ | 训练样本总数 | total samples | 正整数 |
| $N_c$ | 类别 $c$ 的样本数 | samples in class $c$ | 正整数 |
| $\pi_c$ | 类别 $c$ 的先验概率 | class prior | $[0,1]$，$\sum_c \pi_c = 1$ |
| $\theta_{ic}$ | 类别 $c$ 下特征 $i$ 的参数 | likelihood parameter | 依分布而定 |
| $\alpha$ | Laplace 平滑系数 | smoothing parameter | $\geq 0$ |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.2

---

## 核心公式

### 公式 1: 贝叶斯定理（NB 的出发点）

**直觉：** 把"结果反推原因"的问题，转化为"原因产生结果"的概率（更容易估计）

$$
P(y \mid x) = \frac{P(x \mid y) \cdot P(y)}{P(x)}
$$

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Eq. 2.14

**参数解释：**

| 项 | 含义 | 作用 |
|----|------|------|
| $P(y \mid x)$ | 后验：看了 x 之后 y 的概率 | 我们要求的目标 |
| $P(x \mid y)$ | 似然：y 类别"产生" x 的概率 | 从训练数据估计 |
| $P(y)$ | 先验：类别的初始概率 | 从类别频率估计 |
| $P(x)$ | 证据：x 出现的边缘概率 | 归一化常数，预测时可忽略 |

**推导过程：**

$$
\text{Step 1: 联合概率分解} \quad P(x, y) = P(x \mid y) \cdot P(y)
$$
$$
\text{Step 2: 同样地} \quad P(x, y) = P(y \mid x) \cdot P(x)
$$
$$
\text{Step 3: 两式相等} \quad P(y \mid x) \cdot P(x) = P(x \mid y) \cdot P(y)
$$
$$
\text{Step 4: 整理} \quad P(y \mid x) = \frac{P(x \mid y) \cdot P(y)}{P(x)}
$$

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Eq.1

---

### 公式 2: 朴素贝叶斯的条件独立分解

**直觉：** 条件独立假设让联合似然从"一个难算的大概率"变成"d 个小概率相乘"

$$
P(x \mid y) = \prod_{i=1}^{d} P(x_i \mid y)
$$

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Eq. 9.1

**推导过程（链式法则 + 独立假设）：**

$$
\text{Step 1: 链式法则展开} \quad P(x_1, x_2, \ldots, x_d \mid y) = P(x_1 \mid y) \cdot P(x_2 \mid x_1, y) \cdots P(x_d \mid x_1,\ldots,x_{d-1}, y)
$$
$$
\text{Step 2: 朴素假设} \quad P(x_i \mid x_1,\ldots,x_{i-1}, y) = P(x_i \mid y) \quad \forall i
$$
$$
\text{Step 3: 化简} \quad P(x \mid y) = \prod_{i=1}^{d} P(x_i \mid y)
$$

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.2.1

---

### 公式 3: MAP 决策规则

**直觉：** 预测时不需要归一化常数 $P(x)$（对所有类别相同），直接比大小

$$
\hat{y} = \underset{y \in \{1,\ldots,C\}}{\arg\max} \; P(y) \cdot \prod_{i=1}^{d} P(x_i \mid y)
$$

实际计算取对数（避免浮点下溢）：

$$
\hat{y} = \underset{y}{\arg\max} \left[ \log P(y) + \sum_{i=1}^{d} \log P(x_i \mid y) \right]
$$

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Eq. 9.3

**推导过程：**

$$
\text{Step 1: 代入条件独立} \quad P(y \mid x) \propto P(y) \cdot \prod_i P(x_i \mid y)
$$
$$
\text{Step 2: 取 argmax（单调）} \quad \hat{y} = \arg\max_y \; P(y) \cdot \prod_i P(x_i \mid y)
$$
$$
\text{Step 3: 取 log（单调递增）} \quad \hat{y} = \arg\max_y \left[\log P(y) + \sum_i \log P(x_i \mid y)\right]
$$

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `_joint_log_likelihood()` L533-L545

---

### 公式 4: GaussianNB 似然

**直觉：** 每个特征在每个类别下服从独立正态分布，参数从训练数据估计

$$
P(x_i \mid y = c) = \frac{1}{\sqrt{2\pi\sigma_{ic}^2}} \exp\!\left(-\frac{(x_i - \mu_{ic})^2}{2\sigma_{ic}^2}\right)
$$

参数估计（MLE）：

$$
\mu_{ic} = \frac{1}{N_c} \sum_{n: y_n=c} x_{ni}, \qquad \sigma_{ic}^2 = \frac{1}{N_c} \sum_{n: y_n=c} (x_{ni} - \mu_{ic})^2 + \epsilon
$$

其中 $\epsilon$ 为 `var_smoothing` 防止方差为零。

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `_update_mean_variance()` L288-L360

---

### 公式 5: Laplace 平滑（MultinomialNB）

**直觉：** 给每个词的计数加 α，防止未见词导致整个概率乘积为零

$$
P(x_i = v \mid y = c) = \frac{N_{icv} + \alpha}{N_c + \alpha \cdot |V|}
$$

其中 $N_{icv}$ 是类别 $c$ 中特征 $i$ 取值 $v$ 的计数，$|V|$ 是词汇量。

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.2.3

---

## 公式关系图

```
贝叶斯定理 (公式1)
        │
        ▼
条件独立分解 (公式2) ──→ MAP 决策规则 (公式3) ──→ 预测 ŷ
        │
        ├──→ GaussianNB 似然 (公式4)  [连续特征]
        │        参数: μ, σ²
        │
        └──→ MultinomialNB 似然 (公式5 平滑)  [离散计数]
                 参数: θ_icv (词频)
```

---

## 手算练习

### 练习 1: 垃圾邮件分类（MultinomialNB）

**题目：** 训练集：3 封正常邮件 (ham)，2 封垃圾邮件 (spam)。词汇表 = {钱, 免费, 会议}。

| 邮件 | 类别 | 钱 | 免费 | 会议 |
|------|------|---|------|------|
| 1 | ham  | 0 | 0  | 1 |
| 2 | ham  | 0 | 0  | 2 |
| 3 | ham  | 1 | 0  | 0 |
| 4 | spam | 2 | 1  | 0 |
| 5 | spam | 1 | 2  | 0 |

新邮件: x = {钱:1, 免费:1, 会议:0}，预测类别？（α=1）

**解答步骤：**

1. **先验**：P(ham) = 3/5 = 0.6，P(spam) = 2/5 = 0.4

2. **词频统计**（ham 总词数 = 0+0+1+0+0+2+1+0+0 = 4，spam 总词数 = 2+1+0+1+2+0 = 6）：

   P(钱|ham) = (0+0+1 + 1) / (4 + 3) = 2/7
   P(免费|ham) = (0+0+0 + 1) / (4 + 3) = 1/7
   P(钱|spam) = (2+1 + 1) / (6 + 3) = 4/9
   P(免费|spam) = (1+2 + 1) / (6 + 3) = 4/9

3. **log 后验**：

   log P(ham|x) ∝ log(0.6) + log(2/7) + log(1/7) = -0.51 + (-1.25) + (-1.95) = **-3.71**
   log P(spam|x) ∝ log(0.4) + log(4/9) + log(4/9) = -0.92 + (-0.81) + (-0.81) = **-2.54**

4. **结果**：log P(spam|x) > log P(ham|x)，预测为 **spam** ✅

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.3 例题改编

### 练习 2: GaussianNB 分类（鸢尾花）

**题目：** 两类花，特征 = 花瓣长度。setosa: μ=1.5, σ²=0.1；versicolor: μ=4.3, σ²=0.2。先验均匀 P(c)=0.5。查询 x=2.5 属于哪类？

**解答步骤：**

1. log P(setosa|x=2.5) ∝ log(0.5) + log N(2.5; 1.5, 0.1)
   = -0.693 + [-0.5·log(2π·0.1) - (2.5-1.5)²/(2·0.1)]
   = -0.693 + [-0.919 - 5] = **-6.61**

2. log P(versicolor|x=2.5) ∝ log(0.5) + log N(2.5; 4.3, 0.2)
   = -0.693 + [-0.5·log(2π·0.2) - (2.5-4.3)²/(2·0.2)]
   = -0.693 + [-1.264 - 8.1] = **-10.06**

3. **结果**：setosa 的 log 后验更大，预测为 **setosa** ✅

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.3 例子改编

---

## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------|
| 贝叶斯定理 | $P(y\|x) = P(x\|y)P(y)/P(x)$ | 后验推导 | 无 |
| 朴素独立分解 | $P(x\|y) = \prod_i P(x_i\|y)$ | 简化似然计算 | 贝叶斯定理 |
| MAP 预测（log） | $\hat{y} = \arg\max[\log P(y) + \sum_i \log P(x_i\|y)]$ | 分类决策 | 独立分解 |
| Gaussian 似然 | $\mathcal{N}(x_i; \mu_{ic}, \sigma_{ic}^2)$ | 连续特征 | 公式3 |
| Laplace 平滑 | $(N_{icv}+\alpha)/(N_c+\alpha\|V\|)$ | 防零概率 | 公式3 |
| 先验估计 | $\hat{\pi}_c = N_c / N$ | 类别先验 | 无 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9 总结表
