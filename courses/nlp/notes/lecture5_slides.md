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

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Why text collection matters for LM (为什么文本收集对语言模型重要):**
>
> Language models learn patterns from data — the MORE text you feed them, the better they predict. Social media generates billions of words per minute, making it the largest free "training set" on earth.
>
> > 语言模型从数据中学习模式——喂的文本越多，预测越好。社交媒体每分钟产生数十亿词，是地球上最大的免费"训练集"。
>
> **(2) API vs Scraping trade-off (API与抓取的权衡):**
>
> APIs give structured, authorized data but are rate-limited and often costly. Web scraping can access any public page but may violate terms of service. In practice, use APIs when available; fall back to scraping for non-API sources.
>
> > API提供结构化、授权的数据，但有速率限制且通常收费。网页抓取可以访问任何公开页面，但可能违反服务条款。实践中优先用API；非API来源才用抓取。
>
> **💡 Intuition:**
> **(1) Fishing analogy (钓鱼类比):**
>
> API = fishing with a permit at a stocked pond — controlled, reliable, limited. Scraping = fishing in the open ocean — unlimited fish, but you need your own boat and net (parsing tools), and you might get in trouble (legal issues).
>
> > API = 在有许可证的鱼塘钓鱼——可控、可靠、有限。抓取 = 在公海捕鱼——鱼无限多，但你需要自己的船和网（解析工具），还可能惹麻烦（法律问题）。
>
> **⚠️ Pitfall:**
> **(1) robots.txt and rate limits (robots.txt和速率限制):**
>
> Always check a website's `robots.txt` before scraping. Ignoring it can get your IP blocked or lead to legal action. Also respect rate limits — sending 1000 requests/second will get you banned.
>
> > 抓取前务必检查网站的`robots.txt`。忽略它可能导致IP被封或法律问题。也要遵守速率限制——每秒发送1000个请求会被封禁。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Chain rule for language (语言中的链式法则):**
>
> The chain rule is THE mathematical foundation of language modeling. P("the students opened their books") = P("the") x P("students"|"the") x P("opened"|"the students") x P("their"|"the students opened") x P("books"|"the students opened their"). Every LM — from N-gram to GPT — is trying to estimate these conditional probabilities.
>
> > 链式法则是语言建模的数学基础。每个LM——从N-gram到GPT——都在试图估计这些条件概率。
>
> **🎯 Why:**
> **(1) Why probability review before LM (为什么在LM之前回顾概率):**
>
> Language models ARE probability models. A LM assigns a probability to every possible sequence of words. Without understanding conditional probability and chain rule, the math behind every LM technique is incomprehensible.
>
> > 语言模型就是概率模型。LM为每个可能的词序列分配概率。不理解条件概率和链式法则，每种LM技术背后的数学都无法理解。
>
> **💡 Intuition:**
> **(1) Domino chain analogy (多米诺骨牌类比):**
>
> The chain rule is like dominoes: each word's probability depends on all the words that came before it. P("books" | "the students opened their") is one domino — it only falls because all previous dominoes fell in a specific order.
>
> > 链式法则就像多米诺骨牌：每个词的概率取决于它之前的所有词。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Use the chain rule to express P('I love NLP')." -> P("I") x P("love"|"I") x P("NLP"|"I love").
>
> > "用链式法则表达P('I love NLP')。" -> P("I") x P("love"|"I") x P("NLP"|"I love")。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Language Model definition (语言模型定义):**
>
> A Language Model (LM) is a probability distribution over sequences of words. Given context words w1, w2, ..., wt-1, it computes P(wt | w1, ..., wt-1) for every word wt in the vocabulary. The word with highest probability is the model's "prediction."
>
> > 语言模型(LM)是词序列上的概率分布。给定上下文词，它计算词汇表中每个词的条件概率。概率最高的词是模型的"预测"。
>
> **🎯 Why:**
> **(1) Why LMs are the foundation of modern NLP (为什么LM是现代NLP的基础):**
>
> LMs are behind autocomplete, machine translation, speech recognition, text generation, and chatbots. GPT-4, Claude, Gemini — they are ALL language models at their core. Understanding LMs means understanding the engine behind all modern AI assistants.
>
> > LM是自动完成、机器翻译、语音识别、文本生成和聊天机器人的基础。GPT-4、Claude、Gemini——它们的核心都是语言模型。理解LM就是理解所有现代AI助手背后的引擎。
>
> **💡 Intuition:**
> **(1) Autocomplete on your phone (手机自动完成类比):**
>
> Every time your phone suggests the next word while texting, that's a language model. It has learned from billions of texts that after "How are" the most likely next word is "you" (not "dog" or "purple"). That's P("you" | "How are") being very high.
>
> > 每次手机在输入时建议下一个词，那就是语言模型在工作。它从数十亿文本中学到"How are"之后最可能的下一个词是"you"。
>
> **📝 Exam:**
> **(1) 定义题 (Definition):**
>
> "What is a Language Model?" -> A probability distribution over sequences of words that predicts the next word given previous context. Formally: P(wt | w1, ..., wt-1).
>
> > "什么是语言模型？" -> 词序列上的概率分布，给定之前的上下文预测下一个词。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) N-gram model definition (N-gram模型定义):**
>
> An N-gram model predicts the next word using only the previous N-1 words (Markov assumption). Unigram (N=1): P(w) -- no context. Bigram (N=2): P(w|w-1) -- one previous word. Trigram (N=3): P(w|w-2,w-1) -- two previous words. Probabilities are estimated by counting n-gram frequencies in a corpus.
>
> > N-gram模型仅使用前N-1个词（马尔可夫假设）预测下一个词。Unigram(N=1)：无上下文。Bigram(N=2)：一个前词。Trigram(N=3)：两个前词。概率通过统计语料库中n-gram频率来估计。
>
> **🎯 Why:**
> **(1) Why the Markov assumption is necessary (为什么马尔可夫假设必要):**
>
> The chain rule requires P(wt | w1...wt-1) -- conditioning on the ENTIRE history. But most word combinations never appear in any corpus (sparsity). By truncating to n-1 words, we get enough counts to estimate probabilities reliably. The trade-off: longer n = more context but more sparsity.
>
> > 链式法则需要以全部历史为条件。但大多数词组合在语料库中从未出现（稀疏性）。截断到n-1个词，我们获得足够的计数来可靠估计概率。权衡：n越长 = 更多上下文但更稀疏。
>
> **⚙️ How:**
> **(1) N-gram probability calculation (N-gram概率计算):**
>
> P(wt | wt-n+1...wt-1) = Count(wt-n+1...wt) / Count(wt-n+1...wt-1). Example: P(books | students opened their) = Count("students opened their books") / Count("students opened their") = 400/1000 = 0.4.
>
> > P(wt | wt-n+1...wt-1) = Count(wt-n+1...wt) / Count(wt-n+1...wt-1)。示例：P(books | students opened their) = 400/1000 = 0.4。
>
> **💡 Intuition:**
> **(1) Goldfish memory analogy (金鱼记忆类比):**
>
> An N-gram model has the memory of a goldfish -- it only remembers the last N-1 words. A bigram model reading "as the proctor started the clock the students opened their \_\_\_" only sees "their" and predicts from there. All the rich context about proctors and clocks? Gone.
>
> > N-gram模型拥有金鱼般的记忆——只记得最后N-1个词。Bigram模型读到长句时只看到最后一个词来预测。关于监考官和计时器的丰富上下文？全忘了。
>
> **⚖️ Compare:**
> **(1) N-gram size trade-offs (N-gram大小权衡):**
>
> | N   | Name    | Context  | Sparsity  | Example            |
> | --- | ------- | -------- | --------- | ------------------ |
> | 1   | Unigram | None     | None      | P(the)             |
> | 2   | Bigram  | 1 word   | Low       | P(cat\|the)        |
> | 3   | Trigram | 2 words  | Medium    | P(sat\|the cat)    |
> | 4   | 4-gram  | 3 words  | High      | P(on\|the cat sat) |
> | 5+  | 5-gram+ | 4+ words | Very high | Often zero counts  |
>
> > | N   | 名称    | 上下文 | 稀疏性 | 示例               |
> > | --- | ------- | ------ | ------ | ------------------ |
> > | 1   | Unigram | 无     | 无     | P(the)             |
> > | 2   | Bigram  | 1词    | 低     | P(cat\|the)        |
> > | 3   | Trigram | 2词    | 中     | P(sat\|the cat)    |
> > | 4   | 4-gram  | 3词    | 高     | P(on\|the cat sat) |
> > | 5+  | 5-gram+ | 4+词   | 非常高 | 经常零计数         |
>
> **⚠️ Pitfall:**
> **(1) Sparsity = zero probability trap (稀疏性 = 零概率陷阱):**
>
> If "students opened their laptops" never appears in the training corpus, P(laptops | students opened their) = 0. This makes the ENTIRE sentence probability zero, even if every other word is common. Solutions: smoothing (add-k), backoff (fall back to shorter n-gram), interpolation.
>
> > 如果"students opened their laptops"从未出现在训练语料库中，概率为0。这使整个句子概率为零。解决方案：平滑（add-k）、回退、插值。
>
> **(2) N-gram cannot capture semantic similarity (N-gram无法捕获语义相似性):**
>
> N-gram treats "cat" and "dog" as completely different tokens. Even if "the dog barked" appears 1000 times, it tells us NOTHING about P(barked | the cat). There's no notion of word similarity -- this is what neural LMs solve with embeddings.
>
> > N-gram将"cat"和"dog"视为完全不同的token。即使"the dog barked"出现1000次，也不能告诉我们P(barked | the cat)。没有词相似性概念——这是神经LM用嵌入解决的问题。
>
> **📝 Exam:**
> **(1) 计算题 (Calculation):**
>
> "Given corpus counts: 'I love' appeared 100 times, 'I love NLP' appeared 30 times. What is P(NLP | I love)?" -> 30/100 = 0.3.
>
> > "给定语料库计数：'I love'出现100次，'I love NLP'出现30次。P(NLP | I love)是多少？" -> 30/100 = 0.3。
>
> **(2) 概念题 (Conceptual):**
>
> "What are the three main limitations of N-gram LMs?" -> Data sparsity (many n-grams never observed), context limitation (only n-1 words of history), no word similarity (treats each word as independent symbol).
>
> > "N-gram LM的三个主要局限是什么？" -> 数据稀疏性、上下文限制（仅n-1词历史）、无词相似性（将每个词视为独立符号）。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Fixed-window NN LM architecture (固定窗口NN LM架构):**
>
> Input: concatenate embeddings of last n words -> e = [e1;e2;...;en]. Hidden: h = f(We + b1) where f is an activation (tanh/ReLU). Output: y-hat = softmax(Uh + b2) gives probability over vocabulary. Key improvement over N-gram: word embeddings capture semantic similarity.
>
> > 输入：拼接最后n个词的嵌入。隐藏层：h = f(We + b1)。输出：y-hat = softmax(Uh + b2)。相比N-gram的关键改进：词嵌入捕获语义相似性。
>
> **🎯 Why:**
> **(1) Why NN LM improves over N-gram (为什么NN LM优于N-gram):**
>
> N-gram treats "cat" and "dog" as unrelated symbols. NN LM uses word embeddings where similar words have similar vectors. If the model learned P(barked | the dog) is high, it can also predict P(barked | the cat) is not-zero, because "dog" and "cat" have similar embeddings. This solves the sparsity problem.
>
> > N-gram将"cat"和"dog"视为无关符号。NN LM使用词嵌入，相似词有相似向量。这解决了稀疏性问题。
>
> **⚠️ Pitfall:**
> **(1) Fixed window remains a fatal flaw (固定窗口仍是致命缺陷):**
>
> Even with embeddings, the window is FIXED. Enlarging the window means: (1) more parameters in W (scales linearly), (2) window never "large enough" for long documents. No fixed window handles "She put the book that she bought at the store on the \_\_\_" which needs 10+ words of context.
>
> > 即使有嵌入，窗口仍是固定的。扩大窗口意味着更多参数且永远"不够大"。
>
> **(2) "Good not bad" vs "Bad not good" trap ("好不坏" vs "坏不好" 陷阱):**
>
> If the window only sees "not bad at all" vs "not good at all", they look nearly identical. Fixed-window models can't see the EARLIER part of the sentence that reverses the meaning. You need memory of the full sentence.
>
> > 如果窗口只看到最后几个词，两个相反含义的句子看起来几乎相同。固定窗口模型看不到句子前面反转含义的部分。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Four requirements for sequence modeling (序列建模的四个需求):**
>
> These four requirements are exactly what N-gram and fixed-window NN CANNOT satisfy: (1) variable length, (2) long-term dependency, (3) order, (4) parameter sharing. RNN satisfies ALL four.
>
> > 这四个需求正是N-gram和固定窗口NN无法满足的。RNN满足全部四个。
>
> **⚠️ Pitfall:**
> **(1) UAT doesn't guarantee learning (UAT不保证学到):**
>
> UAT says a NN CAN approximate any function -- it doesn't say gradient descent WILL find the right weights. It's an existence theorem, not a learning guarantee.
>
> > UAT说NN能逼近任何函数——不是说梯度下降一定能找到正确权重。这是存在性定理，不是学习保证。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) RNN definition (RNN定义):**
>
> An RNN processes sequences by maintaining a hidden state ht that gets updated at each timestep: ht = sigma(Wh*ht-1 + We*et + b). The SAME weights (Wh, We) are used at every timestep -- this is "parameter sharing." The hidden state acts as a "memory" that carries information from all previous words.
>
> > RNN通过维护隐藏状态ht处理序列。每个时间步使用相同的权重（参数共享）。隐藏状态充当"记忆"，携带来自所有先前词的信息。
>
> **🎯 Why:**
> **(1) Why RNN solves the four sequence requirements (为什么RNN解决了四个序列需求):**
>
> (1) Variable length: RNN processes any number of timesteps -- just keep running. (2) Long-term dependency: hidden state carries info forward indefinitely (in theory). (3) Order: position matters -- h3 differs if words at positions 1-2 differ. (4) Parameter sharing: same Wh at every step -- knowledge at position 5 transfers to position 50.
>
> > (1) 变长：RNN处理任意数量的时间步。(2) 长期依赖：隐藏状态无限向前传递信息（理论上）。(3) 顺序：位置重要。(4) 参数共享：每步相同Wh。
>
> **💡 Intuition:**
> **(1) Assembly line worker analogy (流水线工人类比):**
>
> An RNN is like a worker on an assembly line who processes items one by one. At each position, the worker receives: (1) the new item (input xt), (2) a note from the previous position about what came before (hidden state ht-1). The worker writes a new note (ht) combining both and passes it to the next position. The SAME worker handles every position (parameter sharing).
>
> > RNN就像流水线上的工人，逐个处理物品。每个位置，工人收到新物品和上一位置的便条，写新便条传给下一位置。同一个工人处理每个位置（参数共享）。
>
> **⚖️ Compare:**
> **(1) N-gram vs Fixed-window NN vs RNN (三种方法对比):**
>
> | Feature           | N-gram         | Fixed-window NN  | RNN                        |
> | ----------------- | -------------- | ---------------- | -------------------------- |
> | Word similarity   | None           | Yes (embeddings) | Yes (embeddings)           |
> | Variable length   | No             | No               | Yes                        |
> | Long-range deps   | No (n-1 words) | No (window size) | Yes (hidden state)         |
> | Parameter sharing | N/A            | No               | Yes (same W at every step) |
>
> > | 特性       | N-gram | 固定窗口NN | RNN            |
> > | ---------- | ------ | ---------- | -------------- |
> > | 词相似性   | 无     | 有（嵌入） | 有（嵌入）     |
> > | 变长输入   | 否     | 否         | 是             |
> > | 长距离依赖 | 否     | 否         | 是（隐藏状态） |
> > | 参数共享   | 不适用 | 否         | 是             |
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What is parameter sharing in RNN and why does it matter?" -> The same weight matrices (Wh, We) are used at every timestep. This means: (1) the model can handle any input length with fixed parameters, (2) patterns learned at one position generalize to other positions.
>
> > "RNN中的参数共享是什么，为什么重要？" -> 每个时间步使用相同的权重矩阵。模型用固定参数处理任意长度输入，一个位置学到的模式泛化到其他位置。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) BPTT and vanishing gradient (BPTT和梯度消失):**
>
> In BPTT, gradients flow from the loss at timestep T back to timestep 1. At each step, the gradient is multiplied by dht/dht-1 which involves Wh. If the eigenvalues of Wh < 1, the gradient shrinks exponentially: gradient proportional to (Wh)^T -> 0 as T grows. This means early words have essentially zero influence on the loss.
>
> > 在BPTT中，梯度从时间步T的损失向后流到时间步1。每步梯度乘以涉及Wh的导数。如果Wh特征值<1，梯度指数缩小。这意味着早期词对损失基本没有影响。
>
> **🎯 Why:**
> **(1) Why this is fatal for language (为什么这对语言是致命的):**
>
> Language has LONG-RANGE dependencies. "The cat, which sat on the warm mat in the sunlit room, purred loudly." The verb "purred" depends on "cat" -- 12 words back. If the gradient from "purred" vanishes before reaching "cat", the model CANNOT learn this dependency.
>
> > 语言有长距离依赖。动词"purred"依赖于12个词之前的"cat"。如果梯度在到达"cat"之前消失，模型无法学习这种依赖关系。
>
> **💡 Intuition:**
> **(1) Telephone game analogy (传话游戏类比):**
>
> Vanishing gradient = playing telephone: by the time the message passes through 20 people, it's completely garbled. The gradient signal from step 100 passes through 100 matrix multiplications to reach step 1 -- it gets exponentially weaker at each step.
>
> > 梯度消失 = 传话游戏：消息经过20个人后完全变形。第100步的梯度信号经过100次矩阵乘法才到达第1步——每步都指数减弱。
>
> **⚠️ Pitfall:**
> **(1) Exploding gradient is the opposite problem (梯度爆炸是相反的问题):**
>
> If |Wh| > 1, gradients EXPLODE exponentially instead of vanishing. This causes NaN losses and training crashes. Solution: gradient clipping. Vanishing gradients are harder to fix -- LSTM is the architectural solution.
>
> > 如果|Wh| > 1，梯度指数爆炸。导致NaN损失和训练崩溃。解决方案：梯度裁剪。梯度消失更难修复——LSTM是架构层面的解决方案。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Explain the vanishing gradient problem in RNNs." -> During BPTT, gradients are multiplied by Wh at each timestep. If |Wh| < 1, gradients shrink exponentially, preventing the model from learning long-range dependencies. Solution: LSTM with its cell state "conveyor belt."
>
> > "解释RNN中的梯度消失问题。" -> BPTT中，梯度在每个时间步乘以Wh。如果|Wh| < 1，梯度指数缩小。解决方案：LSTM及其细胞状态"传送带"。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) LSTM cell state = long-term memory (LSTM细胞状态 = 长期记忆):**
>
> The cell state ct is a vector that flows through time with only minor linear interactions (pointwise multiply and add). This "conveyor belt" allows information to pass unchanged across many timesteps. The three gates control what gets on/off this conveyor belt. This is how LSTM solves the vanishing gradient problem -- gradients can flow along the cell state without exponential decay.
>
> > 细胞状态ct是一个向量，仅通过少量线性交互在时间中流动。这条"传送带"允许信息不变地跨越多个时间步。三个门控制什么上/下传送带。这就是LSTM如何解决梯度消失。
>
> **🎯 Why:**
> **(1) Why three gates instead of one (为什么需要三个门而非一个):**
>
> Each gate serves a distinct purpose: Forget gate = "should I keep remembering the subject 'cat' from 20 words ago?" Input gate = "this new word 'dog' is important, should I memorize it?" Output gate = "I need to predict a verb -- should I use the subject info in my memory?" Without separate gates, the model can't independently control reading, writing, and erasing memory.
>
> > 每个门有不同目的：遗忘门决定是否继续记住旧信息。输入门决定是否记忆新信息。输出门决定是否使用记忆中的信息。没有独立门控，模型无法独立控制读写擦除。
>
> **💡 Intuition:**
> **(1) Notebook with pencil and eraser analogy (笔记本与铅笔橡皮类比):**
>
> Cell state = a notebook. Forget gate = eraser (selectively erase old notes). Input gate = pencil (selectively write new notes). Output gate = reading glasses (selectively read notes to answer the current question). RNN = a whiteboard that gets fully erased and rewritten at every step -- no selective memory control.
>
> > 细胞状态 = 笔记本。遗忘门 = 橡皮。输入门 = 铅笔。输出门 = 老花镜。RNN = 每步被完全擦除和重写的白板。
>
> **⚙️ How:**
> **(1) LSTM computation pipeline (LSTM计算流水线):**
>
> Step 1: ft = sigma(Wf*[ht-1, xt] + bf) -- what to forget
> Step 2: it = sigma(Wi*[ht-1, xt] + bi), c-tilde = tanh(Wc*[ht-1, xt] + bc) -- what to add
> Step 3: ct = ft . ct-1 + it . c-tilde -- update cell state
> Step 4: ot = sigma(Wo*[ht-1, xt] + bo), ht = ot . tanh(ct) -- compute output
>
> > 步骤1：遗忘门 -> 步骤2：输入门+候选 -> 步骤3：更新细胞状态 -> 步骤4：输出门+隐藏状态
>
> **⚖️ Compare:**
> **(1) RNN vs LSTM comparison (RNN与LSTM对比):**
>
> | Feature          | RNN                       | LSTM                            |
> | ---------------- | ------------------------- | ------------------------------- |
> | Long-term memory | Poor (vanishing gradient) | Good (cell state conveyor belt) |
> | Gates            | None                      | 3 (forget, input, output)       |
> | Parameters       | Fewer                     | ~4x more                        |
> | Training speed   | Faster per step           | Slower per step                 |
> | Gradient flow    | Exponential decay         | Linear highway                  |
>
> > | 特性         | RNN            | LSTM                 |
> > | ------------ | -------------- | -------------------- |
> > | 长期记忆     | 差（梯度消失） | 好（细胞状态传送带） |
> > | 门控         | 无             | 3个                  |
> > | 参数量       | 较少           | 约4倍                |
> > | 每步训练速度 | 更快           | 更慢                 |
> > | 梯度流       | 指数衰减       | 线性通道             |
>
> **⚠️ Pitfall:**
> **(1) LSTM doesn't eliminate vanishing gradient entirely (LSTM并非完全消除梯度消失):**
>
> LSTM MITIGATES vanishing gradients via the cell state highway, but doesn't completely solve it. For very long sequences (1000+ tokens), even LSTM struggles. This is one reason Transformers eventually replaced LSTMs.
>
> > LSTM通过细胞状态通道减轻梯度消失，但并非完全解决。对于超长序列（1000+ token），LSTM仍然困难。这是Transformer最终取代LSTM的原因之一。
>
> **📝 Exam:**
> **(1) 对比题 (Comparison):**
>
> "What are the three gates in LSTM and their functions?" -> Forget gate: sigma, decides what to erase from cell state. Input gate: sigma+tanh, decides what new info to store. Output gate: sigma, decides what to output from cell state as hidden state.
>
> > "LSTM的三个门及其功能？" -> 遗忘门：决定擦除什么。输入门：决定存储什么新信息。输出门：决定从细胞状态输出什么。
>
> **(2) 概念题 (Conceptual):**
>
> "How does LSTM solve the vanishing gradient problem?" -> The cell state acts as a linear highway -- information flows through with only pointwise operations (multiply by forget gate, add via input gate). This avoids the repeated matrix multiplications that cause exponential gradient decay in vanilla RNN.
>
> > "LSTM如何解决梯度消失？" -> 细胞状态作为线性通道——信息仅通过逐元素操作流动。避免了原始RNN中导致梯度指数衰减的重复矩阵乘法。

---

## 11. 语言模型评估 (Evaluating Language Models)

![Page 61](lecture5_slides_pages/page_061.png)

**Evaluating Language Models -- Perplexity:** — 评估语言模型——困惑度：

- The standard evaluation metric for Language Models is **perplexity** — 标准评估指标是**困惑度**
- Formula: perplexity = product over t=1 to T of (1 / P_LM(x(t+1) | x(t),...,x(1)))^(1/T) — normalized by number of words
- **Low perplexity** -> the model predicts the text well — 低困惑度表示模型预测良好
- **High perplexity** -> the text is unexpected for the model — 高困惑度表示文本对模型出乎意料
- Perplexity (PPL) measures **how confused** a language model is when predicting the next word — PPL衡量语言模型预测下一个词时的"困惑程度"

> **📝 Notes:**
>
> **📌 What:**
> **(1) Perplexity definition (困惑度定义):**
>
> Perplexity = exponentiation of the average negative log likelihood. PPL = exp(-(1/T) \* sum(log P(wt | w1...wt-1))). Equivalently, it's the inverse probability of the test set, normalized by the number of words. Lower PPL = better model. A model with PPL=50 is "as confused as if it were choosing uniformly among 50 words at each step."
>
> > 困惑度 = 平均负对数似然的指数。PPL = 50 意味着"模型在每步像在50个词中均匀选择一样困惑"。越低越好。
>
> **🎯 Why:**
> **(1) Why not just use accuracy (为什么不用准确率):**
>
> The vocabulary is huge (50,000+ words). Getting the exact top-1 word right is very hard. Perplexity captures "how close" the model was -- if P(correct word) = 0.8, that's much better than P(correct word) = 0.01, even though both might be "wrong."
>
> > 词汇量巨大（50,000+词）。正确预测top-1词非常困难。困惑度捕获模型"有多接近"。
>
> **💡 Intuition:**
> **(1) Multiple choice test analogy (多选题类比):**
>
> PPL = average number of choices the model is confused between. PPL=10 means the model narrows down to ~10 plausible words at each position on average. PPL=2 means it's almost always deciding between 2 words. PPL=1 means it's perfectly certain.
>
> > PPL = 模型平均在多少个选项间困惑。PPL=10意味着每个位置平均缩小到约10个合理词。PPL=1意味着完全确定。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What does a perplexity of 30 mean?" -> The model is, on average, as uncertain as if it were choosing uniformly among 30 words at each position. Lower is better.
>
> > "困惑度30意味着什么？" -> 模型平均像在30个词中均匀选择一样不确定。越低越好。

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
