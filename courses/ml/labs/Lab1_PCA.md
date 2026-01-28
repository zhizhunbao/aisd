# CST8506 - Lab 1: Dimensionality Reduction – PCA

**Due Date:** Check Brightspace for due dates.

## Introduction

The goal of this lab is to reduce the dimensionality using PCA on Diabetes dataset.

You are required to complete this assignment using a Google Colab notebook. Your notebook must be organized into clearly labeled cells, following the steps outlined below. Each step must appear in a separate cell, with an appropriate heading and brief description explaining the purpose of the code and the results of that cell. If there is no explanation, no marks will be given. After finishing the lab, take screenshots of each step and paste it in the given answer document and save the document as `Lab1_<firstname>.doc`.

Before starting the lab, create a `diabetes.csv` file (add column headers too) from `diabetes.arff` file that is in the Weka's data folder. There is a diabetes file in sklearn, but the feature names are not clear. So, we will use the diabetes file in Weka that has a meaningful explanation for the features.

> **📝 笔记:**
>
> **实验目标:**
>
> - 使用主成分分析 (PCA) 对糖尿病数据集进行降维
> - 对比降维前后的分类效果（Random Forest）
>
> **准备工作:**
>
> - 从 Weka 的 `diabetes.arff` 文件转换为 `diabetes.csv`
> - 需要手动添加列名（特征名称）
>
> **💡 提示:** 每个步骤需要单独的代码单元格，并附带说明文字

## Steps

All these steps should be done in Python:

1. Load the csv file using Pandas csv read functionality.

> **📝 笔记:**
>
> **加载数据:**
>
> - 使用 `pd.read_csv()` 读取CSV文件
> - 确保文件路径正确

2. Print the attribute names, number of instances, number of attributes and the first 5 instances.

> **📝 笔记:**
>
> **数据探索:**
>
> - `df.columns` 查看属性名
> - `df.shape` 查看样本数和特征数
> - `df.head(5)` 查看前5行

3. Split the dataset into train and test sets.

> **📝 笔记:**
>
> **数据划分:**
>
> - 使用 `train_test_split()` 划分训练集和测试集
> - 常用比例：80/20 或 70/30

4. Standardize data in the dataset (fit on the train set and transform it, also, transform the test set).

> **📝 笔记:**
>
> **数据标准化:**
>
> - 使用 `StandardScaler()` 进行标准化
> - 只在训练集上 `fit`，然后对训练集和测试集都 `transform`
> - PCA 对数据尺度敏感，标准化是必要的预处理
>
> **💡 提示:** 避免数据泄露，不要在整个数据集上 fit

5. Fit a Random Forest model on the train dataset and then predict the class for the test set. Record the confusion matrix and the accuracy.

> **📝 笔记:**
>
> **Random Forest 分类:**
>
> - 使用 `RandomForestClassifier()` 训练模型
> - `confusion_matrix()` 和 `accuracy_score()` 评估性能
> - 记录这个结果，后续与 PCA 降维后对比

6. Apply PCA to find the principal components (fit and transform the train set and transform the test set). (Generate all possible components at this step). Explain the parameter to set the required number of components.

> **📝 笔记:**
>
> **PCA 主成分分析:**
>
> - 使用 `PCA(n_components=None)` 生成所有主成分
> - `n_components` 参数控制保留的主成分数量
> - 同样在训练集上 fit，然后 transform 两个数据集

7. Print the explained variance ratios and cumulative explained variance ratios.

> **📝 笔记:**
>
> **方差解释率:**
>
> - `pca.explained_variance_ratio_` 每个主成分的方差贡献
> - `np.cumsum()` 计算累计方差解释率
> - 用于确定需要保留多少个主成分

8. Generate both scree plots (with explained variance and with cumulative variance) to find the best number of principal components (denote it as d).

> **📝 笔记:**
>
> **Scree Plot 碎石图:**
>
> - 图1：各主成分的方差解释率（柱状图）
> - 图2：累计方差解释率（折线图）
> - 找到"肘部"点或累计解释率达到预期阈值（如 90%）的位置
> - 确定最佳主成分数量 d

9. Once you find d, re-run PCA with d components.

> **📝 笔记:**
>
> **重新执行 PCA:**
>
> - 使用 `PCA(n_components=d)` 保留 d 个主成分
> - 得到降维后的数据集

10. Apply Random Forest to the new d-dimensional dataset and find the confusion matrix and the accuracy.

> **📝 笔记:**
>
> **降维后分类:**
>
> - 在降维后的数据上重新训练 Random Forest
> - 记录混淆矩阵和准确率
> - 与步骤5的结果进行对比

11. Print Confusion matrix before and after applying PCA.

> **📝 笔记:**
>
> **混淆矩阵对比:**
>
> - 并排展示原始数据和 PCA 降维后的混淆矩阵
> - 分析分类性能的变化

12. Print accuracies before and after applying PCA.

> **📝 笔记:**
>
> **准确率对比:**
>
> - 比较降维前后的准确率
> - 讨论维度降低对分类效果的影响

13. Plot the first 2 principal components color coded by each class.

> **📝 笔记:**
>
> **2D 可视化:**
>
> - 使用 `plt.scatter()` 绘制前两个主成分
> - 不同类别用不同颜色表示
> - 观察类别的分离程度

14. Plot the first 3 principal components color coded by each class.

> **📝 笔记:**
>
> **3D 可视化:**
>
> - 使用 `Axes3D` 绘制前三个主成分
> - 通过 3D 视图观察数据分布
>
> **💡 提示:** 使用 `from mpl_toolkits.mplot3d import Axes3D`

## Grading

To get grades:

1. You should demo your Python code and results.
2. Submit your answer document and the google colab runnable code in Brightspace. You must use the given answer template to write your answers.
3. DO NOT ZIP your files. Zipped files will not be graded.

> **📝 笔记:**
>
> **提交要求:**
>
> - 文档命名：`Lab1_<firstname>.doc`
> - 每个步骤需要截图并粘贴到答题模板
> - 提交 Colab notebook 和答题文档到 Brightspace
> - **注意：不要压缩文件，压缩包不予评分**
