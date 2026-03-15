# 高级深度学习 Advanced Deep Learning

> 名词总表 · 来源：CMU 10-707 (Ruslan Salakhutdinov) · Goodfellow《DLBook》· 原始论文 · PyTorch 官方文档
>
> 级别：博士 PhD · 角色：ML 工程师

---

### 概率图模型 Graphical Models

| 名词 | 英文 |
|------|------|
| 有向图模型 | Directed Graphical Models (Bayesian Networks) |
| 无向图模型 | Undirected Graphical Models (Markov Random Fields) |
| 因子图 | Factor Graph |
| 条件独立 | Conditional Independence |
| d-分离 | d-Separation |
| 精确推断 | Exact Inference |
| 变分推断 | Variational Inference |
| 信念传播 | Belief Propagation |
| 期望最大化 | EM (Expectation-Maximization) |
| 指数族分布 | Exponential Family |

---

### 线性因子模型 Linear Factor Models

| 名词 | 英文 |
|------|------|
| 概率主成分分析 | PPCA (Probabilistic PCA) |
| 因子分析 | Factor Analysis (FA) |
| 独立成分分析 | Independent Component Analysis (ICA) |
| 稀疏编码 | Sparse Coding |
| 字典学习 | Dictionary Learning |
| 潜变量 | Latent Variable |
| 低秩近似 | Low-Rank Approximation |

---

### 自编码器 Autoencoders

| 名词 | 英文 |
|------|------|
| 自编码器 | Autoencoder (AE) |
| 降噪自编码器 | Denoising Autoencoder (DAE) |
| 稀疏自编码器 | Sparse Autoencoder |
| 收缩自编码器 | Contractive Autoencoder (CAE) |
| 变分自编码器 | Variational Autoencoder (VAE) |
| β-VAE | β-VAE |
| 重参数化技巧 | Reparameterization Trick |
| 隐空间 | Latent Space |
| 重构损失 | Reconstruction Loss |
| 证据下界 | ELBO (Evidence Lower Bound) |

---

### 基于能量的模型 Energy-Based Models

| 名词 | 英文 |
|------|------|
| 能量函数 | Energy Function |
| 玻尔兹曼机 | Boltzmann Machine |
| 受限玻尔兹曼机 | Restricted Boltzmann Machine (RBM) |
| 深度信念网络 | Deep Belief Network (DBN) |
| 深度玻尔兹曼机 | Deep Boltzmann Machine (DBM) |
| 配分函数 | Partition Function |
| 自由能 | Free Energy |
| 亥姆霍兹机 | Helmholtz Machine |
| 醒眠算法 | Wake-Sleep Algorithm |

---

### 蒙特卡洛方法 Monte Carlo Methods

| 名词 | 英文 |
|------|------|
| 蒙特卡洛采样 | Monte Carlo Sampling |
| 马尔可夫链蒙特卡洛 | MCMC (Markov Chain Monte Carlo) |
| 吉布斯采样 | Gibbs Sampling |
| 重要性采样 | Importance Sampling |
| 退火重要性采样 | Annealed Importance Sampling (AIS) |
| 对比散度 | Contrastive Divergence (CD) |
| 持续对比散度 | Persistent Contrastive Divergence (PCD) |
| 随机最大似然估计 | Stochastic Maximum Likelihood Estimation |
| 混合速率 | Mixing Rate |

---

### 学习与推断技巧 Learning & Inference Techniques

| 名词 | 英文 |
|------|------|
| 分数匹配 | Score Matching |
| 比率匹配 | Ratio Matching |
| 伪似然估计 | Pseudo-Likelihood Estimation |
| 噪声对比估计 | Noise-Contrastive Estimation (NCE) |
| 配分函数估计 | Partition Function Estimation |
| 变分下界 | Variational Lower Bound |
| 均值场近似 | Mean Field Approximation |
| 重要性加权自编码器 | Importance-Weighted Autoencoder (IWAE) |

---

### 深度生成模型 Deep Generative Models

| 名词 | 英文 |
|------|------|
| 生成对抗网络 | GAN (Generative Adversarial Network) |
| Wasserstein GAN | WGAN |
| 生成矩匹配网络 | Generative Moment Matching Network (GMMN) |
| 神经自回归密度估计 | NADE (Neural Autoregressive Density Estimator) |
| 自回归流 | Autoregressive Flow |
| 因果卷积 | Causal Convolution |
| PixelCNN | PixelCNN |
| WaveNet | WaveNet |
| 变分自编码器 | VAE (Variational Autoencoder) |
| 扩散模型 | Diffusion Model |
| 去噪扩散概率模型 | DDPM (Denoising Diffusion Probabilistic Model) |
| 基于分数的生成模型 | Score-Based Generative Model |
| 流匹配 | Flow Matching |
| 正规化流 | Normalizing Flow |
| 可逆网络 | Invertible Network |

---

### 序列建模 Sequence Modeling

| 名词 | 英文 |
|------|------|
| 循环神经网络 | RNN (Recurrent Neural Network) |
| LSTM | Long Short-Term Memory |
| GRU | Gated Recurrent Unit |
| 序列到序列 | Seq2Seq (Sequence-to-Sequence) |
| 注意力机制 | Attention Mechanism |
| 自注意力 | Self-Attention |
| Transformer | Transformer |
| 因果掩码 | Causal Mask |
| 自回归解码 | Autoregressive Decoding |
| 时间卷积网络 | Temporal Convolutional Network (TCN) |

---

### 深度强化学习 Deep Reinforcement Learning

| 名词 | 英文 |
|------|------|
| 深度 Q 网络 | DQN (Deep Q-Network) |
| 策略梯度 | Policy Gradient |
| Actor-Critic | Actor-Critic |
| 近端策略优化 | PPO (Proximal Policy Optimization) |
| 优势函数 | Advantage Function |
| 模型预测控制 | Model Predictive Control (MPC) |
| 世界模型 | World Model |
| 离线强化学习 | Offline RL |
| 逆向强化学习 | Inverse RL |

---

### 高级优化与正则化 Advanced Optimization & Regularization

| 名词 | 英文 |
|------|------|
| 二阶优化 | Second-Order Optimization |
| 自然梯度 | Natural Gradient |
| Fisher 信息矩阵 | Fisher Information Matrix |
| K-FAC | Kronecker-Factored Approximate Curvature |
| 损失曲面分析 | Loss Surface Analysis |
| 锐度感知最小化 | Sharpness-Aware Minimization (SAM) |
| 彩票假说 | Lottery Ticket Hypothesis |
| 谱正则化 | Spectral Regularization |
| 梯度惩罚 | Gradient Penalty |

---

### 理论基础 Theoretical Foundations

| 名词 | 英文 |
|------|------|
| 通用近似定理 | Universal Approximation Theorem |
| 深度分离定理 | Depth Separation Theorem |
| 神经正切核 | Neural Tangent Kernel (NTK) |
| 过参数化 | Over-Parameterization |
| 双下降 | Double Descent |
| 隐式正则化 | Implicit Regularization |
| 信息瓶颈 | Information Bottleneck |
| PAC 学习 | PAC Learning |
| Rademacher 复杂度 | Rademacher Complexity |
| 泛化界 | Generalization Bound |
