---
topic: gpt
dimension: tutorial
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Brown et al., 'Language Models are Few-Shot Learners', NeurIPS 2020 — https://arxiv.org/abs/2005.14165"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10-11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Docs: HuggingFace GPT-2 — https://huggingface.co/docs/transformers/model_doc/gpt2"
expiry: 12m
status: current
---

# GPT 教程

> **前置知识：** Transformer 架构 (Self-Attention, FFN)、语言模型基础 (N-gram, 困惑度)、词嵌入 (Word2Vec, 子词分词)
> **参考来源：** [GPT-1 论文](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)、[GPT-3 论文](https://arxiv.org/abs/2005.14165)、[《SLP3》Ch.10-11](../../../textbooks/jurafsky_slp3_jan2026.pdf)

---

## Section 0: 前置知识速查

1. **Transformer 架构**：Self-Attention 让每个词能关注序列中所有其他词；FFN 提供非线性变换；LayerNorm + 残差连接保证深层训练稳定 → 详见 [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762)
2. **语言模型**：给定前文预测下一个词的概率模型。N-gram 用固定窗口统计频率；神经语言模型用神经网络拟合条件概率 → 详见 [《SLP3》Ch.10](../../../textbooks/jurafsky_slp3_jan2026.pdf)
3. **子词分词 (BPE)**：把词拆成子词片段，解决 OOV 问题。GPT-2 使用 Byte-Level BPE → 详见 [Sennrich et al. 2016](https://arxiv.org/abs/1508.07909)
4. **困惑度 (Perplexity)**：语言模型的标准评估指标，PPL 越低越好 = 模型越不"困惑" → 详见 [gpt_math.md](gpt_math.md) 公式 5

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：传统模型无法泛化到新任务** — 2017 年以前，每个 NLP 任务（情感分析、翻译、QA）都需要从头训练一个专门模型。标注数据需求大、训练周期长、模型之间不共享知识——做情感分析的模型完全不知道如何做翻译

- 🔥 **痛点 2：LSTM/RNN 的序列建模瓶颈** — RNN/LSTM 按时间步顺序处理，无法并行化；长距离依赖信息在传递过程中衰减（梯度消失）。一个 1000 词的句子，RNN 很难让第 1 个词和第 999 个词建立关联

- 🔥 **痛点 3：即使有 BERT，也不能生成文本** — BERT（2019）证明了预训练的价值，但它是双向的，不能逐词生成文本。你不能用 BERT 写故事、做对话、做翻译

- 🔥 **痛点 4：小模型需要大量标注数据才能微调** — 即使 GPT-1 用了预训练，也需要几千到几万条标注数据来微调。低资源语言和小众任务仍然困难

### 它的核心价值

1. **一个模型解决所有任务** — GPT 证明了：只要模型足够大、预训练数据足够多，一个通用的语言模型就能处理翻译、问答、摘要、分类等各种任务——不需要针对每个任务设计专门架构

2. **文本生成能力** — Decoder-Only + 自回归设计让 GPT 天生擅长生成连贯、流畅的文本。从 GPT-1 的基础生成到 ChatGPT 的多轮对话，生成能力一脉相承

3. **缩放带来涌现** — GPT 系列证明了 Scaling Laws：模型参数翻倍，性能稳步提升。更惊人的是，到了一定规模（~100B 参数），模型突然"涌现"出训练中从未明确教过的能力（如链式推理、代码生成）

4. **不需要微调的时代** — GPT-3 的 In-Context Learning 革命：只要在 prompt 中给几个例子，模型就"学会"了新任务。这把 NLP 从"训练模型"变成了"写提示词"

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1
> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §1

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 GPT 的三代演进

    ┌─────────────────────────────────────────────────────────────┐
    │  GPT-1 (2018): 预训练 + 微调                                │
    │  ┌─────────────────┐    ┌──────────────────┐               │
    │  │ 大量无标注文本    │───→│ Transformer      │──→ 通用表示    │
    │  │ (BooksCorpus)   │    │ Decoder (12层)   │               │
    │  └─────────────────┘    └──────────────────┘               │
    │          │                                                  │
    │          ▼ (第二步) 少量标注数据 → 微调 → 下游任务            │
    └─────────────────────────────────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  GPT-2 (2019): 零样本，不需要微调                            │
    │  模型更大 (1.5B) + 数据更多 (WebText 40GB)                  │
    │  发现: 足够大的模型能在零样本下完成任务                       │
    │  任务格式: 自然语言描述 → "Translate to French: cheese →"   │
    └─────────────────────────────────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  GPT-3 (2020): 上下文学习 (In-Context Learning)              │
    │  模型巨大 (175B) + 数据海量                                  │
    │  发现: 在 prompt 中给几个示例 → 模型"学会"新任务              │
    │  不需要梯度更新 → 彻底改变 NLP 使用范式                       │
    │                                                             │
    │  Prompt: "sea otter → loutre de mer                          │
    │           cheese → "  模型输出: "fromage"                    │
    └─────────────────────────────────────────────────────────────┘

### 2.2 核心机制：Decoder-Only Transformer

**为什么用 Decoder-Only 而不是 Encoder-Decoder？**

原始 Transformer (Vaswani 2017) 是 Encoder-Decoder 结构，用于翻译。但 GPT 的目标不是翻译，而是"预测下一个词"——这只需要解码器。去掉编码器后：
- **结构更简单**：参数全集中在一个方向上，训练更高效
- **缩放更友好**：Chinchilla 和 Scaling Laws 研究表明 Decoder-Only 在同等 FLOPs 下性能最好
- **训练目标一致**：预训练（预测下一词）和推理（生成下一词）完全一致，没有 BERT 的预训练-微调不一致问题

**每一层在做什么？**

    输入 token 序列
         │
         ▼
    ┌───────────────────────────────────────────────┐
    │ Token Embedding + Position Embedding            │
    │ (GPT 无 Segment Embedding)                     │
    └───────────────────────────────────────────────┘
         │
         ▼ (重复 L 次)
    ┌───────────────────────────────────────────────┐
    │ Masked Multi-Head Self-Attention                │
    │ (因果掩码: 只看左边，不看右边)                    │
    │ + Residual Connection + LayerNorm               │
    ├───────────────────────────────────────────────┤
    │ Feed-Forward Network (FFN)                      │
    │ FFN(x) = GELU(xW₁ + b₁)W₂ + b₂               │
    │ + Residual Connection + LayerNorm               │
    └───────────────────────────────────────────────┘
         │
         ▼
    ┌───────────────────────────────────────────────┐
    │ Linear → Softmax → P(next_token | context)     │
    │ (权重与 Token Embedding 共享!)                  │
    └───────────────────────────────────────────────┘

### 2.3 设计决策

**为什么用 GELU 而不是 ReLU？**

GPT 使用 GELU (Gaussian Error Linear Unit) 激活函数，而不是更常见的 ReLU。GELU 是平滑的、处处可微的，而 ReLU 在 0 点不可微。经验上 GELU 在 Transformer 中表现更好。

> 📖 Paper: Hendrycks & Gimpel, [Gaussian Error Linear Units](https://arxiv.org/abs/1606.08415), 2016

**为什么 GPT-1 用 Pre-Norm 而不是 Post-Norm？**

GPT 系列使用 LayerNorm 在注意力/FFN 之前（Pre-Norm），而不是之后（Post-Norm, 原始 Transformer 的做法）。Pre-Norm 让梯度更稳定，深层训练更容易。

> 📖 Paper: Xiong et al., [On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745), ICML 2020

**为什么 Embedding 权重和输出层权重共享？**

GPT 把 token embedding 矩阵 $W_e$ 重用为最后的输出投影矩阵 $W_e^T$。这减少了参数量，并且在语义上是合理的：embedding 把词映射到向量空间，输出层把向量映射回词——两者应该是逆操作。

> 📖 Paper: Press & Wolf, [Using the Output Embedding to Improve Language Models](https://arxiv.org/abs/1608.05859), EACL 2017

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §3

---

## Section 3: 局限性

1. **幻觉 (Hallucination)** — GPT 会自信地生成看起来合理但事实上错误的内容。根因：模型优化的是"看起来像真话"的概率分布，不是"说真话"→ 应对策略：RAG（检索增强生成）、事实验证系统

2. **上下文窗口限制** — GPT-2 只有 1024 token，GPT-3 是 2048 token。超过窗口的内容被截断→ 应对策略：长上下文模型 (GPT-4 128K)、滑动窗口、RAG

3. **训练数据偏见** — 模型从互联网数据中学习，会继承数据中的偏见（性别、种族、文化）→ 应对策略：RLHF 对齐、数据过滤、安全提示

4. **计算成本** — GPT-3 训练一次的估计成本约 460 万美元（按 2020 年 GPU 价格）。推理也很贵→ 应对策略：模型蒸馏、量化 (INT8/INT4)、LoRA 微调

5. **不擅长精确推理** — 数学计算、逻辑推理、计数等确定性任务仍然不可靠→ 应对策略：链式推理 (CoT)、工具调用（让模型调用计算器）

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §6 "Limitations"

---

## Section 4: 方案对比

| 方案 | 代表 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|---------|
| Decoder-Only (自回归) | GPT 系列 | 天生擅长生成；缩放性最好；In-Context Learning | 不擅长双向理解；幻觉 | 文本生成、对话、代码 |
| Encoder-Only (双向) | BERT 系列 | 双向上下文理解强；精确的 NER/分类 | 不能直接生成；缩放性差 | 分类、标注、信息抽取 |
| Encoder-Decoder | T5, BART | 理解+生成兼顾；翻译/摘要效果好 | 结构复杂；训练效率低于 Decoder-Only | 翻译、摘要、结构化生成 |
| 混合专家 (MoE) | Switch Transformer, Mixtral | 参数量大但计算量小；高效缩放 | 训练不稳定；负载均衡难 | 超大规模模型 |
| 微调范式 | GPT-1, BERT | 任务特定性能最优 | 需要标注数据；每个任务一个模型 | 数据充足的单一任务 |
| Prompt 范式 | GPT-3+ | 无需训练；一个模型多任务 | 效果依赖 prompt 质量；token 有限 | 灵活多任务、快速原型 |

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §2
> 📖 Paper: Raffel et al., [T5](https://arxiv.org/abs/1910.10683), §3 — Encoder-Decoder 对比
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Radford et al. "GPT-1" (2018)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | 全文核心参考 |
| [Radford et al. "GPT-2" (2019)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | 📖 论文 | §1 零样本能力 |
| [Brown et al. "GPT-3" (2020)](https://arxiv.org/abs/2005.14165) | 📖 论文 | §1 上下文学习, §6 局限性 |
| [Vaswani et al. "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | §2.2 Transformer 架构 |
| [《SLP3》Ch.10-11](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | §0 前置知识 |
| [Hendrycks & Gimpel "GELU" (2016)](https://arxiv.org/abs/1606.08415) | 📖 论文 | §2.3 激活函数 |
| [Press & Wolf "Output Embedding" (2017)](https://arxiv.org/abs/1608.05859) | 📖 论文 | §2.3 权重共享 |
