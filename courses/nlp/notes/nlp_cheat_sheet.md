# NLP Midterm Cheat Sheet (W1–6)

<!-- ==================== SIDE A ==================== -->

## W1: NLP Overview

- **NLP** = Linguistics × CS × AI，让计算机处理/理解/生成人类语言
- **NLU** = Natural Language Understanding（理解：分类、NER、情感分析）
- **NLG** = Natural Language Generation（生成：翻译、摘要、ChatGPT）
- **AI ⊃ ML ⊃ DL**，NLP 横跨所有层级
- **Turing Test**: 机器对话让人无法分辨它是机器 → 语言是智能基准
- **Structured knowledge**: 表格/数据库，精确 | **Unstructured**: 自由文本，歧义，>80%企业数据
- **7 Applications**: Speech Recognition, Dialogue/Chatbot, Text Classification, Sentiment Analysis, Summarization, QA, Generative AI

**4 Challenges:**

| Challenge | Definition |
|---|---|
| **Ambiguity** | 同一表达多种含义：词汇歧义(bank)、句法歧义(attachment)、指代歧义(pronoun) |
| **Sparsity** | 大多数词极稀有，Zipf's Law: 词频 ∝ 1/排名 |
| **Variation** | 同一含义多种表达：词汇/句法/地域/社会/风格/代际 |
| **Common Knowledge** | 机器缺乏世界常识 |

**3 Approaches**: Heuristics(规则/Regex) → ML(从标注数据学) → DL(学表示+规则)

---

## W2: Text Preprocessing

**Preprocessing Pipeline**: Tokenization → POS/NER → Noise Removal → Normalization

- **Tokenization**: 将连续文本切分为离散 token（词/子词/字符）
- **Noise Removal**: 小写化、去数字/标点/停用词/HTML/URL
- **Stop Words**: 高频低语义词(the, is, at...)，移除以降维
- **Stemming**: 规则砍后缀，快但粗，输出可能非真词 (studying→studi)
- **Lemmatization**: 查词典+词性，慢但准，输出永远真词 (better→good)，需要 POS
- **POS Tagging**: 标注每个词的语法角色 (NN名词, VB动词, JJ形容词, RB副词, DT限定词, PRP代词)
- **NER**: 识别命名实体并分类 (PERSON, LOCATION/GPE, ORGANIZATION, DATE, MONEY)

**Regex Metacharacters:**
`.` 任意字符 | `[]` 字符集 | `[^]` 否定 | `^` 行首 | `$` 行尾
`*` 0+次 | `+` 1+次 | `?` 0或1次 | `{m,n}` m到n次 | `\` 转义 | `|` 或 | `()` 捕获组
`\d`=[0-9] `\w`=[A-Za-z0-9_] `\s`=空白 | 大写取反(\D \W \S)

**Python re**: `match`(仅开头) | `search`(任意位置首个) | `findall`(所有→列表) | `sub`(替换)

---

## W3: Text Vectorization

- **Vector Space Model**: 文本→向量空间中的点，用距离/角度衡量相似度
- **One-Hot Encoding (OHE)**: 每词一个独热向量，极稀疏，无频率，无语义，所有词等距
- **Bag of Words (BOW)**: 统计词频，有频率信息，丢失词序
- **N-Gram**: 连续N个词作为特征，部分恢复词序，特征数V^N爆炸
- **TF-IDF**: 词频×逆文档频率，常见词降权，稀有词升权

### Formulas

**TF-IDF:**
```
TF(t, d) = count(t in d) / total words in d
IDF(t) = log(N / df(t))          N=总文档数, df=包含t的文档数
TF-IDF(t, d) = TF(t, d) × IDF(t)
```
- 每个文档都有的词: IDF=log(1)=0 → 权重为零
- 仅1个文档有的词: IDF=log(N) → 权重最高

**Cosine Similarity:**
```
cos(θ) = (A · B) / (‖A‖ × ‖B‖) = Σaᵢbᵢ / (√Σaᵢ² × √Σbᵢ²)
```
值域: [−1, 1]，1=相同方向，0=正交无关，−1=相反 | 不受文档长度影响

**Euclidean Distance:**
```
d(A, B) = √Σ(aᵢ − bᵢ)²
```
受向量长度（文档长度）影响

**Levenshtein (Edit) Distance:** 将字符串A变为B的最少操作数（插入/删除/替换）

---

## W4: Word Embeddings

- **Distributional Hypothesis**: 出现在相似上下文中的词具有相似含义
- **Word Embedding**: 每词映射为稠密低维向量 (d=50–300)，语义相近→位置接近
- **Word2Vec**: 自监督学习，从上下文学习词向量
  - **CBOW**: 上下文词 → 预测中心词（适合高频词）
  - **Skip-gram**: 中心词 → 预测上下文词（适合低频词）
  - 向量 = 隐藏层权重矩阵的行
- **Negative Sampling (SGNS)**: 将 softmax 多分类 O(V) 简化为二分类 O(k)
- **GloVe**: 全局共现矩阵 + 预测优化，wᵢ·wⱼ ≈ log(共现次数)
- **FastText**: 字符 n-gram 组合，词向量=Σ所有子词向量，解决 OOV
- **Word Analogy**: king − man + woman ≈ queen（向量算术编码语义关系）
- **Static Embedding 缺陷**: 上下文不敏感，一词一向量（"bank"河岸/银行共享同一向量）

<!-- ==================== SIDE B ==================== -->

## W5: Language Models

- **Language Model (LM)**: 给定前文，预测下一个词的概率分布 P(wₜ | w₁...wₜ₋₁)
- **Chain Rule**: P(w₁w₂...wₙ) = P(w₁) × P(w₂|w₁) × P(w₃|w₁w₂) × ...

### N-gram LM
- **Markov Assumption**: 只看前 n−1 个词近似完整历史
```
P(wₜ | wₜ₋ₙ₊₁...wₜ₋₁) = Count(wₜ₋ₙ₊₁...wₜ) / Count(wₜ₋ₙ₊₁...wₜ₋₁)
```
- 局限: 数据稀疏、上下文受限(仅n−1词)、无语义相似性

### Neural Network LM (Fixed-window)
- 输入: 拼接最后n个词的嵌入 → 隐藏层 → softmax 输出词汇表概率
- 改进: 词嵌入捕获语义 | 局限: 仍是固定窗口

### RNN (Recurrent Neural Network)
- **有状态计算**: 隐藏状态 hₜ 跨时间步传递信息
```
hₜ = σ(Wₕ · hₜ₋₁ + Wₑ · eₜ + b)
ŷₜ = softmax(U · hₜ + b₂)
```
- **参数共享**: 同一套权重(Wₕ, Wₑ)在每个时间步重复使用
- **Loss**: J = −(1/T) Σ log P(correct word at t)
- **BPTT** (Backpropagation Through Time): 误差在时间步间反向传播
- ✅ 变长输入、保留顺序、参数共享 | ❌ **梯度消失**: 梯度 ∝ (Wₕ)ᵀ → 0

### LSTM (Long Short-Term Memory)
- **双状态**: hₜ (短期/隐藏状态) + cₜ (长期/细胞状态)
- **三门控制信息流**:
```
Forget gate:  fₜ = σ(W_f · [hₜ₋₁, xₜ] + b_f)
Input gate:   iₜ = σ(W_i · [hₜ₋₁, xₜ] + b_i)
Candidate:    c̃ₜ = tanh(W_c · [hₜ₋₁, xₜ] + b_c)
Cell update:  cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ c̃ₜ       ← 加法，梯度直通
Output gate:  oₜ = σ(W_o · [hₜ₋₁, xₜ] + b_o)
Hidden:       hₜ = oₜ ⊙ tanh(cₜ)
```
- Cell State 通过**加法**传递 → 梯度不衰减 → 解决梯度消失
- **Perplexity (PPL)**: 评估LM，低=预测准，高=困惑

### Evolution
N-gram(统计计数) → FFNN(学嵌入,固定窗口) → RNN(变长记忆) → LSTM(解决梯度消失)

---

## W6: Seq2Seq & Attention

### Bi-LSTM (Bidirectional LSTM)
- 正向LSTM(左→右) + 反向LSTM(右→左)，拼接: hₜ = [h→ₜ ; h←ₜ]
- 每个位置同时拥有左右上下文信息
- ⚠️ 不能用于文本生成（反向需要完整序列，未来词不存在）

### Seq2Seq (Encoder-Decoder)
- **Encoder**: LSTM 读完整个源序列 → 压缩为固定长度向量
- **Decoder**: 以该向量为初始状态，自回归逐步生成目标序列
- **Conditional LM**: P(y₁...yₜ | x₁...xₛ) — 以源序列为条件的语言模型
- **Teacher Forcing** (训练): 解码器输入=真实前一词 | **Autoregressive** (测试): 输入=自己的预测
- **Exposure Bias**: 训练/测试输入不一致 → 错误累积
- ❌ **Information Bottleneck**: 整个源句压缩为单一向量，长句信息丢失

### Attention Mechanism
- 解码器每步动态关注编码器的不同位置，消除瓶颈
```
1. Attention score:   score_i = dot(decoder_state, encoder_state_i)
2. Attention weight:  α = softmax(scores)
3. Context vector:    context = Σ αᵢ × encoder_state_i
4. Output:            [decoder_state ; context] → prediction
```
- ✅ 消除瓶颈 | ✅ 处理长句 | ✅ 可解释性(对齐表) | ✅ 梯度快捷路径
- ❌ 仍基于 RNN 顺序处理，无法并行

### Transformer ("Attention Is All You Need", 2017)
- **Self-Attention**: 每个词同时注意到所有其他词 → 完全并行
- **Positional Encoding**: 显式编码位置信息（替代RNN的隐式顺序）
- O(1) 路径长度: 任意两个位置直接连接
- → **BERT**(仅编码器, 双向, 理解任务) | **GPT**(仅解码器, 自回归, 生成任务)

### Architecture Evolution

| 从 → 到 | 解决的核心问题 |
|---|---|
| 单向LSTM → Bi-LSTM | 方向盲区: 只看左 → 看两边 |
| Bi-LSTM → Seq2Seq | 输入输出长度不同 |
| Seq2Seq → +Attention | 信息瓶颈: 单一向量 → 动态加权所有位置 |
| RNN+Attention → Transformer | 顺序处理 → 完全并行 |

### Five Sequence Architectures
| Type | Input→Output | Example |
|---|---|---|
| One-to-one | Fixed→Fixed | Image classification |
| One-to-many | Fixed→Sequence | Image captioning |
| Many-to-one | Sequence→Fixed | Sentiment analysis |
| Many-to-many (synced) | Seq→Seq (same len) | POS tagging |
| Many-to-many (unsynced) | Seq→Seq (diff len) | Translation (Seq2Seq) |
