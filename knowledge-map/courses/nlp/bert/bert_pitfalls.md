---
topic: bert
dimension: pitfalls
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019 — https://arxiv.org/abs/1810.04805"
  - "📖 Docs: Hugging Face Transformers — https://huggingface.co/docs/transformers/model_doc/bert"
  - "🧪 经验: 微调 BERT 的常见问题总结"
expiry: 6m
status: current
---

# BERT 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 学习率太高导致微调崩溃

**痛点类别：** 代码型——"跑起来了但效果很差，不知道为什么"

**场景：** 第一次微调 BERT，使用了常见的学习率（如 1e-3 或 1e-4）

**症状：** 训练 loss 不下降甚至上升、验证集准确率 ~50%（和随机猜一样）、训练过程震荡严重

**根因：** BERT 已经有了很好的预训练权重。学习率太大会破坏这些权重（"灾难性遗忘"），相当于把预训练学到的知识全部覆盖掉了。微调的本质是"微调"——轻微地调整已有权重。

**解法：**

❌ 错误做法 — 使用常规深度学习学习率

```python
# 1e-3 太大了，会毁掉预训练权重 / 1e-3 is too large, destroys pre-trained weights
optimizer = AdamW(model.parameters(), lr=1e-3)
```

✅ 正确做法 — 使用 BERT 推荐的学习率范围

```python
# 2e-5 到 5e-5 是 Devlin 等人推荐的范围 / 2e-5 to 5e-5 recommended by Devlin et al.
optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)

# 加上学习率预热 / Add learning rate warmup
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(0.1 * total_steps),  # 前 10% step 线性预热
    num_training_steps=total_steps
)
```

**教训：** 微调≠从零训练。学习率必须比普通训练小 100 倍以上（2e-5 vs 1e-3）。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §A.3 "Fine-tuning Procedure"

---

## 坑 2: 忘记加 attention_mask 导致效果差

**痛点类别：** 代码型——"代码没报错但结果不对"

**场景：** tokenizer 编码后只传了 `input_ids`，没传 `attention_mask`

**症状：** 模型可以训练，但效果明显低于预期。特别是在 batch 中序列长度差异大时更明显。

**根因：** batch 中短序列会被 padding 填充到最大长度。没有 `attention_mask`，模型会"关注"那些 padding token，把无意义的填充当作真实内容来处理。

**解法：**

❌ 错误做法 — 只传 input_ids

```python
# 忘记 attention_mask / Forgot attention_mask
outputs = model(input_ids=input_ids)
```

✅ 正确做法 — 同时传 attention_mask

```python
# attention_mask 告诉模型哪些是真实 token（1），哪些是 padding（0）
# attention_mask tells model which are real tokens (1) vs padding (0)
outputs = model(
    input_ids=input_ids,
    attention_mask=attention_mask  # 必须传！/ Must pass!
)
```

**教训：** tokenizer 返回的 `attention_mask` 不是装饰品，它告诉 attention 层哪些位置要忽略。

> 📖 Docs: [HuggingFace BERT](https://huggingface.co/docs/transformers/model_doc/bert), `attention_mask` 参数说明

---

## 坑 3: 长文本被截断丢失关键信息

**痛点类别：** 概念型——"不理解 max_length 的含义"

**场景：** 输入文本很长（如新闻文章、法律文档），但 BERT 最大只支持 512 tokens

**症状：** 分类效果不稳定；对长文本效果差；关键信息恰好在文末被截断

**根因：** BERT 位置嵌入只有 512 个，超过的 token 会被截断。如果关键信息在文末（如结论、判决结果），截断会直接丢失。

**解法：**

❌ 错误做法 — 简单截断，不考虑信息丢失

```python
# 默认截断前 512 个 token，尾部可能有关键信息 / Truncates first 512 tokens
tokenizer(long_text, max_length=512, truncation=True)
```

✅ 正确做法 — 滑动窗口或首尾拼接

```python
# 方法 1: 首尾拼接策略 / Head-tail concatenation strategy
tokens = tokenizer.tokenize(long_text)
head = tokens[:256]      # 取开头 256 个 / Take first 256
tail = tokens[-254:]     # 取结尾 254 个 / Take last 254
combined = ["[CLS]"] + head + ["[SEP]"] + tail + ["[SEP]"]  # 总共 ≤ 512

# 方法 2: 滑动窗口 + 投票 / Sliding window + voting
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
chunks = []
stride = 128  # 窗口重叠 / Window overlap
for i in range(0, len(tokens), 512 - stride):
    chunk = tokens[i:i + 510]  # 留出 [CLS] 和 [SEP] 的位置
    chunks.append(chunk)
# 对每个 chunk 分别推理，然后投票或平均 / Infer each chunk, then vote or average
```

**教训：** BERT 的 512 限制不是软限制，是硬限制（位置嵌入只有 512 个）。长文本必须有策略。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §3.2

---

## 坑 4: uncased/cased 模型选错

**痛点类别：** 概念型——"不知道 uncased 和 cased 的区别"

**场景：** 做 NER（命名实体识别）任务时使用了 `bert-base-uncased`

**症状：** NER 效果明显差于预期，特别是人名和地名容易被遗漏

**根因：** `uncased` 模型在预训练时把所有文本转成了小写。NER 任务中，大写是非常重要的特征——"Apple"（公司）vs "apple"（水果）。用 uncased 模型等于丢掉了这个关键信号。

**解法：**

❌ 错误做法 — NER 用 uncased 模型

```python
# uncased 会丢失大小写信息 / uncased loses case information
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=9)
```

✅ 正确做法 — NER 用 cased 模型

```python
# cased 保留大小写，对 NER 至关重要 / cased preserves case, crucial for NER
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
model = BertForTokenClassification.from_pretrained("bert-base-cased", num_labels=9)
```

**教训：** 分类任务用 uncased 通常够了（大小写不影响情感）；NER/信息抽取等需要大小写信号的任务必须用 cased。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §5.1

---

## 坑 5: 微调 epoch 数过多导致过拟合

**痛点类别：** 代码型——"训练集很好但测试集很差"

**场景：** 小数据集（几百条），微调了 10+ epoch

**症状：** 训练集准确率 99%+，验证集准确率从第 3 个 epoch 开始下降

**根因：** BERT 有 110M (Base) 或 340M (Large) 参数，能力极强。在小数据集上过多迭代会让模型"死记硬背"训练数据，丧失泛化能力。

**解法：**

❌ 错误做法 — 训练太多 epoch

```python
# 10 个 epoch 太多了 / 10 epochs is too many for fine-tuning
for epoch in range(10):
    train(model, dataloader)
```

✅ 正确做法 — 2-4 epoch + 早停

```python
# Devlin 推荐 2-4 epoch / Devlin recommends 2-4 epochs
best_val_acc = 0
patience = 2  # 容忍 2 个 epoch 不提升 / Tolerate 2 epochs without improvement

for epoch in range(4):
    train(model, train_loader)
    val_acc = evaluate(model, val_loader)

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "best_model.pt")
        wait = 0
    else:
        wait += 1
        if wait >= patience:
            print("Early stopping!")
            break
```

**教训：** BERT 微调不需要也不应该训练太多 epoch。预训练已经学到了大量知识，微调只需要"微调"。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §A.3

---

## 坑 6: 不理解 [CLS] 和 pooler_output 的区别

**痛点类别：** 概念型——"两个都叫句子表示，用哪个？"

**场景：** 想获取句子级别的表示用于下游任务

**症状：** 不确定用 `last_hidden_state[:, 0, :]` 还是 `pooler_output`

**根因：** 两者确实接近但不同：`last_hidden_state[:, 0, :]` 是 [CLS] token 的原始最终隐藏状态；`pooler_output` 是 [CLS] 经过一层 Linear + Tanh 后的输出（为 NSP 任务设计）。

**解法：**

```python
outputs = model(**inputs)

# 方法 1: 直接取 [CLS] 的隐藏状态 / Direct [CLS] hidden state
cls_raw = outputs.last_hidden_state[:, 0, :]  # [batch, 768]

# 方法 2: 使用 pooler_output / Use pooler_output
cls_pooled = outputs.pooler_output  # [batch, 768], 经过 Linear + Tanh

# 微调分类时通常用 pooler_output (HuggingFace 默认行为)
# For fine-tuning classification: typically use pooler_output (HF default)

# 特征提取 / 语义相似度时通常用 mean pooling / last_hidden_state
# For feature extraction / semantic similarity: typically use mean pooling
token_embeddings = outputs.last_hidden_state  # [batch, seq_len, 768]
attention_mask_expanded = attention_mask.unsqueeze(-1).float()
mean_pooled = (token_embeddings * attention_mask_expanded).sum(1) / attention_mask_expanded.sum(1)
```

**教训：** 没有绝对最好的选择——微调用 `pooler_output`，语义相似度用 mean pooling。

> 📖 Docs: [HuggingFace BertModel](https://huggingface.co/docs/transformers/model_doc/bert#transformers.BertModel)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别一上来就看代码** → 先理解 MLM 和 NSP 的直觉，再看实现
2. [ ] **别混淆 BERT 和 GPT** → 编码器/双向 vs 解码器/单向，适用任务完全不同
3. [ ] **别以为 BERT 能做所有 NLP 任务** → 生成任务需要 GPT / T5
4. [ ] **别跳过 WordPiece 分词** → 理解子词分词是理解 BERT 输入的关键

### 作业/项目避坑

1. [ ] **先确认任务类型** → 分类用 `BertForSequenceClassification`，NER 用 `BertForTokenClassification`
2. [ ] **先用小数据验证流程** → 确认管道跑通再用全量数据
3. [ ] **记录实验超参** → 学习率、batch size、epoch 数都要记
4. [ ] **保存最优模型** → 不是最后一个 epoch 的模型最好

### 考试/答辩避坑

1. [ ] **能一句话说清 MLM** → "随机遮住 15% 的词让模型猜，从而学到双向上下文"
2. [ ] **能说清 BERT vs GPT 的核心区别** → "BERT 双向理解型 vs GPT 单向生成型"
3. [ ] **能解释为什么预训练+微调有用** → "通用知识迁移，减少标注需求"

### 调试清单（技术类）

1. [ ] **训练 loss 不下降？** → 检查学习率是否太大（应该 2e-5~5e-5）
2. [ ] **验证集效果差？** → 检查是否过拟合（减少 epoch / 增加 dropout）
3. [ ] **内存溢出 (OOM)？** → 减小 batch_size 或 max_length；或用梯度累积
4. [ ] **推理结果全是同一个类？** → 检查数据是否类别不平衡；检查学习率
5. [ ] **分词后序列太长？** → 检查 truncation=True 和合理的 max_length
6. [ ] **NER 效果差？** → 检查是否用了 cased 模型
