# Week 5: 语言模型导论 (Introduction to Language Model)

> Source: `lecture_5_W26.pdf`
> Total slides: 63
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程 (Lesson Agenda)

![Page 1](lecture5_slides_pages/page_001.png)

**CST8507: Natural Language Processing — Week #5: Introduction to Language Model** — CST8507自然语言处理，第5周：语言模型导论

![Page 2](lecture5_slides_pages/page_002.png)

**Lesson Agenda:** — 本节课议程：

- Lab — 实验
- Text Collection (overview) — 文本收集（概述）
- Language Model — 语言模型
- N-gram — N元语法
- NN Language model — 神经网络语言模型
- Recurrent Neural Networks RNN — 循环神经网络RNN
- LSTMs — 长短时记忆网络

---

## 2. 文本收集 (Text Collection)

### 2.1 NLP开发生命周期 (NLP Development Life Cycle)

![Page 3](lecture5_slides_pages/page_003.png)

**NLP Development Life Cycle:** Circular pipeline diagram showing iterative stages: Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model. — NLP开发生命周期循环流程图。

### 2.2 社交平台数据 (Social Media Data)

![Page 4](lecture5_slides_pages/page_004.png)

**Data generated in one minute on various social platforms:** Infographic showing massive volumes of data produced each minute across platforms. — 各社交平台每分钟生成的数据量信息图。

Ref: https://localiq.com/blog/what-happens-in-an-internet-minute/

### 2.3 推文收集与X API (Tweet Collecting & X API)

![Page 5](lecture5_slides_pages/page_005.png)

**Text Collection:** Tweet Collecting, X API — 文本收集：推文收集，X API

![Page 6](lecture5_slides_pages/page_006.png)

**Create X Developer Account:** Reference link for creating a developer account to access X API. — 创建X开发者账户。

Ref: https://help.rssground.com/articles/233141-how-to-create-x-twitter-developer-app

### 2.4 网页抓取 (Web Scraping)

![Page 7](lecture5_slides_pages/page_007.png)

**Web Scraping: Extraction of data from a website** — 网页抓取：从网站提取数据

- **Beautiful Soup:** Popular library for parsing HTML and XML documents — 流行的HTML/XML解析库
- **lxml:** Known for its speed, one of the fastest parsing libraries — 以速度闻名的解析库
- **html5lib:** Pure-Python library conforming to WHATWG HTML specification — 纯Python库，遵循WHATWG规范

![Page 8](lecture5_slides_pages/page_008.png)

**Demo:** In-class code demonstration. — 课堂代码演示。


---

## 3. 概率论回顾 (Probability Theory Reminder)

![Page 9](lecture5_slides_pages/page_009.png)

**Reminder: Probability Theory** — 回顾：概率论

### 3.1 有放回抽样 (Sampling with Replacement)

![Page 10](lecture5_slides_pages/page_010.png)

**Basic Probability Theory: Sampling with replacement** — 基础概率论：有放回抽样

Pick a random shape, then put it back in the bag. Examples of probability calculations with shapes and colors. — 随机挑选一个形状，然后放回袋中。使用形状和颜色进行概率计算的例子。

![Page 11](lecture5_slides_pages/page_011.png)

**Sampling with replacement — Sequence probability:** The probability of drawing a specific sequence is the product of individual probabilities. — 抽取特定序列的概率是各个概率的乘积。

### 3.2 条件概率 (Conditional Probability)

![Page 12](lecture5_slides_pages/page_012.png)

**Conditional Probability:** P(X|Y) = P(X, Y) / P(Y) — The probability that one event occurs given that another event has already occurred. — 条件概率：在另一事件已发生的情况下，某事件发生的概率。

### 3.3 链式法则 (Chain Rule of Probability)

![Page 13](lecture5_slides_pages/page_013.png)

**Chain Rule of Probability:** The chain rule expresses a joint probability as a product of conditional probabilities. For a sequence of events X1, X2, ..., Xn: P(X1, X2, ..., Xn) = P(X1) _ P(X2|X1) _ P(X3|X1,X2) \* ... — 链式法则将联合概率表示为条件概率的乘积。


---

## 4. 语言建模 (Language Modeling)

### 4.1 语言模型定义 (Definition)

![Page 14](lecture5_slides_pages/page_014.png)

**Language Modeling** — 语言建模

![Page 15](lecture5_slides_pages/page_015.png)

**Language Modeling: the task of predicting what word comes next** — 预测下一个词的任务

- "the students opened their \_\_\_" -> books / minds / exams / laptops — 示例：给定上下文预测下一个词
- Given a sequence of words, compute the probability distribution of the next word — 给定词序列，计算下一个词的概率分布
- A system that does this is called a **Language Model** — 执行此任务的系统称为**语言模型**

### 4.2 语言模型应用 (Popular Usages)

![Page 16](lecture5_slides_pages/page_016.png)

**Popular Usages:** Applications of language models in real-world tasks. — 语言模型的实际应用。

### 4.3 语言建模目标 (Goal of Language Modeling)

![Page 17](lecture5_slides_pages/page_017.png)

**Goal of Language Modeling:** Learn patterns in text and predict the next word (or sequence of words) based on prior context. — 目标：学习文本中的模式，基于先前上下文预测下一个词（或词序列）。


---

## 5. N-gram语言模型 (N-gram Language Modeling)

### 5.1 N-gram基本思想 (N-gram Basic Idea)

![Page 18](lecture5_slides_pages/page_018.png)

**N-gram Language Modeling:** IDEA: Collect statistics about how frequent different n-grams are, and use these to predict next word. — 思想：收集不同n-gram的频率统计，用这些来预测下一个词。

Ref: https://devopedia.org/n-gram-model

### 5.2 N-gram与链式法则 (N-gram & Chain Rule)

![Page 19](lecture5_slides_pages/page_019.png)

**N-gram Language Modeling:** For a sequence of tokens, the probability is computed using the chain rule. The LM provides the conditional probability at each step. — 对于token序列，使用链式法则计算概率。

![Page 20](lecture5_slides_pages/page_020.png)

**Language Modeling: N-gram -- Markov Assumption:** We approximate by only looking at the preceding n-1 words instead of the full history. P(wt | w1...wt-1) approx P(wt | wt-n+1...wt-1). Recall conditional probability: P(B|A) = P(A,B)/P(A). — 马尔可夫假设：只看前n-1个词来近似。

### 5.3 4-gram示例 (4-gram Example)

![Page 21](lecture5_slides_pages/page_021.png)

**N-gram Language Models: Example using 4-gram** — 4-gram示例：

- "as the proctor started the clock the students opened their \_\_\_" — 示例句子
- Discard all but the last 3 words (fixed window of n-1=3) — 丢弃除最后3个词外的所有词
- In the corpus: "students opened their" occurred 1000 times — 在语料库中出现1000次
- "students opened their books" occurred 400 times -> P(books | students opened their) = 0.4
- "students opened their exams" occurred 100 times -> P(exams | students opened their) = 0.1

### 5.4 N-gram局限性 (N-gram Limitations)

![Page 22](lecture5_slides_pages/page_022.png)

**N-grams: Limitations and Challenges** — N-gram的局限性与挑战：

- **Data Sparsity** — 数据稀疏性
- **Computational Complexity** — 计算复杂度
- **Context Limitations** — 上下文限制


---

## 6. 神经网络语言模型 (Neural Network Language Models)

### 6.1 神经网络回顾 (Neural Nets Quick Review)

![Page 23](lecture5_slides_pages/page_023.png)

**Neural Network Based Language Models** — 基于神经网络的语言模型

![Page 24](lecture5_slides_pages/page_024.png)

**A Quick Review Of Neural Nets:** — 神经网络快速回顾：

- **Input layer:** a set of features; each arrow = a weight (float) telling how much each input contributes — 输入层：一组特征；每个箭头 = 一个权重
- **Hidden layer:** some combination of all inputs — 隐藏层：所有输入的某种组合
- **Output layer:** final prediction — 输出层：最终预测
- **Backpropagation:** adjusts weights to improve accuracy — 反向传播：调整权重以提高准确率

### 6.2 感知器 (Perceptron)

![Page 25](lecture5_slides_pages/page_025.png)

**NN basic element: Perceptron / Neuron:** Diagram showing input attributes x1...xm with weights w1...wm, summing function v = sum(wj\*xj) + b, activation function, and output y. — 感知器/神经元：输入属性通过权重求和，经激活函数输出。

### 6.3 固定窗口神经网络LM (Fixed-window NN LM)

![Page 26](lecture5_slides_pages/page_026.png)

**Language Model: Neural Nets:** "as the proctor started the clock the students opened their \_\_\_" — Same problem but now using NN. Discard all but fixed window. — 使用NN解决相同问题，只保留固定窗口。

![Page 27](lecture5_slides_pages/page_027.png)

**Language Model: Neural Nets -- Architecture:** Bottom: words as one-hot vectors ("the students opened their"). Middle: concatenated word embeddings e = [e1;e2;e3;e4]. Hidden layer: h = f(We + b1). Output: y-hat = softmax(Uh + b2) -- probability over entire vocabulary. — 固定窗口NN LM架构图。

**固定窗口NN LM架构图：** 底部为one-hot向量输入，通过嵌入矩阵转为词嵌入，拼接后送入隐藏层，最终softmax输出词汇表上的概率分布。

### 6.4 固定窗口NN的局限 (Fixed-window NN Limitations)

![Page 28](lecture5_slides_pages/page_028.png)

**Feed Forward NN: Limitation** — 前馈NN的局限：Still uses fixed window, discards earlier context. — 仍使用固定窗口，丢弃更早的上下文。

![Page 29](lecture5_slides_pages/page_029.png)

**Feed Forward NN: Limitation -- Sentiment example:** — 情感分析示例：

- "The food was good, not bad at all" (positive) — 正面
- "The food was bad, not good at all" (negative) — 负面
- If the window only sees "not bad at all" vs "not good at all", they look very similar! — 如果窗口只看到最后几个词，两句看起来非常相似！

![Page 30](lecture5_slides_pages/page_030.png)

**Feed Forward NN: Limitation -- Variable length:** Short vs long reviews require different context lengths. — 短评和长评需要不同的上下文长度。


---

## 7. 序列建模动机与UAT (Sequence Modeling Motivations & UAT)

![Page 31](lecture5_slides_pages/page_031.png)

**Sequence Modeling: Motivations** — 序列建模动机：

- Handle variable length sequence data — 处理变长序列数据
- Track long term dependency — 追踪长期依赖
- Maintain information about order — 维护顺序信息
- Share information across the sequence — 在序列中共享信息

![Page 32](lecture5_slides_pages/page_032.png)

**DNN: Universal Approximation Theorem (UAT):** Proven by George Cybenko in 1989. A neural network with a single sufficiently wide hidden layer can approximate any continuous function. — 通用逼近定理：1989年Cybenko证明。


---

## 8. 循环神经网络 (Recurrent Neural Networks -- RNN)

### 8.1 RNN核心思想 (Core Idea of RNN)

![Page 33](lecture5_slides_pages/page_033.png)

**Core idea of RNN: Stateful computation:** Diagram showing RNN cell with input xt, hidden state ht (with self-loop), and output yt. Formula: yt, ht = f(xt, ht-1). The self-loop arrow represents the recurrence. — RNN核心思想：有状态计算。

**RNN核心图：** 输入xt进入RNN单元，结合上一步的隐藏状态ht-1，产生输出yt和新的隐藏状态ht。自循环箭头表示递归。

![Page 34](lecture5_slides_pages/page_034.png)

**Core idea of RNN (unrolled):** Unrolled view showing the same RNN cell replicated at each timestep: h1, h2, ..., ht. Formula: ht = Wh*ht-1 + We*et + b. Same weights Wh are used at EVERY timestep (parameter sharing). — 展开后的RNN：同一RNN单元在每个时间步复制。

### 8.2 RNN语言模型 (RNN Language Model)

![Page 40](lecture5_slides_pages/page_040.png)

**Language Model: RNN -- Full architecture:** Bottom: words ("the students opened their") as one-hot vectors. Word embeddings: e(t) = E*x(t) via embedding matrix E. Hidden states: h(t) = sigma(Wh*h(t-1) + We*e(t) + b1), where h(0) is the initial state. Output: y-hat(t) = softmax(U*h(t) + b2). Same Wh at every step. — RNN LM完整架构图。

**RNN LM架构图：** 底部为one-hot输入，通过嵌入矩阵E转为嵌入。隐藏状态通过Wh在时间步间传递（参数共享）。输出经softmax产生词汇表上的概率。

### 8.3 RNN vs 传统NN (RNN vs Traditional NN)

![Page 41](lecture5_slides_pages/page_041.png)

**Difference between NN and RNN:** Side-by-side comparison. Traditional NN for LM (left) vs RNN for LM (right). Key difference: RNN has recurrent connections that carry information across timesteps. — 传统NN与RNN的区别。

### 8.4 RNN训练 (Training RNN)

![Page 35](lecture5_slides_pages/page_035.png)

![Page 36](lecture5_slides_pages/page_036.png)

![Page 37](lecture5_slides_pages/page_037.png)

![Page 38](lecture5_slides_pages/page_038.png)

**How we train the RNN model:** Step-by-step training on "the students opened their exams": At each timestep, compute loss = negative log probability of the correct next word. Loss at step t = -log P(correct word at t+1). — RNN训练逐步演示。

![Page 39](lecture5_slides_pages/page_039.png)

**Total loss:** J = (1/T) \* sum(Jt) — average of per-step losses over the corpus. — 总损失 = 各步损失的平均值。


---

## 9. 梯度消失问题 (Vanishing Gradient Problem)

### 9.1 时序反向传播 (Backpropagation Through Time -- BPTT)

![Page 43](lecture5_slides_pages/page_043.png)

**Back Propagation in RNN:** Backpropagation Through Time (BPTT). — RNN中的反向传播：时序反向传播。

### 9.2 梯度消失直觉 (Vanishing Gradient Intuition)

![Page 44](lecture5_slides_pages/page_044.png)

![Page 45](lecture5_slides_pages/page_045.png)

![Page 46](lecture5_slides_pages/page_046.png)

![Page 47](lecture5_slides_pages/page_047.png)

![Page 48](lecture5_slides_pages/page_048.png)

![Page 49](lecture5_slides_pages/page_049.png)

**Vanishing gradient intuition:** Step-by-step animation showing how gradients shrink as they flow backward through many timesteps. At each step, the gradient is multiplied by Wh -- if |Wh| < 1, the gradient shrinks exponentially. — 梯度消失直觉：逐步展示梯度在多个时间步中向后流动时如何缩小。

### 9.3 为什么梯度消失是问题 (Why Vanishing Gradient is a Problem)

![Page 50](lecture5_slides_pages/page_050.png)

**Why Vanishing Gradients is Problem:** Vanishing gradients occur when gradient values become too small, causing the model to stop learning or learn extremely slowly. Earlier layers receive exponentially smaller gradients. — 梯度消失导致模型停止学习或极慢学习。

### 9.4 梯度消失实例 (Vanishing Gradient Example)

![Page 51](lecture5_slides_pages/page_051.png)

**Vanishing Gradients Problem -- Example:** "When she tried to print her tickets, she found that the printer was out of toner. She went to the stationery store to buy more toner. It was very overpriced. After installing the toner into the printer, she finally printed her \_\_\_" — The RNN needs to connect "tickets" (7th word) to the prediction at the end. With vanishing gradients, this signal is lost. — RNN需要将"tickets"与结尾的预测连接。梯度消失使这个信号丢失。


---

## 10. 长短时记忆网络 (Long Short-Term Memory -- LSTM)

### 10.1 LSTM简介 (LSTM Introduction)

![Page 52](lecture5_slides_pages/page_052.png)

**Long Short-Term Memory (LSTM):** — LSTM：

- Hochreiter & Schmidhuber (1997) solved the problem of getting an RNN to remember things for a long time — 解决了RNN长期记忆问题
- At each timestep t, LSTM maintains two key components: — 每个时间步维护两个关键组件：
  - **Hidden state** -- captures short-term dependencies — 隐藏状态——捕获短期依赖
  - **Cell state** -- acts as a memory unit, storing long-term information — 细胞状态——充当记忆单元，存储长期信息

### 10.2 LSTM门控机制 (LSTM Gates)

![Page 53](lecture5_slides_pages/page_053.png)

**LSTM Key Concepts -- Three specialized gates:** — 三个专用门：

- **Forget gate** -- decides which information to erase — 遗忘门——决定擦除哪些信息
- **Input gate** -- determines what new information should be stored — 输入门——决定存储什么新信息
- **Output gate** -- regulates what information is passed to the next timestep — 输出门——调节传递到下一时间步的信息
- Each gate takes values between 0 (closed) and 1 (open) dynamically — 每个门的值在0（关）和1（开）之间动态变化

### 10.3 LSTM架构图 (LSTM Architecture Diagram)

![Page 54](lecture5_slides_pages/page_054.png)

**LSTM at time stamp T:** Detailed architecture diagram showing: Previous Cell State -> (x forget) -> (+ new input) -> New Cell State. Previous Hidden State + Input Data -> Forget gate (sigma), Input gate (sigma + tanh), Output gate (sigma). Operations: x = Pointwise Multiplication, + = Pointwise Addition, tanh = Pointwise Tanh, sigma = Sigmoid Activated NN. — LSTM在时间步T的详细架构图。

**LSTM架构图：** 展示细胞状态（顶部传送带）如何通过遗忘门选择性擦除、通过输入门选择性添加新信息。输出门决定隐藏状态中输出细胞状态的哪些部分。

### 10.4 LSTM三步详解 (LSTM Step-by-Step)

![Page 55](lecture5_slides_pages/page_055.png)

**LSTM Step 1 -- Forget gate:** ft = sigma(Wf \* [ht-1, xt] + bf). Decides what parts of old cell state to forget. — 第1步：遗忘门，决定遗忘旧细胞状态的哪些部分。

![Page 56](lecture5_slides_pages/page_056.png)

**LSTM Step 2 -- Input gate:** it = sigma(Wi _ [ht-1, xt] + bi) and c-tilde-t = tanh(Wc _ [ht-1, xt] + bc). Decides what new information to store. ct = ft _ ct-1 + it _ c-tilde-t. — 第2步：输入门，决定存储什么新信息。

![Page 57](lecture5_slides_pages/page_057.png)

**LSTM Step 3 -- Output gate:** ot = sigma(Wo _ [ht-1, xt] + bo). ht = ot _ tanh(ct). Decides what to output as hidden state. — 第3步：输出门，决定输出什么作为隐藏状态。

### 10.5 LSTM完整总结图 (LSTM Complete Summary)

![Page 58](lecture5_slides_pages/page_058.png)

**LSTM Complete Summary:** Annotated diagram showing all operations: Compute the forget gate -> Forget some cell content -> Write some new cell content -> Compute the input gate -> Compute the new cell content -> Compute the output gate -> Output some cell content to the hidden state. — LSTM完整总结注释图。

### 10.6 Keras实现 (Keras Implementation)

![Page 60](lecture5_slides_pages/page_060.png)

**Keras -- Simplifying LSTMs in Python:** — Keras简化LSTM：

```python
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

model = Sequential()
model.add(LSTM(10, input_shape=(TIMESTEPS, FEATURE_LENGTH)))
model.add(Dense(NUMBER_OF_OUTPUT_NODES))
model.add(Activation('softmax'))
```


---

## 11. 语言模型评估 (Evaluating Language Models)

![Page 61](lecture5_slides_pages/page_061.png)

**Evaluating Language Models -- Perplexity:** — 评估语言模型——困惑度：

- The standard evaluation metric for Language Models is **perplexity** — 标准评估指标是**困惑度**
- Formula: perplexity = product over t=1 to T of (1 / P_LM(x(t+1) | x(t),...,x(1)))^(1/T) — normalized by number of words
- **Low perplexity** -> the model predicts the text well — 低困惑度表示模型预测良好
- **High perplexity** -> the text is unexpected for the model — 高困惑度表示文本对模型出乎意料
- Perplexity (PPL) measures **how confused** a language model is when predicting the next word — PPL衡量语言模型预测下一个词时的"困惑程度"


---

## 12. 总结与问答 (Summary & Q&A)

![Page 62](lecture5_slides_pages/page_062.png)

**Summary:** — 总结：

- We introduced the concepts of recurrent neural networks and how they can be applied to language problems — 介绍了循环神经网络及其语言应用
- RNNs can be trained with backpropagation through time (BPTT) — RNN可通过BPTT训练
- How LSTM is used for text generation — LSTM如何用于文本生成
- Applications of LSTM for sequence-to-sequence modeling — LSTM在序列到序列建模中的应用

![Page 63](lecture5_slides_pages/page_063.png)

**Q&A** — 问答环节
