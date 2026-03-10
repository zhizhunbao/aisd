# Week 9: Transformer-Based Language Models

> Source: `lecture_9_W26.pdf`
> Total slides: 49
> Instructor: Hala Own, Ph.D.

---

## 1. 课程议程与问题背景 (Agenda & Motivation)

![Page 1](lecture9_slides_pages/page_001.png)

**CST8507: Natural Language Processing - Week #9: Transformer-Based Language Models** - 第9周主题是基于 Transformer 的语言模型。

![Page 2](lecture9_slides_pages/page_002.png)

**Lesson Agenda:** - 本讲核心内容：

- Transformer architecture - Transformer 架构
- Self-attention mechanisms - 自注意力机制
- Transfer learning and fine-tuning - 迁移学习与微调
- Applications of transformer-based language models - 基于 Transformer 的应用
- Drawbacks and variants of Transformers - 局限与变体

![Page 3](lecture9_slides_pages/page_003.png)

**Text Representation Techniques:** 图示回顾文本表示技术从传统表示到深度表示的演进。

![Page 4](lecture9_slides_pages/page_004.png)

**Problem with static embeddings (word2vec):** - 静态词向量的核心问题：

- One word = one vector - 一个词只有一个固定向量
- Fixed at training time - 训练后不随上下文变化
- OOV problem - 存在未登录词问题
- Morphological blindness - 对词形变化不敏感，如 `run / running / runner`

![Page 5](lecture9_slides_pages/page_005.png)

**Contextual Embeddings:** - 上下文化表示强调：

- 同一个词在不同上下文里应有不同向量
- 词义由周围词共同决定

---

## 2. 自注意力的动机 (Motivation for Self-Attention)

![Page 6](lecture9_slides_pages/page_006.png)

**Self-attention: Motivations:** 为了构造某个词的上下文化表示，需要从整句中选择性整合其他词的信息，而且不同词的重要性不同。

![Page 7](lecture9_slides_pages/page_007.png)

**What is Self-attention:** 每个词都会问一句话：

> 在当前句子里，哪些其他词最有助于理解我？

自注意力就是对这个问题的并行回答机制。

![Page 8](lecture9_slides_pages/page_008.png)

**Why Multi-Head Attention?:** 单头注意力只能得到一份加权混合，表达能力有限，因此需要多头去同时关注不同关系。

![Page 9](lecture9_slides_pages/page_009.png)

**Transformers (2017):** Transformer 出自论文 *Attention Is All You Need*。  
Ref: https://arxiv.org/abs/1706.03762

![Page 10](lecture9_slides_pages/page_010.png)

**What is Transformer:** Transformer 是一种完全依赖 self-attention 来建模输入与输出表示的序列架构，擅长处理长距离依赖。

---

## 3. Transformer 总体结构 (Transformer Overview)

![Page 11](lecture9_slides_pages/page_011.png)

**Transformer Architecture:** 先给出整体结构图。

![Page 12](lecture9_slides_pages/page_012.png)

**Transformer's Model Architecture:** 模型由 Encoder stack 和 Decoder stack 组成。  
Source in slide: https://arxiv.org/abs/1706.03762

![Page 13](lecture9_slides_pages/page_013.png)

**Encoder Anatomy:** 编码器的基本模块包括：

- Multi-head self-attention
- Feed-forward layer
- Residual connection
- Layer normalization

---

## 4. 位置编码 (Positional Encoding)

![Page 14](lecture9_slides_pages/page_014.png)
![Page 15](lecture9_slides_pages/page_015.png)
![Page 16](lecture9_slides_pages/page_016.png)

**Encoder: Positional Encoding:** 因为 Transformer 不依赖循环结构，词序信息必须显式加入输入表示。

![Page 17](lecture9_slides_pages/page_017.png)

**Positional vector is added to embedding vector:** 每个位置都有一个位置向量，并与词嵌入相加，得到带顺序信息的表示。  
Ref in slide: https://towardsdatascience.com/understanding-positional-encoding-in-transformers-dc6bafc021ab

![Page 18](lecture9_slides_pages/page_018.png)

**Positional Encoding Example:** 用 `"I love NLP"` 演示了位置编码数值如何随位置变化。示例展示了 `sin` / `cos` 周期函数如何构造不同维度上的位置特征。

---

## 5. 编码器中的自注意力 (Self-Attention in the Encoder)

![Page 19](lecture9_slides_pages/page_019.png)

**Encoder: Self Attention:** 编码器内部每个词都能直接看见整句中所有其他词。

![Page 20](lecture9_slides_pages/page_020.png)

**The Attention Mechanism Workflow:** 该页用流程图说明注意力从打分到加权汇总的全过程。

![Page 21](lecture9_slides_pages/page_021.png)

**Self-attention:** 核心是把一个词的表示更新为“自己 + 与其他词的相关信息”的加权组合。

![Page 22](lecture9_slides_pages/page_022.png)
![Page 23](lecture9_slides_pages/page_023.png)
![Page 24](lecture9_slides_pages/page_024.png)

**Scale Dot-Product Motivation / Softmax Sensitivity:** 由于 softmax 对数值尺度敏感，点积值过大时会让分布过于尖锐，因此需要缩放。

![Page 25](lecture9_slides_pages/page_025.png)

**Encoder: Self (Scaled Dot-Product) Attention:** 缩放点积注意力在高维情形下更稳定。幻灯片示例中使用了 `d = 64` 的情形。  
Slide credit: Jay Alammar

![Page 26](lecture9_slides_pages/page_026.png)

**Transformer Architecture - Score:** 这一页按步骤列出了自注意力计算：

1. Query 和 Key 做点积得到分数
2. 用维度大小做缩放
3. 经过 softmax 得到权重
4. 用权重加权各个 Value
5. 求和得到上下文表示

![Page 27](lecture9_slides_pages/page_027.png)

**Encoder: Multi-Headed Attention:** 多头注意力让模型从不同子空间、不同关系模式上并行建模。

---

## 6. 前馈层、残差与归一化 (FFN, Residual, Add & Norm)

![Page 28](lecture9_slides_pages/page_028.png)

**The Feed-Forward Layer (position-wise feed-forward layer):**

`FFN(Z) = ReLU(ZW1 + b1)W2 + b2`

该层对每个位置单独做非线性变换，提高表示能力。

![Page 29](lecture9_slides_pages/page_029.png)

**Residual Connections:** 残差连接让每层学习“对输入做增量修正”，而不是完全重写输入表示。

![Page 30](lecture9_slides_pages/page_030.png)

**Add & Norm:** 残差相加后接 Layer Normalization，有助于训练稳定。

---

## 7. 并行计算优势 (Parallel Processing)

![Page 31](lecture9_slides_pages/page_031.png)
![Page 32](lecture9_slides_pages/page_032.png)
![Page 33](lecture9_slides_pages/page_033.png)

**Parallel processing / Parallel Computation of Query, Key, and Value:** Transformer 的关键优势之一是并行。整句的 Query、Key、Value 可以一次性并行计算，而不像 RNN 那样必须按时间步顺序执行。

---

## 8. 解码器、掩码与交叉注意力 (Decoder, Masking, Cross-Attention)

![Page 34](lecture9_slides_pages/page_034.png)

**Decoder:** 解码器负责自回归地产生输出序列。

![Page 35](lecture9_slides_pages/page_035.png)
![Page 36](lecture9_slides_pages/page_036.png)

**Masking the future in self-attention:** 解码器中的 masked self-attention 会屏蔽未来词，确保当前位置只能看到已经生成的历史词，不能偷看后面的正确答案。

![Page 37](lecture9_slides_pages/page_037.png)

**Cross-Attention: The Bridge Between Encoder and Decoder:** 交叉注意力让解码器在生成时读取编码器输出，从源序列中提取当前最相关的信息。

![Page 38](lecture9_slides_pages/page_038.png)

**How the Encoder and the Decoder Stack Works:** 编码器逐层变换输入；最后一层编码器输出会提供给所有解码器层作为条件信息。  
Ref in slide: https://www.analyticsvidhya.com/blog/2019/06/understanding-transformers-nlp-state-of-the-art-models/

![Page 39](lecture9_slides_pages/page_039.png)

**The Final SoftMax Layer:** 最后通过 softmax 在词表上输出下一词概率分布。

---

## 9. Hugging Face 生态与应用 (Ecosystem & Applications)

![Page 40](lecture9_slides_pages/page_040.png)

**The Hugging Face Ecosystem:** 介绍 Transformer 时代最常用的开源工具生态。  
Source in slide: *Natural Language Processing with Transformers*, O'Reilly, 2022

![Page 41](lecture9_slides_pages/page_041.png)

**The Hugging Face Hub:** 模型、数据集和演示代码的共享平台。

![Page 42](lecture9_slides_pages/page_042.png)

**Transformer Applications - Text Classification:** 使用 `pipeline("text-classification")` 做文本分类。

![Page 43](lecture9_slides_pages/page_043.png)

**Transformer Applications - Named Entity Recognition:** 使用 `pipeline("ner", aggregation_strategy="simple")` 做命名实体识别。

![Page 44](lecture9_slides_pages/page_044.png)

**Transformer Applications - Question Answering:** 使用 `pipeline("question-answering")` 做抽取式问答。

![Page 45](lecture9_slides_pages/page_045.png)

**Transformer Applications - Summarization:** 使用 `pipeline("summarization")` 做摘要生成。

![Page 46](lecture9_slides_pages/page_046.png)

**The Transformer Tree of Life:** 展示 Transformer 系列模型家族和后续分支发展。

---

## 10. 局限与总结 (Challenges & Summary)

![Page 47](lecture9_slides_pages/page_047.png)

**Challenges with Transformers:** 本讲列出的主要问题：

- Language - 语言覆盖与迁移问题
- Data availability - 数据依赖高
- Working with long documents - 长文档处理困难
- Transparency - 可解释性有限
- Bias - 容易继承训练数据偏差

![Page 48](lecture9_slides_pages/page_048.png)

**Summary:** 注意力机制会聚焦输入中的关键部分并生成上下文相关摘要；自注意力是对输入自身做总结；Transformer 则重复堆叠自注意力和前馈层来逐步变换表示。

![Page 49](lecture9_slides_pages/page_049.png)

**Q&A** - 问答环节。
