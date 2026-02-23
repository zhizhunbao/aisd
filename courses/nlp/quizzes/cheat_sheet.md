# 📋 CST8507 NLP Cheat Sheet — 速查表

> 基于 Quiz 1–5 全部考点，按知识体系重组。标注 ⚠️ 为常见陷阱题。
>
> Reorganized by knowledge domain from Quiz 1–5. ⚠️ marks common trap questions.

---

## 1. NLP 基础概念 / NLP Fundamentals

### 1.1 领域层级关系 / Domain Hierarchy

```
AI ⊃ ML ⊃ DL
         ↑
NLP ⊂ AI (应用领域 / application domain)
```

| 层级 / Level | 定义 / Definition                                                                                       |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| **AI**       | 最广泛的范畴，包含基于规则和学习的系统 / Broadest scope, includes rule-based AND learning-based systems |
| **ML**       | AI 的实现路径，从数据中学习 / A way to achieve AI, learns from data                                     |
| **DL**       | ML 的分支，使用深度神经网络 / A branch of ML using deep neural networks                                 |
| **NLP**      | AI 的应用领域，专注语言任务 / AI application domain focused on language                                 |

> ⚠️ **陷阱**: "AI 仅依赖固定规则" → **False**（AI 包含学习方法）
> ⚠️ **陷阱**: "ML 与 AI 无关" → **False**（ML 是 AI 的核心子集）

### 1.2 NLP 的目标 / Goal of NLP

**理解 (Understand) + 解释 (Interpret) + 生成 (Generate)** 人类语言

### 1.3 图灵测试 / Turing Test (1950)

- 人类评估者通过文字与一人一机交互
- 若**无法区分**机器和人 → 机器通过测试 ✅

### 1.4 NLG vs NLU 区分 / NLG vs NLU

| 类型           | 任务示例               | 是否生成新文本 |
| -------------- | ---------------------- | -------------- |
| **NLG** (生成) | 翻译、写作、摘要       | ✅ 产出新文本  |
| **NLU** (理解) | **文本分类**、情感分析 | ❌ 归类/理解   |

> ⚠️ **考点**: Text Classification = **NLU**（不是 NLG）

### 1.5 Document vs Knowledge

| 概念                 | 说明                                     |
| -------------------- | ---------------------------------------- |
| **Document** (文档)  | 原始/半结构化文本（文章、报告）          |
| **Knowledge** (知识) | 结构化、解释过的信息（实体、关系、事实） |

---

## 2. NLP 核心挑战 / Key Challenges

### 2.1 语言变异性 / Variation — Zipf's Law

- 少数词极高频，大量词极低频 → **长尾分布**
- 模型难以充分学习低频词语义

### 2.2 情感分析难度 / Sentiment Analysis

- 人类语言含讽刺 (sarcasm)、反语 (irony)、隐喻 (metaphor)
- 需要**深层上下文理解**，非简单关键词匹配

### 2.3 文本摘要 / Text Summarization

- **必须**保持原文含义和连贯性 + 提取关键信息
  > ⚠️ **陷阱题**: "不需要保持整体含义" → **False**（前后矛盾的题干）

---

## 3. 文本预处理 / Text Preprocessing

### 3.1 处理流程 / Pipeline

```
Raw Text → Text Cleaning → Tokenization → Stemming/Lemmatization → Feature Extraction
```

### 3.2 核心操作对比 / Core Operations

| 操作                         | 定义                           | 特点                         |
| ---------------------------- | ------------------------------ | ---------------------------- |
| **Tokenization** (分词)      | 将文本切分为 token 序列        | NLP 管道**第一步**           |
| **Stemming** (词干提取)      | 规则剥离后缀 (-ed, -s, -ing)   | 快但不精确，可能产生非词典词 |
| **Lemmatization** (词元化)   | 词典查询还原原形               | 准确但慢，输出合法词典词     |
| **Text Cleaning** (文本清洗) | 去除特殊字符、空格、统一大小写 | 降噪 + 标准化                |

### 3.3 Stemming vs Lemmatization 速记

| 维度     | Stemming                 | Lemmatization         |
| -------- | ------------------------ | --------------------- |
| 方法     | 规则去后缀               | 词典查询              |
| 速度     | ⚡ 更快                  | 🐢 较慢               |
| 精度     | 较低（可能产出 "studi"） | ✅ 更高（输出词典词） |
| 选择场景 | 速度优先                 | **准确性优先**        |
| 典型示例 | helped → help ✅         | was/am/is → be ✅     |

> ⚠️ **考点**: "helped/helps → help" = **Stemming**（简单去后缀）
> ⚠️ **考点**: "was/am/is/are → be" = **Lemmatization**（需词典映射不规则动词）

### 3.4 何时不做 Stemming/Lemmatization？

- **诗歌分析 (Poetry Analysis)** → 词形变化对韵律/节奏至关重要

### 3.5 SpaCy vs NLTK

| 库        | Stemming                           | Lemmatization        |
| --------- | ---------------------------------- | -------------------- |
| **SpaCy** | ❌ 无内置                          | ✅ 有                |
| **NLTK**  | ✅ PorterStemmer / SnowballStemmer | ✅ WordNetLemmatizer |

---

## 4. 正则表达式 / Regular Expressions

### 4.1 常用模式

| 模式       | 含义                    |
| ---------- | ----------------------- |
| `\b`       | 单词边界                |
| `\w`       | 单词字符 `[a-zA-Z0-9_]` |
| `\w+`      | 一个或多个单词字符      |
| `[a-zA-Z]` | 任意字母                |
| `d+`       | 一个或多个字面字符 `d`  |
| `[-]`      | 字面连字符              |

### 4.2 易错正则

> ⚠️ `\b\w+[-]\w+\b` → 匹配**中间含连字符的复合词**（如 "high-tech"）
> **不是**以连字符结尾的词！因为 `-` 两侧都有 `\w+`

> ⚠️ `[a-zA-Z]\w*d+` → 匹配以字母开头、以 `d` 结尾的**任意子串**
> 结果不止 `['and']`，还包含其他匹配

---

## 5. 文本表示方法 / Text Representation

### 5.1 方法演进 / Evolution

```
One-Hot → BoW → TF-IDF → Word2Vec/GloVe → BERT/GPT (Contextual Embeddings)
     稀疏高维 ────────────→ 密集低维 ──────→ 上下文感知
```

### 5.2 Bag of Words (BoW) / 词袋模型

- **忽略词序**，每个词独立
- 只关注**词频** (word frequency)
  > ⚠️ "词序至关重要/词与上下文相关" → **False**

### 5.3 TF-IDF

**公式 / Formulas:**

$$TF(t,d) = \frac{f(t,d)}{|d|}$$

$$IDF(t) = \log\frac{N}{df(t)}$$

$$TF\text{-}IDF(t,d) = TF(t,d) \times IDF(t)$$

| 符号     | 含义                         |
| -------- | ---------------------------- |
| $f(t,d)$ | 词 $t$ 在文档 $d$ 中出现次数 |
| $\|d\|$  | 文档 $d$ 的总词数            |
| $N$      | 语料库总文档数               |
| $df(t)$  | 包含词 $t$ 的文档数          |

**TF-IDF 特点:**

- ✅ 适合搜索引擎等应用
- ❌ **高维稀疏**向量（维度 = 词汇表大小）
- ❌ **无语义理解**，无上下文，无词序
- ❌ 不适合深度学习任务

> ⚠️ **考点**: TF-IDF 的缺点 = "不考虑上下文和语义关系"

### 5.4 余弦相似度 / Cosine Similarity

$$\cos(\theta) = \frac{\vec{A} \cdot \vec{B}}{||\vec{A}|| \times ||\vec{B}||}$$

| 值   | 含义                    |
| ---- | ----------------------- |
| ≈ 1  | 方向一致 → **语义相似** |
| ≈ 0  | 正交 → 无关             |
| ≈ -1 | 方向相反 → 相反         |

**计算步骤:**

1. 点积: $\vec{A} \cdot \vec{B} = \sum a_i \times b_i$
2. 模长: $||\vec{A}|| = \sqrt{\sum a_i^2}$
3. 结果: $\cos(\theta) = \frac{\text{点积}}{||\vec{A}|| \times ||\vec{B}||}$

> **例题**: $w_1=(0.2,0.2,0.3,0.7)$, $w_2=(0.3,0.4,0.8,0.5)$
> 点积 = 0.73, $||w_1||=0.8124$, $||w_2||=1.0677$ → $\cos(\theta) ≈ 0.8421$

### 5.5 编辑距离 / Edit Distance (Levenshtein)

- 允许操作: 插入 (Insert)、删除 (Delete)、替换 (Substitute)
- "intention" → "execution" = **5 步**
- 用动态规划 (DP) 求解

### 5.6 CountVectorizer

- `CountVectorizer(ngram_range=(1,2))` → 同时生成 unigram **和** bigram
- 向量维度 = 词汇表中所有 n-gram 的总数

> ⚠️ 训练语料 `["I love NLP", "He love NLP", "good man"]` 的 (1,2)-gram 词汇表有 **8+ 个特征**，不是 7 个

---

## 6. 词嵌入 / Word Embeddings

### 6.1 核心思想 / Core Idea

将词映射到**低维密集向量空间**，语义相近的词向量距离近。

| 对比   | TF-IDF             | Word Embeddings     |
| ------ | ------------------ | ------------------- |
| 维度   | 高维（词汇表大小） | 低维（50–300）      |
| 稀疏性 | 稀疏               | 密集                |
| 语义   | ❌ 无              | ✅ 有               |
| 上下文 | ❌ 无              | ✅ 有（上下文学习） |

> ⚠️ **考点**: 1000 词汇表 → 嵌入维度应该是 1000？ → **False**（典型 50-300 维）

### 6.2 Word2Vec 两种架构

| 架构          | 输入 → 输出           | 适用场景       |
| ------------- | --------------------- | -------------- |
| **CBOW**      | 上下文词 → **中心词** | 高频词，大语料 |
| **Skip-gram** | **中心词** → 上下文词 | 低频词，小语料 |

> ⚠️ **易混题**: "Skip-gram 根据上下文确定中心词" → **False**（这是 CBOW 的功能！）

**Gensim Word2Vec 默认维度: `vector_size = 100`**

### 6.3 GloVe (Global Vectors)

- **全局 (Global)**: 利用整个语料库的共现矩阵
- **局部 (Local)**: 基于有限上下文窗口
- 结合两种视角的优势

### 6.4 词类比 / Word Analogy

$$e_{boy} - e_{girl} \approx e_{brother} - e_{sister}$$

> 同一语义关系（性别）在向量空间中保持一致

### 6.5 自监督学习 / Self-Supervised Learning

- 从数据本身生成训练信号，**无需人工标注**
- 例: CBOW 用上下文预测缺失词，Skip-gram 用中心词预测上下文

### 6.6 现代 NLP 与嵌入

> ⚠️ "大多数现代 NLP 不使用嵌入" → **False**
> 从 Word2Vec, GloVe 到 BERT, GPT，嵌入是**核心组件**

---

## 7. RNN 与语言模型 / RNN & Language Models

### 7.1 RNN 核心特征

**有状态计算 (Stateful Computation):**

$$h_t = f(W_h h_{t-1} + W_x x_t + b)$$

| 符号       | 含义                               |
| ---------- | ---------------------------------- |
| $h_t$      | 当前时间步隐藏状态（携带历史信息） |
| $h_{t-1}$  | 上一时间步隐藏状态                 |
| $x_t$      | 当前输入                           |
| $W_h, W_x$ | 权重矩阵                           |

### 7.2 RNN vs FFN

| 特性     | FFN (前馈网络)  | RNN (循环网络)     |
| -------- | --------------- | ------------------ |
| 序列处理 | ❌ 固定长度输入 | ✅ **变长**序列    |
| 时序依赖 | ❌ 无           | ✅ 通过 $h_t$ 传递 |
| 适用场景 | 静态输入        | 语言建模、机器翻译 |

### 7.3 梯度 / Gradient

$$\text{梯度} = \frac{\partial L}{\partial \theta}$$

- 通过 **BPTT** (Backpropagation Through Time) 计算
- 用于**梯度下降**更新参数: $\theta = \theta - \alpha \cdot \nabla L$

| 问题         | 原因                         | 后果               |
| ------------ | ---------------------------- | ------------------ |
| **梯度消失** | 长序列反向传播时梯度趋近于 0 | 无法学习长距离依赖 |
| **梯度爆炸** | 梯度趋近于 ∞                 | 训练不稳定         |

### 7.4 LSTM — 解决梯度消失

**三个门控机制 (Gating Mechanisms):**

| 门                       | 功能               |
| ------------------------ | ------------------ |
| **遗忘门 (Forget Gate)** | 决定丢弃哪些旧信息 |
| **输入门 (Input Gate)**  | 决定存储哪些新信息 |
| **输出门 (Output Gate)** | 决定输出哪些信息   |

> 门控允许梯度沿 cell state 长距离传播 → 解决梯度消失

> ⚠️ **干扰项排除**:
>
> - "更多隐藏层自动防止梯度消失" → ❌（关键是门控机制）
> - "LSTM 替换循环为前馈" → ❌（LSTM 仍是循环结构）
> - "LSTM 不需要反向传播" → ❌（仍需 BPTT）

### 7.5 N-gram 语言模型

$$P(w_n | w_{n-N+1}, ..., w_{n-1}) = \frac{Count(w_{n-N+1}...w_n)}{Count(w_{n-N+1}...w_{n-1})}$$

**Bigram 示例:**

$$P(\text{happy} | \text{feel}) = \frac{Count(\text{feel happy})}{Count(\text{feel})} = \frac{40}{100} = 0.4$$

> ⚠️ Count("happy") = 30 是**干扰信息**！条件概率只用共现次数 ÷ 条件词次数

**N-gram 局限:**

- ❌ **无语义理解**，无深层推理
- ❌ 固定窗口大小
- ❌ 数据稀疏性
- 只是基于统计频率的浅层预测

### 7.6 学习率 / Learning Rate ($\alpha$)

| 设置     | 效果                           |
| -------- | ------------------------------ |
| **过低** | 收敛**极慢**，可能陷入局部最优 |
| **过高** | 振荡/发散，跳过最优解          |
| **合适** | 稳定收敛到最优解               |

> ⚠️ "学习率过低 → 训练更快" → **False**（恰好相反，会更慢！）

### 7.7 训练数据来源

- 新闻文章 / 社交媒体 / 网页 → 提供多样化语言模式 ✅

---

## 8. Python 编程考点 / Python Snippets

### 8.1 字符串索引

| 表达式  | 含义             |
| ------- | ---------------- |
| `s[0]`  | **第一个**字符   |
| `s[1]`  | **第二个**字符   |
| `s[-1]` | **最后一个**字符 |

> 元音首尾检查: `s[0].lower() in 'aeiou' and s[-1].lower() in 'aeiou'`

---

## 9. 关键转折点 / Milestone

| 年份     | 里程碑                                                     |
| -------- | ---------------------------------------------------------- |
| **1950** | Turing Test (图灵测试)                                     |
| **1997** | LSTM (长短期记忆网络)                                      |
| **2013** | Word2Vec                                                   |
| **2014** | GloVe                                                      |
| **2017** | **Transformer** — "Attention is All You Need" ← NLP 转折点 |

---

## 10. 一页速记卡 / One-Page Flash Card

```
✅ Transformer = 2017 转折点 (self-attention)
✅ NLP 目标 = 理解 + 解释 + 生成
✅ 文本分类 = NLU (不是 NLG)
✅ Zipf's Law = 少数高频词 + 大量低频词
✅ 摘要必须保持连贯性
✅ Tokenization = 管道第一步
✅ SpaCy 无 Stemming; NLTK 有
✅ 诗歌分析不做 Stemming
✅ BoW 忽略词序
✅ TF-IDF = 高维稀疏、无语义
✅ IDF = log(N / df(t))
✅ cos ≈ 1 → 语义相似
✅ 嵌入维度 50-300 (不等于词汇表大小)
✅ Word2Vec 默认 100 维
✅ CBOW: 上下文→中心词;  Skip-gram: 中心词→上下文
✅ GloVe = 全局共现 + 局部窗口
✅ 自监督 = 无需手工标注
✅ RNN 有状态计算 (h_t 跨时间步)
✅ LSTM 三门: 遗忘门、输入门、输出门
✅ N-gram = 统计浅层，无语义推理
✅ 条件概率 = Count(AB) / Count(A)  (ignore Count(B))
✅ 学习率过低 → 慢 (不是快!)
```
