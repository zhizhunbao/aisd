---
topic: mlp
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6,9,10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Vaswani et al., 'Attention is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Tolstikhin et al., 'MLP-Mixer', NeurIPS 2021 — https://arxiv.org/abs/2105.01601"
expiry: 12m
status: current
---

# MLP (Multi-Layer Perceptron) 衔接与扩展

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 线性回归 / 逻辑回归 | MLP 是线性模型的非线性扩展 | — |
| ← 前置 | 感知机 (Perceptron) | MLP 是多层版本 + 可微激活函数 | — |
| ← 前置 | 梯度下降 | MLP 训练的优化方法 | — |
| → 后续 | CNN (卷积神经网络) | 引入局部连接+权值共享的特殊 MLP | [cnn/](../cnn/) |
| → 后续 | RNN (循环神经网络) | 加入时间维度的反馈连接 | — |
| → 后续 | Transformer | FFN 模块就是两层 MLP | — |
| → 后续 | 正则化技术 | Dropout、BN 等应用于 MLP | — |
| → 后续 | 高级优化器 | Adam、AdaGrad 等替代 SGD | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.9, Ch.10

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 线性代数 | 矩阵乘法 $\mathbf{Wx}$、向量加法 | MLP 每层的核心操作 |
| 微积分 | 链式法则 $\frac{\partial f}{\partial x} = \frac{\partial f}{\partial g} \frac{\partial g}{\partial x}$ | 反向传播的数学基础 |
| 概率论 | 极大似然估计、交叉熵 | 损失函数的推导动机 |
| 线性模型 | $\hat{y} = \mathbf{w}^T\mathbf{x} + b$ | MLP 每层的线性变换部分 |
| 优化理论 | 梯度下降、学习率 | MLP 参数更新策略 |
| 感知机 | 加权求和 + 阈值判断 | MLP 的历史前身，激发了多层结构的设计 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.2–5
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1–4

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| CNN | 全连接层、反向传播、激活函数 | CNN 的分类头 (classifier head) 是 MLP；卷积层本质是带约束的全连接层 |
| RNN/LSTM | 前向传播、反向传播框架 | RNN 的每一步是一个共享权重的 MLP，BPTT 是 BP 的时间展开版 |
| Transformer | MLP 结构 | FFN (Feed-Forward Network) 模块就是两层 MLP: `W₂·ReLU(W₁·x + b₁) + b₂` |
| GANs | 全连接生成器和判别器 | 早期 GAN 的生成器和判别器都是 MLP |
| 自编码器 | 对称的编码器-解码器 | 编码器和解码器各是一个 MLP |
| 迁移学习 | 预训练特征提取 → 微调分类头 | 分类头通常是一个 MLP |
| MLP-Mixer | 纯 MLP 架构 | 用 MLP 替代卷积和注意力机制处理图像 |
| Batch Normalization | 依赖 MLP 的训练动态分析 | BN 解决 MLP 的 internal covariate shift |
| Dropout | 正则化 MLP | Srivastava et al. 2014 最初在 MLP 上验证 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.9, Ch.10
> 📖 Paper: Vaswani et al., [Attention is All You Need](https://arxiv.org/abs/1706.03762), 2017

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化原因 |
|------|-------------|-------------|---------|
| 激活函数 | Sigmoid / Tanh（1986-2009） | ReLU / GELU / SiLU（2010-至今） | Sigmoid 导致梯度消失；ReLU 正半轴梯度恒为 1 |
| 初始化策略 | 小随机数（均匀分布） | Xavier (2010) / He (2015) 初始化 | 保持各层方差稳定，防止信号放大/消失 |
| 优化器 | 纯 SGD | SGD + Momentum → Adam / AdamW | 自适应学习率加速收敛，减少调参负担 |
| 正则化 | L2 正则化 + Early Stopping | Dropout (2014) + BN (2015) + Weight Decay | 更有效的过拟合控制，训练更稳定 |
| 深度信念 | "浅层更好"（SVM 时代） | "深层有优势"（特征层次化） | 算力突破 + ReLU + BN 使深层训练成为可能 |
| 预训练 | 逐层无监督预训练必需（2006-2012） | 直接端到端训练即可（2012-至今） | ReLU + 更好初始化 + 大数据消除了预训练必要性 |
| 角色定位 | 独立的完整模型 | 更大架构中的子组件 | CNN/Transformer 等特化架构在特定领域更优 |

> 📖 Paper: Glorot & Bengio, [Xavier Init](http://proceedings.mlr.press/v9/glorot10a.html), 2010
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.6

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Rumelhart et al. 1986](https://www.nature.com/articles/323533a0) | 📖 论文 | 反向传播的经典原始论文，写作清晰 | ⭐⭐ |
| [Goodfellow Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | MLP 最完整的教科书级讲解 | ⭐⭐⭐ |
| [Cybenko 1989](https://doi.org/10.1007/BF02551274) | 📖 论文 | 万能近似定理原始证明 | ⭐⭐⭐⭐ |
| [Bishop PRML Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 概率视角的神经网络 | ⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Tolstikhin et al. 2021, MLP-Mixer](https://arxiv.org/abs/2105.01601) | 纯 MLP vs CNN vs Transformer 在视觉任务上的对比 | 了解 MLP 在现代视觉中的复兴 |
| [Goodfellow Ch.9](../../../textbooks/goodfellow_deep_learning.pdf) | MLP vs CNN | 理解从全连接到局部连接的设计动机 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | Transformer 中 FFN 模块的 MLP 应用 | 学习 Transformer 架构时 |
| [Goodfellow Ch.20](../../../textbooks/goodfellow_deep_learning.pdf) | MLP 在 GAN/VAE 中的应用 | 学习生成模型时 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf)

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 深度学习架构 | 3 | [CNN](../cnn/), [Tensor](../tensor/), [梯度消失](../vanishing_gradient/) | MLP → CNN 的演进；MLP 操作依赖 Tensor；深层 MLP 面临梯度消失 |
| 传统 ML | 9 | [逻辑回归](../../ml/logistic_regression/), [SVM](../../ml/svm/), [KNN](../../ml/knn/) | MLP 是逻辑回归的非线性扩展；与 SVM 在 1990s 竞争；MLP 可替代 KNN 做分类 |
