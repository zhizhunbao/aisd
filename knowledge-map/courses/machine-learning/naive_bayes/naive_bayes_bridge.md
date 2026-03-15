---
topic: naive_bayes
dimension: bridge
created: 2026-03-13
last_verified: 2026-03-13
source_versions:
  - "📚 Book: Murphy, 《Probabilistic Machine Learning: An Introduction》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Paper: Raschka, 'Naive Bayes and Text Classification I', arXiv:1410.5329 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf"
expiry: 12m
status: current
---

# Naive Bayes 衔接与扩展

> 📚 Book: Murphy, [《Probabilistic Machine Learning: An Introduction》](../../../textbooks/murphy_pml1.pdf), Ch.9

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 贝叶斯定理 / 条件概率 | NB 的数学根基 | — |
| ← 前置 | 概率分布（正态/多项/伯努利） | NB 似然建模所用的分布族 | — |
| ← 前置 | 最大似然估计 (MLE) | NB 参数估计方法 | — |
| → 后续 | LDA / QDA（线性/二次判别分析） | 放弃独立假设，用完整协方差矩阵 | [ml/lda 未建立] |
| → 后续 | 贝叶斯网络 (Bayesian Network) | NB 是最简单的贝叶斯网络（星形结构） | — |
| → 后续 | 逻辑回归 (Logistic Regression) | NB 的判别式对应物（相同线性边界，不同假设） | — |
| → 后续 | LDA 主题模型 | 从 NB 的词袋扩展到文档-主题-词的三层生成模型 | — |
| → 后续 | 文本特征工程 | TF-IDF、词袋、n-gram 是 NB 的标准前处理 | — |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9.4 — NB 与 LR 的理论关系

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 Naive Bayes 中如何使用 |
|---------|-----------|------------------------|
| 概率论基础 | 贝叶斯定理 P(y\|x) = P(x\|y)P(y)/P(x) | NB 的核心推断框架 |
| 概率论基础 | 条件独立性 | 朴素假设，使联合似然可分解 |
| 统计学习 | 最大似然估计 (MLE) | 从训练数据估计 μ, σ², θ 等参数 |
| 统计学习 | 正则化（平滑） | Laplace/Lidstone 平滑防零概率 |
| 概率分布 | 高斯分布 N(μ, σ²) | GaussianNB 的似然建模 |
| 概率分布 | 多项分布 Multinomial | MultinomialNB 的词频建模 |
| 概率分布 | 伯努利分布 Bernoulli | BernoulliNB 的 0/1 特征建模 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.2-3 概率基础

---

## 下游影响

| 去向主题 | NB 提供的概念 | 在下游如何被使用 |
|---------|-------------|---------------|
| 贝叶斯网络 | 条件独立图结构 | NB 是星形贝叶斯网；BN 推广到任意 DAG |
| LDA 主题模型 | 词袋生成思想 | LDA 把 NB 单一类别扩展为混合主题分布 |
| 垃圾邮件过滤 | MultinomialNB 词频建模 | 工业界标准方案：词袋 + MultinomialNB |
| 文本情感分析 | NB 快速基线 | 新任务的 baseline，先跑 NB 再优化 |
| 在线学习系统 | partial_fit 增量更新 | 流式 NLP 系统不需要每次重训练全模型 |
| 朴素贝叶斯网络 | 条件独立分解 | NLP 中的序列标注中作为特征独立近似 |

> 📖 Paper: Vidhya & Aghila, [Survey](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf), Sec.5 — NB 的下游应用综述

---

## 概念演变追踪

| 概念 | 在早期（1990s） | 在现代（2020s） | 变化原因 |
|------|--------------|--------------|--------|
| 似然建模 | 主要用 BernoulliNB（词是否出现） | MultinomialNB + TF-IDF 为主 | 词频信息提升准确率 |
| 平滑方式 | Laplace (α=1) 唯一选择 | Lidstone（可调 α<1）为主 | 超参调优改善泛化 |
| 概率输出 | 直接用 predict_proba | 加 CalibratedClassifierCV 后处理 | 实践发现 NB 概率极端化 |
| 文本不平衡 | 标准 MultinomialNB | ComplementNB 已是默认选择 | Rennie et al. 2003 证明更优 |
| 训练方式 | 批量一次 fit | partial_fit 增量学习成标准 | 大规模流式数据场景需求 |

> 💻 Source: [sklearn/naive_bayes.py](../../../.github/scikit-learn/sklearn/naive_bayes.py) — 版本演进可见 git history

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Murphy PML1 Ch.9](../../../textbooks/murphy_pml1.pdf) | 📚 教科书 | 贝叶斯推断框架的完整数学，NB 作为生成模型的统一视角 | ⭐⭐⭐ |
| [Raschka 2014 arXiv:1410.5329](../../../.documents/papers/naive_bayes/raschka_2014_naive_bayes_text_classification.pdf) | 📖 论文 | 最清晰的 NB 文本分类教程，含伯努利/多项模型对比 | ⭐⭐ |
| [Ng & Jordan NIPS 2002](https://arxiv.org/abs/cs/0212023) | 📖 论文 | 理论证明 NB vs LR 偏差-方差权衡，数据量阈值分析 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Vidhya & Aghila 2010](../../../.documents/papers/naive_bayes/vidhya_2010_naive_bayes_text_classification_survey.pdf) | NB 各变体的横向比较 + 与其他分类器对比 | 选型时 |
| [scikit-learn 分类器比较](https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html) | NB vs SVM vs RF vs LR 可视化结果 | 快速选型时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Rennie et al. 2003 ICML](https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf) | ComplementNB 提出论文，针对不平衡文本 | 文本不平衡问题时 |
| [Paul Graham "A Plan for Spam" 2002](http://www.paulgraham.com/spam.html) | NB 在工业垃圾邮件过滤中的实践 | 了解工程应用时 |

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.9 参考文献

---

## 与工作区已有知识库的关联

| 类别 | 关联知识库 | 关联说明 |
|------|----------|--------|
| 同领域生成模型 | [ml/lof](../lof/) | LOF 是密度估计，NB 是概率生成，共同点：对数据分布做假设 |
| 同领域分类器 | [ml/svm](../svm/) | SVM（判别式）vs NB（生成式）— 互补对比，选型时对照看 |
| 同领域分类器 | [ml/knn](../knn/) | KNN（非参数化）vs NB（参数化）— 假设量的对立面 |
| 聚类（无监督对应） | [ml/kmeans](../kmeans/) | K-Means 可看作高斯 NB 的无标签版本（EM思路） |
| 深度学习连接 | [deep-learning/](../../deep-learning/) | 深度生成模型 VAE/GAN 是 NB 生成思想的深度延伸 |
