# CST8507 NLP Quiz 1 — NLP概述 (Introduction to NLP)

Topic: NLP Overview, AI/ML/DL Hierarchy, NLP Tasks & Challenges

---

## Question 1 (1 point)

Which deep learning architecture, introduced in 2017, demonstrated remarkable performance in various NLP tasks and marked a turning point in natural language understanding?

Question 1 options:

A) Long Short-Term Memory (LSTM)

B) Convolutional Neural Network (CNN)

C) Transformer

D) Recurrent Neural Network (RNN)

> **Answer**: C
> **Explanation**:
> The Transformer architecture was introduced in 2017 by Google in the paper "Attention is All You Need," featuring the self-attention mechanism that revolutionized NLP. **Why C**: Only the Transformer was the 2017 breakthrough that fundamentally changed the field.
>
> > Transformer 架构于 2017 年由 Google 在论文 "Attention is All You Need" 中提出，引入了自注意力机制（Self-Attention），成为 NLP 领域的转折点。**为什么是 C**：只有 Transformer 是 2017 年提出并彻底改变 NLP 的架构。
>
> - **A/D**: LSTM (1997) and RNN appeared much earlier; while once dominant, they were not the 2017 turning point.
> - **B**: CNN is primarily for image tasks; while applicable to NLP, it was not the landmark architecture of 2017.
>
> > - **A/D 错**：LSTM (1997) 和 RNN 更早出现，虽然曾是主流但并非 2017 年的突破。
> > - **B 错**：CNN 主要用于图像任务，在 NLP 中有应用但未成为 2017 年的标志性转折。
>
> **Key**: Transformer (2017, "Attention is All You Need") — self-attention mechanism, the turning point of modern NLP.

---

## Question 2 (1 point)

The main challenge in sentiment analysis lies in the complexity of human emotions and language, so it requires a deeper understanding of language and context.

Question 2 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> The core difficulty of sentiment analysis lies in the complexity of human emotional expression, including sarcasm, irony, and metaphor. **Why True**: Accurately determining sentiment requires deep semantic understanding beyond simple keyword matching.
>
> > 情感分析的核心难点在于人类语言表达情感的复杂性，包括讽刺、反语、隐喻等。**为什么是 True**：准确判断情感需要深层语义理解，而非仅靠关键词匹配。
>
> **Key**: Sentiment analysis requires deep contextual understanding due to sarcasm, irony, and ambiguity in human language.

---

## Question 3 (1 point)

Which of the following is not an example of natural language generation?

Question 3 options:

A) Converting speech to text

B) Translating a document from English to French

C) Writing a news article

D) Text Classification

> **Answer**: D
> **Explanation**:
> NLG (Natural Language Generation) refers to systems that **produce** new natural language text. **Why D**: Text Classification assigns text to predefined categories — it is an NLU (Natural Language Understanding) task, not generation.
>
> > NLG（自然语言生成）是指系统**产出**新的自然语言文本。**为什么是 D**：文本分类是将文本归入预定义类别，属于 NLU（自然语言理解）任务，不生成新文本。
>
> - **A**: Speech-to-Text (ASR) is more recognition than generation, but in this question context it's not the best answer since it doesn't "generate" creative text either.
> - **B/C**: Translation and news article writing both involve producing text, so they are NLG tasks.
>
> > - **A**：语音转文本 (ASR) 偏识别，但此题语境下不是最佳答案。
> > - **B/C**：翻译和新闻写作都涉及文本生成，属于 NLG。
>
> **Key**: Text Classification = NLU (understanding); NLG = producing new text output (translation, writing, summarization).

---

## Question 4 (1 point)

A document is a raw or semi-structured piece of text (such as an article or report), whereas knowledge refers to structured, interpreted information such as facts, entities, or relationships extracted from documents.

Question 4 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> A document is raw text material; knowledge is structured information (entities, relationships, facts) extracted from it. **Why True**: This is the standard distinction between Document and Knowledge in NLP.
>
> > 文档是原始文本素材，知识是从中提取的结构化信息（如实体、关系、事实）。**为什么是 True**：这正是 NLP 中 Document vs Knowledge 的标准区分。
>
> **Key**: Document = raw/semi-structured text; Knowledge = structured, interpreted information (entities, facts, relationships).

---

## Question 5 (1 point)

Variation in NLP is a challenge because language data is often highly skewed, with a few words being very frequent and a vast number of words occurring rarely.

Question 5 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> Language data follows Zipf's Law: a few high-frequency words dominate, while the vast majority of unique words are rare, forming a long-tail distribution. **Why True**: This skewed distribution is a core NLP challenge, making it difficult for models to learn semantics of rare words.
>
> > 语言数据遵循齐普夫定律（Zipf's Law）：少数高频词占据大量出现次数，大量低频词极少出现，形成长尾分布。**为什么是 True**：这种分布不均是 NLP 的核心挑战之一，导致模型难以充分学习低频词的语义。
>
> **Key**: Zipf's Law — few words are very frequent, most words are rare. This skewed distribution is a key NLP challenge.

---

## Question 6 (1 point)

Which of the following best describes the relationship between AI, ML, DL, and NLP?

Question 6 options:

A) AI is a subset of ML, ML is a subset of DL, and NLP is unrelated to these fields.

B) DL and ML are unrelated to AI, while NLP is the main branch of AI.

C) AI is a subset of DL, ML is a subset of DL, and NLP is subset of ML

D) NLP is a subset of AI focused on language tasks; ML is an approach to achieve AI; DL is a type of ML.

> **Answer**: D
> **Explanation**:
> The correct hierarchy: AI (broadest) ⊃ ML (a way to achieve AI) ⊃ DL (a branch of ML); NLP is an application domain of AI. **Why D**: Only D correctly describes this nested relationship.
>
> > 正确的层级关系：AI（最大范畴）⊃ ML（AI 的实现路径之一）⊃ DL（ML 的分支）；NLP 是 AI 的一个应用领域。**为什么是 D**：只有 D 正确描述了这个嵌套关系。
>
> - **A**: Hierarchy inverted — AI is the parent, not a subset.
> - **B**: ML and DL are subfields of AI, not unrelated.
> - **C**: AI is not a subset of DL — it's the opposite.
>
> > - **A 错**：层级颠倒，AI 是父类不是子类。
> > - **B 错**：ML 和 DL 都是 AI 的子领域，并非无关。
> > - **C 错**：AI 不是 DL 的子集，恰好相反。
>
> **Key**: AI ⊃ ML ⊃ DL; NLP is an AI application domain focused on language tasks.

---

## Question 7 (1 point)

Text summarization is challenging because the system must select the most important information while maintaining coherence, context, and meaning from the original text. In text summarization, there is no need to maintain the overall meaning and coherence of the original text while extracting key information.

Question 7 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Trap question**: The first half is correct (summarization must maintain coherence), but the second half contradicts itself by claiming "no need to maintain meaning and coherence." **Why False**: Text summarization MUST preserve meaning and logical coherence while extracting key information.
>
> > ⚠️ **陷阱题**：题干前半句正确（摘要需保持连贯性），但后半句自相矛盾地声称"不需要保持整体含义和连贯性"。**为什么是 False**：文本摘要必须在提取关键信息的同时保持原文的意义和逻辑连贯性。
>
> **Key**: Text summarization MUST preserve meaning and coherence — the statement contradicts itself.

---

## Question 8 (1 point)

The goal of NLP is to develop algorithms and models that can understand, interpret, and generate human language in a way that is useful and meaningful.

Question 8 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> This is the standard definition of NLP. **Why True**: The goal of NLP is precisely to enable computers to understand, interpret, and generate human language meaningfully.
>
> > 这是 NLP 的标准定义。**为什么是 True**：NLP 的目标正是让计算机理解、解释和生成人类语言。
>
> **Key**: NLP aims to develop algorithms that understand, interpret, and generate human language meaningfully.

---

## Question 9 (1 point)

AI aims to create systems that rely only on fixed rules and do not involve learning, while machine learning is an unrelated field that does not use data to make predictions.

Question 9 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> Modern AI is not limited to fixed rules (like expert systems); it includes learning-based approaches. ML is a core branch of AI that specifically learns from data to make predictions. **Why False**: Both claims in the statement are wrong — AI encompasses learning capabilities, and ML is a subset of AI, not an "unrelated field."
>
> > 现代 AI 不仅限于固定规则（如专家系统），更包括从数据中学习的方法。ML 是 AI 的核心分支，专门通过数据学习来做预测。**为什么是 False**：题干两个断言都错——AI 包含学习能力，ML 也不是"无关领域"而是 AI 的子集。
>
> **Key**: AI includes learning-based systems (not just fixed rules); ML is a core subset of AI that learns from data.

---

## Question 10 (1 point)

In the Alan Turing test, a human evaluator interacts through text with two unseen participants: one human and one machine. If the evaluator cannot reliably tell which one is the machine based on the conversation, the machine is said to have passed the Turing Test.

Question 10 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> This is an accurate description of the Turing Test (1950). **Why True**: The core criterion of the Turing Test is — if an evaluator cannot distinguish the machine from the human in text-based conversation, the machine is considered intelligent.
>
> > 这是图灵测试（Turing Test, 1950）的准确描述。**为什么是 True**：图灵测试的核心标准是——如果评估者无法区分机器和人的对话，则认为机器具有智能。
>
> **Key**: Turing Test (1950) — if an evaluator cannot distinguish machine from human in text conversation, the machine passes.
