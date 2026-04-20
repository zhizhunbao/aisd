# Week 6: 序列到序列模型 (Sequence to Sequence Models - Seq2Seq)

> Source: `lecture_6_W26.pdf`
> Total slides: 50
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程与期中考试 (Lesson Agenda & Midterm)

![Page 1](lecture6_slides_pages/page_001.png)

**CST8507: Natural Language Processing — Week #6: Sequence to Sequence Models (Seq2Seq)** — CST8507自然语言处理，第6周：序列到序列模型

![Page 2](lecture6_slides_pages/page_002.png)

**Lesson Agenda:** — 本节课议程：

- Midterm (week 7) — 期中考试（第7周）
- Bidirectional Long Short Term Memory (Bi-LSTM) — 双向长短时记忆网络
- The encoder-decoder framework — 编码器-解码器框架
- Attention mechanisms — 注意力机制

### 1.1 期中考试信息 (Midterm Information)

![Page 3](lecture6_slides_pages/page_003.png)

**Midterm:** — 期中考试信息：

- Midterm is on Tuesday, Feb. 23, at 2:00 pm. — 期中考试时间：2月23日周二下午2:00
- The exam will consist of 30 questions, including multiple-choice and true/false questions, with no essay questions. — 考试包含30道题，含选择题和判断题，无论述题
- Material includes from week 1 – week 6 — 考试范围：第1-6周
- You will have 60 minutes to complete the exam. — 考试时间60分钟
- The exam is closed book. However, you may bring one cheat sheet: a single letter-size page (8.5 × 11 inches) that may be used on both sides. — 闭卷考试，但允许携带一张单面/双面小抄
- Ensure that you leave a 5 cm by 5 cm space in the top-left corner of each side of your cheat sheet for the proctor's signature. — 小抄左上角需留5cm×5cm空白供监考签名

![Page 4](lecture6_slides_pages/page_004.png)

**Midterm preparation:** — 考前准备：

- Read the instruction before starting your exam. — 开考前阅读说明
- Write your name and ID number on the spaces provided on the questionnaire and Answer sheet. — 在试卷和答题卡上写姓名和学号
- Make sure to have your ID. — 确保携带证件
- Please do not forget to bring your HB pencils and eraser. — 携带HB铅笔和橡皮
- Submit both the questionnaire and the Scantron answer sheet — 提交试卷和答题卡

![Page 5](lecture6_slides_pages/page_005.png)

**How to Prepare:** — 如何准备：

- Lecture summary slides are a good place to start: they don't have all the details, but make sure you understand the details underlying the main points mentioned. — 从课程总结幻灯片开始复习
- Do the labs! Make sure you understand the answers you get. — 做实验！确保理解答案
- Code-Examples demonstrated during the lecture (check lecture materials folder on Brightspace). — 课堂代码示例
- Hybrid work — 混合作业

---

## 2. 回顾：N-gram、RNN与LSTM (Recap: N-gram, RNN & LSTM)

### 2.1 N-gram回顾 (N-gram Recap)

![Page 7](lecture6_slides_pages/page_007.png)

**Recap: N-gram** — 回顾N-gram模型的基本概率计算

> 📖 **图解读笔记：**
> 这张图就两个公式，都在说“用数数的方法预测下一个词”：
> - **Bigram公式** P(w2|w1) = count(w1,w2) / count(w1) → 给定前一个词w1，下一个是w2的概率 = “w1w2连着出现的次数” ÷ “w1总共出现的次数”
> - **Trigram公式** P(w3|w1,w2) = count(w1,w2,w3) / count(w1,w2) → 给定前两个词，第三个词的概率
> - **绿框链式法则** P(w1,w2,w3) = P(w1) × P(w2|w1) × P(w3|w2) → 一个句子的概率 = 每一步条件概率的连乘
> - 底部要点：N越大能看越远，但组合爆炸 → **这就是N-gram的致命伤，引出后面为什么要用RNN**

![Page 8](lecture6_slides_pages/page_008.png)

**Bigram Probability:** — Bigram概率：

- I have a dog whose name is Lucy. I have two cats. They like playing with Lucy. — 示例语料库用于计算Bigram概率

> 📖 **图解读笔记：** 用具体例子演算Bigram
> - P(have|I) = "I have"出现2次 ÷ "I"出现2次 = **1.0**（I后面100%是have）
> - P(two|have) = "have two"出现1次 ÷ "have"出现2次 = **0.5**
> - P(eating|have) = "have eating"出现0次 ÷ "have"出现2次 = **0**（从未出现过！）
> - ⚠️ P=0是个问题：只要语料库里没见过的组合，概率直接归零 → 这就是**数据稀疏问题**

### 2.2 RNN回顾 (RNN Recap)

![Page 9](lecture6_slides_pages/page_009.png)

**Recap: RNN** — 回顾RNN：

- Designed to handle sequential data by maintaining a hidden state that captures information from previous time steps. — 通过维护隐藏状态捕获前一时间步的信息来处理序列数据

> 📖 **图解读笔记：** RNN处理句子 "I called her but she did not ___"
> - **底部彩色小方块** = 每个词的输入（通过 Wx 权重矩阵转成数字向量）
> - **中间大彩块** = 每个时间步的**隐藏状态 h**（通过 Wh 从上一步传来）
> - **箭头方向** = 从左到右，每一步把上一步的隐藏状态 + 当前输入合在一起处理
> - **颜色条纹** = 越往右颜色越多 = 积累了越多前面词的信息。但早期颜色会“褰色” → **梯度消失**，远处的词信息丢失
> - **最右边 "answer"** = 最终输出（预测空格应该是什么词）

### 2.3 LSTM回顾 (LSTM Recap)

![Page 10](lecture6_slides_pages/page_010.png)

**Recap: LSTM** — 回顾LSTM：

- LSTM networks are a type of RNN that can learn long-term dependencies. They use gates (input, forget, and output gates) to control the flow of information, making them effective for tasks requiring memory over long sequences. — LSTM是一种能学习长期依赖的RNN，使用门控（输入门、遗忘门、输出门）控制信息流

> 📖 **图解读笔记（LSTM内部结构）：** 三个输入从左侧进来：旧记忆(Cell State) + 上一步输出(Hidden State) + 当前词(xt)
>
> | 符号 | 名称 | 功能 |
> |---|---|---|
> | σ（左一） | **遗忘门** Forget Gate | 决定“旧记忆中哪些该扔掉”（0=全扔，1=全留） |
> | σ+tanh（中间） | **输入门** Input Gate | σ决定“新信息哪些值得记”，tanh生成“新信息内容” |
> | σ（右边） | **输出门** Output Gate | 决定“记忆中哪些该输出给下一步” |
> | x (×) | 逐元素乘法 | 开关：0x任何=关，1x值=开 |
> | + | 逐元素加法 | 把新信息加到旧记忆上 |
>
> 🔑 **顶部那条橘色横线 = Cell State = 长期记忆高速公路**。它直直穿过整个单元，只被遗忘门擦除一些 + 输入门添加一些 → 这就是LSTM能记住长期信息的关键！

![Page 11](lecture6_slides_pages/page_011.png)

**RNN vs LSTM cell:** Diagram comparing the internal structure of an RNN cell (simple tanh activation) vs an LSTM cell (with forget gate, input gate, cell state, output gate). — RNN单元（简单tanh激活）vs LSTM单元（含遗忘门、输入门、细胞状态、输出门）的内部结构对比图

**RNN与LSTM单元对比图：** 左侧为RNN的简单结构，右侧为LSTM的复杂门控结构。

> 📖 **图解读笔记（RNN vs LSTM对比）：**
>
> | 左边 RNN | 右边 LSTM |
> |---|---|
> | 内部只有一个 **tanh**（简单计算） | 内部有 **σ σ tanh σ**（三个门+一个候选值） |
> | ht-1 + xt → tanh → ht | ht-1 + ct-1 + xt → 三重门控 → ht + ct |
> | 结构简单，记忆力差 | 结构复杂，记忆力强 |
>
> 💡 不用记每条线，只需记：**LSTM比RNN多了一条“记忆高速公路”(Cell State)和三个“水龙头”(门)，能选择记什么、忘什么。**


---

## 3. NLP序列问题类型 (Types of Sequence Problems in NLP)

![Page 12](lecture6_slides_pages/page_012.png)

**Types of Sequence Problems in NLP Task:** Five architectures shown with diagrams — one-to-one (Image classification), one-to-many (Image captioning), many-to-one (Sentimental analysis, highlighted with red box), many-to-many (Stock Market prediction), many-to-many (Translation). Each shows input (red), RNN/LSTM (green), output (blue) blocks. — NLP中的五种序列问题类型，展示了不同的输入输出结构。

**NLP序列问题类型图：** 五种架构 —— 一对一（图像分类）、一对多（图像描述）、多对一（情感分析，红框高亮）、多对多（股票预测）、多对多（翻译）。

> 📖 **图解读笔记：** 每一列从下到上 = 🔴红色输入 → 🟢绿色RNN处理 → 🔵蓝色输出
>
> | 模式 | 输入→输出 | 例子 | 理解 |
> |---|---|---|---|
> | one-to-one | 1→1 | 图像分类 | 不需要RNN |
> | one-to-many | 1→多 | 图像描述 | 一张图→一段话 |
> | many-to-one | 多→1 | 情感分析⭐红框 | 一段话→正/负 |
> | many-to-many(同步) | N→N | 股票预测 | 每天输入对应每天输出 |
> | many-to-many(异步) | N→M | **翻译⭐本周重点** | 读N词→生M词（长度不同！） |
>
> 🔑 红框=上周重点（情感分析）。本周重点=最右边的异步many-to-many=**Seq2Seq翻译**

Ref: http://karpathy.github.io/2015/05/21/rnn-effectiveness/


---

## 4. 双向LSTM (Bidirectional LSTM — Bi-LSTM)

### 4.1 动机 (Motivation)

![Page 13](lecture6_slides_pages/page_013.png)

**Motivation — Bidirectional Long Short-Term Memory (Bi-LSTM):** Example sentence "The movie was terribly exciting!" — the word "terribly" requires BOTH left context ("was") and right context ("exciting") to determine it means "very" (positive) rather than "horrible" (negative). — 动机示例：句子"The movie was terribly exciting!"中，"terribly"需要左右两侧上下文才能判断含义。

**动机示意图：** 仅看左侧上下文，"terribly"看起来像负面词；需要看到右侧的"exciting"才能确定是"非常"（正面）的意思。

> 📖 **图解读笔记（Bi-LSTM动机）：**
> - **左边压缩版：** 一个方块A = 一个RNN单元，输入x_t，输出h_t。循环箭头 = 自己反复调用自己
> - **右边展开版：** 同一个A在不同时间步展开成链：x0→A→h0, x1→A→h1, x2→A→h2...
> - **底部句子：** "The movie was terribly exciting!" → 说明为什么需要**双向**读取：如果只从左往右读到"terribly"，会误以为是负面词
> - 🔑 这张图的重点：**单向RNN只能看到左边的词，看不到右边的，所以会误判** → 这就是为什么需要Bi-LSTM

![Page 14](lecture6_slides_pages/page_014.png)

**Motivation positive — Sentence encoding:** The word "terribly" in "the movie was terribly exciting!" is positive. Forward-only RNN would see "was terribly" and might predict negative sentiment. — 正向RNN只看到"was terribly"可能预测负面情感。

> 📖 **图解读笔记（正向RNN的局限）：**
> - 图中展示了正向RNN从左到右处理句子，到"terribly"时只看到了"The movie was terribly"
> - 没有"exciting"的信息 → 会判断为负面情感 ❌
> - **解决方案：** 再加一个反向RNN，从右到左读，这样到"terribly"时已经看到了"exciting !" → 两个方向拼接 = **Bi-LSTM**

### 4.2 Bi-LSTM架构 (Bi-LSTM Architecture)

![Page 15](lecture6_slides_pages/page_015.png)

**Bi-LSTM architecture:** Three-layer diagram showing: Bottom — Forward RNN processes "the movie was terribly exciting !" left-to-right (red nodes). Middle — Backward RNN processes right-to-left (green nodes). Top — Concatenated hidden states (grey/green nodes) combine both directions. A callout box highlights: "This contextual representation of 'terribly' has both left and right context!" — Bi-LSTM三层架构图。

**Bi-LSTM架构图：** 底层——正向RNN从左到右处理（红色节点）。中层——反向RNN从右到左处理（绿色节点）。顶层——拼接的隐藏状态（灰绿节点）结合两个方向。标注框强调"terribly"的上下文表示包含左右两侧信息。

> 📖 **图解读笔记（Bi-LSTM架构）：** 从下往上读三层：
>
> | 层 | 颜色 | 方向 | 说明 |
> |---|---|---|---|
> | 底层 Forward RNN | 🔴红点 | → 左到右 | 正向读：the → movie → was → terribly → exciting → ! |
> | 中层 Backward RNN | 🟢绿点 | ← 右到左 | 反向读：! → exciting → terribly → was → movie → the |
> | 顶层 Concatenated | 🔴+🟢 | 合并 | 每个位置的正向+反向拼在一起 |
>
> 🔑 蓝框标注的重点：在"terribly"位置，正向已看到"the movie was"（可能偏负面），反向已看到"exciting !"（正面）。**拼在一起** → terribly = "非常"（正面修饰），不是"糟糕”

![Page 16](lecture6_slides_pages/page_016.png)

**Bi-LSTM detailed diagram:** Detailed architecture from deeplearning.ai showing forward and backward LSTM cells with concatenated outputs at each timestep. — 来自deeplearning.ai的Bi-LSTM详细架构图。

> 📖 **图解读笔记（Bi-LSTM数学图）：** 和Page 15一样的东西，但用数学符号画：
> - `→fW` = 正向LSTM单元（从左到右处理）
> - `←fW` = 反向LSTM单元（从右到左处理）
> - `→h<t>` = 正向隐藏状态（已看到t及其左边所有词）
> - `←h<t>` = 反向隐藏状态（已看到t及其右边所有词）
> - `y<t>` = 输出 = 正向+反向**拼接**后得到
>
> 底部关键句："Information flows from the past and from the future **independently**" = 过去和未来的信息**独立地**流入。考试只需理解"两个方向独立计算+最后拼接"的核心思想。

![Page 17](lecture6_slides_pages/page_017.png)

**Bi-LSTM summary diagram:** Compact visualization of bidirectional processing. — Bi-LSTM总结图。

### 4.3 数学表示 (Mathematical Notation)

![Page 18](lecture6_slides_pages/page_018.png)

**Bidirectional RNNs — On timestep t:** — 双向RNN时间步t：

- This is a general notation to mean "compute one forward step of the RNN" – it could be a vanilla, LSTM or GRU computation. — 这是"计算RNN一步前向传播"的通用符号
- Forward RNN and Backward RNN generally have **separate weights** — 正向和反向RNN通常有**独立的权重**
- Concatenated hidden states: We regard this as "the hidden state" of a bidirectional RNN. This is what we pass on to the next parts of the network. — 拼接的隐藏状态被视为双向RNN的"隐藏状态"，传递给网络后续部分

### 4.4 单向LSTM vs Bi-LSTM (Single vs Bi-LSTM)

![Page 19](lecture6_slides_pages/page_019.png)

**Single forward LSTM layer vs Bi-LSTM model:** Side-by-side comparison showing single-direction LSTM (left) and bidirectional LSTM (right) with double the hidden states. — 单向LSTM层（左）与Bi-LSTM模型（右）对比图。

### 4.5 Bi-LSTM分类模型代码 (Bi-LSTM Classification Code)

![Page 20](lecture6_slides_pages/page_020.png)

**Bi-LSTM model Architecture for Classification:** — 用于分类的Bi-LSTM模型架构：

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense

model = Sequential([
    Embedding(input_dim=vocab_size,
              output_dim=embedding_dim,
              input_length=max_len),
    Bidirectional(LSTM(n_lstm)),
    Dense(1, activation='sigmoid')
])
```

### 4.6 多层RNN/LSTM (Multi-layer RNNs/LSTM)

![Page 21](lecture6_slides_pages/page_021.png)

**Multi-layer RNNs/LSTM:** The hidden states from RNN layer i are the inputs to RNN layer i+1. Diagram shows 3 stacked RNN layers processing "the movie was terribly exciting !". — 多层RNN：第i层的隐藏状态是第i+1层的输入。

**多层RNN/LSTM图：** 展示3层叠加的RNN层处理示例句子。

![Page 22](lecture6_slides_pages/page_022.png)

**Multi-layer RNNs continued:** Additional detail on stacking multiple layers. — 多层RNN补充说明。


---

## 5. 序列到序列模型 (Sequence-to-Sequence — Seq2Seq)

### 5.1 Seq2Seq简介 (Introduction to Seq2Seq)

![Page 23](lecture6_slides_pages/page_023.png)

**Types of Sequence Problems:** Same Karpathy diagram again, highlighting the many-to-many (unsynced) architecture — the focus of Seq2Seq. — 再次展示Karpathy的序列问题类型图，强调多对多（异步）架构。

![Page 24](lecture6_slides_pages/page_024.png)

**Introduction to Sequence-to-Sequence (Seq2Seq):** — Seq2Seq简介：

- Seq2Seq is a type of model used to transform one sequence into another sequence. — Seq2Seq将一个序列转换为另一个序列
- Commonly used in tasks where the input and output are sequences of varying lengths. — 常用于输入输出长度不同的任务

### 5.2 编码器-解码器模型 (Encoder-Decoder Model)

![Page 25](lecture6_slides_pages/page_025.png)

**Encoder-Decoder Model — solution to Seq2Seq task:** Left — abstract block diagram: ENCODER receives Input, passes STATE to DECODER, which produces Output. Right — detailed LSTM implementation: Encoder processes x₁, x₂, x₃ through LSTM cells producing h₁, h₂, h₃, final state becomes "Encoder Vector" that initializes Decoder LSTM cells producing y₁, y₂. — 编码器-解码器模型图。

**编码器-解码器模型图：** 左侧为抽象框图（编码器→状态→解码器）。右侧为详细LSTM实现（编码器处理输入序列产生编码向量，初始化解码器生成输出序列）。

> 📖 **图解读笔记（编码器-解码器）：**
>
> **左边简版：** Input → [ENCODER] → STATE → [DECODER] → Output。就这么简单。
>
> **右边详细版（从左到右读）：**
> 1. **编码器（左下）：** x1,x2,x3=输入词 → 经过三个LSTM单元 → h3就是**“Encoder Vector”（编码向量）** —— 整个源句子被压缩成**这一个向量**
> 2. **解码器（右上）：** 用Encoder Vector作为初始状态 → LSTM自回归生成y1,y2
>
> 🔑 **关键理解：编码器和解码器之间只有一根线 = 一个向量。这就是后面“瓶颈问题”的根源。**

Ref: https://pradeep-dhote9.medium.com/seq2seq-encoder-decoder-lstm-model-1a1c9a43bbac

### 5.3 机器翻译作为条件语言模型 (MT as Conditional Language Model)

![Page 26](lecture6_slides_pages/page_026.png)

**Machine Translation (MT):** — 机器翻译：

- The sequence-to-sequence model is an example of a **Conditional Language Model**. — 序列到序列模型是**条件语言模型**的一个例子
- **Language Model:** task is predicting the next word of the target sentence y — 语言模型：预测目标句子的下一个词
- **Conditional:** predictions are also conditioned on the source sentence x — 条件性：预测还以源句子x为条件
- MT directly calculates: Probability of next target word, given target words so far and source sentence x — MT直接计算：给定已有目标词和源句子x，下一个目标词的概率

### 5.4 训练Seq2Seq (Training Seq2Seq)

![Page 27](lecture6_slides_pages/page_027.png)

**Training a Neural Machine Translation system:** Diagram showing end-to-end training: Source sentence "il a m' entarté" → Encoder RNN → Decoder RNN → generates "he hit me with a pie". Loss J = (1/T)Σ Jₜ = sum of negative log probabilities for each target word. Seq2seq is optimized as a single system. Backpropagation operates "end-to-end". — 端到端训练NMT系统的示意图。

**NMT训练图：** 源句子通过编码器RNN处理，解码器RNN逐步生成目标词。损失函数是每个目标词负对数概率的平均值。整个系统端到端优化。

> 📖 **图解读笔记（NMT训练）：** 从下往上读：
> 1. **底部：** 源句子 "il a m' entarte" → 进入红色**编码器RNN**（从左到右读完）
> 2. **中间：** 绿色+蓝色 = **解码器RNN**，接收\<START\>信号开始生成
> 3. **顶部：** 每一步解码器预测一个词，和真实答案对比：J1=-log P("he"), J2=-log P("hit")...
> 4. **总损失** J = (1/T) Σ Jt = 所有步的平均损失
>
> 🔑 底部标注重点：
> - "optimized as a **single system**" = 编码器+解码器**一起训练**，不是分开练
> - "Backpropagation operates **end-to-end**" = 梯度从损失一路传回编码器

### 5.5 测试阶段 (Testing/Inference)

![Page 28](lecture6_slides_pages/page_028.png)

**Neural Machine Translation (Testing):** Diagram showing test-time behavior: Encoder RNN produces an encoding of the source sentence. This provides initial hidden state for Decoder RNN. Decoder RNN is a Language Model that generates target sentence, conditioned on encoding. Note: decoder output is fed in as next step's input (autoregressive). — 测试时行为图。

**NMT测试图：** 编码器RNN生成源句子的编码。此编码提供解码器RNN的初始隐藏状态。解码器是一个条件语言模型，自回归地生成目标句子（上一步输出作为下一步输入）。

### 5.6 瓶颈问题 (Bottleneck Problem)

![Page 29](lecture6_slides_pages/page_029.png)

**Sequence-to-sequence: bottleneck problem:** Same diagram but highlighting the single encoding vector that must capture ALL information about the source sentence. Arrow points to the connection between encoder and decoder labeled "Information bottleneck!" — 展示信息瓶颈问题。

**Seq2Seq瓶颈图：** 与之前相同的架构图，但高亮了编码器与解码器之间的单一编码向量，标注"Information bottleneck!"——这一个向量必须包含源句子的所有信息。

> 📖 **图解读笔记（瓶颈问题 ⭐⭐考试几乎必考）：**
> 看编码器（红色）最后一个方块和解码器（绿色）第一个方块之间——**只有一根线连接**。
>
> 橘色标注说："This needs to capture **ALL** information about the source sentence. Information bottleneck!"
>
> | 如果源句子... | 编码向量（如512维） | 信息丢失？ |
> |---|---|---|
> | 3个词 "I am fine" | 足够表示 | ✅ 不太丢 |
> | 20个词 | 勉强够 | ⚠️ 开始模糊 |
> | 50个词的复杂长句 | 严重不够 | ❌❌ 大量丢失 |
>
> 🔑 **这张图的灵魂：那根橘色线 = 一个向量要装整个句子 = 不可能完美 → 需要注意力机制！**

![Page 30](lecture6_slides_pages/page_030.png)

**Sequence-to-sequence: Limitations** — Seq2Seq的局限性

- Pair of RNN used for translation — 一对RNN用于翻译


---

## 6. 注意力机制 (Attention Mechanism)

### 6.1 注意力的动机与定义 (Motivation & Definition)

![Page 31](lecture6_slides_pages/page_031.png)

**Solution with Attention:** Title slide introducing attention as the solution to the bottleneck problem. — 注意力作为瓶颈问题的解决方案。

![Page 32](lecture6_slides_pages/page_032.png)

**What is attention?** — 什么是注意力？

- Attention is a **weighted average over a set of inputs** — 注意力是输入集合上的**加权平均**
- How should we compute this weighted average? — 如何计算这个加权平均？
  - **Compute** pairwise similarity between **each encoder hidden state** and **decoder hidden state**. — 计算每个编码器隐藏状态与解码器隐藏状态之间的成对相似度
  - **Convert** pairwise similarity scores to probability distribution (using softmax) over encoder hidden states and compute weighted average — 将相似度分数通过softmax转为概率分布，计算加权平均

### 6.2 注意力的优势 (Attention Benefits)

![Page 33](lecture6_slides_pages/page_033.png)

**Attention — Solution to the bottleneck problem:** — 注意力——瓶颈问题的解决方案：

- Benefits: — 优势：
  - ➢ Improved handling of variable-length input sequences. — 改善对变长输入序列的处理
  - ➢ Enhanced modeling of long-range dependencies. — 增强长距离依赖建模
  - ➢ Better performance in tasks where certain parts of the input sequence are more relevant to specific parts of the output sequence. — 在输入特定部分与输出特定部分更相关的任务中表现更好
- Core idea: on each step of the decoder, use direct connection to the encoder to focus on a particular part of the source sequence — 核心思想：解码器每一步都直接连接到编码器，聚焦于源序列的特定部分

### 6.3 注意力分步详解 (Attention Step-by-Step)

![Page 34](lecture6_slides_pages/page_034.png)

**Sequence-to-sequence with attention — Step 1:** Architecture diagram showing: Encoder RNN processes source sentence "il a m' entarté". At decoder \<START\> token, dot product attention scores are computed between decoder hidden state and each encoder hidden state. — 注意力Seq2Seq第1步：编码器处理源句子，解码器\<START\>位置计算注意力分数。

![Page 35](lecture6_slides_pages/page_035.png)

**Step 2: Compute attention scores** — Dot product between decoder state and each encoder state produces raw scores. — 第2步：计算注意力分数。

![Page 36](lecture6_slides_pages/page_036.png)

**Step 3: Apply softmax** — Convert raw scores to probability distribution. — 第3步：对原始分数应用softmax得到概率分布。

![Page 37](lecture6_slides_pages/page_037.png)

**Step 4: Attention distribution** — The softmax output gives an attention distribution over encoder states. — 第4步：softmax输出给出编码器状态上的注意力分布。

![Page 38](lecture6_slides_pages/page_038.png)

**Step 5: Focus on relevant input:** On this decoder timestep, we're mostly focusing on the first encoder hidden state ("he"). Take softmax to turn the scores into a probability distribution. The attention distribution shows high weight on "il" (French for "he"). — 第5步：聚焦相关输入——解码器主要关注第一个编码器隐藏状态（"il"对应"he"）。

**注意力聚焦图：** 在解码"he"时，注意力分布在"il"上给出最高权重。底部标注展示softmax将分数转为概率分布。

> 📖 **图解读笔记（注意力三步曲 ⭐⭐⭐最关键的图）：**
>
> **Step 5 (Page 38) — 聚焦相关输入：** 从下往上四层：
>
> | 层 | 名称 | 这一步在做什么 |
> |---|---|---|
> | 最底层 | **Encoder RNN** | 红色方块 = 编码器已读完"il a m' entarte"，每个位置都有一个隐藏状态 |
> | 第二层 | **Attention scores** | 空心圆 = 解码器当前状态 和 每个编码器状态 做**点积** → 相似度分数 |
> | 第三层 | **Attention distribution** | 小方块 = 通过**softmax**变成概率(0~1，加起来=1) |
> | 最顶层 | 蓝色长条 | = 注意力分布可视化。**"il"位置的条最高** → 最关注"il" |

![Page 39](lecture6_slides_pages/page_039.png)

**Step 6: Compute attention output:** Use the attention distribution to take a weighted sum of the encoder hidden states. The attention output mostly contains information from the hidden states that received high attention. — 第6步：用注意力分布对编码器隐藏状态做加权求和。

**注意力输出图：** 注意力输出主要包含获得高注意力的隐藏状态信息。

> 📖 **Step 6 — 加权求和：** 顶部新增的红色小球 = **Attention output** = 加权求和结果
> ```
> attention_output = 0.72 x h("il") + 0.10 x h("a") + 0.09 x h("m'") + 0.09 x h("entarte")
> ```
> 注意力输出**主要包含**权重高的那个词("il")的信息，其他词的信息也有一点但很少。

![Page 40](lecture6_slides_pages/page_040.png)

**Step 7: Generate output word:** Concatenate attention output with decoder hidden state, then use to compute ŷ₁ as before. Output: "he". — 第7步：拼接注意力输出与解码器隐藏状态，生成输出词"he"。

> 📖 **Step 7 — 生成输出：** 右上角出现了 **y1 = "he"** ！
> 1. 把 **attention output**（红色小球）和 **decoder hidden state**（绿色节点）**拼接**(concatenate)
> 2. 通过输出层 → 预测出 **"he"** ✅
>
> 🔑 **注意力三步总结：** ① dot积算相似度 → ② softmax变概率 → ③ 加权求和得上下文 → ④ 拼接后输出。然后对每个解码步重复此过程！

![Page 41](lecture6_slides_pages/page_041.png)

**Step 8: Next timestep — "hit":** Same process repeats. Attention now focuses on different source words. Output: "hit". — 第8步：重复过程，注意力聚焦不同源词，输出"hit"。

![Page 42](lecture6_slides_pages/page_042.png)

**Step 9: "me":** Attention shifts to "m'" in the source. Output: "me". — 第9步：注意力转向源句的"m'"，输出"me"。

![Page 43](lecture6_slides_pages/page_043.png)

**Step 10: "with":** Attention distributes across relevant source words. Output: "with". — 第10步：输出"with"。

![Page 44](lecture6_slides_pages/page_044.png)

**Step 11: "a":** Output: "a". — 第11步：输出"a"。

![Page 45](lecture6_slides_pages/page_045.png)

**Step 12: "pie":** Attention focuses on "entarté" (French for "pied/pie"). Output: "pie". Full translation complete. — 第12步：注意力聚焦"entarté"，输出"pie"。翻译完成。

### 6.4 注意力机制优势与挑战 (Benefits vs Challenges)

![Page 46](lecture6_slides_pages/page_046.png)

**Attention Mechanism Benefits vs Challenges:** Discussion question — "How does attention address the temporal bottleneck in sequence-to-sequence models?" — 讨论题："注意力如何解决Seq2Seq模型中的时间瓶颈？"


---

## 7. Transformer简介 (Introduction to Transformers)

![Page 47](lecture6_slides_pages/page_047.png)

**Transformers (2017):** Title slide. — Transformer（2017年提出）标题页。

Ref: https://arxiv.org/abs/1706.03762

![Page 48](lecture6_slides_pages/page_048.png)

**What is Transformer:** — 什么是Transformer：

- The Transformer in NLP is a novel architecture that aims to **solve sequence-to-sequence** tasks while handling long-range dependencies with ease. — Transformer是一种旨在解决序列到序列任务同时轻松处理长距离依赖的新型架构
- The Transformer was proposed in the paper **_Attention Is All You Need_**. — Transformer在论文*Attention Is All You Need*中提出
- Relying entirely on **self-attention** to compute representations of its input and output. — 完全依赖**自注意力**计算输入输出的表示

Ref: https://arxiv.org/abs/1706.03762

![Page 49](lecture6_slides_pages/page_049.png)

**Transformer Architecture:** Diagram showing the full Transformer architecture with encoder (left) and decoder (right) stacks, multi-head attention, feed-forward networks, and positional encoding. — Transformer完整架构图。

**Transformer架构图：** 展示完整架构，左侧为编码器堆栈，右侧为解码器堆栈，包含多头注意力、前馈网络和位置编码。

> 📖 **图解读笔记（Transformer架构）：** 这周只是简介，详细讲解在后面的课
>
> **上半部分 = 概念图：**
> - INPUT "Je suis etudiant" → 🔥 THE TRANSFORMER 🔥 → OUTPUT "I am a student"
> - 和Seq2Seq的目标一样——翻译！但内部结构完全不同
>
> **下半部分 = 结构图：**
> - 左边绿色 = **ENCODERS**（编码器堆叠，不再是RNN，而是自注意力层堆叠）
> - 右边粉色 = **DECODERS**（解码器堆叠，也是自注意力层堆叠）
>
> 🔑 这张图只需记住：**Transformer = 编码器+解码器，但内部用自注意力替代了RNN**。详细的等后面的课讲。


---

## 8. 问答环节 (Q&A)

![Page 50](lecture6_slides_pages/page_050.png)

**Q&A** — 问答环节
