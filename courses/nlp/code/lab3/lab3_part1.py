"""
CST8507 Lab 3 Part 1: Evaluating Semantic Similarity with Human Judgments
Author: Peng Wang
Student Number: 041107730

Evaluate how well Word2Vec and GloVe pre-trained word embeddings capture
human-judged semantic similarity using the SimLex-999 benchmark dataset.
Compare embedding-based cosine similarity scores against human annotations.
"""

# ================================================================
# 导入模块
# Import Modules
# ================================================================

import os

from dotenv import load_dotenv
import pandas as pd
import gensim.downloader as api
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

# SimLex-999 数据集路径（兼容脚本和 Notebook 两种运行方式）
# SimLex-999 dataset path (compatible with both script and Notebook execution)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
SIMLEX_PATH = os.path.join(SCRIPT_DIR, '..', '..', 'labs', 'SimLex-999.txt')

# 高相似度词对数量
# Number of top similar word pairs to select
TOP_N = 60

# 设置 pandas 显示选项
# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)

# 打印程序标题
# Print program header
print("=" * 60)
print("CST8507 Lab 3 Part 1: Evaluating Semantic Similarity")
print(f"Author: {STUDENT_NAME} ({STUDENT_NUMBER})")
print("=" * 60)
print()

# ============================================================
# 步骤 1：探索数据
# Step 1: Explore Your Data
# ============================================================

# 加载 SimLex-999 数据集（制表符分隔文件）
# Load SimLex-999 dataset (tab-separated file)
df = pd.read_csv(SIMLEX_PATH, sep='\t')

# 选择所需的三列：word1, word2, SimLex999
# Select the three required columns: word1, word2, SimLex999
df_selected = df[['word1', 'word2', 'SimLex999']].copy()

# 显示数据集基本信息
# Display basic dataset information
print("=" * 60)
print("Step 1: Explore Your Data")
print("=" * 60)
print(f"Total word pairs: {len(df_selected)}")
print()

# 显示前 5 行数据
# Display first 5 rows
print("First 5 word pairs:")
print(df_selected.head())
print()

# 计算并显示 SimLex999 相似度列的最小值、平均值和最大值
# Compute and display min, average, and max similarity values
sim_min = df_selected['SimLex999'].min()
sim_avg = df_selected['SimLex999'].mean()
sim_max = df_selected['SimLex999'].max()

print(f"Minimum similarity: {sim_min:.2f}")
print(f"Average similarity: {sim_avg:.2f}")
print(f"Maximum similarity: {sim_max:.2f}")
print()


# ============================================================
# 步骤 2：选择高相似度词对
# Step 2: Select Highly Similar Word Pairs
# ============================================================

# 按 SimLex999 相似度分数降序排列
# Sort by SimLex999 similarity score in descending order
df_sorted = df_selected.sort_values('SimLex999', ascending=False)

# 选择相似度最高的前 60 个词对
# Select top 60 word pairs with highest similarity scores
df_top60 = df_sorted.head(TOP_N).reset_index(drop=True)

print("=" * 60)
print("Step 2: Select Highly Similar Word Pairs")
print("=" * 60)
print(f"Top {TOP_N} word pairs (sorted by SimLex999 descending):")
print(df_top60.to_string(index=True))
print()

# ============================================================
# 步骤 3：加载两个预训练词嵌入模型
# Step 3: Load Two Pre-trained Word Embedding Models
# ============================================================

# ================================================================
# 概念：词嵌入 (Word Embedding)
# Concept: Word Embedding
# ================================================================
#
# -------- 术语解释 / Terminology --------
#
# 【Word2Vec】
#   Google 提出的词嵌入模型，在 Google News 数据集上训练
#   Word embedding model by Google, trained on Google News dataset
#
# 【GloVe (Global Vectors)】
#   Stanford 提出的词嵌入模型，基于全局词共现矩阵
#   Word embedding model by Stanford, based on global word co-occurrence matrix
#
# 【余弦相似度 Cosine Similarity】
#   衡量两个向量方向的相似程度，值域 [-1, 1]
#   Measures directional similarity between two vectors, range [-1, 1]
#
# -------- 算法原理 / Algorithm --------
#
# 定义 / Definition:
#   将词映射到高维向量空间，语义相似的词在空间中距离更近
#   Map words to high-dimensional vector space, semantically similar words are closer
#
# 公式 / Formula:
#   cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
#
# 举例 / Example:
#   vec("king") 和 vec("queen") 的余弦相似度约 0.65
#   vec("king") - vec("man") + vec("woman") ≈ vec("queen")
#
# 优点 / Advantages:
#   - 捕捉词的语义关系和类比关系
#   - 预训练模型可直接使用，无需重新训练
# ================================================================

print("=" * 60)
print("Step 3: Load Two Pre-trained Word Embedding Models")
print("=" * 60)

# 加载 Word2Vec 模型（word2vec-google-news-300）
# Load Word2Vec model (word2vec-google-news-300)
# 原因：300 维向量，在约 1000 亿词的 Google News 上训练
# Reason: 300-dimensional vectors, trained on ~100 billion words from Google News
print("Loading Word2Vec (word2vec-google-news-300)...")
w2v_model = api.load('word2vec-google-news-300')
print(f"  Vocabulary size: {len(w2v_model.key_to_index):,}")
print(f"  Vector dimension: {w2v_model.vector_size}")
print()

# 加载 GloVe 模型（glove-wiki-gigaword-300）
# Load GloVe model (glove-wiki-gigaword-300)
# 原因：300 维向量，在 Wikipedia + Gigaword 语料上训练
# Reason: 300-dimensional vectors, trained on Wikipedia + Gigaword corpus
print("Loading GloVe (glove-wiki-gigaword-300)...")
glove_model = api.load('glove-wiki-gigaword-300')
print(f"  Vocabulary size: {len(glove_model.key_to_index):,}")
print(f"  Vector dimension: {glove_model.vector_size}")
print()


# ============================================================
# 步骤 4：计算基于嵌入的相似度
# Step 4: Computing Embedding-Based Similarity
# ============================================================

print("=" * 60)
print("Step 4: Computing Embedding-Based Similarity")
print("=" * 60)

# 存储结果的列表
# List to store results
results = []

# 对前 60 个词对分别计算 Word2Vec 和 GloVe 的余弦相似度
# Compute cosine similarity using Word2Vec and GloVe for top 60 pairs
for _, row in df_top60.iterrows():
    w1 = row['word1']
    w2 = row['word2']
    simlex_score = row['SimLex999']

    # 计算 Word2Vec 相似度
    # Compute Word2Vec similarity
    # 如果词不在词汇表中，返回 None
    # If word not in vocabulary, return None
    if w1 in w2v_model.key_to_index and w2 in w2v_model.key_to_index:
        sim_w2v = w2v_model.similarity(w1, w2)
    else:
        sim_w2v = None

    # 计算 GloVe 相似度
    # Compute GloVe similarity
    if w1 in glove_model.key_to_index and w2 in glove_model.key_to_index:
        sim_glove = glove_model.similarity(w1, w2)
    else:
        sim_glove = None

    results.append({
        'word1': w1,
        'word2': w2,
        'similarity_w2v': sim_w2v,
        'similarity_glove': sim_glove,
        'SimLex999': simlex_score,
    })

# 创建结果 DataFrame
# Create results DataFrame
df_results = pd.DataFrame(results)

# 统计词汇覆盖情况
# Count vocabulary coverage
w2v_missing = df_results['similarity_w2v'].isna().sum()
glove_missing = df_results['similarity_glove'].isna().sum()
print(f"Word2Vec: {TOP_N - w2v_missing}/{TOP_N} pairs computed ({w2v_missing} missing)")
print(f"GloVe:    {TOP_N - glove_missing}/{TOP_N} pairs computed ({glove_missing} missing)")
print()

# ============================================================
# 步骤 5：结果表格
# Step 5: Results Table
# ============================================================

print("=" * 60)
print("Step 5: Results Table")
print("=" * 60)

# 格式化结果表格
# Format results table
table_data = []
for _, row in df_results.iterrows():
    # 格式化相似度分数，None 显示为 "N/A"
    # Format similarity scores, None displayed as "N/A"
    w2v_str = f"{row['similarity_w2v']:.4f}" if row['similarity_w2v'] is not None else "N/A"
    glove_str = f"{row['similarity_glove']:.4f}" if row['similarity_glove'] is not None else "N/A"

    table_data.append([
        row['word1'],
        row['word2'],
        w2v_str,
        glove_str,
        f"{row['SimLex999']:.2f}",
    ])

# 使用 tabulate 打印格式化表格
# Print formatted table using tabulate
headers = ['word1', 'word2', 'similarity_w2v', 'similarity_glove', 'SimLex999']
print(tabulate(table_data, headers=headers, tablefmt='simple'))
print()


# ============================================================
# 步骤 6：分析与讨论
# Step 6: Analysis and Discussion
# ============================================================

print("=" * 60)
print("Step 6: Analysis and Discussion")
print("=" * 60)

# ----------------------------------------
# 步骤 6.1：计算整体相关性
# Step 6.1: Compute overall correlation
# ----------------------------------------

# 过滤掉缺失值后计算 Pearson 相关系数
# Compute Pearson correlation after filtering missing values
df_valid_w2v = df_results.dropna(subset=['similarity_w2v'])
df_valid_glove = df_results.dropna(subset=['similarity_glove'])

# Word2Vec 与 SimLex999 的相关性
# Correlation between Word2Vec and SimLex999
corr_w2v = df_valid_w2v['similarity_w2v'].corr(df_valid_w2v['SimLex999'])

# GloVe 与 SimLex999 的相关性
# Correlation between GloVe and SimLex999
corr_glove = df_valid_glove['similarity_glove'].corr(df_valid_glove['SimLex999'])

print("Pearson Correlation with SimLex999 (top 60 pairs):")
print(f"  Word2Vec: {corr_w2v:.4f}")
print(f"  GloVe:    {corr_glove:.4f}")
print()

# 判断哪个模型更好
# Determine which model aligns better
if corr_w2v > corr_glove:
    print("Word2Vec shows higher correlation with human judgments for the top-60 pairs.")
else:
    print("GloVe shows higher correlation with human judgments for the top-60 pairs.")
print()

# ----------------------------------------
# 步骤 6.2：嵌入低估人类相似度的示例
# Step 6.2: Examples where embeddings underestimate human similarity
# ----------------------------------------

print("Examples where embeddings underestimate human similarity:")
print("-" * 40)

# 找出 SimLex999 分数高但嵌入相似度低的词对
# Find pairs with high SimLex999 but low embedding similarity
# 使用 SimLex999 归一化到 [0,1] 范围进行比较
# Normalize SimLex999 to [0,1] range for comparison
df_analysis = df_results.copy()
df_analysis['simlex_norm'] = df_analysis['SimLex999'] / 10.0

# Word2Vec 低估的示例（差值最大的前 5 个）
# Word2Vec underestimation examples (top 5 largest gaps)
df_w2v_valid = df_analysis.dropna(subset=['similarity_w2v']).copy()
df_w2v_valid['gap_w2v'] = df_w2v_valid['simlex_norm'] - df_w2v_valid['similarity_w2v']
underest_w2v = df_w2v_valid.nlargest(5, 'gap_w2v')

print("\nWord2Vec underestimates (largest gaps):")
for _, row in underest_w2v.iterrows():
    print(f"  {row['word1']:12s} - {row['word2']:12s}  "
          f"SimLex={row['SimLex999']:.2f}  W2V={row['similarity_w2v']:.4f}  "
          f"Gap={row['gap_w2v']:.4f}")

# GloVe 低估的示例
# GloVe underestimation examples
df_glove_valid = df_analysis.dropna(subset=['similarity_glove']).copy()
df_glove_valid['gap_glove'] = df_glove_valid['simlex_norm'] - df_glove_valid['similarity_glove']
underest_glove = df_glove_valid.nlargest(5, 'gap_glove')

print("\nGloVe underestimates (largest gaps):")
for _, row in underest_glove.iterrows():
    print(f"  {row['word1']:12s} - {row['word2']:12s}  "
          f"SimLex={row['SimLex999']:.2f}  GloVe={row['similarity_glove']:.4f}  "
          f"Gap={row['gap_glove']:.4f}")
print()

# ----------------------------------------
# 步骤 6.3：Word2Vec 与 GloVe 行为比较
# Step 6.3: Compare Word2Vec and GloVe behavior
# ----------------------------------------

print("Word2Vec vs GloVe Comparison:")
print("-" * 40)

# 计算两个模型的平均相似度
# Compute average similarity for both models
avg_w2v = df_valid_w2v['similarity_w2v'].mean()
avg_glove = df_valid_glove['similarity_glove'].mean()

print(f"  Average similarity (Word2Vec): {avg_w2v:.4f}")
print(f"  Average similarity (GloVe):    {avg_glove:.4f}")
print()

# 找出两个模型差异最大的词对
# Find pairs with largest difference between models
df_both = df_results.dropna(subset=['similarity_w2v', 'similarity_glove']).copy()
df_both['model_diff'] = abs(df_both['similarity_w2v'] - df_both['similarity_glove'])
top_diff = df_both.nlargest(5, 'model_diff')

print("Pairs with largest difference between Word2Vec and GloVe:")
for _, row in top_diff.iterrows():
    print(f"  {row['word1']:12s} - {row['word2']:12s}  "
          f"W2V={row['similarity_w2v']:.4f}  GloVe={row['similarity_glove']:.4f}  "
          f"Diff={row['model_diff']:.4f}")
print()
