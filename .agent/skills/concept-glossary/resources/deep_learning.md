# Deep Learning (深度学习)

> This file grows automatically as new notes are written. Entries are alphabetical.

---

### CNN / Convolutional Neural Network (卷积神经网络)

**Tags:** `#deep_learning` `#cnn` `#ml-week3`

**📌 Definition (定义):**

> A feed-forward neural network designed to process grid-like data (images) using convolution layers with local connectivity and weight sharing, drastically reducing parameters compared to fully-connected networks while preserving spatial structure.
>
> > 一种前馈神经网络，使用具有局部连接和权重共享的卷积层来处理网格形数据（图像），与全连接网络相比大幅减少参数，同时保留空间结构。

**💡 Analogy (类比):**

> MLP reads a book by looking at all letters simultaneously. CNN reads with a magnifying glass — examining one small patch at a time, sliding across the page, recognizing letters → words → sentences.
>
> > MLP 像同时看所有字母来猜故事。CNN 像用放大镜看书——每次只放大检查一小块，在页面上滑动，从字母→单词→句子逐级识别。

**⚖️ Contrast (易混淆对比):**

> | Aspect                       | MLP for images             | CNN                  |
> | ---------------------------- | -------------------------- | -------------------- |
> | Parameters (1000×1000 image) | ~1 billion                 | ~hundreds            |
> | Spatial structure            | ❌ Destroyed by flattening | ✅ Preserved         |
> | Translation invariance       | ❌ No                      | ✅ Yes (via pooling) |

**🔗 Related Concepts (关联概念):**

> → see: Convolution (核心操作)
> → see: Pooling (降采样)
> → see: ReLU (标准激活函数)

**📚 Appears In (出现课程):**

> - ML Week 3: Convolutional Neural Networks

---

### Convolution (卷积)

**Tags:** `#deep_learning` `#cnn` `#ml-week3`

**📌 Definition (定义):**

> A mathematical operation where a small filter/kernel slides across an input image, computing element-wise multiplication and summation at each position to produce a feature map that highlights specific patterns (edges, textures, etc.).
>
> > 一种数学操作，小的滤波器/核在输入图像上滑动，在每个位置进行逐元素乘法和求和，产生突出特定模式（边缘、纹理等）的特征图。

**💡 Analogy (类比):**

> Like a flashlight illuminating a small region of a dark painting. Slide it around and it "lights up" when it finds the feature it's looking for (e.g., a vertical edge).
>
> > 像手电筒照亮黑暗画作的一小块区域。在画上移动，当找到它要找的特征（如竖直边缘）时就"亮起来"。

**⚠️ Common Mistake (常见错误):**

> Filter depth must match input channels: RGB input (3 channels) requires 3-channel filters (e.g., 3×3×3). Multiple filters produce multiple output channels.
>
> > 滤波器深度必须匹配输入通道数：RGB 输入（3通道）需要 3 通道滤波器（如 3×3×3）。多个滤波器产生多个输出通道。

**📚 Appears In (出现课程):**

> - ML Week 3: Convolution Operation

---

### Pooling (池化)

**Tags:** `#deep_learning` `#cnn` `#ml-week3`

**📌 Definition (定义):**

> A downsampling operation that reduces spatial dimensions by taking the max or average value within non-overlapping windows. Has NO learnable parameters.
>
> > 一种降采样操作，通过在不重叠的窗口内取最大值或平均值来减小空间维度。没有可学习参数。

**⚖️ Contrast (易混淆对比):**

> | Aspect       | Max Pooling                    | Average Pooling   |
> | ------------ | ------------------------------ | ----------------- |
> | Operation    | Takes maximum                  | Takes average     |
> | Effect       | Preserves strongest activation | Smooths features  |
> | Modern usage | ✅ Standard                    | Rare (older nets) |

**📚 Appears In (出现课程):**

> - ML Week 3: Pooling Layers

---

### ReLU / Rectified Linear Unit (修正线性单元)

**Tags:** `#deep_learning` `#activation` `#ml-week3`

**📌 Definition (定义):**

> An activation function that outputs the input directly if positive, zero otherwise: f(x) = max(0, x). The standard choice for hidden layers in modern CNNs due to fast computation and reduced vanishing gradient problem.
>
> > 一种激活函数，正输入直接输出，否则输出零：f(x) = max(0, x)。由于计算快速且减轻梯度消失问题，是现代 CNN 隐藏层的标准选择。

**⚖️ Contrast (易混淆对比):**

> | Activation | Range   | Vanishing Gradient?  | Speed   |
> | ---------- | ------- | -------------------- | ------- |
> | Sigmoid    | (0, 1)  | ❌ Yes               | Slow    |
> | Tanh       | (-1, 1) | ❌ Yes               | Medium  |
> | ReLU       | [0, ∞)  | ✅ No (for positive) | ✅ Fast |

**📚 Appears In (出现课程):**

> - ML Week 3: Activation Functions

---
