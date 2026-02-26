# CST8507 NLP Mock Test — 模拟测试 (W1–W6 Full Coverage)

> 62 multiple-choice / true-false questions covering ALL knowledge points from W1–W6 cheat sheet.
> 62 道选择/判断题，全面覆盖 W1–W6 cheat sheet 所有知识点。

---

# W1: NLP Overview — NLP 概述 (10 questions)

---

## Q1.1 (1 point)

NLP is a subfield that sits at the intersection of Linguistics, Computer Science, and Artificial Intelligence, enabling computers to process, understand, and generate human language.

> NLP 是语言学、计算机科学和人工智能交叉领域的子领域，使计算机能够处理、理解和生成人类语言。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is the standard definition of NLP. NLP = subfield of Linguistics × CS × AI.
>
> > 这是 NLP 的标准定义。NLP = 语言学 × 计算机科学 × 人工智能 的交叉领域。
>
> **Key**: NLP sits at the intersection of Linguistics, CS, and AI.
> **关键**: NLP 位于语言学、CS 和 AI 的交叉点。

---

## Q1.2 (1 point)

Which of the following correctly describes the hierarchy of AI, ML, DL, and NLP?

> 以下哪项正确描述了 AI、ML、DL 和 NLP 的层级关系？

A) AI ⊃ ML ⊃ DL; NLP is an application domain of AI that spans all levels

B) DL ⊃ ML ⊃ AI; NLP is a subset of DL only

C) AI, ML, and DL are independent fields; NLP connects them

D) NLP ⊃ AI ⊃ ML ⊃ DL

> **Answer**: A
> **Explanation**:
> AI is the broadest concept, ML is a core subset of AI, DL is a branch of ML. NLP is an **application domain** of AI that spans all levels (heuristics, ML, DL) — it is NOT a technique level.
>
> > AI 是最广泛的概念，ML 是 AI 的核心子集，DL 是 ML 的分支。NLP 是 AI 的**应用领域**，跨越所有层级（启发式、ML、DL）——不是一个技术层级。
>
> **Key**: AI ⊃ ML ⊃ DL. NLP = application domain spanning all levels.

---

## Q1.3 (1 point)

AI aims to create systems that rely only on fixed rules and do not involve learning, while machine learning is an unrelated field that does not use data to make predictions.

> AI 旨在创建仅依赖固定规则且不涉及学习的系统，而机器学习是一个与之无关的领域，不使用数据进行预测。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Both claims are wrong.** Modern AI is not limited to fixed rules — it includes learning-based approaches. ML is a core subset of AI (not unrelated) that specifically learns from data to make predictions.
>
> > ⚠️ **两个断言都错。** 现代 AI 不仅限于固定规则，还包括基于学习的方法。ML 是 AI 的核心子集（不是无关领域），专门通过数据学习做预测。
>
> **Key**: AI includes learning; ML is a core subset of AI that learns from data.

---

## Q1.4 (1 point)

A document is a raw or semi-structured piece of text (such as an article or report), whereas knowledge refers to structured, interpreted information such as facts, entities, or relationships extracted from documents. More than 80% of enterprise data is unstructured.

> 文档是原始或半结构化文本（如文章或报告），知识是从文档中提取的结构化信息（如事实、实体、关系）。超过 80% 的企业数据是非结构化的。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Document = raw/semi-structured text; Knowledge = structured, interpreted information extracted from documents. The claim that >80% of enterprise data is unstructured is also accurate.
>
> > 文档 = 原始/半结构化文本；知识 = 从文档中提取的结构化解释信息。企业数据中超过 80% 是非结构化数据也是正确的。
>
> **Key**: Document = raw text; Knowledge = structured facts/entities/relations. >80% enterprise data = unstructured.

---

## Q1.5 (1 point)

In the Turing Test (1950), a human evaluator interacts via text with one human and one machine. If the evaluator cannot reliably distinguish which is the machine, the machine is said to have passed the test. The core criterion is the ability to understand and generate language.

> 在图灵测试（1950）中，人类评估者通过文本与一个人和一台机器交互。如果评估者无法可靠地判断哪个是机器，则该机器通过了测试。核心标准是理解和生成语言的能力。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is an accurate description of the Turing Test. The evaluator communicates via text only, and the machine passes if it's indistinguishable from the human.
>
> > 这是对图灵测试的准确描述。评估者仅通过文本交流，如果机器无法被区分则通过测试。
>
> **Key**: Turing Test (1950) — text-based interaction, indistinguishable = pass, language ability ≈ intelligence.

---

## Q1.6 (1 point)

Sentiment Analysis is classified as NLG (Natural Language Generation) because it generates emotional labels for text.

> 情感分析属于 NLG（自然语言生成），因为它为文本生成情感标签。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ Sentiment Analysis is **NLU** (Natural Language Understanding), not NLG. It classifies/understands the sentiment in text — it does not generate new natural language text. Generating a label is classification, not text generation.
>
> > ⚠️ 情感分析是 **NLU**（自然语言理解），不是 NLG。它对文本中的情感进行分类/理解——不生成新的自然语言文本。生成标签是分类，不是文本生成。
>
> **Key**: Sentiment Analysis = NLU (understanding). Text Classification = NLU. NLG = producing new text (translation, summarization, ChatGPT).

---

## Q1.7 (1 point)

Which NLP challenge does the following example illustrate? The word "bank" can mean a financial institution or the side of a river.

> 以下示例说明了哪个 NLP 挑战？"bank" 可以指金融机构或河岸。

A) Sparsity

B) Variation

C) Ambiguity (lexical)

D) Common Knowledge

> **Answer**: C
> **Explanation**:
> One word having multiple meanings is **lexical ambiguity** — a subcategory of the Ambiguity challenge. Syntactic ambiguity = sentence structure ("saw man with telescope"). Referential ambiguity = pronoun reference ("she" refers to whom?).
>
> > 一个词有多个含义是**词汇歧义**——歧义性挑战的子类。句法歧义 = 句子结构。指代歧义 = 代词指代。
>
> - **A**: Sparsity = Zipf's Law, few frequent words, many rare words.
> - **B**: Variation = same meaning expressed many ways (regional, social, stylistic).
> - **D**: Common Knowledge = machines lack world knowledge ("man bit dog" = news).
>
> **Key**: "bank" = lexical ambiguity. Three types: Lexical (word meaning), Syntactic (structure), Referential (pronoun).

---

## Q1.8 (1 point)

Text summarization is challenging because the system must select the most important information while maintaining coherence, context, and meaning from the original text. In text summarization, there is no need to maintain the overall meaning and coherence of the original text while extracting key information.

> 文本摘要具有挑战性，因为系统必须在保持连贯性、上下文和原意的同时选取最重要的信息。在文本摘要中，提取关键信息时不需要保持原文的整体含义和连贯性。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Trap question**: The first sentence is correct, but the second sentence directly contradicts it. Summarization **MUST** preserve original meaning and coherence.
>
> > ⚠️ **陷阱题**：第一句正确，但第二句直接矛盾。摘要**必须**保持原文含义和连贯性。
>
> **Key**: Summarization MUST preserve meaning + coherence. Read the ENTIRE statement carefully for contradictions.

---

## Q1.9 (1 point)

Which of the following is NOT one of the three main approaches to NLP?

> 以下哪项不是 NLP 的三种主要方法之一？

A) Heuristics (Rules / Regex)

B) Machine Learning (Supervised / Unsupervised)

C) Deep Learning (RNN, LSTM, Transformer)

D) Quantum Computing

> **Answer**: D
> **Explanation**:
> The three approaches to NLP are: (1) Heuristics (rule-based/regex), (2) ML (learn from labeled data), (3) DL (learn representations + rules: RNN, LSTM, Transformer). Quantum Computing is not one of them.
>
> > NLP 的三种方法：(1) 启发式（基于规则/正则），(2) 机器学习（从标注数据学习），(3) 深度学习（学习表示+规则：RNN、LSTM、Transformer）。量子计算不是其中之一。
>
> **Key**: 3 NLP approaches: Heuristics, ML, DL. Each corresponds to increasing complexity and capability.

---

## Q1.10 (1 point)

In the NLP Development Life Cycle, the correct order is: Requirements gathering → Data collection → Feature extraction → Text preprocessing → Model building → Evaluation → Deployment.

> 在 NLP 开发生命周期中，正确顺序是：需求收集 → 数据收集 → 特征提取 → 文本预处理 → 模型构建 → 评估 → 部署。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ Text preprocessing must come BEFORE feature extraction, not after. Correct order: Requirements → Data collection → **Text preprocessing** → **Feature extraction** → Model building → Evaluation → Deployment → Iterate.
>
> > ⚠️ 文本预处理必须在特征提取之前，不是之后。正确顺序：需求收集 → 数据收集 → **文本预处理** → **特征提取** → 模型构建 → 评估 → 部署 → 迭代。
>
> **Key**: Preprocessing comes BEFORE feature extraction. Raw data must be cleaned before extracting features.

---

# W2: Text Preprocessing — 文本预处理 (12 questions)

---

## Q2.1 (1 point)

The standard text preprocessing pipeline order is: Documents → Tokenization → Noise Entities Removal → Normalization.

> 标准文本预处理流水线顺序为：文档 → 分词 → 噪声实体移除 → 规范化。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Tokenization (split into tokens) → Noise Removal (remove stop words, punctuation, etc.) → Normalization (stemming/lemmatization). Tokenization is always the **FIRST** step because you need tokens before you can clean or normalize them.
>
> > 分词（切分为 token）→ 噪声移除（去除停用词、标点等）→ 规范化（词干提取/词元化）。分词始终是**第一步**，因为需要先有 token 才能清洗和规范化。
>
> **Key**: Tokenization → Noise Removal → Normalization. Pipeline may vary by task.

---

## Q2.2 (1 point)

Stop words are rare, semantically rich words that carry important meaning and should always be preserved in NLP preprocessing.

> 停用词是稀有的、语义丰富的词，携带重要含义，在 NLP 预处理中应始终保留。

A) True
B) False

> **Answer**: B
> **Explanation**:
> Stop words are the OPPOSITE — they are **high-frequency, low-semantic** words (the, is, at, a, etc.) that are typically removed during preprocessing because they add noise without adding meaningful information.
>
> > 停用词恰恰相反——它们是**高频、低语义**的词（the、is、at、a 等），通常在预处理中被移除，因为它们增加噪声而不增加有意义的信息。
>
> **Key**: Stop words = high-frequency, low-semantic (the, is, at). Removed during noise removal step.

---

## Q2.3 (1 point)

Stemming uses rule-based suffix stripping and may produce non-dictionary words (e.g., "studying" → "studi"), while Lemmatization uses dictionary lookup and POS analysis to always output valid dictionary words (e.g., "was" → "be").

> 词干提取使用基于规则的后缀剥离，可能产生非词典词（如 "studying" → "studi"），而词元化使用词典查询和词性分析，始终输出有效词典词（如 "was" → "be"）。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This accurately describes the key difference. Stemming = fast, rule-based, crude (may produce "studi"). Lemmatization = slower, dictionary-based, accurate (always valid words like "be", "good").
>
> > 这准确描述了关键区别。词干提取 = 快速、基于规则、粗糙（可能产出 "studi"）。词元化 = 较慢、基于词典、准确（总是有效词如 "be"、"good"）。
>
> **Key**: Stemming = suffix stripping, may produce invalid words. Lemmatization = dictionary lookup + POS, always valid.

---

## Q2.4 (1 point)

Pick the stemming action:

> 选出词干提取（stemming）的操作：

A) was, am, is, are → be

B) helped, helps → help

C) better → good

> **Answer**: B
> **Explanation**:
> "helped" strips `-ed`, "helps" strips `-s` — both achieve "help" through simple suffix removal. This is pure rule-based stemming.
>
> > "helped" 去掉 `-ed`，"helps" 去掉 `-s`——都通过简单后缀移除得到 "help"。这是纯规则操作。
>
> - **A**: "was/am/is/are → be" requires dictionary knowledge for irregular verb forms = **Lemmatization**.
> - **C**: "better → good" requires dictionary knowledge for irregular adjective forms = **Lemmatization**.
>
> **Key**: Stemming = simple suffix removal (-ed, -s, -ing). Irregular forms (was→be, better→good) = Lemmatization.

---

## Q2.5 (1 point)

For which of the following tasks should we NOT do stemming or lemmatization?

> 对于以下哪项任务不应该进行词干提取或词元化？

A) Text Classification

B) Poetry Analysis

C) Information Retrieval

D) Text Clustering

> **Answer**: B
> **Explanation**:
> ⚠️ In poetry analysis, word forms, tenses, and endings are crucial for rhyme, rhythm, and rhetoric. Stemming/lemmatization would destroy these features. All other tasks benefit from normalization.
>
> > ⚠️ 诗歌分析中，词形、时态和词尾对押韵、节奏和修辞至关重要。词干提取/词元化会破坏这些特征。其他任务均受益于规范化。
>
> **Key**: Poetry analysis: do NOT stem/lemmatize (rhyme/rhythm are crucial).

---

## Q2.6 (1 point)

SpaCy provides built-in functions for both Stemming and Lemmatization, just like NLTK.

> SpaCy 和 NLTK 一样，提供了词干提取和词元化的内置功能。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ SpaCy has **NO built-in Stemming** — it only provides Lemmatization. NLTK has BOTH (PorterStemmer, SnowballStemmer for stemming + WordNetLemmatizer for lemmatization).
>
> > ⚠️ SpaCy **没有内置词干提取**——只提供词元化。NLTK 两者都有（PorterStemmer、SnowballStemmer 用于词干提取 + WordNetLemmatizer 用于词元化）。
>
> **Key**: SpaCy = Lemmatization only, NO Stemming. NLTK = both Stemming + Lemmatization.

---

## Q2.7 (1 point)

Among NLTK's stemmers, which is the most aggressive and may over-stem words?

> 在 NLTK 的词干提取器中，哪个最激进且可能过度词干化？

A) Porter Stemmer (most common, least aggressive)

B) Snowball Stemmer (improved Porter, multi-language)

C) Lancaster Stemmer (most aggressive)

> **Answer**: C
> **Explanation**:
> Lancaster Stemmer is the most aggressive stemmer in NLTK. Aggressiveness ranking: Lancaster > Snowball > Porter. Porter is the most commonly used and least aggressive.
>
> > Lancaster Stemmer 是 NLTK 中最激进的词干提取器。激进程度：Lancaster > Snowball > Porter。Porter 最常用且最温和。
>
> **Key**: Lancaster (most aggressive) > Snowball (improved Porter) > Porter (least aggressive, most common).

---

## Q2.8 (1 point)

POS tagging labels grammatical roles such as NN (noun), VB (verb), JJ (adjective), RB (adverb), DT (determiner), PRP (pronoun). NER identifies named entities such as PERSON, LOCATION, ORGANIZATION. Which of the following is a POS tag, NOT an NER entity type?

> POS 标注标记语法角色如 NN（名词）、VB（动词）等。NER 识别命名实体如 PERSON、LOCATION。以下哪个是 POS 标签而不是 NER 实体类型？

A) PERSON

B) JJ (adjective)

C) GPE (Geo-Political Entity)

D) MONEY

> **Answer**: B
> **Explanation**:
> JJ (adjective) is a POS tag — it labels the grammatical role of a word. PERSON, GPE, and MONEY are all NER entity types that identify specific named entities in text.
>
> > JJ（形容词）是 POS 标签——标记词的语法角色。PERSON、GPE 和 MONEY 都是 NER 实体类型。
>
> **Key**: POS tags = NN, VB, JJ, RB, DT, PRP (grammar). NER entities = PERSON, LOCATION, ORG, DATE, MONEY (named entities).

---

## Q2.9 (1 point)

The following regex will match all the words ended with a hyphen(-):

> 以下正则表达式将匹配所有以连字符（-）结尾的单词：

`rgx = r'\b\w+[-]\w+\b'`

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Regex trap**: `\b\w+[-]\w+\b` requires `\w+` (one or more word characters) on BOTH sides of the hyphen. This matches **compound words with a hyphen in the middle** (e.g., "high-tech", "well-known"), NOT words ending with a hyphen.
>
> > ⚠️ **正则陷阱**：`\b\w+[-]\w+\b` 要求连字符两侧都有 `\w+`。这匹配**中间含连字符的复合词**（如 "high-tech"），不是以连字符结尾的词。
>
> **Key**: `\b\w+[-]\w+\b` = hyphenated compound words (high-tech). NOT words ending with hyphen.

---

## Q2.10 (1 point)

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
> The regex `[a-zA-Z]\w*d+` matches substrings starting with a letter, followed by any word characters, ending with one or more `d`. Since `\w` includes digits, it matches multiple substrings in the text, not just `'and'`.
>
> > 正则 `[a-zA-Z]\w*d+` 匹配以字母开头、任意单词字符、以一个或多个 `d` 结尾的子串。由于 `\w` 包含数字，会匹配多个子串，不只是 `'and'`。
>
> **Key**: `[a-zA-Z]\w*d+` matches any substring starting with letter, ending with 'd'. Output includes multiple matches, not just 'and'.

---

## Q2.11 (1 point)

The `re.match()` function searches for a pattern match at the **start** of the string only, while `re.search()` finds the **first** occurrence anywhere in the string.

> `re.match()` 只在字符串**开头**搜索模式匹配，而 `re.search()` 在字符串**任意位置**查找第一次匹配。

A) True
B) False

> **Answer**: A
> **Explanation**:
> `re.match(r'\d+', 'abc123')` returns None (no digit at start). `re.search(r'\d+', 'abc123')` returns match for '123' (found anywhere). `re.findall()` returns ALL matches as a list. `re.sub()` replaces matches.
>
> > `re.match(r'\d+', 'abc123')` 返回 None（开头不是数字）。`re.search(r'\d+', 'abc123')` 返回 '123' 的匹配（任意位置）。`re.findall()` 返回所有匹配列表。`re.sub()` 替换匹配。
>
> **Key**: match = START only. search = FIRST anywhere. findall = ALL matches. sub = REPLACE.

---

## Q2.12 (1 point)

Which Python expression correctly outputs state names that start AND end with a vowel character?

> 哪个 Python 表达式正确输出以元音字符开头且结尾的州名？

A) `[s for s in states if s[0].lower() in 'aeiou' and s[1] in 'aeiou']`

B) `[s for s in states if s[0].lower() in 'aeiou' and s[-1].lower() in 'aeiou']`

C) `[s for s in states if s[1].lower() in 'aeiou' and s[-1] in 'aeiou']`

> **Answer**: B
> **Explanation**:
> `s[0]` = first character, `s[-1]` = last character. Both need `.lower()` and check `in 'aeiou'`. Option A uses `s[1]` (second char) for the end check, Option C uses `s[1]` for the start check — both wrong.
>
> > `s[0]` = 首字符，`s[-1]` = 末字符。都需要 `.lower()` 并检查 `in 'aeiou'`。A 用 `s[1]`（第二字符）检查尾部，C 用 `s[1]` 检查首部——都错。
>
> **Key**: `s[0]` = first char, `s[-1]` = last char. Python string indexing: 0-based, -1 = last.

---

# W3: Text Vectorization & Similarity — 文本向量化与相似度 (10 questions)

---

## Q3.1 (1 point)

In a Bag of Words representation, the order of words in a document is crucial, and each word is treated as dependent on its surrounding words.

> 在词袋（Bag of Words）表示中，文档中单词的顺序至关重要，每个单词都被视为依赖于其周围的单词。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ BOW **IGNORES word order** and treats each word as an **independent** feature. "John is quicker than Mary" and "Mary is quicker than John" produce the **same BOW vector** — opposite meanings are lost.
>
> > ⚠️ BOW **忽略词序**，将每个词视为**独立**特征。"John is quicker than Mary" 和 "Mary is quicker than John" 产生**相同的 BOW 向量**——相反的含义丢失。
>
> **Key**: BOW = ignores word order, treats words independently, only cares about frequency.

---

## Q3.2 (1 point)

N-grams partially restore word order by using consecutive N words as features. However, the feature count explodes as $V^N$ (where V = vocabulary size), making higher-order N-grams impractical.

> N-gram 通过使用连续 N 个词作为特征部分恢复词序。然而特征数量以 $V^N$ 爆炸增长（V = 词汇表大小），使高阶 N-gram 不实用。

A) True
B) False

> **Answer**: A
> **Explanation**:
> N-grams capture partial word order (bigram = 2-word sequences, trigram = 3-word sequences). But the feature space grows as $V^N$, which becomes extremely large for higher N values. Also still suffers from sparsity and OOV issues.
>
> > N-gram 捕捉部分词序。但特征空间以 $V^N$ 增长，高阶 N 值时变得极大。且仍然存在稀疏性和 OOV 问题。
>
> **Key**: N-gram = partial word order, but feature explosion $V^N$. Unigram → Bigram → Trigram.

---

## Q3.3 (1 point)

One of the disadvantages of using TF-IDF is:

> 使用 TF-IDF 的缺点之一是：

A) It produces low-dimensional dense vectors

B) It considers the context and semantic relationships between words

C) It does not consider the context and semantic relationships between words

D) It captures word order information

> **Answer**: C
> **Explanation**:
> TF-IDF is a bag-of-words statistical method — it only measures word frequency × inverse document frequency. It has **NO** semantic understanding, **NO** context awareness, and **NO** word order information. It produces high-dimensional sparse vectors.
>
> > TF-IDF 是词袋统计方法——只衡量词频 × 逆文档频率。**没有**语义理解、**没有**上下文感知、**没有**词序信息。产出高维稀疏向量。
>
> - **A**: TF-IDF produces HIGH-dimensional SPARSE vectors (not low-dim dense).
> - **B/D**: These are capabilities TF-IDF does NOT have.
>
> **Key**: TF-IDF = high-dim sparse, no semantics, no context, no word order. Not suitable for DL.

---

## Q3.4 (1 point)

Given the following TF values for a word "data" across different documents:

> 给定词 "data" 在不同文档中的 TF 值：

| Document | TF Calculation | TF Value |
| -------- | -------------- | -------- |
| d1       | 25/127         | ≈ 0.197  |
| d2       | 3/250          | = 0.012  |
| d3       | 20/650         | ≈ 0.031  |
| d9       | 15/125         | = 0.120  |
| d1000    | 20/800         | = 0.025  |

The proposed ascending order by TF is: [d2, d1000, d3, d1, d9]

> 提出的按 TF 升序排列为：[d2, d1000, d3, d1, d9]

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ Calculate and sort: d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197). The proposed order swaps d1 and d9. Correct ascending order: **[d2, d1000, d3, d9, d1]**.
>
> > ⚠️ 计算排序：d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197)。提出的排序将 d1 和 d9 位置反了。正确升序：**[d2, d1000, d3, d9, d1]**。
>
> **Key**: Correct ascending TF: [d2, d1000, d3, d9, d1]. d1(0.197) > d9(0.120), not the other way around.

---

## Q3.5 (1 point)

If a word appears in every document in the corpus ($df(t) = N$), its IDF value is:

> 如果一个词出现在语料库中的每个文档中（$df(t) = N$），其 IDF 值为：

A) $\log(N)$ — very high

B) $1$

C) $0$

D) Undefined

> **Answer**: C
> **Explanation**:
> $IDF(t) = \log\frac{N}{df(t)} = \log\frac{N}{N} = \log(1) = 0$. Words in every document get zero weight — they provide no discriminative power. Conversely, a word in only 1 document gets $IDF = \log(N)$ (highest).
>
> > $IDF(t) = \log\frac{N}{N} = \log(1) = 0$。出现在每个文档中的词权重为零——没有区分能力。相反，只出现在 1 个文档中的词 $IDF = \log(N)$（最高）。
>
> **Key**: Word in all docs → IDF = 0. Word in 1 doc → IDF = log(N). IDF downweights common words.

---

## Q3.6 (1 point)

`CountVectorizer` counts raw word occurrences, so common words like "the" and "is" get high counts. `TfidfVectorizer` applies TF-IDF weighting, which downweights common words and upweights rare discriminative words like "milk".

> `CountVectorizer` 统计原始词频，常见词如 "the" 和 "is" 获得高计数。`TfidfVectorizer` 应用 TF-IDF 加权，降低常见词权重，提升稀有区分词如 "milk" 的权重。

A) True
B) False

> **Answer**: A
> **Explanation**:
> CountVectorizer = raw counts (common words dominate). TfidfVectorizer = TF-IDF weighted (common words downweighted, rare words upweighted). Example: "hot" in many docs → high count but low TF-IDF; "milk" is rare → better differentiator with TF-IDF.
>
> > CountVectorizer = 原始计数（常见词占主导）。TfidfVectorizer = TF-IDF 加权（常见词降权，稀有词升权）。
>
> **Key**: CountVectorizer = raw counts. TfidfVectorizer = weighted (upweights rare, downweights common).

---

## Q3.7 (1 point)

```python
cv = CountVectorizer(ngram_range=(1,2)).fit(
    ["I love NLP", "He love NLP", "good man"]
)
cv.transform(["love"]).toarray()
```

Claimed output: `array([[0, 0, 1, 0, 0, 0, 0]], dtype=int64)`

> 声称的输出: `array([[0, 0, 1, 0, 0, 0, 0]], dtype=int64)`

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ `CountVectorizer(ngram_range=(1,2))` generates BOTH unigrams AND bigrams. The vocabulary includes: unigrams ("good", "he", "love", "man", "nlp") + bigrams ("good man", "he love", "love nlp") = at least **8 features**, so the vector length should be 8+, NOT 7.
>
> > ⚠️ `CountVectorizer(ngram_range=(1,2))` 同时生成 unigram 和 bigram。词汇表包括：5 个 unigram + 3 个 bigram = 至少 **8 个特征**，向量长度应为 8+，不是 7。
>
> **Key**: ngram_range=(1,2) → unigrams + bigrams. The claimed vector length (7) is incorrect — should be 8+.

---

## Q3.8 (1 point)

Cosine Similarity measures the angle between two vectors and is independent of document length, while Euclidean Distance measures the straight-line distance and IS affected by document length.

> 余弦相似度衡量两个向量之间的角度且不受文档长度影响，而欧几里得距离衡量直线距离且受文档长度影响。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Cosine Similarity: $\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \times ||\vec{B}||}$, range $[-1, 1]$, length-independent. Euclidean Distance: $d = \sqrt{\sum(a_i - b_i)^2}$, range $[0, \infty)$, affected by magnitude/length. Levenshtein Distance: min edit operations (insert/delete/substitute), string-level.
>
> > 余弦相似度范围 $[-1, 1]$，不受长度影响。欧几里得距离范围 $[0, \infty)$，受大小/长度影响。编辑距离：最小编辑操作数，字符串级别。
>
> **Key**: Cosine = angle, length-independent. Euclidean = distance, length-dependent. Levenshtein = edit ops.

---

## Q3.9 (1 point)

Given two word vectors $w_1 = (0.2, 0.2, 0.3, 0.7)$ and $w_2 = (0.3, 0.4, 0.8, 0.5)$, the cosine similarity is approximately:

> 给定两个词向量 $w_1 = (0.2, 0.2, 0.3, 0.7)$ 和 $w_2 = (0.3, 0.4, 0.8, 0.5)$，余弦相似度约为：

A) 0.5000

B) 0.7300

C) 0.8421

D) 1.0000

> **Answer**: C
> **Explanation**:
> Step by step: Dot product = $0.06+0.08+0.24+0.35 = 0.73$. $||w_1|| = \sqrt{0.04+0.04+0.09+0.49} = \sqrt{0.66} \approx 0.8124$. $||w_2|| = \sqrt{0.09+0.16+0.64+0.25} = \sqrt{1.14} \approx 1.0677$. $\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$.
>
> > 逐步计算：点积 = 0.73。$||w_1|| \approx 0.8124$。$||w_2|| \approx 1.0677$。$\cos(\theta) \approx 0.8421$。
>
> **Key**: $\cos(\theta) = \frac{dot(A,B)}{||A|| \times ||B||} = \frac{0.73}{0.8124 \times 1.0677} \approx 0.8421$.

---

## Q3.10 (1 point)

The minimum number of edit operations (insert, delete, substitute) to transform "intention" into "execution" is:

> 将 "intention" 转换为 "execution" 的最少编辑操作（插入、删除、替换）次数是：

A) 3

B) 4

C) 5

D) 6

> **Answer**: C
> **Explanation**:
> This is the classic Levenshtein edit distance problem solved by dynamic programming. "intention" → "execution" requires a minimum of **5 operations**. Also remember: "kitten" → "sitting" = 3 operations.
>
> > 这是经典的编辑距离问题，通过动态规划求解。"intention" → "execution" 最少需要 **5 步操作**。另外记住："kitten" → "sitting" = 3 步。
>
> **Key**: intention → execution = 5 edits. kitten → sitting = 3 edits. Solved by dynamic programming.

---

# W4: Word Embeddings — 词嵌入 (10 questions)

---

## Q4.1 (1 point)

In WordNet, "dog" is a hyponym of "animal" (dog IS-A animal), and "wheel" is a meronym of "car" (wheel PART-OF car). These two relationship types should NOT be confused.

> 在 WordNet 中，"dog" 是 "animal" 的下位词（dog IS-A animal），"wheel" 是 "car" 的部分词（wheel PART-OF car）。这两种关系类型不应混淆。

A) True
B) False

> **Answer**: A
> **Explanation**:
> ⚠️ Hypernym/Hyponym = **IS-A** relationship (animal↔dog). Meronym/Holonym = **PART-OF** relationship (wheel↔car). These are commonly confused on exams. Other WordNet relations: Synset (synonym set), Antonym (opposite), Troponym (manner of verb), Entailment (implies).
>
> > ⚠️ 上位词/下位词 = **IS-A** 关系。部分词/整体词 = **PART-OF** 关系。考试常混淆。其他 WordNet 关系：同义词集、反义词、方式动词、蕴含。
>
> **Key**: Hypernym/Hyponym = IS-A. Meronym/Holonym = PART-OF. Don't confuse them!

---

## Q4.2 (1 point)

Suppose you learn a word embedding for a vocabulary of 1000 words. The embedding vectors should be 1000 dimensional to capture the full range of variation and meaning in those words.

> 假设你为 1000 个单词的词汇表学习词嵌入。嵌入向量应该是 1000 维的，以捕捉这些词的全部变化和含义。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ 1000 dimensions = one-hot encoding size, which defeats the entire purpose of embeddings. The core value of word embeddings is **dimensionality reduction** — typical dimensions are **50–300**, compressing semantic information into a low-dimensional dense space.
>
> > ⚠️ 1000 维 = one-hot 编码的维度，完全违背了嵌入的目的。词嵌入的核心价值是**降维**——典型维度为 **50-300**，将语义信息压缩到低维密集空间。
>
> **Key**: Embedding dim = 50–300 (NOT vocab size). 1000-dim = one-hot, defeats the purpose.

---

## Q4.3 (1 point)

Most modern NLP algorithms do not use embeddings as the representation of word meaning.

> 大多数现代 NLP 算法不使用嵌入（embeddings）作为词义的表示方式。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Completely false.** Modern NLP heavily relies on embeddings. The evolution: Word2Vec (2013) → GloVe (2014) → FastText (2016) → BERT/GPT (2018). Virtually ALL modern NLP algorithms use embeddings as the core word representation.
>
> > ⚠️ **完全错误。** 现代 NLP 高度依赖嵌入。演进：Word2Vec → GloVe → FastText → BERT/GPT。几乎所有现代 NLP 算法都使用嵌入作为核心词表示。
>
> **Key**: Modern NLP = ALL embeddings (Word2Vec, GloVe, BERT, GPT). Embeddings are THE standard.

---

## Q4.4 (1 point)

Which of the following word analogy equations should hold for an effective word embedding?

> 对于有效的词嵌入，以下哪个词类比等式应该成立？

A) $e_{boy} - e_{brother} \approx e_{sister} - e_{girl}$

B) $e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$

C) $e_{boy} - e_{girl} \approx e_{sister} - e_{brother}$

> **Answer**: B
> **Explanation**:
> boy - girl = "gender" relationship. brother - sister = same "gender" relationship. So $e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$. Similarly: $\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$.
>
> > boy - girl = "性别"关系。brother - sister = 同样的"性别"关系。类似：$\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$。
>
> **Key**: Word analogy preserves semantic relationships in vector space. king - man + woman ≈ queen.

---

## Q4.5 (1 point)

The goal of the Skip-Gram model is to determine the central word based on its surrounding context words.

> Skip-Gram 模型的目标是根据周围的上下文词来确定中心词。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Easy to confuse!** That description is for CBOW, not Skip-gram. Skip-gram: **center word → predict context words**. CBOW: **context words → predict center word**. Skip-gram is better for rare words and small corpora; CBOW is faster and better for frequent words.
>
> > ⚠️ **易混淆！** 题干描述的是 CBOW，不是 Skip-gram。Skip-gram：中心词 → 预测上下文词。CBOW：上下文词 → 预测中心词。
>
> **Key**: Skip-gram = center → context. CBOW = context → center. Don't confuse them!

---

## Q4.6 (1 point)

What is the default dimensionality of word embeddings in the Gensim Word2Vec method?

> Gensim Word2Vec 方法中词嵌入的默认维度是多少？

A) 4000

B) 120

C) 100

D) 10

> **Answer**: C
> **Explanation**:
> Gensim Word2Vec default: `vector_size=100`. Code example: `Word2Vec(text, min_count=1, vector_size=50, window=5, sg=1, negative=5)` where `sg=1` = Skip-gram, `sg=0` = CBOW.
>
> > Gensim Word2Vec 默认：`vector_size=100`。代码示例中 `sg=1` = Skip-gram，`sg=0` = CBOW。
>
> **Key**: Gensim Word2Vec default = 100 dimensions. sg=1 → Skip-gram, sg=0 → CBOW.

---

## Q4.7 (1 point)

GloVe combines global corpus-wide co-occurrence statistics with local context window information. It builds a global word-word co-occurrence matrix and factorizes it so that $w_i \cdot w_j \approx \log(\text{co-occurrence count})$.

> GloVe 结合了全局语料级共现统计和局部上下文窗口信息。它构建全局词-词共现矩阵并对其进行分解，使得 $w_i \cdot w_j \approx \log(\text{共现次数})$。

A) True
B) False

> **Answer**: A
> **Explanation**:
> GloVe (Global Vectors, Stanford, Pennington et al. 2014) = **Glo**bal (corpus-wide co-occurrence matrix) + **Ve**ctors (local context window). This dual perspective is its key advantage over Word2Vec (prediction-based, local only).
>
> > GloVe（全局词向量，Stanford，2014）= 全局（语料级共现矩阵）+ 向量（局部上下文窗口）。这种双重视角是它相比 Word2Vec 的关键优势。
>
> **Key**: GloVe = global co-occurrence + local window. Word2Vec = local prediction only. FastText = prediction + subword.

---

## Q4.8 (1 point)

Which word embedding method can handle Out-of-Vocabulary (OOV) words by composing word vectors from character n-grams (length 3–6)?

> 哪种词嵌入方法可以通过字符 n-gram（长度 3-6）组合来处理未登录词（OOV）？

A) Word2Vec (2013, Mikolov et al.)

B) GloVe (2014, Pennington et al., Stanford)

C) FastText (2016, Bojanowski et al., Facebook)

D) One-Hot Encoding

> **Answer**: C
> **Explanation**:
> FastText represents each word as the sum of its character n-gram vectors (length 3–6). Even for unseen words, it composes a vector from known subword parts. Word2Vec and GloVe **cannot** handle OOV.
>
> > FastText 将每个词表示为其字符 n-gram 向量的总和。即使未见过的词也能从已知子词组合出向量。Word2Vec 和 GloVe **不能**处理 OOV。
>
> **Key**: FastText = subword n-grams → handles OOV. Word2Vec/GloVe = no OOV handling.

---

## Q4.9 (1 point)

Static word embeddings (Word2Vec, GloVe) are context-insensitive — the word "bank" always has the same vector regardless of whether it means a financial institution or a river bank.

> 静态词嵌入（Word2Vec、GloVe）对上下文不敏感——"bank" 无论表示金融机构还是河岸，始终具有相同的向量。

A) True
B) False

> **Answer**: A
> **Explanation**:
> This is a key limitation of static embeddings. Each word has ONE fixed vector regardless of context. Contextual embeddings (ELMo, BERT, GPT) solve this by generating different vectors for the same word in different contexts.
>
> > 这是静态嵌入的关键局限。每个词只有一个固定向量，不随上下文变化。上下文嵌入（ELMo、BERT、GPT）通过为相同词在不同上下文中生成不同向量来解决。
>
> **Key**: Static (Word2Vec/GloVe) = one vector per word, context-insensitive. Contextual (BERT/GPT) = different vectors per context.

---

## Q4.10 (1 point)

Intrinsic evaluation of word embeddings assesses quality through downstream tasks like text classification and NER, while extrinsic evaluation uses word similarity and analogy tasks independently.

> 词嵌入的内在评估通过下游任务（如文本分类和 NER）评估质量，而外在评估使用词相似度和类比任务独立评估。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Swapped!** Intrinsic = assess quality **independently** (word similarity, analogy tasks). Extrinsic = assess via **downstream tasks** (text classification, NER). The statement has them reversed.
>
> > ⚠️ **搞反了！** 内在评估 = **独立**评估质量（词相似度、类比任务）。外在评估 = 通过**下游任务**评估（文本分类、NER）。题干将两者对调了。
>
> **Key**: Intrinsic = independent (similarity, analogy). Extrinsic = downstream tasks (classification, NER).

---

# W5: Language Models & RNN/LSTM — 语言模型与 RNN/LSTM (10 questions)

---

## Q5.1 (1 point)

The Chain Rule of probability — $P(w_1 w_2 \cdots w_n) = P(w_1) \times P(w_2|w_1) \times P(w_3|w_1 w_2) \times \cdots$ — is the mathematical foundation of only N-gram language models, not neural language models.

> 概率链式法则是仅 N-gram 语言模型的数学基础，不适用于神经语言模型。

A) True
B) False

> **Answer**: B
> **Explanation**:
> The Chain Rule is the mathematical foundation of **ALL** language models — from N-gram to FFNN to RNN to LSTM to GPT. Every language model ultimately computes $P(w_t | w_1 \cdots w_{t-1})$ based on the chain rule decomposition.
>
> > 链式法则是**所有**语言模型的数学基础——从 N-gram 到 FFNN 到 RNN 到 LSTM 到 GPT。每个语言模型最终都基于链式法则分解计算 $P(w_t | w_1 \cdots w_{t-1})$。
>
> **Key**: Chain Rule = foundation of ALL LMs (N-gram, FFNN, RNN, LSTM, Transformer, GPT).

---

## Q5.2 (1 point)

The core idea of an N-gram language model is to predict the next word by understanding the semantic meaning of entire sentences and applying deep reasoning.

> N-gram 语言模型的核心思想是通过理解整个句子的语义含义并应用深层推理来预测下一个词。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ N-gram models are **shallow, statistics-based** — they only count co-occurrence frequencies of the previous $n-1$ words (Markov Assumption). They have NO semantic understanding and NO deep reasoning capability.
>
> > ⚠️ N-gram 是**浅层统计方法**——只统计前 $n-1$ 个词的共现频率（马尔可夫假设）。没有语义理解能力，没有深层推理能力。
>
> **Key**: N-gram = statistical counting, Markov Assumption, fixed window, no semantic reasoning.

---

## Q5.3 (1 point)

Suppose we have: Count("feel") = 100, Count("feel happy") = 40, Count("happy") = 30. The conditional probability P("happy" | "feel") is:

> 假设：Count("feel") = 100，Count("feel happy") = 40，Count("happy") = 30。条件概率 P("happy" | "feel") 是：

A) 0.3

B) 0.4

C) 0.75

D) 0.2

> **Answer**: B
> **Explanation**:
> $P(\text{happy}|\text{feel}) = \frac{Count(\text{feel happy})}{Count(\text{feel})} = \frac{40}{100} = 0.4$. ⚠️ Count("happy") = 30 is a **DISTRACTOR** — conditional probability only uses Count(AB) / Count(A), NOT Count(B) alone.
>
> > $P(\text{happy}|\text{feel}) = \frac{40}{100} = 0.4$。⚠️ Count("happy") = 30 是**干扰信息**——条件概率只用 Count(AB)/Count(A)，不用 Count(B)。
>
> **Key**: $P(B|A) = \frac{Count(AB)}{Count(A)}$. Ignore Count(B) alone — it's a distractor!

---

## Q5.4 (1 point)

A fixed-window neural network language model (FFNN LM) can correctly distinguish between "The food was good, not bad at all" (positive) and "The food was bad, not good at all" (negative) because it considers the full sentence context.

> 固定窗口神经网络语言模型（FFNN LM）可以正确区分 "The food was good, not bad at all"（正面）和 "The food was bad, not good at all"（负面），因为它考虑了完整句子上下文。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ FFNN LM uses a **fixed window** of the last N words. If the window only covers "not good at all" vs "not bad at all", the model sees similar patterns and cannot distinguish them. The key limitation of FFNN is the fixed context window that discards earlier context.
>
> > ⚠️ FFNN LM 使用最后 N 个词的**固定窗口**。如果窗口只覆盖后几个词，模型看到相似模式无法区分。FFNN 的关键限制是固定上下文窗口丢弃了更早的上下文。
>
> **Key**: FFNN LM = fixed window, discards earlier context. Cannot distinguish sentences needing full context.

---

## Q5.5 (1 point)

RNNs maintain an internal hidden state $h_t$ that carries information across time steps, using the same weights ($W_h$, $W_e$) at EVERY time step (parameter sharing). This is a key advantage over FFNNs.

> RNN 维持内部隐藏状态 $h_t$ 跨时间步传递信息，在每个时间步使用相同的权重（$W_h$、$W_e$）（参数共享）。这是相比 FFNN 的关键优势。

A) True
B) False

> **Answer**: A
> **Explanation**:
> RNN core features: (1) Stateful computation via $h_t = \sigma(W_h \cdot h_{t-1} + W_e \cdot e_t + b)$, (2) Parameter sharing — same weights reused at every step, (3) Variable-length input support. FFNN has: fixed-length only, no state, different weights per layer.
>
> > RNN 核心特征：(1) 通过 $h_t$ 的有状态计算，(2) 参数共享——相同权重在每步复用，(3) 支持变长输入。FFNN：仅固定长度、无状态、每层不同权重。
>
> **Key**: RNN = stateful ($h_t$), parameter sharing, variable-length. FFNN = stateless, fixed-length.

---

## Q5.6 (1 point)

The vanishing gradient problem in RNNs occurs when gradients become extremely small during BPTT (Backpropagation Through Time), making it impossible to learn long-range dependencies. The exploding gradient problem occurs when gradients grow to infinity, causing unstable training.

> RNN 中的梯度消失问题发生在 BPTT 中梯度变得极小时，使学习长距离依赖变得不可能。梯度爆炸问题发生在梯度增长到无穷大时，导致训练不稳定。

A) True
B) False

> **Answer**: A
> **Explanation**:
> During BPTT, gradient ∝ $(W_h)^T$. If $|W_h| < 1$, gradient → 0 (vanishing). If $|W_h| > 1$, gradient → ∞ (exploding). Vanishing gradient is the main motivation for LSTM.
>
> > BPTT 中，梯度 ∝ $(W_h)^T$。若 $|W_h| < 1$，梯度 → 0（消失）。若 $|W_h| > 1$，梯度 → ∞（爆炸）。梯度消失是 LSTM 的主要动机。
>
> **Key**: Vanishing = gradient → 0, can't learn long-range. Exploding = gradient → ∞, unstable. LSTM solves vanishing.

---

## Q5.7 (1 point)

LSTM solves the vanishing gradient problem because it uses more hidden layers, which automatically prevent gradient decay.

> LSTM 解决梯度消失问题是因为使用了更多隐藏层，自动防止梯度衰减。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **More layers do NOT automatically prevent vanishing gradient.** LSTM solves it through its **gating mechanisms** (forget gate, input gate, output gate) and the cell state update using **ADDITION** ($c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$), which allows gradients to flow without multiplicative decay.
>
> > ⚠️ **更多层不能自动防止梯度消失。** LSTM 通过**门控机制**和细胞状态的**加法**更新解决：$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$，允许梯度不经乘法衰减直接流动。
>
> **Key**: LSTM = 3 gates + cell state ADDITION → gradient flows. NOT "more layers".

---

## Q5.8 (1 point)

LSTM has a dual state mechanism: $h_t$ (short-term hidden state) carries recent information, while $c_t$ (long-term cell state) carries information over long distances. The three gates are: Forget gate (discard old info), Input gate (store new info), Output gate (control output).

> LSTM 有双状态机制：$h_t$（短期隐藏状态）携带近期信息，$c_t$（长期细胞状态）携带长距离信息。三个门：遗忘门（丢弃旧信息）、输入门（存储新信息）、输出门（控制输出）。

A) True
B) False

> **Answer**: A
> **Explanation**:
> LSTM (Hochreiter & Schmidhuber, 1997): dual state ($h_t$ short-term + $c_t$ long-term), 3 gates controlling information flow. Forget gate: $f_t = \sigma(W_f[h_{t-1}, x_t] + b_f)$. Each gate outputs values between 0 (closed) and 1 (open).
>
> > LSTM（Hochreiter & Schmidhuber, 1997）：双状态（$h_t$ 短期 + $c_t$ 长期），3 门控制信息流。每个门输出值在 0（关闭）和 1（打开）之间。
>
> **Key**: LSTM = dual state (h_t + c_t) + 3 gates (forget, input, output). Cell state uses ADDITION.

---

## Q5.9 (1 point)

When the learning rate is set too low, the training process will become much faster, and the model will reach the optimal solution quickly because small weight updates allow for faster progress.

> 当学习率设置得过低时，训练过程会变得更快，模型会迅速达到最优解，因为较小的权重更新可以带来更快的进展。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Completely opposite.** Too low learning rate → **extremely SLOW** convergence, may get stuck in local optima. Too high → oscillation/divergence, may skip optimal solution. The parameter update is $\theta = \theta - \alpha \cdot \nabla L$; tiny $\alpha$ means tiny steps.
>
> > ⚠️ **完全相反。** 学习率过低 → **收敛极慢**，可能陷入局部最优。过高 → 振荡/发散。参数更新 $\theta = \theta - \alpha \cdot \nabla L$，$\alpha$ 极小意味着步长极小。
>
> **Key**: Low α → SLOW (not fast!). High α → oscillation/divergence. Need balanced learning rate.

---

## Q5.10 (1 point)

The evolution of language models follows this order: N-gram → FFNN → RNN → LSTM. Each stage solves a limitation of the previous one.

> 语言模型的演进顺序为：N-gram → FFNN → RNN → LSTM。每个阶段解决了上一阶段的局限。

A) True
B) False

> **Answer**: A
> **Explanation**:
> N-gram (statistical, fixed window) → FFNN (learns embeddings, still fixed window) → RNN (variable-length memory, parameter sharing, but vanishing gradient) → LSTM (solves vanishing gradient via gating). This continues: → Bi-LSTM → Seq2Seq → +Attention → Transformer.
>
> > N-gram（统计，固定窗口）→ FFNN（学习嵌入，仍固定窗口）→ RNN（变长记忆、参数共享，但梯度消失）→ LSTM（门控解决梯度消失）。继续：→ Bi-LSTM → Seq2Seq → +Attention → Transformer。
>
> **Key**: N-gram → FFNN → RNN → LSTM → Bi-LSTM → Seq2Seq → +Attention → Transformer.

---

# W6: Seq2Seq & Attention — 序列到序列与注意力机制 (10 questions)

---

## Q6.1 (1 point)

Bi-LSTM processes sequences in both directions (forward: left→right, backward: right→left), with output dimension = $2 \times n_{lstm}$. It can be used for both text understanding and text generation tasks.

> Bi-LSTM 从两个方向处理序列（正向：左→右，反向：右→左），输出维度 = $2 \times n_{lstm}$。它既可用于文本理解也可用于文本生成任务。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ The output dimension ($2 \times n_{lstm}$) and bidirectional processing are correct. But Bi-LSTM **CANNOT** be used for text generation — the backward pass requires future words that don't exist during generation. It's only good for understanding tasks (classification, NER, sentiment).
>
> > ⚠️ 输出维度和双向处理描述正确。但 Bi-LSTM **不能**用于文本生成——反向传播需要尚不存在的未来词。只适用于理解任务（分类、NER、情感分析）。
>
> **Key**: Bi-LSTM = 2×n_lstm output, CANNOT generate text. Forward/backward have separate weights.

---

## Q6.2 (1 point)

Which sequence architecture type matches each task?

> 哪种序列架构类型匹配以下任务？

Sentiment Analysis = ?; Machine Translation = ?; Image Captioning = ?

A) Many-to-one; Many-to-many (unsynced); One-to-many

B) One-to-many; Many-to-one; Many-to-many (synced)

C) Many-to-many (synced); One-to-many; Many-to-one

D) One-to-one; Many-to-many (unsynced); One-to-many

> **Answer**: A
> **Explanation**:
> Five sequence architectures: (1) One-to-one = image classification, (2) One-to-many = image captioning (image→words), (3) Many-to-one = sentiment analysis (words→label), (4) Many-to-many synced = POS tagging (same length), (5) Many-to-many unsynced = translation (different lengths, Seq2Seq).
>
> > 五种序列架构：一对一=图像分类，一对多=图像描述，多对一=情感分析，多对多同步=POS标注，多对多异步=翻译（Seq2Seq）。
>
> **Key**: Sentiment=many-to-one. Translation=many-to-many(unsynced). Captioning=one-to-many. POS=many-to-many(synced).

---

## Q6.3 (1 point)

In the basic Seq2Seq model, the encoder compresses the entire source sequence into a single fixed-length vector ("Encoder Vector"), and the decoder uses this as its initial state to generate the target sequence. This works well for long sentences because a single vector can capture all information.

> 在基础 Seq2Seq 模型中，编码器将整个源序列压缩为单个固定长度向量（"编码器向量"），解码器以此为初始状态生成目标序列。这对长句子效果很好，因为单个向量可以捕获所有信息。

A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ The Seq2Seq architecture description is correct, but the claim about long sentences is **wrong**. Compressing an entire source sequence into a **single fixed-length vector** is the **bottleneck problem** — long sentences lose information. This is precisely why the Attention mechanism was developed.
>
> > ⚠️ Seq2Seq 架构描述正确，但关于长句子的说法**错误**。将整个源序列压缩为**单个固定长度向量**是**信息瓶颈问题**——长句子丢失信息。这正是注意力机制被开发的原因。
>
> **Key**: Seq2Seq bottleneck = single vector → information loss for long sentences → motivates Attention.

---

## Q6.4 (1 point)

During training, Seq2Seq uses Teacher Forcing (decoder receives ground truth previous word). During testing, the decoder uses its own previous prediction (autoregressive). This training/testing mismatch is called:

> 训练时 Seq2Seq 使用教师强制（解码器接收真实标签），测试时使用自身预测（自回归）。这种训练/测试不匹配称为：

A) Vanishing Gradient

B) Information Bottleneck

C) Exposure Bias

D) Overfitting

> **Answer**: C
> **Explanation**:
> Exposure Bias occurs because the model is trained on perfect (ground truth) inputs but tested with its own imperfect predictions. This mismatch can cause error accumulation during testing — each mistake feeds into the next prediction.
>
> > 曝光偏差发生在模型训练时使用完美输入（真实标签）但测试时使用自身不完美预测。这种不匹配会在测试时导致误差累积。
>
> **Key**: Exposure Bias = Teacher Forcing (training) vs Autoregressive (testing) mismatch → error accumulation.

---

## Q6.5 (1 point)

The Attention mechanism has 4 steps in order: (1) Compute attention scores (dot product), (2) Apply softmax to get weights, (3) Compute context vector (weighted sum of encoder states), (4) Concatenate with decoder state for output.

> 注意力机制有 4 个步骤：(1) 计算注意力分数（点积），(2) 通过 softmax 获得权重，(3) 计算上下文向量（编码器状态的加权和），(4) 与解码器状态拼接输出。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Score → Softmax → Context vector → Output. Benefits: eliminates bottleneck, handles long sentences, provides interpretability (alignment visualization), and creates gradient shortcut paths. Limitation: still sequential (RNN-based), cannot fully parallelize.
>
> > 分数 → Softmax → 上下文向量 → 输出。优点：消除瓶颈、处理长句、可解释性、梯度捷径。局限：仍然顺序处理（基于 RNN），无法完全并行。
>
> **Key**: Attention 4 steps: Score → Softmax → Context vector → Output. Still sequential = limitation.

---

## Q6.6 (1 point)

The Transformer architecture (2017, "Attention Is All You Need") uses Self-Attention where each word attends to ALL other words simultaneously, enabling fully parallel processing. It uses Positional Encoding to replace RNN's implicit sequential ordering.

> Transformer 架构（2017，"Attention Is All You Need"）使用自注意力机制，每个词同时关注所有其他词，实现完全并行处理。它使用位置编码替代 RNN 的隐式顺序排列。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Transformer key features: Self-Attention (fully parallel, $O(1)$ path length between any two positions), Positional Encoding (explicit position info), encoder+decoder stacks, multi-head attention. Memory complexity: $O(n^2)$. This was the 2017 turning point for NLP.
>
> > Transformer 关键特征：自注意力（完全并行，任意两位置 $O(1)$ 路径长度），位置编码，编码器+解码器堆栈，多头注意力。内存复杂度 $O(n^2)$。这是 2017 年 NLP 的转折点。
>
> **Key**: Transformer = Self-Attention (parallel) + Positional Encoding. O(1) path, O(n²) memory.

---

## Q6.7 (1 point)

In RNN-based Attention, the decoder attends to encoder states (decoder → encoder). In the Transformer's Self-Attention, every word attends to all other words in the same sequence (every word → all words), and it does NOT depend on RNN.

> 在基于 RNN 的注意力中，解码器关注编码器状态（解码器→编码器）。在 Transformer 的自注意力中，每个词关注同一序列中的所有其他词（每个词→所有词），且不依赖 RNN。

A) True
B) False

> **Answer**: A
> **Explanation**:
> RNN Attention: decoder → encoder, still sequential, depends on RNN. Self-Attention: every word → all words, fully parallel, no RNN dependency, $O(1)$ direct connections, but $O(n^2)$ memory.
>
> > RNN 注意力：解码器→编码器，仍顺序处理，依赖 RNN。自注意力：每个词→所有词，完全并行，不依赖 RNN，$O(1)$ 直接连接，但 $O(n^2)$ 内存。
>
> **Key**: RNN Attention = decoder→encoder, sequential. Self-Attention = every→all, parallel, no RNN.

---

## Q6.8 (1 point)

BERT uses the encoder part of the Transformer and is designed for understanding tasks (classification, NER, QA). GPT uses the decoder part and is designed for generation tasks (text completion, dialogue).

> BERT 使用 Transformer 的编码器部分，用于理解任务（分类、NER、QA）。GPT 使用解码器部分，用于生成任务（文本补全、对话）。

A) True
B) False

> **Answer**: A
> **Explanation**:
> BERT (2018) = Encoder-only, bidirectional, understanding tasks. GPT (2018) = Decoder-only, autoregressive (left-to-right), generation tasks. Both build on the Transformer architecture.
>
> > BERT（2018）= 仅编码器，双向，理解任务。GPT（2018）= 仅解码器，自回归（从左到右），生成任务。都基于 Transformer 架构。
>
> **Key**: BERT = Encoder, bidirectional, understanding. GPT = Decoder, autoregressive, generation.

---

## Q6.9 (1 point)

The full architecture evolution chain in NLP is: N-gram → FFNN → RNN → LSTM → Bi-LSTM → Seq2Seq → Seq2Seq + Attention → Transformer. Each step solves a specific limitation of its predecessor.

> NLP 中完整的架构演进链为：N-gram → FFNN → RNN → LSTM → Bi-LSTM → Seq2Seq → Seq2Seq + Attention → Transformer。每一步解决了前一步的特定局限。

A) True
B) False

> **Answer**: A
> **Explanation**:
> Evolution with problems solved: N-gram (statistical) → FFNN (learns embeddings, fixed window) → RNN (variable-length, vanishing gradient) → LSTM (gating solves gradient) → Bi-LSTM (both directions, can't generate) → Seq2Seq (diff I/O lengths, bottleneck) → +Attention (dynamic weighting, still sequential) → Transformer (fully parallel, $O(n^2)$ memory).
>
> > 演进及解决的问题：N-gram → FFNN（学嵌入但固定窗口）→ RNN（变长但梯度消失）→ LSTM（门控解决梯度）→ Bi-LSTM（双向但不能生成）→ Seq2Seq（不同长度但瓶颈）→ +Attention（动态加权但仍顺序）→ Transformer（完全并行但 $O(n^2)$ 内存）。
>
> **Key**: Each architecture solves the previous one's limitation. Know the evolution chain and trade-offs.

---

## Q6.10 (1 point)

Which of the following milestones is correctly matched with its year?

> 以下哪个里程碑的年份匹配正确？

A) LSTM — 2003, Word2Vec — 2016, Transformer — 2017

B) LSTM — 1997, Word2Vec — 2013, GloVe — 2014, FastText — 2016, Transformer — 2017

C) LSTM — 1997, Word2Vec — 2014, Transformer — 2013

D) Turing Test — 1997, LSTM — 2013, BERT — 2017

> **Answer**: B
> **Explanation**:
> Key milestones: Turing Test (1950), LSTM (1997, Hochreiter & Schmidhuber), Neural LM (2003, Bengio), Word2Vec (2013, Mikolov), GloVe (2014, Pennington, Stanford), FastText (2016, Bojanowski, Facebook), Transformer (2017, "Attention Is All You Need"), BERT/GPT (2018).
>
> > 关键里程碑：图灵测试(1950)、LSTM(1997)、神经LM(2003)、Word2Vec(2013)、GloVe(2014, Stanford)、FastText(2016, Facebook)、Transformer(2017)、BERT/GPT(2018)。
>
> **Key**: 1950 Turing, 1997 LSTM, 2013 Word2Vec, 2014 GloVe, 2016 FastText, 2017 Transformer, 2018 BERT/GPT.

---

## Summary of Answers / 答案汇总

| Week   | Question | Answer | Topic / 主题                                           |
| :----- | :------- | :----- | :----------------------------------------------------- |
| **W1** | Q1.1     | A      | NLP = Linguistics × CS × AI                            |
|        | Q1.2     | A      | AI ⊃ ML ⊃ DL; NLP = application domain                |
|        | Q1.3     | B      | AI not just fixed rules; ML is subset of AI            |
|        | Q1.4     | A      | Document vs Knowledge; >80% unstructured               |
|        | Q1.5     | A      | Turing Test (1950)                                     |
|        | Q1.6     | B      | Sentiment Analysis = NLU (not NLG)                     |
|        | Q1.7     | C      | Ambiguity types (lexical: "bank")                      |
|        | Q1.8     | B      | Summarization MUST preserve coherence (trap)           |
|        | Q1.9     | D      | 3 NLP approaches: Heuristics, ML, DL                   |
|        | Q1.10    | B      | NLP lifecycle: preprocessing BEFORE feature extraction |
| **W2** | Q2.1     | A      | Preprocessing pipeline order                           |
|        | Q2.2     | B      | Stop words = high-freq, low-semantic                   |
|        | Q2.3     | A      | Stemming vs Lemmatization comparison                   |
|        | Q2.4     | B      | Stemming action: helped→help (suffix removal)          |
|        | Q2.5     | B      | Poetry: do NOT stem/lemmatize                          |
|        | Q2.6     | B      | SpaCy = NO stemming; NLTK = both                       |
|        | Q2.7     | C      | Lancaster > Snowball > Porter (aggressiveness)         |
|        | Q2.8     | B      | POS tags vs NER entity types                           |
|        | Q2.9     | B      | Regex: `\w+[-]\w+` = compound words (trap)             |
|        | Q2.10    | B      | Regex: `[a-zA-Z]\w*d+` multi-match (trap)             |
|        | Q2.11    | A      | re.match (start) vs re.search (anywhere)               |
|        | Q2.12    | B      | Python s[0] and s[-1] string indexing                  |
| **W3** | Q3.1     | B      | BOW ignores word order (trap)                          |
|        | Q3.2     | A      | N-gram: partial word order, $V^N$ explosion            |
|        | Q3.3     | C      | TF-IDF: no context, no semantics                       |
|        | Q3.4     | B      | TF value sorting trap (d1 vs d9 swap)                  |
|        | Q3.5     | C      | IDF = 0 when word in all docs                          |
|        | Q3.6     | A      | CountVectorizer vs TfidfVectorizer                     |
|        | Q3.7     | B      | CountVectorizer ngram_range (8+ features, not 7)       |
|        | Q3.8     | A      | Cosine (length-independent) vs Euclidean               |
|        | Q3.9     | C      | Cosine similarity calculation ≈ 0.8421                 |
|        | Q3.10    | C      | Edit distance: intention→execution = 5                 |
| **W4** | Q4.1     | A      | WordNet: IS-A vs PART-OF relations                     |
|        | Q4.2     | B      | Embedding dim = 50-300, NOT vocab size                 |
|        | Q4.3     | B      | Modern NLP ALL uses embeddings                         |
|        | Q4.4     | B      | Word analogy: boy-girl ≈ brother-sister                |
|        | Q4.5     | B      | Skip-gram = center→context (NOT context→center)        |
|        | Q4.6     | C      | Gensim Word2Vec default = 100 dim                      |
|        | Q4.7     | A      | GloVe = global co-occurrence + local window            |
|        | Q4.8     | C      | FastText = subword n-grams, handles OOV                |
|        | Q4.9     | A      | Static embeddings: context-insensitive                 |
|        | Q4.10    | B      | Intrinsic=independent; Extrinsic=downstream (swapped)  |
| **W5** | Q5.1     | B      | Chain Rule = foundation of ALL LMs                     |
|        | Q5.2     | B      | N-gram = statistical, no semantic reasoning            |
|        | Q5.3     | B      | P(happy|feel)=0.4; Count(happy) is distractor          |
|        | Q5.4     | B      | FFNN fixed window limitation                           |
|        | Q5.5     | A      | RNN: stateful, parameter sharing, variable-length      |
|        | Q5.6     | A      | Vanishing (→0) vs Exploding (→∞) gradient              |
|        | Q5.7     | B      | LSTM: gates + ADDITION (not "more layers")             |
|        | Q5.8     | A      | LSTM dual state + 3 gates                              |
|        | Q5.9     | B      | Low learning rate = SLOW (not fast!)                   |
|        | Q5.10    | A      | LM evolution: N-gram→FFNN→RNN→LSTM                     |
| **W6** | Q6.1     | B      | Bi-LSTM CANNOT generate text                           |
|        | Q6.2     | A      | 5 sequence architectures mapping                       |
|        | Q6.3     | B      | Seq2Seq bottleneck (single vector = info loss)         |
|        | Q6.4     | C      | Exposure Bias (Teacher Forcing vs Autoregressive)      |
|        | Q6.5     | A      | Attention 4 steps: Score→Softmax→Context→Output        |
|        | Q6.6     | A      | Transformer: Self-Attention + Positional Encoding      |
|        | Q6.7     | A      | RNN Attention vs Self-Attention comparison             |
|        | Q6.8     | A      | BERT (Encoder) vs GPT (Decoder)                        |
|        | Q6.9     | A      | Full evolution chain + trade-offs                      |
|        | Q6.10    | B      | Milestones with years                                  |
