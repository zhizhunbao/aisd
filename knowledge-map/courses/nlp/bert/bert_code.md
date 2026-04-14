---
topic: bert
dimension: code
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📖 Docs: HuggingFace Transformers — https://huggingface.co/docs/transformers/"
  - "💻 Code: google-research/bert — https://github.com/google-research/bert"
expiry: 6m
status: current
---

# BERT 代码参考

> 📖 Docs: [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
> 💻 Code: [google-research/bert](https://github.com/google-research/bert)

---

## 快速开始

```python
# pip install transformers torch
from transformers import BertTokenizer, BertModel

# 加载预训练模型和分词器
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# 编码输入
text = "Hello, BERT is amazing!"
inputs = tokenizer(text, return_tensors="pt")
# inputs 包含: input_ids, token_type_ids, attention_mask

# 前向传播
outputs = model(**inputs)
# outputs.last_hidden_state: [batch, seq_len, 768] — 每个 token 的上下文表示
# outputs.pooler_output:     [batch, 768] — [CLS] 输出过一个 Dense + Tanh
```

> 📖 Docs: HuggingFace Transformers, Quick Tour

---

## 核心示例

### 示例 1: 文本分类（情感分析）

```python
from transformers import BertForSequenceClassification, BertTokenizer
import torch

# 加载微调过的模型（SST-2 情感分析）
model = BertForSequenceClassification.from_pretrained(
    "textattack/bert-base-uncased-SST-2"
)
tokenizer = BertTokenizer.from_pretrained("textattack/bert-base-uncased-SST-2")

# 预测
text = "This movie is absolutely wonderful!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

with torch.no_grad():
    outputs = model(**inputs)

# logits → 概率
probs = torch.softmax(outputs.logits, dim=-1)
label = "positive" if probs[0][1] > 0.5 else "negative"
print(f"{label}: {probs[0][1]:.3f}")  # positive: 0.998
```

> 📖 Paper: Devlin et al. (2019), Section 4.1

### 示例 2: Masked Language Model（填空预测）

```python
from transformers import pipeline

# 使用 pipeline 简化调用
unmasker = pipeline("fill-mask", model="bert-base-uncased")

# 预测被遮盖的词
results = unmasker("BERT is a [MASK] model for NLP.")
for r in results[:3]:
    print(f"  {r['token_str']:12s}  score: {r['score']:.3f}")
# 输出示例:
#   great          score: 0.112
#   powerful       score: 0.089  
#   good           score: 0.075
```

> 📖 Paper: Devlin et al. (2019), Section 3.1 — Masked LM

### 示例 3: 抽取式问答（SQuAD）

```python
from transformers import pipeline

# 加载 QA pipeline
qa = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

result = qa(
    question="What does BERT stand for?",
    context="BERT stands for Bidirectional Encoder Representations from Transformers. "
            "It was developed by Google AI Language team."
)
print(f"Answer: {result['answer']}")   # Bidirectional Encoder Representations from Transformers
print(f"Score:  {result['score']:.3f}") # 0.987
```

> 📖 Paper: Devlin et al. (2019), Section 4.2. — SQuAD

---

## API 速查

### BertTokenizer

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 输入文本 | 必填 |
| `text_pair` | 第二个句子（句对任务） | None |
| `max_length` | 最大 token 数 | 512 |
| `truncation` | 是否截断超长输入 | False |
| `padding` | 填充策略 | False |
| `return_tensors` | 返回类型 ("pt"/"tf"/"np") | None |

### BertModel / BertForSequenceClassification

| 输出字段 | 形状 | 说明 |
|---------|------|------|
| `last_hidden_state` | [B, L, H] | 每个 token 最终层的上下文表示 |
| `pooler_output` | [B, H] | [CLS] 经过 Dense+Tanh |
| `logits` | [B, K] | 分类模型的未归一化预测 |

### 常用预训练模型

| 模型名 | 参数量 | 用途 |
|--------|-------|------|
| `bert-base-uncased` | 110M | 通用基础模型 |
| `bert-large-uncased` | 340M | 高精度模型 |
| `bert-base-chinese` | 110M | 中文 BERT |
| `bert-base-multilingual-cased` | 110M | 多语言 BERT |

> 📖 Docs: HuggingFace Transformers API Reference

---
