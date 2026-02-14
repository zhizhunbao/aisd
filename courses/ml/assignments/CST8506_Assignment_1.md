## Page 1

CST8506 Assignment 1 
Due: Feb 13, 2026, at 11:59 PM Sharp!!! 
(Late submissions will not be accepted) 
 
Goal: The goal of this lab is to explore and analyze Wine Quality dataset from UCI Machine 
Learning Repository (https://archive.ics.uci.edu/dataset/186/wine+quality) and then reduce the 
dimensionality by applying PCA and LDA approaches, and perform classification using kNN, 
Random Forest, SVM, Logistic Regression and MLP. Compare the results before and after 
dimensionality reduction. You need to follow CRISP-DM for this assignment.  
Seeds dataset is tab-separated. When you download the file, if you have extra tabs in some rows, 
remove them manually or in python.  
There is no need to create a professional report for this assignment. Just like we do in labs, include 
code for each step and explain it (make sure to explain parameters too. Even if you are using 
default parameters, make sure to specify them and explain) in a word document. 
Data Understanding 
Thoroughly analyze your data to have a clear understanding of your data and their attributes and 
types. Perform all CRISP-DM steps of this phase.  
Data Preparation 
Perform all steps in Data Preparation phase of CRISP-DM while preparing your data. Make sure 
to include attribute names. Print basic stats like number of instances, number of attributes, first 
few instances etc. As part of data formatting, reduce the dimensionality by applying PCA and LDA 
techniques. Save both new dataframes separately (X_train_scaled, X_train_pca, X_train_lda, 
X_test_pca, X_test_lda etc.). 
Modeling & Evaluation 
As you will be performing the same task - classification - for different datasets using different 
methods, write a function that takes the datasets and methods as parameters. The results should be 
added accordingly to a data structure.  
You have 3 sets of data frames:  
1. Standardized Dataset 
2. After PCA 
3. After LDA 
For all three sets of data listed above, perform classification using the following methods (include 
three sets of parameters for each method): 
1. Random Forest 
2. MLP 
3. SVM  
4. Logistic Regression  
5. kNN 


---

## Page 2

Tabulate best results (Accuracy and F1 measure) for each dataset and each method one table 
(Make sure to include the best parameters also in the table – see the sample below).  
Method 
Parameters 
Standardized 
After PCA 
After LDA 
kNN 
 
 
 
 
RF 
 
 
 
 
SVM 
 
 
 
 
LR 
 
 
 
 
MLP 
 
 
 
 
 
 
 
 
 
 
 
 
Visualizations to be included:  
1. scree plot, cumulative scree plot 
2. After applying PCA, actual classes of the train set color coded by class and then in the 
second plot, support vectors should also be plotted, color coded by class (2 plots in parallel) 
3. After applying LDA, actual classes of the train set color coded by class and then in the 
second plot, support vectors should also be plotted, color coded by class (2 plots in parallel) 
 
Submission Details:  
Assignment should have a cover page, table of contents, figures etc. Upload the answer document 
and notebook to Brightspace (Don’t zip, zipped files will not be graded). There will be mark 
deduction if you are not following the submission requirements. As mentioned earlier, no need to 
spend time on creating a professional report.  
 


---
