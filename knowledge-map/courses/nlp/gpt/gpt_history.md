---
topic: gpt
dimension: history
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Radford et al., 'Language Models are Unsupervised Multitask Learners', OpenAI 2019 — https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"
  - "📖 Paper: Brown et al., 'Language Models are Few-Shot Learners', NeurIPS 2020 — https://arxiv.org/abs/2005.14165"
  - "📖 Paper: Ouyang et al., 'Training language models to follow instructions', NeurIPS 2022 — https://arxiv.org/abs/2203.02155"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
expiry: never
status: current
---

# GPT 的故事线：从预测下一个词到改变世界

> **核心主题：** "Just predict the next word"——一个看似简单的目标，如何随着规模增长而涌现出令人震惊的智能
> **故事线：** 从统计语言模型到神经网络，从小模型微调到巨型模型上下文学习，最终催生出 ChatGPT 和 AGI 讨论

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> "给定前面的所有词，下一个词最可能是什么？" —— 这是人类对语言建模最古老的提问，也是 GPT 系列的全部核心。

1948 年，Claude Shannon 在《A Mathematical Theory of Communication》中提出了信息论，并用马尔可夫链模型来分析英语：给定前一个字母，下一个字母的概率是多少？这个问题看似简单，但它蕴含了对语言结构、语法、语义、甚至世界知识的全部理解。

70 年后，OpenAI 发现：用一个足够大的神经网络来回答这个问题，结果不仅仅是"预测下一个词"——模型涌现出了翻译、推理、编程、甚至类似"思考"的能力。

> 🔑 **问题提出：** 统计语言模型的窗口太小、表达能力太弱，能不能用神经网络来做更好的"下一个词预测"？

---

## 📚 第一章：N-gram 语言模型（1980s-2000s）

> **关键人物：** Frederick Jelinek (IBM)
> **关键论文：** Jelinek, "Statistical Methods for Speech Recognition", MIT Press, 1997

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Frederick Jelinek 肖像 | JHU CLSP 档案 | `https://www.clsp.jhu.edu/about/history/` | 学术引用 |

### 发生了什么？

IBM 语音识别组的 Jelinek 团队把统计方法引入了语言建模。核心思想简单粗暴：统计训练语料中每个 n-gram（连续 n 个词）出现的频率，用它来预测下一个词。

例如，bigram 模型：$P(\text{cat} \mid \text{the}) = \frac{\text{count}(\text{the cat})}{\text{count}(\text{the})}$

### 为什么这很重要？

N-gram 模型首次把语言建模变成了**可量化、可优化**的工程问题。困惑度 (Perplexity) 成为标准评估指标，语音识别准确率大幅提升。Jelinek 有句名言："Every time I fire a linguist, the performance of the speech recognizer goes up."

### 但还有一个问题……

N-gram 的窗口太小了——bigram 只看前 1 个词，trigram 只看前 2 个词。上下文一长就完全不行。更致命的是"数据稀疏"问题：语料中没出现过的 n-gram 概率是 0，各种平滑方法 (Kneser-Ney, Good-Turing) 都只是打补丁。

> 🔑 **故事转折点：** N-gram 的表达能力到了天花板——需要一种能学习"语义相似性"的方法，而不是死记硬背。

---

## 📚 第二章：神经语言模型（2003-2013）

> **关键人物：** Yoshua Bengio
> **关键论文：** Bengio et al., [A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html), JMLR 2003

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| Yoshua Bengio 肖像 | Wikimedia Commons | `https://commons.wikimedia.org/wiki/File:Yoshua_Bengio_-_2017.jpg` | CC BY-SA 4.0 |
| 论文首页 | JMLR | `https://jmlr.org/papers/v3/bengio03a.html` | 学术引用 |

### 发生了什么？

Bengio 提出了革命性的思路：(1) 把每个词映射为一个稠密向量（词嵌入），(2) 用神经网络来学习"给定前几个词的嵌入，预测下一个词"。这样语义相似的词（如 "cat" 和 "dog"）在向量空间中靠近，模型自动学到了泛化能力。

后来 Mikolov 等人提出了 RNN 语言模型 (2010) 和 LSTM 语言模型，不再限制窗口大小——理论上可以看到任意远的上下文。

### 为什么这很重要？

词嵌入 + 神经网络彻底解决了数据稀疏问题——即使某个 n-gram 没在训练集中出现过，只要其中的词在语义空间中靠近已见过的 n-gram，模型就能给出合理的预测。

### 但还有一个问题……

RNN/LSTM 虽然理论上能看到长距离上下文，但实际上长距离信息在传递过程中会衰减（梯度消失）。而且 RNN 按时间步顺序计算，无法并行化——训练一个大模型需要几个月。

> 🔑 **故事转折点：** 我们需要一种能并行处理、真正捕获长距离依赖的全新架构。2017 年，Transformer 出现了。

---

## 📚 第三章：GPT-1 — 预训练 + 微调（2018）

> **关键人物：** Alec Radford, OpenAI
> **关键论文：** Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), 2018

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| GPT-1 论文首页 | OpenAI | `https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf` | 学术引用 |

### 发生了什么？

OpenAI 的 Radford 等人把 Transformer Decoder 用于语言模型预训练。GPT-1 的做法分两步：

1. **预训练**：在 BooksCorpus（约 800M 词）上用 CLM（预测下一个词）训练一个 12 层 Transformer Decoder (117M 参数)
2. **微调**：在下游任务（分类、NLI、QA 等）上用少量标注数据微调

结果：在 12 个 NLP 任务的 9 个上取得了最优——证明了"预训练通用语言模型 + 任务特定微调"的范式。

### 为什么这很重要？

GPT-1 和同期的 BERT 一起开创了"预训练 + 微调"时代。但两者的哲学不同：BERT 选择了双向理解（Encoder），GPT 选择了单向生成（Decoder）。当时学术界认为 BERT 更好——它在 GLUE 等理解类 benchmark 上分数更高。但历史证明，GPT 的方向更有前途。

### 但还有一个问题……

GPT-1 仍然需要微调——每个新任务都需要标注数据和一轮训练。能不能让模型不需要微调就能处理新任务？

> 🔑 **故事转折点：** 如果模型足够大、训练数据足够多，也许微调就不需要了？

---

## 📚 第四章：GPT-2 — "太危险了不敢发布"（2019）

> **关键人物：** Alec Radford, Jeffrey Wu, OpenAI
> **关键论文：** Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), 2019

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| GPT-2 论文首页 | OpenAI | `https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf` | 学术引用 |

### 发生了什么？

OpenAI 把模型扩大到 1.5B 参数（是 GPT-1 的 13 倍），训练数据换成了 WebText（800 万网页，40GB 文本）。然后他们发现了一件惊人的事：

**不需要微调**，只要把任务用自然语言描述出来，模型就能在零样本下完成。例如：
- 翻译：`"Translate English to French: cheese →"` → `"fromage"`
- 摘要：`"TL;DR:"` → 生成摘要

论文标题就是核心发现："Language Models are Unsupervised Multitask Learners"——语言模型是无监督的多任务学习器。

OpenAI 最初以"担心被滥用生成虚假新闻"为由拒绝发布完整模型，引发了 AI 安全和开放性的激烈讨论。

### 为什么这很重要？

GPT-2 暗示了一个范式转变：也许我们不需要为每个任务设计架构和收集标注数据——一个足够好的语言模型本身就是一个通用任务解决器。

### 但还有一个问题……

GPT-2 的零样本能力仍然不够强——在很多任务上不如微调后的 BERT。需要更大的模型来验证"缩放假说"。

> 🔑 **故事转折点：** 如果 10 倍的参数带来了质变，那 100 倍呢？

---

## 📚 第五章：GPT-3 — 上下文学习的诞生（2020）

> **关键人物：** Tom Brown, OpenAI
> **关键论文：** Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), NeurIPS 2020

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| GPT-3 论文首页 | arXiv | `https://arxiv.org/abs/2005.14165` | 学术引用 |

### 发生了什么？

OpenAI 把模型扩大到 **175B 参数**（是 GPT-2 的 117 倍），训练了约 300B token。然后他们发现了 In-Context Learning：

在 prompt 中给几个"输入→输出"示例，模型就能"学会"这个任务——**不需要梯度更新**。

更惊人的是**涌现能力**：模型展示出训练数据中从未明确包含的能力——算术、代码生成、逻辑推理。这些能力在小模型中完全不存在，只有当参数量超过某个阈值（约 100B）后才突然"涌现"。

### 为什么这很重要？

GPT-3 彻底改变了 NLP 的使用范式：
- **之前**：收集标注数据 → 训练模型 → 评估 → 部署
- **之后**：写一段 prompt → 直接用

这催生了 Prompt Engineering 这个全新的领域，也让非技术人员能"编程"AI。

### 但还有一个问题……

GPT-3 虽然强大，但它不"听话"——给它一个指令，它可能会续写成一篇文章而不是回答问题。它有时会说有毒、有偏见、或完全编造的内容。

> 🔑 **故事转折点：** 模型有了能力，但缺乏"对齐"——如何让它做人类真正想要它做的事？

---

## 📚 第六章：InstructGPT → ChatGPT — 对齐革命（2022-2023）

> **关键人物：** Long Ouyang, OpenAI
> **关键论文：** Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), NeurIPS 2022

#### 🎥 视觉素材

| 素材 | 来源 | 链接 | 版权 |
|------|------|------|------|
| InstructGPT 论文首页 | arXiv | `https://arxiv.org/abs/2203.02155` | 学术引用 |

### 发生了什么？

OpenAI 开发了 RLHF（基于人类反馈的强化学习）三步流程来"对齐"GPT-3：

1. **SFT (Supervised Fine-Tuning)**：用人工编写的高质量回答微调 GPT-3
2. **RM (Reward Model)**：让标注人员比较多个回答的好坏，训练一个打分模型
3. **PPO (Proximal Policy Optimization)**：用 RM 的打分作为奖励信号，用强化学习优化 GPT-3

结果就是 InstructGPT——一个 1.3B 的 InstructGPT 比 175B 的 GPT-3 更能理解和执行用户指令。

2022 年 11 月，OpenAI 把 RLHF 应用到更大的模型上，发布了 **ChatGPT**——它在 5 天内获得了 100 万用户，两个月内达到 1 亿用户，成为有史以来增长最快的应用。

### 为什么这很重要？

RLHF 证明了"能力"和"对齐"是两个独立的问题。GPT-3 有能力但不听话；InstructGPT/ChatGPT 既有能力又听话。这开启了 AI 安全和对齐研究的新时代。

> 📖 Paper: Ouyang et al., [InstructGPT](https://arxiv.org/abs/2203.02155), §1

---

## 🗺️ 全局回顾：技术演进路线图

    N-gram (1980s)
      │ 数据稀疏, 窗口小
      ▼
    神经语言模型 (2003)
      │ Bengio: 词嵌入 + 前馈网络
      ▼
    RNN/LSTM LM (2010)
      │ 理论上无限上下文, 但梯度消失
      ▼
    Transformer (2017)
      │ Vaswani: Self-Attention, 并行计算
      ▼
    GPT-1 (2018)
      │ 预训练(CLM) + 微调, 117M
      ▼
    GPT-2 (2019)
      │ 零样本能力, 1.5B
      ▼
    GPT-3 (2020)
      │ 上下文学习, 涌现能力, 175B
      ▼
    InstructGPT (2022)
      │ RLHF 对齐, 让模型听话
      ▼
    ChatGPT (2022.11)
      │ 改变世界的产品
      ▼
    GPT-4 (2023.3)
      │ 多模态 (图片+文本), 更强推理
      ▼
    未来: GPT-5, Agent, 多模态...

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| N-gram → 神经 LM | 数据稀疏 → 词嵌入自动泛化 |
| 前馈 → RNN/LSTM | 固定窗口 → 可变长上下文 |
| RNN → Transformer | 顺序计算 → 并行 + 全局注意力 |
| Transformer → GPT-1 | 单任务训练 → 预训练+微调 |
| GPT-1 → GPT-2 | 需要微调 → 零样本 |
| GPT-2 → GPT-3 | 零样本弱 → 上下文学习 + 涌现 |
| GPT-3 → InstructGPT | 有能力但不听话 → RLHF 对齐 |
| InstructGPT → ChatGPT | 研究模型 → 亿级用户产品 |

### 🎥 视觉素材总表（视频制作用）

| 章节 | 人物 | 肖像来源 | 论文/事件图片 | 版权 |
|------|------|---------|-------------|------|
| 第一章 | Frederick Jelinek | JHU CLSP 档案 | IBM 语音识别系统 | 学术引用 |
| 第二章 | Yoshua Bengio | Wikimedia Commons: `File:Yoshua_Bengio_-_2017.jpg` | JMLR 论文首页 | CC BY-SA 4.0 |
| 第三章 | Alec Radford | OpenAI 团队页面 | GPT-1 论文首页 | 学术引用 |
| 第四章 | Alec Radford | OpenAI 团队页面 | GPT-2 论文首页 | 学术引用 |
| 第五章 | Tom Brown | OpenAI | arXiv: `2005.14165` | 学术引用 |
| 第六章 | Long Ouyang | OpenAI | arXiv: `2203.02155` | 学术引用 |
