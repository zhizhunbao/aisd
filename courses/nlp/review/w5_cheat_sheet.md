# W5: Language Models & RNN/LSTM (语言模型 & 循环神经网络)

## 1. Definitions (定义)

### Text Collection (文本收集)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| NLP Development Life Cycle (NLP开发生命周期) | NLP项目的迭代循环流程：需求→数据收集→预处理→特征提取→建模→评估→部署→改进 | 每个阶段可以回到前面的阶段迭代改进 |
| Web Scraping (网页抓取) | 从网站自动提取数据的技术，常用库包括 Beautiful Soup(HTML解析)、lxml(高速解析)、html5lib(纯Python) | 用 Beautiful Soup 抓取新闻文本做情感分析 |
| X API (Twitter API) | 通过 X 开发者账户访问推文数据的接口，用于收集社交媒体文本 | 抓取推文用于舆情分析 |

### Probability Theory Recap (概率论回顾)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Sampling with Replacement (有放回抽样) | 每次抽取后放回，各次抽取独立；序列概率 = 各个概率的乘积 | 抽到红、蓝、红: P = P(红)×P(蓝)×P(红) |
| Conditional Probability (条件概率) | 在已知某事件发生的前提下另一事件的概率 P(X\|Y) = P(X,Y)/P(Y) | P(rain\|cloudy) = P(rain,cloudy)/P(cloudy) |
| Chain Rule (链式法则) | 联合概率可以分解为条件概率的连乘：P(w1..wn) = P(w1)·P(w2\|w1)·P(w3\|w1,w2)... | 所有语言模型的数学基础 |

### Language Model Concepts (语言模型概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Language Model (语言模型, LM) | 给词序列分配概率的模型，核心任务：预测下一个词 P(wt\|context)，学习文本中的语言模式 | "the students opened their ___" → books (40%), exams (10%), minds (5%) |
| LM Popular Usages (LM应用) | 语言模型广泛应用于自动补全、拼写纠错、机器翻译、语音识别、文本生成等任务 | 手机输入法的下一个词建议 |
| Markov Assumption (马尔可夫假设) | 简化假设：下一个词只依赖前 n-1 个词，而不是全部历史，使计算可行 | Bigram: P(wt\|w1...wt-1) ≈ P(wt\|wt-1) |
| Perplexity (困惑度, PP) | 语言模型的标准评估指标，越低越好；衡量模型预测下一个词时有多"困惑"，按词数归一化 | PP=1 完美预测; PP=V 等于随机猜; PP=50 很好 |

### N-gram Language Model (N-gram 语言模型)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| N-gram LM (N元语法模型) | 基于前 n-1 个词的计数频率统计来预测下一个词的语言模型 | 4-gram: P(books\|students opened their) = 400/1000 = 0.4 |
| Unigram (一元) | N=1，只看单个词的频率，完全不考虑任何上下文 | P("the") = 0.07 (最高频词) |
| Bigram (二元) | N=2，只看前1个词来预测当前词 | P(sat\|cat) = C("cat sat")/C("cat") |
| Data Sparsity (数据稀疏) | N-gram 的核心问题：很多 N-gram 组合在语料中从未出现过，导致概率为0 | "students opened their quantum" → C=0 → P=0 |
| Context Limitations (上下文限制) | N-gram 只能看固定窗口的前 n-1 个词，无法利用更远的上下文信息 | 4-gram 只看3个前词，更远的信息全部丢失 |

### Neural Network Concepts (神经网络概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Perceptron / Neuron (感知器/神经元) | NN 的基本计算单元：输入×权重求和 v=Σ(wj·xj)+b，经激活函数输出 | 多个输入加权求和→激活→输出 |
| FFNN (前馈神经网络) | 信号只向前流动 (输入→隐藏→输出)，固定输入大小，无记忆能力 | 不能处理变长序列 |
| Fixed-window NN LM (固定窗口神经LM) | 用前n-1个词的词嵌入拼接为固定输入，经隐藏层+softmax预测下一个词 | 输入[e1;e2;e3;e4] → h = f(We+b1) → ŷ = softmax(Uh+b2) |
| UAT (通用逼近定理, 1989) | Cybenko 1989年证明：一个足够宽的单隐藏层神经网络可以逼近任何连续函数 | 理论保证NN的表达能力 |
| Sequence Modeling Motivations (序列建模动机) | 处理变长序列、追踪长期依赖、维护顺序信息、在序列中共享信息——4大核心动机 | 评论3词或300词都需要处理 |
| RNN (循环神经网络) | 有自循环连接的网络，能逐步处理变长序列数据，参数在所有时间步共享 | h_t = f(W_h·h_{t-1} + W_e·e_t + b) |
| Hidden State (隐藏状态, h_t) | RNN 在每个时间步的内部记忆，携带前面所有输入的累积信息 | h_3 包含了 w1, w2, w3 的信息 |
| Parameter Sharing (参数共享) | RNN 在每个时间步使用相同的权重矩阵 W_h，参数不随序列长度增加——RNN的关键特性 | 不管句子多长，同一套 W_h 处理每一步 |
| Embedding Layer (嵌入层) | 将词 ID 映射为稠密向量的查找表 e(t)=E·x(t)，在训练中学习 | `Embedding(10000, 100)` → 10K词×100维矩阵 |

### Training Concepts (训练概念)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| Backpropagation (反向传播) | 计算损失对权重的梯度，用于更新参数的核心训练算法 | 每轮训练都用BP调整权重 |
| BPTT (时序反向传播) | RNN 的训练方法：将 RNN 按时间展开后做反向传播，梯度从 t=T 流回 t=1 | 梯度从最后一步沿时间轴反向传播 |
| Learning Rate (学习率) | 控制每次参数更新的步长：太小→收敛慢; 太大→震荡/发散 | lr=0.001 是常见默认值 |
| Softmax (归一化指数) | 把实数向量转成概率分布 (所有值 >0 且总和=1) | [2.0, 1.0, 0.1] → [0.7, 0.2, 0.1] |
| Cross-Entropy Loss (交叉熵损失) | 分类任务的标准损失函数，衡量预测概率分布与真实分布的差异 | categorical→多分类; binary→二分类 |
| Vanishing Gradient (梯度消失) | 梯度在 BPTT 中经过多步乘以 W_h 后指数缩小，导致无法学习长距离依赖 | \|W_h\| < 1 → 梯度 → 0, 无法连接远处的 "tickets" 到预测 |
| Exploding Gradient (梯度爆炸) | 梯度在反向传播中指数增大导致训练不稳定，可用梯度裁剪 (gradient clipping) 解决 | \|W_h\| > 1 → 梯度 → ∞ |

### LSTM (长短期记忆网络, 1997)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------| 
| LSTM (长短期记忆) | Hochreiter & Schmidhuber (1997) 提出的门控 RNN 变体，用加法更新的细胞状态解决梯度消失问题 | 通过细胞状态 + 3个门控制信息流 |
| Cell State (细胞状态, c_t) | LSTM 的长期记忆传送带，用**加法** (非乘法) 更新 → 梯度得以保留而不缩小 | c_t = f_t⊙c_{t-1} **+** i_t⊙c̃_t |
| Hidden State (隐藏状态, h_t) | LSTM 的短期工作记忆，是细胞状态经输出门过滤后的版本 | h_t = o_t ⊙ tanh(c_t) |
| Forget Gate (遗忘门, f_t) | 决定从旧细胞状态中**丢弃**多少信息 (σ: 0=全部遗忘, 1=全部保留) | 读到新话题 → f≈0 → 清除旧记忆 |
| Input Gate (输入门, i_t) | 决定**存储**多少新信息到细胞状态 (σ: 0=忽略, 1=全部写入) | 重要新信息 → i≈1 → 写入细胞 |
| Output Gate (输出门, o_t) | 决定从细胞状态中**输出**多少信息到隐藏状态 | 控制当前时间步暴露多少细胞信息 |
| Candidate (候选值, c̃_t) | 用 tanh 生成的新候选信息 (范围[-1,1])，准备被输入门筛选后写入细胞 | c̃_t = tanh(W_c·[h_{t-1}, x_t] + b_c) |

## 2. Comparisons (对比)

### FFNN vs Fixed-window NN vs RNN (三种LM架构对比)

| Dimension (维度) | FFNN / Fixed-window NN | RNN (循环网络) | Example (示例) |
|-----------|------------|-----------|---------| 
| Input size (输入) | ❌ 固定长度窗口 | ✅ 可变长序列 | FFNN 只能看固定n-1个词 |
| Memory (记忆) | ❌ 无记忆 | ✅ 隐藏状态携带历史信息 | RNN 能记住前面所有词 |
| Parameter sharing (参数共享) | ❌ 每层独立参数 | ✅ 所有时间步共享同一套参数 | RNN 参数不随序列长度增加 |
| Context (上下文) | ❌ 只看窗口内，丢弃更远上下文 | ✅ 理论上看到全部历史 | "not bad" vs "not good" 固定窗口可能混淆 |

### RNN vs LSTM

| Dimension (维度) | RNN (循环网络) | LSTM (长短期记忆) | Example (示例) |
|-----------|-----|------|---------| 
| Long-range deps (长距离依赖) | ❌ 梯度消失 → 无法学习 | ✅ 细胞状态保留信息 | 10步以前的信息: RNN 丢失, LSTM 保留 |
| Gates (门) | 无门控 | 3个门: Forget/Input/Output | 门值 0-1 动态控制信息流 |
| Memory (记忆) | 只有 hidden state (乘法更新) | Cell state (**加法更新**) + hidden state | 加法 = 梯度保留的关键 |
| Training (训练) | BPTT (梯度容易消失) | BPTT (仍用反向传播，但梯度不消失) | LSTM 没有新的训练方法，只是架构不同 |
| Key innovation (关键创新) | — | 细胞状态用**加法**而非乘法 → 梯度可穿越长距离 | c_t = f⊙c + i⊙c̃ (+ 保持梯度流动) |

### N-gram vs Fixed-window NN vs RNN LM (三代语言模型)

| Dimension (维度) | N-gram | Fixed-window NN | RNN LM | Example (示例) |
|-----------|-------|-----|------|---------| 
| Context (上下文) | 前 n-1 个词 (计数) | 前 n-1 个词 (嵌入) | 理论上全部历史 | N-gram=3词; RNN=全部 |
| Data Sparsity (稀疏) | ❌ 严重 (C=0→P=0) | ✅ 嵌入泛化 | ✅ 嵌入泛化 | 未见过的组合: N-gram=0, NN>0 |
| Variable length (变长) | ❌ 固定窗口 | ❌ 固定窗口 | ✅ 任意长度 | 3词或300词评论 |
| Parameters (参数) | O(V^n) | 与窗口大小相关 | 与窗口无关 (共享) | RNN参数不随长度增加 |

### LM Evolution (语言模型演进)

| Generation (代际) | Method (方法) | Limitation (局限) | Example (示例) |
|------------|--------|-----------|---------| 
| Statistical (统计) | N-gram + 马尔可夫 | 数据稀疏，固定上下文长度 | 4-gram 只看3个前词 |
| Fixed-window (固定窗口) | FFNN LM | 仍是固定窗口，丢弃远处上下文 | "not bad" vs "not good" 容易混淆 |
| Neural (神经) | RNN | 梯度消失 → 不能学长距离 | 10步以前的信息丢失 |
| Gated (门控) | LSTM / GRU | ❌ 顺序处理无法并行 | 长序列训练慢 |
| Attention (注意力) | Transformer | O(n²) 内存开销 | GPT, BERT |

## 3. Formulas (公式)

### Probability & Language Model (概率与语言模型公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $P(X \mid Y) = \frac{P(X, Y)}{P(Y)}$ | 条件概率的定义 | P(rain\|cloudy) = P(rain∧cloudy)/P(cloudy) |
| $P(w_1, \dots, w_n) = \prod_{t=1}^{n} P(w_t \mid w_1, \dots, w_{t-1})$ | 链式法则：联合概率 = 条件概率连乘 | 所有语言模型的数学基础 |
| $P(w_t \mid w_1 \dots w_{t-1}) \approx P(w_t \mid w_{t-n+1} \dots w_{t-1})$ | 马尔可夫假设：只看前 n-1 个词近似 | Bigram: P(wt\|全部历史) ≈ P(wt\|wt-1) |
| $P(w_t \mid \text{context}) = \frac{C(\text{context}, w_t)}{C(\text{context})}$ | N-gram 条件概率：计数比 | C("students opened their books")=400, C("students opened their")=1000 → P=0.4 |
| $PP = \left(\prod_{i=1}^{T} \frac{1}{P(w_i)}\right)^{1/T}$ | 困惑度(Perplexity)：越低模型越好，按词数归一化 | PP=1→完美; PP=V→随机; PP=50→很好 |

### Neural LM (神经语言模型公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $e(t) = E \cdot x(t)$ | 嵌入层：one-hot 向量通过嵌入矩阵 E 转为稠密向量 | x(t)=one-hot, E=嵌入矩阵 |
| $h = f(W_e \cdot [e_1;e_2;...;e_n] + b_1)$ | Fixed-window NN：拼接嵌入 → 隐藏层 | 4个词嵌入拼接→隐藏层 |
| $\hat{y} = \text{softmax}(U \cdot h + b_2)$ | 输出层：隐状态映射为词汇表上的概率分布 | softmax 保证概率和为1 |

### RNN Formula (RNN 公式)

| Formula (公式) | Description (说明) | Example (示例) |
|---------|-------------|---------| 
| $h_t = \sigma(W_h \cdot h_{t-1} + W_e \cdot e_t + b)$ | RNN 隐藏状态更新：上一步隐状态 + 当前输入，W_h 每步共享 | W_h 在每个时间步相同 (参数共享) |
| $\hat{y}_t = \text{softmax}(U \cdot h_t + b_2)$ | RNN 输出层：将隐状态映射为词汇表上的概率分布 | softmax 保证所有词概率和=1 |
| $J = \frac{1}{T} \sum_{t} J_t$ | 总损失 = 各时间步交叉熵损失的平均 | 每步 Jₜ = -log P(正确词) |

### LSTM Gate Formulas (LSTM 门控公式)

| Gate (门) | Formula (公式) | Purpose (作用) | Example (示例) |
|------|---------|---------|---------| 
| Forget (遗忘门) | $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$ | 决定丢弃旧信息的比例 | f=0→全忘; f=1→全记 |
| Input (输入门) | $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$ | 决定写入新信息的比例 | i=1→全部写入; i=0→忽略 |
| Candidate (候选) | $\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$ | 生成新候选信息 | tanh 输出范围 [-1,1] |
| Cell update (细胞更新) | $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ | **加法更新** → 梯度保留 | 这是 LSTM 解决梯度消失的核心 |
| Output (输出门) | $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$ | 控制输出多少细胞信息 | o=1→全输出; o=0→屏蔽 |
| Hidden state | $h_t = o_t \odot \tanh(c_t)$ | 过滤后的细胞状态 = 当前时间步最终输出 | 经输出门过滤的细胞信息 |

## 4. Practical / Lab (实战结论)

### 🔑 Key Distinctions (关键区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|-------------|--------|---------| 
| LSTM `units=128` = hidden state size | ≠ embedding size! 是隐藏状态维度，越大容量越大但越慢 | `LSTM(units=64)` → h_t ∈ ℝ^64 |
| `categorical_crossentropy` vs `binary` | categorical = 多分类; binary = 二分类; 选错损失函数 → 结果错 | 5个类 → categorical; 正/负 → binary |
| `Embedding(10000, 100)` = 查找表 | vocab_size × embed_dim 的矩阵，训练中学习，不是固定的 | 10K词 × 100维 = 100万可训练参数 |
| Perplexity: 越低越好 | PP=1 完美; PP=V 随机猜; 实际好的LM通常 PP<100 | PP=50 on V=10K → 远优于随机 |
| Fixed-window NN 的情感分析陷阱 | "The food was good, not bad" vs "The food was bad, not good"——固定窗口可能只看到最后几词导致混淆 | 窗口=4 → "not bad at all" ≈ "not good at all" |
| Keras LSTM 三层结构 | `LSTM(10, input_shape=(TIMESTEPS, FEATURE_LENGTH))` → `Dense(N)` → `Activation('softmax')` | TIMESTEPS=序列长度, FEATURE_LENGTH=每步特征维度 |

### 📊 Lab/Assignment Conclusions (实验结论)

| Conclusion (结论) | Detail (详情) | Example (示例) |
|------------|--------|---------| 
| TF-IDF + LogReg 经常媲美 LSTM | 简单基线永远先试！复杂模型只在长文本/大数据才有明显优势 | TF-IDF:85% vs LSTM:86% → 改善微小但复杂度大增 |
| Word embedding 需要取平均/池化 | 单词向量 ≠ 文档向量，必须用 mean/max 聚合才能用于分类 | doc_vec = mean([vec("I"), vec("love"), vec("NLP")]) |
| LSTM 通过**加法**解决梯度消失 | 细胞状态用 + 不用 ×，梯度可以穿越很长距离不会缩小 | c_t = f⊙c_{t-1} **+** i⊙c̃ → 梯度不缩小 |
| Vanishing Gradient 实际例子 | "...print her tickets...installed toner...printed her ___"——RNN无法连接远处"tickets"到预测 | 信号需穿越多步 → 梯度消失 → RNN预测失败 |

### ⚠️ W5 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------| 
| Perplexity 越高越好? | ❌ Perplexity 越**低**越好！PP=1是完美，PP=V是随机猜 | PP=50 >> PP=500 |
| RNN 能学习长距离依赖? | ❌ RNN 有梯度消失问题，长距离信息会丢失！LSTM 才能 | 10步以前的信息 RNN 学不到 |
| LSTM 用新的训练算法? | ❌ LSTM 仍然用 BPTT (反向传播)！只是架构不同，不是训练方法不同 | 训练方法相同，区别在门控结构 |
| LSTM 细胞状态用乘法更新? | ❌ 用**加法**: c_t = f⊙c + i⊙c̃。加法是保持梯度的关键！ | 乘法→梯度消失; 加法→梯度保留 |
| LSTM units = embedding dim? | ❌ units = hidden state 维度, 和 embedding 维度是两个独立参数 | units=128, embedding_dim=100 → 不同 |
| FFNN 能处理变长序列? | ❌ FFNN 是固定输入大小！RNN 才能处理变长序列 | 评论有3词或300词 → FFNN 无法统一处理 |
| N-gram 可以处理未见过的词组? | ❌ N-gram 依赖计数，未见过的组合 C=0 → P=0 (数据稀疏问题) | "opened their quantum" 从未出现 → 概率=0 |
| Fixed-window NN 解决了上下文限制? | ❌ 仍然是固定窗口！只是用嵌入代替了计数，窗口大小限制依然存在 | "not bad" vs "not good" 仍可能混淆 |
