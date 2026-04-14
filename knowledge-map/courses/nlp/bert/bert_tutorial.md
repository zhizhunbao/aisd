---
topic: bert
dimension: tutorial
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019"
  - "📚 Book: Jurafsky & Martin, SLP3 Ch.11"
expiry: 12m
status: current
---

# BERT 教程

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📚 Book: Jurafsky & Martin, [SLP3](../../../textbooks/jurafsky_slp3.pdf), Ch.11

---

## Section 1: 它解决什么问题（Why）

![BERT Pre-training & Fine-tuning](textbook_screenshots/concepts_1_devlin_2019_bert_p2.png)

> 📚 Source: Devlin et al. (2019), Figure 1, p.3

![BERT Input Representation](textbook_screenshots/math_extra_devlin_2019_bert_p4_1.png)

> 📚 Source: Devlin et al. (2019), Figure 2, p.5

### 🔥 没有 BERT 之前的三大痛点

1. **每个 NLP 任务都要从头设计模型** — 情感分析用 CNN，问答用 BiDAF，NER 用 BiLSTM-CRF……每换一个任务就要重新设计网络结构、重新训练参数、重新调超参

2. **标注数据稀缺且昂贵** — 监督学习需要大量人工标注。一个 SQuAD 数据集需要花 $50k+，但只能用于问答；做 NER 还得再花 $50k 标另一套数据

3. **词向量只是"静态快照"** — Word2Vec/GloVe 给每个词一个固定向量，但同一个词在不同语境下含义不同（"bank" 可以是银行也可以是河岸）。ELMo 尝试用双向 LSTM 解决，但只是浅层拼接两个方向

> 📖 Paper: Devlin et al. (2019), Section 1 — "The major limitation [of existing methods] is that standard language models are unidirectional, and this limits the choice of architectures that can be used during pre-training."

### ✅ BERT 的核心价值

| 痛点 | BERT 的解决方案 |
|------|---------------|
| 每个任务重新设计 | **统一架构** — 预训练一次，所有任务只加一个输出层 |
| 标注数据稀缺 | **无标注预训练** — 在 3.3B 词的无标注文本上学通用知识 |
| 静态词向量 | **深度双向** — 每个 token 同时看左右所有上下文，动态生成 |

> 📚 Book: Jurafsky & Martin, SLP3, p.209

---

## Section 2: 它怎么工作的（How — 底层原理）

### Step 1: 输入构造

BERT 把任意文本转换为统一格式：

```
[CLS]  my  dog  is  cute  [SEP]  he  likes  play  ##ing  [SEP]
  ↓    ↓    ↓    ↓    ↓     ↓     ↓     ↓     ↓      ↓     ↓
Token: E_CLS E_my E_dog ...                    (WordPiece 词表)
  +
Segment: E_A   E_A  E_A  E_A  E_A   E_A   E_B   E_B   E_B   E_B   E_B
  +
Position: E_0   E_1  E_2  E_3  E_4   E_5   E_6   E_7   E_8   E_9   E_10
  =
Input:   三者逐元素相加
```

> 📖 Paper: Devlin et al. (2019), Figure 2, Section 3

### Step 2: 预训练任务 1 — Masked Language Model (MLM)

![MLM Training](textbook_screenshots/math_extra_jurafsky_slp3_p210_1.png)

> 📚 Source: Jurafsky & Martin, SLP3, Figure 9.3, p.211

**过程**：
1. 随机选择 15% 的 token
2. 对选中的 token：80% 替换为 [MASK]，10% 换随机词，10% 不变
3. 模型预测被选中位置的原始 token
4. 只在选中位置计算交叉熵损失

> **为什么不全替换 [MASK]？** — 如果只见过 [MASK]，微调时没有 [MASK] token，模型会"认不出"正常词。保留 10% 原词 + 10% 随机词，迫使模型始终保持对每个位置的预测能力。

> 📚 Book: Jurafsky & Martin, SLP3, p.210-211

### Step 3: 预训练任务 2 — Next Sentence Prediction (NSP)

![NSP Training](textbook_screenshots/math_extra_jurafsky_slp3_p212_1.png)

> 📚 Source: Jurafsky & Martin, SLP3, Figure 9.4, p.213

**过程**：
1. 50% 的句对是真正连续的（IsNext）
2. 50% 的 B 句是从语料库随机抽取的（NotNext）
3. [CLS] 的输出通过 softmax 二分类

> 📚 Book: Jurafsky & Martin, SLP3, p.212

### Step 4: 微调（Fine-tuning）

预训练完成后，针对具体任务只需：
1. 保持 BERT 权重不变
2. 添加一个任务特定的输出层（线性层 + softmax）
3. 用任务标注数据端到端微调所有参数

| 任务类型 | 输入格式 | 输出取自 |
|---------|---------|---------|
| 文本分类（情感分析） | [CLS] 句子 [SEP] | [CLS] 向量 → softmax |
| 句对分类（NLI） | [CLS] 句A [SEP] 句B [SEP] | [CLS] 向量 → softmax |
| 问答（SQuAD） | [CLS] 问题 [SEP] 段落 [SEP] | 每个 token → start/end |
| 序列标注（NER） | [CLS] 句子 [SEP] | 每个 token → 标签 |

> 📖 Paper: Devlin et al. (2019), Section 4

---

## Section 3: 局限性

1. **输入长度限制 512 token** — BERT 使用固定长度的位置编码，超过 512 个 token 的文档无法处理 → 应对：使用 Longformer、BigBird 等长文档模型

2. **预训练-微调不匹配** — 预训练时有 [MASK] token，微调时没有；虽然 80/10/10 策略缓解了这个问题，但本质不匹配依然存在 → 应对：ELECTRA 使用"替换检测"完全避免 [MASK]

3. **只适合理解，不适合生成** — Encoder-only 架构无法自回归生成文本 → 应对：GPT 系列（Decoder-only）或 T5/BART（Encoder-Decoder）

> 📖 Paper: Devlin et al. (2019), Section 3.1

---
