"""
CST8507 Lab 3 Part 2: Word Embedding Similarity Using FastText
Author: Peng Wang
Student Number: 041107730

Explore FastText sub-word modeling for word analogies, and compare
Word2Vec vs FastText performance on handling misspelled words.
"""

# ============================================================
# 模块导入
# Module Imports
# ============================================================

import os
import numpy as np
import fasttext
import fasttext.util
import gensim.downloader as api

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 输出图片目录
# Output images directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'lab3_images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# FastText 模型文件路径（下载到脚本所在目录）
# FastText model file path (downloaded to script directory)
FASTTEXT_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'cc.en.300.bin')

# ============================================================
# 步骤 1：加载预训练 FastText 模型
# Step 1: Load the Pre-trained FastText Model
# ============================================================

print("=" * 60)
print("Step 1: Loading Pre-trained FastText Model (cc.en.300.bin)")
print("=" * 60)

# 如果模型文件不存在，使用 fasttext.util 下载
# If model file does not exist, download using fasttext.util
if not os.path.exists(FASTTEXT_MODEL_PATH):
    print("Downloading FastText cc.en.300.bin model...")
    # 切换到脚本目录以便模型下载到正确位置
    # Switch to script directory so model downloads to the correct location
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    fasttext.util.download_model('en', if_exists='ignore')
    os.chdir(original_dir)

# 加载 FastText 模型
# Load FastText model
ft_model = fasttext.load_model(FASTTEXT_MODEL_PATH)
print(f"FastText model loaded: {ft_model.get_dimension()}d vectors")
print()

# ============================================================
# 步骤 2：检查词类比
# Step 2: Check Word Analogies
# ============================================================

print("=" * 60)
print("Step 2: Word Analogies using FastText")
print("=" * 60)


def compute_analogy_fasttext(model, word_a, word_b, word_c):
    """
    计算词类比: word_a - word_b + word_c = ?
    Compute word analogy: word_a - word_b + word_c = ?

    使用向量运算: result_vector = vec(word_a) - vec(word_b) + vec(word_c)
    Uses vector arithmetic: result_vector = vec(word_a) - vec(word_b) + vec(word_c)
    然后找到最近邻
    Then finds the nearest neighbor
    """
    # 获取词向量并进行向量运算
    # Get word vectors and perform vector arithmetic
    vec_a = model.get_word_vector(word_a)
    vec_b = model.get_word_vector(word_b)
    vec_c = model.get_word_vector(word_c)
    result_vec = vec_a - vec_b + vec_c

    # 使用 get_nearest_neighbors 找到最近的词
    # Use get_nearest_neighbors to find the closest word
    # FastText 的 get_nearest_neighbors 需要传入向量，但官方 API 不直接支持
    # FastText's get_nearest_neighbors doesn't directly support passing a vector
    # 因此我们使用 get_nearest_neighbors 对结果词检查相似度
    # So we use a manual approach to find the nearest word
    neighbors = model.get_nearest_neighbors(word_a, k=100)

    # 手动计算与结果向量的余弦相似度
    # Manually compute cosine similarity with the result vector
    result_norm = result_vec / (np.linalg.norm(result_vec) + 1e-10)

    best_word = None
    best_sim = -1
    # 搜索大范围的词汇来找到最佳匹配
    # Search a broad range of words to find the best match
    # 使用输入词的近邻作为候选集
    # Use neighbors of input words as candidate set
    candidate_words = set()
    for word in [word_a, word_b, word_c]:
        for sim, w in model.get_nearest_neighbors(word, k=50):
            candidate_words.add(w)

    # 排除输入词
    # Exclude input words
    exclude = {word_a.lower(), word_b.lower(), word_c.lower()}

    for w in candidate_words:
        if w.lower() in exclude:
            continue
        w_vec = model.get_word_vector(w)
        w_norm = w_vec / (np.linalg.norm(w_vec) + 1e-10)
        sim = np.dot(result_norm, w_norm)
        if sim > best_sim:
            best_sim = sim
            best_word = w

    return best_word, best_sim


# 定义类比任务列表
# Define list of analogy tasks
analogies = [
    ("king", "man", "woman"),
    ("computer_programmer", "man", "woman"),
    ("doctor", "man", "woman"),
    ("career", "man", "woman"),
    ("intelligent", "scientist", "woman"),
]

# 显示格式化标题
# Display formatted header
print(f"{'Analogy':<45} {'Result':<20} {'Similarity':>10}")
print("-" * 75)

# 对每个类比任务计算结果
# Compute result for each analogy task
analogy_results = []
for word_a, word_b, word_c in analogies:
    result_word, similarity = compute_analogy_fasttext(ft_model, word_a, word_b, word_c)
    analogy_str = f"{word_a} - {word_b} + {word_c}"
    print(f"{analogy_str:<45} {result_word:<20} {similarity:>10.4f}")
    analogy_results.append((analogy_str, result_word, similarity))

print()

# ============================================================
# 步骤 3：结果与讨论
# Step 3: Results and Discussion
# ============================================================

print("=" * 60)
print("Step 3: Results and Discussion")
print("=" * 60)

print("\nWord Analogy Results Summary:")
print(f"{'Analogy':<45} {'= Result':<20}")
print("-" * 65)
for analogy_str, result_word, sim in analogy_results:
    print(f"{analogy_str:<45} = {result_word:<20}")

print()
print("Observations:")
print("  1. The classic 'king - man + woman' analogy tests whether the model")
print("     captures gender relationships in word embeddings.")
print("  2. Analogies involving profession terms (doctor, computer_programmer)")
print("     may reveal gender biases present in the training data.")
print("  3. The 'career - man + woman' analogy explores gender associations")
print("     with career-related concepts in the embedding space.")
print("  4. FastText's sub-word modeling allows it to handle compound words")
print("     and morphological variations better than traditional Word2Vec.")
print()

# ============================================================
# 步骤 4：比较 Word2Vec 和 FastText 处理拼写错误
# Step 4: Comparing Word2Vec and FastText for Handling Misspellings
# ============================================================

print("=" * 60)
print("Step 4: Comparing Word2Vec and FastText for Misspellings")
print("=" * 60)

# 加载 Word2Vec 模型用于比较
# Load Word2Vec model for comparison
print("\nLoading Word2Vec model for comparison...")
w2v_model = api.load('word2vec-google-news-300')
print(f"Word2Vec loaded: {len(w2v_model)} words, {w2v_model.vector_size}d vectors")
print()

# 创建测试词列表
# Create test word list
test_words = {
    "correct": ["apple", "banana", "computer", "science", "education"],
    "misspelled": ["appple", "bananna", "computar", "sciience", "edcation"]
}


def cosine_similarity_vectors(vec1, vec2):
    """
    计算两个向量之间的余弦相似度
    Compute cosine similarity between two vectors
    """
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def calc_w2v_similarity(model, word1, word2):
    """
    使用 Word2Vec 计算词对的余弦相似度
    Calculate cosine similarity between word pair using Word2Vec

    如果任一词不在词汇表中，返回 None
    If either word is missing from vocabulary, return None
    """
    if word1 not in model or word2 not in model:
        return None
    return model.similarity(word1, word2)


def calc_fasttext_similarity(model, word1, word2):
    """
    使用 FastText 计算词对的余弦相似度
    Calculate cosine similarity between word pair using FastText

    FastText 可以生成任何词的向量（包括 OOV 词）
    FastText can generate vectors for any word (including OOV words)
    """
    vec1 = model.get_word_vector(word1)
    vec2 = model.get_word_vector(word2)
    return cosine_similarity_vectors(vec1, vec2)


# ============================================================
# 步骤 5：结果格式
# Step 5: Results Format
# ============================================================

print("=" * 60)
print("Step 5: Misspelling Comparison Results")
print("=" * 60)
print()

# 对每对正确/拼写错误的词计算相似度
# Compute similarity for each correct/misspelled word pair
for correct, misspelled in zip(test_words["correct"], test_words["misspelled"]):
    # Word2Vec 相似度
    # Word2Vec similarity
    w2v_sim = calc_w2v_similarity(w2v_model, correct, misspelled)

    # FastText 相似度
    # FastText similarity
    ft_sim = calc_fasttext_similarity(ft_model, correct, misspelled)

    print(f"Correct: {correct}, Misspelled: {misspelled}")
    if w2v_sim is not None:
        print(f"  Word2Vec Similarity: {w2v_sim:.4f}")
    else:
        print(f"  Word2Vec Similarity: N/A (word not in vocabulary)")
    print(f"  FastText Similarity: {ft_sim:.4f}")
    print()

# 总结讨论
# Summary discussion
print("=" * 60)
print("Discussion: Word2Vec vs FastText on Misspellings")
print("=" * 60)
print()
print("Key Observations:")
print("  1. Word2Vec relies on whole-word lookup. If a misspelled word is not")
print("     in its vocabulary, it cannot compute a similarity score (returns N/A).")
print("  2. FastText uses sub-word (character n-gram) information, allowing it")
print("     to generate meaningful vectors even for misspelled or OOV words.")
print("  3. FastText similarity scores for correct vs misspelled pairs tend to")
print("     be high, demonstrating its robustness to spelling errors.")
print("  4. This sub-word capability makes FastText particularly valuable for")
print("     real-world NLP applications where noisy text is common.")
print()
print("=" * 60)
print("Lab 3 Part 2 Complete")
print("=" * 60)
