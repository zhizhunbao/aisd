# CST8506 - Lab 2: Support Vector Machines

**Due Date:** Check Brightspace for due dates.

## Introduction

The goal of this lab is to classify Wine dataset using SVM (using standardized dataset, transformed dataset by applying PCA and LDA). The dataset can be found in sklearn's datasets package (<https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html>).

> **📝 笔记:**
>
> **实验目标:**
>
> - 使用支持向量机 (SVM) 对葡萄酒数据集进行分类
> - 对比三种核函数：线性 (linear)、多项式 (poly)、RBF
> - 对比三种数据处理方式：标准化、PCA 降维、LDA 降维
>
> **💡 提示:** Wine 数据集来自 sklearn，可直接使用 `load_wine()` 加载

## Steps

All these steps should be done in Python:

1. Load the dataset.

> **📝 笔记:**
>
> **加载数据:**
>
> - 使用 `from sklearn.datasets import load_wine`
> - `wine = load_wine()` 获取数据
> - `X = wine.data`，`y = wine.target`

2. Print number of instances, number and names of attributes and first 5 rows of the dataset.

> **📝 笔记:**
>
> **数据探索:**
>
> - `wine.feature_names` 查看特征名称
> - `X.shape` 查看样本数和特征数
> - 打印前5行数据

3. Split the dataset into train and test sets.

> **📝 笔记:**
>
> **数据划分:**
>
> - 使用 `train_test_split()` 划分数据
> - 常用比例：70/30 或 80/20

4. Standardize data in the dataset.

> **📝 笔记:**
>
> **数据标准化:**
>
> - 使用 `StandardScaler()` 标准化
> - SVM 对特征尺度敏感，标准化是必要步骤
>
> **💡 提示:** 只在训练集上 fit，避免数据泄露

5. Fit SVM model on the train set and make predictions for the test set. (use linear, polynomial and rbf kernels)

> **📝 笔记:**
>
> **SVM 三种核函数:**
>
> - `SVC(kernel='linear')` 线性核
> - `SVC(kernel='poly')` 多项式核
> - `SVC(kernel='rbf')` 高斯径向基核（默认）
> - 每种核函数都需要训练并预测

6. Apply PCA to find the principal components of the standardized dataset. Find the best 'd'.

> **📝 笔记:**
>
> **PCA 降维:**
>
> - 使用 Scree Plot 或累计方差解释率确定最佳 d
> - 通常选择累计方差达到 90% 或 95% 的点

7. Using the first 2 components, plot 2D graphs – the train set (color-coded by each class) and the support vectors too (edge-colors should be color-coded by each class) for all three models (refer to the slides for a reference) for each SVM model.

> **📝 笔记:**
>
> **PCA 2D 可视化:**
>
> - 使用前2个主成分绘制散点图
> - 训练样本：按类别着色
> - 支持向量：使用边框颜色按类别区分
> - 需要绘制3个子图（linear, poly, rbf）
> - 支持向量可通过 `svm.support_vectors_` 获取
>
> **💡 提示:** 每个图中有6种颜色 — 3个类别 + 3组支持向量

8. Apply LDA to reduce the dimensionality of the standardized dataset. Mention how many components you have used.

> **📝 笔记:**
>
> **LDA 降维:**
>
> - 使用 `LinearDiscriminantAnalysis()` 进行 LDA
> - LDA 最多保留 (n_classes - 1) 个成分
> - Wine 数据集有3类，因此最多2个成分
> - 需要明确说明使用了多少个成分

9. For the new dataset, plot 2D graphs – the train set (color-coded by each class) and the support vectors too (edge colors should be color-coded by each class) for all three models (refer to the slides for a sample) for each SVM model.

> **📝 笔记:**
>
> **LDA 2D 可视化:**
>
> - 与步骤7类似，但使用 LDA 降维后的数据
> - 同样需要3个子图展示三种核函数
> - 标注支持向量

10. Find accuracies and CM for all three models on Standardized dataset, reduced dataset by PCA, and reduced dataset by LDA and tabulate them in Python. The table should be in the following format (For PCA and LDA, fill in the value for d, which is the number of components):

| Model                    | Accuracy | Confusion Matrix |
| ------------------------ | -------- | ---------------- |
| Standardized, linear SVM |          |                  |
| Standardized, poly SVM   |          |                  |
| Standardized, RBF SVM    |          |                  |
| PCA (d), linear SVM      |          |                  |
| PCA (d), poly SVM        |          |                  |
| PCA (d), RBF SVM         |          |                  |
| LDA (d), linear SVM      |          |                  |
| LDA (d), poly SVM        |          |                  |
| LDA (d), RBF SVM         |          |                  |

> **📝 笔记:**
>
> **结果汇总:**
>
> - 共9组实验结果（3种数据 × 3种核函数）
> - 使用 `accuracy_score()` 计算准确率
> - 使用 `confusion_matrix()` 生成混淆矩阵
> - 可以使用 `pd.DataFrame` 创建表格
>
> **💡 提示:** d 需要替换为实际使用的主成分数量

## Grading

To get grades:

1. You should be ready with your Python code and results.
2. Submit your Colab notebook file and the answer document to Brightspace.
3. In each graph, you will have 6 colors – 3 classes and 3 sets of support vectors.

> **📝 笔记:**
>
> **提交要求:**
>
> - 提交 Colab notebook 文件
> - 提交答题文档
> - 上传到 Brightspace
> - 绘图时注意：每张图应有6种颜色（3个类别 + 3组支持向量边框）
