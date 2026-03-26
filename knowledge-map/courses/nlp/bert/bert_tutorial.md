---
topic: bert
dimension: tutorial
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/model_doc/bert"
expiry: 12m
status: current
---

# BERT 教程

> **前置知识：** Transformer 架构 (Self-Attention, Multi-Head Attention), 词嵌入 (Word2Vec / 子词分词), 语言模型基础 (MLM 概念), 交叉熵损失
> **参考来源：** [Devlin et al. 2019](https://arxiv.org/abs/1810.04805), [HuggingFace BERT Docs](https://huggingface.co/docs/transformers/model_doc/bert)

---

## Section 0: 前置知识速查

1. **Transformer 编码器**：由 Self-Attention + FFN + LayerNorm 组成的堆叠结构，能并行处理序列中的所有 token（参考 Vaswani et al. 2017）
2. **Self-Attention**：每个 token 通过 Query-Key-Value 机制计算对其他所有 token 的关注权重，得到上下文感知的表示
3. **WordPiece 分词**：把词拆成子词片段（如 `playing` → `play` + `##ing`），解决 OOV 问题并减小词表
4. **交叉熵损失**：$-\sum y_i \log p_i$，用于衡量预测分布和真实分布的差异
5. **迁移学习**：在大数据集上预训练，再在小数据集上微调的范式

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：每个任务从零开始训练** — 2018 年之前，做情感分析要训练一个模型，做 NER 又要训练另一个模型，做 QA 再训练一个。每个任务都需要大量标注数据（几万到几十万条），但标注数据又贵又难获取。这就像每学一门课都要从小学一年级重新读起。

- 🔥 **痛点 2：单向语言模型丢失信息** — GPT (Radford et al., 2018) 虽然引入了预训练+微调范式，但它是单向的（只看左边）。这在很多理解任务上是致命的。例如 "The bank by the river" vs "He went to the bank to deposit money"——要判断 "bank" 的含义，必须同时看左右两边的上下文。

- 🔥 **痛点 3：特征工程繁琐** — 传统方法需要手动设计特征（TF-IDF 权重、词性标注、句法分析等），不同任务需要不同的特征工程，耗时耗力且难以迁移。

- 🔥 **痛点 4：静态词向量不区分语境** — Word2Vec / GloVe 给每个词一个固定向量，无法区分同一个词在不同语境下的不同含义。"The bank of the river" 和 "I went to the bank" 中的 "bank" 得到完全相同的向量。

### 它的核心价值

1. **预训练 + 微调范式**：一次大规模预训练（Google 用 16 个 TPU 花几天），模型学到通用语言知识。之后任何人只需少量标注数据（几千条）+ 几小时 GPU 微调，就能在自己的任务上达到最优效果。就像读完通识教育后，专业课学起来特别快。

2. **真正的双向上下文表示**：通过 MLM 训练目标，BERT 在编码每个词时同时使用左右两边的完整上下文，生成"上下文感知"的词表示。同一个词在不同句子中会得到不同的向量。

3. **统一架构**：同一个 BERT 模型，只需换不同的输出头，就能处理分类、序列标注、QA、NLI 等几乎所有 NLP 任务。不需要为每个任务设计不同的模型架构。

4. **刷新了 11 个 NLP 基准**：BERT 发布时在 GLUE、SQuAD、SWAG 等基准上全面超越之前的最优方法，引发了 NLP 领域的"BERT 革命"。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §1 "Introduction"
> 📖 Paper: Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), 2018

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

    阶段 1: 预训练 (Pre-Training)
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │  大规模无标注语料                                      │
    │  (BooksCorpus 800M + Wikipedia 2500M words)          │
    │         │                                           │
    │         ▼                                           │
    │  ┌─────────────────────┐                            │
    │  │ WordPiece 分词       │                            │
    │  │ + 特殊 Token 插入     │                            │
    │  │ [CLS]....[SEP]      │                            │
    │  └─────────────────────┘                            │
    │         │                                           │
    │         ▼                                           │
    │  ┌─────────────────────┐                            │
    │  │ Input Representation │                            │
    │  │ Token+Segment+Pos    │                            │
    │  └─────────────────────┘                            │
    │         │                                           │
    │         ▼                                           │
    │  ┌─────────────────────┐                            │
    │  │ 12/24 层 Transformer │                            │
    │  │ Encoder 堆叠         │                            │
    │  └─────────────────────┘                            │
    │         │                                           │
    │    ┌────┴────┐                                      │
    │    ▼         ▼                                      │
    │  ┌──────┐ ┌──────┐                                  │
    │  │ MLM  │ │ NSP  │  ← 两个自监督任务                  │
    │  │ Loss │ │ Loss │                                  │
    │  └──────┘ └──────┘                                  │
    │    └────┬────┘                                      │
    │         ▼                                           │
    │  Total Loss = MLM + NSP                             │
    │  → 反向传播更新全部参数                                │
    └─────────────────────────────────────────────────────┘

    阶段 2: 微调 (Fine-Tuning)
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │  下游任务标注数据 (几千~几万条)                         │
    │         │                                           │
    │         ▼                                           │
    │  ┌─────────────────────┐                            │
    │  │ 预训练好的 BERT       │  ← 加载预训练权重            │
    │  └─────────────────────┘                            │
    │         │                                           │
    │         ▼                                           │
    │  ┌─────────────────────┐                            │
    │  │ + 任务特定输出头      │  ← 新增一个线性层            │
    │  │ (Linear Classifier) │                            │
    │  └─────────────────────┘                            │
    │         │                                           │
    │         ▼                                           │
    │  端到端训练 (2-4 epochs)                              │
    │  学习率 ~2e-5 (比预训练小很多)                         │
    └─────────────────────────────────────────────────────┘

### 2.2 核心机制

**为什么用 MLM 而不是传统的从左到右语言建模？**

传统语言模型（包括 GPT）只能单向预测：$P(w_t | w_1, ..., w_{t-1})$。这从数学上就决定了模型在编码第 $t$ 个词时只能看到左边的上下文。但在很多理解任务中（如 NER、QA），一个词的含义同时取决于左右两边。

直接做双向语言模型有一个致命问题：如果模型能同时看到所有词，那在预测一个词时它可以"偷看"到答案。MLM 用"遮住再猜"的方法巧妙解决了这个问题——被遮住的词看不到自己，只能依赖上下文。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

**为什么 80/10/10 替换策略？**

如果总是把选中的 token 替换为 `[MASK]`，问题是：微调阶段的输入中没有 `[MASK]` token。这造成预训练和微调之间的数据分布不一致。80/10/10 策略（80% → [MASK]，10% → 随机词，10% → 保持不变）是一个工程妥协：

- 80% [MASK]：主要信号源，让模型学会从上下文推断
- 10% 随机词：让模型不能假设"没被 mask 的都是对的"
- 10% 不变：让模型保持对真实输入的表示能力

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

**为什么用 Transformer Encoder 而不是 Decoder？**

Encoder 的 self-attention 没有因果掩码（causal mask），每个 token 可以同时关注到序列中所有位置——这正好实现了"双向"。Decoder 有因果掩码，每个 token 只能看到左边，这就是单向的。BERT 需要双向上下文，所以只用 Encoder。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.1
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

---

## Section 3: 局限性

1. **预训练/微调不一致** — MLM 在预训练时引入 `[MASK]` token，但微调时没有这个 token。80/10/10 策略缓解但未完全解决。→ 应对：ELECTRA 用"替换 Token 检测"完全消除了这个问题。

2. **最大序列长度 512** — 受限于位置嵌入和内存，BERT 最多处理 512 个 token。→ 应对：Longformer / BigBird 扩展到 4096+；或对长文档分块处理。

3. **不擅长生成** — BERT 是编码器模型，无法自回归地生成文本。→ 应对：生成需求用 GPT 系列或 T5。

4. **计算资源需求大** — BERT-Large (340M) 预训练需要 16 TPU × 4 天；微调也至少需要 GPU。→ 应对：DistilBERT (66M) 保留 97% 性能，体积减半。

5. **NSP 任务效果存疑** — RoBERTa (Liu et al., 2019) 实验表明去掉 NSP 反而效果更好。→ 应对：ALBERT 改为 SOP (Sentence Order Prediction)；RoBERTa 直接去掉 NSP。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §5
> 📖 Paper: Liu et al., [RoBERTa](https://arxiv.org/abs/1907.11692), §4

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **BERT** | 双向上下文、统一微调范式、理解任务强 | 不能生成、512 限制、预训练/微调不一致 | 分类、NER、QA、NLI |
| **GPT** | 强大的生成能力、自回归灵活 | 单向上下文、理解任务较弱 | 文本生成、对话、续写 |
| **T5** | 统一 Text-to-Text 框架、编解码器 | 更多参数、更慢推理 | 翻译、摘要、多任务 |
| **RoBERTa** | BERT 改进版、更强训练策略 | 仍有 BERT 局限 | 需要最佳理解性能时 |
| **DistilBERT** | 体积减半、速度加倍、97% 性能 | 准确率略有下降 | 资源受限/推理速度优先 |
| **ELECTRA** | 消除 [MASK] 不一致、样本效率高 | 需要额外的生成器 | 低资源预训练 |
| **ELMo** | 上下文嵌入先驱 | BiLSTM 慢于 Transformer、浅层双向 | 已被 BERT 取代 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §2 "Related Work"
> 📖 Paper: Liu et al., [RoBERTa](https://arxiv.org/abs/1907.11692)
> 📖 Paper: Sanh et al., [DistilBERT](https://arxiv.org/abs/1910.01108)

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Devlin et al., BERT (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | 全文核心参考 |
| [Vaswani et al., Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | Section 0, 2.2 — Transformer 基础 |
| [Radford et al., GPT (2018)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | Section 1, 4 — 单向预训练对比 |
| [Liu et al., RoBERTa (2019)](https://arxiv.org/abs/1907.11692) | 📖 论文 | Section 3, 4 — NSP 效果分析 |
| [Sanh et al., DistilBERT (2019)](https://arxiv.org/abs/1910.01108) | 📖 论文 | Section 3, 4 — 知识蒸馏 |
| [《SLP3》Ch.11](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | 全文背景参考 |
| [HuggingFace BERT Docs](https://huggingface.co/docs/transformers/model_doc/bert) | 📖 文档 | Section 2 — 实现参考 |
