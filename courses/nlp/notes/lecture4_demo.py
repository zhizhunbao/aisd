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
# 概念01：分布相似性
# Concept 01: Distributional Similarity
# ============================================================
# 定义：一个词的含义可以从它出现的上下文中理解。
#       "You shall know a word by the company it keeps." — Firth 1957
# Definition: The meaning of a word can be understood from the context
#             in which it appears.
# ============================================================

# ── 本单元自包含数据 ──
# 语料库：3个句子，观察 "cat" 和 "dog" 的上下文
# Corpus: 3 sentences to observe context of "cat" and "dog"
corpus = [
    "the cat sat on the mat",
    "the dog sat on the rug",
    "the cat chased the dog",
]

# 窗口大小：中心词左右各取1个词 / Window: 1 word left and right of center
WINDOW = 1

def get_context(sentence, target, window):
    """提取目标词的上下文词集合 / Extract context words for target"""
    words = sentence.split()
    contexts = set()
    for i, w in enumerate(words):
        if w == target:
            for j in range(max(0, i - window), min(len(words), i + window + 1)):
                if j != i:
                    contexts.add(words[j])
    return contexts

# 收集 "cat" 和 "dog" 在整个语料中的上下文 / Collect contexts across corpus
cat_ctx = set()
dog_ctx = set()
for sent in corpus:
    cat_ctx |= get_context(sent, "cat", WINDOW)
    dog_ctx |= get_context(sent, "dog", WINDOW)

# 共享上下文词 / Shared context words
shared = cat_ctx & dog_ctx

ptable([
    ["cat 的上下文", f"{sorted(cat_ctx)}"],
    ["dog 的上下文", f"{sorted(dog_ctx)}"],
    ["共享上下文", f"{sorted(shared)}"],
    ["结论", f"共享{len(shared)}个词 → 含义相似!"],
], headers=["概念01: 分布相似性", "值"])


# %%
# ============================================================
# 概念02：分布假说
# Concept 02: Distributional Hypothesis
# ============================================================
# 定义：出现在相似上下文中的词具有相似含义。
#       这是词嵌入的理论基础。
# Definition: Words that occur in similar contexts have similar meanings.
#             This is the theoretical foundation of word embeddings.
# ============================================================

# ── 本单元自包含数据 ──
# 上下文模式表：展示不同词的上下文共现频率
# Context pattern table: shows context co-occurrence frequency for different words
# 行=目标词，列=上下文词 / Rows=target words, Cols=context words
context_words = ["cute", "furry", "pet", "eat", "sleep", "volcano", "lava"]
# 每个目标词在各上下文词附近出现的频率 / Frequency of target near each context
target_patterns = {
    "cat":     [5, 4, 6, 3, 4, 0, 0],
    "dog":     [4, 5, 7, 4, 3, 0, 0],
    "kitten":  [6, 3, 5, 2, 5, 0, 0],
    "volcano": [0, 0, 0, 0, 0, 5, 6],
}

def cosine_similarity(a, b):
    """余弦相似度 / Cosine similarity"""
    dot = sum(ai * bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai ** 2 for ai in a))
    norm_b = math.sqrt(sum(bi ** 2 for bi in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# 计算词对的上下文相似度 / Compute context-based similarity between word pairs
pairs = [("cat", "dog"), ("cat", "kitten"), ("cat", "volcano")]
rows = []
for w1, w2 in pairs:
    sim = cosine_similarity(target_patterns[w1], target_patterns[w2])
    label = "✅ 语义近" if sim > 0.8 else "❌ 语义远"
    rows.append([f"{w1} ↔ {w2}", f"{sim:.4f}", label])

ptable(rows, headers=["概念02: 分布假说", "上下文相似度", "判定"])


# %%
# ============================================================
# 概念03：词语相似性
# Concept 03: Word Similarity
# ============================================================
# 定义：词可以相似但不是同义词。语义场是覆盖特定语义域的一组词。
# Definition: Words can be similar without being synonyms.
#             A semantic field is a set of words covering a semantic domain.
# ============================================================

# ── 本单元自包含数据 ──
# 语义场示例：每个场景的相关词汇 / Semantic field examples
semantic_fields = {
    "餐厅 Restaurant": ["waiter", "menu", "plate", "food", "chef"],
    "房屋 House":      ["door", "roof", "kitchen", "family", "bed"],
    "学校 School":     ["teacher", "student", "exam", "book", "class"],
}

# 词语相似性 vs 同义性 / Similarity vs Synonymy
similarity_examples = [
    ("cat", "dog", "相似但非同义 (similar, not synonym)"),
    ("happy", "glad", "同义词 (synonyms)"),
    ("cat", "volcano", "不相似 (not similar)"),
]

rows_fields = [[field, ", ".join(words)] for field, words in semantic_fields.items()]
ptable(rows_fields, headers=["概念03: 语义场", "词汇"])

print()
rows_sim = [[w1, w2, relation] for w1, w2, relation in similarity_examples]
ptable(rows_sim, headers=["词1", "词2", "关系"])


# %%
# ============================================================
# 概念04：WordNet 同义词集
# Concept 04: WordNet Synset
# ============================================================
# 定义：WordNet将共享同一含义的同义词分组为synset（同义词集）。
#       这些synset通过语义关系连接。
# Definition: WordNet groups synonyms sharing a meaning into synsets,
#             connected by semantic relationships.
# ============================================================

# ── 本单元自包含数据 ──
# 模拟 WordNet 的 synset 结构 / Simulated WordNet synset structure
synsets = {
    "dog.n.01": {
        "定义 Definition": "a domesticated canid",
        "同义词 Synonyms": ["dog", "domestic_dog", "Canis_familiaris"],
        "例句 Example": "the dog barked all night",
    },
    "bank.n.01": {
        "定义 Definition": "sloping land beside a body of water",
        "同义词 Synonyms": ["bank"],
        "例句 Example": "they pulled the canoe up on the bank",
    },
    "bank.n.02": {
        "定义 Definition": "a financial institution",
        "同义词 Synonyms": ["bank", "banking_company"],
        "例句 Example": "he cashed a check at the bank",
    },
}

rows = []
for synset_id, info in synsets.items():
    rows.append([synset_id, info["定义 Definition"], ", ".join(info["同义词 Synonyms"])])
ptable(rows, headers=["概念04: WordNet Synset", "定义", "同义词"])
print("⚠️ 'bank' 有多个 synset → 一词多义（polysemy）!")


# %%
# ============================================================
# 概念05：WordNet 语义关系
# Concept 05: WordNet Semantic Relationships
# ============================================================
# 定义：WordNet中8种关键关系类型，连接不同synset。
# Definition: 8 key relationship types in WordNet connecting synsets.
# ============================================================

# ── 本单元自包含数据 ──
# WordNet 8种语义关系 / 8 WordNet semantic relationships
relationships = [
    ("Synset 同义词集",   "共享同一含义的词集合",         "happy, glad, cheerful"),
    ("Hypernym 上位词",   "更通用的类别",                 "animal 是 dog 的上位词"),
    ("Hyponym 下位词",    "更具体的子类",                 "dog 是 animal 的下位词"),
    ("Meronym 部分词",    "表示整体的一部分",             "wheel 是 car 的部分词"),
    ("Holonym 整体词",    "表示整体",                     "car 是 wheel 的整体词"),
    ("Antonym 反义词",    "含义相反",                     "hot ↔ cold"),
    ("Troponym 方式动词", "行为的具体方式",               "run 是 move 的方式动词"),
    ("Entailment 蕴含",   "一个动词隐含另一个",           "snore → sleep"),
]

rows = [[rel, defn, example] for rel, defn, example in relationships]
ptable(rows, headers=["概念05: WordNet关系", "定义", "示例"])


# %%
# ============================================================
# 概念06：WordNet 的局限性
# Concept 06: WordNet Limitations
# ============================================================
# 定义：手工维护、覆盖有限、静态、不可计算、领域受限。
# Definition: Manual curation, limited coverage, static, not computable.
# ============================================================

# ── 本单元自包含数据 ──
# WordNet 五大局限 / 5 key limitations of WordNet
limitations = [
    ("覆盖有限+静态", "缺少新词、俚语、网络用语", "Missing: 'selfie', 'GOAT', 'vibe'"),
    ("不可计算",       "只有关系，不给向量",        "No vector for similarity score"),
    ("领域特定",       "通用词汇为主",              "Weak in: medical, legal, tech"),
    ("语言限制",       "主要覆盖英语",              "Limited: Chinese, Arabic"),
    ("人工维护",       "需要语言学家手动更新",      "Slow, expensive, labor-intensive"),
]

rows = [[lim, desc, example] for lim, desc, example in limitations]
ptable(rows, headers=["概念06: WordNet局限", "说明", "示例"])
print("🔑 手动编码太慢 → 需要自动从文本学习 → 词嵌入登场!")


# %%
# ============================================================
# 概念07：One-Hot 编码及其局限
# Concept 07: One-Hot Encoding & Limitations
# ============================================================
# 定义：长度V向量，该词位置=1，其余=0。高维稀疏、无语义。
# Definition: Vector of length V, 1 at word's index, 0 elsewhere.
#             High-dimensional, sparse, no semantic meaning.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词汇表：6个词 / Vocabulary: 6 words
VOCAB = ["cat", "dog", "happy", "glad", "volcano", "lava"]
# 词→编号映射 / Word-to-index mapping
WORD2ID = {w: i for i, w in enumerate(VOCAB)}
# 词汇量 / Vocabulary size
V = len(VOCAB)

def one_hot(word_id, vocab_size):
    """生成 one-hot 向量 / Generate one-hot vector"""
    vec = [0] * vocab_size
    vec[word_id] = 1
    return vec

def dot_product(a, b):
    """点积 / Dot product"""
    return sum(ai * bi for ai, bi in zip(a, b))

# 生成 one-hot 向量 / Generate one-hot vectors
oh_cat = one_hot(WORD2ID["cat"], V)
oh_dog = one_hot(WORD2ID["dog"], V)
oh_happy = one_hot(WORD2ID["happy"], V)
oh_glad = one_hot(WORD2ID["glad"], V)

# 点积衡量相似度（one-hot 点积永远=0）/ Dot product = 0 for any pair
ptable([
    ["cat",   f"{oh_cat}"],
    ["dog",   f"{oh_dog}"],
    ["happy", f"{oh_happy}"],
    ["glad",  f"{oh_glad}"],
], headers=["概念07: One-Hot", "向量"])

print()
ptable([
    ["cat · dog",     f"{dot_product(oh_cat, oh_dog)}",   "❌ 正交=无相似"],
    ["happy · glad",  f"{dot_product(oh_happy, oh_glad)}", "❌ 同义词也正交"],
    ["cat · volcano", f"{dot_product(oh_cat, one_hot(WORD2ID['volcano'], V))}", "❌ 和任何词一样"],
], headers=["词对", "点积", "问题"])
print("⚠️ 四大缺陷: 高维(V维) + 稀疏(只1个1) + 无语义 + OOV!")


# %%
# ============================================================
# 概念08：词嵌入 / 向量语义
# Concept 08: Word Embedding / Vector Semantics
# ============================================================
# 定义：将词映射为稠密低维向量 f: V → Rᵈ (d=50~300)。
#       在嵌入空间中，含义相近的词位置接近。
# Definition: Map words to dense low-dimensional vectors f: V → Rᵈ.
#             Semantically similar words are close in embedding space.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 模拟词嵌入向量（4维）：语义相近的词向量接近
# Simulated word embeddings (4d): similar words have close vectors
embeddings = {
    "cat":     [ 0.80,  0.60, -0.30,  0.50],
    "dog":     [ 0.75,  0.65, -0.25,  0.45],
    "kitten":  [ 0.82,  0.58, -0.28,  0.52],
    "happy":   [-0.20,  0.40,  0.70,  0.30],
    "glad":    [-0.18,  0.42,  0.72,  0.28],
    "volcano": [ 0.10, -0.80,  0.05, -0.60],
}

def cosine_similarity(a, b):
    """余弦相似度 / Cosine similarity"""
    dot = sum(ai * bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai ** 2 for ai in a))
    norm_b = math.sqrt(sum(bi ** 2 for bi in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# 对比 one-hot（正交）vs 嵌入（有相似度）/ Compare one-hot (orthogonal) vs embedding
pairs = [("cat", "dog"), ("cat", "kitten"), ("happy", "glad"), ("cat", "volcano")]
rows = []
for w1, w2 in pairs:
    sim = cosine_similarity(embeddings[w1], embeddings[w2])
    label = "✅ 语义近" if sim > 0.8 else "❌ 语义远" if sim < 0.3 else "⚠️ 中等"
    rows.append([f"{w1} ↔ {w2}", f"{sim:.4f}", label])

ptable(rows, headers=["概念08: 词嵌入相似度", "cos_sim", "判定"])
print("✅ 嵌入空间: cat≈dog≈kitten, happy≈glad, cat≠volcano")


# %%
# ============================================================
# 概念09：词向量类比（向量算术）
# Concept 09: Word Analogy (Vector Arithmetic)
# ============================================================
# 定义：king - man + woman ≈ queen
#       向量算术捕获语义关系。
# Definition: king - man + woman ≈ queen
#             Vector arithmetic captures semantic relationships.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 模拟词向量（6维）：编码性别和皇室属性
# Simulated vectors (6d): encoding gender and royalty attributes
analogy_vecs = {
    "king":   [ 0.8,  0.7,  0.9,  0.2,  0.1,  0.3],
    "queen":  [ 0.8,  0.7,  0.1,  0.9,  0.3,  0.3],
    "man":    [ 0.1,  0.2,  0.8,  0.1,  0.1,  0.2],
    "woman":  [ 0.1,  0.2,  0.1,  0.8,  0.3,  0.2],
    "prince": [ 0.7,  0.6,  0.85, 0.15, 0.1,  0.25],
    "princess":[ 0.7,  0.6,  0.15, 0.85, 0.3,  0.25],
}

def vec_add(a, b):
    """向量加法 / Vector addition"""
    return [ai + bi for ai, bi in zip(a, b)]

def vec_sub(a, b):
    """向量减法 / Vector subtraction"""
    return [ai - bi for ai, bi in zip(a, b)]

def cosine_similarity(a, b):
    """余弦相似度 / Cosine similarity"""
    dot = sum(ai * bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai ** 2 for ai in a))
    norm_b = math.sqrt(sum(bi ** 2 for bi in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# king - man + woman = ? / Analogy: king - man + woman = ?
result_vec = vec_add(vec_sub(analogy_vecs["king"], analogy_vecs["man"]),
                     analogy_vecs["woman"])

# 找最近的词 / Find nearest word to result vector
rows = []
for word, vec in analogy_vecs.items():
    sim = cosine_similarity(result_vec, vec)
    marker = " ← 最近!" if word == "queen" else ""
    rows.append([word, f"{sim:.4f}", marker])

# 按相似度排序 / Sort by similarity
rows.sort(key=lambda r: float(r[1]), reverse=True)
ptable(rows, headers=["概念09: king-man+woman=?", "cos_sim", ""])
print("✅ queen 最接近 → 向量算术捕获了'皇室'这个方向!")


# %%
# ============================================================
# 概念10：CBOW（连续词袋模型）
# Concept 10: CBOW (Continuous Bag of Words)
# ============================================================
# 定义：上下文词 → 预测中心词。输入的上下文向量取平均。
# Definition: Context words → predict center word.
#             Average context embeddings as input.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 训练语料 / Training corpus
sentence = "the cat sat on the mat"
# 词汇表 / Vocabulary
words = sentence.split()
vocab = sorted(set(words))
# 词→编号映射 / Word-to-index mapping
word2id = {w: i for i, w in enumerate(vocab)}
# 词汇量 / Vocabulary size
V = len(vocab)
# 嵌入维度 / Embedding dimension
D = 4
# 窗口大小 / Window size
WINDOW = 2

# 模拟嵌入矩阵 [V×D] / Simulated embedding matrix
emb = {
    "cat": [0.8, 0.6, -0.3, 0.5],
    "mat": [0.3, -0.1, 0.2, 0.15],
    "on":  [0.05, 0.1, 0.05, -0.05],
    "sat": [0.15, -0.2, 0.45, -0.1],
    "the": [0.1, 0.2, -0.3, 0.05],
}

def average_vectors(vecs):
    """向量平均 / Average of vectors"""
    n = len(vecs)
    d = len(vecs[0])
    return [sum(v[j] for v in vecs) / n for j in range(d)]

# CBOW 示例: window=2, center="sat"
# 上下文: ["the", "cat", "on", "the"]
center = "sat"
context = ["the", "cat", "on", "the"]

# 上下文词嵌入取平均 / Average context embeddings
ctx_vecs = [emb[w] for w in context]
avg_ctx = average_vectors(ctx_vecs)

ptable([
    ["中心词 Center", center],
    ["上下文 Context", f"{context}"],
    ["各上下文向量", f"{[emb[w] for w in context]}"],
    ["平均后输入", f"{[f'{v:.4f}' for v in avg_ctx]}"],
    ["目标", f"P('{center}' | context) 最大化"],
], headers=["概念10: CBOW", "值"])
print("💡 CBOW = 完形填空: 从上下文猜中心词")


# %%
# ============================================================
# 概念11：Skip-gram（跳字模型）
# Concept 11: Skip-gram
# ============================================================
# 定义：中心词 → 预测上下文词。CBOW的反向。
# Definition: Center word → predict context words. Reverse of CBOW.
# ============================================================

# ── 本单元自包含数据 ──
# 训练语料 / Training corpus
sentence = "the cat sat on the mat"
words = sentence.split()
# 窗口大小 / Window size
WINDOW = 2

def generate_skipgram_pairs(words, window):
    """生成Skip-gram训练对 / Generate Skip-gram training pairs"""
    pairs = []
    for i, center in enumerate(words):
        # 窗口范围 / Window range
        start = max(0, i - window)
        end = min(len(words), i + window + 1)
        for j in range(start, end):
            if j != i:
                pairs.append((center, words[j]))
    return pairs

# 生成所有训练对 / Generate all training pairs
sg_pairs = generate_skipgram_pairs(words, WINDOW)

# 只展示前8个训练对 / Show first 8 pairs
rows = [[f"Step {k+1}", pair[0], pair[1]]
        for k, pair in enumerate(sg_pairs[:8])]
ptable(rows, headers=["概念11: Skip-gram训练对", "中心词", "上下文词"])
print(f"总共 {len(sg_pairs)} 个训练对 (窗口={WINDOW})")
print("💡 Skip-gram = 扩展联想: 从一个词猜它的邻居")


# %%
# ============================================================
# 概念12：CBOW vs Skip-gram 对比
# Concept 12: CBOW vs Skip-gram Comparison
# ============================================================
# 定义：两种Word2Vec架构各有优劣。
# Definition: Two Word2Vec architectures with different trade-offs.
# ============================================================

# ── 本单元自包含数据 ──
# 对比维度 / Comparison dimensions
comparison = [
    ("方向 Direction",  "上下文 → 中心词",     "中心词 → 上下文"),
    ("任务 Task",       "完形填空(1个预测)",    "扩展联想(多个预测)"),
    ("速度 Speed",      "✅ 更快",             "⚠️ 较慢"),
    ("高频词 Frequent", "✅ 更好(平均平滑)",   "⚠️ 有噪声"),
    ("低频词 Rare",     "❌ 被平均掉",         "✅ 更好(独立信号)"),
    ("数据量 Data",     "需要较多数据",         "少量数据也可"),
    ("分类难度",        "✅ 较简单",           "⚠️ 较难"),
]

rows = [[dim, cbow, sg] for dim, cbow, sg in comparison]
ptable(rows, headers=["概念12: 对比", "CBOW", "Skip-gram"])


# %%
# ============================================================
# 概念13：上下文窗口
# Concept 13: Context Window
# ============================================================
# 定义：中心词左右各取 window 个词作为上下文。
#       窗口大小影响学到的语义类型。
# Definition: Take 'window' words on each side of center word.
#             Window size affects the type of semantics captured.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 示例句子 / Example sentence
sentence = "I love natural language processing very much"
words = sentence.split()
# 中心词位置 / Center word position
center_idx = 3  # "language"
center_word = words[center_idx]

def get_window_context(words, center_idx, window_size):
    """根据窗口大小获取上下文 / Get context by window size"""
    start = max(0, center_idx - window_size)
    end = min(len(words), center_idx + window_size + 1)
    return [words[j] for j in range(start, end) if j != center_idx]

# 不同窗口大小的上下文 / Context for different window sizes
rows = []
for w in [1, 2, 3]:
    ctx = get_window_context(words, center_idx, w)
    rows.append([f"window={w}", f"{ctx}", f"{len(ctx)}个词"])

ptable(rows, headers=[f"概念13: 窗口(中心='{center_word}')", "上下文", "数量"])
print("💡 窗口小→语法关系, 窗口大→语义/主题关系")


# %%
# ============================================================
# 概念14：Skip-gram 滑动窗口详解
# Concept 14: Skip-gram Sliding Window Detail
# ============================================================
# 定义：句子 "the cat sat on the mat"，window=2，
#       展示每一步中心词和上下文。
# Definition: Walk through each step of Skip-gram with window=2
#             on "the cat sat on the mat".
# ============================================================

# ── 本单元自包含数据 ──
sentence = "the cat sat on the mat"
words = sentence.split()
WINDOW = 2

rows = []
for i, center in enumerate(words):
    start = max(0, i - WINDOW)
    end = min(len(words), i + WINDOW + 1)
    ctx = [words[j] for j in range(start, end) if j != i]
    rows.append([f"Step {i+1}", center, f"{ctx}"])

ptable(rows, headers=["概念14: 滑动窗口", "中心词", "上下文"])


# %%
# ============================================================
# 概念15：Word2Vec 的核心洞察（向量=权重）
# Concept 15: Word2Vec Key Insight (Vectors = Weights)
# ============================================================
# 定义：训练完成后不要预测结果，要的是隐藏层权重矩阵的每一行。
#       训练目标（预测上下文）只是一个借口——真正的产品是权重。
# Definition: After training, discard predictions. Keep the hidden layer
#             weight matrix — each row IS the word embedding.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 模拟训练后的权重矩阵 W_hidden [V×d] / Simulated trained weight matrix
# 每一行 = 一个词的嵌入向量 / Each row = one word's embedding
vocab = ["the", "cat", "sat", "on", "mat"]
# 训练后的隐藏层权重矩阵 [5词 × 4维] / Trained hidden weights [5×4]
W_trained = [
    [ 0.10,  0.20, -0.30,  0.05],  # the
    [ 0.80,  0.60, -0.30,  0.50],  # cat
    [ 0.15, -0.20,  0.45, -0.10],  # sat
    [ 0.05,  0.10,  0.05, -0.05],  # on
    [ 0.30, -0.10,  0.20,  0.15],  # mat
]

ptable([
    ["训练输入", "大量文本 (自监督)"],
    ["训练目标", "预测上下文/中心词 (借口)"],
    ["真正产品", "隐藏层权重矩阵 W"],
    ["取嵌入方式", "W[word_id] = 词的向量"],
], headers=["概念15: 向量=权重", "说明"])

print()
rows = [[w, f"{W_trained[i]}"] for i, w in enumerate(vocab)]
ptable(rows, headers=["词", "嵌入向量 (=W的那一行)"])


# %%
# ============================================================
# 概念16：Softmax 瓶颈
# Concept 16: Softmax Bottleneck
# ============================================================
# 定义：原始 Skip-gram 输出层用 softmax 计算所有词的概率。
#       词表V=50000 → 每个样本都要对50000个词求和 → 极慢!
# Definition: Original Skip-gram uses softmax over entire vocabulary.
#             O(V) per training step — prohibitively slow for large V.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 小型 softmax 演示 / Small softmax demonstration
# 输出层的原始分数（logits）/ Raw output scores (logits)
logits = [2.0, 1.0, 0.1, -0.5, 3.0]
# 词汇表 / Vocabulary for this demo
vocab_demo = ["cat", "dog", "fish", "rock", "mat"]

def softmax(logits):
    """softmax: e^zᵢ / Σⱼ e^zⱼ — 需要遍历所有V个词! / Must sum over ALL V words!"""
    max_z = max(logits)  # 数值稳定 / Numerical stability
    exps = [math.exp(z - max_z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

probs = softmax(logits)

rows = [[w, f"{logits[i]:+.1f}", f"{probs[i]:.4f}"]
        for i, w in enumerate(vocab_demo)]
ptable(rows, headers=["概念16: Softmax", "logit", "P(word)"])

print()
# 训练代价对比 / Training cost comparison
ptable([
    ["softmax O(V)",  "V=50,000",   "每步需计算50000次exp和求和"],
    ["softmax O(V)",  "V=100,000",  "每步需计算100000次 → 更慢"],
    ["SGNS O(k)",     "k=5~15",     "只需计算5~15次 → 快3000倍!"],
], headers=["方法", "词汇量", "训练代价"])
print(f"⚠️ softmax 概率总和验证: {sum(probs):.6f} (应=1.0)")


# %%
# ============================================================
# 概念17：SGNS（Skip-gram 负采样）
# Concept 17: SGNS (Skip-gram with Negative Sampling)
# ============================================================
# 定义：不再问"V个词中哪个正确"，改问"这个词对是真是假"。
#       正样本: 真实共现对 → 标签=1
#       负样本: 随机配对   → 标签=0
#       训练逻辑回归区分两者。
# Definition: Instead of softmax over V words, turn it into a binary
#             classification: real pair (label=1) vs random pair (label=0).
# ============================================================

# ── 本单元自包含数据与函数 ──
# 示例句子 / Example sentence
sentence = "a tablespoon of apricot jam a pinch"
# 目标词 / Target word
target = "apricot"
# 真实上下文词（正样本）/ Real context words (positive)
positive_contexts = ["tablespoon", "of", "jam", "a"]
# 负采样词（随机选的非上下文词）/ Negative samples (random non-context words)
negative_samples = ["volcano", "democracy", "penguin", "algebra", "toaster"]
# 负采样数量 k / Number of negative samples
K = 5

def sigmoid(z):
    """sigmoid: 1 / (1 + e^(-z)) — 二分类概率 / Binary classification"""
    if z > 20: return 1.0
    if z < -20: return 0.0
    return 1.0 / (1.0 + math.exp(-z))

# 模拟正/负样本的相似度分数 / Simulated similarity scores
rows = []
for ctx in positive_contexts[:2]:
    # 正样本分数较高 / Positive pair: higher score
    score = 1.5 + 0.3 * len(ctx) % 3
    rows.append([f"({target}, {ctx})", "正样本 +", f"{score:.2f}", f"{sigmoid(score):.4f}"])
for neg in negative_samples[:3]:
    # 负样本分数较低 / Negative pair: lower score
    score = -1.0 - 0.2 * len(neg) % 3
    rows.append([f"({target}, {neg})", "负样本 -", f"{score:.2f}", f"{sigmoid(score):.4f}"])

ptable(rows, headers=["概念17: SGNS", "类型", "score", "σ(score)"])
print(f"✅ 加速: O(50000) → O(1+{K}) = O({1+K}), 快了 ~{50000//(1+K)} 倍!")


# %%
# ============================================================
# 概念18：负采样策略（频率加权）
# Concept 18: Negative Sampling Strategy (Frequency Weighting)
# ============================================================
# 定义：负样本不是均匀随机的，而是按 f(w)^(3/4) 采样。
#       3/4次方提升低频词的采样概率，避免高频词主导。
# Definition: Negative samples drawn proportional to f(w)^(3/4).
#             The 3/4 exponent boosts rare words, prevents "the" domination.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词频分布 / Word frequency distribution
word_freqs = {
    "the": 10000,
    "cat": 500,
    "quantum": 10,
    "antidisestablish": 1,
}
# 总词频 / Total word count
total = sum(word_freqs.values())

# 均匀采样概率 vs f(w)^(3/4) 加权概率 / Uniform vs 3/4-weighted probability
alpha = 0.75  # 3/4次方指数 / 3/4 exponent

# 计算 f(w)^alpha / Compute f(w)^alpha for each word
weighted = {w: freq ** alpha for w, freq in word_freqs.items()}
# 加权总和 / Weighted total
total_weighted = sum(weighted.values())

rows = []
for w, freq in word_freqs.items():
    # 均匀概率 / Uniform probability
    p_uniform = freq / total
    # 加权概率 / Weighted probability
    p_weighted = weighted[w] / total_weighted
    # 变化倍数 / Change factor
    change = p_weighted / p_uniform if p_uniform > 0 else 0
    rows.append([w, f"{freq}", f"{p_uniform:.6f}", f"{p_weighted:.4f}", f"{change:.1f}x"])

ptable(rows, headers=["概念18: 负采样策略", "词频", "P_均匀", "P_加权(3/4)", "变化"])
print("💡 高频词(the)被压低，低频词(quantum)被提升 → 更均衡的负样本")


# %%
# ============================================================
# 概念19：共现矩阵
# Concept 19: Co-Occurrence Matrix
# ============================================================
# 定义：V×V矩阵，记录词i在词j附近出现的次数。
#       GloVe的基础数据结构。
# Definition: V×V matrix counting how often word i appears near word j.
#             Foundation data structure for GloVe.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 语料 / Corpus
corpus = [
    "I love Programming",
    "I love Math",
    "I tolerate Biology",
]
# 窗口大小 / Window size
WINDOW = 1

def build_cooccurrence(corpus, window):
    """构建共现矩阵 / Build co-occurrence matrix"""
    # 收集词汇 / Collect vocabulary
    all_words = []
    for sent in corpus:
        all_words.extend(sent.split())
    vocab = sorted(set(all_words))
    w2i = {w: i for i, w in enumerate(vocab)}
    n = len(vocab)
    # 初始化矩阵 / Initialize matrix
    matrix = [[0] * n for _ in range(n)]
    # 统计共现 / Count co-occurrences
    for sent in corpus:
        words = sent.split()
        for i, center in enumerate(words):
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            for j in range(start, end):
                if j != i:
                    matrix[w2i[center]][w2i[words[j]]] += 1
    return vocab, matrix

vocab, cooc = build_cooccurrence(corpus, WINDOW)

# 显示共现矩阵 / Display co-occurrence matrix
rows = [[vocab[i]] + cooc[i] for i in range(len(vocab))]
ptable(rows, headers=["概念19: 共现矩阵"] + vocab)
print("💡 'I' 和 'love' 共现2次 → 密切相关")
print("💡 'love' 和 'tolerate' 共现0次 → 不直接相邻")


# %%
# ============================================================
# 概念20：GloVe 算法
# Concept 20: GloVe Algorithm
# ============================================================
# 定义：学习向量使得 wᵢ · wⱼ ≈ log(共现次数)。
#       结合全局统计和预测优化的优点。
# Definition: Learn vectors such that wᵢ · wⱼ ≈ log(co-occurrence count).
#             Combines global statistics with prediction optimization.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 共现次数 / Co-occurrence counts (from concept 19)
cooc_pairs = {
    ("I", "love"): 2,
    ("I", "tolerate"): 1,
    ("love", "Programming"): 1,
    ("love", "Math"): 1,
    ("tolerate", "Biology"): 1,
    ("I", "Programming"): 0,
}

def dot_product(a, b):
    """点积 / Dot product"""
    return sum(ai * bi for ai, bi in zip(a, b))

# 模拟 GloVe 训练后的向量 / Simulated GloVe-trained vectors
glove_vecs = {
    "I":           [ 0.5,  0.3,  0.1],
    "love":        [ 0.4,  0.6,  0.2],
    "tolerate":    [ 0.3,  0.1,  0.4],
    "Programming": [ 0.2,  0.5,  0.3],
    "Math":        [ 0.25, 0.45, 0.35],
    "Biology":     [ 0.1,  0.15, 0.5],
}

rows = []
for (w1, w2), count in cooc_pairs.items():
    dot = dot_product(glove_vecs[w1], glove_vecs[w2])
    log_count = f"{math.log(count):.4f}" if count > 0 else "−∞"
    rows.append([f"{w1} · {w2}", f"{count}", log_count, f"{dot:.4f}"])

ptable(rows, headers=["概念20: GloVe优化目标", "共现次数", "log(count)", "wᵢ·wⱼ"])
print("✅ GloVe: 全局共现统计 + 向量优化 = 两全其美")


# %%
# ============================================================
# 概念21：GloVe vs Word2Vec 对比
# Concept 21: GloVe vs Word2Vec Comparison
# ============================================================
# 定义：Word2Vec只看局部窗口，GloVe结合全局统计。
# Definition: Word2Vec sees only local windows;
#             GloVe combines global statistics with prediction.
# ============================================================

# ── 本单元自包含数据 ──
comparison = [
    ("全局统计",    "❌ 只看窗口",   "✅ 共现矩阵",        "GloVe ✅"),
    ("语义优化",    "✅ 预测学习",   "✅ log(count)优化",   "平手 ="),
    ("类比能力",    "好",            "更好",                "GloVe ✅"),
    ("训练速度",    "快(SGNS)",      "快(矩阵分解)",        "平手 ="),
    ("OOV处理",     "❌ 无法处理",   "❌ 无法处理",         "都不行 ❌"),
    ("上下文敏感",  "❌ 静态向量",   "❌ 静态向量",         "都不行 ❌"),
]

rows = [[dim, w2v, glove, winner] for dim, w2v, glove, winner in comparison]
ptable(rows, headers=["概念21: 对比", "Word2Vec", "GloVe", "胜出"])


# %%
# ============================================================
# 概念22：FastText 子词（字符 N-gram）
# Concept 22: FastText Subword (Character N-grams)
# ============================================================
# 定义：FastText将词拆成字符n-gram (长度3~6)。
#       词向量 = Σ 所有n-gram向量 + 整词向量。
# Definition: FastText decomposes words into character n-grams (length 3-6).
#             Word vector = Σ all n-gram vectors + whole-word vector.
# ============================================================

# ── 本单元自包含数据与函数 ──
def generate_ngrams(word, min_n=3, max_n=6):
    """生成字符 n-gram / Generate character n-grams"""
    # 添加边界标记 / Add boundary markers
    padded = f"<{word}>"
    ngrams = []
    for n in range(min_n, max_n + 1):
        for i in range(len(padded) - n + 1):
            ngrams.append(padded[i:i+n])
    return ngrams

# 示例词 / Example word
word = "where"
ngrams = generate_ngrams(word)

# 按长度分组显示 / Group by length
for n in range(3, 7):
    group = [ng for ng in ngrams if len(ng) == n]
    if group:
        print(f"  {n}-gram: {group}")

print()
ptable([
    ["原词", f"'{word}'"],
    ["加边界", f"'<{word}>'"],
    ["n-gram总数", f"{len(ngrams)}"],
    ["词向量", "Σ(所有n-gram向量) + 整词向量"],
], headers=["概念22: FastText子词", "值"])


# %%
# ============================================================
# 概念23：FastText 解决 OOV
# Concept 23: FastText Solves OOV
# ============================================================
# 定义：新词的n-gram在已知词中出现过 → 自动获得向量。
# Definition: Unseen word shares n-grams with known words → gets a vector.
# ============================================================

# ── 本单元自包含数据与函数 ──
def generate_ngrams(word, min_n=3, max_n=6):
    """生成字符 n-gram（自包含重复定义）/ Generate char n-grams (self-contained redefinition)"""
    padded = f"<{word}>"
    ngrams = []
    for n in range(min_n, max_n + 1):
        for i in range(len(padded) - n + 1):
            ngrams.append(padded[i:i+n])
    return ngrams

# 已知词 / Known words (in training data)
known_words = ["unhappy", "happily", "happy"]
# 新词（训练时未见过）/ New word (unseen during training)
new_word = "unhappily"

# 新词的n-gram / N-grams of the new word
new_ngrams = set(generate_ngrams(new_word))

# 检查哪些已知词共享n-gram / Check which known words share n-grams
rows = []
for known in known_words:
    known_ng = set(generate_ngrams(known))
    shared = new_ngrams & known_ng
    rows.append([known, f"{len(known_ng)}", f"{len(shared)}", f"{sorted(shared)[:5]}..."])

ptable(rows, headers=[f"概念23: OOV'{new_word}'", "已知n-gram数", "共享数", "共享示例"])
print(f"✅ '{new_word}' 虽未见过，但与已知词共享大量n-gram → 自动获得向量!")
print("💡 词根类比: un-(不) + happy(快乐) + -ly(地) → 不快乐地")


# %%
# ============================================================
# 概念24：Word2Vec vs GloVe vs FastText 全方位对比
# Concept 24: Word2Vec vs GloVe vs FastText Full Comparison
# ============================================================
# 定义：三种静态词嵌入方法的完整对比。
# Definition: Complete comparison of three static embedding methods.
# ============================================================

# ── 本单元自包含数据 ──
comparison = [
    ("表示单位",     "整词",               "整词",               "字符n-gram + 整词"),
    ("学习方式",     "预测(局部窗口)",     "计数+预测(全局)",     "预测(局部窗口)"),
    ("OOV处理",      "❌ 不能",            "❌ 不能",            "✅ n-gram拼接"),
    ("拼写错误容忍", "❌ 无容错",          "❌ 无容错",          "✅ 共享n-gram"),
    ("形态学感知",   "忽略",               "忽略",               "✅ 捕获"),
    ("模型大小",     "小",                 "小",                 "大(存所有n-gram)"),
    ("类比能力",     "好",                 "更好",               "好"),
    ("上下文敏感",   "❌ 静态(一词一向量)", "❌ 静态(一词一向量)", "❌ 静态(一词一向量)"),
]

rows = [[dim, w2v, glove, ft] for dim, w2v, glove, ft in comparison]
ptable(rows, headers=["概念24: 三方对比", "Word2Vec", "GloVe", "FastText"])
print("⚠️ 终极缺陷: 三者都是静态嵌入 → 'bank'(河岸) = 'bank'(银行)")


# %%
# ============================================================
# 概念25：余弦相似度
# Concept 25: Cosine Similarity
# ============================================================
# 定义：cos(θ) = (a·b) / (||a|| × ||b||)。
#       衡量两个向量方向的相似程度，忽略长度。
# Definition: cos(θ) = dot(a,b) / (norm(a) × norm(b)).
#             Measures directional similarity, ignores magnitude.
# ============================================================

# ── 本单元自包含数据与函数 ──
# 词嵌入向量 / Word embedding vectors
vecs = {
    "cat":     [ 0.80,  0.60, -0.30,  0.50],
    "dog":     [ 0.75,  0.65, -0.25,  0.45],
    "happy":   [-0.20,  0.40,  0.70,  0.30],
    "volcano": [ 0.10, -0.80,  0.05, -0.60],
}

def cosine_similarity(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = sum(ai * bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai ** 2 for ai in a))
    norm_b = math.sqrt(sum(bi ** 2 for bi in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def dot_product(a, b):
    """点积（自包含重复定义）/ Dot product (self-contained redefinition)"""
    return sum(ai * bi for ai, bi in zip(a, b))

def norm(a):
    """向量范数 / Vector norm"""
    return math.sqrt(sum(ai ** 2 for ai in a))

# 详细展示计算过程 / Show detailed computation
a, b = vecs["cat"], vecs["dog"]
dot_val = dot_product(a, b)
norm_a_val = norm(a)
norm_b_val = norm(b)
cos_val = dot_val / (norm_a_val * norm_b_val)

ptable([
    ["a = cat",    f"{a}"],
    ["b = dog",    f"{b}"],
    ["a · b",      f"{dot_val:.4f}"],
    ["||a||",      f"{norm_a_val:.4f}"],
    ["||b||",      f"{norm_b_val:.4f}"],
    ["cos(θ)",     f"{cos_val:.4f}"],
], headers=["概念25: 余弦相似度计算过程", "值"])

print()
# 多对比较 / Multiple pair comparisons
pairs = [("cat","dog"), ("cat","happy"), ("cat","volcano"), ("happy","volcano")]
rows = []
for w1, w2 in pairs:
    sim = cosine_similarity(vecs[w1], vecs[w2])
    label = "✅近" if sim > 0.7 else "❌远" if sim < 0 else "⚠️中"
    rows.append([f"{w1} ↔ {w2}", f"{sim:.4f}", label])
ptable(rows, headers=["词对", "cos_sim", "判定"])


# %%
# ============================================================
# 概念26：嵌入评估（内在评估 vs 外在评估）
# Concept 26: Embedding Evaluation (Intrinsic vs Extrinsic)
# ============================================================
# 定义：内在评估 = 独立测评（类比、相似度）。
#       外在评估 = 下游任务表现（文本分类、NER等）。
# Definition: Intrinsic = standalone evaluation (analogy, similarity).
#             Extrinsic = downstream task performance (classification, NER).
# ============================================================

# ── 本单元自包含数据与函数 ──
# 内在评估示例：词相似度任务 / Intrinsic: word similarity task
# 人类评分 (0-10) / Human similarity ratings
human_ratings = {
    ("cat", "dog"): 7.5,
    ("cat", "car"): 1.2,
    ("happy", "glad"): 9.0,
    ("king", "queen"): 8.5,
}

# 模拟嵌入的余弦相似度 / Simulated embedding cosine similarities
model_sims = {
    ("cat", "dog"): 0.82,
    ("cat", "car"): 0.15,
    ("happy", "glad"): 0.95,
    ("king", "queen"): 0.88,
}

rows = []
for pair, human in human_ratings.items():
    model = model_sims[pair]
    # 归一化人类评分到 [0,1] / Normalize human rating to [0,1]
    human_norm = human / 10.0
    match = "✅" if abs(human_norm - model) < 0.15 else "⚠️"
    rows.append([f"{pair[0]}↔{pair[1]}", f"{human}/10", f"{model:.2f}", match])

ptable(rows, headers=["概念26: 内在评估", "人类评分", "模型cos_sim", "一致"])
print()
ptable([
    ["内在评估 Intrinsic", "独立测评", "词相似度、类比任务"],
    ["外在评估 Extrinsic", "下游任务", "文本分类、NER、情感分析"],
], headers=["评估类型", "方式", "示例"])


# %%
# ============================================================
# 概念27：上下文不敏感（静态嵌入的终极缺陷）
# Concept 27: Context Insensitivity (Fatal Flaw of Static Embeddings)
# ============================================================
# 定义："bank"(河岸)和"bank"(银行)永远是同一个向量。
#       所有静态嵌入（Word2Vec/GloVe/FastText）都有此缺陷。
# Definition: "bank" (river) and "bank" (finance) always have the SAME vector.
#             All static embeddings share this fatal flaw.
# ============================================================

# ── 本单元自包含数据 ──
# 三个不同上下文中的 "bank" / "bank" in 3 different contexts
contexts = [
    ("I deposited money at the bank.",        "银行 (金融)"),
    ("The river bank was covered with grass.", "河岸 (自然)"),
    ("Bank on me, I won't let you down.",      "依靠 (动词)"),
]

# 静态嵌入: 同一个 bank 只有一个向量 / Static: one vector for "bank"
bank_static = [0.35, 0.20, -0.15, 0.40]

# 理想的上下文嵌入: 不同含义不同向量 / Ideal contextual: different vectors
bank_contextual = {
    "银行 (金融)":  [ 0.80,  0.60, -0.30,  0.10],
    "河岸 (自然)":  [-0.10,  0.30,  0.70,  0.50],
    "依靠 (动词)":  [ 0.20, -0.40,  0.15,  0.60],
}

rows = []
for sent, meaning in contexts:
    ctx_vec = bank_contextual[meaning]
    rows.append([meaning, f"{bank_static}", f"{ctx_vec}", "❌ 静态相同"])

ptable(rows, headers=["概念27: 上下文不敏感", "静态向量(相同)", "理想向量(不同)", "问题"])
print("⚠️ Word2Vec/GloVe/FastText: bank(河岸) = bank(银行) → 无法区分!")
print("🔑 解决方案: ELMo/BERT → 同词不同上下文 → 不同向量 (Week 5+)")


# %%
# ============================================================
# 概念28：嵌入偏见
# Concept 28: Embedding Bias
# ============================================================
# 定义：词嵌入从训练数据中学到社会偏见。
#       如: man:computer_programmer :: woman:homemaker
# Definition: Word embeddings learn social biases from training data.
#             E.g.: man:computer_programmer :: woman:homemaker
# ============================================================

# ── 本单元自包含数据与函数 ──
# 模拟有偏见的嵌入 / Simulated biased embeddings
biased_vecs = {
    "man":        [ 0.5,  0.3,  0.8,  0.1],
    "woman":      [ 0.5,  0.3,  0.1,  0.8],
    "programmer": [ 0.6,  0.2,  0.7,  0.15],
    "homemaker":  [ 0.6,  0.2,  0.15, 0.7],
    "doctor":     [ 0.7,  0.4,  0.65, 0.2],
    "nurse":      [ 0.7,  0.4,  0.2,  0.65],
}

def cosine_similarity(a, b):
    """余弦相似度（自包含重复定义）/ Cosine similarity (self-contained redefinition)"""
    dot = sum(ai * bi for ai, bi in zip(a, b))
    norm_a = math.sqrt(sum(ai ** 2 for ai in a))
    norm_b = math.sqrt(sum(bi ** 2 for bi in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# 偏见检测: 哪个职业更接近哪个性别? / Bias detection
occupations = ["programmer", "homemaker", "doctor", "nurse"]
rows = []
for occ in occupations:
    sim_man = cosine_similarity(biased_vecs[occ], biased_vecs["man"])
    sim_woman = cosine_similarity(biased_vecs[occ], biased_vecs["woman"])
    bias_dir = "→ man" if sim_man > sim_woman else "→ woman"
    rows.append([occ, f"{sim_man:.4f}", f"{sim_woman:.4f}", f"偏向{bias_dir}"])

ptable(rows, headers=["概念28: 嵌入偏见", "sim(man)", "sim(woman)", "偏见方向"])
print("⚠️ 嵌入从数据中学到社会偏见 → 需要 debiasing 去偏!")


# %%
# ============================================================
# 概念29：词嵌入优点总结
# Concept 29: Word Embedding Benefits Summary
# ============================================================
# 定义：词嵌入相对频率方法的四大优势。
# Definition: Four key advantages of word embeddings over frequency methods.
# ============================================================

# ── 本单元自包含数据 ──
benefits = [
    ("降维 Dimensionality Reduction",
     "50,000维 → 300维", "✅ 99.4%压缩"),
    ("语义含义 Semantic Meaning",
     "cat≈dog, happy≈glad", "✅ 捕获含义"),
    ("OOV处理 Handle OOV",
     "FastText子词拼接", "✅ 新词可表示"),
    ("迁移学习 Transfer Learning",
     "预训练→下游任务微调", "✅ 即插即用"),
]

rows = [[b, example, status] for b, example, status in benefits]
ptable(rows, headers=["概念29: 嵌入优点", "示例", "状态"])

print()
# 与频率方法对比 / Comparison with frequency methods
ptable([
    ["维度",     "V维(50000+)",     "d维(50~300)",    "✅ 嵌入"],
    ["稀疏性",   "极稀疏(1个1)",    "稠密(全非零)",   "✅ 嵌入"],
    ["语义",     "❌ 无",           "✅ 有",          "✅ 嵌入"],
    ["OOV",      "❌ 无法处理",     "✅ FastText",    "✅ 嵌入"],
    ["NLP任务",  "性能一般",        "性能显著提升",   "✅ 嵌入"],
], headers=["指标", "频率方法", "词嵌入", "胜出"])


# %%
# ============================================================
# 概念30：词嵌入局限性总结
# Concept 30: Word Embedding Limitations Summary
# ============================================================
# 定义：六大局限性，引出上下文嵌入。
# Definition: Six key limitations, leading to contextual embeddings.
# ============================================================

# ── 本单元自包含数据 ──
limitations = [
    ("上下文不敏感", "bank(河岸)=bank(银行)", "❌ 致命"),
    ("嵌入偏见",     "man:programmer::woman:homemaker", "⚠️ 严重"),
    ("语义适应有限", "固定向量无法适应新领域", "⚠️ 中等"),
    ("维度选择困难", "50? 100? 300? 需要实验", "⚠️ 中等"),
    ("资源密集",     "大语料训练需大量计算", "⚠️ 中等"),
    ("OOV问题",      "Word2Vec/GloVe仍有此问题", "⚠️ 部分解决"),
]

rows = [[lim, example, severity] for lim, example, severity in limitations]
ptable(rows, headers=["概念30: 嵌入局限", "示例", "严重程度"])

print()
ptable([
    ["静态嵌入", "Word2Vec/GloVe/FastText", "一词一向量", "❌ 上下文不敏感"],
    ["上下文嵌入", "ELMo/BERT/GPT", "一词多向量", "✅ 上下文敏感"],
], headers=["类型", "代表", "特点", "上下文"])
print("🔑 下一代: ELMo(2018) → BERT(2018) → GPT → 上下文嵌入时代!")


print("\n✅ 30个概念全部演示完毕 — tabulate 表格输出")
