"""
CST8507 Lab 2 Part 2: Rule-Based Sentiment Annotation
Author: Peng Wang
Student Number: 041107730

A rule-based sentiment annotation system using regular expressions.
Processes IMDb movie reviews, applies text preprocessing, and assigns
sentiment labels based on a predefined sentiment lexicon.
"""

# ============================================================
# 模块导入和资源下载
# Module Imports and Resource Downloads
# ============================================================

import re
import nltk
from nltk.corpus import movie_reviews  # IMDb电影评论数据集
from nltk.tokenize import word_tokenize  # 分词器

# 下载NLTK资源（首次运行需要下载，之后会跳过）
# Download NLTK resources (required on first run, skipped afterward)
nltk.download('movie_reviews', quiet=True)  # IMDb评论数据
nltk.download('punkt', quiet=True)  # 分词器模型
nltk.download('punkt_tab', quiet=True)  # 分词器查找表（punkt依赖）


# ============================================================
# 情感词典定义
# Sentiment Lexicon Definition
# ============================================================

# 正面情感词列表
# Positive sentiment words list
POSITIVE_WORDS = [
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
    'brilliant', 'outstanding', 'superb', 'awesome', 'love', 'loved',
    'beautiful', 'perfect', 'best', 'enjoy', 'enjoyed', 'fun', 'funny',
    'interesting', 'impressive', 'recommend', 'recommended', 'masterpiece',
    'entertaining', 'engaging', 'compelling', 'touching', 'moving',
    'delightful', 'charming', 'clever', 'smart', 'strong', 'powerful',
    'remarkable', 'stunning', 'exceptional', 'incredible', 'marvelous',
    'pleasant', 'satisfying', 'thrilling', 'exciting', 'captivating',
    'heartwarming', 'uplifting', 'inspiring', 'memorable'
]

# 负面情感词列表
# Negative sentiment words list
NEGATIVE_WORDS = [
    'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'boring',
    'dull', 'disappointing', 'disappointed', 'waste', 'wasted', 'stupid',
    'lame', 'pathetic', 'annoying', 'annoyed', 'hate', 'hated', 'fail',
    'failed', 'failure', 'weak', 'mess', 'ugly', 'ridiculous', 'absurd',
    'painful', 'tedious', 'slow', 'predictable', 'cliche', 'uninspired',
    'mediocre', 'forgettable', 'bland', 'flat', 'lifeless', 'dreadful',
    'atrocious', 'abysmal', 'dismal', 'frustrating', 'irritating',
    'unbearable', 'uninteresting', 'unconvincing', 'lousy', 'cheap'
]


# ============================================================
# 文本预处理函数
# Text Preprocessing Function
# @param text: 原始文本 / Raw text
# @return: 预处理后的干净文本 / Cleaned text
# ============================================================

def preprocess_text(text):
    """预处理文本：小写转换、去除HTML标签、URL、标点和多余空格
    Preprocess text: lowercase, remove HTML tags, URLs, punctuation and extra whitespace"""

    # 转换为小写
    # Convert to lowercase
    text = text.lower()

    # 去除HTML标签 (如 <br>)
    # Remove HTML tags (e.g., <br>)
    text = re.sub(r'<[^>]+>', ' ', text)

    # 去除URL和网页链接
    # Remove URLs and web links
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)

    # 去除标点、数字和特殊字符（只保留字母和空格）
    # Remove punctuation, numbers and special characters (keep only letters and spaces)
    text = re.sub(r'[^a-z\s]', ' ', text)

    # 去除多余空格
    # Remove extra whitespace
    text = ' '.join(text.split())

    return text


# ============================================================
# 情感词统计函数
# Sentiment Word Counting Function
# @param text: 已预处理的文本 / Preprocessed text
# @param word_list: 情感词列表 / Sentiment word list
# @return: 匹配的情感词数量 / Count of matched words
# ============================================================

def count_sentiment_words(text, word_list):
    """统计文本中出现的情感词数量
    Count the number of sentiment words appearing in text"""

    # 分词
    # Tokenize
    tokens = word_tokenize(text)

    # 统计匹配的词数
    # Count matching words
    count = sum(1 for token in tokens if token in word_list)

    return count


# ============================================================
# 情感标注函数
# Sentiment Annotation Function
# @param text: 原始评论文本 / Raw review text
# @return: 情感标签 ('pos'/'neg'/'neutral') / Sentiment label
# ============================================================

def annotate_sentiment(text):
    """为文本标注情感标签
    Annotate sentiment label for text"""

    # 预处理文本
    # Preprocess text
    preprocessed = preprocess_text(text)

    # 统计正面和负面情感词
    # Count positive and negative sentiment words
    pos_count = count_sentiment_words(preprocessed, POSITIVE_WORDS)
    neg_count = count_sentiment_words(preprocessed, NEGATIVE_WORDS)

    # 根据情感词数量确定标签
    # Determine label based on sentiment word counts
    if pos_count > neg_count:
        return 'pos'
    elif neg_count > pos_count:
        return 'neg'
    else:
        return 'neutral'


# ============================================================
# 数据加载函数
# Data Loading Function
# @param num_reviews: 要加载的评论总数，默认200 / Total reviews to load, default 200
# @return: 评论列表 [{text, label}] / List of review dicts
# ============================================================

def load_reviews(num_reviews=200):
    """加载IMDb电影评论数据集
    Load IMDb movie reviews dataset"""

    reviews = []

    # 加载正面评论
    # Load positive reviews
    pos_fileids = movie_reviews.fileids('pos')[:num_reviews // 2]
    for fileid in pos_fileids:
        text = movie_reviews.raw(fileid)
        reviews.append({'text': text, 'label': 'pos'})

    # 加载负面评论
    # Load negative reviews
    neg_fileids = movie_reviews.fileids('neg')[:num_reviews // 2]
    for fileid in neg_fileids:
        text = movie_reviews.raw(fileid)
        reviews.append({'text': text, 'label': 'neg'})

    return reviews


# ============================================================
# 评估函数
# Evaluation Function
# @param reviews: 原始评论列表，包含真实标签 / Reviews with true labels
# @param predictions: 预测标签列表 / List of predicted labels
# @return: 准确率 (0.0-1.0) / Accuracy
# ============================================================

def evaluate_predictions(reviews, predictions):
    """计算预测准确率
    Calculate prediction accuracy"""

    # 统计正确预测数（neutral被视为错误，因为数据集没有neutral标签）
    # Count correct predictions (neutral is considered incorrect as dataset has no neutral labels)
    correct = sum(1 for r, p in zip(reviews, predictions) if r['label'] == p)

    # 计算准确率
    # Calculate accuracy
    accuracy = correct / len(reviews)

    return accuracy


# ============================================================
# 主函数
# Main Function
# ============================================================

def main():
    """主函数：运行情感分析系统
    Main function: run sentiment analysis system"""

    print("=" * 80)
    print("Rule-Based Sentiment Annotation using Regular Expression")
    print("=" * 80)
    print()

    # ------------------------------------------------------------
    # 步骤1：加载数据集
    # Step 1: Load dataset
    # ------------------------------------------------------------
    print("-" * 60)
    print("Step 1: Load dataset")
    print("-" * 60)
    print("Input: num_reviews=200")
    reviews = load_reviews(200)
    pos = sum(1 for r in reviews if r['label'] == 'pos')
    neg = sum(1 for r in reviews if r['label'] == 'neg')
    print(f"Output: {len(reviews)} reviews (pos: {pos}, neg: {neg})")
    print()

    # ------------------------------------------------------------
    # 步骤2：情感标注
    # Step 2: Sentiment annotation
    # ------------------------------------------------------------
    print("-" * 60)
    print("Step 2: Sentiment annotation")
    print("-" * 60)
    print(f"Input: {len(reviews)} reviews")
    predictions = []
    for review in reviews:
        pred = annotate_sentiment(review['text'])
        predictions.append(pred)
    pred_pos = sum(1 for p in predictions if p == 'pos')
    pred_neg = sum(1 for p in predictions if p == 'neg')
    pred_neutral = sum(1 for p in predictions if p == 'neutral')
    print(f"Output: {len(predictions)} predictions (pos: {pred_pos}, neg: {pred_neg}, neutral: {pred_neutral})")
    print()

    # ------------------------------------------------------------
    # 步骤3：评估准确率
    # Step 3: Evaluate accuracy
    # ------------------------------------------------------------
    print("-" * 60)
    print("Step 3: Evaluate accuracy")
    print("-" * 60)
    print(f"Input: {len(reviews)} reviews + {len(predictions)} predictions")
    accuracy = evaluate_predictions(reviews, predictions)
    print(f"Output: accuracy = {accuracy:.2%}")
    print()

    # ------------------------------------------------------------
    # 步骤4：显示样本评论分析
    # Step 4: Display sample review analysis
    # ------------------------------------------------------------
    print("-" * 60)
    print("Step 4: Sample Review Analysis")
    print("-" * 60)
    print()

    # 选择一个有趣的样本（预测与真实标签不同的）
    # Select an interesting sample (prediction differs from true label)
    sample_idx = None
    for i, (review, pred) in enumerate(zip(reviews, predictions)):
        if review['label'] != pred:
            sample_idx = i
            break

    # 如果没有找到不匹配的样本，使用第一个
    # If no mismatched sample found, use the first one
    if sample_idx is None:
        sample_idx = 0

    sample = reviews[sample_idx]
    sample_pred = predictions[sample_idx]

    # 显示原始文本（清理换行符防止终端显示错乱，但不截断）
    # Display original text (clean newlines but no truncation)
    original_text = sample['text'].replace('\r', ' ').replace('\n', ' ')
    original_text = ' '.join(original_text.split())

    print(f"Review (Original):\n{original_text}")
    print()

    # 显示预处理后的文本
    # Display preprocessed text
    preprocessed = preprocess_text(sample['text'])
    print(f"Preprocessed Review:\n{preprocessed}")
    print()

    # 统计并显示具体匹配到的情感词（以便分析误判原因）
    # Count and display specific matched sentiment words
    tokens = word_tokenize(preprocessed)
    matched_pos = [t for t in tokens if t in POSITIVE_WORDS]
    matched_neg = [t for t in tokens if t in NEGATIVE_WORDS]

    print(f"Matched Positive Words ({len(matched_pos)}): {matched_pos}")
    print(f"Matched Negative Words ({len(matched_neg)}): {matched_neg}")
    print()

    # 显示标签对比
    # Display label comparison
    print(f"Original Label:  {sample['label']}")
    print(f"Predicted Label: {sample_pred}")
    print()


# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
