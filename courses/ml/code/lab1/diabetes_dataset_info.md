# Diabetes Dataset Information

## Overview

**Dataset Name:** Pima Indians Diabetes Database  
**Source:** National Institute of Diabetes and Digestive and Kidney Diseases  
**Instances:** 768  
**Features:** 8 numeric attributes  
**Target:** Binary classification (tested_positive, tested_negative)

## Purpose

Predict whether a patient has diabetes based on diagnostic measurements. All patients are females at least 21 years old of Pima Indian heritage.

## Feature Descriptions

| Column | Name | Description | Unit | Range |
|--------|------|-------------|------|-------|
| preg | Pregnancies | Number of times pregnant | count | 0-17 |
| plas | Plasma Glucose | Plasma glucose concentration (2 hours in oral glucose tolerance test) | mg/dL | 0-199 |
| pres | Blood Pressure | Diastolic blood pressure | mm Hg | 0-122 |
| skin | Skin Thickness | Triceps skin fold thickness | mm | 0-99 |
| insu | Insulin | 2-Hour serum insulin | mu U/ml | 0-846 |
| mass | BMI | Body mass index | kg/m² | 0-67.1 |
| pedi | Diabetes Pedigree | Diabetes pedigree function (genetic influence) | - | 0.078-2.42 |
| age | Age | Age of patient | years | 21-81 |
| class | Class | Diabetes test result | - | tested_positive / tested_negative |

## Feature Details

### preg (Pregnancies)
- Number of times the patient has been pregnant
- Higher pregnancy count may correlate with diabetes risk

### plas (Plasma Glucose)
- Blood sugar level measured 2 hours after glucose tolerance test
- Normal: < 140 mg/dL
- Prediabetes: 140-199 mg/dL
- Diabetes: ≥ 200 mg/dL

### pres (Blood Pressure)
- Diastolic blood pressure (lower number in BP reading)
- Normal: < 80 mm Hg
- Elevated: 80-89 mm Hg
- High: ≥ 90 mm Hg

### skin (Skin Thickness)
- Triceps skin fold thickness measurement
- Used to estimate body fat percentage
- Correlates with insulin resistance

### insu (Insulin)
- Serum insulin level 2 hours after glucose load
- Normal fasting: 2.6-24.9 mu U/ml
- Higher levels may indicate insulin resistance

### mass (BMI - Body Mass Index)
- Weight (kg) / Height (m)²
- Underweight: < 18.5
- Normal: 18.5-24.9
- Overweight: 25-29.9
- Obese: ≥ 30

### pedi (Diabetes Pedigree Function)
- Provides genetic influence on diabetes likelihood
- Considers diabetes history in relatives
- Higher values indicate stronger family history

### age (Age)
- Patient age in years
- Diabetes risk increases with age
- All patients are at least 21 years old

### class (Target Variable)
- **tested_positive:** Patient has diabetes
- **tested_negative:** Patient does not have diabetes

## Data Quality Notes

- Some features contain zero values which may represent missing data:
  - Glucose, blood pressure, skin thickness, insulin, and BMI should not be zero
  - Zero values may need special handling (imputation or removal)

- Class distribution:
  - Positive cases: ~35% (268 instances)
  - Negative cases: ~65% (500 instances)
  - Dataset is somewhat imbalanced

## Usage in PCA Lab

This dataset is used to demonstrate:
1. Dimensionality reduction from 8 features to fewer components
2. Variance preservation through principal components
3. Classification performance comparison before/after PCA
4. Visualization of data in reduced dimensions (2D and 3D)

## References

- Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). 
  Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. 
  Proceedings of the Symposium on Computer Applications and Medical Care (pp. 261-265). 
  IEEE Computer Society Press.

- UCI Machine Learning Repository: https://archive.ics.uci.edu/ml/datasets/diabetes
