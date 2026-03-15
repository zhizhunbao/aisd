---
topic: transformer
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📚 Book: Jurafsky & Martin, 《SLP3》 Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/jurafsky_slp3.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.10,12 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Transformer 第一性原理

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), NeurIPS 2017
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10,12

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **Transformer 在做什么？** → 将一个序列（如英文句子）映射为另一个序列（如中文翻译），或将序列映射为上下文化的表示向量
2. **为什么要用 Self-Attention 而不是 RNN？** → 因为我们需要**并行计算**和**直接长距离依赖**——RNN 的串行处理在 GPU 时代成为了性能瓶颈
3. **为什么并行性和长距离依赖重要？** → 因为语言中的含义依赖于远距离的上下文（"The cat that sat on the mat by the window chased the mouse" 中 "cat" 和 "chased" 相距很远），而 GPU 有数千核心却被 RNN 闲置
4. **这背后的根基是什么？** → **语言的上下文依赖性**（一个词的含义由其周围的词决定）和 **GPU 的 SIMD 并行架构**（同时处理大量数据才能发挥硬件优势）
5. **这些根基能否继续拆分？** → 不能 → **到达公理**

> 📖 Paper: Vaswani et al., Section 1
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9.1

---


## 公理与基本假设

> 列出 Transformer 赖以成立的**不可再分的基本事实**。这些是"如果它们不成立，整个技术就崩塌"的根基。

### 公理 1: 分布假说（Distributional Hypothesis）

**陈述：** 一个词的含义由其上下文中共同出现的词决定。

**白话：** "Tell me your friends, and I'll tell you who you are"——一个词的意思不是固有的，而是由它经常出现在什么词旁边来定义的。

**来源：** J.R. Firth (1957) "You shall know a word by the company it keeps"。语言学的经验观察，后来被 Word2Vec 等统计方法验证。

**可验证性：** 在绝大多数自然语言中成立。但对专有名词（如 "Elon Musk"）和数字（如 "42"）的含义捕获有局限——这些词的含义更多来自外部世界知识而非分布统计。

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.6
> 📖 Paper: Firth, J.R. (1957). "A Synopsis of Linguistic Theory"

### 公理 2: 全局上下文可及性假设

**陈述：** 对序列中任意位置的正确表示，需要同时访问序列中**所有其他位置**的信息。

**白话：** 要真正理解一个词，你需要看整个句子（甚至整个段落），而不是只看它附近的几个词。

**来源：** 这是 Self-Attention 设计的核心假设。与 RNN（只看历史）和 CNN（只看局部窗口）形成对比。经验证据：BERT 的双向注意力全面超越单向模型；移除注意力的长距离连接会导致性能下降。

**可验证性：** 对大多数 NLP 任务成立。但对于纯局部模式的任务（如字符级别的拼写检查），全局注意力是过度的——局部窗口注意力（如 Longformer 的 sliding window）已经足够。

> 📖 Paper: Vaswani et al., Section 1, Table 1

### 公理 3: 可微分的加权组合假设

**陈述：** 序列中的信息聚合可以通过**可微分的软权重**实现——即 softmax 加权求和。

**白话：** 从多个信息源组合信息的方式是"给每个源打个分，按分数加权平均"，而不是"只取最重要的那个"（hard attention）。

**来源：** 这是使 Transformer 可通过梯度下降训练的关键。softmax 是光滑可微的，使得注意力权重可以通过反向传播学习。来自 Bahdanau et al. 2015 的注意力机制。

**可验证性：** 在连续优化框架下总是成立。但 hard attention（只选 top-1）在某些场景更高效（如检索增强生成中的硬检索步骤），需要 REINFORCE 等策略梯度方法训练。

> 📖 Paper: [Bahdanau et al. 2015](https://arxiv.org/abs/1409.0473)

### 公理 4: 位置信息可加性假设

**陈述：** 序列中 token 的位置信息可以通过**与内容嵌入相加**的方式注入，而不必改变架构。

**白话：** 把"我在哪里"和"我是什么"的信息直接相加，模型就能同时知道词义和位置。

**来源：** Transformer 的设计选择。Self-Attention 本身是置换不变的（permutation invariant），必须外部注入位置信息。选择相加而非拼接是为了保持 $d_{model}$ 维度不变。

**可验证性：** 在原始 Transformer 中有效。但后续研究表明，相加可能导致内容和位置信号互相干扰——RoPE（旋转位置编码）通过旋转变换隐式编码相对位置，表现更好。

> 📖 Paper: Vaswani et al., Section 3.5
> 📖 Paper: [Su et al. "RoFormer", 2021](https://arxiv.org/abs/2104.09864)

---


## 从公理到技术的推导链

> 展示如何**仅从上述公理出发**，一步步逻辑推导出完整的 Transformer 技术方案。

### Step 1: {从公理 1} → 需要上下文化的词表示

**推理：** 因为公理 1（分布假说）成立——词的含义由上下文决定——所以我们不能使用固定的词向量（如 Word2Vec），而需要根据当前上下文动态计算每个词的表示。

**结果：** 需要一种机制，让每个 token 的表示依赖于它所在序列中的其他 token。

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.9

### Step 2: {结合 Step 1 + 公理 2} → 需要全局交互机制

**推理：** Step 1 告诉我们需要上下文化表示，公理 2 告诉我们需要访问**所有**位置。因此，我们需要一种机制让每个位置都能与所有其他位置交互——RNN 太慢（逐步传递），CNN 太局部（固定窗口），我们需要一种 $O(1)$ 直达的全局交互。

**结果：** 设计一种"每个位置直接查看所有其他位置"的机制——Self-Attention。

> 📖 Paper: Vaswani et al., Section 1, Table 1

### Step 3: {结合 Step 2 + 公理 3} → Self-Attention 的具体形式

**推理：** Step 2 要求全局交互，公理 3 要求可微分的软权重聚合。将两者结合：每个位置生成一个 Query（"我在找什么"），用它与所有位置的 Key 计算相似度（点积），通过 softmax 得到可微分的权重，再用这些权重对 Value 加权求和。

**结果：** $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$ — Scaled Dot-Product Attention。

> 📖 Paper: Vaswani et al., Section 3.2.1

### Step 4: {从 Step 3} → Multi-Head Attention

**推理：** 单一的 Attention 只能学习一种交互模式。但语言有多种关系（语法、语义、位置等）。通过独立的投影矩阵并行运行多组 Attention（多个"头"），可以捕获不同类型的关系。

**结果：** Multi-Head Attention — 用 $h$ 组不同的 $W^Q, W^K, W^V$ 并行计算，拼接后合并。

> 📖 Paper: Vaswani et al., Section 3.2.2

### Step 5: {结合 Step 4 + 公理 4} → 完整的 Transformer

**推理：** Step 4 给出了核心的 Multi-Head Self-Attention，但它缺少位置信息（置换不变的）。公理 4 告诉我们位置信息可以通过相加注入。再加上 FFN（逐位置非线性变换）、残差连接（稳定深层训练）、LayerNorm（归一化），就组成了完整的 Transformer 层。堆叠 $N$ 层形成 Encoder/Decoder。

**结果：** 完整的 Transformer 架构 = (Embedding + PE) → N × (Multi-Head Attention + Add&Norm + FFN + Add&Norm) → Output。

> 📖 Paper: Vaswani et al., Figure 1, Section 3

### 推导链全景图

```
公理 1 (分布假说) ─────────────┐
                               ├──→ 需要上下文化表示 ──┐
公理 2 (全局可及性) ────────────┘                       │
                                                       ├──→ Self-Attention ──┐
公理 3 (可微分加权) ───────────────→ 软权重聚合 ────────┘                     │
                                                                            ├──→ Transformer
公理 4 (位置可加性) ───────────────→ 位置编码 ──→ Embedding + PE ────────────┘
```

---


## 如果公理不成立？

> 逐个"拔掉"公理，分析技术会如何崩塌。这揭示了 Transformer 的**真正边界**。

### 公理 1 失效：分布假说不成立

**如果不成立：** 词的含义不由上下文决定——例如在某些高度结构化的形式语言中，每个符号有固定的、上下文无关的含义。

**技术后果：** Self-Attention 会浪费计算——上下文化表示没有必要，因为每个 token 的固定嵌入已经包含了全部信息。

**替代方案：** 使用固定查找表（embedding table）或符号系统（如知识图谱），不需要上下文化。

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3.pdf), Ch.6

### 公理 2 失效：不需要全局上下文

**如果不成立：** 理解每个 token 只需要看局部几个邻居——例如字符级别的拼写纠错，只需看前后 3-5 个字符。

**技术后果：** 全局 Self-Attention 的 $O(n^2)$ 计算是浪费的。局部窗口就够了。

**替代方案：** CNN / Sliding Window Attention（如 Longformer 的 local attention）/ 状态空间模型（Mamba）。

> 📖 Paper: [Beltagy et al. "Longformer", 2020](https://arxiv.org/abs/2004.05150)

### 公理 3 失效：不能用可微分的软权重

**如果不成立：** 信息聚合需要**硬选择**（只选 top-1 源），而不是加权平均——例如在检索增强生成中，从数据库检索最相关的文档是离散操作。

**技术后果：** softmax 加权求和被替换为 argmax 硬选择，不可直接用梯度下降训练注意力权重。

**替代方案：** Hard Attention + REINFORCE 策略梯度；或 Gumbel-Softmax 近似；或将检索步骤与 Transformer 解耦（如 RAG 架构）。

> 📖 Paper: [Lewis et al. "RAG", 2020](https://arxiv.org/abs/2005.11401)

### 公理 4 失效：位置信息不能通过相加注入

**如果不成立：** 内容和位置信号相加后互相干扰，模型无法有效分离两者——当 $d_{model}$ 较小或序列较长时尤其明显。

**技术后果：** 模型在长序列上的位置推理能力下降；无法泛化到训练时未见的序列长度。

**替代方案：** RoPE（旋转位置编码）——通过旋转变换隐式编码相对位置，不直接相加；ALiBi——在注意力分数上加线性偏置。

> 📖 Paper: [Su et al. "RoFormer", 2021](https://arxiv.org/abs/2104.09864)

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------| 
| 分布假说 | 词义由上下文决定 | 自然语言 | Self-Attention 无意义 |
| 全局可及性 | 理解需要看全局 | 长距离依赖的任务 | $O(n^2)$ 是浪费 |
| 可微分加权 | 软权重聚合 | 可梯度训练的场景 | 需要硬选择 + 策略梯度 |
| 位置可加性 | PE 与 embedding 相加 | 序列不太长 | 长序列位置推理失败 |

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.10,12
