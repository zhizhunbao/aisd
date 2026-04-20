# W9: Transformer Architecture (Transformer 架构)

## 1. Definitions (定义)

### Static vs Contextual Embeddings (静态 vs 上下文化嵌入)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Static Embedding (静态嵌入) | 一个词无论出现在什么上下文中都只有一个固定向量，训练后不再变化 (word2vec, GloVe) | "bank" 在"去银行"和"河岸"中向量完全相同 |
| Fixed at Training Time (训练后固化) | 静态嵌入一旦训练完成就冻结，推理时不会根据新的上下文调整向量 | word2vec 模型部署后，词向量表就是一张查找表 |
| OOV Problem (未登录词问题) | 训练集中未出现的词无法获得向量表示，模型直接无法处理 | "ChatGPT"(新词) → word2vec 返回 UNK |
| Morphological Blindness (词形盲) | 静态嵌入将同一词根的不同形态视为完全独立的词，无法利用词形变化信息 | "run"、"running"、"runner" 是三个独立向量，无共享 |
| Contextual Embedding (上下文化嵌入) | 同一个词在不同上下文中获得不同的向量表示，词义由周围词动态决定 | "bank" 在金融句中 → 金融向量; 在河流句中 → 自然向量 |

### Self-Attention (自注意力)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Self-Attention (自注意力) | 让序列中每个词同时评估所有其他词的相关性并按权重加权聚合信息的并行机制 | "it was tired" 中 "it" 自动学到关注 "cat"(指代) |
| Query (查询向量 Q) | 表示"我在找什么信息"的向量，由输入词经线性变换 W_Q 得到 | "it" 的 Q 向量代表"谁是我指代的对象？" |
| Key (键向量 K) | 表示"我能提供什么信息"的向量，由输入词经线性变换 W_K 得到 | "cat" 的 K 向量代表"我是一个动物主语" |
| Value (值向量 V) | 表示"我的实际信息内容"的向量，由输入词经线性变换 W_V 得到 | "cat" 的 V 向量承载 "cat" 的语义信息 |
| Attention Score (注意力分数) | Query 与 Key 的点积 Q·K^T，衡量两个词之间的原始相似度 | score("it","cat")=高; score("it","the")=低 |
| Attention Weight (注意力权重) | 对缩放后的分数做 softmax 得到的概率分布 (和=1)，表示各位置的关注程度 | α = [0.02, 0.45, 0.10, ...] → 最关注位置2 |
| Multi-Head Attention (多头注意力) | 同时运行多个独立的注意力头，每个头学习不同类型的关系模式，最后拼接结果 | Head1 关注语法关系; Head2 关注语义关系; Head3 关注位置邻近 |

### Transformer Architecture (Transformer 架构)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Transformer (变换器, 2017) | 完全依赖自注意力的序列架构，彻底抛弃循环和卷积，可全部并行处理 ("Attention Is All You Need") | 2017 年 Vaswani 等人提出 → 催生 GPT, BERT 等 |
| Encoder (编码器) | Transformer 中负责将输入序列编码为上下文化表示的堆叠模块，每层含自注意力+FFN | 6层编码器堆叠，逐层精炼输入表示 |
| Decoder (解码器) | Transformer 中负责自回归生成输出序列的堆叠模块，含掩码自注意力+交叉注意力+FFN | 翻译时逐词生成目标语言 |
| Positional Encoding (位置编码) | 用 sin/cos 函数为每个位置生成唯一的位置向量并与词嵌入相加，给无循环的架构注入顺序信息 | PE(0)=[0,1,0,1]; PE(1)=[0.84,0.54,0.01,1.0] |
| Scaled Dot-Product Attention (缩放点积注意力) | 标准注意力公式 Attention(Q,K,V)=softmax(QK^T/√d_k)V，除以√d_k防止softmax过于尖锐 | d_k=64 → 除以8来稳定梯度 |
| Feed-Forward Network / FFN (前馈网络) | 对每个位置独立做两层线性变换+ReLU: FFN(Z)=ReLU(ZW₁+b₁)W₂+b₂，增加非线性表达力 | 512→2048→512 维度变换 |
| Residual Connection (残差连接) | 将子层输入直接加到子层输出上 output=x+Sublayer(x)，让每层学增量修正而非完全重写 | 梯度可以通过残差路径直接回传 |
| Layer Normalization (层归一化) | 对残差相加后的结果做归一化 LayerNorm(x+Sublayer(x))，稳定训练并加速收敛 | 标准化每一层的激活值分布 |

### Decoder Components (解码器组件)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Masked Self-Attention (掩码自注意力) | 解码器中将未来位置的注意力分数设为 -∞，确保生成时只能看到已生成的历史词 | 生成"love"时只能看"I"，不能偷看"NLP" |
| Cross-Attention (交叉注意力) | 解码器用自己的 Q 去查询编码器的 K 和 V，从源序列提取当前最相关的信息 | 翻译"pie"时通过 Cross-Attn 聚焦源句的"entarté" |
| Softmax Output Layer (Softmax输出层) | 解码器最后一层通过 softmax 在整个词表上输出下一个词的概率分布 | P("he")=0.85, P("she")=0.10, ... → 选 "he" |

### Hugging Face Ecosystem (Hugging Face 生态)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Hugging Face Hub (HF Hub) | 提供预训练模型、数据集和演示代码的共享平台，一站式下载和部署 Transformer 模型 | 数十万模型可通过 `from_pretrained()` 下载 |
| `pipeline()` API (管道API) | Hugging Face 提供的高层 API，一行代码封装分词→推理→后处理的完整流程 | `pipeline("text-classification")(text)` |
| Transformer Tree of Life (Transformer家族树) | Transformer 演化出的三大分支：Encoder-only(BERT)、Decoder-only(GPT)、Encoder-Decoder(T5) | BERT做理解; GPT做生成; T5做翻译/摘要 |

## 2. Comparisons (对比)

### Static Embedding vs Contextual Embedding (静态嵌入 vs 上下文化嵌入)

| Dimension (维度) | Static (word2vec/GloVe) | Contextual (Transformer) | Example (示例) |
|-----------|---|---|---------| 
| 向量是否变化 (Vector change) | ❌ 一个词一个固定向量 | ✅ 同词不同语境不同向量 | "bank"在银行/河岸两句中向量不同 |
| 训练后能否调整 | ❌ 固化不变 | ✅ 推理时动态计算 | 上下文化嵌入每次前向传播重新算 |
| OOV 处理 | ❌ 无法表示未见词 | ✅ 子词分词解决 | "unhappiness"→"un"+"happi"+"ness" |
| 词形利用 | ❌ 词形盲 | ✅ 子词共享信息 | "run"+"ning"共享"run"的信息 |
| 计算成本 | 查表 O(1) | 前向传播 O(n²) | 静态快但弱; 上下文慢但强 |

### Encoder vs Decoder (编码器 vs 解码器)

| Dimension (维度) | Encoder (编码器) | Decoder (解码器) | Example (示例) |
|-----------|---|---|---------| 
| 注意力类型 | 自注意力 (看全部) | 掩码自注意力 + 交叉注意力 | 编码器双向; 解码器只能往左看 |
| 掩码 (Mask) | 无掩码 (全部可见) | 下三角掩码 (屏蔽未来) | 掩码将未来位置设为 -∞ |
| KV 来源 | 全部来自自身输入 | 自注意力来自自身; 交叉注意力KV来自编码器 | Cross-Attn的K,V=编码器输出 |
| 处理方式 | 并行处理整个输入 | 自回归逐步生成 | 编码器一次看完; 解码器逐词输出 |

### Single-Head vs Multi-Head Attention (单头 vs 多头注意力)

| Dimension (维度) | Single-Head (单头) | Multi-Head (多头) | Example (示例) |
|-----------|---|---|---------| 
| 关注模式 | 只能学一种关系 | h 个头同时学 h 种关系 | 语法+语义+位置多维度并行 |
| 表达能力 | 有限 (一份加权) | 丰富 (多份加权拼接) | 8头→8种不同的关注视角 |
| 输出 | 单个 d 维向量 | h 个 d/h 维向量拼接后投影 | 8头×64维=512维→投影回512维 |

### RNN vs Transformer (RNN vs Transformer)

| Dimension (维度) | RNN/LSTM | Transformer | Example (示例) |
|-----------|---|---|---------| 
| 序列处理 | 顺序 (→ 逐步) | 并行 (一次性) | RNN: O(n)步; Transformer: O(1)步 |
| 位置信息 | 隐式 (处理顺序) | 显式 (位置编码) | Transformer 必须加 PE 否则不知词序 |
| 长距离依赖 | 多步传播 (梯度消失) | O(1) 路径长度 | 任意两词直接连接 |
| 并行训练 | ❌ 不能 | ✅ 完全并行 | GPU 利用率: RNN低, Transformer高 |
| 内存复杂度 | O(n) | O(n²) | Transformer 注意力矩阵是 n×n |

### Transformer 三大分支 (Three Branches)

| Dimension (维度) | Encoder-only | Decoder-only | Encoder-Decoder | Example (示例) |
|-----------|---|---|---|---------| 
| 代表模型 | BERT, RoBERTa, ALBERT | GPT, LLaMA, Claude | T5, BART, mT5 | - |
| 注意力方向 | 双向 (看全部) | 单向 (只看左边) | 编码双向, 解码单向 | BERT双向; GPT从左到右 |
| 适合任务 | 理解 (分类/NER/QA) | 生成 (对话/创作) | 翻译/摘要 | 分类用BERT; 聊天用GPT |
| 预训练目标 | MLM (掩码预测) | 下一词预测 | 多种 (Span corruption等) | BERT=[MASK]; GPT=下一词 |

## 3. Formulas (公式)

### Positional Encoding (位置编码公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $PE(pos, 2i) = \sin(pos / 10000^{2i/d})$ | 偶数维度使用正弦函数编码位置信息 | PE(1,0)=sin(1)≈0.8415 |
| $PE(pos, 2i+1) = \cos(pos / 10000^{2i/d})$ | 奇数维度使用余弦函数编码位置信息 | PE(1,1)=cos(1)≈0.5403 |
| $\text{Input} = \text{WordEmbed} + PE$ | 最终输入=词嵌入向量+位置编码向量(逐元素相加) | 语义信息+顺序信息→完整表示 |

### Scaled Dot-Product Attention (缩放点积注意力)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $\text{score} = Q \cdot K^T$ | Query 与 Key 的点积得到原始相似度分数 | 5个词→5×5 的分数矩阵 |
| $\text{scaled} = \frac{Q \cdot K^T}{\sqrt{d_k}}$ | 除以√d_k 控制方差，防止 softmax 过于尖锐导致梯度消失 | d_k=64 → 除以8 |
| $\alpha = \text{softmax}(\frac{Q \cdot K^T}{\sqrt{d_k}})$ | Softmax 将缩放分数转为概率分布(和=1)=注意力权重 | [高,低,低]→[0.8,0.1,0.1] |
| $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$ | 完整的缩放点积注意力公式：权重×Value得到加权输出 | 按权重聚合所有Value的信息 |

### Feed-Forward Network (前馈网络)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $FFN(Z) = \text{ReLU}(Z \cdot W_1 + b_1) \cdot W_2 + b_2$ | 两层线性变换+ReLU激活，对每个位置独立做非线性变换 | 512→2048(ReLU)→512 |

### Residual + LayerNorm (残差+归一化)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $\text{output} = \text{LayerNorm}(x + \text{Sublayer}(x))$ | 残差连接后接层归一化，稳定训练 | x + SelfAttn(x) → LayerNorm |

### PE Calculation Example (位置编码计算实例)

| Word (词) | Position (位置) | Encoding Vector (编码向量) | Detail (计算过程) |
|------|------|----|---|
| "I" | 0 | [0, 1, 0, 1] | sin(0)=0, cos(0)=1, sin(0/100)=0, cos(0/100)=1 |
| "love" | 1 | [0.8415, 0.5403, 0.01, 0.9999] | sin(1)≈0.84, cos(1)≈0.54, sin(0.01)≈0.01, cos(0.01)≈1.0 |
| "NLP" | 2 | [0.9093, -0.4161, 0.02, 0.9998] | sin(2)≈0.91, cos(2)≈-0.42, sin(0.02)≈0.02, cos(0.02)≈1.0 |

## 4. Practical / Lab (实战结论)

### 📊 Hugging Face Pipeline 应用 (实验结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| pipeline() 一行代码完成 NLP 任务 | `pipeline("task_name")` 封装了分词→模型推理→后处理的全部复杂性 | `pipeline("text-classification")(text)` → 情感标签 |
| 文本分类 pipeline | `pipeline("text-classification")` 自动加载默认的情感分类模型 | 输入投诉信 → 输出 NEGATIVE + 置信度 |
| NER pipeline | `pipeline("ner", aggregation_strategy="simple")` 做命名实体识别 | 输入文本 → 识别人名、地名、组织名 |
| QA pipeline | `pipeline("question-answering")` 做抽取式问答 | question + context → 从 context 中提取答案片段 |
| 摘要 pipeline | `pipeline("summarization")` 自动生成文本摘要 | 长文本 → 简短摘要 (可设 max_length) |
| 缩放因子√d_k的工程意义 | 不除以√d_k时softmax会被大数值推向one-hot，梯度几乎为零→训练崩溃 | d=64不缩放: softmax≈[1,0,0,0]; 缩放后: softmax≈[0.4,0.3,0.2,0.1]→梯度健康 |
| 位置编码是加法不是拼接 | PE 与词嵌入逐元素相加(维度不变)，不是拼接(会增加维度)，设计目的是保持模型维度一致 | 512d嵌入+512d PE=512d输入(不是1024d) |

## 5. Exam Traps (考试陷阱)

### ⚠️ Common Traps (常见陷阱)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| Transformer 仍然使用 RNN? | ❌ Transformer 完全抛弃 RNN/LSTM，纯靠自注意力+位置编码。"Attention Is All You Need"=只需注意力 | 没有任何循环结构 |
| 自注意力自带位置信息? | ❌ 自注意力是**集合操作**(对称的)，不区分词序。必须加位置编码(PE)才能知道顺序 | "I love NLP"和"NLP love I"没有PE时结果相同 |
| 位置编码是训练学来的? | 原始 Transformer 用**固定的**sin/cos函数(不学习)。后来 BERT 等用可学习的PE，但本讲用固定PE | sin/cos是预定义的数学公式，不用训练 |
| 缩放点积的√d_k可以省略? | ❌ 不能！d 大时点积方差大→softmax太尖锐→梯度消失。√d_k把方差控制在1附近是训练成功的关键 | d=512不缩放→softmax=[0.99,0.01,...]=梯度=0 |
| 编码器和解码器的注意力一样? | ❌ 编码器用**无掩码**自注意力(双向看全部)；解码器用**掩码**自注意力(只看已生成的)+ **交叉**注意力(看编码器) | 编码器=开卷; 解码器=闭卷+可查编码器 |
| Cross-Attention 的 Q,K,V 都来自解码器? | ❌ **Q 来自解码器**, **K 和 V 来自编码器**输出。这样解码器用自己的"问题"去编码器中"查找"信息 | Q=解码器当前状态; KV=编码器完整输出 |
| 多头注意力只是重复多次同样的注意力? | ❌ 每个头有**独立的** W_Q/W_K/W_V 权重，学到不同的关注模式(语法/语义/位置等) | Head1看语法; Head2看语义→不同角度 |
| FFN 是对整个序列操作的? | ❌ FFN 是 **position-wise** 的——对每个位置独立做相同的变换，位置之间不交互信息 | 位置1和位置3经过完全相同的FFN但独立 |
| Transformer O(n²)比RNN O(n)慢? | 虽然注意力矩阵 O(n²)，但 Transformer 可**完全并行**(GPU一次算完)，实际训练速度远快于RNN的O(n)**顺序**处理 | GPU矩阵乘法: n²并行 >> n串行 |
| BERT 和 GPT 都是完整的 Encoder-Decoder? | ❌ BERT=仅编码器(Encoder-only); GPT=仅解码器(Decoder-only); T5=完整Encoder-Decoder | 三大分支对应不同任务类型 |
| Transformer 没有缺点? | ❌ 五大挑战：语言覆盖↓、数据依赖↑、长文档O(n²)↑、可解释性↓、训练数据偏见→输出偏见 | 语言不均衡+不透明+偏见=现实问题 |
