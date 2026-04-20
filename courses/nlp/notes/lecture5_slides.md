# Week 5: 语言模型入门 (Introduction to Language Model)

> Source: `lecture_5_W26.pdf`
> Total slides: 63
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程 (Lesson Agenda)

![Page 1](lecture5_slides_pages/page_001.png)

**CST8507: Natural Language Processing — Week #5: Introduction to Language Model** — CST8507自然语言处理，第5周：语言模型入门

![Page 2](lecture5_slides_pages/page_002.png)

**Lesson Agenda:** — 本节课议程：

- Lab — 实验
- Text Collection (overview) — 文本收集（概述）
- Language Model — 语言模型
- N-gram — N元语法
- NN Language model — 神经网络语言模型
- Recurrent Neural Networks RNN — 循环神经网络 RNN
- LSTMs — 长短期记忆网络

> **📝 Notes:**
>
> **承接**: 本节作为第5周开篇，列出从文本收集到语言模型（N-gram → NN → RNN → LSTM）的完整路线图；这些主题将在后续各节中逐一展开。

---

## 2. NLP开发生命周期 (NLP Development Life Cycle)

![Page 3](lecture5_slides_pages/page_003.png)

**NLP Development Life Cycle:** Circular pipeline diagram — Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model. — NLP开发生命周期循环流程图——需求收集→数据收集→文本预处理→特征提取→模型构建→评估→部署→收集更多数据/改进模型。

---

## 3. 文本收集 (Text Collection)

### 3.1 互联网数据规模 (Internet Data Scale)

![Page 4](lecture5_slides_pages/page_004.png)

**Data generated in one minute on various social platforms** — 各社交平台一分钟内产生的数据量

Ref: https://localiq.com/blog/what-happens-in-an-internet-minute/

### 3.2 推文收集与X API (Tweet Collecting & X API)

![Page 5](lecture5_slides_pages/page_005.png)

**Text Collection:** — 文本收集：

- Tweet Collecting — 推文收集
- X API — X平台API

![Page 6](lecture5_slides_pages/page_006.png)

**Create X Developer Account:** — 创建X开发者账户：

Ref: https://help.rssground.com/articles/233141-how-to-create-x-twitter-developer-app

### 3.3 网页抓取 (Web Scraping)

![Page 7](lecture5_slides_pages/page_007.png)

**Web Scraping: Extraction of data from a website** — 网页抓取：从网站中提取数据

Python libraries are widely used for parsing HTML: — Python库广泛用于解析HTML：

1. **Beautiful Soup:** A popular library for parsing HTML and XML documents. It simplifies extracting data from web pages and has an active community with detailed documentation. — 用于解析HTML和XML文档的流行库，简化了从网页提取数据的过程
2. **lxml:** Known for its speed, lxml is one of the fastest parsing libraries available. It receives regular updates, with the latest released in July 2023. — 以速度著称，是最快的解析库之一
3. **html5lib:** A pure-Python library designed to conform to the WHATWG (Web Hypertext Application Technology Working Group) HTML specification, ensuring compatibility with major web browsers. — 纯Python库，遵循WHATWG HTML规范

![Page 8](lecture5_slides_pages/page_008.png)

**Demo:** In-class code demonstration. — 课堂代码演示。

> **📝 Notes:**
>
> **承接**: 上一节回顾了NLP开发流程中的数据收集阶段；本节介绍了文本收集的三种途径（API、网页抓取、社交平台），为下一节「概率论基础」提供语料来源的背景理解。

---

## 4. 概率论基础回顾 (Probability Theory Review)

### 4.1 有放回抽样 (Sampling with Replacement)

![Page 9](lecture5_slides_pages/page_009.png)

**Reminder: Probability Theory** — 复习：概率论

![Page 10](lecture5_slides_pages/page_010.png)

**Basic Probability Theory: Sampling with replacement** — 基本概率论：有放回抽样

Pick a random shape, then put it back in the bag. — 随机取出一个形状，然后放回袋中。

- P(blue) = 5/15, P(red) = 5/15 — 蓝色概率=5/15，红色概率=5/15
- P(△|red) = 3/5 — 在红色条件下三角形的概率=3/5
- P(blue|□) = 2/5 — 在方形条件下蓝色的概率=2/5

![Page 11](lecture5_slides_pages/page_011.png)

**Sampling with replacement — Sequence probability:** — 有放回抽样——序列概率：

Pick a random shape, then put it back in the bag. What sequence of shapes will you draw? — 随机取出形状再放回，你会抽到什么序列？

- P(sequence₁) = 1/15 × 1/15 × 1/15 × 2/15 = 2/50625
- P(sequence₂) = 3/15 × 2/15 × 2/15 × 3/15 = 36/50625

### 4.2 条件概率 (Conditional Probability)

![Page 12](lecture5_slides_pages/page_012.png)

**Conditional Probability:** — 条件概率：

P(X|Y) = P(X, Y) / P(Y) — P(X|Y) = P(X, Y) / P(Y)

The conditional probability of X given Y: Probability that one event occurs given that another event has already occurred. — X在Y已发生条件下的概率：一个事件在另一事件已发生的前提下发生的概率。

### 4.3 概率链式法则 (Chain Rule of Probability)

![Page 13](lecture5_slides_pages/page_013.png)

**Chain Rule of Probability:** — 概率链式法则：

The chain rule expresses a joint probability as a product of conditional probabilities. — 链式法则将联合概率表示为条件概率的乘积。

For a sequence of events X₁, X₂, …, Xₙ: — 对于事件序列 X₁, X₂, …, Xₙ：

P(X₁, X₂, …, Xₙ) = P(X₁) · P(X₂|X₁) · P(X₃|X₁,X₂) · … · P(Xₙ|X₁,…,Xₙ₋₁)

> **📝 Notes:**
>
> **承接**: 上一节介绍了数据收集途径；本节复习了概率论三大基础——有放回抽样、条件概率、链式法则——这些数学工具是理解下一节「语言模型」核心公式的必备前提。

---

## 5. 语言建模 (Language Modeling)

### 5.1 语言模型定义 (Definition)

![Page 14](lecture5_slides_pages/page_014.png)

**LANGUAGE MODELING** — 语言建模

![Page 15](lecture5_slides_pages/page_015.png)

**Language Modeling: the task of predicting what word comes next** — 语言建模：预测下一个词的任务

- "the students opened their ______" → books / minds / exams / laptops — "学生们打开了他们的______" → 书/思想/考卷/笔记本电脑
- Given a sequence of words, compute the probability distribution of the next word — 给定一个词序列，计算下一个词的概率分布
- Where the next word can be any word in the vocabulary — 下一个词可以是词汇表中的任何词
- ➢ A system that does this is called a **Language Model** — 执行此任务的系统称为**语言模型**

![Page 16](lecture5_slides_pages/page_016.png)

**Popular Usages:** — 常见应用场景

> 📖 **图解读笔记：**
>
> | 符号/元素 | 含义 |
> |-----------|------|
> | 对话框图标 | 语言模型的各种应用场景 |
>
> **人话解释**: 语言模型广泛应用于自动补全、机器翻译、语音识别、文本生成等任务。

### 5.2 语言模型目标 (Goal)

![Page 17](lecture5_slides_pages/page_017.png)

**Goal of Language Modeling:** learn patterns in text and predict the next word (or sequence of words) based on prior context. — 语言模型的目标：学习文本中的模式，并根据先前的上下文预测下一个词（或词序列）。

> **📝 Notes:**
>
> **承接**: 上一节复习了概率论基础工具；本节正式定义了「语言模型」——给定上下文预测下一个词的概率分布，这个定义将在下一节「N-gram语言模型」中被具体化为基于统计频率的实现方案。

---

## 6. N-gram语言模型 (N-gram Language Modeling)

### 6.1 N-gram基本思想 (N-gram Basic Idea)

![Page 18](lecture5_slides_pages/page_018.png)

**N-gram Language Modeling:** IDEA: Collect statistics about how frequent different n-grams are, and use these to predict next word. — N-gram语言模型的核心思想：收集不同n-gram出现频率的统计数据，并用这些数据来预测下一个词。

Ref: https://devopedia.org/n-gram-model

### 6.2 链式法则应用 (Chain Rule Application)

![Page 19](lecture5_slides_pages/page_019.png)

**N-gram Language Modeling…** — N-gram语言建模……

- For example, if we have sequence of tokens, then the probability to see these tokens in this order is: — 例如，如果我们有一个token序列，那么按此顺序看到这些token的概率是：
- Using chain Rule → This is what our LM provides — 使用链式法则 → 这就是我们的语言模型提供的

### 6.3 马尔可夫假设 (Markov Assumption)

![Page 20](lecture5_slides_pages/page_020.png)

**Language Modeling: n-gram…** — 语言建模：n-gram……

- n-1 words → Our assumption — n-1个词 → 我们的假设（马尔可夫假设：下一个词只依赖前n-1个词）
- Recall the definition of conditional probabilities: — 回忆条件概率的定义：
  - p(B|A) = P(A,B)/P(A)
  - P(A,B) = P(A)P(B|A)

### 6.4 4-gram示例 (4-gram Example)

![Page 21](lecture5_slides_pages/page_021.png)

**n-gram Language Models: Example using 4-gram** — n-gram语言模型：使用4-gram的示例

- "as the proctor started the clock the students opened their ______" — "当监考老师启动计时器后，学生们打开了他们的______"
  - discard (丢弃前面的词) → fixed window (固定窗口)
- For example, suppose that in the corpus: — 例如，假设在语料库中：
  - "students opened their" occurred 1000 times — "students opened their"出现了1000次
  - "students opened their books" occurred 400 times — "students opened their books"出现了400次
  - ➔ P(books | students opened their) = 0.4
  - "students opened their exams" occurred 100 times — "students opened their exams"出现了100次
  - ➔ P(exams | students opened their) = 0.1

### 6.5 N-gram局限性 (N-gram Limitations)

![Page 22](lecture5_slides_pages/page_022.png)

**N-grams: limitations and challenges** — N-gram：局限性与挑战

- **Data Sparsity** — **数据稀疏**：很多n-gram组合在训练语料中从未出现
- **Computational Complexity** — **计算复杂度**：n越大，存储和计算需求越高
- **Context Limitations** — **上下文限制**：只能看到固定窗口内的n-1个词，无法捕获更远的依赖关系

> **📝 Notes:**
>
> **承接**: 上一节定义了语言模型的目标——预测下一个词；本节将概率链式法则具体化为N-gram统计方法，但也暴露了数据稀疏和上下文窗口固定的根本缺陷，这些缺陷推动了下一节「神经网络语言模型」的出现。

---

## 7. 神经网络语言模型 (Neural Network Based Language Models)

### 7.1 神经网络快速回顾 (Quick Review of Neural Nets)

![Page 23](lecture5_slides_pages/page_023.png)

**Neural Network Based Language Models** — 基于神经网络的语言模型

![Page 24](lecture5_slides_pages/page_024.png)

**A Quick Review Of Neural Nets:** — 神经网络快速回顾：

- **Input layer** is a set of features; each arrow represents a weight (float number) that tells us how much each input contributes to each following step. — **输入层**是一组特征；每个箭头代表一个权重（浮点数），告诉我们每个输入对下一步的贡献
- Each node in the **hidden layer** is some combination of all the inputs. The hidden layer acts as the 'input' for the output layer. — **隐藏层**的每个节点是所有输入的某种组合。隐藏层作为输出层的"输入"
- **Backpropagation** allows us to adjust the weights to improve accuracy and find the 'correct' way to combine the inputs and hidden layers to get the best possible results. — **反向传播**允许我们调整权重以提高准确性

### 7.2 感知器 (Perceptron)

![Page 25](lecture5_slides_pages/page_025.png)

**NN basic element: Perceptron or Neuron** — 神经网络基本元素：感知器/神经元

> 📖 **图解读笔记：**
>
> | 符号 | 含义 |
> |------|------|
> | x₁, x₂, …, xₘ | 输入属性值 (Input attribute values) |
> | w₁, w₂, …, wₘ | 权重 (Weights) |
> | b (bias) | 偏置项 |
> | Σ (Summing function) | 加权求和函数：v = Σwⱼxⱼ + b |
> | Activation function | 激活函数：将加权求和的结果映射到输出 |
> | y | 输出类别 (Output class) |
>
> **阅读顺序**: 从左到右——输入 → 加权求和 → 激活函数 → 输出
>
> **人话解释**: 感知器就是一个最简单的"决策单元"——把所有输入乘以权重加起来，通过一个激活函数决定输出什么。

### 7.3 前馈神经网络语言模型 (Feed-Forward NN Language Model)

![Page 26](lecture5_slides_pages/page_026.png)

**Language Model: Neural Nets** — 神经网络语言模型

- "as the proctor started the clock the students opened their ______?______" — 与N-gram类似的预测任务
- discard (丢弃) → fixed window (固定窗口) — 仍然使用固定大小的上下文窗口

![Page 27](lecture5_slides_pages/page_027.png)

**Language Model: Neural Nets …** — 神经网络语言模型架构

> 📖 **图解读笔记：**
>
> | 层级 | 含义 |
> |------|------|
> | words / one-hot vectors | 输入词的独热向量 |
> | concatenated word embeddings | 拼接后的词嵌入向量 |
> | hidden layer | 隐藏层 |
> | output distribution | 输出概率分布（所有词的概率）|
>
> **阅读顺序**: 从下到上——输入词 → 嵌入查找 → 拼接 → 隐藏层 → softmax输出
>
> **人话解释**: 把上下文窗口中的每个词转换成嵌入向量，拼接在一起，通过隐藏层计算，最终输出每个候选词的概率。

Ref: Stanford's "Natural Language Processing with Deep Learning" course

### 7.4 前馈神经网络的局限性 (Feed-Forward NN Limitations)

![Page 28](lecture5_slides_pages/page_028.png)

**Feed Forward NN: Limitation...** — 前馈神经网络的局限性……

- Fixed window size — 固定窗口大小：丢弃窗口外的上下文信息

![Page 29](lecture5_slides_pages/page_029.png)

**Feed Forward NN: Limitation** — 前馈神经网络局限性

- "The food was good, not bad at all" — "食物很好，一点也不差"
- "The food was bad, not good at all" — "食物很差，一点也不好"
- → 固定窗口无法区分这两句的不同语义，因为窗口可能只看到局部片段

![Page 30](lecture5_slides_pages/page_030.png)

**Feed Forward NN: Limitation…** — 前馈神经网络局限性……

- "Just watched the new movie. Loved it! #entertained" — 短文本
- "The storyline was captivating, the characters were well-developed, and the cinematography was impressive. Overall, a fantastic movie night! #movienight #recommend" — 长文本
- → 固定窗口无法处理**可变长度**的输入序列

> **📝 Notes:**
>
> **承接**: 上一节展示了N-gram的统计局限；本节引入神经网络语言模型作为改进方案——使用嵌入向量和隐藏层替代简单的频率统计，但前馈网络仍受限于固定窗口大小和无法处理变长序列的问题，这直接激发了下一节「序列建模与RNN」的需求。

---

## 8. 序列建模动机 (Sequence Modeling Motivations)

![Page 31](lecture5_slides_pages/page_031.png)

**Sequence Modeling: Motivations** — 序列建模的动机

- **Handle variable length sequence data** — **处理可变长度的序列数据**
- **Track long term dependency** — **追踪长距离依赖关系**
- **Maintain information about order** — **保持词序信息**
- **Share information across the sequence** — **在序列中共享信息**

![Page 32](lecture5_slides_pages/page_032.png)

**DNN: Universal Approximation Theorem (UAT)** — 深度神经网络：万能逼近定理

- proven by George Cybenko in 1989 — 由George Cybenko于1989年证明

> **📝 Notes:**
>
> **承接**: 上一节暴露了前馈神经网络处理序列的固有缺陷（固定窗口、不能处理变长输入）；本节明确了序列建模的四大需求（变长、长距离依赖、词序、信息共享），为下一节「RNN」的架构设计提供了目标。

---

## 9. 循环神经网络 (Recurrent Neural Networks — RNNs)

### 9.1 RNN核心思想 (Core Idea)

![Page 33](lecture5_slides_pages/page_033.png)

**Core idea of Recurrent Neural Networks (RNNs):** Stateful computation — RNN核心思想：有状态的计算

> 📖 **图解读笔记：**
>
> | 符号 | 含义 |
> |------|------|
> | xₜ | 时间步t的输入 (Input at time step t) |
> | hₜ | 时间步t的隐藏状态 (Hidden state at time t) |
> | yₜ | 时间步t的输出 (Output at time t) |
> | 循环箭头 | 隐藏状态从上一时间步传递到当前时间步 |
>
> **人话解释**: RNN的核心在于"状态记忆"——每一步的计算不仅依赖当前输入，还依赖前一步的隐藏状态，这让网络能够"记住"之前看过的信息。
>
> yₜ, hₜ = f(xₜ, hₜ₋₁)

![Page 34](lecture5_slides_pages/page_034.png)

**Core idea of RNNs — Unrolled view:** — RNN展开视图：

> 📖 **图解读笔记：**
>
> | 符号 | 含义 |
> |------|------|
> | h₀, h₁, …, hₜ | 各时间步的隐藏状态序列 |
> | x₁, …, xₜ | 各时间步的输入序列 |
> | y₁, …, yₜ | 各时间步的输出序列 |
>
> **阅读顺序**: 从左到右，每个时间步接收当前输入xₜ和前一步隐藏状态hₜ₋₁
>
> **公式**: hₜ = W_xh · xₜ + W_hh · hₜ₋₁ + b
>
> **人话解释**: 把循环展开后，RNN就是一条链——每一步都把当前输入和上一步的"记忆"结合起来，产生新的"记忆"和输出。同一组权重（W_xh, W_hh）在所有时间步共享。

### 9.2 RNN训练过程 (Training RNN Language Model)

![Page 35](lecture5_slides_pages/page_035.png)

**How we train the model:** — 如何训练模型：

- Loss = negative log probability of "students" — 损失 = "students"的负对数概率
- Corpus: "the students opened their exams …" — 语料库示例

![Page 36](lecture5_slides_pages/page_036.png)

**Training step — predicting "opened":** Loss = negative log prob of "opened" — 训练步骤——预测"opened"：损失=负对数概率

![Page 37](lecture5_slides_pages/page_037.png)

**Training step — predicting "their":** Loss = negative log prob of "their" — 训练步骤——预测"their"

![Page 38](lecture5_slides_pages/page_038.png)

**Training step — predicting "exams":** Loss = negative log prob of "exams" — 训练步骤——预测"exams"

![Page 39](lecture5_slides_pages/page_039.png)

**Overall training loss:** Sum of all individual losses across the sequence. — 总体训练损失：序列中所有单步损失的总和。

> 📖 **图解读笔记：**
>
> | 元素 | 含义 |
> |------|------|
> | Predicted probability distribution | 每一步的预测词概率分布 |
> | Loss (各步) | 各步的负对数概率（cross-entropy loss） |
> | 总 Loss | 所有步骤损失之和 |
>
> **人话解释**: 训练时，RNN逐词读入语料，每一步都预测下一个词，用"实际下一个词"的负对数概率作为损失。所有步骤的损失加起来就是总损失，通过反向传播优化权重。

Ref: Stanford's "Natural Language Processing with Deep Learning" course

### 9.3 RNN语言模型架构 (RNN Language Model Architecture)

![Page 40](lecture5_slides_pages/page_040.png)

**Language Model: RNN** — RNN语言模型架构

> 📖 **图解读笔记：**
>
> | 层级 | 含义 |
> |------|------|
> | word embeddings | 词嵌入向量（底层） |
> | hidden states | 隐藏状态（中层），h₀是初始隐藏状态 |
> | output distribution | 输出概率分布（顶层）|
>
> **人话解释**: 与前馈NN不同，RNN的隐藏状态会逐词传递——每看一个词，隐藏状态就"更新"一次，最终输出基于**整个**已读序列的上下文信息。

### 9.4 NN与RNN的区别 (Difference between NN and RNN)

![Page 41](lecture5_slides_pages/page_041.png)

**Difference between NN and RNN:** — NN与RNN的区别：

- **Traditional NN for LM:** Fixed-size input, no memory across time steps — 传统NN用于语言模型：固定大小输入，时间步之间没有记忆
- **RNN for LM:** Variable-length input, hidden state carries memory — RNN用于语言模型：可变长度输入，隐藏状态携带记忆

Ref: NLP in Action text book, O'Reilly

![Page 42](lecture5_slides_pages/page_042.png)

**Fun With RNN Language Model:** — RNN语言模型的有趣应用：

Ref: https://medium.com/@samim/obama-rnn-machine-generated-political-speeches-c8abd18a2ea0

> **📝 Notes:**
>
> **承接**: 上一节提出了序列建模的四大需求；本节介绍了RNN如何通过"有状态计算"满足这些需求——隐藏状态在时间步之间传递，实现变长输入和信息共享。但RNN在训练中面临梯度消失问题，这将在下一节中详细讨论。

---

## 10. 反向传播与梯度消失 (Backpropagation & Vanishing Gradient)

### 10.1 BPTT (Backpropagation Through Time)

![Page 43](lecture5_slides_pages/page_043.png)

**Back Propagation in RNN:** Backpropagation Through Time (BPTT). — RNN中的反向传播：时间反向传播（BPTT）。

### 10.2 梯度消失直觉 (Vanishing Gradient Intuition)

![Page 44](lecture5_slides_pages/page_044.png)

**RNN Vanishing Gradient Intuition:** — RNN梯度消失直觉

![Page 45](lecture5_slides_pages/page_045.png)

**Vanishing gradient intuition** — 梯度消失直觉

![Page 46](lecture5_slides_pages/page_046.png)

**Vanishing gradient intuition** — 梯度消失直觉（续）

![Page 47](lecture5_slides_pages/page_047.png)

**Vanishing gradient intuition** — 梯度消失直觉（续）

![Page 48](lecture5_slides_pages/page_048.png)

**Vanishing gradient intuition** — 梯度消失直觉（续）

![Page 49](lecture5_slides_pages/page_049.png)

**Vanishing gradient intuition** — 梯度消失直觉（续）

> 📖 **图解读笔记：**
>
> **阅读顺序**: 从Page 44到Page 49是一组连续动画，逐步展示梯度在时间步之间传播时的衰减过程。
>
> **人话解释**: 反向传播时，梯度需要从最后一个时间步一路传回第一个时间步。每经过一个时间步，梯度都要乘以一个权重矩阵，如果这个值小于1，多次相乘后梯度会指数级衰减——这就是"梯度消失"。结果是：网络无法学习到远距离的依赖关系。

Ref: Stanford's "Natural Language Processing with Deep Learning" course

### 10.3 为什么梯度消失是个问题 (Why It's a Problem)

![Page 50](lecture5_slides_pages/page_050.png)

**Why Vanishing Gradients is Problem:** — 为什么梯度消失是个问题：

Vanishing gradients occur when the values of a gradient are too small and the model stops learning or takes way too long as a result. — 当梯度值太小时，模型停止学习或学习速度变得极慢。

> 📖 **图解读笔记：**
>
> | 位置 | 梯度大小 |
> |------|----------|
> | 靠近输出层 | 梯度较大（Learning Rate 大） |
> | 靠近输入层 | 梯度接近零（Learning Rate ≈ 0） |
>
> **人话解释**: 越靠近输入层，梯度越小，权重几乎不更新，导致前面的层"学不到东西"。

### 10.4 梯度消失实例 (Vanishing Gradient Example)

![Page 51](lecture5_slides_pages/page_051.png)

**Vanishing Gradients Problem — Example:** — 梯度消失问题实例：

- "When she tried to print her tickets, she found that the printer was out of toner. She went to the stationery store to buy more toner. It was very overpriced. After installing the toner into the printer, she finally printed her ______" — 长文本中需要关联"tickets"（第7个词）和最终的预测目标
- RNN-LM needs to model the dependency between "tickets" on the 7th step and the target word "tickets" at the end — RNN需要建模第7步的"tickets"与末尾目标词"tickets"之间的依赖关系
- → 由于梯度消失，RNN很难学到这种远距离的依赖

> **📝 Notes:**
>
> **承接**: 上一节展示了RNN的优势——通过隐藏状态记忆过去的信息；本节揭示了RNN的致命弱点——BPTT中的梯度消失使得网络无法学习长距离依赖（如相隔几十步的"tickets"关联）。这个问题直接催生了下一节「LSTM」的门控机制设计。

---

## 11. 长短期记忆网络 (Long Short-Term Memory — LSTM)

### 11.1 LSTM概述 (LSTM Overview)

![Page 52](lecture5_slides_pages/page_052.png)

**Long Short-Term Memory (LSTM):** — 长短期记忆网络：

- Hochreiter & Schmidhuber (1997) solved the problem of getting an RNN to remember things for a long time. — Hochreiter和Schmidhuber（1997）解决了让RNN长期记忆的问题。
- At each timestep t, the LSTM maintains two key components: — 在每个时间步t，LSTM维护两个关键组件：
  - **Hidden state** – captures short-term dependencies — **隐藏状态** — 捕获短期依赖
  - **Cell state** – acts as a memory unit, storing long-term information — **细胞状态** — 作为记忆单元，存储长期信息

### 11.2 三大门控机制 (Three Gate Mechanisms)

![Page 53](lecture5_slides_pages/page_053.png)

**Long Short-Term Memory (LSTM) — Key Concepts:** — LSTM关键概念：

Unlike standard RNNs, LSTMs can control the flow of information through three specialized gates: — 与标准RNN不同，LSTM通过三个专门的门来控制信息流：

- **Forget gate** – decides which information to erase — **遗忘门** — 决定擦除哪些信息
- **Input gate** – determines what new information should be stored — **输入门** — 决定存储哪些新信息
- **Output gate** – regulates what information is passed to the next timestep — **输出门** — 调节哪些信息传递到下一个时间步

Each gate is represented as a vector of size n and can take values between 0 (closed) and 1 (open) dynamically, based on the current context. — 每个门表示为大小为n的向量，可以根据当前上下文在0（关闭）和1（打开）之间动态取值。

### 11.3 LSTM架构图 (LSTM Architecture Diagram)

![Page 54](lecture5_slides_pages/page_054.png)

**Long Short-Term Memory (LSTM):** LSTM at time stamp T — LSTM在时间步T的架构图

> 📖 **图解读笔记：**
>
> | 符号/颜色 | 含义 |
> |-----------|------|
> | σ (sigmoid) | 门控激活函数，输出0~1之间的值 |
> | tanh | 生成候选值，输出-1~1之间的值 |
> | × (pointwise multiply) | 逐元素乘法（门控操作） |
> | + (pointwise add) | 逐元素加法（信息合并） |
> | Cₜ₋₁ → Cₜ | 细胞状态（长期记忆通道） |
> | hₜ₋₁ → hₜ | 隐藏状态（短期记忆/输出） |
>
> **阅读顺序**: 先看顶部的细胞状态通道（横向直线），再看底部三个门的计算
>
> **人话解释**: LSTM的精髓在于细胞状态（Cell State）——一条信息高速公路，只通过简单的加法和乘法操作，信息可以几乎无损地沿着这条通道传播很远。三个门就像三个"阀门"，控制什么该忘、什么该记、什么该输出。

Ref: https://towardsdatascience.com/lstm-networks-a-detailed-explanation-8fae6aefc7f9

### 11.4 LSTM三步计算 (LSTM Three-Step Computation)

**Step 1 — Forget Gate (遗忘门):**

![Page 55](lecture5_slides_pages/page_055.png)

**Long Short Term Memory (LSTM): step 1** — LSTM步骤1

- **Forget gate:** decide what parts of old state to forget — **遗忘门：** 决定遗忘旧状态的哪些部分
- fₜ = σ(Wf · [hₜ₋₁, xₜ] + bf) — fₜ输出0~1之间的值，0=完全遗忘，1=完全保留

**Step 2 — Input Gate (输入门):**

![Page 56](lecture5_slides_pages/page_056.png)

**Long Short Term Memory (LSTM): step 2** — LSTM步骤2

- **Input gate:** decide how to update the cell state — **输入门：** 决定如何更新细胞状态
- iₜ = σ(Wi · [hₜ₋₁, xₜ] + bi) — 输入门决定哪些值需要更新
- c̃ₜ = tanh(Wc · [hₜ₋₁, xₜ] + bc) — 候选细胞状态
- Cₜ = fₜ ⊙ Cₜ₋₁ + iₜ ⊙ c̃ₜ — 新细胞状态 = 遗忘旧信息 + 写入新信息

**Step 3 — Output Gate (输出门):**

![Page 57](lecture5_slides_pages/page_057.png)

**Long Short Term Memory (LSTM): step 3** — LSTM步骤3

- Finally, decide what to output as hidden state — 最后，决定输出什么作为隐藏状态
- oₜ = σ(Wo · [hₜ₋₁, xₜ] + bo) — 输出门
- hₜ = oₜ ⊙ tanh(Cₜ) — 隐藏状态 = 输出门 × tanh(细胞状态)

### 11.5 LSTM完整流程总结 (Complete LSTM Flow Summary)

![Page 58](lecture5_slides_pages/page_058.png)

**Long Short Term Memory (LSTM):** Complete flow diagram — 完整流程图

> 📖 **图解读笔记：**
>
> | 操作步骤 | 描述 |
> |----------|------|
> | ① Compute the forget gate | 计算遗忘门 |
> | ② Compute the input gate | 计算输入门 |
> | ③ Compute the new cell content | 计算新的细胞内容 |
> | ④ Forget some cell content | 遗忘部分细胞内容 |
> | ⑤ Write some new cell content | 写入新的细胞内容 |
> | ⑥ Compute the output gate | 计算输出门 |
> | ⑦ Output some cell content to the hidden state | 将部分细胞内容输出到隐藏状态 |
>
> **人话解释**: LSTM每一步做三件事：①决定忘什么（遗忘门）；②决定记什么新东西（输入门+候选值）；③决定输出什么（输出门）。细胞状态像一条传送带，信息可以沿它长距离传播，解决了RNN的梯度消失问题。

### 11.6 LSTM资源与Keras实现 (Resources & Keras Implementation)

![Page 59](lecture5_slides_pages/page_059.png)

**LSTM Great resources:** — LSTM优质资源：

Ref: https://colah.github.io/posts/2015-08-Understanding-LSTMs/

![Page 60](lecture5_slides_pages/page_060.png)

**Keras — Simplifying LSTMs in Python:** — Keras：简化Python中的LSTM实现

Keras is a Python package that makes building and training TensorFlow neural networks really simple. We'll be working with the "Sequential" model which lets you add layers one at a time. — Keras是简化TensorFlow神经网络构建和训练的Python包。

```python
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

model = Sequential()
model.add(LSTM(10, input_shape=(TIMESTEPS, FEATURE_LENGTH)))  # 10个隐藏节点的单层LSTM
model.add(Dense(NUMBER_OF_OUTPUT_NODES))  # 输出层
model.add(Activation('softmax'))  # softmax激活函数
```

> **📝 Notes:**
>
> **承接**: 上一节揭示了RNN的梯度消失问题——无法学习长距离依赖；本节介绍了LSTM通过细胞状态和三大门控机制（遗忘门、输入门、输出门）解决了这个问题。LSTM的门控设计让信息可以选择性地保留或遗忘，使网络能够"记住"几十甚至上百步之前的关键信息。Keras提供了简洁的API来实现LSTM。

---

## 12. 语言模型评估 (Evaluating Language Models)

![Page 61](lecture5_slides_pages/page_061.png)

**Evaluating Language Models:** — 评估语言模型：

- The standard evaluation metric for Language Models is **perplexity**. — 语言模型的标准评估指标是**困惑度（Perplexity）**。
- Normalized by number of words — 按词数归一化
- Inverse probability of corpus, according to Language Model — 语料库的逆概率
- → **Low perplexity** → the model predicts the text well — → **低困惑度** → 模型很好地预测了文本
- → **High perplexity** → the text is unexpected for the model — → **高困惑度** → 文本对模型来说是意外的
- **Perplexity (PPL)** measures how confused a language model is when predicting the next word in a sentence. — **困惑度（PPL）** 衡量语言模型在预测句子中下一个词时有多"困惑"。

> **📝 Notes:**
>
> **承接**: 前面各节完成了从N-gram到RNN再到LSTM的语言模型演进；本节介绍了统一的评估标准——困惑度（Perplexity），PPL越低表示模型预测能力越强。这个指标将在后续课程中反复用于比较不同模型的性能。

---

## 13. 本周总结 (Week Summary)

![Page 62](lecture5_slides_pages/page_062.png)

**Summary:** — 总结：

- We introduced the concepts of recurrent neural networks and how it can be applied to language problems. — 介绍了循环神经网络的概念及其在语言问题中的应用
- RNNs can be trained with a straightforward extension of the backpropagation algorithm. — RNN可以通过反向传播算法的直接扩展来训练
- How LSTM used for text generation — LSTM如何用于文本生成
- Applications of LSTM for sequence-to-sequence modeling — LSTM在序列到序列建模中的应用

![Page 63](lecture5_slides_pages/page_063.png)

**Q&A** — 问答环节

> **📝 Notes:**
>
> **承接**: 本节回顾了本周从文本收集→概率基础→N-gram→前馈NN→RNN→LSTM的完整演进路线；Week 6将进入更高级的架构——Bi-LSTM、Seq2Seq、Attention机制和Transformer。
