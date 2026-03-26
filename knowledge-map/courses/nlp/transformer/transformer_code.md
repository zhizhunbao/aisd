---
topic: transformer
dimension: code
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
  - "📖 Docs: HuggingFace Transformers — https://huggingface.co/docs/transformers/"
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
expiry: 6m
status: current
---

# Transformer 代码参考

> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)
> 📖 Docs: [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

## 快速开始

### 最简示例 — 30 秒上手

```python
import torch
import torch.nn as nn

# ============================================================
# 最简 Transformer: 用 PyTorch 内置模块做序列到序列
# Minimal Transformer: using PyTorch built-in for seq2seq
# ============================================================

# 超参数 / Hyperparameters
d_model = 512   # 模型维度 / model dimension
nhead = 8       # 注意力头数 / number of attention heads
num_layers = 6  # 编码/解码器层数 / encoder/decoder layers

# 创建 Transformer 模型 / Create Transformer model
model = nn.Transformer(
    d_model=d_model,
    nhead=nhead,
    num_encoder_layers=num_layers,
    num_decoder_layers=num_layers,
)

# 模拟输入 / Simulated input (seq_len, batch_size, d_model)
src = torch.rand(10, 1, d_model)   # 源序列：10 个词 / source: 10 tokens
tgt = torch.rand(5, 1, d_model)    # 目标序列：5 个词 / target: 5 tokens

# 前向传播 / Forward pass
output = model(src, tgt)  # shape: (5, 1, 512)
print(f"输出形状 / Output shape: {output.shape}")
```

**测试方法：** 直接运行，无需 GPU。输出应为 `torch.Size([5, 1, 512])`。

---

## 完整实现示例

### 示例 1: 手写 Scaled Dot-Product Attention

```python
import torch
import torch.nn.functional as F
import math

# ============================================================
# 1. 缩放点积注意力（从零实现）
# Scaled Dot-Product Attention (from scratch)
# ============================================================

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    缩放点积注意力 / Scaled dot-product attention
    
    Args:
        Q: 查询矩阵 / Query (batch, heads, seq_len, d_k)
        K: 键矩阵 / Key (batch, heads, seq_len, d_k)
        V: 值矩阵 / Value (batch, heads, seq_len, d_v)
        mask: 掩码矩阵 / Mask (optional)
    Returns:
        output: 注意力加权输出 / Attention-weighted output
        attention_weights: 注意力权重 / Attention weights
    """
    d_k = Q.size(-1)  # 每个头的维度 / dimension per head
    
    # Step 1: Q·K^T 计算相关度分数 / compute attention scores
    scores = torch.matmul(Q, K.transpose(-2, -1))  # (batch, heads, seq, seq)
    
    # Step 2: 缩放——除以 √d_k 防止 softmax 饱和 / scale to prevent saturation
    scores = scores / math.sqrt(d_k)
    
    # Step 3: 掩码——把不该看的位置设为 -inf / mask out forbidden positions
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    # Step 4: softmax 归一化——变成概率 / normalize to probabilities
    attention_weights = F.softmax(scores, dim=-1)
    
    # Step 5: 加权求和 V / weighted sum of values
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights


# ============================================================
# 2. 测试 / Test
# ============================================================

batch_size, n_heads, seq_len, d_k = 1, 1, 4, 8
Q = torch.randn(batch_size, n_heads, seq_len, d_k)
K = torch.randn(batch_size, n_heads, seq_len, d_k)
V = torch.randn(batch_size, n_heads, seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print(f"输出形状 / Output shape: {output.shape}")       # (1, 1, 4, 8)
print(f"注意力权重 / Attention weights:\n{weights[0, 0]}")  # (4, 4) 每行和为 1
print(f"权重行和 / Row sums: {weights[0, 0].sum(dim=-1)}")  # 全是 1.0
```

### 示例 2: 手写 Multi-Head Attention

```python
import torch
import torch.nn as nn
import math

# ============================================================
# 1. 多头注意力（从零实现）
# Multi-Head Attention (from scratch)
# ============================================================

class MultiHeadAttention(nn.Module):
    """
    多头注意力模块 / Multi-Head Attention module
    拆成 h 个头，每个头独立算注意力，最后拼接
    Split into h heads, each computes attention independently, then concat
    """
    def __init__(self, d_model=512, n_heads=8):
        super().__init__()
        assert d_model % n_heads == 0, "d_model 必须整除 n_heads"
        
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads  # 每头维度 / per-head dim = 64
        
        # Q/K/V 的线性投影 / Linear projections for Q, K, V
        self.W_Q = nn.Linear(d_model, d_model)  # 512 → 512
        self.W_K = nn.Linear(d_model, d_model)  # 512 → 512
        self.W_V = nn.Linear(d_model, d_model)  # 512 → 512
        
        # 输出投影 / Output projection
        self.W_O = nn.Linear(d_model, d_model)  # 512 → 512
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        seq_len = query.size(1)
        
        # Step 1: 线性投影 / Linear projection
        Q = self.W_Q(query)  # (batch, seq, 512)
        K = self.W_K(key)
        V = self.W_V(value)
        
        # Step 2: 拆成多头 / Reshape to (batch, n_heads, seq, d_k)
        Q = Q.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
        
        # Step 3: 每个头做缩放点积注意力 / Scaled dot-product per head
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn_weights = torch.softmax(scores, dim=-1)
        context = torch.matmul(attn_weights, V)  # (batch, heads, seq, d_k)
        
        # Step 4: 拼接所有头 / Concat all heads
        context = context.transpose(1, 2).contiguous().view(
            batch_size, -1, self.d_model
        )  # (batch, seq, 512)
        
        # Step 5: 输出投影 / Output projection
        output = self.W_O(context)  # (batch, seq, 512)
        
        return output, attn_weights


# ============================================================
# 2. 测试 / Test
# ============================================================

mha = MultiHeadAttention(d_model=512, n_heads=8)
x = torch.randn(2, 10, 512)  # batch=2, seq=10, dim=512
output, weights = mha(x, x, x)  # Self-Attention: Q=K=V=x
print(f"输出形状 / Output shape: {output.shape}")   # (2, 10, 512)
print(f"注意力形状 / Attn shape: {weights.shape}")   # (2, 8, 10, 10)
print(f"参数量 / Params: {sum(p.numel() for p in mha.parameters()):,}")
```

### 示例 3: 位置编码 + 因果掩码

```python
import torch
import math

# ============================================================
# 1. 正弦位置编码 / Sinusoidal Positional Encoding
# ============================================================

def positional_encoding(max_len, d_model):
    """
    生成正弦余弦位置编码 / Generate sinusoidal positional encoding
    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len).unsqueeze(1).float()  # (max_len, 1)
    
    # 分母：10000^(2i/d_model) / Denominator
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
    )
    
    pe[:, 0::2] = torch.sin(position * div_term)  # 偶数维 sin / even dims
    pe[:, 1::2] = torch.cos(position * div_term)  # 奇数维 cos / odd dims
    
    return pe  # (max_len, d_model)


# ============================================================
# 2. 因果掩码 / Causal Mask (for Decoder)
# ============================================================

def generate_causal_mask(seq_len):
    """
    生成因果掩码——下三角矩阵 / Generate causal mask — lower triangular
    1 = 可以看, 0 = 不能看 / 1 = attend, 0 = mask out
    """
    mask = torch.tril(torch.ones(seq_len, seq_len))
    return mask  # (seq_len, seq_len)


# ============================================================
# 3. 测试 / Test
# ============================================================

# 位置编码 / Positional encoding
pe = positional_encoding(max_len=100, d_model=512)
print(f"位置编码形状 / PE shape: {pe.shape}")  # (100, 512)
print(f"位置 0 前 4 维 / Pos 0, first 4 dims: {pe[0, :4]}")
print(f"位置 1 前 4 维 / Pos 1, first 4 dims: {pe[1, :4]}")

# 因果掩码 / Causal mask
mask = generate_causal_mask(5)
print(f"\n因果掩码 (5×5) / Causal mask:\n{mask}")
# 输出：下三角矩阵，位置 i 只能看到位置 0~i
```

---

## API 速查

### PyTorch nn.Transformer

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Transformer()` | | | 完整 Encoder-Decoder Transformer |
| ↳ `d_model` | int | 512 | 模型维度 / Model dimension |
| ↳ `nhead` | int | 8 | 注意力头数 / Number of heads |
| ↳ `num_encoder_layers` | int | 6 | Encoder 层数 |
| ↳ `num_decoder_layers` | int | 6 | Decoder 层数 |
| ↳ `dim_feedforward` | int | 2048 | FFN 隐藏维度 |
| ↳ `dropout` | float | 0.1 | Dropout 概率 |
| ↳ `batch_first` | bool | False | True: (batch, seq, dim); False: (seq, batch, dim) |
| `nn.TransformerEncoder()` | | | 只有 Encoder 部分 |
| ↳ `encoder_layer` | Module | — | 单层 EncoderLayer |
| ↳ `num_layers` | int | — | 堆叠层数 |
| `nn.TransformerEncoderLayer()` | | | 单层 Encoder |
| ↳ `d_model` | int | — | 模型维度 |
| ↳ `nhead` | int | — | 头数 |
| ↳ `dim_feedforward` | int | 2048 | FFN 维度 |
| ↳ `norm_first` | bool | False | True=Pre-LN, False=Post-LN |
| `nn.MultiheadAttention()` | | | 多头注意力模块 |
| ↳ `embed_dim` | int | — | 嵌入维度 (= d_model) |
| ↳ `num_heads` | int | — | 头数 |
| ↳ `batch_first` | bool | False | 是否 batch 维在前 |

### HuggingFace Transformers（高层 API）

| 函数/类 | 参数 | 说明 |
|---------|------|------|
| `AutoModel.from_pretrained()` | model_name | 加载预训练模型 |
| `AutoTokenizer.from_pretrained()` | model_name | 加载对应分词器 |
| `model(**inputs)` | input_ids, attention_mask | 前向传播 |
| `model.generate()` | max_length, num_beams, temperature | 文本生成（Decoder 模型）|

> 📖 Docs: [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html)
> 📖 Docs: [HuggingFace Transformers](https://huggingface.co/docs/transformers/)

---

## 目录结构模板

### 简单结构

```
project/
├── train.py              ← 训练脚本 / Training script
├── model.py              ← Transformer 模型 / Model definition
└── data/
    ├── train.txt          ← 训练数据 / Training data
    └── val.txt            ← 验证数据 / Validation data
```

### 标准结构

```
project/
├── config.py              ← 超参数配置 / Hyperparameters
├── dataset.py             ← 数据加载 + 分词 / Data loading + tokenization
├── model.py               ← Transformer 各模块 / Model components
│   ├── attention.py       ← Multi-Head Attention
│   ├── encoder.py         ← Encoder stack
│   ├── decoder.py         ← Decoder stack
│   └── transformer.py     ← Full model
├── train.py               ← 训练循环 / Training loop
├── evaluate.py            ← 评估 + BLEU / Evaluation
├── utils.py               ← 掩码生成等工具 / Mask utils
├── data/                  ← 数据目录 / Data directory
├── checkpoints/           ← 模型存档 / Model checkpoints
└── logs/                  ← TensorBoard 日志 / Logs
```
