# Week 4: 卷积神经网络简介 (Introduction to Convolutional Neural Networks)

> Source: `Week 4 - Introduction to Convolutional Neural Networks (CNNs)1.pptx`
> Total slides: 37
> Instructor: Stephin Rachel Thomas | Feb 05, 2026

---

## 1. 人工神经网络与图像分类 (Artificial Neural Networks & Image Classification)

![Page 1](week4_cnn_intro_slides_pages/page_001.png)

- **Convolutional Neural Networks (CNN) in Machine Vision** — 通过深度学习变革视觉识别
- Transforming visual recognition through deep learning.

![Page 2](week4_cnn_intro_slides_pages/page_002.png)

**Today's Topics:**

- Artificial Neural Networks — 人工神经网络
- Disadvantages of simple ANN for Image classification — 简单ANN用于图像分类的缺点
- Introduction to CNN — CNN简介
- CNN architecture — CNN架构
- Deep dive into CNN layers — 深入CNN各层
- Application of CNN — CNN的应用
- Performance Evaluation Metrics — 性能评估指标

![Page 3](week4_cnn_intro_slides_pages/page_003.png)

**What are Artificial Neural Networks?** — **什么是人工神经网络？**

1. **Biological Inspiration** — ANNs are inspired by the structure and function of the human brain, composed of interconnected nodes called neurons. — **生物启发** — ANN受人脑结构和功能的启发，由称为神经元的互连节点组成。
2. **Learning Through Data** — These networks learn by analyzing large datasets, adjusting the connections between neurons to improve their performance. — **通过数据学习** — 这些网络通过分析大型数据集来学习，调整神经元之间的连接以提高性能。
3. **Pattern Recognition** — ANNs are particularly effective at recognizing complex patterns in data, making them ideal for image classification. — **模式识别** — ANN在识别数据中的复杂模式方面特别有效，使其成为图像分类的理想选择。

![Page 4](week4_cnn_intro_slides_pages/page_004.png)

- **Classification using Traditional Methods** — 展示决策树方法的传统分类流程图
- Decision-tree method — 决策树方法

![Page 5](week4_cnn_intro_slides_pages/page_005.png)

- **ANN for Image Classification** — 展示用ANN对图像进行分类的流程：输入层接收像素、隐藏层提取特征、输出层给出类别

![Page 6](week4_cnn_intro_slides_pages/page_006.png)

**Limitation of ANN for Image Classification:** — **ANN用于图像分类的局限性：**

- 1000 * 1000px
- High computational cost — 高计算成本
- Over-fitting problem — 过拟合问题
- Longer training time — 训练时间更长

---

## 2. CNN简介与架构 (Introduction to CNN & Architecture)

![Page 7](week4_cnn_intro_slides_pages/page_007.png)

**Convolutional Neural Network (CNN):** — **卷积神经网络（CNN）：**

1. **Definition** — A deep learning model designed for processing images to identify patterns and make decisions. — **定义** — 一种专为处理图像以识别模式和做出决定而设计的深度学习模型。
2. **Objective** — Solve complex visual tasks with deep learning. — **目标** — 用深度学习解决复杂的视觉任务。
3. **Benefits:** — **优势：**
   - Handles high-dimensional, structured data like images, videos and audio. — 处理图像、视频和音频等高维结构化数据。
   - Hierarchical feature learning. — 层次化特征学习。
   - Robust to translation of object. — 对物体平移具有鲁棒性。

![Page 8](week4_cnn_intro_slides_pages/page_008.png)

**CNN Architecture:** — **CNN架构：**

- CNNs typically consist of an input layer, multiple hidden layers, and an output layer. — CNN通常由输入层、多个隐藏层和输出层组成。
- The hidden layers include a series of convolutional layers, pooling layers and fully connected layers. — 隐藏层包括一系列卷积层、池化层和全连接层。
- Each layer performs distinct operations: Convolutional layers apply a convolution operation, Pooling layers perform down-sampling, Fully connected layers compute the class scores. — 每层执行不同的操作：卷积层执行卷积运算，池化层执行下采样，全连接层计算类别分数。

![Page 9](week4_cnn_intro_slides_pages/page_009.png)

**Key Components of CNN:** — **CNN的关键组件：**

- **Convolutional Layers** — Extract spatial features from input images. — **卷积层** — 从输入图像中提取空间特征。
- **Pooling Layers** — Reduce spatial dimensions, simplify computation. — **池化层** — 减少空间维度，简化计算。
- **Fully Connected Layers** — Integrate features for final classification. — **全连接层** — 整合特征用于最终分类。

---

## 3. 卷积层详解 (Convolutional Layers Deep Dive)

### 3.1 卷积层原理 (Convolutional Layer Fundamentals)

![Page 10](week4_cnn_intro_slides_pages/page_010.png)

**Deep Dive into Convolutional Layers:** — **深入卷积层：**

- In these layers, small, learnable filters slide over the input data (like images) to extract features such as edges, textures, and shapes. — 在这些层中，小的可学习滤波器在输入数据（如图像）上滑动，提取边缘、纹理和形状等特征。
- Each filter in a convolutional layer detects different features, and multiple layers work together to capture increasingly complex aspects of the data. — 卷积层中的每个滤波器检测不同的特征，多个层协同工作以捕获数据中越来越复杂的方面。
- The convolutional layers thus play a crucial role in feature detection and representation, enabling CNNs to effectively perform tasks like image recognition and classification. — 因此卷积层在特征检测和表示中起着关键作用，使CNN能够有效执行图像识别和分类等任务。

![Page 11](week4_cnn_intro_slides_pages/page_011.png)

**CNN Fundamentals:** — **CNN基础：**

- The basic principle of a Convolutional Neural Network (CNN) is to automatically learn and extract hierarchical features from input data, typically images, through the use of convolutional layers. — 卷积神经网络（CNN）的基本原理是通过使用卷积层，从输入数据（通常是图像）中自动学习和提取分层特征。

### 3.2 特征图与卷积运算 (Feature Maps & Convolution Operation)

![Page 12](week4_cnn_intro_slides_pages/page_012.png)

**Convolutional Layers — Feature Maps:** — **卷积层 — 特征图：**

- Convolutional layers help the network focus on only the most important features — 卷积层帮助网络只关注最重要的特征
- Not all the pixel information in the image is relevant for training the model — 图像中并非所有像素信息都与训练模型相关
- Improves performance and accuracy — 提高性能和准确度

![Page 13](week4_cnn_intro_slides_pages/page_013.png)

- **Convolution Operation** — 展示卷积运算过程：输入图像通过滤波器（卷积算子）生成输出图像

![Page 14](week4_cnn_intro_slides_pages/page_014.png)

- **Convolution Operation** — 展示5×5输入矩阵与3×3滤波器执行卷积运算的详细步骤，逐步填充输出矩阵

![Page 15](week4_cnn_intro_slides_pages/page_015.png)

- **Convolution Operation** — 展示步幅（Stride）在卷积运算中的作用：滤波器以指定步长在输入上滑动

### 3.3 滤波器尺寸、步幅与填充 (Filter Size, Stride & Padding)

![Page 16](week4_cnn_intro_slides_pages/page_016.png)

**Convolutional Layers — Key Hyperparameters:** — **卷积层 — 关键超参数：**

- The **filter size** determines the extent of the input data that each filter covers, affecting the granularity of the features detected; smaller filters capture fine details, while larger filters identify broader patterns. — **滤波器大小**决定每个滤波器覆盖输入数据的范围，影响检测到的特征粒度；较小的滤波器捕获精细细节，较大的滤波器识别更宏观的模式。
- **Stride**, the step size with which filters move across the input, influences the overlap of receptive fields and the size of the output feature map; larger strides result in smaller, more abstract feature maps. — **步幅**，滤波器在输入上移动的步长，影响感受野的重叠和输出特征图的大小；较大的步幅产生更小、更抽象的特征图。
- **Padding**, the addition of zeroes around the input border, allows control over the spatial dimensions of the output, preserving edge information and enabling deeper layers to build a spatial hierarchy of increasingly complex and abstract features. — **填充**，在输入边界周围添加零，允许控制输出的空间维度，保留边缘信息并使更深层能够构建越来越复杂和抽象特征的空间层次结构。

### 3.4 输出尺寸计算 (Output Size Calculation)

![Page 17](week4_cnn_intro_slides_pages/page_017.png)

**Convolutional Layer – Output Image Size:** — **卷积层 — 输出图像尺寸：**

- The image output size is given by the following — 图像输出尺寸由以下公式给出
- **(N – F + 2P) / S + 1**
  - F: size of filter — F：滤波器大小
  - S: stride — S：步幅
  - N: size of image — N：图像大小
  - P: amount of padding — P：填充量

---

## 4. 池化层 (Pooling Layers)

![Page 18](week4_cnn_intro_slides_pages/page_018.png)

**Pooling Layers:** — **池化层：**

- Responsible for reducing the spatial size of the feature maps generated by convolutional layers — 负责减小卷积层生成的特征图的空间尺寸
- By performing operations such as max or average pooling, they down sample the input features, which helps to decrease the computational load and the number of parameters in the network — 通过执行最大池化或平均池化等操作，它们对输入特征进行下采样，有助于减少网络的计算负载和参数数量
- This reduction also contributes to making the network more tolerant to variations and distortions in the input data, enhancing its ability to generalize. — 这种减少还有助于使网络对输入数据中的变化和失真更具容忍性，增强其泛化能力。

![Page 19](week4_cnn_intro_slides_pages/page_019.png)

- The pooling layer reduces the spatial dimensionality of the input feature map. — 池化层减少输入特征图的空间维度。

![Page 20](week4_cnn_intro_slides_pages/page_020.png)

---

## 5. 全连接层与展平 (Fully Connected Layers & Flattening)

### 5.1 全连接层 (Fully Connected Layers)

![Page 21](week4_cnn_intro_slides_pages/page_021.png)

**Fully Connected Layers:** — **全连接层：**

- Where the high-level reasoning based on extracted features occurs. Transform high-dimensional feature maps into a probability distribution — 基于提取特征进行高级推理的地方。将高维特征图转换为概率分布
- After convolutional and pooling layers extract and down sample features, fully connected layers integrate these features to make predictions or classifications. — 在卷积层和池化层提取并下采样特征后，全连接层整合这些特征进行预测或分类。
- Each neuron in these layers is connected to all activations in the previous layer, allowing the network to consider the entire representation of the input data. — 这些层中的每个神经元都与前一层的所有激活相连，使网络能够考虑输入数据的整体表示。

### 5.2 展平操作 (Flattening)

![Page 22](week4_cnn_intro_slides_pages/page_022.png)

- Convolutional and pooling layers produce feature maps — 卷积层和池化层生成特征图
- Feature maps are multi-dimensional arrays — 特征图是多维数组
- Flattening converts feature maps to one-dimensional vector — 展平将特征图转换为一维向量
- Concatenates elements along depth dimension — 沿深度维度拼接元素
- Enables feeding into fully connected layers — 使其能够输入全连接层

### 5.3 权重矩阵与偏置向量 (Weight Matrix & Bias Vector)

![Page 23](week4_cnn_intro_slides_pages/page_023.png)

**Weight Matrix and Bias Vector:** — **权重矩阵和偏置向量：**

- Foundation for deep learning algorithms. — 深度学习算法的基础。
- Fully connected layer have **weight matrix (W)** and **bias vector (b)** — 全连接层有**权重矩阵（W）**和**偏置向量（b）**
- Weight matrix: (n x m), n = neurons, m = flattened vector length — 权重矩阵：(n x m)，n = 神经元数，m = 展平向量长度
- Bias vector length: number of neurons in the current layer — 偏置向量长度：当前层的神经元数量
- **Learnable parameters** of the fully connected layer — 全连接层的**可学习参数**
- Enable transformation and introduce **nonlinearity** — 启用变换并引入**非线性**
- Input vector is multiplied by weight matrix and bias vector is added — 输入向量乘以权重矩阵并加上偏置向量
- Operation: **W * input + b** — 运算：**W * input + b**
- Output represents weighted sum of input from previous layer — 输出表示前一层输入的加权和

---

## 6. 激活函数与输出层 (Activation Functions & Output Layer)

![Page 24](week4_cnn_intro_slides_pages/page_024.png)

- Activation function determines if a neuron fires — 激活函数决定神经元是否激活
- Introduces nonlinearity to the network — 为网络引入非线性
- Applied after convolution layer, after each fully connected layer and output layer allowing the network to learn and represent complex patterns in the data — 在卷积层之后、每个全连接层之后和输出层应用，使网络能够学习和表示数据中的复杂模式
- Most commonly used activation function is **ReLU** — 最常用的激活函数是**ReLU**

![Page 25](week4_cnn_intro_slides_pages/page_025.png)

**Output Layer:** — **输出层：**

- The final layer generates predictions — 最后一层生成预测
- Neurons in the last layer match number of classes — 最后一层的神经元数量与类别数匹配
- Activation function differs in final layer — 最后一层的激活函数不同
- **Softmax** commonly used for multi-class classification — **Softmax**常用于多类分类
- Highest probability neuron represents prediction — 最高概率的神经元代表预测结果

---

## 7. 反向传播与CNN处理流程 (Back Propagation & CNN Pipeline)

![Page 26](week4_cnn_intro_slides_pages/page_026.png)

**Back Propagation:** — **反向传播：**

- A supervised learning algorithm used for training neural networks. — 一种用于训练神经网络的监督学习算法。
- It happens only during training — 仅在训练期间发生
- Optimizes the parameters (weights and biases) of a neural network by minimizing the error between the predicted output and the actual target value. — 通过最小化预测输出与实际目标值之间的误差来优化神经网络的参数（权重和偏置）。
- Basic Steps are: — 基本步骤是：
  1. Feed a sample to the network — 向网络输入一个样本
  2. Calculate the mean squared error — 计算均方误差
  3. Calculate the error term of each output neuron — 计算每个输出神经元的误差项
  4. Iteratively calculate the error terms in the hidden layers — 迭代计算隐藏层中的误差项
  5. Apply the delta rule — 应用delta规则
  6. Adjust the weights — 调整权重

![Page 27](week4_cnn_intro_slides_pages/page_027.png)

- **Input** — Raw image data enters the network. — **输入** — 原始图像数据进入网络。
- **Feature Extraction** — Convolutional layers detect edges, shapes, textures. — **特征提取** — 卷积层检测边缘、形状、纹理。
- **Down-sampling** — Pooling layers reduce data complexity. — **下采样** — 池化层降低数据复杂度。
- **Classification** — Fully connected layers determine image content. — **分类** — 全连接层确定图像内容。

---

## 8. CNN应用与现实影响 (Applications & Real-World Impact)

![Page 28](week4_cnn_intro_slides_pages/page_028.png)

**Applications of CNNs:** — **CNN的应用：**

- CNNs have revolutionized the field of computer vision. Applications include image and video recognition, image segmentation, object detection, face recognition, and automated medical diagnosis. They are also used in self-driving cars for detecting objects and pedestrians. — CNN已经彻底改变了计算机视觉领域。应用包括图像和视频识别、图像分割、目标检测、人脸识别和自动化医疗诊断。它们还用于自动驾驶汽车中检测物体和行人。
- Can be used for tasks like: — 可用于以下任务：
  - Image classification — 图像分类
  - Object detection — 目标检测
  - Semantic and instance segmentation — 语义分割和实例分割
  - Multiple object tracking — 多目标跟踪
  - Re-identification — 重识别
  - Any vision task — 任何视觉任务

![Page 29](week4_cnn_intro_slides_pages/page_029.png)

| Domain              | Application                          | 领域              | 应用             |
| ------------------- | ------------------------------------ | ------------------- | -------------------- |
| Medical Imaging     | Anomaly detection in scans           | 医学影像     | 扫描中的异常检测           |
| Autonomous Vehicles | Real-time environment perception     | 自动驾驶 | 实时环境感知     |
| Facial Recognition  | Security and user authentication     | 人脸识别  | 安全和用户认证     |
| Quality Control     | Defect detection in manufacturing    | 质量控制     | 制造中的缺陷检测    |

---

## 9. 性能评估指标 (Performance Evaluation Metrics)

### 9.1 分类、回归与聚类评估概览 (Classification, Regression & Clustering Overview)

![Page 30](week4_cnn_intro_slides_pages/page_030.png)

**Performance Evaluation Metrics — Classification, Regression or Clustering?** — 展示三类任务的评估指标对比表：聚类（距离度量）、回归（MAE/RMSE等）、分类（Accuracy/Precision/Recall/F1/AUC）

Ref: https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/evaluate-model?view=azureml-api-2

### 9.2 准确率与精确率 (Accuracy & Precision)

![Page 31](week4_cnn_intro_slides_pages/page_031.png)

- **Accuracy** measures the proportion of total predictions (both positive and negative) that the model got correct, offering a general sense of its performance across all classes. — **准确率**衡量模型正确预测的总比例（包括正例和反例），提供其在所有类别中性能的总体感觉。
- **Precision** assesses the accuracy of the positive predictions made by a CNN, specifically calculating the proportion of true positive predictions out of all positive predictions made (true and false positives), which is crucial in scenarios where false positives have significant consequences. — **精确率**评估CNN正预测的准确性，具体计算真正例占所有正预测（真正例和假正例）的比例，在假正例产生重大后果的场景中至关重要。

### 9.3 召回率、F1分数与ROC (Recall, F1 Score & ROC)

![Page 32](week4_cnn_intro_slides_pages/page_032.png)

- **F1-Score** = 2 × (Precision × Recall) / (Precision + Recall) — **F1分数** = 2 × (精确率 × 召回率) / (精确率 + 召回率)
  - Harmonic mean of precision and recall — 精确率和召回率的调和平均数
  - Balances both metrics into a single score — 将两个指标平衡为一个单一分数
- **ROC Curve** — Receiver Operating Characteristic — **ROC曲线** — 接收者操作特征曲线
  - Plots True Positive Rate vs False Positive Rate — 绘制真正例率vs假正例率
  - **AUC** (Area Under Curve) — closer to 1.0 = better model — **AUC**（曲线下面积）— 越接近1.0 = 模型越好
  - Diagonal line = random chance (AUC = 0.5) — 对角线 = 随机猜测（AUC = 0.5）

### 9.4 混淆矩阵 (Confusion Matrix)

![Page 33](week4_cnn_intro_slides_pages/page_033.png)

**Confusion Matrix** — 展示混淆矩阵结构图：Predicted vs Actual 的2×2表格，标注TP/TN/FP/FN四个象限

- A confusion matrix is a tool used in machine learning and statistical classification to evaluate the performance of a classification model. It provides a summary of the prediction results on a classification problem. The matrix itself is a table that compares the actual target values with the predicted values. — 混淆矩阵是机器学习和统计分类中用于评估分类模型性能的工具。它提供分类问题预测结果的摘要。矩阵本身是一个将实际目标值与预测值进行比较的表格。
- **True Positives (TP):** The number of correct positive predictions. — **真正例（TP）：**正确的正预测数量。
- **True Negatives (TN):** The number of correct negative predictions. — **真反例（TN）：**正确的负预测数量。
- **False Positives (FP):** The number of incorrect positive predictions. — **假正例（FP）：**错误的正预测数量。
- **False Negatives (FN):** The number of incorrect negative predictions. — **假反例（FN）：**错误的负预测数量。

### 9.5 评估指标公式 (Metric Formulas)

![Page 34](week4_cnn_intro_slides_pages/page_034.png)

**Performance Evaluation Metrics — Formulas** — 展示Accuracy、Precision、Recall和F1 Score的计算公式

---

## 10. 伦理考虑与下周预告 (Ethical Considerations & Next Week Preview)

### 10.1 伦理考虑与AI偏见 (Ethical Considerations & Bias in CNNs)

![Page 35](week4_cnn_intro_slides_pages/page_035.png)

**Ethical Considerations and Bias in CNNs:** — **CNN的伦理考虑和偏见：**

- **Privacy:** Privacy concerns arise when CNN models process sensitive personal data, such as facial images or medical records, potentially leading to unauthorized access or misuse of personal information if data security is not adequately maintained. This also causes issues when collecting and annotating data. — **隐私：**当CNN模型处理敏感个人数据（如面部图像或医疗记录）时，如果数据安全未得到充分维护，可能导致未经授权的访问或个人信息的滥用。这也在收集和标注数据时产生问题。
- **Surveillance:** The use of CNNs in surveillance systems can enhance public safety and security by identifying threats more efficiently; however, it also raises ethical issues related to mass surveillance and the potential infringement on individuals' rights to privacy and freedom. — **监控：**在监控系统中使用CNN可以通过更有效地识别威胁来增强公共安全；然而，它也引发了与大规模监控和可能侵犯个人隐私和自由权利相关的伦理问题。
- **Bias in AI:** particularly in CNNs, occurs when the data used to train these models contain inherent prejudices, leading to skewed or unfair outcomes in decision-making processes, often reinforcing existing societal stereotypes and discriminations. — **AI偏见：**尤其在CNN中，当用于训练这些模型的数据包含固有偏见时，会导致决策过程中的偏斜或不公平结果，往往强化现有的社会刻板印象和歧视。

### 10.2 参考文献 (References)

![Page 36](week4_cnn_intro_slides_pages/page_036.png)

1. https://austingwalters.com/edge-detection-in-computer-vision
2. https://www.kaggle.com/datasets/tongpython/cat-and-dog
3. Google search
4. https://gamma.app/#images
5. https://www.semanticscholar.org/paper/Cats-and-dogs-Parkhi-Vedaldi/84b50ebe85f7a1721800125e7882fce8c45b5c5a
6. https://www.simplilearn.com/tutorials/deep-learning-tutorial/convolutional-neural-network
7. https://www.analyticsvidhya.com/blog/2021/08/beginners-guide-to-convolutional-neural-network-with-implementation-in-python/
8. https://learn.microsoft.com/en-us/azure/machine-learning/component-reference/evaluate-model?view=azureml-api-2

### 10.3 下周预告 (Next Week Preview)

![Page 37](week4_cnn_intro_slides_pages/page_037.png)

**Next Week Topics:** — **下周主题：**

- CNN Training Process — CNN训练过程
- Loss Function — 损失函数
- Different types of Activation Functions — 不同类型的激活函数
- Back propagation Algorithm — 反向传播算法
- Common Problems in Machine Vision — 机器视觉中的常见问题
- CNN Solutions — CNN解决方案
