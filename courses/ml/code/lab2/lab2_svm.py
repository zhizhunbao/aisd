"""
CST8506 Lab 2: Support Vector Machines
Author: Peng Wang
Student Number: 041107730
Date: 2026-01-30

Classifies Wine dataset using SVM with linear, polynomial and RBF kernels.
Compares performance on standardized, PCA-reduced, and LDA-reduced datasets.
"""

# 导入必要的库：
# numpy - 数值计算库
# pandas - 数据处理库
# matplotlib.pyplot - 绑图库
# sklearn模块 - 机器学习工具

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from tabulate import tabulate
from pathlib import Path

# ============================================================
# 步骤0：配置常量
# Step 0: Configuration constants
# ============================================================

# 固定随机种子以确保结果可复现
# Fixed seed for reproducibility
RANDOM_STATE = 42

# 80-20 训练集-测试集划分
# 80-20 train-test split
TEST_SIZE = 0.2

# 保留95%的方差用于PCA
# Retain 95% of variance for PCA
VARIANCE_THRESHOLD = 0.95

# 创建images目录用于保存图片
# Create images directory for saving plots
OUTPUT_DIR = Path('lab2_images')
OUTPUT_DIR.mkdir(exist_ok=True)

# 设置numpy的随机种子
# Set numpy random seed
np.random.seed(RANDOM_STATE)

# 设置pandas显示选项，避免输出被截断
# Set pandas display options to avoid truncated output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)

print("=" * 80)
print("CST8506 Lab 2: Support Vector Machines")
print("=" * 80)
print()

# ============================================================
# 步骤1：加载Wine数据集
# Step 1: Load the Wine dataset
# ============================================================
print("=" * 80)
print("Step 1: Load the Wine dataset")
print("=" * 80)

# 使用sklearn的load_wine()函数加载数据集
# Use sklearn's load_wine() function to load the dataset
wine = load_wine()

# X是特征矩阵，y是目标变量
# X is the feature matrix, y is the target variable
X = wine.data
y = wine.target

print("Wine dataset loaded successfully")
print(f"Feature names: {wine.feature_names}")
print(f"Target names: {wine.target_names}")
print()

# ============================================================
# 步骤2：打印数据集统计信息
# Step 2: Print dataset statistics
# ============================================================
print("=" * 80)
print("Step 2: Print dataset statistics")
print("=" * 80)

print(f"Number of instances: {X.shape[0]}")
print(f"Number of attributes: {X.shape[1]}")
print(f"\nAttribute names:")
for i, name in enumerate(wine.feature_names):
    print(f"  {i+1}. {name}")

# 创建DataFrame用于显示前5行
# Create DataFrame to display first 5 rows
df = pd.DataFrame(X, columns=wine.feature_names)
df['target'] = y
print(f"\nFirst 5 rows of the dataset:")
print(df.head())
print()

# ============================================================
# 步骤3：划分训练集和测试集
# Step 3: Split the dataset into train and test sets
# ============================================================
print("=" * 80)
print("Step 3: Split the dataset into train and test sets")
print("=" * 80)

# 使用train_test_split划分数据
# Use train_test_split to split data
# stratify=y 确保训练集和测试集中各类别比例相同
# stratify=y ensures same class proportions in train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

print(f"Training set size: {X_train.shape[0]} instances")
print(f"Test set size: {X_test.shape[0]} instances")
print(f"Train/Test ratio: {1-TEST_SIZE:.0%}/{TEST_SIZE:.0%}")
print()

# ============================================================
# 步骤4：标准化数据
# Step 4: Standardize the data
# ============================================================
print("=" * 80)
print("Step 4: Standardize the data")
print("=" * 80)

# SVM对特征尺度敏感，标准化使所有特征在同一尺度上
# SVM is sensitive to feature scales, standardization puts all features on same scale
# 原因：不同特征量级差异大（如酒精含量12-15 vs 脯氨酸300-1700）
# Reason: Features have different scales (e.g., alcohol 12-15 vs proline 300-1700)
scaler = StandardScaler()

# 对训练集进行拟合和转换
# Fit and transform training set
X_train_scaled = scaler.fit_transform(X_train)

# 对测试集只进行转换，使用训练集的均值和标准差，避免数据泄露
# Only transform test set using training set's mean and std to avoid data leakage
X_test_scaled = scaler.transform(X_test)

print("Data standardized successfully")
print(f"Mean of scaled training data: {X_train_scaled.mean():.6f}")
print(f"Standard deviation of scaled training data: {X_train_scaled.std():.6f}")
print()

# ============================================================
# 步骤5：训练SVM模型（使用三种核函数）
# Step 5: Fit SVM models with three kernels
# ============================================================
print("=" * 80)
print("Step 5: Fit SVM models (linear, polynomial, RBF kernels)")
print("=" * 80)

# 定义三种核函数配置
# Define three kernel configurations
# 
# SVM核函数解释：
# SVM kernel explanation:
# - linear: 线性核，最简单，适用于线性可分或近似线性可分的数据
#           Linear kernel, simplest, suitable for linearly or near-linearly separable data
# - poly: 多项式核，通过多项式变换将数据映射到高维空间
#         Polynomial kernel, maps data to higher-dimensional space via polynomial transformation
#         degree=3 表示三次多项式，数值越大边界越复杂，但可能过拟合
#         degree=3 means cubic polynomial, higher values create more complex boundaries but may overfit
# - rbf: 高斯径向基函数核（默认），能处理复杂的非线性边界
#        Gaussian Radial Basis Function kernel (default), handles complex non-linear boundaries
#        gamma='scale' 自动根据特征数和方差调整，是sklearn推荐的默认值
#        gamma='scale' automatically adjusts based on features and variance, sklearn's recommended default
kernels = ['linear', 'poly', 'rbf']

# 存储标准化数据的SVM模型和结果
# Store SVM models and results for standardized data
svm_models_std = {}
results_std = []

for kernel in kernels:
    print(f"\nTraining SVM with {kernel} kernel...")
    
    # 创建SVM分类器，使用默认参数
    # Create SVM classifier with default parameters
    # 
    # SVC 默认参数及含义：
    # SVC default parameters and meanings:
    # 
    # C=1.0（正则化参数）
    # C=1.0 (regularization parameter)
    #   - C 越大，对误分类惩罚越重，决策边界更紧贴数据点，可能过拟合
    #   - Larger C = stricter penalty, tighter boundary around data points, may overfit
    #   - C 越小，允许更多误分类，决策边界更平滑，可能欠拟合
    #   - Smaller C = allows more misclassification, smoother boundary, may underfit
    # 
    # gamma='scale'（RBF/poly核的参数，控制单个样本的影响范围）
    # gamma='scale' (parameter for RBF/poly kernel, controls influence range of single sample)
    #   - gamma = 1 / (n_features * X.var())，自动根据数据计算
    #   - gamma = 1 / (n_features * X.var()), automatically calculated from data
    #   - gamma 越大，影响范围越小，决策边界越复杂，可能过拟合
    #   - Larger gamma = smaller influence range, more complex boundary, may overfit
    # 
    # degree=3（多项式核的次数，仅 kernel='poly' 时使用）
    # degree=3 (polynomial degree, only used when kernel='poly')
    #   - 次数越高，决策边界越复杂，但计算量更大
    #   - Higher degree = more complex boundary, but more computation
    # 
    # coef0=0.0（多项式和sigmoid核的独立项）
    # coef0=0.0 (independent term in poly and sigmoid kernels)
    #   - 影响高阶项和低阶项的权重平衡
    #   - Affects the balance between high-order and low-order terms
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    svm.fit(X_train_scaled, y_train)
    
    # 保存模型
    # Save model
    svm_models_std[kernel] = svm
    
    # 预测并评估
    # Predict and evaluate
    y_pred = svm.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    # 存储结果
    # Store results
    results_std.append({
        'model': f'Standardized, {kernel} SVM',
        'accuracy': acc,
        'confusion_matrix': cm
    })
    
    print(f"  Accuracy: {acc:.4f}")
    print(f"  Confusion Matrix:\n{cm}")

print()

# ============================================================
# 步骤6：应用PCA找出主成分并确定最佳d
# Step 6: Apply PCA to find the principal components and best d
# ============================================================
print("=" * 80)
print("Step 6: Apply PCA to find the principal components")
print("=" * 80)

# 首先运行完整PCA分析所有主成分
# First run full PCA to analyze all components
pca_full = PCA()
X_train_pca_full = pca_full.fit_transform(X_train_scaled)

# 打印解释方差比
# Print explained variance ratios
explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

print("Explained Variance Ratio for each component:")
for i, var in enumerate(explained_var, 1):
    print(f"  PC{i}: {var:.4f} ({var*100:.2f}%)")

print("\nCumulative Explained Variance Ratios:")
for i, cum_var in enumerate(cumulative_var, 1):
    print(f"  PC1-PC{i}: {cum_var:.4f} ({cum_var*100:.2f}%)")

# 找到达到95%方差所需的最少主成分数量
# Find minimum number of components needed for 95% variance
d_pca = np.argmax(cumulative_var >= VARIANCE_THRESHOLD) + 1
print(f"\nOptimal number of components (d) for {VARIANCE_THRESHOLD*100:.0f}% variance: {d_pca}")
print(f"Variance explained by {d_pca} components: {cumulative_var[d_pca-1]:.4f} ({cumulative_var[d_pca-1]*100:.2f}%)")

# 使用最佳d重新运行PCA
# Re-run PCA with optimal d
pca = PCA(n_components=d_pca)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

print(f"\nDimensionality reduction: {X_train_scaled.shape[1]} -> {d_pca}")
print()

# 训练PCA数据上的SVM模型
# Train SVM models on PCA data
svm_models_pca = {}
results_pca = []

print("Training SVM models on PCA-reduced data...")
for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    svm.fit(X_train_pca, y_train)
    svm_models_pca[kernel] = svm
    
    y_pred = svm.predict(X_test_pca)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    results_pca.append({
        'model': f'PCA ({d_pca}), {kernel} SVM',
        'accuracy': acc,
        'confusion_matrix': cm
    })
    
    print(f"  {kernel} kernel - Accuracy: {acc:.4f}")

print()

# ============================================================
# 步骤7：PCA 2D可视化（包含支持向量）
# Step 7: 2D Plots for PCA with support vectors
# ============================================================
print("=" * 80)
print("Step 7: 2D Plots for PCA dataset with support vectors")
print("=" * 80)

# 为2D可视化使用前2个主成分重新训练模型
# Retrain models using first 2 components for 2D visualization
pca_2d = PCA(n_components=2)
X_train_pca_2d = pca_2d.fit_transform(X_train_scaled)
X_test_pca_2d = pca_2d.transform(X_test_scaled)

# 在2D数据上重新训练SVM，用于获取支持向量
# Retrain SVM on 2D data to get support vectors
svm_models_pca_2d = {}
for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    svm.fit(X_train_pca_2d, y_train)
    svm_models_pca_2d[kernel] = svm

# 创建3个子图（1行3列）
# Create 3 subplots (1 row, 3 columns)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 定义类别颜色
# Define class colors
# 使用tab10颜色映射，前3个颜色分别代表3个类别
# Use tab10 colormap, first 3 colors represent 3 classes
colors = plt.cm.tab10(np.linspace(0, 0.3, 3))
edge_colors = ['red', 'green', 'blue']  # 支持向量边框颜色 / Support vector edge colors

for idx, kernel in enumerate(kernels):
    ax = axes[idx]
    svm = svm_models_pca_2d[kernel]
    
    # 获取支持向量
    # Get support vectors
    support_vectors = svm.support_vectors_
    support_vector_indices = svm.support_
    
    # 获取支持向量对应的类别标签
    # Get class labels for support vectors
    support_vector_labels = y_train[support_vector_indices]
    
    # 绘制所有训练数据点
    # Plot all training data points
    for class_label in range(3):
        mask = y_train == class_label
        ax.scatter(X_train_pca_2d[mask, 0], X_train_pca_2d[mask, 1],
                  c=[colors[class_label]], label=f'Class {class_label}',
                  alpha=0.6, s=50)
    
    # 绘制支持向量（使用边框颜色区分类别）
    # Plot support vectors (use edge colors to distinguish classes)
    for class_label in range(3):
        sv_mask = support_vector_labels == class_label
        if np.any(sv_mask):
            ax.scatter(support_vectors[sv_mask, 0], support_vectors[sv_mask, 1],
                      c='none', edgecolors=edge_colors[class_label],
                      label=f'SV Class {class_label}',
                      s=150, linewidths=2, marker='o')
    
    ax.set_xlabel('First Principal Component (PC1)', fontsize=11)
    ax.set_ylabel('Second Principal Component (PC2)', fontsize=11)
    ax.set_title(f'PCA: {kernel.upper()} Kernel', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle('PCA 2D Visualization with Support Vectors', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'pca_2d_svm.png', dpi=150, bbox_inches='tight')
plt.close()

print("PCA 2D plots saved as 'lab2_images/pca_2d_svm.png'")
print()

# ============================================================
# 步骤8：应用LDA降维
# Step 8: Apply LDA to reduce dimensionality
# ============================================================
print("=" * 80)
print("Step 8: Apply LDA to reduce dimensionality")
print("=" * 80)

# LDA最多保留 (n_classes - 1) 个成分
# LDA retains at most (n_classes - 1) components
# Wine数据集有3个类别，因此LDA最多保留2个成分
# Wine dataset has 3 classes, so LDA retains at most 2 components
# 
# LDA与PCA的区别：
# Difference between LDA and PCA:
# - PCA是无监督的，只考虑数据方差，不考虑类别信息
#   PCA is unsupervised, only considers data variance, ignores class labels
# - LDA是有监督的，最大化类间距离同时最小化类内距离
#   LDA is supervised, maximizes between-class distance while minimizing within-class distance
# - 因此LDA降维后的数据更有利于分类任务
#   Therefore LDA-reduced data is more favorable for classification tasks
n_classes = len(np.unique(y))
d_lda = n_classes - 1

print(f"Number of classes: {n_classes}")
print(f"Number of LDA components (n_classes - 1): {d_lda}")

# 创建LDA对象
# Create LDA object
lda = LinearDiscriminantAnalysis(n_components=d_lda)

# 对训练集进行拟合和转换
# Fit and transform training set
X_train_lda = lda.fit_transform(X_train_scaled, y_train)

# 对测试集进行转换
# Transform test set
X_test_lda = lda.transform(X_test_scaled)

print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d_lda}")
print(f"Explained variance ratio by LDA: {lda.explained_variance_ratio_}")
print()

# 训练LDA数据上的SVM模型
# Train SVM models on LDA data
svm_models_lda = {}
results_lda = []

print("Training SVM models on LDA-reduced data...")
for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    svm.fit(X_train_lda, y_train)
    svm_models_lda[kernel] = svm
    
    y_pred = svm.predict(X_test_lda)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    results_lda.append({
        'model': f'LDA ({d_lda}), {kernel} SVM',
        'accuracy': acc,
        'confusion_matrix': cm
    })
    
    print(f"  {kernel} kernel - Accuracy: {acc:.4f}")

print()

# ============================================================
# 步骤9：LDA 2D可视化（包含支持向量）
# Step 9: 2D Plots for LDA with support vectors
# ============================================================
print("=" * 80)
print("Step 9: 2D Plots for LDA dataset with support vectors")
print("=" * 80)

# LDA已经是2D的（因为只有2个成分）
# LDA is already 2D (since only 2 components)
# 直接使用svm_models_lda中的模型
# Use models from svm_models_lda directly

# 创建3个子图（1行3列）
# Create 3 subplots (1 row, 3 columns)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, kernel in enumerate(kernels):
    ax = axes[idx]
    svm = svm_models_lda[kernel]
    
    # 获取支持向量
    # Get support vectors
    support_vectors = svm.support_vectors_
    support_vector_indices = svm.support_
    
    # 获取支持向量对应的类别标签
    # Get class labels for support vectors
    support_vector_labels = y_train[support_vector_indices]
    
    # 绘制所有训练数据点
    # Plot all training data points
    for class_label in range(3):
        mask = y_train == class_label
        ax.scatter(X_train_lda[mask, 0], X_train_lda[mask, 1],
                  c=[colors[class_label]], label=f'Class {class_label}',
                  alpha=0.6, s=50)
    
    # 绘制支持向量（使用边框颜色区分类别）
    # Plot support vectors (use edge colors to distinguish classes)
    for class_label in range(3):
        sv_mask = support_vector_labels == class_label
        if np.any(sv_mask):
            ax.scatter(support_vectors[sv_mask, 0], support_vectors[sv_mask, 1],
                      c='none', edgecolors=edge_colors[class_label],
                      label=f'SV Class {class_label}',
                      s=150, linewidths=2, marker='o')
    
    ax.set_xlabel('First Linear Discriminant (LD1)', fontsize=11)
    ax.set_ylabel('Second Linear Discriminant (LD2)', fontsize=11)
    ax.set_title(f'LDA: {kernel.upper()} Kernel', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle('LDA 2D Visualization with Support Vectors', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'lda_2d_svm.png', dpi=150, bbox_inches='tight')
plt.close()

print("LDA 2D plots saved as 'lab2_images/lda_2d_svm.png'")
print()

# ============================================================
# 步骤10：结果汇总表格
# Step 10: Results summary table
# ============================================================
print("=" * 80)
print("Step 10: Results table with accuracies and confusion matrices")
print("=" * 80)

# 合并所有结果
# Combine all results
all_results = results_std + results_pca + results_lda

# 创建表格数据
# Create table data
table_data = []
for result in all_results:
    # 将混淆矩阵转换为字符串格式
    # Convert confusion matrix to string format
    cm_str = str(result['confusion_matrix'].tolist())
    table_data.append([
        result['model'],
        f"{result['accuracy']:.4f}",
        cm_str
    ])

# 打印表格
# Print table
headers = ['Model', 'Accuracy', 'Confusion Matrix']
print(tabulate(table_data, headers=headers, tablefmt='simple'))
print()

# 打印最佳模型
# Print best model
best_result = max(all_results, key=lambda x: x['accuracy'])
print(f"\nBest performing model: {best_result['model']}")
print(f"Best accuracy: {best_result['accuracy']:.4f}")
print()

print("=" * 80)
print("Lab 2 completed!")
print("=" * 80)
