---
topic: hugging_face
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: Hugging Face Transformers Documentation — https://huggingface.co/docs/transformers"
  - "📖 Docs: Hugging Face Datasets Documentation — https://huggingface.co/docs/datasets"
  - "📖 Docs: Hugging Face PEFT Documentation — https://huggingface.co/docs/peft"
  - "📖 Docs: Hugging Face Accelerate Documentation — https://huggingface.co/docs/accelerate"
  - "💻 Source: huggingface/transformers — https://github.com/huggingface/transformers"
expiry: 3m
status: current
---

# Hugging Face 代码参考

> 📖 Docs: [Hugging Face Transformers](https://huggingface.co/docs/transformers)


## 快速开始

### 最简示例 — 30 秒上手

```python
# ============================================================
# Hugging Face 最简推理示例 / Minimal Inference Example
# 一行代码完成情感分析 / One-line sentiment analysis
# ============================================================
from transformers import pipeline

# 创建情感分析 pipeline / Create sentiment analysis pipeline
# pipeline() 自动下载模型 + 分词器 + 后处理
# pipeline() auto-downloads model + tokenizer + post-processing
classifier = pipeline("sentiment-analysis")

# 推理 / Inference
result = classifier("I love using Hugging Face Transformers!")
print(result)
# 输出 / Output: [{'label': 'POSITIVE', 'score': 0.9998}]

# 批量推理 / Batch inference
results = classifier([
    "This is amazing!",
    "This is terrible.",
    "I'm not sure about this."
])
print(results)
# 输出 / Output: [{'label': 'POSITIVE', ...}, {'label': 'NEGATIVE', ...}, ...]
```

**测试方法：** 运行脚本，首次执行会自动下载默认模型（`distilbert-base-uncased-finetuned-sst-2-english`），确认输出包含 `label` 和 `score` 字段。

> 📖 Docs: [Quick Tour](https://huggingface.co/docs/transformers/quicktour)

---

## 完整实现示例

### 示例 1: Pipeline 多任务推理（开箱即用）

```python
# ============================================================
# 1. Pipeline 多任务推理 / Multi-Task Inference with Pipeline
# ============================================================
from transformers import pipeline

# --- 文本分类 / Text Classification ---
classifier = pipeline("sentiment-analysis")
print(classifier("Hugging Face is the best!"))
# [{'label': 'POSITIVE', 'score': 0.9998}]

# --- 文本生成 / Text Generation ---
generator = pipeline("text-generation", model="gpt2")
print(generator("Machine learning is", max_length=50, num_return_sequences=1))
# [{'generated_text': 'Machine learning is ...'}]

# --- 命名实体识别 / Named Entity Recognition ---
ner = pipeline("ner", grouped_entities=True)
print(ner("Hugging Face is based in New York City."))
# [{'entity_group': 'ORG', 'word': 'Hugging Face', ...}, ...]

# --- 问答 / Question Answering ---
qa = pipeline("question-answering")
result = qa(
    question="What is Hugging Face?",
    context="Hugging Face is a company that provides open-source NLP tools."
)
print(result)
# {'answer': 'a company that provides open-source NLP tools', 'score': 0.95, ...}

# --- 翻译 / Translation ---
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
print(translator("Hello, how are you?"))
# [{'translation_text': 'Bonjour, comment allez-vous ?'}]

# --- 零样本分类 / Zero-Shot Classification ---
zero_shot = pipeline("zero-shot-classification")
result = zero_shot(
    "I want to book a flight to Paris",
    candidate_labels=["travel", "food", "technology"]
)
print(result)
# {'labels': ['travel', 'food', 'technology'], 'scores': [0.98, ...]}

# --- 图像分类 / Image Classification ---
from PIL import Image
import requests

img_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/cats.png"
image = Image.open(requests.get(url, stream=True).raw)
print(img_classifier(image))
# [{'label': 'Egyptian cat', 'score': 0.95}, ...]
```

> 📖 Docs: [Pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines)
> 📖 Docs: [Task Summary](https://huggingface.co/docs/transformers/task_summary)

---

### 示例 2: AutoModel 手动推理（细粒度控制）

```python
# ============================================================
# 2. AutoModel 手动推理 / Manual Inference with AutoModel
# ============================================================
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ============================================================
# 2.1 加载模型和分词器 / Load Model & Tokenizer
# ============================================================
model_name = "bert-base-uncased"

# AutoTokenizer 自动选择 BertTokenizerFast
# AutoTokenizer auto-selects BertTokenizerFast
tokenizer = AutoTokenizer.from_pretrained(model_name)

# AutoModelForSequenceClassification 自动选择 BertForSequenceClassification
# 注意：这里用 ForSequenceClassification，不是 AutoModel
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2  # 二分类任务 / Binary classification
)
model.eval()  # 切换到推理模式 / Switch to eval mode

# ============================================================
# 2.2 分词 / Tokenization
# ============================================================
text = "I really enjoy learning about transformers!"

# 分词并转换为张量 / Tokenize and convert to tensors
inputs = tokenizer(
    text,
    return_tensors="pt",       # 返回 PyTorch 张量 / Return PyTorch tensors
    padding=True,              # 填充到最大长度 / Pad to max length
    truncation=True,           # 截断过长文本 / Truncate long texts
    max_length=512             # 最大序列长度 / Max sequence length
)
print(f"Input IDs shape: {inputs['input_ids'].shape}")
# Input IDs shape: torch.Size([1, 10])

# ============================================================
# 2.3 推理 / Inference
# ============================================================
with torch.no_grad():  # 关闭梯度计算 / Disable gradient computation
    outputs = model(**inputs)

# outputs.logits 是原始分数 / outputs.logits are raw scores
logits = outputs.logits
print(f"Logits: {logits}")

# 转换为概率 / Convert to probabilities
probabilities = torch.softmax(logits, dim=-1)
predicted_class = torch.argmax(probabilities, dim=-1).item()
print(f"Predicted class: {predicted_class}")
print(f"Probabilities: {probabilities}")

# ============================================================
# 2.4 GPU 推理 / GPU Inference
# ============================================================
if torch.cuda.is_available():
    device = torch.device("cuda")
    model = model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
    print(f"GPU Logits: {outputs.logits}")
```

> 📖 Docs: [AutoClass](https://huggingface.co/docs/transformers/model_doc/auto)
> 📖 Docs: [Tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer)

---

### 示例 3: Trainer 微调（标准训练流程）

```python
# ============================================================
# 3. Trainer 微调 / Fine-tuning with Trainer
# ============================================================
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

# ============================================================
# 3.1 数据准备 / Data Preparation
# ============================================================
# 加载 IMDB 影评数据集 / Load IMDB movie review dataset
dataset = load_dataset("imdb")
print(dataset)
# DatasetDict({
#     train: Dataset({features: ['text', 'label'], num_rows: 25000})
#     test:  Dataset({features: ['text', 'label'], num_rows: 25000})
# })

# 分词器 / Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(examples):
    """批量分词函数 / Batch tokenization function"""
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=256
    )

# 应用分词（使用 map 批量处理）/ Apply tokenization with map
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 取小子集用于演示 / Take small subset for demo
small_train = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval = tokenized_datasets["test"].shuffle(seed=42).select(range(200))

# ============================================================
# 3.2 模型定义 / Model Definition
# ============================================================
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2  # 正面/负面 / Positive/Negative
)

# ============================================================
# 3.3 训练配置 / Training Configuration
# ============================================================
training_args = TrainingArguments(
    output_dir="./results",              # 输出目录 / Output directory
    num_train_epochs=3,                  # 训练轮数 / Number of epochs
    per_device_train_batch_size=16,      # 训练 batch 大小 / Training batch size
    per_device_eval_batch_size=64,       # 评估 batch 大小 / Eval batch size
    warmup_steps=100,                    # 学习率预热步数 / Warmup steps
    weight_decay=0.01,                   # 权重衰减 / Weight decay
    logging_dir="./logs",                # 日志目录 / Logging directory
    logging_steps=50,                    # 每50步记录日志 / Log every 50 steps
    eval_strategy="epoch",              # 每 epoch 评估 / Evaluate each epoch
    save_strategy="epoch",              # 每 epoch 保存 / Save each epoch
    load_best_model_at_end=True,         # 训练结束加载最佳模型 / Load best at end
    fp16=True,                           # 混合精度训练 / Mixed precision (需GPU)
)

# ============================================================
# 3.4 评估指标 / Evaluation Metrics
# ============================================================
def compute_metrics(eval_pred):
    """计算准确率 / Compute accuracy"""
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = (predictions == labels).mean()
    return {"accuracy": accuracy}

# ============================================================
# 3.5 训练 / Training
# ============================================================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train,
    eval_dataset=small_eval,
    compute_metrics=compute_metrics,
)

# 启动训练 / Start training
trainer.train()

# 评估 / Evaluate
results = trainer.evaluate()
print(f"Accuracy: {results['eval_accuracy']:.4f}")

# 保存模型 / Save model
trainer.save_model("./fine-tuned-model")

# 推送到 Hub / Push to Hub (需要先 huggingface-cli login)
# trainer.push_to_hub("my-fine-tuned-model")
```

> 📖 Docs: [Fine-tune a pretrained model](https://huggingface.co/docs/transformers/training)
> 📖 Docs: [Trainer](https://huggingface.co/docs/transformers/main_classes/trainer)

---

### 示例 4: PEFT LoRA 高效微调（低显存场景）

```python
# ============================================================
# 4. PEFT LoRA 微调 / Parameter-Efficient Fine-tuning with LoRA
# ============================================================
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

# ============================================================
# 4.1 加载基座模型 / Load Base Model
# ============================================================
model_name = "facebook/opt-350m"  # 350M 参数的因果语言模型 / 350M param causal LM
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 查看原始参数量 / Check original parameter count
total_params = sum(p.numel() for p in model.parameters())
print(f"原始参数量 / Original params: {total_params:,}")

# ============================================================
# 4.2 配置 LoRA / Configure LoRA
# ============================================================
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,      # 任务类型 / Task type
    r=8,                                # LoRA 秩 / LoRA rank (低 = 更高效)
    lora_alpha=32,                      # 缩放因子 / Scaling factor
    lora_dropout=0.1,                   # Dropout 率 / Dropout rate
    target_modules=["q_proj", "v_proj"] # 目标模块 / Target modules (注意力层)
)

# 包装模型 / Wrap model with LoRA
model = get_peft_model(model, lora_config)

# 查看可训练参数量 / Check trainable parameter count
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"可训练参数量 / Trainable params: {trainable_params:,}")
print(f"可训练比例 / Trainable ratio: {trainable_params/total_params:.4%}")
# 通常只有 0.1%~1% 的参数需要训练 / Usually only 0.1%~1% params are trainable

# ============================================================
# 4.3 训练 / Training (同 Trainer 流程)
# ============================================================
# ... (同示例 3 的 Trainer 流程)

# ============================================================
# 4.4 保存和加载 LoRA 权重 / Save & Load LoRA Weights
# ============================================================
# 仅保存 LoRA 适配器（几 MB）/ Save only LoRA adapter (few MB)
model.save_pretrained("./lora-adapter")

# 加载时合并 LoRA 到基座模型 / Load and merge LoRA into base model
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(base_model, "./lora-adapter")
model = model.merge_and_unload()  # 合并权重 / Merge weights
```

> 📖 Docs: [PEFT](https://huggingface.co/docs/peft)
> 📖 Docs: [LoRA](https://huggingface.co/docs/peft/conceptual_guides/lora)

---

## API 速查

### 核心加载 API

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `AutoTokenizer.from_pretrained(name)` | `name` | — | 自动加载匹配的分词器 |
| ↳ `use_fast` | `bool` | `True` | 是否使用 Rust 快速分词器 |
| `AutoModel.from_pretrained(name)` | `name` | — | 加载基础模型（输出 hidden states）|
| ↳ `torch_dtype` | `dtype` | `float32` | 加载精度：`float16`/`bfloat16` |
| ↳ `device_map` | `str/dict` | `None` | 自动设备映射：`"auto"`/`"cuda:0"` |
| ↳ `load_in_8bit` | `bool` | `False` | 8-bit 量化加载（需 bitsandbytes）|
| ↳ `load_in_4bit` | `bool` | `False` | 4-bit 量化加载 |
| `AutoModelForSequenceClassification` | `num_labels` | `2` | 分类任务模型 |
| `AutoModelForCausalLM` | — | — | 因果语言模型（GPT 式）|
| `AutoModelForSeq2SeqLM` | — | — | 序列到序列模型（T5 式）|
| `AutoModelForTokenClassification` | `num_labels` | — | 序列标注模型（NER 等）|

### Pipeline API

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `pipeline(task)` | `task` | — | 任务名：见下表 |
| ↳ `model` | `str` | 任务默认 | 指定模型名或路径 |
| ↳ `device` | `int` | `-1` (CPU) | GPU 设备号：`0` 为第一块 GPU |
| ↳ `batch_size` | `int` | `1` | 批处理大小 |
| ↳ `torch_dtype` | `dtype` | `float32` | 推理精度 |

**支持的 task 列表：**

| task 名称 | 说明 | 默认模型 |
|-----------|------|---------|
| `"sentiment-analysis"` | 情感分类 | distilbert-sst-2 |
| `"text-generation"` | 文本生成 | gpt2 |
| `"text2text-generation"` | 文本到文本 | t5-base |
| `"ner"` | 命名实体识别 | dbmdz-bert-ner |
| `"question-answering"` | 抽取式问答 | distilbert-squad |
| `"summarization"` | 文本摘要 | bart-large-cnn |
| `"translation_xx_to_yy"` | 翻译 | opus-mt |
| `"fill-mask"` | 掩码预测 | bert-base |
| `"zero-shot-classification"` | 零样本分类 | bart-large-mnli |
| `"image-classification"` | 图像分类 | vit-base |
| `"automatic-speech-recognition"` | 语音识别 | whisper |

### Trainer API

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `TrainingArguments(output_dir)` | `output_dir` | — | 输出目录（必填）|
| ↳ `num_train_epochs` | `float` | `3.0` | 训练轮数 |
| ↳ `per_device_train_batch_size` | `int` | `8` | 每设备训练 batch |
| ↳ `learning_rate` | `float` | `5e-5` | 学习率 |
| ↳ `weight_decay` | `float` | `0` | 权重衰减 |
| ↳ `fp16` | `bool` | `False` | FP16 混合精度 |
| ↳ `bf16` | `bool` | `False` | BF16 混合精度 |
| ↳ `gradient_accumulation_steps` | `int` | `1` | 梯度累积步数 |
| ↳ `eval_strategy` | `str` | `"no"` | `"steps"`/`"epoch"` |
| ↳ `save_strategy` | `str` | `"steps"` | `"steps"`/`"epoch"` |
| ↳ `load_best_model_at_end` | `bool` | `False` | 训练结束加载最佳 |
| `Trainer(model, args, ...)` | `model` | — | 模型实例 |
| ↳ `train_dataset` | `Dataset` | — | 训练数据集 |
| ↳ `eval_dataset` | `Dataset` | `None` | 评估数据集 |
| ↳ `compute_metrics` | `callable` | `None` | 评估函数 |
| ↳ `data_collator` | `DataCollator` | 默认 | 数据整理器 |

### 常用工具

| 函数 | 说明 |
|------|------|
| `tokenizer(text, return_tensors="pt")` | 分词并转 PyTorch 张量 |
| `tokenizer.decode(ids)` | token ID 解码回文本 |
| `model.save_pretrained(path)` | 保存模型到本地 |
| `model.push_to_hub(repo_name)` | 推送模型到 Hub |
| `load_dataset(name)` | 加载 HF 数据集 |
| `model.generate(**inputs)` | 自回归文本生成 |
| `model.config` | 查看模型配置 |
| `model.num_parameters()` | 查看参数量 |

> 📖 Docs: [Transformers API Reference](https://huggingface.co/docs/transformers/main_classes/model)

---

## 目录结构模板

### 简单结构

```
project/
├── inference.py            ← 推理脚本（pipeline 快速推理）
├── requirements.txt        ← 依赖列表
└── README.md               ← 项目说明
```

### 标准结构

```
project/
├── train.py                ← 训练脚本（Trainer 微调）
├── inference.py            ← 推理脚本
├── config.yaml             ← 训练超参数配置
├── data/
│   ├── train.csv           ← 训练数据
│   └── test.csv            ← 测试数据
├── results/                ← 训练输出和检查点
├── logs/                   ← TensorBoard 日志
└── requirements.txt
```

### 高级结构

```
project/
├── configs/
│   ├── training_config.yaml      ← 训练超参数
│   └── model_config.yaml         ← 模型配置
├── src/
│   ├── data/
│   │   ├── dataset.py            ← 自定义数据集
│   │   └── preprocessing.py      ← 数据预处理
│   ├── models/
│   │   ├── model.py              ← 模型定义 / 自定义头
│   │   └── lora_config.py        ← LoRA 配置
│   ├── training/
│   │   ├── trainer.py            ← 自定义 Trainer
│   │   └── callbacks.py          ← 自定义回调
│   └── inference/
│       ├── predict.py            ← 推理脚本
│       └── serve.py              ← API 服务
├── scripts/
│   ├── train.sh                  ← 训练启动脚本
│   └── evaluate.sh               ← 评估脚本
├── tests/                        ← 单元测试
├── results/                      ← 训练输出
├── logs/                         ← 日志
└── requirements.txt
```

> 📖 Docs: [Examples](https://github.com/huggingface/transformers/tree/main/examples)
