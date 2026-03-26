---
topic: gpt
dimension: map
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Radford et al., 'Improving Language Understanding by Generative Pre-Training', OpenAI 2018 — https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf"
  - "📖 Paper: Radford et al., 'Language Models are Unsupervised Multitask Learners', OpenAI 2019 — https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"
  - "📖 Paper: Brown et al., 'Language Models are Few-Shot Learners', NeurIPS 2020 — https://arxiv.org/abs/2005.14165"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.10-11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Eisenstein, 《Natural Language Processing》, Ch.18 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/eisenstein_nlp.pdf"
expiry: 12m
status: current
---

# GPT 知识地图

> 📖 Paper: Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), OpenAI 2018
> 📖 Paper: Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), NeurIPS 2020
> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10-11

## 1. 核心问题

- **GPT 和 BERT 最大的区别是什么？** → GPT 是单向自回归模型——只从左到右依次预测下一个词，而 BERT 是双向的同时看左右上下文。GPT 天生擅长生成文本，BERT 擅长理解文本
- **什么是自回归语言模型（Autoregressive LM）？** → 给定前面所有的词，预测下一个词的概率。GPT 把这个目标做到了极致：用 Transformer Decoder 逐个生成 token
- **GPT 的"预训练 + 微调"范式和 BERT 有什么不同？** → GPT-1 同样是先预训练再微调，但到了 GPT-2/3 发现，模型足够大时不需要微调，直接"提示"（prompt）就能完成各种任务——这催生了 In-Context Learning
- **GPT 系列的演进路线是什么？** → GPT-1 (117M, 预训练+微调) → GPT-2 (1.5B, 零样本) → GPT-3 (175B, 少样本/上下文学习) → GPT-4 (多模态, RLHF)
- **为什么 GPT-3 的"上下文学习"是革命性的？** → 不需要梯度更新/微调，只在 prompt 中给几个示例，模型就能"学会"新任务——这彻底改变了 NLP 的使用范式

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1-2
> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §1

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
│   └── Seq2Seq + Attention
├── Transformer 架构
│   ├── 原始 Transformer (Vaswani 2017)
│   └── 位置编码 + 多头注意力
└── 预训练语言模型 ← 你在这里
    ├── ELMo (上下文嵌入先驱, biLSTM)
    ├── BERT (双向 Transformer, MLM+NSP)
    ├── 【GPT 系列】 (单向自回归, Decoder-Only)
    │   ├── GPT-1 (预训练+微调, 117M)
    │   ├── GPT-2 (零样本, 1.5B)
    │   ├── GPT-3 (上下文学习, 175B)
    │   └── GPT-4 (多模态, RLHF)
    ├── T5 (编码器-解码器, Text-to-Text)
    ├── LLaMA / PaLM / Claude (开源/闭源 LLM)
    └── ELECTRA / XLNet (其他变体)
```

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10 "Language Models", Ch.11 "Transfer Learning"
> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §2 "Related Work"

---

## 3. 依赖地图

```
前置知识                       本主题                       后续方向
┌───────────────────────┐     ┌──────────────────────┐     ┌──────────────────────────────┐
│ Transformer 架构       │────→│                      │────→│ GPT-4 / 多模态大模型          │
│ (Self-Attention, MHA) │     │                      │     │                              │
│                       │     │                      │────→│ InstructGPT / ChatGPT (RLHF) │
├───────────────────────┤     │   GPT 系列            │     │                              │
│ 语言模型基础            │────→│  (Autoregressive      │────→│ Prompt Engineering           │
│ (N-gram, 困惑度)       │     │   Decoder-Only        │     │ (提示工程, CoT, Few-Shot)     │
│                       │     │   Language Model)      │     │                              │
├───────────────────────┤     │                      │────→│ PEFT (LoRA / Adapter)        │
│ 词嵌入                 │────→│                      │     │                              │
│ (Word2Vec, BPE 分词)  │     │                      │────→│ BERT 对比 → 理解生成 vs 理解   │
└───────────────────────┘     └──────────────────────┘     └──────────────────────────────┘
```

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §2-3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.10-11

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [gpt_map.md](gpt_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [gpt_concepts.md](gpt_concepts.md) | ② 概念 | 理解 CLM/BPE/因果掩码/KV Cache 等术语 |
| [gpt_math.md](gpt_math.md) | ③ 公式 | 推导自回归损失函数、注意力计算 |
| [gpt_tutorial.md](gpt_tutorial.md) | ④ 教程 | Why-First 理解 GPT 设计动机 |
| [gpt_code.md](gpt_code.md) | ⑤ 代码 | 快速上手 HuggingFace GPT-2 文本生成 |
| [gpt_pitfalls.md](gpt_pitfalls.md) | ⑥ 踩坑 | 生成重复/温度设置/上下文截断等常见问题 |
| [gpt_history.md](gpt_history.md) | ⑦ 历史 | 从 N-gram 到 GPT-4 的技术演进 |
| [gpt_bridge.md](gpt_bridge.md) | ⑧ 衔接 | 连接 BERT / Transformer / LLM 生态 |
| [gpt_first_principles.md](gpt_first_principles.md) | ⑨ 第一性原理 | 追问"为什么自回归能涌现智能" |

> 📖 Docs: Norman, 《The Design of Everyday Things》(2013), Ch.3 "Knowledge in the World"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [gpt_map.md](gpt_map.md) 了解 GPT 在 NLP 全景中的位置
2. 读 [gpt_tutorial.md](gpt_tutorial.md) Section 1 理解"为什么需要自回归语言模型"
3. 读 [gpt_concepts.md](gpt_concepts.md) 掌握 CLM / BPE / 因果掩码 / In-Context Learning 等核心术语
4. 读 [gpt_math.md](gpt_math.md) 手算一次自回归损失函数
5. 跟 [gpt_code.md](gpt_code.md) 用 HuggingFace 跑一个 GPT-2 文本生成
6. 读 [gpt_history.md](gpt_history.md) 了解从 N-gram → RNN → Transformer → GPT 的演进
7. 读 [gpt_first_principles.md](gpt_first_principles.md) 理解自回归模型的数学根基

### 日常参考 🔧

1. 查 [gpt_code.md](gpt_code.md) HuggingFace API 速查表
2. 查 [gpt_math.md](gpt_math.md) 自回归损失和采样公式速查
3. 查 [gpt_pitfalls.md](gpt_pitfalls.md) 排查生成类常见问题

### 深度研究 🔬

1. 读 [gpt_history.md](gpt_history.md) 完整演进线
2. 读 [gpt_first_principles.md](gpt_first_principles.md) 追问自回归与涌现
3. 读 [gpt_bridge.md](gpt_bridge.md) 对比 GPT vs BERT vs T5
4. 阅读原始论文 [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)、[GPT-3](https://arxiv.org/abs/2005.14165)

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
| [Radford et al. "GPT-1" (2018)](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) | 📖 论文 | 全文核心参考——GPT-1 原始论文 |
| [Radford et al. "GPT-2" (2019)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | 📖 论文 | Concepts, History——零样本学习 |
| [Brown et al. "GPT-3" (2020)](https://arxiv.org/abs/2005.14165) | 📖 论文 | Concepts, History, First Principles——上下文学习 |
| [Ouyang et al. "InstructGPT" (2022)](https://arxiv.org/abs/2203.02155) | 📖 论文 | History, Bridge——RLHF 对齐 |
| [OpenAI "GPT-4 Technical Report" (2023)](https://arxiv.org/abs/2303.08774) | 📖 论文 | History, Bridge——多模态 |
| [《SLP3》Ch.10-11](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | Language Models, Transfer Learning |
| [《NLP》Ch.18](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | 预训练语言模型理论 |
| [Vaswani et al. "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | Math, Tutorial——Transformer 架构基础 |
| [HuggingFace GPT-2 Docs](https://huggingface.co/docs/transformers/model_doc/gpt2) | 📖 文档 | Code——API 接口和使用方法 |
| [Devlin et al. "BERT" (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | Concepts, Bridge——双向 vs 单向对比 |
