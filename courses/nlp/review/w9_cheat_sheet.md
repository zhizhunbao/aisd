# W9: Transformer Architecture (Transformer 架构)

## 1. Definitions (定义)

### Static Embedding Problem (静态嵌入问题)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Static Embedding Problem (静态嵌入问题) | Word2Vec/GloVe 一词一向量，不随上下文变化，无法区分多义词，且有 OOV 和词形盲区 | "bank" 在"river bank"和"bank account"中向量完全相同 |
| Contextual Embedding (上下文嵌入) | 同一个词在不同上下文中生成不同的向量表示，词义由周围词共同决定 | "bank" 在金融语境和河流语境中产生不同向量 |
| Morphological Blindness (词形盲区) | 静态嵌入对词形变化不敏感，run/running/runner 被当做不同词 | "run" vs "running" → Word2Vec 无法关联 |

### Core Transformer Concepts (核心 Transformer 概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Transformer (2017) | Vaswani 等人提出的 "Attention Is All You Need" 架构，完全基于 Self-Attention，不使用 RNN | 论文: arxiv.org/abs/1706.03762 |
| Self-Attention (自注意力) | 每个词向整句所有其他词提问 "谁最能帮助理解我？"，然后按相关性加权聚合信息 | "The cat sat on the mat" → "cat" 关注 "sat" 和 "mat" |
| Query (Q, 查询) | 当前词在问的问题——"我在找什么样的信息？" | Q = x · W_Q; 代表当前词的搜索需求 |
| Key (K, 键) | 每个词提供的标签——"我能提供什么信息？"；与 Q 点乘得到相关性分数 | K = x · W_K; Q·K^T = 相关性分数 |
| Value (V, 值) | 每个词的实际内容——"我的信息是什么？"；按注意力权重加权求和 | V = x · W_V; 高分的 V 贡献更多 |
| Multi-Head Attention (多头注意力) | 多个注意力头并行运行，每个头关注不同类型的关系 (语法/语义/指代)，拼接后投影 | Head1:语法关系; Head2:指代关系; Head3:语义关系 |
| Positional Encoding (位置编码) | 用 sin/cos 函数生成位置向量并加到词嵌入上，因为 Transformer 没有固有的序列顺序 | PE(pos,2i)=sin(pos/10000^(2i/d)); PE(pos,2i+1)=cos(...) |
| Residual Connection (残差连接) | 跳跃连接让每层学习"对输入的增量修正"而非"完全重写"，缓解深层网络退化 | output = x + Sublayer(x) |
| Layer Normalization (层归一化) | 在残差相加后做归一化，稳定训练过程中的数值尺度 | LayerNorm(x + Sublayer(x)) |
| FFN (前馈网络) | 逐位置的两层全连接网络，用 ReLU 激活，增加模型的非线性表达能力 | FFN(Z) = ReLU(ZW₁+b₁)W₂+b₂ |
| Scaled Dot-Product (缩放点积) | 点积分数除以 √d_k 防止高维度下 softmax 饱和导致梯度消失 | d_k=64 → 分数/8; 不缩放 → softmax→[0,0,1,0] |

### Encoder vs Decoder (编码器 vs 解码器)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Encoder (编码器) | 并行处理整个输入序列，双向自注意力，可同时看到所有位置的词 | 输入 "I love NLP" → 三个词同时互相注意 |
| Decoder (解码器) | 自回归地逐词生成输出，使用掩码自注意力，只能看到已生成的词 | 生成 "Je" → "Je aime" → "Je aime NLP" |
| Masked Self-Attention (掩码自注意力) | 解码器中用掩码屏蔽未来位置的词，确保不会偷看还没生成的答案 | 生成第3个词时只能看到位置1和2 |
| Cross-Attention (交叉注意力) | 解码器读取编码器的输出：Q来自解码器，K/V来自编码器，是编解码器之间的桥梁 | 翻译时解码器回看源语言的编码 |
| Final Softmax Layer (最终Softmax层) | 解码器最后一层，在整个词表上输出下一个词的概率分布 | softmax → P("aime")=0.75, P("love")=0.1, ... |

### HuggingFace Ecosystem (HuggingFace 生态)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| HuggingFace Hub (模型仓库) | 共享预训练模型、数据集和演示代码的开源平台 | hub.huggingface.co 上有数万个预训练模型 |
| `pipeline()` (管道API) | 一行代码完成分词+模型推理+解码的快捷接口，支持多种NLP任务 | `pipeline("sentiment-analysis")("I love NLP")` → POSITIVE |
| Transformer Tree of Life (家族树) | Transformer 系列模型的分支和演化：Encoder-only (BERT)、Decoder-only (GPT)、Enc-Dec (T5) | BERT→RoBERTa→ALBERT; GPT→GPT-2→GPT-4 |

## 2. Comparisons (对比)

### RNN vs Transformer

| Dimension (维度) | RNN/LSTM | Transformer | Example (示例) |
|-----------|----------|-------------|---------|
| Processing (处理方式) | 顺序逐步处理 (sequential) | ✅ 完全并行 (fully parallel) | RNN: h₁→h₂→h₃; Transformer: 同时计算 |
| Long-range deps (长距离依赖) | ❌ 梯度消失 | ✅ O(1) 路径长度，任意两词直接连接 | 10步前的信息: RNN丢失, Transformer直接访问 |
| Position info (位置信息) | 隐式 (处理顺序即位置) | 显式 (位置编码 sin/cos) | RNN 不需要额外编码; Transformer 必须加 PE |
| Memory (内存) | O(n) | O(n²) (注意力矩阵) | 长序列Transformer内存开销大 |
| Training speed (训练速度) | 🐢 慢 (无法并行) | ⚡ 快 (GPU并行加速) | Transformer 训练时间可缩短10倍 |

### Encoder Self-Attention vs Decoder Masked Self-Attention

| Dimension (维度) | Encoder (编码器) | Decoder (解码器) | Example (示例) |
|-----------|---------|---------|---------|
| Visibility (可见范围) | 所有位置 (双向) | 仅过去位置 (单向) | Encoder 看整句; Decoder 只看已生成的词 |
| Masking (掩码) | 无掩码 | 未来token被掩码 | Decoder 位置3看不到位置4,5 |
| Purpose (目的) | 全句上下文理解 | 自回归生成 | BERT=Encoder; GPT=Decoder |

### Transformer Encoder vs Decoder Applications (应用场景)

| Dimension (维度) | Encoder-only | Decoder-only | Encoder-Decoder | Example (示例) |
|-----------|-------------|-------------|----------------|---------|
| 代表模型 | BERT | GPT | T5, BART | 每类架构专长不同 |
| 适合任务 | 分类、NER、QA (理解) | 文本生成 (生成) | 翻译、摘要 (理解+生成) | BERT做分类; GPT做写作 |
| 方向性 | 双向 (bidirectional) | 单向 (left→right) | 双向编码+单向解码 | BERT看全句; GPT只看左边 |

### Transformer Challenges (挑战)

| Challenge (挑战) | Description (说明) | Example (示例) |
|-----------|-------------|---------|
| Language coverage (语言覆盖) | 低资源语言训练数据不足，模型表现差 | 英语模型质量远高于冰岛语 |
| Data availability (数据依赖) | 需要海量训练数据才能充分发挥能力 | GPT-3 用了 300B+ tokens 训练 |
| Long documents (长文档) | O(n²) 注意力矩阵内存限制了输入长度 | 512 tokens 是 BERT 的硬限制 |
| Transparency (可解释性) | 注意力头的决策过程难以解释 | 无法清晰解释为何输出某个词 |
| Bias (偏见) | 继承训练数据中的社会偏见和刻板印象 | 性别、种族相关的偏见输出 |

## 3. Formulas (公式)

### Scaled Dot-Product Attention (缩放点积注意力)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V$ | 核心注意力公式：查询与键的点积→缩放→softmax→加权值 | d_k=64, 缩放因子=8 |
| $\sqrt{d_k}$ 缩放 | 防止高维度下点积值过大导致 softmax 饱和/梯度消失 | 不缩放 → scores=1000 → softmax→[0,0,1,0] |

### Attention Computation Steps (注意力计算步骤)

| Step (步骤) | Operation (操作) | Purpose (目的) | Example (示例) |
|------|-----------|---------|---------|
| 1 | $Q \cdot K^T$ | 点积计算原始相关性分数 | "cat" Q · "sat" K = 高分 |
| 2 | $\div \sqrt{d_k}$ | 缩放保证数值稳定性 | 512/8 = 64 (合理范围) |
| 3 | $\text{softmax}(\cdot)$ | 转换为概率权重 (总和=1) | [64, 32, 8] → [0.7, 0.2, 0.1] |
| 4 | $\times V$ | 按权重加权求和各位置的值 | 0.7×V_sat + 0.2×V_on + 0.1×V_mat |

### Multi-Head Attention (多头注意力)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$ | 每个头用不同投影矩阵映射到子空间 | 8个头, d_model=512 → 每头 d_k=64 |
| $\text{MultiHead} = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) \cdot W^O$ | 拼接所有头的输出，再做线性投影 | 8×64=512 → W^O投影回512维 |

### FFN & Add&Norm (前馈网络与残差归一化)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------|
| $\text{FFN}(Z) = \text{ReLU}(ZW_1 + b_1)W_2 + b_2$ | 逐位置的两层前馈网络，提供非线性变换 | 512→2048(ReLU)→512 |
| $\text{Add\&Norm}: \text{LayerNorm}(x + \text{Sublayer}(x))$ | 残差连接 + 层归一化，稳定深层训练 | 每个子层后都做 Add&Norm |

## 4. Practical / Lab (实战结论)

### 🔑 Key Distinctions (关键区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| Encoder (编码器) = 双向并行 | Decoder (解码器) = 掩码自回归 | Encoder 一次看全句; Decoder 逐词生成 |
| √d_k 缩放是**必须的** | 不缩放 → softmax 饱和 → 梯度消失 → 训练失败 | d_k=64 → 分数/8; 不做→scores=1000→softmax单点 |
| Multi-Head = 捕捉**不同类型**的关系 | 每个头关注不同模式 (语法/指代/语义) | Head1: 主谓关系; Head2: 代词-名词指代 |
| Positional Encoding 用 sin/cos | 因为 Transformer **没有固有序列顺序** (不像RNN) | PE(0)≠PE(1)≠PE(2) → 注入位置信息 |
| `pipeline("task")` = HuggingFace 快捷API | 一次调用完成分词+模型推理+解码 | `pipeline("ner")("Steve lives in Ottawa")` → PERSON, GPE |
| Cross-Attention 是编解码器的桥梁 | Q=Decoder, K/V=Encoder; 没有它解码器无法读源序列 | 翻译时: Q="Je", K/V=Encoder("I love NLP")的输出 |

### 📊 Lab 4 Conclusions (实验4结论): DistilBERT Fine-tuning (微调)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| DistilBERT = 97% BERT, 40% 更小, 60% 更快 | 部署的最佳实用权衡 (知识蒸馏产物) | BERT: 110M params vs DistilBERT: 66M params |
| 微调 DistilBERT > TF-IDF + LogReg | 证明上下文嵌入优于词袋模型 | DistilBERT: 91% F1 vs TF-IDF+LogReg: 85% F1 |
| 基线对比是**必须的** | 没有基线对比则无法声称改进 | 表格必须同时展示 baseline 和新模型 |
| 词表裁剪: 44,276 → 25,767 词 | 移除出现≤2次的词提高效率 | "xylophone" 出现1次 → 移除 |
| 必须报告完整评估指标 | Accuracy + Precision + Recall + F1 + Confusion Matrix | 仅报告 Accuracy 会隐藏类别不平衡问题 |

### ⚠️ W9 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| Transformer 有循环结构? | ❌ 完全没有RNN！全部靠 Self-Attention + FFN | Transformer ≠ RNN; 靠注意力并行处理 |
| Decoder 可以看到未来词? | ❌ Masked Self-Attention 屏蔽未来位置; 只能看已生成的词 | 位置3只能看1,2; 不能看4,5 |
| √d_k 缩放可以省略? | ❌ 必须缩放！不缩放 → softmax饱和 → 梯度消失 → 训练崩溃 | d_k=64 → 必须除以8 |
| Transformer 有固有的序列顺序? | ❌ 没有！必须加 Positional Encoding (sin/cos) 注入位置信息 | 不加PE → "I love NLP" = "NLP love I" |
| Multi-Head 的多个头做同样的事? | ❌ 每个头关注不同类型的关系 (语法/语义/指代) | Head1看语法; Head2看语义; Head3看指代 |
| Encoder 和 Decoder 的注意力相同? | ❌ Encoder=双向; Decoder=掩码单向; 还有 Cross-Attention 连接两者 | 三种不同的注意力机制 |
