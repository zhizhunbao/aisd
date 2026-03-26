---
topic: transformer
dimension: pitfalls
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
  - "🧪 经验: 基于 Transformer 实现和教学中的常见错误总结"
expiry: 6m
status: current
---

# Transformer 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: "Attention 到底在算什么？" —— 把注意力想成了固定的规则

**痛点类别：** 概念理解坑（痛点 5: 名词多黑话多）

**场景：** 第一次学 Self-Attention，以为注意力权重是人工设计的规则（比如"动词关注主语"）

**症状：** 看到注意力可视化图，发现权重分布和自己预期完全不同，觉得"模型学错了"

**根因：** 注意力权重是**学出来的**，不是规定的。Q/K/V 的投影矩阵 W^Q, W^K, W^V 在训练中学到什么模式，注意力就呈现什么模式。不同头学到的模式也不同——有的关注语法，有的关注位置，有的可能"没有明显模式"但对最终效果有贡献

**解法：**

❌ 错误做法 — 以为每个头都应该有可解释的语言学含义

```python
# 错误：期望 head_0 = 语法依赖，head_1 = 共指
# Wrong: expecting each head to have a clear linguistic role
for i, head in enumerate(attention_weights):
    assert has_linguistic_pattern(head), f"Head {i} 没有语言学模式！"
```

✅ 正确做法 — 理解注意力是端到端学出来的特征，不一定可解释

```python
# 正确：注意力权重是统计模式，可视化只是辅助理解
# Correct: attention weights are learned patterns, visualization is auxiliary
# 关注最终任务指标（BLEU/Accuracy），不要纠结单个头的"含义"
output = model(src, tgt)
bleu_score = compute_bleu(output, reference)
print(f"BLEU: {bleu_score}")  # 这才是唯一重要的
```

**教训：** 注意力权重是手段不是目的——别被可视化骗了，看最终效果。

> 📖 Paper: Jain & Wallace, [Attention is not Explanation](https://arxiv.org/abs/1902.10186), NAACL 2019

---

## 坑 2: 维度错乱 —— batch_first 搞混了输入形状

**痛点类别：** 代码实操坑（痛点 1: 只甩任务不教思路）

**场景：** 用 PyTorch 的 `nn.Transformer`，输入张量维度报错

**症状：** `RuntimeError: Expected src shape (seq, batch, dim) but got (batch, seq, dim)` 或者结果不对但不报错

**根因：** PyTorch 默认 `batch_first=False`，期望输入形状是 `(seq_len, batch_size, d_model)`。但大多数人习惯数据是 `(batch_size, seq_len, d_model)`。不匹配时有时报错、有时静默算出错误结果（更危险）

**解法：**

❌ 错误做法 — 使用默认参数但传入 batch_first 格式的数据

```python
model = nn.Transformer(d_model=512, nhead=8)  # 默认 batch_first=False
src = torch.rand(32, 10, 512)  # (batch, seq, dim) —— 错了！
output = model(src, tgt)  # 静默错误，维度恰好匹配但语义不对
```

✅ 正确做法 — 显式设置 batch_first=True

```python
model = nn.Transformer(d_model=512, nhead=8, batch_first=True)
src = torch.rand(32, 10, 512)  # (batch, seq, dim) —— 正确！
output = model(src, tgt)
```

**教训：** 永远显式设置 `batch_first=True`，别让默认参数坑你。

> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html) — `batch_first` parameter

---

## 坑 3: 掩码方向反了 —— 因果掩码和填充掩码搞混

**痛点类别：** 代码实操坑（痛点 1: 只甩任务不教思路）

**场景：** Decoder 生成时输出全是重复的同一个词，或者训练 loss 异常低但生成效果极差

**症状：** 训练时 loss 看起来正常，但推理时模型总是生成开头几个词的重复

**根因：** 忘了加因果掩码（Causal Mask），或者掩码方向反了。没有掩码，Decoder 在训练时可以"偷看"未来的词（看到正确答案），相当于开卷考试——loss 当然低，但推理时没有未来信息就崩了

**解法：**

❌ 错误做法 — Decoder 不加因果掩码

```python
# 错误：Decoder 可以看到未来的词——等于作弊
output = model(src, tgt)  # 没有传 tgt_mask
```

✅ 正确做法 — 传入因果掩码

```python
# 正确：生成下三角掩码，阻止 Decoder 看未来
tgt_mask = nn.Transformer.generate_square_subsequent_mask(tgt.size(1))
output = model(src, tgt, tgt_mask=tgt_mask)
```

**教训：** Decoder 必须有因果掩码，否则训练时作弊、推理时崩溃。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.1

---

## 坑 4: 位置编码加错了 —— 先嵌入后编码的顺序搞反

**痛点类别：** 概念理解坑（痛点 3: 知识碎片化）

**场景：** 手写 Transformer 时，位置编码和词嵌入的组合方式搞错了

**症状：** 模型能训练但效果比预期差很多，对词序敏感的任务（如翻译）性能下降

**根因：** 位置编码应该**加到**（+）词嵌入上，不是拼接（concat）。而且必须先 scale 词嵌入（乘以 √d_model），再加位置编码——否则位置编码的信号会被词嵌入淹没

**解法：**

❌ 错误做法 — 直接拼接或不缩放

```python
# 错误 1: 拼接而不是相加
x = torch.cat([token_embed, pos_encoding], dim=-1)  # 维度翻倍了！

# 错误 2: 不缩放词嵌入
x = token_embed + pos_encoding  # 位置信号太弱
```

✅ 正确做法 — 缩放词嵌入后相加

```python
# 正确：先缩放词嵌入，再加位置编码（原始论文做法）
x = token_embed * math.sqrt(d_model) + pos_encoding
```

**教训：** 位置编码是加法不是拼接，词嵌入要先乘 √d_model。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.4

---

## 坑 5: 学习率设置 —— 不用 Warmup 直接大学习率起步

**痛点类别：** 代码实操坑（痛点 4: 全靠AI生成，不懂为什么）

**场景：** 训练 Transformer，loss 一开始就 NaN 或者震荡不收敛

**症状：** 训练第一个 epoch loss 就爆炸（NaN），或者 loss 在高位剧烈震荡

**根因：** Transformer 训练初期，Layer Normalization 的参数还不稳定，如果学习率太大会导致梯度爆炸。原始论文用了 Warmup 策略——先用很小的学习率线性升到峰值（前 4000 步），然后逐步衰减

**解法：**

❌ 错误做法 — 固定大学习率

```python
# 错误：一上来就用大学习率
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

✅ 正确做法 — 使用 Warmup + Inverse Square Root Decay

```python
# 正确：原始论文的学习率策略
# lr = d_model^(-0.5) * min(step^(-0.5), step * warmup^(-1.5))
class TransformerScheduler:
    def __init__(self, optimizer, d_model=512, warmup_steps=4000):
        self.optimizer = optimizer
        self.d_model = d_model
        self.warmup_steps = warmup_steps
        self.step_num = 0
    
    def step(self):
        self.step_num += 1
        lr = (self.d_model ** -0.5) * min(
            self.step_num ** -0.5,
            self.step_num * self.warmup_steps ** -1.5
        )
        for p in self.optimizer.param_groups:
            p['lr'] = lr

optimizer = torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9)
scheduler = TransformerScheduler(optimizer, d_model=512, warmup_steps=4000)
```

**教训：** Transformer 训练必须 Warmup，这不是可选的，是必须的。

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §5.3

---

## 坑 6: 混淆 Encoder-Only / Decoder-Only / Full Transformer

**痛点类别：** 概念理解坑（痛点 5: 名词多黑话多）

**场景：** 被问"BERT 用的是什么架构？GPT 呢？"答不上来

**症状：** 知道 BERT 和 GPT 都"基于 Transformer"，但说不清具体用了 Transformer 的哪部分

**根因：** 原始 Transformer 是完整的 Encoder-Decoder 架构。后续工作只用了其中一半：BERT 只用 Encoder（双向注意力），GPT 只用 Decoder（因果注意力）。T5 / BART 才是完整的 Encoder-Decoder

**解法：**

❌ 错误做法 — "BERT 和 GPT 都是 Transformer"就完事了

```
学生: "BERT 和 GPT 有什么区别？"
回答: "都是 Transformer"  ← 没有区分关键差异
```

✅ 正确做法 — 区分架构变体

```
BERT  = Transformer Encoder  → 双向注意力 → 擅长理解
GPT   = Transformer Decoder  → 因果注意力 → 擅长生成
T5    = Transformer Enc-Dec  → 编码+解码  → 擅长翻译/摘要
原始   = Full Enc-Dec         → Vaswani 2017 的完整架构
```

**教训：** "基于 Transformer"不等于"用了完整 Transformer"——必须说清是 Encoder / Decoder / 还是两者都用。

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), §1
> 📖 Paper: Radford et al., [GPT-1](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf), §1

---

## 超级避坑指南

### 学习避坑

1. [ ] **别被 Q/K/V 吓住** → 就是"搜索词/标签/内容"的类比，本质是三个线性变换
2. [ ] **别死背公式** → 记住核心思想：算相关度（Q·K）→ 归一化（softmax）→ 加权求和（×V）
3. [ ] **别把注意力可视化当真理** → 注意力权重不等于"解释"，可解释性研究仍在争论
4. [ ] **别忽略位置编码** → Transformer 不加位置编码就是一个集合操作，不认识顺序
5. [ ] **先搞懂单头再看多头** → 多头就是"跑多次单头再拼接"，不要一上来就看多头

### 作业/项目避坑

1. [ ] **先用 `nn.Transformer` 跑通** → 别一上来就手写全部模块，先用 PyTorch 内置版确认管道正常
2. [ ] **设 `batch_first=True`** → 避免维度混淆
3. [ ] **Decoder 一定加因果掩码** → 忘了就等于训练时作弊
4. [ ] **词嵌入乘 √d_model** → 原始论文的做法，不是可选的
5. [ ] **检查 padding mask 和 causal mask 是否同时使用** → 两种掩码用途不同，可以叠加

### 考试/答辩避坑

1. [ ] **被问"Transformer 和 RNN 的区别"** → 三个词：并行、O(1)路径、注意力
2. [ ] **被问"为什么除以 √d_k"** → 点积方差 = d_k，缩放让 softmax 不饱和
3. [ ] **被问"多头的意义"** → 学不同类型的注意力模式，一个头不够

### 调试清单（技术类）

1. [ ] **loss 是 NaN？** → 检查学习率是否用了 warmup
2. [ ] **生成全是重复？** → 检查因果掩码是否正确设置
3. [ ] **效果差于预期？** → 检查位置编码是否正确添加（加法 + 缩放）
4. [ ] **内存爆了？** → 检查序列长度——O(n²) 内存，减小 seq_len 或用 gradient checkpointing
5. [ ] **训练正常推理崩了？** → 检查 Decoder 训练时是否用了 teacher forcing 但推理没切换到自回归模式
