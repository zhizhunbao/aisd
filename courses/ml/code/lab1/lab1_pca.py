"""
CST8506 Lab 1: Dimensionality Reduction using PCA
Author: Peng Wang
Student Number: 041107730
Date: 2026-01-22

Applies PCA to the Diabetes dataset and compares Random Forest performance
before and after dimensionality reduction.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from pathlib import Path

# Configuration constants
RANDOM_STATE = 42  # Fixed seed for reproducibility (42 is a common convention in ML community)
TEST_SIZE = 0.2  # 80-20 train-test split (standard practice)
N_ESTIMATORS = 100  # Number of trees in Random Forest (balance between performance and speed)
VARIANCE_THRESHOLD = 0.95  # Retain 95% of variance (recommended range: 85-95%)

IMAGES_DIR = Path('images')
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(RANDOM_STATE)

print("=" * 80)
print("CST8506 Lab 1: PCA Dimensionality Reduction")
print("=" * 80)
print()

# Step 1: Load the CSV file
print("Step 1: Loading diabetes.csv file...")
print("-" * 80)
df = pd.read_csv('diabetes.csv')
print("Dataset loaded successfully")
print()


# Step 2: Print dataset information
print("Step 2: Dataset Information")
print("-" * 80)
print("Attribute names:", df.columns.tolist())
print(f"Number of instances: {len(df)}")
print(f"Number of attributes: {len(df.columns)}")
print("\nFirst 5 instances:")
print(df.head())
print()


# Step 3: Split the dataset into train and test sets
print("Step 3: Splitting dataset into train and test sets")
print("-" * 80)
X = df.drop('class', axis=1)
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"Training set size: {X_train.shape[0]} instances")
print(f"Test set size: {X_test.shape[0]} instances")
print(f"Number of features: {X_train.shape[1]}")
print()


# Step 4: Standardize the data
print("Step 4: Standardizing the data")
print("-" * 80)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Data standardized successfully")
print(f"Mean of scaled training data: {X_train_scaled.mean():.6f}")
print(f"Standard deviation of scaled training data: {X_train_scaled.std():.6f}")
print()


# Step 5: Fit Random Forest model (Baseline)
print("Step 5: Training baseline Random Forest model (before PCA)")
print("-" * 80)
rf_baseline = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
rf_baseline.fit(X_train_scaled, y_train)
y_pred_baseline = rf_baseline.predict(X_test_scaled)
cm_baseline = confusion_matrix(y_test, y_pred_baseline)
acc_baseline = accuracy_score(y_test, y_pred_baseline)
print("Baseline model trained successfully")
print("Baseline Confusion Matrix:")
print(cm_baseline)
print(f"Baseline Accuracy: {acc_baseline:.4f}")
print()


# Step 6: Apply PCA to find all principal components
print("Step 6: Applying PCA to find all principal components")
print("-" * 80)
pca_full = PCA()
X_train_pca_full = pca_full.fit_transform(X_train_scaled)
X_test_pca_full = pca_full.transform(X_test_scaled)
print("PCA applied successfully")
print(f"Total number of components: {pca_full.n_components_}")
print()


# Step 7: Print explained variance ratios
print("Step 7: Explained Variance Ratios")
print("-" * 80)
explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

print("Explained Variance Ratio for each component:")
for i, var in enumerate(explained_var, 1):
    print(f"  PC{i}: {var:.4f} ({var*100:.2f}%)")

print("\nCumulative Explained Variance Ratios:")
for i, cum_var in enumerate(cumulative_var, 1):
    print(f"  PC1-PC{i}: {cum_var:.4f} ({cum_var*100:.2f}%)")
print()


# Step 8: Generate Scree Plots
print("Step 8: Generating Scree Plots")
print("-" * 80)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(range(1, len(explained_var) + 1), explained_var, 
         'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('Principal Component Number', fontsize=12)
ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
ax1.set_title('Scree Plot - Explained Variance Ratio', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, len(explained_var) + 1))

ax2.plot(range(1, len(cumulative_var) + 1), cumulative_var, 
         'ro-', linewidth=2, markersize=8)
ax2.axhline(y=0.85, color='g', linestyle='--', linewidth=2, label='85% variance')
ax2.axhline(y=0.90, color='orange', linestyle='--', linewidth=2, label='90% variance')
ax2.axhline(y=0.95, color='purple', linestyle='--', linewidth=2, label='95% variance')
ax2.set_xlabel('Principal Component Number', fontsize=12)
ax2.set_ylabel('Cumulative Explained Variance Ratio', fontsize=12)
ax2.set_title('Scree Plot - Cumulative Variance', fontsize=14, fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(1, len(cumulative_var) + 1))

plt.tight_layout()
plt.savefig(IMAGES_DIR / 'lab1_scree_plots.png', dpi=300, bbox_inches='tight')
plt.close()

print("Scree plots saved as 'images/lab1_scree_plots.png'")

d = np.argmax(cumulative_var >= VARIANCE_THRESHOLD) + 1
print(f"\nOptimal number of components (d) for {VARIANCE_THRESHOLD*100:.0f}% variance: {d}")
print(f"Variance explained by {d} components: {cumulative_var[d-1]:.4f} ({cumulative_var[d-1]*100:.2f}%)")
print()


# Step 9: Re-run PCA with d components
print(f"Step 9: Re-running PCA with d={d} components")
print("-" * 80)
pca_final = PCA(n_components=d)
X_train_pca = pca_final.fit_transform(X_train_scaled)
X_test_pca = pca_final.transform(X_test_scaled)
print("PCA with optimal components applied successfully")
print(f"Original dimensions: {X_train_scaled.shape[1]}")
print(f"Reduced dimensions: {X_train_pca.shape[1]}")
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d}")
print()


# Step 10: Apply Random Forest to reduced dataset
print("Step 10: Training Random Forest on PCA-reduced dataset")
print("-" * 80)
rf_pca = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
rf_pca.fit(X_train_pca, y_train)
y_pred_pca = rf_pca.predict(X_test_pca)
cm_pca = confusion_matrix(y_test, y_pred_pca)
acc_pca = accuracy_score(y_test, y_pred_pca)
print("Model trained on PCA-reduced data successfully")
print("PCA Confusion Matrix:")
print(cm_pca)
print(f"PCA Accuracy: {acc_pca:.4f}")
print()


# Step 11: Print confusion matrices comparison
print("Step 11: Confusion Matrix Comparison")
print("-" * 80)
print("Before PCA (Baseline):")
print(cm_baseline)
print()
print("After PCA:")
print(cm_pca)
print()


# Step 12: Print accuracy comparison
print("Step 12: Accuracy Comparison")
print("-" * 80)
print(f"Accuracy before PCA: {acc_baseline:.4f} ({acc_baseline*100:.2f}%)")
print(f"Accuracy after PCA:  {acc_pca:.4f} ({acc_pca*100:.2f}%)")
print(f"Accuracy change:     {acc_pca - acc_baseline:+.4f} ({(acc_pca - acc_baseline)*100:+.2f}%)")
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d} features")
print()


# Step 13: Plot first 2 principal components (2D)
print("Step 13: Plotting first 2 principal components (2D visualization)")
print("-" * 80)

plt.figure(figsize=(10, 8))
classes = np.unique(y_train)
colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))

for class_label, color in zip(classes, colors):
    mask = y_train == class_label
    plt.scatter(X_train_pca[mask, 0], X_train_pca[mask, 1], c=[color],
               label=f'Class {class_label}', alpha=0.6,
               edgecolors='black', linewidth=0.5, s=50)

plt.xlabel('First Principal Component (PC1)', fontsize=12)
plt.ylabel('Second Principal Component (PC2)', fontsize=12)
plt.title('2D Visualization: First 2 Principal Components', 
          fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(IMAGES_DIR / 'lab1_pca_2d.png', dpi=300, bbox_inches='tight')
plt.close()

print("2D plot saved as 'images/lab1_pca_2d.png'")
print()


# Step 14: Plot first 3 principal components (3D)
print("Step 14: Plotting first 3 principal components (3D visualization)")
print("-" * 80)

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

classes = np.unique(y_train)
colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))

for class_label, color in zip(classes, colors):
    mask = y_train == class_label
    ax.scatter(X_train_pca[mask, 0], X_train_pca[mask, 1], X_train_pca[mask, 2],
              c=[color], label=f'Class {class_label}', alpha=0.6,
              edgecolors='black', linewidth=0.5, s=50)

ax.set_xlabel('First Principal Component (PC1)', fontsize=11)
ax.set_ylabel('Second Principal Component (PC2)', fontsize=11)
ax.set_zlabel('Third Principal Component (PC3)', fontsize=11)
ax.set_title('3D Visualization: First 3 Principal Components', 
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(IMAGES_DIR / 'lab1_pca_3d.png', dpi=300, bbox_inches='tight')
plt.close()

print("3D plot saved as 'images/lab1_pca_3d.png'")
print()
