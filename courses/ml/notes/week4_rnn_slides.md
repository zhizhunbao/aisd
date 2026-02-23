# Week 4: 循环神经网络 (Recurrent Neural Networks)

> Source: `04_CST8506_RNN.pdf`
> Total slides: 38
> Instructor: Dr. Abbas Akkasi | Winter 2025

---

## 1. 前馈网络回顾 (Review of Feed Forward Networks)

![Page 3](week4_rnn_slides_pages/page_003.png)

**Review on Feed Forward Network:** This slide shows the basic FNN architecture with arrows pointing in one direction only (input → hidden → output). No loops or cycles exist in the network.

**前馈网络回顾：** 这张幻灯片展示了基本的FNN架构，箭头只指向一个方向（输入 → 隐藏层 → 输出）。网络中不存在循环。

- Information flows only in the **forward direction**. No cycles or Loops. — 信息仅沿**前向方向**流动。没有循环或回路。
- Decisions are based on **current input**, no memory about the past — 决策仅基于**当前输入**，没有关于过去的记忆
- Doesn't know how to handle **sequential data** — 不知道如何处理**序列数据**

> **📝 Notes:**
>
> **📌 What:**
> **(1) Feed Forward Network, FFN (前馈网络):**
>
> A neural network where connections between nodes do NOT form a cycle. Information moves in only one direction: from input nodes, through hidden nodes, to output nodes.
>
> > 一种神经网络，节点之间的连接不形成循环。信息只朝一个方向移动：从输入节点，经过隐藏节点，到输出节点。
>
> **(2) Memoryless architecture (无记忆架构):**
>
> Each input is processed independently. If you feed the same input twice, you get the exact same output — the network has no "memory" of previous inputs.
>
> > 每个输入都是独立处理的。如果你输入相同的数据两次，你会得到完全相同的输出 — 网络没有对先前输入的"记忆"。
>
> **🎯 Why:**
> **(1) Why is memorylessness a problem? (为什么无记忆是问题？):**
>
> Many real-world tasks depend on context: "I grew up in France... I speak fluent \_\_\_". The answer "French" depends on remembering "France" from earlier. FFN cannot do this.
>
> > 许多现实任务依赖上下文："我在法国长大...我说流利的\_\_\_"。答案"法语"取决于记住之前的"法国"。FFN做不到这一点。
>
> **(2) Why does FFN fail on sequences? (FFN为什么处理不了序列？):**
>
> FFN treats each time step independently. It cannot learn that the word at position 5 depends on the word at position 1. For time series, it sees today's stock price but ignores yesterday's trend.
>
> > FFN独立处理每个时间步。它无法学习位置5的词依赖于位置1的词。对于时间序列，它看到今天的股价但忽略昨天的趋势。
>
> **⚖️ Compare:**
> **(1) FFN vs RNN:**
>
> | Feature        | FFN                  | RNN                           |
> | -------------- | -------------------- | ----------------------------- |
> | Memory         | None                 | Hidden state stores past info |
> | Input type     | Fixed-size           | Sequential, variable length   |
> | Time awareness | No                   | Yes, processes step by step   |
> | Use cases      | Image classification | Text, speech, time series     |
>
> > | 特性     | FFN      | RNN                  |
> > | -------- | -------- | -------------------- |
> > | 记忆     | 无       | 隐藏状态存储过去信息 |
> > | 输入类型 | 固定大小 | 序列，可变长度       |
> > | 时间感知 | 否       | 是，逐步处理         |
> > | 使用场景 | 图像分类 | 文本、语音、时间序列 |
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Why can't FFN process sequential data?" → Because it has no memory mechanism; each input is processed independently without context from previous inputs.
>
> > "FFN为什么不能处理序列数据？" → 因为它没有记忆机制；每个输入都是独立处理的，没有来自先前输入的上下文。

---

## 2. 动机 (Motivation)

![Page 4](week4_rnn_slides_pages/page_004.png)

**Questions slide:** Lists real-world applications that require understanding sequences, including autocomplete, translation, speech recognition, music generation, and price prediction.

**问题幻灯片：** 列出了需要理解序列的现实应用，包括自动补全、翻译、语音识别、音乐生成和价格预测。

**Questions:**

- How Google's autocomplete feature predicts the **next word** when a user is typing? — Google的自动补全功能如何在用户打字时预测**下一个词**？
- How Translators converting sentences from **English to French**? — 翻译器如何将句子从**英语转换为法语**？
- How Siri or Google Assistant converting **spoken words into text**? — Siri或Google助手如何将**语音转换为文本**？
- How AI composes **melodies** or generates background music? — AI如何创作**旋律**或生成背景音乐？
- How it is possible to predict the **future prices** based on historical trends? — 如何基于历史趋势预测**未来价格**？

![Page 5](week4_rnn_slides_pages/page_005.png)

**Solution slide:** Introduces RNN as the solution to sequential data processing, highlighting the need for memory.

**解决方案幻灯片：** 将RNN作为序列数据处理的解决方案，强调对记忆的需求。

**We need a model:**

- To handle **sequential data** — 处理**序列数据**
- Able to consider the **current input** also the **previously received inputs** — 能够考虑**当前输入**以及**之前接收的输入**
- Able to **memorize history** in its internal memory — 能够在内部记忆中**记住历史**

**FFNs cannot process the sequential data!**

**What is the solution? Recurrent Neural Networks (RNNs)**

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Why memory matters (为什么记忆重要):**
>
> Language, music, and time series all have **temporal dependencies**. The meaning of "it" in "The cat sat on the mat. It was comfortable." depends on remembering "cat" from the previous sentence.
>
> > 语言、音乐和时间序列都有**时间依赖性**。"猫坐在垫子上。它很舒服。"中"它"的意思取决于记住上一句的"猫"。
>
> **(2) Why sequence order matters (为什么序列顺序重要):**
>
> "Dog bites man" vs "Man bites dog" — same words, different order, completely different meaning. Models must understand that word order changes semantics.
>
> > "狗咬人" vs "人咬狗" — 相同的词，不同的顺序，完全不同的意思。模型必须理解词序改变语义。
>
> **💡 Intuition:**
> **(1) The conversation analogy (对话类比):**
>
> Imagine having a conversation but forgetting everything after each sentence. You couldn't follow a story or answer follow-up questions. FFNs are like this — goldfish memory.
>
> > 想象进行对话但每句话后都忘记一切。你无法跟随故事或回答后续问题。FFN就是这样 — 金鱼记忆。
>
> **(2) The movie analogy (电影类比):**
>
> Understanding a movie requires remembering earlier scenes. If you only see one frame at a time with no memory, the plot makes no sense. RNNs "remember" earlier frames.
>
> > 理解电影需要记住早期场景。如果你一次只看一帧且没有记忆，剧情就没有意义。RNN"记住"早期帧。
>
> **📝 Exam:**
> **(1) 列举题 (List examples):**
>
> "Give 3 applications of RNNs." → Speech recognition, machine translation, time series forecasting, sentiment analysis, music generation.
>
> > "举出3个RNN的应用。" → 语音识别、机器翻译、时间序列预测、情感分析、音乐生成。

---

## 3. 序列数据应用 (Usages of Sequence Data)

![Page 6](week4_rnn_slides_pages/page_006.png)

**Examples slide:** Shows six common applications of sequence models with brief descriptions.

**示例幻灯片：** 展示了序列模型的六个常见应用及简要描述。

**Examples:**

- **Speech recognition** (audio clip to text) — **语音识别**（音频片段转文本）
- **Sentiment analysis** (sequence of text to number of stars) — **情感分析**（文本序列转星级评分）
- **DNA Sequence analysis** — **DNA序列分析**
- **Machine translation** (sequence of text in one language translated to another) — **机器翻译**（一种语言的文本序列翻译成另一种语言）
- **Video activity recognition** (detect the activity from a sequence of video frames) — **视频活动识别**（从视频帧序列中检测活动）
- **Time Series Forecasting** — **时间序列预测**

> **📝 Notes:**
>
> **📌 What:**
> **(1) Sequence data types (序列数据类型):**
>
> Sequence data comes in many forms: text (words/characters), audio (waveforms), video (frames), time series (measurements), and biological sequences (DNA/protein).
>
> > 序列数据有多种形式：文本（词/字符）、音频（波形）、视频（帧）、时间序列（测量值）和生物序列（DNA/蛋白质）。
>
> **⚖️ Compare:**
> **(1) Audio vs Text sequences:**
>
> | Feature       | Audio               | Text               |
> | ------------- | ------------------- | ------------------ |
> | Unit          | Sample points       | Words/Tokens       |
> | Length        | Very long (16k/sec) | Shorter (hundreds) |
> | Preprocessing | Spectrogram/MFCC    | Tokenization       |
>
> > | 特性   | 音频             | 文本         |
> > | ------ | ---------------- | ------------ |
> > | 单位   | 采样点           | 词/Token     |
> > | 长度   | 非常长（16k/秒） | 较短（数百） |
> > | 预处理 | 频谱图/MFCC      | 分词         |
>
> **⚠️ Pitfall:**
> **(1) Not all time-stamped data needs RNN (不是所有时间戳数据都需要RNN):**
>
> If data points are independent (e.g., daily temperature with no autocorrelation), RNN may not help. RNN shines when current output depends on past inputs.
>
> > 如果数据点是独立的（例如，没有自相关的每日温度），RNN可能没有帮助。当当前输出依赖于过去输入时，RNN才发挥优势。

---

## 4. 时间序列 (Time Series)

### 4.1 概念定义 (Definition)

![Page 7](week4_rnn_slides_pages/page_007.png)

**Definition slide:** Explains time series with X-axis/Y-axis interpretation and the forecasting goal.

**定义幻灯片：** 用X轴/Y轴解释时间序列以及预测目标。

- A **Time Series** is a sequence of data points collected or recorded at specific time intervals. — **时间序列**是在特定时间间隔收集或记录的数据点序列。
- Unlike standard "cross-sectional" data (where you look at a snapshot of many things at once), time series focuses on **one (or more) thing over a duration**. — 与标准的"横截面"数据（一次查看多个事物的快照）不同，时间序列关注**一个（或多个）事物随时间的变化**。
- **The X-Axis:** Almost always represents time (seconds, days, years). — **X轴：** 几乎总是代表时间（秒、天、年）。
- **The Y-Axis:** The variable you are measuring (Price, Temperature, Population). — **Y轴：** 你测量的变量（价格、温度、人口）。
- **The Goal:** To understand the past and, ideally, peer into the future (**Forecasting**). — **目标：** 理解过去，理想情况下，预见未来（**预测**）。

### 4.2 示例：航空乘客数据 (Example: Air Passengers)

![Page 8](week4_rnn_slides_pages/page_008.png)

**Air Passengers plot:** Shows a classic time series with visible upward trend and seasonal pattern (peaks in summer months).

**航空乘客图：** 展示了一个经典的时间序列，具有明显的上升趋势和季节性模式（夏季月份的峰值）。

- **Air Passengers** dataset — **航空乘客**数据集
- **Non-stationary data** — Mean & sd changes with time — **非平稳数据** — 均值和标准差随时间变化
- **Seasonal data** — **季节性数据**
- Data from Jan 1949 - Dec 1960 — 数据来自1949年1月至1960年12月

Ref: https://www.kaggle.com/datasets/rakannimer/air-passengers

### 4.3 时间序列成分 (Time Series Components)

![Page 9](week4_rnn_slides_pages/page_009.png)

**Components definition slide:** Lists the four components of time series decomposition.

**成分定义幻灯片：** 列出时间序列分解的四个成分。

1. **Trend:** The long-term "direction." Is it generally going up, down, or staying flat? — **趋势：** 长期"方向"。总体是上升、下降还是持平？
2. **Seasonal:** Patterns that repeat over a fixed period (e.g., retail sales spiking every December). — **季节性：** 在固定周期内重复的模式（例如，每年12月零售销售激增）。
3. **Cycle:** A cycle is a long-term fluctuation in a time series that repeats, but **NOT at a fixed, regular interval**. — **周期：** 时间序列中重复的长期波动，但**不是在固定的、规则的间隔**。
4. **Noise (Residuals):** The random "hiccups" in the data that can't be explained by the other three. — **噪声（残差）：** 数据中无法被其他三个成分解释的随机"波动"。

![Page 10](week4_rnn_slides_pages/page_010.png)

**Decomposition visualization:** Shows the original plot broken down into Trend, Seasonal, and Residual components.

**分解可视化：** 展示原始图分解为趋势、季节性和残差成分。

**Decomposition:**

- Original plot — 原始图
- Trend — 趋势
- Seasonal — 季节性
- Residual — 残差

> **📝 Notes:**
>
> **📌 What:**
> **(1) Stationary vs Non-stationary (平稳 vs 非平稳):**
>
> Stationary: statistical properties (mean, variance) don't change over time. Non-stationary: properties change — like Air Passengers where both mean and variance increase.
>
> > 平稳：统计属性（均值、方差）不随时间变化。非平稳：属性变化 — 如航空乘客数据，均值和方差都增加。
>
> **(2) Seasonal vs Cycle (季节性 vs 周期):**
>
> Seasonal: fixed period (12 months, 7 days). Cycle: variable period (economic cycles of 3-7 years). Seasonal is predictable; cycles are harder to forecast.
>
> > 季节性：固定周期（12个月、7天）。周期：可变周期（3-7年的经济周期）。季节性可预测；周期更难预测。
>
> **🎯 Why:**
> **(1) Why decomposition matters (为什么分解重要):**
>
> To forecast, you need to separate and model each component differently. You can extrapolate the trend, use past seasonal patterns, and treat residuals as noise.
>
> > 要预测，你需要分别对每个成分建模。你可以外推趋势，使用过去的季节模式，并将残差视为噪声。
>
> **⚠️ Pitfall:**
> **(1) Confusing seasonal with cycle (混淆季节性和周期):**
>
> Exam trap: "The economy peaks every 5-7 years" is a CYCLE (irregular period), not seasonal. "Sales peak every December" is SEASONAL (fixed 12-month period).
>
> > 考试陷阱："经济每5-7年达到峰值"是周期（不规则周期），不是季节性。"每年12月销售达到峰值"是季节性（固定12个月周期）。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What's the difference between trend and cycle?" → Trend is the overall direction (up/down); cycle is a repeating fluctuation around the trend with irregular periods.
>
> > "趋势和周期有什么区别？" → 趋势是总体方向（上升/下降）；周期是围绕趋势的重复波动，周期不规则。

---

## 5. 循环神经网络 (Recurrent Neural Networks)

### 5.1 RNN 概述 (RNN Overview)

![Page 11](week4_rnn_slides_pages/page_011.png)

**RNN introduction slide:** Describes RNN's key property of using previous hidden states as inputs.

**RNN介绍幻灯片：** 描述了RNN使用先前隐藏状态作为输入的关键特性。

- RNNs are kind of DL models that takes the **previous output or hidden states as inputs**. i.e. the composite input at time t has some historical information about the happenings at time T < t. — RNN是一种深度学习模型，将**先前的输出或隐藏状态作为输入**。即，时间t的复合输入包含关于时间T < t发生事件的历史信息。
- RNNs are useful as their **intermediate states can store information** about past inputs for a time that is not fixed. — RNN很有用，因为它们的**中间状态可以存储**关于过去输入的信息，存储时间不固定。
- In RNNs, each input vector (e.g. word vector) is typically fed into the network **one at a time**, not all at once. — 在RNN中，每个输入向量（例如词向量）通常**一次一个**地输入网络，而不是一次全部输入。

### 5.2 RNN 与 FFN 对比 (RNN vs FFN)

![Page 12](week4_rnn_slides_pages/page_012.png)

**Architecture comparison:** Side-by-side diagram showing FFN (no loop) vs RNN (with loop from hidden state back to itself). The RNN shows the same cell repeated across time steps.

**架构对比：** 并排图显示FFN（无循环）vs RNN（隐藏状态循环回自身）。RNN显示同一单元在时间步上重复。

**FFNs vs RNNs Architecture:**

- **FFNs:** `X → h → y` (single pass, no feedback) — **FFN：** `X → h → y`（单次传递，无反馈）
- **RNNs:** `X_t → h_t → y_t` with hidden state `h_{t-1}` feeding back (loop/recurrence) — **RNN：** `X_t → h_t → y_t`，隐藏状态 `h_{t-1}`反馈（循环/递归）

### 5.3 RNN 公式 (RNN Formula)

![Page 13](week4_rnn_slides_pages/page_013.png)

**Formula slide:** Shows the core RNN equation with explanation of weight sharing across time.

**公式幻灯片：** 展示了核心RNN方程以及权重在时间上共享的解释。

**Hidden state formula:**

$$h_t = f(W_x \cdot x_t + W_h \cdot h_{t-1})$$

- $h_t$ = hidden state at time step $t$ — 时间步 $t$ 的隐藏状态
- $x_t$ = input at time step $t$ — 时间步 $t$ 的输入
- $W_x$ = weight matrix for input — 输入的权重矩阵
- $W_h$ = weight matrix for previous hidden state — 前一隐藏状态的权重矩阵
- $f$ = activation function (typically tanh) — 激活函数（通常是 tanh）

**Key Points:**

- Note that the **weights are shared over time** — 注意**权重在时间上是共享的**
- Essentially, copies of the RNN cell are made over time (**unrolling/unfolding**), with different inputs at different time steps. — 本质上，RNN单元在时间上被复制（**展开**），在不同时间步有不同的输入。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Hidden state as memory (隐藏状态作为记忆):**
>
> The hidden state h_t is RNN's "memory". It's a vector that encodes relevant information from ALL previous time steps, not just the immediate past.
>
> > 隐藏状态h_t是RNN的"记忆"。它是一个向量，编码了所有先前时间步的相关信息，而不仅仅是紧邻的过去。
>
> **(2) Weight sharing (权重共享):**
>
> The SAME W_x and W_h are used at every time step. This is what makes RNN "recurrent" — it's the same transformation applied repeatedly, not different weights at each step.
>
> > 相同的W_x和W_h在每个时间步使用。这就是RNN"循环"的原因 — 重复应用相同的变换，而不是每步不同的权重。
>
> **🎯 Why:**
> **(1) Why weight sharing? (为什么权重共享？):**
>
> If weights were different at each time step, the model would have O(T) parameters where T is sequence length. Weight sharing allows handling variable-length sequences with fixed parameters.
>
> > 如果每个时间步权重不同，模型将有O(T)个参数，其中T是序列长度。权重共享允许用固定参数处理可变长度的序列。
>
> **(2) Why combine x*t and h*{t-1}? (为什么结合x*t和h*{t-1}？):**
>
> x*t brings new information from the current input. h*{t-1} brings context from the past. Together they form a "composite input" that captures both present and history.
>
> > x*t带来当前输入的新信息。h*{t-1}带来过去的上下文。它们一起形成"复合输入"，同时捕获当前和历史。
>
> **💡 Intuition:**
> **(1) The note-passing analogy (传纸条类比):**
>
> Imagine students in a row. Each student gets a note from the previous student (h\_{t-1}) and sees something new (x_t). They write a new note combining both and pass it forward. The final note contains info from everyone.
>
> > 想象一排学生。每个学生从前一个学生那里收到一张纸条（h\_{t-1}），并看到新东西（x_t）。他们写一张结合两者的新纸条并传递。最后的纸条包含所有人的信息。
>
> **(2) The unrolling visualization (展开可视化):**
>
> Unrolling shows the loop as a chain of identical cells. Each cell takes x*t and h*{t-1}, outputs h_t. It's the same cell copied T times, not T different cells.
>
> > 展开将循环显示为相同单元的链。每个单元接收x*t和h*{t-1}，输出h_t。它是同一单元复制T次，而不是T个不同的单元。
>
> **📐 Formula:**
> **(1) RNN hidden state update (RNN隐藏状态更新):**
>
> Breaking down h*t = f(W_x · x_t + W_h · h*{t-1}):
>
> - W_x · x_t: projects the new input into hidden space
> - W*h · h*{t-1}: projects the previous memory into hidden space
> - Sum them: combines new info with old memory
> - f(...): applies non-linearity (tanh squashes to [-1,1])
>
> > 拆解 h*t = f(W_x · x_t + W_h · h*{t-1})：
> >
> > - W_x · x_t：将新输入投影到隐藏空间
> > - W*h · h*{t-1}：将先前记忆投影到隐藏空间
> > - 求和：结合新信息和旧记忆
> > - f(...)：应用非线性（tanh压缩到[-1,1]）
>
> **⚠️ Pitfall:**
> **(1) h_0 initialization (h_0初始化):**
>
> At t=0, there's no h\_{-1}. Common practice: initialize h_0 to zeros. Some models learn h_0. Forgetting to initialize leads to errors.
>
> > 在t=0时，没有h\_{-1}。常见做法：将h_0初始化为零。一些模型学习h_0。忘记初始化会导致错误。
>
> **(2) Tanh vs ReLU (Tanh vs ReLU):**
>
> RNN traditionally uses tanh, not ReLU. Why? tanh outputs [-1,1], helping control the range. ReLU can cause hidden states to explode since it's unbounded.
>
> > RNN传统上使用tanh，而不是ReLU。为什么？tanh输出[-1,1]，有助于控制范围。ReLU可能导致隐藏状态爆炸，因为它是无界的。
>
> **📝 Exam:**
> **(1) 公式解释题 (Formula explanation):**
>
> "Explain each term in the RNN hidden state equation." → W*x·x_t processes new input; W_h·h*{t-1} incorporates past; f is non-linear activation.
>
> > "解释RNN隐藏状态方程中的每一项。" → W*x·x_t处理新输入；W_h·h*{t-1}融入过去；f是非线性激活。
>
> **(2) 对比题 (Comparison):**
>
> "Why are weights shared in RNN?" → To handle variable-length sequences with fixed parameters; to learn patterns that can appear at any position.
>
> > "为什么RNN中权重是共享的？" → 为了用固定参数处理可变长度序列；为了学习可以出现在任何位置的模式。

---

## 6. 输入输出场景与示例 (Input-Output Scenarios)

### 6.1 图像描述示例 (Image Captioning Example)

![Page 14](week4_rnn_slides_pages/page_014.png)

**Image captioning problem statement:** Shows an image of a dog with the caption "The dog is hiding".

**图像描述问题陈述：** 展示了一张狗的图片，标题为"The dog is hiding"。

**Problem:** Given an image, produce a sentence describing its contents

- **Inputs:** Image feature (from a CNN) — **输入：** 图像特征（来自CNN）
- **Outputs:** Multiple words — **输出：** 多个词

Example: "The dog is hiding"

![Page 15](week4_rnn_slides_pages/page_015.png)

**Basic architecture:** CNN extracts features, which are fed to RNN.

**基本架构：** CNN提取特征，然后输入RNN。

![Page 16](week4_rnn_slides_pages/page_016.png)

**Step 1:** CNN output initializes the first RNN hidden state, which goes through a classifier to produce "The".

**步骤1：** CNN输出初始化第一个RNN隐藏状态，通过分类器产生"The"。

![Page 17](week4_rnn_slides_pages/page_017.png)

**Step 2:** The previous word "The" and hidden state are fed to produce "dog". This continues until the sentence is complete.

**步骤2：** 前一个词"The"和隐藏状态被输入以产生"dog"。这个过程继续直到句子完成。

**Architecture:** CNN extracts image features → RNN generates caption

**Step-by-step:**

- CNN output → RNN → first hidden state → Linear Classifier → "The"
- Continue: → RNN → next hidden state → Linear Classifier → "dog"

### 6.2 输入输出类型 (Input-Output Types)

![Page 18](week4_rnn_slides_pages/page_018.png)

**Taxonomy of RNN architectures:** Four different input-output configurations shown as diagrams with examples.

**RNN架构分类：** 四种不同的输入输出配置以图表形式展示，附有示例。

| Type                    | Scenario                       | Example                     |
| ----------------------- | ------------------------------ | --------------------------- |
| **Single - Single**     | Feed-forward Network           | Classification              |
| **Single - Multiple**   | Image Captioning               | Image → "The dog is hiding" |
| **Multiple - Single**   | Sentiment Classification       | Text → Rating               |
| **Multiple - Multiple** | Translation / Video Captioning | Sequence → Sequence         |

> **📝 Notes:**
>
> **📌 What:**
> **(1) One-to-Many (单对多):**
>
> One input produces a sequence of outputs. Example: image → caption. The CNN encodes the image once; RNN generates words one by one.
>
> > 一个输入产生一系列输出。例如：图像 → 标题。CNN编码图像一次；RNN逐个生成词。
>
> **(2) Many-to-One (多对单):**
>
> A sequence of inputs produces one output. Example: text → sentiment. Read all words, then output a single sentiment score.
>
> > 一系列输入产生一个输出。例如：文本 → 情感。读取所有词，然后输出一个情感分数。
>
> **(3) Many-to-Many (多对多):**
>
> Two types: (a) same length — video frame by frame; (b) different length — translation with encoder-decoder.
>
> > 两种类型：(a) 相同长度 — 视频逐帧；(b) 不同长度 — 带编码器-解码器的翻译。
>
> **🎯 Why:**
> **(1) Why does image captioning work this way? (为什么图像描述这样工作？):**
>
> CNN is good at extracting visual features (what objects are there). RNN is good at generating sequences (language). Combine them: CNN sees the image, RNN describes it.
>
> > CNN擅长提取视觉特征（有哪些物体）。RNN擅长生成序列（语言）。结合它们：CNN看图像，RNN描述它。
>
> **⚖️ Compare:**
> **(1) Architecture types:**
>
> | Type   | Input Length | Output Length | Example                 |
> | ------ | ------------ | ------------- | ----------------------- |
> | 1-to-1 | 1            | 1             | Standard classification |
> | 1-to-N | 1            | Variable      | Image captioning        |
> | N-to-1 | Variable     | 1             | Sentiment analysis      |
> | N-to-M | Variable     | Variable      | Translation             |
>
> > | 类型 | 输入长度 | 输出长度 | 示例     |
> > | ---- | -------- | -------- | -------- |
> > | 1对1 | 1        | 1        | 标准分类 |
> > | 1对N | 1        | 可变     | 图像描述 |
> > | N对1 | 可变     | 1        | 情感分析 |
> > | N对M | 可变     | 可变     | 翻译     |
>
> **📝 Exam:**
> **(1) 匹配题 (Matching):**
>
> "Match the architecture to the task: (a) Sentiment analysis (b) Machine translation (c) Image captioning." → (a) Many-to-One, (b) Many-to-Many, (c) One-to-Many.
>
> > "将架构与任务匹配：(a) 情感分析 (b) 机器翻译 (c) 图像描述。" → (a) 多对一，(b) 多对多，(c) 一对多。

---

## 7. 损失函数 (Loss Functions)

### 7.1 概述 (Overview)

![Page 19](week4_rnn_slides_pages/page_019.png)

**Loss function overview:** General definition and categories of loss functions.

**损失函数概述：** 损失函数的一般定义和类别。

- Method to evaluate how well an algorithm models the given data — 评估算法对给定数据建模效果的方法
- Quantifies the **error between the output and the target** — 量化**输出与目标之间的误差**
- Also known as **cost function** or **error function** — 也称为**代价函数**或**误差函数**

**Categories:**

- Regression Losses — 回归损失
- Probabilistic Losses — 概率损失
- Hinge Losses for maximum-margin classification — 最大间隔分类的Hinge损失

Ref: https://keras.io/api/losses/

### 7.2 回归损失函数 (Regression Loss Functions)

![Page 20](week4_rnn_slides_pages/page_020.png)

**Regression losses:** Definitions of MSE, MAE, and Mean Bias Error.

**回归损失：** MSE、MAE和平均偏差误差的定义。

**Mean Square Error (MSE) / Quadratic Loss / L2 Loss:**

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

- $y$ = actual value, $\hat{y}$ = predicted value, $n$ = number of samples
- Penalizes large errors more heavily (squared term)

- Average of the sum of the **squared differences** between actual value and the predicted value — 实际值与预测值之间**平方差**的总和的平均值

**Mean Absolute Error (MAE) / L1 Loss:**

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n}|y_i - \hat{y}_i|$$

- Takes absolute difference, not squared
- **Robust to outliers** since it does not make use of square

- Average of the sum of the **absolute differences** between actual value and the predicted value — 实际值与预测值之间**绝对差**的总和的平均值

**Mean Bias Error:**

$$\text{MBE} = \frac{1}{n} \sum_{i=1}^{n}(y_i - \hat{y}_i)$$

- No absolute value or square — can be positive or negative
- Positive and negative values may cancel out – less accurate in practice
- Can be used to see whether model has **positive or negative bias**

![Page 21](week4_rnn_slides_pages/page_021.png)

**MSE & MAE visualization:** Shows how MSE and MAE differ in penalizing errors.

**MSE和MAE可视化：** 展示MSE和MAE在惩罚误差方面的差异。

### 7.3 概率损失函数 (Probabilistic Loss Functions)

![Page 22](week4_rnn_slides_pages/page_022.png)

**Cross Entropy losses:** Used when model outputs probabilities rather than class labels.

**交叉熵损失：** 当模型输出概率而不是类别标签时使用。

Used when a model predicts **probabilities** for different classes instead of class labels — 当模型预测不同类别的**概率**而不是类别标签时使用

**Cross Entropy (also known as log loss):**

$$\text{CE} = -\sum_{i} y_i \cdot \log(\hat{y}_i)$$

- $y$ = true distribution (one-hot), $\hat{y}$ = predicted probabilities
- Measure of the **difference between two probability distributions** (predicted vs actual)

**Types:**

- **Binary Cross Entropy** (two classes – 0 and 1 as class labels) — **二元交叉熵**（两个类别 – 0和1作为类别标签）
- **Categorical Cross Entropy** (one-hot encoded class labels) — **分类交叉熵**（独热编码的类别标签）
- **Sparse Categorical Cross Entropy** (integers as class labels) — **稀疏分类交叉熵**（整数作为类别标签）

### 7.4 Hinge Loss

![Page 23](week4_rnn_slides_pages/page_023.png)

**Hinge loss:** Used for SVMs and maximum-margin classifiers.

**Hinge损失：** 用于SVM和最大间隔分类器。

$$\text{Hinge} = \max(0, 1 - y \cdot \hat{y})$$

- $y \in \{-1, +1\}$, $\hat{y}$ = raw model output (not probability)

- Primarily for classification tasks, especially with **SVMs** — 主要用于分类任务，特别是**SVM**
- Helps maximizes the **margin** between different classes — 帮助最大化不同类别之间的**间隔**
- Loss is **0** when the correct class is confidently predicted, but penalizes predictions that are too close to the decision boundary — 当正确类别被自信地预测时损失为**0**，但惩罚太接近决策边界的预测
- Requires labels to be **-1 and +1** (instead of 0 and 1) — 要求标签为**-1和+1**（而不是0和1）
- For multi-class classification: **Categorical Hinge Loss** — 对于多类分类：**分类Hinge损失**
- Can be used in NN — 可以在神经网络中使用

> **📝 Notes:**
>
> **📌 What:**
> **(1) Loss function purpose (损失函数的目的):**
>
> Loss functions quantify how "wrong" the model's predictions are. Training minimizes this loss by adjusting weights via gradient descent.
>
> > 损失函数量化模型预测的"错误程度"。训练通过梯度下降调整权重来最小化这个损失。
>
> **🎯 Why:**
> **(1) Why MSE penalizes outliers more (为什么MSE更多地惩罚离群值):**
>
> MSE squares the error: an error of 10 becomes 100, while an error of 2 becomes 4. The large error is penalized 25x more. This makes MSE sensitive to outliers.
>
> > MSE平方误差：误差10变成100，而误差2变成4。大误差被多惩罚25倍。这使得MSE对离群值敏感。
>
> **(2) Why Cross Entropy for classification (为什么分类用交叉熵):**
>
> Cross Entropy heavily penalizes confident wrong predictions. If true label = 1 and you predict 0.01, the -log(0.01) ≈ 4.6 is huge. This forces the model to avoid confident mistakes.
>
> > 交叉熵严重惩罚自信的错误预测。如果真实标签=1而你预测0.01，-log(0.01) ≈ 4.6 非常大。这迫使模型避免自信的错误。
>
> **⚖️ Compare:**
> **(1) MSE vs MAE vs Cross Entropy:**
>
> | Loss | Use Case            | Outlier Sensitivity | Gradient at 0 Error   |
> | ---- | ------------------- | ------------------- | --------------------- |
> | MSE  | Regression          | High (squares)      | 0 (smooth)            |
> | MAE  | Regression (robust) | Low (linear)        | Constant (non-smooth) |
> | CE   | Classification      | N/A                 | High near wrong       |
>
> > | 损失 | 使用场景     | 离群值敏感度 | 0误差时的梯度  |
> > | ---- | ------------ | ------------ | -------------- |
> > | MSE  | 回归         | 高（平方）   | 0（平滑）      |
> > | MAE  | 回归（鲁棒） | 低（线性）   | 常数（不平滑） |
> > | CE   | 分类         | 不适用       | 接近错误时高   |
>
> **⚠️ Pitfall:**
> **(1) Using wrong loss for the task (对任务使用错误的损失):**
>
> Classification task + MSE = bad idea. MSE doesn't penalize confident wrong predictions enough. Always use Cross Entropy for classification.
>
> > 分类任务 + MSE = 坏主意。MSE对自信的错误预测惩罚不够。分类任务总是使用交叉熵。
>
> **(2) Categorical vs Sparse Categorical CE (分类 vs 稀疏分类CE):**
>
> Categorical: labels are one-hot [0,1,0]. Sparse: labels are integers [1]. Mathematically the same, but Sparse saves memory for many classes.
>
> > Categorical：标签是独热编码[0,1,0]。Sparse：标签是整数[1]。数学上相同，但Sparse对多类节省内存。
>
> **📝 Exam:**
> **(1) 选择题 (Multiple choice):**
>
> "Which loss is most robust to outliers?" → MAE (no squaring).
>
> > "哪种损失对离群值最鲁棒？" → MAE（不平方）。
>
> **(2) 对比题 (Comparison):**
>
> "When to use MSE vs Cross Entropy?" → MSE for regression (continuous output), Cross Entropy for classification (probability output).
>
> > "什么时候用MSE vs 交叉熵？" → MSE用于回归（连续输出），交叉熵用于分类（概率输出）。

---

## 8. 反向传播与BPTT (Backpropagation and BPTT)

### 8.1 反向传播回顾 (Backpropagation Refresher)

![Page 24](week4_rnn_slides_pages/page_024.png)

**Backpropagation diagram:** Shows the chain rule applied to a 2-layer network. Gradients flow backward from loss to weights.

**反向传播图：** 展示了应用于2层网络的链式法则。梯度从损失向权重反向流动。

**Standard Backpropagation:**

- For a 2-layer network: `f₁(x; W₁) → f₂(ŷ₁; W₂) → ŷ₂ → Loss(y, ŷ₂)`

**Gradient Descent:**

$$W = W - \alpha \cdot \frac{\partial L}{\partial W}$$

- $W$ = weights, $\alpha$ = learning rate, $L$ = loss

**Chain Rule:**

$$\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial \hat{y}_2} \cdot \frac{\partial \hat{y}_2}{\partial \hat{y}_1} \cdot \frac{\partial \hat{y}_1}{\partial W_1}$$

- Gradient flows backward through layers

### 8.2 时间反向传播 (BPTT)

![Page 25](week4_rnn_slides_pages/page_025.png)

**BPTT concept:** Explains how backpropagation is adapted for RNNs by unrolling through time.

**BPTT概念：** 解释了如何通过在时间上展开来将反向传播适应于RNN。

- In a normal neural network, we use backpropagation to update weights by calculating gradients **layer by layer**. — 在普通神经网络中，我们使用反向传播通过**逐层**计算梯度来更新权重。
- In an RNN, the same **weights are used at every time step**, and the network is "unrolled" across time steps. — 在RNN中，**每个时间步使用相同的权重**，网络在时间步上"展开"。

**BPTT means we compute gradients across all these time steps and update the shared weights.** — **BPTT意味着我们计算所有这些时间步的梯度并更新共享权重。**

- The weight updates are computed for each copy in the unfolded network, then **summed (or averaged)** and then applied to the RNN weights. — 权重更新在展开网络的每个副本中计算，然后**求和（或平均）**，然后应用于RNN权重。

### 8.3 BPTT 展开图 (BPTT Unfolded RNN)

![Page 26](week4_rnn_slides_pages/page_026.png)

**Forward pass diagram:** Shows the unrolled RNN with inputs x₁, x₂, x₃ feeding into hidden states h₁, h₂, h₃ and producing outputs ŷ₁, ŷ₂, ŷ₃ with losses L₁, L₂, L₃.

**前向传播图：** 展示了展开的RNN，输入x₁, x₂, x₃输入到隐藏状态h₁, h₂, h₃并产生输出ŷ₁, ŷ₂, ŷ₃以及损失L₁, L₂, L₃。

**Forward Pass:**

```
x₁ → h₁ → ŷ₁ → L₁
x₂ → h₂ → ŷ₂ → L₂
x₃ → h₃ → ŷ₃ → L₃
```

(With h₀ as initial hidden state)

![Page 27](week4_rnn_slides_pages/page_027.png)

**Backward pass diagram:** Shows gradients flowing backward through time with the chain rule multiplying through multiple time steps.

**反向传播图：** 展示了梯度通过时间向后流动，链式法则通过多个时间步相乘。

**Backward Pass:**

- Gradients flow back through time — 梯度通过时间向后流动
- $\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$ summed over all time steps — $\frac{\partial L}{\partial W} = \sum_t \frac{\partial L_t}{\partial W}$ 在所有时间步上求和
- Requires multiplying gradients through many time steps — 需要通过许多时间步相乘梯度

> **📝 Notes:**
>
> **📌 What:**
> **(1) BPTT = Backpropagation Through Time (BPTT = 时间反向传播):**
>
> BPTT is just regular backprop applied to the unrolled RNN graph. The "through time" part means gradients flow backward through all time steps.
>
> > BPTT只是应用于展开RNN图的常规反向传播。"时间"部分意味着梯度通过所有时间步向后流动。
>
> **🎯 Why:**
> **(1) Why sum gradients over time? (为什么对时间求和梯度？):**
>
> The same weight W affects the output at t=1, t=2, ..., t=T. Its total effect is the sum of its effects at each time step. So we sum ∂L/∂W from all time steps.
>
> > 相同的权重W影响t=1, t=2, ..., t=T的输出。它的总效果是每个时间步效果的总和。所以我们从所有时间步求和∂L/∂W。
>
> **(2) Why does gradient chain multiply? (为什么梯度链相乘？):**
>
> To get ∂L/∂h₁, you need: ∂L/∂h₃ · ∂h₃/∂h₂ · ∂h₂/∂h₁. Each link in the chain is a multiplication. This creates the vanishing/exploding gradient problem.
>
> > 要得到∂L/∂h₁，你需要：∂L/∂h₃ · ∂h₃/∂h₂ · ∂h₂/∂h₁。链中的每个环节都是一次乘法。这产生了梯度消失/爆炸问题。
>
> **💡 Intuition:**
> **(1) The telephone game analogy (传话游戏类比):**
>
> BPTT is like playing the telephone game backward. The error message at the end needs to travel back through every person (time step). Each person might distort it (multiply by a number < 1 or > 1), causing the message to vanish or explode.
>
> > BPTT就像反向玩传话游戏。最后的错误消息需要通过每个人（时间步）传回。每个人可能会扭曲它（乘以一个<1或>1的数），导致消息消失或爆炸。
>
> **📐 Formula:**
> **(1) Chain rule through time (时间上的链式法则):**
>
> For weight $W_h$ affecting $h_t$:
>
> $$\frac{\partial L}{\partial W_h} = \sum_t \left( \frac{\partial L_t}{\partial \hat{y}_t} \cdot \frac{\partial \hat{y}_t}{\partial h_t} \cdot \sum_{k \leq t} \frac{\partial h_t}{\partial h_k} \cdot \frac{\partial h_k}{\partial W_h} \right)$$
>
> The inner sum over $k \leq t$ captures how $h_t$ depends on all previous hidden states.
>
>> 对于影响 $h_t$ 的权重 $W_h$：
>>
>> $$\frac{\partial L}{\partial W_h} = \sum_t \left( \frac{\partial L_t}{\partial \hat{y}_t} \cdot \frac{\partial \hat{y}_t}{\partial h_t} \cdot \sum_{k \leq t} \frac{\partial h_t}{\partial h_k} \cdot \frac{\partial h_k}{\partial W_h} \right)$$
>>
>> 内部对 $k \leq t$ 的求和捕获了 $h_t$ 如何依赖于所有先前的隐藏状态。
>
> **⚠️ Pitfall:**
> **(1) Truncated BPTT (截断BPTT):**
>
> Full BPTT through 1000 time steps is expensive. In practice, we often "truncate" — only backprop through the last k steps. Trades accuracy for speed.
>
> > 通过1000个时间步的完整BPTT很昂贵。实践中，我们经常"截断" — 只反向传播最后k步。用准确性换取速度。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Why does BPTT sum gradients over time?" → Because the same weight affects outputs at all time steps; total gradient is the sum of contributions from each step.
>
> > "为什么BPTT对时间求和梯度？" → 因为相同的权重影响所有时间步的输出；总梯度是每步贡献的总和。

---

## 9. 梯度消失问题 (Vanishing Gradient Problem)

### 9.1 问题描述 (Problem Description)

![Page 28](week4_rnn_slides_pages/page_028.png)

**Vanishing gradient explanation:** Shows how repeated multiplication can cause gradients to shrink to zero.

**梯度消失解释：** 展示了重复乘法如何导致梯度收缩为零。

**Problems with the Vanilla RNN:**

- In the same way a product of k real numbers can shrink to zero or explode to infinity, so can a **product of matrices** — 就像k个实数的乘积可以收缩为零或爆炸到无穷大一样，**矩阵的乘积**也可以

**Vanishing gradient causes:**

- Gradients become **extremely small** as they propagate backward — 梯度在向后传播时变得**极小**
- The **first layers (or earliest time steps in RNN)** receive almost no updates — **第一层（或RNN中最早的时间步）**几乎不接收更新
- The network **fails to learn long-term dependencies** — 网络**无法学习长期依赖**

### 9.2 解决方案 (Solutions)

![Page 29](week4_rnn_slides_pages/page_029.png)

**Five solutions:** Lists approaches to mitigate vanishing gradients.

**五种解决方案：** 列出减轻梯度消失的方法。

1. **Use Gated Architectures (LSTM / GRU)** — **使用门控架构（LSTM / GRU）**
2. **Gradient Clipping** — Prevents gradients from becoming too small or too large — **梯度裁剪** — 防止梯度变得太小或太大
3. **Use Activation Functions Carefully** — functions like ReLU (instead of tanh or sigmoid) do not squash values as much — **谨慎使用激活函数** — ReLU（代替tanh或sigmoid）不会过度压缩值
4. **Layer Normalization / Batch Normalization** — Normalizes activations to keep values in a stable range — **层归一化/批归一化** — 归一化激活值以保持值在稳定范围内
5. **Use Shorter Sequences** — Backpropagating through fewer time steps reduces gradient decay — **使用更短的序列** — 通过更少的时间步反向传播减少梯度衰减

> **📝 Notes:**
>
> **📌 What:**
> **(1) Vanishing gradient (梯度消失):**
>
> When gradients become exponentially small as they propagate backward. At step 1, the gradient might be 10⁻¹⁰ — essentially zero. No learning happens.
>
> > 当梯度在向后传播时变得指数级小。在步骤1，梯度可能是10⁻¹⁰ — 基本上是零。没有学习发生。
>
> **(2) Exploding gradient (梯度爆炸):**
>
> The opposite: gradients become exponentially large. Values overflow to NaN or Inf. Gradient clipping directly addresses this.
>
> > 相反的情况：梯度变得指数级大。值溢出到NaN或Inf。梯度裁剪直接解决这个问题。
>
> **🎯 Why:**
> **(1) Why does vanishing happen with tanh/sigmoid? (为什么tanh/sigmoid会导致消失？):**
>
> tanh has derivative in (0,1). When you multiply many numbers < 1, the product → 0. Example: 0.5^100 ≈ 10⁻³⁰.
>
> > tanh的导数在(0,1)之间。当你乘以许多<1的数时，乘积→0。例如：0.5^100 ≈ 10⁻³⁰。
>
> **(2) Why does this break long-term dependencies? (为什么这会破坏长期依赖？):**
>
> If the gradient from step 100 to step 1 is ~0, the network can't learn that step 1 affects step 100. It only learns short-range patterns.
>
> > 如果从步骤100到步骤1的梯度约为0，网络无法学习步骤1影响步骤100。它只能学习短程模式。
>
> **💡 Intuition:**
> **(1) The fading echo analogy (回声衰减类比):**
>
> Imagine shouting in a canyon. Each bounce loses energy. After 100 bounces, the echo is inaudible. Vanishing gradients are similar — the "error signal" fades as it travels back through time.
>
> > 想象在峡谷中喊叫。每次反弹都会失去能量。100次反弹后，回声听不见了。梯度消失类似 — "错误信号"在通过时间向后传播时衰减。
>
> **(2) Why LSTM helps (为什么LSTM有帮助):**
>
> LSTM adds a "shortcut highway" (cell state) that allows gradients to flow with minimal multiplication. It's like an express lane bypassing traffic.
>
> > LSTM添加了一个"快捷高速公路"（细胞状态），允许梯度以最小乘法流动。就像一条绕过交通的快速车道。
>
> **⚖️ Compare:**
> **(1) Solutions comparison:**
>
> | Solution          | Addresses           | Mechanism                          |
> | ----------------- | ------------------- | ---------------------------------- |
> | LSTM/GRU          | Vanishing           | Gate-controlled information flow   |
> | Gradient Clipping | Exploding           | Cap gradient magnitude             |
> | ReLU              | Vanishing (partial) | Derivative = 1 for positive inputs |
> | Normalization     | Both                | Keeps activations in good range    |
>
> > | 解决方案 | 解决问题     | 机制               |
> > | -------- | ------------ | ------------------ |
> > | LSTM/GRU | 消失         | 门控信息流         |
> > | 梯度裁剪 | 爆炸         | 限制梯度幅度       |
> > | ReLU     | 消失（部分） | 正输入的导数=1     |
> > | 归一化   | 两者         | 保持激活在良好范围 |
>
> **⚠️ Pitfall:**
> **(1) ReLU in RNN (RNN中的ReLU):**
>
> ReLU has unbounded output, which can cause hidden states to explode over long sequences. That's why RNN typically uses tanh, and LSTM/GRU have gates.
>
> > ReLU有无界输出，可能导致隐藏状态在长序列上爆炸。这就是为什么RNN通常使用tanh，而LSTM/GRU有门控。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What causes vanishing gradients in RNN?" → Repeated multiplication by values < 1 (derivatives of tanh/sigmoid) causes gradients to shrink exponentially over time steps.
>
> > "是什么导致RNN中的梯度消失？" → 重复乘以<1的值（tanh/sigmoid的导数）导致梯度在时间步上指数级收缩。
>
> **(2) 解决方案题 (Solutions):**
>
> "Name 3 solutions for vanishing gradients." → (1) Use LSTM/GRU, (2) Gradient clipping, (3) Use normalization.
>
> > "说出3个解决梯度消失的方案。" → (1) 使用LSTM/GRU，(2) 梯度裁剪，(3) 使用归一化。

---

## 10. 长短期记忆网络 (Long Short-Term Memory - LSTM)

### 10.1 LSTM 概述 (LSTM Overview)

![Page 30](week4_rnn_slides_pages/page_030.png)

**LSTM introduction:** Describes LSTM as a special RNN capable of learning long-term dependencies, with citation.

**LSTM介绍：** 将LSTM描述为一种能够学习长期依赖的特殊RNN，附有引用。

**Long Short Term Memory networks** – usually just called "LSTMs" – are a special kind of RNN, capable of learning **long-term dependencies**.

- Introduced by **Hochreiter & Schmidhuber (1997)** — 由**Hochreiter & Schmidhuber (1997)**提出

![Page 31](week4_rnn_slides_pages/page_031.png)

**LSTM vs RNN architecture:** Shows that LSTM's repeating module contains more complex structure than vanilla RNN's single layer.

**LSTM vs RNN架构：** 显示LSTM的重复模块比普通RNN的单层包含更复杂的结构。

**The repeating module in a standard LSTM contains a single layer** (vs multiple interacting gates in LSTM)

### 10.2 LSTM 核心概念 (Core Concepts)

![Page 32](week4_rnn_slides_pages/page_032.png)

**Cell state and gates:** The key innovation of LSTM is the cell state (the horizontal line at top) and gates that control information flow.

**细胞状态和门：** LSTM的关键创新是细胞状态（顶部的水平线）和控制信息流的门。

- The core idea behind LSTMs is the **cell state** — LSTM的核心思想是**细胞状态**
- The LSTM has the ability to **remove or add information** to the cell state: thanks to **gates** — LSTM有能力**删除或添加信息**到细胞状态：多亏了**门**
- Gates are composed out of a **sigmoid neural net layer** and a **pointwise multiplication operation** — 门由**sigmoid神经网络层**和**逐点乘法运算**组成

### 10.3 LSTM 步骤详解 (Step-by-Step LSTM Walk Through)

#### Step 1: 遗忘门 (Forget Gate)

![Page 33](week4_rnn_slides_pages/page_033.png)

**Forget gate diagram:** Shows the sigmoid layer that outputs values between 0 and 1, controlling what to forget from the cell state.

**遗忘门图：** 显示输出0到1之间值的sigmoid层，控制从细胞状态中遗忘什么。

**Decide what information to throw away from the cell state, forget layer.**

$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

- $f_t$ = forget gate output (0 to 1 for each dimension)
- $\sigma$ = sigmoid function
- $[h_{t-1}, x_t]$ = concatenation of previous hidden state and current input

- `1` represents **"completely keep this"** — `1`表示**"完全保留"**
- `0` represents **"completely get rid of this"** — `0`表示**"完全丢弃"**

#### Step 2: 输入门 (Input Gate)

![Page 34](week4_rnn_slides_pages/page_034.png)

**Input gate diagram:** Shows two parts: (1) sigmoid layer deciding what to update, (2) tanh layer creating candidate values.

**输入门图：** 显示两部分：(1) sigmoid层决定更新什么，(2) tanh层创建候选值。

**Decide what new information we're going to store in the cell state:**

$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

- $i_t$ = Input gate (what to update)
- $\tilde{C}_t$ = Candidate values (new information)
- **Input gate layer:** decides which values we will update — **输入门层：** 决定我们将更新哪些值
- **Tanh layer:** creates a vector of new candidate values — **Tanh层：** 创建新候选值的向量

Example: "I grew up in France… I speak fluent French." — 示例："我在法国长大...我说流利的法语。"

#### Step 3: 更新细胞状态 (Update Cell State)

![Page 35](week4_rnn_slides_pages/page_035.png)

**Cell state update:** Shows the formula combining forget gate output, old cell state, input gate output, and candidate values.

**细胞状态更新：** 显示结合遗忘门输出、旧细胞状态、输入门输出和候选值的公式。

**Update the cell state:**

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

- $f_t \odot C_{t-1}$: old state scaled by forget gate
- $i_t \odot \tilde{C}_t$: new info scaled by input gate

- Multiply old state by forget gate output — 将旧状态乘以遗忘门输出
- Add new candidate values scaled by input gate output — 添加由输入门输出缩放的新候选值

#### Step 4: 输出门 (Output Gate)

![Page 36](week4_rnn_slides_pages/page_036.png)

**Output gate diagram:** Shows sigmoid deciding what parts of cell state to output, then cell state through tanh multiplied by that decision.

**输出门图：** 显示sigmoid决定细胞状态的哪些部分输出，然后细胞状态通过tanh乘以该决定。

**Decide what is the output:**

$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

$$h_t = o_t \odot \tanh(C_t)$$

- $o_t$ = Output gate
- $h_t$ = Hidden state output
- Sigmoid layer decides what parts of the cell state to output — Sigmoid层决定细胞状态的哪些部分输出
- Cell state passed through tanh and multiplied by sigmoid output — 细胞状态通过tanh并乘以sigmoid输出

Example: "I grew up in France… I speak fluent French." — 示例："我在法国长大...我说流利的法语。"

> **📝 Notes:**
>
> **📌 What:**
> **(1) Cell state C_t (细胞状态C_t):**
>
> The "long-term memory" — a vector that flows through time with minimal transformations. It's the "highway" that allows gradients to flow without vanishing.
>
> > "长期记忆" — 一个以最小变换流经时间的向量。它是允许梯度流动而不消失的"高速公路"。
>
> **(2) Hidden state h_t (隐藏状态h_t):**
>
> The "short-term memory" / working memory. It's derived from the cell state and used for predictions and passed to the next step.
>
> > "短期记忆"/工作记忆。它从细胞状态派生，用于预测并传递到下一步。
>
> **(3) The three gates (三个门):**
>
> - Forget gate (f_t): what to throw away from old memory
> - Input gate (i_t): what new info to add
> - Output gate (o_t): what to expose as output/next hidden state
>
> > - 遗忘门(f_t)：从旧记忆中丢弃什么
> > - 输入门(i_t)：添加什么新信息
> > - 输出门(o_t)：作为输出/下一隐藏状态暴露什么
>
> **🎯 Why:**
> **(1) Why does LSTM solve vanishing gradients? (为什么LSTM解决梯度消失？):**
>
> The cell state C_t flows through time with only element-wise operations (multiply by f_t, add i_t \* C̃_t). No matrix multiplication → no exponential shrinkage. Gradients can flow for hundreds of steps.
>
> > 细胞状态C_t只通过逐元素操作流经时间（乘以f_t，加i_t \* C̃_t）。没有矩阵乘法 → 没有指数收缩。梯度可以流过数百步。
>
> **(2) Why sigmoid for gates? (为什么门用sigmoid？):**
>
> Sigmoid outputs [0,1], perfect for "how much to keep". 0 = completely forget, 1 = completely keep. It's a smooth, learnable switch.
>
> > Sigmoid输出[0,1]，完美用于"保留多少"。0 = 完全遗忘，1 = 完全保留。它是一个平滑的、可学习的开关。
>
> **💡 Intuition:**
> **(1) The notebook analogy (笔记本类比):**
>
> Cell state = a notebook. Forget gate = eraser (decide what to erase). Input gate + candidate = pencil (decide what to write and write it). Output gate = what to read aloud from the notebook.
>
> > 细胞状态 = 笔记本。遗忘门 = 橡皮擦（决定擦除什么）。输入门 + 候选值 = 铅笔（决定写什么并写下）。输出门 = 从笔记本大声读出什么。
>
> **(2) The France example (法国示例):**
>
> "I grew up in France." — The input gate stores "France" as location context. "I speak fluent \_\_\_" — The output gate recalls the stored location to help predict "French".
>
> > "我在法国长大。" — 输入门存储"法国"作为位置上下文。"我说流利的\_\_\_" — 输出门回忆存储的位置以帮助预测"法语"。
>
> **📐 Formula:**
> **(1) LSTM equations summary (LSTM方程总结):**
>
> $$\begin{aligned}
> f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) & \text{(Forget gate)} \\
> i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) & \text{(Input gate)} \\
> \tilde{C}_t &= \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) & \text{(Candidate)} \\
> C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t & \text{(Cell state)} \\
> o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) & \text{(Output gate)} \\
> h_t &= o_t \odot \tanh(C_t) & \text{(Hidden state)}
> \end{aligned}$$
>
>> $$\begin{aligned}
>> f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) & \text{(遗忘门)} \\
>> i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) & \text{(输入门)} \\
>> \tilde{C}_t &= \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) & \text{(候选值)} \\
>> C_t &= f_t \odot C_{t-1} + i_t \odot \tilde{C}_t & \text{(细胞状态)} \\
>> o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) & \text{(输出门)} \\
>> h_t &= o_t \odot \tanh(C_t) & \text{(隐藏状态)}
>> \end{aligned}$$
>
> **⚖️ Compare:**
> **(1) LSTM vs GRU:**
>
> | Feature     | LSTM                      | GRU               |
> | ----------- | ------------------------- | ----------------- |
> | Gates       | 3 (forget, input, output) | 2 (reset, update) |
> | States      | 2 (C_t and h_t)           | 1 (h_t only)      |
> | Parameters  | More                      | Fewer             |
> | Performance | Slightly better for long  | Faster training   |
>
> > | 特性 | LSTM                    | GRU               |
> > | ---- | ----------------------- | ----------------- |
> > | 门   | 3个（遗忘、输入、输出） | 2个（重置、更新） |
> > | 状态 | 2个（C_t和h_t）         | 1个（仅h_t）      |
> > | 参数 | 更多                    | 更少              |
> > | 性能 | 长序列稍好              | 训练更快          |
>
> **⚠️ Pitfall:**
> **(1) Confusing C_t and h_t (混淆C_t和h_t):**
>
> C_t is the cell state (long-term memory). h_t is the hidden state (what gets passed to next layer and used for output). Students often confuse which is which.
>
> > C_t是细胞状态（长期记忆）。h_t是隐藏状态（传递到下一层并用于输出）。学生经常混淆哪个是哪个。
>
> **(2) LSTM doesn't guarantee perfect memory (LSTM不保证完美记忆):**
>
> LSTM CAN learn long-term dependencies, but doesn't always. Training still requires sufficient data and proper hyperparameters.
>
> > LSTM能够学习长期依赖，但并不总是能。训练仍然需要足够的数据和适当的超参数。
>
> **📝 Exam:**
> **(1) 公式解释题 (Formula explanation):**
>
> "Explain the cell state update equation $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$." → $f_t \odot C_{t-1}$ keeps old memory scaled by forget gate; $i_t \odot \tilde{C}_t$ adds new info scaled by input gate.
>
>> "解释细胞状态更新方程 $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$。" → $f_t \odot C_{t-1}$ 保留由遗忘门缩放的旧记忆；$i_t \odot \tilde{C}_t$ 添加由输入门缩放的新信息。
>
> **(2) 概念题 (Conceptual):**
>
> "How does LSTM solve the vanishing gradient problem?" → The cell state provides a "gradient highway" — it flows through time with only element-wise operations, not matrix multiplications, allowing gradients to propagate without exponential decay.
>
> > "LSTM如何解决梯度消失问题？" → 细胞状态提供了"梯度高速公路" — 它只通过逐元素操作流经时间，而不是矩阵乘法，允许梯度传播而不会指数衰减。
>
> **(3) 对比题 (Comparison):**
>
> "What's the role of each LSTM gate?" → Forget: discard old info. Input: add new info. Output: decide what to expose.
>
> > "每个LSTM门的作用是什么？" → 遗忘：丢弃旧信息。输入：添加新信息。输出：决定暴露什么。

---

## 11. 总结 (Summary)

![Page 37](week4_rnn_slides_pages/page_037.png)

**Summary slide:** Lists all topics covered in the lecture.

**总结幻灯片：** 列出了本讲座涵盖的所有主题。

**Topics Covered:**

- FNN – Review — FNN回顾
- Motivation — 动机
- Usages of Sequential Data — 序列数据的应用
- Time Series — 时间序列
- Time Series – Components — 时间序列成分
- Recurrent Neural Networks (RNNs) — 循环神经网络
- Backpropagation Refresher — 反向传播复习
- Backpropagation Through Time (BPTT) — 时间反向传播
- Vanishing Gradient Problem — 梯度消失问题
- Long-Short Term Memory (LSTM) — 长短期记忆

---
