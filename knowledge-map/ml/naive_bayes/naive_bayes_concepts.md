---
topic: naive_bayes
dimension: concepts
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv:1410.5329 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Docs: scikit-learn Naive Bayes — https://scikit-learn.org/stable/modules/naive_bayes.html"
expiry: 12m
status: current
---

# Naive Bayes 核心概念

> 📚 Book: Murphy, [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.9
> 📖 Paper: Raschka, [Naive Bayes and Text Classification I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf)

---

## 术语定义

### 生成式分类器 (Generative Classifier)

生成式分类器对**联合分布 P(x, y) = P(x|y) · P(y)** 建模，先学习"每个类别长什么样"，再用贝叶斯定理反推"给定样本最可能是哪个类"。朴素贝叶斯是最简单的生成式分类器。

> 易混淆：**生成式 vs 判别式** — 判别式分类器（如 Logistic Regression）直接建模 P(y|x)，不关心 x 本身的分布；生成式则先建模 P(x|y)。生成式需要更多假设，但能做密度估计和数据生成

### 朴素性假设 (Naive Independence Assumption)

在给定类别标签 y 的条件下，所有特征 x₁, x₂, ..., xₙ **相互条件独立**：

P(x₁, x₂, ..., xₙ | y) = P(x₁|y) · P(x₂|y) · ... · P(xₙ|y)

这让联合似然从指数级参数降为线性级，是"朴素"的来源。现实中几乎不成立，但实践效果出奇地好。

> 易混淆：**条件独立 vs 无条件独立** — 特征之间无条件时可能高度相关（如词"优秀"和"推荐"），但在 given y=垃圾邮件 的条件下，NB 视其为独立。这是强假设，不是事实

### 先验概率 (Prior Probability) P(y)

在观察任何特征之前，对类别 y 的初始信念。通常从训练集中计算：P(y=c) = 该类样本数 / 总样本数。

> 易混淆：**先验 vs 后验** — 先验是未看数据前的信念；后验 P(y|x) 是看了数据 x 之后更新的信念。贝叶斯定理就是从先验到后验的桥梁

### 似然 (Likelihood) P(x|y)

给定类别 y，观测到特征 x 的概率。这是 NB 各变体的**核心差异所在**：
- **GaussianNB**: P(xᵢ|y) = 正态分布（连续特征）
- **MultinomialNB**: P(xᵢ|y) = 多项分布（词频计数）
- **BernoulliNB**: P(xᵢ|y) = 伯努利分布（0/1 二值特征）
- **CategoricalNB**: P(xᵢ|y) = 类别分布（有限离散类别）

> 易混淆：**似然 vs 概率** — P(x|y) 作为 x 的函数叫"概率"；作为 y 的函数（看待固定 x 时不同 y 下的值）叫"似然"。MLE 最大化似然

### MAP 决策规则 (Maximum A Posteriori)

预测时选后验概率最大的类别：

ŷ = argmax_y P(y|x) = argmax_y [P(y) · ∏ P(xᵢ|y)]

实际计算用**对数形式**避免下溢：

ŷ = argmax_y [log P(y) + Σ log P(xᵢ|y)]

> 易混淆：**MAP vs MLE** — MLE 忽略先验（等价于均匀先验的 MAP）；MAP 乘了先验，是贝叶斯框架下的最大化。NB 默认用 MAP

### 拉普拉斯平滑 (Laplace Smoothing / Add-α Smoothing)

在计数中加入伪计数 α（默认 α=1）避免零概率问题：

P(xᵢ=v | y=c) = (count(xᵢ=v, y=c) + α) / (count(y=c) + α·|V|)

其中 |V| 是特征值的词汇量大小。

> 易混淆：**Laplace(α=1) vs Lidstone(α<1)** — 两者都是 add-α 平滑，只是 α 值不同。scikit-learn 的 `alpha` 参数即为 Lidstone/Laplace 的 α

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.3
> 📖 Paper: Raschka, [Naive Bayes I](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf), Sec.2

---

## 概念辨析

### GaussianNB vs MultinomialNB vs BernoulliNB

| 维度 | GaussianNB | MultinomialNB | BernoulliNB |
|------|-----------|--------------|------------|
| **特征类型** | 连续实数 | 非负整数计数 | 0/1 二值 |
| **似然模型** | 正态分布 | 多项分布 | 伯努利分布 |
| **典型场景** | 鸢尾花分类、医疗数据 | TF 文本分类（词频） | 二值特征文本（词是否出现） |
| **参数学习** | 均值 μ + 方差 σ² | 词频归一化 θ | 出现概率 p |
| **负值支持** | ✅ | ❌（需非负） | ❌（只有0/1） |
| **稀疏数据** | ❌ 效果一般 | ✅ 很好 | ✅ 很好 |

> 📖 Docs: [scikit-learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

### 朴素贝叶斯 vs Logistic Regression

| 维度 | Naive Bayes | Logistic Regression |
|------|-------------|---------------------|
| **模型类型** | 生成式 | 判别式 |
| **假设** | 特征条件独立（强） | 线性决策边界（弱） |
| **小数据集** | ✅ 效果好（参数少） | ❌ 容易过拟合 |
| **大数据集** | ❌ 独立假设造成偏差 | ✅ 渐近更优 |
| **训练速度** | ✅ O(nd) 极快 | 需要迭代优化 |
| **输出概率** | 校准性差（过于自信） | 校准性好 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.4 — 生成 vs 判别模型的偏差-方差权衡

---

## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                     Naive Bayes 架构                          │
├──────────────────────────────────────────────────────────────┤
│  训练阶段                                                     │
│  ├─ 估计先验: P(y=c) = Nc / N  (各类样本比例)                │
│  └─ 估计似然: P(xᵢ | y=c)                                    │
│      ├─ GaussianNB: 计算每类每特征的 μ, σ²                   │
│      ├─ MultinomialNB: 计算词频 + Laplace 平滑               │
│      └─ BernoulliNB: 计算二值出现概率 + 平滑                  │
├──────────────────────────────────────────────────────────────┤
│  预测阶段                                                     │
│  └─ MAP 推断: ŷ = argmax_y [log P(y) + Σ log P(xᵢ|y)]       │
│      ├─ 数值稳定: 使用 log 避免下溢                           │
│      └─ 输出: 类别标签 + 后验概率（已归一化）                 │
└──────────────────────────────────────────────────────────────┘
```

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) `_joint_log_likelihood()` 方法

### 适用场景 ✅

- 文本分类（垃圾邮件过滤、情感分析、新闻分类）
- 特征数量多但样本量小的场景（高维稀疏）
- 需要增量在线学习（`partial_fit` 支持）
- 需要快速基线模型（训练极快）
- 多分类问题（天然支持，无需 One-vs-Rest）
- 实时预测（推理极快，无需矩阵运算）

### 不适用场景 ❌

- 特征高度相关的场景（违反独立假设，输出概率不准）
- 需要精确概率校准的场景（输出倾向于极端值 0 或 1）
- 连续特征不服从正态分布时慎用 GaussianNB
- 特征间存在明确交互效应的场景（如 x₁ AND x₂ 共同决定标签）

> 📖 Paper: Vidhya & Aghila, [Survey of Naive Bayes](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf), Sec.3

---

## 速查表

| 项 | 说明 | 示例值 |
|-----|------|--------|
| 先验估计 | P(y=c) = Nc/N | 垃圾邮件占 30% → P(spam)=0.3 |
| Gaussian 似然 | N(μ_c, σ²_c) 每类每特征独立 | 花瓣长度均值/方差 |
| Multinomial 平滑 | (count + α) / (total + α·\|V\|) | α=1，词汇量=1000 |
| 预测公式（log） | log P(y) + Σ log P(xᵢ\|y) | 选最大对数后验 |
| `alpha` 参数 | Laplace/Lidstone 平滑量 | 默认 1.0 |
| `var_smoothing` | GaussianNB 方差稳定化 | 默认 1e-9 |
| `fit_prior` | 是否从数据估计先验 | 默认 True |
| 支持增量学习 | `partial_fit()` | 流式数据场景 |

> 📖 Docs: [scikit-learn NB API](https://scikit-learn.org/stable/modules/naive_bayes.html)
