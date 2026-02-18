# CST8508 Machine Vision — Mock Midterm Exam 模拟期中考试

> **Time:** 60 minutes | **Total Marks:** 25 | **Calculator:** ✅ Allowed
> **Instructions:** Answer ALL questions.

---

## Section 1: Multiple Choice (10 marks — 1 mark each)

**1.** What is the primary purpose of Machine Vision?
- A) To create 3D animations for video games
- B) To design websites with interactive features
- C) To enable imaging-based automatic inspection and analysis
- D) To develop mobile applications
<details><summary>Answer</summary>C — MV 的核心定义：基于成像的自动检测与分析</details>

**2.** Which stage of the Machine Vision workflow is responsible for analyzing and manipulating images?
- A) Image Acquisition
- B) Image Processing
- C) Interpretation
- D) Image Compression
<details><summary>Answer</summary>B — Image Processing 阶段负责图像的分析和操作</details>

**3.** Which of the following is the correct order of steps in Canny edge detection?
- A) Gradient → Noise Reduction → Double Thresholding → Non-Max Suppression → Hysteresis
- B) Noise Reduction → Gradient → Non-Max Suppression → Double Thresholding → Hysteresis
- C) Double Thresholding → Gradient → Noise Reduction → Hysteresis → Non-Max Suppression
- D) Hysteresis → Noise Reduction → Gradient → Non-Max Suppression → Double Thresholding
<details><summary>Answer</summary>B — 正确顺序：降噪→梯度→非极大值抑制→双阈值→滞后跟踪</details>

**4.** Which thresholding technique calculates different thresholds for different regions, making it suitable for images with uneven illumination?
- A) Binary Thresholding
- B) Otsu's Thresholding
- C) Adaptive Thresholding
- D) Global Thresholding
<details><summary>Answer</summary>C — Adaptive Thresholding 为不同区域计算局部阈值，适合光照不均匀</details>

**5.** ORB feature detector is a combination of:
- A) SIFT keypoint detector and SURF descriptor
- B) Harris corner detector and HOG descriptor
- C) FAST keypoint detector and BRIEF descriptor
- D) Canny edge detector and SIFT descriptor
<details><summary>Answer</summary>C — ORB = Oriented FAST + Rotated BRIEF</details>

**6.** Which technique is most commonly used for pedestrian detection?
- A) SIFT
- B) ORB
- C) HOG (Histogram of Oriented Gradients)
- D) SURF
<details><summary>Answer</summary>C — HOG 捕捉梯度方向模式，与人体结构匹配，常配合 SVM</details>

**7.** In a CNN, which layer reduces the spatial dimensions of feature maps?
- A) Convolutional Layer
- B) Fully Connected Layer
- C) Pooling Layer
- D) Dropout Layer
<details><summary>Answer</summary>C — Pooling Layer 通过 Max/Average Pooling 进行下采样</details>

**8.** What is the main advantage of ReLU over Sigmoid activation?
- A) ReLU outputs values between 0 and 1
- B) ReLU is more susceptible to vanishing gradient
- C) ReLU reduces the vanishing gradient problem and is computationally simpler
- D) Sigmoid generates sparser representations than ReLU
<details><summary>Answer</summary>C — ReLU 在正区间梯度恒为 1，不会梯度消失；计算只需 max(0,x)</details>

**9.** Which of the following is a valid strategy to prevent overfitting?
- A) Increasing model complexity
- B) Removing the validation set
- C) Applying Dropout regularization
- D) Training for more epochs without any stopping criteria
<details><summary>Answer</summary>C — Dropout 随机关闭神经元防止共适应，是经典防过拟合方法</details>

**10.** Which hardware is best suited for training deep learning models?
- A) CPU
- B) GPU
- C) Hard Disk Drive
- D) Network Router
<details><summary>Answer</summary>B — GPU 拥有大量并行核心，适合深度学习的矩阵运算</details>

---

## Section 2: Fill in the Blanks (5 marks — 1 mark each)

**11.** In an image histogram, the horizontal axis represents _____________ levels and the vertical axis represents the _____________ of pixels.

<details><summary>Answer</summary>brightness (intensity); count (number)</details>

**12.** The morphological operation that applies erosion followed by dilation is called _____________, and it is useful for removing small _____________.

<details><summary>Answer</summary>Opening; noise (噪点)</details>

**13.** SIFT generates a _____________-dimensional feature descriptor, while SURF generates a _____________-dimensional descriptor.

<details><summary>Answer</summary>128; 64</details>

**14.** The function f(x) = max(0, x) is the _____________ activation function, and the function that converts output scores to a probability distribution summing to 1 is called _____________.

<details><summary>Answer</summary>ReLU; Softmax</details>

**15.** _____________ is a deep learning optimization technique that reduces numerical precision of weights, and is generally preferred over _____________ for model compression.

<details><summary>Answer</summary>Quantization; Pruning</details>

---

## Section 3: Short Answer (5 marks)

**16. (2 marks)** Compare Traditional Computer Vision and Deep Learning approaches. List two advantages and one disadvantage of each.

<details><summary>Answer</summary>

**Traditional CV:**
- ✅ Advantages: (1) Transparent and interpretable — you can understand why decisions are made; (2) Lower computational requirements — can run on CPU without GPU
- ❌ Disadvantage: Requires manual feature engineering by domain experts; struggles with complex scenes

**Deep Learning:**
- ✅ Advantages: (1) Automatic feature extraction — CNN learns features end-to-end; (2) Higher accuracy for complex tasks like image classification
- ❌ Disadvantage: Requires large datasets and expensive hardware (GPU/TPU); acts as a "black box"

</details>

**17. (3 marks)** Describe the complete architecture of a CNN. For each major layer type (Convolutional, Pooling, Fully Connected), explain: (a) what it does, (b) why it is needed.

<details><summary>Answer</summary>

**CNN Architecture:** Input → [Conv → Activation → Pooling]×N → Flatten → FC → Softmax → Output

**(a) Convolutional Layer:**
- What: Slides learnable kernels (filters) across the input, performing dot product operations to produce feature maps
- Why: Automatically extracts spatial features (edges, textures, shapes) from images while preserving spatial relationships

**(b) Pooling Layer (e.g., Max Pooling):**
- What: Reduces spatial dimensions by selecting the maximum (or average) value within a window
- Why: Reduces computational cost, provides translation invariance, and prevents overfitting by reducing parameters

**(c) Fully Connected Layer:**
- What: Flattens the 2D feature maps into a 1D vector and connects every neuron to compute final classification scores
- Why: Combines all learned features to make the final classification decision; output layer uses Softmax to produce probability distribution

</details>

---

## Section 4: Mathematical Questions (5 marks)

**18. (2 marks)** A CNN has the following layer configuration:
- Input: 28×28×1 (grayscale image)
- Conv Layer: 16 filters, 3×3 kernel, stride=1, padding=0
- Max Pooling: 2×2, stride=2

Calculate:
(a) The output size after the Conv layer
(b) The output size after the Max Pooling layer

<details><summary>Answer</summary>

**(a) After Conv:**
Output = (Input - Kernel + 2×Padding) / Stride + 1
Output = (28 - 3 + 0) / 1 + 1 = **26×26×16** ✓ (1 mark)

**(b) After Max Pooling:**
Output = 26 / 2 = **13×13×16** ✓ (1 mark)

</details>

**19. (1 mark)** How many trainable parameters (including bias) does the Conv layer in Q18 have?

<details><summary>Answer</summary>

Parameters = (K_h × K_w × C_in + 1_bias) × C_out
Parameters = (3 × 3 × 1 + 1) × 16 = 10 × 16 = **160** ✓

</details>

**20. (2 marks)** A model produces the following confusion matrix:

```
                Predicted Positive    Predicted Negative
Actual Positive       35                    15
Actual Negative       10                    40
```

Calculate: (a) Accuracy (b) Precision (c) Recall (d) F1 Score

<details><summary>Answer</summary>

TP=35, FN=15, FP=10, TN=40, Total=100

**(a) Accuracy** = (TP+TN)/Total = (35+40)/100 = **75%** (0.5 mark)

**(b) Precision** = TP/(TP+FP) = 35/(35+10) = 35/45 = **77.8%** ≈ 0.778 (0.5 mark)

**(c) Recall** = TP/(TP+FN) = 35/(35+15) = 35/50 = **70%** = 0.70 (0.5 mark)

**(d) F1** = 2×P×R/(P+R) = 2×0.778×0.70/(0.778+0.70) = 1.089/1.478 = **0.737 = 73.7%** (0.5 mark)

</details>

---

## Scoring Summary 分值分布

| Section | Type | Marks |
|---------|------|-------|
| Section 1 | MCQ (10 questions) | 10 |
| Section 2 | Fill in the Blanks (5 questions) | 5 |
| Section 3 | Short Answer (2 questions) | 5 |
| Section 4 | Mathematical (3 questions) | 5 |
| **Total** | | **25** |

---

> ⏱ **Target completion time:** 60 minutes
> - MCQ: ~15 min
> - Fill in Blanks: ~5 min  
> - Short Answer: ~20 min
> - Math: ~20 min
