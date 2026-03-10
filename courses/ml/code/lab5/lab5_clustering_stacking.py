"""
CST8506 Lab 5: Clustering, Outlier Detection & Stacking
Author: Peng Wang
Student Number: 041107730

Task 1: Outlier detection using 1-Class SVM + clustering using DBSCAN on EmployeesSalary dataset.
Task 2: Resampling for class imbalance + Stacking classifier on Diabetes dataset.
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 非交互模式，不弹窗
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.dpi'] = 150

from scipy.io import arff

# 预处理和聚类
# Preprocessing and clustering
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

# 异常值检测
# Outlier detection
from sklearn.svm import OneClassSVM

# 聚类算法
# Clustering algorithms
from sklearn.cluster import DBSCAN

# 重采样
# Resampling
from sklearn.utils import resample

# 分类模型
# Classification models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier

# 评估指标
# Evaluation metrics
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from sklearn.model_selection import train_test_split

# ============================================================
# 工具函数
# Utility Functions
# ============================================================

# 创建图片保存目录
# Create directory for saving images
os.makedirs('lab5_images', exist_ok=True)

STUDENT_NUMBER = 41107730
RANDOM_STATE = STUDENT_NUMBER % 1000  # 730

print("=" * 60)
print("CST8506 Lab 5: Clustering, Outlier Detection & Stacking")
print(f"Student Number: {STUDENT_NUMBER} | Random State: {RANDOM_STATE}")
print("=" * 60)


# ============================================================
# TASK 1: Clustering & Outlier Detection
# 任务1：聚类和异常值检测
# ============================================================

print("\n" + "=" * 60)
print("TASK 1: Clustering & Outlier Detection")
print("=" * 60)

# ============================================================
# Step 1: 加载 EmployeesSalary 数据集
# Step 1: Load EmployeesSalary Dataset
# ============================================================

print("\n--- Step 1: Load EmployeesSalary Dataset ---")

# 直接加载本地数据
# Load local dataset
employees_df = pd.read_csv("EmployeesSalary.csv")
print("Loaded from: EmployeesSalary.csv")

print(f"\nDataset shape: {employees_df.shape}")
print(f"\nColumn names: {list(employees_df.columns)}")
print(f"\nFirst 5 rows:\n{employees_df.head()}")
print(f"\nData types:\n{employees_df.dtypes}")
print(f"\nMissing values:\n{employees_df.isnull().sum()}")
print(f"\nBasic statistics:\n{employees_df.describe()}")


# ============================================================
# Step 2: 数据预处理
# Step 2: Data Preprocessing
# ============================================================

print("\n--- Step 2: Data Preprocessing ---")

# 保留原始数据框用于后续合并
# Keep original dataframe for later joining
original_df = employees_df.copy()

# 识别数值型列和类别型列 (排除 ID、姓名、邮件、地址等非特征列)
# Identify numerical and categorical columns (exclude ID, name, email, address columns)
exclude_cols = [c for c in employees_df.columns
                if any(kw in c.lower() for kw in ['id', 'name', 'email', 'address'])]
num_cols = employees_df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = employees_df.select_dtypes(include=['object', 'category']).columns.tolist()

# 从数值列中移除排除列
# Remove excluded columns from numerical columns
num_cols = [c for c in num_cols if c not in exclude_cols]
cat_cols = [c for c in cat_cols if c not in exclude_cols]

print(f"Numerical columns: {num_cols}")
print(f"Categorical columns: {cat_cols}")
print(f"Excluded columns: {exclude_cols}")

# 处理缺失值：数值列用中位数填充，类别列用众数填充
# Handle missing values: numerical with median, categorical with mode
for col in num_cols:
    if employees_df[col].isnull().any():
        employees_df[col].fillna(employees_df[col].median(), inplace=True)
for col in cat_cols:
    if employees_df[col].isnull().any():
        employees_df[col].fillna(employees_df[col].mode()[0], inplace=True)

# 对类别列进行 One-Hot 编码 (距离度量需要)
# One-hot encode categorical columns (required for distance-based methods)
if cat_cols:
    df_encoded = pd.get_dummies(employees_df[cat_cols], drop_first=False)
    print(f"After OHE, categorical columns expanded to {df_encoded.shape[1]} columns")
else:
    df_encoded = pd.DataFrame(index=employees_df.index)

# 对数值列进行标准化 (距离度量需要)
# Scale numerical columns (required for distance-based methods)
scaler = StandardScaler()
df_num_scaled = pd.DataFrame(
    scaler.fit_transform(employees_df[num_cols]),
    columns=num_cols,
    index=employees_df.index
)

# 合并预处理后的特征
# Combine preprocessed features
X_processed = pd.concat([df_num_scaled, df_encoded], axis=1)
print(f"\nProcessed feature matrix shape: {X_processed.shape}")
print(f"Feature columns: {list(X_processed.columns)}")


# ============================================================
# Step 3: 使用 1-Class SVM 进行异常值检测
# Step 3: Outlier Detection using 1-Class SVM
# ============================================================

print("\n--- Step 3: Outlier Detection with 1-Class SVM ---")

# 训练 1-Class SVM 模型
# Train 1-Class SVM model
ocsvm = OneClassSVM(
    kernel='rbf',   # 使用 RBF 核函数
    nu=0.05,        # 期望异常值比例 (5%)
    gamma='scale'   # 自动缩放 gamma
)
ocsvm.fit(X_processed)

# 获取异常值分数（越低越异常）
# Get outlier scores (lower = more anomalous)
outlier_scores = ocsvm.decision_function(X_processed)
outlier_predictions = ocsvm.predict(X_processed)

# 将预测值转换为标志：-1 = 异常值 (True)，1 = 正常 (False)
# Convert predictions to flag: -1 = outlier (True), 1 = normal (False)
outlier_flag = outlier_predictions == -1

# 将结果与原始数据集合并
# Join results with original dataset
result_task1_outlier = original_df.copy()
result_task1_outlier['Outlier_Score'] = outlier_scores
result_task1_outlier['Outlier_Flag'] = outlier_flag

# 找出异常值实例
# Find outlier instances
outlier_instances = result_task1_outlier[result_task1_outlier['Outlier_Flag'] == True].copy()

print(f"\nTotal instances: {len(employees_df)}")
print(f"Outlier instances: {outlier_flag.sum()} ({outlier_flag.mean()*100:.1f}%)")
print(f"\nOutlier instances (first 10):\n{outlier_instances.head(10).to_string()}")


# ============================================================
# Step 4: 可视化异常值
# Step 4: Visualize Outliers
# ============================================================

print("\n--- Step 4: Visualize Outliers ---")

# 找到薪资列名
# Find salary column name
salary_col = next((c for c in num_cols if 'salary' in c.lower()), num_cols[-1])
exp_col = next((c for c in num_cols if 'year' in c.lower() or 'exp' in c.lower()),
               num_cols[0] if len(num_cols) > 0 else salary_col)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Task 1: 1-Class SVM Outlier Detection', fontsize=14, fontweight='bold')

# 散点图：薪资 vs 经验年限
# Scatter plot: Salary vs Experience
normal_mask = ~outlier_flag
axes[0].scatter(
    original_df.loc[normal_mask, exp_col] if exp_col in original_df.columns else range(normal_mask.sum()),
    original_df.loc[normal_mask, salary_col],
    c='steelblue', alpha=0.6, label='Normal', s=40
)
axes[0].scatter(
    original_df.loc[outlier_flag, exp_col] if exp_col in original_df.columns else range(outlier_flag.sum()),
    original_df.loc[outlier_flag, salary_col],
    c='red', alpha=0.8, label='Outlier', s=80, marker='x', linewidths=2
)
axes[0].set_xlabel(exp_col)
axes[0].set_ylabel(salary_col)
axes[0].set_title('Outlier Detection Result')
axes[0].legend()

# 异常值分数分布直方图
# Outlier score distribution histogram
axes[1].hist(outlier_scores[~outlier_flag], bins=30, color='steelblue', alpha=0.7, label='Normal')
axes[1].hist(outlier_scores[outlier_flag], bins=10, color='red', alpha=0.7, label='Outlier')
axes[1].axvline(x=0, color='black', linestyle='--', label='Decision boundary')
axes[1].set_xlabel('Outlier Score')
axes[1].set_ylabel('Count')
axes[1].set_title('Outlier Score Distribution')
axes[1].legend()

plt.tight_layout()
plt.savefig('lab5_images/lab5_task1_outlier_detection.png', bbox_inches='tight')
plt.show()
print("Saved: lab5_images/lab5_task1_outlier_detection.png")


# ============================================================
# Step 5: 使用 DBSCAN 进行聚类
# Step 5: Clustering using DBSCAN
# ============================================================

print("\n--- Step 5: DBSCAN Clustering ---")

# 使用 DBSCAN 进行聚类
# Apply DBSCAN clustering
dbscan = DBSCAN(
    eps=1.5,         # 邻域半径（需要根据数据调整）
    min_samples=5,   # 形成核心点的最少样本数
    metric='euclidean'
)
cluster_labels = dbscan.fit_predict(X_processed)

# 将聚类结果与原始数据合并
# Join clustering results with original data
result_task1_cluster = original_df.copy()
result_task1_cluster['Cluster'] = cluster_labels

n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
n_noise = list(cluster_labels).count(-1)

print(f"\nDBSCAN Results:")
print(f"  Number of clusters: {n_clusters}")
print(f"  Noise points (cluster=-1): {n_noise}")
print(f"\nCluster distribution:\n{result_task1_cluster['Cluster'].value_counts().sort_index()}")

# 噪声实例（cluster = -1）
# Noise instances (cluster = -1)
noise_instances = result_task1_cluster[result_task1_cluster['Cluster'] == -1].copy()
print(f"\nNoise instances (first 10):\n{noise_instances.head(10).to_string()}")


# ============================================================
# Step 6: 可视化聚类结果
# Step 6: Visualize Clustering Results
# ============================================================

print("\n--- Step 6: Visualize Clustering Results ---")

# 使用 PCA 降维到 2D 进行可视化
# Reduce to 2D with PCA for visualization
from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_processed)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Task 1: DBSCAN Clustering', fontsize=14, fontweight='bold')

# 聚类可视化（PCA 投影）
# Cluster visualization (PCA projection)
unique_labels = sorted(set(cluster_labels))
colors = plt.cm.tab10(np.linspace(0, 1, max(len(unique_labels), 1)))
for k, color in zip(unique_labels, colors):
    mask = cluster_labels == k
    label = f'Cluster {k}' if k != -1 else 'Noise'
    c = 'black' if k == -1 else color
    marker = 'x' if k == -1 else 'o'
    axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1],
                    c=[c], label=label, alpha=0.6, s=50, marker=marker)
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
axes[0].set_title(f'DBSCAN Clusters (PCA projection)\n{n_clusters} clusters, {n_noise} noise points')
axes[0].legend(loc='best', fontsize=8)

# 薪资分布箱线图（按聚类）
# Salary distribution boxplot by cluster
cluster_df = result_task1_cluster.copy()
cluster_groups = [cluster_df[cluster_df['Cluster'] == k][salary_col].values
                  for k in sorted(set(cluster_labels))]
labels_bp = [f'C{k}' if k != -1 else 'Noise' for k in sorted(set(cluster_labels))]
if any(len(g) > 0 for g in cluster_groups):
    axes[1].boxplot([g for g in cluster_groups if len(g) > 0],
                    labels=[l for l, g in zip(labels_bp, cluster_groups) if len(g) > 0])
    axes[1].set_xlabel('Cluster')
    axes[1].set_ylabel(salary_col)
    axes[1].set_title(f'Salary Distribution by Cluster')

plt.tight_layout()
plt.savefig('lab5_images/lab5_task1_dbscan_clustering.png', bbox_inches='tight')
plt.show()
print("Saved: lab5_images/lab5_task1_dbscan_clustering.png")

print("\n=== Task 1 Summary ===")
print(f"Outlier Detection (1-Class SVM): {outlier_flag.sum()} outliers found out of {len(employees_df)} instances")
print(f"Clustering (DBSCAN): {n_clusters} clusters, {n_noise} noise points")


# ============================================================
# TASK 2: Sampling and Stacking
# 任务2：采样和堆叠
# ============================================================

print("\n" + "=" * 60)
print("TASK 2: Sampling and Stacking (Diabetes Dataset)")
print("=" * 60)


# ============================================================
# Step 1: 加载糖尿病数据集
# Step 1: Load Diabetes Dataset
# ============================================================

print("\n--- Step 1: Load Diabetes Dataset ---")

# 直接加载本地数据
# Load local dataset
data, meta = arff.loadarff("diabetes.arff")
diabetes_df = pd.DataFrame(data)
# 将字节类型转换为字符串
# Convert byte strings to regular strings
for col in diabetes_df.select_dtypes(include=['object']).columns:
    diabetes_df[col] = diabetes_df[col].apply(
        lambda x: x.decode('utf-8') if isinstance(x, bytes) else x
    )
print("Loaded from: diabetes.arff")

print(f"\nDataset shape: {diabetes_df.shape}")
print(f"\nColumn names: {list(diabetes_df.columns)}")
print(f"\nFirst 5 rows:\n{diabetes_df.head()}")

# 识别目标列（通常是 'class' 列）
# Identify target column (usually 'class')
target_col = next((c for c in diabetes_df.columns if 'class' in c.lower()), diabetes_df.columns[-1])
print(f"\nTarget column: '{target_col}'")
print(f"\nClass distribution (before resampling):\n{diabetes_df[target_col].value_counts()}")


# ============================================================
# Step 2: 数据预处理
# Step 2: Data Preprocessing
# ============================================================

print("\n--- Step 2: Data Preprocessing ---")

# 分离特征和目标列
# Separate features and target
feature_cols = [c for c in diabetes_df.columns if c != target_col]
X_diabetes = diabetes_df[feature_cols].copy()
y_diabetes = diabetes_df[target_col].copy()

# 将目标列编码为整数（如果是字符串类型）
# Encode target to integers if string type
le = LabelEncoder()
y_diabetes_encoded = le.fit_transform(y_diabetes)
print(f"Class mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# 确保数值型特征
# Ensure numerical features
X_diabetes = X_diabetes.select_dtypes(include=[np.number])
print(f"Feature columns used: {list(X_diabetes.columns)}")

# 标准化特征（距离度量算法需要）
# Standardize features (required for distance-based algorithms)
scaler_diabetes = StandardScaler()
X_diabetes_scaled = scaler_diabetes.fit_transform(X_diabetes)
X_diabetes_scaled = pd.DataFrame(X_diabetes_scaled, columns=X_diabetes.columns)

print(f"\nClass distribution:\n{pd.Series(y_diabetes_encoded).value_counts()}")


# ============================================================
# Step 3: 重采样处理类别不平衡
# Step 3: Resampling to Handle Class Imbalance
# ============================================================

print("\n--- Step 3: Resampling (Oversampling minority class) ---")

# 合并特征和标签
# Combine features and labels
df_diabetes_full = X_diabetes_scaled.copy()
df_diabetes_full[target_col] = y_diabetes_encoded

# 分离两个类别
# Separate two classes
counts = pd.Series(y_diabetes_encoded).value_counts()
majority_class = counts.idxmax()
minority_class = counts.idxmin()
print(f"Majority class: {majority_class} ({counts[majority_class]} samples)")
print(f"Minority class: {minority_class} ({counts[minority_class]} samples)")

df_majority = df_diabetes_full[df_diabetes_full[target_col] == majority_class]
df_minority = df_diabetes_full[df_diabetes_full[target_col] == minority_class]

# 对少数类进行过采样（上采样到与多数类相同数量）
# Oversample minority class (upsample to match majority class count)
df_minority_upsampled = resample(
    df_minority,
    replace=True,                           # 有放回采样
    n_samples=len(df_majority),             # 匹配多数类
    random_state=RANDOM_STATE
)
df_resampled = pd.concat([df_majority, df_minority_upsampled])
df_resampled = df_resampled.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

X_resampled = df_resampled[feature_cols if all(c in df_resampled.columns for c in feature_cols)
                            else X_diabetes.columns].values
y_resampled = df_resampled[target_col].values

print(f"\nAfter resampling:")
print(f"Total samples: {len(y_resampled)}")
print(f"Class distribution:\n{pd.Series(y_resampled).value_counts()}")


# ============================================================
# Step 4: 70-30 划分训练集和测试集
# Step 4: 70-30 Train-Test Split
# ============================================================

print("\n--- Step 4: 70-30 Train-Test Split ---")

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled,
    test_size=0.3,
    random_state=RANDOM_STATE,
    stratify=y_resampled
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
print(f"Train class distribution: {pd.Series(y_train).value_counts().to_dict()}")
print(f"Test class distribution: {pd.Series(y_test).value_counts().to_dict()}")


# ============================================================
# Step 5: 训练并评估各个模型
# Step 5: Train and Evaluate Individual Models
# ============================================================

print("\n--- Step 5: Train and Evaluate Individual Models ---")


def evaluate_model(name, model, X_tr, y_tr, X_te, y_te):
    """训练模型并输出评估结果 / Train model and print evaluation results"""
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    acc = accuracy_score(y_te, y_pred)
    prec = precision_score(y_te, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_te, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_te, y_pred, average='weighted', zero_division=0)
    print(f"\n{name}:")
    print(f"  Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1-Score:  {f1:.4f}")
    print(f"\nClassification Report:\n{classification_report(y_te, y_pred, zero_division=0)}")
    return {'Model': name, 'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1}


results = []

# kNN 分类器
# kNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
results.append(evaluate_model('kNN (k=5)', knn, X_train, y_train, X_test, y_test))

# 朴素贝叶斯分类器
# Naive Bayes classifier
nb = GaussianNB()
results.append(evaluate_model('Naïve Bayes', nb, X_train, y_train, X_test, y_test))

# SVM 分类器
# SVM classifier
svm = SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE)
results.append(evaluate_model('SVM (RBF kernel)', svm, X_train, y_train, X_test, y_test))

# 逻辑回归分类器
# Logistic Regression classifier
lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
results.append(evaluate_model('Logistic Regression', lr, X_train, y_train, X_test, y_test))


# ============================================================
# Step 6: Stacking 模型
# Step 6: Stacking Model
# ============================================================

print("\n--- Step 6: Stacking Classifier ---")
print("Base learners: kNN, Naïve Bayes, SVM")
print("Meta-learner: Logistic Regression")

# 定义基础学习器和元学习器
# Define base learners and meta-learner
estimators = [
    ('knn', KNeighborsClassifier(n_neighbors=5)),
    ('nb', GaussianNB()),
    ('svm', SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE))
]

stacking_clf = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    cv=5,           # 5-fold 交叉验证生成元特征
    passthrough=False
)

results.append(evaluate_model(
    'Stacking (kNN+NB+SVM → LR)',
    stacking_clf, X_train, y_train, X_test, y_test
))


# ============================================================
# Step 7: 汇总结果表格
# Step 7: Results Summary Table
# ============================================================

print("\n--- Step 7: Results Summary Table ---")

results_df = pd.DataFrame(results)
results_df[['Accuracy', 'Precision', 'Recall', 'F1-Score']] = \
    results_df[['Accuracy', 'Precision', 'Recall', 'F1-Score']].round(4)

print(f"\n{'='*75}")
print(f"{'Model':<35} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
print(f"{'-'*75}")
for _, row in results_df.iterrows():
    print(f"{row['Model']:<35} {row['Accuracy']:>10.4f} {row['Precision']:>10.4f} "
          f"{row['Recall']:>10.4f} {row['F1-Score']:>10.4f}")
print(f"{'='*75}")


# ============================================================
# Step 8: 可视化模型比较
# Step 8: Visualize Model Comparison
# ============================================================

print("\n--- Step 8: Model Performance Visualization ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Task 2: Model Performance Comparison (after resampling)', fontsize=13, fontweight='bold')

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
model_names = [r['Model'].replace('Stacking (kNN+NB+SVM → LR)', 'Stacking') for r in results]
x = np.arange(len(results))
width = 0.2

# 分组条形图：各模型各指标
# Grouped bar chart: metrics per model
colors_bar = ['steelblue', 'darkorange', 'green', 'red']
for i, (metric, color) in enumerate(zip(metrics, colors_bar)):
    values = [r[metric] for r in results]
    axes[0].bar(x + i * width, values, width, label=metric, color=color, alpha=0.8)
axes[0].set_xticks(x + width * 1.5)
axes[0].set_xticklabels(model_names, rotation=20, ha='right', fontsize=9)
axes[0].set_ylim(0, 1.05)
axes[0].set_ylabel('Score')
axes[0].set_title('All Metrics by Model')
axes[0].legend(loc='lower right')
axes[0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

# 仅准确率对比
# Accuracy only comparison
accuracies = [r['Accuracy'] for r in results]
bar_colors = ['steelblue'] * (len(results) - 1) + ['darkorange']
bars = axes[1].bar(model_names, accuracies, color=bar_colors, alpha=0.8, edgecolor='black')
for bar, val in zip(bars, accuracies):
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                 f'{val:.4f}', ha='center', va='bottom', fontsize=9)
axes[1].set_xticklabels(model_names, rotation=20, ha='right', fontsize=9)
axes[1].set_ylim(0, 1.1)
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Accuracy Comparison (Orange = Stacking)')
axes[1].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('lab5_images/lab5_task2_model_comparison.png', bbox_inches='tight')
plt.show()
print("Saved: lab5_images/lab5_task2_model_comparison.png")


# ============================================================
# Step 9: 可视化类别不平衡处理前后的类别分布
# Step 9: Visualize class distribution before and after resampling
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle('Task 2: Class Distribution Before and After Resampling', fontsize=13, fontweight='bold')

# 重采样前
# Before resampling
before_counts = pd.Series(y_diabetes_encoded).value_counts()
axes[0].bar([str(c) for c in before_counts.index], before_counts.values,
            color=['steelblue', 'darkorange'], alpha=0.8, edgecolor='black')
for i, v in enumerate(before_counts.values):
    axes[0].text(i, v + 2, str(v), ha='center', fontsize=10)
axes[0].set_title('Before Resampling')
axes[0].set_xlabel('Class')
axes[0].set_ylabel('Count')

# 重采样后（训练集）
# After resampling (training set)
after_counts_all = pd.Series(y_resampled).value_counts()
axes[1].bar([str(c) for c in after_counts_all.index], after_counts_all.values,
            color=['steelblue', 'darkorange'], alpha=0.8, edgecolor='black')
for i, v in enumerate(after_counts_all.values):
    axes[1].text(i, v + 2, str(v), ha='center', fontsize=10)
axes[1].set_title('After Resampling (Full balanced dataset)')
axes[1].set_xlabel('Class')
axes[1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('lab5_images/lab5_task2_class_balance.png', bbox_inches='tight')
plt.show()
print("Saved: lab5_images/lab5_task2_class_balance.png")

print("\n" + "=" * 60)
print("Lab 5 Complete!")
print("=" * 60)
print("\nGenerated files:")
print("  - lab5_images/lab5_task1_outlier_detection.png")
print("  - lab5_images/lab5_task1_dbscan_clustering.png")
print("  - lab5_images/lab5_task2_model_comparison.png")
print("  - lab5_images/lab5_task2_class_balance.png")
