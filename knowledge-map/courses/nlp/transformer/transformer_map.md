---
topic: transformer
dimension: map
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9-10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Eisenstein, 《Natural Language Processing》, Ch.18 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/eisenstein_nlp.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Bahdanau et al., 'Neural Machine Translation by Jointly Learning to Align and Translate', ICLR 2015 — https://arxiv.org/abs/1409.0473"
expiry: 12m
status: current
---

# Transformer 知识地图

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9-10
> 📚 Book: Eisenstein, [《Natural Language Processing》](../../../textbooks/eisenstein_nlp.pdf), Ch.18

## 1. 核心问题

- **Transformer 到底是什么？** → 一种完全基于注意力机制（Attention）的序列到序列模型架构，彻底抛弃了 RNN/CNN 的顺序计算方式，用 Self-Attention 让每个位置直接"看到"序列中所有其他位置
- **为什么 Transformer 要淘汰 RNN？** → RNN 必须一步一步按顺序处理序列（t=1→t=2→…），天然无法并行，训练极慢。Transformer 用 Self-Attention 一次性计算所有位置的关系，训练速度提升数十倍
- **Self-Attention 的核心思想是什么？** → 对序列中的每个词，计算它和所有其他词的"相关度分数"，然后用这些分数加权求和，得到融合了全局上下文的新表示。Q（查询）、K（键）、V（值）三个矩阵是实现这个目标的数学工具
- **Multi-Head Attention 为什么需要"多头"？** → 一个头只能学到一种注意力模式（比如关注语法关系），多个头可以同时关注不同类型的关系（语义、语法、位置等），最后拼接起来得到更丰富的表示
- **Transformer 怎么知道词的顺序？** → Self-Attention 本身不区分位置——把句子打乱，计算结果一样。所以必须加入位置编码（Positional Encoding），用正弦余弦函数给每个位置一个独特的信号

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §1-3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9 "Deep Learning Architectures for Sequence Processing"

---

## 2. 全景位置

```
自然语言处理 NLP
├── 传统方法
│   ├── N-gram 语言模型
│   ├── TF-IDF + 逻辑回归
│   └── CRF / HMM 序列标注
├── 词向量时代
│   ├── Word2Vec (静态嵌入)
│   ├── GloVe (全局统计)
│   └── FastText (子词)
├── 序列模型时代
│   ├── RNN / LSTM / GRU
│   └── Seq2Seq + Attention (Bahdanau 2015)
├── Transformer 架构 ← 你在这里
│   ├── 【Transformer】 (Self-Attention, 完全并行, Encoder-Decoder)
│   ├── 位置编码 (Sinusoidal / Learned / RoPE)
│   ├── 多头注意力 (Multi-Head Attention)
│   └── 前馈网络 + 残差连接 + 层归一化
└── 预训练语言模型
    ├── BERT (双向 Transformer Encoder, MLM+NSP)
    ├── GPT 系列 (单向 Transformer Decoder, CLM)
    ├── T5 (完整 Encoder-Decoder, Text-to-Text)
    └── LLaMA / PaLM / Claude (大规模 LLM)
```

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9-10
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §2 "Background"

---

## 3. 依赖地图

```
前置知识                       本主题                       后续方向
┌───────────────────────┐     ┌──────────────────────┐     ┌──────────────────────────────┐
│ Seq2Seq + Attention    │────→│                      │────→│ BERT (Encoder-Only)           │
│ (Bahdanau/Luong)      │     │                      │     │                              │
│                       │     │                      │────→│ GPT (Decoder-Only)            │
├───────────────────────┤     │   Transformer        │     │                              │
│ RNN / LSTM / GRU       │────→│  (Self-Attention     │────→│ T5 / BART (Full Enc-Dec)      │
│ (序列模型基础)          │     │   Multi-Head Attn    │     │                              │
│                       │     │   Positional Enc)    │────→│ Vision Transformer (ViT)      │
├───────────────────────┤     │                      │     │                              │
│ 词嵌入 + 位置表示       │────→│                      │────→│ 多模态 Transformer             │
│ (Word2Vec, 矩阵运算)   │     │                      │     │ (图像+文本+音频)               │
├───────────────────────┤     │                      │────→│ 高效 Transformer               │
│ 线性代数 + Softmax      │────→│                      │     │ (Sparse / Linear Attention)    │
│ (矩阵乘法, 概率归一化)  │     │                      │     │                              │
└───────────────────────┘     └──────────────────────┘     └──────────────────────────────┘
```

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §2-6
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.9-10

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [transformer_map.md](transformer_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [transformer_concepts.md](transformer_concepts.md) | ② 概念 | 理解 Self-Attention/MHA/FFN/位置编码等术语 |
| [transformer_math.md](transformer_math.md) | ③ 公式 | 推导缩放点积注意力、多头注意力、位置编码 |
| [transformer_tutorial.md](transformer_tutorial.md) | ④ 教程 | Why-First 理解 Transformer 设计动机 |
| [transformer_code.md](transformer_code.md) | ⑤ 代码 | 快速上手 PyTorch 实现 Transformer |
| [transformer_pitfalls.md](transformer_pitfalls.md) | ⑥ 踩坑 | 注意力计算/掩码设置/位置编码等常见问题 |
| [transformer_history.md](transformer_history.md) | ⑦ 历史 | 从 Seq2Seq+Attention 到 Transformer 的技术演进 |
| [transformer_bridge.md](transformer_bridge.md) | ⑧ 衔接 | 连接 BERT / GPT / ViT / 高效 Transformer |
| [transformer_first_principles.md](transformer_first_principles.md) | ⑨ 第一性原理 | 追问"为什么注意力能取代循环" |

> 📖 Docs: Norman, 《The Design of Everyday Things》(2013), Ch.3 "Knowledge in the World"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [transformer_map.md](transformer_map.md) 了解 Transformer 在 NLP 全景中的位置
2. 读 [transformer_tutorial.md](transformer_tutorial.md) Section 1 理解"为什么需要抛弃 RNN"
3. 读 [transformer_concepts.md](transformer_concepts.md) 掌握 Self-Attention / MHA / FFN / 位置编码等核心术语
4. 读 [transformer_math.md](transformer_math.md) 手算一次缩放点积注意力
5. 跟 [transformer_code.md](transformer_code.md) 用 PyTorch 实现一个最简 Transformer
6. 读 [transformer_history.md](transformer_history.md) 了解从 Attention → Transformer → BERT/GPT 的演进
7. 读 [transformer_first_principles.md](transformer_first_principles.md) 理解注意力机制的数学根基

### 日常参考 🔧

1. 查 [transformer_code.md](transformer_code.md) PyTorch API 速查表
2. 查 [transformer_math.md](transformer_math.md) 注意力公式速查
3. 查 [transformer_pitfalls.md](transformer_pitfalls.md) 排查注意力/掩码/位置编码常见问题

### 深度研究 🔬

1. 读 [transformer_history.md](transformer_history.md) 完整演进线
2. 读 [transformer_first_principles.md](transformer_first_principles.md) 追问注意力与表达能力
3. 读 [transformer_bridge.md](transformer_bridge.md) 对比 Encoder-Only / Decoder-Only / Full Enc-Dec
4. 阅读原始论文 [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ✅ 已完成 |
| Math | ✅ 已完成 |
| Tutorial | ✅ 已完成 |
| Code | ✅ 已完成 |
| Pitfalls | ✅ 已完成 |
| History | ✅ 已完成 |
| Bridge | ✅ 已完成 |
| First Principles | ✅ 已完成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-03-24 | 12m | ✅ current |
| Concepts | 2026-03-24 | 12m | ✅ current |
| Math | 2026-03-24 | 12m | ✅ current |
| Tutorial | 2026-03-24 | 12m | ✅ current |
| Code | 2026-03-24 | 6m | ✅ current |
| Pitfalls | 2026-03-24 | 6m | ✅ current |
| History | 2026-03-24 | never | ✅ current |
| Bridge | 2026-03-24 | 12m | ✅ current |
| First Principles | 2026-03-24 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Vaswani et al. "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | 全文核心参考——Transformer 原始论文 |
| [Bahdanau et al. "Neural Machine Translation by Jointly Learning to Align and Translate" (2015)](https://arxiv.org/abs/1409.0473) | 📖 论文 | History, Tutorial——注意力机制起源 |
| [Luong et al. "Effective Approaches to Attention-based NMT" (2015)](https://arxiv.org/abs/1508.04025) | 📖 论文 | Concepts, History——Luong 注意力 |
| [《SLP3》Ch.9-10](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | Deep Learning Architectures, Language Models |
| [《NLP》Ch.18](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | 预训练语言模型理论 |
| [《Deep Learning》Ch.10](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 序列模型基础 |
| [Devlin et al. "BERT" (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | Bridge——Encoder-Only 变体 |
| [Radford et al. "GPT-1" (2018)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | Bridge——Decoder-Only 变体 |
| [Dosovitskiy et al. "ViT" (2021)](https://arxiv.org/abs/2010.11929) | 📖 论文 | Bridge——视觉领域 Transformer |
| [PyTorch nn.Transformer Docs](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html) | 📖 文档 | Code——API 接口和使用方法 |
| [HuggingFace Transformers Docs](https://huggingface.co/docs/transformers/) | 📖 文档 | Code——高层 API 封装 |
