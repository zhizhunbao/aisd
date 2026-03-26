---
topic: word_vectors
dimension: code
created: 2026-03-24
last_verified: 2026-03-24
source_versions:
  - "📖 Docs: Gensim Word2Vec — https://radimrehurek.com/gensim/models/word2vec.html"
  - "📖 Docs: Gensim KeyedVectors — https://radimrehurek.com/gensim/models/keyedvectors.html"
  - "📖 Docs: PyTorch nn.Embedding — https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html"
  - "📖 Docs: GloVe Official — https://nlp.stanford.edu/projects/glove/"
  - "📖 Paper: Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space', ICLR 2013 — https://arxiv.org/abs/1301.3781"
expiry: 6m
status: current
---

# Word Vectors 代码参考

> 📖 Docs: [Gensim Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
> 📖 Docs: [PyTorch nn.Embedding](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)

## 快速开始

### 最简示例 — 30 秒加载预训练词向量

```python
# 加载预训练 GloVe 词向量 / Load pre-trained GloVe word vectors
import gensim.downloader as api

# 下载并加载 GloVe-Wiki-50d (66MB) / Download and load GloVe-Wiki-50d
model = api.load("glove-wiki-gigaword-50")  # 50维, 40万词 / 50d, 400K words

# 查找相似词 / Find similar words
print(model.most_similar("king", topn=5))
# [('queen', 0.87), ('prince', 0.82), ('monarch', 0.78), ...]

# 词类比: king - man + woman = ? / Word analogy
print(model.most_similar(positive=["king", "woman"], negative=["man"], topn=1))
# [('queen', 0.85)]

# 余弦相似度 / Cosine similarity
print(model.similarity("cat", "dog"))   # ≈ 0.80
print(model.similarity("cat", "car"))   # ≈ 0.30
```

**测试方法：** `pip install gensim` 后直接运行，首次会自动下载模型文件

---

## 完整实现示例

### 示例 1: 用 Gensim 在自定义语料上训练 Word2Vec

```python
# ============================================================
# 1. 数据准备 / Data Preparation
# ============================================================
from gensim.models import Word2Vec
import nltk
nltk.download('punkt_tab')

# 准备分词后的语料 (list of list of words) / Tokenized corpus
corpus = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "played", "in", "the", "park"],
    ["a", "cat", "and", "a", "dog", "are", "friends"],
    # ... 实际使用时需要大量句子 / Need many sentences in practice
]

# 也可以从文件加载 / Or load from file
# from gensim.models import LineSentence
# corpus = LineSentence("corpus.txt")  # 每行一个句子,空格分词 / One sentence per line

# ============================================================
# 2. 模型训练 / Model Training
# ============================================================
model = Word2Vec(
    sentences=corpus,          # 分词后的语料 / Tokenized sentences
    vector_size=100,           # 词向量维度 / Embedding dimension
    window=5,                  # 上下文窗口半径 / Context window radius
    min_count=1,               # 最小词频阈值 / Minimum word frequency
    sg=1,                      # 1=Skip-gram, 0=CBOW
    negative=5,                # 负采样个数 / Number of negative samples
    epochs=10,                 # 训练轮数 / Training epochs
    workers=4,                 # 并行线程数 / Parallel threads
    seed=42,                   # 随机种子 / Random seed
)

# ============================================================
# 3. 使用模型 / Using the Model
# ============================================================
# 获取词向量 / Get word vector
vec_cat = model.wv["cat"]  # numpy array, shape=(100,)
print(f"vec('cat') shape: {vec_cat.shape}")
print(f"vec('cat')[:5]: {vec_cat[:5]}")

# 查找最相似词 / Find most similar words
similar = model.wv.most_similar("cat", topn=3)
print(f"Most similar to 'cat': {similar}")

# 余弦相似度 / Cosine similarity
sim = model.wv.similarity("cat", "dog")
print(f"similarity('cat','dog') = {sim:.4f}")

# ============================================================
# 4. 保存与加载 / Save & Load
# ============================================================
# 保存完整模型(可继续训练) / Save full model (can resume training)
model.save("word2vec_model.bin")
loaded_model = Word2Vec.load("word2vec_model.bin")

# 只保存词向量(更小,只读) / Save only vectors (smaller, read-only)
model.wv.save("word2vec_vectors.kv")
from gensim.models import KeyedVectors
loaded_wv = KeyedVectors.load("word2vec_vectors.kv")
```

### 示例 2: 用 PyTorch 从零实现 Skip-gram + 负采样

```python
# ============================================================
# 1. 构建词表与数据集 / Build Vocabulary & Dataset
# ============================================================
import torch
import torch.nn as nn
import torch.optim as optim
from collections import Counter
import numpy as np

# 样例语料 / Sample corpus
corpus = "the cat sat on the mat the dog played in the park".split()

# 构建词表 / Build vocabulary
word_counts = Counter(corpus)
vocab = sorted(word_counts.keys())
word2idx = {w: i for i, w in enumerate(vocab)}
idx2word = {i: w for w, i in word2idx.items()}
V = len(vocab)  # 词表大小 / Vocabulary size

# 生成 Skip-gram 训练对 / Generate Skip-gram training pairs
WINDOW = 2  # 窗口半径 / Window radius
pairs = []  # (center_idx, context_idx)
for i, word in enumerate(corpus):
    center = word2idx[word]
    for j in range(max(0, i-WINDOW), min(len(corpus), i+WINDOW+1)):
        if j != i:
            context = word2idx[corpus[j]]
            pairs.append((center, context))

# 负采样分布: freq^{3/4} / Negative sampling distribution
freqs = np.array([word_counts[w] for w in vocab], dtype=np.float64)
noise_dist = freqs ** 0.75  # 3/4次方 / Raised to 3/4 power
noise_dist /= noise_dist.sum()  # 归一化 / Normalize

# ============================================================
# 2. 模型定义 / Model Definition
# ============================================================
class SkipGramNS(nn.Module):
    """Skip-gram with Negative Sampling"""
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        # 两个独立的嵌入矩阵 / Two separate embedding matrices
        self.center_embed = nn.Embedding(vocab_size, embed_dim)  # W / Center
        self.context_embed = nn.Embedding(vocab_size, embed_dim) # C / Context
        # 初始化 / Initialize
        nn.init.xavier_uniform_(self.center_embed.weight)
        nn.init.xavier_uniform_(self.context_embed.weight)

    def forward(self, center_ids, context_ids, neg_ids):
        """
        center_ids:  (batch,)     中心词索引 / Center word indices
        context_ids: (batch,)     正上下文索引 / Positive context indices
        neg_ids:     (batch, k)   负样本索引 / Negative sample indices
        """
        # 查嵌入 / Look up embeddings
        center = self.center_embed(center_ids)    # (batch, d)
        context = self.context_embed(context_ids) # (batch, d)
        neg = self.context_embed(neg_ids)         # (batch, k, d)

        # 正样本: σ(c·w) / Positive: σ(c·w)
        pos_score = torch.sum(center * context, dim=1)  # (batch,)
        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-10)

        # 负样本: σ(-c_neg·w) / Negative: σ(-c_neg·w)
        neg_score = torch.bmm(neg, center.unsqueeze(2)).squeeze(2)  # (batch, k)
        neg_loss = -torch.log(torch.sigmoid(-neg_score) + 1e-10).sum(dim=1)

        return (pos_loss + neg_loss).mean()

# ============================================================
# 3. 训练循环 / Training Loop
# ============================================================
EMBED_DIM = 50    # 嵌入维度 / Embedding dimension
K = 5             # 负采样数 / Number of negative samples
EPOCHS = 100      # 训练轮数 / Training epochs
LR = 0.01         # 学习率 / Learning rate

model = SkipGramNS(V, EMBED_DIM)
optimizer = optim.Adam(model.parameters(), lr=LR)

for epoch in range(EPOCHS):
    total_loss = 0
    np.random.shuffle(pairs)

    # Mini-batch (简化:全batch) / Mini-batch (simplified: full batch)
    centers = torch.tensor([p[0] for p in pairs])
    contexts = torch.tensor([p[1] for p in pairs])
    # 采负样本 / Sample negatives
    neg_samples = torch.tensor(
        np.random.choice(V, size=(len(pairs), K), p=noise_dist)
    )

    loss = model(centers, contexts, neg_samples)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {loss.item():.4f}")

# ============================================================
# 4. 获取词向量 / Extract Word Vectors
# ============================================================
# 取中心词矩阵作为最终词向量 / Use center embedding as final vectors
word_vectors = model.center_embed.weight.detach().numpy()
print(f"Word vectors shape: {word_vectors.shape}")  # (V, 50)

# 查看词向量 / Inspect vectors
for word in ["cat", "dog", "the"]:
    idx = word2idx[word]
    print(f"vec('{word}')[:5] = {word_vectors[idx][:5]}")
```

---

## API 速查

### Gensim Word2Vec

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `Word2Vec()` | `sentences` | — | 分词后的语料迭代器 / Tokenized corpus |
| ↳ | `vector_size` | 100 | 词向量维度 / Embedding dimension |
| ↳ | `window` | 5 | 上下文窗口半径 / Context window size |
| ↳ | `min_count` | 5 | 最小词频（低于此值被忽略）/ Min word freq |
| ↳ | `sg` | 0 | 0=CBOW, 1=Skip-gram |
| ↳ | `negative` | 5 | 负采样数（0 = 不用负采样）/ Negative samples |
| ↳ | `epochs` | 5 | 训练轮数 / Training epochs |
| ↳ | `workers` | 3 | 并行线程数 / Parallel threads |
| ↳ | `sample` | 1e-3 | 高频词下采样阈值 / Subsampling threshold |
| `model.wv.most_similar()` | `positive` | — | 正向词列表 / Positive words |
| ↳ | `negative` | [] | 负向词列表 / Negative words |
| ↳ | `topn` | 10 | 返回前 N 个结果 / Top N results |
| `model.wv.similarity()` | `w1, w2` | — | 两个词的余弦相似度 / Cosine similarity |
| `model.wv[word]` | — | — | 获取词向量 numpy array / Get vector |
| `gensim.downloader.load()` | `name` | — | 加载预训练模型 / Load pretrained model |

### 常用预训练模型

| 模型名 | 维度 | 词表 | 大小 | 加载方式 |
|--------|------|------|------|---------|
| `glove-wiki-gigaword-50` | 50 | 400K | 66MB | `api.load("glove-wiki-gigaword-50")` |
| `glove-wiki-gigaword-100` | 100 | 400K | 128MB | `api.load("glove-wiki-gigaword-100")` |
| `glove-wiki-gigaword-200` | 200 | 400K | 252MB | `api.load("glove-wiki-gigaword-200")` |
| `glove-wiki-gigaword-300` | 300 | 400K | 376MB | `api.load("glove-wiki-gigaword-300")` |
| `word2vec-google-news-300` | 300 | 3M | 1.6GB | `api.load("word2vec-google-news-300")` |
| `fasttext-wiki-news-subwords-300` | 300 | 999K | 959MB | `api.load("fasttext-wiki-news-subwords-300")` |

### PyTorch nn.Embedding

| 函数/类 | 参数 | 默认值 | 说明 |
|---------|------|--------|------|
| `nn.Embedding()` | `num_embeddings` | — | 词表大小 V / Vocabulary size |
| ↳ | `embedding_dim` | — | 嵌入维度 d / Embedding dimension |
| ↳ | `padding_idx` | None | 填充词索引（该位置梯度为0）/ Padding token |
| ↳ | `max_norm` | None | 向量最大范数 / Max norm clipping |
| ↳ | `from_pretrained()` | — | 用预训练权重初始化 / Init from pretrained |

---

## 目录结构模板

### 简单结构

```
word_vectors/
├── train_word2vec.py         ← 训练脚本 / Training script
├── evaluate.py               ← 评估脚本 (类比/相似度) / Evaluation
├── data/
│   └── corpus.txt            ← 语料 (每行一句,空格分词) / Corpus
└── models/
    └── word2vec.bin           ← 训练好的模型 / Trained model
```

### 标准结构

```
word_vectors/
├── config.py                 ← 超参数配置 / Hyperparameters
├── data_loader.py            ← 语料加载与预处理 / Data loading
├── model.py                  ← Skip-gram / CBOW 模型定义 / Model
├── train.py                  ← 训练循环 / Training loop
├── evaluate.py               ← 评估 (类比/相似度/OOV) / Evaluation
├── visualize.py              ← t-SNE 可视化 / Visualization
├── utils.py                  ← 工具函数 / Utilities
├── data/
│   ├── raw/                  ← 原始语料 / Raw corpus
│   └── processed/            ← 预处理后 / Processed
├── pretrained/               ← 预训练向量 / Pretrained vectors
│   ├── glove.6B.100d.txt
│   └── fasttext_en.bin
├── models/                   ← 训练检查点 / Checkpoints
└── results/                  ← 评估结果 / Results
    └── analogy_accuracy.json
```
