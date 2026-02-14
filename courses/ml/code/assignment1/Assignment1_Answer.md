---
title: "CST8506 Assignment 1: Wine Quality Classification"
author: "Peng Wang (041107730)"
date: "February 13, 2026"
subtitle: "CST8506 - Machine Learning"
---

# Step 1: Data Understanding - Load Wine Quality Dataset {#step-1}

## Code

![Step 1 Code](assignment1_images/assignment1_wine_quality_step01_code.png)

## Output

![Step 1 Output](assignment1_images/assignment1_wine_quality_step01_result.png)

## Explanation

I chose the Wine dataset because it has 178 samples with 13 chemical features and 3 wine types - perfect for testing dimensionality reduction.

---

# Step 2: Data Understanding - Dataset Statistics {#step-2}

## Code

![Step 2 Code](assignment1_images/assignment1_wine_quality_step02_code.png)

## Output

![Step 2 Output](assignment1_images/assignment1_wine_quality_step02_result.png)

## Explanation

I noticed the classes are fairly balanced and the feature scales differ a lot, so I'll need to standardize the data later.

---

# Step 3: Data Understanding - Missing Values & Data Types {#step-3}

## Code

![Step 3 Code](assignment1_images/assignment1_wine_quality_step03_code.png)

## Output

![Step 3 Output](assignment1_images/assignment1_wine_quality_step03_result.png)

## Explanation

Good news - no missing values, so I can skip data cleaning and move directly to preprocessing.

---

# Step 4: Data Preparation - Train/Test Split {#step-4}

## Code

![Step 4 Code](assignment1_images/assignment1_wine_quality_step04_code.png)

## Output

![Step 4 Output](assignment1_images/assignment1_wine_quality_step04_result.png)

## Explanation

I used stratified split to keep class proportions consistent between training and test sets.

---

# Step 5: Data Preparation - Standardize Data {#step-5}

## Code

![Step 5 Code](assignment1_images/assignment1_wine_quality_step05_code.png)

## Output

![Step 5 Output](assignment1_images/assignment1_wine_quality_step05_result.png)

## Explanation

I standardized the features so they're on the same scale - this helps algorithms like kNN and SVM work better.

---

# Step 6: Data Preparation - Apply PCA {#step-6}

## Code

![Step 6 Code](assignment1_images/assignment1_wine_quality_step06_code.png)

## Output

![Step 6 Output](assignment1_images/assignment1_wine_quality_step06_result.png)

## Explanation

I kept 10 PCA components to retain 95% of the variance - reducing dimensions while keeping most information.

---

# Step 7: Data Preparation - Apply LDA {#step-7}

## Code

![Step 7 Code](assignment1_images/assignment1_wine_quality_step07_code.png)

## Output

![Step 7 Output](assignment1_images/assignment1_wine_quality_step07_result.png)

## Explanation

LDA gave me only 2 components (since we have 3 classes), but it uses class labels to find the best separation.

---

# Step 8: Visualization - Scree Plots {#step-8}

## Code

![Step 8 Code](assignment1_images/assignment1_wine_quality_step08_code.png)

## Scree Plots

![Scree Plots](assignment1_images/scree_plots.png)

## Explanation

The scree plot helped me decide on 10 components - that's where we hit 95% cumulative variance.

---

# Step 9: Modeling - Define Classification Function {#step-9}

## Code

![Step 9 Code](assignment1_images/assignment1_wine_quality_step09_code.png)

## Explanation

I wrote this function to avoid repeating the same code 45 times for different classifier-parameter combinations.

---

# Step 10: Modeling & Evaluation - Run All Classifiers {#step-10}

## Code

![Step 10 Code](assignment1_images/assignment1_wine_quality_step10_code.png)

## Output

![Step 10 Output](assignment1_images/assignment1_wine_quality_step10_result.png)

## Explanation

I tested each classifier with different parameters to see which settings work best for each data representation.

---

# Step 11: Best Results Table {#step-11}

## Code

![Step 11 Code](assignment1_images/assignment1_wine_quality_step11_code.png)

## Output

![Step 11 Output](assignment1_images/assignment1_wine_quality_step11_result.png)

## Explanation

Standardized data got 100% accuracy. Surprisingly, LDA with just 2 components still hit 97%+ - impressive compression!

---

# Step 12: Detailed Results - All Parameters {#step-12}

## Code

![Step 12 Code](assignment1_images/assignment1_wine_quality_step12_code.png)

## Output

![Step 12 Output](assignment1_images/assignment1_wine_quality_step12_result.png)

## Explanation

kNN and SVM did well across the board. Simple models worked as good as complex ones - makes sense for a small clean dataset.

---

# Step 13: PCA 2D Visualization with Support Vectors {#step-13}

## Code

![Step 13 Code](assignment1_images/assignment1_wine_quality_step13_code.png)

## PCA 2D Visualization

![PCA 2D SVM](assignment1_images/pca_2d_svm.png)

## Explanation

In PCA space, the classes have some overlap. The support vectors appear right where the classes meet - that's where SVM draws its boundaries.

---

# Step 14: LDA 2D Visualization with Support Vectors {#step-14}

## Code

![Step 14 Code](assignment1_images/assignment1_wine_quality_step14_code.png)

## LDA 2D Visualization

![LDA 2D SVM](assignment1_images/lda_2d_svm.png)

## Explanation

LDA separates the classes much better than PCA - you can see the clusters are tighter and need fewer support vectors.
