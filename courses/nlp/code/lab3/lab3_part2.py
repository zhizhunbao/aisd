"""
CST8507 Lab 3 Part 2: Word Embedding Similarity Using FastText
Author: Peng Wang
Student Number: 041107730

Explore FastText sub-word modeling for word analogies and misspelling handling.
Compare Word2Vec and FastText on their ability to process misspelled words
using cosine similarity.
"""

# ================================================================
# 导入模块
# Import Modules
# ================================================================

import os

from dotenv import load_dotenv
import fasttext
import fasttext.util
import gensim.downloader as api
import numpy as np
from tabulate import tabulate


# ============================================================
# 环境设置
# Environment Setup
# ============================================================

# 加载环境变量
# Load environment variables
load_dotenv('.env.local')
STUDENT_NAME = os.getenv('NAME', 'Peng Wang')
STUDENT_NUMBER = os.getenv('NUMBER', '041107730')

# 打印程序标题
# Print program header
print("=" * 60)
print("CST8507 Lab 3 Part 2: Word Embedding with FastText")
print(f"Author: {STUDENT_NAME} ({STUDENT_NUMBER})")
print("=" * 60)
print()

# ============================================================
# 步骤 1：加载预训练 FastText 模型
# Step 1: Load Pre-trained FastText Model
# ============================================================

# ================================================================
# 概念：FastText 子词建模 (Sub-word Modeling)
# Concept: FastText Sub-word Modeling
# ================================================================
#
# -------- 术语解释 / Terminology --------
#
# 【子词 Sub-word / Character n-gram】
#   将词拆分为字符级别的片段，如 "apple" → ["<ap", "app", "ppl", "ple", "le>"]
#   Split words into character-level fragments
#
# 【OOV (Out-of-Vocabulary)】
#   不在训练词汇表中的词，传统模型无法处理
#   Words not in training vocabulary, traditional models cannot handle them
#
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   FastText 将每个词表示为字符 n-gram 向量的和，能处理未见过的词
#   FastText represents each word as sum of character n-gram vectors, handles unseen words
#
# 公式 / Formula:
#   vec("apple") = vec("<ap") + vec("app") + vec("ppl") + vec("ple") + vec("le>")
#
# 举例 / Example:
#   "appple"（拼写错误）与 "apple" 共享大部分 n-gram
#   因此 FastText 仍能为拼写错误的词生成合理的向量
#   "appple" (misspelled) shares most n-grams with "apple"
#   So FastText can still generate reasonable vectors for misspelled words
#
# 优点 / Advantages:
#   - 能处理 OOV 词（拼写错误、罕见词、新词）
#   - 对形态丰富的语言效果更好
# ================================================================

print("=" * 60)
print("Step 1: Load Pre-trained FastText Model")
print("=" * 60)

# 下载并加载 FastText 英文预训练模型（cc.en.300.bin）
# Download and load FastText English pre-trained model (cc.en.300.bin)
# 原因：包含 200 万词的 300 维向量，支持子词信息
# Reason: Contains 300-dim vectors for 2M words, supports sub-word information
fasttext.util.download_model('en', if_exists='ignore')
ft_model = fasttext.load_model('cc.en.300.bin')

print(f"  Vector dimension: {ft_model.get_dimension()}")
print(f"  Number of words: {len(ft_model.get_words()):,}")
print()


# ============================================================
# 步骤 2：检查词类比
# Step 2: Check Word Analogies
# ============================================================

print("=" * 60)
print("Step 2: Check Word Analogies")
print("=" * 60)

# 词类比列表：A - B + C = ?
# Word analogy list: A - B + C = ?
# 格式：(positive_words, negative_word, description)
# Format: (positive_words, negative_word, description)
analogies = [
    (['king', 'woman'], 'man', 'King - Man + Woman'),
    (['computer_programmer', 'woman'], 'man', 'Computer Programmer - Man + Woman'),
    (['doctor', 'woman'], 'man', 'Doctor - Man + Woman'),
    (['career', 'woman'], 'man', 'Career - Man + Woman'),
    (['intelligent', 'woman'], 'scientist', 'Intelligent - Scientist + Woman'),
]

# 存储所有类比结果用于 Step 3 汇总
# Store all analogy results for Step 3 summary
analogy_results = []

# 对每个类比计算结果
# Compute result for each analogy
for positive, negative, description in analogies:
    print(f"\n{description} = ?")

    # 使用 FastText 的 get_analogies 方法
    # Use FastText get_analogies method
    # FastText 原生 API：get_analogies(A, B, C) 计算 B - A + C
    # FastText native API: get_analogies(A, B, C) computes B - A + C
    # 我们需要：positive[0] - negative + positive[1]
    # We need: positive[0] - negative + positive[1]
    # 手动计算向量类比
    # Manually compute vector analogy
    result_vec = (
        ft_model.get_word_vector(positive[0])
        - ft_model.get_word_vector(negative)
        + ft_model.get_word_vector(positive[1])
    )

    # 归一化结果向量
    # Normalize result vector
    result_vec = result_vec / np.linalg.norm(result_vec)

    # 在词汇表中找最近邻（排除输入词）
    # Find nearest neighbors in vocabulary (excluding input words)
    # 使用 FastText 的 get_nearest_neighbors 不支持自定义向量
    # get_nearest_neighbors doesn't support custom vectors
    # 手动计算与所有词的相似度
    # Manually compute similarity with all words
    exclude_words = set(positive + [negative])

    # 获取候选词（使用模型词汇表的子集以提高效率）
    # Get candidate words (use subset of model vocabulary for efficiency)
    # 原因：完整词汇表太大，取前 50000 个高频词
    # Reason: Full vocabulary too large, use top 50000 frequent words
    CANDIDATE_LIMIT = 50000
    candidates = ft_model.get_words()[:CANDIDATE_LIMIT]

    # 计算余弦相似度
    # Compute cosine similarity
    best_word = None
    best_sim = -1.0
    top_results = []

    for word in candidates:
        if word in exclude_words:
            continue

        # 获取候选词向量并归一化
        # Get candidate word vector and normalize
        word_vec = ft_model.get_word_vector(word)
        word_vec_norm = word_vec / np.linalg.norm(word_vec)

        # 余弦相似度（两个归一化向量的点积）
        # Cosine similarity (dot product of two normalized vectors)
        sim = float(np.dot(result_vec, word_vec_norm))

        top_results.append((word, sim))

    # 按相似度降序排列，取前 5 个
    # Sort by similarity descending, take top 5
    top_results.sort(key=lambda x: x[1], reverse=True)

    print(f"  Top 5 results:")
    for word, sim in top_results[:5]:
        print(f"    {word:20s}  similarity: {sim:.4f}")

    # 保存第一名结果用于 Step 3 汇总表格
    # Save top-1 result for Step 3 summary table
    analogy_results.append((description, top_results[0][0], top_results[0][1]))

print()


# ============================================================
# 步骤 3：结果与讨论
# Step 3: Results and Discussion
# ============================================================

print("=" * 60)
print("Step 3: Results and Discussion")
print("=" * 60)

# 汇总表格：类比结果
# Summary table: analogy results
table_data = [[desc, word, f"{sim:.4f}"] for desc, word, sim in analogy_results]
headers = ['Analogy', 'Top Result', 'Similarity']
print(tabulate(table_data, headers=headers, tablefmt='simple'))
print()

print("Observations:")
print()
print("1. Classic Analogy Success:")
print("   'King - Man + Woman = Queen' works well (similarity ~0.65),")
print("   confirming that FastText captures basic gender relationships.")
print()
print("2. Gender Bias in Word Embeddings:")
print("   'Computer Programmer - Man + Woman' yields Nursing/Breastfeeding,")
print("   and 'Doctor - Man + Woman' yields pediatrician/midwife.")
print("   These results reflect gender stereotypes in the training data,")
print("   associating female-related vectors with caregiving professions.")
print()
print("3. Semantic Drift in Abstract Analogies:")
print("   'Intelligent - Scientist + Woman' returns man/lady/women rather")
print("   than an intelligence-related word. Subtracting 'scientist' removes")
print("   too much semantic content, leaving mostly the 'person' component.")
print()

# ============================================================
# 步骤 4：比较 Word2Vec 和 FastText 处理拼写错误
# Step 4: Comparing Word2Vec and FastText for Handling Misspellings
# ============================================================

print("=" * 60)
print("Step 4: Comparing Word2Vec and FastText for Handling Misspellings")
print("=" * 60)

# 加载 Word2Vec 模型用于对比
# Load Word2Vec model for comparison
print("Loading Word2Vec (word2vec-google-news-300)...")
w2v_model = api.load('word2vec-google-news-300')
print(f"  Vocabulary size: {len(w2v_model.key_to_index):,}")
print()

# 测试词列表：正确拼写和拼写错误的变体
# Test word list: correctly spelled words and misspelled variants
test_words = {
    "correct": ["apple", "banana", "computer", "science", "education"],
    "misspelled": ["appple", "bananna", "computar", "sciience", "edcation"]
}


def compute_similarity(correct_word, misspelled_word, model, model_name):
    """计算正确词和拼写错误词之间的余弦相似度
    Compute cosine similarity between correct and misspelled word"""

    if model_name == 'FastText':
        # FastText 可以为任何词生成向量（包括 OOV 词）
        # FastText can generate vectors for any word (including OOV words)
        vec_correct = model.get_word_vector(correct_word)
        vec_misspelled = model.get_word_vector(misspelled_word)

        # 计算余弦相似度
        # Compute cosine similarity
        norm_correct = np.linalg.norm(vec_correct)
        norm_misspelled = np.linalg.norm(vec_misspelled)

        # 避免除以零
        # Avoid division by zero
        if norm_correct == 0 or norm_misspelled == 0:
            return None

        similarity = float(np.dot(vec_correct, vec_misspelled) / (norm_correct * norm_misspelled))
        return similarity

    else:
        # Word2Vec：如果词不在词汇表中，返回 None
        # Word2Vec: if word not in vocabulary, return None
        if correct_word not in model.key_to_index or misspelled_word not in model.key_to_index:
            return None

        return float(model.similarity(correct_word, misspelled_word))


# ============================================================
# 步骤 5：结果格式
# Step 5: Results Format
# ============================================================

print("=" * 60)
print("Step 5: Results Format")
print("=" * 60)
print()

# 对每对正确/拼写错误的词计算相似度
# Compute similarity for each correct/misspelled pair
for correct, misspelled in zip(test_words["correct"], test_words["misspelled"]):
    print(f"Correct: {correct}, Misspelled: {misspelled}")

    # Word2Vec 相似度
    # Word2Vec similarity
    w2v_sim = compute_similarity(correct, misspelled, w2v_model, 'Word2Vec')
    if w2v_sim is not None:
        print(f"  Word2Vec Similarity: {w2v_sim:.4f}")
    else:
        print(f"  Word2Vec Similarity: N/A (word not in vocabulary)")

    # FastText 相似度
    # FastText similarity
    ft_sim = compute_similarity(correct, misspelled, ft_model, 'FastText')
    if ft_sim is not None:
        print(f"  FastText Similarity: {ft_sim:.4f}")
    else:
        print(f"  FastText Similarity: N/A")

    print()

# 总结对比
# Summary comparison
print("-" * 40)
print("Summary:")
print("  Word2Vec cannot handle misspelled words that are not in its")
print("  vocabulary, returning N/A. FastText leverages sub-word (character")
print("  n-gram) information to generate meaningful vectors even for")
print("  misspelled words, resulting in high similarity scores between")
print("  correct and misspelled variants.")
print()
