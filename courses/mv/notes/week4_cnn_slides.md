# Week 4: 卷积神经网络 (Introduction to CNN)

> Source: `Week 4 - Introduction to Convolutional Neural Networks (CNNs)1.pptx`
> Total slides: 37
> Instructor: Stephin Rachel Thomas | Feb 05, 2026

---

## 1. 人工神经网络 (Artificial Neural Networks)

### 1.1 什么是 ANN (What are ANNs)

1. **Biological Inspiration:** Inspired by human brain, composed of interconnected neurons
2. **Learning Through Data:** Learn by analyzing large datasets, adjusting connections
3. **Pattern Recognition:** Effective at recognizing complex patterns, ideal for image classification

![Image 0](week4_cnn_slides_images/slide03_img1.png)

> **📝 笔记:**
>
> **ANN 三大特点:** 模仿大脑神经元结构、通过数据学习调整连接权重、擅长复杂模式识别

### 1.2 传统分类方法 (Traditional Classification)

Decision-tree method

![Picture 7](week4_cnn_slides_images/slide04_img1.png)
![Picture 16](week4_cnn_slides_images/slide04_img2.jpg)

### 1.3 ANN 图像分类的局限性 (Limitations of ANN)

For a 1000×1000px image:

- High computational cost
- Over-fitting problem
- Longer training time

![Picture 5](week4_cnn_slides_images/slide06_img1.jpg)

> **📝 笔记:**
>
> **ANN 处理图像的问题:** 1000×1000 像素 = 100 万个输入节点, 导致计算成本高、过拟合严重、训练时间长。这就是 CNN 诞生的原因。

---

## 2. CNN 概述 (CNN Overview)

### 2.1 定义与优势 (Definition & Benefits)

1. **Definition:** A deep learning model designed for processing images to identify patterns and make decisions
2. **Objective:** Solve complex visual tasks with deep learning
3. **Benefits:**
   - Handles high-dimensional, structured data (images, videos, audio)
   - Hierarchical feature learning
   - Robust to translation of object

![Image 0](week4_cnn_slides_images/slide07_img1.png)

> **📝 笔记:**
>
> **CNN 优势:** 处理高维结构化数据、分层特征学习(底层→高层)、对目标平移具有鲁棒性。解决了 ANN 处理图像的三大问题。

### 2.2 CNN 架构 (Architecture)

- Input layer → Multiple hidden layers → Output layer
- Hidden layers: **Convolutional layers** + **Pooling layers** + **Fully connected layers**
- Each layer performs distinct operations:
  - Convolutional layers: apply convolution operation
  - Pooling layers: perform down-sampling
  - Fully connected layers: compute class scores

![Picture 3](week4_cnn_slides_images/slide08_img1.png)

> **📝 笔记:**
>
> **CNN 三层核心:** 卷积层(提取特征) → 池化层(降维) → 全连接层(分类)

---

## 3. 卷积层详解 (Convolutional Layers)

### 3.1 基本原理 (Fundamentals)

- CNN automatically learns and extracts hierarchical features from input data through convolutional layers
- Feature Maps: Focus on only the most important features, not all pixel information
- Improves performance and accuracy

![Picture 2](week4_cnn_slides_images/slide11_img1.png)
![Picture 2](week4_cnn_slides_images/slide12_img1.jpg)
![Picture 4](week4_cnn_slides_images/slide12_img3.png)

### 3.2 卷积运算 (Convolution Operation)

Filter × Input Image → Output Image (Feature Map)

![Picture 2](week4_cnn_slides_images/slide13_img1.png)
![Picture 2](week4_cnn_slides_images/slide14_img1.png)
![Picture 2](week4_cnn_slides_images/slide15_img1.png)

### 3.3 输出尺寸计算 (Output Image Size)

![Picture 1](week4_cnn_slides_images/slide17_img1.png)

> **📝 笔记:**
>
> **卷积层核心:**
>
> - **作用:** 自动从输入数据中学习并提取分层特征
> - **特征图 (Feature Map):** 卷积操作的输出, 只保留最重要的特征信息
> - **运算过程:** 滤波器(kernel)在图像上滑动, 逐元素相乘后求和
>
> **💡 提示:** 输出尺寸公式需要掌握, 考试可能会考计算题

---

## 4. 池化层 (Pooling Layers)

- Reduces the spatial dimensionality of the input feature map
- Types: Max Pooling, Average Pooling

![Picture 2](week4_cnn_slides_images/slide19_img1.png)
![Picture 2](week4_cnn_slides_images/slide20_img1.png)
![Picture 2](week4_cnn_slides_images/slide20_img2.gif)

> **📝 笔记:**
>
> **池化层:** 降低特征图的空间维度, 减少计算量。最常用 Max Pooling(取最大值)。

---

## 5. 全连接层 (Fully Connected Layers)

### 5.1 展平 (Flattening)

- Converts multi-dimensional feature maps to **one-dimensional vector**
- Concatenates elements along depth dimension
- Enables feeding into fully connected layers

![Picture 2](week4_cnn_slides_images/slide22_img1.png)

### 5.2 权重矩阵与偏置 (Weight Matrix and Bias)

- Weight matrix (W): `n × m`, n=neurons, m=flattened vector length
- Bias vector length: number of neurons in current layer
- Operation: `W * input + b`

![Picture 2](week4_cnn_slides_images/slide23_img1.png)

> **📝 笔记:**
>
> **全连接层流程:** 展平(多维→一维) → 权重矩阵乘法 + 偏置 → 输出分数
>
> - 展平: 将特征图拉成一维向量
> - `W * input + b`: 加权求和 + 偏置, 可学习参数

---

## 6. 激活函数与输出层 (Activation & Output)

### 6.1 激活函数 (Activation Functions)

- Determines if a neuron fires, introduces nonlinearity
- Applied after convolution layer, fully connected layer, and output layer
- Most commonly used: **ReLU**

![Picture 6](week4_cnn_slides_images/slide24_img1.png)

### 6.2 输出层 (Output Layer)

- Neurons match number of classes
- **Softmax** commonly used for multi-class classification
- Highest probability neuron = prediction

![Picture 2](week4_cnn_slides_images/slide25_img1.png)

> **📝 笔记:**
>
> **激活函数:** 引入非线性, 使网络能学习复杂模式。隐藏层常用 ReLU, 输出层多类分类用 Softmax。

---

## 7. 反向传播 (Back Propagation)

A supervised learning algorithm, happens **only during training**. Optimizes weights and biases by minimizing error.

**Six steps:**

1. Feed a sample to the network
2. Calculate the mean squared error
3. Calculate the error term of each output neuron
4. Iteratively calculate the error terms in the hidden layers
5. Apply the delta rule
6. Adjust the weights

> **📝 笔记:**
>
> **反向传播:** 只在训练时发生。前向传播→计算误差→从输出层到隐藏层逐层计算误差项→更新权重。
>
> **💡 提示:** 理解反向传播的六个步骤是考试重点

---

## 8. CNN 处理流程与应用 (Processing & Applications)

### 8.1 图像处理流程 (Image Processing in CNNs)

1. **Input:** Raw image data
2. **Feature Extraction:** Convolutional layers detect edges, shapes, textures
3. **Down-sampling:** Pooling layers reduce data complexity
4. **Classification:** Fully connected layers determine image content

### 8.2 应用 (Applications)

- Image classification, Object detection
- Semantic and instance segmentation
- Multiple object tracking, Re-identification
- Medical Imaging, Autonomous Vehicles, Facial Recognition, Quality Control

![Image 0](week4_cnn_slides_images/slide29_img1.png)

> **📝 笔记:**
>
> **CNN 处理流程:** 原始图像 → 卷积提取特征 → 池化降维 → 全连接分类
> **应用:** 图像分类、目标检测、语义分割、医学影像、自动驾驶、人脸识别、质量控制

---

## 9. 性能评估指标 (Performance Evaluation Metrics)

### 9.1 核心指标 (Key Metrics)

- **Accuracy:** Proportion of total correct predictions
- **Precision:** True positives / (True positives + False positives) — important when FP is costly
- **Recall (Sensitivity):** True positives / (True positives + False negatives) — important when FN is costly
- **F1 Score:** Harmonic mean of precision and recall
- **ROC/AUC:** True positive rate vs false positive rate across thresholds

### 9.2 混淆矩阵 (Confusion Matrix)

|                     | Predicted Positive  | Predicted Negative  |
| ------------------- | ------------------- | ------------------- |
| **Actual Positive** | TP (True Positive)  | FN (False Negative) |
| **Actual Negative** | FP (False Positive) | TN (True Negative)  |

![Picture 2](week4_cnn_slides_images/slide33_img1.png)
![Picture 8](week4_cnn_slides_images/slide34_img1.png)

Ref: https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/evaluate-model?view=azureml-api-2

> **📝 笔记:**
>
> **评估指标:**
>
> - **准确率(Accuracy):** 整体正确率
> - **精确率(Precision):** 预测为正的样本中真正为正的比例 (假阳性代价高时重要)
> - **召回率(Recall):** 所有正样本中被正确识别的比例 (假阴性代价高时重要)
> - **F1:** 精确率和召回率的调和平均
> - **混淆矩阵:** TP/TN/FP/FN 四个关键值, 是计算所有指标的基础
>
> **💡 提示:** 理解 TP/TN/FP/FN 是理解所有评估指标的基础, 考试必考

---

## 10. 下周主题 (Next Week)

CNN Training Process, Loss Function, Activation Functions, Back Propagation Algorithm, Common Problems in Machine Vision, CNN Solutions

---
