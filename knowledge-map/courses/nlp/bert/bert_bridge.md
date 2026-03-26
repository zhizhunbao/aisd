---
topic: bert
dimension: bridge
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# BERT 衔接与扩展

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Transformer | BERT 使用 Transformer Encoder 作为骨架 | — |
| ← 前置 | ELMo | 上下文嵌入的先驱，启发了 BERT 的双向设计 | — |
| ← 前置 | Word2Vec / GloVe | 静态词向量，BERT 的 WordPiece 嵌入替代了它们 | — |
| → 后续 | RoBERTa | BERT 的训练策略优化（去 NSP、更多数据） | — |
| → 后续 | DistilBERT | BERT 的知识蒸馏（更小更快） | — |
| → 后续 | GPT 系列 | BERT 的对照组——单向生成 vs 双向理解 | — |
| → 后续 | LoRA / PEFT | 参数高效微调，减少 BERT 微调的计算需求 | — |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 上游依赖

| 来自主题 | 复用的概念 | 在 BERT 中如何使用 |
|---------|-----------|-------------------|
| Transformer | Self-Attention, Multi-Head Attention, FFN, LayerNorm | BERT 直接使用 Transformer 的 Encoder 部分（去掉 Decoder 和因果掩码） |
| Transformer | 位置编码 (Positional Encoding) | BERT 改为可学习的位置嵌入（不用正弦/余弦） |
| Word2Vec | 分布假说 (Distributional Hypothesis) | BERT 的 MLM 本质上也是利用上下文来学习词的表示 |
| Word2Vec | 词嵌入 (Word Embedding) | BERT 使用 WordPiece + 可学习的 Token Embedding |
| ELMo | 上下文化词表示 (Contextualized Embedding) | BERT 用 Transformer 取代 BiLSTM，实现更深层的双向融合 |
| ELMo | 预训练 + 微调范式 | BERT 完善了这一范式：整体微调 vs ELMo 的特征提取 |
| 语言模型 | 交叉熵损失 (Cross-Entropy Loss) | MLM 和 NSP 都使用交叉熵损失 |
| 子词分词 | BPE / WordPiece | BERT 使用 WordPiece 分词减小词表并处理 OOV |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §2 "Related Work"

---

## 下游影响

| 去向主题 | BERT 提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| RoBERTa | 掩码语言模型 (MLM) | RoBERTa 改为动态掩码，去掉 NSP |
| DistilBERT | BERT 知识 (教师模型) | 知识蒸馏：DistilBERT 学习复现 BERT 的输出分布 |
| ALBERT | MLM + Transformer Encoder | 参数共享 + 嵌入分解 + SOP 替代 NSP |
| ELECTRA | BERT 的 [MASK] 策略 | ELECTRA 用"替换检测"完全替代 MLM，消除预训练/微调不一致 |
| GPT-2/3 | 预训练 + 微调范式 | GPT 用解码器 + 自回归，走了生成路线 |
| T5 | 预训练范式 | T5 用编码器-解码器，统一为 Text-to-Text 格式 |
| LoRA / PEFT | 微调全部参数 | LoRA 只微调低秩分解矩阵，大幅减少参数 |
| Sentence-BERT | [CLS] 句子表示 | 用孪生 BERT 网络学习更好的句子嵌入 |
| BERTScore | BERT 的上下文嵌入 | 用 BERT 嵌入的相似度替代 BLEU/ROUGE 做生成质量评估 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805)
> 📖 Paper: Liu et al., [RoBERTa](https://arxiv.org/abs/1907.11692)

---

## 概念演变追踪

| 概念 | 在早期 | 在 BERT 中 | 变化原因 |
|------|--------|-----------|---------|
| 词表示 | 静态向量 (Word2Vec: 每个词一个固定向量) | 上下文化表示 (每个词每次出现得到不同向量) | 一词多义需要上下文信息 |
| 预训练目标 | 从左到右语言建模 (GPT) | 掩码语言建模 MLM (双向) | 理解任务需要双向上下文 |
| 模型架构 | BiLSTM (ELMo) → Transformer Decoder (GPT) | Transformer Encoder (无因果掩码) | Encoder 天然支持双向 attention |
| 微调方式 | 特征提取 (ELMo: 冻结模型，只用输出) | 端到端微调 (更新所有参数) | 端到端微调效果更好 |
| 位置编码 | 正弦/余弦固定函数 (Transformer) | 可学习位置嵌入 | 可学习更灵活（但失去外推能力） |
| NSP 任务 | BERT 提出 | RoBERTa 去掉 | 实验证明 NSP 效果有限甚至有害 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §2, §5
> 📖 Paper: Liu et al., [RoBERTa](https://arxiv.org/abs/1907.11692), §4

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Devlin et al., BERT (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | 原始论文，理解每一个设计决策 | ⭐⭐⭐ |
| [Clark et al., What Does BERT Look At? (2019)](https://arxiv.org/abs/1906.04341) | 📖 论文 | 分析 BERT 的 attention 头在关注什么 | ⭐⭐⭐⭐ |
| [Rogers et al., A Primer in BERTology (2020)](https://arxiv.org/abs/2002.12327) | 📖 论文 | BERT 研究综述，覆盖 150+ 论文 | ⭐⭐⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [Liu et al., RoBERTa (2019)](https://arxiv.org/abs/1907.11692) | MLM 训练策略优化 | 想改进 BERT 训练时 |
| [Clark et al., ELECTRA (2020)](https://arxiv.org/abs/2003.10555) | MLM vs 替换检测 | 想理解更高效的预训练方法时 |
| [Radford et al., GPT-2 (2019)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | 编码器 vs 解码器路线 | 想理解 BERT vs GPT 范式差异时 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Raffel et al., T5 (2020)](https://arxiv.org/abs/1910.10683) | 统一 Text-to-Text 框架 | 想超越 BERT 看预训练模型全景时 |
| [Hu et al., LoRA (2021)](https://arxiv.org/abs/2106.09685) | 参数高效微调 | 想在实际项目中低成本使用 BERT 时 |
| [《SLP3》Ch.11](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 教科书视角的迁移学习 | 系统学习预训练模型时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| NLP 课程 | 13 个计划主题 | `pretrained_lm` (最直接) | BERT 是预训练模型主题的核心 |
| NLP 前置 | 6 个相关主题 | `attention_transformer`, `word_vectors` | 理解 BERT 需要这些前置知识 |
| NLP 后续 | 3 个相关主题 | `peft`, `llm`, `evaluation` | BERT 为这些主题提供基础 |
| Deep Learning | 已有主题 | `conv_layer`, `neural_network` | Transformer 是 DL 的核心架构 |
