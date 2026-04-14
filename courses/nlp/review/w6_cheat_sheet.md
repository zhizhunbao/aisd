# W6: Seq2Seq & Attention (序列到序列 & 注意力机制)

## 1. Definitions (定义)

### Recap: N-gram / RNN / LSTM (回顾)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| N-gram LM (N元语法模型) | 基于前 N-1 个词的计数频率来预测下一个词的统计语言模型 (Statistical LM) | Bigram: P("dog"\|"the") = C("the dog")/C("the") |
| RNN (循环神经网络) | 通过隐藏状态 hₜ = f(hₜ₋₁, xₜ) 处理序列数据，每步保留历史信息但有梯度消失问题 | 顺序读取句子，h 从左到右传递前面的信息 |
| LSTM (长短期记忆) | 用门控(遗忘门/输入门/输出门)和**加法**更新的细胞状态解决 RNN 梯度消失问题 (Hochreiter & Schmidhuber, 1997) | 遗忘门决定丢弃多少旧信息；输入门决定写入多少新信息；细胞状态用加法保持梯度 |
| RNN vs LSTM Cell (内部结构) | RNN 只有一个简单 tanh 激活；LSTM 含 forget/input/output gate + cell state 四个交互组件 | RNN=1个tanh层; LSTM=4个交互的门和状态 |

### Bidirectional LSTM (双向 LSTM)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Bi-LSTM (双向LSTM) | 用两个独立的 LSTM 同时从左到右和从右到左读取序列，拼接两个方向的隐藏状态以获得完整上下文 | "terribly exciting" → 需要看到右侧 "exciting" 才知道 "terribly"=非常(正面) |
| Forward LSTM (正向LSTM) | 从左到右处理序列，只携带过去的上下文信息 | "the cat sat" → h₃ 只知道 the, cat, sat |
| Backward LSTM (反向LSTM) | 从右到左处理序列，只携带未来的上下文信息 | "the cat sat" → h₁ 从反向看到了 cat, sat |
| Concatenation (拼接) | Bi-LSTM 的输出是正向和反向隐藏状态的拼接 [h→; h←]，维度翻倍 | LSTM(128) → Bi-LSTM 输出 256 维 |
| Separate Weights (独立权重) | 正向和反向 LSTM 有各自独立的权重矩阵，不共享参数，各自独立训练 | W_forward ≠ W_backward |
| Multi-layer RNN (多层RNN) | 将多层 RNN/LSTM 叠加，第 i 层的输出作为第 i+1 层的输入，更深层学习更抽象的特征 | 3层 LSTM 堆叠 → 高层表示更抽象 |
| `return_sequences` (Keras参数) | True=返回所有时间步输出(Attention需要)；False(默认)=只返回最后一步(分类用) | True: shape(10,256); False: shape(256,) |

### Sequence Problem Types (序列问题类型)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| One-to-One (一对一) | 单输入单输出，不涉及序列处理 | 图像分类：图片 → "cat" |
| One-to-Many (一对多) | 单个输入生成一个序列输出 | 图像描述：图片 → "a cat sitting on mat" |
| Many-to-One (多对一) | 序列输入产生单个输出 (W6 slides 红框高亮此类型) | 情感分析："I love this movie" → Positive |
| Many-to-Many Synced (多对多同步) | 序列输入产生同长度的序列输出 | 词性标注："The cat sat" → "DT NN VBD"；股票预测 |
| Many-to-Many Unsynced (多对多异步) | 序列输入产生不同长度的序列输出，**Seq2Seq 的核心场景** | 机器翻译："je suis" (2词) → "I am" (2词，但可以不同长度) |

### Seq2Seq Architecture (序列到序列架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Seq2Seq (序列到序列) | 用编码器读完输入序列压缩为固定向量，再用解码器从该向量逐步生成输出序列的架构 | "il a m'entarté" → 编码向量 → "he hit me with a pie" |
| Encoder (编码器) | 用 RNN/LSTM 读取整个输入序列，将全部信息压缩为一个固定长度的隐藏状态向量 (Encoder Vector) | 读完 "il a m'entarté" → 产生一个 256 维向量 |
| Decoder (解码器) | 用编码器向量初始化 RNN/LSTM，自回归地逐步生成输出序列，每步输出作为下一步输入 | 向量 → "he" → "hit" → "me" → ... → \<END\> |
| Encoder Vector (编码向量) | 编码器 LSTM 最后一步的隐藏状态，是编码器和解码器之间的**唯一桥梁** | 编码器最终 h → 解码器初始 h |
| Bottleneck (信息瓶颈) | Seq2Seq 的核心缺陷：整个输入序列被压缩到一个固定大小的向量中，长序列必然丢失信息 | 100词句子压成 256维向量 → 细节必然丢失 |
| Conditional LM (条件语言模型) | Seq2Seq 的数学本质——一个以源句子 x 为条件的语言模型，P(yₜ\|y₁...yₜ₋₁, x) | 普通LM: P(y); 条件LM: P(y\|x)——额外依赖源句 |

### Training & Inference (训练与推理)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Teacher Forcing (教师强制) | 训练时给解码器输入**真实的**前一个词(而非模型预测)，让训练快速稳定收敛 | 预测第3个词时，输入真实的第2个词(不管模型猜对没) |
| Auto-regressive (自回归) | 推理时解码器只能用自己之前的**预测**作为输入，因为没有真实目标 | "he"→"like"(错)→"cats" → 错误向后累积 |
| Exposure Bias (暴露偏差) | 训练用真实输入 vs 推理用自身预测的不一致，导致推理时错误像滚雪球一样累积 | 训练时从没见过自己的错误 → 推理时一错到底 |
| End-to-End Training (端到端) | 整个 Encoder+Decoder 作为一个统一系统联合优化，反向传播从解码器穿过编码器 | J = (1/T) Σ Jₜ，一个损失函数优化整个系统 |
| NMT Training Loss (训练损失) | 每个目标词负对数概率 Jₜ = -log P(yₜ\|...) 的平均值 J = (1/T) Σ Jₜ，整体端到端反向传播 | 所有步的交叉熵求均值 → 反向传播 |

### Attention Mechanism (注意力机制)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Attention (注意力) | 解码器在生成每个词时**动态选择性关注**编码器的不同位置，解决信息瓶颈问题的核心技术 | 翻译 "he" 时重点看 "il"; 翻译 "pie" 时重点看 "entarté" |
| Attention = Weighted Average (加权平均) | 注意力的数学本质是对编码器隐藏状态集合的加权平均，权重由解码器-编码器相似度决定 | 权重高=当前最相关位置; 权重低=不太相关位置 |
| Attention Score (注意力分数) | 解码器隐藏状态与每个编码器隐藏状态之间的相似度值，通常用点积 (dot product) 计算 | eᵢ = dec_state^T · enc_stateᵢ → 4个编码器状态产生4个分数 |
| Attention Weight (注意力权重) | 对原始分数做 softmax 得到的概率分布 (和=1)，表示每个编码器位置的重要程度 | α = [0.7, 0.1, 0.1, 0.1] → 主要关注位置1 |
| Context Vector (上下文向量) | 用注意力权重对编码器隐藏状态做加权求和得到的向量，浓缩了"当前步最相关的源句信息" | c = 0.7·h₁ + 0.1·h₂ + 0.1·h₃ + 0.1·h₄ |
| Dot Product Attention (点积注意力) | 用向量点积 (内积) 计算注意力分数的方法，最简单直觉的相似度度量 | score = query^T · key |
| Attention Output (注意力输出) | 将解码器状态和上下文向量拼接后经过全连接层，再通过 softmax 预测输出词 | output = f([dec_state; context]) → softmax → word |

### Transformer Preview (Transformer 预告)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Transformer (变换器, 2017) | 完全依赖自注意力的架构，彻底不需要 RNN，可以全部并行处理序列 ("Attention Is All You Need") | 2017年论文提出 → 催生 GPT, BERT 等所有现代LLM |
| Self-Attention (自注意力) | 序列中每个词**同时关注**序列中所有其他词(包括自己)，而非仅限于 Encoder→Decoder | "it" 直接关注前面的 "cat" 来理解指代，无论距离多远 |
| Positional Encoding (位置编码) | 因为 Transformer 没有循环结构，需要显式加入位置编码向量来告诉模型词的顺序信息 | 给每个位置加一个固定向量，否则模型不知道词序 |
| Transformer Architecture (架构) | 编码器堆栈(Self-Attn + FFN) + 解码器堆栈(Self-Attn + Cross-Attn + FFN)，含多头注意力 | 编码器: Self-Attn→FFN; 解码器: Self-Attn→Cross-Attn→FFN |

## 2. Comparisons (对比)

### Uni-LSTM vs Bi-LSTM (单向 vs 双向)

| Dimension (维度) | Uni-LSTM (单向) | Bi-LSTM (双向) | Example (示例) |
|-----------|-----------------|---------------|---------| 
| Direction (方向) | 只看过去 (→) | 过去 + 未来 (→ + ←) | "terribly" 需要看右侧才能判断正面含义 |
| Output dim (输出维度) | hidden_size | **2** × hidden_size | LSTM(128)=128d; Bi-LSTM(128)=256d |
| Context (上下文) | 只有左侧上下文 | 左右两侧完整上下文 | Bi-LSTM 理解更全面 |
| Generation (生成) | ✅ 可以生成文本 | ❌ 不能生成 (需要未来信息才能运行) | 自回归生成需要从左到右，反向LSTM需要整个序列已存在 |
| Use case (场景) | 文本生成, 语言模型 | 分类, NER, 问答 | 分类用 Bi-LSTM; 生成用 Uni |
| Weights (权重) | 一组权重 | 两组独立权重 (不共享) | W_forward ≠ W_backward |

### Seq2Seq vs Seq2Seq + Attention (有无注意力)

| Dimension (维度) | Seq2Seq (原始) | Seq2Seq + Attention | Example (示例) |
|-----------|-----------------|---------------------|---------| 
| Info path (信息路径) | 仅通过单一固定编码向量 (瓶颈) | 直接访问所有编码器隐藏状态 | 瓶颈 vs 直通道 |
| Long sequences (长序列) | ❌ 信息丢失严重 (>20词急剧退化) | ✅ 无瓶颈，长句也能良好处理 | 100词句子: 原始严重丢信息 |
| Interpretability (可解释性) | ❌ 黑盒，无法知道模型在看什么 | ✅ 注意力权重可视化 = 对齐图 | 能看到翻译每个词时关注了源句哪里 |
| Gradient (梯度) | 只通过 RNN 传播 (长距离梯度弱) | 注意力提供快捷路径 (缓解梯度消失) | 编码器→解码器有直接连接通道 |
| Processing (处理方式) | RNN 顺序处理 | 仍然是 RNN 顺序处理 (不能并行！) | 两者都是 RNN 基础，都不能并行 |
| Cost per step (每步开销) | O(1) — 只用编码向量 | O(n) — 每步看所有编码器状态 | Attention 计算量更大但效果更好 |

### Training vs Inference (训练 vs 推理)

| Phase (阶段) | Input to decoder (解码器输入) | Issue (问题) | Example (示例) |
|-------|-----------------|-------|---------| 
| Training (Teacher Forcing) | 真实的前一个目标词 | 快速稳定收敛 | 真实 "I" → 预测 "love" |
| Inference (Auto-regressive) | 模型自己上一步的预测 | 错误会向后累积 | 预测 "like"(错) → 后续全偏 |
| Gap = Exposure Bias | 训练/推理输入不一致 | 误差像滚雪球越滚越大 | 训练从没见过自己的错误 → 推理时脆弱 |

### RNN Attention vs Self-Attention (编解码注意力 vs 自注意力)

| Dimension (维度) | RNN Attention (本讲重点) | Self-Attention (Transformer) | Example (示例) |
|-----------|---------------|------|---------| 
| Who attends (谁关注谁) | Decoder → Encoder (解码器看编码器) | 每个词 → 所有词 (包括自己) | 翻译对齐 vs 自身序列内部理解 |
| Depends on RNN | ✅ 需要 RNN 作为骨架 | ❌ 完全不需要 RNN | Transformer 完全去掉 RNN |
| Parallel (并行) | ❌ RNN 必须顺序处理 | ✅ 完全并行 | Transformer 训练快得多 |
| Long-range path (长距离) | 需要多步 RNN 传播 | O(1) 路径长度，任意两位置直接连接 | 远处的词也能直接关注 |
| Position info (位置) | 隐式 (RNN 处理顺序自带位置) | 显式 (必须加 Positional Encoding) | 没有循环→必须额外编码位置 |

### 技术演进路线 (Evolution Path)

| From → To | Problem Solved (解决了什么) | Cost (代价) |
|-----------|-------------|----------| 
| 单向LSTM → Bi-LSTM | 方向盲区：只看左边 → 看两边完整上下文 | 不能生成文本；参数翻倍(2n) |
| Bi-LSTM → Seq2Seq | 长度不同：无法处理输入输出不等长 → 编码器+解码器两阶段 | 信息瓶颈(整个句子→一个向量) |
| Seq2Seq → +Attention | 信息瓶颈：一个向量装不下 → 每步动态加权看所有位置 | 仍需 RNN 顺序处理；每步开销 O(n) |
| RNN+Attention → Transformer | 顺序处理：RNN 不能并行 → 自注意力完全并行 | O(n²)内存开销；需要位置编码 |

## 3. Formulas (公式)

### Attention Mechanism 4 Steps (注意力机制4步)

| Step (步骤) | Formula (公式) | Description (说明) | Example (示例) |
|------|---------|-------------|---------| 
| 1. Score (打分) | $e_i = \text{dec\_state}^T \cdot \text{enc\_state}_i$ | 解码器状态与每个编码器状态的点积相似度 | 4个编码器状态 → 4个分数 |
| 2. Normalize (归一化) | $\alpha_i = \text{softmax}(e_i) = \frac{\exp(e_i)}{\sum_j \exp(e_j)}$ | 用 softmax 转为概率分布 (和=1) | [3,1,1,1] → [0.7,0.1,0.1,0.1] |
| 3. Context (上下文) | $\mathbf{c} = \sum_i \alpha_i \cdot \text{enc\_state}_i$ | 用权重对编码器状态做加权求和 | 主要包含高权重位置的信息 |
| 4. Output (输出) | $\text{output} = f([\text{dec\_state}; \mathbf{c}])$ | 拼接解码器状态和上下文向量 → 全连接 → softmax | 拼接后经过全连接层预测目标词 |

### Bi-LSTM Output (Bi-LSTM 输出)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $\mathbf{h}_{bi} = [\overrightarrow{h}; \overleftarrow{h}]$ | 正向和反向隐状态拼接成完整表示 | 每个位置都有左右两侧上下文 |
| $\dim(\mathbf{h}_{bi}) = 2 \times \text{hidden\_size}$ | 输出维度是单向的两倍 | Bi-LSTM(128) 输出 256 维 |

### Conditional LM (条件语言模型公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $P(y_1, \dots, y_T) = \prod_{t=1}^{T} P(y_t \mid y_1, \dots, y_{t-1})$ | 普通语言模型：只依赖已生成的上文 | 无条件自由生成文本 |
| $P(y_1, \dots, y_T \mid x) = \prod_{t=1}^{T} P(y_t \mid y_1, \dots, y_{t-1}, x)$ | 条件语言模型 (Seq2Seq)：额外以源句子 x 为条件 | 翻译时每个词同时依赖已翻译的词和源句 |

### NMT Training Loss (NMT 训练损失)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $J_t = -\log P(y_t \mid y_1, \dots, y_{t-1}, x)$ | 第 t 步的交叉熵损失 (单个目标词的负对数概率) | 目标词 "hit" 的预测概率越高 → Jₜ 越小 |
| $J = \frac{1}{T} \sum_{t=1}^{T} J_t$ | 整个序列的平均损失，端到端反向传播优化此目标 | 所有时间步损失的均值 → 一个标量 → 梯度反传 |

### Attention Step-by-Step Example (注意力分步数值示例)

| Step | Translating "pie" from "il a m' entarté" | Detail |
|------|-------------|--------| 
| Score | e = [0.1, 0.05, 0.02, 0.83] | dot(dec_h, enc_hᵢ)，"entarté" 最相似 |
| Softmax | α ≈ [0.10, 0.09, 0.09, 0.72] | "entarté" 获得最高注意力权重 0.72 |
| Context | c = 0.10·h₁ + 0.09·h₂ + 0.09·h₃ + 0.72·h₄ | 上下文向量主要包含 "entarté" 信息 |
| Output | [dec_h; c] → FC → softmax → "pie" | 拼接后预测出正确的目标词 |

## 4. Practical / Lab (实战结论)

### 🔑 Key Distinctions (关键区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| Bi-LSTM 输出维度 = 2 × hidden_size | `Bidirectional(LSTM(128))` → 输出 256 维，因为正向128+反向128拼接 | hidden=128 → 正向128+反向128=256 |
| `return_sequences=True` vs `False` | True=返回**所有**时间步输出(Attention/Seq2Seq 需要)；False(默认)=只返最后一步(分类用) | True: shape(10,256); False: shape(256,) |
| 正反向 LSTM 有独立权重 | 两个方向不共享参数，各自独立训练不同的权重矩阵 | W_forward ≠ W_backward |
| Attention 权重是动态计算的 | 不是训练学来的固定参数；每个新输入/时间步都通过点积+softmax 重新计算 | 换一个源句子 → 注意力权重完全不同 |
| Seq2Seq 短句好 长句差 | 编码向量容量固定 → 句子越长丢失信息越多(<20词还行; >20词急剧退化) | 加 Attention 后长句也能处理 |
| Bi-LSTM 分类模型三层结构 | Embedding → Bidirectional(LSTM) → Dense(sigmoid)，这是用于分类的标准三层 | `Sequential([Embedding, Bidirectional(LSTM), Dense(1)])` |

### ⚠️ W6 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| Bi-LSTM 可以做文本生成? | ❌ 不能！反向LSTM需要未来上下文(整个序列预先存在) → 无法自回归生成；只能做分类/NER/QA | 生成必须用单向 LSTM |
| Teacher Forcing 在推理时也用? | ❌ 推理时用自回归(模型自己的预测)！Teacher Forcing **只在训练时**用(输入真实的前一个词) | 训练=真实输入; 推理=自身预测 |
| Seq2Seq 没有信息丢失? | ❌ 有！固定长度向量瓶颈 → 长序列严重丢失信息。Attention 才解决这个问题 | 100词→256d向量→信息被压缩丢失 |
| Attention 让 Seq2Seq 可以并行? | ❌ RNN+Attention 仍然是顺序处理！**Transformer** 才能并行 | RNN 必须逐步处理，Attention 没有改变这点 |
| 注意力权重是训练学来的固定参数? | ❌ 注意力权重是动态计算的(点积+softmax)，每个输入/时间步都重新计算，不是固定的网络参数 | 不同输入产生不同的注意力分布 |
| Exposure Bias 是什么? | 训练时总用真实输入 vs 推理时必须用自身预测 → 这个不一致导致推理时错误滚雪球 | 训练从没见过自己的错误 → 推理脆弱 |
| Transformer 仍然需要 RNN? | ❌ Transformer 完全抛弃 RNN，用自注意力+位置编码替代循环结构 | "Attention Is All You Need" = 只需注意力 |
| RNN Attention 和 Self-Attention 一样? | ❌ RNN Attention 是 Decoder→Encoder(跨序列)；Self-Attention 是每个词→每个词(序列内部) | 前者用于翻译对齐；后者用于序列内部理解 |
