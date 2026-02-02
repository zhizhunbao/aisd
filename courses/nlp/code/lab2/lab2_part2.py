"""
CST8507 Lab 2 Part 2: Rule-Based Sentiment Annotation
Author: Peng Wang
Student Number: 041107730

A rule-based sentiment annotation system using regular expressions.
Processes IMDb movie reviews, applies text preprocessing, and assigns
sentiment labels based on a predefined sentiment lexicon.
"""

# ============================================================
# 步骤0：导入模块和下载资源
# Step 0: Import modules and download resources
# ============================================================

# 导入正则表达式模块，用于文本预处理
# Import regular expression module for text preprocessing
import re

# 导入NLTK模块，用于加载IMDb数据集和分词
# Import NLTK module for loading IMDb dataset and tokenization
import nltk
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize

# 下载必要的NLTK资源
# Download necessary NLTK resources
nltk.download('movie_reviews', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


# ============================================================
# 步骤1：定义情感词典
# Step 1: Define sentiment lexicon
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
# 步骤2：实现文本预处理函数
# Step 2: Implement text preprocessing function
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
# 步骤3：实现情感词统计函数
# Step 3: Implement sentiment word counting function
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
# 步骤4：实现情感标注函数
# Step 4: Implement sentiment annotation function
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
# 步骤5：实现数据加载函数
# Step 5: Implement data loading function
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
# 步骤6：实现评估函数
# Step 6: Implement evaluation function
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
# 步骤7：主函数 - 运行情感分析
# Step 7: Main function - Run sentiment analysis
# ============================================================

def main():
    """主函数：运行情感分析系统
    Main function: run sentiment analysis system"""

    print("=" * 80)
    print("Rule-Based Sentiment Annotation using Regular Expression")
    print("=" * 80)
    print()

    # 加载数据集
    # Load dataset
    print("Loading IMDb movie reviews dataset...")
    reviews = load_reviews(200)
    print(f"Loaded {len(reviews)} reviews")
    print()

    # 情感标注
    # Sentiment annotation
    print("Annotating sentiments...")
    predictions = []
    for review in reviews:
        pred = annotate_sentiment(review['text'])
        predictions.append(pred)
    print("Annotation complete")
    print()

    # 评估准确率
    # Evaluate accuracy
    accuracy = evaluate_predictions(reviews, predictions)
    print(f"Accuracy on {len(reviews)} reviews: {accuracy:.2f}")
    print()

    # 显示样本评论
    # Display sample review
    print("-" * 80)
    print("Sample Review Analysis")
    print("-" * 80)
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

    # 显示原始文本（截断到200字符）
    # Display original text (truncated to 200 characters)
    original_text = sample['text'].replace('\n', ' ')
    if len(original_text) > 200:
        original_text = original_text[:200] + " ..."

    print(f"review (original): {original_text}")
    print()

    # 显示预处理后的文本（截断到100字符）
    # Display preprocessed text (truncated to 100 characters)
    preprocessed = preprocess_text(sample['text'])
    if len(preprocessed) > 100:
        preprocessed = preprocessed[:100] + " ..."

    print(f"Preprocessed review: {preprocessed}")
    print()

    # 显示标签
    # Display labels
    print(f"Original label: {sample['label']}")
    print(f"Predicted label: {sample_pred}")
    print()


# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
