# CST8507 NLP All Quizzes — 全部测验合集

> 💡 **使用说明**: 所有题目的答案和解析均已直接显示在下方。

---

# Quiz 1 — NLP概述 (Introduction to NLP)

Topic: NLP Overview, AI/ML/DL Hierarchy, NLP Tasks & Challenges

---

## Q1.1 (1 point)

Which deep learning architecture, introduced in 2017, demonstrated remarkable performance in various NLP tasks and marked a turning point in natural language understanding?

> 哪种深度学习架构于2017年提出，在各种NLP任务中表现卓越，并标志着自然语言理解的转折点？

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
> **关键**: Transformer（2017，"Attention is All You Need"）— 自注意力机制，现代 NLP 的转折点。

---

## Q1.2 (1 point)

The main challenge in sentiment analysis lies in the complexity of human emotions and language, so it requires a deeper understanding of language and context.

> 情感分析的主要挑战在于人类情感和语言的复杂性，因此它需要对语言和上下文有更深层次的理解。

A) True
B) False

> **Answer**: A
> **Explanation**:
> The core difficulty of sentiment analysis lies in the complexity of human emotional expression, including sarcasm, irony, and metaphor. **Why True**: Accurately determining sentiment requires deep semantic understanding beyond simple keyword matching.
>
> > 情感分析的核心难点在于人类语言表达情感的复杂性，包括讽刺、反语、隐喻等。**为什么是 True**：准确判断情感需要深层语义理解，而非仅靠关键词匹配。
>
> **Key**: Sentiment analysis requires deep contextual understanding due to sarcasm, irony, and ambiguity in human language.
> **关键**: 情感分析需要深层上下文理解，因为人类语言中存在讽刺、反语和歧义。

---

## Q1.3 (1 point)

Which of the following is not an example of natural language generation?

> 以下哪项不是自然语言生成（NLG）的示例？

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
> **关键**: 文本分类 = NLU（理解）；NLG = 产出新文本（翻译、写作、摘要）。

---

## Q1.4 (1 point)

A document is a raw or semi-structured piece of text (such as an article or report), whereas knowledge refers to structured, interpreted information such as facts, entities, or relationships extracted from documents.

> 文档是原始或半结构化的文本（如文章或报告），而知识是指从文档中提取的结构化、经过解释的信息，如事实、实体或关系。

A) True
B) False

> **Answer**: A
> **Explanation**:
> A document is raw text material; knowledge is structured information (entities, relationships, facts) extracted from it. **Why True**: This is the standard distinction between Document and Knowledge in NLP.
>
> > 文档是原始文本素材，知识是从中提取的结构化信息（如实体、关系、事实）。**为什么是 True**：这正是 NLP 中 Document vs Knowledge 的标准区分。
>
> **Key**: Document = raw/semi-structured text; Knowledge = structured, interpreted information (entities, facts, relationships).
> **关键**: 文档 = 原始/半结构化文本；知识 = 结构化、解释过的信息（实体、事实、关系）。

---

## Q1.5 (1 point)

Variation in NLP is a challenge because language data is often highly skewed, with a few words being very frequent and a vast number of words occurring rarely.

> NLP中的变异性是一个挑战，因为语言数据往往高度偏斜——少数词非常高频，而大量词极少出现。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Language data follows Zipf's Law: a few high-frequency words dominate, while the vast majority of unique words are rare, forming a long-tail distribution. **Why True**: This skewed distribution is a core NLP challenge, making it difficult for models to learn semantics of rare words.
>
> > 语言数据遵循齐普夫定律（Zipf's Law）：少数高频词占据大量出现次数，大量低频词极少出现，形成长尾分布。**为什么是 True**：这种分布不均是 NLP 的核心挑战之一，导致模型难以充分学习低频词的语义。
>
> **Key**: Zipf's Law — few words are very frequent, most words are rare. This skewed distribution is a key NLP challenge.
> **关键**: 齐普夫定律 — 少数词非常高频，大多数词极少出现。这种偏斜分布是 NLP 的关键挑战。

---

## Q1.6 (1 point)

Which of the following best describes the relationship between AI, ML, DL, and NLP?

> 以下哪项最能描述 AI、ML、DL 和 NLP 之间的关系？

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
> **关键**: AI ⊃ ML ⊃ DL；NLP 是 AI 中专注语言任务的应用领域。

---

## Q1.7 (1 point)

Text summarization is challenging because the system must select the most important information while maintaining coherence, context, and meaning from the original text. In text summarization, there is no need to maintain the overall meaning and coherence of the original text while extracting key information.

> 文本摘要具有挑战性，因为系统必须在保持连贯性、上下文和原意的同时选取最重要的信息。在文本摘要中，提取关键信息时不需要保持原文的整体含义和连贯性。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Trap question**: The first half is correct (summarization must maintain coherence), but the second half contradicts itself by claiming "no need to maintain meaning and coherence." **Why False**: Text summarization MUST preserve meaning and logical coherence while extracting key information.
>
> > ⚠️ **陷阱题**：题干前半句正确（摘要需保持连贯性），但后半句自相矛盾地声称"不需要保持整体含义和连贯性"。**为什么是 False**：文本摘要必须在提取关键信息的同时保持原文的意义和逻辑连贯性。
>
> **Key**: Text summarization MUST preserve meaning and coherence — the statement contradicts itself.
> **关键**: 文本摘要必须保持原文含义和连贯性 — 题干自相矛盾。

---

## Q1.8 (1 point)

The goal of NLP is to develop algorithms and models that can understand, interpret, and generate human language in a way that is useful and meaningful.

> NLP的目标是开发能够以有用且有意义的方式理解、解释和生成人类语言的算法和模型。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is the standard definition of NLP. **Why True**: The goal of NLP is precisely to enable computers to understand, interpret, and generate human language meaningfully.
>
> > 这是 NLP 的标准定义。**为什么是 True**：NLP 的目标正是让计算机理解、解释和生成人类语言。
>
> **Key**: NLP aims to develop algorithms that understand, interpret, and generate human language meaningfully.
> **关键**: NLP 旨在开发能有意义地理解、解释和生成人类语言的算法。

---

## Q1.9 (1 point)

AI aims to create systems that rely only on fixed rules and do not involve learning, while machine learning is an unrelated field that does not use data to make predictions.

> AI旨在创建仅依赖固定规则且不涉及学习的系统，而机器学习是一个与之无关的领域，不使用数据进行预测。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Modern AI is not limited to fixed rules (like expert systems); it includes learning-based approaches. ML is a core branch of AI that specifically learns from data to make predictions. **Why False**: Both claims in the statement are wrong — AI encompasses learning capabilities, and ML is a subset of AI, not an "unrelated field."
>
> > 现代 AI 不仅限于固定规则（如专家系统），更包括从数据中学习的方法。ML 是 AI 的核心分支，专门通过数据学习来做预测。**为什么是 False**：题干两个断言都错——AI 包含学习能力，ML 也不是"无关领域"而是 AI 的子集。
>
> **Key**: AI includes learning-based systems (not just fixed rules); ML is a core subset of AI that learns from data.
> **关键**: AI 包含基于学习的系统（不仅是固定规则）；ML 是 AI 的核心子集，从数据中学习。

---

## Q1.10 (1 point)

In the Alan Turing test, a human evaluator interacts through text with two unseen participants: one human and one machine. If the evaluator cannot reliably tell which one is the machine based on the conversation, the machine is said to have passed the Turing Test.

> 在图灵测试中，一个人类评估者通过文字与两个看不见的参与者（一个人和一台机器）交互。如果评估者无法根据对话可靠地判断哪个是机器，则该机器被认为通过了图灵测试。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is an accurate description of the Turing Test (1950). **Why True**: The core criterion of the Turing Test is — if an evaluator cannot distinguish the machine from the human in text-based conversation, the machine is considered intelligent.
>
> > 这是图灵测试（Turing Test, 1950）的准确描述。**为什么是 True**：图灵测试的核心标准是——如果评估者无法区分机器和人的对话，则认为机器具有智能。
>
> **Key**: Turing Test (1950) — if an evaluator cannot distinguish machine from human in text conversation, the machine passes.
> **关键**: 图灵测试（1950）— 如果评估者无法在文字对话中区分机器和人类，则机器通过测试。

---

# Quiz 2 — 文本预处理与正则 (Text Preprocessing & Regex)

Topic: Tokenization, Stemming, Lemmatization, Regex, Text Cleaning

---

## Q2.1 (1 point)

The process of converting raw text into a sequence of units that a model can process.

> 将原始文本转换为模型可以处理的单元序列的过程。

A) Tokenization

B) Lemmatization

C) Stemming

> **Answer**: A
> **Explanation**:
> Tokenization is the process of splitting continuous text into minimal semantic units (tokens) — the first step in the NLP pipeline. **Why A**: Only Tokenization describes the process of "converting raw text into a sequence of processable units."
>
> > 分词（Tokenization）是将连续文本切割为最小语义单元（Token）的过程，是 NLP 管道的第一步。**为什么是 A**：只有 Tokenization 描述的是"将文本转化为模型可处理的单元序列"这个过程。
>
> - **B**: Lemmatization reduces words to their dictionary base form (e.g., "running" → "run"), not splitting text.
> - **C**: Stemming crudely removes suffixes to get word roots, also not splitting text.
>
> > - **B 错**：Lemmatization（词元化）是将词还原为词典原形（如 "running" → "run"），不是切分文本。
> > - **C 错**：Stemming（词干提取）是粗暴地去除后缀获取词根，也不是切分文本。
>
> **Key**: Tokenization = splitting raw text into processable units (tokens). First step in NLP pipeline.
> **关键**: 分词 = 将原始文本切分为可处理的单元（token）。NLP 管道的第一步。

---

## Q2.2 (1 point)

For which of the following tasks we shouldn't do stemming/lemmatization?

> 对于以下哪项任务我们不应该进行词干提取/词元化？

A) Sentiment Analysis

B) Poetry Analysis

C) Text Classification

> **Answer**: B
> **Explanation**:
> In poetry analysis, the original word forms, tenses, and endings are crucial for rhyme, rhythm, and rhetoric. **Why B**: Stemming/Lemmatization would destroy word form variations, losing rhyme and rhetorical information essential to poetry.
>
> > 诗歌分析中，词汇的原始形态、时态变化和词尾韵律对押韵、节奏至关重要。**为什么是 B**：Stemming/Lemmatization 会破坏词形变化，从而丢失诗歌中的韵律和修辞信息。
>
> - **A/C**: In sentiment analysis and text classification, word normalization typically helps reduce feature space and improve model performance.
>
> > - **A/C**：情感分析和文本分类中，词形归一化通常有助于减少特征空间、提升模型性能。
>
> **Key**: Poetry relies on exact word forms for rhyme/rhythm; stemming/lemmatization would destroy this information.
> **关键**: 诗歌依赖精确的词形来实现韵律/节奏；词干提取/词元化会破坏这些信息。

---

## Q2.3 (1 point)

SpaCy does not provide a built-in function for Stemming

> SpaCy 没有提供内置的词干提取（Stemming）功能。

A) True
B) False

> **Answer**: A
> **Explanation**:
> SpaCy's design philosophy favors dictionary-based Lemmatization, so it does not include built-in Stemming functionality. **Why True**: SpaCy considers Lemmatization more accurate and does not provide a Stemming API. Use NLTK's PorterStemmer or SnowballStemmer for stemming.
>
> > SpaCy 的设计理念偏向使用基于词典的 Lemmatization，因此没有内置 Stemming 功能。**为什么是 True**：SpaCy 认为 Lemmatization 更准确，不提供 Stemming API。如需 Stemming 可使用 NLTK 的 PorterStemmer 或 SnowballStemmer。
>
> **Key**: SpaCy provides lemmatization only, no built-in stemming. Use NLTK (PorterStemmer, SnowballStemmer) for stemming.
> **关键**: SpaCy 只提供词元化，无内置词干提取。词干提取使用 NLTK（PorterStemmer、SnowballStemmer）。

---

## Q2.4 (1 point)

The following rgx will match all the words ended with a hyphen(-):

> 以下正则表达式将匹配所有以连字符（-）结尾的单词：

`rgx = r'\b\w+[-]\w+\b'`

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Regex trap**: The regex `\b\w+[-]\w+\b` matches **compound words with a hyphen in the middle** (e.g., "high-tech", "well-known"), NOT words ending with a hyphen. **Why False**: The pattern requires `\w+` (one or more word characters) on both sides of the hyphen, so the hyphen must be in the middle, not at the end.
>
> > ⚠️ **正则陷阱**：该正则 `\b\w+[-]\w+\b` 匹配的是**中间含连字符的复合词**（如 "high-tech"、"well-known"），而非以连字符结尾的词。**为什么是 False**：模式要求连字符两侧都有 `\w+`（一个或多个单词字符），因此连字符必须在词中间，不可能在末尾。
>
> **Key**: `\b\w+[-]\w+\b` matches hyphenated compound words (e.g., "high-tech"), NOT words ending with a hyphen.
> **关键**: `\b\w+[-]\w+\b` 匹配含连字符的复合词（如 "high-tech"），不是以连字符结尾的词。

---

## Q2.5 (1 point)

Text cleaning removes noise (like special characters, irrelevant symbols, and unnecessary spaces) and standardizes the text (e.g., converting to lowercase), is essential for improving the quality of the data and the performance of NLP models.

> 文本清洗去除噪声（如特殊字符、无关符号和多余空格）并标准化文本（如转为小写），这对于提高数据质量和NLP模型性能至关重要。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Text cleaning reduces noise and feature space dimensionality by removing special characters and extra spaces, and standardizing case. **Why True**: Cleaned text is more normalized, reducing irrelevant variants the model must handle, thus improving performance.
>
> > 文本清洗通过去除特殊字符、多余空格并统一大小写，能有效降低噪声和特征空间维度。**为什么是 True**：清洗后的文本更规范，减少了模型需要处理的无关变体，从而提升模型性能。
>
> **Key**: Text cleaning removes noise (special chars, extra spaces) and standardizes text (lowercasing) → improved model performance.
> **关键**: 文本清洗去除噪声（特殊字符、多余空格）并标准化文本（小写化）→ 提升模型性能。

---

## Q2.6 (1 point)

Consider you have the following list that represents the USA's state names:

> 假设你有以下代表美国州名的列表：

```python
states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado',
          'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho',
          'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
          'Maine','Maryland','Massachusetts','Michigan','Minnesota',
          'Mississippi','Missouri','Montana','Nebraska','Nevada',
          'New Hampshire','New Jersey','New Mexico','New York',
          'North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
          'Pennsylvania','Rhode Island','South Carolina','South Dakota',
          'Tennessee','Texas','Utah','Vermont','Virginia','Washington',
          'West Virginia','Wisconsin','Wyoming']
```

Which python expression outputs which state names start and end with a "vowel" character?

> 哪个 Python 表达式可以输出以元音字符开头和结尾的州名？

A) `[s for s in states if s[0].lower() in 'aeiou' and s[1] in 'aeiou']`

B) `[s for s in states if s[0].lower() in 'aeiou' and s[-1] in 'aeiou']`

C) `[s for s in states if s[1].lower() in 'aeiou' and s[-1] in 'aeiou']`

> **Answer**: B
> **Explanation**:
> We need to check whether the first and last characters are vowels. **Why B**: `s[0]` gets the first character, `s[-1]` gets the last character, and both check `in 'aeiou'` for vowel membership.
>
> > 需要检查首字母和末尾字母是否为元音。**为什么是 B**：`s[0]` 取首字母，`s[-1]` 取末尾字母，两者都检查是否在 `'aeiou'` 中。
>
> - **A**: `s[1]` gets the **second** character, not the last.
> - **C**: `s[1]` gets the second character, not the first.
> - **Note**: `s[0].lower()` handles uppercase first letters; `s[-1]` happens to be lowercase so `.lower()` isn't needed, but strictly speaking it should be added.
>
> > - **A 错**：`s[1]` 取的是第二个字符，不是末尾字符。
> > - **C 错**：`s[1]` 取第二个字符，不是首字母。
> > - **注意**：`s[0].lower()` 处理大写首字母，`s[-1]` 末尾恰好小写不需要 `.lower()`，但严格来说应加上。
>
> **Key**: `s[0]` = first char, `s[-1]` = last char. Check both `in 'aeiou'` for vowel start and end.
> **关键**: `s[0]` = 首字符，`s[-1]` = 末字符。两者都检查 `in 'aeiou'` 判断元音开头和结尾。

---

## Q2.7 (1 point)

When might you use lemmatizing over stemming?

> 什么时候你应该选择词元化（lemmatizing）而非词干提取（stemming）？

A) when accuracy is preferred more than speed

B) when non-dictionary words are allowed to appear in the output

C) when the data file contains a large number of simple words

D) when speed is preferred more than accuracy

> **Answer**: A
> **Explanation**:
> Lemmatization uses dictionary lookup to restore words to their standard base form — more accurate but slower than Stemming. **Why A**: When accuracy matters more than speed, Lemmatization is the better choice.
>
> > Lemmatization 通过词典查询将词还原为标准形式，比 Stemming 更准确但更慢。**为什么是 A**：当准确性比速度更重要时，应选择 Lemmatization。
>
> - **B**: Lemmatization output consists of valid dictionary words; Stemming may produce non-dictionary forms (e.g., "studi").
> - **C/D**: Simple words and speed-priority scenarios are better suited for Stemming.
>
> > - **B 错**：Lemmatization 产出的是词典中的合法词，Stemming 才可能产出非词典词（如 "studi"）。
> > - **C/D 错**：简单词和速度优先的场景更适合 Stemming。
>
> **Key**: Lemmatization = dictionary-based, accurate but slower; Stemming = rule-based suffix stripping, faster but less accurate.
> **关键**: 词元化 = 基于词典，准确但较慢；词干提取 = 基于规则去后缀，更快但不太准确。

---

## Q2.8 (1 point)

Pick the stemming action

> 选出词干提取（stemming）的操作：

A) was, am, is, are ----> be

B) helped, helps -----> help

C) troubled, troubling, trouble ------> trouble

> **Answer**: B
> **Explanation**:
> Stemming obtains word stems by stripping common suffixes (-ed, -s, -ing) through pure rule-based operations. **Why B**: "helped" strips `-ed`, "helps" strips `-s` — both achieve the stem "help" through simple suffix removal.
>
> > Stemming 通过剥离常见后缀（如 -ed, -s, -ing）来获取词干，是纯规则操作。**为什么是 B**："helped" 去掉 `-ed`、"helps" 去掉 `-s`，都通过简单的后缀剥离得到词干 "help"。
>
> - **A**: "was/am/is/are → be" is Lemmatization — it requires dictionary knowledge to map irregular verb forms.
> - **C**: "troubled/troubling → trouble" may seem like suffix removal, but "trouble → trouble" shows no change — this is more of a Lemmatization result.
>
> > - **A 错**："was/am/is/are → be" 是 Lemmatization，因为需要词典知识来映射不规则变形。
> > - **C 错**："troubled/troubling → trouble" 虽然看似后缀剥离，但 "trouble → trouble" 没有变化，更像 Lemmatization 的结果。
>
> **Key**: Stemming = simple suffix removal (-ed, -s, -ing). Irregular forms (was→be) require lemmatization.
> **关键**: 词干提取 = 简单去后缀（-ed, -s, -ing）。不规则变形（was→be）需要词元化。

---

## Q2.9 (1 point)

Consider the provided code snippet:

> 考虑以下代码片段：

```python
Text = 'I love NLP and I am read9y to study in 5 hours per Day'
regex = '[a-zA-Z]\w*d+'
print(re.findall(regex, Text))
```

The output is: `['and']`

> 输出结果是：`['and']`

A) True
B) False

> **Answer**: B
> **Explanation**:
> The regex `[a-zA-Z]\w*d+` matches: starts with a letter → any number of word characters → ends with one or more `d`. **Why False**: This regex doesn't only match `"and"` — it also matches `"read"` (from "read9y", since `d` ends it) and `"stud"` (from "study"), producing multiple results.
>
> > 正则 `[a-zA-Z]\w*d+` 匹配：以字母开头 → 任意个单词字符 → 以一个或多个 `d` 结尾的序列。**为什么是 False**：该正则不仅匹配 `"and"`，还会匹配其他以 `d` 结尾的子串，输出不止一个结果。
>
> - **Note**: `\w` includes digits, so patterns within "read9y" and "study" can also produce matches ending in `d`.
>
> > - **注意**：`\w` 包含数字，所以 "read9y" 和 "study" 中的子模式也能产生以 `d` 结尾的匹配。
>
> **Key**: `[a-zA-Z]\w*d+` matches any substring starting with a letter and ending with 'd'. Output includes multiple matches, not just 'and'.
> **关键**: `[a-zA-Z]\w*d+` 匹配以字母开头、以 'd' 结尾的任意子串。输出包含多个匹配，不只是 'and'。

---

# Quiz 3 — 文本表示 (Text Representation)

Topic: Edit Distance, Bag of Words, TF-IDF, Cosine Similarity, CountVectorizer

---

## Q3.1 (1 point)

Given the words "intention" and "execution", what is the minimum number of operations required to transform "intention" into "execution"?

> 给定单词 "intention" 和 "execution"，将 "intention" 转换为 "execution" 所需的最小操作次数是多少？

A) 3

B) 4

C) 5

D) 6

> **Answer**: C
> **Explanation**:
> This is the classic Levenshtein edit distance problem, with allowed operations: insertion, deletion, substitution. **Why 5**: Through dynamic programming, transforming "intention" → "execution" requires a minimum of 5 operations.
>
> > 这是经典的 Levenshtein 编辑距离（Edit Distance）问题，允许的操作有插入、删除、替换。**为什么是 5**：通过动态规划计算，"intention" → "execution" 最少需要 5 步操作。
>
> - **$d(s_1, s_2)$**: Edit distance — the minimum number of operations to transform string $s_1$ into $s_2$
>
> > - **$d(s_1, s_2)$**: 编辑距离 — 将字符串 $s_1$ 转换为 $s_2$ 的最小操作数
>
> **Key**: Levenshtein (edit) distance = minimum insertions, deletions, substitutions to transform one string into another.
> **关键**: 编辑距离 = 通过插入、删除、替换将一个字符串转换为另一个的最小操作数。

---

## Q3.2 (1 point)

In a Bag of Words representation, the order of words in a document is crucial, and each word is treated as dependent on its surrounding words.

> 在词袋（Bag of Words）表示中，文档中单词的顺序至关重要，每个单词都被视为依赖于其周围的单词。

A) True
B) False

> **Answer**: B
> **Explanation**:
> The core characteristic of BoW (Bag of Words) is that it **ignores word order** and treats each word as an independent feature. **Why False**: The statement claims "word order is crucial" and "words are dependent on context" — these are exactly what BoW does NOT have. BoW only cares about word frequency.
>
> > BoW（词袋模型）的核心特征就是**忽略词序**，每个词被视为独立的特征。**为什么是 False**：题干说"词序至关重要"和"词与上下文相关"，这恰好是 BoW 不具备的特性。BoW 只关注词频。
>
> **Key**: Bag of Words ignores word order and treats each word independently — only word frequency matters.
> **关键**: 词袋模型忽略词序，将每个词视为独立特征 — 只关注词频。

---

## Q3.3 (1 point)

The inverse document frequency (IDF) of a word is calculated by dividing the total number of documents by the number of documents containing the word.

> 单词的逆文档频率（IDF）通过将文档总数除以包含该单词的文档数来计算。

A) True
B) False

> **Answer**: A
> **Explanation**:
> The IDF formula is $IDF(t) = \log\frac{N}{df(t)}$, where $N$ is the total number of documents and $df(t)$ is the number of documents containing word $t$. **Why True**: The statement describes exactly the core IDF calculation logic — total documents divided by documents containing the word (usually with log applied).
>
> > IDF 的计算公式为 $IDF(t) = \log\frac{N}{df(t)}$，其中 $N$ 是总文档数，$df(t)$ 是包含词 $t$ 的文档数。**为什么是 True**：题干描述的正是 IDF 的核心计算逻辑——用总文档数除以包含该词的文档数（通常取对数）。
>
> - **$N$**: Total number of documents in corpus (语料库总文档数)
> - **$df(t)$**: Number of documents containing word $t$ (包含词 $t$ 的文档数)
> - **$IDF(t) = \log\frac{N}{df(t)}$**: Inverse Document Frequency (逆文档频率)
>
> **Key**: $IDF(t) = \log\frac{N}{df(t)}$ — words appearing in fewer documents get higher IDF scores.
> **关键**: 出现在越少文档中的词获得越高的 IDF 分数。$IDF(t) = \log\frac{N}{df(t)}$

---

## Q3.4 (1 point)

If the cosine similarity between the word vectors for Word A and Word B is close to 1, it means that Word A and Word B are considered highly similar in meaning.

> 如果词A和词B的词向量之间的余弦相似度接近1，则意味着它们在语义上被认为高度相似。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Cosine similarity measures the directional angle between two vectors, with value range $[-1, 1]$. **Why True**: When cosine similarity is close to 1, the two vectors point in nearly the same direction, indicating high semantic similarity in embedding space.
>
> > 余弦相似度衡量两个向量的方向夹角，值域为 $[-1, 1]$。**为什么是 True**：当余弦相似度接近 1 时，两个向量方向近乎一致，在词嵌入空间中表示语义高度相似。
>
> - **$\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \times ||\vec{B}||}$**: Cosine similarity formula (余弦相似度公式)
> - Close to 1 = same direction (similar); close to 0 = orthogonal (unrelated); close to -1 = opposite (contrary)
>
> > - 接近 1 = 方向一致（相似）；接近 0 = 正交（无关）；接近 -1 = 方向相反（相反）
>
> **Key**: Cosine similarity close to 1 → vectors point in same direction → semantically similar.
> **关键**: 余弦相似度接近 1 → 向量方向一致 → 语义相似。

---

## Q3.5 (1 point)

One of the disadvantages of using TF-IDF is:

> 使用TF-IDF的缺点之一是：

A) It produces low-dimensional dense vectors

B) It considers the context and semantic relationships between words

C) It does not consider the context and semantic relationships between words

D) It captures word order information

> **Answer**: C
> **Explanation**:
> TF-IDF is a bag-of-words statistical method with no semantic understanding capability. **Why C**: TF-IDF only computes word frequency and document frequency — it cannot capture contextual relationships or word meaning.
>
> > TF-IDF 是基于词袋模型的统计方法，不具备语义理解能力。**为什么是 C**：TF-IDF 只统计词频和文档频率，无法捕捉上下文关系或词义。
>
> - **A**: TF-IDF produces high-dimensional sparse vectors (vocabulary size), not low-dimensional dense ones.
> - **B/D**: These are capabilities TF-IDF does NOT have — it understands neither semantic relationships nor word order.
>
> > - **A 错**：TF-IDF 产生的是高维稀疏向量（词汇表大小），不是低维密集向量。
> > - **B/D 错**：这些是 TF-IDF **不具备**的能力——它既不理解语义关系，也不保留词序。
>
> **Key**: TF-IDF is a bag-of-words statistical method — no context, no semantics, no word order. High-dimensional and sparse.
> **关键**: TF-IDF 是词袋统计方法 — 无上下文、无语义、无词序。高维且稀疏。

---

## Q3.6 (1 point)

Given the following TF values for a word across different documents:

> 给定一个词在不同文档中的以下TF值：

| Document | TF Calculation | TF Value |
| -------- | -------------- | -------- |
| d1       | 25/127         | ≈ 0.1969 |
| d2       | 3/250          | = 0.0120 |
| d3       | 20/650         | ≈ 0.0308 |
| d9       | 15/125         | = 0.1200 |
| d1000    | 20/800         | = 0.0250 |

The proposed ascending order by TF is: [d2, d1000, d3, d1, d9]

> 提出的按TF升序排列为：[d2, d1000, d3, d1, d9]

A) True
B) False

> **Answer**: B
> **Explanation**:
> Calculate and sort TF values: d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197). **Why False**: The proposed order [d2, d1000, d3, **d1, d9**] has d1 and d9 swapped.
>
> > 计算各文档的 TF 值并排序：d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197)。**为什么是 False**：题目给出的排序 [d2, d1000, d3, **d1, d9**] 中，d1 和 d9 的位置反了。
>
> - **Correct ascending order (正确升序)**: [d2, d1000, d3, d9, d1]
> - **$TF(t,d) = \frac{f(t,d)}{|d|}$**: Term Frequency = word count in document / total words in document
>
> > - **$TF(t,d) = \frac{f(t,d)}{|d|}$**: 词频 = 词在文档中出现的次数 / 文档总词数
>
> **Key**: Correct ascending TF order: [d2, d1000, d3, d9, d1]. The proposal swapped d1 and d9.
> **关键**: 正确升序 TF 排列：[d2, d1000, d3, d9, d1]。题目把 d1 和 d9 位置搞反了。

---

## Q3.7 (1 point)

Given two word vectors:

> 给定两个词向量：

- $w_1 = (0.2, 0.2, 0.3, 0.7)$
- $w_2 = (0.3, 0.4, 0.8, 0.5)$

Calculate the cosine similarity.

> 计算余弦相似度。

> **Answer**: ≈ 0.8421
> **Explanation**:
> Step-by-step cosine similarity calculation:
>
> 1. **Dot product**: $w_1 \cdot w_2 = 0.2 \times 0.3 + 0.2 \times 0.4 + 0.3 \times 0.8 + 0.7 \times 0.5 = 0.06 + 0.08 + 0.24 + 0.35 = 0.73$
> 2. **Magnitude**: $||w_1|| = \sqrt{0.04 + 0.04 + 0.09 + 0.49} = \sqrt{0.66} \approx 0.8124$
> 3. **Magnitude**: $||w_2|| = \sqrt{0.09 + 0.16 + 0.64 + 0.25} = \sqrt{1.14} \approx 1.0677$
> 4. **Cosine similarity**: $\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx \frac{0.73}{0.8674} \approx 0.8421$
>
> > 余弦相似度计算步骤：
> >
> > 1. **点积**：$w_1 \cdot w_2 = 0.06 + 0.08 + 0.24 + 0.35 = 0.73$
> > 2. **模长**：$||w_1|| = \sqrt{0.66} \approx 0.8124$
> > 3. **模长**：$||w_2|| = \sqrt{1.14} \approx 1.0677$
> > 4. **结果**：$\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$
>
> **Key**: $\cos(\theta) = \frac{w_1 \cdot w_2}{||w_1|| \times ||w_2||} = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$
> **关键**: $\cos(\theta) = \frac{w_1 \cdot w_2}{||w_1|| \times ||w_2||} = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$

---

## Q3.8 (1 point)

> 考虑以下代码，声称的输出是否正确？

```python
cv = CountVectorizer(ngram_range=(1,2)).fit(
    ["I love NLP", "He love NLP", "good man"]
)
cv.transform(["love"]).toarray()
```

Claimed output / 声称的输出: `array([[0, 0, 1, 0, 0, 0, 0]], dtype=int64)`

A) True
B) False

> **Answer**: B
> **Explanation**:
> `CountVectorizer(ngram_range=(1,2))` generates a vocabulary of both unigrams and bigrams. **Why False**: The training corpus produces more than 7 features, so the vector length should be longer than claimed.
>
> > `CountVectorizer(ngram_range=(1,2))` 会生成 unigram 和 bigram 的词汇表。**为什么是 False**：训练语料会生成超过 7 个特征词，向量维度不止 7。
>
> - **Vocabulary includes (词汇表包含)**: unigrams ("good", "he", "love", "man", "nlp") + bigrams ("good man", "he love", "love nlp") = at least 8 features
> - Input `"love"` only matches unigram "love", so only that position is 1, but the vector dimension should be 8+, not 7
>
> > - 输入 `"love"` 只匹配 unigram "love"，除 "love" 位置为 1 外其余为 0，但向量维度应为 8+，不是 7
>
> **Key**: `CountVectorizer(ngram_range=(1,2))` creates both unigrams and bigrams. The claimed vector length (7) is incorrect.
> **关键**: `CountVectorizer(ngram_range=(1,2))` 同时生成 unigram 和 bigram。声称的向量长度（7）不正确。

---

# Quiz 4 — 词嵌入 (Word Embeddings)

Topic: TF-IDF, Word Embeddings, Word2Vec (CBOW & Skip-gram), GloVe, Self-Supervised Learning

---

## Q4.1 (1 point)

While TF-IDF is useful for some applications (like search engines), its high-dimensional nature can make it difficult to use efficiently for tasks like deep learning-based NLP.

> 虽然TF-IDF对某些应用（如搜索引擎）很有用，但其高维特性使其在深度学习NLP任务中难以高效使用。

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> TF-IDF produces vectors with dimensions equal to vocabulary size (typically tens to hundreds of thousands), and these vectors are highly sparse. **Why True**: Deep learning models work better with low-dimensional dense vectors (e.g., Word2Vec's 100–300 dimensions); high-dimensional sparse vectors lead to computational inefficiency and overfitting.
>
> > TF-IDF 产生的向量维度等于词汇表大小（通常数万到数十万），且向量高度稀疏。**为什么是 True**：深度学习模型更适合处理低维密集向量（如 Word2Vec 的 100-300 维），高维稀疏向量会导致计算效率低下和过拟合。
>
> **Key**: TF-IDF = high-dimensional sparse vectors; DL prefers low-dimensional dense embeddings.
> **关键**: TF-IDF = 高维稀疏向量；深度学习偏好低维密集嵌入。

---

## Q4.2 (1 point)

Which of the following equations should hold for an effective word embedding?

> 对于有效的词嵌入，以下哪个等式应该成立？

- [ ] e_boy − e_brother ≈ e_sister − e_girl
- [x] e_boy − e_girl ≈ e_brother − e_sister
- [ ] e_boy − e_girl ≈ e_sister − e_brother

> **Answer**: e*boy − e_girl ≈ e_brother − e_sister
> **Explanation**:
> Effective word embeddings capture semantic relationships through vector arithmetic (analogy reasoning). **Why this option**: The difference between boy and girl represents the "gender" relationship; the difference between brother and sister should reflect the same "gender" relationship: $e*{boy} - e*{girl} \approx e*{brother} - e\_{sister}$.
>
> > 有效的词嵌入能通过向量运算捕捉语义关系（类比推理）。**为什么是第二项**：boy 和 girl 的差异代表"性别"关系，brother 和 sister 的差异也应体现相同的"性别"关系。
>
> - **Option 1**: boy - brother represents a "role type" difference, not parallel with sister - girl.
> - **Option 3**: Direction is reversed — sister - brother is opposite to boy - girl.
>
> > - **第一项错**：boy - brother 表示"角色类型"差异，与 sister - girl 不对等。
> > - **第三项错**：方向反了，sister - brother 与 boy - girl 方向相反。
>
> **Key**: Word analogy: $e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$ — same semantic relationship (gender) preserved in vector space.
> **关键**: 词类比：$e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$ — 向量空间中保持相同语义关系（性别）。

---

## Q4.3 (1 point)

The self-supervision method in neural language modeling avoids the need for hand-labeled supervision signals by using surrounding words as implicit training data for classifiers.

> 神经语言建模中的自监督方法通过使用周围的词作为分类器的隐式训练数据，从而避免了对手工标注监督信号的需求。

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> Self-supervised learning generates training signals from the data itself, requiring no manual labeling. **Why True**: Language models automatically obtain supervision signals by predicting missing or next words from context (e.g., CBOW predicts center word from context, Skip-gram predicts context from center word).
>
> > 自监督学习（Self-Supervised Learning）从数据本身生成训练信号，无需人工标注。**为什么是 True**：语言模型通过预测上下文中的缺失词或下一个词来自动获得监督信号（如 CBOW 用上下文预测中心词，Skip-gram 用中心词预测上下文）。
>
> **Key**: Self-supervised learning generates labels from data itself (e.g., predicting missing/next words from context).
> **关键**: 自监督学习从数据本身生成标签（如从上下文预测缺失词/下一个词）。

---

## Q4.4 (1 point)

One advantage of GloVe over other word embedding methods is that it is global in the sense that it considers the entire corpus to learn relationships between words, and local in the sense that it considers the co-occurrence of words within a limited context window.

> GloVe相比其他词嵌入方法的一个优势是：它是全局的（考虑整个语料库来学习词间关系），同时也是局部的（考虑有限上下文窗口内的词共现）。

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> GloVe (Global Vectors for Word Representation) combines two information sources. **Why True**:
>
> - **Global**: Uses the entire corpus to build a global word co-occurrence matrix, counting co-occurrence across all word pairs.
> - **Local**: Co-occurrence statistics are based on a limited context window, only considering nearby words.
> - This combination captures both global statistical patterns and local contextual relationships.
>
> > GloVe（全局词向量表示）结合了两种信息来源。**为什么是 True**：
> >
> > - **全局（Global）**：利用整个语料库构建全局词共现矩阵。
> > - **局部（Local）**：共现统计基于有限的上下文窗口。
> > - 这种结合使 GloVe 既能捕捉全局统计规律，又能反映局部上下文关系。
>
> **Key**: GloVe = **Glo**bal (corpus-wide co-occurrence matrix) + **Ve**ctors (local context window). Combines both perspectives.
> **关键**: GloVe = 全局（语料级共现矩阵）+ 向量（局部上下文窗口）。结合两种视角。

---

## Q4.5 (1 point)

Suppose you learn a word embedding for a vocabulary of 1000 words. Should the embedding vectors be 1000 dimensional to capture the full range of variation and meaning in those words?

> 假设你为1000个单词的词汇表学习词嵌入。嵌入向量是否应该是1000维的，以捕捉这些词的全部变化范围和含义？

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> The core value of word embeddings lies in **dimensionality reduction** — representing word meaning in far fewer dimensions than vocabulary size. **Why False**: 1000 dimensions equals one-hot encoding size, which defeats the purpose of embeddings. Typical embedding dimensions are 50–300, compressing semantic information into a low-dimensional dense space.
>
> > 词嵌入的核心价值在于**降维**——用远低于词汇表大小的维度来表示词义。**为什么是 False**：1000 维就等于 one-hot 编码的维度，失去了嵌入的意义。典型的嵌入维度为 50-300 维，通过学习将语义信息压缩到低维密集空间。
>
> **Key**: Embedding dim ≪ vocabulary size. Typical: 50–300 dimensions. 1000-dim = one-hot — defeats the purpose.
> **关键**: 嵌入维度 ≪ 词汇表大小。典型：50-300 维。1000 维 = one-hot，失去意义。

---

## Q4.6 (1 point)

What is the default dimensionality of word embeddings in the Gensim Word2Vec method?

> Gensim Word2Vec 方法中词嵌入的默认维度是多少？

- [ ] 4000
- [ ] 120
- [x] 100
- [ ] 10

> **Answer**: 100
> **Explanation**:
> The default vector dimension parameter in Gensim's Word2Vec model is `vector_size = 100`. **Why 100**: This is the Gensim default setting, providing a balance between accuracy and computational efficiency for most tasks.
>
> > Gensim 库中 Word2Vec 模型的默认向量维度参数 `vector_size = 100`。**为什么是 100**：这是 Gensim 的默认设置，在大多数任务中提供了准确性和计算效率的平衡。
>
> - 4000 is too large (computationally expensive); 10 is too small (insufficient expressiveness); 120 is not the default.
>
> > - 4000 太大（计算昂贵）；10 太小（表达力不足）；120 不是默认值。
>
> **Key**: Gensim Word2Vec default: `vector_size=100`. Adjustable based on corpus size and task needs.
> **关键**: Gensim Word2Vec 默认：`vector_size=100`。可根据语料大小和任务需求调整。

---

## Q4.7 (1 point)

Word2Vec consists of two main techniques: CBOW (Continuous Bag of Words) and Skip-gram.

> Word2Vec由两种主要技术组成：CBOW（连续词袋模型）和 Skip-gram。

- [x] True
- [ ] False

> **Answer**: A (True)
> **Explanation**:
> Word2Vec includes two training architectures. **Why True**:
>
> - **CBOW**: Predicts the center word from context words (Context → Word), better for frequent words.
> - **Skip-gram**: Predicts context words from the center word (Word → Context), better for rare words and small corpora.
>
> > Word2Vec 包含两种训练架构。**为什么是 True**：
> >
> > - **CBOW**：用上下文词预测中心词（Context → Word），适合高频词。
> > - **Skip-gram**：用中心词预测上下文词（Word → Context），适合低频词和小语料。
>
> **Key**: Word2Vec = CBOW (context→word, frequent words) + Skip-gram (word→context, rare words).
> **关键**: Word2Vec = CBOW（上下文→中心词，适合高频词）+ Skip-gram（中心词→上下文，适合低频词）。

---

## Q4.8 (1 point)

Is the goal of the Skip-Gram model to determine the central word based on its surrounding context words?

> Skip-Gram模型的目标是根据周围的上下文词来确定中心词吗？

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> ⚠️ **Easy to confuse**: The statement describes CBOW's function, not Skip-gram's. **Why False**: Skip-gram's goal is to predict surrounding context words FROM the center word (Word → Context) — the opposite of what the statement says.
>
> > ⚠️ **易混淆题**：题干描述的是 CBOW 的功能，而非 Skip-gram。**为什么是 False**：Skip-gram 的目标是用中心词预测周围的上下文词（Word → Context），与题干所述相反。
>
> - **Skip-gram**: Input center word → predict context words
> - **CBOW**: Input context words → predict center word (what the statement actually describes)
>
> > - **Skip-gram**：输入中心词 → 预测上下文词
> > - **CBOW**：输入上下文词 → 预测中心词（题干描述的就是这个）
>
> **Key**: Skip-gram: **center word → context words**. CBOW: context words → center word. Don't confuse them!
> **关键**: Skip-gram：中心词 → 上下文词。CBOW：上下文词 → 中心词。别搞混！

---

## Q4.9 (1 point)

Most modern NLP algorithms do not use embeddings as the representation of word meaning.

> 大多数现代NLP算法不使用嵌入（embeddings）作为词义的表示方式。

- [ ] True
- [x] False

> **Answer**: B (False)
> **Explanation**:
> Modern NLP heavily relies on word embeddings as the foundational representation. **Why False**: From Word2Vec, GloVe to pre-trained models like BERT and GPT, embeddings are the core component. Virtually all modern NLP algorithms use embeddings to represent word meaning.
>
> > 现代 NLP 高度依赖词嵌入作为基础表示。**为什么是 False**：从 Word2Vec、GloVe 到 BERT、GPT 等预训练模型，嵌入都是核心组件。几乎所有现代 NLP 算法都使用嵌入来表示词义。
>
> **Key**: Modern NLP relies heavily on embeddings (Word2Vec, GloVe, BERT, GPT). Embeddings are THE standard word representation.
> **关键**: 现代 NLP 高度依赖嵌入（Word2Vec、GloVe、BERT、GPT）。嵌入是标准词表示方式。

---

## Quick Review Notes / 快速复习

| Concept / 概念           | Key Point / 要点                                            |
| ------------------------ | ----------------------------------------------------------- |
| TF-IDF                   | Sparse, high-dimensional, no semantics / 稀疏、高维、无语义 |
| Embeddings / 词嵌入      | Dense, low-dimensional, semantic / 密集、低维、有语义       |
| Self-supervised / 自监督 | Data generates its own labels / 数据自生成标签              |
| GloVe                    | Global statistics + local context / 全局统计 + 局部上下文   |
| Word2Vec                 | CBOW + Skip-gram                                            |
| CBOW                     | Context → Word / 上下文 → 中心词                            |
| Skip-gram                | Word → Context / 中心词 → 上下文                            |

---

# Quiz 5 — RNN与语言模型 (RNN & Language Models)

Topic: RNN, LSTM, Gradient, N-gram Language Models, Learning Rate, Training Data

---

## Q5.1 (1 point)

In the context of Recurrent Neural Networks (RNNs), the gradient refers to the rate of change of the loss function with respect to the network's parameters (weights and biases). During the training process, these gradients are computed using backpropagation to adjust the model's parameters in order to minimize the loss and improve the model's performance.

> 在循环神经网络（RNN）中，梯度是指损失函数相对于网络参数（权重和偏置）的变化率。在训练过程中，这些梯度通过反向传播计算，用于调整模型参数以最小化损失并提升模型性能。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is the standard definition of gradients in RNN training. **Why True**: The gradient $\frac{\partial L}{\partial \theta}$ represents the rate of change of the loss function with respect to parameters. In RNNs, gradients are computed via BPTT (Backpropagation Through Time), then used with gradient descent to update parameters and minimize loss.
>
> > 这是 RNN 训练中梯度的标准定义。**为什么是 True**：梯度 $\frac{\partial L}{\partial \theta}$ 表示损失函数对参数的变化率，通过时序反向传播（BPTT）计算梯度，然后用梯度下降法更新参数以最小化损失。
>
> - **$\frac{\partial L}{\partial \theta}$**: Partial derivative of loss w.r.t. parameters (gradient) / 损失函数对参数的偏导数（梯度）
> - **BPTT**: Backpropagation Through Time — the specialized backpropagation algorithm for RNNs / 时序反向传播，RNN 专用的反向传播算法
>
> **Key**: Gradient = $\frac{\partial L}{\partial \theta}$, computed via BPTT in RNNs, used to minimize loss by adjusting weights and biases.
> **关键**: 梯度 = $\frac{\partial L}{\partial \theta}$，在 RNN 中通过 BPTT 计算，用于调整权重和偏置以最小化损失。

---

## Q5.2 (1 point)

"Stateful computation" in the context of Recurrent Neural Networks (RNNs) refers to maintaining internal memory states across multiple inputs.

> 在循环神经网络（RNN）中，"有状态计算"是指在多个输入之间维持内部记忆状态。

A) True
B) False

> **Answer**: A
> **Explanation**:
> The core feature of RNNs is "stateful computation" — transferring information between time steps through hidden state $h_t$. **Why True**: At each time step, the RNN receives the current input and previous hidden state: $h_t = f(W_h h_{t-1} + W_x x_t + b)$. This mechanism enables RNNs to maintain memory across multiple inputs.
>
> > RNN 的核心特征就是"有状态计算"——通过隐藏状态 $h_t$ 在时间步之间传递信息。**为什么是 True**：RNN 在每个时间步接收当前输入和上一步的隐藏状态 $h_t = f(W_h h_{t-1} + W_x x_t + b)$，使其能跨多个输入维持记忆。
>
> - **$h_t$**: Hidden state — carries historical information across time steps / 隐藏状态，携带历史信息
>
> **Key**: Stateful computation = RNN maintains hidden state $h_t$ across time steps, carrying information from previous inputs.
> **关键**: 有状态计算 = RNN 跨时间步维持隐藏状态 $h_t$，携带之前输入的信息。

---

## Q5.3 (1 point)

Publicly available datasets, such as news articles, social media posts, and web pages, are commonly used as sources of data for training NLP models, as they provide a diverse range of language usage and context.

> 公开可用的数据集（如新闻文章、社交媒体帖子和网页）通常用作训练NLP模型的数据来源，因为它们提供了多样化的语言使用和上下文。

A) True
B) False

> **Answer**: A
> **Explanation**:
> NLP model training relies on large-scale, diverse text datasets. **Why True**: News, social media, and web data cover various genres, topics, and expressions, providing rich linguistic diversity and contextual information essential for robust model training.
>
> > NLP 模型训练依赖大规模多样化文本数据集。**为什么是 True**：新闻、社交媒体、网页等公开数据涵盖了各种文体、话题和表达方式，为模型提供了丰富的语言多样性和上下文信息。
>
> **Key**: Public datasets (news, social media, web) provide diverse language patterns essential for training robust NLP models.
> **关键**: 公开数据集（新闻、社交媒体、网页）提供训练稳健 NLP 模型所需的多样化语言模式。

---

## Q5.4 (1 point)

Suppose we have the following sentence:

> 假设我们有以下句子：

"Sunny days make people feel **\_\_\_\_**."

Let's assume we have a corpus, and we count the occurrences:

> 假设我们有一个语料库，并统计了以下出现次数：

- Count("feel"): 100 occurrences
- Count("feel happy"): 40 occurrences
- Count("happy"): 30 occurrences

The conditional probability P("happy" | "feel") is:

> 条件概率 P("happy" | "feel") 是：

A) 0.2

B) 0.4

C) 0

D) 0.3

> **Answer**: B
> **Explanation**:
> Conditional probability formula: $P(w_2|w_1) = \frac{Count(w_1, w_2)}{Count(w_1)}$. **Why 0.4**:
>
> - $P(\text{"happy"} | \text{"feel"}) = \frac{Count(\text{"feel happy"})}{Count(\text{"feel"})} = \frac{40}{100} = 0.4$
> - **Note**: Count("happy") = 30 is a **distractor** — conditional probability only uses the co-occurrence count divided by the conditioning word count.
>
> > 条件概率公式：$P(w_2|w_1) = \frac{Count(w_1, w_2)}{Count(w_1)}$。**为什么是 0.4**：
> >
> > - $P(\text{"happy"} | \text{"feel"}) = \frac{40}{100} = 0.4$
> > - **注意**：Count("happy") = 30 是**干扰信息**，条件概率只用共现次数除以条件词总次数。
>
> - **$P(w_2|w_1) = \frac{Count(w_1 w_2)}{Count(w_1)}$**: N-gram conditional probability (Bigram model) / N-gram 条件概率（Bigram 模型）
>
> **Key**: $P(\text{happy}|\text{feel}) = \frac{Count(\text{feel happy})}{Count(\text{feel})} = \frac{40}{100} = 0.4$. Count("happy") alone is a distractor.
> **关键**: $P(happy|feel) = \frac{Count(feel\ happy)}{Count(feel)} = \frac{40}{100} = 0.4$。Count("happy") 单独出现是干扰信息。

---

## Q5.5 (1 point)

What is a significant advantage of Recurrent Neural Networks (RNNs) over traditional feedforward neural networks (FFNs) that makes them particularly suited for natural language processing tasks?

> 循环神经网络（RNN）相比传统前馈神经网络（FFN）的一个显著优势是什么，使其特别适合自然语言处理任务？

A) RNNs maintain an internal state that allows them to model sequential dependencies, which is crucial for tasks like language modeling and machine translation.

B) RNNs can process fixed-length input sequences, making them ideal for tasks with static input sizes.

C) RNNs only process input in a single forward pass, making them more efficient than FFNs for sequential tasks.

D) RNNs are faster to train than FFNs because they do not require backpropagation.

> **Answer**: A
> **Explanation**:
> The core advantage of RNNs over FFNs is the ability to process sequential data and model temporal dependencies. **Why A**: RNNs pass information between time steps via hidden state $h_t$, capturing sequential dependencies crucial for language modeling and machine translation.
>
> > RNN 相比 FFN 的核心优势在于能处理序列数据并建模时序依赖关系。**为什么是 A**：RNN 通过隐藏状态 $h_t$ 在时间步之间传递信息，捕捉序列中的依赖关系，对语言建模和机器翻译至关重要。
>
> - **B**: RNNs can handle **variable-length** sequences — that's precisely their advantage, not "fixed-length."
> - **C**: RNNs compute at every time step and use BPTT for backpropagation — not "a single forward pass."
> - **D**: RNNs require backpropagation (BPTT) and are typically slower than FFNs due to sequential unrolling.
>
> > - **B 错**：RNN 能处理**变长**序列，这恰恰是它的优势，不限于固定长度。
> > - **C 错**：RNN 在每个时间步都进行计算，并通过 BPTT 反向传播，不是"单次前向传播"。
> > - **D 错**：RNN 需要反向传播（BPTT），且由于序列展开通常比 FFN 更慢。
>
> **Key**: RNN advantage over FFN: internal state $h_t$ models sequential dependencies — essential for language tasks.
> **关键**: RNN 相比 FFN 的优势：内部状态 $h_t$ 建模序列依赖 — 对语言任务至关重要。

---

## Q5.6 (1 point)

Which of the following best explains why LSTMs are able to handle long-term dependencies better than standard RNNs?

> 以下哪项最能解释为什么LSTM比标准RNN更能处理长期依赖关系？

A) Because LSTMs use more hidden layers, which automatically prevent vanishing gradients.

B) Because LSTMs replace the recurrent connection with a fully connected feedforward network.

C) Because LSTMs use gating mechanisms that regulate information flow and help preserve gradients over long sequences.

D) Because LSTMs remove backpropagation and instead rely only on forward propagation.

> **Answer**: C
> **Explanation**:
> LSTMs solve the standard RNN's vanishing gradient problem through three gating mechanisms. **Why C**:
>
> - **Forget Gate**: Decides which old information to discard
> - **Input Gate**: Decides which new information to store
> - **Output Gate**: Decides which information to output
> - These gates allow gradients to flow along the cell state over long distances, preventing vanishing gradients.
>
> > LSTM 通过三个门控机制解决了标准 RNN 的梯度消失问题。**为什么是 C**：
> >
> > - **遗忘门（Forget Gate）**：决定丢弃哪些旧信息
> > - **输入门（Input Gate）**：决定存储哪些新信息
> > - **输出门（Output Gate）**：决定输出哪些信息
> > - 这些门控机制允许梯度沿细胞状态长距离传播，避免梯度消失。
>
> - **A**: More layers don't automatically prevent vanishing gradients — the key is the gating mechanism.
> - **B**: LSTMs are still recurrent architectures — they don't replace recurrence with feedforward networks.
> - **D**: LSTMs still require backpropagation for training.
>
> > - **A 错**：层数多不能自动防止梯度消失，关键是门控机制。
> > - **B 错**：LSTM 仍然是循环结构，没有替换为前馈网络。
> > - **D 错**：LSTM 仍需反向传播来训练。
>
> **Key**: LSTM gates (forget, input, output) regulate information flow, preserving gradients across long sequences — solving vanishing gradient.
> **关键**: LSTM 门控（遗忘门、输入门、输出门）调节信息流，跨长序列保持梯度 — 解决梯度消失。

---

## Q5.7 (1 point)

The core idea of an n-gram language model is to predict the next word by understanding the semantic meaning of entire sentences and applying deep reasoning.

> N-gram语言模型的核心思想是通过理解整个句子的语义含义并应用深层推理来预测下一个词。

A) True
B) False

> **Answer**: B
> **Explanation**:
> N-gram models are shallow, statistics-based methods without deep semantic understanding. **Why False**: N-gram models only rely on the frequency of the previous $n-1$ words to predict the next word ($P(w_n|w_1,...,w_{n-1})$). They don't understand sentence meaning or perform "deep reasoning."
>
> > N-gram 模型是基于统计的浅层方法，不具备深层语义理解能力。**为什么是 False**：N-gram 模型只依赖前 $n-1$ 个词的出现频率来预测下一个词，不理解句子含义，也不进行"深层推理"。
>
> - **$P(w_n|w_{n-N+1},...,w_{n-1})$**: N-gram conditional probability — only looks at the previous N-1 words / N-gram 条件概率 — 只看前 N-1 个词
> - N-gram limitations / N-gram 局限：no semantic understanding (无语义理解), fixed window size (固定窗口), sparsity (稀疏性)
>
> **Key**: N-gram = statistical frequency-based prediction from previous N-1 words. No semantic understanding or deep reasoning.
> **关键**: N-gram = 基于统计频率从前 N-1 个词预测。无语义理解，无深层推理。

---

## Q5.8 (1 point)

When the learning rate is set too low, the training process will become much faster, and the model will reach the optimal solution quickly because small weight updates allow for faster progress.

> 当学习率设置得过低时，训练过程会变得更快，模型会迅速达到最优解，因为较小的权重更新可以带来更快的进展。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Too low a learning rate causes training to become **slower**, not faster — the opposite of what the statement claims. **Why False**: A very small learning rate means each parameter update is tiny ($\theta = \theta - \alpha \cdot \nabla L$), requiring many more iterations to converge, and potentially getting stuck in local optima.
>
> > 学习率过低会导致训练**变慢**而非变快，与题干所述相反。**为什么是 False**：过小的学习率意味着每次参数更新幅度极小，需要更多迭代才能收敛，甚至可能卡在局部最优。
>
> - **Too low learning rate / 学习率过低**: Extremely slow convergence, may get stuck in local optima / 收敛极慢，可能陷入局部最优
> - **Too high learning rate / 学习率过高**: Oscillation/divergence, may skip the optimal solution / 振荡不收敛，可能跳过最优解
> - **$\alpha$**: Learning rate — controls the step size of parameter updates / 学习率，控制参数更新步长
>
> **Key**: Low learning rate → slow convergence (not faster). Too high → oscillation/divergence. Need balanced $\alpha$.
> **关键**: 低学习率 → 收敛慢（不是更快）。过高 → 振荡/发散。需要平衡的 $\alpha$。

</details>

---

# Quiz 6 — 注意力与Transformer (Attention & Transformer)

Topic: BiLSTM, Encoder-Decoder, Multi-Head Attention, Transformer, Positional Encoding, Masking

---

## Q6.1 (1 point)

BiLSTM is capable of capturing contextual information exclusively from upcoming time steps.

> BiLSTM 只能从未来的时间步捕获上下文信息。

A) True
B) False

> **Answer**: B
> **Explanation**:
> BiLSTM (Bidirectional LSTM) processes sequences in **both** directions — forward (past → future) and backward (future → past). **Why False**: The statement claims "exclusively from upcoming time steps," but BiLSTM captures context from both past AND future, not just upcoming steps.
>
> > BiLSTM（双向 LSTM）从**两个方向**处理序列 — 正向（过去→未来）和反向（未来→过去）。**为什么是 False**：题干说"只能从未来时间步"捕获信息，但 BiLSTM 同时捕获过去和未来的上下文。
>
> **Key**: BiLSTM = forward LSTM + backward LSTM. Captures both past and future context, not just one direction.
> **关键**: BiLSTM = 前向 LSTM + 后向 LSTM。同时捕获过去和未来的上下文，而非仅单方向。

---

## Q6.2 (1 point)

The Encoder-Decoder Framework is primarily used for image classification tasks.

> 编码器-解码器框架主要用于图像分类任务。

A) True
B) False

> **Answer**: B
> **Explanation**:
> The Encoder-Decoder framework is designed for **sequence-to-sequence** tasks, not image classification. **Why False**: It is primarily used for machine translation, text summarization, and text generation — tasks where the input and output are both sequences of variable length.
>
> > 编码器-解码器框架是为**序列到序列（Seq2Seq）**任务设计的，不是图像分类。**为什么是 False**：它主要用于机器翻译、文本摘要和文本生成等输入输出都是变长序列的任务。
>
> - **Encoder**: Compresses input sequence into a fixed-length context vector / 将输入序列压缩为固定长度的上下文向量
> - **Decoder**: Generates output sequence from the context vector / 从上下文向量生成输出序列
>
> > - **编码器**：将输入序列压缩为固定长度的上下文向量
> > - **解码器**：从上下文向量生成输出序列
>
> **Key**: Encoder-Decoder = Seq2Seq architecture for translation, summarization, generation. NOT for image classification.
> **关键**: 编码器-解码器 = 序列到序列架构，用于翻译、摘要、生成。不是图像分类。

---

## Q6.3 (1 point)

The primary motivation behind using multi-head self-attention is to capture different types of relationships and dependencies in the input data by allowing the model to attend to different positions at different semantic levels.

> 使用多头自注意力的主要动机是通过允许模型在不同语义层次关注不同位置，从而捕获输入数据中不同类型的关系和依赖。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Multi-head attention splits the attention computation into multiple "heads," each learning different relationship patterns. **Why True**: Different heads can focus on different aspects — one head might capture syntactic dependencies, another might capture semantic relationships, enabling richer representation.
>
> > 多头注意力将注意力计算拆分为多个"头"，每个头学习不同的关系模式。**为什么是 True**：不同的头可以关注不同的方面 — 一个头可能捕捉句法依赖，另一个可能捕捉语义关系，从而实现更丰富的表示。
>
> **Key**: Multi-head attention = multiple parallel attention mechanisms, each capturing different types of relationships.
> **关键**: 多头注意力 = 多个并行的注意力机制，每个捕获不同类型的关系。

---

## Q6.4 (1 point)

The Transformer in NLP is a novel architecture that aims to solve sequence-to-sequence tasks while handling long-range dependencies.

> NLP 中的 Transformer 是一种旨在解决序列到序列任务并处理长距离依赖的新型架构。

A) True
B) False

> **Answer**: A
> **Explanation**:
> The Transformer (2017, "Attention is All You Need") was designed specifically to handle Seq2Seq tasks with superior long-range dependency modeling. **Why True**: Unlike RNNs which process tokens sequentially, self-attention allows each token to directly attend to all other tokens, regardless of distance.
>
> > Transformer（2017，"Attention is All You Need"）专为处理 Seq2Seq 任务而设计，具有优越的长距离依赖建模能力。**为什么是 True**：与 RNN 逐步处理 token 不同，自注意力允许每个 token 直接关注所有其他 token，不受距离限制。
>
> **Key**: Transformer solves Seq2Seq + long-range dependencies via self-attention (O(1) path length between any two tokens).
> **关键**: Transformer 通过自注意力解决 Seq2Seq 和长距离依赖问题（任意两个 token 之间路径长度 O(1)）。

---

## Q6.5 (1 point)

In transformer, residual connections let each layer subtract refinements to the input rather than replace it. This preserves information across depth, prevents vanishing gradients, and makes it possible to train Transformers with dozens or hundreds of layers.

> 在 Transformer 中，残差连接让每一层对输入进行减法式精炼而非替换。这在深度上保持了信息，防止了梯度消失，使得训练数十甚至数百层的 Transformer 成为可能。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Residual connections (skip connections) add the input directly to the layer output: $\text{output} = \text{LayerNorm}(x + \text{Sublayer}(x))$. **Why True**: This preserves the original information flow, prevents vanishing gradients in deep networks, and enables training very deep Transformers.
>
> > 残差连接（跳跃连接）将输入直接加到层输出上：$\text{output} = \text{LayerNorm}(x + \text{Sublayer}(x))$。**为什么是 True**：这保持了原始信息流，防止深层网络中的梯度消失，使训练非常深的 Transformer 成为可能。
>
> - ⚠️ **Note**: The statement says "subtract refinements" — this is a conceptual description meaning each layer only needs to learn the **residual** (difference), not reconstruct the full output.
>
> > - ⚠️ **注意**：题干说"减法式精炼" — 这是概念性描述，意思是每层只需学习**残差**（差异），不用重建完整输出。
>
> **Key**: Residual connections: $\text{output} = x + \text{Sublayer}(x)$. Preserves information, prevents vanishing gradients, enables deep training.
> **关键**: 残差连接：$\text{output} = x + \text{Sublayer}(x)$。保持信息、防止梯度消失、支持深层训练。

---

## Q6.6 (1 point)

Positional encoding is a type of regularization technique that stabilizes the training process.

> 位置编码是一种稳定训练过程的正则化技术。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Positional encoding provides **sequence order information** to the Transformer, NOT regularization. **Why False**: Since the Transformer has no recurrence or convolution, it cannot inherently capture token order. Positional encoding injects position information (using sine/cosine functions) so the model knows which token is where.
>
> > 位置编码为 Transformer 提供**序列顺序信息**，而非正则化。**为什么是 False**：由于 Transformer 没有循环或卷积结构，它本身无法捕获 token 顺序。位置编码通过正弦/余弦函数注入位置信息，让模型知道每个 token 的位置。
>
> - **$PE_{(pos,2i)} = \sin(pos / 10000^{2i/d_{model}})$**: Sinusoidal positional encoding formula
> - **Regularization (正则化)**: Techniques like Dropout, L2 — these prevent overfitting, NOT encode position.
>
> > - **正则化技术**：Dropout、L2 等防止过拟合的技术，与位置编码无关。
>
> **Key**: Positional encoding = provides token order information (sin/cos). NOT regularization.
> **关键**: 位置编码 = 提供 token 顺序信息（正弦/余弦）。不是正则化。

---

## Q6.7 (1 point)

In the context of the Transformer model's attention mechanism, what does the term "scaled" refer to in the scaled dot-product attention?

> 在 Transformer 模型的注意力机制中，缩放点积注意力中的"缩放"是什么意思？

A) Scaling the input embeddings to a fixed size

B) Scaling the output probabilities to ensure they sum to one

C) Scaling the dot product of the query and key vectors by the square root of the dimensionality

D) Scaling the learning rate during training

> **Answer**: C
> **Explanation**:
> In scaled dot-product attention, the dot product of Q and K is divided by $\sqrt{d_k}$ to prevent excessively large values before softmax. **Why C**: The formula is $\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$. The "scaling" specifically refers to dividing by $\sqrt{d_k}$.
>
> > 在缩放点积注意力中，Q 和 K 的点积除以 $\sqrt{d_k}$ 以防止 softmax 前值过大。**为什么是 C**：公式为 $\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$。"缩放"特指除以 $\sqrt{d_k}$。
>
> - **A**: Scaling input embeddings is not what "scaled" refers to here.
> - **B**: Softmax naturally ensures probabilities sum to 1; that's not the "scaling."
> - **D**: Learning rate scaling is unrelated to attention mechanism.
>
> > - **A 错**：这里的"缩放"不是指缩放输入嵌入。
> > - **B 错**：Softmax 自然保证概率和为 1，这不是"缩放"的含义。
> > - **D 错**：学习率缩放与注意力机制无关。
>
> **Key**: "Scaled" = divide $QK^T$ by $\sqrt{d_k}$ to prevent large dot products that push softmax into extreme regions.
> **关键**: "缩放" = 将 $QK^T$ 除以 $\sqrt{d_k}$，防止点积过大导致 softmax 进入极端区域。

---

## Q6.8 (1 point)

Which of the following deep learning architectures commonly uses the attention mechanism?

> 以下哪种深度学习架构通常使用注意力机制？

A) Simple Feedforward Networks

B) Basic Convolutional Neural Networks

C) Transformer-based models

D) Traditional Decision Trees

> **Answer**: C
> **Explanation**:
> Attention is the core mechanism of Transformer-based models. **Why C**: Transformers are built entirely around self-attention — it is their fundamental building block, unlike FFN, CNN, or decision trees.
>
> > 注意力是 Transformer 模型的核心机制。**为什么是 C**：Transformer 完全围绕自注意力构建，这是它的基本构建模块，与 FFN、CNN 或决策树不同。
>
> - **A/B**: FFN and basic CNN do not inherently use attention (though attention can be added to CNN).
> - **D**: Decision trees are non-neural, rule-based models — no attention mechanism.
>
> > - **A/B 错**：FFN 和基本 CNN 本身不使用注意力（虽然可以给 CNN 添加注意力）。
> > - **D 错**：决策树是非神经网络的规则模型，没有注意力机制。
>
> **Key**: Transformer-based models = built on attention mechanism. FFN/CNN/Decision Trees do not inherently use attention.
> **关键**: Transformer 模型 = 基于注意力机制构建。FFN/CNN/决策树本身不使用注意力。

---

## Q6.9 (1 point)

Attention mechanisms enhance model interpretability by emphasizing the most relevant parts of the input sequences.

> 注意力机制通过强调输入序列中最相关的部分来增强模型的可解释性。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Attention weights show which input tokens the model focuses on when generating each output, making the model's decision process more transparent. **Why True**: By visualizing attention weights, we can see which parts of the input are most influential — this is a key advantage for interpretability.
>
> > 注意力权重展示了模型在生成每个输出时关注哪些输入 token，使模型决策过程更透明。**为什么是 True**：通过可视化注意力权重，我们可以看到输入的哪些部分最有影响力 — 这是可解释性的关键优势。
>
> **Key**: Attention weights are visualizable → show which input parts the model focuses on → enhanced interpretability.
> **关键**: 注意力权重可视化 → 展示模型关注输入的哪些部分 → 增强可解释性。

---

## Q6.10 (1 point)

When implementing self-attention in deep learning models, the purpose of the masking mechanism is to mask out gradients during backpropagation and speed up training.

> 在深度学习模型中实现自注意力时，掩码机制的目的是在反向传播过程中屏蔽梯度并加速训练。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Masking in self-attention is used to **hide padding tokens or future tokens**, NOT to mask gradients. **Why False**: There are two types of masking: (1) Padding mask — prevents attention to padding positions; (2) Causal/Look-ahead mask — prevents decoder from seeing future tokens during training. Neither is about masking gradients.
>
> > 自注意力中的掩码用于**隐藏填充 token 或未来 token**，而非屏蔽梯度。**为什么是 False**：掩码有两种：(1) 填充掩码 — 防止注意到填充位置；(2) 因果/前瞻掩码 — 防止解码器在训练中看到未来 token。两者都与梯度无关。
>
> - **Padding mask / 填充掩码**: Sets attention scores to $-\infty$ for padding tokens → softmax outputs 0
> - **Causal mask / 因果掩码**: Prevents decoder from "cheating" by seeing future tokens during autoregressive generation
>
> > - **填充掩码**：将填充 token 的注意力分数设为 $-\infty$ → softmax 输出 0
> > - **因果掩码**：防止解码器在自回归生成中"作弊"看到未来 token
>
> **Key**: Masking = hide padding/future tokens in attention. NOT about masking gradients or speeding up training.
> **关键**: 掩码 = 在注意力中隐藏填充/未来 token。与屏蔽梯度或加速训练无关。

---

# Quiz 7 — 问答系统 (Question Answering & Reading Comprehension)

Topic: Retriever-Reader, Fine-tuning, BiDAF, QA Tasks

---

## Q7.1 (1 point)

The objective of the Reader Retrieval Model in questioning answering task is to generate answers without considering the context of the query.

> 问答任务中读取器检索模型的目标是在不考虑查询上下文的情况下生成答案。

A) True
B) False

> **Answer**: B
> **Explanation**:
> The Reader in a Retriever-Reader QA system must **deeply consider the context** to extract or generate accurate answers. **Why False**: The Reader's entire purpose is to read the retrieved passage(s) alongside the query and understand the context to find the correct answer span.
>
> > 检索器-读取器（Retriever-Reader）QA 系统中的 Reader 必须**深入考虑上下文**以提取或生成准确答案。**为什么是 False**：Reader 的全部目的是结合查询阅读检索到的段落，理解上下文以找到正确答案。
>
> - **Retriever / 检索器**: Finds relevant documents/passages from a knowledge source
> - **Reader / 读取器**: Reads retrieved context + query → extracts answer span
>
> > - **检索器**：从知识库中寻找相关文档/段落
> > - **读取器**：阅读检索到的上下文 + 查询 → 提取答案片段
>
> **Key**: Reader MUST consider query context to extract answers. The statement claiming "without context" is wrong.
> **关键**: Reader 必须考虑查询上下文来提取答案。题干说"不考虑上下文"是错误的。

---

## Q7.2 (1 point)

In the retriever-reader architecture, the reader is usually a reading comprehension model.

> 在检索器-读取器架构中，读取器通常是一个阅读理解模型。

A) True
B) False

> **Answer**: A
> **Explanation**:
> The Reader component in Retriever-Reader QA systems is typically a reading comprehension model (e.g., BERT-based). **Why True**: The reader takes a passage and a question as input, then identifies the answer span within the passage — this is exactly the definition of a reading comprehension model.
>
> > 检索器-读取器 QA 系统中的 Reader 组件通常是一个阅读理解模型（如基于 BERT 的模型）。**为什么是 True**：Reader 以段落和问题作为输入，然后在段落中定位答案片段 — 这正是阅读理解模型的定义。
>
> **Key**: Reader = reading comprehension model (e.g., BERT). Takes question + passage → outputs answer span.
> **关键**: Reader = 阅读理解模型（如 BERT）。输入问题 + 段落 → 输出答案片段。

---

## Q7.3 (1 point)

Fine-tuning requires more data when compared to training from scratch.

> 与从头训练相比，微调需要更多的数据。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Fine-tuning requires **less** data than training from scratch because it leverages knowledge already learned during pre-training. **Why False**: The pre-trained model has already learned general language representations, so fine-tuning on a downstream task needs only a small, task-specific labeled dataset.
>
> > 微调比从头训练需要**更少的**数据，因为它利用了预训练中已经学到的知识。**为什么是 False**：预训练模型已经学习了通用语言表示，因此在下游任务上微调只需要少量的任务特定标注数据。
>
> - **Pre-training / 预训练**: Large-scale unsupervised learning on massive data (e.g., Wikipedia, BookCorpus)
> - **Fine-tuning / 微调**: Small-scale supervised learning on task-specific data (much less data needed)
>
> > - **预训练**：在大规模数据上进行无监督学习（如 Wikipedia、BookCorpus）
> > - **微调**：在任务特定数据上进行小规模监督学习（需要的数据少得多）
>
> **Key**: Fine-tuning < training from scratch in data requirements. Pre-trained models transfer learned knowledge.
> **关键**: 微调比从头训练需要更少数据。预训练模型传递已学习的知识。

---

## Q7.4 (1 point)

In BiDAF, Attention Flow Layer role is to generates word embeddings for the input text.

> 在 BiDAF 中，注意力流层的作用是为输入文本生成词嵌入。

A) True
B) False

> **Answer**: B
> **Explanation**:
> The Attention Flow Layer in BiDAF computes **bidirectional attention** between the context and query, NOT generating word embeddings. **Why False**: Word embeddings are generated by earlier layers (Character Embed Layer, Word Embed Layer). The Attention Flow Layer fuses context and query representations through context-to-query (C2Q) and query-to-context (Q2C) attention.
>
> > BiDAF 中的注意力流层计算上下文和查询之间的**双向注意力**，而非生成词嵌入。**为什么是 False**：词嵌入由前面的层（字符嵌入层、词嵌入层）生成。注意力流层通过上下文到查询（C2Q）和查询到上下文（Q2C）注意力来融合上下文和查询的表示。
>
> - **BiDAF Attention Flow**: C2Q attention + Q2C attention → fused query-aware context representation
>
> > - **BiDAF 注意力流**：C2Q 注意力 + Q2C 注意力 → 融合了查询感知的上下文表示
>
> **Key**: Attention Flow Layer = bidirectional attention (C2Q + Q2C), NOT word embedding generation.
> **关键**: 注意力流层 = 双向注意力（C2Q + Q2C），不是词嵌入生成。

---

## Q7.5 (1 point)

The primary goal of the Question Answering task in NLP reading comprehension is to generating context from given questions.

> NLP 阅读理解中问答任务的主要目标是从给定的问题生成上下文。

A) True
B) False

> **Answer**: B
> **Explanation**:
> QA reading comprehension aims to **extract answers from given context**, NOT generate context from questions. **Why False**: The direction is reversed — given a context passage and a question, the task is to find or extract the answer from the context, not to generate the context itself.
>
> > QA 阅读理解旨在**从给定上下文中提取答案**，而非从问题生成上下文。**为什么是 False**：方向反了 — 给定一个上下文段落和一个问题，任务是从上下文中查找或提取答案，而不是生成上下文本身。
>
> - **Input / 输入**: Context passage + Question
> - **Output / 输出**: Answer span extracted from the context
>
> > - **输入**：上下文段落 + 问题
> > - **输出**：从上下文中提取的答案片段
>
> **Key**: QA = extract answer from context. NOT generate context from question. Direction matters!
> **关键**: QA = 从上下文提取答案。不是从问题生成上下文。方向很重要！

---

## Q7.6 (1 point)

There is a number of similarities between translation model and reading comprehension model.

> 翻译模型和阅读理解模型之间存在许多相似之处。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Both translation and reading comprehension models share key architectural similarities. **Why True**: Both use encoder-decoder or attention-based architectures, both process input sequences to generate/extract output, and both heavily rely on attention mechanisms to align relevant parts of input with output.
>
> > 翻译模型和阅读理解模型在架构上有关键相似之处。**为什么是 True**：两者都使用编码器-解码器或基于注意力的架构，都处理输入序列以生成/提取输出，都大量依赖注意力机制来对齐输入和输出的相关部分。
>
> - **Similarities / 相似点**: Both use attention, both process sequences, both align source with target
> - **Difference / 不同点**: Translation generates new text; RC extracts spans from existing text
>
> > - **相似点**：都使用注意力，都处理序列，都对齐源和目标
> > - **不同点**：翻译生成新文本；阅读理解从现有文本中提取片段
>
> **Key**: Translation and RC share encoder-decoder architecture, attention mechanism, and sequence processing. Key overlap exists.
> **关键**: 翻译和阅读理解共享编码器-解码器架构、注意力机制和序列处理。存在关键重叠。

---

## Summary of Answers / 答案汇总

| Quiz       | Question | Answer   | Topic / 主题                                          |
| :--------- | :------- | :------- | :---------------------------------------------------- |
| **Quiz 1** | Q1.1     | C        | Transformer architecture (2017) / Transformer 架构    |
|            | Q1.2     | A        | Sentiment Analysis complexity / 情感分析复杂性        |
|            | Q1.3     | D        | NLG vs NLU (Classification) / 生成与理解的区别        |
|            | Q1.4     | A        | Document vs Knowledge / 文档与知识的区别              |
|            | Q1.5     | A        | Variation & Zipf's Law / 语言变体与齐普夫定律         |
|            | Q1.6     | D        | AI/ML/DL/NLP Relationship / 领域层级关系              |
|            | Q1.7     | B        | Text Summarization goals / 文本摘要的目标             |
|            | Q1.8     | A        | Goal of NLP / NLP 的核心目标                          |
|            | Q1.9     | B        | AI vs ML concepts / AI 与 ML 的基本概念               |
|            | Q1.10    | A        | Turing Test / 图灵测试                                |
| **Quiz 2** | Q2.1     | A        | Tokenization process / 分词过程                       |
|            | Q2.2     | B        | Stemming in Poetry / 诗歌分析中的词干提取             |
|            | Q2.3     | A        | SpaCy Stemming support / SpaCy 对词干提取的支持       |
|            | Q2.4     | B        | Regex for Compound Words / 复合词正则表达式           |
|            | Q2.5     | A        | Text Cleaning benefits / 文本清洗的作用               |
|            | Q2.6     | B        | Python Vowel Check / Python 元音字符检查              |
|            | Q2.7     | A        | Lemmatization vs Stemming / 词元化与词干提取对比      |
|            | Q2.8     | B        | Stemming Action Example / 词干提取动作示例            |
|            | Q2.9     | B        | Regex `\w*d+` match logic / 正则匹配逻辑              |
| **Quiz 3** | Q3.1     | C        | Edit Distance calculation / 编辑距离计算              |
|            | Q3.2     | B        | Bag of Words features / 词袋模型特征                  |
|            | Q3.3     | A        | IDF calculation formula / IDF 计算公式                |
|            | Q3.4     | A        | Cosine Similarity meaning / 余弦相似度含义            |
|            | Q3.5     | C        | TF-IDF limitations / TF-IDF 的局限性                  |
|            | Q3.6     | B        | TF values sorting / TF 值排序                         |
|            | Q3.7     | 0.8421   | Cosine Similarity calculation / 余弦相似度计算        |
|            | Q3.8     | B        | CountVectorizer n-grams / 词频向量化与 N-gram         |
| **Quiz 4** | Q4.1     | True     | TF-IDF dimensionality / TF-IDF 的高维特性             |
|            | Q4.2     | Option 2 | Word Analogy (boy-girl) / 词类比运算                  |
|            | Q4.3     | True     | Self-supervised learning / 自监督学习                 |
|            | Q4.4     | True     | GloVe Global+Local / GloVe 的全局与局部特性           |
|            | Q4.5     | False    | Embedding dimensionality / 嵌入向量的维度             |
|            | Q4.6     | 100      | Gensim Word2Vec default / Gensim 默认维度             |
|            | Q4.7     | True     | Word2Vec CBOW & Skip-gram                             |
|            | Q4.8     | False    | Skip-gram objective / Skip-gram 的预测方向            |
|            | Q4.9     | False    | Embeddings in modern NLP / 嵌入在现代 NLP 中的地位    |
| **Quiz 5** | Q5.1     | True     | RNN gradient & backpropagation / RNN 梯度与反向传播   |
|            | Q5.2     | True     | RNN stateful computation / RNN 有状态计算             |
|            | Q5.3     | True     | NLP training data sources / NLP 训练数据来源          |
|            | Q5.4     | 0.4      | Conditional probability (bigram) / 条件概率（二元组） |
|            | Q5.5     | A        | RNN vs FFN advantage / RNN 相比 FFN 的优势            |
|            | Q5.6     | C        | LSTM gating mechanisms / LSTM 门控机制                |
|            | Q5.7     | False    | N-gram limitations / N-gram 局限性                    |
|            | Q5.8     | False    | Learning rate effects / 学习率影响                    |
| **Quiz 6** | Q6.1     | False    | BiLSTM context direction / BiLSTM 上下文方向          |
|            | Q6.2     | False    | Encoder-Decoder purpose / 编码器-解码器用途           |
|            | Q6.3     | True     | Multi-head attention / 多头注意力                     |
|            | Q6.4     | True     | Transformer Seq2Seq / Transformer 序列到序列          |
|            | Q6.5     | True     | Residual connections / 残差连接                       |
|            | Q6.6     | False    | Positional encoding / 位置编码                        |
|            | Q6.7     | C        | Scaled dot-product attention / 缩放点积注意力         |
|            | Q6.8     | C        | Attention in architectures / 使用注意力的架构         |
|            | Q6.9     | True     | Attention interpretability / 注意力可解释性           |
|            | Q6.10    | False    | Masking mechanism / 掩码机制                          |
| **Quiz 7** | Q7.1     | False    | Reader context usage / 读取器上下文使用               |
|            | Q7.2     | True     | Reader as RC model / 读取器作为阅读理解模型           |
|            | Q7.3     | False    | Fine-tuning data needs / 微调数据需求                 |
|            | Q7.4     | False    | BiDAF Attention Flow / BiDAF 注意力流                 |
|            | Q7.5     | False    | QA task direction / QA 任务方向                       |
|            | Q7.6     | True     | Translation vs RC / 翻译与阅读理解对比               |
