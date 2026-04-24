# Week 5 Review — Deep Learning for Image Classification

> 📋 Based on instructor's revision topics:
> **Limitation of ANN for image classification, Performance evaluation metrics – ROC curve, Data augmentation, Designing CNN architecture**

---

## Q1: What are the limitations of ANN for image classification?

| Limitation | Description |
|---|---|
| **High computational cost** | 1000×1000 image → millions of parameters |
| **Overfitting** | Too many parameters without spatial awareness |
| **Longer training time** | Fully connected architecture is inefficient |
| **No spatial hierarchy** | ANN treats all pixels equally, loses spatial relationships |

**Solution:** CNN uses convolutional layers for parameter sharing and local connectivity, drastically reducing parameters.

---

## Q2: What are ROC curve and AUC?

**ROC (Receiver Operating Characteristic) Curve:**
- Plots **True Positive Rate (TPR)** vs **False Positive Rate (FPR)**

**AUC (Area Under Curve):**

| AUC Value | Interpretation |
|---|---|
| **AUC = 1.0** | Perfect model |
| **AUC = 0.5** | Random chance (diagonal line) |
| **AUC < 0.5** | Worse than random |
| **Closer to 1.0** | Better model |

---

## Q3: What are the data augmentation strategies?

Data augmentation artificially expands the training dataset to **reduce overfitting**.

| Technique | Description |
|---|---|
| **Rotation** | Rotate images by random angles |
| **Scaling** | Resize images randomly |
| **Flipping** | Horizontal/vertical flip |
| **Cropping** | Random crop regions |

**Why it works:** Exposes the model to more varied features and scenarios → more robust, better generalization.

---

## Q4: What factors should be considered when designing a CNN architecture?

| Decision | Options / Considerations |
|---|---|
| **Number of layers** | Deeper networks for complex tasks |
| **Layer types** | Convolutional, Pooling, Fully Connected |
| **Filter size** | Smaller = fine details; Larger = broader patterns |
| **Stride** | Larger stride = smaller output |
| **Activation functions** | ReLU (hidden), Softmax (output) |
| **Overfitting risk** | Add dropout, regularization |
| **Computational efficiency** | Balance depth with available resources |

---

## Q5: What are the best practices for CNN training?

| Practice | Description |
|---|---|
| **Validation set** | Use validation set for hyperparameter tuning |
| **Early stopping** | Stop training when validation performance degrades |
| **Model checkpointing** | Periodically save model state for recovery |
| **Monitor metrics** | Monitor loss and accuracy on both training and validation sets |
| **Data augmentation** | Increase training data diversity |
| **Dropout + Regularization** | Prevent overfitting |

---

## Q6: What are common optimizers?

| Optimizer | Description |
|---|---|
| **SGD** | Stochastic Gradient Descent — Simple yet effective |
| **Adam** | Adaptive — Known for adaptiveness across different problems |
| **RMSprop** | Adjusts learning rate during training |

---

## Q7: CPU vs GPU vs TPU Comparison

| Hardware | Cores | Best For |
|---|---|---|
| **CPU** | Few | Versatile but slow for DL |
| **GPU** | Thousands | Ideal for parallel processing |
| **TPU** | Specialized | Fastest for neural network ops |
