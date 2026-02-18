# CST8508 Machine Vision — Midterm Quiz Bank 期中题库

> **Exam Format:** MCQ + Fill in the blanks + Short Answer + Mathematical Questions
> **Scope:** Weeks 1–5 | **Duration:** 60 min | **Total:** 25 marks

---

## Part A: Multiple Choice Questions (MCQ)

### Week 1: Introduction to Machine Vision

**Q1.** What is Machine Vision primarily used for?
- A) Gaming development
- B) 3D animation
- C) ✅ Imaging-based automatic inspection and analysis
- D) Web design

> **解释:** Machine Vision 的核心定义是基于成像的自动检测与分析，用于工业质检、对象识别等。

**Q2.** What are the three main stages of a Machine Vision workflow?
- A) Filtering, Classification, Output
- B) ✅ Image Acquisition, Image Processing, Interpretation/Action
- C) Training, Validation, Testing
- D) Input, Hidden Layer, Output

> **解释:** MV 工作流的三步：采集图像 → 处理分析 → 解释决策。

**Q3.** Which type of image sensor converts light into electrical signals using a grid of tiny photosites?
- A) ✅ CMOS
- B) LCD
- C) LED
- D) OLED

> **解释:** CMOS (Complementary Metal-Oxide Semiconductor) 和 CCD 都是将光信号转换为电信号的图像传感器。

**Q4.** A pixel in a grayscale image is represented by:
- A) A tuple of 3 values (R, G, B)
- B) ✅ A single intensity value (0-255)
- C) A binary value only (0 or 1)
- D) A 16-bit floating point number

> **解释:** 灰度图的每个像素是一个 0-255 的单值，0=黑，255=白。彩色图才是 RGB 三元组。

---

### Week 2: Image Processing Fundamentals

**Q5.** Which filter type smoothens an image?
- A) Image Sharpening
- B) ✅ Image Blurring
- C) Image Translation
- D) Image Segmentation

> **解释:** Blurring 通过对邻域像素取平均来降噪和平滑图像。

**Q6.** Select ALL stages involved in Canny edge detection:
- A) Noise Reduction
- B) Edge tracking by Hysteresis
- C) Gradient Calculation
- D) ✅ All of the above

> **解释:** Canny 包括：降噪 → 梯度计算 → 非极大值抑制 → 双阈值 → 滞后边缘跟踪。

**Q7.** Which stage in Canny edge detection applies two thresholds to classify edges?
- A) Noise Reduction
- B) Gradient Calculation
- C) ✅ Double Thresholding
- D) Edge Tracking by Hysteresis

> **解释:** Double Thresholding 使用高、低两个阈值将边缘分为强边缘、弱边缘和非边缘。

**Q8.** The horizontal axis of an image histogram shows:
- A) Count of pixels
- B) ✅ Different brightness levels
- C) Number of channels
- D) Size of image

> **解释:** 直方图的 X 轴是亮度级别(0-255)，Y 轴是对应的像素数量。

**Q9.** What are morphological operations in image processing typically used for?
- A) ✅ Processing images based on shapes
- B) Enhancing image resolution
- C) Color corrections
- D) Image compression

> **解释:** 形态学操作（腐蚀、膨胀、开运算、闭运算）基于对象的形状和结构进行处理。

**Q10.** Which thresholding technique is best for images with uneven lighting?
- A) Binary Thresholding
- B) Otsu's Thresholding
- C) ✅ Adaptive Thresholding
- D) Double Thresholding

> **解释:** Adaptive Thresholding 为图像的不同区域计算局部阈值，适合光照不均匀的场景。

**Q11.** Which morphological operation is used to remove small noise from a binary image while preserving the shape of larger objects?
- A) Dilation
- B) Erosion
- C) ✅ Opening (erosion followed by dilation)
- D) Closing (dilation followed by erosion)

> **解释:** Opening = 先腐蚀后膨胀，可以去除小噪点同时保持大对象的形状。Closing 则用于填补小孔。

**Q12.** Gaussian Blur differs from Average Blur in that it:
- A) Uses the minimum value in the kernel window
- B) ✅ Assigns higher weight to the center pixel and lower weight to surrounding pixels
- C) Only works on binary images
- D) Produces a sharpened image

> **解释:** 高斯模糊使用高斯核，中心像素权重最高，越远权重越低，比均值模糊更自然。

---

### Week 3: Feature Detection & Description

**Q13.** The output of segmentation is typically a _____ image.
- A) Color image
- B) Grayscale image
- C) ✅ Binary image
- D) Compressed image

> **解释:** 分割将图像分为前景和背景，输出为二值图像（对象=1，背景=0）。

**Q14.** Which OpenCV command is used for drawing contour outlines?
- A) cv2.findContours()
- B) cv2.fillContours()
- C) ✅ cv2.drawContours()
- D) cv2.getContours()

> **解释:** `cv2.findContours()` 找轮廓，`cv2.drawContours()` 画轮廓。

**Q15.** ORB is a fusion of _____ keypoint detector and _____ descriptor.
- A) SIFT and SURF
- B) Harris and SIFT
- C) ✅ FAST keypoint detector and BRIEF descriptor
- D) HOG and SVM

> **解释:** ORB = Oriented FAST (快速角点检测) + Rotated BRIEF (二进制描述符)，开源免费。

**Q16.** Which technique is most effective for human/pedestrian detection?
- A) SURF
- B) FAST
- C) ✅ HOG (Histogram of Oriented Gradients)
- D) SIFT

> **解释:** HOG 捕捉梯度方向模式，与人体结构特征匹配，常配合 SVM 用于行人检测。

**Q17.** Which feature detection algorithm produces a 128-dimensional descriptor?
- A) ORB
- B) SURF (64-D)
- C) ✅ SIFT
- D) FAST

> **解释:** SIFT 将关键点区域分为 4×4 子块，每块 8 个方向的直方图，4×4×8=128 维向量。SURF 生成 64 维。

**Q18.** What property makes SIFT particularly robust?
- A) It only works on binary images
- B) It requires no computation
- C) ✅ It is invariant to scale and rotation changes
- D) It can only detect edges

> **解释:** SIFT 的核心优势是尺度不变性（通过 DoG）和旋转不变性（通过方向分配）。

**Q19.** Which feature detection algorithm is the fastest and most suitable for real-time applications on resource-constrained devices?
- A) SIFT
- B) SURF
- C) ✅ ORB
- D) HOG

> **解释:** ORB 开源免费，使用二进制描述符（Hamming distance），计算最快，适合嵌入式/实时场景。

---

### Week 4: CNNs

**Q20.** Which layer in CNN is responsible for downsampling of feature maps?
- A) Convolutional Layer
- B) ✅ Pooling Layer
- C) Fully-connected Layer
- D) Output Layer

> **解释:** Pooling Layer（池化层）通过 Max/Average Pooling 降低空间维度，减少计算量。

**Q21.** What is the main advantage of using ReLU over Sigmoid as an activation function?
- A) ReLU always produces outputs between 0 and 1
- B) ✅ ReLU is less susceptible to the vanishing gradient problem
- C) ReLU is more computationally expensive
- D) Sigmoid produces sparser representations

> **解释:** Sigmoid 在两端梯度接近 0（梯度消失），ReLU 在正区间梯度恒为 1，训练更高效。

**Q22.** In a CNN, what is the role of the kernel (filter)?
- A) To store the final classification results
- B) ✅ To detect specific features (edges, textures) through convolution
- C) To reduce the learning rate
- D) To normalize the input data

> **解释:** 卷积核是可学习的权重矩阵，在图像上滑动做点积运算，自动检测特征（边缘、纹理等）。

**Q23.** _____ measures the proportion of total predictions that the model got correct.
- A) Precision
- B) ✅ Accuracy
- C) F1 Score
- D) Recall

> **解释:** Accuracy = (TP+TN)/(TP+TN+FP+FN)，衡量所有预测中正确的比例。

**Q24.** What is the purpose of the Softmax function in the output layer of a CNN?
- A) To perform convolution on the input
- B) To reduce overfitting
- C) ✅ To convert output scores into probability distributions that sum to 1
- D) To perform max pooling

> **解释:** Softmax 将最后一层的原始分数映射为概率分布（所有类别的概率之和为 1）。

**Q25.** Which of the following is NOT a component of a typical CNN architecture?
- A) Convolutional Layer
- B) Pooling Layer
- C) Fully Connected Layer
- D) ✅ Recurrent Layer

> **解释:** CNN 的三大基本组件是 Convolutional, Pooling, Fully Connected。Recurrent Layer 属于 RNN。

---

### Week 5: Deep Learning

**Q26.** Which technique is used to artificially increase the size of a training dataset?
- A) Pruning
- B) ✅ Data Augmentation
- C) Quantization
- D) Backpropagation

> **解释:** Data Augmentation 通过旋转、翻转、裁剪等变换人为扩大训练集，减少过拟合。

**Q27.** What is overfitting in deep learning?
- A) The model cannot learn from the training data
- B) The model performs equally on training and test data
- C) ✅ The model learns the training data too well, including noise, leading to poor generalization
- D) The model has too few parameters

> **解释:** 过拟合是模型"记住"了训练数据的噪声和细节，在新数据上表现差。表现为训练准确率远高于验证准确率。

**Q28.** Which of the following is NOT a strategy to prevent overfitting?
- A) Dropout
- B) L1/L2 Regularization
- C) Data Augmentation
- D) ✅ Increasing model complexity (adding more layers)

> **解释:** 增加模型复杂度反而会加剧过拟合。正确的防过拟合方法包括 Dropout、正则化、数据增强、早停、简化模型。

**Q29.** Which optimizer is known for its adaptiveness to different problems and is widely used in deep learning?
- A) SGD
- B) ✅ Adam
- C) Newton's Method
- D) Gradient Descent

> **解释:** Adam 结合了 Momentum 和 RMSprop 的优点，自适应调整每个参数的学习率，通用性最强。

**Q30.** Which hardware is BEST suited for training deep learning models due to its parallel processing capabilities?
- A) CPU
- B) ✅ GPU
- C) HDD
- D) RAM

> **解释:** GPU 拥有数千个核心，适合深度学习需要的大规模并行矩阵运算。TPU 更快但更昂贵。

**Q31.** What is the purpose of Early Stopping in CNN training?
- A) To speed up the forward pass
- B) To increase the number of epochs
- C) ✅ To halt training when validation performance starts to degrade
- D) To reduce the learning rate

> **解释:** Early Stopping 监控验证集性能，当性能开始下降时停止训练，防止过拟合。

**Q32.** Cross-Entropy Loss is primarily used for:
- A) Regression tasks
- B) ✅ Classification tasks
- C) Image generation
- D) Dimensionality reduction

> **解释:** Cross-Entropy (交叉熵) 衡量预测概率分布与真实分布的差异，是分类任务的标准损失函数。

**Q33.** Which CNN optimization technique reduces the precision of numbers used to represent weights?
- A) Pruning
- B) ✅ Quantization
- C) Dropout
- D) Batch Normalization

> **解释:** Quantization 量化将权重从高精度（如 FP32）降为低精度（如 INT8），减少存储和计算。

---

## Part B: Fill in the Blanks

**B1.** Machine Vision workflow consists of three stages: Image __________, Image __________, and Interpretation/Action.

> **Answer:** Acquisition, Processing

**B2.** The horizontal axis of an image histogram represents __________ levels, while the vertical axis represents the __________ of pixels.

> **Answer:** brightness (intensity), count (number)

**B3.** In Canny edge detection, __________ Thresholding is used to classify edges into strong, weak, and non-edges.

> **Answer:** Double

**B4.** __________ is a morphological operation that first applies erosion followed by dilation, useful for removing small noise.

> **Answer:** Opening

**B5.** SIFT generates a __________-dimensional feature descriptor for each keypoint.

> **Answer:** 128

**B6.** ORB combines the __________ keypoint detector with the __________ descriptor.

> **Answer:** FAST, BRIEF

**B7.** In CNN, the __________ layer is responsible for downsampling feature maps to reduce spatial dimensions.

> **Answer:** Pooling

**B8.** The activation function f(x) = max(0, x) is called __________.

> **Answer:** ReLU (Rectified Linear Unit)

**B9.** __________ occurs when a model learns the training data too well, resulting in poor performance on unseen data.

> **Answer:** Overfitting

**B10.** The __________ function converts the output of a neural network into a probability distribution where all values sum to 1.

> **Answer:** Softmax

**B11.** __________ is the technique of artificially increasing the training dataset through transformations like rotation, flipping, and scaling.

> **Answer:** Data Augmentation

**B12.** Accuracy is calculated as the ratio of __________ to total predictions.

> **Answer:** correct predictions (TP + TN)

**B13.** In a Confusion Matrix, a __________ occurs when the model incorrectly predicts a positive result.

> **Answer:** False Positive (FP)

**B14.** __________ Thresholding calculates thresholds locally, making it suitable for images with uneven lighting.

> **Answer:** Adaptive

**B15.** A CNN typically consists of __________ layers, Pooling layers, and __________ Connected layers.

> **Answer:** Convolutional, Fully

---

## Part C: Short Answer Questions

**C1.** Compare SIFT, SURF, and ORB in terms of speed, descriptor size, and best use case. (对比 SIFT、SURF、ORB)

> **Answer:**
> | Feature | SIFT | SURF | ORB |
> |---------|------|------|-----|
> | Speed | Slowest | Medium | **Fastest** |
> | Descriptor | 128-D float | 64-D float | 32 bytes binary |
> | Scale Invariant | Yes | Yes | No |
> | Rotation Invariant | Yes | Yes | Yes |
> | Patent-free | Yes (expired) | No | **Yes** |
> | Best for | Accurate matching | Real-time + accuracy | Embedded / real-time |
>
> SIFT 最精确但最慢；SURF 是 SIFT 的加速版，用积分图加速；ORB 最快且免费，使用 Hamming distance 做匹配。

**C2.** Explain the purpose of each layer in a CNN architecture. (解释 CNN 各层的作用)

> **Answer:**
> 1. **Convolutional Layer 卷积层:** Uses learnable kernels/filters to extract features (edges, textures, patterns) through convolution operations. Produces feature maps.
> 2. **Activation Function (ReLU):** Introduces non-linearity, allowing the network to learn complex patterns. ReLU: f(x) = max(0, x).
> 3. **Pooling Layer 池化层:** Reduces spatial dimensions through downsampling (Max/Average Pooling), reducing computation while preserving important features.
> 4. **Fully Connected Layer 全连接层:** Flattens the feature maps and performs classification by connecting every neuron to the output.
> 5. **Output Layer (Softmax):** Produces probability distribution across output classes.

**C3.** What is overfitting? List 3 strategies to prevent it. (过拟合是什么？列出 3 种防止策略)

> **Answer:**
> Overfitting occurs when a model learns the training data too well, including its noise and outliers, leading to high accuracy on training data but poor generalization to unseen data.
>
> Prevention strategies:
> 1. **Dropout:** Randomly deactivates neurons during training to prevent co-adaptation
> 2. **Regularization (L1/L2):** Adds penalty terms to the loss function to discourage large weights
> 3. **Data Augmentation:** Artificially increases training data through transformations (rotation, flipping, etc.)
> 4. **Early Stopping:** Halts training when validation performance starts degrading
> 5. **Simplify the model:** Reduce layers or neurons

**C4.** Describe the 5 steps of Canny edge detection. (描述 Canny 边缘检测的 5 个步骤)

> **Answer:**
> 1. **Noise Reduction 降噪:** Apply Gaussian blur to smooth the image and reduce noise
> 2. **Gradient Calculation 梯度计算:** Compute intensity gradients (magnitude and direction) using Sobel operators in both x and y directions
> 3. **Non-Maximum Suppression 非极大值抑制:** Thin edges by keeping only local maxima in the gradient direction
> 4. **Double Thresholding 双阈值:** Apply high and low thresholds to classify pixels as strong edges, weak edges, or non-edges
> 5. **Edge Tracking by Hysteresis 滞后边缘跟踪:** Finalize edges by keeping weak edges only if connected to strong edges

**C5.** Explain the difference between Traditional Computer Vision and Deep Learning approaches. When might you choose one over the other? (对比传统 CV 和 DL)

> **Answer:**
> **Traditional CV:**
> - Uses hand-crafted features (SIFT, SURF, HOG)
> - Requires manual feature engineering by experts
> - Transparent and interpretable
> - Lower computational requirements
> - Better for simple tasks, limited data, resource-constrained environments
>
> **Deep Learning:**
> - End-to-end learning, CNN automatically extracts features
> - Requires large training datasets and powerful hardware (GPU/TPU)
> - Higher accuracy for complex tasks
> - Acts as a "black box" — less interpretable
>
> **When to use Traditional CV:** Simple classification (color-based sorting), limited data, low-power devices, 3D vision/SLAM
> **When to use Deep Learning:** Complex image classification, large datasets available, high accuracy needed

**C6.** What is the difference between Precision and Recall? Give an example. (Precision 和 Recall 的区别)

> **Answer:**
> - **Precision = TP / (TP + FP):** Of all items predicted as positive, what fraction is actually positive? 在所有预测为正的结果中，有多少是真正为正的？
> - **Recall = TP / (TP + FN):** Of all actual positive items, what fraction did we correctly identify? 在所有实际为正的结果中，有多少被正确识别？
>
> **Example (Medical diagnosis 医学诊断):**
> - High Precision = 检测到的疾病大部分确实是疾病（少误诊）
> - High Recall = 大多数实际患病的人都被检测出来（少漏诊）
> - In cancer screening, HIGH RECALL is critical (不能漏诊)

**C7.** Explain what a Confusion Matrix is and how it relates to Accuracy, Precision, and Recall. (解释混淆矩阵)

> **Answer:**
> A Confusion Matrix is a table that summarizes the performance of a classification model by showing counts of:
> ```
>                 Predicted Positive    Predicted Negative
> Actual Positive      TP                    FN
> Actual Negative      FP                    TN
> ```
> - **TP (True Positive):** Correctly predicted positive
> - **TN (True Negative):** Correctly predicted negative
> - **FP (False Positive):** Incorrectly predicted positive (Type I Error)
> - **FN (False Negative):** Incorrectly predicted negative (Type II Error)
>
> Metrics derived:
> - Accuracy = (TP + TN) / Total
> - Precision = TP / (TP + FP)
> - Recall = TP / (TP + FN)

---

## Part D: Mathematical / Calculation Questions

**D1.** Given a 6×6 input image, a 3×3 kernel, stride=1, and padding=0, calculate the output feature map size.

> **Answer:**
> Output = (Input - Kernel + 2×Padding) / Stride + 1
> Output = (6 - 3 + 2×0) / 1 + 1 = **4×4**

**D2.** A convolutional layer has 64 filters of size 3×3 applied to an input with 3 channels (RGB). How many trainable parameters does this layer have? (Include bias.)

> **Answer:**
> Parameters = (Kernel_H × Kernel_W × Input_Channels + 1_bias) × Num_Filters
> Parameters = (3 × 3 × 3 + 1) × 64 = 28 × 64 = **1,792**

**D3.** Apply 2×2 Max Pooling with stride=2 to the following 4×4 feature map:

```
| 1 | 3 | 2 | 4 |
| 5 | 6 | 7 | 8 |
| 3 | 2 | 1 | 0 |
| 1 | 2 | 3 | 4 |
```

> **Answer:**
> Max Pooling takes the maximum value in each 2×2 window:
> ```
> | max(1,3,5,6) | max(2,4,7,8) |     | 6 | 8 |
> | max(3,2,1,2) | max(1,0,3,4) |  =  | 3 | 4 |
> ```
> Output: **2×2 matrix: [[6, 8], [3, 4]]**

**D4.** A classification model has the following Confusion Matrix:

```
                Predicted Pos    Predicted Neg
Actual Pos          40                10
Actual Neg           5                45
```

Calculate: (a) Accuracy (b) Precision (c) Recall (d) F1 Score

> **Answer:**
> TP=40, FN=10, FP=5, TN=45, Total=100
>
> (a) **Accuracy** = (40+45)/100 = **85%** = 0.85
>
> (b) **Precision** = 40/(40+5) = 40/45 = **88.9%** ≈ 0.889
>
> (c) **Recall** = 40/(40+10) = 40/50 = **80%** = 0.80
>
> (d) **F1 Score** = 2 × (0.889 × 0.80) / (0.889 + 0.80) = 2 × 0.711 / 1.689 = **0.842** = 84.2%

**D5.** Given a 32×32 input image with 1 channel, processed through the following CNN layers, calculate the output size after each layer:

1. Conv: 16 filters, 5×5 kernel, stride=1, padding=0
2. Max Pooling: 2×2, stride=2
3. Conv: 32 filters, 3×3 kernel, stride=1, padding=0

> **Answer:**
> After Conv1: (32-5+0)/1 + 1 = **28×28×16**
> After Pool1: 28/2 = **14×14×16**
> After Conv2: (14-3+0)/1 + 1 = **12×12×32**

**D6.** How many total trainable parameters are in the Conv1 layer from D5? (1 input channel, 16 filters of 5×5)

> **Answer:**
> Parameters = (5 × 5 × 1 + 1) × 16 = 26 × 16 = **416**

---

## Answer Key Summary 答案速查

### Part A (MCQ)
| Q | Ans | Q | Ans | Q | Ans | Q | Ans |
|---|-----|---|-----|---|-----|---|-----|
| 1 | C | 10 | C | 19 | C | 28 | D |
| 2 | B | 11 | C | 20 | B | 29 | B |
| 3 | A | 12 | B | 21 | B | 30 | B |
| 4 | B | 13 | C | 22 | B | 31 | C |
| 5 | B | 14 | C | 23 | B | 32 | B |
| 6 | D | 15 | C | 24 | C | 33 | B |
| 7 | C | 16 | C | 25 | D | | |
| 8 | B | 17 | C | 26 | B | | |
| 9 | A | 18 | C | 27 | C | | |

### Part B (Fill in the Blanks)
| Q | Answer |
|---|--------|
| B1 | Acquisition, Processing |
| B2 | brightness, count/number |
| B3 | Double |
| B4 | Opening |
| B5 | 128 |
| B6 | FAST, BRIEF |
| B7 | Pooling |
| B8 | ReLU |
| B9 | Overfitting |
| B10 | Softmax |
| B11 | Data Augmentation |
| B12 | correct predictions (TP+TN) |
| B13 | False Positive |
| B14 | Adaptive |
| B15 | Convolutional, Fully |

---

> 📅 Generated: 2026-02-17
> 📚 Sources: Course slides W1-5, Quiz 1, research papers, lab code
> 📝 Total: 33 MCQ + 15 Fill-in-the-blanks + 7 Short Answer + 6 Math = **61 questions**
