---
title: "CST8506 Assignment 2: CIFAR-10 Classification"
author: "Peng Wang (041107730)"
date: "March 20, 2026"
subtitle: "CST8506 - Machine Learning"
---

# Imports and Setup {#step-0}

## Code

![Step 0 Code](assignment2_images/assignment2_cifar10_step00_imports_and_setup_code.png)

## Explanation

I imported NumPy, Matplotlib, scikit-learn (for MLP), and TensorFlow/Keras (for NN and CNN models). I also set up caching to avoid retraining models on subsequent runs.

---

# Step 1: Data Understanding - Load CIFAR-10 Dataset {#step-1}

## Code

![Step 1 Code](assignment2_images/assignment2_cifar10_step01_code.png)

## Output

![Step 1 Output](assignment2_images/assignment2_cifar10_step01_result.png)

## Explanation

I loaded the CIFAR-10 dataset from Keras. It has 50,000 training and 10,000 test images of size 32×32×3, evenly distributed across 10 classes (5,000 per class).

---

# Step 2: Data Understanding - Visualize Sample Images {#step-2}

## Code

![Step 2 Code](assignment2_images/assignment2_cifar10_step02_code.png)

## Output

![Step 2 Output](assignment2_images/assignment2_cifar10_step02_result.png)

## Sample Images

![Sample Images](assignment2_images/sample_images.png)

## Explanation

I displayed 2 random samples per class to visually understand the dataset. Classes include airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck.

---

# Step 3: Data Preparation - Normalize and Encode Labels {#step-3}

## Code

![Step 3 Code](assignment2_images/assignment2_cifar10_step03_code.png)

## Output

![Step 3 Output](assignment2_images/assignment2_cifar10_step03_result.png)

## Explanation

I normalized pixel values from [0,255] to [0,1] for faster convergence. Labels are one-hot encoded for Keras models. Images are also flattened to 3,072 features for MLP.

---

# Step 4: MLP Classification (scikit-learn) {#step-4}

## Code

![Step 4 Code](assignment2_images/assignment2_cifar10_step04_code.png)

## Output

![Step 4 Output](assignment2_images/assignment2_cifar10_step04_result.png)

## Explanation

I used scikit-learn's MLPClassifier with hidden layers (256, 128), ReLU activation, and Adam optimizer. It achieved 51.53% accuracy. Ship and automobile had the highest F1 scores; cat and bird were hardest to classify.

---

# Step 5: NN with Dense Layers Only (Keras) {#step-5}

## Code

![Step 5 Code](assignment2_images/assignment2_cifar10_step05_code.png)

## Output

![Step 5 Output](assignment2_images/assignment2_cifar10_step05_result.png)

## Explanation

I built a Dense-only NN: Flatten → Dense(512,relu) → Dropout(0.3) → Dense(256,relu) → Dropout(0.3) → Dense(10,softmax). It achieved 41.03% accuracy with 1,707,274 total parameters. The parameter table shows calculations like (3072+1)×512 = 1,573,376 for the first Dense layer.

---

# Step 6: CNN Model 1 - Conv + Dense (No Pooling) {#step-6}

## Code

![Step 6 Code](assignment2_images/assignment2_cifar10_step06_code.png)

## Output

![Step 6 Output](assignment2_images/assignment2_cifar10_step06_result.png)

## Explanation

CNN Model 1 uses Conv2D and Dense layers without pooling. Without pooling, the feature map stays at 32×32, producing a huge flatten output (65,536) and 8.4M parameters. It achieved 62.35% accuracy but is memory-intensive.

---

# Step 7: CNN Model 2 - Conv + MaxPool + Dense {#step-7}

## Code

![Step 7 Code](assignment2_images/assignment2_cifar10_step07_code.png)

## Output

![Step 7 Output](assignment2_images/assignment2_cifar10_step07_result.png)

## Explanation

I added MaxPooling2D layers which take the max in each 2×2 window, reducing dimensions from 32→16→8. This cuts parameters to 1.14M and improves accuracy to 72.12% — a big improvement over no-pooling Model 1.

---

# Step 8: CNN Model 3 - Conv + AvgPool + Dense {#step-8}

## Code

![Step 8 Code](assignment2_images/assignment2_cifar10_step08_code.png)

## Output

![Step 8 Output](assignment2_images/assignment2_cifar10_step08_result.png)

## Explanation

I replaced MaxPool with AveragePooling2D which takes the average instead of maximum. Same parameter count (1.14M) but slightly lower accuracy (70.24%). MaxPool usually wins in classification because it preserves the strongest features.

---

# Step 9: CNN Model 4 - Conv + MaxPool + AvgPool + Dense {#step-9}

## Code

![Step 9 Code](assignment2_images/assignment2_cifar10_step09_code.png)

## Output

![Step 9 Output](assignment2_images/assignment2_cifar10_step09_result.png)

## Explanation

Model 4 combines both MaxPool and AvgPool with 3 pooling layers total, reducing to 4×4 with only 356,810 parameters — the smallest model. It achieved the best accuracy at 74.13%, showing that combining pooling types captures both strong and averaged features.

---

# Step 11: CNN Architecture Diagrams {#step-11}

## Code

![Step 11 Code](assignment2_images/assignment2_cifar10_step11_code.png)

## Output

![Step 11 Output](assignment2_images/assignment2_cifar10_step11_result.png)

## CNN Model 1 Architecture

![CNN1 Architecture](assignment2_images/cnn1_architecture.png)

## CNN Model 2 Architecture

![CNN2 Architecture](assignment2_images/cnn2_architecture.png)

## CNN Model 3 Architecture

![CNN3 Architecture](assignment2_images/cnn3_architecture.png)

## CNN Model 4 Architecture

![CNN4 Architecture](assignment2_images/cnn4_architecture.png)

## Explanation

These pictorial representations show how data flows through each CNN model, with layer types, output shapes, and parameter counts labeled at each stage.

---

# Step 12: Results Summary {#step-12}

## Code

![Step 12 Code](assignment2_images/assignment2_cifar10_step12_code.png)

## Output

![Step 12 Output](assignment2_images/assignment2_cifar10_step12_result.png)

## Explanation

CNN Model 4 is the best (74.13%) and NN Dense-only is the worst (41.03%). CNNs outperform flat models because convolution extracts spatial features that are lost when images are flattened.

---

# Step 13: Training History Visualization {#step-13}

## Code

![Step 13 Code](assignment2_images/assignment2_cifar10_step13_code.png)

## Training History

![Training History](assignment2_images/training_history.png)

## Explanation

The training curves show CNN models converge faster and reach higher accuracy than the Dense-only NN. Model 4 has the most stable learning curve.

---

# Step 14: Prepare Subset Data for Parameter Study {#step-14}

## Code

![Step 14 Code](assignment2_images/assignment2_cifar10_step14_code.png)

## Output

![Step 14 Output](assignment2_images/assignment2_cifar10_step14_result.png)

## Explanation

I created a subset of 5,000 training and 1,000 test samples to speed up parameter experiments. Relative performance differences stay consistent on subsets.

---

# Step 15: MLP Parameter Study (6 parameters) {#step-15}

## Code

![Step 15 Code](assignment2_images/assignment2_cifar10_step15_code.png)

## Output

![Step 15 Output](assignment2_images/assignment2_cifar10_step15_result.png)

## Activation Function Calculations

Each activation function transforms inputs differently:

1. **ReLU**: f(x) = max(0, x). Example: f(3.5) = 3.5, f(-2.0) = 0. Fast, avoids vanishing gradient.
2. **Tanh**: f(x) = (e^x - e^{-x}) / (e^x + e^{-x}). Output [-1, 1], zero-centered.
3. **Sigmoid**: f(x) = 1 / (1 + e^{-x}). Output [0, 1], for probabilities.
4. **Softmax**: f(x_i) = e^{x_i} / Σe^{x_j}. Outputs sum to 1, for multi-class problems.

## Parameter Charts

![hidden_layer_sizes](assignment2_images/mlp_hidden_layer_sizes.png)

![activation](assignment2_images/mlp_activation.png)

![solver](assignment2_images/mlp_solver.png)

![batch_size](assignment2_images/mlp_batch_size.png)

![learning_rate](assignment2_images/mlp_learning_rate.png)

![max_iter](assignment2_images/mlp_max_iter.png)

## Explanation

- **hidden_layer_sizes**: (512,256,128) got 39.9% vs (128,) at 37.0%. Bigger networks learn more complex patterns.
- **activation**: All similar (~37-38%). Logistic slightly best at 38.1%.
- **solver**: Adam (37.8%) beats SGD (36.0%) and LBFGS (35.3%) because it adapts learning rates per parameter.
- **batch_size**: Smaller batches (32 → 40.5%) give more frequent gradient updates than larger ones (256 → 37.8%).
- **learning_rate**: 0.0001 (39.1%) is best. Too high (0.01 → 34.3%) causes overshooting.
- **max_iter**: 50 iterations (40.8%) is optimal; after that, performance plateaus.

---

# Step 16: Dense NN Parameter Study (2 parameters) {#step-16}

## Code

![Step 16 Code](assignment2_images/assignment2_cifar10_step16_code.png)

## Output

![Step 16 Output](assignment2_images/assignment2_cifar10_step16_result.png)

![units](assignment2_images/dense_units.png)

![activation](assignment2_images/dense_activation.png)

## Explanation

- **units**: Single layer (256,) at 32.9% beat deeper (512,256 → 30.4%) on this small subset — deeper networks need more data and epochs.
- **activation**: ReLU (33.0%) > sigmoid (31.7%) > tanh (27.5%). ReLU avoids vanishing gradient and computes faster.

---

# Step 17: CNN Parameter Study — Conv2D (6 parameters) {#step-17}

## Code

![Step 17 Code](assignment2_images/assignment2_cifar10_step17_code.png)

## Output

![Step 17 Output](assignment2_images/assignment2_cifar10_step17_result.png)

![filters](assignment2_images/cnn_filters.png)

![kernel_size](assignment2_images/cnn_kernel_size.png)

![strides](assignment2_images/cnn_strides.png)

![padding](assignment2_images/cnn_padding.png)

![activation](assignment2_images/cnn_activation.png)

![input_shape](assignment2_images/cnn_input_shape.png)

## Explanation

- **filters**: 64→128 (49.1%) slightly better. More filters detect more feature patterns.
- **kernel_size**: 3×3 (48.4%) > 7×7 (43.1%). Smaller kernels capture finer details.
- **strides**: (1,1) (49.6%) >> (2,2) (43.0%). Stride 2 skips pixels and loses information.
- **padding**: same (49.5%) > valid (46.0%). Same padding preserves spatial dimensions.
- **activation**: ReLU (49.9%) >> sigmoid (9.0%). Sigmoid causes severe vanishing gradient in deep CNNs.
- **input_shape**: 32×32 (49.5%) is the original CIFAR-10 resolution and works best. 16×16 loses detail, 48×48 adds noise from upscaling.

---

# Step 18: CNN Parameter Study — Compile (3 parameters) {#step-18}

## Code

![Step 18 Code](assignment2_images/assignment2_cifar10_step18_code.png)

## Output

![Step 18 Output](assignment2_images/assignment2_cifar10_step18_result.png)

## Role of Compile and Fit Methods

**model.compile()** configures training (does NOT train): sets the optimizer (weight update algorithm), loss function (error measurement), and metrics (monitoring).

**model.fit()** executes training: performs forward pass, calculates loss, runs backpropagation, and updates weights over specified epochs with given batch size.

![optimizer](assignment2_images/cnn_optimizer.png)

![loss](assignment2_images/cnn_loss.png)

![metrics](assignment2_images/cnn_metrics.png)

## Explanation

- **optimizer**: Adam (47.0%) ≈ RMSprop (46.9%) >> SGD (24.0%). SGD without momentum struggles with complex loss landscapes.
- **loss**: categorical_crossentropy (52.2%) is best for classification. MSE (46.6%) is designed for regression, not classification.
- **metrics**: All produce similar accuracy (~47-50%) because metrics only monitor training — they don't affect weight updates.

---

# Step 19: CNN Parameter Study — Fit (5 parameters) {#step-19}

## Code

![Step 19 Code](assignment2_images/assignment2_cifar10_step19_code.png)

## Output

![Step 19 Output](assignment2_images/assignment2_cifar10_step19_result.png)

![epochs](assignment2_images/cnn_epochs.png)

![batch_size](assignment2_images/cnn_batch_size.png)

![learning_rate](assignment2_images/cnn_learning_rate.png)

![validation_split](assignment2_images/cnn_validation_split.png)

![validation_method](assignment2_images/cnn_validation_method.png)

## Explanation

- **epochs**: 15 (55.1%) > 3 (43.6%). More epochs allow better convergence but risk overfitting.
- **batch_size**: 32 (52.2%) > 256 (42.0%). Smaller batches give noisier but more frequent gradient updates.
- **learning_rate**: 0.001 (45.4%) is optimal. 0.0001 converges too slowly; 0.01 overshoots.
- **validation_split**: 0.3 (50.4%) slightly better than 0.1 (47.0%), but uses fewer training samples.
- **validation_data**: Using explicit validation_data (49.7%) vs validation_split (50.4%) gives similar results. validation_data provides more control over which samples are used.

---

# Step 20: Parameter Study Summary {#step-20}

## Code

![Step 20 Code](assignment2_images/assignment2_cifar10_step20_code.png)

## Output

![Step 20 Output](assignment2_images/assignment2_cifar10_step20_result.png)

## Explanation

I studied 22 parameters across 74 models total. Key findings: (1) CNN outperforms MLP/NN for image classification. (2) Pooling layers are essential — they reduce parameters and improve accuracy. (3) Adam optimizer, ReLU activation, and categorical_crossentropy are the best default choices. (4) Smaller batch sizes and moderate learning rates (0.001) yield the best results.
