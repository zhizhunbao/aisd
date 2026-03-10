# Lab 5 — RapidMiner Build Guide

## CST8506 — Clustering, Outlier Detection & Stacking

**Student:** Peng Wang | **Student Number:** 041107730

> This guide walks through building both Task 1 and Task 2 processes in RapidMiner Studio, operator by operator.
> Reference Python results are in `courses/ml/code/lab5/lab5_images/`.

---

## Prerequisites

- RapidMiner Studio installed (version 9.x or 10.x)
- **Anomaly Detection Extension** installed (for One-Class SVM operator)
  - Go to: `Help > Marketplace > Search "Anomaly Detection"` → Install → Restart
- Files in RapidMiner working directory or accessible path:
  - `EmployeesSalary.csv`
  - `diabetes.arff` (from Weka data folder, typically `C:\Program Files\Weka-3-8\data\diabetes.arff`)

---

## Task 1: Clustering & Outlier Detection

### Final Process Flow

```
Read CSV ──► Generate ID ──► Multiply ──────────────────────────────────────────► Join ──► Select Attributes ──► DBSCAN ──► Join ──► Select Attributes
                                │                                                    ▲                                       ▲
                                └──► Select Attributes ──► Normalize ──► Nominal to Numerical ──► Detect Outlier (SVM) ──┘
                                                                                                                   [outlier score/flag]
```

> **Simplified version**: You can also run outlier detection first, then DBSCAN as two sequential steps on the same preprocessed data, joined back to original each time.

---

### Build Steps

---

#### STEP 0 — New Process

1. Open RapidMiner Studio
2. `File > New Process`
3. Name it: `Lab5_Task1_Outlier_Clustering`

---

#### STEP 1 — Read CSV (Load EmployeesSalary)

| Field | Value |
|-------|-------|
| Operator | **Read CSV** |
| Location | `Import > Read CSV` (or search "Read CSV" in operator panel) |

**How to configure:**
1. Drag **Read CSV** onto the canvas
2. In the Parameters panel → click **Import Configuration Wizard**
3. Navigate to and select `EmployeesSalary.csv`
4. Set: Separator = `,`, First Row = Column Names = ✓
5. Click **Next** through all steps → **Finish**
6. Verify 9 columns detected: Id, first_name, last_name, email, Address, Country, Branch, Currency, Salary

**Screenshot to take:** Parameters panel showing file path + the result tab showing 155 rows.

---

#### STEP 2 — Generate ID (Add Row Number for Join)

| Field | Value |
|-------|-------|
| Operator | **Generate ID** |
| Location | `Data Transformation > Generation > Generate ID` |

**How to configure:**
1. Drag **Generate ID** after Read CSV
2. Connect: Read CSV `exa out` → Generate ID `exa in`
3. Parameters: `id attribute name = row_id`, `create nominal id = false` (leave default)

> This adds a numeric `row_id` column so we can join the outlier results back to the original data later.

---

#### STEP 3 — Multiply (Split into Two Branches)

| Field | Value |
|-------|-------|
| Operator | **Multiply** |
| Location | `Utility > Multiply` |

**How to configure:**
1. Drag **Multiply** after Generate ID
2. Connect: Generate ID `exa out` → Multiply `exa in`
3. Multiply has two output ports: `out1` and `out2`
   - `out1` → goes to preprocessing pipeline (→ Step 4)
   - `out2` → kept as original data (→ Step 8, the first Join)

---

#### STEP 4 — Select Attributes (Remove Non-Feature Columns)

| Field | Value |
|-------|-------|
| Operator | **Select Attributes** |
| Location | `Data Transformation > Attribute Set Reduction > Select Attributes` |

**How to configure:**
1. Drag **Select Attributes** after Multiply `out1`
2. Connect: Multiply `out1` → Select Attributes `exa in`
3. Parameters:
   - `attribute filter type` = **Subset**
   - Click **Select Attributes...** button
   - **Keep** (select these): `Country`, `Branch`, `Currency`, `Salary`, `row_id`
   - **Remove** (deselect): `Id`, `first_name`, `last_name`, `email`, `Address`
4. Click OK

> Keep `row_id` so we can join later. Keep `Salary` as the numerical feature (will be scaled).

---

#### STEP 5 — Normalize (Z-Score Scaling for Numerical Columns)

| Field | Value |
|-------|-------|
| Operator | **Normalize** |
| Location | `Data Transformation > Normalization > Normalize` |

**How to configure:**
1. Drag **Normalize** after Select Attributes
2. Connect: Select Attributes `exa out` → Normalize `exa in`
3. Parameters:
   - `method` = **Z-transformation**
   - `attribute filter type` = **Subset** → select `Branch` and `Salary` only
   - Do NOT normalize `Country`, `Currency`, or `row_id`

> Normalization applies to continuous numerical features only. Categorical columns will be handled in the next step.

---

#### STEP 6 — Nominal to Numerical (One-Hot Encode Categorical Columns)

| Field | Value |
|-------|-------|
| Operator | **Nominal to Numerical** |
| Location | `Data Transformation > Type Conversion > Nominal to Numerical` |

**How to configure:**
1. Drag **Nominal to Numerical** after Normalize
2. Connect: Normalize `exa out` → Nominal to Numerical `exa in`
3. Parameters:
   - `attribute filter type` = **Subset** → select `Country` and `Currency` only
   - `coding type` = **Dummy Coding** (= one-hot encoding, N-1 binary columns per nominal attribute)

> After this step, Country and Currency become binary indicator columns (e.g., Country_Canada, Country_Germany, etc.)

---

#### STEP 7 — Detect Outlier (Support Vectors) — One-Class SVM

| Field | Value |
|-------|-------|
| Operator | **Detect Outlier (Support Vectors)** |
| Location | `Anomaly Detection > Detect Outlier (Support Vectors)` (requires extension) |

**How to configure:**
1. Drag **Detect Outlier (Support Vectors)** after Nominal to Numerical
2. Connect: Nominal to Numerical `exa out` → Detect Outlier `exa in`
3. Parameters:

| Parameter | Value | Notes |
|-----------|-------|-------|
| kernel | **Radial** (= RBF) | Captures non-linear structure |
| outlier fraction | **0.05** | Expect ~5% of data to be outliers |
| output label | true | Adds `outlier` boolean attribute |

4. Connect: Detect Outlier `exa out` → Join (Step 8, left port)

> The operator adds an `outlier` attribute (true/false) and `anomaly_score` to each instance.

**Screenshot to take:** Operator parameters panel. Show kernel = Radial, outlier fraction = 0.05.

---

#### STEP 8 — Join (Outlier Results + Original Data)

| Field | Value |
|-------|-------|
| Operator | **Join** |
| Location | `Data Transformation > Join > Join` |

**How to configure:**
1. Drag **Join** onto canvas
2. Connect:
   - Detect Outlier `exa out` → Join `left` port
   - Multiply `out2` (original data) → Join `right` port
3. Parameters:
   - `join type` = **Inner Join**
   - `key attributes` = `row_id` (select same attribute from both sides)
   - Check: remove key attributes from result = no (keep row_id)

---

#### STEP 9 — Select Attributes (Keep Original Columns + Outlier Info)

| Field | Value |
|-------|-------|
| Operator | **Select Attributes** |
| Location | Same as Step 4 |

**How to configure:**
1. Drag **Select Attributes** after Step 8 Join
2. Connect: Join `joi out` → Select Attributes `exa in`
3. Parameters: Keep only:
   - `Id` (original employee columns)
   - `first_name`, `last_name`
   - `Country`, `Branch`, `Currency`, `Salary` (original, unscaled)
   - `anomaly_score` (outlier score)
   - `outlier` (boolean flag)
   - Remove duplicate columns from the join (e.g., `_right` suffixed columns if any)

**Screenshot to take:** The result table filtered to show only outlier = true rows. Use **Filter** in the results view: click the filter icon, set `outlier = true`.

This is the **Step 3 screenshot** required by the lab (outlier instances with all employee info + score + flag).

---

#### STEP 10 — DBSCAN Clustering

| Field | Value |
|-------|-------|
| Operator | **DBSCAN** |
| Location | `Modeling > Segmentation > DBSCAN` |

**How to configure:**
1. Drag **DBSCAN** onto canvas
2. Connect: Nominal to Numerical `exa out` (same preprocessed data) → DBSCAN `exa in`
   - OR: Add another **Multiply** at the preprocessing output to reuse it
3. Parameters:

| Parameter | Value | Notes |
|-----------|-------|-------|
| epsilon | **1.5** | Neighborhood radius |
| min_points | **5** | Minimum neighbors for core point |
| measure_types | **Mixed Measures** or **Numerical Measures** | Select appropriate |
| numerical_measure | **Euclidean Distance** | Standard distance |

4. DBSCAN has two output ports:
   - `clu out` (cluster model) → connect to Result port for **cluster model visualization screenshot**
   - `exa out` (data with cluster label) → connect to Join (Step 11)

**Screenshot to take:** The cluster model output — this is the **Step 4 screenshot** (DBSCAN model visualization).

---

#### STEP 11 — Join (Cluster Results + Original Data)

Same as Step 8. Join the DBSCAN output (with cluster label) back to original data on `row_id`.

**How to configure:** Same as Step 8 — join DBSCAN `exa out` with original data on `row_id`.

---

#### STEP 12 — Select Attributes + Filter Noise

1. **Select Attributes**: Keep original employee columns + `cluster` attribute
2. Connect result to output

**Screenshot to take:** Filter the result to show only `cluster = -1` (noise instances). Use the filter icon in results view. This is the **Step 5 screenshot** (noise instances).

---

### Task 1 — Screenshots Checklist

| # | Screenshot | What to Capture |
|---|-----------|-----------------|
| ✅ | `task1_00_process_overview.png` | Full canvas/process view |
| ✅ | `task1_01_data_prep.png` | Preprocessing operators and settings |
| ✅ | `task1_02_ocsvm_settings.png` | Detect Outlier parameters (kernel=Radial, nu=0.05) |
| ✅ | `task1_02_ocsvm_scores.png` | Result view showing outlier score + flag columns |
| ✅ | `task1_03_outlier_instances.png` | Result filtered to outlier=true, showing original columns + score + flag |
| ✅ | `task1_04_dbscan_model.png` | DBSCAN cluster visualization model output |
| ✅ | `task1_05_noise_instances.png` | Result filtered to cluster=-1 |

---

## Task 2: Sampling and Stacking

### Final Process Flow

```
Read ARFF ──► Store
                └──► [new process] ──► Retrieve ──► Set Role ──► Normalize ──► Resample ──► Multiply ──► Split Data
                                                                                                                ├── train ──► Multiply ──► [kNN, NB, SVM, LR] ──► Apply Model ──► Performance ──► Compare
                                                                                                                │                └──► Stacking ──► Apply Model ──► Performance ──────────────────────────────┤
                                                                                                                └── test ──► Multiply ──► [feed to all Apply Models above]
```

---

### Build Steps

---

#### STEP 0 — New Process

1. `File > New Process`
2. Name it: `Lab5_Task2_Sampling_Stacking`

---

#### STEP 1 — Read ARFF

| Field | Value |
|-------|-------|
| Operator | **Read ARFF** |
| Location | `Import > Read ARFF` |

**How to configure:**
1. Drag **Read ARFF** onto canvas
2. Parameters → click folder icon next to `filename`
3. Navigate to `diabetes.arff`
   - Default Weka location: `C:\Program Files\Weka-3-8\data\diabetes.arff`
   - Or wherever you saved it
4. Run to preview: verify 768 rows, 9 columns, `class` column present

---

#### STEP 2 — Store to Local Repository

| Field | Value |
|-------|-------|
| Operator | **Store** |
| Location | `Repository > Store` |

**How to configure:**
1. Drag **Store** after Read ARFF
2. Connect: Read ARFF `out` → Store `exa in`
3. Parameters → click folder icon → save to: `/data/diabetes` (in Local Repository)
4. Run the process (Ctrl+R) to save the data

> After running, the diabetes data is stored in your Local Repository.

---

#### STEP 3 — Retrieve

| Field | Value |
|-------|-------|
| Operator | **Retrieve** |
| Location | `Repository > Retrieve` |

**How to configure:**
1. Drag **Retrieve** onto canvas (can be in same or new process)
2. Parameters → click folder icon → navigate to `/data/diabetes`
3. Connect to Set Role (Step 4)

---

#### STEP 4 — Set Role (Define Label Column)

| Field | Value |
|-------|-------|
| Operator | **Set Role** |
| Location | `Data Transformation > Attribute > Set Role` |

**How to configure:**
1. Drag **Set Role** after Retrieve
2. Connect: Retrieve `out` → Set Role `exa in`
3. Parameters:
   - `attribute name` = **class**
   - `target role` = **label**

---

#### STEP 5 — Normalize

| Field | Value |
|-------|-------|
| Operator | **Normalize** |
| Location | `Data Transformation > Normalization > Normalize` |

**How to configure:**
1. Drag **Normalize** after Set Role
2. Connect: Set Role `exa out` → Normalize `exa in`
3. Parameters:
   - `method` = **Z-transformation**
   - `attribute filter type` = **All** (applies to all numerical, skips label automatically)

---

#### STEP 6 — Resample (Oversample Minority Class)

| Field | Value |
|-------|-------|
| Operator | **Sample (Bootstrapping)** or **Resample** |
| Location | `Data Transformation > Sampling > Sample (Bootstrapping)` |

**How to configure option A (Bootstrapping/Resample):**
1. Drag **Sample (Bootstrapping)** after Normalize
2. Connect: Normalize `exa out` → Resample `exa in`
3. Parameters:
   - `sample size` = **1000**
   - `balance classes` = **true** (enables equal sampling per class)
   - `local random seed` = **730**

**Alternative approach if balance option not available:**
Use **Filter Examples** to separate the two classes, then use **Sample** individually on the minority class, then **Append** to combine.

> Target result: 1000 total instances, 500 tested_negative + 500 tested_positive.

**Screenshot to take:** Result view showing class distribution → 500/500.

---

#### STEP 7 — Multiply

| Field | Value |
|-------|-------|
| Operator | **Multiply** |
| Location | `Utility > Multiply` |

**How to configure:**
1. Drag **Multiply** after Resample
2. You may need multiple output ports — right-click Multiply → "Add output port" to get enough ports (need at least 2)
3. Connect to Split Data (Step 8)

---

#### STEP 8 — Split Data (70/30)

| Field | Value |
|-------|-------|
| Operator | **Split Data** |
| Location | `Data Transformation > Sampling > Split Data` |

**How to configure:**
1. Drag **Split Data** after Multiply
2. Connect: Multiply `out1` → Split Data `exa in`
3. Parameters:
   - Click **Add Partition** button → set splits: `0.7` and `0.3`
   - `sampling type` = **stratified sampling** (maintains class ratio in both splits)
   - `local random seed` = **730**
4. Split Data output ports: `par1` (70% train) and `par2` (30% test)

---

#### STEP 9 — Multiply Train and Test Sets

1. Add **Multiply** after Split Data `par1` (train) — call it `Multiply_Train`
2. Add **Multiply** after Split Data `par2` (test) — call it `Multiply_Test`
3. Each needs enough output ports for 5 models (4 individual + 1 stacking)
   - Right-click each Multiply → Add output port until you have 5 outputs

---

#### STEP 10 — Individual Models

For each model, you need:
1. A model operator → **Apply Model** → **Performance (Classification)**

Repeat for each model below:

---

##### Model 1: kNN

| Field | Value |
|-------|-------|
| Operator | **K-Nearest Neighbors** or **k-NN** |
| Location | `Modeling > Predictive > Lazy > k-NN` |

**Parameters:**
- `k` = **5**
- `weighted vote` = false
- `measure_types` = Mixed Measures → Euclidean Distance

**Connect:**
- Multiply_Train `out1` → k-NN `tra in`
- k-NN `mod out` → Apply Model `mod in`
- Multiply_Test `out1` → Apply Model `unl in`
- Apply Model `lab out` → Performance `tst in`

---

##### Model 2: Naïve Bayes

| Field | Value |
|-------|-------|
| Operator | **Naive Bayes** |
| Location | `Modeling > Predictive > Bayesian > Naive Bayes` |

**Parameters:** Default (no changes needed)

**Connect:** Same pattern as kNN, using `out2` of Multiply_Train and Multiply_Test.

---

##### Model 3: SVM

| Field | Value |
|-------|-------|
| Operator | **Support Vector Machine (Libsvm)** or **SVM** |
| Location | `Modeling > Predictive > Support Vector Machine > Support Vector Machine (libsvm)` |

**Parameters:**
- `kernel_type` = **Radial** (RBF)
- `C` = 1.0 (default)
- `gamma` = 0.0 (= scale, RapidMiner auto-computes)

**Connect:** Same pattern, using `out3` of Multiply_Train and Multiply_Test.

---

##### Model 4: Logistic Regression

| Field | Value |
|-------|-------|
| Operator | **Logistic Regression** |
| Location | `Modeling > Predictive > Logistic Regression` |

**Parameters:** Default (max iterations = 100 or increase to 1000 if convergence issues)

**Connect:** Same pattern, using `out4` of Multiply_Train and Multiply_Test.

---

#### STEP 11 — Stacking Classifier

| Field | Value |
|-------|-------|
| Operator | **Stacking** |
| Location | `Modeling > Ensembles > Stacking` |

**How to configure:**
1. Drag **Stacking** onto canvas
2. Connect:
   - Multiply_Train `out5` → Stacking `tra in`
   - Multiply_Test `out5` → Apply Model `unl in`
3. Double-click **Stacking** to open the subprocess
4. Inside the subprocess, you will see sub-processes for base learners:
   - Add **k-NN** (k=5) as base learner 1
   - Add **Naive Bayes** as base learner 2
   - Add **Support Vector Machine (Libsvm)** (RBF) as base learner 3
5. Back in the main Stacking parameters:
   - `stack_type` = **Classifier Stacking**
   - `meta_learner` = **Logistic Regression**
   - `number of folds` = **5**

**Connect stacking result to Performance:**
- Stacking `mod out` → Apply Model `mod in`
- Multiply_Test `out5` → Apply Model `unl in`
- Apply Model `lab out` → Performance `tst in`

**Screenshot to take:** Stacking operator configuration showing the 3 base learners and meta-learner Logistic Regression.

---

#### STEP 12 — Performance (Classification) for Each Model

| Field | Value |
|-------|-------|
| Operator | **Performance (Classification)** |
| Location | `Evaluation > Performance > Performance (Classification)` |

**How to configure (applies to all 5 Performance operators):**
1. Connect `Apply Model lab out` → `Performance tst in`
2. Parameters: Check all boxes:
   - ✅ `accuracy`
   - ✅ `precision` (class: tested_positive)
   - ✅ `recall` (class: tested_positive)
   - ✅ `f_measure` (class: tested_positive)
   - ✅ `confusion matrix`
3. Connect Performance `per out` → Result port (or a **Compare ROCs** / **Log** operator)

---

#### STEP 13 — Screenshot Results

For each of the 5 models, after running the process:
1. Click the Performance result in the Results panel
2. Screenshot the accuracy, precision, recall, f-measure values
3. Note them down in the Results Table (Step 7 of Answer Template)

---

### Task 2 — Screenshots Checklist

| # | Screenshot | What to Capture |
|---|-----------|-----------------|
| ✅ | `task2_00_process_overview.png` | Full process canvas |
| ✅ | `task2_01_dataset_loaded.png` | Diabetes data table (768 rows, class distribution) |
| ✅ | `task2_02_data_prep.png` | Set Role + Normalize operators with settings |
| ✅ | `task2_03_before.png` | Class distribution before resampling (500/268) |
| ✅ | `task2_03_after.png` | Class distribution after resampling (500/500) |
| ✅ | `task2_04_split.png` | Split Data parameters (0.7/0.3, seed=730) |
| ✅ | `task2_05_knn.png` | kNN Performance results |
| ✅ | `task2_05_nb.png` | Naive Bayes Performance results |
| ✅ | `task2_05_svm.png` | SVM Performance results |
| ✅ | `task2_05_lr.png` | Logistic Regression Performance results |
| ✅ | `task2_06_stacking_setup.png` | Stacking operator showing 3 base learners + LR meta |
| ✅ | `task2_06_stacking_result.png` | Stacking Performance results |

---

## Results Summary (from Python Verification)

Use these as reference when filling out the Answer Template. Actual RapidMiner results may vary slightly.

### Task 1

| Metric | Result |
|--------|--------|
| Total instances | 155 |
| Outliers (1-Class SVM) | **42** (27.1%) |
| DBSCAN clusters | **4** |
| DBSCAN noise points | **4** |

**4 noise instances (investigation priority):**

| Id | Country | Branch | Currency | Salary | Issue |
|----|---------|--------|----------|--------|-------|
| 40010160 | Germany | 1 | EUR | **60,500,999** | Salary data entry error (×1000 off) |
| 41010220 | USA | **6** | USD | ~81,000 | Invalid branch number |
| 41110300 | USA | 2 | USD | **32,000,999** | Salary data entry error (×1000 off) |
| 41110350 | Mexico | 2 | **MXD** | ~71,000 | Invalid currency code (should be MXN) |

### Task 2

| Model | Accuracy |
|-------|----------|
| kNN (k=5) | ~68.67% |
| Naïve Bayes | ~68.67% |
| SVM (RBF) | ~73.33% |
| Logistic Regression | ~73.00% |
| **Stacking (kNN+NB+SVM → LR)** | **~73.67%** |

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Detect Outlier (Support Vectors)" not found | Install Anomaly Detection extension via `Help > Marketplace` |
| DBSCAN gives only 1 cluster | Decrease epsilon (try 1.0 or 0.8) or decrease min_points (try 3) |
| Join produces extra `_right` columns | Add another Select Attributes after Join to remove duplicates |
| Stacking base learners not configurable | Double-click the Stacking operator to enter the subprocess |
| Performance shows NaN for precision/recall | Set `positive class` parameter in Performance to `tested_positive` |
| Resample doesn't balance classes | Try `Sample (Bootstrapping)` with balance=true, or manually oversample the minority class |
| SVM very slow | Reduce `C` parameter or use linear kernel first to test pipeline |

---

## Submission Checklist

Before submitting, verify:

- [ ] Task 1 `.rmp` file saved and tested (runs without errors)
- [ ] Task 2 `.rmp` file saved and tested (runs without errors)
- [ ] All screenshots taken and placed in `lab5_screenshots/` folder
- [ ] Answer Template (`Lab5AnswerTemplate.md`) filled with all screenshots and explanations
- [ ] Results table completed with actual RapidMiner numbers
- [ ] Student name and number correct at top of Answer Template
- [ ] All files submitted to Brightspace (`.rmp` + answer document, NOT zipped)
