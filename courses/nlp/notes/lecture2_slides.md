# Week 2: 文本预处理与探索性分析 (Text Preprocessing and Exploratory Analysis)

> Source: `lecture_2_W26.pdf`
> Total slides: 56
> Instructor: Hala Own, Ph.D.

---

## 1. NLP方法概览 (Approaches to NLP)

![Page 3](lecture2_slides_pages/page_003.png)

**Approaches to NLP:** — NLP的方法

- Heuristics-Based NLP — 基于启发式的NLP
  - Regular Expression — 正则表达式
- Machine Learning for NLP — 用于NLP的机器学习
  - Supervised — 监督学习
  - Unsupervised — 无监督学习
- Deep Learning for NLP — 用于NLP的深度学习
  - Recurrent neural networks — 循环神经网络
  - Long short-term memory — 长短期记忆网络
  - Transformers — Transformer架构

![Page 4](lecture2_slides_pages/page_004.png)

**Rule Based System — Computer Troubleshooting:** — 基于规则的系统——计算机故障排除

- Rule 1: If the computer does not power on, check if the power cable is connected. — 规则1：如果电脑无法开机，检查电源线是否连接。
- Rule 2: If the power is on but the screen is blank, check the monitor's connections. — 规则2：如果电源开启但屏幕空白，检查显示器连接。
- Rule 3: If there is no sound, check the speaker connections and volume settings. — 规则3：如果没有声音，检查扬声器连接和音量设置。
- Rule 4: If the computer is slow, check for malware and free up disk space. — 规则4：如果电脑运行慢，检查恶意软件并释放磁盘空间。
- Design a simple rule-based inference engine to match user-reported symptoms with corresponding rules and provide recommendations. — 设计一个简单的基于规则的推理引擎，将用户报告的症状与对应规则匹配并提供建议。


---

## 2. 正则表达式 (Regular Expressions)

### 2.1 什么是正则表达式 (What Are Regular Expressions?)

![Page 5](lecture2_slides_pages/page_005.png)

**What are Regular Expressions?** — 什么是正则表达式？

- ❑In computing, a regular expression, also referred to as "regex" or "regexp", provides a concise and flexible means for matching strings of text, such as particular characters, words, or patterns of characters. — 在计算中，正则表达式（也称"regex"或"regexp"）提供了一种简洁灵活的方式来匹配文本字符串，如特定字符、单词或字符模式。
- ❑A regular expression is written in a formal language that can be interpreted by a regular expression processor. — 正则表达式用一种可被正则表达式处理器解释的形式语言编写。

### 2.2 元字符 (Metacharacters)

![Page 6](lecture2_slides_pages/page_006.png)

**Regular Expression Quick Guide: metacharacters** — 正则表达式快速指南：元字符

| Symbol | Meaning                                           |
| ------ | ------------------------------------------------- |
| `.`    | Matches any single character                      |
| `[ ]`  | Matches a single character in the listed set      |
| `^`    | Beginning of string (based on the position)       |
| `$`    | End of string                                     |
| `*`    | Matches 0 or more characters                      |
| `+`    | Matches 1 or more characters                      |
| `?`    | Zero or one occurrence of the preceding character |

![Page 7](lecture2_slides_pages/page_007.png)

**Regular Expression Quick Guide (continued):** — 正则表达式快速指南（续）

| Symbol  | Meaning                                                            |
| ------- | ------------------------------------------------------------------ |
| `{m,n}` | Specify number of times character is matched between m and n times |
| `\`     | Escape character                                                   |
| `\|`    | Or                                                                 |
| `( )`   | Capture group inside parenthesis                                   |

### 2.3 字符类 (Character Classes)

![Page 8](lecture2_slides_pages/page_008.png)

**Character Classes:** — 字符类

- `\s` — matches any whitespace — 匹配任何空白字符
- `\w` — matches any alpha character. Equivalent to `[A-Za-z]` — 匹配任何字母字符
- `\d` — matches any numeric character. Equivalent to `[0-9]` — 匹配任何数字字符
- You may negate these by capitalizing. For example, `\D` matches anything not a digit — 大写表示取反，例如 `\D` 匹配非数字字符

### 2.4 正则表达式示例 (Examples)

![Page 9](lecture2_slides_pages/page_009.png)

**Letters inside square brackets `[]`:** — 方括号内的字母

| Pattern        | Matches              |
| -------------- | -------------------- |
| `[wW]oodchuck` | Woodchuck, woodchuck |
| `[1234567890]` | Any digit            |

**Ranges `[A-Z]`:** — 范围

| Pattern | Matches              |
| ------- | -------------------- |
| `[A-Z]` | An upper case letter |
| `[a-z]` | A lower case letter  |
| `[0-9]` | A single digit       |

![Page 10](lecture2_slides_pages/page_010.png)

**Regular Expressions: `?` `*` `+` `.`** — 正则表达式：`?` `*` `+` `.`

| Pattern   | Meaning                    | Matches                    |
| --------- | -------------------------- | -------------------------- |
| `colou?r` | Optional previous char     | color, colour              |
| `oo*h!`   | 0 or more of previous char | oh!, ooh!, oooh!, ooooh!   |
| `o+h!`    | 1 or more of previous char | oh!, ooh!, oooh!, ooooh!   |
| `baa+`    | 1 or more 'a'              | baa, baaa, baaaa, baaaaa   |
| `beg.n`   | Any single char            | begin, begun, begun, beg3n |

### 2.5 否定与锚定 (Negation and Anchors)

![Page 11](lecture2_slides_pages/page_011.png)

**Regular Expressions: Negation** — 正则表达式：否定

- Carat means negation only when first in `[]` — 尖号仅在`[]`中第一个位置时表示否定

| Pattern  | Matches                  |
| -------- | ------------------------ |
| `[^A-Z]` | Not an upper case letter |
| `[^Ss]`  | Neither 'S' nor 's'      |
| `[^e^]`  | Neither e nor ^          |

![Page 12](lecture2_slides_pages/page_012.png)

**Regular Expressions: Anchors `^` `$`**

| Pattern      | Matches           |
| ------------ | ----------------- |
| `^[A-Z]`     | Palo Alto         |
| `^[^A-Za-z]` | "Hello"           |
| `\.$`        | The end.          |
| `.$`         | The end? The end! |

### 2.6 Python正则函数 (Python Regex Functions)

![Page 13](lecture2_slides_pages/page_013.png)

**Online Regular Expressions:** https://regex101.com/ — 在线正则表达式工具

![Page 14](lecture2_slides_pages/page_014.png)

**Python Regex Functions:** — Python正则函数

- `re.match(r, s)` returns a matched object if the regex r matches at the start of string s — 如果正则 r 在字符串 s 开头匹配则返回匹配对象
- `re.search(r, s)` returns a matched object if the regex r matches anywhere in string s — 如果正则 r 在字符串 s 任何位置匹配则返回匹配对象
- `findall(pattern, string)` return a list of strings giving all nonoverlapping matches of pattern in string — 返回字符串中所有不重叠匹配的列表

![Page 15](lecture2_slides_pages/page_015.png)

- `sub(pattern, repl, string)` returns the string obtained by replacing the (first count) leftmost nonoverlapping occurrences of pattern in string by repl — 用 repl 替换字符串中 pattern 的最左边不重叠出现
- `compile(pattern)` compiles a regular expression pattern string into a regular expression pattern object, for later matching — 将正则表达式模式字符串编译成模式对象供后续匹配使用

![Page 16](lecture2_slides_pages/page_016.png)

- `groups()` Returns a tuple of all group's substrings of the match — 返回匹配中所有分组子串的元组
- `span([group])` Returns the two-item tuple: `(start(group), end(group))` — 返回二元组：(开始位置, 结束位置)

![Page 17](lecture2_slides_pages/page_017.png)

```python
import re
re.split(" ", "ab bc cd")       # ['ab', 'bc', 'cd']
re.split("\d", "ab1bc4cd")      # ['ab', 'bc', 'cd']
```

### 2.7 正则表达式用例 (Use Cases)

![Page 18](lecture2_slides_pages/page_018.png)

**Regular Expression: Use Cases** — 正则表达式：用例

- Text cleaning — 文本清洗
- Tokenization — 分词
- Information Retrieval — 信息检索
- Sentiment Analysis — 情感分析
- Language Detection — 语言检测

### 2.8 课堂练习 (Class Activities)

![Page 19](lecture2_slides_pages/page_019.png)

**Activity 1:** Write a regexp to check if any URL exists in the text. — 活动1：编写正则表达式检查文本中是否存在URL。

```python
text = "Visit my website at https://www.example.com or check out http://another-example.org/path/page.html"
```

![Page 20](lecture2_slides_pages/page_020.png)

**Activity 2:** Given a text, list all the longest possible substrings that are proper variable names in most programming languages. A proper variable name does not start with a digit and does not contain any special character other than underscore. — 活动2：给定文本，列出所有最长的合法变量名子串。合法变量名不以数字开头，且不包含下划线以外的特殊字符。

```python
Text = 'hsdgkjdh;efjewipjrndendrwerji2;;;;8888p9nskdj3905jdkwqld***w3w945{{{{{jwkqs ;weoijrtwioejri'
# Output: ['hsdgkjdh', 'efjewipjrndendrwerji2', 'p9nskdj3905jdkwqld', 'w3w945', 'jwkqs', 'weoijrtwioejri']
```


---

## 3. NLP开发生命周期 (NLP Development Life Cycle)

![Page 21](lecture2_slides_pages/page_021.png)

**NLP Development Life Cycle:** — NLP开发生命周期

Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model (iterative loop) — 需求收集 → 数据收集 → 文本预处理 → 特征提取 → 模型构建 → 评估 → 部署 → 收集更多数据/改进模型（迭代循环）


---

## 4. 文本预处理流水线 (Text Preprocessing Pipeline)

### 4.1 预处理动机 (Motivations)

![Page 22](lecture2_slides_pages/page_022.png)

**Text-Preprocessing and Cleaning: Motivations** — 文本预处理与清洗：动机

- Clean and standardize the text data to make it more suitable for NLP tasks — 清洗和标准化文本数据使其更适合NLP任务
- Convert the text data into a format that can be easily understood and processed by NLP algorithms — 将文本数据转换为NLP算法容易理解和处理的格式
- Improve the performance and accuracy of NLP models — 提高NLP模型的性能和准确性

### 4.2 流水线概览 (Pipeline Overview)

![Page 23](lecture2_slides_pages/page_023.png)

**Text Pre-Processing Pipeline:** — 文本预处理流水线

Documents → Tokenization → Noise Entities Removal → Normalization

- May be varied depending on the task you are working on and the data you have — 可能因你正在处理的任务和数据而有所不同

### 4.3 语言的构建块 (Building Blocks of Language)

![Page 24](lecture2_slides_pages/page_024.png)

**Building Blocks of Language** — 语言的构建块

### 4.4 基本术语 (Basic Terminology)

![Page 25](lecture2_slides_pages/page_025.png)

**Text Preprocessing: Basic Terminology** — 文本预处理：基本术语

- ❑**Corpus** — A Corpus is defined as a collection of text documents. — 语料库——定义为文本文档的集合
  - A data set containing news — 包含新闻的数据集
  - The tweets containing Twitter — 包含推文的Twitter数据
- ❑**Words** — unit of language that has a specific meaning and is separated by spaces or punctuation — 单词——具有特定含义的语言单位，由空格或标点分隔


---

## 5. 分词 (Tokenization)

![Page 26](lecture2_slides_pages/page_026.png)

**Tokenization** — 分词

![Page 27](lecture2_slides_pages/page_027.png)

**Text Pre-processing: Basic Terminology** — 文本预处理：基本术语——语料库、文档、段落、句子和token之间的关系

![Page 28](lecture2_slides_pages/page_028.png)

**Tokenization Demo:** https://text-processing.com/demo/tokenize/ — 分词演示


---

## 6. 噪声实体移除 (Noise Entities Removal)

### 6.1 数据清洗 (Cleaning Data)

![Page 29](lecture2_slides_pages/page_029.png)

**Noise Entities Removal (Cleaning Data):** — 噪声实体移除（数据清洗）

- Noise is considered as that piece of text which is not relevant to the context of the data — 噪声被认为是与数据上下文无关的文本部分
- **Removing Capital letters:** `lowercased_text = text.lower()` — 移除大写字母
- **Removing Numbers:** `clean_text = re.sub('\w*\d\w*', ' ', clean_text)` — 移除数字
- **Removing Punctuation** — 移除标点符号
- **Removing stop words** — 移除停用词

![Page 30](lecture2_slides_pages/page_030.png)

**Cleaning Data — Demo** — 数据清洗——演示

### 6.2 标点符号移除 (Punctuation Removal)

![Page 31](lecture2_slides_pages/page_031.png)

**Cleaning Data - Punctuations** — 数据清洗——标点符号

### 6.3 停用词移除 (Stop Words Removal)

![Page 32](lecture2_slides_pages/page_032.png)

**Cleaning Data – Stop words** — 数据清洗——停用词

![Page 33](lecture2_slides_pages/page_033.png)

**Language stop words — Demo** — 语言停用词——演示

### 6.4 其他噪声实体 (Other Noise Entities)

![Page 34](lecture2_slides_pages/page_034.png)

**Other Noise Entities** — 其他噪声实体：HTML标签、URL、邮箱地址、特殊字符、多余空白

### 6.5 噪声移除通用步骤 (Noise Removal General Steps)

![Page 35](lecture2_slides_pages/page_035.png)

**Noise Removal General Steps** — 噪声移除通用步骤

### 6.6 复合词提取 (Compound Term Extraction)

![Page 36](lecture2_slides_pages/page_036.png)

**Compound Term Extraction:** — 复合词提取

- Extracting and tagging compound words or phrases in text — 提取和标记文本中的复合词或短语
- Demo — 演示


---

## 7. 规范化 (Normalization)

### 7.1 什么是规范化 (What is Normalization?)

![Page 37](lecture2_slides_pages/page_037.png)

**What is Normalization?** — 什么是规范化？

- Normalization is the process of converting a token into its base form — 规范化是将token转换为其基本形式的过程
- Inflection from a word is removed — 移除词的屈折变化

### 7.2 词干提取 (Stemming)

![Page 38](lecture2_slides_pages/page_038.png)

**Stemming:** — 词干提取

- Word stems, known as the base form of a word — 词干，即词的基本形式
- Example: studying → studi, studies → studi — 示例：studying → studi, studies → studi

![Page 39](lecture2_slides_pages/page_039.png)

**Stemming Algorithms (NLTK):** — 词干提取算法（NLTK）

- **Porter Stemmer** — most common, least aggressive — 最常用，最不激进
- **Snowball Stemmer** — improved version of Porter, supports multiple languages — Porter的改进版，支持多种语言
- **Lancaster Stemmer** — most aggressive, may over-stem — 最激进，可能过度切割

![Page 40](lecture2_slides_pages/page_040.png)

**Stemming: Applications** — 词干提取：应用

- Classifying text — 文本分类
- Clustering text — 文本聚类
- Information retrieval, etc. — 信息检索等

### 7.3 词元化 (Lemmatization)

![Page 41](lecture2_slides_pages/page_041.png)

**Lemmatization:** — 词元化

- Obtaining the root form of the word, as it makes use of vocabulary (dictionary importance of words) and morphological analysis (word structure and grammar relations) — 使用词汇表（词典中词的重要性）和形态学分析（词的结构和语法关系）获取词的词根形式
- The output of lemmatization is the root word called **lemma** — 词元化的输出是被称为**词元**的词根
- Example: Am, Are, Is >> **Be** | Running, Ran, Run >> **Run** — 示例：Am, Are, Is >> Be | Running, Ran, Run >> Run

### 7.4 词干提取 vs 词元化 (Stemming vs Lemmatization)

![Page 42](lecture2_slides_pages/page_042.png)

**Normalization Techniques:** — 规范化技术

- ❑Lemmatization is a potentially more accurate way to normalize a word than stemming, because it takes into account a word's meaning — 词元化可能比词干提取更准确，因为它考虑了词的含义
- ❑A lemmatizer uses a knowledge base of word synonyms and word endings to ensure that only words that mean similar things are consolidated into a single token — 词元化器使用同义词和词尾的知识库来确保只有含义相似的词被合并

![Page 43](lecture2_slides_pages/page_043.png)

**Difference between Stemming and Lemmatization:** — 词干提取与词元化的区别

- Based on Context Consideration — 基于上下文考虑
- Stemming is typically faster but not that accurate — 词干提取通常更快但不够准确
- Lemmatization is typically more accurate — 词元化通常更准确
- **Speed vs Accuracy trade-off** — 速度与准确性的权衡

### 7.5 词元化工具 (Lemmatization Tools)

![Page 44](lecture2_slides_pages/page_044.png)

**Lemmatization Tools:** — 词元化工具

- Wordnet Lemmatizer (NLTK)
- Spacy Lemmatizer
- TextBlob
- CLiPS Pattern
- Stanford CoreNLP
- Gensim Lemmatizer
- TreeTagger

### 7.6 何时不使用 (When Not to Use)

![Page 45](lecture2_slides_pages/page_045.png)

**When Not to Use Lemmatization and Stemming:** — 何时不使用词元化和词干提取

- Specific tasks (e.g., poetry analysis) — 特定任务（如诗歌分析）
- Computational cost — 计算成本
- Social media — 社交媒体

### 7.7 规范化的重要性 (Importance of Normalization)

![Page 46](lecture2_slides_pages/page_046.png)

**Importance of Normalization** — 规范化的重要性

![Page 47](lecture2_slides_pages/page_047.png)

**How Do They Work? — Demo** — 它们如何工作？——演示


---

## 8. 词性标注与命名实体识别 (POS Tagging & Named Entity Recognition)

### 8.1 词性标注 (POS Tagging)

![Page 48](lecture2_slides_pages/page_048.png)

**Parts of Speech (POS) Tagging:** — 词性标注

- Process of identifying a word as nouns, pronouns, verbs, adjectives, etc. — 将词识别为名词、代词、动词、形容词等的过程
- Ref: https://nlpforhackers.io/tag/part-of-speech/

![Page 49](lecture2_slides_pages/page_049.png)

**POS Tag Set:** — 词性标记集

- You can print it using Python: `nltk.help.upenn_tagset()` — 可以用Python打印：`nltk.help.upenn_tagset()`
- Ref: https://thottingal.in/blog/2019/09/10/bis-pos-tagset-review/

![Page 50](lecture2_slides_pages/page_050.png)

**POS Tagging — Demo** — 词性标注——演示

![Page 51](lecture2_slides_pages/page_051.png)

**Why Do We Need Part Of Speech (POS)?** — 为什么需要词性标注？

- ❑Syntactic and semantic analysis — 句法和语义分析
- ❑Structure and meaning of sentences — 句子的结构和含义
- Improve the accuracy of other NLP tasks — 提高其他NLP任务的准确性

### 8.2 命名实体识别 (Named Entity Recognition - NER)

![Page 52](lecture2_slides_pages/page_052.png)

**Named Entity Recognition:** — 命名实体识别

- Identifies and tags named entities in text (people, places, organizations, phone numbers, emails, etc.) — 识别和标记文本中的命名实体（人名、地名、组织、电话号码、邮箱等）

```python
from nltk.chunk import ne_chunk
text = "James Smith lives in the United States."
tokens = pos_tag(word_tokenize(text))
entities = ne_chunk(tokens)
```

![Page 53](lecture2_slides_pages/page_053.png)

**Why Do We Need Named Entity Recognition:** — 为什么需要命名实体识别

- Information extraction — 信息提取
- Searching and indexing — 搜索和索引
- Sentiment analysis — 情感分析


---

## 9. 本周总结 (Summary)

![Page 54](lecture2_slides_pages/page_054.png)

**Class Activity:** — 课堂活动

For which of the following tasks we shouldn't do stemming/lemmatization? A. Poetry Analysis, B. Text Classification, C. Sentiment Analysis → **Answer: A. Poetry Analysis** — 以下哪个任务不应该做词干提取/词元化？A. 诗歌分析 B. 文本分类 C. 情感分析 → 答案：A. 诗歌分析

![Page 55](lecture2_slides_pages/page_055.png)

**Summary:** — 总结

- **Regular expressions**, which will play an important part throughout the course — 正则表达式，将在整个课程中发挥重要作用
- **Fundamental operations in text analysis:** — 文本分析的基本操作：
  - **Tokenization:** breaking up a character string into words, punctuation marks and other meaningful expressions — 分词：将字符串分解为词、标点和其他有意义的表达
  - **Stemming:** removing affixes from words — 词干提取：去除词的词缀
  - **Tagging:** associating each word in a text with a grammatical category or part of speech — 标注：将文本中每个词与语法类别或词性关联

![Page 56](lecture2_slides_pages/page_056.png)

**Q&A** — 问答环节
