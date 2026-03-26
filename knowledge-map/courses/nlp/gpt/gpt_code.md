---
topic: gpt
dimension: code
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Docs: HuggingFace GPT-2 — https://huggingface.co/docs/transformers/model_doc/gpt2"
  - "📖 Docs: HuggingFace Text Generation — https://huggingface.co/docs/transformers/main_classes/text_generation"
  - "📖 Docs: OpenAI API — https://platform.openai.com/docs/api-reference"
expiry: 6m
status: current
---

# GPT 代码参考

> 📖 Docs: [HuggingFace GPT-2](https://huggingface.co/docs/transformers/model_doc/gpt2)
> 📖 Docs: [HuggingFace Text Generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

## 快速开始

### 最简示例 — 30 秒上手 GPT-2 文本生成

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# ============================================================
# 加载预训练模型和分词器 / Load pre-trained model and tokenizer
# ============================================================
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# ============================================================
# 编码输入文本 / Encode input text
# ============================================================
prompt = "Once upon a time"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# ============================================================
# 生成文本 / Generate text
# ============================================================
output = model.generate(
    input_ids,
    max_new_tokens=50,     # 最多生成 50 个新 token / Max new tokens
    temperature=0.7,       # 温度: 越低越保守 / Temperature: lower = more conservative
    top_p=0.9,             # 核采样阈值 / Nucleus sampling threshold
    do_sample=True,        # 启用采样 / Enable sampling (vs greedy)
)

# ============================================================
# 解码并输出 / Decode and print
# ============================================================
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
```

**测试方法：** `pip install transformers torch` → 运行上述代码 → 应该看到 "Once upon a time" 的续写

---

## 完整实现示例

### 示例 1: GPT-2 文本生成 — 多种解码策略对比

```python
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# ============================================================
# 1. 加载模型 / Load Model
# ============================================================
model_name = "gpt2"  # 可选: gpt2, gpt2-medium, gpt2-large, gpt2-xl
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()  # 推理模式 / Inference mode

# ============================================================
# 2. 编码输入 / Encode Input
# ============================================================
prompt = "Artificial intelligence will"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

# ============================================================
# 3. 贪心解码 / Greedy Decoding
# ============================================================
greedy_output = model.generate(
    input_ids,
    max_new_tokens=50,
    do_sample=False,       # 贪心: 每步选概率最高的词 / Greedy: pick highest prob
)
print("=== Greedy ===")
print(tokenizer.decode(greedy_output[0], skip_special_tokens=True))

# ============================================================
# 4. Beam Search 解码 / Beam Search Decoding
# ============================================================
beam_output = model.generate(
    input_ids,
    max_new_tokens=50,
    num_beams=5,           # 5 条搜索路径 / 5 search beams
    no_repeat_ngram_size=2, # 禁止 bigram 重复 / Prevent bigram repetition
    early_stopping=True,
)
print("\n=== Beam Search ===")
print(tokenizer.decode(beam_output[0], skip_special_tokens=True))

# ============================================================
# 5. Top-k + Top-p 采样 / Top-k + Top-p Sampling
# ============================================================
sample_output = model.generate(
    input_ids,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.8,       # 略低温度 / Slightly lower temperature
    top_k=50,              # 只考虑前 50 个词 / Consider top 50 tokens
    top_p=0.92,            # 核采样阈值 / Nucleus sampling threshold
)
print("\n=== Top-k + Top-p Sampling ===")
print(tokenizer.decode(sample_output[0], skip_special_tokens=True))

# ============================================================
# 6. 多个候选生成 / Multiple Candidates
# ============================================================
multi_output = model.generate(
    input_ids,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.9,
    top_p=0.95,
    num_return_sequences=3, # 生成 3 个不同的续写 / Generate 3 candidates
)
print("\n=== Multiple Candidates ===")
for i, output in enumerate(multi_output):
    print(f"\n--- Candidate {i+1} ---")
    print(tokenizer.decode(output, skip_special_tokens=True))
```

### 示例 2: GPT-2 微调 — 在自定义数据上训练

```python
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AdamW

# ============================================================
# 1. 自定义数据集 / Custom Dataset
# ============================================================
class TextDataset(Dataset):
    """
    简单的文本数据集 / Simple text dataset
    每个样本是一段文本，模型学习预测下一个词 / Each sample is text, model learns next-word prediction
    """
    def __init__(self, texts, tokenizer, max_length=128):
        self.encodings = []
        for text in texts:
            enc = tokenizer.encode(
                text,
                max_length=max_length,      # 截断到最大长度 / Truncate to max length
                truncation=True,
                padding="max_length",       # 填充到统一长度 / Pad to uniform length
                return_tensors="pt"
            )
            self.encodings.append(enc.squeeze())

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        input_ids = self.encodings[idx]
        # 自回归: labels = input_ids (偏移一位在模型内部处理)
        # Autoregressive: labels = input_ids (shift handled inside model)
        return {"input_ids": input_ids, "labels": input_ids}

# ============================================================
# 2. 准备模型和数据 / Prepare Model and Data
# ============================================================
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # GPT-2 没有 pad token / GPT-2 has no pad token

model = GPT2LMHeadModel.from_pretrained("gpt2")

# 示例训练数据 / Example training data
train_texts = [
    "Machine learning is a subset of artificial intelligence.",
    "Deep learning uses neural networks with many layers.",
    "Natural language processing enables computers to understand text.",
    # ... 实际使用时需要更多数据 / Need more data in practice
]

dataset = TextDataset(train_texts, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

# ============================================================
# 3. 训练循环 / Training Loop
# ============================================================
optimizer = AdamW(model.parameters(), lr=5e-5)  # 学习率要小 / Small learning rate
model.train()

for epoch in range(3):
    total_loss = 0
    for batch in dataloader:
        optimizer.zero_grad()

        outputs = model(
            input_ids=batch["input_ids"],
            labels=batch["labels"],       # 传入 labels 自动计算 CLM loss
        )

        loss = outputs.loss               # 自回归交叉熵损失 / Autoregressive CE loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss / len(dataloader):.4f}")

# ============================================================
# 4. 生成测试 / Generation Test
# ============================================================
model.eval()
prompt = "Machine learning"
input_ids = tokenizer.encode(prompt, return_tensors="pt")
output = model.generate(input_ids, max_new_tokens=30, do_sample=True, temperature=0.7)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

---

## API 速查

### HuggingFace GPT-2 模型

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `GPT2LMHeadModel.from_pretrained()` | `model_name` | — | 加载预训练模型 |
| ↳ | `"gpt2"` | — | 124M 参数, 12 层 |
| ↳ | `"gpt2-medium"` | — | 355M 参数, 24 层 |
| ↳ | `"gpt2-large"` | — | 774M 参数, 36 层 |
| ↳ | `"gpt2-xl"` | — | 1.5B 参数, 48 层 |
| `GPT2Tokenizer.from_pretrained()` | `model_name` | — | 加载 BPE 分词器 |

### 生成配置 (GenerationConfig)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_new_tokens` | `None` | 最多生成的新 token 数 |
| `max_length` | `20` | 生成序列的最大总长度 (含 prompt) |
| `do_sample` | `False` | `True`=采样, `False`=贪心/Beam |
| `temperature` | `1.0` | 温度: `<1` 保守, `>1` 创意 |
| `top_k` | `50` | Top-k 采样: 只从前 k 个词中选 |
| `top_p` | `1.0` | Top-p (核采样): 累积概率阈值 |
| `num_beams` | `1` | Beam Search 路径数 (`1`=无 Beam) |
| `no_repeat_ngram_size` | `0` | 禁止重复 n-gram (防止生成重复) |
| `repetition_penalty` | `1.0` | 重复惩罚: `>1` 降低重复概率 |
| `num_return_sequences` | `1` | 返回多少个不同的生成结果 |
| `pad_token_id` | `None` | 通常设为 `tokenizer.eos_token_id` |
| `eos_token_id` | `50256` | 遇到此 token 停止生成 |
| `use_cache` | `True` | 启用 KV Cache 加速推理 |

### 模型前向传播

| 参数 | 说明 |
|------|------|
| `input_ids` | 输入 token ID 张量, shape `(batch, seq_len)` |
| `attention_mask` | 注意力掩码 (1=关注, 0=忽略) |
| `labels` | 训练标签 (传入则自动计算 CLM loss) |
| `past_key_values` | KV Cache (推理时传入加速) |
| `use_cache` | 是否返回 KV Cache |

---

## 目录结构模板

### 简单结构

```
project/
├── generate.py           ← 文本生成脚本 / Generation script
├── requirements.txt      ← transformers, torch
└── prompts/
    └── examples.txt      ← 示例提示词 / Example prompts
```

### 标准结构

```
project/
├── config.py             ← 模型和生成参数 / Model & generation config
├── dataset.py            ← 自定义数据集 / Custom dataset
├── train.py              ← 微调训练脚本 / Fine-tuning script
├── generate.py           ← 推理生成脚本 / Inference script
├── evaluate.py           ← PPL 评估脚本 / Perplexity evaluation
├── utils.py              ← 工具函数 / Utility functions
├── data/
│   ├── train.txt         ← 训练文本 / Training text
│   └── eval.txt          ← 评估文本 / Evaluation text
├── checkpoints/          ← 模型存档 / Model checkpoints
└── outputs/              ← 生成结果 / Generated outputs
```
