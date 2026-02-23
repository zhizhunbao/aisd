# CST8506 - Lab 4: Time Series Analysis

**Due Date:** Check Brightspace for due dates.

## Introduction

The goal of this lab is to analyse temperature dataset – Australia using NN in Keras. All tasks should be performed using Keras and Python. (Refer to documentation: https://keras.io/api/layers/)

## Steps (all these steps should be done in Python):

### Part 1: Time Series with Neural Networks

1. Load the dataset (download from https://www.kaggle.com/datasets/paulbrabban/daily-minimum-temperatures-in-melbourne)
2. Convert the daily temperature data to weekly averages and print the first 5 instances.
3. Plot the weekly average temperature series.
4. Plot original, trend, seasonal, and residue of the series as subplots of a plot.
5. Generate train and test time series sequences (use the keras method discussed in class).
6. Normalize the data.
7. Build a sequential model with at least 2 dense layers and an output layer.
8. Compile and Fit the model (should fit the model with at least 20 epochs).
9. Predict for the test data.
10. Plot the original weekly data and the prediction for the test data (denormalize predictions). (Should use different colors for original data and predictions)
11. Build a sequential model with at least two simpleRNN, same number of Dense layers as before and an output layer. Add a dropout layer after every RNN layer.
12. Compile and fit the model and predict with the model (at least 20 epochs).
13. Plot the original weekly data and the prediction by both models for the test data (Should use different colors for original data and predictions)

### Part 2: Naive Bayes (Handwritten)

14. Create a Naïve Bayes model manually for the following dataset:

| ID | Height | Weight | Foot Size | Sex (Class) |
|----|--------|--------|-----------|-------------|
| 1  | 6      | 75     | 9         | M           |
| 2  | 5.92   | 80     | 9.5       | M           |
| 3  | 5.58   | 85     | 10        | M           |
| 4  | 5.92   | 90     | 11        | M           |
| 5  | 5.2    | 55     | 7         | F           |
| 6  | 5.5    | 60     | 8         | F           |
| 7  | 5.45   | 65     | 8.5       | F           |
| 8  | 5.6    | 70     | 9         | F           |

**All calculations should be handwritten on paper. For covariance matrix calculations, you can use excel.**

Using the created model, find the class of the person with the information:
- Height: (val = yourStudentNumber mod 10; if val <5, then 5+val, else val)
- Weight: (val = yourStudentNumber mod 100; if val <50, then 50+val, else val)
- FootSize: (val = lastdigit of student number, if val <5, then 5+val, else val)

Photos/scans of the handwritten work should be included in the answer document.

## Submission Requirements

1. You should be ready with your Python code and results.
2. Submit your answer document and notebook to Brightspace. The Lab will not be graded if any of these files are missing.
3. Files should not be zipped. Zipped files will not be graded.
