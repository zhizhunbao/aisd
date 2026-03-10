# CST8506 - Lab 5: Clustering, Outlier Detection & Stacking

**Due Date:** Check Brightspace for due dates.

---

## Introduction

The goal of this lab is to:

- Find outliers in the **EmployeesSalary** file using **1-class SVM** and perform clustering using **DBSCAN**.
- Handle the imbalance in the **Diabetes dataset** (you have the arff file in Weka's data folder) using **resampling techniques** and compare the classification results before and after resampling.

All tasks should be performed using RapidMiner. Compare your results with the results that you got with kMeans, LOF and ISF earlier.

---

## Steps

> All these steps should be done in RapidMiner as one RMP file.

---

### Task 1: Clustering & Outlier Detection

You must have your process for this task as shown below:

> **Process Flow:** Read CSV → Data Preparation → 1-Class SVM (Outlier Detection) → Score to Flag → Join with Original → Select Columns → DBSCAN Clustering → Join with Original → Select Columns

#### Step 1: Data Preparation

For the data preparation, you must select relevant columns and do the required data preparation steps. Keep in mind that you will be using a **distance-based approach**, so your data should be prepared accordingly:

- Numerical attributes must be **scaled**
- Nominal attributes must be **one-hot encoded**

#### Step 2: Outlier Detection with 1-Class SVM

You must find outliers using the **1-class SVM approach**. This operator will give you an **outlier score**. You must:

1. Convert the score to a **flag** (outlier / not outlier)
2. Join the results with the original dataset
3. Select the original columns along with the result columns
4. When you select salary, make sure to select the **original salary**

#### Step 3: Screenshot of Outlier Instances

Take a screenshot of the outlier instances. It should have the format:

| Employee columns... | Outlier Score | Outlier Flag |
|---------------------|--------------|--------------|
| ...                 | ...          | true/false   |

#### Step 4: DBSCAN Clustering

Perform clustering using the **DBSCAN approach** and:

1. Join the results with the original data
2. Select relevant original columns along with the result columns

#### Step 5: Screenshots for Clustering

- Take a screenshot of the **model** (cluster visualization)
- Take a screenshot of the **noise instances** (cluster ID = -1)

---

### Task 2: Sampling and Stacking

You must have your process for this task as shown below:

> **Process Flow:** Read ARFF → Store → Retrieve → Set Role → Data Prep → Resample → Multiply → 70-30 Split → Multiply (Train & Test) → [kNN, NB, SVM, LR] → Apply Models → [Compare] → Stack (kNN+NB+SVM → LR) → Apply → Compare

#### Step 1: Load Dataset

Read the diabetes file (you have the arff file in Weka's data folder) and store it in RapidMiner's Data under **Local Repository**.

#### Step 2: Data Preparation

Retrieve the dataset, set the class column and perform any required data preparation steps. Make sure to prepare the dataset for **distance-based approaches**.

#### Step 3: Resampling

Perform **resampling** on the prepared data to resolve the class imbalance problem.

#### Step 4: Split and Multiply

After multiplying the dataset:

1. Apply a **70-30 split** to split the data into train and test data
2. Multiply both train and test sets
3. This ensures the same data is used for various modeling, and the test data is the same for all models

#### Step 5: Apply Individual Models

You must use the following models. Apply each model on the test set and get the results:

| Model | Type |
|-------|------|
| kNN | K-Nearest Neighbors |
| Naïve Bayes | Probabilistic classifier |
| SVM | Support Vector Machine |
| Logistic Regression | Linear classifier |

#### Step 6: Stacking

Create a **stacked model** with:

- **Base learners:** kNN, Naïve Bayes, SVM
- **Stacking model (meta-learner):** Logistic Regression

Apply the stacked model on the test set and get the results.

#### Step 7: Results Table

Tabulate all results in a table. This should be done manually.

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| kNN | | | | |
| Naïve Bayes | | | | |
| SVM | | | | |
| Logistic Regression | | | | |
| Stacking (kNN+NB+SVM → LR) | | | | |

---

## Submission Requirements

1. You should be ready with your RapidMiner process and results.
2. Submit your **`.rmp` file** AND the **answer document** to Brightspace. Missing any of these will result in 0 grade.
3. Don't zip — zipped files will **NOT** be graded.
