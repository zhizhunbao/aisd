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

    # 分词
    # Tokenization
    tokens = word_tokenize(text)

    # 移除停用词
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    # 词形还原（还原为词典形式，比词干提取更准确）
    # Lemmatization (reduce to dictionary form, more accurate than stemming)
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

    # 分离特征和标签
    # Separate features and labels
    X = df["cleaned_text"]
    X_tokens = df["tokens"]
    y = df["Score"]

    # 使用分层抽样划分数据集（保持各类别比例一致）
    # Use stratified sampling to split dataset (maintain class proportions)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    # 同步划分 token 列表（Word2Vec 需要 token 列表输入）
    # Synchronize split for token lists (Word2Vec requires token list input)
    X_train_tokens = X_tokens.loc[X_train.index]
    X_test_tokens = X_tokens.loc[X_test.index]

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

    return X_train, X_test, y_train, y_test, X_train_tokens, X_test_tokens


# ============================================================
# 步骤 3B：特征提取 - n-gram (BoW)
# Step 3B: Feature Extraction - n-gram (BoW)
# ============================================================
def extract_ngram_features(X_train, X_test):
    """使用CountVectorizer提取n-gram (BoW)特征
    Extract n-gram (BoW) features using CountVectorizer"""

    print("\n" + "=" * 60)
    print("Step 3B: Feature Extraction - n-gram (BoW)")
    print("=" * 60)

    # 创建 CountVectorizer：unigram + bigram，限制最大特征数
    # Create CountVectorizer: unigram + bigram, limit max features
    # 参数：ngram_range=(1,2) 表示同时使用单个词和两个连续词作为特征，
    #       max_features=10000 限制词汇表大小以降低维度和内存使用
    # Parameters: ngram_range=(1,2) uses both single words and consecutive word pairs as features,
    #       max_features=10000 limits vocabulary size to reduce dimensionality and memory usage
    bow_vectorizer = CountVectorizer(
        ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
    )

    # 在训练集上拟合并转换，在测试集上仅转换（防止数据泄露）
    # Fit and transform on training set, only transform on test set (prevent data leakage)
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

    # 创建 TfidfVectorizer：TF-IDF 在 BoW 基础上增加逆文档频率权重，
    #   降低常见词的权重，提升稀有但有区分度的词的权重
    # Create TfidfVectorizer: TF-IDF adds inverse document frequency weighting on top of BoW,
    #   reduces weight of common words, increases weight of rare but discriminative words
    tfidf_vectorizer = TfidfVectorizer(
        ngram_range=NGRAM_RANGE, max_features=MAX_FEATURES
    )

    # 在训练集上拟合并转换，在测试集上仅转换
    # Fit and transform on training set, only transform on test set
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


def extract_word2vec_features(X_train_tokens, X_test_tokens):
    """训练Word2Vec模型并提取文档向量
    Train Word2Vec model and extract document vectors"""

    print("\n" + "=" * 60)
    print("Step 3D: Feature Extraction - Word2Vec")
    print("=" * 60)

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

    # 计算评估指标
    # Calculate evaluation metrics
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
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

    # 定义两个分类器
    # Define two classifiers
    # Logistic Regression：多分类使用 multinomial 策略，lbfgs 求解器适合中等规模数据
    # Logistic Regression: multinomial strategy for multiclass, lbfgs solver for medium-scale data
    # LinearSVC：线性 SVM，dual="auto" 让算法自动选择求解策略
    # LinearSVC: linear SVM, dual="auto" lets the algorithm auto-select solving strategy
    classifiers = {
        "Logistic Regression": LogisticRegression(
            max_iter=LR_MAX_ITER, multi_class="multinomial", random_state=RANDOM_STATE
        ),
        "Linear SVM": LinearSVC(
            max_iter=LR_MAX_ITER, dual="auto", random_state=RANDOM_STATE
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

    # 对 Logistic Regression 进行网格搜索
    # Grid search for Logistic Regression
    # 参数空间：C 控制正则化强度（越大正则化越弱，可能过拟合；越小正则化越强，可能欠拟合）
    # Parameter space: C controls regularization strength (larger = less regularization, may overfit;
    #   smaller = more regularization, may underfit)
    print("\n--- Logistic Regression Tuning ---")
    lr_param_grid = {
        "C": [0.01, 0.1, 1.0, 10.0],
        "solver": ["lbfgs", "saga"],
    }

    lr_grid = GridSearchCV(
        LogisticRegression(max_iter=LR_MAX_ITER, multi_class="multinomial", random_state=RANDOM_STATE),
        lr_param_grid,
        cv=CV_FOLDS,
        scoring="accuracy",
        n_jobs=-1,
        verbose=0,
    )
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
    X_train, X_test, y_train, y_test, X_train_tokens, X_test_tokens = split_data(df)

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
    X_train_w2v, X_test_w2v, w2v_model = extract_word2vec_features(X_train_tokens, X_test_tokens)

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
