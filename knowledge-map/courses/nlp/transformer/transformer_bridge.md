---
topic: transformer
dimension: bridge
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📖 Paper: Radford et al., 'GPT-1', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9-11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# Transformer 衔接与扩展

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9-11
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | RNN / LSTM / Seq2Seq | Transformer 取代了 RNN 的序列建模角色 | — |
| ← 前置 | Attention (Bahdanau/Luong) | Transformer 把注意力从"补丁"升级为"核心架构" | — |
| → 后续 | BERT | 只用 Encoder + 双向注意力，擅长理解任务 | [../bert/bert_map.md](../bert/bert_map.md) |
| → 后续 | GPT | 只用 Decoder + 因果注意力，擅长生成任务 | [../gpt/gpt_map.md](../gpt/gpt_map.md) |
| → 后续 | T5 / BART | 完整 Encoder-Decoder，文本到文本统一框架 | — |
| → 后续 | ViT | Transformer 应用于计算机视觉（图像 patch = token） | — |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §1
> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| 线性代数 | 矩阵乘法 | Q·K^T 计算注意力分数；所有投影都是矩阵乘法 |
| 概率论 | Softmax 归一化 | 把注意力分数变成概率分布 |
| 词嵌入 (Word2Vec) | 将词映射为向量 | 输入嵌入层把 token ID 映射为 d_model 维向量 |
| RNN / LSTM | 序列建模概念 | Transformer 解决了 RNN 的"不能并行"和"长距离遗忘"问题 |
| Bahdanau Attention | 注意力思想 | Self-Attention 是 Bahdanau Attention 的自反版本（Q/K/V 都来自自身） |
| ResNet | 残差连接 | 每个子层都有 skip connection: output = x + SubLayer(x) |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10
> 📖 Paper: He et al., [Deep Residual Learning](https://arxiv.org/abs/1512.03385), CVPR 2016

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| BERT | Encoder + Self-Attention + LayerNorm | BERT 只用 Encoder 部分，加上 MLM + NSP 预训练目标 |
| GPT | Decoder + Causal Mask + 自回归生成 | GPT 只用 Decoder 部分，因果注意力 + CLM 预训练目标 |
| T5 / BART | 完整 Encoder-Decoder + Cross-Attention | T5 保留完整架构，统一成 Text-to-Text 框架 |
| ViT | Self-Attention + 位置编码 + FFN | 把图像切成 16×16 patch 当作 token，纯 Transformer 做视觉分类 |
| Whisper | Encoder-Decoder Transformer | 把音频梅尔频谱切成帧当序列，Transformer 做语音识别 |
| AlphaFold 2 | Self-Attention | 蛋白质氨基酸序列当 token，注意力建模残基间关系 |
| Flash Attention | Scaled Dot-Product Attention | 优化 GPU 内存访问模式，加速标准注意力 2-4 倍 |
| RoPE / ALiBi | Positional Encoding | 改进位置编码方案，让模型支持更长序列 |

> 📖 Paper: Dosovitskiy et al., [ViT](https://arxiv.org/abs/2010.11929), ICLR 2021
> 📖 Paper: Dao et al., [FlashAttention](https://arxiv.org/abs/2205.14135), NeurIPS 2022

---

## 概念演变追踪

| 概念 | 在早期 | 在现代 | 变化原因 |
|------|--------|--------|---------|
| 注意力 | RNN 的附加模块 (Bahdanau 2015) | 核心计算单元，取代 RNN (Vaswani 2017) | 发现注意力本身就足够强，RNN 是多余的 |
| 位置编码 | 固定正弦函数 (Vaswani 2017) | 可学习(BERT) / 旋转编码 RoPE (2021) / ALiBi (2022) | 固定编码对长序列泛化差，相对位置更灵活 |
| 层归一化 | Post-LN (Vaswani 2017) | Pre-LN (GPT-2+) | Pre-LN 训练更稳定，不需要 warmup |
| FFN 激活函数 | ReLU (Vaswani 2017) | GELU (GPT/BERT) / SwiGLU (LLaMA) | GELU 更平滑，SwiGLU 效果更好 |
| 模型规模 | 65M (Transformer base) | 175B+ (GPT-3) / 1.8T (Switch) | 缩放定律表明更大 = 更好 |

> 📖 Paper: Su et al., [RoPE](https://arxiv.org/abs/2104.09864), 2021
> 📖 Paper: Shazeer, [SwiGLU](https://arxiv.org/abs/2002.05202), 2020

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | 📖 论文 | 原始论文——必读，只有 11 页 | ⭐⭐⭐ |
| [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) | 📖 博客 | 最好的 Transformer 可视化讲解 | ⭐⭐ |
| [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) | 💻 代码 | 逐行注释的 PyTorch 实现 | ⭐⭐⭐ |
| [Formal Algorithms for Transformers (DeepMind)](https://arxiv.org/abs/2207.09238) | 📖 论文 | Transformer 的形式化数学描述 | ⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Efficient Transformers: A Survey](https://arxiv.org/abs/2009.06732) | 各种高效注意力变体 | 处理长序列时 |
| [BERT vs GPT vs T5 对比](https://arxiv.org/abs/1910.10683) | Encoder vs Decoder vs Full | 选择预训练模型时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223) | LLM 全景综述 | 了解 Transformer 如何催生 LLM 革命 |
| [Vision Transformer Survey](https://arxiv.org/abs/2101.01169) | Transformer 在视觉领域的应用 | 了解跨模态迁移 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| NLP 同课程主题 | 2 | [BERT](../bert/bert_map.md), [GPT](../gpt/gpt_map.md) | Transformer 拆成 Encoder/Decoder 的两种用法 |
| 深度学习基础 | — | deep-learning 课程（如已有） | Transformer 的训练技巧（残差、归一化、warmup）根源 |
