# Lecture 9 学习地图

## 1. 核心问题

这讲要回答三件事：

- 为什么静态词向量不够
- Self-Attention 如何让词读取整句上下文
- Transformer 为什么能取代顺序型 RNN 架构，成为现代 NLP 基座

如果你只记一条主线，就记这句：

> Transformer 的本质不是“更复杂的 RNN”，而是“用并行注意力替代顺序记忆传递”。

## 2. 全景位置

lecture9 是前面序列模型内容的延续。

- lecture5: 语言模型、RNN、LSTM
- lecture6: Seq2Seq、Attention、Transformer 初次登场
- lecture9: 把 Transformer 从“课程结尾彩蛋”升级成“本讲主角”

所以这讲默认你已经知道：

- 词嵌入是什么
- RNN / LSTM 为什么要处理序列
- Attention 为什么能缓解编码瓶颈

## 3. 依赖地图

建议按下面的依赖来理解：

1. 静态嵌入的局限
2. 上下文化表示的需求
3. Self-Attention 的直觉
4. Scaled Dot-Product Attention
5. Multi-Head Attention
6. Positional Encoding
7. Encoder / Decoder / Masking / Cross-Attention
8. Transformer 应用与生态
9. 挑战与后续变体

如果第 3-7 步断了，后面的 Hugging Face 和应用部分会变成只会调包不会理解。

## 4. 文件地图

当前 lecture9 已有文件：

- `lecture9_slides.md`
  作用：按幻灯片顺序整理本讲内容，适合先扫一遍全貌。
- `lecture9_storyline.md`
  作用：把本讲重新组织成“问题 -> 动机 -> 方案 -> 新问题”的因果叙事，适合理解为什么会出现 Transformer。

当前 lecture9 还缺少的常见后续产物：

- `lecture9_concepts.md`
  作用：按概念归档整理，不按讲课顺序。
- `lecture9_math.md`
  作用：专门整理 Query / Key / Value、scaled dot-product、FFN 等公式。
- `lecture9_code.md`
  作用：整理 Hugging Face pipeline、最小 Transformer 使用代码。
- `lecture9_quiz.md`
  作用：用于自测。

## 5. 学习路线

第一次学：

1. 先看 `lecture9_storyline.md`，先把“为什么需要 Transformer”搞清楚
2. 再看 `lecture9_slides.md`，把各模块和老师的例子对上
3. 最后手跑一遍 Hugging Face 的 `pipeline` 例子

考前复习：

1. 直接看 `lecture9_storyline.md` 的“全局回顾”和 checklist
2. 回头翻 `lecture9_slides.md` 对照结构图
3. 用自己的话复述 encoder、decoder、masking、cross-attention

偏代码路线：

1. 先理解 self-attention 的数据流
2. 再理解为什么 decoder 要 mask
3. 再看 Hugging Face pipeline 示例

## 6. 缺口检查

你如果卡住，多半会卡在下面几个点：

- 不清楚静态嵌入和上下文化嵌入的区别
- 把 self-attention 和 cross-attention 混了
- 只会背 Query / Key / Value 名字，不知道它们分别干什么
- 知道并行更快，但说不清为什么 RNN 不能像 Transformer 那样并行
- 知道 Hugging Face 会用，但不知道背后模型结构

最小过关标准：

- 能解释 Self-Attention 在做什么
- 能解释 Transformer 为什么不需要循环
- 能解释 decoder 为什么必须 mask future tokens
- 能列出 3 个 Transformer 应用
