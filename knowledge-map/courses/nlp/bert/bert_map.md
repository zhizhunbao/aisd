---
topic: bert
dimension: map
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Eisenstein, 《Natural Language Processing》, Ch.18 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/eisenstein_nlp.pdf"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/model_doc/bert"
expiry: 12m
status: current
---

# BERT 知识地图

> 📖 Paper: Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📚 Book: Jurafsky & Martin, [《Speech and Language Processing》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

## 1. 核心问题

- **BERT 和之前的语言模型（如 GPT）最大的区别是什么？** → BERT 是双向的——同时看左边和右边的上下文来理解每个词，而 GPT 只能从左到右单向看
- **什么是掩码语言模型（MLM）？** → 随机遮住输入句子中 15% 的词，让模型去猜被遮住的词，从而学到真正的双向上下文表示
- **BERT 的"预训练 + 微调"范式为什么重要？** → 一次大规模无监督预训练，之后只需少量标注数据微调就能在各种 NLP 任务上达到最优，大幅降低了任务特定数据的需求
- **BERT 的输入是怎么构造的？** → Token Embedding + Segment Embedding + Position Embedding 三者相加，其中 [CLS] 用于分类，[SEP] 用于分隔句子
- **BERT 有哪些主要变体，它们分别改进了什么？** → RoBERTa 去掉了 NSP 并加大数据量；DistilBERT 做了知识蒸馏减小体积；ALBERT 做了参数共享减少参数

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), NAACL 2019, §1-2

---

## 2. 全景位置

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
        ├── 【BERT】 (双向 Transformer, MLM+NSP)
        ├── GPT 系列 (单向, 自回归)
        ├── T5 (编码器-解码器, Text-to-Text)
        ├── RoBERTa / ALBERT / DistilBERT (BERT 变体)
        ├── XLNet (排列语言模型)
        └── ELECTRA (替换 Token 检测)

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11 "Transfer Learning"
> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §2 "Related Work"

---

## 3. 依赖地图

    前置知识                       本主题                       后续方向
    ┌───────────────────────┐     ┌──────────────────────┐     ┌────────────────────────────┐
    │ Transformer 架构       │────→│                      │────→│ RoBERTa / ALBERT 变体优化    │
    │ (Self-Attention, MHA) │     │                      │     │                            │
    │                       │     │                      │────→│ DistilBERT 知识蒸馏          │
    ├───────────────────────┤     │       BERT           │     │                            │
    │ 词嵌入                 │────→│  (Bidirectional      │────→│ 微调下游任务                  │
    │ (Word2Vec, 子词分词)   │     │   Encoder            │     │ (分类/NER/QA/NLI)          │
    │                       │     │   Representations)   │     │                            │
    ├───────────────────────┤     │                      │────→│ GPT 对比 → 理解双向 vs 单向   │
    │ 语言模型基础            │────→│                      │     │                            │
    │ (MLM, 上下文表示)      │     │                      │────→│ PEFT (LoRA / Adapter)      │
    └───────────────────────┘     └──────────────────────┘     └────────────────────────────┘

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §2-3
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.11

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [bert_map.md](bert_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [bert_concepts.md](bert_concepts.md) | ② 概念 | 理解 MLM/NSP/[CLS]/[SEP] 等术语 |
| [bert_math.md](bert_math.md) | ③ 公式 | 推导注意力得分、MLM 损失函数 |
| [bert_tutorial.md](bert_tutorial.md) | ④ 教程 | Why-First 理解 BERT 设计动机 |
| [bert_code.md](bert_code.md) | ⑤ 代码 | 快速上手 HuggingFace BERT 微调 |
| [bert_pitfalls.md](bert_pitfalls.md) | ⑥ 踩坑 | 微调时学习率过高/输入截断等常见问题 |
| [bert_history.md](bert_history.md) | ⑦ 历史 | 从 Word2Vec 到 BERT 的技术演进 |
| [bert_bridge.md](bert_bridge.md) | ⑧ 衔接 | 连接 Transformer / GPT / 下游任务 |
| [bert_first_principles.md](bert_first_principles.md) | ⑨ 第一性原理 | 追问"为什么双向比单向好" |

> 📖 Docs: Norman, 《The Design of Everyday Things》(2013), Ch.3 "Knowledge in the World"

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [bert_map.md](bert_map.md) 了解 BERT 在 NLP 全景中的位置
2. 读 [bert_tutorial.md](bert_tutorial.md) Section 1 理解"为什么需要双向语言模型"
3. 读 [bert_concepts.md](bert_concepts.md) 掌握 MLM / NSP / [CLS] / WordPiece 等核心术语
4. 读 [bert_math.md](bert_math.md) 手算一次 MLM 损失函数
5. 跟 [bert_code.md](bert_code.md) 用 HuggingFace 跑一个情感分类微调
6. 读 [bert_history.md](bert_history.md) 了解从 Word2Vec → ELMo → BERT 的演进
7. 读 [bert_first_principles.md](bert_first_principles.md) 理解双向上下文的数学基础

### 日常参考 🔧

1. 查 [bert_code.md](bert_code.md) HuggingFace API 速查表
2. 查 [bert_math.md](bert_math.md) Attention 和 MLM 公式速查
3. 查 [bert_pitfalls.md](bert_pitfalls.md) 排查微调常见问题

### 深度研究 🔬

1. 读 [bert_history.md](bert_history.md) 完整演进线
2. 读 [bert_first_principles.md](bert_first_principles.md) 追问双向表示的本质
3. 读 [bert_bridge.md](bert_bridge.md) 对比 BERT vs GPT vs T5
4. 阅读原始论文 [Devlin et al. 2019](https://arxiv.org/abs/1810.04805)

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
| [Devlin et al. "BERT" (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | 全文核心参考——BERT 原始论文 |
| [《SLP3》Ch.11](../../../textbooks/jurafsky_slp3_jan2026.pdf) | 📚 教科书 | Transfer Learning, BERT 架构讲解 |
| [《NLP》Ch.18](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | 预训练语言模型理论 |
| [Liu et al. "RoBERTa" (2019)](https://arxiv.org/abs/1907.11692) | 📖 论文 | History, Bridge——BERT 训练策略改进 |
| [Sanh et al. "DistilBERT" (2019)](https://arxiv.org/abs/1910.01108) | 📖 论文 | History, Bridge——BERT 知识蒸馏 |
| [Lan et al. "ALBERT" (2019)](https://arxiv.org/abs/1909.11942) | 📖 论文 | History, Bridge——BERT 参数共享 |
| [Clark et al. "ELECTRA" (2020)](https://arxiv.org/abs/2003.10555) | 📖 论文 | History, Bridge——替换 Token 检测 |
| [HuggingFace BERT Docs](https://huggingface.co/docs/transformers/model_doc/bert) | 📖 文档 | Code——API 接口和使用方法 |
| [Peters et al. "ELMo" (2018)](https://arxiv.org/abs/1802.05365) | 📖 论文 | History——BERT 的前驱 |
| [Vaswani et al. "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) | 📖 论文 | Math, Tutorial——Transformer 架构基础 |
