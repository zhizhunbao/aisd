---
topic: transformer
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
  - "🧪 经验: Transformer 实现与训练常见问题"
expiry: 6m
status: current
---

# Transformer 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 忘记缩放因子 $\sqrt{d_k}$ 导致训练不收敛

**场景：** 手动实现 Scaled Dot-Product Attention 时漏掉了除以 $\sqrt{d_k}$

**症状：** 训练 loss 不下降或震荡，注意力权重接近 one-hot（几乎只关注一个 token）

**根因：** 当 $d_k=64$ 时，$Q \cdot K^T$ 的方差约为 64，点积值很大（如 ±20），softmax 输出接近 0/1，梯度极小

**解法：**

❌ 错误写法 — 漏掉缩放

```python
scores = torch.matmul(Q, K.transpose(-2, -1))  # 没有除以 sqrt(d_k)
weights = F.softmax(scores, dim=-1)  # softmax 饱和
```

✅ 正确写法 — 除以 sqrt(d_k)

```python
d_k = Q.size(-1)
scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
weights = F.softmax(scores, dim=-1)
```

**教训：** 缩放是 Transformer 注意力的核心设计之一，不是可选的——它确保 softmax 输入在有意义的梯度区间

> 📖 Paper: Vaswani et al., Section 3.2.1, 脚注 4

---

## 坑 2: PyTorch nn.Transformer 的 batch_first 默认是 False

**场景：** 使用 `nn.Transformer` 或 `nn.MultiheadAttention` 但输入格式为 `(batch, seq, d_model)`

**症状：** 模型输出维度不符合预期，或 loss 不下降，但不报错

**根因：** PyTorch 的 Transformer 默认期望输入格式为 `(seq_len, batch, d_model)`（序列维度在前），而大多数人习惯 `(batch, seq_len, d_model)`

**解法：**

❌ 错误写法 — 忽略 batch_first

```python
model = nn.Transformer(d_model=512, nhead=8)
src = torch.randn(2, 10, 512)  # (batch, seq, d_model) — 格式不匹配！
output = model(src, tgt)  # 静默计算，结果错误
```

✅ 正确写法 — 明确设置 batch_first=True

```python
model = nn.Transformer(d_model=512, nhead=8, batch_first=True)
src = torch.randn(2, 10, 512)  # (batch, seq, d_model) — 正确！
output = model(src, tgt)
```

**教训：** 使用 PyTorch Transformer API 时**始终显式设置** `batch_first=True`，或者在文档中确认默认行为

> 📖 Docs: [nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)

---

## 坑 3: 因果掩码方向搞反导致 Decoder 偷看未来

**场景：** 手动创建因果掩码（causal mask / look-ahead mask）时方向错误

**症状：** Decoder 训练 loss 异常低但测试时生效差（训练时偷看了答案），或者训练 loss 不下降（屏蔽了不该屏蔽的位置）

**根因：** `torch.triu` 生成**上三角**矩阵（对角线以上为 1），应该将上三角设为 $-\infty$（禁止看未来），但容易搞反成下三角

**解法：**

❌ 错误写法 — 掩码方向搞反

```python
# 上三角为 True → 只能看「未来」！方向反了
mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
scores = scores.masked_fill(mask, float('-inf'))  # 屏蔽了过去而非未来
```

✅ 正确写法 — 屏蔽上三角（未来位置）

```python
# 方案 1: 上三角为 True → 用 masked_fill 屏蔽（正确）
causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
scores = scores.masked_fill(causal_mask, float('-inf'))

# 方案 2: 使用 PyTorch 内置方法（最安全）
causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len)
```

**教训：** 优先使用 PyTorch 内置的 `generate_square_subsequent_mask()`；手写掩码时一定验证：位置 $i$ 只能看到 $\leq i$ 的位置

> 📖 Paper: Vaswani et al., Section 3.1
> 🧪 经验: Decoder 训练过拟合排查

---

## 坑 4: 位置编码未与嵌入相加而是拼接

**场景：** 将位置编码与词嵌入**拼接（concat）** 而非**相加（add）**

**症状：** 模型维度翻倍（$d_{model} \times 2$），后续层参数不匹配，或者能跑但性能差

**根因：** 原始论文明确使用**相加**（$\text{input} = \text{Embedding} + \text{PE}$），这保持了 $d_{model}$ 维度不变

**解法：**

❌ 错误写法 — 拼接

```python
x = torch.cat([embedding, positional_encoding], dim=-1)  # 维度变成 2*d_model！
```

✅ 正确写法 — 相加

```python
x = embedding + positional_encoding  # 保持 d_model 维度
# 注意：原始论文对 embedding 乘以 sqrt(d_model) 再加 PE
x = embedding * math.sqrt(d_model) + positional_encoding
```

**教训：** 位置编码和词嵌入是**相加**关系，不是拼接；别忘了 `sqrt(d_model)` 缩放

> 📖 Paper: Vaswani et al., Section 3.4

---

## 坑 5: 训练时未使用 Warmup 学习率导致早期崩溃

**场景：** 使用固定学习率或标准 Adam 设置训练 Transformer

**症状：** 训练前几百步 loss 暴涨或 NaN，模型完全崩溃

**根因：** Transformer 在初始化时参数接近随机，梯度方差大。如果一开始就用大学习率，会导致参数剧烈变化。原始论文使用 warmup 策略：先线性增加学习率到峰值，再逐步衰减

**解法：**

❌ 错误写法 — 固定学习率

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
# 前几步 loss 爆炸
```

✅ 正确写法 — 使用 Warmup 学习率调度

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, betas=(0.9, 0.98), eps=1e-9)

# 使用 PyTorch 的学习率调度器
scheduler = torch.optim.lr_scheduler.LambdaLR(
    optimizer,
    lr_lambda=lambda step: min(
        (step + 1) ** (-0.5),
        (step + 1) * (4000 ** (-1.5))
    ) * (512 ** 0.5)  # d_model=512
)
```

**教训：** Transformer 训练**必须使用 warmup**——这不是可选的超参数，是训练稳定性的必要条件

> 📖 Paper: Vaswani et al., Section 5.3

---

## 坑 6: 注意力头数不能整除 d_model

**场景：** 设置 `d_model=100, n_heads=8`

**症状：** `AssertionError` 或维度不匹配错误

**根因：** 多头注意力将 $d_{model}$ 均分到 $h$ 个头，每头维度 $d_k = d_{model}/h$，必须是整数

**解法：**

❌ 错误写法 — 不整除

```python
model = nn.Transformer(d_model=100, nhead=8)  # 100/8 = 12.5 → 报错
```

✅ 正确写法 — 确保整除

```python
model = nn.Transformer(d_model=512, nhead=8)   # 512/8 = 64 ✓
model = nn.Transformer(d_model=768, nhead=12)  # 768/12 = 64 ✓ (BERT 配置)
```

**教训：** `d_model` 必须是 `nhead` 的整数倍。常见配置：512/8=64, 768/12=64, 1024/16=64

> 📖 Paper: Vaswani et al., Section 3.2.2

---

## 坑 7: 嵌入层未乘以 $\sqrt{d_{model}}$ 导致位置编码信号过强

**场景：** 位置编码与词嵌入直接相加，但未对嵌入进行缩放

**症状：** 模型过度依赖位置信息，忽视词义信息

**根因：** `nn.Embedding` 初始化时权重较小（均值 0，标准差约 1），而正弦位置编码的幅值在 [-1, 1]。当 $d_{model}$ 较大时，嵌入向量的 L2 范数远小于位置编码，信号被淹没。乘以 $\sqrt{d_{model}}$ 是为了平衡两者的量级

**解法：**

❌ 错误写法 — 不缩放嵌入

```python
x = self.embedding(tokens) + self.positional_encoding  # 嵌入信号太弱
```

✅ 正确写法 — 缩放嵌入

```python
x = self.embedding(tokens) * math.sqrt(self.d_model) + self.positional_encoding
```

**教训：** 原始论文的缩放因子 $\sqrt{d_{model}}$ 不是装饰，而是保持嵌入和位置编码信号量级平衡的关键

> 📖 Paper: Vaswani et al., Section 3.4

---

## 调试清单

1. [ ] **缩放因子加了吗？** → 注意力分数是否除以了 `math.sqrt(d_k)`
2. [ ] **batch_first 设对了吗？** → PyTorch Transformer 默认 `batch_first=False`
3. [ ] **因果掩码方向对吗？** → 位置 $i$ 是否只能看到 $\leq i$ 的位置
4. [ ] **位置编码是相加不是拼接？** → `embedding + PE`，不是 `concat`
5. [ ] **嵌入乘以 sqrt(d_model) 了吗？** → 平衡嵌入和位置编码的量级
6. [ ] **d_model 能被 nhead 整除吗？** → $d_{model} / h$ 必须是整数
7. [ ] **学习率有 warmup 吗？** → Transformer 训练必须使用 warmup
8. [ ] **Decoder 输入右移了吗？** → Decoder 输入应该是目标序列右移一位（开头加 BOS）
9. [ ] **padding mask 和 causal mask 都加了吗？** → 两者需要同时使用
10. [ ] **模型进入 eval 模式了吗？** → 推理时 `model.eval()` + `torch.no_grad()`
