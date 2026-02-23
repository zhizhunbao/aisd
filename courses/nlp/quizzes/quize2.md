# CST8507 NLP Quiz 2 — 文本预处理与正则 (Text Preprocessing & Regex)

Topic: Tokenization, Stemming, Lemmatization, Regex, Text Cleaning

---

## Question 1 (1 point)

The process of converting raw text into a sequence of units that a model can process.

Question 1 options:

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

---

## Question 2 (1 point)

For which of the following tasks we shouldn't do stemming/lemmatization?

Question 2 options:

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

---

## Question 3 (1 point)

SpaCy does not provide a built-in function for Stemming

Question 3 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> SpaCy's design philosophy favors dictionary-based Lemmatization, so it does not include built-in Stemming functionality. **Why True**: SpaCy considers Lemmatization more accurate and does not provide a Stemming API. Use NLTK's PorterStemmer or SnowballStemmer for stemming.
>
> > SpaCy 的设计理念偏向使用基于词典的 Lemmatization，因此没有内置 Stemming 功能。**为什么是 True**：SpaCy 认为 Lemmatization 更准确，不提供 Stemming API。如需 Stemming 可使用 NLTK 的 PorterStemmer 或 SnowballStemmer。
>
> **Key**: SpaCy provides lemmatization only, no built-in stemming. Use NLTK (PorterStemmer, SnowballStemmer) for stemming.

---

## Question 4 (1 point)

The following rgx will match all the words ended with a hyphen(-):

`rgx = r'\b\w+[-]\w+\b'`

Question 4 options:
A) True
B) False

> **Answer**: B
> **Explanation**:
> ⚠️ **Regex trap**: The regex `\b\w+[-]\w+\b` matches **compound words with a hyphen in the middle** (e.g., "high-tech", "well-known"), NOT words ending with a hyphen. **Why False**: The pattern requires `\w+` (one or more word characters) on both sides of the hyphen, so the hyphen must be in the middle, not at the end.
>
> > ⚠️ **正则陷阱**：该正则 `\b\w+[-]\w+\b` 匹配的是**中间含连字符的复合词**（如 "high-tech"、"well-known"），而非以连字符结尾的词。**为什么是 False**：模式要求连字符两侧都有 `\w+`（一个或多个单词字符），因此连字符必须在词中间，不可能在末尾。
>
> **Key**: `\b\w+[-]\w+\b` matches hyphenated compound words (e.g., "high-tech"), NOT words ending with a hyphen.

---

## Question 5 (1 point)

Text cleaning removes noise (like special characters, irrelevant symbols, and unnecessary spaces) and standardizes the text (e.g., converting to lowercase), is essential for improving the quality of the data and the performance of NLP models.

Question 5 options:
A) True
B) False

> **Answer**: A
> **Explanation**:
> Text cleaning reduces noise and feature space dimensionality by removing special characters and extra spaces, and standardizing case. **Why True**: Cleaned text is more normalized, reducing irrelevant variants the model must handle, thus improving performance.
>
> > 文本清洗通过去除特殊字符、多余空格并统一大小写，能有效降低噪声和特征空间维度。**为什么是 True**：清洗后的文本更规范，减少了模型需要处理的无关变体，从而提升模型性能。
>
> **Key**: Text cleaning removes noise (special chars, extra spaces) and standardizes text (lowercasing) → improved model performance.

---

## Question 6 (1 point)

Consider you have the following list that represents the USA's state names:

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

Question 6 options:

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

---

## Question 7 (1 point)

When might you use lemmatizing over stemming?

Question 7 options:

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

---

## Question 8 (1 point)

Pick the stemming action

Question 8 options:

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

---

## Question 9 (1 point)

Consider the provided code snippet:

```python
Text = 'I love NLP and I am read9y to study in 5 hours per Day'
regex = '[a-zA-Z]\w*d+'
print(re.findall(regex, Text))
```

The output is: `['and']`

Question 9 options:
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
