"""
CST8506 Lab 2: Support Vector Machines
Author: Peng Wang
Student Number: 041107730

Classify Wine dataset using SVM with linear, polynomial, and RBF kernels.
Compare performance on standardized, PCA-reduced, and LDA-reduced datasets.
"""

import os

# 导入NumPy，用于数值计算和数组操作
# Import NumPy for numerical computing and array operations
import numpy as np

# 导入Pandas，用于数据处理和DataFrame操作
# Import Pandas for data processing and DataFrame operations
import pandas as pd

# 导入Matplotlib，用于绘制图表和可视化
# Import Matplotlib for plotting and visualization
import matplotlib.pyplot as plt

# 导入sklearn的葡萄酒数据集
# Import Wine dataset from sklearn
from sklearn.datasets import load_wine

# 导入数据集划分函数
# Import train-test split function
from sklearn.model_selection import train_test_split

# 导入标准化缩放器，将数据转换为均值0、标准差1
# Import StandardScaler to transform data to mean=0, std=1
from sklearn.preprocessing import StandardScaler

# 导入支持向量分类器
# Import Support Vector Classifier
from sklearn.svm import SVC

# 导入主成分分析（PCA），用于无监督降维
# Import Principal Component Analysis (PCA) for unsupervised dimensionality reduction
from sklearn.decomposition import PCA

# 导入线性判别分析（LDA），用于有监督降维
# Import Linear Discriminant Analysis (LDA) for supervised dimensionality reduction
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# 导入模型评估指标：准确率和混淆矩阵
# Import model evaluation metrics: accuracy score and confusion matrix
from sklearn.metrics import accuracy_score, confusion_matrix

# 设置随机种子，确保实验可重现
# Set random seed to ensure experiment reproducibility
RANDOM_STATE = 42

# 设置测试集比例为30%
# Set test set ratio to 30%
TEST_SIZE = 0.3

# 设置PCA累计方差阈值为95%，用于确定最佳主成分数量
# Set PCA cumulative variance threshold to 95% for determining optimal number of components
PCA_VARIANCE_THRESHOLD = 0.95

# 定义三种SVM核函数（核函数决定SVM如何画决策边界来分类数据）
# Define three SVM kernels (kernels determine how SVM draws decision boundaries to classify data)
#
# ┌─────────────────────────────────────────────────────────────────────┐
# │ 核函数的作用：把数据从低维映射到高维，让原本分不开的数据变得可分    │
# │ Kernel trick: map data to higher dimensions to make it separable   │
# │                                                                     │
# │  低维(分不开)        高维(分得开)                                   │
# │   o x o x           o o o                                          │
# │   x o x o    ──→    -------  ← 超平面 (hyperplane)                 │
# │   o x o x           x x x                                          │
# └─────────────────────────────────────────────────────────────────────┘
#
# 1. LINEAR（线性核）
#    公式 / Formula: K(x, y) = x · y （两个向量的点积 / dot product）
#    决策边界 / Decision boundary:
#      class A  |  class B
#       o o o   |   x x x        ← 直线分割 (straight line)
#       o o o   |   x x x
#    计算逻辑：直接在原始空间计算，不做任何变换，找一条直线（高维是超平面）
#    Logic: compute directly in original space, find a straight line (hyperplane in high-dim)
#
# 2. POLY（多项式核）
#    公式 / Formula: K(x, y) = (gamma * x·y + r)^d
#      - d = degree（默认3），次数越高曲线越弯曲
#      - d = degree (default 3), higher degree = more curved boundary
#      - gamma = 1/(n_features * X.var())（默认'scale'）
#      - r = coef0（默认0）
#    决策边界 / Decision boundary:
#       o o  ╲  x x
#       o o   ╲  x x             ← 曲线分割 (curved line)
#       o o   ╱ x x
#    计算逻辑：把每个特征做多项式组合（如 x1², x1*x2, x2²），在高维空间画直线
#    Logic: create polynomial combinations of features, draw a line in that higher-dim space
#
# 3. RBF（高斯径向基核，sklearn默认核函数）
#    公式 / Formula: K(x, y) = exp(-gamma * ||x - y||²)
#      - ||x - y||² = 两点间的欧氏距离平方 (squared Euclidean distance)
#      - gamma 控制"影响半径"：gamma大 → 只看近邻，边界复杂；gamma小 → 看得远，边界平滑
#      - gamma controls influence radius: large → local, complex; small → global, smooth
#    决策边界 / Decision boundary:
#       x x x x x
#       x ╭───╮ x
#       x │o o│ x                ← 可以画封闭曲线 (can draw closed curves)
#       x ╰───╯ x
#       x x x x x
#    计算逻辑：计算每对点的距离，近的点相似度高(≈1)，远的点相似度低(≈0)
#    Logic: compute distance between each pair, close points → similarity≈1, far → ≈0
#
KERNELS = ['linear', 'poly', 'rbf']

# 定义三种颜色，用于区分三个类别
# Define three colors to distinguish three classes
COLORS = ['red', 'green', 'blue']

# 创建相对于脚本所在目录的输出目录
# Create output directory relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'lab2_images')

# 使用exist_ok=True避免目录已存在时报错
# Use exist_ok=True to avoid error if directory already exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Step 1: Load the dataset
# ============================================================
print("=" * 80)
print("Step 1: Load the dataset")
print("=" * 80)

# 使用sklearn加载葡萄酒数据集
# Load Wine dataset from sklearn
# 原因：这是一个经典的多分类数据集，包含178个样本、13个特征、3个类别
# Reason: This is a classic multi-class dataset with 178 samples, 13 features, 3 classes
wine = load_wine()
X = wine.data
y = wine.target

print(f"Dataset successfully loaded from sklearn.")
print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
print()

# ============================================================
# 步骤2：打印数据集统计信息
# Step 2: Print dataset statistics
# ============================================================
print("=" * 80)
print("Step 2: Print dataset statistics")
print("=" * 80)

# 配置 Pandas 显示选项，确保所有列都能显示出来而不被截断
# Configure Pandas display options to ensure all columns are shown without truncation
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)

# 打印样本数量和特征信息
# Print number of samples and feature information
print(f"Number of instances: {X.shape[0]}")
print(f"Number of attributes: {X.shape[1]}")
print(f"Attribute names: {wine.feature_names}")

print(f"\nFirst 5 rows (all 13 features):")
# 将NumPy数组转换为Pandas DataFrame以便展示
# Convert NumPy array to Pandas DataFrame for display
df = pd.DataFrame(X, columns=wine.feature_names)
print(df.head())
print()

# ============================================================
# 步骤3：划分训练集和测试集
# Step 3: Split into train and test sets
# ============================================================
print("=" * 80)
print("Step 3: Split into train and test sets")
print("=" * 80)

# 使用train_test_split划分数据集
# Use train_test_split to split dataset
# test_size=0.3表示30%数据用于测试，70%用于训练
# test_size=0.3 means 30% for testing, 70% for training
# random_state确保每次运行得到相同的划分结果
# random_state ensures same split results on each run
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

# 打印划分后的结果
# Print split results
print(f"Total samples: {len(X)}")
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")
print()

# ============================================================
# 步骤4：数据标准化
# Step 4: Standardize the data
# ============================================================
print("=" * 80)
print("Step 4: Standardize the data")
print("=" * 80)

# 创建StandardScaler对象
# Create StandardScaler object
# 原因：SVM对特征尺度非常敏感，不同尺度的特征会导致某些特征主导距离计算
# Reason: SVM is very sensitive to feature scales, different scales cause some features to dominate distance calculation
scaler = StandardScaler()

# 在训练集上fit并transform，学习均值和标准差
# Fit and transform on training set, learn mean and std
# 注意：只在训练集上fit，避免数据泄露（data leakage）
# Note: Only fit on training set to avoid data leakage
X_train_scaled = scaler.fit_transform(X_train)

# 在测试集上只transform，使用训练集学到的参数
# Only transform on test set, use parameters learned from training set
X_test_scaled = scaler.transform(X_test)

# 验证标准化结果并打印详细信息
# Verify standardization and print detailed information
print(f"Before scaling (first 3 features):")
print(f"  Mean: [{', '.join([f'{v:.2f}' for v in scaler.mean_[:3]])}]")
print(f"  Std:  [{', '.join([f'{v:.2f}' for v in np.sqrt(scaler.var_[:3])])}]")
print(f"\nAfter scaling (first 3 features):")
print(f"  Mean: [{', '.join([f'{v:.6f}' for v in X_train_scaled[:, :3].mean(axis=0)])}]")
print(f"  Std:  [{', '.join([f'{v:.6f}' for v in X_train_scaled[:, :3].std(axis=0)])}]")
print()

# ============================================================
# 步骤5：使用三种核函数训练SVM模型
# Step 5: Fit SVM models with three kernels
# ============================================================
print("=" * 80)
print("Step 5: Fit SVM models with three kernels")
print("=" * 80)

# 创建字典存储每种核函数的模型和结果
# Create dictionary to store model and results for each kernel
svm_models_std = {}

print()

# 遍历三种核函数
# Iterate through three kernels
for kernel in KERNELS:
    # 创建SVM分类器，关键超参数说明：
    # Create SVM classifier, key hyperparameters:
    # kernel：核函数类型
    # kernel: type of kernel function
    #   - linear：线性核，适用于线性可分数据
    #   - linear kernel: suitable for linearly separable data
    #   - poly：多项式核，可以处理非线性边界（默认degree=3）
    #   - polynomial kernel: can handle non-linear boundaries (default degree=3)
    #   - rbf：高斯径向基核（默认），最常用，可以映射到无限维空间
    #   - RBF (Gaussian) kernel (default): most commonly used, can map to infinite dimensional space
    # C=1.0（默认）：正则化参数，控制误分类惩罚力度
    # C=1.0 (default): regularization parameter, controls misclassification penalty
    #   - C越大，模型越严格拟合训练数据（可能过拟合）
    #   - Larger C → stricter fit to training data (risk of overfitting)
    #   - C越小，允许更多误分类（更平滑的决策边界）
    #   - Smaller C → more misclassifications allowed (smoother decision boundary)
    # gamma='scale'（默认）：核函数系数，仅对rbf和poly有效
    # gamma='scale' (default): kernel coefficient, only for rbf and poly
    #   - 'scale'表示gamma = 1 / (n_features * X.var())
    #   - 'scale' means gamma = 1 / (n_features * X.var())
    #   - gamma越大，单个样本影响范围越小（决策边界越复杂）
    #   - Larger gamma → smaller influence per sample (more complex boundary)
    # degree=3（默认）：多项式核的次数，仅对poly有效
    # degree=3 (default): polynomial degree, only for poly kernel
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    
    # 在标准化后的训练数据上拟合模型
    # Fit model on standardized training data
    svm.fit(X_train_scaled, y_train)
    
    # 在测试集上进行预测
    # Make predictions on test set
    y_pred = svm.predict(X_test_scaled)
    
    # 计算准确率
    # Calculate accuracy
    acc = accuracy_score(y_test, y_pred)
    
    # 计算混淆矩阵
    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # 存储模型、准确率和混淆矩阵
    # Store model, accuracy, and confusion matrix
    svm_models_std[kernel] = {'model': svm, 'accuracy': acc, 'cm': cm}
    
    # 打印当前核函数的准确率
    # Print accuracy for current kernel
    print(f"{kernel.upper()} kernel:")
    print(f"  Accuracy: {acc:.4f}")
    print(f"  Confusion Matrix:")
    for row in cm:
        print(f"    {row}")

print()

# ============================================================
# 步骤6：应用PCA降维并确定最佳维度d
# Step 6: Apply PCA and find the best 'd'
# ============================================================
print("=" * 80)
print("Step 6: Apply PCA and find the best 'd'")
print("=" * 80)

# 首先拟合完整PCA（保留所有成分），分析方差贡献
# First fit full PCA (keep all components) to analyze variance contribution
# n_components=None表示保留所有成分
# n_components=None means keep all components
pca_full = PCA(n_components=None)
pca_full.fit(X_train_scaled)

# 获取每个主成分解释的方差比例
# Get variance ratio explained by each principal component
explained_variance_ratio = pca_full.explained_variance_ratio_

# 计算累计方差解释率
# Calculate cumulative variance ratio
cumulative_variance = np.cumsum(explained_variance_ratio)

# 找到累计方差首次达到阈值（95%）的主成分数量
# Find number of components where cumulative variance first reaches threshold (95%)
# argmax返回第一个True的索引，+1是因为索引从0开始
# argmax returns index of first True, +1 because index starts from 0
pca_d = np.argmax(cumulative_variance >= PCA_VARIANCE_THRESHOLD) + 1

# 打印方差解释详情
# Print variance explanation details
print(f"Variance explained by each component:")
for i, (ev, cv) in enumerate(zip(explained_variance_ratio[:5], cumulative_variance[:5]), 1):
    print(f"  PC{i}: {ev:.4f} (cumulative: {cv:.4f})")
print(f"  ... (showing first 5 of {len(explained_variance_ratio)} components)")
print(f"\nBest d for {PCA_VARIANCE_THRESHOLD * 100:.0f}% variance: {pca_d}")
print(f"Using d=2 for visualization")
print(f"  Variance captured with 2 components: {cumulative_variance[1]:.4f}")

# 使用2个主成分进行可视化（便于2D绘图）
# Use 2 principal components for visualization (for 2D plotting)
# 原因：虽然最佳d可能更大，但2D图更直观，作业要求2D可视化
# Reason: Although optimal d may be larger, 2D plot is more intuitive, assignment requires 2D visualization
pca = PCA(n_components=2)

# 拟合并转换训练数据
# Fit and transform training data
X_train_pca = pca.fit_transform(X_train_scaled)

# 仅转换测试数据（使用训练集学到的主成分方向）
# Only transform test data (use principal component directions learned from training set)
X_test_pca = pca.transform(X_test_scaled)

print(f"\nSVM Results on PCA-reduced data (d=2):")
# 在PCA降维后的数据上训练SVM
# Train SVM on PCA-reduced data
svm_models_pca = {}
for kernel in KERNELS:
    # 创建新的SVM分类器
    # Create new SVM classifier
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    
    # 在PCA降维后的训练数据上拟合
    # Fit on PCA-reduced training data
    svm.fit(X_train_pca, y_train)
    
    # 在PCA降维后的测试数据上预测
    # Predict on PCA-reduced test data
    y_pred = svm.predict(X_test_pca)
    
    # 计算准确率和混淆矩阵
    # Calculate accuracy and confusion matrix
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    # 存储结果
    # Store results
    svm_models_pca[kernel] = {'model': svm, 'accuracy': acc, 'cm': cm}
    
    # 打印结果
    # Print results
    print(f"  {kernel.upper()} kernel: Accuracy = {acc:.4f}")

print()

# ============================================================
# 步骤7：绘制PCA降维数据的2D图
# Step 7: Plot 2D graphs for PCA-reduced data
# ============================================================
print("=" * 80)
print("Step 7: Plot 2D graphs for PCA-reduced data")
print("=" * 80)

# 创建1行3列的子图布局
# Create 1 row x 3 columns subplot layout
# figsize=(15, 5)设置图形大小为15x5英寸
# figsize=(15, 5) sets figure size to 15x5 inches
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 设置总标题
# Set overall title
fig.suptitle('SVM with PCA-reduced data (2 components)')

# 遍历三种核函数
# Iterate through three kernels
for idx, kernel in enumerate(KERNELS):
    # 获取当前子图
    # Get current subplot
    ax = axes[idx]
    
    # 获取当前核函数的模型
    # Get model for current kernel
    model = svm_models_pca[kernel]['model']
    
    # 按类别绘制训练样本散点图
    # Plot training samples scatter plot by class
    for class_idx in range(3):
        # 创建布尔掩码选择当前类别的样本
        # Create boolean mask to select samples of current class
        mask = y_train == class_idx
        
        # 绘制散点图，使用不同颜色区分类别
        # Plot scatter, use different colors for classes
        # alpha=0.6设置透明度，使重叠点可见
        # alpha=0.6 sets transparency so overlapping points are visible
        ax.scatter(X_train_pca[mask, 0], X_train_pca[mask, 1], 
                   c=COLORS[class_idx], label=f'Class {class_idx}', alpha=0.6)
    
    # 获取支持向量
    # Get support vectors
    # 原因：支持向量是决定决策边界的关键点
    # Reason: Support vectors are key points that determine decision boundary
    sv = model.support_vectors_
    
    # 获取支持向量对应的类别标签
    # Get class labels for support vectors
    sv_labels = y_train[model.support_]
    
    # 用空心圆标记支持向量
    # Mark support vectors with hollow circles
    for class_idx in range(3):
        # 选择当前类别的支持向量
        # Select support vectors of current class
        mask = sv_labels == class_idx
        
        # 只有当该类别有支持向量时才绘制
        # Only plot if this class has support vectors
        if mask.sum() > 0:
            # facecolors='none'表示空心
            # facecolors='none' means hollow
            # edgecolors设置边框颜色
            # edgecolors sets edge color
            # s=100设置大小，linewidths=2设置边框宽度
            # s=100 sets size, linewidths=2 sets edge width
            ax.scatter(sv[mask, 0], sv[mask, 1], 
                       facecolors='none', edgecolors=COLORS[class_idx], 
                       s=100, linewidths=2, label=f'SV Class {class_idx}')
    
    # 设置坐标轴标签
    # Set axis labels
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    
    # 设置子图标题
    # Set subplot title
    ax.set_title(f'{kernel.upper()} Kernel')
    
    # 添加图例
    # Add legend
    ax.legend(loc='best', fontsize=8)

# 自动调整子图间距
# Automatically adjust subplot spacing
plt.tight_layout()

# 构建保存路径
# Build save path
pca_plot_path = os.path.join(OUTPUT_DIR, 'pca_svm_plots.png')

# 保存图表，dpi=150设置分辨率，bbox_inches='tight'去除多余空白
# Save plot, dpi=150 sets resolution, bbox_inches='tight' removes extra whitespace
plt.savefig(pca_plot_path, dpi=150, bbox_inches='tight')

# 关闭图表，释放内存（不弹出显示窗口）
# Close plot to release memory (no popup display window)
plt.close()

# 打印图表信息
# Print plot information
print(f"Saved: {os.path.relpath(pca_plot_path, SCRIPT_DIR)}")
print()

# ============================================================
# 步骤8：应用LDA降维
# Step 8: Apply LDA to reduce dimensionality
# ============================================================
print("=" * 80)
print("Step 8: Apply LDA to reduce dimensionality")
print("=" * 80)

# 创建LDA对象，设置降维到2个成分
# Create LDA object, set to reduce to 2 components
# 原因：LDA是有监督降维，利用类别信息最大化类间方差、最小化类内方差
# Reason: LDA is supervised dimensionality reduction, uses class info to maximize between-class variance, minimize within-class variance
# 对于k类问题，LDA最多保留k-1个成分（葡萄酒3类，最多2个）
# For k-class problem, LDA keeps at most k-1 components (wine has 3 classes, max 2)
lda = LDA(n_components=2)

# LDA需要类别标签y_train来学习投影方向
# LDA needs class labels y_train to learn projection direction
X_train_lda = lda.fit_transform(X_train_scaled, y_train)

# 转换测试数据
# Transform test data
X_test_lda = lda.transform(X_test_scaled)

# 打印LDA详细信息
# Print LDA detailed information
print(f"Explained variance ratio:")
for i, ev in enumerate(lda.explained_variance_ratio_, 1):
    print(f"  LD{i}: {ev:.4f}")
print(f"  Total: {sum(lda.explained_variance_ratio_):.4f}")

print(f"\nSVM Results on LDA-reduced data (d=2):")
# 在LDA降维后的数据上训练SVM
# Train SVM on LDA-reduced data
svm_models_lda = {}
for kernel in KERNELS:
    # 创建新的SVM分类器
    # Create new SVM classifier
    svm = SVC(kernel=kernel, random_state=RANDOM_STATE)
    
    # 在LDA降维后的训练数据上拟合
    # Fit on LDA-reduced training data
    svm.fit(X_train_lda, y_train)
    
    # 在LDA降维后的测试数据上预测
    # Predict on LDA-reduced test data
    y_pred = svm.predict(X_test_lda)
    
    # 计算准确率和混淆矩阵
    # Calculate accuracy and confusion matrix
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    # 存储结果
    # Store results
    svm_models_lda[kernel] = {'model': svm, 'accuracy': acc, 'cm': cm}
    
    # 打印结果
    # Print results
    print(f"  {kernel.upper()} kernel: Accuracy = {acc:.4f}")

print()

# ============================================================
# 步骤9：绘制LDA降维数据的2D图
# Step 9: Plot 2D graphs for LDA-reduced data
# ============================================================
print("=" * 80)
print("Step 9: Plot 2D graphs for LDA-reduced data")
print("=" * 80)

# 创建1行3列的子图布局
# Create 1 row x 3 columns subplot layout
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 设置总标题
# Set overall title
fig.suptitle('SVM with LDA-reduced data (2 components)')

# 遍历三种核函数
# Iterate through three kernels
for idx, kernel in enumerate(KERNELS):
    # 获取当前子图
    # Get current subplot
    ax = axes[idx]
    
    # 获取当前核函数的模型
    # Get model for current kernel
    model = svm_models_lda[kernel]['model']
    
    # 按类别绘制训练样本散点图
    # Plot training samples scatter plot by class
    for class_idx in range(3):
        # 创建布尔掩码选择当前类别的样本
        # Create boolean mask to select samples of current class
        mask = y_train == class_idx
        
        # 绘制散点图
        # Plot scatter
        ax.scatter(X_train_lda[mask, 0], X_train_lda[mask, 1], 
                   c=COLORS[class_idx], label=f'Class {class_idx}', alpha=0.6)
    
    # 获取支持向量和对应标签
    # Get support vectors and corresponding labels
    sv = model.support_vectors_
    sv_labels = y_train[model.support_]
    
    # 用空心圆标记支持向量
    # Mark support vectors with hollow circles
    for class_idx in range(3):
        mask = sv_labels == class_idx
        if mask.sum() > 0:
            ax.scatter(sv[mask, 0], sv[mask, 1], 
                       facecolors='none', edgecolors=COLORS[class_idx], 
                       s=100, linewidths=2, label=f'SV Class {class_idx}')
    
    # 设置坐标轴标签（LDA使用LD1、LD2）
    # Set axis labels (LDA uses LD1, LD2)
    ax.set_xlabel('LD1')
    ax.set_ylabel('LD2')
    
    # 设置子图标题
    # Set subplot title
    ax.set_title(f'{kernel.upper()} Kernel')
    
    # 添加图例
    # Add legend
    ax.legend(loc='best', fontsize=8)

# 自动调整子图间距
# Automatically adjust subplot spacing
plt.tight_layout()

# 构建保存路径
# Build save path
lda_plot_path = os.path.join(OUTPUT_DIR, 'lda_svm_plots.png')

# 保存图表
# Save plot
plt.savefig(lda_plot_path, dpi=150, bbox_inches='tight')

# 关闭图表，释放内存
# Close plot to release memory
plt.close()

# 打印图表信息
# Print plot information
print(f"Saved: {os.path.relpath(lda_plot_path, SCRIPT_DIR)}")
print()

# ============================================================
# 步骤10：汇总结果表格（准确率和混淆矩阵）
# Step 10: Results table with accuracies and confusion matrices
# ============================================================
print("=" * 80)
print("Step 10: Results table with accuracies and confusion matrices")
print("=" * 80)

# 创建空列表存储所有结果
# Create empty list to store all results
results = []

# 添加标准化数据的SVM结果
# Add SVM results on standardized data
for kernel in KERNELS:
    results.append({
        'Model': f'Standardized, {kernel} SVM',
        'Accuracy': svm_models_std[kernel]['accuracy'],
        'Confusion Matrix': str(svm_models_std[kernel]['cm'].tolist())
    })

# 添加PCA降维数据的SVM结果
# Add SVM results on PCA-reduced data
for kernel in KERNELS:
    results.append({
        'Model': f'PCA (d=2), {kernel} SVM',
        'Accuracy': svm_models_pca[kernel]['accuracy'],
        'Confusion Matrix': str(svm_models_pca[kernel]['cm'].tolist())
    })

# 添加LDA降维数据的SVM结果
# Add SVM results on LDA-reduced data
for kernel in KERNELS:
    results.append({
        'Model': f'LDA (d=2), {kernel} SVM',
        'Accuracy': svm_models_lda[kernel]['accuracy'],
        'Confusion Matrix': str(svm_models_lda[kernel]['cm'].tolist())
    })

# 将结果列表转换为DataFrame
# Convert results list to DataFrame
results_df = pd.DataFrame(results)

# 打印完整的结果表格
# Print complete results table
print(f"\nSummary of all 9 model configurations:")
print(f"\n{'Model':<30} {'Accuracy':>10}")
print("-" * 42)
for _, row in results_df.iterrows():
    print(f"{row['Model']:<30} {row['Accuracy']:>10.4f}")

# 构建CSV保存路径
# Build CSV save path
csv_path = os.path.join(OUTPUT_DIR, 'lab2_results.csv')

# 保存结果到CSV文件
# Save results to CSV file
results_df.to_csv(csv_path, index=False)

# 打印保存路径
# Print save path
print(f"\nResults saved: {os.path.relpath(csv_path, SCRIPT_DIR)}")
