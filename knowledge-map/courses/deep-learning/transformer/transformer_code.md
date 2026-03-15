---
topic: transformer
dimension: code
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
  - "📖 Docs: PyTorch nn.MultiheadAttention — https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html"
  - "💻 Source: pytorch/pytorch — https://github.com/pytorch/pytorch"
expiry: 6m
status: current
---

# Transformer 代码参考

> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)
> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)


## 快速开始

### 最简示例 — 从零理解 Scaled Dot-Product Attention

```python
# ============================================================
# Transformer 最简示例: 手动实现 Scaled Dot-Product Attention
# Minimal Example: Manual Scaled Dot-Product Attention
# ============================================================
import torch
import torch.nn.functional as F

# 模拟输入: 2 个 token，每个 4 维 / Simulate: 2 tokens, 4-dim each
d_k = 4
Q = torch.tensor([[1.0, 0.0, 1.0, 0.0],   # token 1 的 query
                   [0.0, 1.0, 0.0, 1.0]])   # token 2 的 query
K = torch.tensor([[1.0, 1.0, 0.0, 0.0],   # token 1 的 key
                   [0.0, 0.0, 1.0, 1.0]])   # token 2 的 key
V = torch.tensor([[1.0, 0.0, 0.0, 0.0],   # token 1 的 value
                   [0.0, 1.0, 0.0, 0.0]])   # token 2 的 value

# 计算注意力 / Compute attention
scores = torch.matmul(Q, K.T) / (d_k ** 0.5)  # QK^T / sqrt(d_k)
weights = F.softmax(scores, dim=-1)             # softmax 归一化
output = torch.matmul(weights, V)               # 加权求和

print(f"注意力分数 / Attention scores:\n{scores}")
print(f"注意力权重 / Attention weights:\n{weights}")
print(f"输出 / Output:\n{output}")
```

**测试方法：** 运行脚本，确认 `weights` 每行和为 1，`output` 的维度为 `[2, 4]`。

> 📖 Paper: Vasvani et al., Section 3.2.1

---

## 完整实现示例

### 示例 1: 从零实现 Transformer（教学版）

```python
# ============================================================
# 1. 从零实现 Transformer / Transformer from Scratch
# 不使用 nn.Transformer，逐组件实现，适合理解原理
# ============================================================
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

# ============================================================
# 1.1 Scaled Dot-Product Attention
# ============================================================
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    计算缩放点积注意力 / Compute scaled dot-product attention
    Q, K, V: (batch, heads, seq_len, d_k)
    mask: (batch, 1, 1, seq_len) or (1, 1, seq_len, seq_len)
    """
    d_k = Q.size(-1)
    # QK^T / sqrt(d_k)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

    # 应用掩码（padding mask 或 causal mask）
    # Apply mask (padding mask or causal mask)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))

    # softmax 归一化 / Softmax normalization
    weights = F.softmax(scores, dim=-1)

    # 加权求和 / Weighted sum
    output = torch.matmul(weights, V)
    return output, weights

# ============================================================
# 1.2 Multi-Head Attention
# ============================================================
class MultiHeadAttention(nn.Module):
    """
    多头注意力 / Multi-Head Attention
    将输入投影到 h 个子空间，分别计算注意力，拼接后合并
    """
    def __init__(self, d_model, n_heads):
        super().__init__()
        assert d_model % n_heads == 0    # d_model 必须被 n_heads 整除
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads    # 每个头的维度 / Per-head dimension

        # Q/K/V 投影矩阵 + 输出投影 / Projection matrices
        self.W_q = nn.Linear(d_model, d_model)  # 所有头共用一个大矩阵
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)  # 输出合并

    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)

        # 线性投影 + 分头 / Linear projection + split heads
        # (batch, seq_len, d_model) → (batch, n_heads, seq_len, d_k)
        Q = self.W_q(Q).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)

        # 多头注意力 / Multi-head attention
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)

        # 合并所有头 / Concatenate heads
        # (batch, n_heads, seq_len, d_k) → (batch, seq_len, d_model)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)

        # 输出投影 / Output projection
        output = self.W_o(attn_output)
        return output

# ============================================================
# 1.3 Position-wise Feed-Forward Network
# ============================================================
class FeedForward(nn.Module):
    """FFN(x) = ReLU(xW₁ + b₁)W₂ + b₂"""
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)    # 扩展层 / Expansion
        self.linear2 = nn.Linear(d_ff, d_model)    # 压缩层 / Compression
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.linear2(self.dropout(F.relu(self.linear1(x))))

# ============================================================
# 1.4 Positional Encoding
# ============================================================
class PositionalEncoding(nn.Module):
    """正弦/余弦位置编码 / Sinusoidal Positional Encoding"""
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)               # (max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)  # (max_len, 1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)      # 偶数维度用 sin
        pe[:, 1::2] = torch.cos(position * div_term)      # 奇数维度用 cos
        pe = pe.unsqueeze(0)                               # (1, max_len, d_model)
        self.register_buffer('pe', pe)                     # 不是参数，不更新

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        x = x + self.pe[:, :x.size(1), :]                 # 与嵌入相加
        return self.dropout(x)

# ============================================================
# 1.5 Encoder Layer
# ============================================================
class EncoderLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Self-Attention + Add & Norm
        attn_out = self.self_attn(x, x, x, mask)       # Q=K=V=x (Self-Attention)
        x = self.norm1(x + self.dropout1(attn_out))     # 残差 + LayerNorm

        # FFN + Add & Norm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout2(ffn_out))      # 残差 + LayerNorm
        return x

# ============================================================
# 1.6 Decoder Layer
# ============================================================
class DecoderLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_heads)     # Masked Self-Attention
        self.cross_attn = MultiHeadAttention(d_model, n_heads)    # Cross-Attention
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_output, src_mask=None, tgt_mask=None):
        # Masked Self-Attention (因果掩码)
        attn1 = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn1))

        # Cross-Attention (Q=Decoder, K/V=Encoder)
        attn2 = self.cross_attn(x, enc_output, enc_output, src_mask)
        x = self.norm2(x + self.dropout(attn2))

        # FFN
        ffn_out = self.ffn(x)
        x = self.norm3(x + self.dropout(ffn_out))
        return x

# ============================================================
# 1.7 完整 Transformer
# ============================================================
class Transformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=512, n_heads=8,
                 n_layers=6, d_ff=2048, dropout=0.1, max_len=5000):
        super().__init__()
        self.d_model = d_model

        # 嵌入层 / Embedding layers
        self.src_embed = nn.Embedding(src_vocab, d_model)
        self.tgt_embed = nn.Embedding(tgt_vocab, d_model)
        self.pos_encoder = PositionalEncoding(d_model, max_len, dropout)

        # Encoder / Decoder stacks
        self.encoder_layers = nn.ModuleList(
            [EncoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)]
        )
        self.decoder_layers = nn.ModuleList(
            [DecoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)]
        )

        # 输出层 / Output layer
        self.fc_out = nn.Linear(d_model, tgt_vocab)

    def generate_causal_mask(self, size):
        """生成因果掩码（下三角矩阵）/ Generate causal (look-ahead) mask"""
        mask = torch.triu(torch.ones(size, size), diagonal=1).bool()
        return ~mask  # True = 可以 attend, False = 被屏蔽

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        # 嵌入 + 位置编码 / Embedding + Positional Encoding
        src = self.pos_encoder(self.src_embed(src) * math.sqrt(self.d_model))
        tgt = self.pos_encoder(self.tgt_embed(tgt) * math.sqrt(self.d_model))

        # 生成因果掩码 / Generate causal mask for decoder
        if tgt_mask is None:
            tgt_mask = self.generate_causal_mask(tgt.size(1)).to(tgt.device)

        # Encoder 前向 / Encoder forward
        enc_output = src
        for layer in self.encoder_layers:
            enc_output = layer(enc_output, src_mask)

        # Decoder 前向 / Decoder forward
        dec_output = tgt
        for layer in self.decoder_layers:
            dec_output = layer(dec_output, enc_output, src_mask, tgt_mask)

        # 输出层 / Output projection
        output = self.fc_out(dec_output)
        return output

# ============================================================
# 1.8 测试 / Quick Test
# ============================================================
if __name__ == "__main__":
    model = Transformer(src_vocab=1000, tgt_vocab=1000, d_model=128, n_heads=4, n_layers=2, d_ff=256)

    src = torch.randint(0, 1000, (2, 10))   # batch=2, src_len=10
    tgt = torch.randint(0, 1000, (2, 8))    # batch=2, tgt_len=8

    output = model(src, tgt)
    print(f"输出形状 / Output shape: {output.shape}")  # (2, 8, 1000)
    print(f"参数量 / Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

> 📖 Paper: Vasvani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 3
> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)

---

### 示例 2: 使用 PyTorch 内置 nn.Transformer（快速使用）

```python
# ============================================================
# 2. PyTorch 内置 nn.Transformer / Built-in PyTorch Transformer
# ============================================================
import torch
import torch.nn as nn

# 创建 Transformer 模型 / Create Transformer model
model = nn.Transformer(
    d_model=512,       # 模型维度 / Model dimension
    nhead=8,           # 注意力头数 / Number of attention heads
    num_encoder_layers=6,
    num_decoder_layers=6,
    dim_feedforward=2048,
    dropout=0.1,
    batch_first=True   # 重要：输入格式 (batch, seq, feature)
)

# 模拟输入 / Simulate input
src = torch.randn(2, 10, 512)   # (batch=2, src_len=10, d_model=512)
tgt = torch.randn(2, 8, 512)    # (batch=2, tgt_len=8, d_model=512)

# 生成因果掩码 / Generate causal mask
tgt_mask = nn.Transformer.generate_square_subsequent_mask(8)

# 前向传播 / Forward pass
output = model(src, tgt, tgt_mask=tgt_mask)
print(f"输出形状 / Output shape: {output.shape}")  # (2, 8, 512)
```

> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)

---

### 示例 3: Hugging Face Transformers 使用预训练模型

```python
# ============================================================
# 3. 使用 HF Transformers 加载预训练 Transformer
# ============================================================
from transformers import AutoTokenizer, AutoModel

# 加载 BERT (Transformer Encoder)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# 推理 / Inference
inputs = tokenizer("Transformer is all you need!", return_tensors="pt")
outputs = model(**inputs)

print(f"Hidden states shape: {outputs.last_hidden_state.shape}")
# (1, 8, 768) — 8 个 token, 768 维隐藏状态
```

> 📖 Docs: [HF Transformers](https://huggingface.co/docs/transformers)

---

## API 速查

### PyTorch 核心 Transformer API

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Transformer(d_model, nhead)` | `d_model` | 512 | 模型隐藏维度 |
| ↳ `nhead` | `int` | 8 | 注意力头数 |
| ↳ `num_encoder_layers` | `int` | 6 | Encoder 层数 |
| ↳ `num_decoder_layers` | `int` | 6 | Decoder 层数 |
| ↳ `dim_feedforward` | `int` | 2048 | FFN 中间层维度 |
| ↳ `dropout` | `float` | 0.1 | Dropout 率 |
| ↳ `batch_first` | `bool` | `False` | `True` → (batch, seq, d) |
| `nn.MultiheadAttention(embed_dim, num_heads)` | `embed_dim` | — | 嵌入维度 |
| ↳ `num_heads` | `int` | — | 头数 |
| ↳ `batch_first` | `bool` | `False` | 同上 |
| `nn.TransformerEncoderLayer` | 同 nn.Transformer | — | 单个 Encoder 层 |
| `nn.TransformerDecoderLayer` | 同 nn.Transformer | — | 单个 Decoder 层 |

### 掩码相关

| 函数 | 说明 |
|------|------|
| `nn.Transformer.generate_square_subsequent_mask(sz)` | 生成因果掩码 $sz \times sz$ |
| `scores.masked_fill(mask == 0, float('-inf'))` | 应用自定义掩码 |
| `torch.triu(torch.ones(n, n), diagonal=1)` | 上三角矩阵（因果掩码基础）|

### 常用工具

| 函数 | 说明 |
|------|------|
| `F.scaled_dot_product_attention(Q, K, V)` | PyTorch 2.0+ 内置 SDPA（支持 FlashAttention）|
| `math.sqrt(d_k)` | 缩放因子 |
| `F.softmax(scores, dim=-1)` | softmax 归一化 |
| `nn.LayerNorm(d_model)` | 层归一化 |
| `nn.Embedding(vocab_size, d_model)` | 词嵌入 |

> 📖 Docs: [PyTorch Transformer Docs](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)

---

## 目录结构模板

### 简单结构

```
transformer-demo/
├── transformer.py          ← 从零实现 Transformer
├── train.py                ← 训练脚本
└── data/
    ├── train.txt           ← 训练数据
    └── vocab.txt           ← 词表
```

### 标准结构

```
transformer-project/
├── model/
│   ├── attention.py        ← 注意力模块
│   ├── encoder.py          ← Encoder
│   ├── decoder.py          ← Decoder
│   ├── transformer.py      ← 完整模型
│   └── positional.py       ← 位置编码
├── data/
│   ├── dataset.py          ← 数据集加载
│   └── tokenizer.py        ← 分词器
├── train.py
├── evaluate.py
├── config.yaml
└── requirements.txt
```

> 📖 Paper: Vasvani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
