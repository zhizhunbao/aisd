---
topic: transformer
dimension: first_principles
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Vaswani et al., 'Attention Is All You Need', NeurIPS 2017 — https://arxiv.org/abs/1706.03762"
  - "📖 Paper: Yun et al., 'Are Transformers universal approximators of sequence-to-sequence functions?', ICLR 2020 — https://arxiv.org/abs/1912.10077"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.9 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📚 Book: Goodfellow et al., 《Deep Learning》, Ch.6,10 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Transformer 第一性原理

> 📖 Paper: Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
> 📖 Paper: Yun et al., [Are Transformers Universal Approximators?](https://arxiv.org/abs/1912.10077), ICLR 2020
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## 核心问题链

> 用"5 个为什么"递归追问，从表层功能到不可再分公理。

1. **Transformer 在做什么？** → 接收一个 token 序列，输出每个位置的上下文感知表示——本质是一个序列到序列的函数
2. **为什么要做上下文感知表示？** → 同一个词在不同语境中含义不同（"bank"= 银行 or 河岸），必须融合上下文才能消歧
3. **为什么用注意力做上下文融合？** → 每个位置直接"看到"所有其他位置（O(1) 路径长度），比 RNN 的逐步传递（O(n) 路径）更高效、信息损失更少
4. **为什么注意力能工作？** → 因为点积可以度量向量相似度——两个向量越相似点积越大，softmax 后权重越高，相关信息被更多地融合进来
5. **能否继续拆分？** → 不能——**点积度量相似度**和**softmax 归一化为概率**是两个数学原子操作 → **到达公理**

---

## 公理与基本假设

### 公理 1: 点积度量相似度

**陈述：** 两个向量的点积 $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\|\mathbf{b}\|\cos\theta$ 是方向相似度的度量。方向越近（$\cos\theta$ 越大），点积越大。

**白话：** 两个向量指向同一方向，它们的点积就大；指向相反方向，点积就小（负）。Transformer 用这个性质来衡量"两个词有多相关"。

**来源：** 线性代数基本定理——内积空间的几何性质。

**可验证性：** 当向量分量独立同分布（如随机初始化的嵌入）且维度 d 足够大时，随机向量对的点积趋近于 0（不相关）。经过训练后，语义相关的词的 Q/K 向量点积会显著偏离 0。失效条件：向量长度差异极大时，点积受长度影响大于方向影响——这就是为什么 Transformer 用了缩放（除以 √d_k）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.2 "Linear Algebra"

### 公理 2: Softmax 归一化为概率分布

**陈述：** $\text{softmax}(z_i) = e^{z_i} / \sum_j e^{z_j}$ 将任意实数向量映射为非负、和为 1 的概率分布。

**白话：** 不管输入是什么数字，softmax 都能把它们变成"百分比"——最大的数得到最大的份额。

**来源：** 指数函数的正性 + 归一化 → Boltzmann 分布。信息论/统计力学基础。

**可验证性：** 永远成立（指数函数永远为正，和永远非零）。但当输入值差异极大时，输出趋近于 one-hot（一个接近 1，其他接近 0），梯度消失。这就是为什么需要缩放——公理 1 和公理 2 的交互产生了"缩放"的必要性。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2 "Softmax"

### 公理 3: 线性变换可以学习任意特征投影

**陈述：** 给定足够大的权重矩阵 W，线性变换 $y = Wx$ 可以将输入投影到任意方向——即可以学习提取输入的任意线性特征。

**白话：** Q = xW^Q 这一步，就是让模型选择"从这个词里提取什么信息作为搜索词（Query）"。不同的 W^Q 提取不同的"看法"。

**来源：** 线性代数——矩阵乘法 = 线性变换 = 基变换。

**可验证性：** 当输入维度 ≥ 输出维度时，线性变换可以保留全部信息（满秩时可逆）。当输出维度 < 输入维度时是有损投影——但这恰好是"注意力头"设计的目的：每个头只看 64 维（而非全部 512 维），强制每个头学不同的关注角度。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.2

### 公理 4: 残差连接保证信息不丢失

**陈述：** $y = x + f(x)$ 的梯度 $\partial y/\partial x = I + \partial f/\partial x$，恒等映射 I 保证梯度至少等于 1，不会因层数加深而消失。

**白话：** 不管中间层学了什么，原始信息总有一条"高速公路"直接传过去。就算某一层完全学坏了（f(x) ≈ 0），输出还是等于输入——不会更差。

**来源：** He et al., Deep Residual Learning (2016)。梯度流动分析。

**可验证性：** 只要 f(x) 的梯度不恰好等于 -I（极端情况），残差连接就能保证梯度流通。深层 Transformer（如 96 层 GPT-3）能训练的核心原因。

> 📖 Paper: He et al., [Deep Residual Learning](https://arxiv.org/abs/1512.03385), CVPR 2016

### 公理 5: 序列的统计规律性（分布假说）

**陈述：** 自然语言中，一个词的含义由它出现的上下文决定——"You shall know a word by the company it keeps" (Firth 1957)。

**白话：** 经常和"银行"一起出现的词（存款、贷款、利率）定义了"银行"的含义。Transformer 用 Self-Attention 捕获这种共现关系。

**来源：** Firth (1957) 分布假说，Harris (1954) 分布语义学。

**可验证性：** 在自然语言上广泛验证（Word2Vec, GloVe 等都基于此假说）。但对非语言序列（如随机生成的 token 序列），这个假设不成立——Transformer 仍然可以过拟合训练数据，但泛化能力会崩塌。

> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 "Vector Semantics"

---

## 从公理到技术的推导链

### Step 1: 从公理 5（分布假说）出发 → 需要上下文信号

**推理：** 如果词义由上下文决定，那模型必须能"看到"上下文——需要某种机制让每个位置获取其他位置的信息。

**结果：** 需要一种"上下文融合操作"。

### Step 2: 从公理 1（点积相似度）出发 → 用相似度决定"关注谁"

**推理：** 因为点积可以度量相似度，而相似的词更可能在语义上相关，所以用 Q·K 的点积来计算"注意力分数"。

**结果：** $\text{score}(i, j) = \mathbf{q}_i \cdot \mathbf{k}_j$ — 原始注意力分数。

### Step 3: 从公理 2（Softmax 归一化）出发 → 分数变概率

**推理：** 原始分数是任意实数，需要变成"百分比"才能做加权求和。Softmax 满足这个需求。

**结果：** $\alpha_{ij} = \text{softmax}(\text{score}(i, j))$ — 注意力权重。

### Step 4: 从公理 1+2 的交互 → 需要缩放

**推理：** 当 d_k 很大时，Q·K 点积方差 = d_k，值太大导致 softmax 饱和。除以 √d_k 让方差回到 1。

**结果：** Scaled Dot-Product Attention: $\text{softmax}(QK^T / \sqrt{d_k})V$。

### Step 5: 从公理 3（线性变换学特征）出发 → Q/K/V 投影 + 多头

**推理：** 不同的 W^Q 可以提取不同的"查询角度"。一个投影太少——用 h 个不同投影（多头），学 h 种关注模式。

**结果：** Multi-Head Attention。

### Step 6: 从公理 4（残差连接）出发 → 深层堆叠

**推理：** 残差连接保证梯度不消失，可以安全堆叠 N 层。每层交替做"注意力"（上下文融合）和"FFN"（特征变换）。

**结果：** 完整的 Transformer = N × (Multi-Head Attention + FFN)，残差 + LayerNorm 包裹每个子层。

### 推导链全景图

```
公理 5 (分布假说)           → 需要上下文融合
          │
公理 1 (点积=相似度)         → Q·K 计算注意力分数
          │
公理 2 (softmax=概率)       → 分数归一化为权重
          │
公理 1+2 (方差爆炸)         → 除以 √d_k 缩放
          │
公理 3 (线性可学特征)        → W^Q/W^K/W^V 投影 + 多头
          │
公理 4 (残差保梯度)          → N 层堆叠，深层不崩
          │
          ▼
    ┌─────────────┐
    │  Transformer  │
    └─────────────┘
```

---

## 如果公理不成立？

### 公理 1 失效：点积不等于语义相似度

**如果不成立：** 在高维空间中，随机向量倾向于近似正交——如果 Q/K 向量没有经过充分训练，点积接近于 0，注意力权重趋于均匀分布。

**技术后果：** 注意力退化为"平均池化"——每个位置等权重地混合所有信息，失去选择性。

**替代方案：** Additive Attention（用前馈网络代替点积计算相似度）、Cosine Similarity Attention（先归一化向量长度再点积）。

### 公理 2 失效：Softmax 饱和

**如果不成立：** 输入值过大时，softmax 输出趋近 one-hot，梯度消失。

**技术后果：** 模型只关注"最相关"的一个位置，忽略其他所有位置——信息过度集中。

**替代方案：** 温度缩放（除以 temperature T）、Sparsemax（稀疏但不完全 one-hot）、Sigmoid Attention（不归一化）。

### 公理 3 失效：线性变换表达力不足

**如果不成立：** 当 d_k 设置太小（如 d_k=2），投影后的空间太窄，无法区分不同的语义关系。

**技术后果：** 多个不同的头学到近似相同的注意力模式——"冗余头"。

**替代方案：** 增大 d_k（但增加计算量）、Head Pruning（剪掉冗余头）。

### 公理 4 失效：残差连接失效（极深网络）

**如果不成立：** 当层数极多（>100）且每层权重初始化不当，残差连接的 $I + \partial f/\partial x$ 中 $\partial f/\partial x$ 趋近 -I，梯度仍可能消失。

**技术后果：** 深层的贡献趋于零，模型实际有效深度远小于名义深度。

**替代方案：** Pre-LN（先归一化再算子层）、DeepNorm（微软提出的深层归一化方案）。

### 公理 5 失效：输入不满足分布假说

**如果不成立：** 对随机 token 序列、加密文本、或完全无规律的序列，上下文不含语义信息。

**技术后果：** 模型可以过拟合训练数据但无法泛化——注意力学到的模式是虚假相关。

**替代方案：** 对非语言模态（图像、音频），需要额外的归纳偏置（如 ViT 的 patch 切分、CNN 的局部先验）。

---

## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------| 
| 点积=相似度 | 方向越近点积越大 | 向量经过训练、维度够大 | 注意力退化为均匀分布 |
| Softmax=概率 | 实数→非负和为1 | 输入值不极端 | softmax 饱和，梯度消失 |
| 线性可学特征 | Wx 可投影到任意方向 | d_k 够大、数据足够 | 多头冗余，学到相同模式 |
| 残差保梯度 | y=x+f(x) 梯度≥1 | 层数不极端、初始化合理 | 深层贡献归零 |
| 分布假说 | 词义=上下文 | 自然语言、有规律的序列 | 过拟合无泛化 |
