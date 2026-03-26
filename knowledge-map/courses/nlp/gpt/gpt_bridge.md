---
topic: gpt
dimension: bridge
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10-11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: 12m
status: current
---

# GPT 衔接与扩展

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10-11

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | Transformer 架构 | GPT 使用 Transformer Decoder 作为骨架 | — |
| ← 前置 | 语言模型基础 | GPT 的训练目标是自回归语言建模 (CLM) | — |
| ← 前置 | 词嵌入 (Word2Vec, BPE) | GPT 使用 BPE 分词 + Token Embedding | — |
| → 后续 | BERT | 同期对比：双向理解 vs 单向生成 | [bert_map.md](../bert/bert_map.md) |
| → 后续 | InstructGPT / ChatGPT | GPT + RLHF 对齐 → 产品化 | — |
| → 后续 | Prompt Engineering | GPT-3 催生的全新交互范式 | — |
| → 后续 | LLM 生态 (LLaMA, Claude) | GPT 开创的 Decoder-Only 路线的后继者 | — |

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|------------------|
| Transformer | Self-Attention | GPT 的核心计算单元——每一层用 Masked Self-Attention 计算上下文表示 |
| Transformer | 位置编码 | GPT-1 使用可学习位置嵌入（不是正弦编码） |
| Transformer | FFN + LayerNorm + 残差 | GPT 每层的标准模块，但改用 Pre-Norm |
| 语言模型 | 自回归建模 (CLM) | GPT 的训练目标——预测下一个词的条件概率 |
| 语言模型 | 困惑度 (Perplexity) | GPT 的标准评估指标 |
| 词嵌入 | BPE 分词 | GPT-2 使用 Byte-Level BPE，词表约 50,257 |
| 词嵌入 | Embedding 矩阵 | Token Embedding + Position Embedding 两者相加 |

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §3
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|-----------------|
| BERT | "预训练 + 微调" 范式 | BERT 借鉴了 GPT-1 的预训练思想，但改用双向编码器 |
| InstructGPT / ChatGPT | GPT-3 基础模型 | 在 GPT-3 上应用 RLHF，使模型对齐人类意图 |
| Prompt Engineering | In-Context Learning | GPT-3 的 Few-Shot 能力催生了 Prompt 设计整个领域 |
| 代码生成 (Codex) | CLM + 代码训练 | 在代码语料上训练 GPT → GitHub Copilot |
| LLaMA / Mistral | Decoder-Only 架构 | 开源社区沿用 GPT 的 Decoder-Only 路线 |
| PEFT (LoRA, Adapter) | 大模型微调需求 | GPT-3 太大无法全量微调 → 催生参数高效微调方法 |
| RAG | 幻觉问题 | GPT 的幻觉问题 → 用检索增强来提供事实基础 |
| 多模态 (GPT-4V) | 语言理解能力 | 把 GPT 的语言能力扩展到图像、音频等模态 |

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §1
> 📖 Paper: Ouyang et al., [InstructGPT](https://arxiv.org/abs/2203.02155), §1

---

## 概念演变追踪

| 概念 | 在早期 (GPT-1, 2018) | 在现代 (GPT-4, 2023+) | 变化原因 |
|------|----------------------|----------------------|---------|
| 预训练目标 | CLM (预测下一词) | 仍是 CLM，但加入了多模态 token | 核心目标没变，输入从纯文本扩展到图像 |
| 使用范式 | 预训练 → 微调 → 部署 | 预训练 → RLHF → Prompt → Agent | 模型足够大后不需要微调 |
| 模型规模 | 117M 参数 | 传闻 1T+ 参数 | Scaling Laws 驱动 |
| 训练数据 | 800M 词 (BooksCorpus) | 数万亿 token (互联网+书+代码) | 数据规模和质量同步增长 |
| 评估方式 | 困惑度 + 下游 benchmark | 人类偏好 + Arena + 多任务 benchmark | 从"技术指标"到"用户体验" |
| 安全考量 | 几乎没有 | RLHF + 红队测试 + 安全过滤 | ChatGPT 产品化后安全成为核心 |

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1
> 📖 Paper: OpenAI, [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774), §2

---

## 📚 扩展阅读

### 深入理解（纵深）

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [Radford et al. "GPT-1" (2018)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | 原始论文，理解 GPT 的起点 | ⭐⭐ |
| [Brown et al. "GPT-3" (2020)](https://arxiv.org/abs/2005.14165) | 📖 论文 | In-Context Learning 的完整分析 | ⭐⭐⭐ |
| [Kaplan et al. "Scaling Laws" (2020)](https://arxiv.org/abs/2001.08361) | 📖 论文 | 理解为什么"越大越好" | ⭐⭐⭐ |
| [Ouyang et al. "InstructGPT" (2022)](https://arxiv.org/abs/2203.02155) | 📖 论文 | RLHF 对齐的完整方法 | ⭐⭐⭐ |

### 横向对比（同层）

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| [BERT 知识地图](../bert/bert_map.md) | 双向(BERT) vs 单向(GPT) | 理解两种预训练路线的取舍 |
| [Raffel et al. "T5" (2020)](https://arxiv.org/abs/1910.10683) | Encoder-Decoder vs Decoder-Only | 理解 Text-to-Text 的第三条路线 |
| [Touvron et al. "LLaMA" (2023)](https://arxiv.org/abs/2302.13971) | 开源 vs 闭源 LLM | 理解开源社区如何复现 GPT 路线 |

### 上层应用（全景）

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [Wei et al. "Chain-of-Thought" (2022)](https://arxiv.org/abs/2201.11903) | 用 CoT 提升 GPT 推理能力 | 学习 Prompt Engineering 进阶 |
| [Lewis et al. "RAG" (2020)](https://arxiv.org/abs/2005.11401) | 检索增强缓解 GPT 幻觉 | 构建实用 LLM 应用时 |
| [Hu et al. "LoRA" (2021)](https://arxiv.org/abs/2106.09685) | 参数高效微调大模型 | 需要微调 GPT 但资源有限时 |

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| NLP 课程知识地图 | 1 | [BERT](../bert/bert_map.md) | 双向 vs 单向的核心设计对比 |
| Deep Learning 课程 | 多个 | Transformer / 注意力机制 | GPT 的底层架构依赖 |
| 课程 Lab | 1 | Lab 4 情感分析 (DistilBERT) | 对比 BERT 微调 vs GPT Prompt 两种方式 |
