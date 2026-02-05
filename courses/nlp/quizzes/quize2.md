Question 1 (1 point) 
 Saved
The process of converting raw text into a sequence of  units that a model can process.

Question 1 options:

Tokenization


Lemmatization


Stemming

Question 2 (1 point) 
 Saved
For which of the following tasks we shouldn’t do stemming/lemmatization?

Question 2 options:

Sentiment Analysis

Poetry Analysis

Text Classification
Question 3 (1 point) 
 Saved
SpaCy does not provide a built-in function for Stemming 

Question 3 options:
	True
	False
Question 4 (1 point) 
 Saved
The following rgx will match all the words ended with a hyphen(-)  :

rgx = r'\b\w+[-]\w+\b'

Question 4 options:
	True
	False
Question 5 (1 point) 
 Saved
Text cleaning removes noise (like special characters, irrelevant symbols, and unnecessary spaces) and standardizes the text (e.g., converting to lowercase),  is essential for improving the quality of the data and the performance of NLP models.

Question 5 options:
	True
	False
Question 6 (1 point) 
 Saved
Consider you have the following list that represents the USA's state names:

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


 which python expression that output Which state names start and end with a "vowel" character? 

Question 6 options:

[s for s in states if s[0].lower() in 'aeiou' and s[1] in 'aeiou']


[s for s in states if s[0].lower() in 'aeiou' and s[-1] in 'aeiou']


[s for s in states if s[1].lower() in 'aeiou' and s[-1] in 'aeiou']

Question 7 (1 point) 
 Saved
When might you use lemmatizing over stemming?

Question 7 options:

when accuracy is preferred more than speed


when non-dictionary words are allowed to appear in the output


when the data file contains a large number of simple words


when speed is preferred more than accuracy

Question 8 (1 point) 
 Saved
Pick the stemming action

Question 8 options:

was, am, is , are ----> be


helped, helps -----> help


troubled, troubling , trouble ------> trouble

Question 9 (1 point) 
 Saved
Consider the provided code snippet:

Text='I love NLP and I am read9y to study in 5 hours per Day'
regex='[a-zA-Z]\w*d+'

print(re.findall(regex,Text))

the output is : [and]

Question 9 options:
	True
	False

---

## Answer Key & Explanations

1. **Tokenization**
   - **解析**：分词（Tokenization）是将连续的文本序列切割成具有语义的最小单位（Token）的过程。
2. **Poetry Analysis**
   - **解析**：在诗歌分析中，词汇的原始形式、时态和语尾对于押韵和节奏至关重要，因此通常不进行词干提取或词元化。
3. **True**
   - **解析**：SpaCy 设计上更倾向于使用基于词典的 Lemmatization，因此没有内置 Stemming 功能。
4. **False**
   - **解析**：正则表达式 `r'\b\w+[-]\w+\b'` 匹配的是像 "high-tech" 这样中间带连字符的词，而不是以连字符结尾的词。
5. **True**
   - **解析**：数据清洗通过去除特殊字符和统一大小写，能有效降低特征空间的维度并提高模型性能。
6. **[s for s in states if s[0].lower() in 'aeiou' and s[-1] in 'aeiou']**
   - **解析**：`s[0]` 检查首字母，`s[-1]` 检查末尾字母，`in 'aeiou'` 确保其为元音。
7. **when accuracy is preferred more than speed**
   - **解析**：Lemmatization（词元化）由于涉及词形还原和词典查询，比简单的 Stemming 更准确但速度较慢。
8. **helped, helps -----> help**
   - **解析**：词干提取通过剥离常见的后缀（如 -ed, -s）来获取词干。
9. **False**
   - **解析**：该正则 `[a-zA-Z]\w*d+` 会匹配 "and"、"read"（来自 read9y）和 "stud"（来自 study），因此输出不唯一。
