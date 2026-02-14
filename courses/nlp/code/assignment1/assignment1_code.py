"""
CST8507 Assignment 1: Comparative Analysis of Text Representation
Author: Peng Wang
Student Number: 041107730

Classify Amazon reviews into five categories (1-5) using different
textual features (n-gram, TF-IDF, Word2Vec) and ML classifiers
(Logistic Regression, Linear SVM). Includes hyperparameter tuning
and error analysis across feature representations.
"""

# ============================================================
# 导入依赖库
# Import Dependencies
# ============================================================

import os
import re
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载环境变量（学生信息）
# Load environment variables (student information)
from dotenv import load_dotenv

# 自然语言处理工具
# Natural language processing tools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# 机器学习工具
# Machine learning tools
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)

# 词嵌入模型
# Word embedding model
from gensim.models import Word2Vec

# 格式化输出表格
# Formatted table output
from tabulate import tabulate

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 随机种子，确保实验可复现
# Random seed to ensure reproducibility
RANDOM_STATE = 42

# 测试集比例（20%）
# Test set ratio (20%)
TEST_SIZE = 0.2

# 子集大小：如果数据集过大，随机抽取此数量的记录
# Subset size: randomly sample this many records if dataset is too large
SUBSET_SIZE = 50000

# n-gram 范围：使用 unigram + bigram
# n-gram range: use unigram + bigram
NGRAM_RANGE = (1, 2)

# 最大特征数量，限制 BoW 和 TF-IDF 的维度
# Maximum number of features, limit BoW and TF-IDF dimensions
MAX_FEATURES = 10000

# Word2Vec 向量维度
# Word2Vec vector dimension
W2V_VECTOR_SIZE = 100

# Word2Vec 上下文窗口大小
# Word2Vec context window size
W2V_WINDOW = 5

# Word2Vec 最小词频：低于此频率的词将被忽略
# Word2Vec minimum word count: words below this frequency are ignored
W2V_MIN_COUNT = 2

# Word2Vec 训练工作线程数
# Word2Vec training worker threads
W2V_WORKERS = 4

# Logistic Regression 最大迭代次数
# Logistic Regression maximum iterations
LR_MAX_ITER = 1000

# 交叉验证折数
# Cross-validation fold count
CV_FOLDS = 5

# 输出图表目录
# Output chart directory
OUTPUT_DIR = "assignment1_images"


# ============================================================
# 步骤 0：实验初始化
# Step 0: Lab Initialization
# ============================================================
def initialize_lab():
    """实验初始化：加载环境变量、下载NLTK数据、设置显示选项
    Lab initialization: load env vars, download NLTK data, set display options"""

    # 加载学生信息
    # Load student information
    load_dotenv(".env.local")
    student_name = os.getenv("NAME", "Peng Wang")
    student_number = os.getenv("NUMBER", "041107730")

    # 忽略警告信息，保持输出清洁
    # Suppress warnings to keep output clean
    warnings.filterwarnings("ignore")

    # 下载 NLTK 所需数据包（静默模式）
    # Download required NLTK data packages (quiet mode)
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)

    # 设置 pandas 显示选项，确保完整输出
    # Set pandas display options to ensure full output
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.expand_frame_repr", False)

    # 设置 matplotlib 风格
    # Set matplotlib style
    plt.style.use("seaborn-v0_8-whitegrid")

    # 创建图表输出目录
    # Create chart output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 打印实验信息
    # Print lab information
    print("=" * 60)
    print("CST8507 Assignment 1: Text Representation Analysis")
    print(f"Student: {student_name} ({student_number})")
    print("=" * 60)

    return student_name, student_number


# ============================================================
# 步骤 1：数据加载
# Step 1: Data Loading
# ============================================================
def load_data(data_path="Reviews.csv"):
    """加载Amazon评论数据集
    Load Amazon reviews dataset"""

    print("\n" + "=" * 60)
    print("Step 1: Data Loading")
    print("=" * 60)

    # 读取 CSV 文件，仅加载需要的列
    # Read CSV file, only load required columns
    df = pd.read_csv(data_path, usecols=["Score", "Text"])

    # 显示原始数据集信息
    # Display original dataset info
    print(f"Original dataset size: {len(df)} records")
    print(f"Columns: {list(df.columns)}")

    # 删除缺失值
    # Drop missing values
    df = df.dropna(subset=["Score", "Text"])
    print(f"After dropping NaN: {len(df)} records")

    # 如果数据集过大，随机抽取子集
    # If dataset is too large, randomly sample a subset
    if len(df) > SUBSET_SIZE:
        df = df.sample(n=SUBSET_SIZE, random_state=RANDOM_STATE)
        print(f"Sampled subset: {SUBSET_SIZE} records")

    # 显示类别分布
    # Display class distribution
    print(f"\nScore distribution:")
    score_counts = df["Score"].value_counts().sort_index()
    for score, count in score_counts.items():
        print(f"  Score {score}: {count} ({count/len(df)*100:.1f}%)")

    # 显示数据样例
    # Display data samples
    print(f"\nSample data:")
    print(df.head())

    return df


# ============================================================
# 步骤 2：数据预处理
# Step 2: Data Preprocessing
# ============================================================
def preprocess_text(text):
    """对单条文本执行预处理流水线
    Execute preprocessing pipeline on a single text"""

    # ================================================================
    # 文本预处理 / Text Preprocessing
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【分词 Tokenization】
    #   将连续文本拆分为单词/词元列表
    #   "I love NLP" → ["I", "love", "NLP"]
    #   Splitting continuous text into a list of words/tokens
    #
    # 【停用词 Stop Words】
    #   高频但无实际语义的词，如 "the", "is", "a"
    #   移除停用词可以减少噪声，提高特征质量
    #   High-frequency words with little semantic meaning
    #
    # 【词形还原 Lemmatization】
    #   将单词还原为词典基本形式（词元）
    #   running/ran/runs → run, better → good
    #   与词干提取(Stemming)区别：产生真实词而非截断
    #   Reduce words to dictionary base form
    #
    # 【词元 Token/Lemma】
    #   文本处理后的最小单位
    #   Token: 分词后的词；Lemma: 词形还原后的词
    #   Smallest unit after text processing
    #
    # ================================================================

    # 转换为小写
    # Convert to lowercase
    text = text.lower()

    # 移除 HTML 标签（评论中可能包含 <br/> 等）
    # Remove HTML tags (reviews may contain <br/> etc.)
    text = re.sub(r"<[^>]+>", " ", text)

    # 移除标点和特殊字符，仅保留字母和空格
    # Remove punctuation and special characters, keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # 移除多余空格
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # 分词：使用 NLTK 的 word_tokenize 函数将文本字符串拆分为单词/词元列表
    #   - 分词是 NLP 的基础步骤，将连续文本转换为可独立处理的词单元
    #   - word_tokenize 比简单的 split() 更智能，能正确处理标点和缩写
    #   - 例如："I don't like it." → ["I", "do", "n't", "like", "it", "."]
    # Tokenization: Use NLTK's word_tokenize to split text string into a list of words/tokens
    #   - Tokenization is a fundamental NLP step, converting continuous text into discrete word units
    #   - word_tokenize is smarter than simple split(), handling punctuation and contractions properly
    #   - Example: "I don't like it." → ["I", "do", "n't", "like", "it", "."]
    tokens = word_tokenize(text)

    # 移除停用词
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    # 词形还原：使用 WordNetLemmatizer 将单词还原为词典基本形式（词元）
    #   - 词形还原基于词典查找，将单词的屈折变体还原为标准形式
    #   - 例如：running/ran/runs → run, better → good, cats → cat
    #   - 与词干提取(Stemming)的区别：
    #     • 词形还原产生真实的词（studies → study）
    #     • 词干提取可能产生非词（studies → studi）
    #   - 优点：减少词汇表大小，提高特征泛化能力
    # Lemmatization: Use WordNetLemmatizer to reduce words to their dictionary base form (lemma)
    #   - Lemmatization uses dictionary lookup to convert inflected word forms to standard form
    #   - Example: running/ran/runs → run, better → good, cats → cat
    #   - Difference from Stemming:
    #     • Lemmatization produces real words (studies → study)
    #     • Stemming may produce non-words (studies → studi)
    #   - Benefit: Reduces vocabulary size, improves feature generalization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    # 移除过短的词（长度 < 2 的词通常无意义）
    # Remove very short tokens (words with length < 2 are usually meaningless)
    tokens = [t for t in tokens if len(t) >= 2]

    return tokens


def preprocess_dataset(df):
    """对整个数据集执行预处理
    Execute preprocessing on the entire dataset"""

    print("\n" + "=" * 60)
    print("Step 2: Data Preprocessing")
    print("=" * 60)

    print("Preprocessing steps:")
    print("  1. Lowercasing")
    print("  2. Remove HTML tags")
    print("  3. Remove punctuation and special characters")
    print("  4. Tokenization (NLTK word_tokenize)")
    print("  5. Stop words removal (English)")
    print("  6. Lemmatization (WordNetLemmatizer)")
    print("  7. Remove short tokens (length < 2)")

    # 对所有文本执行预处理，保存为 token 列表
    # Preprocess all texts, save as token lists
    print("\nProcessing texts...")
    df = df.copy()
    df["tokens"] = df["Text"].apply(preprocess_text)

    # 将 token 列表重新连接为字符串（供 CountVectorizer/TfidfVectorizer 使用）
    # Rejoin token lists to strings (for CountVectorizer/TfidfVectorizer)
    df["cleaned_text"] = df["tokens"].apply(lambda tokens: " ".join(tokens))

    # 显示预处理结果样例
    # Display preprocessing result samples
    print(f"\nPreprocessing complete. Sample results:")
    for i in range(3):
        original = df.iloc[i]["Text"][:80]
        cleaned = df.iloc[i]["cleaned_text"][:80]
        print(f"\n  Original : {original}...")
        print(f"  Cleaned  : {cleaned}...")

    # 统计预处理后平均 token 数
    # Calculate average token count after preprocessing
    avg_tokens = df["tokens"].apply(len).mean()
    print(f"\nAverage tokens per review after preprocessing: {avg_tokens:.1f}")

    return df


# ============================================================
# 步骤 3A：训练集/测试集划分
# Step 3A: Train/Test Split
# ============================================================
def split_data(df):
    """先划分再提取特征，避免数据泄露
    Split before feature extraction to prevent data leakage"""

    print("\n" + "=" * 60)
    print("Step 3: Train/Test Split")
    print("=" * 60)

    # ================================================================
    # 数据划分 / Data Splitting
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【训练集 Training Set】
    #   用于训练模型的数据（通常占 80%）
    #   模型从这些数据中"学习"规律
    #   Data used to train the model
    #
    # 【测试集 Test Set】
    #   用于评估模型性能的数据（通常占 20%）
    #   模拟模型在"未见过"的新数据上的表现
    #   Data used to evaluate model performance
    #
    # 【数据泄露 Data Leakage】
    #   训练时使用了测试集的信息，导致评估结果虚高
    #   例如：在整个数据集上学习词汇表，再划分
    #   正确做法：先划分，再在训练集上学习
    #   Using test set information during training, causing inflated metrics
    #
    # 【分层抽样 Stratified Sampling】
    #   划分时保持类别比例一致
    #   例如：原数据 60%正类/40%负类 → 训练集和测试集也是 60%/40%
    #   目的：防止某个类别在训练集中过多或过少
    #   Maintain class proportions when splitting
    #
    # ================================================================

    # 分离特征和标签
    # Separate features and labels
    X = df["cleaned_text"]
    y = df["Score"]

    # 使用分层抽样划分数据集（保持各类别比例一致）
    # Use stratified sampling to split dataset (maintain class proportions)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    print(f"Training set: {len(X_train)} samples")
    print(f"Test set:     {len(X_test)} samples")
    print(f"Split ratio:  {1 - TEST_SIZE:.0%} / {TEST_SIZE:.0%}")
    print(f"Stratified:   Yes (class proportions preserved)")

    # 显示训练集类别分布
    # Display training set class distribution
    print(f"\nTraining set class distribution:")
    train_counts = y_train.value_counts().sort_index()
    for score, count in train_counts.items():
        print(f"  Score {score}: {count} ({count/len(y_train)*100:.1f}%)")

    return X_train, X_test, y_train, y_test


# ============================================================
# 步骤 3B：特征提取 - n-gram (BoW)
# Step 3B: Feature Extraction - n-gram (BoW)
# ============================================================
def extract_ngram_features(X_train, X_test):
    """使用CountVectorizer提取n-gram (BoW)特征
    Extract n-gram (BoW) features using CountVectorizer"""

    print("\\n" + "=" * 60)
    print("Step 3B: Feature Extraction - n-gram (BoW)")
    print("=" * 60)

    # ================================================================
    # 特征提取：n-gram + BoW（词袋模型）
    # Feature Extraction: n-gram + Bag of Words (BoW)
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【n-gram（n元组）】
    #   将文本切分为连续的 n 个词组合
    #   unigram (n=1): "I love this" → ["I", "love", "this"]
    #   bigram (n=2):  "I love this" → ["I love", "love this"]
    #   Text split into consecutive n-word combinations
    #
    # 【词袋模型 Bag of Words (BoW)】
    #   把文档看作一个"装词的袋子"，只统计词频，忽略词序
    #   "I love you" 和 "You love I" 在 BoW 中表示相同
    #   Treats document as a "bag of words", counts frequency, ignores order
    #
    # 【稀疏向量 Sparse Vector】
    #   向量中大部分值为 0 的向量
    #   因为一篇文档只包含词汇表中很少的词
    #   例如：词汇表 10000 词，文档只用到 50 词 → 99.5% 是 0
    #   Vector with mostly zero values (document uses few of all vocabulary words)
    #
    # 【稀疏矩阵 scipy.sparse.csr_matrix】
    #   只存储非零值的位置和值，节省内存
    #   例如：10000×5000 矩阵只需存几十万个非零值
    #   Only stores positions and values of non-zeros, saves memory
    #
    # -------- 算法原理 / Algorithm --------
    #
    # 定义 / Definition:
    #   1. 将文本切分为 n-gram
    #   2. 统计每个 n-gram 在文档中出现的次数
    #   3. 生成词频向量表示文档
    #
    # 举例 / Example:
    #   原文: "good product good"
    #   词汇表: {good: 0, product: 1}
    #   向量:   [2, 1]  (good 出现 2 次, product 出现 1 次)
    #
    # 输出格式 / Output Format:
    #   [样本数 × 词汇表大小] 稀疏矩阵，值为词频
    # ================================================================

    # 创建 CountVectorizer：unigram + bigram，限制最大特征数
    # Create CountVectorizer: unigram + bigram, limit max features
    bow_vectorizer = CountVectorizer(
        ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
    )

    # ----------------------------------------------------------------
    # fit_transform vs transform 的区别
    # Difference between fit_transform and transform
    # ----------------------------------------------------------------
    #   fit_transform（仅用于训练集）：
    #     1. fit：学习词汇表，统计训练集中所有出现的 n-gram
    #     2. transform：将文本转换为词频向量
    #   transform（仅用于测试集）：
    #     - 使用训练集学到的词汇表转换（不学习新词）
    #     - 防止数据泄露：测试集不应影响模型的词汇表
    # ----------------------------------------------------------------
    #   fit_transform (only for training set):
    #     1. fit: Learn vocabulary, count all n-grams in training set
    #     2. transform: Convert text to word frequency vectors
    #   transform (only for test set):
    #     - Use vocabulary learned from training set (no new words)
    #     - Prevent data leakage: test set should not affect vocabulary
    # ----------------------------------------------------------------
    #
    # 举例 / Example:
    #   原始文本 / Original texts:
    #     doc1: "good product"
    #     doc2: "bad product"
    #   词汇表 / Vocabulary: {"good": 0, "product": 1, "bad": 2, "good product": 3, "bad product": 4}
    #   转换后 / After transform:
    #     doc1 → [1, 1, 0, 1, 0]  (good=1, product=1, good product=1)
    #     doc2 → [0, 1, 1, 0, 1]  (product=1, bad=1, bad product=1)
    #   输出格式 / Output format: 稀疏矩阵 (scipy.sparse.csr_matrix)
    # ----------------------------------------------------------------
    X_train_bow = bow_vectorizer.fit_transform(X_train)
    X_test_bow = bow_vectorizer.transform(X_test)

    print(f"n-gram range: {NGRAM_RANGE}")
    print(f"Max features: {MAX_FEATURES}")
    print(f"Training feature matrix shape: {X_train_bow.shape}")
    print(f"Test feature matrix shape:     {X_test_bow.shape}")
    print(f"Vocabulary size: {len(bow_vectorizer.vocabulary_)}")

    return X_train_bow, X_test_bow, bow_vectorizer


# ============================================================
# 步骤 3C：特征提取 - TF-IDF
# Step 3C: Feature Extraction - TF-IDF
# ============================================================
def extract_tfidf_features(X_train, X_test):
    """使用TfidfVectorizer提取TF-IDF特征
    Extract TF-IDF features using TfidfVectorizer"""

    print("\n" + "=" * 60)
    print("Step 3C: Feature Extraction - TF-IDF")
    print("=" * 60)

    # ================================================================
    # 特征提取：TF-IDF（词频-逆文档频率）
    # Feature Extraction: TF-IDF (Term Frequency - Inverse Document Frequency)
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【TF (Term Frequency, 词频)】
    #   词在当前文档中出现的次数 / 文档总词数
    #   衡量词在单个文档中的重要性
    #   举例："good good bad" → TF(good) = 2/3 = 0.67
    #   Word count / total words in document
    #
    # 【IDF (Inverse Document Frequency, 逆文档频率)】
    #   log(总文档数 / 包含该词的文档数) + 1
    #   衡量词的稀有程度
    #   举例：100 篇文档，50 篇含 "product" → IDF = log(100/50)+1 = 1.69
    #   常见词如 "the" 几乎每篇都有 → IDF ≈ 1（很低）
    #   log(total docs / docs containing word) + 1
    #
    # 【L2 归一化 (L2 Normalization)】
    #   使每个文档向量的长度（范数）为 1
    #   目的：消除文档长度对相似度计算的影响
    #   公式：v_normalized = v / ||v||
    #   Make each document vector have unit length
    #
    # -------- 算法原理 / Algorithm --------
    #
    # 定义 / Definition:
    #   TF-IDF = TF × IDF
    #   既考虑词在文档中的频率，又惩罚过于常见的词
    #
    # 举例 / Example:
    #   "delicious" 在美食评论中：
    #     - TF 高（常在美食文档中出现）
    #     - IDF 高（只在美食类文档出现，其他类少）
    #     → TF-IDF 高，有区分度
    #   "the" 在所有文档中：
    #     - TF 高
    #     - IDF 极低（几乎所有文档都有）
    #     → TF-IDF 低，无区分度
    #
    # 相比 BoW 的优势 / Advantage over BoW:
    #   自动降低停用词权重，突出关键词
    # ================================================================

    # 创建 TfidfVectorizer
    # Create TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(
        ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
    )

    # ----------------------------------------------------------------
    # fit_transform 过程说明
    # fit_transform process explanation
    # ----------------------------------------------------------------
    #   fit 阶段：
    #     1. 学习词汇表（同 BoW）
    #     2. 计算每个词的 IDF 值：IDF(t) = log(N / df(t)) + 1
    #        - N = 总文档数，df(t) = 包含词 t 的文档数
    #   transform 阶段：
    #     1. 计算每个词的 TF 值：词频 / 文档长度
    #     2. 计算 TF-IDF 值：TF × IDF
    #     3. L2 归一化：使每个文档向量的长度为 1
    # ----------------------------------------------------------------
    #   fit phase:
    #     1. Learn vocabulary (same as BoW)
    #     2. Compute IDF for each word: IDF(t) = log(N / df(t)) + 1
    #        - N = total docs, df(t) = docs containing word t
    #   transform phase:
    #     1. Compute TF for each word: word count / doc length
    #     2. Compute TF-IDF: TF × IDF
    #     3. L2 normalization: make each doc vector length = 1
    # ----------------------------------------------------------------
    #
    # 举例（假设只有 2 个文档）/ Example (assuming only 2 docs):
    #   doc1: "good good product"  (good 出现 2 次)
    #   doc2: "bad product"
    #   词汇表 / Vocabulary: {good, product, bad}
    #   IDF 值 / IDF values:
    #     - good:    log(2/1) + 1 = 1.69  (只在 doc1 出现，稀有)
    #     - product: log(2/2) + 1 = 1.00  (两个文档都有，常见)
    #     - bad:     log(2/1) + 1 = 1.69  (只在 doc2 出现，稀有)
    #   转换后（归一化前）/ After transform (before normalization):
    #     doc1: TF × IDF = [2/3 × 1.69, 1/3 × 1.00, 0] = [1.13, 0.33, 0]
    #     doc2: TF × IDF = [0, 1/2 × 1.00, 1/2 × 1.69] = [0, 0.50, 0.85]
    #   输出格式 / Output format: 稀疏矩阵，值为 TF-IDF 权重（已 L2 归一化）
    # ----------------------------------------------------------------
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    print(f"n-gram range: {NGRAM_RANGE}")
    print(f"Max features: {MAX_FEATURES}")
    print(f"Training feature matrix shape: {X_train_tfidf.shape}")
    print(f"Test feature matrix shape:     {X_test_tfidf.shape}")

    return X_train_tfidf, X_test_tfidf, tfidf_vectorizer


# ============================================================
# 步骤 3D：特征提取 - Word2Vec
# Step 3D: Feature Extraction - Word2Vec
# ============================================================
def get_document_vector(tokens, model, vector_size):
    """计算一个文档的 Word2Vec 平均向量
    Compute the average Word2Vec vector for a document"""

    # 过滤出模型词汇表中存在的词的向量
    # Filter word vectors that exist in the model vocabulary
    vectors = [model.wv[word] for word in tokens if word in model.wv]

    # 如果没有有效词向量，返回全零向量
    # If no valid word vectors, return zero vector
    if len(vectors) == 0:
        return np.zeros(vector_size)

    # 取所有词向量的平均值作为文档向量
    # Average all word vectors as the document vector
    return np.mean(vectors, axis=0)


def extract_word2vec_features(df, train_index, test_index):
    """训练Word2Vec模型并提取文档向量
    Train Word2Vec model and extract document vectors"""

    print("\n" + "=" * 60)
    print("Step 3D: Feature Extraction - Word2Vec")
    print("=" * 60)

    # ================================================================
    # 特征提取：Word2Vec（词向量嵌入）
    # Feature Extraction: Word2Vec (Word Embedding)
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【词嵌入 Word Embedding】
    #   将离散的词（符号）映射为连续的向量空间
    #   使得语义相近的词在向量空间中距离也近
    #   Map discrete words to continuous vector space
    #
    # 【稠密向量 Dense Vector】
    #   向量中所有维度都有有意义的值（与稀疏向量相反）
    #   例如：[0.23, -0.15, 0.87, ...] 每个值都有语义含义
    #   All dimensions have meaningful values (opposite of sparse)
    #
    # 【Skip-gram 模型】
    #   用中心词预测上下文词
    #   输入："good"，预测：["very", "product"]
    #   训练目标：让 P(context | center) 最大
    #   Predict context words from center word
    #
    # 【CBOW (Continuous Bag of Words)】
    #   用上下文词预测中心词
    #   输入：["very", "product"]，预测："good"
    #   训练目标：让 P(center | context) 最大
    #   Predict center word from context words
    #
    # 【语义相似性 Semantic Similarity】
    #   词义相近的词向量距离也近
    #   著名例子：king - man + woman ≈ queen
    #   Words with similar meanings have similar vectors
    #
    # -------- 算法原理 / Algorithm --------
    #
    # 定义 / Definition:
    #   通过预测任务（上下文预测词）学习词的语义表示
    #   每个词映射为固定维度的稠密向量（如 100 维）
    #
    # 文档向量 / Document Vector:
    #   对文档中所有词向量取平均
    #   doc_vec = mean([word1_vec, word2_vec, ...])
    #   简单有效，但会丢失词序信息
    #
    # 举例 / Example:
    #   文档: ["good", "product"]
    #   good → [0.2, 0.5, -0.3, ...]  (100维)
    #   product → [0.1, 0.3, 0.4, ...]  (100维)
    #   文档向量 = 平均 = [0.15, 0.4, 0.05, ...]
    #
    # 相比 BoW/TF-IDF 的优势 / Advantages:
    #   - 低维稠密向量 (100维) vs 高维稀疏向量 (10000+维)
    #   - 能捕捉语义相似性（如 "good" 和 "great" 向量接近）
    # ================================================================


    # 同步划分 token 列表（Word2Vec 需要 token 列表输入）
    #   - train_test_split 在划分时会打乱数据顺序，train_index 保存了划分后的样本索引
    #   - 使用 .loc[index] 方法按索引从 tokens 列中提取对应行，确保数据对齐
    #   - Word2Vec 需要 token 列表（如 ['good', 'product']）而非字符串
    # Synchronize split for token lists (Word2Vec requires token list input)
    #   - train_test_split shuffles data, train_index stores the indices of split samples
    #   - Use .loc[index] to extract corresponding rows from tokens column, ensuring data alignment
    #   - Word2Vec requires token lists (e.g. ['good', 'product']) not strings
    X_train_tokens = df["tokens"].loc[train_index]
    X_test_tokens = df["tokens"].loc[test_index]

    # 在训练集上训练 Word2Vec 模型
    # Train Word2Vec model on training set
    # 参数：vector_size=100 每个词用100维向量表示，
    #       window=5 上下文窗口为前后各5个词，
    #       min_count=2 忽略出现次数少于2次的词（减少噪声），
    #       workers=4 使用4个线程并行训练
    # Parameters: vector_size=100 represents each word with a 100-dim vector,
    #       window=5 context window covers 5 words before and after,
    #       min_count=2 ignores words appearing less than 2 times (reduce noise),
    #       workers=4 uses 4 threads for parallel training
    print("Training Word2Vec model on training data...")
    w2v_model = Word2Vec(
        sentences=X_train_tokens.tolist(),
        vector_size=W2V_VECTOR_SIZE,
        window=W2V_WINDOW,
        min_count=W2V_MIN_COUNT,
        workers=W2V_WORKERS,
        seed=RANDOM_STATE,
    )

    print(f"Word2Vec parameters:")
    print(f"  vector_size: {W2V_VECTOR_SIZE}")
    print(f"  window:      {W2V_WINDOW}")
    print(f"  min_count:   {W2V_MIN_COUNT}")
    print(f"  Vocabulary size: {len(w2v_model.wv)}")

    # 将每个文档转换为平均词向量
    # Convert each document to average word vector
    # ----------------------------------------------------------------
    # 文档向量计算过程
    # Document vector computation process
    # ----------------------------------------------------------------
    #   1. 对文档中每个词，查找其 Word2Vec 向量
    #   2. 过滤掉不在词汇表中的词（如训练时未见过的词）
    #   3. 对所有词向量取平均，得到文档向量
    # ----------------------------------------------------------------
    #   1. For each word in document, look up its Word2Vec vector
    #   2. Filter out words not in vocabulary (unseen during training)
    #   3. Average all word vectors to get document vector
    # ----------------------------------------------------------------
    #
    # 举例 / Example:
    #   假设 vector_size=3（实际为 100 维）
    #   Assuming vector_size=3 (actually 100-dim)
    #
    #   词向量 / Word vectors:
    #     "good"    → [0.8, 0.2, 0.1]
    #     "product" → [0.3, 0.5, 0.4]
    #     "love"    → [0.7, 0.3, 0.2]
    #
    #   文档: ["good", "product", "love"]
    #   文档向量 = mean([[0.8, 0.2, 0.1], [0.3, 0.5, 0.4], [0.7, 0.3, 0.2]])
    #           = [(0.8+0.3+0.7)/3, (0.2+0.5+0.3)/3, (0.1+0.4+0.2)/3]
    #           = [0.6, 0.33, 0.23]
    #
    #   输出格式 / Output format:
    #     numpy 数组，形状 [样本数 × vector_size]
    #     numpy array, shape [num_samples × vector_size]
    #     相比 BoW/TF-IDF：稠密矩阵，维度低（100 vs 10000）
    #     Compared to BoW/TF-IDF: dense matrix, low-dim (100 vs 10000)
    # ----------------------------------------------------------------
    print("Computing document vectors...")
    X_train_w2v = np.array(
        [
            get_document_vector(tokens, w2v_model, W2V_VECTOR_SIZE)
            for tokens in X_train_tokens
        ]
    )
    X_test_w2v = np.array(
        [
            get_document_vector(tokens, w2v_model, W2V_VECTOR_SIZE)
            for tokens in X_test_tokens
        ]
    )

    print(f"Training feature matrix shape: {X_train_w2v.shape}")
    print(f"Test feature matrix shape:     {X_test_w2v.shape}")

    return X_train_w2v, X_test_w2v, w2v_model


# ============================================================
# 步骤 4：模型训练与评估
# Step 4: Model Training and Evaluation
# ============================================================
def train_and_evaluate(X_train, X_test, y_train, y_test, model, model_name, feature_name):
    """训练单个模型并评估，返回结果字典
    Train a single model and evaluate, return results dict"""

    # 训练模型
    # Train model
    model.fit(X_train, y_train)

    # 在测试集上预测
    # Predict on test set
    y_pred = model.predict(X_test)

    # ================================================================
    # 评估指标 / Evaluation Metrics
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【TP / TN / FP / FN】
    #   TP (True Positive):  实际是正类，预测也是正类（正确）
    #   TN (True Negative):  实际是负类，预测也是负类（正确）
    #   FP (False Positive): 实际是负类，预测为正类（误报）
    #   FN (False Negative): 实际是正类，预测为负类（漏报）
    #
    # 【Precision（精确率）】
    #   预测为正类中，实际是正类的比例
    #   公式：Precision = TP / (TP + FP)
    #   举例：预测 10 个垃圾邮件，8 个确实是垃圾 → Precision = 80%
    #   Of predicted positives, how many are actually positive
    #
    # 【Recall（召回率）】
    #   实际为正类中，被预测为正类的比例
    #   公式：Recall = TP / (TP + FN)
    #   举例：100 封垃圾邮件，模型找出 80 封 → Recall = 80%
    #   Of actual positives, how many are correctly predicted
    #
    # 【调和平均 Harmonic Mean】
    #   一种平均方法，对较小值更敏感
    #   普通平均 (0.9+0.1)/2 = 0.5，调和平均 2×0.9×0.1/(0.9+0.1) = 0.18
    #   意义：防止一高一低的情况被掩盖
    #   Average method that is more sensitive to smaller values
    #
    # ================================================================

    # ================================================================
    # 评估指标 1：Accuracy（准确率）
    # Metric 1: Accuracy
    # ================================================================
    # 定义 / Definition:
    #   Accuracy = 正确预测数 / 总样本数
    #   Accuracy = Correct predictions / Total samples
    #
    # 公式 / Formula:
    #   Accuracy = (TP + TN) / (TP + TN + FP + FN)
    #
    # 举例 / Example:
    #   100 个样本，80 个预测正确 → Accuracy = 80%
    #
    # 局限性 / Limitation:
    #   不平衡数据可能误导
    #   例如：95% 是正类，模型全猜正也有 95% 准确率
    # ================================================================
    acc = accuracy_score(y_test, y_pred)

    # ================================================================
    # 评估指标 2：F1-score（F1 分数）
    # Metric 2: F1-score
    # ================================================================
    # 定义 / Definition:
    #   F1 = Precision 和 Recall 的调和平均数
    #   F1 = Harmonic mean of Precision and Recall
    #
    # 公式 / Formula:
    #   F1 = 2 × (Precision × Recall) / (Precision + Recall)
    #
    # 举例 / Example:
    #   Precision=0.8, Recall=0.6
    #   F1 = 2 × (0.8 × 0.6) / (0.8 + 0.6) = 0.686
    #
    # weighted 模式 / Weighted mode:
    #   按类别样本数加权平均各类别的 F1
    #   适合多分类不平衡场景
    # ================================================================
    f1 = f1_score(y_test, y_pred, average="weighted")

    # ================================================================
    # 评估指标 3：Confusion Matrix（混淆矩阵）
    # Metric 3: Confusion Matrix
    # ================================================================
    # 定义 / Definition:
    #   显示每个类别的预测结果分布
    #   Shows prediction distribution for each class
    #
    # 矩阵结构 / Matrix Structure:
    #            预测类别 (Predicted)
    #              1    2    3    4    5
    #   真实  1 [ 85   5    3    2    5 ]  ← 类别1的样本被预测成各类的数量
    #   类别  2 [  8  72   10   5    5 ]
    #   (True) 
    #
    # 解读 / Interpretation:
    #   对角线元素：正确预测（越大越好）
    #   非对角线元素：误分类（越小越好）
    #   例如：[1,2]=5 表示 5 个类别 1 被错误预测为类别 2
    #
    # 用途 / Usage:
    #   识别易混淆的类别对，发现系统性错误模式
    # ================================================================
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n  {model_name} + {feature_name}:")
    print(f"    Accuracy: {acc:.4f}")
    print(f"    F1-score (weighted): {f1:.4f}")

    return {
        "feature": feature_name,
        "model_name": model_name,
        "model": model,
        "accuracy": acc,
        "f1_score": f1,
        "confusion_matrix": cm,
        "y_pred": y_pred,
        "y_test": y_test,
    }


def run_all_models(features_dict, y_train, y_test):
    """在所有特征和模型组合上训练并评估
    Train and evaluate on all feature and model combinations"""

    print("\n" + "=" * 60)
    print("Step 4: Model Training and Evaluation")
    print("=" * 60)

    classifiers = {
        # ================================================================
        # 分类器 1：Logistic Regression（逻辑回归）
        # Classifier 1: Logistic Regression
        # ================================================================
        #
        # -------- 术语解释 / Terminology --------
        #
        # 【二分类 Binary Classification】
        #   只有两个类别的分类问题，如：垃圾邮件(1) vs 正常邮件(0)
        #   Classification with only 2 classes, e.g., spam(1) vs normal(0)
        #
        # 【多分类 Multi-class Classification】
        #   有多个类别的分类问题，如：评分 1,2,3,4,5 星
        #   Classification with multiple classes, e.g., rating 1,2,3,4,5 stars
        #
        # 【sigmoid 函数】
        #   将任意实数压缩到 (0,1) 区间，输出可解释为概率
        #   公式：σ(z) = 1 / (1 + e^(-z))
        #   举例：σ(0)=0.5, σ(2)=0.88, σ(-2)=0.12
        #   Compresses any real number to (0,1), output = probability
        #
        # 【softmax 函数】
        #   多分类版本的 sigmoid，将向量转为概率分布（和为1）
        #   公式：P(y=k) = e^(z_k) / Σ e^(z_j)
        #   举例：z=[2,1,0] → softmax=[0.67, 0.24, 0.09]（和=1）
        #   Multi-class sigmoid, converts vector to probability distribution (sum=1)
        #
        # 【损失函数 Loss Function】
        #   衡量模型预测与真实值的差距，训练目标是最小化损失
        #   Measures gap between prediction and truth, training minimizes loss
        #
        # 【交叉熵 Cross-entropy】
        #   分类问题常用的损失函数，惩罚错误的概率预测
        #   公式：L = -Σ y_true × log(y_pred)
        #   举例：真实=1，预测概率=0.9 → L=-log(0.9)=0.105（小损失，好）
        #         真实=1，预测概率=0.1 → L=-log(0.1)=2.303（大损失，差）
        #   Common loss for classification, penalizes wrong probability predictions
        #
        # -------- 算法原理 / Algorithm --------
        #
        # 定义 / Definition:
        #   通过 sigmoid(二分类) 或 softmax(多分类) 将线性输出映射到概率
        #   Map linear output to probability via sigmoid/softmax
        #
        # 公式 / Formula:
        #   二分类：P(y=1|x) = sigmoid(w·x) = 1 / (1 + e^(-w·x))
        #   多分类：P(y=k|x) = softmax(w_k·x) = e^(w_k·x) / Σ e^(w_j·x)
        #
        # 举例 / Example:
        #   特征 x=[0.5,0.3,0.8], 权重 w=[0.2,-0.1,0.5]
        #   线性输出 z = 0.5×0.2 + 0.3×(-0.1) + 0.8×0.5 = 0.47
        #   概率 = sigmoid(0.47) = 1/(1+e^(-0.47)) = 0.615
        #   因为 0.615 > 0.5，预测为正类
        #
        # 优点 / Advantages:
        #   - 输出概率值，可解释性强（知道模型有多"自信"）
        #   - 训练速度快，适合大规模数据
        #   - 有正则化，不易过拟合
        # ================================================================
        "Logistic Regression": LogisticRegression(
            max_iter=LR_MAX_ITER,           # 最大迭代次数
            random_state=RANDOM_STATE
        ),

        # ================================================================
        # 分类器 2：Linear SVM（线性支持向量机）
        # Classifier 2: Linear SVM (Support Vector Machine)
        # ================================================================
        #
        # -------- 术语解释 / Terminology --------
        #
        # 【超平面 Hyperplane】
        #   在 N 维空间中分隔数据的 N-1 维"平面"
        #   2D 中是一条线，3D 中是一个平面，高维中叫超平面
        #   A (N-1)-dimensional "plane" separating data in N-dimensional space
        #
        # 【间隔 Margin】
        #   超平面到最近训练样本的距离
        #   SVM 的目标是找到使间隔最大的超平面（泛化能力更强）
        #   Distance from hyperplane to nearest training samples
        #   SVM aims to find hyperplane with maximum margin (better generalization)
        #
        # 【支持向量 Support Vectors】
        #   距离超平面最近的那些训练样本
        #   只有它们决定超平面的位置，其他样本可以删除不影响结果
        #   Training samples closest to the hyperplane
        #   Only they determine hyperplane position; other samples can be removed
        #
        # 【Hinge Loss（合页损失）】
        #   SVM 的损失函数，只惩罚分类错误或在间隔内的样本
        #   公式：L = max(0, 1 - y·f(x))  其中 y∈{-1,+1}
        #   举例：正确分类且远离边界 → L=0（无损失）
        #         分类错误或靠近边界 → L>0（有损失）
        #   SVM loss function, only penalizes misclassified or margin-violating samples
        #
        # -------- 算法原理 / Algorithm --------
        #
        # 定义 / Definition:
        #   在高维空间中寻找最优超平面，最大化类别间隔
        #   Find optimal hyperplane in high-dim space, maximize margin
        #
        # 公式 / Formula:
        #   超平面方程：w·x + b = 0
        #   决策规则：sign(w·x + b)
        #     若 w·x + b > 0 → 正类
        #     若 w·x + b < 0 → 负类
        #
        # 举例 / Example:
        #   想象二维平面上有两类点（红和蓝）
        #   SVM 找一条线（超平面）把它们分开
        #   这条线要离两边的点都尽量远（最大间隔）
        #   最靠近这条线的点就是"支持向量"
        #
        # 优点 / Advantages:
        #   - 对高维稀疏数据（如文本 TF-IDF）效果特别好
        #   - 间隔最大化提供良好的泛化能力
        #   - 只依赖支持向量，对异常值不敏感
        #
        # 与 Logistic Regression 的区别 / Difference from LR:
        #   - LR 输出概率（如 0.85），SVM 输出距离超平面的距离
        #   - LR 使用所有样本计算损失，SVM 主要依赖边界样本（支持向量）
        #   - SVM 更"硬"：正确分类的远离边界的样本不产生损失
        # ================================================================
        "Linear SVM": LinearSVC(
            max_iter=LR_MAX_ITER,            # 最大迭代次数
            dual="auto",                      # 自动选择求解策略
            random_state=RANDOM_STATE
        ),
    }

    all_results = []

    # 遍历所有特征 × 模型组合
    # Iterate through all feature × model combinations
    for feature_name, (X_train_feat, X_test_feat) in features_dict.items():
        for model_name, model in classifiers.items():
            # 为每个组合创建新的模型实例（避免状态泄露）
            # Create a new model instance for each combination (avoid state leakage)
            from sklearn.base import clone

            model_clone = clone(model)
            result = train_and_evaluate(
                X_train_feat, X_test_feat, y_train, y_test,
                model_clone, model_name, feature_name
            )
            all_results.append(result)

    return all_results


# ============================================================
# 步骤 5：结果可视化 - 混淆矩阵
# Step 5: Results Visualization - Confusion Matrix
# ============================================================
def plot_confusion_matrices(all_results):
    """为所有模型绘制混淆矩阵
    Plot confusion matrices for all models"""

    print("\n" + "=" * 60)
    print("Step 5: Confusion Matrices")
    print("=" * 60)

    # 创建 2 行 3 列的子图布局（2 个模型 × 3 种特征）
    # Create 2x3 subplot layout (2 models × 3 features)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Confusion Matrices for All Model-Feature Combinations", fontsize=14)

    for idx, result in enumerate(all_results):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]

        # 绘制混淆矩阵热力图
        # Plot confusion matrix heatmap
        disp = ConfusionMatrixDisplay(
            confusion_matrix=result["confusion_matrix"],
            display_labels=[1, 2, 3, 4, 5]
        )
        disp.plot(ax=ax, cmap="Blues", values_format="d")
        ax.set_title(f"{result['model_name']}\n{result['feature']}")

    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, "confusion_matrices.png"),
        dpi=150, bbox_inches="tight"
    )
    plt.close()
    print(f"Saved: {OUTPUT_DIR}/confusion_matrices.png")


# ============================================================
# 步骤 6：结果汇总表
# Step 6: Results Summary Table
# ============================================================
def print_results_summary(all_results):
    """打印所有模型的结果汇总表
    Print results summary table for all models"""

    print("\n" + "=" * 60)
    print("Step 6: Results Summary")
    print("=" * 60)

    # 构建结果表格
    # Build results table
    table_data = []
    for r in all_results:
        table_data.append([
            r["feature"],
            r["model_name"],
            f"{r['accuracy']:.4f}",
            f"{r['f1_score']:.4f}",
        ])

    headers = ["Feature Type", "Model", "Accuracy", "F1-score"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # 找出最佳模型
    # Find the best model
    best = max(all_results, key=lambda x: x["accuracy"])
    print(f"\nBest model: {best['model_name']} + {best['feature']}")
    print(f"  Accuracy: {best['accuracy']:.4f}")
    print(f"  F1-score: {best['f1_score']:.4f}")

    return best


# ============================================================
# 步骤 7：超参数调优
# Step 7: Hyperparameter Tuning
# ============================================================
def tune_hyperparameters(X_train_tfidf, y_train, X_test_tfidf, y_test):
    """对最佳特征组合进行超参数调优
    Perform hyperparameter tuning on the best feature combination"""

    print("\n" + "=" * 60)
    print("Step 7: Hyperparameter Tuning")
    print("=" * 60)

    # ================================================================
    # 超参数调优：GridSearchCV（网格搜索 + 交叉验证）
    # Hyperparameter Tuning: GridSearchCV (Grid Search + Cross Validation)
    # ================================================================
    #
    # -------- 术语解释 / Terminology --------
    #
    # 【超参数 Hyperparameter】
    #   训练前手动设置的参数，不是从数据中学习的
    #   例如：正则化强度 C、学习率、树的深度等
    #   Parameters set manually before training, not learned from data
    #
    # 【交叉验证 Cross Validation (CV)】
    #   将训练集分成 K 份，轮流用 K-1 份训练，1 份验证
    #   重复 K 次，取平均分数作为模型性能评估
    #   目的：更可靠地评估模型性能，减少单次划分的随机性
    #   Split training set into K folds, train on K-1, validate on 1
    #
    # 【过拟合 Overfitting】
    #   模型在训练集上表现很好，但在新数据上表现差
    #   原因：模型过于复杂，"记住"了训练数据的噪声
    #   Model performs well on training data but poorly on new data
    #
    # 【欠拟合 Underfitting】
    #   模型在训练集上表现就不好
    #   原因：模型过于简单，无法捕捉数据的规律
    #   Model performs poorly even on training data
    #
    # 【正则化 Regularization】
    #   限制模型复杂度的技术，防止过拟合
    #   通过惩罚大的权重值来实现
    #   Technique to limit model complexity, prevent overfitting
    #
    # -------- 算法原理 / Algorithm --------
    #
    # 定义 / Definition:
    #   GridSearchCV = 网格搜索 + 交叉验证
    #   穷举所有参数组合，用交叉验证评估每个组合
    #
    # 工作原理 / How it works:
    #   1. 定义参数网格：列出每个超参数的候选值
    #   2. 穷举所有组合：尝试每个可能的参数组合
    #   3. 交叉验证评估：对每个组合进行 K 折交叉验证
    #   4. 选择最优：返回平均验证分数最高的组合
    #
    # 举例 / Example:
    #   参数网格：C = [0.1, 1, 10], solver = [lbfgs, saga]
    #   组合数：3 × 2 = 6 种组合
    #   5 折交叉验证 → 每个组合训练 5 次
    #   共训练：6 × 5 = 30 次
    #   结果：选择 CV accuracy 平均值最高的组合
    # ================================================================

    print("\n--- Logistic Regression Tuning ---")

    # ================================================================
    # 超参数：C（正则化强度的倒数）
    # Hyperparameter: C (inverse of regularization strength)
    # ================================================================
    # 定义 / Definition:
    #   C 控制正则化的强度，防止过拟合
    #   C controls regularization strength, prevents overfitting
    #
    # 公式 / Formula:
    #   C 越大 → 正则化越弱 → 模型越复杂 → 可能过拟合
    #   C 越小 → 正则化越强 → 模型越简单 → 可能欠拟合
    #
    # 举例 / Example:
    #   C=0.01：强正则化，简单模型，可能欠拟合
    #   C=1.0： 适中正则化，平衡复杂度
    #   C=10.0：弱正则化，复杂模型，可能过拟合
    # ================================================================
    lr_param_grid = {
        "C": [0.01, 0.1, 1.0, 10.0],
        "solver": ["lbfgs", "saga"],
    }

    lr_grid = GridSearchCV(
        LogisticRegression(max_iter=LR_MAX_ITER, random_state=RANDOM_STATE),
        lr_param_grid,
        cv=CV_FOLDS,       # 5 折交叉验证
        scoring="accuracy", # 用准确率评分
        n_jobs=-1,         # 并行计算
        verbose=0,
    )

    # fit 执行网格搜索：训练 8×5=40 个模型
    lr_grid.fit(X_train_tfidf, y_train)

    print(f"Best parameters: {lr_grid.best_params_}")
    print(f"Best CV accuracy: {lr_grid.best_score_:.4f}")

    # 用最佳参数在测试集上评估
    # Evaluate with best parameters on test set
    lr_best_pred = lr_grid.best_estimator_.predict(X_test_tfidf)
    lr_best_acc = accuracy_score(y_test, lr_best_pred)
    lr_best_f1 = f1_score(y_test, lr_best_pred, average="weighted")
    print(f"Test accuracy (tuned): {lr_best_acc:.4f}")
    print(f"Test F1-score (tuned): {lr_best_f1:.4f}")

    # 对 Linear SVM 进行网格搜索
    # Grid search for Linear SVM
    print("\n--- Linear SVM Tuning ---")
    svm_param_grid = {
        "C": [0.01, 0.1, 1.0, 10.0],
    }

    svm_grid = GridSearchCV(
        LinearSVC(max_iter=LR_MAX_ITER, dual="auto", random_state=RANDOM_STATE),
        svm_param_grid,
        cv=CV_FOLDS,
        scoring="accuracy",
        n_jobs=-1,
        verbose=0,
    )
    svm_grid.fit(X_train_tfidf, y_train)

    print(f"Best parameters: {svm_grid.best_params_}")
    print(f"Best CV accuracy: {svm_grid.best_score_:.4f}")

    # 用最佳参数在测试集上评估
    # Evaluate with best parameters on test set
    svm_best_pred = svm_grid.best_estimator_.predict(X_test_tfidf)
    svm_best_acc = accuracy_score(y_test, svm_best_pred)
    svm_best_f1 = f1_score(y_test, svm_best_pred, average="weighted")
    print(f"Test accuracy (tuned): {svm_best_acc:.4f}")
    print(f"Test F1-score (tuned): {svm_best_f1:.4f}")

    # 汇总调优结果
    # Summarize tuning results
    print("\n--- Tuning Summary ---")
    tuning_table = [
        ["Logistic Regression", str(lr_grid.best_params_), f"{lr_best_acc:.4f}", f"{lr_best_f1:.4f}"],
        ["Linear SVM", str(svm_grid.best_params_), f"{svm_best_acc:.4f}", f"{svm_best_f1:.4f}"],
    ]
    print(tabulate(tuning_table, headers=["Model", "Best Params", "Accuracy", "F1-score"], tablefmt="grid"))

    return lr_grid, svm_grid


# ============================================================
# 步骤 8：错误分析 (Part 2)
# Step 8: Error Analysis (Part 2)
# ============================================================
def error_analysis(all_results, X_test_text, y_test):
    """分析不同特征表示下的误分类样本
    Analyze misclassified samples across different feature representations"""

    print("\n" + "=" * 60)
    print("Step 8: Error Analysis (Part 2)")
    print("=" * 60)

    # 为每种特征收集误分类样本的索引（使用第一个模型的结果）
    # Collect misclassified sample indices for each feature (use first model's results)
    feature_errors = {}
    for result in all_results:
        feature_name = result["feature"]
        model_name = result["model_name"]
        y_pred = result["y_pred"]
        y_true = result["y_test"]

        # 获取误分类的索引
        # Get misclassified indices
        error_mask = y_pred != y_true.values
        error_indices = set(y_true.index[error_mask])

        key = f"{feature_name} ({model_name})"
        feature_errors[key] = error_indices
        print(f"\n{key}: {len(error_indices)} misclassified samples")

    # 按纯特征类型分组（合并两个模型的错误）
    # Group by pure feature type (merge errors from both models)
    ngram_errors = set()
    tfidf_errors = set()
    embedding_errors = set()

    for key, indices in feature_errors.items():
        if "n-gram" in key:
            ngram_errors.update(indices)
        elif "TF-IDF" in key:
            tfidf_errors.update(indices)
        elif "Word2Vec" in key:
            embedding_errors.update(indices)

    # 分析三种情况
    # Analyze three scenarios
    print("\n" + "-" * 40)
    print("Error Analysis Categories:")
    print("-" * 40)

    # 1. 所有表示都误分类的样本
    # 1. Samples misclassified by all representations
    common_errors = ngram_errors & tfidf_errors & embedding_errors
    print(f"\n1. Misclassified by ALL representations: {len(common_errors)} samples")

    # 2. 仅简单模型（BoW/TF-IDF）误分类的样本
    # 2. Samples misclassified only by simpler models (BoW/TF-IDF)
    simple_only_errors = (ngram_errors | tfidf_errors) - embedding_errors
    print(f"2. Misclassified by BoW/TF-IDF ONLY: {len(simple_only_errors)} samples")

    # 3. 仅嵌入模型误分类的样本
    # 3. Samples misclassified only by embedding-based models
    embedding_only_errors = embedding_errors - (ngram_errors | tfidf_errors)
    print(f"3. Misclassified by Word2Vec ONLY: {len(embedding_only_errors)} samples")

    # 展示每类错误的具体样例
    # Display specific examples for each error category
    categories = {
        "Misclassified by ALL representations": common_errors,
        "Misclassified by BoW/TF-IDF ONLY": simple_only_errors,
        "Misclassified by Word2Vec ONLY": embedding_only_errors,
    }

    # 获取每种特征的最佳模型预测结果（用于展示）
    # Get best model predictions for each feature (for display)
    pred_by_feature = {}
    for result in all_results:
        feature_name = result["feature"]
        if feature_name not in pred_by_feature:
            pred_by_feature[feature_name] = pd.Series(
                result["y_pred"], index=result["y_test"].index
            )

    for category_name, error_set in categories.items():
        print(f"\n{'=' * 40}")
        print(f"{category_name}")
        print(f"{'=' * 40}")

        if not error_set:
            print("  No samples in this category.")
            continue

        # 选择最多 10 个样例展示
        # Select up to 10 examples to display
        sample_indices = list(error_set)[:10]

        for idx in sample_indices:
            if idx in X_test_text.index:
                text = X_test_text.loc[idx]
                true_label = y_test.loc[idx]

                # 截断过长文本
                # Truncate long text
                display_text = text[:150] + "..." if len(str(text)) > 150 else text
                print(f"\n  Index: {idx}")
                print(f"  True label: {true_label}")

                # 显示各特征的预测结果
                # Display predictions from each feature
                for feat_name, preds in pred_by_feature.items():
                    if idx in preds.index:
                        print(f"  {feat_name} predicted: {preds.loc[idx]}")

                print(f"  Text: {display_text}")

    # 错误原因分析
    # Error cause analysis
    print("\n" + "=" * 40)
    print("Error Analysis Discussion")
    print("=" * 40)
    print("""
Common causes of misclassification:

1. Ambiguity: Words with different meanings in different contexts.
   Example: "sick" can mean "ill" (negative) or "amazing" (positive slang).

2. Sarcasm/Irony: Surface-level positive words but negative intent.
   Example: "Oh great, another product that doesn't work."

3. Mixed sentiment: Reviews containing both positive and negative aspects.
   Example: "Great product but terrible customer service."

4. Short text: Insufficient information for accurate classification.
   Very short reviews lack enough features for reliable prediction.

5. Class boundary: Scores 2-4 are inherently harder to distinguish
   than extreme scores (1 and 5), as the sentiment is more subtle.

Why BoW/TF-IDF fail but embeddings succeed:
  - BoW/TF-IDF treat words independently (bag of words assumption)
  - Cannot capture word order or semantic relationships
  - Embeddings capture semantic similarity between words

Why embeddings fail but BoW/TF-IDF succeed:
  - Averaging word vectors dilutes key discriminative words
  - BoW/TF-IDF preserve exact word occurrences and their importance
  - Some reviews rely on specific keywords rather than semantics
""")

    return categories


# ============================================================
# 主函数
# Main Function
# ============================================================
def main():
    # ============================================================
    # 步骤 0：实验初始化
    # Step 0: Lab Initialization
    # ============================================================
    student_name, student_number = initialize_lab()

    # ============================================================
    # 步骤 1：数据加载
    # Step 1: Data Loading
    # ============================================================
    df = load_data("Reviews.csv")

    # ============================================================
    # 步骤 2：数据预处理
    # Step 2: Data Preprocessing
    # ============================================================
    df = preprocess_dataset(df)

    # ============================================================
    # 步骤 3A：训练集/测试集划分
    # Step 3A: Train/Test Split
    # ============================================================
    X_train, X_test, y_train, y_test = split_data(df)

    # ============================================================
    # 步骤 3B：n-gram (BoW) 特征提取
    # Step 3B: n-gram (BoW) Feature Extraction
    # ============================================================
    X_train_bow, X_test_bow, bow_vectorizer = extract_ngram_features(X_train, X_test)

    # ============================================================
    # 步骤 3C：TF-IDF 特征提取
    # Step 3C: TF-IDF Feature Extraction
    # ============================================================
    X_train_tfidf, X_test_tfidf, tfidf_vectorizer = extract_tfidf_features(X_train, X_test)

    # ============================================================
    # 步骤 3D：Word2Vec 特征提取
    # Step 3D: Word2Vec Feature Extraction
    # ============================================================
    X_train_w2v, X_test_w2v, w2v_model = extract_word2vec_features(df, X_train.index, X_test.index)

    # 组织所有特征供模型训练使用
    # Organize all features for model training
    features_dict = {
        "n-gram (BoW)": (X_train_bow, X_test_bow),
        "TF-IDF": (X_train_tfidf, X_test_tfidf),
        "Word2Vec": (X_train_w2v, X_test_w2v),
    }

    # ============================================================
    # 步骤 4：训练所有模型并评估
    # Step 4: Train All Models and Evaluate
    # ============================================================
    all_results = run_all_models(features_dict, y_train, y_test)

    # ============================================================
    # 步骤 5：绘制混淆矩阵
    # Step 5: Plot Confusion Matrices
    # ============================================================
    plot_confusion_matrices(all_results)

    # ============================================================
    # 步骤 6：打印结果汇总
    # Step 6: Print Results Summary
    # ============================================================
    best = print_results_summary(all_results)

    # ============================================================
    # 步骤 7：超参数调优（使用 TF-IDF 特征）
    # Step 7: Hyperparameter Tuning (using TF-IDF features)
    # ============================================================
    lr_grid, svm_grid = tune_hyperparameters(X_train_tfidf, y_train, X_test_tfidf, y_test)

    # ============================================================
    # 步骤 8：错误分析
    # Step 8: Error Analysis
    # ============================================================
    X_test_text = df.loc[X_test.index, "Text"]
    categories = error_analysis(all_results, X_test_text, y_test)


# 程序入口点
# Program entry point
if __name__ == "__main__":
    main()
