# 概率图模型 Probabilistic Graphical Models

> 名词总表 · 来源：Koller & Friedman《Probabilistic Graphical Models》· CMU 10-708 · Jordan《Introduction to PGM》
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 基础概率 Probability Foundations

| 名词 | 英文 |
|------|------|
| 联合分布 | Joint Distribution |
| 条件分布 | Conditional Distribution |
| 边缘化 | Marginalization |
| 贝叶斯定理 | Bayes' Theorem |
| 条件独立 | Conditional Independence |
| 指数族分布 | Exponential Family |
| 充分统计量 | Sufficient Statistics |
| 共轭先验 | Conjugate Prior |

---

### 有向图模型 Directed Graphical Models (Bayesian Networks)

| 名词 | 英文 |
|------|------|
| 贝叶斯网络 | Bayesian Network (BN) |
| 有向无环图 | DAG (Directed Acyclic Graph) |
| 条件概率表 | CPT (Conditional Probability Table) |
| 父节点 / 子节点 | Parent / Child Node |
| d-分离 | d-Separation |
| 活跃路径 | Active Trail |
| 因果推断 | Causal Inference |
| 朴素贝叶斯 | Naive Bayes |
| 隐马尔可夫模型 | HMM (Hidden Markov Model) |
| 卡尔曼滤波 | Kalman Filter |
| 动态贝叶斯网络 | Dynamic Bayesian Network |
| 板块表示 | Plate Notation |

---

### 无向图模型 Undirected Graphical Models (Markov Random Fields)

| 名词 | 英文 |
|------|------|
| 马尔可夫随机场 | MRF (Markov Random Field) |
| 势函数 | Potential Function |
| 团 | Clique |
| 极大团 | Maximal Clique |
| 配分函数 | Partition Function Z |
| 吉布斯分布 | Gibbs Distribution |
| 对数线性模型 | Log-Linear Model |
| 条件随机场 | CRF (Conditional Random Field) |
| 伊辛模型 | Ising Model |
| 马尔可夫毯 | Markov Blanket |
| Hammersley-Clifford 定理 | Hammersley-Clifford Theorem |
| 因子图 | Factor Graph |

---

### 精确推断 Exact Inference

| 名词 | 英文 |
|------|------|
| 变量消除 | Variable Elimination |
| 消除顺序 | Elimination Ordering |
| 信念传播 | Belief Propagation (BP) |
| 和积算法 | Sum-Product Algorithm |
| 最大积算法 | Max-Product Algorithm |
| 联合树算法 | Junction Tree Algorithm |
| 团树 | Clique Tree |
| 前向-后向算法 | Forward-Backward Algorithm |
| Viterbi 算法 | Viterbi Algorithm |
| 树宽 | Treewidth |
| 消息传递 | Message Passing |

---

### 近似推断 Approximate Inference

| 名词 | 英文 |
|------|------|
| 变分推断 | Variational Inference (VI) |
| 均值场近似 | Mean Field Approximation |
| 证据下界 | ELBO (Evidence Lower Bound) |
| KL 散度最小化 | KL Divergence Minimization |
| 期望传播 | Expectation Propagation (EP) |
| 环路信念传播 | Loopy Belief Propagation |
| Bethe 自由能 | Bethe Free Energy |
| 变分 EM | Variational EM |
| 摊销推断 | Amortized Inference |
| 黑盒变分推断 | Black-Box VI |
| 随机变分推断 | Stochastic VI |

---

### 蒙特卡洛推断 Monte Carlo Inference

| 名词 | 英文 |
|------|------|
| 蒙特卡洛采样 | Monte Carlo Sampling |
| 重要性采样 | Importance Sampling |
| 拒绝采样 | Rejection Sampling |
| MCMC | Markov Chain Monte Carlo |
| Metropolis-Hastings | Metropolis-Hastings Algorithm |
| 吉布斯采样 | Gibbs Sampling |
| 哈密顿蒙特卡洛 | HMC (Hamiltonian Monte Carlo) |
| NUTS | No-U-Turn Sampler |
| 粒子滤波 | Particle Filter (Sequential MC) |
| 混合时间 | Mixing Time |
| 遍历性 | Ergodicity |
| 自相关 | Autocorrelation |
| 收敛诊断 | Convergence Diagnostics |

---

### 学习 Learning

| 名词 | 英文 |
|------|------|
| 参数学习 | Parameter Learning |
| 最大似然估计 | MLE (Maximum Likelihood Estimation) |
| 最大后验估计 | MAP (Maximum A Posteriori) |
| 完全数据 vs 不完全数据 | Complete vs Incomplete Data |
| EM 算法 | EM (Expectation-Maximization) Algorithm |
| E 步 / M 步 | E-step / M-step |
| 结构学习 | Structure Learning |
| 评分搜索 | Score-Based Search |
| BIC / AIC | Bayesian / Akaike Information Criterion |
| 约束搜索 | Constraint-Based Search |
| PC 算法 | PC Algorithm |
| 因果发现 | Causal Discovery |

---

### 深度生成模型 Deep Generative Models

| 名词 | 英文 |
|------|------|
| 变分自编码器 | VAE (Variational Autoencoder) |
| 重参数化技巧 | Reparameterization Trick |
| 生成对抗网络 | GAN (Generative Adversarial Network) |
| 正规化流 | Normalizing Flow |
| 扩散模型 | Diffusion Model |
| 自回归模型 | Autoregressive Model |
| 受限玻尔兹曼机 | RBM (Restricted Boltzmann Machine) |
| 深度信念网络 | DBN (Deep Belief Network) |
| 能量模型 | Energy-Based Model (EBM) |
| 基于分数的模型 | Score-Based Model |

---

### 因果推断 Causal Inference

| 名词 | 英文 |
|------|------|
| 因果图 | Causal Graph |
| 干预 | Intervention (do-Calculus) |
| 反事实 | Counterfactual |
| 因果效应 | Causal Effect |
| 后门准则 | Back-Door Criterion |
| 前门准则 | Front-Door Criterion |
| 工具变量 | Instrumental Variable |
| 结构因果模型 | SCM (Structural Causal Model) |
| 平均处理效应 | ATE (Average Treatment Effect) |

---

### 工具 Tools

| 名词 | 英文 |
|------|------|
| PyMC | PyMC (Probabilistic Programming) |
| Stan | Stan |
| Edward / Edward2 | Edward / Edward2 |
| Pyro | Pyro (Uber AI) |
| NumPyro | NumPyro |
| pgmpy | pgmpy (Python PGM Library) |
| pomegranate | pomegranate |
