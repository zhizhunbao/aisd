---
topic: gpt
dimension: pitfalls
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Brown et al., 'Language Models are Few-Shot Learners', NeurIPS 2020 — https://arxiv.org/abs/2005.14165"
  - "📖 Paper: Holtzman et al., 'The Curious Case of Neural Text Degeneration', ICLR 2020 — https://arxiv.org/abs/1904.09751"
  - "📖 Docs: HuggingFace Text Generation — https://huggingface.co/docs/transformers/main_classes/text_generation"
  - "🧪 经验: GPT 系列模型文本生成实践"
expiry: 6m
status: current
---

# GPT 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 生成文本不断重复

**痛点类别：** 代码跑不通 / 结果不对

**场景：** 使用 GPT-2 生成文本时，输出不断重复同一个短语或句子，如 "The the the the..." 或一整段话被反复输出。

**症状：** 生成结果看起来"卡住了"——同样的内容循环出现，尤其是在贪心解码 (Greedy) 或低温度设置下。

**根因：** 贪心解码每步总是选概率最高的词，容易陷入局部循环。自回归模型把已生成的文本作为输入，如果某个 n-gram 的概率很高，模型就会一直选择它。这在学术上叫"neural text degeneration"。

**解法：**

❌ 错误做法 — 使用贪心解码且无重复惩罚

```python
# 贪心解码: 每步选概率最高的词 → 容易重复
output = model.generate(
    input_ids,
    max_new_tokens=100,
    do_sample=False,         # 贪心! / Greedy!
)
```

✅ 正确做法 — 使用采样 + 重复惩罚

```python
# Top-p 采样 + 重复惩罚 → 多样且不重复
output = model.generate(
    input_ids,
    max_new_tokens=100,
    do_sample=True,           # 启用采样 / Enable sampling
    temperature=0.8,          # 适中温度 / Moderate temperature
    top_p=0.92,               # 核采样 / Nucleus sampling
    repetition_penalty=1.2,   # 惩罚已出现的词 / Penalize seen tokens
    no_repeat_ngram_size=3,   # 禁止 3-gram 重复 / Block 3-gram repeats
)
```

**教训：** 默认的贪心解码几乎不应该用于开放式生成。使用 `do_sample=True` + `top_p` + `repetition_penalty` 是标准组合。

> 📖 Paper: Holtzman et al., [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751), ICLR 2020

---

## 坑 2: 温度设置不当导致胡说八道

**痛点类别：** 概念理解偏差

**场景：** 学生设置 `temperature=2.0` 或更高，期望"更有创意"的输出，结果得到了完全不可读的乱码。

**症状：** 输出看起来像随机拼凑的词，没有语法结构，不知所云。

**根因：** 温度过高时，softmax 分布变得极度平坦，所有词的概率接近均匀分布，等于随机选词。温度过低时，输出又过于死板重复。

**解法：**

❌ 错误做法 — 温度过高

```python
output = model.generate(
    input_ids,
    do_sample=True,
    temperature=2.0,    # 太高! 接近随机 / Too high! Nearly random
    max_new_tokens=50,
)
```

✅ 正确做法 — 适中温度范围

```python
# 推荐温度范围: 0.6~1.0 / Recommended range: 0.6-1.0
output = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.7,    # 略保守, 质量高 / Slightly conservative, high quality
    top_p=0.9,          # 配合 top_p 使用 / Combine with top_p
    max_new_tokens=50,
)
```

**教训：** 温度不是"创造力旋钮"那么简单。实践中 0.7~0.9 是最佳区间。超过 1.2 通常质量就开始下降了。

> 📖 Docs: [HuggingFace Generation Config](https://huggingface.co/docs/transformers/main_classes/text_generation)

---

## 坑 3: GPT-2 没有 pad_token 导致批量推理报错

**痛点类别：** 代码跑不通

**场景：** 对多个不同长度的 prompt 做批量生成时，需要 padding 到统一长度。但 GPT-2 分词器没有定义 `pad_token`，直接调用会报错。

**症状：** `ValueError: Cannot handle this padding strategy` 或 `Setting pad_token_id to eos_token_id` 警告后结果异常。

**根因：** GPT-2 的原始设计只处理单个序列（自回归逐词生成），不需要 padding。但批量推理需要统一长度。

**解法：**

❌ 错误做法 — 不设置 pad_token

```python
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# 直接编码多个文本 → 报错
inputs = tokenizer(["Hello", "The quick brown fox"], padding=True, return_tensors="pt")
```

✅ 正确做法 — 设置 pad_token 并注意 attention_mask

```python
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token   # 用 EOS 当 PAD / Use EOS as PAD
model.config.pad_token_id = tokenizer.pad_token_id

# padding_side="left" 对生成更友好 / Left padding is better for generation
tokenizer.padding_side = "left"

inputs = tokenizer(
    ["Hello", "The quick brown fox"],
    padding=True,
    return_tensors="pt"
)

output = model.generate(
    **inputs,
    max_new_tokens=30,
    attention_mask=inputs["attention_mask"],  # 关键: 传入 attention_mask / Critical!
)
```

**教训：** GPT-2 批量推理必须：(1) 设置 `pad_token`，(2) 使用左侧 padding (`padding_side="left"`)，(3) 传入 `attention_mask`。

> 📖 Docs: [HuggingFace GPT-2](https://huggingface.co/docs/transformers/model_doc/gpt2)

---

## 坑 4: 混淆 max_length 和 max_new_tokens

**痛点类别：** 概念理解偏差

**场景：** 学生设置 `max_length=50` 期望生成 50 个词，但 prompt 本身就有 40 个 token，结果只生成了 10 个新 token。

**症状：** 生成的文本比预期短得多，或者设置了 `max_length` 和 `max_new_tokens` 两个参数导致警告。

**根因：** `max_length` 是包括 prompt 在内的**总长度**；`max_new_tokens` 才是**新生成**的 token 数量。两个参数不能同时设置。

**解法：**

❌ 错误做法 — 混用两个参数

```python
output = model.generate(
    input_ids,              # prompt 长度: 40 tokens
    max_length=50,          # 总长度 50 → 只能新生成 10 个词!
    max_new_tokens=50,      # 冲突! 会报警告 / Conflict! Will warn
)
```

✅ 正确做法 — 用 max_new_tokens

```python
output = model.generate(
    input_ids,              # prompt 长度: 40 tokens
    max_new_tokens=100,     # 新生成 100 个 token (总共 140)
    do_sample=True,
    temperature=0.7,
)
```

**教训：** 永远用 `max_new_tokens` 而不是 `max_length`。

> 📖 Docs: [HuggingFace Text Generation](https://huggingface.co/docs/transformers/main_classes/text_generation)

---

## 坑 5: 微调 GPT 时学习率过高导致灾难性遗忘

**痛点类别：** 概念理解偏差 / 结果不对

**场景：** 在自定义数据集上微调 GPT-2 时使用了 `lr=1e-3`（常见的 CNN 学习率），结果模型丧失了预训练学到的语言能力。

**症状：** 微调后模型在自定义数据上 loss 很低，但在通用文本上生成完全不通顺的内容——预训练知识被"洗掉了"。

**根因：** 预训练模型的权重已经在很好的位置了，学习率太大会把权重"冲离"这个好位置。这就是灾难性遗忘 (Catastrophic Forgetting)。

**解法：**

❌ 错误做法 — 学习率太高

```python
optimizer = AdamW(model.parameters(), lr=1e-3)  # 太高! / Too high!
```

✅ 正确做法 — 使用小学习率 + 学习率预热

```python
from transformers import get_linear_schedule_with_warmup

optimizer = AdamW(model.parameters(), lr=5e-5)  # GPT 微调推荐: 2e-5 ~ 5e-5

# 学习率预热: 前 10% 步骤线性增加 / Warmup: linear increase for first 10% steps
total_steps = len(dataloader) * num_epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(0.1 * total_steps),
    num_training_steps=total_steps,
)
```

**教训：** GPT 微调学习率不能超过 `5e-5`。永远使用 warmup scheduler。考虑只微调最后几层或使用 LoRA。

> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §4 "Experiments"

---

## 坑 6: 不理解 In-Context Learning 和微调的区别

**痛点类别：** 概念理解偏差

**场景：** 学生认为 GPT-3 的 Few-Shot Learning 是在"训练"模型，以后再问它还能记住。实际上 In-Context Learning 不更新参数，每次推理都是从头开始。

**症状：** 在一次对话中用 Few-Shot 教会模型一个任务后，新对话中模型完全"忘记"了——因为它从来没"学会"过。

**根因：** In-Context Learning 发生在前向传播中，通过注意力机制在当前 prompt 的示例上"即时推理"，不修改任何权重。这和微调（更新梯度修改权重）是完全不同的机制。

**解法：**

| 方法 | 是否更新权重 | 持久性 | 适用场景 |
|------|-------------|--------|---------|
| In-Context Learning | ❌ 不更新 | 仅当前推理有效 | 快速原型、灵活多任务 |
| Fine-Tuning | ✅ 更新 | 永久保存 | 需要稳定高性能的场景 |
| LoRA / Adapter | ✅ 更新（少量参数）| 永久保存 | 资源有限时的微调 |

**教训：** In-Context Learning 是"临时抱佛脚"（推理时看示例），Fine-Tuning 是"真正学习"（更新权重）。前者灵活但不持久，后者持久但需要数据和计算。

> 📖 Paper: Brown et al., [GPT-3](https://arxiv.org/abs/2005.14165), §2 "Approach"

---

## 超级避坑指南

### 学习避坑

1. [ ] **先分清三代 GPT** → GPT-1 (微调), GPT-2 (零样本), GPT-3 (上下文学习)——三者范式完全不同
2. [ ] **别把 GPT 当搜索引擎** → 它生成"看起来对"的文本，不保证事实正确
3. [ ] **理解生成 vs 理解** → GPT 擅长生成，BERT 擅长理解——用错场景浪费时间
4. [ ] **别被参数量吓住** → 理解 GPT-2 (1.5B) 的原理和 GPT-3 (175B) 是一样的
5. [ ] **先跑 GPT-2 再聊 GPT-4** → GPT-2 是开源的、可以本地跑的最佳学习工具

### 作业/项目避坑

1. [ ] **先确认用什么 API** → HuggingFace (本地) vs OpenAI API (云端)——不要混淆
2. [ ] **生成参数先从默认开始调** → `temperature=0.7, top_p=0.9` 是安全起点
3. [ ] **记录 token 消耗** → OpenAI API 按 token 计费，跑循环生成前先估算成本
4. [ ] **保存生成结果** → 生成有随机性，不保存就无法复现

### 调试清单（技术类）

1. [ ] **生成重复？** → 加 `repetition_penalty=1.2` + `no_repeat_ngram_size=3`
2. [ ] **生成乱码？** → 降低温度到 0.7，加 `top_p=0.9`
3. [ ] **生成太短？** → 检查 `max_new_tokens` 而非 `max_length`
4. [ ] **批量推理报错？** → 设置 `pad_token` + `padding_side="left"` + `attention_mask`
5. [ ] **微调后模型变差？** → 学习率降到 `2e-5~5e-5`，加 warmup
6. [ ] **CUDA OOM？** → 用更小的模型 (`gpt2` 而非 `gpt2-xl`)、减小 batch size、用 `torch.float16`
