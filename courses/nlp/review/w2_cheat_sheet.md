# W2: Text Preprocessing (文本预处理)

## 1. Definitions (定义)

### Core Preprocessing Terms (核心预处理术语)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Tokenization (分词) | NLP 流水线的第一步：把文本切成离散的 token (词/符号) | "I love NLP!" → ["I", "love", "NLP", "!"] |
| Stop Words (停用词) | 高频但语义贡献低的词，通常在分析前移除以减少噪声 | "the", "is", "at", "a" → 移除后只留实义词 |
| Stemming (词干提取) | 用规则暴力砍词尾得到词根，速度快但可能产生非真词 | "studies" → "studi"; "running" → "run" |
| Lemmatization (词元化) | 用词典 + 词性信息还原到标准词形，输出一定是真实的词 | "studies" → "study"; "was/am/is" → "be"; "better" → "good" |
| Lemma (词元) | 词元化的输出结果，是一个词的标准/词典形式 | "running" 的 lemma 是 "run" |
| POS Tagging (词性标注) | 给每个 token 标上语法类别标签 (名词/动词/形容词等) | "The(DT) quick(JJ) fox(NN) runs(VBZ)" |
| NER (命名实体识别) | 从文本中找出并分类专有名词 (人名/地名/组织/日期/货币) | "James lives in Ottawa" → James=PERSON, Ottawa=GPE |
| Normalization (规范化) | 把 token 转换成统一的基本形式，消除屈折变化 (包括 Stemming 和 Lemmatization) | "Running", "ran", "runs" → 统一成 "run" |
| Noise Removal (噪声移除) | 删除对分析无用的元素：数字、标点、停用词、HTML标签、URL | `<br>Visit http://... ` → 移除后只留正文文字 |
| Corpus (语料库) | 用于 NLP 训练/分析的大规模文本集合 | IMDb影评数据集、Twitter推文数据、新闻语料 |

### Regular Expression (正则表达式)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Regex / RegExp (正则表达式) | 用特殊语法描述文本模式的工具，可做匹配、搜索、替换 | `r'\d+'` 匹配一个或多个数字 |
| Metacharacter (元字符) | 正则中有特殊含义的字符 (`.` `*` `+` `?` `^` `$` `[]` `()`) | `.` = 任意字符; `*` = 0次或多次; `+` = 1次或多次 |
| Character Class (字符类) | 预定义的字符集快捷写法：`\d`=数字, `\w`=字母, `\s`=空白 | `\d` matches '5'; `\D` (大写取反) matches 'a' |
| Capture Group (捕获组) | 用圆括号 `()` 标记正则中想提取的部分 | `r'I feel (.*)'` 匹配 "I feel sad" → 捕获 "sad" |
| Anchor (锚定) | `^` = 字符串开头, `$` = 字符串结尾 (限定匹配位置) | `^Hello` 只匹配开头的 "Hello"; `end$` 只匹配结尾 |

### Python Regex Functions (Python 正则函数)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| `re.match()` (开头匹配) | 只在字符串**开头**查找匹配，不匹配返回 None | `re.match(r'\d+', 'abc123')` → None (开头不是数字) |
| `re.search()` (任意位置搜索) | 在字符串**任意位置**查找第一个匹配 | `re.search(r'\d+', 'abc123')` → Match '123' |
| `re.findall()` (查找全部) | 返回字符串中**所有**不重叠匹配的列表 | `re.findall(r'\d+', 'a1b2c3')` → ['1','2','3'] |
| `re.sub()` (替换) | 用替换文本替换所有匹配的部分 | `re.sub(r'\d+', '#', 'a1b2')` → 'a#b#' |
| `re.split()` (分割) | 按正则模式切分字符串 | `re.split(r'\d', 'ab1bc4cd')` → ['ab','bc','cd'] |

### Preprocessing Pipeline (预处理流水线顺序)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Step ① Tokenization (分词) | 第一步：把原始文本切分成 token 列表 | "He's running!" → ["He","'s","running","!"] |
| Step ② Noise Removal (去噪) | 第二步：移除标点/数字/停用词/HTML/URL 等噪声 | ["He","'s","running","!"] → ["running"] |
| Step ③ Normalization (规范化) | 第三步：Stemming 或 Lemmatization 还原词形 | ["running"] → ["run"] |

### Sentiment Lexicon (情感词典)

| Term (术语) | Definition (定义) | Example (示例) |
|------|-----------|---------|
| Sentiment Lexicon (情感词典) | 预先定义的正面/负面情感词列表，用于规则情感分析 | 正面: good, great, amazing; 负面: bad, terrible, boring |
| Rule-based Sentiment (规则情感分析) | 统计文本中正/负情感词的数量来判断情感极性，简单但不理解上下文 | pos_count=5, neg_count=2 → 判断为 Positive |
| ELIZA (聊天机器人) | 1966年的经典规则聊天机器人，用正则匹配 + 代词替换模拟心理医生 | 输入 "I feel sad" → 回复 "Why do you feel sad?" |

## 2. Comparisons (对比)

### Stemming vs Lemmatization (词干提取 vs 词元化)

| Dimension (维度) | Stemming (词干提取) | Lemmatization (词元化) | Example (示例) |
|-----------|---------------------|----------------------|---------|
| Method (方法) | 规则砍词尾 (Rule-based suffix stripping) | 词典查找 + 词性分析 (Dictionary lookup + POS) | Porter 用规则; WordNet 用词典 |
| Speed (速度) | ⚡ 更快 (无需查词典) | 🐢 更慢 (需要加载词典和做POS) | 大数据集优先用 Stemming |
| Accuracy (精度) | ❌ 低 — 可能产生非真词 | ✅ 高 — 始终输出真实的词 | helped→"help"✅; studies→"studi"❌ |
| Trade-off (权衡) | 速度优先场景 (Speed priority) | 精度优先场景 (Accuracy priority) | 搜索引擎→Stem; 问答系统→Lem |
| Output (输出) | 词干 (stem)，可能不是真词 | 词元 (lemma)，一定是真词 | "better" → Stem:"better"; Lem:"good" |

### SpaCy vs NLTK (工具库对比)

| Feature (功能) | SpaCy | NLTK | Example (示例) |
|---------|-------|------|---------|
| Stemming (词干提取) | ❌ 不支持 | ✅ Porter/Snowball/Lancaster 三种 | NLTK: `PorterStemmer().stem("studies")` → "studi" |
| Lemmatization (词元化) | ✅ 内置 (`token.lemma_`) | ✅ WordNetLemmatizer | SpaCy: 一行搞定; NLTK: 需手动指定词性 |
| 设计理念 | 工业级管道 (Pipeline) | 教学研究工具箱 (Toolkit) | SpaCy 一次调用做完所有; NLTK 每步手动调 |

### NLTK 3 Stemmers (三种词干提取器对比)

| Stemmer (提取器) | Aggressiveness (激进程度) | Use Case (使用场景) | Example (示例) |
|---------|---------------|---------|---------|
| Porter Stemmer | 最温和 (Least aggressive) | 最常用，通用场景 | "generously" → "generous" |
| Snowball Stemmer | 中等 (Improved Porter) | 需要多语言支持时 | 支持英/法/德/西等 |
| Lancaster Stemmer | 最激进 (Most aggressive) | 需要最大化归并时 (可能过度切割) | "generously" → "gener" |

### POS Tags & NER Entities (词性标签与命名实体)

| POS Tag (词性标签) | Meaning (含义) | NER Entity (实体类型) | Example (示例) |
|---------|---------|------------|---------|
| NN | Noun 名词 | PERSON (人名) | "James" = PERSON |
| VB | Verb 动词 | LOCATION/GPE (地点) | "Ottawa" = GPE |
| JJ | Adjective 形容词 | ORGANIZATION (组织) | "Google" = ORG |
| RB | Adverb 副词 | DATE (日期) | "January 2026" = DATE |
| DT | Determiner 限定词 | MONEY (货币) | "$100" = MONEY |
| PRP | Pronoun 代词 | — | — |

### When NOT to Stem/Lemmatize (何时不用规范化)

| Scenario (场景) | Reason (原因) | Example (示例) |
|----------|--------|---------|
| Poetry Analysis (诗歌分析) | 韵律和节奏是分析核心，不能改词形 | "running" 的韵脚在分析中很重要 |
| Social Media (社交媒体) | 充满俚语、缩写、故意拼写错误，规范化会丢信息 | "luv", "gr8", "thx" → stemmer 无法处理 |
| Speed-critical (极限速度场景) | 规范化增加计算开销，某些实时场景可跳过 | 实时搜索建议可跳过 Lemmatization |

## 3. Formulas (公式)

_No formulas this week._

## 4. Practical / Lab (实战结论)

### 🔑 Regex Key Distinctions (正则关键区别)

| Distinction (区别) | Detail (详情) | Example (示例) |
|----------|------------|---------|
| `re.match` vs `re.search` | match = 仅匹配字符串开头; search = 匹配任意位置 (**考试常考!**) | `re.match(r'\d+', 'abc123')` → None; `re.search` → '123' |
| `re.findall` vs `re.search` | findall = 返回所有匹配的列表; search = 仅第一个 Match 对象 | `re.findall(r'\d+', 'a1b2')` → ['1','2'] |
| `\d` vs `\w` vs `\s` | 数字 / 字母数字 / 空白; 大写取反 `\D \W \S` | `\d`='5'; `\w`='a'; `\s`=' '; `\D`='a' |
| `*` vs `+` vs `?` | 0次以上 / 1次以上 / 0或1次 (量词区别) | `a*` matches ''; `a+` 需要至少一个 'a'; `colou?r` = color/colour |

### 📊 Lab 2 Part 1 结论: ELIZA Chatbot (ELIZA 聊天机器人)

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| ELIZA 用正则捕获组 (Capture Group) 提取用户关键词 | 模式 `r'i feel (.*)'` 捕获情感描述 → 反射回复 | 输入 "I feel sad" → 捕获 "sad" → "Why do you feel sad?" |
| 代词替换 (Pronoun Swap) 是 ELIZA 的核心技巧 | 把 "I/my/me" 换成 "you/your/you" 产生自然回复 | "I feel my life is..." → "Why do you feel your life is..." |
| 用占位符 (Placeholder) 避免替换冲突 | 直接替换 I→you→I 会死循环；先换占位符再统一替换 | I→\_\_YOU\_\_, you→\_\_I\_\_ → 最后统一替换为真实代词 |
| 无匹配时用默认回复 (Default Response) | 兜底策略：无规则命中时随机选一条通用回复 | "Please go on." / "Tell me more." / "Can you elaborate?" |

### 📊 Lab 2 Part 2 结论: Rule-based Sentiment (规则情感分析)

| Finding (发现) | Detail (详情) | Example (示例) |
|---------|--------|---------|
| 规则法准确率有限 (~60-65%) | 只数正/负面词的数量，不理解语境和否定 | "not bad" → neg=1, pos=0 → 判断错误 (实际是正面) |
| 预处理步骤：小写→去HTML→去URL→去标点→去多余空格 | 用正则链式清洗：`re.sub(r'<[^>]+>', ' ', text)` 等 | `<br>Great movie!` → `great movie` |
| neutral 判断 = 系统局限 | pos_count == neg_count 时输出 neutral，但数据集没有 neutral 标签 → 算错误 | pos=3, neg=3 → "neutral" → 实际是 pos → 错误 |
| 情感词典 (Lexicon) 越大越好但仍有限 | 正面50词+负面50词 → 覆盖率不足，很多情感表达无法捕获 | "masterpiece" 在词典里 → 捕获; "a must-see" → 遗漏 |

### ⚠️ W2 考试陷阱 (Exam Traps)

| Trap (陷阱) | Correct Answer (正确答案) | Example (示例) |
|------|----------------|---------|
| re.match 能匹配任意位置? | ❌ match 只匹配开头! search 才是任意位置 | `re.match(r'\d+', 'abc123')` → None，不是 '123' |
| SpaCy 可以做 Stemming? | ❌ SpaCy 只有 Lemmatization，没有 Stemming; NLTK 才两个都有 | SpaCy: `token.lemma_`; 无 `stem()` 方法 |
| 预处理顺序随便排? | ❌ 必须 Tokenize → Noise Removal → Normalize，顺序错会影响结果 | 先 Stem 再 Tokenize = 无法正确切分 |
| 诗歌分析应该做 Lemmatization? | ❌ 诗歌分析不应做 Stemming/Lemmatization，因为韵律和词形是分析重点 | "running" 的韵脚信息会被 Lemmatization 丢掉 |
| 规则情感分析能处理否定? | ❌ "not bad" 会被误判为负面，规则法不理解否定词的语义翻转 | "not bad" → neg=1 → Negative (实际是正面评价) |
