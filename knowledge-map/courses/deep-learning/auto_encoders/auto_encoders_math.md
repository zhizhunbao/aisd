---
topic: auto_encoders
dimension: math
created: 2026-04-15
last_verified: 2026-04-15
source_versions:
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.14 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Kingma & Welling, Auto-Encoding Variational Bayes, ICLR 2014 — https://arxiv.org/abs/1312.6114"
expiry: 12m
status: current
---

# Auto-Encoders 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14
> 📖 Paper: Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

---

## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| **x** | 原始输入数据 | Input | ℝᵈ |
| **x̂** | 解码器的重构输出 | Reconstruction | ℝᵈ |
| **h** / **z** | 隐空间表征（编码器输出） | Latent code | ℝᵏ, k < d |
| **f(·)** | 编码器函数 | Encoder | ℝᵈ → ℝᵏ |
| **g(·)** | 解码器函数 | Decoder | ℝᵏ → ℝᵈ |
| **θ** | 解码器（生成模型）参数 | Decoder params | — |
| **φ** | 编码器（推断模型）参数 | Encoder params | — |
| **L** | 损失函数 | Loss | ℝ⁺ |
| **Ω(h)** | 正则化惩罚项 | Regularizer | ℝ⁺ |
| **λ** | 正则化系数 | Regularization weight | ℝ⁺ |
| **μ, σ²** | VAE 编码器输出的均值和方差 | Mean, Variance | ℝᵏ |
| **ε** | 标准正态噪声（重参数化用） | Noise | N(0, I) |
| **J** | 编码器的 Jacobian 矩阵 | Jacobian | ℝᵏˣᵈ |
| **KL(·‖·)** | KL 散度 | KL Divergence | ℝ⁺ |
| **p(x)** | 数据的真实分布 | Data distribution | — |
| **p_θ(x|z)** | 解码器定义的条件分布 | Likelihood | — |
| **q_φ(z|x)** | 编码器定义的近似后验 | Approximate posterior | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14

---

## 核心公式

### 公式 1：基本 AE 损失（重构损失）

**直觉**：让输出尽量接近输入——衡量"压缩→还原"丢了多少信息。

**MSE 形式**（连续数据）：

L(x, x̂) = ‖x - g(f(x))‖²

**Binary Cross-Entropy 形式**（二值数据）：

L(x, x̂) = -Σᵢ [xᵢ log(x̂ᵢ) + (1 - xᵢ) log(1 - x̂ᵢ)]

| 参数 | 含义 | 备注 |
|------|------|------|
| x | 原始输入 | 真实数据 |
| x̂ = g(f(x)) | 重构输出 | 经过编码→解码 |
| f(·) | 编码器 | 压缩 |
| g(·) | 解码器 | 还原 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14.1

### 公式 2：正则化 AE 损失（带惩罚项）

**直觉**：光靠瓶颈还不够，加个惩罚让隐空间更有结构。

L = L_reconstruction(x, g(f(x))) + λ · Ω(h)

| 参数 | 含义 | 不同变体的选择 |
|------|------|---------------|
| Ω(h) | 正则化项 | Sparse AE: ‖h‖₁ 或 KL(ρ‖ρ̂) |
| | | Contractive AE: ‖J_f(x)‖²_F |
| λ | 正则化强度 | 平衡重构质量与正则化 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14.2

### 公式 3：稀疏惩罚（KL 散度形式）

**直觉**：让每个隐藏单元的平均激活接近一个很小的目标值 ρ（如 0.05），大多数时候"关着"。

Ω_sparse = Σⱼ KL(ρ ‖ ρ̂ⱼ) = Σⱼ [ρ log(ρ/ρ̂ⱼ) + (1-ρ) log((1-ρ)/(1-ρ̂ⱼ))]

| 参数 | 含义 | 典型值 |
|------|------|--------|
| ρ | 目标稀疏度 | 0.05 |
| ρ̂ⱼ | 第 j 个隐藏单元的平均激活 | 训练集均值 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14.2.1

### 公式 4：收缩惩罚（Jacobian Frobenius 范数）

**直觉**：让编码器对输入的微小扰动不敏感——输入稍微变一点，编码不能变太多。

Ω_contractive = ‖J_f(x)‖²_F = Σᵢⱼ (∂hⱼ/∂xᵢ)²

| 参数 | 含义 |
|------|------|
| J_f(x) | 编码器 f 在 x 处的 Jacobian 矩阵 |
| ‖·‖²_F | Frobenius 范数的平方 |

> **教科书原文**（Goodfellow Ch.14.7, p.521）：
> "We can think of the Jacobian matrix J at a point x as approximating the nonlinear encoder f(x) as being a linear operator."

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14.7

### 公式 5：VAE — ELBO（核心目标函数）

**直觉**：同时做两件事——(1) 重构要好（似然项），(2) 隐空间要像标准正态（KL 项）。

L_VAE = -E_{q_φ(z|x)} [log p_θ(x|z)] + KL(q_φ(z|x) ‖ p(z))
      = 重构损失 + KL 正则化

展开 KL 项（两个高斯之间有解析解）：

KL(N(μ, σ²) ‖ N(0, 1)) = -½ Σⱼ (1 + log(σⱼ²) - μⱼ² - σⱼ²)

| 参数 | 含义 |
|------|------|
| q_φ(z\|x) | 编码器输出的近似后验 N(μ, σ²) |
| p_θ(x\|z) | 解码器定义的似然（重构分布） |
| p(z) | 先验分布 N(0, I) |
| ELBO | Evidence Lower BOund（越大越好，取负为损失） |

> 📖 Paper: Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

### 公式 6：重参数化技巧

**直觉**：从 N(μ, σ²) 采样不可微，换个写法让梯度能传过去。

z = μ + σ ⊙ ε,  ε ~ N(0, I)

| 参数 | 含义 |
|------|------|
| μ | 编码器输出的均值 |
| σ | 编码器输出的标准差 |
| ε | 从标准正态采样的噪声（与参数无关） |
| ⊙ | 逐元素相乘 |

> 📖 Paper: Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

---

## 公式关系图

```
基本 AE 损失: L = ‖x - g(f(x))‖²
       │
       ├──→ + λ·‖h‖₁ ──→ Sparse AE
       │
       ├──→ + λ·‖J_f‖²_F ──→ Contractive AE
       │
       ├──→ 输入加噪 x̃ ──→ Denoising AE
       │                      (损失仍是 ‖x - g(f(x̃))‖²)
       │
       └──→ 概率化 ──→ VAE
                    │
                    ├── 编码器输出 (μ, σ²)
                    ├── 重参数化: z = μ + σ·ε
                    ├── 重构损失: -E[log p(x|z)]
                    └── KL 正则: KL(q(z|x) ‖ p(z))
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14

---

## 手算练习

### 练习 1：线性 AE ≡ PCA

**题**：证明当编码器 f(x) = Wx、解码器 g(h) = W'h 都是线性的，且损失为 MSE 时，最优解的 W 的行是数据协方差矩阵的前 k 个特征向量。

**解题思路**：
1. 损失: L = E[‖x - W'Wx‖²]
2. 令 P = W'W，P 是投影矩阵
3. 最小化重构误差等价于最大化投影方差
4. 最优 W 的行 = 协方差矩阵 Σ 的前 k 个特征向量（即 PCA 方向）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14.1

### 练习 2：VAE KL 散度计算

**题**：给定 q(z|x) = N(μ=[1, -2], σ²=[0.5, 0.3])，计算 KL(q ‖ N(0,I))。

**解**：
KL = -½ Σⱼ (1 + log(σⱼ²) - μⱼ² - σⱼ²)
   = -½ [(1 + log(0.5) - 1² - 0.5) + (1 + log(0.3) - (-2)² - 0.3)]
   = -½ [(1 - 0.693 - 1 - 0.5) + (1 - 1.204 - 4 - 0.3)]
   = -½ [(-1.193) + (-4.504)]
   = -½ × (-5.697)
   = **2.849**

> 📖 Paper: Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)

---

## 公式速查表

| 名称 | 公式 | 用途 | 教科书来源 |
|------|------|------|-----------|
| 重构损失 (MSE) | L = ‖x - g(f(x))‖² | 基本 AE 训练 | Goodfellow Ch.14.1 |
| 重构损失 (BCE) | L = -Σ[x log x̂ + (1-x) log(1-x̂)] | 二值数据 AE | Goodfellow Ch.14.1 |
| 稀疏惩罚 | Ω = Σ KL(ρ ‖ ρ̂ⱼ) | Sparse AE | Goodfellow Ch.14.2.1 |
| 收缩惩罚 | Ω = ‖J_f(x)‖²_F | Contractive AE | Goodfellow Ch.14.7 |
| VAE ELBO | L = -E[log p(x\|z)] + KL(q\|p) | VAE 训练 | Kingma 2014 |
| KL (两高斯) | -½Σ(1+log σ²-μ²-σ²) | VAE 正则项 | Kingma 2014 |
| 重参数化 | z = μ + σ⊙ε | VAE 可微采样 | Kingma 2014 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.14
