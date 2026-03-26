---
topic: bert
dimension: code
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Docs: Hugging Face Transformers BERT — https://huggingface.co/docs/transformers/model_doc/bert"
  - "📖 Docs: Hugging Face Transformers Fine-Tuning — https://huggingface.co/docs/transformers/training"
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
expiry: 6m
status: current
---

# BERT 代码参考

> 📖 Docs: [HuggingFace Transformers BERT](https://huggingface.co/docs/transformers/model_doc/bert)

## 快速开始

### 最简示例 — 30 秒上手

```python
# ============================================================
# BERT 情感分类推理 / BERT Sentiment Classification Inference
# 30 秒体验 BERT 做文本分类 / 30-second BERT text classification demo
# ============================================================
from transformers import pipeline  # 高层 API / High-level API

# 加载预训练好的情感分析管道 / Load pre-trained sentiment analysis pipeline
classifier = pipeline("sentiment-analysis")  # 默认用 distilbert-base-uncased-finetuned-sst-2-english

# 做推理 / Run inference
result = classifier("I love this movie! It's absolutely fantastic.")
print(result)  # [{'label': 'POSITIVE', 'score': 0.9998}]

# 批量推理 / Batch inference
results = classifier([
    "This is the worst experience ever.",
    "The food was okay, nothing special.",
    "Absolutely brilliant performance!"
])
for r in results:
    print(f"{r['label']}: {r['score']:.4f}")
```

**测试方法：** `pip install transformers torch` 后直接运行，第一次会自动下载模型。

> 📖 Docs: [HuggingFace Pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines)

---

## 完整实现示例

### 示例 1: BERT 文本分类微调

```python
# ============================================================
# 1. 环境准备 / Environment Setup
# ============================================================
# pip install transformers datasets torch scikit-learn

import torch
from transformers import (  # HuggingFace 核心组件 / Core HF components
    BertTokenizer,          # BERT 分词器 / BERT tokenizer
    BertForSequenceClassification,  # 带分类头的 BERT / BERT with classification head
    AdamW,                  # 优化器 / Optimizer
    get_linear_schedule_with_warmup  # 学习率调度器 / LR scheduler
)
from torch.utils.data import DataLoader, TensorDataset  # PyTorch 数据加载 / Data loading
from sklearn.model_selection import train_test_split  # 数据集划分 / Dataset split

# ============================================================
# 2. 数据准备 / Data Preparation
# ============================================================
# 示例数据 / Sample data (实际项目用 datasets 库加载)
texts = [
    "I absolutely love this product!",          # 正面 / Positive
    "Terrible quality, waste of money.",         # 负面 / Negative
    "It's okay, nothing special.",               # 负面 / Negative
    "Best purchase I've ever made!",             # 正面 / Positive
    "Disappointing experience overall.",         # 负面 / Negative
    "Fantastic service and great value!",        # 正面 / Positive
]
labels = [1, 0, 0, 1, 0, 1]  # 1=正面, 0=负面 / 1=positive, 0=negative

# 加载 BERT 分词器 / Load BERT tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# 编码文本 / Encode texts
# padding=True: 填充到最长序列 / Pad to longest
# truncation=True: 超过 max_length 截断 / Truncate if exceeds max_length
# return_tensors="pt": 返回 PyTorch 张量 / Return PyTorch tensors
encodings = tokenizer(
    texts,
    padding=True,       # 填充到批次最大长度 / Pad to batch max length
    truncation=True,    # 截断超长序列 / Truncate long sequences
    max_length=128,     # 最大 token 数 / Max token count
    return_tensors="pt" # 返回 PyTorch 张量 / Return PyTorch tensors
)

# 创建数据集和加载器 / Create dataset and dataloader
dataset = TensorDataset(
    encodings["input_ids"],       # token ID 序列 / Token ID sequence
    encodings["attention_mask"],  # 注意力掩码 (1=真实token, 0=padding) / Attention mask
    torch.tensor(labels)          # 标签 / Labels
)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# ============================================================
# 3. 模型定义 / Model Definition
# ============================================================
# 加载预训练 BERT + 分类头 / Load pre-trained BERT + classification head
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",  # 预训练模型名 / Pre-trained model name
    num_labels=2          # 分类数 (正/负) / Number of classes (pos/neg)
)

# 设备选择 / Device selection
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# ============================================================
# 4. 训练配置 / Training Configuration
# ============================================================
# BERT 微调推荐超参 / Recommended BERT fine-tuning hyperparameters
# (Devlin et al., 2019, §A.3)
optimizer = AdamW(
    model.parameters(),
    lr=2e-5,            # 学习率 (BERT 推荐 2e-5~5e-5) / Learning rate
    weight_decay=0.01   # 权重衰减 / Weight decay
)

epochs = 3  # 微调 epoch 数 (推荐 2-4) / Fine-tuning epochs (recommended 2-4)
total_steps = len(dataloader) * epochs

# 学习率预热调度 / Learning rate warmup schedule
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(0.1 * total_steps),  # 10% 预热 / 10% warmup
    num_training_steps=total_steps
)

# ============================================================
# 5. 训练循环 / Training Loop
# ============================================================
model.train()
for epoch in range(epochs):
    total_loss = 0
    for batch in dataloader:
        # 解包批次数据 / Unpack batch data
        input_ids, attention_mask, batch_labels = [b.to(device) for b in batch]

        # 前向传播 / Forward pass
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=batch_labels       # 传入标签会自动计算损失 / Passing labels auto-computes loss
        )
        loss = outputs.loss           # 交叉熵损失 / Cross-entropy loss

        # 反向传播 / Backward pass
        loss.backward()

        # 梯度裁剪 (防止梯度爆炸) / Gradient clipping (prevent exploding gradients)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        # 参数更新 / Parameter update
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

# ============================================================
# 6. 推理 / Inference
# ============================================================
model.eval()
test_text = "This is an amazing product!"
test_encoding = tokenizer(
    test_text,
    padding=True,
    truncation=True,
    max_length=128,
    return_tensors="pt"
).to(device)

with torch.no_grad():  # 推理不需要梯度 / No gradients needed for inference
    outputs = model(**test_encoding)
    logits = outputs.logits                       # 原始分数 / Raw scores
    prediction = torch.argmax(logits, dim=-1)     # 取最大值的索引 / Index of max value
    probabilities = torch.softmax(logits, dim=-1) # 概率分布 / Probability distribution

print(f"Prediction: {'Positive' if prediction.item() == 1 else 'Negative'}")
print(f"Confidence: {probabilities.max().item():.4f}")
```

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §A.3 "Fine-tuning Procedure"
> 📖 Docs: [HuggingFace Fine-Tuning](https://huggingface.co/docs/transformers/training)

### 示例 2: BERT 用于命名实体识别 (NER)

```python
# ============================================================
# 1. NER 推理 (使用预训练 NER 管道) / NER Inference (pre-trained pipeline)
# ============================================================
from transformers import pipeline

# 加载 NER 管道 / Load NER pipeline
ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",     # 专门做 NER 的 BERT / BERT fine-tuned for NER
    aggregation_strategy="simple"     # 合并子词 token / Merge subword tokens
)

# 做推理 / Run inference
text = "Hugging Face is based in New York City and was founded by Clément Delangue."
entities = ner(text)

for entity in entities:
    print(f"{entity['word']:20s} | {entity['entity_group']:5s} | score: {entity['score']:.4f}")
# Hugging Face          | ORG   | score: 0.9987
# New York City         | LOC   | score: 0.9992
# Clément Delangue      | PER   | score: 0.9856

# ============================================================
# 2. NER 微调 (使用 BertForTokenClassification) / NER Fine-Tuning
# ============================================================
from transformers import BertForTokenClassification

# NER 标签集 / NER label set
label_list = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC"]

# 加载带 Token 分类头的 BERT / Load BERT with token classification head
model = BertForTokenClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(label_list)  # 每个 token 分 9 类 / 9 classes per token
)
# 微调流程与示例 1 类似 / Fine-tuning procedure similar to Example 1
# 注意：NER 的标签是 per-token 的 / Note: NER labels are per-token
```

> 📖 Docs: [HuggingFace NER Pipeline](https://huggingface.co/docs/transformers/task_summary#named-entity-recognition)

### 示例 3: BERT 特征提取（获取上下文嵌入）

```python
# ============================================================
# 获取 BERT 隐藏状态 / Get BERT Hidden States
# ============================================================
from transformers import BertModel, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()

# 编码文本 / Encode text
text = "The bank by the river is beautiful."
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# 最后一层隐藏状态 / Last layer hidden states
last_hidden = outputs.last_hidden_state  # [1, seq_len, 768]
print(f"Shape: {last_hidden.shape}")     # torch.Size([1, 9, 768])

# [CLS] 向量 = 整句表示 / [CLS] vector = sentence representation
cls_embedding = last_hidden[:, 0, :]     # [1, 768]
print(f"[CLS] embedding shape: {cls_embedding.shape}")

# 所有层隐藏状态 / All layer hidden states
outputs_all = model(**inputs, output_hidden_states=True)
all_layers = outputs_all.hidden_states   # 13 个张量 (embedding + 12 层) / 13 tensors
print(f"Number of layers: {len(all_layers)}")  # 13

# 拼接最后 4 层 (Devlin 推荐的特征提取方式)
# Concatenate last 4 layers (Devlin's recommended feature extraction)
last_4 = torch.cat(all_layers[-4:], dim=-1)  # [1, seq_len, 768*4]
print(f"Last 4 layers concatenated: {last_4.shape}")  # [1, 9, 3072]
```

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §5.3 "Feature-based Approach"

---

## API 速查

### Tokenizer

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `BertTokenizer.from_pretrained()` | `pretrained_model_name` | — | 加载分词器 / Load tokenizer |
| `tokenizer()` | `text` | — | 编码文本 / Encode text |
| ↳ `padding` | `bool/str` | `False` | 填充策略 / Padding strategy |
| ↳ `truncation` | `bool` | `False` | 是否截断 / Whether to truncate |
| ↳ `max_length` | `int` | `512` | 最大长度 / Max length |
| ↳ `return_tensors` | `str` | `None` | `"pt"` (PyTorch) 或 `"tf"` (TensorFlow) |
| `tokenizer.decode()` | `token_ids` | — | 解码 token ID 为文本 / Decode token IDs |
| `tokenizer.convert_tokens_to_ids()` | `tokens` | — | token 转 ID / Convert tokens to IDs |

### Model

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `BertModel.from_pretrained()` | `pretrained_model_name` | — | 基础模型 (无分类头) / Base model |
| `BertForSequenceClassification` | `num_labels` | `2` | 文本分类 / Text classification |
| `BertForTokenClassification` | `num_labels` | — | 序列标注 (NER) / Token classification |
| `BertForQuestionAnswering` | — | — | 抽取式 QA / Extractive QA |
| `BertForMaskedLM` | — | — | MLM 预测 / Masked LM prediction |
| `model()` 输出 | `.last_hidden_state` | — | 最后一层 [batch, seq, hidden] |
| ↳ | `.pooler_output` | — | [CLS] 经过线性+tanh [batch, hidden] |
| ↳ | `.loss` | — | 传了 labels 时自动计算 / Auto-computed with labels |
| ↳ | `.logits` | — | 分类 logits [batch, num_labels] |

### 微调超参推荐 (Devlin et al., 2019, §A.3)

| 超参 | 推荐值 | 说明 |
|------|--------|------|
| 学习率 | 2e-5, 3e-5, 5e-5 | 三个值中选验证集最好的 / Grid search |
| Batch Size | 16, 32 | 显存允许则用 32 |
| Epochs | 2, 3, 4 | 小数据集用 4，大数据集用 2 |
| Warmup | 10% of steps | 学习率线性预热 |
| Weight Decay | 0.01 | AdamW 的权重衰减 |
| Max Seq Length | 128 或 512 | 按任务需求选择 |

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §A.3

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 微调脚本 / Fine-tuning script
├── predict.py            ← 推理脚本 / Inference script
└── data/
    ├── train.csv         ← 训练数据 / Training data
    └── test.csv          ← 测试数据 / Test data
```

### 标准结构

```
project/
├── config.py             ← 超参配置 / Hyperparameter config
├── dataset.py            ← 数据加载 / Dataset loading
├── model.py              ← 模型定义 (BERT + 分类头) / Model definition
├── train.py              ← 训练循环 / Training loop
├── evaluate.py           ← 评估脚本 / Evaluation script
├── predict.py            ← 推理脚本 / Inference script
├── utils.py              ← 工具函数 / Utility functions
├── data/
│   ├── raw/              ← 原始数据 / Raw data
│   └── processed/        ← 预处理后 / Preprocessed data
├── checkpoints/          ← 模型保存 / Model checkpoints
├── logs/                 ← 训练日志 / Training logs
└── requirements.txt      ← 依赖包 / Dependencies
```
