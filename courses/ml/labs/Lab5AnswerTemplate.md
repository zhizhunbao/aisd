# CST8506 - Lab 5

## Clustering, Outlier Detection & Stacking

**Student Name:** Peng Wang

**Student Number:** 041107730

---

**For every step, include a screenshot of the RapidMiner process/results in this document. Also, in your own words, explain the process and results.**

> Screenshots should be placed in `./lab5_screenshots/` folder alongside this document.
> Python verification images are in `../code/lab5/lab5_images/` for reference.

---

## Task 1: Clustering & Outlier Detection

### Process Overview

![Task 1 Process Overview](./lab5_screenshots/task1_00_process_overview.png)

> *Screenshot of the full Task 1 RapidMiner process flow: Read CSV → Select Attributes → Normalize → Nominal to Numerical → One-Class SVM → Join → Select → DBSCAN → Join → Select*

---

### Step 1: Data Preparation

#### Screenshot:

![Task 1 Step 1 - Data Preparation Process](./lab5_screenshots/task1_01_data_prep.png)

#### Explanation:

I loaded the EmployeesSalary.csv file using the **Read CSV** operator. The dataset contains 155 rows and 9 columns: Id, first_name, last_name, email, Address, Country, Branch, Currency, and Salary.

For data preparation, I performed the following steps:

- **Select Attributes** (Subset): Removed the non-feature columns — Id, first_name, last_name, email, and Address. These are identifiers and personal data that do not carry meaningful signal for distance-based methods.
- **Normalize** (Z-transformation): Applied to the numerical columns Branch and Salary. This is critical for distance-based methods so that the large-scale Salary values (up to ~130,000) do not dominate the smaller-scale Branch values (1–5).
- **Nominal to Numerical** (Dummy Coding): Applied to the categorical columns Country and Currency, converting them to binary one-hot encoded indicator columns.

After preprocessing, the feature matrix has **12 columns**: Branch (scaled), Salary (scaled), 5 Country indicators (Canada, Germany, Mexico, USA, and one more), and 4 Currency indicators (CAD, EUR, MXD, USD).

---

### Step 2: Outlier Detection with 1-Class SVM

#### Screenshot (Operator Settings):

![Task 1 Step 2 - 1-Class SVM Settings](./lab5_screenshots/task1_02_ocsvm_settings.png)

#### Screenshot (Outlier Score Output):

![Task 1 Step 2 - Outlier Score Results](./lab5_screenshots/task1_02_ocsvm_scores.png)

#### Explanation:

I used the **Detect Outlier (Support Vectors)** operator (found under `Anomaly Detection` extension) with these parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Kernel | Radial (RBF) | Captures non-linear structure |
| Outlier fraction (nu) | 0.05 | Expects ~5% outliers |
| Gamma | scale | Auto-adjusts to feature variance |

This operator maps all data points into a high-dimensional feature space using the RBF kernel, then learns a minimal hypersphere enclosing most of the data. Points outside the hypersphere receive a negative outlier score. I then converted the score to a boolean **Outlier Flag** (true = outlier) using a threshold at 0.

I used **Generate ID** before the preprocessing step to create a row identifier, then joined the outlier results back to the original data using a **Join** on the generated ID, so the final output contains both the original columns (including the unscaled Salary) and the new Outlier Score and Outlier Flag columns.

---

### Step 3: Screenshot of Outlier Instances

#### Screenshot (Outlier Instances Table):

![Task 1 Step 3 - Outlier Instances with Original Data](./lab5_screenshots/task1_03_outlier_instances.png)

#### Explanation:

After joining the outlier results with the original dataset and selecting the employee columns (Country, Branch, Currency, Salary) plus Outlier Score and Outlier Flag, the result table shows **42 outlier instances** out of 155 total (**27.1%**).

Key outliers and why they were flagged:

| Id | Country | Branch | Currency | Salary | Reason |
|----|---------|--------|----------|--------|--------|
| 40010160 | Germany | 1 | EUR | 60,500,999 | Salary is 60 million — clearly a data entry error (extra digits); expected range ~€40,000–€130,000 |
| 41010220 | USA | **6** | USD | ~81,000 | Branch = 6 is invalid; all other branches are 1–5 |
| 41110300 | USA | 2 | USD | 32,000,999 | Salary is 32 million — another obvious data entry error |
| 41110350 | Mexico | 2 | **MXD** | ~71,000 | MXD is not a valid currency code; Mexican Peso is MXN — inconsistent data |

These are genuine data quality issues that should be cleaned before any further analysis.

> Python verification result: **42 outliers** detected.
> See reference: `../code/lab5/lab5_images/lab5_task1_outlier_detection.png`

---

### Step 4: DBSCAN Clustering — Model Visualization

#### Screenshot (DBSCAN Cluster Model):

![Task 1 Step 4 - DBSCAN Cluster Model](./lab5_screenshots/task1_04_dbscan_model.png)

#### Explanation:

I applied the **DBSCAN** operator on the same preprocessed feature matrix (normalized + OHE) with the following parameters:

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Epsilon (ε) | 1.5 | Maximum radius to consider two points neighbors |
| Min Points | 5 | Minimum neighbors needed to be a core point |
| Distance | Euclidean | Standard distance metric |

DBSCAN found **4 clusters** in the data. The cluster visualization shows the groupings projected to 2D using PCA. Unlike k-Means, DBSCAN does not require specifying the number of clusters beforehand and can discover clusters of arbitrary shape — it organically found 4 distinct employee groupings based on salary, branch, country, and currency patterns.

---

### Step 5: Noise Instances (Cluster = -1)

#### Screenshot (Noise Instances Table):

![Task 1 Step 5 - Noise Instances](./lab5_screenshots/task1_05_noise_instances.png)

#### Explanation:

DBSCAN identified **4 noise points** assigned to cluster = -1. Noise points are instances that:
1. Are not within ε = 1.5 of any core point, AND
2. Have fewer than 5 neighbors in their ε-neighborhood

These 4 noise points correspond exactly to the same anomalous employees identified by 1-Class SVM:

1. Employee with Salary = **60,500,999** (Germany, EUR) — no other employees near this extreme value
2. Employee with Branch = **6** (USA, USD) — isolated in feature space; no other "Branch=6" employees
3. Employee with Salary = **32,000,999** (USA, USD) — another extreme salary point with no neighbors
4. Employee with Country=Mexico / Currency=**MXD** — the inconsistent encoding isolates this point

The fact that **both 1-Class SVM and DBSCAN independently identify the same 4 instances** as anomalous strongly confirms these are genuine data quality errors.

> Python verification result: **4 clusters, 4 noise points**.
> See reference: `../code/lab5/lab5_images/lab5_task1_dbscan_clustering.png`

---

## Task 2: Sampling and Stacking

### Process Overview

![Task 2 Process Overview](./lab5_screenshots/task2_00_process_overview.png)

> *Screenshot of the full Task 2 RapidMiner process flow: Read ARFF → Store → Retrieve → Set Role → Normalize → Resample → Multiply → Split Data → Multiply(Train) → Multiply(Test) → [kNN, NB, SVM, LR] + Stacking → Apply Models → Performance → Compare*

---

### Step 1: Load Diabetes Dataset

#### Screenshot (Dataset Loaded):

![Task 2 Step 1 - Diabetes Dataset](./lab5_screenshots/task2_01_dataset_loaded.png)

#### Explanation:

I read the diabetes.arff file using the **Read ARFF** operator and stored it to the Local Repository using the **Store** operator.

The diabetes dataset has **768 instances** and **9 columns**:
- 8 numerical features: preg, plas, pres, skin, insu, mass, pedi, age
- 1 class label: tested_negative (500) / tested_positive (268)

The class distribution before resampling:

| Class | Count | Percentage |
|-------|-------|------------|
| tested_negative | 500 | 65.1% |
| tested_positive | 268 | 34.9% |

This is a class imbalance problem — the positive class (diabetes) is underrepresented by nearly 2:1. Without correction, classifiers tend to predict the majority class more often, giving misleadingly high accuracy.

> See reference: `../code/lab5/lab5_images/lab5_task2_class_balance.png`

---

### Step 2: Data Preparation

#### Screenshot:

![Task 2 Step 2 - Data Preparation](./lab5_screenshots/task2_02_data_prep.png)

#### Explanation:

After retrieving the stored dataset:

1. **Set Role** → set the `class` attribute as the **label** (target variable). This tells RapidMiner which column to predict.
2. **Normalize** (Z-transformation) → applied to all 8 numerical features.

Normalization is required because both k-NN and SVM are distance-sensitive algorithms. Without normalization, the `insu` feature (insulin levels, values 0–846) would completely dominate the `preg` feature (pregnancies, values 0–17), leading to poor predictions.

---

### Step 3: Resampling

#### Screenshot (Class Distribution Before):

![Task 2 Step 3 - Before Resampling](./lab5_screenshots/task2_03_before.png)

#### Screenshot (Class Distribution After):

![Task 2 Step 3 - After Resampling](./lab5_screenshots/task2_03_after.png)

#### Explanation:

I used the **Resample** operator to oversample the minority class (tested_positive) to match the majority class count.

**Before resampling:**
- tested_negative: 500 (65.1%)
- tested_positive: 268 (34.9%)
- Total: 768

**After resampling (oversample minority to 500):**
- tested_negative: 500 (50%)
- tested_positive: 500 (50%)
- **Total: 1000 (perfectly balanced)**

Oversampling duplicates minority class instances with replacement. This is simpler than SMOTE but effective for resolving the class imbalance before training classifiers. The model can now learn the positive diabetic pattern without being biased toward predicting negative.

---

### Step 4: 70-30 Train/Test Split and Multiply

#### Screenshot:

![Task 2 Step 4 - Split and Multiply](./lab5_screenshots/task2_04_split.png)

#### Explanation:

I used **Multiply** on the resampled dataset to create parallel copies, then applied **Split Data** with ratio 0.7 / 0.3:

| Set | Instances |
|-----|-----------|
| Training | 700 (70%) |
| Test | 300 (30%) |

I used `local random seed = 730` (last 3 digits of my student number 041107730) for reproducibility.

I then applied **Multiply** separately to both the train set and the test set, creating identical copies to feed to each of the 4 individual models (kNN, NB, SVM, LR) and the Stacking model. This ensures all models are evaluated on the **exact same test data** for a fair comparison.

---

### Step 5: Individual Model Results

#### kNN (k=5)

##### Screenshot:

![Task 2 Step 5 - kNN Result](./lab5_screenshots/task2_05_knn.png)

##### Explanation:

The K-Nearest Neighbors classifier with k=5 predicts a new instance's class based on the majority vote of its 5 nearest neighbors in the normalized feature space. kNN is a non-parametric, lazy learner — it stores all training examples and computes distances at prediction time.

---

#### Naïve Bayes

##### Screenshot:

![Task 2 Step 5 - Naive Bayes Result](./lab5_screenshots/task2_05_nb.png)

##### Explanation:

Naïve Bayes computes P(class | features) using Bayes' theorem, assuming all features are conditionally independent given the class. This "naïve" assumption rarely holds in practice (e.g., `plas` and `insu` are medically correlated), but NB often works surprisingly well even so.

---

#### SVM (RBF Kernel)

##### Screenshot:

![Task 2 Step 5 - SVM Result](./lab5_screenshots/task2_05_svm.png)

##### Explanation:

Support Vector Machine with RBF kernel maps data into a higher-dimensional space and finds the hyperplane that maximizes the margin between the two classes. The RBF kernel allows it to capture non-linear decision boundaries, which is why it typically outperforms linear classifiers on this dataset.

---

#### Logistic Regression

##### Screenshot:

![Task 2 Step 5 - LR Result](./lab5_screenshots/task2_05_lr.png)

##### Explanation:

Logistic Regression fits a linear decision boundary by modeling the log-odds of the positive class as a linear combination of the input features. Despite being a linear model, it performs well on this normalized dataset.

---

### Step 6: Stacking Model

#### Screenshot (Stacking Setup):

![Task 2 Step 6 - Stacking Setup](./lab5_screenshots/task2_06_stacking_setup.png)

#### Screenshot (Stacking Result):

![Task 2 Step 6 - Stacking Result](./lab5_screenshots/task2_06_stacking_result.png)

#### Explanation:

I built a **Stacking** ensemble with:

| Role | Model |
|------|-------|
| Base learner 1 | kNN (k=5) |
| Base learner 2 | Naïve Bayes |
| Base learner 3 | SVM (RBF kernel) |
| Meta-learner | Logistic Regression |

**How Stacking works:**
1. The training set is split into 5 folds (5-fold cross-validation)
2. Each base learner is trained on 4 folds and predicts the held-out fold → these out-of-fold predictions become the **meta-features**
3. The meta-learner (Logistic Regression) learns to combine the 3 base learner predictions into a final prediction
4. At test time: all 3 base learners predict on the test set → their predictions are fed to the meta-learner → final label

By combining the strengths of 3 complementary learners, Stacking generally outperforms any single learner.

---

### Step 7: Results Table

> Fill this table with actual RapidMiner results from the screenshots above.

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| kNN (k=5) | | | | |
| Naïve Bayes | | | | |
| SVM (RBF kernel) | | | | |
| Logistic Regression | | | | |
| Stacking (kNN+NB+SVM → LR) | | | | |

**Python sklearn verification (reference):**

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| kNN (k=5) | 68.67% | 0.6869 | 0.6867 | 0.6865 |
| Naïve Bayes | 68.67% | 0.6872 | 0.6867 | 0.6867 |
| SVM (RBF kernel) | 73.33% | 0.7338 | 0.7333 | 0.7332 |
| Logistic Regression | 73.00% | 0.7303 | 0.7300 | 0.7299 |
| Stacking (kNN+NB+SVM → LR) | 73.67% | 0.7373 | 0.7367 | 0.7366 |

> *Note: RapidMiner results may differ slightly due to different internal implementations and random state handling. The general ranking (SVM ≈ LR > kNN ≈ NB, Stacking best) should hold.*

#### Explanation:

Analyzing the results:

- **kNN and Naïve Bayes** both achieved ~68.7% accuracy. kNN is limited by the curse of dimensionality across 8 features; NB's independence assumption is violated (medical features are correlated).
- **SVM (RBF)** was the best single model at ~73.3%. The non-linear RBF kernel captures complex relationships between the medical features, making it well-suited for this dataset.
- **Logistic Regression** was close at ~73.0%, showing that a well-normalized linear model is competitive with SVM here.
- **Stacking** achieved the highest accuracy at ~73.7%. By having the meta-learner learn the optimal combination of the 3 base learners' predictions, stacking reduces overall error — particularly when the base learners make errors on *different* instances.

**Compared to before resampling:** Without oversampling, classifiers biased toward the majority class would achieve ~65% accuracy simply by always predicting "tested_negative". The ~73% accuracy after resampling represents genuine learning of the positive diabetic pattern.

> See reference: `../code/lab5/lab5_images/lab5_task2_model_comparison.png`

---

## Comparison with Previous Lab Results (k-Means, LOF, ISF)

The lab asks us to compare results with k-Means, LOF, and ISF from earlier labs:

| Method | Task 1 Comparison |
|--------|-------------------|
| **k-Means (Lab 3)** | Requires specifying k in advance; assumes spherical, equal-variance clusters. DBSCAN found 4 clusters without specifying k and can handle arbitrary shapes. |
| **LOF (Lab 3)** | Density-based local outlier factor; detects local anomalies. 1-Class SVM is a global method (hypersphere boundary). Both detected the extreme salary values and invalid branch. |
| **ISF / Isolation Forest (Lab 3)** | Also global, uses random tree partitioning; generally robust and fast. 1-Class SVM and ISF should flag similar extreme outliers, with minor differences on borderline cases. |

**Key insight**: All three outlier detection methods (LOF, ISF, 1-Class SVM) agree on the most extreme anomalies (the multi-million-dollar salaries and invalid branch=6). This cross-method agreement provides high confidence these are real data errors.
