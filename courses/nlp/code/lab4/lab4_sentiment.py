"""
CST8507 Lab 4: Sentiment Analysis using DistilBERT
Author: Peng Wang
Student Number: 041107730

Implement sentiment analysis on the Movie Review Polarity Dataset using
two approaches: a TF-IDF + Logistic Regression baseline and a fine-tuned
DistilBERT transformer model. Compare their performance and make predictions
on new text samples.
"""

import os
import re
import tarfile
import urllib.request
from collections import Counter

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from tabulate import tabulate

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
    get_linear_schedule_with_warmup,
)

# ============================================================
# 环境设置
# Environment Setup
# ============================================================

# 加载环境变量
# Load environment variables
load_dotenv('.env.local')
STUDENT_NAME = os.getenv('NAME', 'Peng Wang')
STUDENT_NUMBER = os.getenv('NUMBER', '041107730')

# 脚本目录路径（兼容脚本和 Notebook 两种运行方式）
# Script directory path (compatible with both script and Notebook execution)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()

# 设置 pandas 显示选项
# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)

# ============================================================
# 配置常量
# Configuration Constants
# ============================================================

# 数据集下载地址
# Dataset download URL
DATASET_URL = "http://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz"

# 数据集文件名和解压目录
# Dataset filename and extraction directory
DATASET_FILENAME = "review_polarity.tar.gz"
DATASET_DIR = os.path.join(SCRIPT_DIR, "txt_sentoken")

# 剪枝阈值：出现次数 <= 此值的词将被移除
# Pruning threshold: words with frequency <= this value will be removed
PRUNING_THRESHOLD = 2

# 打印的高频词数量
# Number of top frequent words to print
TOP_FREQUENT_WORDS = 50

# 训练/测试集拆分比例
# Train/test split ratio
TEST_SIZE = 0.2

# 随机种子
# Random seed for reproducibility
RANDOM_STATE = 42

# DistilBERT 模型名称
# DistilBERT model name
DISTILBERT_MODEL_NAME = "distilbert-base-uncased"

# DistilBERT 训练超参数
# DistilBERT training hyperparameters

# 最大序列长度：DistilBERT 最多支持 512 个 token，128 足够覆盖大部分短评论
# Max sequence length: DistilBERT supports up to 512 tokens, 128 is enough for most short reviews
MAX_SEQ_LENGTH = 128

# 批大小：每次训练迭代处理的样本数，16 在单 GPU 上内存友好
# Batch size: number of samples per training iteration, 16 is memory-friendly on single GPU
BATCH_SIZE = 16

# 训练轮数：3 轮通常足以微调预训练 Transformer，更多轮可能过拟合
# Number of epochs: 3 is usually sufficient for fine-tuning pre-trained Transformers, more may overfit
NUM_EPOCHS = 3

# 学习率：0.00002 是 BERT/DistilBERT 微调的推荐学习率
# Learning rate: 0.00002 is the recommended learning rate for BERT/DistilBERT fine-tuning
LEARNING_RATE = 0.00002

# 情感类别标签
# Sentiment class labels
LABEL_NAMES = ["Negative", "Positive"]

# 图表输出目录
# Chart output directory
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "lab4_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 新文本样本（用于最终预测演示）
# New text samples (for final prediction demonstration)
NEW_TEXT_SAMPLES = [
    "This book was great!",
    "This book was terrible!",
    "To say that this is the worst story ever is to insult the worst story ever!",
    "I loved this book!",
    "It was so-so!",
    "This novel was good enough for me!",
    "Total piece of garbage",
    "Most amazing stories ever that inspired me to great things!",
    "It would be neither confusing nor coherent to describe the novel in some optimal way that does not distract from its idiocratic syncronicity",
]

# 打印程序标题
# Print program header
print("=" * 60)
print("CST8507 Lab 4: Sentiment Analysis using DistilBERT")
print(f"Author: {STUDENT_NAME} ({STUDENT_NUMBER})")
print("=" * 60)
print()

# 选择计算设备（GPU 可用时使用 GPU，否则 CPU）
# Select compute device (use GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
print()


# ============================================================
# 步骤 1：下载并加载数据集
# Step 1: Download and Load Dataset
# ============================================================

print("=" * 60)
print("Step 1: Download and Load Dataset")
print("=" * 60)

# 下载数据集（如果本地不存在）
# Download dataset (if not already present locally)
dataset_path = os.path.join(SCRIPT_DIR, DATASET_FILENAME)
if not os.path.exists(DATASET_DIR):
    if not os.path.exists(dataset_path):
        print(f"Downloading dataset from {DATASET_URL}...")
        urllib.request.urlretrieve(DATASET_URL, dataset_path)
        print("Download complete.")

    # 解压 tar.gz 文件
    # Extract tar.gz file
    print("Extracting dataset...")
    with tarfile.open(dataset_path, "r:gz") as tar:
        tar.extractall(path=SCRIPT_DIR)
    print("Extraction complete.")
else:
    print("Dataset already exists locally.")

# 加载正面和负面评论
# Load positive and negative reviews
pos_dir = os.path.join(DATASET_DIR, "pos")
neg_dir = os.path.join(DATASET_DIR, "neg")


def load_reviews(directory):
    """Load all review text files from a directory.

    Args:
        directory: Path to directory containing .txt review files.

    Returns:
        List of review text strings.
    """
    reviews = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                reviews.append(f.read())
    return reviews


# 加载所有评论
# Load all reviews
pos_reviews = load_reviews(pos_dir)
neg_reviews = load_reviews(neg_dir)

print(f"Positive reviews loaded: {len(pos_reviews)}")
print(f"Negative reviews loaded: {len(neg_reviews)}")
print(f"Total reviews: {len(pos_reviews) + len(neg_reviews)}")
print()


# ============================================================
# 步骤 2：文本预处理
# Step 2: Text Preprocessing
# ============================================================

print("=" * 60)
print("Step 2: Text Preprocessing")
print("=" * 60)


def clean_text(text):
    """清理文本数据：去除标点、数字、转小写
    Clean text data: remove punctuation, numbers, convert to lowercase.

    Args:
        text: Raw review text string.

    Returns:
        Cleaned text with only lowercase alphabetic words.
    """
    # 转小写
    # Convert to lowercase
    text = text.lower()

    # 移除标点和数字，仅保留字母和空格
    # Remove punctuation and numbers, keep only letters and spaces
    text = re.sub(r"[^a-z\s]", "", text)

    # 将多个空格合并为一个
    # Merge multiple spaces into one
    text = re.sub(r"\s+", " ", text).strip()

    return text


# 清理所有评论
# Clean all reviews
pos_cleaned = [clean_text(r) for r in pos_reviews]
neg_cleaned = [clean_text(r) for r in neg_reviews]

# 显示预处理示例
# Show preprocessing example
print("Sample original review (first 200 chars):")
print(pos_reviews[0][:200])
print()
print("Sample cleaned review (first 200 chars):")
print(pos_cleaned[0][:200])
print()


# ============================================================
# 步骤 3：定义词汇表
# Step 3: Define a Vocabulary
# ============================================================

print("=" * 60)
print("Step 3: Define a Vocabulary")
print("=" * 60)

# 构建词汇表 Counter：遍历所有评论（负面 + 正面）
# Build vocabulary Counter: iterate through all reviews (negative + positive)
vocab_counter = Counter()
for review in neg_cleaned + pos_cleaned:
    tokens = review.split()
    vocab_counter.update(tokens)

print(f"Total unique words in vocabulary: {len(vocab_counter)}")
print()

# 打印出现频率最高的前 50 个词
# Print top 50 most frequently occurring words
print(f"Top {TOP_FREQUENT_WORDS} most frequent words:")
top_words = vocab_counter.most_common(TOP_FREQUENT_WORDS)
top_words_table = [[word, count] for word, count in top_words]
print(tabulate(top_words_table, headers=["Word", "Count"], tablefmt="simple"))
print()


# ============================================================
# 步骤 4：剪枝
# Step 4: Pruning
# ============================================================

print("=" * 60)
print("Step 4: Pruning")
print("=" * 60)

# 记录剪枝前的词汇量
# Record vocabulary size before pruning
vocab_size_before = len(vocab_counter)

# 移除出现次数 <= PRUNING_THRESHOLD 的低频词
# Remove words with frequency <= PRUNING_THRESHOLD
vocab_pruned = {word for word, count in vocab_counter.items() if count > PRUNING_THRESHOLD}

print(f"Vocabulary before pruning: {vocab_size_before}")
print(f"Vocabulary after pruning (frequency > {PRUNING_THRESHOLD}): {len(vocab_pruned)}")
print(f"Words removed: {vocab_size_before - len(vocab_pruned)}")
print()

# 保存剪枝后的词汇表到文件
# Save pruned vocabulary to file
vocab_path = os.path.join(SCRIPT_DIR, "vocab.txt")
with open(vocab_path, "w", encoding="utf-8") as f:
    for word in sorted(vocab_pruned):
        f.write(word + "\n")
print(f"Vocabulary saved to: {vocab_path}")
print()


# ============================================================
# 步骤 5：准备数据（合并标签和拆分数据集）
# Step 5: Prepare Data (Combine Labels and Split Dataset)
# ============================================================

print("=" * 60)
print("Step 5: Prepare Data")
print("=" * 60)

# 合并评论和标签（0 = 负面，1 = 正面）
# Combine reviews and labels (0 = negative, 1 = positive)
all_reviews_raw = neg_reviews + pos_reviews
all_reviews_cleaned = neg_cleaned + pos_cleaned
all_labels = [0] * len(neg_reviews) + [1] * len(pos_reviews)

print(f"Total samples: {len(all_labels)}")
print(f"Negative (0): {all_labels.count(0)}")
print(f"Positive (1): {all_labels.count(1)}")
print()

# 按 80/20 拆分训练集和测试集
# Split into 80% training and 20% testing sets
X_train_clean, X_test_clean, y_train, y_test = train_test_split(
    all_reviews_cleaned, all_labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=all_labels
)

# 同时拆分原始文本（用于 DistilBERT 的 tokenizer 输入）
# Also split raw text (for DistilBERT tokenizer input)
X_train_raw, X_test_raw, _, _ = train_test_split(
    all_reviews_raw, all_labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=all_labels
)

print(f"Training set size: {len(X_train_clean)}")
print(f"Testing set size: {len(X_test_clean)}")
print()


# ============================================================
# 步骤 6：基线模型 - TF-IDF + 逻辑回归
# Step 6: Baseline Model - TF-IDF + Logistic Regression
# ============================================================

print("=" * 60)
print("Step 6: Baseline Model - TF-IDF + Logistic Regression")
print("=" * 60)

# 使用 TF-IDF 向量化器将文本转换为数值特征
# Use TF-IDF vectorizer to convert text into numerical features
# 原因：TF-IDF 衡量词在文档中的重要性，同时降低常见词的权重
# Reason: TF-IDF measures word importance in documents while downweighting common words
tfidf = TfidfVectorizer(max_features=10000)
X_train_tfidf = tfidf.fit_transform(X_train_clean)
X_test_tfidf = tfidf.transform(X_test_clean)

print(f"TF-IDF feature matrix shape: {X_train_tfidf.shape}")

# 训练逻辑回归分类器
# Train Logistic Regression classifier
# 参数 max_iter=1000：设置最大迭代次数以确保收敛
# Parameter max_iter=1000: set max iterations to ensure convergence
lr_model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
lr_model.fit(X_train_tfidf, y_train)

# 在测试集上预测
# Predict on test set
y_pred_baseline = lr_model.predict(X_test_tfidf)

# 计算并报告基线模型指标
# Compute and report baseline model metrics
baseline_accuracy = accuracy_score(y_test, y_pred_baseline)
baseline_precision = precision_score(y_test, y_pred_baseline)
baseline_recall = recall_score(y_test, y_pred_baseline)
baseline_f1 = f1_score(y_test, y_pred_baseline)
baseline_cm = confusion_matrix(y_test, y_pred_baseline)

print(f"\nBaseline Model Results (TF-IDF + Logistic Regression):")
print(f"  Accuracy:  {baseline_accuracy:.4f}")
print(f"  Precision: {baseline_precision:.4f}")
print(f"  Recall:    {baseline_recall:.4f}")
print(f"  F1-score:  {baseline_f1:.4f}")
print(f"\nConfusion Matrix:")
print(baseline_cm)
print()
print("Classification Report:")
print(classification_report(y_test, y_pred_baseline, target_names=LABEL_NAMES))
print()


# ============================================================
# 步骤 7：DistilBERT 数据准备
# Step 7: DistilBERT Data Preparation
# ============================================================

print("=" * 60)
print("Step 7: DistilBERT Data Preparation")
print("=" * 60)

# 加载 DistilBERT 分词器
# Load DistilBERT tokenizer
tokenizer = DistilBertTokenizer.from_pretrained(DISTILBERT_MODEL_NAME)
print(f"Tokenizer loaded: {DISTILBERT_MODEL_NAME}")
print(f"Vocabulary size: {tokenizer.vocab_size}")
print()

# 进一步拆分训练集为训练集和验证集（80% 训练，20% 验证）
# Further split training set into train and validation (80% train, 20% validation)
X_train_bert, X_val_bert, y_train_bert, y_val_bert = train_test_split(
    X_train_raw, y_train, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_train
)

print(f"DistilBERT training set: {len(X_train_bert)}")
print(f"DistilBERT validation set: {len(X_val_bert)}")
print(f"DistilBERT test set: {len(X_test_raw)}")
print()


# ============================================================
# ReviewDataset: 自定义 PyTorch 数据集类，用于电影评论
#                Custom PyTorch Dataset class for movie reviews
# ============================================================
class ReviewDataset(Dataset):
    """自定义数据集类，将文本和标签转换为 DistilBERT 输入格式
    Custom dataset class converting text and labels to DistilBERT input format."""

    def __init__(self, texts, labels, tokenizer, max_length):
        """初始化数据集
        Initialize dataset.

        Args:
            texts: List of review text strings.
            labels: List of integer labels (0 or 1).
            tokenizer: DistilBERT tokenizer instance.
            max_length: Maximum token sequence length.
        """
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        """返回数据集大小
        Return dataset size."""
        return len(self.texts)

    def __getitem__(self, idx):
        """获取单个样本的编码表示
        Get encoded representation of a single sample."""
        text = self.texts[idx]
        label = self.labels[idx]

        # 使用 tokenizer 编码文本，添加 padding 和截断
        # Encode text using tokenizer, add padding and truncation
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long),
        }


# 创建 PyTorch 数据集
# Create PyTorch datasets
train_dataset = ReviewDataset(X_train_bert, y_train_bert, tokenizer, MAX_SEQ_LENGTH)
val_dataset = ReviewDataset(X_val_bert, y_val_bert, tokenizer, MAX_SEQ_LENGTH)
test_dataset = ReviewDataset(X_test_raw, y_test, tokenizer, MAX_SEQ_LENGTH)

# 创建 DataLoader
# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Training batches: {len(train_loader)}")
print(f"Validation batches: {len(val_loader)}")
print(f"Test batches: {len(test_loader)}")
print()


# ============================================================
# 步骤 8：微调 DistilBERT
# Step 8: Fine-Tune DistilBERT
# ============================================================

print("=" * 60)
print("Step 8: Fine-Tune DistilBERT")
print("=" * 60)

# 加载预训练的 DistilBERT 序列分类模型（2 类：正面/负面）
# Load pre-trained DistilBERT sequence classification model (2 classes: positive/negative)
model = DistilBertForSequenceClassification.from_pretrained(
    DISTILBERT_MODEL_NAME, num_labels=2
)
model.to(device)
print(f"Model loaded and moved to {device}")

# 设置优化器（AdamW 是 Transformer 微调的标准选择）
# Set up optimizer (AdamW is the standard choice for Transformer fine-tuning)
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

# 设置学习率调度器（线性预热后线性衰减）
# Set up learning rate scheduler (linear warmup then linear decay)
total_steps = len(train_loader) * NUM_EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=total_steps
)

print(f"Optimizer: AdamW (lr={LEARNING_RATE})")
print(f"Scheduler: Linear with warmup")
print(f"Total training steps: {total_steps}")
print()

# 训练循环
# Training loop
for epoch in range(NUM_EPOCHS):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch_idx, batch in enumerate(train_loader):
        # 将数据移到计算设备
        # Move data to compute device
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        # 前向传播
        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        # 反向传播和参数更新
        # Backward pass and parameter update
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

        # 计算训练准确率
        # Compute training accuracy
        preds = torch.argmax(outputs.logits, dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    # 计算训练指标
    # Compute training metrics
    avg_loss = total_loss / len(train_loader)
    train_acc = correct / total

    # ----------------------------------------
    # 步骤 8.1：验证集评估
    # Step 8.1: Validation evaluation
    # ----------------------------------------
    model.eval()
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            preds = torch.argmax(outputs.logits, dim=1)
            val_correct += (preds == labels).sum().item()
            val_total += labels.size(0)

    val_acc = val_correct / val_total

    print(f"Epoch {epoch + 1}/{NUM_EPOCHS} - Loss: {avg_loss:.4f}, "
          f"Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")

print()


# ============================================================
# 步骤 9：DistilBERT 测试集评估
# Step 9: DistilBERT Test Set Evaluation
# ============================================================

print("=" * 60)
print("Step 9: DistilBERT Test Set Evaluation")
print("=" * 60)

# 在测试集上评估模型
# Evaluate model on test set
model.eval()
all_preds = []
all_labels_test = []

with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        preds = torch.argmax(outputs.logits, dim=1)

        all_preds.extend(preds.cpu().numpy())
        all_labels_test.extend(labels.cpu().numpy())

# 计算 DistilBERT 模型指标
# Compute DistilBERT model metrics
bert_accuracy = accuracy_score(all_labels_test, all_preds)
bert_precision = precision_score(all_labels_test, all_preds)
bert_recall = recall_score(all_labels_test, all_preds)
bert_f1 = f1_score(all_labels_test, all_preds)
bert_cm = confusion_matrix(all_labels_test, all_preds)

print(f"DistilBERT Model Results:")
print(f"  Accuracy:  {bert_accuracy:.4f}")
print(f"  Precision: {bert_precision:.4f}")
print(f"  Recall:    {bert_recall:.4f}")
print(f"  F1-score:  {bert_f1:.4f}")
print(f"\nConfusion Matrix:")
print(bert_cm)
print()
print("Classification Report:")
print(classification_report(all_labels_test, all_preds, target_names=LABEL_NAMES))
print()


# ============================================================
# 步骤 10：模型对比
# Step 10: Model Comparison
# ============================================================

print("=" * 60)
print("Step 10: Model Comparison")
print("=" * 60)

# 对比基线模型和 DistilBERT 的性能
# Compare baseline and DistilBERT performance
comparison_table = [
    ["TF-IDF + LR", f"{baseline_accuracy:.4f}", f"{baseline_precision:.4f}",
     f"{baseline_recall:.4f}", f"{baseline_f1:.4f}"],
    ["DistilBERT", f"{bert_accuracy:.4f}", f"{bert_precision:.4f}",
     f"{bert_recall:.4f}", f"{bert_f1:.4f}"],
]
print(tabulate(
    comparison_table,
    headers=["Model", "Accuracy", "Precision", "Recall", "F1-Score"],
    tablefmt="simple"
))
print()


# ============================================================
# 步骤 11：新文本预测
# Step 11: Predictions on New Text Samples
# ============================================================

print("=" * 60)
print("Step 11: Predictions on New Text Samples")
print("=" * 60)

# 使用微调后的 DistilBERT 对新文本进行预测
# Use fine-tuned DistilBERT to predict on new text samples
model.eval()
predictions = []

with torch.no_grad():
    for text in NEW_TEXT_SAMPLES:
        # 编码新文本
        # Encode new text
        encoding = tokenizer(
            text,
            max_length=MAX_SEQ_LENGTH,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        input_ids = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)

        # 前向传播获取预测结果
        # Forward pass to get predictions
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        pred = torch.argmax(outputs.logits, dim=1).item()
        predictions.append(pred)

# 打印预测结果
# Print prediction results
pred_table = []
for text, pred in zip(NEW_TEXT_SAMPLES, predictions):
    # 截断过长的文本以便显示
    # Truncate long text for display
    display_text = text[:70] + "..." if len(text) > 70 else text
    pred_table.append([display_text, LABEL_NAMES[pred]])

print(tabulate(pred_table, headers=["Text", "Prediction"], tablefmt="simple"))
print()
