---
topic: transformer
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
expiry: 12m
status: current
---

# Transformer 衔接与扩展

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9-10

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | RNN / LSTM | Transformer 替代了 RNN 的序列建模角色 | — |
| ← 前置 | Seq2Seq + Attention | Transformer 的直接前身（Bahdanau 注意力）| — |
| ← 前置 | CNN | CNN 的卷积思想影响了局部注意力和多头设计 | [CNN 知识地图](../cnn/cnn_map.md) |
| ← 前置 | 梯度消失问题 | Transformer 用残差连接彻底解决了深层训练问题 | [vanishing_gradient](../vanishing_gradient/) |
| → 后续 | BERT | Transformer Encoder → 双向预训练模型 | — |
| → 后续 | GPT / LLM | Transformer Decoder → 自回归生成大模型 | — |
| → 后续 | Vision Transformer (ViT) | Transformer 应用于计算机视觉 | — |
| → 后续 | Hugging Face | Transformer 模型的标准化管理和使用平台 | [Hugging Face 知识地图](../../ai-tools/hugging_face/hugging_face_map.md) |

> 📖 Paper: Vaswani et al., Section 1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9-10

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 线性代数 | 矩阵乘法 | $QK^T$ 点积计算、所有投影变换 |
| 概率论 | softmax 函数 | 注意力权重归一化 |
| RNN / LSTM | 序列建模概念（hidden state、序列到序列） | Transformer 替代了 RNN 但继承了序列处理的任务 |
| Bahdanau Attention | 注意力机制（Query-Key-Value 思想的雏形） | Self-Attention 是其推广——Q/K/V 来自同一序列 |
| 残差网络 (ResNet) | 残差连接（skip connection） | 每个子层 $\text{output} = x + \text{Sublayer}(x)$ |
| Layer Normalization | 层归一化 | 每个子层后 Add & LayerNorm |
| Word2Vec / GloVe | 词嵌入（将词映射到向量空间） | Transformer 的输入嵌入层 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10
> 📖 Paper: [Bahdanau et al. 2015](https://arxiv.org/abs/1409.0473)

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|----------------|
| BERT | Encoder 架构 + Self-Attention | 用 Transformer Encoder + MLM 预训练做双向语言理解 |
| GPT / LLM | Decoder 架构 + 因果掩码 | 用 Transformer Decoder 做自回归文本生成 |
| T5 / BART | 完整 Encoder-Decoder | 文本到文本的统一框架（翻译、摘要、问答）|
| Vision Transformer (ViT) | Self-Attention + 位置编码 | 图像分割为 patch → 作为 token 序列输入 Transformer |
| CLIP | Dual-Encoder (图文各用一个 Encoder) | 图像和文本的联合表示学习 |
| Whisper | Encoder-Decoder | 语音 Mel 频谱图 → Encoder → Decoder → 文字 |
| AlphaFold 2 | Attention 机制 | 蛋白质序列的成对注意力预测 3D 结构 |
| Diffusion Transformer (DiT) | Transformer 替代 U-Net 做噪声预测 | Stable Diffusion 3 等使用 DiT 替代 CNN |
| Hugging Face | AutoModel、from_pretrained、pipeline | 统一的 Transformer 模型管理和使用平台 |

> 📖 Paper: [Devlin et al. 2019 (BERT)](https://arxiv.org/abs/1810.04805)
> 📖 Paper: [Dosovitskiy et al. 2021 (ViT)](https://arxiv.org/abs/2010.11929)

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化原因 |
|------|------------|------------|---------|
| 注意力方向 | Encoder-Decoder（原始 Transformer） | Encoder-only (BERT) / Decoder-only (GPT) | 发现单一方向对特定任务更优 |
| 位置编码 | 固定正弦/余弦 | RoPE（旋转位置编码）/ ALiBi | 需要支持训练时未见的更长序列 |
| 激活函数 | ReLU (FFN) | GeLU / SwiGLU / GeGLU | GeLU 更平滑，SwiGLU 实验效果更好 |
| 归一化位置 | Post-LN（LN 在残差之后）| Pre-LN（LN 在子层之前）| Pre-LN 训练更稳定 |
| 注意力效率 | 标准 $O(n^2)$ | Flash Attention / 稀疏注意力 | 解决长序列的显存瓶颈 |
| 参数量 | 65M (Transformer-base) | 1.8T (GPT-4 MoE) | Scaling Law 驱动 |
| 训练范式 | 有监督学习（翻译平行语料）| 自监督预训练 + 微调/RLHF | 无需大量标注数据 |
| 应用领域 | 纯 NLP（机器翻译）| NLP + CV + 语音 + 蛋白质 + 代码 | Transformer 的通用性得到验证 |
| 解码策略 | Beam Search | Top-k / Top-p / Temperature Sampling | 生成质量和多样性的权衡 |

> 📖 Paper: Vaswani et al., Section 3-6
> 📖 Paper: [Su et al. "RoFormer: Enhanced Transformer with Rotary Position Embedding", 2021](https://arxiv.org/abs/2104.09864)

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|-------------|------|
| [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | 📖 论文 | 原始论文，必读——所有后续工作的基础 | ⭐⭐⭐ |
| [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | 📖 博文 | Jay Alammar 的经典可视化教程 | ⭐ |
| [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) | 📖 教程 | Harvard NLP 的逐行代码注释实现 | ⭐⭐ |
| [Formal Algorithms for Transformers](https://arxiv.org/abs/2207.09238) | 📖 论文 | DeepMind 对 Transformer 的形式化数学描述 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Gu & Dao "Mamba", 2023](https://arxiv.org/abs/2312.00752) | Transformer vs 状态空间模型 | 研究线性复杂度替代方案时 |
| [Tay et al. "Efficient Transformers: A Survey", 2022](https://arxiv.org/abs/2009.06732) | 各种高效注意力变体汇总 | 需要处理长序列时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Devlin et al. 2019 (BERT)](https://arxiv.org/abs/1810.04805) | Encoder-only 预训练模型 | 学习文本理解任务时 |
| [Brown et al. 2020 (GPT-3)](https://arxiv.org/abs/2005.14165) | Decoder-only + In-Context Learning | 学习大语言模型时 |
| [Dosovitskiy et al. 2021 (ViT)](https://arxiv.org/abs/2010.11929) | Transformer 在计算机视觉中的应用 | 学习 Vision Transformer 时 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 深度学习基础 | 3 | [CNN 知识地图](../cnn/cnn_map.md) | CNN 的卷积思想 vs Transformer 的全局注意力 |
| 深度学习基础 | 1 | [梯度消失](../vanishing_gradient/) | Transformer 用残差+LN 解决了 RNN 的梯度问题 |
| AI 工具 | 1 | [Hugging Face 知识地图](../../ai-tools/hugging_face/hugging_face_map.md) | HF 是使用预训练 Transformer 模型的标准平台 |
| AI 工具 | 1 | [Keras 知识地图](../../ai-tools/keras/keras_map.md) | Keras 提供 `keras.layers.MultiHeadAttention` 等 Transformer 组件 |
