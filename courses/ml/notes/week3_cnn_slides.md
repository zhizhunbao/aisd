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

