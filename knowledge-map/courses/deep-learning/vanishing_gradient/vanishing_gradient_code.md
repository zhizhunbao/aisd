---
topic: vanishing_gradient
dimension: code
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch RNN](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html)"
  - "📖 Docs: [PyTorch LSTM](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)"
  - "📖 Docs: [Keras LSTM](https://keras.io/api/layers/recurrent_layers/lstm/)"
expiry: 6m
status: current
---

# 梯度消失 (Vanishing Gradient) 代码参考

> 📖 Docs: [PyTorch RNN](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html) | [PyTorch LSTM](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

## 快速开始

### 最简示例 — 30 秒看到梯度消失

```python
"""
梯度消失可视化 — 30 秒快速体验
Vanishing Gradient Visualization — 30-second Quick Demo
"""
import torch
import torch.nn as nn

# 创建一个简单 RNN / Create a simple RNN
rnn = nn.RNN(input_size=10, hidden_size=20, num_layers=1, batch_first=True)

# 生成长度为 50 的序列 / Generate sequence of length 50
x = torch.randn(1, 50, 10, requires_grad=True)
h0 = torch.zeros(1, 1, 20)

# 前向传播 / Forward pass
output, hn = rnn(x, h0)

# 计算最后一步的损失并回传 / Compute loss on last step and backprop
loss = output[:, -1, :].sum()
loss.backward()

# 查看输入各时间步的梯度大小 / Check gradient magnitude at each timestep
grad_norms = x.grad[0].norm(dim=1).detach().numpy()
print("时间步 1 梯度:", grad_norms[0])     # 远离输出 → 梯度极小
print("时间步 50 梯度:", grad_norms[-1])    # 靠近输出 → 梯度较大
print("比值:", grad_norms[0] / grad_norms[-1])  # 应该远小于 1
```

运行后你会看到第 1 步的梯度比第 50 步小很多 — **这就是梯度消失**。

> 📖 Docs: [PyTorch RNN](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html)

---


## 完整实现示例

### 示例 1: RNN vs LSTM 梯度对比实验（可视化）

```python
"""
RNN vs LSTM 梯度消失对比实验
RNN vs LSTM Vanishing Gradient Comparison Experiment

验证: LSTM 是否真的解决了梯度消失
Verify: Does LSTM really solve vanishing gradient?
"""
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

def compute_gradient_norms(model_class, seq_len=100, input_size=10, hidden_size=20):
    """
    计算模型各时间步的梯度范数
    Compute gradient norms at each timestep for a given model
    
    Args:
        model_class: nn.RNN 或 nn.LSTM / nn.RNN or nn.LSTM
        seq_len: 序列长度 / Sequence length
        input_size: 输入维度 / Input dimension
        hidden_size: 隐藏维度 / Hidden dimension
    
    Returns:
        grad_norms: 各时间步梯度范数数组 / Array of gradient norms per timestep
    """
    # 创建模型 / Create model
    model = model_class(input_size=input_size, hidden_size=hidden_size, 
                        num_layers=1, batch_first=True)
    
    # 准备输入 / Prepare input
    x = torch.randn(1, seq_len, input_size, requires_grad=True)
    
    # 准备初始隐藏状态 / Prepare initial hidden state
    if model_class == nn.LSTM:
        h0 = (torch.zeros(1, 1, hidden_size), torch.zeros(1, 1, hidden_size))
    else:
        h0 = torch.zeros(1, 1, hidden_size)
    
    # 前向传播 / Forward pass
    output, _ = model(x, h0)
    
    # 只对最后一步求损失 / Loss only on last timestep
    loss = output[:, -1, :].sum()
    loss.backward()
    
    # 提取各时间步梯度范数 / Extract gradient norms per timestep
    grad_norms = x.grad[0].norm(dim=1).detach().numpy()
    
    return grad_norms

# 运行实验 / Run experiment
seq_len = 100
rnn_grads = compute_gradient_norms(nn.RNN, seq_len=seq_len)
lstm_grads = compute_gradient_norms(nn.LSTM, seq_len=seq_len)

# 可视化 / Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图: 线性刻度 / Left: linear scale
axes[0].plot(range(seq_len), rnn_grads, label='RNN', color='red', alpha=0.7)
axes[0].plot(range(seq_len), lstm_grads, label='LSTM', color='blue', alpha=0.7)
axes[0].set_xlabel('Timestep (时间步)')
axes[0].set_ylabel('Gradient Norm (梯度范数)')
axes[0].set_title('Gradient Norms: RNN vs LSTM (Linear Scale)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 右图: 对数刻度 / Right: log scale
axes[1].semilogy(range(seq_len), rnn_grads + 1e-10, label='RNN', color='red', alpha=0.7)
axes[1].semilogy(range(seq_len), lstm_grads + 1e-10, label='LSTM', color='blue', alpha=0.7)
axes[1].set_xlabel('Timestep (时间步)')
axes[1].set_ylabel('Gradient Norm (log scale)')
axes[1].set_title('Gradient Norms: RNN vs LSTM (Log Scale)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('vanishing_gradient_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# 打印统计 / Print statistics
print(f"\n{'='*50}")
print(f"序列长度 / Sequence Length: {seq_len}")
print(f"{'='*50}")
print(f"RNN  - 第1步梯度: {rnn_grads[0]:.2e}, 最后一步: {rnn_grads[-1]:.2e}, "
      f"比值: {rnn_grads[0]/rnn_grads[-1]:.2e}")
print(f"LSTM - 第1步梯度: {lstm_grads[0]:.2e}, 最后一步: {lstm_grads[-1]:.2e}, "
      f"比值: {lstm_grads[0]/lstm_grads[-1]:.2e}")
```

> 📖 Docs: [PyTorch RNN](https://pytorch.org/docs/stable/generated/torch.nn.RNN.html) | [PyTorch LSTM](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

---

### 示例 2: LSTM 文本生成（Keras 实现）

```python
"""
LSTM 语言模型 — Keras 实现
LSTM Language Model — Keras Implementation
"""
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, Embedding

# 模型参数 / Model parameters
VOCAB_SIZE = 10000          # 词汇表大小 / Vocabulary size
EMBEDDING_DIM = 128         # 嵌入维度 / Embedding dimension
HIDDEN_SIZE = 256           # LSTM 隐藏层大小 / LSTM hidden size
TIMESTEPS = 50              # 序列长度 / Sequence length
NUM_CLASSES = VOCAB_SIZE    # 输出类别数 = 词汇表大小 / Output = vocab size

# 构建模型 / Build model
model = Sequential([
    Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=TIMESTEPS),
    LSTM(HIDDEN_SIZE),                       # LSTM 层（自动处理梯度消失）
    Dense(NUM_CLASSES),                       # 全连接输出层 / Dense output
    Activation('softmax')                     # Softmax 概率分布 / Probability distribution
])

model.compile(
    loss='categorical_crossentropy',          # 交叉熵损失 / Cross-entropy loss
    optimizer='adam',                          # Adam 优化器 / Adam optimizer
    metrics=['accuracy']                       # 准确率 / Accuracy
)

model.summary()
```

> 📖 Docs: [Keras LSTM](https://keras.io/api/layers/recurrent_layers/lstm/)

---

### 示例 3: 梯度裁剪实战

```python
"""
梯度裁剪 — 防止梯度爆炸的标准做法
Gradient Clipping — Standard practice to prevent exploding gradients
"""
import torch
import torch.nn as nn

# 模型和优化器 / Model and optimizer
model = nn.LSTM(input_size=50, hidden_size=100, num_layers=2, batch_first=True)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练循环（伪代码）/ Training loop (pseudo)
for epoch in range(10):
    # 前向传播 / Forward
    x = torch.randn(32, 30, 50)  # batch=32, seq_len=30, input=50
    output, _ = model(x)
    loss = output.sum()  # 简化的损失 / Simplified loss
    
    # 反向传播 / Backward
    optimizer.zero_grad()
    loss.backward()
    
    # ★ 梯度裁剪（关键步骤）/ Gradient clipping (KEY STEP)
    # max_norm=5 表示：如果梯度的总范数 > 5，按比例缩小
    # max_norm=5 means: if total gradient norm > 5, scale down proportionally
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
    
    # 更新参数 / Update parameters
    optimizer.step()
    
    # 监控梯度范数 / Monitor gradient norms
    total_norm = sum(p.grad.norm().item()**2 for p in model.parameters() if p.grad is not None)**0.5
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}, Grad Norm: {total_norm:.4f}")
```

> 📖 Docs: [clip_grad_norm_](https://pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html)

---


## API 速查

### PyTorch RNN/LSTM

| 函数 | 说明 | 关键参数 |
|------|------|---------|
| `nn.RNN()` | 基本 RNN | `input_size, hidden_size, num_layers, nonlinearity='tanh'` |
| `nn.LSTM()` | LSTM | `input_size, hidden_size, num_layers, dropout` |
| `nn.GRU()` | GRU | `input_size, hidden_size, num_layers` |
| `clip_grad_norm_()` | 梯度裁剪 | `parameters, max_norm, norm_type=2.0` |
| `clip_grad_value_()` | 梯度值裁剪 | `parameters, clip_value` |

### Keras LSTM

| 函数 | 说明 | 关键参数 |
|------|------|---------|
| `LSTM()` | LSTM 层 | `units, return_sequences=False, dropout=0.0` |
| `Bidirectional()` | 双向包装 | `layer, merge_mode='concat'` |

> 📖 Docs: [PyTorch](https://pytorch.org/docs/stable/) | [Keras](https://keras.io/api/layers/recurrent_layers/)
