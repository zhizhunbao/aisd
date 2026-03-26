---
topic: gpt
dimension: concepts
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Brown et al., 'Language Models are Few-Shot Learners', NeurIPS 2020 — https://arxiv.org/abs/2005.14165"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10-11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/model_doc/gpt2"
expiry: 12m
status: current
---

# GPT 核心概念

> 📖 Paper: Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI 2018
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10-11

---

## 术语定义

### 生成式预训练 Transformer (Generative Pre-trained Transformer, GPT)

GPT 是 OpenAI 在 2018 年提出的预训练语言模型系列。它的核心思想很简单：用 Transformer 的解码器（Decoder）部分做一个"下一个词预测器"——给定前面所有的词，预测下一个词是什么。通过在海量文本上做这件事，模型学会了语言的语法、语义、甚至世界知识。

和 BERT 不同，GPT 只从左到右看，不看右边的内容。这看起来像是缺点（上下文信息不如 BERT 全面），但正是这个特性让 GPT 天生擅长文本生成——因为生成文本时你确实只有前面的内容可参考。

> 别名：**GPT**（通用简称）— 来自 OpenAI 论文标题首字母缩写

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1

### 因果语言模型 (Causal Language Model, CLM)

GPT 的预训练目标。"因果"的意思是：每个位置只能看到自己之前（左边）的 token，不能"偷看"后面的——就像写作文时只能基于已经写出的内容来决定下一个字。数学上就是最大化条件概率的乘积：$P(x_1, x_2, ..., x_n) = \prod_{i=1}^{n} P(x_i | x_1, ..., x_{i-1})$。

这和人类写作/说话的过程完全一致：你总是基于已经说过的话来决定下面说什么。

> 别名：**自回归语言建模** (Autoregressive Language Modeling)（来自统计学领域的"自回归"概念）/ **CLM**（通用简称）

> 易混淆：**掩码语言模型 (MLM)** — CLM 从左到右预测下一个词，天生适合生成；MLM（BERT 使用）随机遮住部分词让模型猜，擅长理解但不能直接生成文本

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §3.1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10 "Language Models"

### 因果掩码 (Causal Mask)

GPT 在 self-attention 中使用的一种掩码机制。它是一个上三角矩阵，把当前位置之后所有位置的注意力权重设为 $-\infty$（softmax 后变成 0）。这确保了第 $i$ 个 token 只能关注位置 $1$ 到 $i$ 的 token，不能偷看未来。

没有因果掩码，GPT 就不是自回归模型了——模型可以直接看到答案，预训练就变成了"抄答案"。

> 别名：**注意力掩码** (Attention Mask, 在这个上下文中) / **下三角掩码** (Lower-Triangular Mask)（从矩阵形状角度描述）

> 易混淆：**填充掩码 (Padding Mask)** — 因果掩码防止看未来；填充掩码防止关注 `[PAD]` token。两者可以叠加使用

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1 "Masked Multi-Head Attention"

### BPE 分词 (Byte Pair Encoding Tokenization)

GPT 系列使用的子词分词算法。它从单个字符开始，不断合并出现频率最高的字符对，直到达到预设的词表大小。比如 `l` + `o` → `lo`，`lo` + `w` → `low`。

BPE 的优点是：(1) 常见词保持完整（如 `the`），(2) 罕见词被拆成子词（如 `unbelievably` → `un` + `believ` + `ably`），(3) 永远不会出现 OOV（词表外）问题。

GPT-2 使用的是 Byte-Level BPE（字节级 BPE），直接在 UTF-8 字节上操作，词表约 50,257 个 token。

> 别名：**BPE**（通用简称）/ **字节对编码**（直译）

> 易混淆：**WordPiece** — BPE 按频率合并字符对；WordPiece（BERT 使用）按似然增益合并。两者都是子词分词，但合并策略不同

> 📖 Paper: Sennrich et al., [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909), ACL 2016
> 📖 Paper: Radford et al., [GPT-2](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), §2.2

### 上下文学习 (In-Context Learning, ICL)

GPT-3 展示的核心能力。不需要梯度更新或微调，只要在 prompt 中给出几个"输入→输出"的示例，模型就能在推理时"学会"这个任务的模式，并对新的输入给出正确的输出。

例如：给模型看 "Translate English to French: sea otter → loutre de mer, peppermint → menthe poivrée, cheese →"，模型能输出 "fromage"。这不是检索，也不是微调——模型在前向传播中就"理解"了翻译这个任务。

> 别名：**ICL**（通用简称）/ **情境学习**（中文翻译变体）

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §1.1 "In-Context Learning"

### 零样本学习 (Zero-Shot Learning)

只给任务描述，不给任何示例，模型就能完成任务。例如："Translate English to French: cheese →"。GPT-2 首次展示了大规模语言模型在零样本设置下的强大能力。

> 易混淆：**少样本学习 (Few-Shot Learning)** — 零样本不给示例；少样本给 1~几十个示例。GPT-3 论文系统比较了两者的效果差异

> 📖 Paper: Radford et al., [GPT-2](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), §1
> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §2

### 少样本学习 (Few-Shot Learning)

在 prompt 中给出少量（通常 1~几十个）"输入→输出"示例，让模型学会任务模式。GPT-3 论文证明，模型越大，少样本学习的效果越好——175B 参数的 GPT-3 在很多任务上用几个示例就能接近或超过微调后的小模型。

> 别名：**Few-Shot Prompting**（从使用角度描述）

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §2.1

### 温度 (Temperature)

文本生成时的一个超参数，控制输出的随机性。在 softmax 计算中，把 logits 除以温度 $T$：$P(x_i) = \text{softmax}(z_i / T)$。

- $T < 1$：分布变得更"尖锐"，模型倾向于选择概率最高的词 → 输出更确定、更保守
- $T = 1$：使用原始分布
- $T > 1$：分布变得更"平坦"，小概率的词也可能被选中 → 输出更多样、更有创意（但也可能更离谱）

> 📖 Paper: Ackley et al., "A Learning Algorithm for Boltzmann Machines", Cognitive Science, 1985 — 温度概念最早来源于统计物理中的玻尔兹曼分布
> 📖 Docs: [HuggingFace Generation Config](https://huggingface.co/docs/transformers/main_classes/text_generation)

### Top-k 采样 (Top-k Sampling)

文本生成时的一种采样策略。每一步只保留概率最高的 $k$ 个词，把其余词的概率设为 0，然后从这 $k$ 个词中按概率采样。

问题是：$k$ 是固定的，但不同上下文中合理选项的数量不同。比如 "The capital of France is" 后面几乎只有一个合理答案（Paris），但 "I like to eat" 后面有很多可能。

> 📖 Paper: Fan et al., [Hierarchical Neural Story Generation](https://arxiv.org/abs/1805.04833), ACL 2018

### Top-p 采样 / 核采样 (Top-p Sampling / Nucleus Sampling)

文本生成时的另一种采样策略。从概率最高的词开始，依次累加概率，直到累积概率达到 $p$（如 $p = 0.9$），把这些词作为候选集。相比 Top-k，候选集大小是动态的——当模型很确定时候选集小，不确定时候选集大。

> 别名：**核采样** (Nucleus Sampling)（论文原名）

> 📖 Paper: Holtzman et al., [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751), ICLR 2020

### KV 缓存 (KV Cache)

GPT 推理优化的关键技术。在自回归生成中，每生成一个新 token，都要重新计算所有之前 token 的 Key 和 Value——但之前 token 的 K 和 V 其实没变。KV Cache 把已经计算过的 K、V 缓存起来，新 token 只需要计算自己的 Q、K、V，然后用缓存的 K、V 做注意力计算。

这把推理复杂度从 $O(n^2)$ 降到了 $O(n)$（每步只增量计算一个 token），但代价是显存占用增大。

> 📖 Docs: [HuggingFace GPT-2 use_cache](https://huggingface.co/docs/transformers/model_doc/gpt2#transformers.GPT2LMHeadModel.forward.use_cache)

### RLHF (Reinforcement Learning from Human Feedback)

InstructGPT / ChatGPT 使用的对齐技术。训练流程分三步：(1) 用人工标注的高质量回答做监督微调 (SFT)，(2) 训练一个奖励模型 (Reward Model) 来打分人类偏好，(3) 用 PPO 算法让 GPT 根据奖励模型的反馈进一步优化。

RLHF 让 GPT 从"能生成文本"变成"生成人类觉得有用、安全、诚实的文本"。

> 别名：**基于人类反馈的强化学习**（中文全称）

> 📖 Paper: Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), NeurIPS 2022

### 上下文窗口 (Context Window)

GPT 模型能同时处理的最大 token 数量。GPT-2 的上下文窗口是 1024 个 token，GPT-3 是 2048，GPT-4 扩展到 8K/32K/128K。超过上下文窗口的内容会被截断，模型"看不到"。

上下文窗口越大，模型能参考的信息越多，但计算成本（self-attention 的 $O(n^2)$ 复杂度）和显存占用也按平方增长。

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §2.1

### Decoder-Only 架构 (Decoder-Only Architecture)

GPT 使用的 Transformer 架构。原始 Transformer 有编码器和解码器两部分，但 GPT 只用了解码器（带因果掩码的 self-attention + FFN）。去掉编码器后，模型结构更简单，训练更高效，而且在缩放定律下表现最好。

> 易混淆：**Encoder-Only（BERT）** — 只用编码器，双向 self-attention，擅长理解。**Encoder-Decoder（T5）** — 编码器理解输入，解码器生成输出，擅长翻译/摘要

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 概念辨析

### GPT vs BERT

| 维度 | GPT | BERT |
|------|-----|------|
| **方向性** | 单向（只看左边）| 双向（同时看左右）|
| **架构** | Transformer Decoder | Transformer Encoder |
| **预训练任务** | CLM（预测下一个词）| MLM + NSP |
| **擅长什么** | 生成任务（文本续写、对话）| 理解任务（分类、NER、QA）|
| **典型应用** | ChatGPT、代码生成 | 文本分类、信息抽取 |
| **缩放潜力** | 极强（GPT-3/4）| 有限（几百M到1B）|
| **论文** | Radford et al., 2018 | Devlin et al., 2019 |

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3, Figure 3

### CLM vs MLM

| 维度 | CLM (GPT) | MLM (BERT) |
|------|-----------|------------|
| **训练目标** | 预测下一个 token | 预测被遮住的 token |
| **上下文方向** | 单向（左到右）| 双向 |
| **预训练/微调一致性** | 一致（都是从左到右）| 不一致（微调无 `[MASK]`）|
| **生成能力** | 强 | 弱 |
| **理解能力** | 较弱 | 强 |
| **信号效率** | 每个 token 都是训练信号 | 只有 15% 被 mask 的 token |

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §3.1
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.3.1

### Top-k vs Top-p 采样

| 维度 | Top-k | Top-p (Nucleus) |
|------|-------|-----------------|
| **候选集大小** | 固定 $k$ 个词 | 动态，由累积概率决定 |
| **适应性** | 差——无论分布如何都取 $k$ 个 | 好——分布尖锐时少选，平坦时多选 |
| **典型值** | $k = 50$ | $p = 0.9$ |
| **组合使用** | 可以同时设置 Top-k + Top-p | 取两者的交集 |

> 📖 Paper: Fan et al., [Hierarchical Neural Story Generation](https://arxiv.org/abs/1805.04833), ACL 2018
> 📖 Paper: Holtzman et al., [Neural Text Degeneration](https://arxiv.org/abs/1904.09751), ICLR 2020

---

## 核心属性

### 信息架构

    输入文本: "The cat sat on"
         │
         ▼
    ┌──────────────────────────────────────────────────┐
    │  BPE 分词                                         │
    │  The  cat  sat  on                                │
    └──────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────┐
    │  Input Representation = Token Embedding + Position │
    │  （GPT 无 Segment Embedding）                      │
    └──────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────┐
    │  N 层 Transformer Decoder                          │
    │  (Masked Self-Attention → FFN → LayerNorm)        │
    │  因果掩码确保只看左边                               │
    └──────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────┐
    │  输出: 每个位置预测下一个 token 的概率分布           │
    │  P("the"|"The") P("mat"|"The cat") ...            │
    │  最后一个位置: P(next_word | "The cat sat on")     │
    └──────────────────────────────────────────────────┘
         │
         ▼  解码策略 (Greedy / Top-k / Top-p / Beam)
    ┌──────────────────────────────────────────────────┐
    │  生成: "the"  → 拼接 → 继续预测 → "the mat"       │
    └──────────────────────────────────────────────────┘

### 适用场景 ✅

- **开放式文本生成**：故事写作、文章续写、创意写作
- **对话系统**：ChatGPT 类的多轮对话
- **代码生成**：Codex / GitHub Copilot（GPT 的代码版本）
- **文本摘要**：把长文档压缩成短摘要
- **翻译**：在 prompt 中给示例即可完成翻译
- **少样本/零样本任务**：通过 Prompt Engineering 完成各种 NLP 任务

### 不适用场景 ❌

- **精确信息检索**：GPT 可能"编造"不存在的事实（幻觉）
- **双向上下文理解**：句子中间的完形填空（BERT 更好）
- **精确的 NER / 序列标注**：BERT 类模型更适合
- **低资源部署**：GPT-3 (175B) 推理成本极高
- **确定性计算**：数学计算、精确逻辑推理仍然不可靠

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §3-4
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 速查表

| 项 | 说明 | 示例 |
|-----|------|------|
| 模型类型 | Transformer Decoder (单向自回归) | 12 层 (GPT-1) / 48 层 (GPT-2 Large) |
| 预训练任务 | CLM (预测下一个词) | 每个 token 都是训练信号 |
| 输入格式 | `token_1 token_2 ... token_n` | 无 [CLS] / [SEP] |
| 输入表示 | Token Embedding + Position Embedding | 两者相加（无 Segment） |
| 分词方法 | BPE / Byte-Level BPE | ~50,257 个 token (GPT-2) |
| 上下文窗口 | 因模型而异 | 1024 (GPT-2) / 2048 (GPT-3) / 128K (GPT-4) |
| GPT-1 参数 | L=12, H=768, A=12 | 117M 参数 |
| GPT-2 参数 | L=48, H=1600, A=25 | 1.5B 参数 (最大版本) |
| GPT-3 参数 | L=96, H=12288, A=96 | 175B 参数 |
| 解码策略 | Greedy / Beam / Top-k / Top-p | temperature + top_p 组合最常用 |
| 微调方式 | GPT-1 微调 / GPT-2+ 推荐 Prompt | In-Context Learning (GPT-3) |
