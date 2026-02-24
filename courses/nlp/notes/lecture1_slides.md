# Week 1: 课程概述与NLP简介 (Course Overview & Introduction to NLP)

> Source: `lecture_1_W26.pdf`
> Total slides: 55
> Instructor: Hala Own, Ph.D.

---

## 1. 课程信息 (Course Information)

![Page 1](lecture1_slides_pages/page_001.png)

**CST8507: Natural Language Processing** — Week 1: Course Overview & Introduction to NLP — 课程封面页：CST8507自然语言处理——第1周：课程概述与NLP简介

![Page 2](lecture1_slides_pages/page_002.png)

**Lesson Agenda:** — 课程议程

- ❑ Course CSI — 课程CSI
- ❑ What is Natural Language Processing (NLP)? — 什么是自然语言处理（NLP）？
- ❑ Applications of Natural Language Processing — 自然语言处理的应用
- ❑ Challenges in Natural Language Processing — 自然语言处理的挑战
- ❑ Approaches to NLP — NLP的方法
- ❑ NLP Libraries in Python — Python中的NLP库

### 1.1 联系方式 (Contact Information)

![Page 3](lecture1_slides_pages/page_003.png)

**Contact Information:** — 联系方式

- Office hours: TBA — 办公时间：待定
- Room#: WT315 — 办公室：WT315
- Email: ownh@algonquincollege.com — 邮箱：ownh@algonquincollege.com
- Expect email reply is within Two business days. Therefore, you need plan your emails accordingly — 预计邮件回复在两个工作日内。因此，请相应地规划你的邮件
- Include in your email: Your name, Course name and code, Section No. — 邮件中需包含：你的姓名、课程名称和代码、班级编号

### 1.2 评估分数分布 (Evaluation Breakdown)

![Page 4](lecture1_slides_pages/page_004.png)

**Evaluation Breakdown:** — 评估分数分布

| Assessment                    | Value         | CLRs          |
| ----------------------------- | ------------- | ------------- |
| Lab (4x 5%)                   | 20%           | 1, 2, 3, 4    |
| Assignment (Week 6)           | 10%           | 1, 2, 3       |
| Assignment 2 (Group Project)  | 20%           | 1, 2, 3, 4, 5 |
| **Total Practical**     | **50%** |               |
| Midterm (1 x 15%, Week 7)     | 15%           | 1, 2, 3       |
| Final Exam (1 x 25%, Week 15) | 25%           | 1, 2, 3, 4, 5 |
| Participation (5 out of 8)    | 10%           | 1, 2, 3, 4    |
| **Total Theory**        | **50%** |               |

### 1.3 实验与作业 (Labs & Assignments)

![Page 5](lecture1_slides_pages/page_005.png)

**Labs (5) 15%:** — 实验（5次）15%

- Labs must be demonstrated according to their scheduled weeks (stated in the CSI). — 实验必须按照计划周次进行演示（如CSI中所述）。
- Lab professor may ask you to do something else to verify that you have done the lab by yourself. — 实验教授可能会要求你做其他事情来验证你是否独立完成了实验。

![Page 6](lecture1_slides_pages/page_006.png)

**Assignments:** — 作业

- Assignment 1 (10%) — week 6: Individual work — 作业1（10%）——第6周：个人作业
- Assignment 2 (Project) 20% — 作业2（项目）20%
  - proposal Week #9 — 提案第9周
  - Submission (Code + Report + Presentation) Week #12 — 提交（代码+报告+演示）第12周
  - group working (max. two members) — 小组合作（最多两人）

### 1.4 考试 (Exams)

![Page 7](lecture1_slides_pages/page_007.png)

**Midterm Exam:** — 期中考试

- ❑ Week 7 Lecture — 第7周课堂
- ❑ 60 min — 60分钟
- ❑ Materials: Week 1 till Week 6 — 范围：第1周至第6周
- ❑ Weight: 15% — 权重：15%
- ❑ Closed Book, On paper — 闭卷，纸质
- Bring your own cheat sheet — 可自带小抄

![Page 8](lecture1_slides_pages/page_008.png)

**Final Exam (Theory):** — 期末考试（理论）

- ❑ Week 15 — 第15周
- ❑ Materials: Week 1 till Week 12 — 范围：第1周至第12周
- ❑ Weight: 25% — 权重：25%
- ❑ Closed Book, On paper — 闭卷，纸质
- Bring your own cheat sheet — 可自带小抄

### 1.5 课堂参与 (Participation)

![Page 9](lecture1_slides_pages/page_009.png)

**Participation (10%):** — 课堂参与（10%）

- ▪ Five best Participation will be counted into final score. Each will occupy 2% of final score — 最好的5次参与计入总分。每次占总分的2%
- ▪ The content in the Participation will be based on the hybrid which have been posted that week and the topic which has been covered that week — 参与内容基于当周发布的混合材料和当周涵盖的主题
- ▪ On Brightspace — 在Brightspace上
- ▪ Multiple Choice / True & False — 选择题/判断题
- ▪ Open book — 开卷
- ▪ one attempt — 一次机会
- ▪ Time: 10 min. — 时间：10分钟
- ▪ Participation will be proctored during the lecture. — 参与将在课堂上监考。
- ▪ Participation must be completed in person during the scheduled lecture time. Submitting a participation without attending the lecture will result in a grade of zero. — 参与必须在预定课堂时间内亲自完成。未出席课堂而提交参与将得零分。

### 1.6 课堂与实验规则 (Lecture & Lab Rules)

![Page 10](lecture1_slides_pages/page_010.png)

**Lecture Rules:** — 课堂规则

- Feel free to ask questions at anytime at all. Don't be shy, you're not the only one who will have questions. — 随时提问。不要害羞，你不是唯一有问题的人。
- Most topics covered in the lecture slides will be demonstrated. Feel free to follow along with the demonstrations with your own computers. — 课件中涵盖的大多数主题都会演示。欢迎用自己的电脑跟着做。
- Note-Taking — 记笔记

![Page 11](lecture1_slides_pages/page_011.png)

**Lab Rules:** — 实验规则

- ❑ Attendance is mandatory for the weeks that have lab activities assigned or require you to demo your work. — 有实验活动或需要演示作业的周次必须出勤。
- ❑ Working with others is encouraged. Explaining concepts and your way of thinking is allowed. Copying someone's answers is not. — 鼓励与他人合作。允许解释概念和思路。不允许抄袭答案。
- ❑ Come and go as you please, just ensure you have time to demo the lab to the instructor before the class ends. — 可以自由进出，但确保在课程结束前有时间向教师演示实验。

### 1.7 重要提醒 (Important Information)

![Page 12](lecture1_slides_pages/page_012.png)

**重要评分政策：** 实践和理论必须分别达到至少50%才能通过。

- You must get at least 50% in practical (labs, assignments) and at least 50% in theory (quizzes, midterm and final exam) to pass the course. Simply getting 50% overall without meeting the 50% min in each theory and practical is not sufficient to pass the course. — 实践（实验、作业）和理论（测验、期中和期末考试）必须分别达到至少50%才能通过课程。仅总分达到50%但未在理论和实践中分别达到50%不足以通过。

![Page 13](lecture1_slides_pages/page_013.png)

**Demo and submission policy:** — 演示与提交政策

- Labs, and Assignments must be demonstrated immediately after the due date and according to their scheduled weeks (as stated in the CSI). Missed Demo on the specified date may result in zero mark. — 实验和作业必须在截止日期后立即按计划周次演示（如CSI中所述）。错过指定日期的演示可能导致零分。
- Demos will be conducted during your lab session, during which your lab professor may ask you to perform additional tasks to ensure the authenticity of your work. Failure to answer questions about your work may result in a Zero mark. — 演示将在实验课期间进行，实验教授可能要求你执行额外任务以确保作业的真实性。无法回答关于你作业的问题可能导致零分。

![Page 14](lecture1_slides_pages/page_014.png)

**Submission deadlines:** — 提交截止日期

- The demo is not for evaluation — 演示不用于评分
- Demonstrating something that does not match what you submitted on Brightspace would result in a zero mark. — 演示内容与Brightspace上提交的不一致将导致零分。
- The official submission deadline for all labs and assignments is Friday night (11:59 PM). To accommodate all learners, I allow submissions until Sunday night (11:59 PM) without any penalties. — 所有实验和作业的官方截止日期为周五晚（11:59 PM）。为照顾所有学生，允许延至周日晚（11:59 PM）提交，无惩罚。
- No Extension or late submission for the Assignment 2 (Project). — 作业2（项目）不接受延期或迟交。

### 1.8 混合学习与工具 (Hybrid Work & Tools)

![Page 15](lecture1_slides_pages/page_015.png)

**Hybrid Work:** — 混合学习

- Each Week, Hybrid materials will be released — 每周将发布混合学习材料
- Part from your course — 部分来自你的课程
- Additional materials related to each week's topic — 与每周主题相关的额外材料

![Page 16](lecture1_slides_pages/page_016.png)

**Textbooks:** — 教材

- Jurafsky, D. & Martin, J. H. (2024) Speech and Language Processing (3rd ed. draft). https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf — 语音与语言处理（第3版草稿）
- Bird, S., Klein, E., & Loper, E. Natural Language Processing with Python. (O'Reilly 2009, website 2018), http://www.nltk.org/book/ — Python自然语言处理

![Page 17](lecture1_slides_pages/page_017.png)

**Tools:** — 工具

- Jupyter Notebook
- Google Colab

![Page 18](lecture1_slides_pages/page_018.png)

**Pre-Requisites:** — 先修要求

- ❑ Fundamental Knowledge of Machine Learning (CST8502) — 机器学习基础知识（CST8502）
- ❑ Fundamental Knowledge of Python — Python基础知识

---

## 2. 什么是自然语言处理 (What Is Natural Language Processing?)

### 2.1 知识表示 (Knowledge Representation)

![Page 20](lecture1_slides_pages/page_020.png)

**Knowledge Representation table:** — 知识表示表格

|                     | NLP "Knowledge" Structured                                                  | Unstructured                               |
| ------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| **Nature**    | Precise, Actionable                                                         | Ambiguous                                  |
| **Scope**     | Specific to the task                                                        | Lots and lots of it!                       |
| **Humans**    | can read them, but very slowly                                              | can't remember all, can't answer questions |
| **Computers** | can use quickly, answer questions, memory is not a problem, don't get tired | —                                         |


### 2.2 NLP的定义与动机 (NLP Definition & Motivations)

![Page 21](lecture1_slides_pages/page_021.png)

**What Is Natural Language Processing?** — 什么是自然语言处理？

- ❑ Subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language. — 语言学、计算机科学和人工智能的交叉子领域，关注计算机与人类语言之间的交互。
- ❑ How to program computers to process and analyze large amounts of natural language data. — 如何编程让计算机处理和分析大量自然语言数据。

![Page 22](lecture1_slides_pages/page_022.png)

**Motivations:** — 动机

- Enables computers to understand and process human language — 使计算机能够理解和处理人类语言
- Helping businesses to analyze customer feedback and improve customer service — 帮助企业分析客户反馈并改善客户服务
- Making it easier for individuals with disabilities to interact with computers and access information — 让残障人士更容易与计算机交互和获取信息
- Extract insights and make sense from data — 从数据中提取洞察并理解数据


### 2.3 AI与NLP的关系 (Interconnections Between AI, ML, DL, and NLP)

![Page 23](lecture1_slides_pages/page_023.png)

**Discussion Activity:** — 讨论活动

Ref: https://pub.towardsai.net/future-of-data-science-machine-learning-or-artificial-intelligence-6e9cbb93f547

![Page 24](lecture1_slides_pages/page_024.png)

**Interconnections Between AI, ML, DL, and NLP:** — AI/ML/DL/NLP的关联

Ref: Real-World NLP, 2021 by Manning Publications Co.


### 2.4 NLP的历史 (History of NLP)

![Page 25](lecture1_slides_pages/page_025.png)

**History of NLP:** — NLP历史

Ref: https://commtelnetworks.com/exploring-the-impact-of-natural-languageprocessing-on-cni-operations

![Page 26](lecture1_slides_pages/page_026.png)

**Turing's test for Artificial Intelligence:** — 图灵的人工智能测试

- Ability to understand and generate language ~ intelligence — 理解和生成语言的能力 ≈ 智能

Ref: https://botsociety.io/blog/2018/03/the-turing-test/


---

## 3. NLP应用 (Applications of Natural Language Processing)

### 3.1 NLU与NLG (NLU and NLG)

![Page 28](lecture1_slides_pages/page_028.png)

**NLP Applications: NLP = NLU + NLG:** — NLP应用：NLP = NLU + NLG


### 3.2 语音识别 (Speech Recognition)

![Page 29](lecture1_slides_pages/page_029.png)

**NLP Applications: Speech Recognition:** — NLP应用：语音识别

Ref: https://www.phonon.io/understanding-nlp-speech-recognition/

### 3.3 对话代理与聊天机器人 (Conversation Agents and Chatbots)

![Page 30](lecture1_slides_pages/page_030.png)

**NLP Applications: Conversation Agents and Chatbots:** — NLP应用：对话代理与聊天机器人

### 3.4 文本分类 (Text Classification)

![Page 31](lecture1_slides_pages/page_031.png)

**NLP Applications: Text Classification:** — NLP应用：文本分类

- spam / not spam — 垃圾邮件/非垃圾邮件
- priority level — 优先级
- category (primary / social / promotions / updates) — 分类（主要/社交/促销/更新）

### 3.5 情感分析 (Sentiment Analysis)

![Page 32](lecture1_slides_pages/page_032.png)

**NLP Applications: Sentiment Analysis:** — NLP应用：情感分析

Ref: text book

### 3.6 文本摘要 (Text Summarization)

![Page 33](lecture1_slides_pages/page_033.png)

**NLP Applications: Text Summarization:** — NLP应用：文本摘要

### 3.7 问答系统 (Question Answering)

![Page 34](lecture1_slides_pages/page_034.png)

**NLP Applications: Question Answering:** — NLP应用：问答系统

Ref: https://www.nlplanet.org/course-practical-nlp/02-practical-nlp-first-tasks/17-question-answering/

### 3.8 生成式AI (Generative AI)

![Page 35](lecture1_slides_pages/page_035.png)

**Generative AI: OpenAI's ChatGPT:** — 生成式AI：OpenAI的ChatGPT


---

## 4. NLP的挑战 (Challenges in Natural Language Processing)

![Page 37](lecture1_slides_pages/page_037.png)

**Challenges in NLP:** — NLP的挑战：歧义性、稀疏性、变异性、常识知识

### 4.1 歧义性 (Ambiguity)

![Page 38](lecture1_slides_pages/page_038.png)

**Language is Ambiguous: Words Have Many Meanings:** — 语言是歧义的：词有多种含义

- word "bass" can refer to a type of fish or a low-frequency sound. — 词"bass"可以指一种鱼或低频声音。
- The word "bank" can refer to a financial institution or the edge of a river. — 词"bank"可以指金融机构或河岸。

![Page 39](lecture1_slides_pages/page_039.png)

**Language is Ambiguous: Attachment Ambiguities:** — 语言是歧义的：附着歧义

- She saw the man with the telescope. — 她用望远镜看到了那个男人。/ 她看到了拿望远镜的那个男人。

![Page 40](lecture1_slides_pages/page_040.png)

**Language is Ambiguous: Coreference Ambiguities:** — 语言是歧义的：指代歧义

- My girlfriend and I met my lawyer for a drink but she became ill and had to leave. — 我和女朋友约了律师喝酒，但她生病了不得不离开。（"她"指谁？）


### 4.2 稀疏性 (Sparsity)

![Page 42](lecture1_slides_pages/page_042.png)

**Zipf's law: the long tail:** — 齐夫定律：长尾

- How many words occur once, twice, 100 times, 1000 times? — 有多少词出现过1次、2次、100次、1000次？
- A few words are very frequent — 少数词非常频繁
- Most words are very rare — 大多数词非常稀有
- English words, sorted by frequency (log-scale): w₁ = the, w₂ = to, …, w₅₃₄₆ = computer, ... — 英语单词按频率排序（对数尺度）

![Page 43](lecture1_slides_pages/page_043.png)

**Sparsity:** — 稀疏性

- Examples of rare/unique words: cornflakes, mathematician, fuzziness, jumbling, pseudo-rapporteur, lobby-ridden, perfunctorily, Lycketoft, UNCITRAL, H-0695, policyfor, Commissioneris
- > 1/3 of words occur only once
  >


### 4.3 变异性 (Variation)

![Page 45](lecture1_slides_pages/page_045.png)

**Variation within the same language:** — 同一语言内的变异

- Lexical variation — She gave the book to Tom vs. She gave Tom the book — 词汇变异
- Regional or Geographic Variation — 地域或地理变异
- Social Variation — 社会变异
- Stylistic Variation — 风格变异
- Generational Variation — 代际变异
- Variation between different languages — 不同语言之间的变异


### 4.4 常识知识 (Common Knowledge)

![Page 47](lecture1_slides_pages/page_047.png)

**Common knowledge:** — 常识知识

- It is the set of all facts that most humans are aware of — 大多数人类都知道的所有事实的集合
- ➢ man bit dog — 人咬狗（新闻！）
- ➢ dog bit man — 狗咬人（平常事）

![Page 48](lecture1_slides_pages/page_048.png)

**Other Challenges?** — 其他挑战？


---

## 5. NLP的方法 (Approaches to NLP)

![Page 50](lecture1_slides_pages/page_050.png)

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


---

## 6. Python中的NLP库 (NLP Libraries in Python)

![Page 52](lecture1_slides_pages/page_052.png)

**NLP Libraries in Python:** — Python中的NLP库

Ref: https://www.appventurez.com/blog/beginners-guide-to-natural-language-processing-nlp/


---

## 7. 总结与下周预告 (Summary & Next Week Preview)

![Page 53](lecture1_slides_pages/page_053.png)

**Summary:** — 总结

- ❑ Language to Knowledge — 从语言到知识
- ❑ Clearing the Confusion: AI vs. Machine Learning vs. Deep Learning Differences — 澄清混淆：AI vs 机器学习 vs 深度学习的区别
- ❑ Lots of applications… — 大量应用…
- ❑ It's quite difficult — 非常困难
- ❑ Varied, sparse, and lots of ambiguities — 变异、稀疏、大量歧义

![Page 54](lecture1_slides_pages/page_054.png)

**What's Next? — Text preprocessing and exploratory analysis:** — 下周预告——文本预处理和探索性分析

- Regular expression — 正则表达式
- Tokenization — 分词/词元化
- Stemming — 词干提取
- Removing stop words — 去除停用词
- Part Of Speech tagging (POS) — 词性标注
