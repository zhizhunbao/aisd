# CST8507 NLP (Natural Language Processing, 自然语言处理) Midterm Cheat Sheet (W1–6)

> Merged from lecture slides (W1–W6) + Quiz 1–5 + Labs 1–3. ⚠️ = common trap questions.

---

## W1: NLP (Natural Language Processing, 自然语言处理) Overview

### Core Definitions (核心定义)

- **NLP (Natural Language Processing, 自然语言处理)** = subfield of Linguistics (语言学) × CS (Computer Science, 计算机科学) × AI (Artificial Intelligence, 人工智能); enables computers to process, understand, and generate human language
- **NLU (Natural Language Understanding, 自然语言理解)** = classification, NER (Named Entity Recognition, 命名实体识别), sentiment analysis (情感分析)
- **NLG (Natural Language Generation, 自然语言生成)** = translation (翻译), summarization (摘要), ChatGPT
- **NLP (Natural Language Processing, 自然语言处理)** = NLU (Natural Language Understanding, 自然语言理解) + NLG (Natural Language Generation, 自然语言生成)

### AI (Artificial Intelligence, 人工智能) Hierarchy (层级关系)

- **AI (Artificial Intelligence, 人工智能)** ⊃ **ML (Machine Learning, 机器学习)** ⊃ **DL (Deep Learning, 深度学习)**
- NLP (Natural Language Processing, 自然语言处理) is an **application domain** of AI (Artificial Intelligence, 人工智能), spans all levels (not a technique level)

> ⚠️ "AI (Artificial Intelligence, 人工智能) relies only on fixed rules" → **False** (modern AI (Artificial Intelligence, 人工智能) includes learning-based approaches)
> ⚠️ "ML (Machine Learning, 机器学习) is unrelated to AI (Artificial Intelligence, 人工智能)" → **False** (ML (Machine Learning, 机器学习) is a core subset of AI (Artificial Intelligence, 人工智能))

### Knowledge Representation (知识表示)

- **Document** (文档) = raw/semi-structured text (articles, reports)
- **Knowledge** (知识) = structured, interpreted information (entities, relations, facts) extracted from documents
- **Structured knowledge** (结构化知识): tables/databases, precise | **Unstructured** (非结构化): free text, ambiguous, >80% enterprise data

### Turing Test (图灵测试, 1950)

- Human evaluator (人类评估者) interacts via text with one human + one machine
- If evaluator cannot reliably distinguish → machine passes
- Core criterion: ability to understand and generate language ≈ intelligence (智能)

### 7 NLP (Natural Language Processing, 自然语言处理) Applications

| Application | Type | Description |
|---|---|---|
| Speech Recognition (语音识别) | NLU (Natural Language Understanding, 自然语言理解) | Convert speech to text |
| Dialogue/Chatbot (对话/聊天机器人) | NLU (Natural Language Understanding, 自然语言理解) + NLG (Natural Language Generation, 自然语言生成) | Conversation agents |
| Text Classification (文本分类) | NLU (Natural Language Understanding, 自然语言理解) | Spam detection, categorization |
| Sentiment Analysis (情感分析) | NLU (Natural Language Understanding, 自然语言理解) | Determine opinion/emotion |
| Summarization (文本摘要) | NLG (Natural Language Generation, 自然语言生成) | Extract key information |
| QA (Question Answering, 问答系统) | NLU (Natural Language Understanding, 自然语言理解) + NLG (Natural Language Generation, 自然语言生成) | Answer questions from text |
| Generative AI (生成式AI) | NLG (Natural Language Generation, 自然语言生成) | ChatGPT, content creation |

> ⚠️ Text Classification (文本分类) = **NLU (Natural Language Understanding, 自然语言理解)** (NOT NLG (Natural Language Generation, 自然语言生成))
> ⚠️ Sentiment Analysis (情感分析) requires deep contextual understanding (sarcasm/irony/metaphor), not simple keyword matching
> ⚠️ Summarization (文本摘要) **MUST** preserve original meaning and coherence (连贯性)
> ⚠️ NLP (Natural Language Processing, 自然语言处理) goal = understand + interpret + generate human language meaningfully

### 4 Challenges (四大挑战)

| Challenge | Definition | Examples |
|---|---|---|
| **Ambiguity** (歧义性) | Multiple interpretations | Lexical (词汇歧义): "bank" (river/financial); Syntactic (句法歧义): attachment "saw man with telescope"; Referential (指代歧义): pronoun "she" |
| **Sparsity** (稀疏性) | Zipf's Law (齐夫定律): word freq ∝ 1/rank | Few words very frequent, >1/3 words appear only once, long-tail distribution (长尾分布) |
| **Variation** (变异性) | Same meaning expressed many ways | Lexical (词汇), Syntactic (句法), Regional (地域), Social (社会), Stylistic (风格), Generational (代际) |
| **Common Knowledge** (常识知识) | Machines lack world knowledge | "man bit dog" = news; "dog bit man" = normal |

### 3 Approaches (三种方法)

| Approach | Method | Example |
|---|---|---|
| **Heuristics** (启发式) | Rules / Regex (正则表达式) | Rule-based systems |
| **ML (Machine Learning, 机器学习)** | Learn from labeled data | Supervised (监督学习) / Unsupervised (无监督学习) |
| **DL (Deep Learning, 深度学习)** | Learn representations + rules | RNN (Recurrent Neural Network, 循环神经网络), LSTM (Long Short-Term Memory, 长短期记忆网络), Transformer |

### NLP (Natural Language Processing, 自然语言处理) Development Life Cycle (开发生命周期)

Requirements gathering (需求收集) → Data collection (数据收集) → Text preprocessing (文本预处理) → Feature extraction (特征提取) → Model building (模型构建) → Evaluation (评估) → Deployment (部署) → Gather more data / Improve model (迭代循环)

### NLP (Natural Language Processing, 自然语言处理) Libraries in Python

- **NLTK (Natural Language Toolkit, 自然语言工具包)**: comprehensive, has both Stemming (词干提取) and Lemmatization (词元化)
- **SpaCy**: industrial-strength, has Lemmatization (词元化) only, NO built-in Stemming (词干提取)
- Tools: Jupyter Notebook, Google Colab


---

## W2: Text Preprocessing (文本预处理)

### Preprocessing Pipeline (预处理流水线)

Documents → Tokenization (分词) → Noise Entities Removal (噪声移除) → Normalization (规范化)

Pipeline may vary depending on task and data.

### Tokenization (分词)

- Split continuous text into discrete tokens (words/subwords/characters)
- **FIRST step** in NLP (Natural Language Processing, 自然语言处理) pipeline
- Corpus (语料库) = collection of text documents | Words = units separated by spaces/punctuation

### Noise Entities Removal (噪声实体移除)

- **Lowercasing** (小写化): `text.lower()`
- **Removing Numbers** (移除数字): `re.sub('\w*\d\w*', ' ', text)`
- **Removing Punctuation** (移除标点)
- **Removing Stop Words** (移除停用词): high-freq low-semantic words (the, is, at...)
- **Other noise**: HTML tags, URLs, email addresses, special characters, extra whitespace
- **Compound Term Extraction** (复合词提取): extracting and tagging compound words/phrases

### Normalization (规范化)

Converting a token into its base form; removing inflection (屈折变化).

#### Stemming (词干提取)

- Rule-based suffix stripping (基于规则的后缀剥离), fast but crude
- May produce non-dictionary words: studying → studi, studies → studi
- **NLTK (Natural Language Toolkit, 自然语言工具包) Stemmers**:
  - **Porter Stemmer**: most common, least aggressive
  - **Snowball Stemmer**: improved Porter, supports multiple languages
  - **Lancaster Stemmer**: most aggressive, may over-stem
- Applications: text classification (文本分类), text clustering (文本聚类), information retrieval (信息检索)

#### Lemmatization (词元化)

- Dictionary lookup + POS (Part of Speech, 词性) analysis → always outputs valid dictionary words
- Output = **lemma** (词元, root word)
- Examples: Am/Are/Is → **Be** | Running/Ran/Run → **Run** | better → good
- Tools: WordNet Lemmatizer (NLTK), SpaCy Lemmatizer, TextBlob, Gensim Lemmatizer, TreeTagger, Stanford CoreNLP

#### Stemming (词干提取) vs Lemmatization (词元化)

| Dimension | Stemming (词干提取) | Lemmatization (词元化) |
|---|---|---|
| Method | Rule-based suffix stripping | Dictionary lookup + POS (Part of Speech, 词性) |
| Speed | ⚡ Faster | 🐢 Slower |
| Accuracy | Lower (may produce "studi") | ✅ Higher (valid dictionary words) |
| When to use | Speed priority | **Accuracy priority** |
| Example | helped→help, helps→help | was/am/is→be, better→good |

> ⚠️ "helped/helps→help" = **Stemming (词干提取)** (simple suffix removal -ed, -s)
> ⚠️ "was/am/is→be" = **Lemmatization (词元化)** (requires dictionary knowledge for irregular forms)
> ⚠️ **Poetry Analysis** (诗歌分析): do NOT stem/lemmatize (rhyme/rhythm are crucial)
> ⚠️ SpaCy has NO built-in Stemming (词干提取); NLTK (Natural Language Toolkit, 自然语言工具包) has both

#### SpaCy vs NLTK (Natural Language Toolkit, 自然语言工具包)

| Library | Stemming (词干提取) | Lemmatization (词元化) |
|---|---|---|
| **SpaCy** | ❌ No built-in | ✅ Yes |
| **NLTK (Natural Language Toolkit, 自然语言工具包)** | ✅ PorterStemmer / SnowballStemmer | ✅ WordNetLemmatizer |

### POS (Part of Speech, 词性) Tagging (词性标注)

- Label grammatical roles: NN (noun, 名词), VB (verb, 动词), JJ (adjective, 形容词), RB (adverb, 副词), DT (determiner, 限定词), PRP (pronoun, 代词)
- Why needed: syntactic/semantic analysis (句法/语义分析), improve accuracy of other NLP (Natural Language Processing, 自然语言处理) tasks
- Print tagset: `nltk.help.upenn_tagset()`

### NER (Named Entity Recognition, 命名实体识别)

- Identify and tag: PERSON (人名), LOCATION/GPE (地名), ORGANIZATION (组织), DATE (日期), MONEY (金额)
- Why needed: information extraction (信息提取), searching/indexing (搜索/索引), sentiment analysis (情感分析)
- Code: `from nltk.chunk import ne_chunk`

### Regular Expressions (正则表达式, Regex)

#### Metacharacters (元字符)

| Symbol | Meaning |
|---|---|
| `.` | Any single character |
| `[]` | Character set |
| `[^]` | Negation (negate set) |
| `^` | Beginning of string / line start |
| `$` | End of string / line end |
| `*` | 0 or more times |
| `+` | 1 or more times |
| `?` | 0 or 1 time (optional) |
| `{m,n}` | Between m and n times |
| `\` | Escape character |
| `\|` | OR |
| `()` | Capture group |

#### Character Classes (字符类)

| Class | Meaning | Equivalent |
|---|---|---|
| `\d` | Digit | `[0-9]` |
| `\w` | Word character | `[A-Za-z0-9_]` |
| `\s` | Whitespace | space/tab/newline |
| `\D` | NOT digit | `[^0-9]` |
| `\W` | NOT word char | `[^A-Za-z0-9_]` |
| `\S` | NOT whitespace | |

#### Python `re` Functions

| Function | Description |
|---|---|
| `re.match(r, s)` | Match at **start** of string only |
| `re.search(r, s)` | Match **first** occurrence anywhere |
| `re.findall(pattern, string)` | Return **all** non-overlapping matches as list |
| `re.sub(pattern, repl, string)` | **Replace** occurrences |
| `re.compile(pattern)` | Compile pattern object for reuse |
| `re.split(pattern, string)` | Split string by pattern |
| `.groups()` | Return tuple of all group substrings |
| `.span()` | Return (start, end) position tuple |

#### Regex Examples

| Pattern | Matches |
|---|---|
| `[wW]oodchuck` | Woodchuck, woodchuck |
| `colou?r` | color, colour |
| `beg.n` | begin, begun, beg3n |
| `[^A-Z]` | Not uppercase letter |
| `^[A-Z]` | Line starts with uppercase |

> ⚠️ `\b\w+[-]\w+\b` → matches **hyphenated compound words** (high-tech), NOT words ending with hyphen (`\w+` required on BOTH sides of `-`)
> ⚠️ `[a-zA-Z]\w*d+` → matches substrings starting with a letter, ending with one or more 'd' — output includes multiple matches, not just 'and'

#### Regex Use Cases (用例)

Text cleaning (文本清洗), Tokenization (分词), Information Retrieval (信息检索), Sentiment Analysis (情感分析), Language Detection (语言检测)

### Python String Indexing (字符串索引)

- `s[0]` = first char | `s[1]` = second char | `s[-1]` = last char
- Vowel start+end check: `s[0].lower() in 'aeiou' and s[-1].lower() in 'aeiou'`


---

## W3: Text Vectorization (文本向量化) & Similarity (相似度)

### Vector Space Model (向量空间模型)

- Text → points in high-dimensional vector space; similar words end up "nearby"
- **Vectorizing** (向量化): encoding text as integers to create feature vectors (特征向量)
- **Feature Vector** (特征向量): n-dimensional numerical representation of a text object
- Vector length (L₂ Norm, L₂范数): $\|x\| = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}$
- Dot Product (点积): $x_1 \cdot x_2 = x_{11}x_{21} + x_{12}x_{22} + \cdots + x_{1n}x_{2n}$

### Text Representation Methods (文本表示方法)

#### OHE (One-Hot Encoding, 独热编码)

- Each unique word → one binary vector, only one element = 1, rest = 0
- Example: "This is an example" → This=[1,0,0,0], is=[0,1,0,0], an=[0,0,1,0], example=[0,0,0,1]
- ❌ Extremely sparse | ❌ No frequency info | ❌ No semantics | ❌ All words equidistant

#### BOW (Bag of Words, 词袋模型)

- Document = unordered collection of tokens, count word frequency
- ✅ Simple, efficient, language-agnostic | ❌ **Loses word order** | ❌ Sparse | ❌ No semantics | ❌ OOV (Out-of-Vocabulary, 未登录词)
- "John is quicker than Mary" and "Mary is quicker than John" → **same BOW (Bag of Words, 词袋模型) vector** (opposite meaning lost)

> ⚠️ BOW (Bag of Words, 词袋模型) **IGNORES word order**; "word order is crucial / words depend on context" → **False**

#### N-Gram (N元组)

- Consecutive N words as features; partially restores word order
- Unigram (单元组) = single words | Bigram (二元组) = 2-word sequences | Trigram (三元组) = 3-word sequences
- Example: "I am learning NLP" → Bigrams: "am learning", "learning NLP"
- ✅ Captures some context/word-order | ❌ Feature count $V^N$ explodes | ❌ Sparse | ❌ OOV (Out-of-Vocabulary, 未登录词)

#### TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率)

- $TF(t, d) = \frac{\text{count}(t \text{ in } d)}{\text{total words in } d}$
- $IDF(t) = \log\frac{N}{df(t)}$ where $N$ = total docs, $df$ = docs containing $t$
- $TF\text{-}IDF(t, d) = TF(t, d) \times IDF(t)$
- Word in every document: $IDF = \log(1) = 0$ → zero weight
- Word in only 1 document: $IDF = \log(N)$ → highest weight
- Why log: without log, IDF for very rare words could be millions; log compresses scale
- ❌ High-dimensional sparse | ❌ No semantics/context/word order | ❌ Not suitable for DL (Deep Learning, 深度学习) | ❌ Poor for small corpora | ❌ OOV (Out-of-Vocabulary, 未登录词) | ✅ Good for search engines

> ⚠️ TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率) disadvantage = "does NOT consider context and semantic relationships"
> ⚠️ TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率) = high-dimensional sparse; DL (Deep Learning, 深度学习) prefers low-dimensional dense embeddings

#### Comparison: Traditional Text Representations (传统文本表示方法对比)

| Dimension | OHE (One-Hot Encoding, 独热编码) | BOW (Bag of Words, 词袋模型) | N-Gram (N元组) | TF-IDF (词频-逆文档频率) |
|---|---|---|---|---|
| Frequency info | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes (weighted) |
| Word order | ❌ No | ❌ No | ✅ Partial | ❌ No |
| Semantics | ❌ No | ❌ No | ❌ No | ❌ No |
| Sparsity | Very high | High | Very high ($V^N$) | High |
| Rare word handling | ❌ | ❌ | ❌ | ✅ Upweights rare words |

### CountVectorizer (计数向量化器)

- `CountVectorizer(ngram_range=(1,2))` → generates BOTH unigram AND bigram features
- Vector dimension = total number of all n-grams in vocabulary

> ⚠️ Corpus ["I love NLP","He love NLP","good man"] with (1,2)-gram produces **8+ features** (unigrams + bigrams), NOT 7

### TF (Term Frequency, 词频) Value Sorting Example

| Doc | Calculation | TF Value |
|---|---|---|
| d1 | 25/127 | ≈ 0.197 |
| d2 | 3/250 | = 0.012 |
| d3 | 20/650 | ≈ 0.031 |
| d9 | 15/125 | = 0.120 |
| d1000 | 20/800 | = 0.025 |

Correct ascending: d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197)

> ⚠️ Proposed order [d2, d1000, d3, **d1, d9**] is **False** — d1 and d9 are swapped. Correct: [d2, d1000, d3, **d9, d1**]

### CountVectorizer vs TfidfVectorizer (对比)

- CountVectorizer: raw word counts → common words ("the", "is") get high counts
- TfidfVectorizer: TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率) weighted → common words downweighted, rare words ("milk") upweighted
- Example: "hot" appears in many docs → high count but low TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率); "milk" is rare → better differentiator with TF-IDF (Term Frequency-Inverse Document Frequency, 词频-逆文档频率)

### Text Similarity Measures (文本相似度度量)

#### Cosine Similarity (余弦相似度)

- $\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \times \|\vec{B}\|} = \frac{\sum a_i b_i}{\sqrt{\sum a_i^2} \times \sqrt{\sum b_i^2}}$
- Range: $[-1, 1]$; ≈1 = same direction (similar), ≈0 = orthogonal (unrelated), ≈-1 = opposite
- **Length-independent** (不受文档长度影响)

> **Worked Example**: $w_1=(0.2,0.2,0.3,0.7)$, $w_2=(0.3,0.4,0.8,0.5)$
> Dot product = $0.06+0.08+0.24+0.35 = 0.73$
> $\|w_1\| = \sqrt{0.66} \approx 0.8124$, $\|w_2\| = \sqrt{1.14} \approx 1.0677$
> $\cos(\theta) = \frac{0.73}{0.8124 \times 1.0677} \approx \mathbf{0.8421}$

#### Euclidean Distance (欧几里得距离)

- $d(A,B) = \sqrt{\sum(a_i - b_i)^2}$
- Straight-line distance between two vector endpoints
- ❌ Affected by document length (受文档长度影响)

#### Levenshtein (Edit) Distance (编辑距离)

- Minimum operations (insert/delete/substitute) to transform one string into another
- Solved by Dynamic Programming (动态规划)
- Example: "kitten" → "sitting" = 3 operations (2 substitutions + 1 insertion)
- Example: "intention" → "execution" = **5 steps**

#### Similarity Measures Comparison (相似度度量对比)

| Measure | What it measures | Range | Length-independent? |
|---|---|---|---|
| Cosine Similarity (余弦相似度) | Angle between vectors | $[-1, 1]$ | ✅ Yes |
| Euclidean Distance (欧几里得距离) | Straight-line distance | $[0, \infty)$ | ❌ No |
| Levenshtein Distance (编辑距离) | Min edit operations | $[0, \infty)$ | N/A (string-level) |


---

## W4: Word Embeddings (词嵌入)

### WordNet (词汇数据库)

- Large lexical database; words organized into **synsets** (synonym sets, 同义词集) connected by semantic relations
- Source: Princeton University — https://wordnet.princeton.edu/

| Relation | Definition | Example |
|---|---|---|
| **Synset** (同义词集) | Set of synonyms sharing a common meaning | {car, auto, automobile} |
| **Hypernym** (上位词) | More general category (IS-A) | animal is hypernym of dog |
| **Hyponym** (下位词) | More specific instance (IS-A) | dog is hyponym of animal |
| **Meronym** (部分词) | Part of something (PART-OF) | wheel is meronym of car |
| **Holonym** (整体词) | Whole that contains the part (HAS-PART) | car is holonym of wheel |
| **Antonym** (反义词) | Opposite meaning | hot ↔ cold |
| **Troponym** (方式动词) | Specific manner of a verb | run is troponym of move |
| **Entailment** (蕴含) | One verb implies another | snore entails sleep |

> ⚠️ Hypernym (上位词)/Hyponym (下位词) = **IS-A** | Meronym (部分词)/Holonym (整体词) = **PART-OF** — don't confuse!

**WordNet (词汇数据库) Applications**: Semantic Text Representation (语义文本表示), Query Expansion (查询扩展)

**WordNet (词汇数据库) Limitations**: Limited coverage & static (覆盖有限且静态), Not computational (不可计算, no vectors), Domain-specific (领域特定), Language limitation (语言限制), Manual curation challenges (人工维护挑战) → motivates Word Embeddings (词嵌入)

### Word Embeddings (词嵌入) Fundamentals

- **Distributional Hypothesis** (分布假说): words appearing in similar contexts have similar meanings
- **Distributional Similarity** (分布相似性): meaning of a word can be understood from its context
- **Word Embedding** (词嵌入): map each word to a dense low-dimensional vector ($d=50$–$300$); semantically similar → close in vector space
- Input: large corpus, Vocabulary $V$, dimension $d$ | Output: $f: V \rightarrow \mathbb{R}^d$
- **Self-Supervised Learning** (自监督学习): generates training signals from data itself, **NO manual labels needed**
- **Word Analogy** (词类比): $\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}$; $e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$ ✅

> ⚠️ 1000-word vocab → embedding dim = 1000? → **False** (typical 50–300, NOT equal to vocab size; 1000-dim = one-hot, defeats purpose)
> ⚠️ "Most modern NLP (Natural Language Processing, 自然语言处理) algorithms do not use embeddings" → **False** (Word2Vec → GloVe → BERT (Bidirectional Encoder Representations from Transformers) → GPT (Generative Pre-trained Transformer) ALL use embeddings)

### TF-IDF (词频-逆文档频率) vs Word Embeddings (词嵌入)

| Property | TF-IDF (词频-逆文档频率) | Word Embeddings (词嵌入) |
|---|---|---|
| Dimensionality (维度) | High (= vocab size) | Low (50–300) |
| Sparsity (稀疏性) | Sparse | Dense |
| Semantics (语义) | ❌ None | ✅ Captures meaning |
| Context (上下文) | ❌ None | ✅ Learned from context |
| DL (Deep Learning, 深度学习) suitability | ❌ Poor | ✅ Good |

### Word2Vec — Self-supervised, learns word vectors from context

#### CBOW (Continuous Bag of Words, 连续词袋模型) vs Skip-gram (跳字模型)

| Property | CBOW (Continuous Bag of Words, 连续词袋模型) | Skip-gram (跳字模型) |
|---|---|---|
| Input → Output | Context words → predict **CENTER word** | **CENTER word** → predict context words |
| Training speed | ⚡ Faster | 🐢 Slower |
| Best for | Frequent words, large corpus | Rare words, small corpus |
| Classification difficulty | Easier | Harder |

> ⚠️ "Skip-gram determines central word from surrounding context" → **False** (that's CBOW (Continuous Bag of Words, 连续词袋模型)!)
> ⚠️ Skip-gram: center word → context words. CBOW (Continuous Bag of Words, 连续词袋模型): context words → center word. Don't confuse!

- Vector = row of hidden layer weight matrix
- **Gensim Word2Vec default**: `vector_size=100`

```python
model = Word2Vec(text, min_count=1, vector_size=50, window=5, sg=1, negative=5)
# sg=1: Skip-gram | sg=0: CBOW | window=5: context window | negative=5: negative samples
```

#### SGNS (Skip-Gram with Negative Sampling, 跳字负采样)

1. Treat target word $t$ and neighboring context word $c$ as positive examples (正样本)
2. Randomly sample other words as negative examples (负样本)
3. Use logistic regression (逻辑回归) to train classifier to distinguish two cases
4. Use learned weights as embeddings (嵌入)
- Reduces softmax $O(V)$ → binary classification $O(k)$

### GloVe (Global Vectors for Word Representation, 全局词向量表示)

- Unsupervised learning; invented at Stanford by Pennington et al. (2014)
- Builds global word-word co-occurrence matrix (全局词-词共现矩阵), then factorizes it
- $w_i \cdot w_j \approx \log(\text{co-occurrence count})$
- **Global** (全局): entire corpus co-occurrence matrix | **Local** (局部): context window

> ⚠️ GloVe (Global Vectors for Word Representation, 全局词向量表示) = global co-occurrence + local context window — combines both perspectives

**Pretrained GloVe (全局词向量表示) Vectors**: Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, 50d/100d/200d/300d), Common Crawl (42B/840B tokens), Twitter (2B tweets)

### FastText (快速文本模型)

- Introduced by Facebook (2016), extension of Word2Vec
- Character n-gram composition (字符n-gram组合): word vector = $\sum$ all subword vectors
- Generates character n-grams of length 3 to 6
- ✅ Handles OOV (Out-of-Vocabulary, 未登录词) | ✅ Captures fine-grained info | ✅ Open-source, lightweight | ✅ Multi-language

### Word2Vec vs GloVe (全局词向量表示) vs FastText (快速文本模型)

| Property | Word2Vec | GloVe (全局词向量表示) | FastText (快速文本模型) |
|---|---|---|---|
| Method | Prediction-based (预测) | Count-based + factorization (计数+分解) | Prediction + subword (预测+子词) |
| Training data | Local context window | Global co-occurrence matrix | Local context + char n-grams |
| OOV (Out-of-Vocabulary, 未登录词) handling | ❌ Cannot | ❌ Cannot | ✅ Via subword composition |
| Year | 2013 (Mikolov et al.) | 2014 (Pennington et al.) | 2016 (Bojanowski et al.) |

### Word Embedding (词嵌入) Benefits & Limitations

| Benefits | Limitations |
|---|---|
| Dimensionality reduction (降维) | Context insensitivity (上下文不敏感) — static: "bank" has one vector |
| Semantic meaning (语义含义) | Bias (偏见) in training data |
| OOV (Out-of-Vocabulary, 未登录词) handling (FastText) | Limited semantic adaptation (有限语义适应) |
| Transfer learning (迁移学习) | Resource intensive (资源密集) |

### Word Embedding (词嵌入) Evaluation (评估)

| Type | Description |
|---|---|
| **Intrinsic Evaluation** (内在评估) | Assess quality independently: word similarity (词相似度), analogy tasks (类比任务) |
| **Extrinsic Evaluation** (外在评估) | Assess via downstream tasks: text classification (文本分类), NER (Named Entity Recognition, 命名实体识别) |

### Universal Text Representations (通用文本表示) — Preview

- Contextual word representations (上下文词表示): ELMo, BERT (Bidirectional Encoder Representations from Transformers), ULMFiT
- Multiple passes through text, left-to-right and right-to-left


---

## W5: Language Models (语言模型) & RNN (Recurrent Neural Network, 循环神经网络) / LSTM (Long Short-Term Memory, 长短期记忆网络)

### Probability Basics (概率论基础)

- **Conditional Probability** (条件概率): $P(X|Y) = \frac{P(X,Y)}{P(Y)}$
- **Chain Rule** (链式法则): $P(w_1 w_2 \cdots w_n) = P(w_1) \times P(w_2|w_1) \times P(w_3|w_1 w_2) \times \cdots$
- Chain Rule (链式法则) is the **mathematical foundation of ALL Language Models (语言模型)** — from N-gram to GPT (Generative Pre-trained Transformer)
- **Sampling with Replacement** (有放回抽样): probability of sequence = product of individual probabilities

### Language Model (语言模型, LM) Definition

- Predict next word probability distribution: $P(w_t | w_1 \cdots w_{t-1})$
- Goal: learn patterns in text and predict next word based on prior context
- Applications: autocomplete, machine translation (机器翻译), speech recognition (语音识别)

### N-gram LM (N元语言模型)

- **Markov Assumption** (马尔可夫假设): only look at previous $n-1$ words
- $P(w_t | w_{t-n+1} \cdots w_{t-1}) = \frac{Count(w_{t-n+1} \cdots w_t)}{Count(w_{t-n+1} \cdots w_{t-1})}$
- Limitations: data sparsity (数据稀疏), fixed context window (固定上下文窗口, only $n-1$ words), no semantic similarity (无语义相似性), shallow statistical prediction (浅层统计预测)

> ⚠️ "N-gram core idea is deep semantic reasoning" → **False** (N-gram = statistical frequency-based, no semantic understanding)

**Bigram (二元组) Example:**
$P(\text{happy}|\text{feel}) = \frac{Count(\text{feel happy})}{Count(\text{feel})} = \frac{40}{100} = \mathbf{0.4}$

> ⚠️ Count("happy")=30 is a **DISTRACTOR** (干扰信息)! Conditional prob only uses $\frac{Count(AB)}{Count(A)}$, ignore $Count(B)$ alone

**4-gram Example:** "students opened their ___"
- "students opened their books" = 400/1000 → $P(\text{books}) = 0.4$
- "students opened their exams" = 100/1000 → $P(\text{exams}) = 0.1$

### Neural Network (神经网络) LM — Fixed-window

- Input: concatenate last $n$ word embeddings (词嵌入) → hidden layer (隐藏层) → softmax over vocabulary (词汇表)
- Architecture: one-hot → embedding matrix $E$ → concatenated embeddings $e = [e_1; e_2; \cdots; e_n]$ → $h = f(We + b_1)$ → $\hat{y} = \text{softmax}(Uh + b_2)$
- ✅ Word embeddings (词嵌入) capture semantics | ❌ Still fixed window, discards earlier context

> ⚠️ FFNN (Feed-Forward Neural Network, 前馈神经网络) limitation: "The food was good, not bad at all" (positive) vs "The food was bad, not good at all" (negative) — if window only sees last few words, they look similar!

### Sequence Modeling Motivations (序列建模动机)

- Handle variable length sequence data (变长序列数据)
- Track long-term dependency (长期依赖)
- Maintain information about order (顺序信息)
- Share information across the sequence (序列间共享信息)

### RNN (Recurrent Neural Network, 循环神经网络)

- **Stateful computation** (有状态计算): hidden state $h_t$ carries info across time steps
- $h_t = \sigma(W_h \cdot h_{t-1} + W_e \cdot e_t + b)$
- $\hat{y}_t = \text{softmax}(U \cdot h_t + b_2)$
- **Parameter Sharing** (参数共享): same weights ($W_h$, $W_e$) reused at EVERY time step
- **Loss** (损失): $J = -\frac{1}{T} \sum \log P(\text{correct word at } t)$
- **BPTT (Backpropagation Through Time, 时序反向传播)**: error propagates backward through time steps
- ✅ Variable-length input | ✅ Preserves order | ✅ Parameter sharing | ❌ **Vanishing Gradient** (梯度消失)

### FFNN (Feed-Forward Neural Network, 前馈神经网络) vs RNN (Recurrent Neural Network, 循环神经网络)

| Feature | FFNN (Feed-Forward NN, 前馈神经网络) | RNN (Recurrent Neural Network, 循环神经网络) |
|---|---|---|
| Sequence handling | ❌ Fixed-length only | ✅ Variable-length |
| Temporal dependency (时序依赖) | ❌ None | ✅ Via $h_t$ |
| Parameter sharing | ❌ Different weights per layer | ✅ Same weights every step |
| Memory | ❌ No internal state | ✅ Hidden state $h_t$ |

### Gradient Problems (梯度问题)

| Problem | Cause | Effect |
|---|---|---|
| **Vanishing Gradient** (梯度消失) | Gradient $\propto (W_h)^T \rightarrow 0$ | Cannot learn long-range dependencies (长距离依赖) |
| **Exploding Gradient** (梯度爆炸) | Gradient $\rightarrow \infty$ | Unstable training (训练不稳定) |

### LSTM (Long Short-Term Memory, 长短期记忆网络)

- Hochreiter & Schmidhuber (1997) — solves vanishing gradient (梯度消失) problem
- **Dual state**: $h_t$ (short-term hidden state, 隐藏状态) + $c_t$ (long-term cell state, 细胞状态)
- **Three gating mechanisms** (三门控制信息流):

| Gate | Formula | Function |
|---|---|---|
| **Forget gate** (遗忘门) | $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$ | Discard old info (丢弃旧信息) |
| **Input gate** (输入门) | $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$ | Store new info (存储新信息) |
| **Candidate** (候选) | $\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$ | New candidate values |
| **Cell update** (细胞更新) | $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ | **ADDITION** allows gradient flow! |
| **Output gate** (输出门) | $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$ | Output info (输出信息) |
| **Hidden state** | $h_t = o_t \odot \tanh(c_t)$ | Short-term output |

- Cell State (细胞状态) uses **ADDITION** (not multiplication) → gradient doesn't decay → solves Vanishing Gradient (梯度消失)
- Each gate takes values between 0 (closed) and 1 (open) dynamically

> ⚠️ "More hidden layers automatically prevent vanishing gradient (梯度消失)" → ❌ (key is **gating mechanism** (门控机制))
> ⚠️ "LSTM (Long Short-Term Memory, 长短期记忆网络) replaces recurrent with feedforward" → ❌ (LSTM is **STILL** recurrent)
> ⚠️ "LSTM (Long Short-Term Memory, 长短期记忆网络) removes backpropagation (反向传播)" → ❌ (still uses BPTT (Backpropagation Through Time, 时序反向传播))

### RNN (循环神经网络) vs LSTM (长短期记忆网络)

| Feature | RNN (Recurrent Neural Network, 循环神经网络) | LSTM (Long Short-Term Memory, 长短期记忆网络) |
|---|---|---|
| Internal structure | Simple tanh activation | 3 gates + cell state |
| Long-term memory | ❌ Vanishing gradient (梯度消失) | ✅ Cell state preserves info |
| Gradient flow | Decays over time | ✅ Addition-based, stable |
| Complexity | Simple | More parameters |

### Keras LSTM (长短期记忆网络) Implementation

```python
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
model = Sequential()
model.add(LSTM(10, input_shape=(TIMESTEPS, FEATURE_LENGTH)))
model.add(Dense(NUMBER_OF_OUTPUT_NODES))
model.add(Activation('softmax'))
```

### Perplexity (困惑度, PPL)

- Standard evaluation metric for LM (Language Model, 语言模型)
- $PPL = \left(\prod_{t=1}^{T} \frac{1}{P_{LM}(x^{(t+1)} | x^{(t)}, \ldots, x^{(1)})}\right)^{1/T}$
- **Low PPL (Perplexity, 困惑度)** → model predicts well | **High PPL (Perplexity, 困惑度)** → model is confused

### Learning Rate (学习率, $\alpha$)

| Setting | Effect |
|---|---|
| **Too low** (过低) | Very **SLOW** convergence (收敛极慢), may get stuck in local optima (局部最优) |
| **Too high** (过高) | Oscillation/divergence (振荡/发散), may skip optimal solution |

> ⚠️ "Low learning rate → faster training" → **False** (OPPOSITE! Low $\alpha$ = slow convergence)

**Training Data** (训练数据): news/social media/web pages → provide diverse language patterns ✅

### LM (Language Model, 语言模型) Evolution (演进)

| Stage | Model | Key Feature |
|---|---|---|
| 1 | N-gram (N元语言模型) | Statistical counting, fixed window |
| 2 | FFNN (Feed-Forward NN, 前馈神经网络) | Learn embeddings, still fixed window |
| 3 | RNN (Recurrent Neural Network, 循环神经网络) | Variable-length memory, parameter sharing |
| 4 | LSTM (Long Short-Term Memory, 长短期记忆网络) | Solve vanishing gradient via gating |


---

## W6: Seq2Seq (Sequence-to-Sequence, 序列到序列) & Attention (注意力机制)

### Bi-LSTM (Bidirectional Long Short-Term Memory, 双向长短期记忆网络)

- Forward LSTM (正向LSTM, left→right) + Backward LSTM (反向LSTM, right→left)
- Concatenate: $h_t = [\overrightarrow{h_t} ; \overleftarrow{h_t}]$, output dim = $2 \times n_{lstm}$
- Each position has BOTH left and right context (左右上下文)
- Forward and Backward RNN (Recurrent Neural Network, 循环神经网络) have **separate weights** (独立权重)
- ❌ **CANNOT** be used for text generation (文本生成) — backward needs complete sequence; future words don't exist
- ✅ Good for understanding tasks: classification (分类), NER (Named Entity Recognition, 命名实体识别), sentiment analysis (情感分析)
- Motivation example: "The movie was terribly exciting!" — "terribly" needs BOTH left ("was") and right ("exciting") context to determine positive meaning

```python
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    Bidirectional(LSTM(n_lstm)),
    Dense(1, activation='sigmoid')
])
```

### Unidirectional LSTM (单向LSTM) vs Bi-LSTM (双向LSTM)

| Feature | Unidirectional LSTM (单向LSTM) | Bi-LSTM (Bidirectional LSTM, 双向LSTM) |
|---|---|---|
| Context direction | Left only (仅左侧) | Both left and right (左右两侧) |
| Output dimension | $n_{lstm}$ | $2 \times n_{lstm}$ |
| Text generation (文本生成) | ✅ Can generate | ❌ Cannot generate |
| Understanding tasks | Good | ✅ Better (richer context) |
| Parameters | Fewer | ~Doubled |

### Multi-layer RNN (多层RNN) / LSTM (长短期记忆网络)

- Hidden states from layer $i$ are inputs to layer $i+1$
- Stacking multiple layers captures increasingly abstract features

### Five Sequence Architectures (五种序列架构)

| Type | Input → Output | Example |
|---|---|---|
| One-to-one (一对一) | Fixed → Fixed | Image classification (图像分类) |
| One-to-many (一对多) | Fixed → Sequence | Image captioning (图像描述) |
| Many-to-one (多对一) | Sequence → Fixed | Sentiment analysis (情感分析) |
| Many-to-many synced (多对多同步) | Seq → Seq (same len) | POS (Part of Speech, 词性) tagging |
| Many-to-many unsynced (多对多异步) | Seq → Seq (diff len) | Translation (翻译) — Seq2Seq (Sequence-to-Sequence, 序列到序列) |

### Seq2Seq (Sequence-to-Sequence, 序列到序列) / Encoder-Decoder (编码器-解码器)

- **Encoder** (编码器): LSTM (Long Short-Term Memory, 长短期记忆网络) reads entire source sequence → compresses into fixed-length vector ("Encoder Vector")
- **Decoder** (解码器): uses that vector as initial state, autoregressively generates target sequence
- **Conditional LM (条件语言模型)**: $P(y_1 \cdots y_t | x_1 \cdots x_s)$ — language model conditioned on source sequence
- Can handle different input/output lengths (e.g., French 4 words → English 6 words)
- Training loss: $J = \frac{1}{T} \sum J_t$ = average negative log probability of each target word
- Backpropagation (反向传播) operates **end-to-end** (端到端)

### Teacher Forcing (教师强制) vs Autoregressive (自回归) Decoding

| Phase | Decoder Input | Effect |
|---|---|---|
| **Training** (Teacher Forcing, 教师强制) | Ground truth previous word (真实标签) | Fast convergence (快速收敛), stable |
| **Testing** (Autoregressive, 自回归) | Own previous prediction (自身预测) | Error accumulation (误差累积) ⚠️ |

- **Exposure Bias** (曝光偏差): training/testing input mismatch → error accumulation at test time

### Seq2Seq (序列到序列) Bottleneck Problem (信息瓶颈)

- ❌ Entire source compressed into **single vector** → long sentences lose information
- This motivates the Attention Mechanism (注意力机制)

### Attention Mechanism (注意力机制)

- Decoder dynamically attends to different encoder positions at each step → eliminates bottleneck (消除瓶颈)

**4-Step Process:**

| Step | Operation | Formula |
|---|---|---|
| 1 | Attention score (注意力分数) | $score_i = \text{dot}(decoder\_state, encoder\_state_i)$ |
| 2 | Attention weight (注意力权重) | $\alpha = \text{softmax}(scores)$ |
| 3 | Context vector (上下文向量) | $context = \sum \alpha_i \times encoder\_state_i$ |
| 4 | Output (输出) | $[decoder\_state ; context] \rightarrow prediction$ |

**Benefits**: ✅ Eliminates bottleneck (消除瓶颈) | ✅ Handles long sentences (处理长句) | ✅ Interpretability (可解释性, alignment table) | ✅ Gradient shortcut path (梯度捷径)
**Limitation**: ❌ Still sequential (RNN-based), cannot parallelize (无法并行)

### Seq2Seq (序列到序列) vs Seq2Seq + Attention (注意力)

| Feature | Seq2Seq (序列到序列) | Seq2Seq + Attention (注意力) |
|---|---|---|
| Source encoding | Single fixed vector (单一固定向量) | Dynamic weighted sum of all states |
| Long sentences | ❌ Information loss (信息丢失) | ✅ Attends to relevant parts |
| Interpretability (可解释性) | ❌ Black box | ✅ Alignment visualization |
| Gradient flow | Through single bottleneck | ✅ Shortcut paths |

### Transformer ("Attention Is All You Need", 2017)

- **Self-Attention** (自注意力): each word attends to ALL other words simultaneously → fully parallel (完全并行)
- **Positional Encoding** (位置编码): explicitly encodes position info (replaces RNN (Recurrent Neural Network, 循环神经网络)'s implicit ordering)
- $O(1)$ path length: any two positions directly connected
- Architecture: encoder stack (编码器堆栈) + decoder stack (解码器堆栈), multi-head attention (多头注意力), feed-forward networks (前馈网络)

### RNN (循环神经网络) Attention vs Self-Attention (自注意力, Transformer)

| Property | RNN (循环神经网络) Attention | Self-Attention (自注意力, Transformer) |
|---|---|---|
| Who attends to whom | Decoder → Encoder | Every word → all words |
| Depends on RNN (循环神经网络) | ✅ Yes | ❌ No |
| Parallel processing (并行处理) | ❌ Sequential | ✅ Fully parallel |
| Long-range dependency (长距离依赖) | Improved via attention | $O(1)$ direct path |
| Memory complexity | Lower | $O(n^2)$ |

→ **BERT (Bidirectional Encoder Representations from Transformers, 双向编码器表示)** (encoder-only, bidirectional, understanding tasks)
→ **GPT (Generative Pre-trained Transformer, 生成式预训练Transformer)** (decoder-only, autoregressive, generation tasks)

### Architecture Evolution (架构演进)

| From → To | Problem Solved | Trade-off |
|---|---|---|
| Unidirectional LSTM → Bi-LSTM (双向LSTM) | Direction blindness → sees both sides | Cannot generate text; params doubled |
| Bi-LSTM (双向LSTM) → Seq2Seq (序列到序列) | Different input/output lengths | Information bottleneck (信息瓶颈, single vector) |
| Seq2Seq (序列到序列) → +Attention (注意力) | Bottleneck → dynamic weighting all positions | Still sequential processing |
| RNN (循环神经网络)+Attention → Transformer | Sequential → fully parallel | $O(n^2)$ memory; needs positional encoding (位置编码) |

**Full evolution chain**: N-gram → FFNN (Feed-Forward Neural Network, 前馈神经网络) → RNN (Recurrent Neural Network, 循环神经网络) → LSTM (Long Short-Term Memory, 长短期记忆网络) → Bi-LSTM (Bidirectional LSTM, 双向LSTM) → Seq2Seq (Sequence-to-Sequence, 序列到序列) → +Attention (注意力机制) → Transformer

---

## Milestones (里程碑)

| Year | Event |
|---|---|
| **1950** | Turing Test (图灵测试) |
| **1989** | UAT (Universal Approximation Theorem, 通用逼近定理) — Cybenko |
| **1997** | LSTM (Long Short-Term Memory, 长短期记忆网络) — Hochreiter & Schmidhuber |
| **2003** | Neural LM (神经语言模型) — Bengio et al. |
| **2013** | Word2Vec — Mikolov et al. |
| **2014** | GloVe (Global Vectors, 全局词向量) — Pennington et al. (Stanford) |
| **2016** | FastText (快速文本模型) — Facebook (Bojanowski et al.) |
| **2017** | **Transformer** — "Attention Is All You Need" ← NLP (Natural Language Processing, 自然语言处理) turning point |
| **2018** | BERT (Bidirectional Encoder Representations from Transformers) / GPT (Generative Pre-trained Transformer) |

---

## Midterm Exam Info (期中考试信息)

- Week 7, 60 min, 30 questions (multiple-choice + true/false, no essay)
- Material: W1–W6, closed book
- Cheat sheet: 1 letter-size page (8.5 × 11 inches), both sides allowed
- **5cm × 5cm blank** in top-left corner of each side for proctor signature
- Bring HB pencils, eraser, ID; submit questionnaire + Scantron answer sheet

---

## Quiz Quick Review (测验速记)

```
✅ Transformer = 2017 turning point (self-attention, 自注意力)
✅ NLP (Natural Language Processing, 自然语言处理) goal = understand + interpret + generate
✅ Text Classification (文本分类) = NLU (Natural Language Understanding, 自然语言理解) (NOT NLG)
✅ Zipf's Law (齐夫定律) = few high-freq words + many rare words
✅ Summarization (文本摘要) must preserve coherence (连贯性)
✅ Tokenization (分词) = pipeline first step
✅ SpaCy has NO Stemming (词干提取); NLTK (Natural Language Toolkit) has both
✅ Poetry analysis (诗歌分析): do NOT stem/lemmatize
✅ WordNet: Hypernym (上位词)/Hyponym (下位词)=IS-A, Meronym (部分词)/Holonym (整体词)=PART-OF
✅ BOW (Bag of Words, 词袋模型) ignores word order
✅ TF-IDF (词频-逆文档频率) = high-dim sparse, no semantics
✅ IDF = log(N / df(t)); word in all docs → IDF=0
✅ cos ≈ 1 → semantically similar
✅ Embedding dim 50-300 (NOT equal to vocab size)
✅ Word2Vec default 100 dim (Gensim)
✅ CBOW (Continuous Bag of Words): context→center; Skip-gram: center→context
✅ GloVe (Global Vectors) = global co-occurrence + local window
✅ FastText = subword n-grams, handles OOV (Out-of-Vocabulary)
✅ Self-supervised (自监督) = no manual labels
✅ Word analogy: king - man + woman ≈ queen
✅ Chain Rule (链式法则) = mathematical foundation of ALL LMs (Language Models)
✅ N-gram = statistical shallow, no semantic reasoning
✅ Conditional prob = Count(AB) / Count(A) — ignore Count(B) alone
✅ RNN (Recurrent Neural Network) stateful computation (h_t across time steps)
✅ LSTM (Long Short-Term Memory) 3 gates: forget, input, output (ADDITION → gradient flows)
✅ Low learning rate → SLOW (not fast!)
✅ Bi-LSTM (Bidirectional LSTM) cannot generate text
✅ Seq2Seq (Sequence-to-Sequence) bottleneck → Attention eliminates it
✅ Exposure Bias (曝光偏差): training uses ground truth, testing uses own prediction
✅ Attention 4 steps: score → softmax → weighted sum → concat output
✅ 5 sequence architectures: 1-1, 1-many, many-1, many-many(synced/unsynced)
✅ Transformer: self-attention, fully parallel, positional encoding
✅ BERT (encoder, bidirectional) / GPT (decoder, autoregressive)
✅ Public datasets (news/social media/web) provide diverse training data
✅ FFNN (Feed-Forward NN) limitation: fixed window, loses earlier context
✅ BPTT (Backpropagation Through Time) = RNN backpropagation method
✅ Perplexity (困惑度): low=good, high=confused
✅ CountVectorizer(ngram_range=(1,2)) → unigrams + bigrams (8+ features, not 7)
✅ Regex \b\w+[-]\w+\b = compound words (high-tech), NOT words ending with hyphen
✅ TF ascending: d2(0.012) < d1000(0.025) < d3(0.031) < d9(0.120) < d1(0.197)
```
