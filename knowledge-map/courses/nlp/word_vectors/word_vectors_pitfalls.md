---
topic: word_vectors
dimension: pitfalls
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Paper: Mikolov et al., 'Distributed Representations of Words and Phrases', NeurIPS 2013 — https://arxiv.org/abs/1310.4546"
  - "📖 Paper: Bolukbasi et al., 'Man is to Computer Programmer as Woman is to Homemaker?', NeurIPS 2016 — https://arxiv.org/abs/1607.06520"
  - "📚 Book: Jurafsky & Martin, 《Speech and Language Processing》 3rd Ed., Ch.6 — file:///C:/Users/40270/Desktop/workspace/aisd/textbooks/jurafsky_slp3_jan2026.pdf"
  - "📖 Docs: Gensim FAQ — https://radimrehurek.com/gensim/auto_examples/index.html"
  - "🧪 经验: 词向量训练与使用中的常见陷阱"
expiry: 6m
status: current
---

# Word Vectors 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: "词类比总是不准，Word2Vec 是不是有 bug？"

**痛点类别：** 概念理解偏差——对词类比的预期过高

**场景：** 学生学完 Word2Vec 后尝试词类比 "king"-"man"+"woman"=?，发现很多类比给不出期望答案

**症状：** "doctor"-"man"+"woman" 给出 "nurse" 而非 "doctor"（预期不变）；某些类比完全离谱

**根因：** 词类比是 Word2Vec 的一个有趣性质，但不是可靠的推理工具。词向量学的是统计共现，不是逻辑关系。语料中的偏见（"doctor"更常和男性上下文共现）会直接反映在向量空间中。此外，类比只在某些语义关系上效果好（性别、首都-国家），在其他关系上很差

**解法：**

❌ 错误做法 — 把词类比当作"计算器"，认为它应该总是给出正确答案

```python
# 认为这应该总是给出 "queen"
result = model.most_similar(positive=["king", "woman"], negative=["man"])
# 错误：词类比不是100%准确的
```

✅ 正确做法 — 理解词类比是统计倾向，不是逻辑推理；关注偏见问题

```python
# 词类比是评估词向量质量的工具，不是推理工具
result = model.most_similar(positive=["king", "woman"], negative=["man"], topn=5)
# 看 top-5 而非只看 top-1，理解这是概率排序

# 偏见检测
bias_result = model.most_similar(positive=["doctor", "woman"], negative=["man"])
print("Bias check:", bias_result)  # 如果出现 "nurse"，说明存在性别偏见
```

**教训：** Word2Vec 反映的是语料中的统计规律，包括偏见。类比任务用来评估和理解词向量，不能当作可靠的推理工具

> 📖 Paper: Bolukbasi et al., [Man is to Computer Programmer as Woman is to Homemaker?](https://arxiv.org/abs/1607.06520), NeurIPS 2016
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.11

---

## 坑 2: "为什么加载预训练词向量后，有些词找不到？"

**痛点类别：** 代码调试——OOV (Out-of-Vocabulary) 问题

**场景：** 加载 GloVe/Word2Vec 预训练词向量后，尝试查询某些词（如专业术语、拼写变体、新造词）报 KeyError

**症状：** `KeyError: "word 'COVID-19' not in vocabulary"` 或类似错误

**根因：** 预训练词向量的词表在训练时就固定了（通常 40 万~300 万个词）。训练语料中未出现的词（或出现次数低于 min_count）不会有向量。这是静态词向量的根本限制

**解法：**

❌ 错误做法 — 不检查直接访问，崩了就跳过

```python
# 直接访问可能报错
vec = model.wv["COVID-19"]  # KeyError!
```

✅ 正确做法 — 先检查是否在词表中，或用 FastText 处理 OOV

```python
# 方法1: 先检查 / Check first
word = "COVID-19"
if word in model.wv:
    vec = model.wv[word]
else:
    # 回退策略: 用零向量 / 随机向量 / UNK 向量
    vec = np.zeros(model.vector_size)
    # 或: vec = model.wv["unk"] if "unk" in model.wv else np.zeros(...)

# 方法2: 用 FastText (能处理 OOV)
import gensim.downloader as api
ft_model = api.load("fasttext-wiki-news-subwords-300")
# FastText 能为未见过的词合成向量 (通过子词 n-gram)
vec = ft_model["COVID-19"]  # 不会报错! 从子词组合得到

# 方法3: 文本预处理，统一格式
word = word.lower().replace("-", "")  # "covid19"
```

**教训：** 使用预训练词向量必须有 OOV 兜底策略。如果 OOV 率高，优先用 FastText（子词 n-gram）或 BPE 分词方案

> 📖 Paper: Bojanowski et al., [FastText (2017)](https://arxiv.org/abs/1607.04606), §1
> 📖 Docs: [Gensim KeyedVectors](https://radimrehurek.com/gensim/models/keyedvectors.html)

---

## 坑 3: "训练出来的词向量质量很差，相似词不相似"

**痛点类别：** 代码调试——训练超参数设置不当

**场景：** 在自己的语料上训练 Word2Vec，发现 most_similar 结果很差，语义相关的词不在 top-10

**症状：** `most_similar("python")` 返回完全不相关的词，或所有词的相似度都差不多

**根因：** 词向量质量取决于三个因素：① 语料大小（最重要）②：超参数设置 ③ 语料质量。最常见的原因是语料太小（需要数百万句子以上），其次是 min_count 设太高导致有效词表太小

**解法：**

❌ 错误做法 — 在几千句的小语料上训练，期望得到好效果

```python
# 语料太小 = 垃圾词向量
tiny_corpus = [["the", "cat", "sat"]] * 100  # 只有100个样本
model = Word2Vec(tiny_corpus, vector_size=300, min_count=1)
# 300维 vs 100个样本 = 严重过拟合/欠拟合
```

✅ 正确做法 — 用足够大的语料 + 合理的超参数

```python
# 超参数诊断清单 / Hyperparameter checklist
model = Word2Vec(
    sentences=large_corpus,     # ① 至少百万句子 / At least millions of sentences
    vector_size=100,            # ② 维度不要比语料大小"大太多" / Match dim to corpus size
    window=5,                   # ③ 小窗口=语法关系, 大窗口=语义关系 / Window affects semantics
    min_count=5,                # ④ 低频词(<5次)噪声太多,过滤掉 / Filter rare words
    sg=1,                       # ⑤ Skip-gram 对小语料和低频词更好 / Skip-gram for small corpus
    negative=5,                 # ⑥ 小语料用 k=15, 大语料用 k=5 / Adjust neg samples
    epochs=15,                  # ⑦ 小语料多跑几轮 / More epochs for small corpus
)

# 如果语料确实小，直接用预训练向量 + fine-tune，不要从零训练!
# If corpus is small, use pre-trained + fine-tune instead!
```

**教训：** 词向量是数据驱动的，数据量是第一优先级。语料太小就直接用预训练向量，不要从零训练

> 📖 Paper: Mikolov et al., [Word2Vec (2013)](https://arxiv.org/abs/1301.3781), §4
> 📖 Docs: [Gensim Word2Vec Tips](https://radimrehurek.com/gensim/models/word2vec.html)

---

## 坑 4: "Word2Vec 和 GloVe 到底应该用哪个？"

**痛点类别：** 概念理解偏差——对两种方法的区别理解不深

**场景：** 学习完 Word2Vec 和 GloVe 后，不确定在实际项目中该用哪个

**症状：** 选择困难，或任何场景都用同一个方法

**根因：** 两者在大多数任务上效果非常接近（Levy et al. 2015 实验证明），真正影响效果的是语料大小、预处理方式、超参数，而不是算法本身。但两者在概念层面确实有区别：Word2Vec 是局部预测模型，GloVe 是全局统计模型

**解法：**

❌ 错误做法 — 纠结算法选择，忽视数据和超参数

```python
# 花了3天对比 Word2Vec vs GloVe，最终差异 < 1%
# 实际上应该把时间花在数据清洗和超参数调优上
```

✅ 正确做法 — 先用预训练向量快速验证，再根据任务需求选择

```python
# 实用决策树:
# 1. 有预训练向量能用吗? → 是 → 直接用 (GloVe-300d 或 FastText)
# 2. 需要处理 OOV? → 是 → 用 FastText
# 3. 需要上下文感知? → 是 → 用 BERT/GPT，不用静态词向量
# 4. 自定义语料训练? → Word2Vec (Gensim，最方便)

import gensim.downloader as api

# 推荐: 直接用预训练 GloVe-300d
model = api.load("glove-wiki-gigaword-300")  # 最常用的公开预训练词向量
```

**教训：** 不要在算法选择上过度纠结，数据质量和超参数对效果的影响远大于算法差异。实际项目优先用预训练向量

> 📖 Paper: Levy et al., [Improving Distributional Similarity with Lessons Learned from Word Embeddings](https://aclanthology.org/Q15-1016/), TACL 2015

---

## 坑 5: "为什么我的词向量有性别/种族偏见？"

**痛点类别：** 概念理解偏差——不理解词向量会继承语料偏见

**场景：** 用词向量发现 "computer programmer" 和 "man" 更接近，"homemaker" 和 "woman" 更接近

**症状：** 词向量在下游任务（如简历筛选）中放大了社会偏见

**根因：** 词向量完全从数据中学习——如果训练语料中 "doctor" 更常出现在男性语境中，词向量就会编码这种统计偏差。这不是算法 bug，是数据反映的社会现实

**解法：**

❌ 错误做法 — 忽视偏见，直接用于敏感场景

```python
# 直接用到招聘系统中，不检查偏见
similarity_score = model.similarity(resume_vector, "programmer")
# 可能系统性地歧视某些群体
```

✅ 正确做法 — 检测偏见 + 使用去偏方法

```python
# 检测偏见 / Detect bias
he_words = model.most_similar(positive=["computer", "he"], negative=["she"], topn=5)
she_words = model.most_similar(positive=["computer", "she"], negative=["he"], topn=5)
print("He-biased:", he_words)
print("She-biased:", she_words)

# 去偏方法 (Bolukbasi et al. 2016): 投影去除性别方向
# Debiasing: project out the gender direction
# 1. 找到性别方向: he-she, man-woman 的平均
# 2. 把所有词向量在该方向上的分量去掉
# 简化示例:
gender_direction = model["he"] - model["she"]
# 对每个词: w_debiased = w - (w·g / g·g) * g
```

**教训：** 词向量是一面镜子，反映数据中的偏见。在敏感应用中必须进行偏见审计和去偏处理

> 📖 Paper: Bolukbasi et al., [Man is to Computer Programmer as Woman is to Homemaker?](https://arxiv.org/abs/1607.06520), NeurIPS 2016
> 📚 Book: Jurafsky & Martin, [《SLP3》](../../../textbooks/jurafsky_slp3_jan2026.pdf), Ch.6 §6.11

---

## 坑 6: "为什么同一个词在不同语境中是完全不同的意思？"

**痛点类别：** 概念理解偏差——混淆了静态嵌入和上下文嵌入

**场景：** 用 Word2Vec 向量做词义消歧 (WSD) 或一词多义相关任务时效果极差

**症状：** "bank"（银行）和 "bank"（河岸）的向量完全相同，无法区分

**根因：** Word2Vec/GloVe/FastText 都是静态嵌入——每个词有且只有一个固定向量。这个向量是所有上下文的"平均"，无法表达一词多义

**解法：**

❌ 错误做法 — 试图用静态词向量做词义消歧

```python
# "bank" 永远只有一个向量，无法区分语义
bank_vec = model.wv["bank"]
# 这个向量混合了"银行"和"河岸"的语义
```

✅ 正确做法 — 使用上下文嵌入 (ELMo / BERT)

```python
# ELMo / BERT 给出上下文相关的表示
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# "bank" 在不同上下文中获得不同向量
s1 = "I went to the bank to deposit money"
s2 = "The river bank was covered with flowers"

for s in [s1, s2]:
    inputs = tokenizer(s, return_tensors="pt")
    outputs = model(**inputs)
    # bank 在两个句子中的向量不同!
    bank_idx = tokenizer.encode("bank", add_special_tokens=False)[0]
    # 找到 "bank" 在 token 序列中的位置并提取其向量
```

**教训：** 认清静态嵌入的能力边界——一词一向量。需要区分同一个词的不同含义时，必须使用上下文嵌入

> 📖 Paper: Peters et al., [ELMo (2018)](https://arxiv.org/abs/1802.05365), §1

---

## 超级避坑指南

### 学习避坑

1. [ ] **别把词类比当推理工具** → 它是评估向量质量的手段，不是可靠的逻辑运算
2. [ ] **别忽视 One-Hot 的存在** → 理解 One-Hot 的缺陷是理解词向量价值的前提
3. [ ] **别混淆 "嵌入" 和 "编码"** → Embedding 是可学习的参数，Encoding 是确定性函数
4. [ ] **别遗忘分布假说** → Word2Vec/GloVe 的全部理论基础就是 "上下文定义语义"
5. [ ] **先用预训练再考虑自己训练** → 99% 的场景不需要从零训练词向量

### 作业/项目避坑

1. [ ] **先确认词表覆盖率** → 检查你的数据中有多少词不在预训练词表里
2. [ ] **处理 OOV 有方案** → 零向量 / 随机初始化 / FastText / 子词分词
3. [ ] **文本预处理要统一** → 大小写、标点、特殊字符的处理必须和预训练模型一致
4. [ ] **别用 Word2Vec 做文档级表示** → 简单求平均损失太大，用 Doc2Vec 或 Sentence-BERT
5. [ ] **保存和加载方式要正确** → `model.save()` 保存完整模型，`model.wv.save()` 只保存向量

### 考试/答辩避坑

1. [ ] **被问"为什么用词向量而不是 One-Hot"** → 三个关键词：语义相似性、维度压缩、迁移学习
2. [ ] **被问"Word2Vec 和 GloVe 的核心区别"** → 局部预测 vs 全局统计，其余效果差不多
3. [ ] **被问"静态嵌入的最大缺陷"** → 一词一向量，无法处理一词多义

### 调试清单（技术类）

1. [ ] **词向量质量差？** → 检查语料大小（至少百万句）、min_count、window、epochs
2. [ ] **KeyError？** → OOV 问题，先检查 `word in model.wv`
3. [ ] **内存不够？** → 降维度（300→100）、提高 min_count、用 KeyedVectors（只读）
4. [ ] **训练太慢？** → 增加 workers、减少 epochs、用 CBOW 替代 Skip-gram
5. [ ] **相似词不合理？** → 检查 window 大小（小=语法，大=语义），检查预处理（大小写、停用词）
