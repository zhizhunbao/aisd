---
topic: naive_bayes
dimension: tutorial
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv:1410.5329 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
  - "📖 Paper: Vidhya & Aghila, 'A Survey of Naive Bayes in Text Document Classification', arXiv:1007.1669 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf"
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn Naive Bayes — https://scikit-learn.org/stable/modules/naive_bayes.html"
expiry: 12m
status: current
---

# Naive Bayes 教程

> **前置知识：** 条件概率、贝叶斯定理、基本概率分布（正态/多项/伯努利）
> **参考来源：** [Raschka 2014](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf) | [Murphy PML1 Ch.9](../../../textbooks/murphy_pml1.pdf) | [scikit-learn 文档](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

## Section 0: 前置知识速查

1. **条件概率 P(A|B)**：已知 B 发生，A 发生的概率。P(A|B) = P(A,B)/P(B)
2. **贝叶斯定理**：P(y|x) = P(x|y)·P(y) / P(x)——把"结果→原因"转化为"原因→结果"
3. **最大似然估计(MLE)**：从数据中估计参数，使数据出现的概率最大
4. **概率分布**：正态分布（连续），多项分布（计数），伯努利分布（0/1二值）
5. **对数技巧**：log(a·b) = log a + log b，避免多个小概率相乘的浮点下溢

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.2-3 前置概率基础

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **直接估计 P(y|x) 极其困难**：如果 x 有 1000 个二值特征，P(y|x) 的参数空间是 2¹⁰⁰⁰，根本无法估计
- 🔥 **判别模型需要大量数据**：Logistic Regression 在小数据集上容易过拟合，垃圾邮件过滤初期样本少
- 🔥 **新词汇问题**：测试时遇到训练中没见过的词，朴素的频率估计会得到 P=0，使整个计算崩溃

### 它的核心价值

1. **急剧降低参数量**：条件独立假设把参数从指数级降到线性级（d 个参数而非 2^d 个）
2. **小数据集下有效**：参数少 → 难过拟合，10 条训练样本也能用
3. **零频率问题有解**：Laplace 平滑优雅解决未见特征的零概率问题
4. **增量在线学习**：服从指数族分布的参数可以按批次累积，不必重新训练

> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.1 — 为什么文本分类需要朴素贝叶斯
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.1 — 生成模型的动机

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌───────────────────────────────────────────────────────────────────────┐
│                     Naive Bayes 完整流程                               │
├───────────────────────────────────────────────────────────────────────┤
│  训练阶段 (fit)                                                        │
│                                                                       │
│  训练数据 (X, y)                                                      │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────────────────────────┐                             │
│  │ Step 1: 统计先验 P(y=c) = Nc/N      │                             │
│  └─────────────────────────────────────┘                             │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────────────────────────┐                             │
│  │ Step 2: 估计似然参数                │                             │
│  │  Gaussian: 计算每类每特征的 μ, σ²   │                             │
│  │  Multinomial: 计算+平滑词频         │                             │
│  │  Bernoulli: 计算+平滑出现概率       │                             │
│  └─────────────────────────────────────┘                             │
│                                                                       │
├───────────────────────────────────────────────────────────────────────┤
│  预测阶段 (predict)                                                    │
│                                                                       │
│  新样本 x                                                             │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────────────────────────┐                             │
│  │ 对每个类别 c 计算:                   │                             │
│  │  log P(c) + Σᵢ log P(xᵢ|c)          │──→ [−3.2, −8.1, −5.4]     │
│  └─────────────────────────────────────┘                             │
│       │                                                               │
│       ▼                                                               │
│  ┌─────────────────────────────────────┐                             │
│  │ argmax → ŷ = class 0               │                             │
│  └─────────────────────────────────────┘                             │
└───────────────────────────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `fit()` + `predict()` 方法

### 2.2 为什么用对数？不能直接乘概率？

**为什么乘很多个小概率会崩溃？**

1000 个特征，每个 P(xᵢ|y) ≈ 0.01，则：

$$
\prod_{i=1}^{1000} 0.01 = 10^{-2000} \approx 0 \quad \text{（64位浮点数无法表示）}
$$

改用对数后：

$$
\sum_{i=1}^{1000} \log(0.01) = 1000 \times (-4.6) = -4600 \quad \text{（完全可表示）}
$$

**关键**：`argmax` 操作在对数变换下不改变结果，因为 $\log$ 是单调递增函数。

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) L537-L545 `_joint_log_likelihood`

### 2.3 为什么朴素假设通常"有效"，尽管现实中不成立？

直觉解释：即使特征相关，MAP 决策边界 (P(y=1|x) = P(y=0|x)) 的位置往往与真实贝叶斯最优边界相近。Ng & Jordan (2002) 从理论上证明：NB 以**指数级更快**的速度从少量样本中学到好的决策规则，尽管渐近准确率不如 Logistic Regression。

```
小样本区间:                 大样本区间:
NB 准确率 > LR 准确率       LR 准确率 > NB 准确率
(低方差,高偏差胜出)          (低偏差,大数据胜出)
```

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.4 — Ng & Jordan 2002 生成 vs 判别对比

### 2.4 各变体的似然建模

```
特征类型                NB 变体              似然 P(xᵢ|y)
┌────────────┐         ┌───────────────┐    ┌──────────────────────┐
│ 连续实数    │────────→│  GaussianNB   │───→│ N(μ_ic, σ²_ic)       │
└────────────┘         └───────────────┘    └──────────────────────┘
┌────────────┐         ┌───────────────┐    ┌──────────────────────┐
│ 词频计数    │────────→│ MultinomialNB │───→│ θ_icv（归一化+平滑）  │
└────────────┘         └───────────────┘    └──────────────────────┘
┌────────────┐         ┌───────────────┐    ┌──────────────────────┐
│ 词是否出现  │────────→│  BernoulliNB  │───→│ p_ic（伯努利参数）    │
└────────────┘         └───────────────┘    └──────────────────────┘
┌────────────┐         ┌───────────────┐    ┌──────────────────────┐
│ 有限离散类别│────────→│ CategoricalNB │───→│ 类别概率表（+平滑）   │
└────────────┘         └───────────────┘    └──────────────────────┘
```

> 📖 Docs: [scikit-learn NB 变体](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

## Section 3: 局限性

1. **条件独立假设经常被违反** → 概率输出过于极端（趋向 0 或 1），不能作为校准概率使用；结合 [CalibratedClassifierCV](https://scikit-learn.org/stable/modules/calibration.html) 可改善
2. **GaussianNB 对分布敏感** → 若特征不服从正态分布（如指数分布、双峰分布），效果下降 → 用 MultinomialNB 或先做 Box-Cox 变换
3. **错误类型选择代价相同** → NB 最小化错误率，不能针对不同误分类代价优化 → 需要在后处理调整决策阈值
4. **高度相关特征会被重复计数** → 两个几乎相同的特征会让 NB "看"两次同一信息 → 特征选择或降维可缓解

> 📖 Paper: Vidhya & Aghila, [Survey of Naive Bayes](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf), Sec.4 局限性分析

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Naive Bayes** | 训练极快、小数据集有效、增量学习 | 独立假设偏差、概率校准差 | 文本分类、快速基线、流式数据 |
| **Logistic Regression** | 概率校准好、无强假设 | 需要更多数据、不支持增量 | 特征相关、需要精确概率输出 |
| **SVM** | 高维效果好、核技巧灵活 | 不输出概率、训练慢 | 高维分类，不需要概率 |
| **Random Forest** | 特征相关鲁棒、准确率高 | 训练慢、不可解释 | 结构化数据、高准确率需求 |
| **LDA** | 考虑特征协方差 | 假设高斯且同方差 | 特征服从多元正态 |

> 📖 Paper: Vidhya & Aghila, [Survey](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf), Sec.5 对比分析
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.4

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [Raschka 2014](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf) | 📖 论文 | Section 1（动机）、Section 2.2/2.3（原理解释） |
| [Vidhya & Aghila 2010](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf) | 📖 论文 | Section 3（局限性）、Section 4（对比） |
| [《PML1》Ch.9](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 全文数学框架 |
| [scikit-learn NB](https://scikit-learn.org/stable/modules/naive_bayes.html) | 📖 官方文档 | Section 2（实现细节） |
| [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) | 💻 源码 | Section 2.1 流程图、2.2 log 计算 |
