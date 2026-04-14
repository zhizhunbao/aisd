---
topic: bert
dimension: pitfalls
created: 2026-04-13
last_verified: 2026-04-13
source_versions:
  - "📖 Paper: Devlin et al., 'BERT', NAACL 2019"
  - "📚 Book: Jurafsky & Martin, SLP3 Ch.11"
expiry: 6m
status: current
---

# BERT 踩坑记录

> 📖 Paper: Devlin et al., [BERT](https://arxiv.org/abs/1810.04805), NAACL 2019
> 📚 Book: Jurafsky & Martin, [SLP3](../../../textbooks/jurafsky_slp3.pdf), Ch.11

---

## 坑 1: 输入超过 512 token 被静默截断

**场景**：用 BERT 做长文档分类，输入一篇 2000 词的论文

**症状**：模型效果很差，只看到了文档的开头部分

**根因**：BERT 的位置编码固定为 512，超出部分直接丢弃。tokenizer 默认 `truncation=False` 会报错，但设为 `True` 后会静默截断

**解法**：
- ❌ `inputs = tokenizer(long_text, truncation=True)` — 只保留前 512 个 token
- ✅ 方案 A：切片 + 投票 — 把文档切成 510 个 token（留 [CLS] [SEP]）的窗口，每段独立预测，投票/平均
- ✅ 方案 B：换用 Longformer / BigBird（支持 4096+ token）

**教训**：永远检查 `len(tokenizer(text)["input_ids"])`，超过 512 必须有策略

> 📚 Book: Jurafsky & Martin, SLP3, p.254

---

## 坑 2: 微调时学习率太大导致灾难性遗忘

**场景**：在小数据集（< 5000 样本）上微调 BERT-Large

**症状**：训练 loss 震荡或飙升，验证集准确率随机

**根因**：BERT 预训练好的权重很精细，学习率 > 5e-5 会破坏已学知识

**解法**：
- ❌ `lr=1e-3` — 通用 Adam 默认值，对 BERT 太大
- ✅ `lr=2e-5` — BERT 论文推荐范围 2e-5 ~ 5e-5
- ✅ 使用 warmup（前 10% steps 线性增加 lr） + linear decay

**教训**：BERT 微调 lr 一般在 {2e-5, 3e-5, 5e-5} 中网格搜索

> 📖 Paper: Devlin et al. (2019), Section 4.1 — "We selected the best fine-tuning learning rate (among 5e-5, 4e-5, 3e-5, and 2e-5) on the Dev set."

---

## 坑 3: WordPiece 分词导致标签对齐错误

**场景**：NER 任务，需要给每个词标注 B-PER / I-PER 等标签

**症状**：模型预测长度和标签长度不一致

**根因**：WordPiece 把 "playing" 拆成 "play" + "##ing"，原始标签只有一个

**解法**：
- ❌ 直接用 token 级标签 — 子词数 ≠ 原词数
- ✅ 标注策略：首子词取原始标签，后续子词标 "X" 或 -100（忽略）
- ✅ `tokenizer(text, is_split_into_words=True)` + `word_ids()` 做对齐

**教训**：NER 必须用 `word_ids()` 建立 token → word 的映射

> 📖 Docs: HuggingFace Token Classification Tutorial

---

## 坑 4: [CLS] vs mean pooling 选错

**场景**：用 BERT 做句子嵌入（sentence embedding）

**症状**：相似句子的余弦相似度很低，效果不如 Word2Vec 平均

**根因**：BERT 的 [CLS] 是为 NSP 任务优化的，不一定包含最好的句子语义

**解法**：
- ❌ 只用 `outputs.pooler_output`（[CLS] + Dense + Tanh）
- ✅ 用 mean pooling：对所有 token 的 last_hidden_state 取平均
- ✅ 更好：使用 Sentence-BERT（专门为句子相似度微调过）

**教训**：句子级任务不要盲目用 [CLS]，试试 mean pooling 或 Sentence-BERT

> 📖 Paper: Reimers & Gurevych, "Sentence-BERT", EMNLP 2019

---

## 坑 5: BERT-Large 在小数据集上不稳定

**场景**：在 < 3000 样本的数据集上微调 BERT-Large

**症状**：不同随机种子的结果差异巨大（F1 波动 ±5%）

**根因**：BERT-Large 340M 参数在小数据上容易过拟合，随机初始化的分类层影响大

**解法**：
- ✅ 多次随机重启（5-10 次），取最优
- ✅ 优先用 BERT-Base（小数据集上 Base 常优于 Large）
- ✅ 增加 dropout、减少 epochs（2-3 epoch 通常够了）

> 📖 Paper: Devlin et al. (2019), Section 4.1 — "For BERT-LARGE we found that fine-tuning was sometimes unstable on small datasets, so we ran several random restarts."

---

## 超级避坑指南

### 学习避坑
- [ ] 先理解 Transformer Encoder 再学 BERT（否则黑箱）
- [ ] 区分 预训练/微调 两个阶段的输入输出
- [ ] 区分 [CLS] vs 各 token 输出的用途（序列级 vs token 级任务）

### 项目避坑
- [ ] 检查输入长度是否超过 512
- [ ] 微调 lr 从 2e-5 开始，不要用默认 1e-3
- [ ] NER 任务用 `word_ids()` 对齐标签
- [ ] 句子嵌入试 mean pooling 或 Sentence-BERT

### 调试清单
- [ ] loss 不降？→ 检查 lr（太大 or 太小）
- [ ] OOM？→ 减小 batch_size，用 gradient accumulation
- [ ] 预测全是同一类？→ 数据不平衡，加 class weights
- [ ] 验证集好但测试集差？→ 过拟合，减少 epochs / 加 dropout

---
