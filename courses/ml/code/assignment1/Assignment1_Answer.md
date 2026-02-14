# CST8506 Assignment 1: Wine Quality Classification

**Author:** Peng Wang
**Student Number:** 041107730
**Course:** CST8506 - Machine Learning
**Date:** February 13, 2026

---

## Table of Contents

1. [Data Understanding - Load Dataset](#step-1)
2. [Data Understanding - Dataset Statistics](#step-2)
3. [Data Understanding - Missing Values & Data Types](#step-3)
4. [Data Preparation - Train/Test Split](#step-4)
5. [Data Preparation - Standardize Data](#step-5)
6. [Data Preparation - Apply PCA](#step-6)
7. [Data Preparation - Apply LDA](#step-7)
8. [Visualization - Scree Plots](#step-8)
9. [Modeling - Define Classification Function](#step-9)
10. [Modeling - Run 5 Classifiers on 3 Datasets](#step-10)
11. [Results - Best Results Table](#step-11)
12. [Results - Detailed All Parameters](#step-12)
13. [Visualization - PCA 2D with Support Vectors](#step-13)
14. [Visualization - LDA 2D with Support Vectors](#step-14)

---

## Step 1: Data Understanding - Load Wine Quality Dataset {#step-1}

Load the Wine dataset from sklearn (sourced from UCI ML Repository). The dataset contains 178 instances with 13 attributes and 3 classes.

### Code

![Step 1 Code](assignment1_images/assignment1_wine_quality_step01_code.png)

### Output

![Step 1 Output](assignment1_images/assignment1_wine_quality_step01_result.png)

### Discussion

The Wine dataset was loaded successfully with 178 instances and 13 chemical analysis attributes. There are 3 classes of wine (class_0, class_1, class_2). This is a well-known benchmark dataset from the UCI Machine Learning Repository, making it suitable for classification experiments.

---

## Step 2: Data Understanding - Dataset Statistics {#step-2}

Analyze the dataset attributes, class distribution, first few instances, and descriptive statistics.

### Code

![Step 2 Code](assignment1_images/assignment1_wine_quality_step02_code.png)

### Output

![Step 2 Output](assignment1_images/assignment1_wine_quality_step02_result.png)

### Discussion

The dataset has 13 numerical attributes including alcohol, malic acid, ash, etc. The class distribution shows class_0 has 59 instances (33.1%), class_1 has 71 instances (39.9%), and class_2 has 48 instances (27.0%). The classes are reasonably balanced. The descriptive statistics reveal that features have different scales (e.g., proline ranges 278-1680 while nonflavanoid_phenols ranges 0.13-0.66), which highlights the need for standardization.

---

## Step 3: Data Understanding - Missing Values & Data Types {#step-3}

Check for missing values and verify data types to ensure data quality.

### Code

![Step 3 Code](assignment1_images/assignment1_wine_quality_step03_code.png)

### Output

![Step 3 Output](assignment1_images/assignment1_wine_quality_step03_result.png)

### Discussion

There are zero missing values in the dataset. All attributes are float64 type (continuous numerical), and the target is int64 (categorical). The dataset is clean and ready for preprocessing without requiring imputation.

---

## Step 4: Data Preparation - Train/Test Split {#step-4}

Split the dataset into training (80%) and test (20%) sets with stratified sampling.

### Code

![Step 4 Code](assignment1_images/assignment1_wine_quality_step04_code.png)

### Output

![Step 4 Output](assignment1_images/assignment1_wine_quality_step04_result.png)

### Discussion

- **train_test_split** with `test_size=0.2` divides data into 142 training and 36 test instances.
- **stratify=y** ensures the class proportions are preserved in both sets.
- **random_state=42** ensures reproducibility.
- The stratified split maintains approximately the same class ratio in both training and test sets.

---

## Step 5: Data Preparation - Standardize Data {#step-5}

Apply StandardScaler to normalize all features to zero mean and unit variance.

### Code

![Step 5 Code](assignment1_images/assignment1_wine_quality_step05_code.png)

### Output

![Step 5 Output](assignment1_images/assignment1_wine_quality_step05_result.png)

### Discussion

StandardScaler transforms features to have mean ≈ 0 and std ≈ 1. This is critical because:

- **SVM** uses distance-based calculations in kernel space, sensitive to feature scales
- **kNN** relies on distance metrics, affected by differing feature magnitudes
- **MLP** performs gradient descent, which converges faster with normalized features
- **Logistic Regression** optimization benefits from uniform feature scales

The scaler is fit only on the training set and the same transformation is applied to the test set to prevent data leakage.

---

## Step 6: Data Preparation - Apply PCA {#step-6}

Apply Principal Component Analysis (PCA) for unsupervised dimensionality reduction, retaining 95% of the total variance.

### Code

![Step 6 Code](assignment1_images/assignment1_wine_quality_step06_code.png)

### Output

![Step 6 Output](assignment1_images/assignment1_wine_quality_step06_result.png)

### Discussion

PCA identifies the principal components that explain the most variance:

- The first principal component (PC1) explains the largest portion of variance
- The cumulative explained variance reaches 95% at the optimal number of components
- The dimensionality was reduced from 13 features to the optimal number of components
- PCA is unsupervised — it does not use class labels, only maximizing variance
- The separate PCA-transformed train/test sets (X_train_pca, X_test_pca) are saved for modeling

---

## Step 7: Data Preparation - Apply LDA {#step-7}

Apply Linear Discriminant Analysis (LDA) for supervised dimensionality reduction.

### Code

![Step 7 Code](assignment1_images/assignment1_wine_quality_step07_code.png)

### Output

![Step 7 Output](assignment1_images/assignment1_wine_quality_step07_result.png)

### Discussion

LDA reduces dimensionality to at most (n_classes - 1) = 2 components, because:

- LDA maximizes the ratio of between-class to within-class scatter
- With 3 classes, only 2 discriminant directions exist
- Unlike PCA, LDA is supervised — it uses class labels to find the most discriminative projections
- LDA typically yields better classification performance than PCA for the same number of components
- The separate LDA-transformed sets (X_train_lda, X_test_lda) are saved for modeling

---

## Step 8: Visualization - Scree Plots {#step-8}

Generate Scree Plot and Cumulative Scree Plot to visualize the explained variance by each principal component.

### Code

![Step 8 Code](assignment1_images/assignment1_wine_quality_step08_code.png)

### Scree Plots

![Scree Plots](assignment1_images/scree_plots.png)

### Discussion

- **Scree Plot** (left): Shows individual explained variance ratio for each principal component. The "elbow" identifies where adding more components provides diminishing returns.
- **Cumulative Scree Plot** (right): Shows the cumulative variance. The 95% threshold line and the optimal number of components are marked. This visual confirms the optimal dimension selected for PCA reduction.

---

## Step 9: Modeling - Define Classification Function {#step-9}

Define a reusable function `classify_and_evaluate()` that takes datasets and classifiers as parameters and returns accuracy and F1 scores.

### Code

![Step 9 Code](assignment1_images/assignment1_wine_quality_step09_code.png)

### Discussion

The function `classify_and_evaluate()` encapsulates the training and evaluation pipeline:

- Takes training/test data, classifier instance, and descriptive parameter string
- Trains the classifier, generates predictions
- Calculates both accuracy and weighted F1-score (appropriate for multi-class)
- Returns results in a dictionary for easy tabulation
- This design follows DRY principle — same function handles all 5 classifiers × 3 datasets × 3 parameter sets = 45 experiments

---

## Step 10: Modeling & Evaluation - Run All Classifiers {#step-10}

Run 5 classifiers (kNN, RF, SVM, LR, MLP) with 3 parameter sets each on 3 datasets (Standardized, After PCA, After LDA).

### Code

![Step 10 Code](assignment1_images/assignment1_wine_quality_step10_code.png)

### Output

![Step 10 Output](assignment1_images/assignment1_wine_quality_step10_result.png)

### Discussion

All 45 experiments completed successfully. Key observations:

- **kNN**: Performance varies with k value and distance metric. Distance-weighted voting generally performs better.
- **Random Forest**: Robust across all datasets. The number of estimators and max_depth affect performance.
- **SVM**: Different kernels (linear, rbf, poly) offer different decision boundaries.
- **Logistic Regression**: Strong baseline performance. Regularization parameter C controls model complexity.
- **MLP**: Neural network performance depends on architecture and activation function.

---

## Step 11: Best Results Table {#step-11}

Best accuracy and F1 score for each method on each dataset.

### Code

![Step 11 Code](assignment1_images/assignment1_wine_quality_step11_code.png)

### Output

![Step 11 Output](assignment1_images/assignment1_wine_quality_step11_result.png)

### Discussion

The summary table shows the best-performing parameter configuration for each classifier on each dataset. Key findings:

- **LDA** generally provides the best or comparable results due to its supervised nature
- **Standardized data** (without dimensionality reduction) often performs well with full feature information
- **PCA** may sacrifice some classification-relevant information since it is unsupervised
- The best overall models achieve near-perfect accuracy on this dataset

---

## Step 12: Detailed Results - All Parameters {#step-12}

Complete results for all 15 parameter configurations across all 3 datasets.

### Code

![Step 12 Code](assignment1_images/assignment1_wine_quality_step12_code.png)

### Output

![Step 12 Output](assignment1_images/assignment1_wine_quality_step12_result.png)

### Discussion

The detailed table allows comparison of how different hyperparameters affect each classifier:

- **kNN**: Smaller k with distance weighting tends to perform best
- **RF**: More trees (n_estimators) generally improve or maintain performance
- **SVM**: RBF kernel is often a strong default; linear kernel works well for linearly separable data
- **LR**: C=1.0 provides a good balance between bias and variance
- **MLP**: Deeper architectures don't always improve performance on small datasets

---

## Step 13: PCA 2D Visualization with Support Vectors {#step-13}

Visualize the PCA-reduced training set color-coded by class, with support vectors highlighted.

### Code

![Step 13 Code](assignment1_images/assignment1_wine_quality_step13_code.png)

### PCA 2D Visualization

![PCA 2D SVM](assignment1_images/pca_2d_svm.png)

### Discussion

The left plot shows the actual class distribution in the PCA 2D space. The right plot overlays the support vectors from an SVM (RBF kernel) trained on the 2D PCA data. Support vectors (marked with black edges) are the critical data points closest to the decision boundary. The visualization shows:

- Classes are reasonably well-separated in PCA space
- Support vectors cluster near the boundaries between classes
- Some overlap exists, particularly between adjacent classes

---

## Step 14: LDA 2D Visualization with Support Vectors {#step-14}

Visualize the LDA-reduced training set color-coded by class, with support vectors highlighted.

### Code

![Step 14 Code](assignment1_images/assignment1_wine_quality_step14_code.png)

### LDA 2D Visualization

![LDA 2D SVM](assignment1_images/lda_2d_svm.png)

### Discussion

The LDA 2D visualization shows superior class separation compared to PCA:

- Classes are more tightly clustered and better separated along the two linear discriminant axes
- Fewer support vectors are needed because the decision boundaries are cleaner
- LD1 captures most of the between-class variation, while LD2 provides additional discrimination
- This confirms LDA's advantage over PCA for classification tasks — by using class label information, LDA finds projections that maximize class separability
