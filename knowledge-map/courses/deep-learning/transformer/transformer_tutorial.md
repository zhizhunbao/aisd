---
topic: transformer
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9-10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10,12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.Transformer — https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html"
expiry: 12m
status: current
---

# Transformer 教程

> **前置知识：** 线性代数（矩阵乘法）、神经网络基础（MLP、反向传播）、序列模型概念（RNN/LSTM）、softmax 函数
> **参考来源：** [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | [《SLP3》Ch.9](../../../textbooks/jurafsky_slp3.pdf) | [《Deep Learning》Ch.10](../../../textbooks/goodfellow_deep_learning.pdf)

---


## Section 0: 前置知识速查

1. **矩阵乘法**：$C = AB$ 中，$A$ 的每行与 $B$ 的每列做点积；理解维度兼容性（$m \times k$ 乘 $k \times n$ 得 $m \times n$）
2. **softmax 函数**：$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$，将任意实数向量归一化为概率分布（所有元素 > 0 且和为 1）
3. **RNN 的顺序处理**：$h_t = f(h_{t-1}, x_t)$ — 每个时间步依赖前一步的隐藏状态，无法并行
4. **Seq2Seq 架构**：Encoder 将输入序列编码为固定向量，Decoder 从该向量解码输出序列（"信息瓶颈"问题）
5. **Bahdanau 注意力**：Decoder 每步不只看固定向量，而是对 Encoder 所有隐藏状态加权求和——Transformer 的直接前身

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10.1-10.2

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **RNN 无法并行**：LSTM/GRU 必须按时间步顺序计算 $h_1 \to h_2 \to ... \to h_n$，GPU 的大量并行计算能力被浪费。一个长度 1000 的序列需要串行 1000 步
- 🔥 **长距离依赖消失**：虽然 LSTM 缓解了梯度消失，但信息仍需"接力传递" $n$ 步才能从第 1 个 token 到达第 $n$ 个 token，传递过程中信息不可避免地衰减
- 🔥 **Seq2Seq 信息瓶颈**：传统 Encoder-Decoder 将整个输入压缩为一个固定长度向量，输入越长信息丢失越严重。Bahdanau 注意力缓解了这一问题，但 Encoder 自身仍是 RNN
- 🔥 **训练时间长**：GPT-3 级别的模型如果用 RNN 架构，训练时间将是天文数字——2017 年的机器翻译模型训练 1 周，而同等质量的 Transformer 只需 12 小时

### 它的核心价值

1. **完全并行化**：Self-Attention 对所有位置**同时**计算，一步即可得到完整的注意力矩阵。训练速度比 RNN 快一个数量级
2. **$O(1)$ 长距离依赖**：任意两个 token 之间只需一步 Self-Attention 就能直接交互——不再需要信息"接力传递"
3. **统一的 Encoder-Decoder**：Encoder 和 Decoder 都基于相同的注意力块构建，架构简洁优雅
4. **易于扩展**：堆叠更多层、增大维度就能提升性能，催生了从 BERT-base (110M) 到 GPT-4 (1.8T) 的规模化路径
5. **跨领域通用**：同一个架构在 NLP、CV、语音、蛋白质结构预测等领域全面成功

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Section 1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.1

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 整体架构

```
┌───────────────────────────────────────────────────────────────┐
│                   Transformer 完整架构                         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  输入: "I love NLP"           输出: "我 爱 NLP"               │
│       │                            │                          │
│       ▼                            ▼                          │
│  ┌──────────┐               ┌──────────┐                     │
│  │ Embedding │               │ Embedding │ (输出右移一位)      │
│  │ + PE      │               │ + PE      │                    │
│  └──────────┘               └──────────┘                     │
│       │                            │                          │
│       ▼                            ▼                          │
│  ┌──────────────────┐  ┌────────────────────────┐            │
│  │   ENCODER ×6     │  │     DECODER ×6          │            │
│  │                  │  │                          │            │
│  │ Multi-Head       │  │ Masked Multi-Head        │            │
│  │ Self-Attention   │  │ Self-Attention            │           │
│  │      │           │  │      │                    │           │
│  │ Add & LayerNorm  │  │ Add & LayerNorm          │            │
│  │      │           │  │      │                    │           │
│  │ FFN              │  │ Multi-Head Cross-Attention│            │
│  │      │           │  │ (Q=Dec, K/V=Enc output)  │←── Enc输出│
│  │ Add & LayerNorm  │  │      │                    │           │
│  │                  │  │ Add & LayerNorm           │            │
│  └──────────────────┘  │      │                    │           │
│                        │ FFN                       │            │
│                        │      │                    │            │
│                        │ Add & LayerNorm           │            │
│                        └────────────────────────┘             │
│                                    │                          │
│                                    ▼                          │
│                            Linear + Softmax                   │
│                                    │                          │
│                             下一个 token 概率                  │
└───────────────────────────────────────────────────────────────┘
```

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), Figure 1

### 2.2 Self-Attention：核心机制

**为什么用点积注意力而不是加性注意力？**

Bahdanau 2015 的加性注意力用一个小型 MLP 计算注意力分数：$\text{score}(s, h) = v^T \tanh(W_1 s + W_2 h)$。虽然理论上更灵活，但**矩阵乘法** $QK^T$ 可以直接调用高度优化的 GPU BLAS 库（如 cuBLAS），速度远快于 MLP 的逐元素操作。在实践中，两者性能相当，但点积注意力快得多。

**Self-Attention 的直觉理解：**

想象一个句子 "The cat sat on the mat because it was tired"。当模型处理 "it" 这个词时：
- **Query**（"it" 在找什么？）：它在寻找自己指代的对象
- **Key**（每个词的标签）：每个词提供自己的"特征标签"
- **Value**（每个词的内容）：每个词提供自己的实际语义表示
- **注意力权重**：$Q_{it} \cdot K_{cat}^T$ 可能很高（因为 "it" 指代 "cat"），而 $Q_{it} \cdot K_{on}^T$ 会很低

> 📖 Paper: Vaswani et al., Section 3.2.1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.2

### 2.3 因果掩码：为什么 Decoder 不能看未来

Decoder 在生成位置 $t$ 的 token 时，**不能偷看** 位置 $t+1, t+2, ...$ 的内容（因为推理时这些位置还没有生成）。因此在计算 Self-Attention 时，将未来位置的注意力分数设为 $-\infty$：

```
注意力分数矩阵（Decoder Self-Attention）:

        pos_1  pos_2  pos_3  pos_4
pos_1 [  ✓     -∞     -∞     -∞  ]
pos_2 [  ✓      ✓     -∞     -∞  ]
pos_3 [  ✓      ✓      ✓     -∞  ]
pos_4 [  ✓      ✓      ✓      ✓  ]

✓ = 可以 attend
-∞ = softmax 后变成 0（被屏蔽）
```

> 📖 Paper: Vaswani et al., Section 3.1

### 2.4 训练与推理的差异

```
训练时                              推理时
┌──────────────────────────┐       ┌───────────────────────────┐
│ Encoder: 并行编码全部输入  │       │ Encoder: 并行编码全部输入   │
│ Decoder: 输入完整目标序列  │       │ Decoder: 逐个 token 生成   │
│   (右移后 + 因果掩码)     │       │   step 1: <BOS>            │
│   一次前向即得所有位置预测 │       │   → 预测 token_1            │
│   Loss = cross_entropy   │       │   step 2: <BOS> token_1    │
│                          │       │   → 预测 token_2            │
│ 教师强制: 用 ground truth │       │   step N: ... → <EOS>       │
│ 而非模型自身预测作为输入   │       │   使用自身预测作为下一步输入  │
└──────────────────────────┘       └───────────────────────────┘
```

训练时可以并行计算所有位置（因为有完整的 ground truth + 因果掩码）；推理时必须顺序生成（因为每步的输入依赖上一步的输出）。

> 📖 Paper: Vaswani et al., Section 5

---


## Section 3: 局限性

1. **$O(n^2)$ 复杂度**：Self-Attention 需要计算 $n \times n$ 的注意力矩阵，序列长度翻倍计算量翻 4 倍 → 应对：稀疏注意力（Longformer）、线性注意力（Performer）、Flash Attention（内存优化）
2. **位置编码非天生**：模型本身无位置概念，必须外部注入 → 应对：RoPE（旋转位置编码）比固定正弦波更好地泛化到更长序列
3. **推理速度慢（自回归）**：Decoder 逐 token 生成，无法并行 → 应对：推测解码（Speculative Decoding）、非自回归模型
4. **数据饥渴**：比 LSTM 需要更多数据才能发挥优势 → 应对：预训练+微调范式（BERT/GPT 的大规模预训练解决了这个问题）
5. **计算资源需求大**：大型 Transformer（GPT-4 级）训练成本数千万美元 → 应对：PEFT/LoRA 微调、量化推理

> 📖 Paper: Vaswani et al., Section 6
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.8

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **Transformer** | 完全并行、$O(1)$ 长距离、可扩展 | $O(n^2)$ 内存、需要位置编码 | 中短序列 + 充足算力 |
| **LSTM/GRU** | 内存占用低、天然有序 | 串行计算、长距离衰减 | 在线/流式处理、小数据 |
| **Temporal CNN** | 并行、O(log n) 长距离 | 感受野有限、需要深层 | 音频、时序信号处理 |
| **Mamba (SSM)** | 线性复杂度、处理长序列 | 较新，生态不如 Transformer | 超长序列（>100K）|
| **Sparse Transformer** | 次二次复杂度 | 稀疏模式需要设计 | 长文档、高分辨率图像 |

> 📖 Paper: Vaswani et al., Table 1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.1

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [Vaswani et al. 2017](https://arxiv.org/abs/1706.03762) | 📖 论文 | 全文核心参考 — Transformer 原始论文 |
| [《SLP3》Ch.9-10](../../../textbooks/jurafsky_slp3.pdf) | 📚 教科书 | Section 0-3 — NLP 中的 Transformer |
| [《Deep Learning》Ch.10,12](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | Section 0 — 序列建模基础 |
| [PyTorch nn.Transformer](https://pytorch.org/docs/stable/generated/torch.nn.Transformer.html) | 📖 文档 | Code — 官方实现参考 |
| [Bahdanau et al. 2015](https://arxiv.org/abs/1409.0473) | 📖 论文 | Section 0/Section 2 — 注意力机制先驱 |
