# 信息论 Information Theory

> 名词总表 · 来源：Cover & Thomas《Elements of Information Theory》· MIT 6.441 · MacKay《Information Theory, Inference, and Learning Algorithms》
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 基本信息度量 Basic Information Measures

| 名词 | 英文 |
|------|------|
| 信息量 | Self-Information / Surprisal |
| 熵 | Entropy H(X) |
| 联合熵 | Joint Entropy H(X,Y) |
| 条件熵 | Conditional Entropy H(Y|X) |
| 互信息 | Mutual Information I(X;Y) |
| 条件互信息 | Conditional Mutual Information I(X;Y|Z) |
| KL 散度 | KL Divergence D_KL(P‖Q) |
| 交叉熵 | Cross-Entropy H(P,Q) |
| 链式法则（熵） | Chain Rule for Entropy |
| 链式法则（互信息） | Chain Rule for Mutual Information |
| 数据处理不等式 | Data Processing Inequality |
| Fano 不等式 | Fano's Inequality |
| 微分熵 | Differential Entropy h(X) |

---

### 熵的性质与不等式 Properties & Inequalities

| 名词 | 英文 |
|------|------|
| 非负性 | Non-Negativity |
| 最大熵原理 | Maximum Entropy Principle |
| Gibbs 不等式 | Gibbs' Inequality |
| Jensen 不等式 | Jensen's Inequality |
| 对数和不等式 | Log-Sum Inequality |
| 凹性（熵） | Concavity of Entropy |
| 凸性（KL 散度） | Convexity of KL Divergence |
| 唯一性定理 | Uniqueness Theorem |
| 充分统计量 | Sufficient Statistic |
| Fisher 信息 | Fisher Information |

---

### 信源编码 Source Coding (Data Compression)

| 名词 | 英文 |
|------|------|
| 无损压缩 | Lossless Compression |
| 有损压缩 | Lossy Compression |
| 信源编码定理 | Source Coding Theorem |
| Huffman 编码 | Huffman Coding |
| 算术编码 | Arithmetic Coding |
| Kraft 不等式 | Kraft Inequality |
| 前缀码 | Prefix Code |
| 码长期望 | Expected Codeword Length |
| 最优码 | Optimal Code |
| 率失真理论 | Rate-Distortion Theory |
| 率失真函数 | Rate-Distortion Function R(D) |
| Lempel-Ziv 压缩 | Lempel-Ziv Coding (LZ77/LZ78) |
| 通用编码 | Universal Coding |

---

### 信道编码 Channel Coding

| 名词 | 英文 |
|------|------|
| 信道 | Channel |
| 离散无记忆信道 | DMC (Discrete Memoryless Channel) |
| 二元对称信道 | BSC (Binary Symmetric Channel) |
| 二元删除信道 | BEC (Binary Erasure Channel) |
| 信道容量 | Channel Capacity C |
| 信道编码定理 | Channel Coding Theorem |
| 编码速率 | Coding Rate R |
| 错误概率 | Error Probability |
| 可达速率 | Achievable Rate |
| 联合典型序列 | Jointly Typical Sequences |
| 典型集 | Typical Set |
| 渐近等分性 | AEP (Asymptotic Equipartition Property) |
| 强逆 | Strong Converse |
| 反馈容量 | Feedback Capacity |

---

### 高斯信道 Gaussian Channel

| 名词 | 英文 |
|------|------|
| 加性高斯白噪声信道 | AWGN Channel |
| 香农公式 | Shannon Capacity Formula C = ½ log(1+SNR) |
| 信噪比 | SNR (Signal-to-Noise Ratio) |
| 功率约束 | Power Constraint |
| 注水算法 | Water-Filling Algorithm |
| 并行高斯信道 | Parallel Gaussian Channels |
| 带宽 | Bandwidth |
| 带限信道 | Band-Limited Channel |
| 香农界 | Shannon Limit |

---

### 多用户信息论 Multi-User Information Theory

| 名词 | 英文 |
|------|------|
| 多址接入信道 | MAC (Multiple Access Channel) |
| 广播信道 | Broadcast Channel |
| 干扰信道 | Interference Channel |
| 中继信道 | Relay Channel |
| Slepian-Wolf 编码 | Slepian-Wolf Coding (Distributed Source Coding) |
| Wyner-Ziv 编码 | Wyner-Ziv Coding (Lossy with Side Info) |
| 容量区域 | Capacity Region |
| 叠加编码 | Superposition Coding |
| 逐次干扰消除 | SIC (Successive Interference Cancellation) |

---

### 大偏差与假设检验 Large Deviations & Hypothesis Testing

| 名词 | 英文 |
|------|------|
| 大偏差 | Large Deviations |
| Sanov 定理 | Sanov's Theorem |
| 类型/经验分布 | Type / Empirical Distribution |
| 方法类型 | Method of Types |
| 似然比检验 | Likelihood Ratio Test |
| Neyman-Pearson 引理 | Neyman-Pearson Lemma |
| Stein 引理 | Stein's Lemma |
| Chernoff 指数 | Chernoff Exponent |
| 错误指数 | Error Exponent |
| I-投影 | I-Projection |

---

### 信息论与 ML Information Theory & ML

| 名词 | 英文 |
|------|------|
| 最大似然估计 | MLE (Maximum Likelihood Estimation) |
| 最大熵模型 | Maximum Entropy Model |
| 信息瓶颈 | Information Bottleneck |
| 最小描述长度 | MDL (Minimum Description Length) |
| 互信息最大化 | Mutual Information Maximization |
| 变分信息最大化 | Variational Information Maximization |
| InfoNCE | InfoNCE Loss |
| 熵正则化 | Entropy Regularization |
| 交叉熵损失 | Cross-Entropy Loss |
| KL 散度正则 | KL Regularization (VAE) |
| 比特每维 | Bits Per Dimension (BPD) |
| 困惑度 | Perplexity |
| 信道容量与学习 | Channel Capacity & Learning |
