# Week 4 Review — Convolutional Neural Networks (CNN)

> 📋 Based on instructor's revision topics:
> **Traditional methods vs neural network for image classification, Activation functions, Loss function, Back propagation, CNN architecture, CNN layers, Best practices for training CNN, Overfitting solutions**

---

## Q1: Traditional Methods vs Neural Networks for Image Classification?

| Aspect | Traditional Methods | Neural Networks (CNN) |
|---|---|---|
| Feature extraction | **Manual** (handcrafted) | **Automatic** (learned from data) |
| Scalability | Poor for large images | Handles high-dimensional data |
| Adaptability | Limited | Robust to translation |
| Example | Decision tree + manual features | CNN with convolutional layers |

**Limitation of ANN for image classification:** A 1000×1000px image leads to high computational cost, overfitting, and long training time.

---

## Q2: What are the key components of CNN architecture?

| Layer | Role | Description |
|---|---|---|
| **Convolutional** | Feature extraction | Small learnable filters slide over input, extracting edges, textures, shapes |
| **Pooling** | Dimensionality reduction | Max/Average pooling downsamples, reducing parameters and computation |
| **Fully Connected** | Classification | Integrates features, outputs class probability distribution |
| **Flattening** | Format conversion | Converts multi-dimensional feature maps into a 1D vector |

**Output size formula:** **(N – F + 2P) / S + 1**
- N = image size, F = filter size, S = stride, P = padding

---

## Q3: What are common activation functions?

| Function | Range | Pros | Cons | Use |
|---|---|---|---|---|
| **Sigmoid** | (0, 1) | Good for binary classification | Vanishing gradient | Output layer (binary) |
| **Tanh** | (-1, 1) | Zero-centered output | Vanishing gradient | Handling negative values |
| **ReLU** | [0, ∞) | Mitigates vanishing gradient, sparse representation | Dead neurons | **Hidden layers (most common)** |
| **Softmax** | (0, 1), sum=1 | Probability distribution | — | Output layer (multi-class) |

ReLU: f(x) = max(0, x)

---

## Q4: What is a loss function?

A loss function measures the difference between model predictions and ground truth, guiding the optimizer to adjust parameters.

| Loss Function | Formula | Use Case |
|---|---|---|
| **MSE** | (1/N)Σ(yᵢ - ŷᵢ)² | Regression |
| **BCE** | -(1/N)Σ[yᵢ·log(ŷᵢ) + (1-yᵢ)·log(1-ŷᵢ)] | Binary classification |
| **CCE** | -(1/N)ΣᵢΣⱼ yᵢⱼ·log(ŷᵢⱼ) | Multi-class classification |

---

## Q5: What are the basic steps of backpropagation?

Backpropagation **only occurs during training**, optimizing weights and biases by minimizing error.

| Step | Description |
|---|---|
| 1 | Feed a sample to the network |
| 2 | Calculate the mean squared error |
| 3 | Calculate error term of each output neuron |
| 4 | Iteratively calculate hidden layer error terms |
| 5 | Apply the delta rule |
| 6 | Adjust the weights |

**Weight Update:** w_new = w_old - η × (∂L/∂w)
- η = learning rate, ∂L/∂w = gradient of loss w.r.t. weight

---

## Q6: How to prevent overfitting?

Overfitting = training accuracy is much higher than validation accuracy.

| Strategy | Description |
|---|---|
| **Dropout** | Randomly deactivate neurons during training to prevent feature co-adaptation |
| **Regularization** | L1 (lasso) / L2 (ridge) penalize large weights |
| **Data Augmentation** | Rotation, scaling, flipping, cropping to increase data diversity |
| **Simplify Model** | Reduce the number of layers or neurons |
| **Early Stopping** | Stop training when validation performance degrades |

---

## Q7: Performance Evaluation Metrics

| Metric | Formula | Description |
|---|---|---|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| **Precision** | TP/(TP+FP) | Accuracy of positive predictions |
| **Recall** | TP/(TP+FN) | Recall rate of true positives |
| **F1-Score** | 2×(P×R)/(P+R) | Harmonic mean of precision and recall |
| **ROC/AUC** | TPR vs FPR curve | AUC closer to 1.0 is better |

**Confusion Matrix:** TP (True Positive), TN (True Negative), FP (False Positive), FN (False Negative)
