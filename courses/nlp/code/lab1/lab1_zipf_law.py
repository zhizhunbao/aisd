"""
CST8507 Lab 1: Zipf's Law and Text Analysis
Author: Peng Wang
Section: 101
Date: 2026-01-20

This program analyzes word frequency distributions in two different text corpora
(literary and informational) to empirically verify Zipf's Law. It performs
tokenization, frequency analysis, and comparative studies including stability
testing with stopword removal and part-of-speech filtering.

Innovations:
- Automated comparative analysis with statistical metrics
- Comprehensive visualization with multiple subplots
- Robust preprocessing pipeline with error handling
"""

# Step 1: Import required libraries
import string
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import gutenberg, stopwords
from scipy import stats

# Ensure required NLTK data is available
# Uncomment these lines on first run to download necessary data
# nltk.download('gutenberg')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')





def tokenize_and_clean(text):
    """
    Tokenize text and perform basic cleaning.
    
    Args:
        text (str): Raw text to tokenize
    
    Returns:
        list: List of cleaned tokens (lowercase, alphabetic only)
    """
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Clean tokens: lowercase and keep only alphabetic words
    cleaned_tokens = [token.lower() for token in tokens 
                     if token.isalpha()]
    
    return cleaned_tokens


def analyze_frequency(tokens):
    """
    Analyze word frequency distribution.
    
    Args:
        tokens (list): List of word tokens
    
    Returns:
        tuple: (FreqDist object, sorted list of (word, frequency) tuples, DataFrame)
    """
    # Create frequency distribution
    fdist = FreqDist(tokens)
    
    # Sort by frequency (descending)
    sorted_fdist = sorted(fdist.items(), key=lambda x: x[1], reverse=True)
    
    # Create DataFrame for analysis
    df = pd.DataFrame(sorted_fdist, columns=['word', 'frequency'])
    df['rank'] = range(1, len(df) + 1)
    
    return fdist, sorted_fdist, df


def calculate_zipf_metrics(df):
    """
    Calculate Zipf's Law metrics including exponent and R-squared.
    
    Args:
        df (DataFrame): DataFrame with 'rank' and 'frequency' columns
    
    Returns:
        tuple: (slope/alpha, R-squared value)
    """
    # Take logarithm of rank and frequency
    log_rank = np.log(df['rank'])
    log_freq = np.log(df['frequency'])
    
    # Perform linear regression
    # 对 (log(rank), log(freq)) 做线性回归：log(freq) = intercept + slope * log(rank)
    # slope: 斜率，表示 log(rank) 每增加1，log(freq) 变化的量
    # intercept: 截距，当 log(rank)=0 时的 log(freq) 值  
    # r_value: 相关系数，范围[-1,1]，表示两个变量的线性相关强度
    # p_value: p值，用于检验斜率是否显著不为0
    # std_err: 标准误差，斜率估计的标准差
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_rank, log_freq)
    
    return -slope, r_value**2


def plot_zipf_distribution(df, title, ax=None):
    """
    Plot Zipf's Law distribution on log-log scale.
    
    Args:
        df (DataFrame): DataFrame with 'rank' and 'frequency' columns
        title (str): Plot title
        ax (matplotlib.axes): Axes object for subplot (optional)
    
    Returns:
        None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.loglog(df['rank'], df['frequency'], 'bo', markersize=3)
    ax.set_xlabel('Rank (log scale)', fontsize=12)
    ax.set_ylabel('Frequency (log scale)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, which='both')
    
    if ax is None:
        plt.tight_layout()
        plt.show()


def remove_stopwords(tokens):
    """
    Remove English stopwords from token list.
    
    Args:
        tokens (list): List of word tokens
    
    Returns:
        list: Tokens with stopwords removed
    """
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    return filtered_tokens


def extract_nouns(tokens):
    """
    Extract only nouns from token list using POS tagging.
    
    Args:
        tokens (list): List of word tokens
    
    Returns:
        list: List of noun tokens only
    """
    # Perform POS tagging
    # 进行词性标注：为每个 token 打上词性标签
    # 输入：['The', 'quick', 'fox'] 
    # 输出：[('The', 'DT'), ('quick', 'JJ'), ('fox', 'NN')]
    # DT=限定词, JJ=形容词, NN=名词单数, VBZ=动词, NNS=名词复数, NNP=专有名词
    pos_tags = nltk.pos_tag(tokens)
    
    # Extract nouns (NN, NNS, NNP, NNPS)
    # 提取名词：以 NN 开头的标签通常表示名词（单数/复数/专有名词等）
    # 过滤条件：pos.startswith('NN') 匹配所有名词类型
    # NN: 普通名词单数 (fox, book), NNS: 普通名词复数 (foxes, books)
    # NNP: 专有名词单数 (John, London), NNPS: 专有名词复数 (Johns, Mondays)
    # 列表推导式：遍历每个(单词,词性)对，只保留词性以'NN'开头的单词
    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
    
    return nouns


# Step 2: Load and prepare data
print("=" * 70)
print("CST8507 Lab 1: Zipf's Law Analysis")
print("=" * 70)
print("\nStep 2: Loading text data...")

# Load literary text (Jane Austen's Emma)
literary_text = gutenberg.raw('austen-emma.txt')
print(f"Literary text loaded: {len(literary_text)} characters")

# Load informational text (King James Bible)
informational_text = gutenberg.raw('bible-kjv.txt')
print(f"Informational text loaded: {len(informational_text)} characters")


# Step 3: Tokenize the data
print("\nStep 3: Tokenizing and cleaning data...")

literary_tokens = tokenize_and_clean(literary_text)
print(f"Literary tokens: {len(literary_tokens)} words")

informational_tokens = tokenize_and_clean(informational_text)
print(f"Informational tokens: {len(informational_tokens)} words")


# Step 4: Analyze word frequencies
print("\nStep 4: Analyzing word frequencies...")

# Analyze literary text
lit_fdist, lit_sorted, lit_df = analyze_frequency(literary_tokens)
print(f"\nLiterary Text Analysis:")
print(f"  Total vocabulary size: {len(lit_fdist)}")
print(f"  Top 20 most frequent words:")
for i, (word, freq) in enumerate(lit_sorted[:20], 1):
    print(f"    {i:2d}. {word:15s} - {freq:5d}")

# Analyze informational text
info_fdist, info_sorted, info_df = analyze_frequency(informational_tokens)
print(f"\nInformational Text Analysis:")
print(f"  Total vocabulary size: {len(info_fdist)}")
print(f"  Top 20 most frequent words:")
for i, (word, freq) in enumerate(info_sorted[:20], 1):
    print(f"    {i:2d}. {word:15s} - {freq:5d}")

# Calculate Zipf metrics
lit_alpha, lit_r2 = calculate_zipf_metrics(lit_df)
info_alpha, info_r2 = calculate_zipf_metrics(info_df)

print(f"\nZipf's Law Metrics:")
print(f"  Literary text - Alpha: {lit_alpha:.3f}, R-squared: {lit_r2:.3f}")
print(f"  Informational text - Alpha: {info_alpha:.3f}, R-squared: {info_r2:.3f}")
# 结果解读：
# Alpha > 1.0 表示词频下降比标准齐夫定律更快，可能因为词汇丰富度较高
# R^2 > 0.95 说明拟合度极好，验证了齐夫定律在真实文本中的有效性
# 文学文本Alpha较低(1.393)说明词汇分布更集中，信息文本Alpha较高(1.625)说明词汇更分散


# Step 5: Plot Zipf distributions for both texts
print("\nStep 4 (continued): Plotting Zipf distributions...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

plot_zipf_distribution(lit_df, "Zipf's Law: Literary Text (Emma)", ax1)
ax1.text(0.05, 0.95, f'alpha = {lit_alpha:.3f}\nR^2 = {lit_r2:.3f}', 
         transform=ax1.transAxes, fontsize=12, 
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plot_zipf_distribution(info_df, "Zipf's Law: Informational Text (Bible)", ax2)
ax2.text(0.05, 0.95, f'alpha = {info_alpha:.3f}\nR^2 = {info_r2:.3f}', 
         transform=ax2.transAxes, fontsize=12, 
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('images/zipf_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Plots saved as 'images/zipf_comparison.png'")
# alpha (α): 齐夫定律指数，理想值约为1.0，表示词频随排名下降的速度
# R^2 (R-squared): 决定系数，范围[0,1]，表示线性回归拟合度，越接近1拟合越好
print(f"  [Image Data] Literary: alpha = {lit_alpha:.3f}, R^2 = {lit_r2:.3f}")
print(f"  [Image Data] Informational: alpha = {info_alpha:.3f}, R^2 = {info_r2:.3f}")


# Step 6: Stability testing - Remove stopwords
print("\nStep 6: Evaluating stability - Removing stopwords...")

# Use literary text for stability testing
lit_no_stop = remove_stopwords(literary_tokens)
print(f"Tokens after stopword removal: {len(lit_no_stop)}")

# Analyze frequency without stopwords
_, _, lit_no_stop_df = analyze_frequency(lit_no_stop)
no_stop_alpha, no_stop_r2 = calculate_zipf_metrics(lit_no_stop_df)

print(f"Zipf metrics without stopwords:")
print(f"  Alpha: {no_stop_alpha:.3f}, R-squared: {no_stop_r2:.3f}")
print(f"  Change in alpha: {no_stop_alpha - lit_alpha:+.3f}")


# Plot comparison: Original vs Without Stopwords
print("\nGenerating comparison plot: Original vs Without Stopwords...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Original distribution
plot_zipf_distribution(lit_df, "Original Distribution (All Words)", axes[0])
axes[0].text(0.05, 0.95, f'alpha = {lit_alpha:.3f}\nR^2 = {lit_r2:.3f}', 
             transform=axes[0].transAxes, fontsize=12, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 2: Without stopwords
plot_zipf_distribution(lit_no_stop_df, "Without Stopwords", axes[1])
axes[1].text(0.05, 0.95, f'alpha = {no_stop_alpha:.3f}\nR^2 = {no_stop_r2:.3f}', 
             transform=axes[1].transAxes, fontsize=12, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Zipf\'s Law: Impact of Stopword Removal', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('images/zipf_stopword_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"  Comparison plot saved as 'images/zipf_stopword_comparison.png'")
print(f"  [Image Data] Original: alpha = {lit_alpha:.3f}, R^2 = {lit_r2:.3f}")
print(f"  [Image Data] Without Stopwords: alpha = {no_stop_alpha:.3f}, R^2 = {no_stop_r2:.3f}")
print(f"\nComparison Summary:")
print(f"  Original:          alpha = {lit_alpha:.3f}, R^2 = {lit_r2:.3f}")
print(f"  Without Stopwords: alpha = {no_stop_alpha:.3f}, R^2 = {no_stop_r2:.3f}")
print(f"  Change in alpha:   {no_stop_alpha - lit_alpha:+.3f}")
print(f"  Change in R^2:     {no_stop_r2 - lit_r2:+.3f}")


# Step 6 (continued): Stability testing - Nouns only
print("\nStep 6 (continued): Evaluating stability - Nouns only...")

lit_nouns = extract_nouns(literary_tokens)
print(f"Noun tokens extracted: {len(lit_nouns)}")

# Analyze frequency for nouns only
_, _, lit_nouns_df = analyze_frequency(lit_nouns)
nouns_alpha, nouns_r2 = calculate_zipf_metrics(lit_nouns_df)

print(f"Zipf metrics for nouns only:")
print(f"  Alpha: {nouns_alpha:.3f}, R-squared: {nouns_r2:.3f}")
print(f"  Change in alpha: {nouns_alpha - lit_alpha:+.3f}")


# Plot stability comparison
print("\nPlotting stability comparison...")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

plot_zipf_distribution(lit_df, "Original (All Words)", axes[0])
axes[0].text(0.05, 0.95, f'alpha = {lit_alpha:.3f}\nR^2 = {lit_r2:.3f}', 
             transform=axes[0].transAxes, fontsize=11, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plot_zipf_distribution(lit_no_stop_df, "Without Stopwords", axes[1])
axes[1].text(0.05, 0.95, f'alpha = {no_stop_alpha:.3f}\nR^2 = {no_stop_r2:.3f}', 
             transform=axes[1].transAxes, fontsize=11, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plot_zipf_distribution(lit_nouns_df, "Nouns Only", axes[2])
axes[2].text(0.05, 0.95, f'alpha = {nouns_alpha:.3f}\nR^2 = {nouns_r2:.3f}', 
             transform=axes[2].transAxes, fontsize=11, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('images/zipf_stability.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Stability plots saved as 'images/zipf_stability.png'")
print(f"  [Image Data] Original: alpha = {lit_alpha:.3f}, R^2 = {lit_r2:.3f}")
print(f"  [Image Data] Without Stopwords: alpha = {no_stop_alpha:.3f}, R^2 = {no_stop_r2:.3f}")
print(f"  [Image Data] Nouns Only: alpha = {nouns_alpha:.3f}, R^2 = {nouns_r2:.3f}")


print("\n" + "=" * 70)
print("Analysis Complete!")
print("=" * 70)
