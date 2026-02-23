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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Rule-based systems (基于规则的系统):**
>
> A rule-based system uses hand-crafted IF-THEN rules to match input patterns to outputs. No learning occurs — the rules are written by domain experts. This is the simplest form of NLP and the oldest approach.
>
> > 基于规则的系统使用手工编写的 IF-THEN 规则将输入模式匹配到输出。没有学习过程——规则由领域专家编写。这是最简单、最古老的 NLP 方法。
>
> **(2) Three eras of NLP (NLP的三个时代):**
>
> Heuristics (hand-written regex rules) → ML (learn from labeled data) → DL (learn representations with neural networks). This course progresses through all three, starting with regex in this week.
>
> > 启发式（手写正则规则）→ ML（从标注数据学习）→ DL（用神经网络学习表示）。本课程按顺序讲解这三种方法，本周从正则表达式开始。
>
> **🎯 Why:**
> **(1) Regex is still essential (正则表达式仍然不可或缺):**
>
> For structured patterns (emails, phone numbers, dates, URLs), regex is faster, cheaper, and more reliable than any ML model. You should NOT use a Transformer to extract email addresses — regex does it perfectly in microseconds.
>
> > 对于结构化模式（邮箱、电话号码、日期、URL），正则表达式比任何 ML 模型更快、更便宜、更可靠。你不应该用 Transformer 来提取邮箱地址——正则表达式在微秒内就能完美完成。
>
> **(2) Understanding limitations drives evolution (理解局限性驱动进化):**
>
> Rule-based systems can't handle ambiguity or unseen patterns. Recognizing this limitation is WHY the field moved to ML and then DL — each era solves problems the previous couldn't.
>
> > 基于规则的系统无法处理歧义或未见过的模式。认识到这个局限性正是该领域转向 ML 然后 DL 的原因——每个时代都解决了前一代无法解决的问题。
>
> **⚠️ Pitfall:**
> **(1) Don't dismiss simple methods (不要忽视简单方法):**
>
> Students often jump to deep learning for every NLP problem. But in production, 80% of text processing tasks (data cleaning, format validation, extraction) are best solved with regex and simple rules. Always try the simplest approach first.
>
> > 学生常常对每个 NLP 问题都用深度学习。但在生产环境中，80% 的文本处理任务（数据清洗、格式验证、提取）用正则和简单规则最好解决。总是先尝试最简单的方法。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What are the three main approaches to NLP?" → Heuristics-based (regex, rules), Machine Learning (supervised/unsupervised), Deep Learning (RNN, LSTM, Transformers).
>
> > "NLP的三种主要方法是什么？" → 基于启发式（正则、规则）、机器学习（监督/无监督）、深度学习（RNN、LSTM、Transformer）。
>
> **(2) 应用题 (Application):**
>
> "Give an example where a rule-based system is preferred over ML." → Extracting phone numbers or email addresses from text — the pattern is fixed and well-defined, ML is overkill.
>
> > "举一个基于规则系统优于 ML 的例子。" → 从文本中提取电话号码或电子邮件地址——模式是固定且明确的，ML 是杀鸡用牛刀。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Regular expression (正则表达式):**
>
> A formal mini-language for describing text patterns. It uses metacharacters (`.`, `*`, `+`, `?`, `[]`, `^`, `$`) to create flexible pattern templates that search engines can match against strings. Regex is deterministic — the same pattern always produces the same match.
>
> > 一种描述文本模式的形式化迷你语言。它使用元字符（`.`、`*`、`+`、`?`、`[]`、`^`、`$`）创建灵活的模式模板，搜索引擎可以用来匹配字符串。正则是确定性的——相同模式总是产生相同匹配结果。
>
> **(2) Greedy vs lazy matching (贪婪匹配 vs 惰性匹配):**
>
> By default, `*` and `+` are **greedy** — they match as much text as possible. Adding `?` after them (`*?`, `+?`) makes them **lazy** — matching as little as possible. This distinction matters when extracting content between delimiters.
>
> > 默认情况下，`*` 和 `+` 是**贪婪**的——它们会匹配尽可能多的文本。在后面加 `?`（`*?`、`+?`）使它们**惰性**——匹配尽可能少的内容。在提取分隔符之间的内容时这个区别很重要。
>
> **🎯 Why:**
> **(1) Foundation of text preprocessing (文本预处理的基础):**
>
> Almost every NLP pipeline starts with regex: cleaning HTML tags, removing special characters, extracting patterns, tokenization. Without regex fluency, you cannot effectively preprocess text data for any downstream NLP task.
>
> > 几乎每个 NLP 流水线都从正则开始：清理 HTML 标签、移除特殊字符、提取模式、分词。没有正则的熟练使用，你无法有效地为任何下游 NLP 任务预处理文本数据。
>
> **(2) match vs search vs findall distinction (match vs search vs findall 的区分):**
>
> `re.match()` only checks the START of the string. `re.search()` scans the ENTIRE string for the first match. `re.findall()` returns ALL non-overlapping matches. Choosing the wrong one is a very common bug. Use `search` when you want "is this pattern anywhere in the text?"
>
> > `re.match()` 只检查字符串的开头。`re.search()` 扫描整个字符串寻找第一个匹配。`re.findall()` 返回所有不重叠的匹配。选错函数是非常常见的 bug。当你想知道"这个模式是否存在于文本中的任何地方"时使用 `search`。
>
> **💡 Intuition:**
> **(1) Regex as a "smart Ctrl+F" (正则表达式是"智能的 Ctrl+F"):**
>
> Regular Ctrl+F searches for exact text. Regex is like Ctrl+F with wildcards and logic — you can say "find any word that starts with a capital letter and ends with 'ing'" or "find all email addresses." The metacharacters are your logic operators.
>
> > 普通 Ctrl+F 搜索精确文本。正则像带通配符和逻辑的 Ctrl+F——你可以说"找所有以大写字母开头、以'ing'结尾的词"或"找所有邮箱地址。"元字符就是你的逻辑运算符。
>
> **(2) The `^` dual personality (尖号 `^` 的双重身份):**
>
> `^` inside `[]` means negation: `[^A-Z]` = NOT uppercase. `^` outside `[]` means start of string: `^Hello` = must start with "Hello". Same symbol, completely different meaning depending on context — a source of many regex bugs.
>
> > `^` 在 `[]` 内表示否定：`[^A-Z]` = 非大写字母。`^` 在 `[]` 外表示字符串开头：`^Hello` = 必须以"Hello"开头。同一个符号，根据上下文含义完全不同——这是许多正则 bug 的来源。
>
> **⚠️ Pitfall:**
> **(1) `re.match` ≠ `re.search` (match ≠ search):**
>
> `re.match("cat", "the cat sat")` returns `None` because "cat" is not at position 0. Use `re.search` to find "cat" anywhere. This is the #1 regex mistake in Python.
>
> > `re.match("cat", "the cat sat")` 返回 `None`，因为"cat"不在位置 0。使用 `re.search` 可以在任何位置找到"cat"。这是 Python 中排名第一的正则错误。
>
> **(2) Forgetting to escape special characters (忘记转义特殊字符):**
>
> `.` in regex means "any character", not a literal dot. To match a real dot (like in "file.txt"), you must escape it: `\.`. Similarly, `$`, `*`, `+`, `?`, `(`, `)` all need `\` to be matched literally.
>
> > 正则中的 `.` 表示"任何字符"，不是字面上的点。要匹配真正的点（如"file.txt"中），必须转义：`\.`。类似地，`$`、`*`、`+`、`?`、`(`、`)` 都需要 `\` 来进行字面匹配。
>
> **(3) Raw string prefix `r''` is essential (原始字符串前缀 `r''` 不可少):**
>
> In Python, `\d` in a regular string is interpreted as an escape sequence first. Use `r'\d'` (raw string) to pass the backslash directly to the regex engine. Without `r`, patterns like `\b` (word boundary) get mangled into a backspace character.
>
> > 在 Python 中，普通字符串中的 `\d` 会先被解释为转义序列。使用 `r'\d'`（原始字符串）将反斜杠直接传递给正则引擎。没有 `r`，像 `\b`（单词边界）这样的模式会被错误地转成退格符。
>
> **📝 Exam:**
> **(1) 模式匹配题 (Pattern Matching):**
>
> "What does `r'[a-zA-Z]\w*d+'` match?" → A string starting with a letter, followed by any word characters, and ending with one or more 'd's. It would match "and", "add", "abcd".
>
> > "`r'[a-zA-Z]\w*d+'` 匹配什么？" → 以字母开头、后跟任意单词字符、以一个或多个'd'结尾的字符串。它会匹配"and"、"add"、"abcd"。
>
> **(2) 函数选择题 (Function Selection):**
>
> "Which Python regex function would you use to find ALL email addresses in a document?" → `re.findall()`, because it returns a list of all non-overlapping matches, not just the first one.
>
> > "你会用哪个 Python 正则函数来查找文档中的所有电子邮件地址？" → `re.findall()`，因为它返回所有不重叠匹配的列表，而不只是第一个。
>
> **(3) 正则编写题 (Regex Writing):**
>
> "Write a regex to match valid variable names." → `r'[a-zA-Z_]\w*'` — starts with letter or underscore, followed by any word characters (letters, digits, underscore).
>
> > "写一个匹配有效变量名的正则。" → `r'[a-zA-Z_]\w*'` — 以字母或下划线开头，后跟任意单词字符（字母、数字、下划线）。

---

## 3. NLP开发生命周期 (NLP Development Life Cycle)

![Page 21](lecture2_slides_pages/page_021.png)

**NLP Development Life Cycle:** — NLP开发生命周期

Requirements gathering → Data collection → Text preprocessing → Feature extraction → Model building → Evaluation → Deployment → Gather more data / Improve the model (iterative loop) — 需求收集 → 数据收集 → 文本预处理 → 特征提取 → 模型构建 → 评估 → 部署 → 收集更多数据/改进模型（迭代循环）

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) NLP is iterative, not linear (NLP是迭代式的，不是线性的):**
>
> Unlike traditional software, NLP projects rarely succeed on the first attempt. Models need continuous refinement: more labeled data, better preprocessing, feature tuning. The feedback loop (evaluate → gather more data → improve model) is the most important part of the lifecycle.
>
> > 与传统软件不同，NLP项目很少第一次就成功。模型需要持续改进：更多标注数据、更好的预处理、特征调优。反馈循环（评估 → 收集更多数据 → 改进模型）是生命周期中最重要的部分。
>
> **(2) Preprocessing determines success (预处理决定成败):**
>
> "Garbage in, garbage out." Text preprocessing (today's topic) is where most real-world NLP projects spend 60-80% of their time. A mediocre model with excellent preprocessing often outperforms a state-of-the-art model with poor preprocessing.
>
> > "垃圾进，垃圾出。"文本预处理（今天的主题）是大多数真实NLP项目花费60-80%时间的地方。一个预处理优秀的普通模型往往胜过预处理糟糕的最先进模型。
>
> **💡 Intuition:**
> **(1) Cooking analogy (烹饪类比):**
>
> Building an NLP model is like cooking: requirements = recipe, data collection = buying ingredients, preprocessing = washing and chopping, feature extraction = seasoning, model building = cooking, evaluation = tasting, deployment = serving. If the ingredients aren't cleaned properly, the dish fails regardless of cooking skill.
>
> > 构建NLP模型就像做菜：需求=食谱，数据收集=买食材，预处理=洗切，特征提取=调味，模型构建=烹饪，评估=品尝，部署=上菜。如果食材没清洗好，再好的厨艺也做不出好菜。
>
> **📝 Exam:**
> **(1) 流程题 (Process):**
>
> "List the steps of the NLP development life cycle." → Requirements → Data collection → Preprocessing → Feature extraction → Modeling → Evaluation → Deployment (with iterative feedback loop).
>
> > "列出NLP开发生命周期的步骤。" → 需求 → 数据收集 → 预处理 → 特征提取 → 建模 → 评估 → 部署（带有迭代反馈循环）。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) The preprocessing pipeline is not fixed (预处理流水线不是固定的):**
>
> The order and combination of preprocessing steps depends on the task. For sentiment analysis, you might keep emoticons (they carry sentiment) but remove stop words. For named entity recognition, you MUST preserve capitalization and stop words. There is no one-size-fits-all pipeline.
>
> > 预处理步骤的顺序和组合取决于任务。对于情感分析，你可能保留表情符号（它们携带情感信息）但删除停用词。对于命名实体识别，你必须保留大小写和停用词。没有万能的流水线。
>
> **(2) Corpus vs Document vs Token (语料库 vs 文档 vs Token):**
>
> Corpus = the entire collection (all books in a library). Document = one text unit (one book). Token = one meaningful piece (one word or sub-word). This hierarchy (corpus → document → sentence → token) is fundamental to all NLP systems.
>
> > 语料库 = 整个集合（图书馆里的所有书）。文档 = 一个文本单元（一本书）。Token = 一个有意义的部分（一个词或子词）。这个层次结构（语料库 → 文档 → 句子 → token）是所有NLP系统的基础。
>
> **🎯 Why:**
> **(1) Raw text is messy (原始文本是杂乱的):**
>
> Real-world text contains inconsistent casing ("NLP" vs "nlp"), punctuation, HTML tags, emojis, URLs, numbers, typos, and multiple languages. Without preprocessing, these inconsistencies create a massive, sparse feature space that degrades model performance.
>
> > 真实世界的文本包含不一致的大小写（"NLP" vs "nlp"）、标点符号、HTML标签、表情符号、URL、数字、拼写错误和多种语言。没有预处理，这些不一致性会创建一个巨大、稀疏的特征空间，降低模型性能。
>
> **⚠️ Pitfall:**
> **(1) Over-preprocessing destroys information (过度预处理破坏信息):**
>
> Common mistake: applying ALL preprocessing steps blindly. Lowercasing destroys "US" vs "us" distinction. Removing numbers kills "COVID-19". Stop word removal breaks "not good" → "good" (opposite meaning!). Always think about WHAT information your task needs before cleaning.
>
> > 常见错误：盲目应用所有预处理步骤。小写化破坏"US"（美国）vs "us"（我们）的区别。删除数字会消灭"COVID-19"。停用词删除会把"not good" → "good"（意思完全相反！）。在清洗之前总要想想你的任务需要什么信息。
>
> **📝 Exam:**
> **(1) 定义题 (Definition):**
>
> "What is a corpus in NLP?" → A collection of text documents used as input for NLP analysis. Example: all tweets from Twitter in 2024, or all Wikipedia articles.
>
> > "NLP中什么是语料库？" → 用于NLP分析输入的文本文档集合。例如：2024年Twitter的所有推文，或所有维基百科文章。
>
> **(2) 推理题 (Reasoning):**
>
> "Why is text preprocessing important?" → Raw text is inconsistent and noisy; preprocessing standardizes it to improve model accuracy and reduce feature space dimensionality.
>
> > "为什么文本预处理重要？" → 原始文本不一致且有噪声；预处理将其标准化以提高模型准确性并降低特征空间维度。

---

## 5. 分词 (Tokenization)

![Page 26](lecture2_slides_pages/page_026.png)

**Tokenization** — 分词

![Page 27](lecture2_slides_pages/page_027.png)

**Text Pre-processing: Basic Terminology** — 文本预处理：基本术语——语料库、文档、段落、句子和token之间的关系

![Page 28](lecture2_slides_pages/page_028.png)

**Tokenization Demo:** https://text-processing.com/demo/tokenize/ — 分词演示

> **📝 Notes:**
>
> **📌 What:**
> **(1) Tokenization definition (分词的定义):**
>
> Tokenization is the process of converting raw text into a sequence of meaningful units (tokens) that a model can process. Tokens can be words, sub-words, or characters depending on the tokenizer used. It is always the FIRST step in any NLP pipeline.
>
> > 分词是将原始文本转换为模型可处理的有意义单元（token）序列的过程。Token可以是词、子词或字符，取决于使用的分词器。在任何NLP流水线中它始终是第一步。
>
> **(2) Word-level vs sub-word tokenization (词级 vs 子词分词):**
>
> Word tokenization: "unhappiness" → ["unhappiness"]. Sub-word tokenization (BPE, WordPiece): "unhappiness" → ["un", "happiness"] or ["un", "happ", "iness"]. Modern models (BERT, GPT) use sub-word tokenization to handle rare/unknown words without an infinitely large vocabulary.
>
> > 词级分词："unhappiness" → ["unhappiness"]。子词分词（BPE、WordPiece）："unhappiness" → ["un", "happiness"] 或 ["un", "happ", "iness"]。现代模型（BERT、GPT）使用子词分词来处理罕见/未知词，而不需要无限大的词表。
>
> **🎯 Why:**
> **(1) Computers need discrete units (计算机需要离散单位):**
>
> Computers cannot process raw character streams meaningfully. Tokenization creates discrete, countable units that can be mapped to numerical vectors. Without tokenization, there is no way to build features for any NLP model.
>
> > 计算机无法有意义地处理原始字符流。分词创建离散的、可计数的单位，可以映射到数值向量。没有分词，就没有办法为任何NLP模型构建特征。
>
> **⚠️ Pitfall:**
> **(1) Splitting on whitespace is naïve (按空格分割是天真的):**
>
> Simple `text.split(" ")` fails for: "New York" (one entity, two tokens), "don't" (should be "do" + "n't"), Chinese/Japanese (no spaces between words), and punctuation attached to words ("hello,"). Production tokenizers like NLTK's `word_tokenize` or spaCy handle these correctly.
>
> > 简单的 `text.split(" ")` 对以下情况失败："New York"（一个实体，两个token）、"don't"（应该是"do"+"n't"）、中日文（词之间没有空格）、和附着在词上的标点（"hello,"）。生产级分词器如NLTK的 `word_tokenize` 或spaCy能正确处理。
>
> **📝 Exam:**
> **(1) 定义题 (Definition):**
>
> "What is tokenization?" → The process of converting raw text into a sequence of units (tokens) that a model can process.
>
> > "什么是分词？" → 将原始文本转换为模型可处理的单元（token）序列的过程。
>
> **(2) 应用题 (Application):**
>
> "Tokenize 'I can't wait'" → Using NLTK: ["I", "ca", "n't", "wait"]. Using simple split: ["I", "can't", "wait"]. Different tokenizers produce different results.
>
> > "对'I can't wait'分词" → 使用NLTK：["I", "ca", "n't", "wait"]。使用简单分割：["I", "can't", "wait"]。不同的分词器产生不同的结果。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) What counts as "noise" (什么算"噪声"):**
>
> Noise = any text element not relevant to your specific NLP task. This includes: capital letters (inconsistency), numbers (if not needed), punctuation, stop words ("the", "is", "a"), HTML tags, URLs, special characters, and extra whitespace. But remember — what is "noise" depends entirely on the task.
>
> > 噪声 = 与你具体NLP任务无关的任何文本元素。包括：大写字母（不一致性）、数字（如果不需要）、标点、停用词（"the"、"is"、"a"）、HTML标签、URL、特殊字符和多余空白。但请记住——什么是"噪声"完全取决于任务。
>
> **(2) Stop words (停用词):**
>
> High-frequency words with little semantic content: "the", "is", "at", "which", "on". They inflate the feature space without adding meaning. NLTK and spaCy provide pre-built stop word lists, but you should always customize them for your domain.
>
> > 语义内容少的高频词："the"、"is"、"at"、"which"、"on"。它们膨胀特征空间而不增加含义。NLTK和spaCy提供预建的停用词列表，但你应该总是根据你的领域自定义它们。
>
> **🎯 Why:**
> **(1) Reduce dimensionality (降低维度):**
>
> Every unique token becomes a dimension in the feature space. "The" appears in almost every document but adds zero discriminative power. Removing it reduces dimensions without losing useful information — making models faster and more accurate.
>
> > 每个唯一的token成为特征空间中的一个维度。"The"出现在几乎每个文档中但增加零区分能力。删除它可以在不丢失有用信息的情况下降低维度——使模型更快更准确。
>
> **(2) Normalize representations (规范化表示):**
>
> "NLP", "nlp", "Nlp" should be treated as the same word. Lowercasing ensures consistent representation. Similarly, removing punctuation prevents "word" and "word," from being treated as different tokens.
>
> > "NLP"、"nlp"、"Nlp"应该被视为同一个词。小写化确保一致的表示。类似地，移除标点防止"word"和"word,"被视为不同的token。
>
> **⚠️ Pitfall:**
> **(1) Lowercasing destroys named entities (小写化破坏命名实体):**
>
> "Apple" (the company) vs "apple" (the fruit). If your task involves named entity recognition, lowercasing will destroy the capitalization cue that distinguishes proper nouns from common nouns. Always consider your downstream task.
>
> > "Apple"（公司）vs "apple"（水果）。如果你的任务涉及命名实体识别，小写化会破坏区分专有名词和普通名词的大小写线索。总是考虑你的下游任务。
>
> **(2) Stop word removal can change meaning (停用词移除可能改变含义):**
>
> "not good" → remove "not" (it's a stop word!) → "good". The meaning is completely reversed. For sentiment analysis, negation words ("not", "no", "never") must be kept even though they're technically stop words.
>
> > "not good" → 删除"not"（它是停用词！）→ "good"。含义完全反转。对于情感分析，否定词（"not"、"no"、"never"）必须保留，即使它们技术上是停用词。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "What are stop words and why do we remove them?" → High-frequency words with little semantic content ("the", "is", "a"). We remove them to reduce feature space dimensionality and improve model efficiency.
>
> > "什么是停用词，为什么要移除？" → 语义内容少的高频词（"the"、"is"、"a"）。我们移除它们来降低特征空间维度并提高模型效率。
>
> **(2) 判断题 (True/False):**
>
> "Text cleaning is always beneficial for NLP." → False — over-cleaning can destroy useful information (e.g., removing negation words for sentiment analysis, lowercasing for NER).
>
> > "文本清洗对NLP总是有益的。" → 错误——过度清洗会破坏有用信息（例如，为情感分析移除否定词，为NER小写化）。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) Stemming (词干提取):**
>
> A crude, rule-based method that chops off word suffixes to approximate the root. "studying" → "studi", "studies" → "studi". The output may NOT be a real word — it's just a stem. It works by applying a series of suffix-stripping rules (e.g., remove "-ing", "-ed", "-tion").
>
> > 一种粗略的、基于规则的方法，通过截断词的后缀来近似词根。"studying" → "studi"、"studies" → "studi"。输出可能不是真正的词——只是一个词干。它通过应用一系列后缀去除规则（如移除"-ing"、"-ed"、"-tion"）工作。
>
> **(2) Lemmatization (词元化):**
>
> A dictionary-based method that converts words to their canonical dictionary form (lemma). "am/are/is" → "be", "better" → "good", "running" → "run". The output is ALWAYS a real word. It requires POS information — "meeting" could be a noun (lemma: "meeting") or verb (lemma: "meet").
>
> > 一种基于词典的方法，将词转换为规范的词典形式（词元）。"am/are/is" → "be"、"better" → "good"、"running" → "run"。输出始终是真正的词。它需要词性信息——"meeting"可以是名词（词元："meeting"）或动词（词元："meet"）。
>
> **🎯 Why:**
> **(1) Reduce vocabulary size (减少词表大小):**
>
> Without normalization, "run", "runs", "running", "ran" are four separate features. Normalization collapses them into one ("run"), reducing the vocabulary by ~40% and making models more robust against surface variation.
>
> > 没有规范化，"run"、"runs"、"running"、"ran"是四个独立特征。规范化将它们合并为一个（"run"），将词表减少约40%，使模型对表面变化更鲁棒。
>
> **💡 Intuition:**
> **(1) Chainsaw vs scalpel analogy (电锯 vs 手术刀类比):**
>
> Stemming is a chainsaw — fast, brutal, chops blindly. "university" → "univers", "universe" → "univers" (wrongly merged!). Lemmatization is a scalpel — precise, uses context, always produces valid words. But the scalpel is slower.
>
> > 词干提取是电锯——快速、粗暴、盲目切割。"university" → "univers"、"universe" → "univers"（错误地合并了！）。词元化是手术刀——精确、使用上下文、总是产生有效的词。但手术刀更慢。
>
> **⚖️ Compare:**
> **(1) Stemming vs Lemmatization:**
>
> | Feature     | Stemming               | Lemmatization          |
> | ----------- | ---------------------- | ---------------------- |
> | Speed       | Fast                   | Slower                 |
> | Accuracy    | Lower (may over-stem)  | Higher (context-aware) |
> | Output      | May not be a real word | Always a real word     |
> | Needs POS?  | No                     | Yes                    |
> | Example     | "better" → "better"    | "better" → "good"      |
> | Tool (NLTK) | PorterStemmer          | WordNetLemmatizer      |
>
> > | 特性        | 词干提取             | 词元化             |
> > | ----------- | -------------------- | ------------------ |
> > | 速度        | 快                   | 较慢               |
> > | 准确性      | 较低（可能过度切割） | 较高（上下文感知） |
> > | 输出        | 可能不是真词         | 总是真词           |
> > | 需要词性？  | 不需要               | 需要               |
> > | 示例        | "better" → "better"  | "better" → "good"  |
> > | 工具 (NLTK) | PorterStemmer        | WordNetLemmatizer  |
>
> **⚠️ Pitfall:**
> **(1) Stemming conflation errors (词干提取合并错误):**
>
> Porter stemmer maps both "university" and "universe" to "univers" — two completely different concepts merged into one! This is called "over-stemming" and can hurt classification accuracy when different concepts share similar suffixes.
>
> > Porter 词干提取器将"university"和"universe"都映射到"univers"——两个完全不同的概念被合并为一个！这叫做"过度词干化"，当不同概念共享相似后缀时会损害分类准确性。
>
> **(2) SpaCy has no built-in stemmer (SpaCy没有内置词干提取器):**
>
> SpaCy intentionally provides only lemmatization, not stemming. This is a quiz question! If you need stemming with spaCy, you must use NLTK's stemmers separately.
>
> > SpaCy有意只提供词元化，不提供词干提取。这是一个考试题！如果你需要用spaCy进行词干提取，必须单独使用NLTK的词干提取器。
>
> **(3) Poetry analysis should skip normalization (诗歌分析应跳过规范化):**
>
> In poetry, word forms carry meaning: tense, rhyme, rhythm all matter. "running" and "run" are rhythmically different. Normalizing destroys the poetic properties. This is why stemming/lemmatization should NOT be applied to poetry analysis.
>
> > 在诗歌中，词形携带含义：时态、韵律、节奏都很重要。"running"和"run"在节奏上不同。规范化会破坏诗歌特性。这就是为什么词干/词元化不应该应用于诗歌分析。
>
> **📝 Exam:**
> **(1) 对比题 (Comparison):**
>
> "When might you use lemmatizing over stemming?" → When accuracy is preferred more than speed, because lemmatization considers word meaning and POS context to produce valid dictionary words.
>
> > "什么时候你会选择词元化而非词干提取？" → 当准确性优先于速度时，因为词元化考虑词义和词性上下文来产生有效的词典词。
>
> **(2) 辨别题 (Identification):**
>
> "Pick the stemming action: (a) was→be (b) helped→help (c) troubled→trouble" → (b) helped→help is stemming (suffix removal). (a) is lemmatization (dictionary lookup). (c) is also lemmatization (morphological change).
>
> > "选择词干提取操作：(a) was→be (b) helped→help (c) troubled→trouble" → (b) helped→help 是词干提取（后缀移除）。(a) 是词元化（词典查找）。(c) 也是词元化（形态变化）。
>
> **(3) 判断题 (True/False):**
>
> "SpaCy does not provide a built-in function for Stemming." → True. SpaCy focuses on lemmatization and deliberately excludes stemming.
>
> > "SpaCy不提供内置的词干提取功能。" → 正确。SpaCy专注于词元化并有意排除词干提取。

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

> **📝 Notes:**
>
> **📌 What:**
> **(1) POS Tagging (词性标注):**
>
> Assigning grammatical categories (noun, verb, adjective, etc.) to each word in a sentence. Uses the Penn Treebank tag set (NN=noun, VB=verb, JJ=adjective, RB=adverb, etc.). POS is crucial because the same word can be different parts of speech: "run" can be a verb ("I run") or a noun ("a morning run").
>
> > 为句子中每个词分配语法类别（名词、动词、形容词等）。使用Penn Treebank标记集（NN=名词、VB=动词、JJ=形容词、RB=副词等）。词性很关键，因为同一个词可以是不同词性："run"可以是动词（"I run"）或名词（"a morning run"）。
>
> **(2) Named Entity Recognition — NER (命名实体识别):**
>
> Identifies and classifies proper nouns into predefined categories: PERSON (James Smith), LOCATION (United States), ORGANIZATION (Google), DATE (January 2024), MONEY ($500). NER builds on POS tagging — it needs to know a word is a noun before deciding if it's a named entity.
>
> > 识别专有名词并将其分类到预定义类别：PERSON（James Smith）、LOCATION（United States）、ORGANIZATION（Google）、DATE（January 2024）、MONEY（$500）。NER建立在词性标注之上——需要先知道一个词是名词才能决定它是否是命名实体。
>
> **🎯 Why:**
> **(1) POS enables disambiguation (词性实现消歧):**
>
> "I need to book a flight" — "book" is a VERB. "I read a book" — "book" is a NOUN. Without POS, a system can't tell the difference. POS tagging is the foundation for parsing, translation, and information extraction.
>
> > "我需要预订航班"——"book"是动词。"我读了一本书"——"book"是名词。没有词性标注，系统无法区分。词性标注是解析、翻译和信息提取的基础。
>
> **(2) NER powers real applications (NER驱动实际应用):**
>
> Search engines use NER to understand queries ("restaurants near Madison Square Garden" → LOCATION). Customer service bots extract product names, dates, and amounts from messages. Knowledge graphs are built by extracting entities and their relationships from text.
>
> > 搜索引擎使用NER理解查询（"restaurants near Madison Square Garden" → LOCATION）。客服机器人从消息中提取产品名称、日期和金额。知识图谱通过从文本中提取实体及其关系来构建。
>
> **⚖️ Compare:**
> **(1) POS Tagging vs NER:**
>
> | Feature     | POS Tagging         | NER                           |
> | ----------- | ------------------- | ----------------------------- |
> | Input       | Every word          | Only named entities           |
> | Labels      | NN, VB, JJ, RB, ... | PERSON, ORG, LOC, DATE, ...   |
> | Granularity | Single tokens       | Multi-word spans ("New York") |
> | Purpose     | Grammar analysis    | Information extraction        |
> | Dependency  | Independent         | Requires POS first            |
>
> > | 特性 | 词性标注            | NER                         |
> > | ---- | ------------------- | --------------------------- |
> > | 输入 | 每个词              | 仅命名实体                  |
> > | 标签 | NN, VB, JJ, RB, ... | PERSON, ORG, LOC, DATE, ... |
> > | 粒度 | 单个token           | 多词跨度（"New York"）      |
> > | 目的 | 语法分析            | 信息提取                    |
> > | 依赖 | 独立                | 需要先做词性标注            |
>
> **⚠️ Pitfall:**
> **(1) Context matters for POS (上下文对词性很重要):**
>
> "I saw her duck" — "duck" could be a NOUN (the animal) or a VERB (to lower oneself). POS taggers use surrounding words to decide, but they're not perfect. This connects directly to the ambiguity challenge from Week 1.
>
> > "I saw her duck"——"duck"可以是名词（鸭子）或动词（蹲下）。词性标注器使用周围词来决定，但它们不完美。这直接关联到第一周的歧义性挑战。
>
> **(2) NER needs capitalization (NER需要大小写):**
>
> If you lowercase text before NER, "apple" (fruit) and "Apple" (company) become indistinguishable. This is why NER should run BEFORE lowercasing in your preprocessing pipeline.
>
> > 如果在NER之前小写化文本，"apple"（水果）和"Apple"（公司）变得无法区分。这就是为什么NER应该在预处理流水线中在小写化之前运行。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Why do we need POS tagging?" → For syntactic/semantic analysis, sentence structure understanding, and improving accuracy of downstream NLP tasks like NER, parsing, and translation.
>
> > "为什么需要词性标注？" → 用于句法/语义分析、理解句子结构、提高下游NLP任务（如NER、解析、翻译）的准确性。
>
> **(2) 应用题 (Application):**
>
> "What entities would NER extract from 'James Smith lives in the United States'?" → PERSON: James Smith, GPE/LOCATION: United States.
>
> > "NER会从'James Smith lives in the United States'中提取什么实体？" → PERSON: James Smith, GPE/LOCATION: United States。

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
