# Math Foundations | 数学基础

> 跨课程共享的数学前置知识，从教科书提取，每个公式都有出处。
> Shared math prerequisites across all courses. Every formula has a textbook citation.

## 📚 Files

### Linear Algebra (线性代数)

| File                                                      | Topic          | Lines | Course Dependencies |
| --------------------------------------------------------- | -------------- | ----- | ------------------- |
| [vectors_matrices.md](linear-algebra/vectors_matrices.md) | 向量与矩阵运算 | ~130  | CNN(W3), RNN(W4)    |
| [inner_product.md](linear-algebra/inner_product.md)       | 内积           | ~213  | SVM(W2)             |
| [norms_distances.md](linear-algebra/norms_distances.md)   | 范数与距离度量 | ~330  | K-Means(W6), KNN    |
| [eigenvalues_svd.md](linear-algebra/eigenvalues_svd.md)   | 特征值与 SVD   | ~150  | PCA                 |

### Calculus (微积分)

| File                                                        | Topic              | Lines | Course Dependencies  |
| ----------------------------------------------------------- | ------------------ | ----- | -------------------- |
| [derivatives.md](calculus/derivatives.md)                   | 导数与偏导数       | ~120  | All training         |
| [chain_rule_gradients.md](calculus/chain_rule_gradients.md) | 链式法则与梯度     | ~126  | CNN-BP(W3), BPTT(W4) |
| [geometric_series.md](calculus/geometric_series.md)         | 几何级数与折扣回报 | ~130  | RL(W1), all RL weeks |

### Probability (概率论)

| File                                                                 | Topic           | Lines | Course Dependencies     |
| -------------------------------------------------------------------- | --------------- | ----- | ----------------------- |
| [conditional_probability.md](probability/conditional_probability.md) | 条件概率        | ~248  | NB(W5), RL(W1)          |
| [bayes_theorem.md](probability/bayes_theorem.md)                     | 贝叶斯定理      | ~174  | NB(W5), BBN(W5)         |
| [markov_chains.md](probability/markov_chains.md)                     | 马尔可夫链与MDP | ~120  | RL(W1-W2), all RL weeks |
| [cross_entropy.md](probability/cross_entropy.md)                     | 交叉熵与信息论  | ~140  | MV Assignment 1, ML(W4) |

### Statistics (统计学)

| File                                                            | Topic            | Lines | Course Dependencies     |
| --------------------------------------------------------------- | ---------------- | ----- | ----------------------- |
| [mean_variance.md](statistics/mean_variance.md)                 | 均值/方差/标准差 | ~260  | Preprocessing(W1), all  |
| [gaussian_distribution.md](statistics/gaussian_distribution.md) | 高斯分布         | ~132  | NB-Gaussian(W5), EM(W6) |
| [mle.md](statistics/mle.md)                                     | 最大似然估计     | ~248  | NB(W5), EM(W6)          |

### Optimization (最优化)

| File                                                            | Topic        | Lines | Course Dependencies |
| --------------------------------------------------------------- | ------------ | ----- | ------------------- |
| [gradient_descent.md](optimization/gradient_descent.md)         | 梯度下降     | ~210  | CNN(W3), RNN(W4)    |
| [lagrange_multipliers.md](optimization/lagrange_multipliers.md) | 拉格朗日乘子 | ~200  | SVM(W2)             |

### General (通用数学工具)

| File                                     | Topic             | Lines | Course Dependencies     |
| ---------------------------------------- | ----------------- | ----- | ----------------------- |
| [argmax.md](general/argmax.md)           | Argmax 与贪婪选择 | ~100  | RL(W1), ML(W5 MAP)      |
| [convolution.md](general/convolution.md) | 卷积运算          | ~160  | MV(W2,W4), Assignment 1 |

## 📐 Dependency Map (依赖关系)

```
vectors_matrices ──→ inner_product ──→ norms_distances
│
 eigenvalues_svd ◀────┘

derivatives ──→ chain_rule_gradients ──→ gradient_descent
│
lagrange_multipliers ◀┘
geometric_series (独立)

conditional_probability ──→ bayes_theorem
│                       ╲
│                        ╲──→ markov_chains
│
mean_variance ──→ gaussian_distribution ──→ mle
cross_entropy ◀── (依赖 derivatives)

argmax (独立)
convolution (独立，来自信号处理)
```

## 🔗 Course Reading Lists (课程阅读清单)

| Course Week         | Read These First                                                                          |
| ------------------- | ----------------------------------------------------------------------------------------- |
| ML W1 Preprocessing | `mean_variance` ✅                                                                        |
| ML W2 SVM           | `inner_product` ✅ → `lagrange_multipliers` ✅                                            |
| ML W3 CNN           | `vectors_matrices` ✅ → `derivatives` ✅ → `chain_rule_gradients` ✅                      |
| ML W4 RNN           | `chain_rule_gradients` ✅ → `gradient_descent` ✅                                         |
| ML W5 Naive Bayes   | `conditional_probability` ✅ → `bayes_theorem` ✅ → `gaussian_distribution` ✅ → `mle` ✅ |
| ML W6 Clustering    | `mean_variance` ✅ → `norms_distances` ✅ → `gaussian_distribution` ✅ → `mle` ✅         |
| RL W1 RL Intro      | `conditional_probability` ✅ → `markov_chains` ✅ + `geometric_series` ✅ + `argmax` ✅   |
| RL W2 MDP           | `markov_chains` ✅ + `geometric_series` ✅                                                |
| MV Assignment 1     | `convolution` ✅ → `chain_rule_gradients` ✅ → `gradient_descent` ✅ + `cross_entropy` ✅ |

## 📖 Primary Sources

| Book                             | Key        | Chapters Used   |
| -------------------------------- | ---------- | --------------- |
| Mathematics for Machine Learning | MML        | Ch2–5, Ch7, Ch8 |
| Bayesian Reasoning and ML        | Barber     | Ch10            |
| Introduction to Probability      | Grinstead  | Ch4, Ch11       |
| Deep Learning                    | Goodfellow | Ch3             |
| Convex Optimization              | Boyd       | Ch5, Ch9        |
| Reinforcement Learning (2nd ed.) | Sutton     | Ch1–3           |
