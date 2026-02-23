# Week 3: 卷积神经网络 (Convolutional Neural Networks)

> Source: `03_CST8506_CNN.pdf`
> Total slides: 35
> Instructor: Dr. Anu Thomas

---

## 1. 神经网络与多层感知机回顾 (Review of ANN and MLP)

![Page 2](week3_cnn_slides_pages/page_002.png)

**Agenda**

- Recap on
- ANN
- Perceptron, MLP
- CNN

![Page 3](week3_cnn_slides_pages/page_003.png)

**Single-layer Perceptron Network**
Taken from: https://towardsdatascience.com/multi-layer-neural-networks-with-sigmoid-function-deep-learning-for-rookies-2-bf464f09eb7f

> **📝 Notes:**
>
> **📌 What:**
> **(1) Perceptron vs. MLP (感知机 vs 多层感知机):**
>
> A perceptron is a single neuron that takes inputs, multiplies them by weights, sums them up, and passes them through an activation function. An MLP (Multi-Layer Perceptron) connects multiple perceptrons in layers (input, hidden, output) to learn complex, non-linear patterns.
>
> > 感知机是单个神经元，它接收输入，乘以权重，求和，并通过激活函数。多层感知机 (MLP) 将多个感知机分层连接（输入层、隐藏层、输出层），以学习复杂的非线性模式。
>
> **🎯 Why:**
> **(1) Why need hidden layers? (为什么需要隐藏层？):**
>
> A single perceptron can only solve linearly separable problems (like AND, OR). It fails on XOR. Hidden layers allow the network to combine linear boundaries into complex, non-linear decision spaces.
>
> > 单个感知机只能解决线性可分问题（如 AND, OR）。它无法解决 XOR（异或）问题。隐藏层允许网络将线性边界组合成复杂的非线性决策空间。
>
> **⚖️ Compare:**
> **(1) Perceptron vs MLP:**
>
> | Feature      | Perceptron                   | Multi-Layer Perceptron (MLP) |
> | ------------ | ---------------------------- | ---------------------------- |
> | Architecture | One neuron, no hidden layers | One or more hidden layers    |
> | Problem type | Linearly separable only      | Non-linear boundaries        |
>
> > | 特性     | 感知机             | 多层感知机 (MLP) |
> > | -------- | ------------------ | ---------------- |
> > | 架构     | 单神经元，无隐藏层 | 一个或多个隐藏层 |
> > | 问题类型 | 仅限线性可分       | 非线性边界       |

---

## 2. 激活函数 (Activation Functions)

![Page 4](week3_cnn_slides_pages/page_004.png)

**Activation Functions**

- Sometimes, activation function is as simple as: `[Mathematical formula - see image above]`
- Most commonly used Activation function is the Sigmoid function: $\sigma(z) = \frac{1}{1 + e^{-z}}$

![Page 5](week3_cnn_slides_pages/page_005.png)

**Activation Functions**

- **Sigmoid**: Maps values between 0 and 1, often used in binary classification.
- **Tanh**: $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$
- **ReLU (Rectified Linear Unit)**: Only outputs positive values. $f(x) = \max(0, x)$
- **Softmax**: Used in multi-class classification, it outputs probabilities summing up to 1.

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Why do we need activation functions? (为什么我们需要激活函数？):**
>
> Without activation functions, no matter how many layers an MLP has, the output would simply be a linear transformation of the input. Activation functions introduce non-linearity, allowing the network to learn complex patterns.
>
> > 如果没有激活函数，无论MLP有多少层，输出仅仅是输入的线性变换。激活函数引入了非线性，允许网络学习复杂的模式。
>
> **💡 Intuition:**
> **(1) The "Switch" Analogy (开关类比):**
>
> Think of a neuron like a light switch with a dimmer. The activation function decides how bright the light should be based on the incoming voltage. ReLU is an abrupt switch that only dims up for positive voltage.
>
> > 把神经元想象成带有调光器的电灯开关。激活函数根据输入电压决定灯应该多亮。ReLU是一个突然的开关，只在正电压时变亮。
>
> **⚖️ Compare:**
> **(1) Sigmoid vs Tanh vs ReLU:**
>
> | Activation  | Range   | Pros/Cons                                                                         | Use Case                                    |
> | ----------- | ------- | --------------------------------------------------------------------------------- | ------------------------------------------- |
> | **Sigmoid** | [0, 1]  | Vanishing gradients problem                                                       | Binary classification (output layer)        |
> | **Tanh**    | [-1, 1] | Zero-centered, still has vanishing gradients                                      | Hidden layers (usually better than Sigmoid) |
> | **ReLU**    | [0, ∞)  | Fast, no vanishing gradient for positive values, but can suffer from "dying ReLU" | Hidden layers (Standard choice for CNNs)    |
>
> > | 激活函数    | 值域    | 优缺点                                         | 用途                     |
> > | ----------- | ------- | ---------------------------------------------- | ------------------------ |
> > | **Sigmoid** | [0, 1]  | 梯度消失问题                                   | 二分类 (输出层)          |
> > | **Tanh**    | [-1, 1] | 零点中心化，仍有梯度消失问题                   | 隐藏层 (通常优于Sigmoid) |
> > | **ReLU**    | [0, ∞)  | 速度快，正值无梯度消失，但可能有"ReLU死亡"问题 | 隐藏层 (CNN的标准选择)   |
>
> **⚠️ Pitfall:**
> **(1) Softmax vs Sigmoid (Softmax 与 Sigmoid 的混淆):**
>
> Sigmoid is for independent probabilities (A or not A). Softmax is for mutually exclusive classes (is it A, B, or C?) because it forces all probabilities to sum up to 1.
>
> > Sigmoid用于独立的概率（是A还是非A）。Softmax用于互斥的分类（是A、B、还是C？），因为它强制所有类别的概率总和为1。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual):**
>
> "Which activation function is best for the hidden layers of a deep CNN?" → ReLU, because it mitigates the vanishing gradient problem and computes efficiently.
>
> > "哪种激活函数最适合深度CNN的隐藏层？" → ReLU，因为它减轻了梯度消失问题并且计算效率高。

---

## 3. 神经网络架构 (Types of Neural Networks)

### 3.1 多层感知机 (Multi-layer Perceptron)

![Page 6](week3_cnn_slides_pages/page_006.png)

**Multi-layer Perceptron**
Some of the parameters:

- `hidden_layer_sizes`: specify the number of layers and the number of nodes in each layer. `hidden_layer_sizes=(5,3)` means we have 2 hidden layers, first one with 5 nodes and second one with 3 nodes.
- `activation`: activation function

![Page 7](week3_cnn_slides_pages/page_007.png)

**Types of Neural Networks**

- **Perceptron**: single neuron. Single layer perceptron can only learn linearly separable problems.
- **Multi-layer Perceptron**: Input layer, one or more hidden layers, output layer.
- **Feed-forward NN**: Data flows only in one direction, without any feedback loops or recurrent connections. Uses back propagation for training. Repeatedly adjust the weights to minimize the difference between actual output and the desired output.
- **Convolutional NN**: Utilized for computer vision etc.
- **Recurrent NN**: For text processing.

### 3.2 从多层感知机到卷积神经网络 (From MLP to CNN)

![Page 8](week3_cnn_slides_pages/page_008.png)

**Convolutional Neural Networks**

- Why we need it?

![Page 9](week3_cnn_slides_pages/page_009.png)

**Example – Iris vs Rose**

- Output: Iris/Rose

![Page 10](week3_cnn_slides_pages/page_010.png)

**Machine Learning vs Deep Learning - Example**

- Machine Learning model: Output -> Feature Extraction -> Classification -> Cat / Not Cat
- Deep Learning model: Output -> Feature extraction and classification -> Cat / Not Cat

![Page 11](week3_cnn_slides_pages/page_011.png)

**Image Classification**

- High number of inputs (for example, if the picture is 1600 X 1200, then 1600 _ 1200 _ 3 = 5,760,000 inputs – 5 million inputs)
- If we have 1000 nodes in the first layer, then we will have 5 million \* 1000 weights, which is 5 billion weights
- High computational and memory requirements
- Can we use MLP for this problem? NO
- Solution: Convolutional Neural Network

![Page 12](week3_cnn_slides_pages/page_012.png)

**Sample Problems to Solve in Vision**

- Image classification: take an input picture, classify it as a cat or not
- Object Detection: For self-driving cars, find objects around

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Why CNN instead of MLP for images? (为什么图像用CNN而不是MLP？):**
>
> MLPs use fully connected layers. An RGB image of 1000x1000 pixels has 3 million inputs. A single hidden layer with 1000 neurons would need 3 billion weights! CNNs solve this via "weight sharing" (same filters slide across the image) and locally-connected layers, reducing parameters drastically.
>
> > MLP使用全连接层。一张1000x1000像素的RGB图像有300万个输入。一个有1000个神经元的单层隐藏层将需要30亿个权重！CNN通过"权重共享"（使用相同的滤波器在图像上滑动）和局部连接层解决了这个问题，大大减少了参数。
>
> **(2) Preserving spatial structure (保留空间结构):**
>
> MLPs must flatten the 2D image into a 1D vector before processing, destroying the spatial relationships between pixels. CNNs process images as 2D/3D grids, naturally preserving and exploiting spatial info (like edges and corners).
>
> > MLP 在处理前必须将 2D 图像展平为 1D 向量，这破坏了像素之间的空间关系。CNN 以 2D/3D 网格的形式处理图像，自然地保留并利用空间信息（如边缘和角）。
>
> **💡 Intuition:**
> **(1) Reading a book analogy (看书类比):**
>
> MLP is like looking at all the letters on a page simultaneously to guess the story. CNN is like reading with a magnifying glass — examining one small patch at a time, moving across the page, recognizing letters, then words, then sentences.
>
> > MLP就像同时看书页上的所有字母来猜测故事。CNN就像用放大镜看书 —— 每次只检查一小块区域，在书页上移动，认出字母，然后是单词，然后是句子。
>
> **⚠️ Pitfall:**
> **(1) CNN is NOT ONLY for images (CNN不只用于图像):**
>
> While famous for Computer Vision, 1D CNNs are also excellent for time-series data and some NLP tasks where local pattern detection is useful.
>
> > 虽然CNN以计算机视觉闻名，但1D CNN也非常适合时间序列数据和一些局部模式检测很有用的NLP任务。
>
> **📝 Exam:**
> **(1) 计算题 (Parameter Calculation):**
>
> Exam sets typically ask you to calculate the number of weights in an MLP vs a CNN for the same image size. Always remember: in MLP, `weights = input_pixels × hidden_nodes`.
>
> > 考试通常要求你计算同一图像尺寸下MLP和CNN的权重数量。永远记住：在MLP中，`权重 = 输入像素数 × 隐藏节点数`。

---

## 4. 卷积神经网络原理 (Convolutional Neural Networks Principles)

### 4.1 核心概念 (Core Concepts)

![Page 13](week3_cnn_slides_pages/page_013.png)

**Convolutional Neural Network**

- Feed forward NN
- Generally used to analyze images
- Done by processing images in the form of arrays of pixel values

![Page 14](week3_cnn_slides_pages/page_014.png)

**Convolutional Neural Network**

- Architecture diagram

![Page 15](week3_cnn_slides_pages/page_015.png)

**Convolutional Neural Network**
Objective: reduce the images into a form that is easier to process, without losing critical features that helps in prediction
Terminologies:

- Convolution
- Filter
- Padding (Valid or Same)
- Stride
- Pooling (Max-pooling or average-pooling)

### 4.2 边缘检测与过滤器 (Edge Detection and Filters)

![Page 16](week3_cnn_slides_pages/page_016.png)

**Edge Detection**

- Cat – Original Picture
- Basic edge filters applied to the greyscale image of cat
- Basic edge filters applied to the RGB image of cat

![Page 17](week3_cnn_slides_pages/page_017.png)

**Edge Detection**
Based on the variation in light intensity at different parts of the image, we should be able to find:

- Vertical edges
- Horizontal edges
- Edges at different angles
- These edges give us important information!

![Page 20](week3_cnn_slides_pages/page_020.png)

**Edge Detection Filters**

- Vertical, Horizontal, Scharr, Sobel
- Can we have our own filters? Yes, we can consider this filter as a parameter and learn them!

### 4.3 卷积操作 (Convolution Operation)

![Page 18](week3_cnn_slides_pages/page_018.png)

**Convolution**
Convolve the image matrix with a filter, which is another matrix.

- `6 x 6` image `*` `3 x 3` filter = `4 x 4` Output image

![Page 19](week3_cnn_slides_pages/page_019.png)

**Convolution**

- Convolution operator calculation example.

![Page 21](week3_cnn_slides_pages/page_021.png)

**Output of Convolution with filters**

- `n x n` image `*` `f x f` filter = `(n – f + 1) x (n – f + 1)` output
- `f` is conventionally odd number

> **📝 Notes:**
>
> **📌 What:**
> **(1) Filter/Kernel (滤波器/核):**
>
> A small matrix (e.g., 3x3) used for convolution. The values in this matrix are weights that are learned during training.
>
> > 一个用于卷积的小矩阵（如 3x3）。这个矩阵中的值是在训练期间学习到的权重。
>
> **🎯 Why:**
> **(1) Why use convolutions instead of just flattening? (为什么用卷积而不是直接展平？):**
>
> Convolutions preserve the spatial relationships of pixels. An edge is defined by how a pixel relates to its immediate neighbors, which is lost if we just flatten the image into a 1D array.
>
> > 卷积保留了像素的空间关系。边缘是由一个像素如何与其直接邻居相关联来定义的，如果我们只是将图像展平成一维数组，这种关系就会丢失。
>
> **💡 Intuition:**
> **(1) Flashlight analogy (手电筒类比):**
>
> Imagine a filter is a flashlight shining on a small region of the image. As you slide the flashlight across the image, it illuminates different features (like edges or curves). The convolution operation "lights up" when it finds a feature it's looking for.
>
> > 想象滤波器是照在图像小区域上的手电筒。当你在图像上滑动这段"光"时，它会照亮不同的特征（如边缘或曲线）。当卷积操作找到它正在寻找的特征时，它就会"亮起来"。
>
> **📐 Formula:**
> **(1) Output size (输出尺寸):**
>
> For an $n \times n$ image and an $f \times f$ filter (with $stride=1, padding=0$), the output size is $(n - f + 1) \times (n - f + 1)$.
>
> > 对于 $n \times n$ 的图像和 $f \times f$ 的滤波器（$stride=1, padding=0$），输出大小为 $(n - f + 1) \times (n - f + 1)$。
>
> **📝 Exam:**
> **(1) 计算题 (Output size calculation):**
>
> "Given a 28x28 image and a 5x5 filter, what is the size of the output feature map?" → $(28 - 5 + 1) = 24$. The output is 24x24.
>
> > "给出一个 28x28 的图像和 5x5 的滤波器，输出特征图的尺寸是多少？" → $(28 - 5 + 1) = 24$。输出是 24x24。

---

## 5. 卷积层超参数 (Convolution Parameters)

### 5.1 填充 (Padding)

![Page 22](week3_cnn_slides_pages/page_022.png)

**Padding**

- Refers to the number of pixels added to an image
- Padding is added to the frame of the image to give more space for the filter to cover the image. Once padding is added, previous end pixels will be part of multiple `3x3` matrices.
- This is a process to make sure the size of the output is not less than that of the input (if we have a `6x6` image convoluted with a `3x3` filter, output will be `4x4`. If we add one layer of padding around the picture, output for a `6x6` image will be another `6x6` image).

![Page 23](week3_cnn_slides_pages/page_023.png)

**Padding - Example**

- Output size formula: $(n + 2p - f + 1) \times (n + 2p - f + 1)$

![Page 24](week3_cnn_slides_pages/page_024.png)

**Valid vs Same Padding**

- **Valid**: No padding. `n x n` image filtered with `f x f` filter gives `(n - f + 1) x (n - f + 1)` image
- **Same**: add padding such that output size should be the same as input size.
  - $n + 2p - f + 1 = n$
  - $p = \frac{f - 1}{2}$

### 5.2 步长 (Stride)

![Page 25](week3_cnn_slides_pages/page_025.png)

**Strided Convolution**

- Example of stride.

![Page 26](week3_cnn_slides_pages/page_026.png)

**Strided Convolution**

- `n x n` image convolve with an `f x f` filter with a padding `p` and stride `s`, output will be:
  - $\lfloor \frac{n + 2p - f}{s} + 1 \rfloor \times \lfloor \frac{n + 2p - f}{s} + 1 \rfloor$

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) Why need padding? (为什么需要填充？):**
>
> Without padding, two problems happen: 1. The image shrinks after every convolution layer. 2. Pixels on the edges/corners are only "seen" a few times by the filter, while center pixels are processed many times. Padding solves both by preserving size and giving edge pixels equal importance.
>
> > 没有填充的话，会出现两个问题：1. 图像在每层卷积后都会缩小。2. 边缘/角落的像素只被滤波器"看到"几次，而中心像素被处理很多次。填充通过保留尺寸和赋予边缘像素同等重要性来解决这两个问题。
>
> **(2) Why use stride > 1? (为什么使用步长>1？):**
>
> A larger stride forces the filter to skip pixels, which aggressively downsamples the image. This reduces spatial dimensions and computational cost without needing a separate pooling layer.
>
> > 较大的步长迫使滤波器跳过像素，从而急剧下采样图像。这减少了空间维度和计算成本，而无需单独的池化层。
>
> **📐 Formula:**
> **(1) The Ultimate CNN Dimension Formula (终极CNN尺寸公式):**
>
> Output size = $\lfloor \frac{n + 2p - f}{s} + 1 \rfloor$.
>
> - $n$: input size
> - $p$: padding
> - $f$: filter size
> - $s$: stride
>
> > 输出尺寸 = $\lfloor \frac{n + 2p - f}{s} + 1 \rfloor$。
> >
> > - $n$：输入大小
> > - $p$：填充
> > - $f$：滤波器大小
> > - $s$：步长
>
> **📝 Exam:**
> **(1) 计算题 (Dimension Calculation):**
>
> "Calculate the output size for a 32x32 image with 3x3 filter, stride 2, and padding 1." → $(32 + 2\times1 - 3) / 2 + 1 = 31 / 2 + 1 = 15.5$. Round down to get 16x16.
>
> > "计算 32x32 图像，3x3 滤波器，步长 2，填充 1 的输出尺寸。" → $(32 + 2\times1 - 3) / 2 + 1 = 31 / 2 + 1 = 15.5$。向下取整得到 16x16。

---

## 6. 彩色图与构建卷积网络 (RGB Convolutions & Building CNN)

### 6.1 RGB通道卷积 (Convolutions on RGB Images)

![Page 27](week3_cnn_slides_pages/page_027.png)

**Convolutions on RGB Images**

- `6 x 6 x 3` (image) `*` `3 x 3 x 3` (filter) = `4 x 4` (output)
- #channels (RGB)
- Note: Can have one or more filters

![Page 28](week3_cnn_slides_pages/page_028.png)

**One Layer of a CNN**

- In this example, we have 2 filters. We can have more!
- Output has shape: `4 x 4 x 2`

![Page 29](week3_cnn_slides_pages/page_029.png)

**Example**

- Input: `39 x 39 x 3` -> Conv -> pooling -> flatten -> MLP (Output)
- Calculate parameters and dimensions at each step.

### 6.2 卷积网络层类型 (Types of Layers in a CNN)

![Page 30](week3_cnn_slides_pages/page_030.png)

**Types of Layers in a CNN**

- Convolution
- Pooling
- Fully Connected

### 6.3 池化层 (Pooling Layers)

![Page 31](week3_cnn_slides_pages/page_031.png)

**Pooling Layers**

- Max-pooling
- Average-pooling
- Example with `f = 2`, `Stride = 2`

![Page 32](week3_cnn_slides_pages/page_032.png)

**Benefits of Pooling**

- Reduces dimensions and computation
- Reduces overfitting as there are less parameters
- Makes the model tolerant towards small variations and distortions
- Filters all important features and filters out noise

![Page 33](week3_cnn_slides_pages/page_033.png)

**Example with Convolution layer, Pooling layer and Fully-connected layers**

- Complete architecture progression with dimensions and parameter tracking.

> **📝 Notes:**
>
> **📌 What:**
> **(1) Channels in CNN (CNN中的通道):**
>
> For RGB images, the input has 3 channels. The filter must also have 3 channels (e.g., $3 \times 3 \times 3$). The convolution happens across all channels simultaneously, summing them up to produce a SINGLE 2D output channel.
> To get multiple feature maps, we use multiple filters. If we use 10 filters, the output has 10 channels.
>
> > 对于RGB图像，输入有3个通道。滤波器也必须有3个通道（如 $3 \times 3 \times 3$）。卷积在所有通道上同时发生，然后将它们相加产生一个单个的2D输出通道。
> > 为了获得多个特征图，我们使用多个滤波器。如果我们使用10个滤波器，输出就有10个通道。
>
> **🎯 Why:**
> **(1) Why use pooling? (为什么使用池化？):**
>
> Pooling reduces the spatial dimensions (height and width) of the input volume for the next convolutional layer. It reduces parameters (preventing overfitting) and adds translation invariance (a slight shift in the input still results in the same pooled feature).
>
> > 池化减小了下一卷积层的输入体的空间维度（高和宽）。它减少了参数（防止过拟合），并增加了平移不变性（输入的轻微偏移仍会导致相同的汇聚特征）。
>
> **⚖️ Compare:**
> **(1) Max Pooling vs Average Pooling:**
>
> | Feature   | Max Pooling                                                            | Average Pooling                                           |
> | --------- | ---------------------------------------------------------------------- | --------------------------------------------------------- |
> | Mechanism | Takes the maximum value in the window                                  | Takes the average of values in the window                 |
> | Use Case  | Extracting dominant features (edges, corners); Standard in modern CNNs | Smoothing out features; Used in older networks like LeNet |
>
> > | 特性 | 最大池化 (Max Pooling)                          | 平均池化 (Average Pooling)              |
> > | ---- | ----------------------------------------------- | --------------------------------------- |
> > | 机制 | 取窗口中的最大值                                | 取窗口中值的平均值                      |
> > | 用途 | 提取主要特征（边缘、角）；现代 CNN 中的标准做法 | 平滑特征；用于像 LeNet 这样较老的网络中 |
>
> **⚠️ Pitfall:**
> **(1) Pooling layers have NO parameters (池化层没有参数):**
>
> Unlike convolutional layers where weights are learned, pooling layers are deterministic functions (max or avg) with no learnable weights.
>
> > 不同于权重是通过学习得到的卷积层，池化层是没有可学习权重的确定性函数（最大值或平均值）。

---

## 7. 总结与参考 (Summary and References)

![Page 34](week3_cnn_slides_pages/page_034.png)

**Convolution Operation - Summary**

- Objective is to extract high-level features like edges from the input image
- Can have multiple convolution layers
- Conventionally, first ConvLayer captures low level features like edges, color, gradient orientation etc.
- Reduce the size without losing relevant information
- Once it is reduced, the output matrix will be flattened and feed it to some classifiers like MLP

![Page 35](week3_cnn_slides_pages/page_035.png)

**References**

- https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53
- https://medium.com/swlh/convolutional-neural-networks-22764af1c42a
- https://austingwalters.com/edge-detection-in-computer-vision/
- https://www.geeksforgeeks.org/machine-learning/activation-functions-neural-networks/

> **📝 Notes:**
>
> **🎯 Why:**
> **(1) The overall CNN pipeline (整体 CNN 流程):**
>
> CNNs are designed to act as automatic feature extractors. The early layers learn simple shapes (edges, lines), middle layers learn parts (eyes, wheels), and final layers recognize whole objects (faces, cars). The flattened output is then passed to a standard MLP for the final classification.
>
> > CNN被设计为自动特征提取器。早期层学习简单的形状（边缘、线条），中间层学习部件（眼睛、轮子），最后层识别整个物体（人脸、汽车）。展平后的输出然后传递给标准的 MLP 用于最终的分类。
>
> **💡 Intuition:**
> **(1) The funnel architecture (漏斗架构):**
>
> Notice how CNNs usually look like a funnel. Spatial dimensions (width/height) decrease due to striding and pooling, while depth (number of channels) increases as we extract more complex features.
>
> > 注意 CNN 通常看起来像个漏斗。由于步长和池化，空间维度（宽/高）会减小，而随着我们提取更复杂的特征，深度（通道数）会增加。
>
> **📝 Exam:**
> **(1) 概念题 (Conceptual Summary):**
>
> "What are the common layers in a CNN and their purposes?" → Conv layer (feature extraction), ReLU (non-linearity), Pooling (downsampling & invariance), Fully Connected (classification).
>
> > "CNN中常见的层及其目的是什么？" → 卷积层（特征提取），ReLU（引入非线性），池化层（下采样和不变性），全连接层（分类）。
