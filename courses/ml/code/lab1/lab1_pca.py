# CST8506 实验1：使用PCA进行降维
# 作者：Peng Wang
# 学号：041107730
# 日期：2026-01-22
# 
# 将PCA应用于糖尿病数据集，并比较降维前后随机森林的性能。
"""
CST8506 Lab 1: Dimensionality Reduction using PCA
Author: Peng Wang
Student Number: 041107730
Date: 2026-01-22

Applies PCA to the Diabetes dataset and compares Random Forest performance
before and after dimensionality reduction.
"""

# 导入必要的库：
# numpy - 数值计算库
# pandas - 数据处理库
# matplotlib.pyplot - 绑图库
# Axes3D - 3D绑图支持
# train_test_split - 数据集划分
# StandardScaler - 数据标准化
# PCA - 主成分分析
# RandomForestClassifier - 随机森林分类器
# confusion_matrix, accuracy_score - 模型评估指标
# Path - 文件路径处理

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from pathlib import Path

# 配置常量
# Configuration constants

# 固定随机种子以确保结果可复现（42是机器学习社区的常用惯例）
# Fixed seed for reproducibility (42 is a common convention in ML community)
# 原因：随机森林和数据划分都涉及随机性，固定种子确保每次运行结果相同，便于调试和验证
# Reason: Random Forest and data splitting involve randomness, fixed seed ensures identical results across runs for debugging and validation
RANDOM_STATE = 42

# 80-20 训练集-测试集划分（标准做法）
# 80-20 train-test split (standard practice)  
TEST_SIZE = 0.2

# 随机森林中的树木数量（在性能和速度之间取得平衡）
# Number of trees in Random Forest (balance between performance and speed)  
N_ESTIMATORS = 100

# 保留95%的方差（推荐范围：85-95%）
# Retain 95% of variance (recommended range: 85-95%)
# 原因：95%是信息保留和降维之间的良好平衡点 - 保留了大部分信息，同时显著减少维度
# Reason: 95% is a good balance between information retention and dimensionality reduction - retains most information while significantly reducing dimensions
# 太低（如80%）会丢失重要信息，太高（如99%）降维效果不明显
# Too low (e.g., 80%) loses important information, too high (e.g., 99%) reduces dimensions insignificantly
VARIANCE_THRESHOLD = 0.95  

# 创建images目录用于保存图片，如果目录已存在则不报错
# Create images directory for saving plots, no error if directory already exists
# 原因：exist_ok=True 防止重复运行程序时因目录已存在而报错
# Reason: exist_ok=True prevents errors when running the program multiple times (directory already exists)
IMAGES_DIR = Path('images')
IMAGES_DIR.mkdir(exist_ok=True)

# 设置numpy的随机种子，确保每次运行结果一致
# Set numpy random seed to ensure consistent results across runs
np.random.seed(RANDOM_STATE)

print("=" * 80)
print("CST8506 Lab 1: PCA Dimensionality Reduction")
print("=" * 80)
print()

# 步骤1：加载CSV文件
# Step 1: Load the CSV file
print("Step 1: Loading diabetes.csv file...")
print("-" * 80)
# 使用pandas读取糖尿病数据集CSV文件
# Use pandas to read the diabetes dataset CSV file
df = pd.read_csv('diabetes.csv')
print("Dataset loaded successfully")
print()


# 步骤2：打印数据集信息
# Step 2: Print dataset information
print("Step 2: Dataset Information")
print("-" * 80)
# 打印所有属性（列）名称
# Print all attribute (column) names
print("Attribute names:", df.columns.tolist())
# 打印实例（行）数量
# Print number of instances (rows)
print(f"Number of instances: {len(df)}")
# 打印属性（列）数量
# Print number of attributes (columns)
print(f"Number of attributes: {len(df.columns)}")
# 打印前5行数据，用于快速查看数据结构
# Print first 5 rows for quick data structure inspection
print("\nFirst 5 instances:")
print(df.head())
print()


# 步骤3：将数据集划分为训练集和测试集
# Step 3: Split the dataset into train and test sets
print("Step 3: Splitting dataset into train and test sets")
print("-" * 80)
# X是特征矩阵，删除'class'列（目标变量）
# X is the feature matrix, drop 'class' column (target variable)
X = df.drop('class', axis=1)
# y是目标变量（类别标签）
# y is the target variable (class labels)
y = df['class']
# 使用train_test_split划分数据：
# Use train_test_split to split data:
# - test_size=0.2 表示20%作为测试集
# - test_size=0.2 means 20% for test set
# - random_state=42 确保划分可复现
# - random_state=42 ensures reproducible split
# - stratify=y 确保训练集和测试集中各类别比例相同（分层抽样）
# - stratify=y ensures same class proportions in train and test sets (stratified sampling)
# 原因：如果原数据有60%阳性40%阴性，分层抽样保证训练集和测试集也是60%/40%
# Reason: If original data has 60% positive 40% negative, stratified sampling ensures train/test sets also have 60%/40%
# 避免类别不平衡导致的评估偏差（如测试集全是阳性样本）
# Prevents evaluation bias from class imbalance (e.g., test set contains only positive samples)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"Training set size: {X_train.shape[0]} instances")
print(f"Test set size: {X_test.shape[0]} instances")
print(f"Number of features: {X_train.shape[1]}")
print()


# 步骤4：标准化数据
# Step 4: Standardize the data
# 为什么要标准化？
# Why standardize?
# 原因1：PCA对特征尺度敏感 - 大数值特征会主导主成分分析
# Reason 1: PCA is sensitive to feature scales - large-valued features dominate principal components
# 原因2：不同特征可能有不同的量级和单位（如：年龄0-100 vs 血糖50-300）
# Reason 2: Different features may have different scales and units (e.g., age 0-100 vs glucose 50-300)
# 原因3：标准化使所有特征在同一尺度上，确保每个特征对PCA的贡献是公平的
# Reason 3: Standardization puts all features on same scale, ensuring fair contribution to PCA
# 标准化后：均值=0，标准差=1，消除量纲影响
# After standardization: mean=0, std=1, eliminates dimensional effects
print("Step 4: Standardizing the data")
print("-" * 80)

# 创建标准化器对象
# Create StandardScaler object
scaler = StandardScaler()

# 对训练集进行拟合和转换：计算均值和标准差，然后标准化
# Fit and transform training set: compute mean and std, then standardize
# 标准化公式：z = (x - μ) / σ，使数据均值为0，标准差为1
# Standardization formula: z = (x - μ) / σ, makes data have mean=0, std=1
# 原因：训练集需要先fit学习数据的分布特征（均值μ和标准差σ），然后用这些特征进行标准化
# Reason: Training set needs to first fit to learn distribution (mean μ and std σ), then standardize using these parameters
X_train_scaled = scaler.fit_transform(X_train)

# 对测试集只进行转换（使用训练集的均值和标准差），避免数据泄露
# Only transform test set (using training set's mean and std) to avoid data leakage
# 原因1：测试集必须用训练集的统计量（μ和σ），不能重新计算，否则会造成数据泄露
# Reason 1: Test set must use training set's statistics (μ and σ), cannot recompute, otherwise causes data leakage
# 原因2：模拟真实场景 - 实际应用中，新数据只能用训练时学到的参数进行标准化
# Reason 2: Simulate real scenario - in practice, new data can only be standardized using parameters learned during training
# 错误示例：scaler.fit_transform(X_test) 会让模型提前"看到"测试集的分布，导致评估结果过于乐观
# Wrong example: scaler.fit_transform(X_test) would let model "see" test set distribution, causing overly optimistic evaluation
X_test_scaled = scaler.transform(X_test)

print("Data standardized successfully")
# 标准化后均值应接近0
# After standardization, mean should be close to 0
print(f"Mean of scaled training data: {X_train_scaled.mean():.6f}")
# 标准化后标准差应接近1
# After standardization, std should be close to 1
print(f"Standard deviation of scaled training data: {X_train_scaled.std():.6f}")
print()


# 步骤5：训练随机森林模型（基准模型）
# Step 5: Fit Random Forest model (Baseline)
# 为什么需要基准模型？
# Why need a baseline model?
# 原因：基准模型使用所有原始特征，作为对比参照，用于评估PCA降维是否有效
# Reason: Baseline model uses all original features as a reference to evaluate if PCA dimensionality reduction is effective
# 如果PCA后准确率接近或超过基准，说明降维成功（用更少特征达到相似性能）
# If accuracy after PCA is close to or exceeds baseline, dimensionality reduction is successful (similar performance with fewer features)
print("Step 5: Training baseline Random Forest model (before PCA)")
print("-" * 80)
# 创建随机森林分类器，包含100棵决策树
# Create Random Forest classifier with 100 decision trees
rf_baseline = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
# 使用标准化后的训练数据训练模型
# Train model using standardized training data
rf_baseline.fit(X_train_scaled, y_train)
# 对测试集进行预测
# Make predictions on test set
y_pred_baseline = rf_baseline.predict(X_test_scaled)
# 计算混淆矩阵：显示真实类别与预测类别的对比
# Compute confusion matrix: shows comparison between true and predicted classes
# 为什么需要混淆矩阵？
# Why need confusion matrix?
# 原因：准确率只是一个数字，混淆矩阵展示模型在各类别上的详细表现
# Reason: Accuracy is just one number, confusion matrix shows detailed performance on each class
# 可以看出模型是否偏向某个类别（如总预测阳性），或哪种错误更常见（假阳性 vs 假阴性）
# Shows if model is biased toward certain class (e.g., always predicts positive), or which errors are more common (false positive vs false negative)
cm_baseline = confusion_matrix(y_test, y_pred_baseline)
# 计算准确率：正确预测数 / 总预测数
# Compute accuracy: number of correct predictions / total predictions
acc_baseline = accuracy_score(y_test, y_pred_baseline)
print("Baseline model trained successfully")
print("Baseline Confusion Matrix:")
# 混淆矩阵解读：
# Confusion matrix interpretation:
# [[TN, FP],   TN=真阴性，FP=假阳性
# [[TN, FP],   TN=True Negative, FP=False Positive
#  [FN, TP]]   FN=假阴性，TP=真阳性
#  [FN, TP]]   FN=False Negative, TP=True Positive
print(cm_baseline)
print(f"Baseline Accuracy: {acc_baseline:.4f}")
print()


# 步骤6：应用PCA找出所有主成分
# Step 6: Apply PCA to find all principal components
# 为什么先运行完整PCA？
# Why run full PCA first?
# 原因：我们还不知道需要保留多少个主成分才能达到95%方差
# Reason: We don't yet know how many components are needed to reach 95% variance
# 先计算所有主成分和它们的解释方差比，然后根据累积方差确定最优数量d
# First compute all components and their variance ratios, then determine optimal number d based on cumulative variance
print("Step 6: Applying PCA to find all principal components")
print("-" * 80)
# 创建PCA对象，不指定组件数量，将保留所有主成分
# Create PCA object without specifying n_components, will retain all principal components
pca_full = PCA()
# 对训练集进行PCA拟合和转换
# Fit and transform PCA on training set
# PCA通过特征值分解协方差矩阵，找到数据方差最大的方向（主成分）
# PCA finds directions of maximum variance (principal components) via eigenvalue decomposition of covariance matrix
# 原因：fit学习主成分的方向（类似标准化学习均值和标准差），transform将数据投影到主成分上
# Reason: fit learns principal component directions (similar to standardization learning mean and std), transform projects data onto principal components
X_train_pca_full = pca_full.fit_transform(X_train_scaled)
# 对测试集进行PCA转换
# Transform test set using PCA
# 原因：测试集必须用训练集学到的主成分方向，不能重新计算，避免数据泄露
# Reason: Test set must use principal component directions learned from training set, cannot recompute to avoid data leakage
X_test_pca_full = pca_full.transform(X_test_scaled)
print("PCA applied successfully")
# 打印主成分总数（等于原始特征数）
# Print total number of components (equals original number of features)
print(f"Total number of components: {pca_full.n_components_}")
print()


# 步骤7：打印解释方差比
# Step 7: Print explained variance ratios
print("Step 7: Explained Variance Ratios")
print("-" * 80)
# 每个主成分解释的方差比例
# Variance ratio explained by each principal component
# 解释方差比 = 该主成分的方差 / 总方差
# Explained variance ratio = variance of this component / total variance
# 什么是解释方差比？
# What is explained variance ratio?
# 原因：衡量每个主成分捕获了多少数据变化信息
# Reason: Measures how much data variation information each principal component captures
# 例如：PC1=0.40表示第一主成分解释了40%的数据变化
# Example: PC1=0.40 means first component explains 40% of data variation
# 主成分按解释方差从大到小排序，PC1最重要，PC2次之...
# Components are sorted by variance explained (largest first), PC1 is most important, then PC2...
explained_var = pca_full.explained_variance_ratio_
# 累积解释方差比：前n个主成分共解释了多少方差
# Cumulative explained variance ratio: how much variance is explained by first n components
# 例如：如果explained_var=[0.40, 0.30, 0.20, 0.10]
# Example: if explained_var=[0.40, 0.30, 0.20, 0.10]
# 则cumulative_var=[0.40, 0.70, 0.90, 1.00]
# then cumulative_var=[0.40, 0.70, 0.90, 1.00]
# 表示PC1解释40%，PC1+PC2解释70%，PC1+PC2+PC3解释90%...
# meaning PC1 explains 40%, PC1+PC2 explain 70%, PC1+PC2+PC3 explain 90%...
cumulative_var = np.cumsum(explained_var)

# 打印每个主成分的解释方差比
# Print explained variance ratio for each component
print("Explained Variance Ratio for each component:")
for i, var in enumerate(explained_var, 1):
    print(f"  PC{i}: {var:.4f} ({var*100:.2f}%)")

# 打印累积解释方差比，用于确定需要保留多少主成分
# Print cumulative explained variance ratios to determine how many components to retain
print("\nCumulative Explained Variance Ratios:")
for i, cum_var in enumerate(cumulative_var, 1):
    print(f"  PC1-PC{i}: {cum_var:.4f} ({cum_var*100:.2f}%)")
print()


# 步骤8：生成碎石图
# Step 8: Generate Scree Plots
# 什么是碎石图？为什么要画它？
# What is a Scree Plot? Why create it?
# 原因：碎石图可视化每个主成分的重要性，帮助确定保留多少个主成分
# Reason: Scree plot visualizes importance of each component, helps determine how many components to retain
# 左图显示各主成分的解释方差（通常呈递减趋势，寻找"肘点"）
# Left plot shows variance explained by each component (usually decreasing, look for "elbow point")
# 右图显示累积方差（帮助找到达到目标方差如95%所需的最少主成分数）
# Right plot shows cumulative variance (helps find minimum components needed to reach target variance like 95%)
print("Step 8: Generating Scree Plots")
print("-" * 80)

# 创建1行2列的子图，图像大小为14x5英寸
# Create 1 row, 2 columns subplots, figure size 14x5 inches
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 绘制解释方差比折线图：蓝色圆点连线
# Plot explained variance ratio line chart: blue circles with lines
ax1.plot(range(1, len(explained_var) + 1), explained_var, 
         'bo-', linewidth=2, markersize=8)
# x轴标签：主成分编号
# x-axis label: principal component number
ax1.set_xlabel('Principal Component Number', fontsize=12)
# y轴标签：解释方差比
# y-axis label: explained variance ratio
ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
# 图标题：碎石图 - 解释方差比
# Plot title: Scree Plot - Explained Variance Ratio
ax1.set_title('Scree Plot - Explained Variance Ratio', fontsize=14, fontweight='bold')
# 添加网格线，透明度0.3
# Add grid lines with alpha=0.3
ax1.grid(True, alpha=0.3)
# 设置x轴刻度
# Set x-axis ticks
ax1.set_xticks(range(1, len(explained_var) + 1))

# 绘制累积解释方差比折线图：红色圆点连线
# Plot cumulative explained variance ratio line chart: red circles with lines
ax2.plot(range(1, len(cumulative_var) + 1), cumulative_var, 
         'ro-', linewidth=2, markersize=8)
# 添加85%方差水平参考线（绿色虚线）
# Add 85% variance horizontal reference line (green dashed)
ax2.axhline(y=0.85, color='g', linestyle='--', linewidth=2, label='85% variance')
# 添加90%方差水平参考线（橙色虚线）
# Add 90% variance horizontal reference line (orange dashed)
ax2.axhline(y=0.90, color='orange', linestyle='--', linewidth=2, label='90% variance')
# 添加95%方差水平参考线（紫色虚线）
# Add 95% variance horizontal reference line (purple dashed)
ax2.axhline(y=0.95, color='purple', linestyle='--', linewidth=2, label='95% variance')
# x轴标签：主成分编号
# x-axis label: principal component number
ax2.set_xlabel('Principal Component Number', fontsize=12)
# y轴标签：累积解释方差比
# y-axis label: cumulative explained variance ratio
ax2.set_ylabel('Cumulative Explained Variance Ratio', fontsize=12)
# 图标题：碎石图 - 累积方差
# Plot title: Scree Plot - Cumulative Variance
ax2.set_title('Scree Plot - Cumulative Variance', fontsize=14, fontweight='bold')
# 添加图例，位于右下角
# Add legend at lower right
ax2.legend(loc='lower right')
# 添加网格线，透明度0.3
# Add grid lines with alpha=0.3
ax2.grid(True, alpha=0.3)
# 设置x轴刻度
# Set x-axis ticks
ax2.set_xticks(range(1, len(cumulative_var) + 1))

# 自动调整子图间距
# Automatically adjust subplot spacing
plt.tight_layout()
# 保存图片，分辨率300dpi
# Save figure with 300 dpi resolution
plt.savefig(IMAGES_DIR / 'lab1_scree_plots.png', dpi=300, bbox_inches='tight')
# 关闭图形，释放内存
# Close figure to release memory
plt.close()

print("Scree plots saved as 'images/lab1_scree_plots.png'")

# 找到累积方差首次达到阈值（95%）的主成分数量
# Find number of components where cumulative variance first reaches threshold (95%)
# argmax返回第一个True的索引，+1是因为索引从0开始
# argmax returns index of first True, +1 because index starts from 0
# 例如：cumulative_var = [0.4, 0.7, 0.92, 0.96] 且 VARIANCE_THRESHOLD=0.95
# Example: cumulative_var = [0.4, 0.7, 0.92, 0.96] and VARIANCE_THRESHOLD=0.95
# 步骤：cumulative_var >= 0.95 → [False, False, False, True]
# Steps: cumulative_var >= 0.95 → [False, False, False, True]
# argmax找到第一个True的位置 → 索引3，+1后得到d=4（需要4个主成分）
# argmax finds first True position → index 3, +1 gives d=4 (need 4 components)
d = np.argmax(cumulative_var >= VARIANCE_THRESHOLD) + 1
# 打印达到95%方差所需的最优主成分数量
# Print optimal number of components needed to reach 95% variance
print(f"\nOptimal number of components (d) for {VARIANCE_THRESHOLD*100:.0f}% variance: {d}")
# 打印这些主成分实际解释的方差比例
# Print actual variance ratio explained by these components
print(f"Variance explained by {d} components: {cumulative_var[d-1]:.4f} ({cumulative_var[d-1]*100:.2f}%)")
print()


# 步骤9：使用d个主成分重新运行PCA
# Step 9: Re-run PCA with d components
# 为什么要重新运行PCA？
# Why re-run PCA?
# 原因1：虽然步骤6已经计算了所有主成分，但只是为了分析和确定最优数量d
# Reason 1: Although step 6 computed all components, it was only for analysis and determining optimal number d
# 原因2：现在明确只保留d个主成分，使输出数据维度更清晰（8个特征→d个特征）
# Reason 2: Now explicitly retain only d components, making output dimensionality clearer (8 features → d features)
# 原因3：代码规范性 - 明确指定n_components=d，而不是使用全量PCA再手动截取
# Reason 3: Code clarity - explicitly specify n_components=d instead of using full PCA and manually truncating
print(f"Step 9: Re-running PCA with d={d} components")
print("-" * 80)
# 创建PCA对象，只保留d个主成分
# Create PCA object, retain only d principal components
pca_final = PCA(n_components=d)
# 对训练集进行降维
# Reduce dimensionality of training set
X_train_pca = pca_final.fit_transform(X_train_scaled)
# 对测试集进行降维
# Reduce dimensionality of test set
X_test_pca = pca_final.transform(X_test_scaled)
print("PCA with optimal components applied successfully")
# 原始维度（特征数）
# Original dimensions (number of features)
print(f"Original dimensions: {X_train_scaled.shape[1]}")
# 降维后的维度
# Reduced dimensions
print(f"Reduced dimensions: {X_train_pca.shape[1]}")
# 维度变化：从原始维度降到d维
# Dimensionality change: from original dimensions to d dimensions
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d}")
print()


# 步骤10：在降维后的数据集上应用随机森林
# Step 10: Apply Random Forest to reduced dataset
print("Step 10: Training Random Forest on PCA-reduced dataset")
print("-" * 80)
# 创建新的随机森林分类器
# Create new Random Forest classifier
rf_pca = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
# 使用降维后的训练数据训练模型
# Train model using dimensionality-reduced training data
rf_pca.fit(X_train_pca, y_train)
# 对降维后的测试集进行预测
# Make predictions on dimensionality-reduced test set
y_pred_pca = rf_pca.predict(X_test_pca)
# 计算混淆矩阵
# Compute confusion matrix
cm_pca = confusion_matrix(y_test, y_pred_pca)
# 计算准确率
# Compute accuracy
acc_pca = accuracy_score(y_test, y_pred_pca)
print("Model trained on PCA-reduced data successfully")
print("PCA Confusion Matrix:")
print(cm_pca)
print(f"PCA Accuracy: {acc_pca:.4f}")
print()


# 步骤11：打印混淆矩阵对比
# Step 11: Print confusion matrices comparison
print("Step 11: Confusion Matrix Comparison")
print("-" * 80)
# PCA之前（基准模型）
# Before PCA (Baseline model)
print("Before PCA (Baseline):")
print(cm_baseline)
print()
# PCA之后
# After PCA
print("After PCA:")
print(cm_pca)
print()


# 步骤12：打印准确率对比
# Step 12: Print accuracy comparison
print("Step 12: Accuracy Comparison")
print("-" * 80)
# PCA之前的准确率
# Accuracy before PCA
print(f"Accuracy before PCA: {acc_baseline:.4f} ({acc_baseline*100:.2f}%)")
# PCA之后的准确率
# Accuracy after PCA
print(f"Accuracy after PCA:  {acc_pca:.4f} ({acc_pca*100:.2f}%)")
# 准确率变化（正值表示提升，负值表示下降）
# Accuracy change (positive means improvement, negative means decrease)
print(f"Accuracy change:     {acc_pca - acc_baseline:+.4f} ({(acc_pca - acc_baseline)*100:+.2f}%)")
# 维度降低：从原始特征数降到d个特征
# Dimensionality reduction: from original features to d features
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d} features")
print()


# 步骤13：绘制前2个主成分（2D可视化）
# Step 13: Plot first 2 principal components (2D)
# 为什么要可视化前2个主成分？
# Why visualize first 2 principal components?
# 原因1：人类只能直观理解2D/3D空间，无法可视化8维空间
# Reason 1: Humans can only intuitively understand 2D/3D space, cannot visualize 8-dimensional space
# 原因2：前2个主成分通常捕获了最多的数据变化信息
# Reason 2: First 2 components usually capture most data variation information
# 原因3：通过颜色区分类别，可以观察不同类别在降维空间中的分布和可分离性
# Reason 3: By color-coding classes, we can observe distribution and separability of different classes in reduced space
print("Step 13: Plotting first 2 principal components (2D visualization)")
print("-" * 80)

# 创建10x8英寸的图形
# Create 10x8 inch figure
plt.figure(figsize=(10, 8))
# 获取所有唯一的类别标签
# Get all unique class labels
classes = np.unique(y_train)
# 使用Set1颜色映射为每个类别分配不同颜色
# Use Set1 colormap to assign different colors to each class
colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))

for class_label, color in zip(classes, colors):
    # 创建布尔掩码，选择属于当前类别的样本
    # Create boolean mask to select samples belonging to current class
    mask = y_train == class_label
    # 绘制散点图：
    # Plot scatter plot:
    # - X_train_pca[mask, 0] 是第一主成分（PC1）
    # - X_train_pca[mask, 0] is the first principal component (PC1)
    # - X_train_pca[mask, 1] 是第二主成分（PC2）
    # - X_train_pca[mask, 1] is the second principal component (PC2)
    # - alpha=0.6 设置透明度
    # - alpha=0.6 sets transparency
    # - edgecolors='black' 设置点的边框颜色
    # - edgecolors='black' sets point border color
    # - s=50 设置点的大小
    # - s=50 sets point size
    plt.scatter(X_train_pca[mask, 0], X_train_pca[mask, 1], c=[color],
               label=f'Class {class_label}', alpha=0.6,
               edgecolors='black', linewidth=0.5, s=50)

# x轴标签：第一主成分
# x-axis label: First Principal Component
plt.xlabel('First Principal Component (PC1)', fontsize=12)
# y轴标签：第二主成分
# y-axis label: Second Principal Component
plt.ylabel('Second Principal Component (PC2)', fontsize=12)
# 图标题：2D可视化：前2个主成分
# Plot title: 2D Visualization: First 2 Principal Components
plt.title('2D Visualization: First 2 Principal Components', 
          fontsize=14, fontweight='bold')
# 添加图例，自动选择最佳位置
# Add legend, automatically choose best location
plt.legend(loc='best', fontsize=10)
# 添加网格线，透明度0.3
# Add grid lines with alpha=0.3
plt.grid(True, alpha=0.3)
# 自动调整子图间距
# Automatically adjust subplot spacing
plt.tight_layout()
# 保存图片，分辨率300dpi
# Save figure with 300 dpi resolution
plt.savefig(IMAGES_DIR / 'lab1_pca_2d.png', dpi=300, bbox_inches='tight')
# 关闭图形，释放内存
# Close figure to release memory
plt.close()

print("2D plot saved as 'images/lab1_pca_2d.png'")
print()


# 步骤14：绘制前3个主成分（3D可视化）
# Step 14: Plot first 3 principal components (3D)
# 为什么还要3D可视化？
# Why also create 3D visualization?
# 原因：3D可视化包含第三主成分（PC3），捕获更多信息，能看到2D图中看不到的数据结构
# Reason: 3D visualization includes third component (PC3), captures more information, reveals data structures invisible in 2D
# PC1+PC2+PC3 通常能解释更高比例的方差（如70-80%），比只看PC1+PC2（如50-60%）更全面
# PC1+PC2+PC3 usually explains higher variance proportion (e.g., 70-80%) than just PC1+PC2 (e.g., 50-60%), more comprehensive
print("Step 14: Plotting first 3 principal components (3D visualization)")
print("-" * 80)

# 创建12x9英寸的图形
# Create 12x9 inch figure
fig = plt.figure(figsize=(12, 9))
# 添加3D子图
# Add 3D subplot
ax = fig.add_subplot(111, projection='3d')

classes = np.unique(y_train)
colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))

for class_label, color in zip(classes, colors):
    mask = y_train == class_label
    # 绘制3D散点图：
    # Plot 3D scatter plot:
    # - X_train_pca[mask, 0] 是第一主成分（PC1）
    # - X_train_pca[mask, 0] is the first principal component (PC1)
    # - X_train_pca[mask, 1] 是第二主成分（PC2）
    # - X_train_pca[mask, 1] is the second principal component (PC2)
    # - X_train_pca[mask, 2] 是第三主成分（PC3）
    # - X_train_pca[mask, 2] is the third principal component (PC3)
    ax.scatter(X_train_pca[mask, 0], X_train_pca[mask, 1], X_train_pca[mask, 2],
              c=[color], label=f'Class {class_label}', alpha=0.6,
              edgecolors='black', linewidth=0.5, s=50)

# x轴标签：第一主成分
# x-axis label: First Principal Component
ax.set_xlabel('First Principal Component (PC1)', fontsize=11)
# y轴标签：第二主成分
# y-axis label: Second Principal Component
ax.set_ylabel('Second Principal Component (PC2)', fontsize=11)
# z轴标签：第三主成分
# z-axis label: Third Principal Component
ax.set_zlabel('Third Principal Component (PC3)', fontsize=11)
# 图标题：3D可视化：前3个主成分
# Plot title: 3D Visualization: First 3 Principal Components
ax.set_title('3D Visualization: First 3 Principal Components',
             fontsize=14, fontweight='bold')
# 添加图例，自动选择最佳位置
# Add legend, automatically choose best location
ax.legend(loc='best', fontsize=10)
# 添加网格线，透明度0.3
# Add grid lines with alpha=0.3
ax.grid(True, alpha=0.3)

# 自动调整子图间距
# Automatically adjust subplot spacing
plt.tight_layout()
# 保存图片，分辨率300dpi
# Save figure with 300 dpi resolution
plt.savefig(IMAGES_DIR / 'lab1_pca_3d.png', dpi=300, bbox_inches='tight')
# 关闭图形，释放内存
# Close figure to release memory
plt.close()

print("3D plot saved as 'images/lab1_pca_3d.png'")
print()
