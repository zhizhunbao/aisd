---
topic: transformer
dimension: map
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10,12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
expiry: 12m
status: current
---

# Transformer 知识地图

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9-10

## 1. 核心问题

- **Transformer 是什么？** → 一种完全基于注意力机制的序列到序列神经网络架构，抛弃了 RNN/CNN，仅靠 Self-Attention 捕获序列依赖
- **它解决了什么问题？** → RNN 的顺序计算无法并行化、长距离依赖捕获困难、训练速度慢
- **核心机制是什么？** → Scaled Dot-Product Attention + Multi-Head Attention + 位置编码（Positional Encoding）+ 残差连接 + Layer Normalization
- **Encoder-Decoder 结构是什么？** → Encoder 对输入序列编码为上下文表示；Decoder 自回归地生成输出序列，同时 attend 到 Encoder 的输出
- **为什么它如此重要？** → 几乎所有现代 NLP/CV/多模态模型（BERT、GPT、ViT、CLIP、Whisper）的基础架构

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 1-3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9

---

## 2. 全景位置

```
深度学习架构
├── 序列模型
│   ├── RNN (循环神经网络)
│   ├── LSTM (长短期记忆)
│   ├── GRU (门控循环单元)
│   └── Seq2Seq + Attention (Bahdanau/Luong)
├── 注意力架构 ← 你在这里
│   ├── 【Transformer】 (纯注意力，Encoder-Decoder)
│   ├── BERT (Transformer Encoder, 双向)
│   ├── GPT (Transformer Decoder, 自回归)
│   ├── T5 (Encoder-Decoder, 文本到文本)
│   └── Vision Transformer (ViT, 图像分块)
├── 卷积模型
│   ├── CNN (图像特征提取)
│   └── TCN (时序卷积网络)
└── 混合架构
    ├── Mamba (状态空间模型)
    └── RWKV (线性注意力 RNN)
```

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 1
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10

---

## 3. 依赖地图

```
前置知识                      本主题                    后续方向
┌───────────────────────┐    ┌───────────────────┐    ┌──────────────────────────┐
│ 线性代数 (矩阵乘法)    │───→│                   │───→│ BERT (双向编码器)         │
│ 概率论 (softmax)       │───→│                   │───→│ GPT (自回归解码器)        │
│ 神经网络基础 (MLP/反向) │───→│    Transformer    │───→│ Vision Transformer (ViT)  │
│ Seq2Seq + 注意力机制   │───→│                   │───→│ 多模态 (CLIP/Whisper)     │
│ 词嵌入 (Word2Vec/GloVe)│───→│                   │───→│ 大语言模型 (LLM)          │
└───────────────────────┘    └───────────────────┘    └──────────────────────────┘
```

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [transformer_map.md](transformer_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [transformer_concepts.md](transformer_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [transformer_math.md](transformer_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [transformer_tutorial.md](transformer_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [transformer_code.md](transformer_code.md) | ⑤ 代码 | 快速上手实现 |
| [transformer_pitfalls.md](transformer_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [transformer_history.md](transformer_history.md) | ⑦ 历史 | 了解技术演进 |
| [transformer_bridge.md](transformer_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [transformer_first_principles.md](transformer_first_principles.md) | ⑨ 第一性原理 | 理解为什么 Transformer 必须是这样 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [transformer_map.md](transformer_map.md) 了解全局位置
2. 读 [transformer_tutorial.md](transformer_tutorial.md) Section 1 理解为什么需要 Transformer
3. 读 [transformer_concepts.md](transformer_concepts.md) 掌握核心术语
4. 读 [transformer_math.md](transformer_math.md) 手算一次 Scaled Dot-Product Attention
5. 跟 [transformer_code.md](transformer_code.md) 快速开始跑一个示例
6. 读 [transformer_history.md](transformer_history.md) 了解从 RNN 到 Transformer 的演进

### 日常参考 🔧

1. 查 [transformer_code.md](transformer_code.md) API 速查表
2. 查 [transformer_math.md](transformer_math.md) 公式速查
3. 查 [transformer_pitfalls.md](transformer_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [transformer_first_principles.md](transformer_first_principles.md) 理解设计必然性
2. 读 [transformer_history.md](transformer_history.md) 完整演进线
3. 读 [transformer_bridge.md](transformer_bridge.md) 探索 BERT/GPT/ViT 方向
4. 阅读 Vaswani et al. 2017 原始论文

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
| Map | 2026-03-14 | 12m | ✅ current |
| Concepts | 2026-03-14 | 12m | ✅ current |
| Math | 2026-03-14 | 12m | ✅ current |
| Tutorial | 2026-03-14 | 12m | ✅ current |
| Code | 2026-03-14 | 6m | ✅ current |
| Pitfalls | 2026-03-14 | 6m | ✅ current |
| History | 2026-03-14 | never | ✅ current |
| Bridge | 2026-03-14 | 12m | ✅ current |
| First Principles | 2026-03-14 | 12m | ✅ current |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | 📖 论文 | 全文核心参考 — Transformer 原始论文 |
| [《Deep Learning》Ch.10,12](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Concepts / Math — 序列建模与注意力基础 |
| [《SLP3》Ch.9-10](../../../textbooks/jurafsky_slp3.pdf) | 📚 教科书 | Tutorial / Concepts — Transformer 与 NLP |
| [《NLP》Eisenstein Ch.10](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | Math / Concepts — 注意力机制数学 |
| [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html) | 📖 文档 | Code — PyTorch 官方实现 |
| [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | 📖 博文 | Tutorial — Jay Alammar 经典可视化 |
| [Bahdanau et al. 2015](https://arxiv.org/abs/1409.0473) | 📖 论文 | History — 注意力机制先驱 |
| [Devlin et al. 2019 (BERT)](https://arxiv.org/abs/1810.04805) | 📖 论文 | Bridge — Encoder-only 变体 |
| [Radford et al. 2018 (GPT)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | Bridge — Decoder-only 变体 |
