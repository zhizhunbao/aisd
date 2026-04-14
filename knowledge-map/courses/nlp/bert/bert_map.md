---
topic: bert
dimension: map
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📖 Paper: Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📚 Book: Jurafsky & Martin, Speech and Language Processing 3rd Ed., Ch.11 — file:///C:/Users/40270/Desktop/workspace/textbook-rag/data/raw_pdfs/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Eisenstein, Introduction to NLP, Ch.14 — file:///C:/Users/40270/Desktop/workspace/textbook-rag/data/raw_pdfs/textbooks/eisenstein_nlp.pdf"
expiry: 12m
status: current
---

# BERT 知识地图

> 📖 Paper: Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📚 Book: Jurafsky & Martin, [SLP3](../../../textbooks/jurafsky_slp3.pdf), Ch.11

---

## 1. 核心问题

- **BERT 是什么？** → 一种基于 Transformer Encoder 的双向预训练语言表示模型，通过 Masked Language Model (MLM) 和 Next Sentence Prediction (NSP) 两个任务在无标注文本上预训练，再在下游任务上微调
- **为什么需要双向？** → 单向模型（如 GPT）只能看到左侧上下文，BERT 通过 MLM 让每个 token 同时关注左右上下文，获得更丰富的语义表示
- **BERT 如何在不同任务上通用？** → 统一架构 + 最少的任务特定参数：预训练和微调使用几乎相同的网络结构，只需添加一个输出层即可适配分类、问答、序列标注等任务
- **预训练-微调范式的核心优势？** → 在大规模无标注数据上学习通用语言知识，微调时只需少量标注数据即可达到 SOTA，大幅降低了对任务特定架构设计的需求
- **BERT 的历史地位？** → 2018 年发布时在 11 个 NLP 基准上刷新记录（GLUE 80.5%、SQuAD F1 93.2），开启了预训练语言模型时代

> 📖 Paper: Devlin et al. (2019), Abstract & Section 1
> 📚 Book: Jurafsky & Martin, SLP3, Ch.11 §9.2

---

## 2. 全景位置

```
自然语言处理 (NLP)
├── 传统方法
│   ├── 规则与特征工程
│   └── 统计模型 (n-gram, HMM, CRF)
├── 词向量 (Static Embeddings)
│   ├── Word2Vec (2013)
│   └── GloVe (2014)
├── 上下文化表示 (Contextual Embeddings) ← 你在这里
│   ├── ELMo (双向 LSTM, feature-based)
│   ├── 【BERT】(双向 Transformer, fine-tuning)
│   ├── GPT (单向 Transformer, fine-tuning)
│   └── XLNet / RoBERTa / ALBERT (BERT 变体)
└── 大语言模型 (LLM)
    ├── GPT-3/4 (自回归生成)
    └── T5 / BART (Encoder-Decoder)
```

> 📖 Paper: Devlin et al. (2019), Figure 3 — ELMo vs GPT vs BERT 架构对比
> 📚 Book: Jurafsky & Martin, SLP3, Ch.11 §9.1

---

## 3. 依赖地图

```
前置知识                     本主题                    后续方向
┌────────────────────┐      ┌───────────────────┐     ┌──────────────────────────┐
│ Transformer 架构    │─────→│                   │────→│ RoBERTa (更强预训练策略)  │
│ Self-Attention 机制 │─────→│                   │────→│ ALBERT (参数共享/分解)    │
│ 词向量 (Word2Vec)   │─────→│      BERT         │────→│ SpanBERT (span 级掩码)   │
│ 语言模型 (LM 基础)  │─────→│                   │────→│ ELECTRA (替换检测目标)    │
│ 迁移学习概念        │─────→│                   │────→│ GPT 系列 (自回归路线)     │
└────────────────────┘      └───────────────────┘     └──────────────────────────┘
```

> 📚 Book: Jurafsky & Martin, SLP3, Ch.11 §9.3
> 📖 Paper: Devlin et al. (2019), Section 2 Related Work

---

## 4. 文件地图

| 文件 | 定位 | 何时用 |
|------|------|--------|
| [bert_map.md](bert_map.md) | ① 导航 | 第一次接触、需要全局视角 |
| [bert_concepts.md](bert_concepts.md) | ② 概念 | 理解术语定义、辨析易混淆概念 |
| [bert_math.md](bert_math.md) | ③ 公式 | 推导公式、理解数学基础 |
| [bert_tutorial.md](bert_tutorial.md) | ④ 教程 | Why-First 理解设计动机与原理 |
| [bert_code.md](bert_code.md) | ⑤ 代码 | 快速上手实现 |
| [bert_pitfalls.md](bert_pitfalls.md) | ⑥ 踩坑 | 调试问题 |
| [bert_history.md](bert_history.md) | ⑦ 历史 | 了解技术演进 |
| [bert_bridge.md](bert_bridge.md) | ⑧ 衔接 | 找相关主题、扩展阅读 |
| [bert_first_principles.md](bert_first_principles.md) | ⑨ 第一性原理 | 追问底层公理、理解边界 |

---

## 5. 学习/使用路线

### 第一次学习 🎒

1. 读 [bert_map.md](bert_map.md) 了解全局位置
2. 读 [bert_tutorial.md](bert_tutorial.md) Section 1 理解动机
3. 读 [bert_concepts.md](bert_concepts.md) 掌握核心术语
4. 读 [bert_math.md](bert_math.md) 手算一次核心公式
5. 跟 [bert_code.md](bert_code.md) 快速开始跑一个示例
6. 读 [bert_history.md](bert_history.md) 了解技术演进
7. 读 [bert_first_principles.md](bert_first_principles.md) 追问底层公理

### 日常参考 🔧

1. 查 [bert_code.md](bert_code.md) API 速查表
2. 查 [bert_math.md](bert_math.md) 公式速查
3. 查 [bert_pitfalls.md](bert_pitfalls.md) 排查问题

### 深度研究 🔬

1. 读 [bert_history.md](bert_history.md) 完整演进线
2. 读 [bert_first_principles.md](bert_first_principles.md) 追问底层公理
3. 读 [bert_bridge.md](bert_bridge.md) 探索下游任务
4. 阅读原始论文

---

## 6. 缺口检查

| 维度 | 状态 |
|------|------|
| Map | ✅ 已完成 |
| Concepts | ⬜ 待生成 |
| Math | ⬜ 待生成 |
| Tutorial | ⬜ 待生成 |
| Code | ⬜ 待生成 |
| Pitfalls | ⬜ 待生成 |
| History | ⬜ 待生成 |
| Bridge | ⬜ 待生成 |
| First Principles | ⬜ 待生成 |

---

## 7. 新鲜度状态

| 维度 | 上次验证 | 过期时间 | 状态 |
|------|---------|---------|------|
| Map | 2026-04-13 | 12m | ✅ current |
| Concepts | 2026-04-13 | 12m | ⬜ pending |
| Math | 2026-04-13 | 12m | ⬜ pending |
| Tutorial | 2026-04-13 | 12m | ⬜ pending |
| Code | 2026-04-13 | 6m | ⬜ pending |
| Pitfalls | 2026-04-13 | 6m | ⬜ pending |
| History | 2026-04-13 | never | ⬜ pending |
| Bridge | 2026-04-13 | 12m | ⬜ pending |
| First Principles | 2026-04-13 | 12m | ⬜ pending |

---

## 8. 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Devlin et al. (2019)](https://arxiv.org/abs/1810.04805) | 📖 论文 | 全文核心参考 |
| [SLP3 Ch.11](../../../textbooks/jurafsky_slp3.pdf) | 📚 教科书 | Concepts, Math, Tutorial, History |
| [Eisenstein NLP Ch.14](../../../textbooks/eisenstein_nlp.pdf) | 📚 教科书 | First Principles, Bridge |
| [HuggingFace Transformers](https://huggingface.co/docs/transformers/) | 📖 文档 | Code |
| [google-research/bert](https://github.com/google-research/bert) | 💻 源码 | Code 参考实现 |

---
