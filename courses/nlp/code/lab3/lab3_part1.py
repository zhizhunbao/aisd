"""
CST8507 Lab 3 Part 1: Evaluating Semantic Similarity with Human Judgments
Author: Peng Wang
Student Number: 041107730

Evaluate how well Word2Vec and GloVe pre-trained word embedding models
capture human-judged semantic similarity using the SimLex-999 benchmark.
"""

# ============================================================
# 模块导入
# Module Imports
# ============================================================

import os
import pandas as pd
import numpy as np
import gensim.downloader as api
from scipy.stats import spearmanr

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# SimLex-999 数据文件路径
# Path to the SimLex-999 dataset file
SIMLEX_FILE = os.path.join(
    os.path.dirname(__file__), '..', '..', 'labs', 'SimLex-999.txt'
)

# 选取的高相似度词对数量
# Number of top similar word pairs to select
TOP_N = 60

# 输出图片目录
# Output images directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'lab3_images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 步骤 1：探索数据
# Step 1: Explore Your Data
# ============================================================

# 加载 SimLex-999 数据集（制表符分隔）
# Load the SimLex-999 dataset (tab-separated)
df = pd.read_csv(SIMLEX_FILE, sep='\t')

# 选取 word1、word2 和 SimLex999 三列
# Select the three columns: word1, word2, and SimLex999
df_selected = df[['word1', 'word2', 'SimLex999']].copy()

# 计算并显示 SimLex999 相似度列的最小值、平均值和最大值
# Compute and display min, average, and max similarity values
sim_min = df_selected['SimLex999'].min()
sim_avg = df_selected['SimLex999'].mean()
sim_max = df_selected['SimLex999'].max()

print("=" * 60)
print("Step 1: SimLex-999 Dataset Statistics")
print("=" * 60)
print(f"Total word pairs: {len(df_selected)}")
print(f"Minimum similarity: {sim_min:.2f}")
print(f"Average similarity: {sim_avg:.2f}")
print(f"Maximum similarity: {sim_max:.2f}")
print()

# 显示数据前 5 行
# Display the first 5 rows
print("First 5 rows of the dataset:")
print(df_selected.head().to_string(index=False))
print()

# ============================================================
# 步骤 2：选择高相似度词对
# Step 2: Select Highly Similar Word Pairs
# ============================================================

# 按 SimLex999 分数降序排列
# Sort by SimLex999 similarity score in descending order
df_sorted = df_selected.sort_values(by='SimLex999', ascending=False)

# 选取相似度最高的前 60 个词对
# Select the top 60 word pairs with the highest similarity scores
top_60 = df_sorted.head(TOP_N).reset_index(drop=True)

print("=" * 60)
print(f"Step 2: Top {TOP_N} Word Pairs (Highest SimLex999 Scores)")
print("=" * 60)
print(top_60.to_string(index=False))
print()

# ============================================================
# 步骤 3：加载预训练词嵌入模型
# Step 3: Load Two Pre-trained Word Embedding Models
# ============================================================

# 加载 Word2Vec 模型（Google News 300维）
# Load Word2Vec model (Google News 300-dimensional)
print("=" * 60)
print("Step 3: Loading Pre-trained Word Embedding Models")
print("=" * 60)
print("Loading Word2Vec (word2vec-google-news-300)...")
w2v_model = api.load('word2vec-google-news-300')
print(f"  Word2Vec loaded: {len(w2v_model)} words, {w2v_model.vector_size}d vectors")

# 加载 GloVe 模型（Wikipedia + Gigaword 300维）
# Load GloVe model (Wikipedia + Gigaword 300-dimensional)
print("Loading GloVe (glove-wiki-gigaword-300)...")
glove_model = api.load('glove-wiki-gigaword-300')
print(f"  GloVe loaded: {len(glove_model)} words, {glove_model.vector_size}d vectors")
print()

# ============================================================
# 步骤 4：计算基于嵌入的相似度
# Step 4: Computing Embedding-Based Similarity
# ============================================================

# 定义计算相似度的函数
# Define a function to compute similarity
def compute_similarity(model, word1, word2):
    """
    计算两个词之间的余弦相似度
    Compute cosine similarity between two words using a given model
    """
    try:
        return model.similarity(word1, word2)
    except KeyError:
        return None

# 对前 60 个词对分别计算 Word2Vec 和 GloVe 相似度
# Compute Word2Vec and GloVe similarity for each of the top 60 pairs
w2v_similarities = []
glove_similarities = []

for _, row in top_60.iterrows():
    w1, w2 = row['word1'], row['word2']

    # Word2Vec 相似度
    # Word2Vec similarity
    w2v_sim = compute_similarity(w2v_model, w1, w2)
    w2v_similarities.append(w2v_sim)

    # GloVe 相似度
    # GloVe similarity
    glove_sim = compute_similarity(glove_model, w1, w2)
    glove_similarities.append(glove_sim)

# 将结果添加到 DataFrame
# Add results to the DataFrame
top_60['similarity_w2v'] = w2v_similarities
top_60['similarity_glove'] = glove_similarities

# ============================================================
# 步骤 5：结果格式
# Step 5: Results Format
# ============================================================

# 创建结果表格
# Create and display the results table
print("=" * 60)
print("Step 5: Results Table")
print("=" * 60)

# 格式化显示表格
# Format display table
results_display = top_60.copy()
results_display.columns = ['word1', 'word2', 'similarity_SimLex999',
                            'similarity_w2v', 'similarity_glove']

# 格式化数值为 4 位小数
# Format numeric values to 4 decimal places
for col in ['similarity_SimLex999', 'similarity_w2v', 'similarity_glove']:
    results_display[col] = results_display[col].apply(
        lambda x: f"{x:.4f}" if x is not None else "N/A"
    )

print(results_display.to_string(index=False))
print()

# ============================================================
# 步骤 6：分析与讨论
# Step 6: Analysis and Discussion
# ============================================================

print("=" * 60)
print("Step 6: Analysis and Discussion")
print("=" * 60)

# 过滤掉包含 None 的行以便分析
# Filter out rows with None values for analysis
valid_mask = (top_60['similarity_w2v'].notna()) & (top_60['similarity_glove'].notna())
valid_data = top_60[valid_mask]

# 计算 Spearman 相关系数
# Compute Spearman correlation coefficients
w2v_corr, w2v_pval = spearmanr(valid_data['SimLex999'], valid_data['similarity_w2v'])
glove_corr, glove_pval = spearmanr(valid_data['SimLex999'], valid_data['similarity_glove'])

print(f"\nSpearman Correlation with SimLex-999 (top {TOP_N} pairs):")
print(f"  Word2Vec: r = {w2v_corr:.4f} (p = {w2v_pval:.4e})")
print(f"  GloVe:    r = {glove_corr:.4f} (p = {glove_pval:.4e})")

# 判断哪个模型更好
# Determine which model aligns better
if abs(w2v_corr) > abs(glove_corr):
    better_model = "Word2Vec"
else:
    better_model = "GloVe"

print(f"\n  => {better_model} shows better alignment with human judgments.")

# 计算嵌入相似度的均值
# Compute average embedding similarities
w2v_mean = valid_data['similarity_w2v'].mean()
glove_mean = valid_data['similarity_glove'].mean()
simlex_mean = valid_data['SimLex999'].mean()

print(f"\nAverage Similarity Scores (top {TOP_N} pairs):")
print(f"  SimLex-999: {simlex_mean:.4f}")
print(f"  Word2Vec:   {w2v_mean:.4f}")
print(f"  GloVe:      {glove_mean:.4f}")

# 找出嵌入低估人类相似度的例子
# Highlight examples where embeddings underestimate human similarity
# SimLex999 分数先归一化到 0-1 范围以便与余弦相似度比较
# Normalize SimLex999 scores to 0-1 range for comparison with cosine similarity
valid_data_analysis = valid_data.copy()
valid_data_analysis['simlex_normalized'] = valid_data_analysis['SimLex999'] / 10.0

# 找出 Word2Vec 比归一化 SimLex 低很多的词对
# Find pairs where Word2Vec significantly underestimates human similarity
valid_data_analysis['w2v_diff'] = (
    valid_data_analysis['simlex_normalized'] - valid_data_analysis['similarity_w2v']
)
valid_data_analysis['glove_diff'] = (
    valid_data_analysis['simlex_normalized'] - valid_data_analysis['similarity_glove']
)

# 显示低估最严重的 5 个词对
# Show 5 pairs where embeddings underestimate similarity the most
print("\nTop 5 pairs where Word2Vec underestimates human similarity:")
underest_w2v = valid_data_analysis.nlargest(5, 'w2v_diff')
for _, row in underest_w2v.iterrows():
    print(f"  {row['word1']:>12} - {row['word2']:<12}  "
          f"SimLex={row['SimLex999']:.2f}  W2V={row['similarity_w2v']:.4f}  "
          f"Diff={row['w2v_diff']:.4f}")

print("\nTop 5 pairs where GloVe underestimates human similarity:")
underest_glove = valid_data_analysis.nlargest(5, 'glove_diff')
for _, row in underest_glove.iterrows():
    print(f"  {row['word1']:>12} - {row['word2']:<12}  "
          f"SimLex={row['SimLex999']:.2f}  GloVe={row['similarity_glove']:.4f}  "
          f"Diff={row['glove_diff']:.4f}")

# Word2Vec 和 GloVe 行为比较
# Compare Word2Vec and GloVe behavior
print("\nComparison of Word2Vec vs GloVe Behavior:")
print(f"  - Word2Vec average cosine similarity: {w2v_mean:.4f}")
print(f"  - GloVe average cosine similarity:    {glove_mean:.4f}")

if w2v_mean > glove_mean:
    print("  - Word2Vec tends to assign higher similarity scores overall.")
else:
    print("  - GloVe tends to assign higher similarity scores overall.")

print(f"  - Word2Vec Spearman r = {w2v_corr:.4f}")
print(f"  - GloVe Spearman r    = {glove_corr:.4f}")
print(f"  - {better_model} correlates better with human-judged semantic similarity.")
print()

print("Discussion Summary:")
print("  Both Word2Vec and GloVe capture semantic similarity to some extent,")
print("  but neither perfectly matches human judgments. Word2Vec is trained on")
print("  Google News data while GloVe is trained on Wikipedia + Gigaword.")
print("  The training corpus influences which semantic relationships each model")
print("  captures best. Pairs with very high SimLex scores (near 10) tend to be")
print("  synonyms, which both models handle reasonably well. However, for some")
print("  pairs, both models underestimate similarity, often because the words")
print("  appear in different contexts in their training data.")
print()
print("=" * 60)
print("Lab 3 Part 1 Complete")
print("=" * 60)
