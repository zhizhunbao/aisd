# %%
# ============================================================
# 工具函数（唯一共享单元）
# Utility Functions (Only shared cell)
# ============================================================
# 设计: 每个概念单元格均自包含 — 数据和辅助函数在单元格内定义,
#       唯一共享: import math 和 ptable() 格式化输出。
# Design: Each concept cell is fully self-contained.
#         Only shared: import math + ptable() for formatted output.
# ============================================================
import math
import tabulate as _tabulate_mod
_tabulate_mod.WIDE_CHARS_MODE = True  # 修复中文对齐 / Fix CJK alignment
from tabulate import tabulate as _tabulate_fn

def ptable(rows, **kwargs):
    """格式化表格输出 / Formatted table output"""
    print(_tabulate_fn(rows, **kwargs, tablefmt="simple_grid"))

print("✅ 工具函数已加载 — 以下30个概念单元格均可独立运行")


# %%
# ============================================================
# 概念01：向量空间模型
# Concept 01: Vector Space Model
# ============================================================
# 将文本表示为高维空间中的数值向量，相似文本在空间中距离相近。
# Mathematical model that represents text as numeric vectors in
# high-dimensional space; similar texts end up "nearby."
# ============================================================

# ── 本单元自包含数据 ──
# 三篇文档及其在2D向量空间中的表示 / 3 docs and their 2D vector-space coordinates
# 维度: x=动物词频, y=科技词频 / Dimensions: x=animal word freq, y=tech word freq
docs = {
    "D1: 动物文章": (4, 1),
    "D2: 科技文章": (1, 5),
    "D3: 动物博客": (3, 2),
}

def euclidean_dist(a, b):
    """欧几里得距离 / Euclidean distance"""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

# 计算文档对之间的距离 / Compute pairwise distances
doc_names = list(docs.keys())
rows = []
for i in range(len(doc_names)):
    for j in range(i + 1, len(doc_names)):
        d = euclidean_dist(docs[doc_names[i]], docs[doc_names[j]])
        rows.append([doc_names[i], doc_names[j], f"{d:.3f}"])

ptable(rows, headers=["概念01: 向量空间模型", "文档B", "距离"])
print("💡 D1(动物)和D3(动物)距离最近 → 主题相似的文档在空间中靠近")


# %%
# ============================================================
# 概念02：向量基础 — 大小与方向
# Concept 02: Vector Basics — Magnitude & Direction
# ============================================================
# 向量是同时具有大小（模）和方向的数学对象。
# A vector is an object that has both a magnitude and a direction.
# ============================================================

# ── 本单元自包含数据 ──
# 两个2D向量 / Two 2D vectors
# 向量A：表示文档1的词频分布 / Vector A: word freq distribution of doc 1
vec_a = (3, 4)
# 向量B：表示文档2的词频分布 / Vector B: word freq distribution of doc 2
vec_b = (1, 7)

# 向量大小 = L₂范数 / Magnitude = L₂ norm
mag_a = math.sqrt(vec_a[0] ** 2 + vec_a[1] ** 2)
mag_b = math.sqrt(vec_b[0] ** 2 + vec_b[1] ** 2)

# 向量方向 = 与x轴的夹角（弧度→角度）/ Direction = angle with x-axis
angle_a = math.degrees(math.atan2(vec_a[1], vec_a[0]))
angle_b = math.degrees(math.atan2(vec_b[1], vec_b[0]))

ptable([
    ["向量A", f"{vec_a}", f"|A| = √(3²+4²) = {mag_a:.2f}", f"{angle_a:.1f}°"],
    ["向量B", f"{vec_b}", f"|B| = √(1²+7²) = {mag_b:.2f}", f"{angle_b:.1f}°"],
], headers=["概念02: 向量基础", "坐标", "大小(模)", "方向(角度)"])
print("💡 向量 = 大小 + 方向; 勾股定理 3²+4² = 5² → |A| = 5")


# %%
# ============================================================
# 概念03：L₂ 范数（向量长度）
# Concept 03: L₂ Norm (Vector Length)
# ============================================================
# L₂范数 = 勾股定理的n维推广: ‖x‖ = √(x₁²+x₂²+...+xₙ²)
# L₂ norm = n-dimensional extension of Pythagoras:
# ‖x‖ = √(x₁² + x₂² + ... + xₙ²)
# ============================================================

# ── 本单元自包含数据与函数 ──
# 3维文本特征向量："cat"在不同维度上的值 / 3D text feature vector for "cat"
x = [3, 4, 0]
# 4维文本特征向量："dog"在不同维度上的值 / 4D text feature vector for "dog"
y = [1, 2, 3, 4]

def l2_norm(vec):
    """L₂范数: √(Σxᵢ²) / L₂ norm: √(Σxᵢ²)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

# 逐步计算展示 / Step-by-step calculation
x_squares = [f"{xi}²={xi**2}" for xi in x]
y_squares = [f"{yi}²={yi**2}" for yi in y]

ptable([
    ["x = [3,4,0]", " + ".join(x_squares), f"√{sum(xi**2 for xi in x)} = {l2_norm(x):.4f}"],
    ["y = [1,2,3,4]", " + ".join(y_squares), f"√{sum(yi**2 for yi in y)} = {l2_norm(y):.4f}"],
], headers=["概念03: L₂范数", "各维平方", "‖x‖"])
print("💡 就是勾股定理: √(3²+4²+0²) = √25 = 5.0")


# %%
# ============================================================
# 概念04：点积（内积）
# Concept 04: Dot Product (Inner Product)
# ============================================================
# x · y = x₁y₁ + x₂y₂ + ... + xₙyₙ
# 衡量两个向量指向同一方向的程度。
# Measures how much two vectors point in the same direction.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 文档向量A和B（4维）/ Document vectors A and B (4-dim)
a = [1, 2, 3, 0]
b = [4, 0, 1, 2]

def dot_product(a, b):
    """点积: Σ(aᵢ×bᵢ) / Dot product: Σ(aᵢ×bᵢ)"""
    return sum(ai * bi for ai, bi in zip(a, b))

# 逐步展示 / Step-by-step breakdown
steps = [f"{ai}×{bi}={ai*bi}" for ai, bi in zip(a, b)]
result = dot_product(a, b)

ptable([
    ["A", f"{a}"],
    ["B", f"{b}"],
    ["逐项相乘", " + ".join(steps)],
    ["A · B", f"{result}"],
], headers=["概念04: 点积", "值"])
print("💡 点积大 = 两向量方向接近 = 内容相似")


# %%
# ============================================================
# 概念05：文本向量化 & 特征向量
# Concept 05: Text Vectorization & Feature Vector
# ============================================================
# 向量化 = 将文本编码为数值向量的过程。
# 特征向量 = 表示一个文本对象的n维数值向量。
# Vectorizing = encoding text as numeric vectors.
# Feature vector = n-dimensional numeric representation of a text.
# ============================================================

# ── 本单元自包含数据 ──
# 原始文本 / Raw text
text = "I love NLP"
# 分词结果 / Tokenized
tokens = text.split()
# 词汇表 / Vocabulary
vocab = ["I", "NLP", "love", "you"]
# 手动编码为特征向量（计数） / Manually encode as feature vector (counts)
feature_vec = [0] * len(vocab)
for t in tokens:
    if t in vocab:
        idx = vocab.index(t)
        feature_vec[idx] += 1

ptable([
    ["原始文本 Raw", text],
    ["分词 Tokens", f"{tokens}"],
    ["词汇表 Vocab", f"{vocab}"],
    ["特征向量", f"{feature_vec}"],
    ["解读", "I=1, NLP=1, love=1, you=0"],
], headers=["概念05: 文本向量化", "值"])
print("💡 向量化 = 给文本分配GPS坐标; 特征向量 = 坐标值")


# %%
# ============================================================
# 概念06：独热编码
# Concept 06: One-Hot Encoding
# ============================================================
# 每个唯一词用一个二进制向量表示，只有自己的位置是1，其余全0。
# Each unique word is represented as a binary vector with exactly
# one 1 at its position and 0 elsewhere.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 示例句子 / Example sentence
sentence = "This is an example"
# 分词 / Tokenize
tokens = sentence.split()
# 词汇表 / Vocabulary (same order as tokens for clarity)
vocab = tokens

def one_hot(word_idx, vocab_size):
    """生成one-hot向量 / Generate one-hot vector"""
    vec = [0] * vocab_size
    vec[word_idx] = 1
    return vec

# 词汇量 / Vocabulary size
V = len(vocab)

# 生成每个词的one-hot / Generate one-hot for each word
rows = []
for i, word in enumerate(vocab):
    vec = one_hot(i, V)
    rows.append([word, f"{vec}"])

ptable(rows, headers=["概念06: One-Hot Encoding", "向量"])
print(f"💡 4个词 → 4维向量, 只有1个位置=1, 其余=0")


# %%
# ============================================================
# 概念07：独热编码文档矩阵
# Concept 07: One-Hot Encoding for Documents
# ============================================================
# 构建词汇表×文档矩阵，每行是一个独热向量，每列代表一个文档。
# Build a Vocabulary × Documents matrix where each row is a
# one-hot vector and each column represents one document.
# ============================================================

# ── 本单元自包含数据 ──
# 三个文档 / Three documents
docs = [
    "cat dog",
    "cat bird",
    "dog bird fish",
]
# 建立词汇表 / Build vocabulary
all_words = []
for doc in docs:
    all_words.extend(doc.split())
vocab = sorted(set(all_words))
# 词汇量 / Vocabulary size
V = len(vocab)

# 构建文档矩阵（每个文档中词是否出现）/ Build doc matrix (presence)
rows = []
for word in vocab:
    row = [word]
    for doc in docs:
        # 1 = 词出现, 0 = 未出现 / 1 = present, 0 = absent
        row.append(1 if word in doc.split() else 0)
    rows.append(row)

ptable(rows, headers=["概念07: OHE文档矩阵", "D1", "D2", "D3"])
print(f"💡 词汇表大小={V}, 矩阵大小={V}×{len(docs)}")


# %%
# ============================================================
# 概念08：独热编码的三大缺陷
# Concept 08: One-Hot Encoding — Three Fatal Flaws
# ============================================================
# OHE 极度稀疏、无频率信息、无语义关系。
# OHE is extremely sparse, has no frequency info, no semantics.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 模拟大词汇量 / Simulate large vocabulary
# 真实词汇量 / Realistic vocabulary size
V_real = 50000
# one-hot中非零元素数 / Non-zero elements in one-hot
nonzero = 1
# 稀疏度 / Sparsity percentage
sparsity = (V_real - nonzero) / V_real * 100

# OHE向量演示: 6词词汇 / OHE demo: 6-word vocab
vocab = ["cat", "dog", "happy", "glad", "volcano", "lava"]

def one_hot(idx, size):
    """生成one-hot向量 / Generate one-hot vector"""
    vec = [0] * size
    vec[idx] = 1
    return vec

def dot_product(a, b):
    """点积 / Dot product"""
    return sum(ai * bi for ai, bi in zip(a, b))

# "happy"和"glad"是同义词但OHE点积=0 / Synonyms but OHE dot=0
oh_happy = one_hot(2, 6)
oh_glad = one_hot(3, 6)
oh_cat = one_hot(0, 6)
oh_volcano = one_hot(4, 6)

ptable([
    ["极度稀疏", f"V={V_real}维, 只有1个1 → {sparsity:.3f}%空间浪费"],
    ["无频率", "'the'出现100次和1次 → 编码相同[...1...]"],
    ["无语义", f"happy·glad = {dot_product(oh_happy, oh_glad)} (同义词=正交!)"],
    ["同义=无关", f"cat·volcano = {dot_product(oh_cat, oh_volcano)} (和同义词一样!)"],
], headers=["概念08: OHE缺陷", "说明"])
print("⚠️ OHE三大问题: 稀疏 + 无频率 + 无语义 → 需要更好的方法!")


# %%
# ============================================================
# 概念09：词袋模型
# Concept 09: Bag of Words (BOW)
# ============================================================
# 文档表示为词的无序集合，只记录频率，忽略词序和语法。
# Document represented as unordered collection of tokens,
# tracking only frequency, ignoring word order and grammar.
# ============================================================

# ── 本单元自包含数据 ──
# 文档 / Document
doc = "cat dog cat bird dog dog"
# 分词 / Tokenize
tokens = doc.split()
# 构建词汇表（按字母序排列）/ Build sorted vocabulary
vocab = sorted(set(tokens))

# 计算各词频率 / Count word frequencies
freq = {}
for t in tokens:
    freq[t] = freq.get(t, 0) + 1

# 生成BOW向量 / Generate BOW vector
bow_vec = [freq.get(w, 0) for w in vocab]

ptable([
    ["原始文档", doc],
    ["分词", f"{tokens}"],
    ["词汇表", f"{vocab}"],
    ["BOW向量", f"{bow_vec}"],
    ["解读", ", ".join(f"{w}={freq[w]}" for w in vocab)],
], headers=["概念09: 词袋模型(BOW)", "值"])
print("💡 BOW = 购物袋: 知道有什么、有几个, 不知道放入顺序")


# %%
# ============================================================
# 概念10：计数向量化（文档-词项矩阵DTM）
# Concept 10: Count Vectorization (Document-Term Matrix)
# ============================================================
# 多个文档映射到共享词汇表后转换为计数向量，形成DTM。
# Multiple documents mapped to shared vocabulary → count vectors → DTM.
# ============================================================

# ── 本单元自包含数据 ──
# 三个文档 / Three documents
corpus = [
    "This is the first document",
    "This is the second document",
    "And the third one One is fun",
]

# 构建词汇表（全小写，按字母排序）/ Build vocab (lowercase, sorted)
all_words = []
for doc in corpus:
    all_words.extend(doc.lower().split())
vocab = sorted(set(all_words))

# 构建文档-词项矩阵(DTM) / Build Document-Term Matrix
rows = []
for i, doc in enumerate(corpus):
    doc_words = doc.lower().split()
    # 计算每个词在此文档中的出现次数 / Count occurrences per word
    counts = [doc_words.count(w) for w in vocab]
    rows.append([f"D{i+1}"] + counts)

ptable(rows, headers=["概念10: DTM"] + vocab)
print(f"💡 DTM: {len(corpus)}文档 × {len(vocab)}词 = 矩阵; 值=出现次数")


# %%
# ============================================================
# 概念11：BOW词序丢失问题
# Concept 11: BOW Word Order Loss
# ============================================================
# "John is quicker than Mary" 和 "Mary is quicker than John"
# 产生完全相同的BOW向量——含义相反但表示相同。
# "John is quicker than Mary" and "Mary is quicker than John"
# produce the same BOW vector — opposite meaning, same vector.
# ============================================================

# ── 本单元自包含数据 ──
# 两个含义相反的句子 / Two sentences with opposite meaning
sent1 = "John is quicker than Mary"
sent2 = "Mary is quicker than John"

# 构建共同词汇表 / Build shared vocabulary
all_tokens = sorted(set(sent1.lower().split() + sent2.lower().split()))

# 计算BOW向量 / Compute BOW vectors
def bow_vector(sentence, vocab):
    """生成BOW向量 / Generate BOW vector"""
    words = sentence.lower().split()
    return [words.count(w) for w in vocab]

bow1 = bow_vector(sent1, all_tokens)
bow2 = bow_vector(sent2, all_tokens)

# 向量是否相同 / Are vectors identical?
identical = bow1 == bow2

ptable([
    ["句子1", sent1],
    ["BOW1", f"{bow1}"],
    ["句子2", sent2],
    ["BOW2", f"{bow2}"],
    ["向量相同?", f"{'✅ 完全相同!' if identical else '不同'}"],
    ["含义相同?", "❌ 完全相反!"],
], headers=["概念11: 词序丢失", "值"])
print(f"词汇表: {all_tokens}")
print("⚠️ BOW丢失词序 → 含义相反的句子变成相同向量!")


# %%
# ============================================================
# 概念12：BOW优缺点总结
# Concept 12: BOW Advantages vs Disadvantages
# ============================================================
# 简单高效但无词序、稀疏、无语义。
# Simple and efficient but no word order, sparse, no semantics.
# ============================================================

# ── 本单元自包含数据 ──
# BOW优缺点对比 / BOW pros and cons
comparison = [
    ("✅ 优点 Advantage", "简单直观", "无需训练，直接计数"),
    ("✅ 优点 Advantage", "计算效率高", "O(n)线性扫描"),
    ("✅ 优点 Advantage", "语言无关", "任何语言都可用"),
    ("✅ 优点 Advantage", "文本分类有效", "频率=有用特征"),
    ("❌ 缺点 Disadvantage", "忽略词序", "\"not good\"丢失否定"),
    ("❌ 缺点 Disadvantage", "高维稀疏", "V=50000 → 大部分为0"),
    ("❌ 缺点 Disadvantage", "无语义信息", "happy ≠ glad"),
    ("❌ 缺点 Disadvantage", "OOV问题", "新词无法表示"),
]

rows = [[cat, item, detail] for cat, item, detail in comparison]
ptable(rows, headers=["概念12: BOW优缺点", "特性", "说明"])


# %%
# ============================================================
# 概念13：N-Gram概念
# Concept 13: N-Gram Concept
# ============================================================
# 不只看单个词，还看连续N个词作为特征，部分恢复BOW丢失的词序。
# Instead of single words, use N consecutive words as features,
# partially restoring word order lost by BOW.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 示例句子 / Example sentence
sentence = "I am learning NLP"
tokens = sentence.split()

def generate_ngrams(tokens, n):
    """生成n-gram / Generate n-grams"""
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

# 生成三种粒度 / Generate three granularities
unigrams = generate_ngrams(tokens, 1)
bigrams = generate_ngrams(tokens, 2)
trigrams = generate_ngrams(tokens, 3)

ptable([
    ["Unigram (N=1)", f"{unigrams}", f"{len(unigrams)}个"],
    ["Bigram (N=2)", f"{bigrams}", f"{len(bigrams)}个"],
    ["Trigram (N=3)", f"{trigrams}", f"{len(trigrams)}个"],
], headers=[f"概念13: N-Gram ('{sentence}')", "结果", "数量"])
print("💡 N越大 → 保留越多词序 → 但特征数也越多")


# %%
# ============================================================
# 概念14：N-Gram 修复否定丢失
# Concept 14: N-Gram Fixes Negation Loss
# ============================================================
# BOW把 "not good" 拆成 {not:1, good:1} → 否定消失。
# Bigram保留 "not good" 作为整体特征 → 否定保留。
# BOW splits "not good" → {not:1, good:1} — negation lost.
# Bigram keeps "not good" as a single feature — negation preserved.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 两个评价 / Two reviews
review_pos = "This movie is good"
review_neg = "This movie is not good"

def generate_ngrams(tokens, n):
    """生成n-gram（自包含重复定义）/ Generate n-grams (self-contained redefinition)"""
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

# BOW（Unigram）表示 / BOW (Unigram) representation
bow_pos = sorted(set(review_pos.lower().split()))
bow_neg = sorted(set(review_neg.lower().split()))

# Bigram 表示 / Bigram representation
bi_pos = generate_ngrams(review_pos.lower().split(), 2)
bi_neg = generate_ngrams(review_neg.lower().split(), 2)

ptable([
    ["正面评价", review_pos],
    ["BOW (Unigram)", f"{bow_pos}"],
    ["Bigram", f"{bi_pos}"],
    ["", ""],
    ["负面评价", review_neg],
    ["BOW (Unigram)", f"{bow_neg}"],
    ["Bigram", f"{bi_neg}"],
], headers=["概念14: N-Gram修复否定", "值"])
# 检查BOW中是否都有"good" / Check if both BOW have "good"
print(f"BOW: 正面含'good'={('good' in bow_pos)}, 负面也含'good'={('good' in bow_neg)} → 无法区分!")
print(f"Bigram: 负面含'not good'={'not good' in bi_neg} → ✅ 否定保留!")


# %%
# ============================================================
# 概念15：N-Gram特征爆炸问题
# Concept 15: N-Gram Feature Explosion
# ============================================================
# 词汇量V时: Unigram=V, Bigram最多V², Trigram最多V³ → 指数增长!
# With vocab size V: Unigram=V, Bigram≤V², Trigram≤V³ → exponential!
# ============================================================

# ── 本单元自包含数据 ──
# 不同词汇量下的特征数 / Feature counts at different vocab sizes
vocab_sizes = [100, 1000, 10000, 50000]

rows = []
for v in vocab_sizes:
    # Unigram特征数 / Unigram features
    uni = v
    # Bigram最大特征数 / Max bigram features
    bi = v * v
    # Trigram最大特征数 / Max trigram features
    tri = v * v * v
    rows.append([
        f"V={v:,}",
        f"{uni:,}",
        f"{bi:,}",
        f"{tri:,}",
    ])

ptable(rows, headers=["概念15: N-Gram特征爆炸", "Unigram(V)", "Bigram(V²)", "Trigram(V³)"])
print("⚠️ V=10,000 时 Bigram = 1亿, Trigram = 1万亿 → 不可计算!")
print("💡 实践: N>3几乎不用; 最常用 unigram+bigram 组合")


# %%
# ============================================================
# 概念16：N-Gram优缺点总结
# Concept 16: N-Gram Advantages vs Disadvantages
# ============================================================
# 捕获部分词序但特征爆炸、仍无语义。
# Captures some word order but features explode, still no semantics.
# ============================================================

# ── 本单元自包含数据 ──
# N-Gram优缺点对比 / N-Gram pros and cons
comparison = [
    ("✅ 优点", "捕获部分上下文和词序", "\"not good\"作为整体"),
    ("✅ 优点", "简单高效的文本表示", "sklearn一行代码"),
    ("❌ 缺点", "稀疏性", "大部分n-gram组合不存在"),
    ("❌ 缺点", "计算开销大", "Bigram=V², Trigram=V³"),
    ("❌ 缺点", "忽略整体结构和语义", "只看N窗口内"),
    ("❌ 缺点", "N的选择困难", "N太大特征爆炸"),
    ("❌ 缺点", "OOV问题", "没见过的词/词对无法表示"),
]

rows = [[cat, item, detail] for cat, item, detail in comparison]
ptable(rows, headers=["概念16: N-Gram优缺点", "特性", "说明"])


# %%
# ============================================================
# 概念17：词频 TF (Term Frequency)
# Concept 17: Term Frequency (TF)
# ============================================================
# TF(词,文档) = 词在文档中出现次数 / 文档总词数
# 归一化消除文档长度的影响。
# TF(term, doc) = count of term in doc / total terms in doc
# Normalization removes document length bias.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 四个文档 / Four documents
docs = {
    "D1": "Dog bites man",
    "D2": "Man bites dog",
    "D3": "Dog eats meat",
    "D4": "Man eats food",
}

def compute_tf(doc_text, term):
    """计算TF / Compute TF"""
    words = doc_text.lower().split()
    # 词在文档中出现的次数 / Count of term in document
    count = words.count(term.lower())
    # 文档总词数 / Total words in document
    total = len(words)
    return count, total, count / total if total > 0 else 0

# 计算各文档中 "dog" 和 "food" 的TF / Compute TF for "dog" and "food"
rows = []
for doc_name, doc_text in docs.items():
    count_dog, total, tf_dog = compute_tf(doc_text, "dog")
    count_food, _, tf_food = compute_tf(doc_text, "food")
    rows.append([
        doc_name, doc_text,
        f"{count_dog}/{total} = {tf_dog:.4f}",
        f"{count_food}/{total} = {tf_food:.4f}",
    ])

ptable(rows, headers=["概念17: TF", "文档内容", "TF(dog)", "TF(food)"])
print("💡 TF = 该词在本文档中的相对频率 (除以总词数消除长度影响)")


# %%
# ============================================================
# 概念18：逆文档频率 IDF (Inverse Document Frequency)
# Concept 18: Inverse Document Frequency (IDF)
# ============================================================
# IDF(词) = log(总文档数N / 包含该词的文档数df)
# 在所有文档中都出现的词 → IDF低; 只在少数文档出现 → IDF高。
# IDF(term) = log(N / df); common words → low IDF, rare → high.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 四个文档 / Four documents
docs = {
    "D1": "dog bites man",
    "D2": "man bites dog",
    "D3": "dog eats meat",
    "D4": "man eats food",
}
# 总文档数 / Total number of documents
N = len(docs)

def compute_idf(docs, term):
    """计算IDF / Compute IDF"""
    # 包含该词的文档数 / Number of docs containing the term
    df = sum(1 for doc in docs.values() if term.lower() in doc.lower().split())
    if df == 0:
        return 0, 0
    return df, math.log10(N / df)

# 计算各词的IDF / Compute IDF for several words
test_words = ["dog", "man", "bites", "eats", "meat", "food"]
rows = []
for word in test_words:
    df, idf = compute_idf(docs, word)
    rarity = "常见" if df >= 3 else "较稀有" if df == 2 else "稀有!"
    rows.append([word, f"{df}/{N}", f"log({N}/{df}) = {idf:.4f}", rarity])

ptable(rows, headers=["概念18: IDF", "df/N", "IDF = log(N/df)", "稀有度"])
print("💡 出现在所有文档 → IDF≈0; 只出现在1个文档 → IDF最高")


# %%
# ============================================================
# 概念19：TF-IDF 计算
# Concept 19: TF-IDF Calculation
# ============================================================
# TF-IDF = TF × IDF; 兼顾局部频率与全局稀有度。
# TF-IDF = TF × IDF; balances local frequency and global rarity.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 四个文档 / Four documents
docs = {
    "D1": "Dog bites man",
    "D2": "Man bites dog",
    "D3": "Dog eats meat",
    "D4": "Man eats food",
}
# 总文档数 / Total documents
N = len(docs)

def compute_tf(doc_text, term):
    """计算TF（自包含重复定义）/ Compute TF (self-contained redefinition)"""
    words = doc_text.lower().split()
    count = words.count(term.lower())
    total = len(words)
    return count / total if total > 0 else 0

def compute_idf(all_docs, term):
    """计算IDF（自包含重复定义）/ Compute IDF (self-contained redefinition)"""
    df = sum(1 for doc in all_docs.values() if term.lower() in doc.lower().split())
    if df == 0:
        return 0
    return math.log10(len(all_docs) / df)

# 计算D1中各词的TF-IDF / Compute TF-IDF for all words in D1
doc_name = "D1"
doc_text = docs[doc_name]
words_in_d1 = doc_text.lower().split()

rows = []
for word in words_in_d1:
    tf = compute_tf(doc_text, word)
    idf = compute_idf(docs, word)
    tfidf = tf * idf
    rows.append([word, f"{tf:.4f}", f"{idf:.4f}", f"{tfidf:.4f}"])

ptable(rows, headers=[f"概念19: TF-IDF ({doc_name})", "TF", "IDF", "TF×IDF"])

# 对比: dog(常见) vs food(稀有) / Compare: dog(common) vs food(rare)
print()
tf_food_d4 = compute_tf(docs["D4"], "food")
idf_food = compute_idf(docs, "food")
tf_dog_d1 = compute_tf(docs["D1"], "dog")
idf_dog = compute_idf(docs, "dog")
ptable([
    ["dog(D1)", f"TF={tf_dog_d1:.4f}", f"IDF={idf_dog:.4f}", f"TF-IDF={tf_dog_d1*idf_dog:.4f}", "常见→低权重"],
    ["food(D4)", f"TF={tf_food_d4:.4f}", f"IDF={idf_food:.4f}", f"TF-IDF={tf_food_d4*idf_food:.4f}", "稀有→高权重"],
], headers=["词(文档)", "TF", "IDF", "TF-IDF", "解读"])
print(f"💡 food的TF-IDF是dog的 {(tf_food_d4*idf_food)/(tf_dog_d1*idf_dog):.1f}倍 → 稀有词更有区分力!")


# %%
# ============================================================
# 概念20：为什么IDF需要log
# Concept 20: Why IDF Needs log
# ============================================================
# 没有log，极稀有词的IDF可达百万级 → 数值爆炸。
# log将其压缩到合理范围。
# Without log, very rare word IDF could be millions → numerical explosion.
# log compresses it to a manageable range.
# ============================================================

# ── 本单元自包含数据 ──
# 不同稀有度下IDF的对比（有log vs 无log）/ IDF with vs without log
# 总文档数 / Total documents
N_total = 1000000

# 不同的df值（包含该词的文档数）/ Different df values
df_values = [1000000, 100000, 10000, 1000, 100, 10, 1]

rows = []
for df in df_values:
    # 无log的IDF / IDF without log
    idf_no_log = N_total / df
    # 有log的IDF / IDF with log
    idf_with_log = math.log10(N_total / df)
    rows.append([
        f"df={df:,}",
        f"{N_total/df:,.0f}",
        f"{idf_with_log:.2f}",
        "常见" if df >= 100000 else "稀有" if df <= 100 else "中等"
    ])

ptable(rows, headers=["概念20: 为什么log", "N/df (无log)", "log(N/df)", "稀有度"])
print("⚠️ 无log: 最稀有词=1,000,000 vs 最常见词=1 → 差100万倍!")
print("✅ 有log: 最稀有词=6 vs 最常见词=0 → 差仅6 → 可控!")


# %%
# ============================================================
# 概念21：TF-IDF 局限性
# Concept 21: TF-IDF Limitations
# ============================================================
# 五项局限：无词间关系、稀疏、无语义、小语料差、OOV。
# Five limitations: no word relationships, sparse, no semantics,
# poor for small corpora, OOV.
# ============================================================

# ── 本单元自包含数据 ──
# TF-IDF的五大局限 / Five TF-IDF limitations
limitations = [
    ("无词间关系", "\"happy\"和\"glad\"是独立维度，无关联", "❌ 致命"),
    ("稀疏性", "V=50,000 → 50,000维向量, 大部分为0", "⚠️ 严重"),
    ("无语义理解", "不理解词的含义，只看频率分布", "❌ 致命"),
    ("小语料效果差", "只有5个文档时IDF统计意义弱", "⚠️ 中等"),
    ("OOV问题", "训练时没见过的词无法表示", "⚠️ 中等"),
]

rows = [[lim, desc, severity] for lim, desc, severity in limitations]
ptable(rows, headers=["概念21: TF-IDF局限", "说明", "严重程度"])
print("🔑 根本局限: 频率方法不理解语义 → 需要词嵌入(Word2Vec)")


# %%
# ============================================================
# 概念22：CountVectorizer vs TfidfVectorizer
# Concept 22: CountVectorizer vs TfidfVectorizer
# ============================================================
# 计数向量化只记录频率; TF-IDF加权后常见词被压低、稀有词被提升。
# CountVectorizer records raw frequency; TfidfVectorizer reweights
# so common words get low weight and rare words get high weight.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 三个文档 / Three documents
corpus = [
    "This is the first document",
    "This is the second document",
    "And the third one One is fun",
]
# 总文档数 / Total documents
N = len(corpus)

# 构建词汇表 / Build vocabulary
all_words = []
for doc in corpus:
    all_words.extend(doc.lower().split())
vocab = sorted(set(all_words))

def compute_tf_for_doc(doc_text, word):
    """计算单词在文档中的TF（自包含重复定义）/ TF (self-contained redefinition)"""
    words = doc_text.lower().split()
    return words.count(word) / len(words) if words else 0

def compute_idf_for_corpus(corpus, word, N):
    """计算IDF（自包含重复定义）/ IDF (self-contained redefinition)"""
    df = sum(1 for doc in corpus if word in doc.lower().split())
    return math.log10(N / df) if df > 0 else 0

# 对比 "the"(常见) 和 "fun"(稀有) / Compare "the"(common) vs "fun"(rare)
target_words = ["the", "is", "first", "fun"]
rows = []
for word in target_words:
    for i, doc in enumerate(corpus):
        count = doc.lower().split().count(word)
        if count > 0:
            tf = compute_tf_for_doc(doc, word)
            idf = compute_idf_for_corpus(corpus, word, N)
            tfidf = tf * idf
            rows.append([word, f"D{i+1}", f"{count}", f"{tf:.3f}", f"{idf:.3f}", f"{tfidf:.3f}"])

ptable(rows, headers=["概念22: Count vs TF-IDF", "文档", "Count", "TF", "IDF", "TF-IDF"])
print("💡 'the': Count高但TF-IDF≈0(太常见)")
print("💡 'fun': Count=1但TF-IDF高(够稀有)")


# %%
# ============================================================
# 概念23：文本相似度概述
# Concept 23: Text Similarity Overview
# ============================================================
# 文本相似度 = 衡量两个文档相似程度的计算度量。
# 应用: 搜索引擎、抄袭检测、机器翻译、文本分类等。
# Text similarity = computational measure of how alike two texts are.
# Applications: search, plagiarism detection, translation, classification.
# ============================================================

# ── 本单元自包含数据 ──
# 五种相似度/距离度量 / Five similarity/distance measures
measures = [
    ("余弦相似度 Cosine", "向量夹角", "文档比较(最常用)", "0~1"),
    ("欧几里得距离 Euclidean", "直线距离", "聚类", "0~∞"),
    ("Levenshtein距离", "编辑操作次数", "拼写纠错", "0~max(m,n)"),
    ("Jaccard相似度", "集合交/并", "集合比较", "0~1"),
    ("汉明距离 Hamming", "不同位的数量", "二进制比较", "0~n"),
]

# 应用场景 / Application scenarios
applications = [
    "🔍 搜索引擎 Search Engine",
    "🔄 机器翻译 Machine Translation",
    "📄 抄袭检测 Plagiarism Detection",
    "📊 信息检索 Information Retrieval",
    "🏷️ 文本分类 Text Classification",
    "🎤 语音识别 Speech Recognition",
]

rows = [[m, what, scene, rng] for m, what, scene, rng in measures]
ptable(rows, headers=["概念23: 相似度度量", "衡量什么", "适用场景", "值域"])
print(f"应用: {', '.join(applications[:3])} ...")


# %%
# ============================================================
# 概念24：Levenshtein距离（编辑距离）
# Concept 24: Levenshtein Distance (Edit Distance)
# ============================================================
# 最少操作数将一个词变成另一个词。操作: 插入、删除、替换。
# Minimum number of operations (insert, delete, substitute)
# to transform one word into another.
# ============================================================

# ── 本单元自包含数据与函数 ──
def levenshtein(s1, s2):
    """计算Levenshtein距离 / Compute Levenshtein distance"""
    m, n = len(s1), len(s2)
    # 初始化DP表 / Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    # 填充DP表 / Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 替换代价: 如果字符相同则为0 / Substitution cost: 0 if same
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # 删除 / Delete
                dp[i][j-1] + 1,      # 插入 / Insert
                dp[i-1][j-1] + cost  # 替换 / Substitute
            )
    return dp[m][n]

# 经典例子: kitten → sitting / Classic example
word1, word2 = "kitten", "sitting"
dist = levenshtein(word1, word2)

# 逐步展示 / Step-by-step
steps = [
    ("kitten → sitten", "替换 k→s", "操作1"),
    ("sitten → sittin", "替换 e→i", "操作2"),
    ("sittin → sitting", "插入 g", "操作3"),
]

rows = [[s, op, step] for s, op, step in steps]
ptable(rows, headers=["概念24: Levenshtein距离", "操作类型", "步骤"])
print(f"Levenshtein('{word1}', '{word2}') = {dist}")
print()

# 更多例子 / More examples
extra_pairs = [("teh", "the"), ("color", "colour"), ("cat", "cats")]
rows2 = [[p[0], p[1], levenshtein(p[0], p[1])] for p in extra_pairs]
ptable(rows2, headers=["词A", "词B", "编辑距离"])
print("💡 拼写纠错: 'teh'→'the' 距离=1 → 很可能是拼错!")


# %%
# ============================================================
# 概念25：欧几里得距离
# Concept 25: Euclidean Distance
# ============================================================
# d(A,B) = √(Σ(aᵢ-bᵢ)²) — 两个向量端点的直线距离。
# d(A,B) = √(Σ(aᵢ-bᵢ)²) — straight-line distance between endpoints.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 两个文档的向量表示 / Two document vectors
doc1 = [1, 2, 0, 1]  # "I love NLP" 的BOW
doc2 = [1, 2, 1, 0]  # "I love you" 的BOW
doc3 = [0, 0, 0, 3]  # "NLP NLP NLP" 的BOW

def euclidean_distance(a, b):
    """欧几里得距离 / Euclidean distance"""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

# 逐步计算 / Step-by-step calculation
diffs = [(a - b) ** 2 for a, b in zip(doc1, doc2)]
dist_12 = euclidean_distance(doc1, doc2)
dist_13 = euclidean_distance(doc1, doc3)
dist_23 = euclidean_distance(doc2, doc3)

ptable([
    ["Doc1 (I love NLP)", f"{doc1}"],
    ["Doc2 (I love you)", f"{doc2}"],
    ["Doc3 (NLP NLP NLP)", f"{doc3}"],
    ["d(D1,D2)", f"√{diffs} = √{sum(diffs)} = {dist_12:.4f}"],
    ["d(D1,D3)", f"{dist_13:.4f}"],
    ["d(D2,D3)", f"{dist_23:.4f}"],
], headers=["概念25: 欧几里得距离", "值"])
print("💡 距离小=文档相似; 但受向量长度(文档长度)影响!")


# %%
# ============================================================
# 概念26：余弦相似度
# Concept 26: Cosine Similarity
# ============================================================
# cos(θ) = (A·B) / (‖A‖ × ‖B‖) — 衡量向量夹角，不受长度影响。
# cos(θ) = (A·B) / (‖A‖ × ‖B‖) — measures angle, length-invariant.
# 值域: 0(正交,无关) ~ 1(同向,最相似)
# Range: 0 (orthogonal, unrelated) ~ 1 (same direction, most similar)
# ============================================================

# ── 本单元自包含数据与函数 ──
def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def l2_norm(vec):
    """L₂范数（自包含重复定义）/ L₂ norm (self-contained redefinition)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

def cosine_sim(a, b):
    """余弦相似度 / Cosine similarity"""
    dot = dot_product(a, b)
    na = l2_norm(a)
    nb = l2_norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

# 课件原题: "I love NLP" vs "I love you" / Slide example
# 词汇表: [I, love, NLP, you] / Vocab: [I, love, NLP, you]
doc1 = [1, 1, 0, 1]  # "I love NLP" → I=1, love=1, NLP=0→应为1(修正下)
# 按课件: Doc1 = [1, 1, 0, 1] 即 (I=1, love=1, you=0, NLP=1)
# 按课件: Doc2 = [1, 1, 1, 0] 即 (I=1, love=1, you=1, NLP=0)
doc1 = [1, 1, 0, 1]
doc2 = [1, 1, 1, 0]

# 逐步计算 / Step-by-step
dot = dot_product(doc1, doc2)
norm1 = l2_norm(doc1)
norm2 = l2_norm(doc2)
cos = cosine_sim(doc1, doc2)

ptable([
    ["Doc1 (I love NLP)", f"{doc1}"],
    ["Doc2 (I love you)", f"{doc2}"],
    ["A · B (点积)", f"1×1 + 1×1 + 0×1 + 1×0 = {dot}"],
    ["‖A‖", f"√(1+1+0+1) = √3 = {norm1:.4f}"],
    ["‖B‖", f"√(1+1+1+0) = √3 = {norm2:.4f}"],
    ["cos(θ)", f"{dot}/({norm1:.4f}×{norm2:.4f}) = {cos:.4f}"],
], headers=["概念26: 余弦相似度", "值"])
print(f"✅ 余弦相似度 = {cos:.4f} ≈ 2/3 ≈ 0.667 → 共享'I'和'love'")


# %%
# ============================================================
# 概念27：余弦 vs 欧几里得 — 为什么余弦更适合文本
# Concept 27: Cosine vs Euclidean — Why Cosine is Better for Text
# ============================================================
# 余弦只看方向(主题)，不受向量长度(文档长度)影响。
# 欧几里得受长度影响：同内容但不同长度的文档距离大。
# Cosine measures direction (topic), ignoring length (doc size).
# Euclidean is affected by length: same-content docs appear distant.
# ============================================================

# ── 本单元自包含数据与函数 ──
def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def l2_norm(vec):
    """L₂范数（自包含重复定义）/ L₂ norm (self-contained redefinition)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

def cosine_sim(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = dot_product(a, b)
    na, nb = l2_norm(a), l2_norm(b)
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0

def euclidean_distance(a, b):
    """欧几里得距离（自包含重复定义）/ Euclidean (self-contained redefinition)"""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

# 场景: 短文档 vs 长文档（内容相同但长度不同）
# Scenario: short vs long doc (same content, different length)
# 短文档: "cat dog cat" / Short doc
doc_short = [2, 1]  # cat=2, dog=1
# 长文档: "cat dog cat cat dog cat dog cat cat dog" (5倍) / Long doc (5x)
doc_long = [10, 5]  # cat=10, dog=5
# 不同内容文档 / Different content doc
doc_diff = [0, 3]   # cat=0, dog=3

cos_same = cosine_sim(doc_short, doc_long)
euc_same = euclidean_distance(doc_short, doc_long)
cos_diff = cosine_sim(doc_short, doc_diff)
euc_diff = euclidean_distance(doc_short, doc_diff)

ptable([
    ["短文档 vs 长文档(同内容)", f"cos={cos_same:.4f}", f"euc={euc_same:.2f}"],
    ["短文档 vs 不同文档", f"cos={cos_diff:.4f}", f"euc={euc_diff:.2f}"],
], headers=["概念27: Cosine vs Euclidean", "余弦相似度", "欧几里得距离"])
print(f"💡 同内容不同长度: cos={cos_same:.4f}(高!)  euc={euc_same:.2f}(大!)")
print(f"💡 余弦认为同内容=相似; 欧几里得被长度差异误导!")
print("🔑 文本比较首选余弦相似度 → 只看方向(主题), 忽略长度")


# %%
# ============================================================
# 概念28：余弦相似度计算 — 词共现矩阵
# Concept 28: Cosine Similarity — Word Co-occurrence Matrix
# ============================================================
# 课堂练习: 用词共现矩阵计算词向量间的余弦相似度。
# Class exercise: compute cosine similarity from co-occurrence matrix.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词共现矩阵（来自slides）/ Word co-occurrence matrix (from slides)
#             pie    data  computer
# cherry      442    8     2
# digital     5      1683  1670
# information 5      3982  3325
word_vectors = {
    "cherry":      [442, 8,    2],
    "digital":     [5,   1683, 1670],
    "information": [5,   3982, 3325],
}

def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def l2_norm(vec):
    """L₂范数（自包含重复定义）/ L₂ norm (self-contained redefinition)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

def cosine_sim(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = dot_product(a, b)
    na, nb = l2_norm(a), l2_norm(b)
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0

# 计算所有词对的余弦相似度 / Compute pairwise cosine similarities
words = list(word_vectors.keys())
rows = []
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        sim = cosine_sim(word_vectors[words[i]], word_vectors[words[j]])
        label = "✅ 语义近" if sim > 0.9 else "⚠️ 中等" if sim > 0.5 else "❌ 语义远"
        rows.append([f"{words[i]} ↔ {words[j]}", f"{sim:.4f}", label])

# 先展示向量 / Show vectors first
vec_rows = [[w, f"{v}"] for w, v in word_vectors.items()]
ptable(vec_rows, headers=["概念28: 词共现向量", "向量 [pie, data, computer]"])
print()
ptable(rows, headers=["词对", "cos_sim", "判定"])
print("💡 digital≈information(都和data/computer共现多) ≠ cherry(和pie共现多)")


# %%
# ============================================================
# 概念29：文档相似度 — CountVectorizer 的误导
# Concept 29: Document Similarity — CountVectorizer Misleading
# ============================================================
# "hot"在多文档中出现 → CountVectorizer把含"hot"的文档判为最相似。
# 但"hot"太常见——这是误导!
# "hot" appears in many docs → CountVectorizer misleadingly scores
# those docs as most similar. But "hot" is too common — misleading!
# ============================================================

# ── 本单元自包含数据与函数 ──
# 五个文档（来自slides）/ Five documents (from slides)
docs = [
    "The weather is hot under the sun",
    "I make my hot chocolate with milk",
    "One hot encoding",
    "I will have a chai latte with milk",
    "There is a hot sale today",
]

def build_count_vectors(docs):
    """构建计数向量 / Build count vectors"""
    # 建立词汇表 / Build vocabulary
    all_w = []
    for d in docs:
        all_w.extend(d.lower().split())
    vocab = sorted(set(all_w))
    # 构建向量 / Build vectors
    vectors = []
    for d in docs:
        words = d.lower().split()
        vec = [words.count(w) for w in vocab]
        vectors.append(vec)
    return vocab, vectors

def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def l2_norm(vec):
    """L₂范数（自包含重复定义）/ L₂ norm (self-contained redefinition)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

def cosine_sim(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = dot_product(a, b)
    na, nb = l2_norm(a), l2_norm(b)
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0

vocab, count_vecs = build_count_vectors(docs)

# 找最相似的文档对（排除自身）/ Find most similar doc pair
best_sim = -1
best_pair = (0, 0)
all_pairs = []
for i in range(len(docs)):
    for j in range(i + 1, len(docs)):
        sim = cosine_sim(count_vecs[i], count_vecs[j])
        all_pairs.append((i, j, sim))
        if sim > best_sim:
            best_sim = sim
            best_pair = (i, j)

# 按相似度排序展示前5个 / Show top 5 by similarity
all_pairs.sort(key=lambda x: x[2], reverse=True)
rows = []
for idx, (i, j, sim) in enumerate(all_pairs[:5]):
    marker = " ← MAX" if (i, j) == best_pair else ""
    rows.append([f"D{i+1} vs D{j+1}", f"{sim:.4f}", marker])

ptable(rows, headers=["概念29: Count相似度(Top5)", "cos_sim", ""])
# 展示共有词分析 / Show shared word analysis
shared_words = []
w1 = set(docs[best_pair[0]].lower().split())
w2 = set(docs[best_pair[1]].lower().split())
shared_words = sorted(w1 & w2)
print(f"⚠️ D{best_pair[0]+1} & D{best_pair[1]+1}最相似(cos={best_sim:.4f})")
print(f"   共有词: {shared_words}")
print("   Count方法对所有词一视同仁 → 常见功能词也贡献相似度 → 可能误导!")


# %%
# ============================================================
# 概念30：文档相似度 — TF-IDF 的智能修正
# Concept 30: Document Similarity — TF-IDF Smart Fix
# ============================================================
# TF-IDF重新加权后，"milk"(稀有)比"hot"(常见)权重更高，
# D2(chocolate+milk) 和 D4(latte+milk) 变成最相似 → 更合理。
# After TF-IDF reweighting, "milk"(rare) > "hot"(common),
# D2 and D4 become most similar → smarter result.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 五个文档（与概念29相同）/ Five documents (same as concept 29)
docs = [
    "The weather is hot under the sun",
    "I make my hot chocolate with milk",
    "One hot encoding",
    "I will have a chai latte with milk",
    "There is a hot sale today",
]
# 总文档数 / Total documents
N = len(docs)

def build_tfidf_vectors(docs):
    """构建TF-IDF向量 / Build TF-IDF vectors"""
    # 建立词汇表 / Build vocabulary
    all_w = []
    for d in docs:
        all_w.extend(d.lower().split())
    vocab = sorted(set(all_w))
    N = len(docs)

    # 计算每个词的df / Compute df for each word
    df = {}
    for w in vocab:
        df[w] = sum(1 for d in docs if w in d.lower().split())

    # 构建TF-IDF向量 / Build TF-IDF vectors
    vectors = []
    for d in docs:
        words = d.lower().split()
        total = len(words)
        vec = []
        for w in vocab:
            # TF = 频率 / TF
            tf = words.count(w) / total if total > 0 else 0
            # IDF = log(N/df) / IDF
            idf = math.log10(N / df[w]) if df[w] > 0 else 0
            vec.append(tf * idf)
        vectors.append(vec)
    return vocab, vectors

def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def l2_norm(vec):
    """L₂范数（自包含重复定义）/ L₂ norm (self-contained redefinition)"""
    return math.sqrt(sum(xi ** 2 for xi in vec))

def cosine_sim(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = dot_product(a, b)
    na, nb = l2_norm(a), l2_norm(b)
    return dot / (na * nb) if na > 0 and nb > 0 else 0.0

vocab, tfidf_vecs = build_tfidf_vectors(docs)

# 找最相似的文档对 / Find most similar doc pair
all_pairs = []
for i in range(N):
    for j in range(i + 1, N):
        sim = cosine_sim(tfidf_vecs[i], tfidf_vecs[j])
        all_pairs.append((i, j, sim))

all_pairs.sort(key=lambda x: x[2], reverse=True)

rows = []
for idx, (i, j, sim) in enumerate(all_pairs[:5]):
    rows.append([f"D{i+1} vs D{j+1}", f"{sim:.4f}"])

ptable(rows, headers=["概念30: TF-IDF相似度(Top5)", "cos_sim"])
print()

# 关键对比 / Key comparison
# 找到"hot"和"milk"的权重对比 / Compare weights of "hot" vs "milk"
hot_idx = vocab.index("hot") if "hot" in vocab else -1
milk_idx = vocab.index("milk") if "milk" in vocab else -1

if hot_idx >= 0 and milk_idx >= 0:
    # D2中 "hot" vs "milk" 的TF-IDF / TF-IDF of "hot" vs "milk" in D2
    ptable([
        ["hot", f"df={sum(1 for d in docs if 'hot' in d.lower().split())}/{N}", f"TF-IDF(D2)={tfidf_vecs[1][hot_idx]:.4f}", "常见→低权重"],
        ["milk", f"df={sum(1 for d in docs if 'milk' in d.lower().split())}/{N}", f"TF-IDF(D2)={tfidf_vecs[1][milk_idx]:.4f}", "稀有→高权重"],
    ], headers=["关键词", "df", "TF-IDF in D2", "解读"])

print("✅ TF-IDF: milk(稀有)权重 > hot(常见)权重 → D2&D4最相似(都含milk) → 更智能!")
print()

# 终极对比表 / Ultimate comparison
# 使用实际计算结果展示对比 / Use computed results for comparison
# Count方法的top pair
count_vocab_c, count_vecs_c = build_count_vectors(docs)
count_pairs = []
for ci in range(N):
    for cj in range(ci + 1, N):
        count_pairs.append((ci, cj, cosine_sim(count_vecs_c[ci], count_vecs_c[cj])))
count_pairs.sort(key=lambda x: x[2], reverse=True)
ci_best, cj_best = count_pairs[0][0], count_pairs[0][1]

ptable([
    ["CountVectorizer", f"D{ci_best+1}&D{cj_best+1}最相似", "常见功能词也贡献相似度", "⚠️ 无区分"],
    ["TF-IDF", f"D{all_pairs[0][0]+1}&D{all_pairs[0][1]+1}最相似", "稀有词'milk'权重提升", "✅ 更智能"],
], headers=["方法", "最相似文档对", "原因", "判断"])


print("\n\n" + "="*60)
print("✅ 30个概念全部演示完毕 — tabulate 表格输出")
print("="*60)
print()
# 最终总结表 / Final summary table
ptable([
    ["One-Hot", "0/1二进制", "❌", "❌", "❌", "极度稀疏"],
    ["BOW", "整数计数", "✅", "❌", "❌", "稀疏"],
    ["N-Gram", "整数计数", "✅", "⚠️部分", "❌", "更稀疏(V²)"],
    ["TF-IDF", "加权浮点", "✅", "❌", "✅", "稀疏"],
], headers=["方法", "值类型", "频率", "词序", "重要性", "稀疏度"])
print()
ptable([
    ["OHE→BOW", "从'有没有'到'有几个'(频率)"],
    ["BOW→N-Gram", "部分恢复词序('not good'保留)"],
    ["N-Gram→TF-IDF", "自动区分重要词和垃圾词"],
    ["TF-IDF→词嵌入(Week4)", "理解词的含义(happy≈glad)"],
], headers=["升级路径", "解决了什么核心问题"])
