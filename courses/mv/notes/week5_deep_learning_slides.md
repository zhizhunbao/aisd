# Week 5: 图像分类的深度学习 (Deep Learning for Image Classification)

> Source: `Week5_ Deep Learning for Image Classification1.pptx`
> Total slides: 32
> Instructor: Stephin Rachel Thomas | Feb 12, 2026

---

## 1. 深度学习概述 (Introduction to Deep Learning)

![Page 1](week5_deep_learning_slides_pages/page_001.png)

**Title slide:** Dark green background with wave pattern. "Deep Learning for Image Classification" in large white text at center. Subtitle area below. Bottom: Instructor name "Stephin Rachel Thomas" and date "February 12, 2026". Algonquin College logo in top-right corner.

**标题页：** 深绿色波浪纹背景。中央大号白色文字"Deep Learning for Image Classification"。下方为副标题区域。底部显示讲师姓名"Stephin Rachel Thomas"和日期"February 12, 2026"。右上角有阿冈昆学院标志。

- **Deep Learning for Image Classification** — 图像分类的深度学习
- Instructor: Stephin Rachel Thomas — 讲师：Stephin Rachel Thomas
- February 12, 2026

![Page 2](week5_deep_learning_slides_pages/page_002.png)

**Agenda slide:** "Today's Topics" as header on dark green background. Twelve bullet items listed vertically covering the topics for the lecture, from CNN fundamentals through midterm test details.

**议程页：** 深绿背景，标题"Today's Topics"。纵向列出十二个要点，涵盖本次讲座的主题，从CNN基础到期中考试详情。

**Today's Topics:**

- Fundamentals of Image classification with CNN — CNN图像分类基础
- Dataset Preparation — 数据集准备
- Discussion — 讨论
- Data augmentation Strategy — 数据增强策略
- Designing CNN architecture — CNN架构设计
- Activation Functions — 激活函数
- Loss Functions — 损失函数
- Back propagation — 反向传播
- Optimizers — 优化器
- Training CNN — 训练CNN
- Common issues in Computer vision — 计算机视觉中的常见问题
- Troubleshooting in CNN Training — CNN训练故障排除
- Midterm test details — 期中考试详情

![Page 3](week5_deep_learning_slides_pages/page_003.png)

**Introduction slide:** Title "INTRODUCTION" at top on dark green background. Main text describes deep learning as a subset of machine learning involving neural networks with many layers. Right side shows a composite image of deep learning applications: face detection, object recognition, autonomous driving.

**简介页：** 深绿背景，顶部标题"INTRODUCTION"。正文描述深度学习是机器学习的子集，涉及多层神经网络。右侧展示深度学习应用的合成图：人脸检测、物体识别、自动驾驶。

- Deep Learning, a subset of machine learning, involves neural networks with many layers. — 深度学习是机器学习的一个子集，涉及多层神经网络。
- In computer vision, deep learning powers tasks such as image classification, object detection, and semantic segmentation. — 在计算机视觉中，深度学习支持图像分类、目标检测和语义分割等任务。
- These tasks are accomplished through models that can identify patterns and features in images, mimicking human vision. — 这些任务通过能够识别图像中的模式和特征的模型来完成，模拟人类视觉。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Deep Learning (深度学习):**
>
> A subset of machine learning that uses neural networks with multiple hidden layers (hence "deep") to automatically learn hierarchical feature representations from raw data.
>
>> 机器学习的子集，使用具有多个隐藏层（因此称为"深度"）的神经网络从原始数据中自动学习分层特征表示。
>>
>
> **(2) Key Application Areas (关键应用领域):**
>
> Image classification, object detection, semantic segmentation, face recognition, autonomous driving — all powered by deep learning models that learn directly from pixels.
>
>> 图像分类、目标检测、语义分割、人脸识别、自动驾驶——都由直接从像素学习的深度学习模型驱动。
>>
>
> **🎯 Why:**
> **(1) Manual feature engineering is limited (手动特征工程有局限):**
>
> Traditional ML (e.g., SVM + HOG) requires experts to design features. Deep learning eliminates this bottleneck by learning features automatically from data.
>
>> 传统ML（如SVM + HOG）需要专家设计特征。深度学习通过从数据中自动学习特征消除了这个瓶颈。
>>
>
> **(2) Hierarchical representation (分层表示):**
>
> Deep networks learn increasingly abstract features: edges → textures → parts → objects. This mirrors how human visual cortex processes information.
>
>> 深度网络学习逐渐抽象的特征：边缘 → 纹理 → 部件 → 物体。这反映了人类视觉皮层处理信息的方式。
>>
>
> **💡 Intuition:**
> **(1) LEGO analogy (乐高类比):**
>
> Think of deep learning like building with LEGO. Layer 1 learns simple bricks (edges). Layer 2 combines bricks into shapes (eyes, wheels). Layer 3 combines shapes into objects (faces, cars). Each layer builds on the previous one.
>
>> 想象深度学习像搭乐高。第1层学习简单的砖块（边缘）。第2层将砖块组合成形状（眼睛、轮子）。第3层将形状组合成物体（面孔、汽车）。每层都建立在前一层之上。
>>
>
> **(2) AI vs ML vs DL hierarchy (AI/ML/DL层级关系):**
>
> AI ⊃ ML ⊃ DL. Deep learning is the most specific subset — all DL is ML, but not all ML is DL. The key differentiator is the use of deep neural networks.
>
>> AI ⊃ ML ⊃ DL。深度学习是最具体的子集——所有DL都是ML，但不是所有ML都是DL。关键区别在于使用深度神经网络。
>>
>
> **⚖️ Compare:**
> **(1) Traditional ML vs Deep Learning (传统ML vs 深度学习):**
>
> | Feature | Traditional ML | Deep Learning |
> |---|---|---|
> | Feature extraction | Manual (HOG, SIFT) | Automatic (learned) |
> | Data requirement | Small-medium | Large |
> | Interpretability | Higher | Lower (black box) |
> | Hardware | CPU sufficient | GPU/TPU needed |
> | Performance ceiling | Saturates with data | Improves with more data |
>
>> | 特性 | 传统ML | 深度学习 |
>> |---|---|---|
>> | 特征提取 | 手动（HOG, SIFT） | 自动（学习到的） |
>> | 数据需求 | 中小量 | 大量 |
>> | 可解释性 | 较高 | 较低（黑盒） |
>> | 硬件 | CPU足够 | 需要GPU/TPU |
>> | 性能上限 | 数据增多后饱和 | 更多数据继续提升 |
>>
>
> **⚠️ Pitfall:**
> **(1) "Deep learning solves everything" fallacy (深度学习万能谬误):**
>
> DL requires large datasets and powerful hardware. For small datasets or simple tasks, traditional ML (e.g., SVM, Random Forest) can outperform DL because DL tends to overfit.
>
>> DL需要大数据集和强大硬件。对于小数据集或简单任务，传统ML（如SVM、随机森林）可能优于DL，因为DL容易过拟合。
>>
>
> **(2) Confusing "many layers" with "good performance" (混淆"层多"与"性能好"):**
>
> More layers does not always mean better results. Without sufficient data or proper regularization, deeper networks perform worse (degradation problem, solved by ResNet's skip connections).
>
>> 更多层并不总是意味着更好的结果。没有足够数据或适当正则化，更深的网络表现更差（退化问题，由ResNet的跳跃连接解决）。
>>
>
> **📝 Exam:**
> **(1) 定义题 (Definition):**
> "What is deep learning and how does it relate to machine learning?" → Deep learning is a subset of ML using multi-layer neural networks to learn hierarchical representations automatically from data.
>
>> "什么是深度学习，它与机器学习有什么关系？" → 深度学习是ML的子集，使用多层神经网络从数据中自动学习分层表示。
>>
>
> **(2) 对比题 (Comparison):**
> "Compare traditional ML and deep learning for image classification." → Traditional ML uses handcrafted features (slower, interpretable); DL learns features automatically (requires more data, GPU, but achieves higher accuracy on large datasets).
>
>> "比较传统ML和深度学习在图像分类中的差异。" → 传统ML使用手工特征（较慢但可解释）；DL自动学习特征（需要更多数据和GPU，但在大数据集上准确率更高）。
>>

---

## 2. CNN图像分类基础 (Fundamentals of Image Classification with CNNs)

![Page 4](week5_deep_learning_slides_pages/page_004.png)

**CNN fundamentals slide:** Title "Fundamentals of Image Classification with CNNs" on dark green background. Left side contains text describing CNN image classification. Right side shows a CNN architecture diagram with an input image (cat) passing through convolutional layers, pooling layers, and fully connected layers to produce a classification output.

**CNN基础页：** 深绿背景，标题"Fundamentals of Image Classification with CNNs"。左侧文字描述CNN图像分类。右侧展示CNN架构示意图，一张输入图像（猫）经过卷积层、池化层和全连接层产生分类输出。

- Image classification with CNNs involves categorizing and labeling images into predefined classes. — CNN图像分类涉及将图像分类并标注到预定义类别中。
- CNNs process images through layers that detect features, reduce dimensions, and classify images based on learned patterns. — CNN通过各层处理图像，检测特征、降低维度，并根据学习到的模式对图像进行分类。
- Key components include convolutional layers for feature extraction, pooling layers for dimensionality reduction, and fully connected layers for classification. — 关键组件包括用于特征提取的卷积层、用于降维的池化层和用于分类的全连接层。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Image Classification Pipeline (图像分类流程):**
>
> Input image → CNN feature extraction (conv + pool layers) → flattened feature vector → fully connected layers → class probabilities (softmax output).
>
>> 输入图像 → CNN特征提取（卷积+池化层） → 展平的特征向量 → 全连接层 → 类别概率（softmax输出）。
>>
>
> **(2) Three Key Components (三个关键组件):**
>
> Convolutional layers extract spatial features (edges, textures). Pooling layers downsample feature maps to reduce computation. Fully connected layers combine all features for final classification decision.
>
>> 卷积层提取空间特征（边缘、纹理）。池化层对特征图降采样以减少计算量。全连接层组合所有特征进行最终分类决策。
>>
>
> **🎯 Why:**
> **(1) Spatial structure preservation (保持空间结构):**
>
> Unlike traditional ML that flattens images into 1D vectors (losing spatial relationships), CNNs preserve the 2D spatial structure, enabling position-invariant feature detection.
>
>> 与传统ML将图像展平为1D向量（丢失空间关系）不同，CNN保留2D空间结构，实现位置不变的特征检测。
>>
>
> **(2) Parameter sharing reduces complexity (参数共享降低复杂度):**
>
> A 3×3 filter has only 9 weights regardless of image size. This makes CNNs much more efficient than fully connected networks where every input pixel connects to every neuron.
>
>> 3×3滤波器无论图像大小只有9个权重。这使CNN比每个输入像素都连接到每个神经元的全连接网络高效得多。
>>
>
> **💡 Intuition:**
> **(1) Factory assembly line (工厂流水线):**
>
> CNN is like a factory: raw image → Stage 1 workers detect edges → Stage 2 workers combine into parts (eyes, noses) → Stage 3 workers assemble into objects (face = "cat"). QC inspectors at the end (FC layers) decide the label.
>
>> CNN像工厂：原始图像 → 第1阶段工人检测边缘 → 第2阶段工人组合成部件（眼睛、鼻子） → 第3阶段工人组装成物体（脸="猫"）。最后的质检员（FC层）决定标签。
>>
>
> **(2) Feature hierarchy (特征层次):**
>
> Each layer learns progressively more abstract features. Layer 1: "horizontal line". Layer 2: "corner". Layer 3: "eye". This is why deeper networks can recognize more complex objects.
>
>> 每层学习逐渐更抽象的特征。第1层："水平线"。第2层："角"。第3层："眼睛"。这就是更深网络能识别更复杂物体的原因。
>>
>
> **⚖️ Compare:**
> **(1) Fully Connected NN vs CNN (全连接NN vs CNN):**
>
> | Feature | Fully Connected NN | CNN |
> |---|---|---|
> | Input handling | Flattened 1D vector | 2D spatial structure |
> | Parameter count | Huge (every pixel to every neuron) | Small (shared filters) |
> | Translation invariance | No | Yes (same filter scans everywhere) |
> | Best for | Tabular data | Images, spatial data |
>
>> | 特性 | 全连接NN | CNN |
>> |---|---|---|
>> | 输入处理 | 展平为1D向量 | 2D空间结构 |
>> | 参数量 | 巨大 | 小（共享滤波器） |
>> | 平移不变性 | 无 | 有 |
>> | 最适合 | 表格数据 | 图像、空间数据 |
>>
>
> **⚠️ Pitfall:**
> **(1) Forgetting the flatten step (忘记展平步骤):**
>
> Between conv/pooling and FC layers, feature maps must be flattened into 1D. This is a common source of dimension mismatch errors in code.
>
>> 在卷积/池化层和FC层之间，特征图必须展平为1D。这是代码中常见的维度不匹配错误来源。
>>
>
> **(2) "CNN = only for images" misconception (CNN仅用于图像的误解):**
>
> CNNs work on any data with local spatial patterns: audio spectrograms, time series (1D conv), even text. The key requirement is local pattern structure.
>
>> CNN适用于任何具有局部空间模式的数据：音频频谱图、时间序列（1D卷积）、甚至文本。关键要求是局部模式结构。
>>
>
> **📝 Exam:**
> **(1) 组件功能题 (Component function):**
> "Name the 3 main components of a CNN and their roles." → Conv layers: feature extraction; Pooling: dimensionality reduction; FC layers: classification.
>
>> "列出CNN的三个主要组件及其作用。" → 卷积层：特征提取；池化层：降维；全连接层：分类。
>>
>
> **(2) 优势题 (Advantage):**
> "Why are CNNs preferred over fully connected networks for images?" → Parameter sharing, spatial structure preservation, and translation invariance.
>
>> "为什么CNN在图像处理中优于全连接网络？" → 参数共享、空间结构保留和平移不变性。
>>

---

## 3. 数据集准备 (Dataset Preparation)

### 3.1 数据收集与标注 (Collection and Annotation)

![Page 5](week5_deep_learning_slides_pages/page_005.png)

**Dataset preparation slide:** Title "Collection and Annotation" with subtitle "Dataset Preparation:" on dark green background. Text describes the importance of collecting diverse images and annotation for supervised learning. Right side shows example images of different animal classes (cats, dogs) with annotation labels overlaid.

**数据集准备页：** 深绿背景，标题"Collection and Annotation"，副标题"Dataset Preparation:"。文字描述收集多样化图像和标注对监督学习的重要性。右侧展示不同动物类别（猫、狗）的示例图像，及叠加的标注标签。

- Dataset preparation is a vital step in image classification. — 数据集准备是图像分类的关键步骤。
- It involves collecting a diverse set of images representing different classes. — 它涉及收集代表不同类别的多样化图像集。
- Annotation, the process of labeling images with class names, is essential for supervised learning. — 标注，即用类名标记图像的过程，对监督学习至关重要。
- Quality and diversity of the dataset directly impact the model's ability to learn and generalize to new, unseen images. — 数据集的质量和多样性直接影响模型学习和泛化到新的、未见过的图像的能力。

### 3.2 数据预处理 (Data Preprocessing)

![Page 6](week5_deep_learning_slides_pages/page_006.png)

**Preprocessing slide:** Title "Data Preprocessing Techniques for Image Data" on dark green/teal background. Three paragraphs of text describe preprocessing steps: resizing, normalizing, color space conversion. Key phrases highlighted in cyan and yellow: "resizing images to a uniform size, normalizing pixel values" in cyan, "consistent input for the CNN" in yellow.

**预处理页：** 深绿/青色背景，标题"Data Preprocessing Techniques for Image Data"。三段文字描述预处理步骤：调整大小、归一化、色彩空间转换。关键短语以青色和黄色高亮："resizing images to a uniform size, normalizing pixel values"为青色，"consistent input for the CNN"为黄色。

- Preprocessing is crucial for preparing images for CNNs. — 预处理对于为CNN准备图像至关重要。
- It includes resizing images to a uniform size, normalizing pixel values (typically to a 0-1 range), and converting images to grayscale or other color spaces if needed. — 它包括将图像调整为统一大小、归一化像素值（通常到0-1范围）、以及根据需要将图像转换为灰度或其他色彩空间。
- These steps ensure consistent input for the CNN, aiding in effective learning and reducing computational load. — 这些步骤确保CNN的一致输入，有助于有效学习并减少计算负荷。

### 3.3 数据集划分讨论 (Data Split Discussion)

![Page 7](week5_deep_learning_slides_pages/page_007.png)

**Discussion slide:** Dark green background with a single bold question: "Discussion – Why do we split our data into train, validation, and testing sets?" No additional text or diagrams.

**讨论页：** 深绿背景，单一粗体问题："Discussion – Why do we split our data into train, validation, and testing sets?" 无其他文字或图表。

- **Discussion – Why do we split our data into train, validation, and testing sets?** — 讨论——为什么我们要将数据分为训练集、验证集和测试集？

### 3.4 数据增强策略 (Data Augmentation Strategies)

![Page 8](week5_deep_learning_slides_pages/page_008.png)

**Data augmentation slide:** Title "Data Augmentation Strategies in Image Classification" on white background. Left side: text describing data augmentation with key terms "Data augmentation" in cyan and "rotation, scaling, flipping, and cropping to the images" in cyan. Right side: a visual grid showing an original cat image and 10 augmented versions labeled Horizontal, Vertically, +45 Rotation, -45 Rotation, Blur, Brighter, Noise added, Darker, Grayscale, Crop. Arrow labeled "Augmented Images" spans the bottom.

**数据增强页：** 白色背景，标题"Data Augmentation Strategies in Image Classification"。左侧：文字描述数据增强，关键术语"Data augmentation"和"rotation, scaling, flipping, and cropping to the images"以青色高亮。右侧：展示一张原始猫图像和10张增强版本的可视网格，标注为Horizontal、Vertically、+45 Rotation、-45 Rotation、Blur、Brighter、Noise added、Darker、Grayscale、Crop。底部有"Augmented Images"跨度箭头。

- Data augmentation artificially expands the training dataset by applying random transformations like rotation, scaling, flipping, and cropping to the images. — 数据增强通过对图像应用旋转、缩放、翻转和裁剪等随机变换来人为扩展训练数据集。
- This process helps in reducing overfitting, as it exposes the model to a wider variety of features and scenarios, making it more robust and improving generalization. — 这一过程有助于减少过拟合，因为它使模型接触到更广泛的特征和场景，使其更加鲁棒并提高泛化能力。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Dataset Preparation Pipeline (数据集准备流程):**
>
> Collect diverse images → annotate with class labels → preprocess (resize, normalize) → split into train/validation/test → augment training data.
>
>> 收集多样化图像 → 标注类别标签 → 预处理（调整大小、归一化） → 划分为训练/验证/测试集 → 增强训练数据。
>>
>
> **(2) Data Augmentation (数据增强):**
>
> Artificially expanding the training dataset by applying transformations (rotation, flipping, scaling, cropping, color jittering) to existing images. Does NOT change validation/test sets.
>
>> 通过对现有图像应用变换（旋转、翻转、缩放、裁剪、颜色抖动）来人为扩展训练数据集。不改变验证/测试集。
>>
>
> **🎯 Why:**
> **(1) Quality data > complex model (优质数据 > 复杂模型):**
>
> "Garbage in, garbage out" — even the best CNN cannot learn from poorly labeled or biased data. Dataset quality is the single biggest factor in model performance.
>
>> "垃圾进，垃圾出" — 即使最好的CNN也无法从标注错误或有偏差的数据中学习。数据集质量是模型性能最大的决定因素。
>>
>
> **(2) Train/Val/Test split rationale (训练/验证/测试集划分原理):**
>
> - **Training set**: model learns from this data (weight updates)
> - **Validation set**: tunes hyperparameters (learning rate, epochs) WITHOUT touching test data
> - **Test set**: final unbiased evaluation — used ONLY ONCE
> Without splitting, you can't know if the model generalizes or just memorizes.
>
>> - **训练集**：模型从这些数据中学习（权重更新）
>> - **验证集**：调整超参数（学习率、轮数），不碰测试数据
>> - **测试集**：最终无偏评估——只使用一次
>> 不划分的话，无法知道模型是否泛化还是只是记忆。
>>
>
> **💡 Intuition:**
> **(1) Exam preparation analogy (考试准备类比):**
>
> Training set = textbook exercises (you learn from). Validation set = practice exams (you check progress). Test set = the real exam (you only see once). If you peek at the real exam beforehand, your score is meaningless.
>
>> 训练集 = 课本练习（从中学习）。验证集 = 模拟考试（检查进度）。测试集 = 真正的考试（只见一次）。如果提前偷看真题，分数就没意义了。
>>
>
> **(2) Why augmentation works (为什么增强有效):**
>
> A cat rotated 45° is still a cat. Augmentation teaches the model this invariance without needing more real images. It's like studying the same concept from different angles.
>
>> 旋转45°的猫仍然是猫。增强教会模型这种不变性，而不需要更多真实图像。就像从不同角度学习相同概念。
>>
>
> **⚙️ How:**
> **(1) Normalization to [0,1] (归一化到[0,1]):**
>
> Divide pixel values by 255 to scale from [0, 255] to [0, 1]. This prevents large pixel values from dominating gradient updates and helps the network converge faster.
>
>> 将像素值除以255，从[0, 255]缩放到[0, 1]。这防止大像素值主导梯度更新，帮助网络更快收敛。
>>
>
> **(2) Common split ratios (常见划分比例):**
>
> Typical: 70% train / 15% val / 15% test, or 80/10/10. For small datasets, use k-fold cross-validation instead.
>
>> 典型比例：70%训练 / 15%验证 / 15%测试，或80/10/10。小数据集使用k折交叉验证。
>>
>
> **⚠️ Pitfall:**
> **(1) Data leakage between splits (数据泄漏):**
>
> Never augment BEFORE splitting! If an augmented version of a training image ends up in the test set, the evaluation is contaminated. Always split first, then augment only the training set.
>
>> 永远不要在划分前增强！如果训练图像的增强版本出现在测试集中，评估就被污染了。始终先划分，然后只增强训练集。
>>
>
> **(2) Overreliance on augmentation (过度依赖增强):**
>
> Augmentation cannot fix fundamental data problems — if your dataset lacks a class entirely, no amount of flipping or rotating will help. It supplements real data, not replaces it.
>
>> 增强不能修复根本的数据问题——如果数据集完全缺少某个类别，再多翻转旋转也没用。它补充真实数据，不能替代。
>>
>
> **📝 Exam:**
> **(1) 概念题 (Concept):**
> "Why do we split data into train, validation, and test sets?" → Train: learn weights. Validation: tune hyperparameters without bias. Test: final unbiased evaluation (used once).
>
>> "为什么将数据分为训练、验证和测试集？" → 训练：学习权重。验证：无偏地调超参数。测试：最终无偏评估（使用一次）。
>>
>
> **(2) 应用题 (Application):**
> "Name 3 data augmentation techniques." → Rotation, horizontal flipping, scaling/cropping, color jittering, adding noise, blur.
>
>> "列出3种数据增强技术。" → 旋转、水平翻转、缩放/裁剪、颜色抖动、添加噪声、模糊。
>>

---

## 4. CNN架构设计 (Designing a CNN Architecture)

![Page 9](week5_deep_learning_slides_pages/page_009.png)

**CNN architecture design slide:** Title "Designing a CNN Architecture: Key Considerations" on white/light background. Left side: two paragraphs describing layer choices and architecture complexity. Key terms "number" in blue, "types" in green, "parameters" in blue. Right side: 3D rendering of interconnected blocks representing a neural network architecture with nodes and edges.

**CNN架构设计页：** 白色/浅色背景，标题"Designing a CNN Architecture: Key Considerations"。左侧：两段文字描述层选择和架构复杂度。关键术语"number"蓝色、"types"绿色、"parameters"蓝色。右侧：神经网络架构的3D渲染，展示互连的方块、节点和边。

- Designing a CNN involves decisions about the number of layers, types of layers (convolutional, pooling, fully connected), and their parameters (like filter size, stride, and activation functions). — 设计CNN涉及关于层数、层类型（卷积、池化、全连接）及其参数（如滤波器大小、步长和激活函数）的决策。
- The architecture should match the complexity of the task; deeper networks for more complex tasks, and consideration of computational efficiency and overfitting risks. — 架构应与任务的复杂度相匹配；更复杂的任务使用更深的网络，并考虑计算效率和过拟合风险。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Architecture Design Choices (架构设计选择):**
>
> Designing a CNN involves deciding: number of conv layers, filter sizes (3×3, 5×5), number of filters per layer, pooling strategy, number of FC layers, and activation functions.
>
>> 设计CNN涉及决定：卷积层数、滤波器大小（3×3、5×5）、每层滤波器数量、池化策略、FC层数和激活函数。
>>
>
> **(2) Task-Architecture Matching (任务与架构匹配):**
>
> Simple tasks (binary classification of 2 objects) need shallow networks. Complex tasks (ImageNet 1000 classes) need deep networks like VGG, ResNet, or Inception.
>
>> 简单任务（2个物体的二分类）需要浅层网络。复杂任务（ImageNet 1000类）需要VGG、ResNet或Inception等深层网络。
>>
>
> **🎯 Why:**
> **(1) Depth enables abstraction (深度实现抽象):**
>
> More layers = more levels of abstraction. Layer 1 learns edges, Layer 2 learns textures, Layer 3 learns object parts. Without sufficient depth, the network cannot compose simple features into complex patterns.
>
>> 更多层 = 更多抽象级别。第1层学习边缘，第2层学习纹理，第3层学习物体部件。没有足够深度，网络无法将简单特征组合成复杂模式。
>>
>
> **(2) Filter size tradeoff (滤波器大小权衡):**
>
> Small filters (3×3): capture fine details, fewer parameters, can be stacked for large receptive fields. Large filters (7×7): capture broader context but with many more parameters. Modern trend: stack small filters.
>
>> 小滤波器（3×3）：捕获细节，参数少，可堆叠获得大感受野。大滤波器（7×7）：捕获更广泛上下文但参数多。现代趋势：堆叠小滤波器。
>>
>
> **💡 Intuition:**
> **(1) Building a house analogy (建房类比):**
>
> Architecture is like a blueprint. Too simple (one room) = can't fit a family. Too complex (100 rooms for one person) = wasteful and hard to maintain. The design must match the need.
>
>> 架构像蓝图。太简单（一间房）= 容不下一家人。太复杂（一个人100间房）= 浪费且难以维护。设计必须与需求匹配。
>>
>
> **(2) Increasing filter count (逐层增加滤波器数):**
>
> Common pattern: 32 → 64 → 128 filters as depth increases. Early layers need few filters (few edge types), deep layers need many (many object parts). Like a pyramid — wide base, narrow top.
>
>> 常见模式：随深度增加32 → 64 → 128个滤波器。早期层需要少量滤波器（边缘类型少），深层需要多个（物体部件多）。像金字塔——底宽顶窄。
>>
>
> **⚖️ Compare:**
> **(1) Classic CNN architectures (经典CNN架构):**
>
> | Architecture | Depth | Key Innovation |
> |---|---|---|
> | LeNet-5 | 5 layers | Pioneer CNN (1998) |
> | VGG-16 | 16 layers | All 3×3 filters, uniform design |
> | ResNet | 50-152 layers | Skip connections solve degradation |
> | MobileNet | ~28 layers | Depthwise separable conv for mobile |
>
>> | 架构 | 深度 | 关键创新 |
>> |---|---|---|
>> | LeNet-5 | 5层 | CNN先驱（1998） |
>> | VGG-16 | 16层 | 全部3×3滤波器，统一设计 |
>> | ResNet | 50-152层 | 跳跃连接解决退化问题 |
>> | MobileNet | ~28层 | 深度可分离卷积用于移动端 |
>>
>
> **⚠️ Pitfall:**
> **(1) Deeper ≠ always better (更深 ≠ 总是更好):**
>
> Without skip connections (ResNet), networks deeper than ~20 layers suffer from vanishing gradients — they actually perform WORSE than shallower networks on training data.
>
>> 没有跳跃连接（ResNet），超过约20层的网络会遭受梯度消失——在训练数据上实际表现比浅层网络更差。
>>
>
> **(2) Starting too complex (起步太复杂):**
>
> Always start with a simple architecture and add complexity only if needed. A 3-layer CNN is often enough for many classroom and real-world tasks.
>
>> 始终从简单架构开始，仅在需要时增加复杂度。3层CNN通常足以应对许多课堂和实际任务。
>>
>
> **📝 Exam:**
> **(1) 设计题 (Design):**
> "What factors should you consider when designing a CNN?" → Number/types of layers, filter sizes, pooling strategy, activation functions, task complexity, computational budget.
>
>> "设计CNN时应考虑哪些因素？" → 层数/类型、滤波器大小、池化策略、激活函数、任务复杂度、计算预算。
>>
>
> **(2) 推理题 (Reasoning):**
> "Why do modern CNNs prefer 3×3 filters over larger ones?" → Two stacked 3×3 filters = same receptive field as one 5×5, but fewer parameters (18 vs 25) and more nonlinearity.
>
>> "为什么现代CNN倾向于使用3×3滤波器而非更大的？" → 两个堆叠的3×3 = 与一个5×5相同的感受野，但参数更少（18 vs 25）且非线性更多。
>>

---

## 5. 激活函数 (Activation Functions)

### 5.1 激活函数概述 (Overview)

![Page 10](week5_deep_learning_slides_pages/page_010.png)

**Activation functions overview slide:** Title "Activation Functions" in green on white background. Three bullet points describing activation functions. Below: a neuron diagram showing inputs (x₁, x₂, …) with weights (ω₁, ω₂, …), summation (Σ ωᵢxᵢ + b), activation function f, and output z = f(Σ ωᵢxᵢ + b). Activation function shown as f(z) = max(0, z).

**激活函数概述页：** 白色背景，标题"Activation Functions"为绿色。三个要点描述激活函数。下方：神经元示意图，展示输入(x₁, x₂, …)与权重(ω₁, ω₂, …)、求和(Σ ωᵢxᵢ + b)、激活函数f及输出z = f(Σ ωᵢxᵢ + b)。激活函数显示为f(z) = max(0, z)。

- Activation function determines if a neuron fires — 激活函数决定神经元是否激活
- Introduces nonlinearity to the network — 向网络引入非线性
- Applied after convolution layer, after each fully connected later and output layer allowing the network to learn and represent complex patterns in the data — 应用在卷积层之后、每个全连接层之后和输出层，使网络能够学习和表示数据中的复杂模式

### 5.2 Sigmoid 函数

![Page 11](week5_deep_learning_slides_pages/page_011.png)

**Sigmoid slide:** Title "Different types of Activation Functions" in green, subtitle "Sigmoid" in green on white background. Four bullet points describe sigmoid properties. Right side: sigmoid curve plot from x = -6 to 6, showing the characteristic S-shaped curve from 0 to 1. Formula: σ(x) = 1 / (1 + e⁻ˣ).

**Sigmoid页：** 白色背景，标题"Different types of Activation Functions"为绿色，副标题"Sigmoid"为绿色。四个要点描述sigmoid属性。右侧：sigmoid曲线图，x从-6到6，展示从0到1的特征S形曲线。公式：σ(x) = 1 / (1 + e⁻ˣ)。

**Sigmoid:**
- Output of activation function between 0 and 1 — 激活函数输出在0和1之间
- Suitable for binary classification tasks — 适用于二分类任务
- Vanishing gradient problem – near boundaries, the network doesn't learn quickly — 梯度消失问题——在边界附近，网络学习速度很慢
- Used for output layer activation in binary classification — 用于二分类中的输出层激活

### 5.3 Tanh 函数

![Page 12](week5_deep_learning_slides_pages/page_012.png)

**Tanh slide:** Subtitle "Tanh" in green on white background. Five bullet points describing tanh properties on left side. Right side: Tanh function plot from x = -10 to 10, showing the S-shaped curve from -1 to 1. Formula: f(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ) shown in plot legend.

**Tanh页：** 白色背景，副标题"Tanh"为绿色。左侧五个要点描述tanh属性。右侧：Tanh函数图，x从-10到10，展示从-1到1的S形曲线。公式：f(x) = (eˣ - e⁻ˣ) / (eˣ + e⁻ˣ) 显示在图例中。

**Tanh:**
- Maps inputs to a range between -1 and 1 — 将输入映射到-1和1之间的范围
- Provides a more balanced output with zero-centered data — 提供以零为中心的更平衡的输出
- Smooth and differentiable activation function — 平滑且可微的激活函数
- Shares vanishing gradient problem with sigmoid — 与sigmoid共享梯度消失问题
- Used for handling negative input values — 用于处理负输入值

### 5.4 ReLU 函数 (Rectified Linear Unit)

![Page 13](week5_deep_learning_slides_pages/page_013.png)

**ReLU slide:** Subtitle "ReLU – Rectified Linear Unit" in green on white background. Five bullet points on left. Center: piecewise formula f(x) = 0 for x<0, x for x>=0. Right side: ReLU "rectifier" plot showing the characteristic kinked line at x=0, rising linearly for positive values.

**ReLU页：** 白色背景，副标题"ReLU – Rectified Linear Unit"为绿色。左侧五个要点。中间：分段公式f(x) = 0 (x<0), x (x>=0)。右侧：ReLU"整流器"图，展示在x=0处的特征折线，正值部分线性上升。

**ReLU – Rectified Linear Unit:**
- Only input values > 0 are kept — 仅保留大于0的输入值
- Range [0, ∞] — 范围[0, ∞]
- f(x)= max(0, x)
- While keeping positive values unchanged, it promotes sparse representations, reducing overfitting — 在保持正值不变的同时，促进稀疏表示，减少过拟合
- Mitigates vanishing gradient problem, enabling faster learning — 缓解梯度消失问题，实现更快学习
- Most commonly used for efficiency and in the hidden layers of feed forward neural networks — 最常用于前馈神经网络的隐藏层中，效率高

> **📝 Notes:**
>
> **📌 What:**
> **(1) Activation Function (激活函数):**
>
> A mathematical function applied to the output of each neuron. It determines whether the neuron "fires" (produces output) and introduces nonlinearity into the network.
>
>> 应用于每个神经元输出的数学函数。它决定神经元是否"激活"（产生输出），并向网络引入非线性。
>>
>
> **(2) Three Main Types (三种主要类型):**
>
> Sigmoid: output [0,1], good for binary classification output. Tanh: output [-1,1], zero-centered. ReLU: output [0,∞), most widely used in hidden layers.
>
>> Sigmoid：输出[0,1]，适合二分类输出。Tanh：输出[-1,1]，零中心。ReLU：输出[0,∞)，隐藏层最广泛使用。
>>
>
> **🎯 Why:**
> **(1) Without activation, network is just linear (没有激活函数，网络只是线性的):**
>
> Without nonlinear activation, stacking 100 linear layers = 1 linear layer (matrix multiplication is closed under composition). The network could only learn linear relationships, which is insufficient for complex tasks like image classification.
>
>> 没有非线性激活，堆叠100个线性层 = 1个线性层（矩阵乘法在复合下封闭）。网络只能学习线性关系，不足以处理图像分类等复杂任务。
>>
>
> **(2) Vanishing gradient problem (梯度消失问题):**
>
> Sigmoid and Tanh squash inputs to small ranges. For extreme values, gradients → 0. During backprop, gradients multiply through layers, so small gradients compound → early layers barely learn. ReLU solves this for positive inputs.
>
>> Sigmoid和Tanh将输入压缩到小范围。对于极端值，梯度→0。反向传播时梯度逐层相乘，小梯度复合 → 早期层几乎不学习。ReLU对正输入解决了这个问题。
>>
>
> **💡 Intuition:**
> **(1) Light switch analogy (灯开关类比):**
>
> ReLU is like a light switch: negative input = OFF (output 0), positive input = ON (output = input). Simple, fast, and effective. No gradual dimming like Sigmoid.
>
>> ReLU像灯开关：负输入 = 关（输出0），正输入 = 开（输出=输入）。简单、快速、有效。不像Sigmoid那样渐变。
>>
>
> **(2) Why ReLU dominates (为什么ReLU占主导):**
>
> ReLU has constant gradient (1) for positive inputs → no vanishing gradient. It's also computationally trivial: just max(0, x). No exponentials like sigmoid/tanh.
>
>> ReLU对正输入有恒定梯度(1) → 无梯度消失。计算也很简单：只是max(0, x)。不像sigmoid/tanh需要指数运算。
>>
>
> **📐 Formula:**
> **(1) Sigmoid (简单形式):**
>
> σ(x) = 1 / (1 + e⁻ˣ) → output always in (0, 1). Derivative: σ'(x) = σ(x)(1 − σ(x)), max at x=0 where σ'(0) = 0.25
>
>> σ(x) = 1 / (1 + e⁻ˣ) → 输出始终在(0,1)。导数：σ'(x) = σ(x)(1−σ(x))，x=0时最大值0.25
>>
>
> **(2) Tanh (双曲正切):**
>
> f(x) = (eˣ − e⁻ˣ)/(eˣ + e⁻ˣ) → output in (-1, 1). Zero-centered (unlike sigmoid). Derivative: f'(x) = 1 − f(x)²
>
>> f(x) = (eˣ−e⁻ˣ)/(eˣ+e⁻ˣ) → 输出在(-1,1)。零中心（不同sigmoid）。导数：f'(x) = 1−f(x)²
>>
>
> **(3) ReLU (线性整流):**
>
> f(x) = max(0, x) → output in [0, ∞). Derivative: 0 for x<0, 1 for x>0 (undefined at x=0, typically set to 0)
>
>> f(x) = max(0, x) → 输出在[0,∞)。导数：x<0时0，x>0时1
>>
>
> **🔢 Example:**
> **(1) Sigmoid vs ReLU comparison (Sigmoid与ReLU对比):**
>
> **Problem:** A neuron receives an input sum of z = -2.0. What will be the output if the activation function is Sigmoid? What if it's ReLU?
> **Solution:**
> - For Sigmoid: σ(-2) = 1 / (1 + e²) ≈ 1 / (1 + 7.389) = 1 / 8.389 ≈ **0.119** (small positive signal).
> - For ReLU: max(0, -2) = **0** (neuron is completely turned off).
>
>> **题目：** 神经元接收到的输入总和为 z = -2.0。如果激活函数是Sigmoid，输出是多少？如果是ReLU呢？
>> **解：**
>> - 计算Sigmoid：σ(-2) = 1 / (1 + e²) ≈ 1 / (1 + 7.389) = 1 / 8.389 ≈ **0.119** （微弱的正信号）。
>> - 计算ReLU：max(0, -2) = **0** （神经元完全关闭）。
>>
>
> **⚖️ Compare:**
> **(1) Sigmoid vs Tanh vs ReLU (三种激活函数对比):**
>
> | Property | Sigmoid | Tanh | ReLU |
> |---|---|---|---|
> | Range | (0, 1) | (-1, 1) | [0, ∞) |
> | Zero-centered | ✘ | ✔ | ✘ |
> | Vanishing gradient | ✔ (severe) | ✔ (less severe) | ✘ (for x>0) |
> | Computation | Slow (exp) | Slow (exp) | Fast (max) |
> | Best use | Output (binary) | Hidden (NLP) | Hidden (CV) |
>
>> | 属性 | Sigmoid | Tanh | ReLU |
>> |---|---|---|---|
>> | 范围 | (0, 1) | (-1, 1) | [0, ∞) |
>> | 零中心 | ✘ | ✔ | ✘ |
>> | 梯度消失 | ✔（严重） | ✔（较轻） | ✘（x>0时） |
>> | 计算速度 | 慢（exp） | 慢（exp） | 快（max） |
>> | 最佳用途 | 输出层（二分类） | 隐藏层（NLP） | 隐藏层（CV） |
>>
>
> **⚠️ Pitfall:**
> **(1) Dead ReLU problem (死ReLU问题):**
>
> If a neuron's input is always negative, ReLU output is always 0, gradient is always 0, and the neuron never updates — it's "dead". Solution: use Leaky ReLU (small slope for negative inputs).
>
>> 如果神经元输入始终为负，ReLU输出始终为0，梯度始终为0，神经元永不更新——它"死"了。解决方案：使用Leaky ReLU（负输入用小斜率）。
>>
>
> **(2) Using Sigmoid in hidden layers (在隐藏层使用Sigmoid):**
>
> A common beginner mistake. Sigmoid should generally be used only in the output layer for binary classification. In hidden layers, ReLU trains much faster and avoids vanishing gradients.
>
>> 初学者常见错误。Sigmoid通常应仅用于二分类的输出层。在隐藏层中，ReLU训练更快且避免梯度消失。
>>
>
> **📝 Exam:**
> **(1) 对比题 (Comparison):**
> "Compare Sigmoid, Tanh, and ReLU." → Answer with range, vanishing gradient behavior, and typical use case for each.
>
>> "比较Sigmoid、Tanh和ReLU。" → 用范围、梯度消失行为和典型用例回答。
>>
>
> **(2) 推理题 (Reasoning):**
> "Why is ReLU preferred over Sigmoid in hidden layers?" → No vanishing gradient for positive inputs (gradient = 1), computationally cheaper (no exp), promotes sparsity.
>
>> "为什么隐藏层优先使用ReLU而非Sigmoid？" → 正输入无梯度消失（梯度=1），计算更廉价（无exp），促进稀疏性。
>>

---

## 6. 损失函数 (Loss Functions)

![Page 14](week5_deep_learning_slides_pages/page_014.png)

**Loss functions slide:** Title "Loss Functions" in green on white background. Four main bullet points describing loss functions, followed by sub-bullets listing specific loss function types: Mean Squared Error (with formula), Cross-Entropy loss, Binary Cross-Entropy Loss, and Categorical Cross-Entropy Loss. MSE formula shown as mathematical notation.

**损失函数页：** 白色背景，标题"Loss Functions"为绿色。四个主要要点描述损失函数，后跟列出特定损失函数类型的子要点：均方误差（含公式）、交叉熵损失、二元交叉熵损失和分类交叉熵损失。MSE公式以数学符号显示。

- A loss function is a mathematical function that measures how well a model's predictions match the true outcomes — 损失函数是衡量模型预测与真实结果匹配程度的数学函数
- Quantify the difference between model predictions and true outcome — 量化模型预测与真实结果之间的差异
- The goal of a loss function is to guide optimization algorithms in adjusting model parameters (weight, bias, convolutional filter values etc) to reduce this loss over time — 损失函数的目标是引导优化算法调整模型参数（权重、偏置、卷积滤波器值等）以逐步减少损失
- Appropriate loss function is vital for successful CNN training — 适当的损失函数对CNN训练成功至关重要
- Example for loss function that are commonly used include: — 常用损失函数示例包括：
  - **Mean Squared Error** — 均方误差
  - **Cross-Entropy loss** — 交叉熵损失
  - **Binary Cross-Entropy Loss (log loss)** - For binary classification, whose output is probability value between 0 and 1 — 二元交叉熵损失（对数损失）- 用于二分类，输出为0到1之间的概率值
  - **Categorical Cross-Entropy Loss** – For multiclass classification problems, whose output is probability distribution over multiple classes — 分类交叉熵损失——用于多分类问题，输出为多个类别上的概率分布

- **MSE (Mean Squared Error)** = (1/N) Σᵢ (yᵢ - ŷᵢ)²
  - N = total number of samples (样本总数)
  - yᵢ = actual true value for sample i (样本i的真实类别/值)
  - ŷᵢ = model prediction for sample i (模型对样本i的预测值)
  - Overall: measures average squared difference between predictions and actuals. (总体：测量预测和真实值之间的平均平方差。)

- **BCE (Binary Cross-Entropy)** = -(1/N) Σᵢ [ yᵢ·log(ŷᵢ) + (1-yᵢ)·log(1-ŷᵢ) ]
  - yᵢ = actual binary class label (0 or 1) (实际二分类标签，0或1)
  - ŷᵢ = predicted probability of class 1 (预测为类1的概率)
  - Overall: guides binary classification by heavily penalizing confident wrong predictions. (总体：通过重度惩罚自信的错误预测来指导二分类。)

- **CCE (Categorical Cross-Entropy)** = -(1/N) Σᵢ Σⱼ yᵢⱼ·log(ŷᵢⱼ)
  - N = total number of samples (样本总数)
  - C = number of classes (类别数)
  - yᵢⱼ = one-hot encoded true label for sample i, class j (1 if sample i belongs to class j, else 0) (样本i类别j的one-hot编码真实标签，属于该类为1否则为0)
  - ŷᵢⱼ = predicted probability of sample i belonging to class j, output of softmax (样本i属于类别j的预测概率，softmax的输出)
  - Overall: generalizes BCE to multi-class; only the true class's predicted probability contributes to the loss. (总体：将BCE推广到多分类；只有真实类别的预测概率对损失有贡献。)

> **📝 Notes:**
>
> **📌 What:**
> **(1) Loss Function (损失函数):**
>
> A mathematical function that measures the discrepancy between the model's predictions and the true labels. It produces a single scalar value — the "loss" — that the optimizer tries to minimize.
>
>> 衡量模型预测与真实标签之间差异的数学函数。它产生一个标量值——"损失"——优化器试图最小化它。
>>
>
> **(2) Task-to-Loss Mapping (任务与损失函数的映射):**
>
> Binary classification → Binary Cross-Entropy (BCE). Multi-class classification → Categorical Cross-Entropy (CCE). Regression → Mean Squared Error (MSE).
>
>> 二分类 → 二元交叉熵（BCE）。多分类 → 分类交叉熵（CCE）。回归 → 均方误差（MSE）。
>>
>
> **🎯 Why:**
> **(1) Loss guides learning (损失引导学习):**
>
> Without a loss function, the network has no feedback. Loss tells the optimizer "how wrong" the prediction is. The optimizer then adjusts weights to reduce this error.
>
>> 没有损失函数，网络没有反馈。损失告诉优化器预测"错了多少"。优化器然后调整权重以减少此误差。
>>
>
> **(2) Wrong loss = wrong optimization (错误的损失 = 错误的优化):**
>
> Using MSE for classification makes the model optimize for distance instead of probability. Cross-entropy properly penalizes confident wrong predictions (e.g., predicting 0.99 for the wrong class).
>
>> 对分类使用MSE会让模型优化距离而非概率。交叉熵正确地惩罚自信的错误预测（如对错误类别预测0.99）。
>>
>
> **💡 Intuition:**
> **(1) GPS distance analogy (GPS距离类比):**
>
> Loss is like GPS distance to your destination. A high loss value = you're far from the goal. The optimizer's job is to take steps that reduce this distance. Different loss functions = different ways of measuring "how far."
>
>> 损失像GPS到目的地的距离。高损失值 = 离目标很远。优化器的工作是采取减少这个距离的步骤。不同损失函数 = 不同的"多远"度量方式。
>>
>
> **(2) Why cross-entropy for classification (为什么分类用交叉熵):**
>
> MSE treats [0.9, 0.1] and [0.99, 0.01] similarly (small difference). Cross-entropy heavily penalizes confident wrong predictions: predicting 0.01 for the correct class produces a loss of -log(0.01) = 4.6, much larger than -log(0.9) = 0.1.
>
>> MSE对[0.9, 0.1]和[0.99, 0.01]处理类似（差异小）。交叉熵严重惩罚自信的错误预测：对正确类别预测0.01产生损失-log(0.01)=4.6，远大于-log(0.9)=0.1。
>>
>
> **📐 Formula:**
> **(1) MSE breakdown (MSE公式拆解):**
>
> Reading MSE = (1/N) Σᵢ (yᵢ - ŷᵢ)² piece by piece:
> - (yᵢ - ŷᵢ): the error — difference between true value and predicted value for sample i
> - (…)²: squaring penalizes large errors more heavily (error of 2 → penalty 4, error of 10 → penalty 100)
> - Σᵢ: sum across all N samples in the batch
> - (1/N): average to make loss independent of batch size
> - Overall: "how far off are we on average, with extra penalty for big mistakes?"
>
>> 逐段解读 MSE = (1/N) Σᵢ (yᵢ - ŷᵢ)²：
>> - (yᵢ - ŷᵢ)：误差——样本i的真实值与预测值之差
>> - (…)²：平方使大误差受到更重的惩罚（误差2 → 惩罚4，误差10 → 惩罚100）
>> - Σᵢ：对批次中所有N个样本求和
>> - (1/N)：取平均使损失不依赖于批次大小
>> - 总体："平均来看我们偏离了多少，大错误额外惩罚？"
>>
>
> **(2) BCE breakdown (BCE公式拆解):**
>
> Reading BCE = -(1/N) Σᵢ [ yᵢ·log(ŷᵢ) + (1-yᵢ)·log(1-ŷᵢ) ]
> - (1/N) Σᵢ: average over all N samples in the batch
> - yᵢ·log(ŷᵢ): active only when true class is 1. If ŷᵢ is close to 1, log(1)=0 (no loss). If ŷᵢ approaches 0, log(0)→-∞ (huge loss penalty).
> - (1-yᵢ)·log(1-ŷᵢ): active only when true class is 0. If ŷᵢ is close to 0, log(1-0)=0 (no loss).
> - The minus sign (-) at the front flips the negative log values to positive, so loss ≥ 0.
> - Overall: ensures the model correctly pushes predicted probabilities near their true 0/1 labels.
>
>> 逐段解读 BCE = -(1/N) Σᵢ [ yᵢ·log(ŷᵢ) + (1-yᵢ)·log(1-ŷᵢ) ]：
>> - (1/N) Σᵢ：对批次中所有N个样本求平均
>> - yᵢ·log(ŷᵢ)：仅当真实类为1时激活。若预测ŷᵢ接近1，log(1)=0（无损失）。若ŷᵢ接近0，log(0)→-∞（巨大惩罚）。
>> - (1-yᵢ)·log(1-ŷᵢ)：仅当真实类为0时激活。若预测ŷᵢ接近0，log(1-0)=0（无损失）。
>> - 前面的负号(-)将负对数值翻转为正值，使损失≥0。
>> - 总体：确保模型正确地将预测概率推向其真实的0/1标签。
>>
>
> **(3) CCE breakdown (CCE公式拆解):**
>
> Reading CCE = -(1/N) Σᵢ Σⱼ yᵢⱼ·log(ŷᵢⱼ) piece by piece:
> - Σᵢ: iterate over all N samples in the batch
> - Σⱼ: iterate over all C classes for each sample
> - yᵢⱼ: one-hot label — equals 1 only for the true class, 0 for all others. So the inner sum collapses to just -log(ŷᵢ,true).
> - log(ŷᵢ,true): if model predicts true class with high probability (ŷ→1), log(1)→0 (no loss). If ŷ→0, log(0)→-∞ (huge penalty).
> - (1/N): average over the batch
> - Overall: only the true class's predicted probability matters — push it as close to 1 as possible.
>
>> 逐段解读 CCE = -(1/N) Σᵢ Σⱼ yᵢⱼ·log(ŷᵢⱼ)：
>> - Σᵢ：遍历批次中所有N个样本
>> - Σⱼ：遍历每个样本的所有C个类别
>> - yᵢⱼ：one-hot标签——仅对真实类别为1，其余全为0。所以内层求和塌缩为 -log(ŷᵢ,真实类)。
>> - log(ŷᵢ,真实类)：若模型以高概率预测真实类（ŷ→1），log(1)→0（无损失）。若ŷ→0，log(0)→-∞（巨大惩罚）。
>> - (1/N)：对批次取平均
>> - 总体：只有真实类别的预测概率有贡献——尽可能推向1。
>>
>
> **🔢 Example:**
> **(1) MSE calculation (MSE计算):**
>
> **Problem:** A regression model predicts house prices for 3 houses. True prices: y = [200, 300, 500] (in $1000). Predicted: ŷ = [210, 280, 520]. Calculate MSE.
> **Solution:**
> - Errors: (200-210)² = 100, (300-280)² = 400, (500-520)² = 400
> - Sum = 100 + 400 + 400 = 900
> - MSE = 900 / 3 = **300**
> - *Interpretation: on average, squared prediction error is 300. Note the two 20-unit errors contribute more than the 10-unit error due to squaring.*
>
>> **题目：** 回归模型预测3栋房屋价格。真实价格：y = [200, 300, 500]（单位：千元）。预测：ŷ = [210, 280, 520]。计算MSE。
>> **解：**
>> - 误差：(200-210)² = 100, (300-280)² = 400, (500-520)² = 400
>> - 总和 = 100 + 400 + 400 = 900
>> - MSE = 900 / 3 = **300**
>> - *解读：平均平方预测误差为300。注意两个20单位的误差由于平方比10单位的误差贡献更多。*
>>
>
> **(2) BCE calculation (BCE计算):**
>
> **Problem:** We have a batch of 2 binary samples. Sample 1: true y₁=1, predicted probability ŷ₁=0.9. Sample 2: true y₂=0, predicted probability ŷ₂=0.8. Calculate BCE (using natural log, ln).
> **Solution:**
> - Sample 1 loss = -[1·ln(0.9) + 0] = -(-0.105) = 0.105
> - Sample 2 loss = -[0 + 1·ln(1-0.8)] = -ln(0.2) = 1.609
> - BCE = (0.105 + 1.609) / 2 = 1.714 / 2 = **0.857**
> - *Notice how Sample 2 (confident wrong prediction of 0.8 for class 0) contributed mostly to the total loss.*
>
>> **题目：** 包含2个二分类样本的批次。样本1：真实y₁=1，预测概率ŷ₁=0.9。样本2：真实y₂=0，预测概率ŷ₂=0.8。计算BCE（使用自然对数ln）。
>> **解：**
>> - 样本1损失 = -[1·ln(0.9) + 0] = -(-0.105) = 0.105
>> - 样本2损失 = -[0 + 1·ln(1-0.8)] = -ln(0.2) = 1.609
>> - BCE = (0.105 + 1.609) / 2 = 1.714 / 2 = **0.857**
>> - *注意样本2（对类别0的自信错误预测0.8）贡献了总损失的绝大部分。*
>>
>
> **(3) CCE calculation (CCE计算):**
>
> **Problem:** A 3-class classifier predicts for 1 sample. True label: class 2 → one-hot y = [0, 1, 0]. Predicted probabilities (softmax output): ŷ = [0.1, 0.7, 0.2]. Calculate CCE for this sample (using natural log, ln).
> **Solution:**
> - CCE = -Σⱼ yⱼ·ln(ŷⱼ) = -[0·ln(0.1) + 1·ln(0.7) + 0·ln(0.2)]
> - Only the true class (j=2) contributes: -ln(0.7) = -(-0.357) = **0.357**
> - *If the model had predicted ŷ = [0.1, 0.95, 0.05] instead, loss = -ln(0.95) = 0.051 — much lower. If ŷ = [0.8, 0.1, 0.1], loss = -ln(0.1) = 2.303 — very high penalty for confident wrong prediction.*
>
>> **题目：** 一个3分类器对1个样本预测。真实标签：类别2 → one-hot y = [0, 1, 0]。预测概率（softmax输出）：ŷ = [0.1, 0.7, 0.2]。计算该样本的CCE（使用自然对数ln）。
>> **解：**
>> - CCE = -Σⱼ yⱼ·ln(ŷⱼ) = -[0·ln(0.1) + 1·ln(0.7) + 0·ln(0.2)]
>> - 仅真实类别（j=2）有贡献：-ln(0.7) = -(-0.357) = **0.357**
>> - *若模型预测ŷ = [0.1, 0.95, 0.05]，损失 = -ln(0.95) = 0.051——低得多。若ŷ = [0.8, 0.1, 0.1]，损失 = -ln(0.1) = 2.303——对自信错误预测的巨大惩罚。*
>>
>
> **⚖️ Compare:**
> **(1) Loss functions by task (按任务分类的损失函数):**
>
> | Loss Function | Task | Output |
> |---|---|---|
> | MSE | Regression | Continuous value |
> | Binary Cross-Entropy | Binary classification | Probability [0,1] |
> | Categorical Cross-Entropy | Multi-class | Probability distribution |
>
>> | 损失函数 | 任务 | 输出 |
>> |---|---|---|
>> | MSE | 回归 | 连续值 |
>> | 二元交叉熵 | 二分类 | 概率[0,1] |
>> | 分类交叉熵 | 多分类 | 概率分布 |
>>
>
> **⚠️ Pitfall:**
> **(1) MSE for classification (分类用MSE):**
>
> MSE is designed for regression. Using it for classification leads to slow convergence and poor probability calibration. Always use cross-entropy for classification tasks.
>
>> MSE是为回归设计的。分类用MSE会导致收敛慢且概率校准差。分类任务始终使用交叉熵。
>>
>
> **(2) BCE vs CCE confusion (BCE和CCE混淆):**
>
> BCE: one output neuron, sigmoid activation, for 2-class problems. CCE: N output neurons (one per class), softmax activation, for N-class problems. Using the wrong one produces incorrect gradients.
>
>> BCE：一个输出神经元，sigmoid激活，用于2类问题。CCE：N个输出神经元（每类一个），softmax激活，用于N类问题。用错会产生错误梯度。
>>
>
> **📝 Exam:**
> **(1) 匹配题 (Matching):**
> "Match the loss function to the task: regression, binary classification, multi-class." → MSE, BCE, CCE.
>
>> "将损失函数与任务匹配：回归、二分类、多分类。" → MSE、BCE、CCE。
>>
>
> **(2) 推理题 (Reasoning):**
> "Why is cross-entropy preferred over MSE for classification?" → Cross-entropy heavily penalizes confident wrong predictions and produces larger gradients for faster learning.
>
>> "为什么分类优先用交叉熵而非MSE？" → 交叉熵严重惩罚自信的错误预测，产生更大梯度以加快学习。
>>

---

## 7. 梯度下降与反向传播 (Gradient Descent & Back Propagation)

### 7.1 梯度下降 (Gradient Descent)

![Page 15](week5_deep_learning_slides_pages/page_015.png)

**Gradient descent slide:** Title "Gradient Descent" in green on white background. Three bullet points describing gradient descent as an optimization algorithm. Right side: 3D surface plot showing the loss landscape with a red path descending from a high point to the minimum, illustrating the gradient descent process.

**梯度下降页：** 白色背景，标题"Gradient Descent"为绿色。三个要点描述梯度下降作为优化算法。右侧：3D曲面图展示损失曲面，红色路径从高点下降到最小值，说明梯度下降过程。

- Most models use gradient descent or its variants to minimize the loss — 大多数模型使用梯度下降或其变体来最小化损失
- It is an optimizing algorithm which is used to iterate through different combinations of weights to find the best combination of weights that minimizes the error — 它是一种优化算法，用于迭代不同的权重组合以找到使误差最小化的最佳权重组合
- The algorithm calculates the gradient of the loss function with respect to the model parameters and updates the parameters in the opposite direction of the gradient. — 该算法计算损失函数相对于模型参数的梯度，并在梯度的反方向更新参数。

### 7.2 反向传播概述 (Back Propagation Overview)

![Page 16](week5_deep_learning_slides_pages/page_016.png)

**Back propagation overview slide:** Title "Back Propagation" in green on white background. Two introductory bullet points followed by a numbered list of 6 basic steps. Right side: a neural network diagram showing forward pass (blue arrows) and backward pass (red arrows) through multiple layers.

**反向传播概述页：** 白色背景，标题"Back Propagation"为绿色。两个介绍性要点，后跟6个基本步骤的编号列表。右侧：神经网络示意图，展示通过多层的前向传播（蓝色箭头）和反向传播（红色箭头）。

- A critical algorithm in training CNN used to compute gradients of the loss function with respect to the weights in a neural network. — 训练CNN的关键算法，用于计算损失函数相对于神经网络权重的梯度。
- It happens only during training — 仅在训练期间发生
- Basic Steps are: — 基本步骤是：
  1. Feed a sample to the network — 将样本馈入网络
  2. Calculate the mean squared error — 计算均方误差
  3. Calculate the error term of each output neuron — 计算每个输出神经元的误差项
  4. Iteratively calculate the error terms in the hidden layers — 迭代计算隐藏层的误差项
  5. Apply the delta rule — 应用delta规则
  6. Adjust the weights — 调整权重

### 7.3 反向传播步骤详解 (Back Propagation Steps)

![Page 17](week5_deep_learning_slides_pages/page_017.png)

**Back propagation Step 1 slide:** Title "Step 1: Feed a sample to the Network" on white background. Shows a neural network diagram with input values being fed into the network, with weights labeled on connections and neuron outputs calculated at each node.

**反向传播步骤1页：** 白色背景，标题"Step 1: Feed a sample to the Network"。展示神经网络示意图，输入值被馈入网络，连接上标注权重，每个节点计算神经元输出。

- **Step 1: Feed a sample to the Network** — 步骤1：将样本馈入网络

![Page 18](week5_deep_learning_slides_pages/page_018.png)

**Back propagation Step 2 slide:** Title "Step 2: Calculate Mean Squared Error" on white background. Shows the same network with the MSE calculation applied to the output, displaying the formula and computed error value.

**反向传播步骤2页：** 白色背景，标题"Step 2: Calculate Mean Squared Error"。展示同一网络，对输出应用MSE计算，显示公式和计算出的误差值。

- **Step 2: Calculate Mean Squared Error** — 步骤2：计算均方误差

![Page 19](week5_deep_learning_slides_pages/page_019.png)

**Back propagation Step 3 slide:** Title "Step 3: Calculate the Output Error Terms" on white background. Shows the neural network with output error term calculations highlighted, displaying the partial derivative computations at the output layer.

**反向传播步骤3页：** 白色背景，标题"Step 3: Calculate the Output Error Terms"。展示神经网络，突出输出误差项计算，显示输出层的偏导数计算。

- **Step 3: Calculate the Output Error Terms** — 步骤3：计算输出误差项

![Page 20](week5_deep_learning_slides_pages/page_020.png)

**Back propagation Step 4 slide:** Title "Step 4: Calculate the Hidden Layer Error Terms" on white background. Shows the neural network with error propagation from output layer back to hidden layers, with mathematical formulas for computing hidden layer error terms.

**反向传播步骤4页：** 白色背景，标题"Step 4: Calculate the Hidden Layer Error Terms"。展示神经网络，误差从输出层反向传播到隐藏层，显示计算隐藏层误差项的数学公式。

- **Step 4: Calculate the Hidden Layer Error Terms** — 步骤4：计算隐藏层误差项

![Page 21](week5_deep_learning_slides_pages/page_021.png)

**Back propagation Step 5 slide:** Title "Step 5: Apply the Delta Rule" on white background. Shows the delta rule formula and its application to compute weight updates using the error terms and learning rate.

**反向传播步骤5页：** 白色背景，标题"Step 5: Apply the Delta Rule"。展示delta规则公式及其应用，使用误差项和学习率计算权重更新。

- **Step 5: Apply the Delta Rule** — 步骤5：应用Delta规则

![Page 22](week5_deep_learning_slides_pages/page_022.png)

**Back propagation Step 6 slide:** Title "Step 6: Adjust the Weights" on white background. Shows the final step of updating all weights in the network using the computed delta values, with the updated weight values displayed on the connections.

**反向传播步骤6页：** 白色背景，标题"Step 6: Adjust the Weights"。展示使用计算出的delta值更新网络中所有权重的最终步骤，连接上显示更新后的权重值。

- **Step 6: Adjust the Weights** — 步骤6：调整权重

- **Weight Update Formula** = w_new = w_old - η * (∂L/∂w)
  - w_new = updated weight after taking a step (迈出一步后更新的权重)
  - w_old = current weight value (当前权重值)
  - η (eta) = learning rate, a hyperparameter controlling step size (学习率，控制步长的超参数)
  - ∂L/∂w = gradient of the loss L with respect to the weight w (损失L对权重w的梯度)
  - Overall: Move the weight opposite to the gradient to decrease the loss. (总体：朝梯度的反方向移动权重以减少损失。)

> **📝 Notes:**
>
> **📌 What:**
> **(1) Gradient Descent (梯度下降):**
>
> An optimization algorithm that iteratively adjusts weights in the direction that reduces the loss function. It calculates the gradient (slope) and steps in the opposite direction.
>
>> 一种迭代调整权重以减少损失函数的优化算法。它计算梯度（斜率）并朝相反方向前进。
>>
>
> **(2) Backpropagation (反向传播):**
>
> The algorithm that computes gradients of the loss w.r.t. each weight by applying the chain rule backward through the network. The 6 steps: feed input → compute MSE → output error terms → hidden layer error terms → delta rule → adjust weights.
>
>> 通过在网络中反向应用链式法则计算损失对每个权重的梯度的算法。6个步骤：输入数据 → 计算MSE → 输出误差项 → 隐藏层误差项 → delta规则 → 调整权重。
>>
>
> **🎯 Why:**
> **(1) Need to know "which weights caused the error" (需要知道"哪些权重导致了误差"):**
>
> With millions of weights, you can't randomly adjust them. Backprop uses calculus to compute exactly how much each weight contributed to the error, enabling efficient targeted updates.
>
>> 有数百万个权重，不能随机调整。反向传播用微积分精确计算每个权重对误差的贡献，实现高效的定向更新。
>>
>
> **(2) Only happens during training (仅在训练时发生):**
>
> During inference (prediction), only forward propagation runs. Backprop is computationally expensive and only needed when learning.
>
>> 推理（预测）时只运行前向传播。反向传播计算成本高，只在学习时需要。
>>
>
> **💡 Intuition:**
> **(1) Blindfolded hiker analogy (蒙眼登山者类比):**
>
> Gradient descent is like being blindfolded on a mountain, trying to reach the valley. You feel the slope under your feet (gradient) and step downhill (opposite direction of gradient). Step size = learning rate.
>
>> 梯度下降像蒙着眼睛在山上试图到达山谷。你感受脚下的坡度（梯度）然后向下坡方向走（梯度反方向）。步长 = 学习率。
>>
>
> **(2) Chain rule as blame assignment (链式法则作为责任分配):**
>
> Backprop uses the chain rule to "assign blame." If output is wrong, how much blame goes to the last layer? Then how much of THAT blame goes to the second-to-last layer? This cascading blame assignment reaches every weight.
>
>> 反向传播用链式法则"分配责任"。如果输出错了，多少责任归于最后一层？然后那个责任中多少归于倒数第二层？这种级联责任分配到达每个权重。
>>
>
> **⚙️ How:**
> **(1) Weight update formula (权重更新公式):**
>
> w_new = w_old − η × (∂L/∂w), where η = learning rate, ∂L/∂w = gradient of loss w.r.t. weight. The learning rate controls how big each step is.
>
>> w_new = w_old − η × (∂L/∂w)，其中η = 学习率，∂L/∂w = 损失对权重的梯度。学习率控制每步的大小。
>>
>
> **(2) Chain rule in action (链式法则实践):**
>
> ∂L/∂w = (∂L/∂output) × (∂output/∂activation) × (∂activation/∂w). Each factor is computed layer by layer, from output back to input.
>
>> ∂L/∂w = (∂L/∂输出) × (∂输出/∂激活) × (∂激活/∂w)。每个因子逐层计算，从输出回到输入。
>>
>
> **📐 Formula:**
> **(1) Weight update rule (权重更新规则):**
>
> Reading w_new = w_old - η * (∂L/∂w) piece by piece:
> - w_old: current position on the loss surface.
> - (∂L/∂w): gradient, pointing to the steepest ascent (how to increase loss).
> - (-): minus sign reverses the direction, pointing downhill towards the minimum.
> - η: learning rate, scales the jump distance.
> - w_new: the adjusted weight, hopefully resulting in lower loss.
>
>> 逐段解读公式 w_new = w_old - η * (∂L/∂w)：
>> - w_old：当前在损失曲面上的位置。
>> - (∂L/∂w)：梯度，指向最陡上升方向（即如何增加损失的方向）。
>> - (-)：负号反转方向，指向下坡迈向最小值。
>> - η：学习率，缩放跳跃距离。
>> - w_new：调整后的权重，期望带来更低的损失。
>>
>
> **🔢 Example:**
> **(1) Weight update calculation (权重更新计算):**
>
> **Problem:** A CNN filter weight is currently w=0.5. After backprop calculation, its gradient ∂L/∂w = 0.2. The learning rate is set to η = 0.1. What is the new weight?
> **Solution:**
> - Update step = - η * (∂L/∂w) = -0.1 * 0.2 = -0.02
> - w_new = w_old + step = 0.5 - 0.02 = **0.48**
> - *Note: gradient was positive (larger weight increases loss), so the optimizer correctly decreased the actual weight.*
>
>> **题目：** 某CNN滤波器当前权重w=0.5。反向传播计算后，其梯度∂L/∂w = 0.2。学习率设为η = 0.1。新权重是多少？
>> **解：**
>> - 更新步长 = - η * (∂L/∂w) = -0.1 * 0.2 = -0.02
>> - w_new = w_old + step = 0.5 - 0.02 = **0.48**
>> - *注意：梯度为正（更大的权重会增加损失），因此优化器正确地减小了实际权重。*
>>
>
> **⚠️ Pitfall:**
> **(1) Learning rate too high (学习率太高):**
>
> Steps overshoot the minimum → loss oscillates or diverges. Like running down a hill so fast you fly past the valley and up the other side.
>
>> 步长超过最小值 → 损失振荡或发散。像下山跑太快，飞过山谷到了对面。
>>
>
> **(2) Learning rate too low (学习率太低):**
>
> Training takes extremely long and may get stuck in local minima. Like taking baby steps down the mountain — you might reach a small valley and think it's the lowest point.
>
>> 训练时间极长且可能陷入局部最小值。像踯着小步下山——可能到达一个小山谷就以为是最低点。
>>
>
> **📝 Exam:**
> **(1) 步骤题 (Steps):**
> "List the 6 basic steps of backpropagation." → Feed sample → calculate MSE → output error terms → hidden layer error terms → delta rule → adjust weights.
>
>> "列出反向传播的6个基本步骤。" → 输入样本 → 计算MSE → 输出误差项 → 隐藏层误差项 → delta规则 → 调整权重。
>>
>
> **(2) 概念题 (Concept):**
> "What is the role of learning rate in gradient descent?" → Controls step size. Too high: loss diverges. Too low: slow convergence, may get stuck in local minima.
>
>> "学习率在梯度下降中的作用是什么？" → 控制步长。太高：损失发散。太低：收敛慢，可能陷入局部最小值。
>>

---

## 8. 优化器 (Optimizers)

![Page 23](week5_deep_learning_slides_pages/page_023.png)

**Optimizers slide:** Title "Optimizers: Types and Their Impact on Training" on dark green background. Two paragraphs of text describing SGD, Adam, and RMSprop optimizers. Right side: illustration of a neural network with colorful gradient overlays representing optimization paths.

**优化器页：** 深绿背景，标题"Optimizers: Types and Their Impact on Training"。两段文字描述SGD、Adam和RMSprop优化器。右侧：带有彩色渐变覆盖的神经网络插图，表示优化路径。

- Optimizers in CNNs are algorithms used to adjust the weights of the network to minimize loss. — CNN中的优化器是用于调整网络权重以最小化损失的算法。
- Key types include SGD (Stochastic Gradient Descent), which is simple yet effective; Adam, known for its adaptiveness to different problems; and RMSprop, which adjusts the learning rate during training. — 关键类型包括SGD（随机梯度下降），简单而有效；Adam，以其对不同问题的适应性而闻名；以及RMSprop，在训练期间调整学习率。
- The choice of optimizer affects the speed and quality of training, and sometimes a combination of optimizers is used for different stages of training to achieve better results. — 优化器的选择影响训练的速度和质量，有时在训练的不同阶段使用优化器的组合以获得更好的结果。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Optimizer (优化器):**
>
> An algorithm that determines HOW to update weights given the gradients from backprop. Different optimizers use different strategies for step size and direction.
>
>> 给定反向传播的梯度，决定如何更新权重的算法。不同优化器对步长和方向使用不同策略。
>>
>
> **(2) Three Key Optimizers (三个关键优化器):**
>
> SGD: vanilla gradient descent with fixed learning rate. Adam: adaptive learning rates per parameter + momentum. RMSprop: adapts learning rate based on recent gradient magnitudes.
>
>> SGD：固定学习率的原始梯度下降。Adam：每个参数自适应学习率+动量。RMSprop：根据近期梯度幅值调整学习率。
>>
>
> **🎯 Why:**
> **(1) Fixed learning rate is suboptimal (固定学习率不最优):**
>
> Some parameters need large updates (rare features), others need small updates (frequent features). Adaptive optimizers like Adam handle this automatically.
>
>> 某些参数需要大更新（稀有特征），其他需要小更新（频繁特征）。Adam等自适应优化器自动处理。
>>
>
> **(2) Momentum prevents oscillation (动量防止振荡):**
>
> SGD can oscillate in narrow valleys. Momentum adds a "rolling ball" effect — past gradients contribute to current direction, smoothing the path and speeding convergence.
>
>> SGD在窄山谷中会振荡。动量添加"滚球"效应——过去梯度贡献于当前方向，平滑路径并加速收敛。
>>
>
> **💡 Intuition:**
> **(1) Car on a hilly road (丘陵公路上的车):**
>
> SGD = walking (slow, consistent). SGD+Momentum = rolling ball (gains speed on slopes). Adam = smart car with GPS (adjusts speed per terrain).
>
>> SGD = 步行（慢，稳定）。SGD+动量 = 滚球（在坡上加速）。Adam = 带GPS的智能车（根据地形调整速度）。
>>
>
> **(2) Adam = "best default" (Adam = "最佳默认选择"):**
>
> When in doubt, start with Adam. It works well across most problems without much hyperparameter tuning. Only switch if you have specific convergence issues.
>
>> 不确定时从 Adam 开始。它在大多数问题上表现良好，无需大量超参数调优。只有出现特定收敛问题时才切换。
>>
>
> **⚖️ Compare:**
> **(1) SGD vs RMSprop vs Adam (三种优化器对比):**
>
> | Optimizer | Learning Rate | Momentum | Best For |
> |---|---|---|---|
> | SGD | Fixed | Optional | Simple tasks, research |
> | RMSprop | Adaptive (per param) | No | RNNs, non-stationary |
> | Adam | Adaptive + momentum | Yes | General default choice |
>
>> | 优化器 | 学习率 | 动量 | 最适合 |
>> |---|---|---|---|
>> | SGD | 固定 | 可选 | 简单任务、研究 |
>> | RMSprop | 自适应（每参数） | 无 | RNN、非平稳 |
>> | Adam | 自适应+动量 | 有 | 通用默认选择 |
>>
>
> **⚠️ Pitfall:**
> **(1) Not tuning optimizer hyperparameters (不调优化器超参数):**
>
> Even Adam has hyperparameters (learning rate, beta1, beta2). The default lr=0.001 is good for most cases, but some tasks need tuning.
>
>> 即使Adam也有超参数（学习率、beta1、beta2）。默认lr=0.001对大多数情况很好，但某些任务需要调整。
>>
>
> **(2) Switching optimizers mid-training (训练中途切换优化器):**
>
> Can be done strategically (e.g., Adam for initial convergence, then SGD for fine-tuning), but doing it without understanding can reset momentum and harm convergence.
>
>> 可以策略性地做（如先用Adam初始收敛，再用SGD微调），但不理解地做会重置动量并损害收敛。
>>
>
> **📝 Exam:**
> **(1) 对比题 (Comparison):**
> "Compare SGD, RMSprop, and Adam." → Use table: fixed vs adaptive LR, with/without momentum, best use case.
>
>> "比较SGD、RMSprop和Adam。" → 用表格：固定vs自适应LR、有/无动量、最佳用例。
>>
>
> **(2) 推理题 (Reasoning):**
> "Why might Adam be preferred over SGD?" → Adaptive per-parameter learning rates + built-in momentum = faster convergence, less hyperparameter tuning.
>
>> "为什么可能优先选择Adam而非SGD？" → 每参数自适应学习率+内置动量 = 更快收敛，更少超参数调优。
>>

---

## 9. 训练CNN (Training a CNN)

![Page 24](week5_deep_learning_slides_pages/page_024.png)

**Training CNN slide:** Title "Training a CNN: Steps and Best Practices" on dark green background. Two paragraphs describing the training process: weight initialization, forward propagation, loss calculation, backpropagation, and best practices like validation, early stopping, and model checkpointing. Right side: training progress visualization showing loss/accuracy curves.

**训练CNN页：** 深绿背景，标题"Training a CNN: Steps and Best Practices"。两段文字描述训练过程：权重初始化、前向传播、损失计算、反向传播，以及验证、早停和模型检查点等最佳实践。右侧：训练进度可视化，展示损失/准确率曲线。

- Training a CNN involves initializing weights, forward propagation to get predictions, calculating loss, and backpropagation to calculate gradients and optimizers adjust weights. — 训练CNN涉及初始化权重、前向传播获得预测、计算损失以及反向传播计算梯度并由优化器调整权重。
- Best practices include using a validation set for hyperparameter tuning, applying early stopping to prevent overfitting, and periodically saving the model state for recovery. — 最佳实践包括使用验证集进行超参数调优、应用早停防止过拟合以及定期保存模型状态以便恢复。
- Monitoring training progress with metrics like loss and accuracy, both on training and validation sets, helps in understanding model performance and making necessary adjustments. — 使用损失和准确率等指标监控训练和验证集上的训练进度，有助于了解模型性能并进行必要调整。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Training Loop (训练循环):**
>
> For each epoch: forward pass (compute predictions) → loss calculation → backward pass (compute gradients) → optimizer step (update weights). Repeat until convergence.
>
>> 每个epoch：前向传播（计算预测） → 损失计算 → 反向传播（计算梯度） → 优化器步骤（更新权重）。重复直到收敛。
>>
>
> **(2) Best Practices (最佳实践):**
>
> Use validation set for hyperparameter tuning. Apply early stopping when validation loss starts increasing. Save model checkpoints periodically to prevent loss of progress.
>
>> 使用验证集调超参数。验证损失开始增加时应用早停。定期保存模型检查点以防止进度丢失。
>>
>
> **🎯 Why:**
> **(1) Monitoring prevents wasted effort (监控防止浪费努力):**
>
> Without monitoring loss curves, you might train for 100 epochs when the model converged at epoch 20 (wasting time) or started overfitting at epoch 30 (harming performance).
>
>> 不监控损失曲线，可能训练100个epoch而模型在第20epoch就收敛了（浪费时间）或在第30epoch开始过拟合（损害性能）。
>>
>
> **(2) Early stopping is cheap regularization (早停是廉价的正则化):**
>
> It prevents overfitting without changing the model architecture. Simply stop when validation performance degrades.
>
>> 它在不改变模型架构的情况下防止过拟合。简单地在验证性能下降时停止。
>>
>
> **💡 Intuition:**
> **(1) Cooking analogy (烹饪类比):**
>
> Training = cooking. Forward pass = taste the dish. Loss = how far from perfect. Backprop = figure out which ingredient to adjust. Optimizer = make the adjustment. Early stopping = don't overcook!
>
>> 训练 = 烹饪。前向传播 = 尝菜。损失 = 离完美多远。反向传播 = 搞清楚调整哪个作料。优化器 = 进行调整。早停 = 别烧糊！
>>
>
> **(2) Reading loss curves (解读损失曲线):**
>
> Healthy: both train and val loss decrease. Overfitting: train loss decreases but val loss increases. Underfitting: both remain high. Learning rate too high: loss oscillates wildly.
>
>> 健康：训练和验证损失都下降。过拟合：训练损失下降但验证损失增加。欠拟合：两者都保持高位。学习率太高：损失剧烈振荡。
>>
>
> **⚠️ Pitfall:**
> **(1) Training too long without validation (不用验证集训练太久):**
>
> Without a validation set, you have no signal for when to stop. The model will memorize training data and fail on new data.
>
>> 没有验证集，你没有何时停止的信号。模型会记忆训练数据并在新数据上失败。
>>
>
> **(2) Not saving checkpoints (不保存检查点):**
>
> If training crashes after 50 epochs and you didn't save, you lose all progress. Always save the best model (lowest validation loss) and periodic checkpoints.
>
>> 如果训练在50个epoch后崩溃而你没保存，所有进度都丢失。始终保存最佳模型（最低验证损失）和定期检查点。
>>
>
> **📝 Exam:**
> **(1) 流程题 (Process):**
> "Describe the CNN training loop." → Initialize weights → forward pass → loss calculation → backprop → optimizer updates weights → repeat for each epoch.
>
>> "描述CNN训练循环。" → 初始化权重 → 前向传播 → 损失计算 → 反向传播 → 优化器更新权重 → 每个epoch重复。
>>
>
> **(2) 曲线解读题 (Curve interpretation):**
> "Training loss decreases but validation loss increases. What's happening?" → Overfitting. Solutions: early stopping, dropout, data augmentation, regularization.
>
>> "训练损失下降但验证损失增加。发生了什么？" → 过拟合。解决方案：早停、dropout、数据增强、正则化。
>>

---

## 10. 过拟合与预防策略 (Overfitting & Prevention Strategies)

### 10.1 理解过拟合 (Understanding Overfitting)

![Page 25](week5_deep_learning_slides_pages/page_025.png)

**Overfitting slide:** Title "Understanding Overfitting in Deep Learning" on dark green background. Text describes overfitting as learning training data too well including noise and outliers. Right side: visualization comparing a well-fitted model (smooth curve) vs. an overfitted model (jagged curve following every data point), with training and validation accuracy gap illustrated.

**过拟合页：** 深绿背景，标题"Understanding Overfitting in Deep Learning"。文字描述过拟合为过度学习训练数据（包括噪声和异常值）。右侧：对比良好拟合模型（平滑曲线）和过拟合模型（跟随每个数据点的锯齿曲线）的可视化，并展示训练和验证准确率的差距。

- Overfitting occurs when a CNN model learns the training data too well, including its noise and outliers, leading to poor performance on new, unseen data. — 过拟合发生在CNN模型过度学习训练数据（包括其噪声和异常值）时，导致在新的、未见过的数据上表现不佳。
- This usually happens in overly complex models with too many parameters. — 这通常发生在参数过多的过度复杂模型中。
- Symptoms of overfitting include much higher accuracy on training data compared to validation data. — 过拟合的症状包括训练数据上的准确率远高于验证数据。

### 10.2 防止过拟合的策略 (Prevention Strategies)

![Page 26](week5_deep_learning_slides_pages/page_026.png)

**Prevention strategies slide:** Title "Strategies to Prevent Overfitting" on white background with green header bar. Five numbered strategies listed: dropout, regularization (L1/L2), data augmentation, model simplification, and early stopping. Each point provides a brief explanation.

**预防策略页：** 白色背景，绿色标题栏，标题"Strategies to Prevent Overfitting"。列出五个编号策略：dropout、正则化（L1/L2）、数据增强、模型简化和早停。每个要点提供简要解释。

**Strategies to Prevent Overfitting:** — **防止过拟合的策略：**

1. Use dropout layers which randomly deactivate certain neurons during training, preventing co-adaptation of features. — 使用dropout层在训练期间随机停用某些神经元，防止特征共适应。
2. Apply regularization methods like L1 (lasso) and L2 (ridge) which penalize large weights. — 应用L1（lasso）和L2（ridge）等正则化方法，惩罚大权重。
3. Augment the dataset to provide more varied training examples. — 增强数据集以提供更多样化的训练示例。
4. Simplify the model by reducing the number of layers or neurons. — 通过减少层数或神经元数来简化模型。
5. Early stopping halts training when performance on a validation set starts to degrade. — 当验证集上的性能开始下降时，早停会停止训练。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Overfitting (过拟合):**
>
> The model memorizes training data (including noise) instead of learning general patterns. It achieves low training loss but high validation/test loss.
>
>> 模型记忆训练数据（包括噪声）而非学习一般模式。训练损失低但验证/测试损失高。
>>
>
> **(2) Prevention Strategies (预防策略):**
>
> Key techniques: Dropout (randomly deactivate neurons), Regularization (L1/L2 penalty on weights), Data Augmentation (more varied training examples), Model Simplification (fewer layers/neurons), Early Stopping.
>
>> 关键技术：Dropout（随机停用神经元）、正则化（L1/L2权重惩罚）、数据增强（更多变化的训练样本）、模型简化（更少层/神经元）、早停。
>>
>
> **🎯 Why:**
> **(1) Generalization is the goal (泛化才是目标):**
>
> A model that scores 99% on training but 60% on new images is useless in production. The whole point of ML is to perform well on UNSEEN data.
>
>> 训练上99%但新图像上60%的模型在生产中无用。ML的整个目的是在未见数据上表现良好。
>>
>
> **(2) More capacity than data → memorization (容量超过数据 → 记忆):**
>
> A complex model with millions of parameters can memorize a small dataset entirely. Overfitting is essentially the model being "too smart" for the amount of data.
>
>> 拥有数百万参数的复杂模型可以完全记忆小数据集。过拟合本质上是模型对数据量来说"太聪明"了。
>>
>
> **💡 Intuition:**
> **(1) Student who memorizes answers (死记答案的学生):**
>
> Overfitting = a student who memorizes past exam answers word-for-word but can't solve new problems. They score perfectly on practice tests but fail the real exam.
>
>> 过拟合 = 一个逐字记忆过去考试答案但不能解决新问题的学生。练习测试满分但真正考试不及格。
>>
>
> **(2) Dropout as team training (Dropout作为团队训练):**
>
> Dropout randomly removes 20-50% of neurons each training step. Like a sports team where random players sit out each practice — everyone must learn to contribute, no one can freeload. This forces redundancy.
>
>> Dropout每个训练步骤随机移除20-50%的神经元。像运动队每次训练随机让部分球员休息——每个人都必须学会贡献，谁也不能偷懒。这迫使冗余。
>>
>
> **⚖️ Compare:**
> **(1) Overfitting prevention techniques (过拟合预防技术):**
>
> | Technique | Mechanism | When to Use |
> |---|---|---|
> | Dropout | Randomly deactivate neurons | Hidden layers; when model is too complex |
> | L2 Regularization | Penalize large weights | Always a good default |
> | Data Augmentation | Expand training set artificially | When dataset is small |
> | Early Stopping | Stop when val loss increases | Always during training |
> | Model Simplification | Reduce layers/neurons | When model is clearly too large |
>
>> | 技术 | 机制 | 何时使用 |
>> |---|---|---|
>> | Dropout | 随机停用神经元 | 隐藏层；模型太复杂时 |
>> | L2正则化 | 惩罚大权重 | 始终是好的默认 |
>> | 数据增强 | 人为扩展训练集 | 数据集小时 |
>> | 早停 | 验证损失增加时停止 | 训练时始终使用 |
>> | 模型简化 | 减少层/神经元 | 模型明显太大时 |
>>
>
> **⚠️ Pitfall:**
> **(1) Dropout at test time (测试时用Dropout):**
>
> Dropout is ONLY used during training. At test time, all neurons are active but outputs are scaled down. Forgetting to disable dropout at test time produces inconsistent predictions.
>
>> Dropout仅在训练时使用。测试时所有神经元都活跃但输出缩放。忘记在测试时禁用Dropout会产生不一致的预测。
>>
>
> **(2) Confusing overfitting with underfitting (混淆过拟合与欠拟合):**
>
> Overfitting: train loss low, val loss high. Underfitting: BOTH losses are high. The solutions are opposite — applying dropout to an underfitting model makes it worse!
>
>> 过拟合：训练损失低，验证损失高。欠拟合：两者都高。解决方案相反——对欠拟合模型应用Dropout会让它更差！
>>
>
> **📝 Exam:**
> **(1) 诊断题 (Diagnosis):**
> "Training accuracy is 98%, test accuracy is 55%. What's the problem and how to fix it?" → Overfitting. Apply dropout, L2 regularization, data augmentation, or early stopping.
>
>> "训练准确率98%，测试准确率55%。问题是什么，如何解决？" → 过拟合。应用dropout、L2正则化、数据增强或早停。
>>
>
> **(2) 概念题 (Concept):**
> "Explain how dropout prevents overfitting." → By randomly deactivating neurons during training, it forces the network to learn redundant representations, preventing any single neuron from becoming essential.
>
>> "解释Dropout如何防止过拟合。" → 通过在训练时随机停用神经元，迫使网络学习冗余表示，防止任何单个神经元变得不可或缺。
>>

---

## 11. 硬件资源及优化 (Hardware Resources & Optimization)

### 11.1 CPU vs GPU vs TPU

![Page 27](week5_deep_learning_slides_pages/page_027.png)

**Hardware resources slide:** Title "Hardware Resources for Deep Learning: CPUs vs GPUs vs TPUs" on dark green background. Text compares CPUs, GPUs, and TPUs for deep learning workloads. Right side: three icons/images representing CPU, GPU, and TPU hardware, arranged vertically for visual comparison.

**硬件资源页：** 深绿背景，标题"Hardware Resources for Deep Learning: CPUs vs GPUs vs TPUs"。文字比较CPU、GPU和TPU用于深度学习工作负载。右侧：三个图标/图像分别代表CPU、GPU和TPU硬件，垂直排列进行视觉比较。

- Deep learning, particularly CNNs, requires significant computational resources. — 深度学习，特别是CNN，需要大量计算资源。
- CPUs, with fewer cores, are versatile but slower for this task. — CPU核心较少，通用但在此任务中较慢。
- GPUs, with thousands of cores, are ideal for the parallel processing needs of deep learning. — GPU拥有数千个核心，非常适合深度学习的并行处理需求。
- TPUs, designed specifically for neural network operations, provide even faster computations. — TPU专为神经网络运算设计，提供更快的计算。
- Choice of hardware can significantly impact training time, cost, and scalability of deep learning models. — 硬件的选择会显著影响深度学习模型的训练时间、成本和可扩展性。

### 11.2 CNN资源优化 (Optimizing CNNs for Efficient Resource Use)

![Page 28](week5_deep_learning_slides_pages/page_028.png)

**Resource optimization slide:** Title "Optimizing CNNs for Efficient Resource Use" on dark green background. Text describes optimization techniques: pruning, quantization, and efficient architectures like MobileNets. Right side: diagram illustrating network pruning — a dense network being simplified by removing connections.

**资源优化页：** 深绿背景，标题"Optimizing CNNs for Efficient Resource Use"。文字描述优化技术：剪枝、量化和MobileNets等高效架构。右侧：网络剪枝示意图——通过移除连接简化密集网络。

- Efficient resource use in CNNs involves techniques like pruning (removing redundant neurons), quantization (reducing the precision of the numbers used), and using efficient architectures like MobileNets. — CNN的高效资源使用涉及剪枝（移除冗余神经元）、量化（降低使用数字的精度）和使用MobileNets等高效架构等技术。
- These optimizations are crucial for deploying models in resource-constrained environments like mobile devices, ensuring a balance between performance and resource use. — 这些优化对于在移动设备等资源受限环境中部署模型至关重要，确保性能和资源使用之间的平衡。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Hardware Hierarchy (硬件层级):**
>
> CPU: general-purpose, few powerful cores. GPU: thousands of simpler cores, ideal for matrix operations. TPU: Google's custom chip, specifically designed for tensor operations in neural networks.
>
>> CPU：通用型，少量强大核心。GPU：数千个简单核心，适合矩阵运算。TPU：谷歌的定制芯片，专为神经网络张量运算设计。
>>
>
> **(2) Optimization Techniques (优化技术):**
>
> Pruning: remove unimportant connections (make network sparser). Quantization: reduce precision (float32 → int8) for faster inference. Efficient architectures: MobileNet uses depthwise separable convolutions for mobile deployment.
>
>> 剪枝：移除不重要的连接（使网络更稀疏）。量化：降低精度（float32→int8）加快推理。高效架构：MobileNet使用深度可分离卷积用于移动部署。
>>
>
> **🎯 Why:**
> **(1) Cost and speed matter (成本和速度很重要):**
>
> Training a large model on CPU can take weeks; the same model on GPU takes hours. Hardware choice directly impacts feasibility and budget.
>
>> 在CPU上训练大模型可能需要数周；同样的模型在GPU上只需几小时。硬件选择直接影响可行性和预算。
>>
>
> **(2) Edge deployment requires optimization (边缘部署需要优化):**
>
> A 500MB ResNet can't run on a phone. Through pruning + quantization, you can reduce it to 5MB with minimal accuracy loss, enabling real-time inference on mobile.
>
>> 500MB的ResNet无法在手机上运行。通过剪枝+量化，可以在精度损失最小的情况下减少到5MB，实现移动端实时推理。
>>
>
> **💡 Intuition:**
> **(1) Factory workers analogy (工厂工人类比):**
>
> CPU = 4 PhD experts (can do anything, but only 4 at a time). GPU = 4000 assembly line workers (simple tasks, massively parallel). TPU = 4000 workers with custom tools built specifically for neural network math.
>
>> CPU = 4个博士专家（什么都能做，但同时只有4个）。GPU = 4000个流水线工人（简单任务，大规模并行）。TPU = 4000个拥有专为神经网络数学定制工具的工人。
>>
>
> **(2) Pruning as tree trimming (剪枝如修剪树木):**
>
> Just as a gardener trims dead branches without killing the tree, pruning removes unnecessary connections (near-zero weights) without significantly affecting accuracy.
>
>> 就像园丁修剪死枝而不会杀死树一样，剪枝移除不必要的连接（接近零的权重）而不会显著影响准确率。
>>
>
> **⚖️ Compare:**
> **(1) CPU vs GPU vs TPU (三种硬件对比):**
>
> | Hardware | Cores | Best For | Cost |
> |---|---|---|---|
> | CPU | 4-16 (complex) | General computing, small models | Low |
> | GPU | 1000s (simple) | Training & inference | Medium |
> | TPU | Custom tensor units | Large-scale training (Google Cloud) | High |
>
>> | 硬件 | 核心 | 最适合 | 成本 |
>> |---|---|---|---|
>> | CPU | 4-16（复杂） | 通用计算、小模型 | 低 |
>> | GPU | 数千（简单） | 训练和推理 | 中 |
>> | TPU | 定制张量单元 | 大规模训练（Google Cloud） | 高 |
>>
>
> **⚠️ Pitfall:**
> **(1) "Just use a bigger GPU" mentality ("就用更大GPU"的心态):**
>
> Hardware upgrades have diminishing returns. A poorly designed model won't become good just by using a faster GPU. Optimize the algorithm first, then scale hardware.
>
>> 硬件升级有递减效应。设计差的模型不会因为用更快的GPU就变好。先优化算法，再扩展硬件。
>>
>
> **(2) Over-pruning (过度剪枝):**
>
> Aggressive pruning (removing 90%+ of weights) can cause significant accuracy drops. Always validate accuracy after pruning.
>
>> 激进剪枝（移除90%+权重）可能导致显著准确率下降。剪枝后始终验证准确率。
>>
>
> **📝 Exam:**
> **(1) 对比题 (Comparison):**
> "Compare CPU, GPU, and TPU for deep learning." → CPU: few complex cores, general purpose. GPU: many simple cores, parallel. TPU: custom for tensor operations, fastest for DL.
>
>> "比较CPU、GPU和TPU用于深度学习。" → CPU：少量复杂核心，通用。GPU：大量简单核心，并行。TPU：张量运算定制，DL最快。
>>
>
> **(2) 应用题 (Application):**
> "Name two techniques to optimize CNN for mobile deployment." → Pruning (remove unimportant connections) and Quantization (reduce precision from float32 to int8).
>
>> "列两种为移动部署优化CNN的技术。" → 剪枝（移除不重要连接）和量化（从float32降低精度到int8）。
>>

---

## 12. CNN与其他深度学习技术集成 (Integrating CNNs with Other Techniques)

![Page 29](week5_deep_learning_slides_pages/page_029.png)

**Integration slide:** Title "Integrating CNNs with Other Deep Learning Techniques" on dark green background. Text describes combining CNNs with RNNs for video classification and NLP models for image captioning, enabling multimodal learning. Right side: visual showing interconnected CNN and RNN architectures processing different data modalities.

**集成页：** 深绿背景，标题"Integrating CNNs with Other Deep Learning Techniques"。文字描述将CNN与RNN结合用于视频分类以及与NLP模型结合用于图像描述，实现多模态学习。右侧：展示互连的CNN和RNN架构处理不同数据模态的可视化。

- Integrating CNNs with other deep learning techniques like Recurrent Neural Networks (RNNs) for video classification or Natural Language Processing (NLP) models for image captioning enhances their application scope. — 将CNN与循环神经网络（RNN）用于视频分类或自然语言处理（NLP）模型用于图像描述等其他深度学习技术集成，扩展了其应用范围。
- These integrations allow for multimodal learning, where CNNs process visual data while other models handle different data types like sequential data in videos or text in captions, leading to more comprehensive AI solutions. — 这些集成允许多模态学习，CNN处理视觉数据，而其他模型处理不同的数据类型（如视频中的序列数据或描述中的文本），从而产生更全面的AI解决方案。

> **📝 Notes:**
>
> **📌 What:**
> **(1) CNN + RNN for video (CNN + RNN用于视频):**
>
> CNN extracts spatial features from each frame, RNN (e.g., LSTM) captures temporal relationships between frames. Together they enable video classification and action recognition.
>
>> CNN从每帧提取空间特征，RNN（如LSTM）捕捉帧之间的时间关系。两者结合实现视频分类和动作识别。
>>
>
> **(2) CNN + NLP for captioning (CNN + NLP用于图像描述):**
>
> CNN acts as an "encoder" (image → feature vector), language model acts as a "decoder" (feature vector → natural language caption). This is the encoder-decoder paradigm.
>
>> CNN作为"编码器"（图像→特征向量），语言模型作为"解码器"（特征向量→自然语言描述）。这是编码器-解码器范式。
>>
>
> **🎯 Why:**
> **(1) Real-world data is multimodal (真实世界数据是多模态的):**
>
> Videos have both spatial and temporal information. Image captioning needs both visual understanding and language generation. No single architecture handles all modalities well.
>
>> 视频同时有空间和时间信息。图像描述需要视觉理解和语言生成。没有单一架构能很好地处理所有模态。
>>
>
> **(2) Transfer learning enables integration (迁移学习使集成成为可能):**
>
> Pre-trained CNNs (e.g., VGG, ResNet) can be used as feature extractors and combined with task-specific models, avoiding training from scratch.
>
>> 预训练的CNN（如VGG、ResNet）可用作特征提取器，与特定任务模型结合，避免从头训练。
>>
>
> **💡 Intuition:**
> **(1) Specialist team analogy (专家团队类比):**
>
> CNN = the "eyes" (processes what things look like). RNN = the "memory" (remembers what happened before). NLP model = the "voice" (describes what it sees). Together they form a complete perception system.
>
>> CNN = "眼睛"（处理事物看起来的样子）。RNN = "记忆"（记住之前发生了什么）。NLP模型 = "声音"（描述所见）。三者共同形成完整的感知系统。
>>
>
> **(2) Encoder-decoder as translation (编码器-解码器如翻译):**
>
> Image captioning is like "translating" a picture into words. The CNN "reads" the image into a universal representation, and the language model "writes" that representation as text.
>
>> 图像描述就像将图片"翻译"成文字。CNN将图像"读"成通用表示，语言模型将该表示"写"成文本。
>>
>
> **⚠️ Pitfall:**
> **(1) Not freezing CNN weights (不冻结CNN权重):**
>
> When combining pre-trained CNN with another model, always freeze the CNN weights initially. Otherwise, fine-tuning can destroy the learned features.
>
>> 将预训练CNN与其他模型组合时，始终先冻结CNN权重。否则微调可能破坏已学习的特征。
>>
>
> **(2) Ignoring modality mismatch (忽视模态不匹配):**
>
> CNN features and RNN/NLP model inputs must be dimensionally compatible. Mismatched feature dimensions is a common integration bug.
>
>> CNN特征和RNN/NLP模型输入必须维度兼容。特征维度不匹配是常见的集成错误。
>>
>
> **📝 Exam:**
> **(1) 应用题 (Application):**
> "How can CNNs be combined with RNNs for video classification?" → CNN extracts per-frame features, RNN processes the sequence of features to capture temporal patterns, final FC layer classifies the video.
>
>> "如何将CNN与RNN结合用于视频分类？" → CNN提取每帧特征，RNN处理特征序列以捕捉时间模式，最终FC层分类视频。
>>
>
> **(2) 概念题 (Concept):**
> "What is the encoder-decoder paradigm in image captioning?" → CNN encodes image to feature vector (encoder), language model generates caption from features (decoder).
>
>> "图像描述中的编码器-解码器范式是什么？" → CNN将图像编码为特征向量（编码器），语言模型从特征生成描述（解码器）。
>>

---

## 13. CNN训练故障排除 (Troubleshooting CNN Training)

### 13.1 常见问题与排除策略 (Common Issues & Strategies)

![Page 30](week5_deep_learning_slides_pages/page_030.png)

**Troubleshooting slide:** Title "Troubleshooting Common Issues in CNN Training" on dark green background. Two paragraphs listing common issues (overfitting, underfitting, convergence) and troubleshooting strategies (learning rate adjustment, architecture modification, batch normalization, dropout). Right side: diagnostic chart or visualization showing training metrics.

**故障排除页：** 深绿背景，标题"Troubleshooting Common Issues in CNN Training"。两段文字列出常见问题（过拟合、欠拟合、收敛问题）和排除策略（学习率调整、架构修改、批量归一化、dropout）。右侧：展示训练指标的诊断图表或可视化。

- Common issues in CNN training include overfitting, underfitting, and convergence problems. — CNN训练中的常见问题包括过拟合、欠拟合和收敛问题。
- Strategies to troubleshoot include adjusting learning rates, modifying network architectures, and using techniques like batch normalization and dropout. — 故障排除策略包括调整学习率、修改网络架构以及使用批量归一化和dropout等技术。
- Ensuring high-quality and diversified training data is also crucial, as is regular monitoring of performance metrics during training to identify and address issues early. — 确保高质量和多样化的训练数据也至关重要，同样重要的是在训练期间定期监控性能指标以及早发现和解决问题。

### 13.2 欠拟合解决方案 (Techniques to Address Underfitting)

![Page 31](week5_deep_learning_slides_pages/page_031.png)

**Underfitting slide:** Title "Techniques to Address Underfitting" on white background with green header. Text describes solutions: increasing model complexity, training longer, and using more powerful feature extraction methods. Also mentions revisiting data preprocessing and augmentation.

**欠拟合页：** 白色背景，绿色标题，标题"Techniques to Address Underfitting"。文字描述解决方案：增加模型复杂度、延长训练时间和使用更强大的特征提取方法。还提到重新审视数据预处理和增强技术。

- Underfitting, where a model fails to capture the underlying trend of the data, can be addressed by increasing the model complexity (adding more layers/neurons), training for longer durations, or using more powerful and diverse feature extraction methods. — 欠拟合，即模型未能捕捉数据的潜在趋势，可以通过增加模型复杂度（添加更多层/神经元）、延长训练时间或使用更强大和多样化的特征提取方法来解决。
- Another approach is to revisit data preprocessing and augmentation techniques to ensure the model receives sufficient and varied information during training. — 另一种方法是重新审视数据预处理和增强技术，以确保模型在训练期间获得充足和多样的信息。

> **📝 Notes:**
>
> **📌 What:**
> **(1) Common Training Issues (常见训练问题):**
>
> Overfitting (memorizes training data), Underfitting (can't learn patterns), Convergence problems (loss doesn't decrease or oscillates).
>
>> 过拟合（记忆训练数据）、欠拟合（无法学习模式）、收敛问题（损失不下降或振荡）。
>>
>
> **(2) Underfitting Solutions (欠拟合解决方案):**
>
> Increase model complexity (more layers/neurons), train for more epochs, use stronger feature extraction, improve data quality/augmentation.
>
>> 增加模型复杂度（更多层/神经元）、训练更多轮次、使用更强的特征提取、改善数据质量/增强。
>>
>
> **🎯 Why:**
> **(1) Diagnosis before treatment (先诊断再治疗):**
>
> Applying the wrong fix can make things worse. Dropout fixes overfitting but worsens underfitting. More training fixes underfitting but worsens overfitting. You MUST diagnose correctly first.
>
>> 应用错误的修复可能让事情更糟。Dropout修复过拟合但加剧欠拟合。更多训练修复欠拟合但加剧过拟合。必须先正确诊断。
>>
>
> **(2) Batch normalization as a universal stabilizer (批量归一化作为通用稳定器):**
>
> BatchNorm normalizes inputs to each layer, reducing internal covariate shift. It stabilizes training, allows higher learning rates, and acts as mild regularization.
>
>> BatchNorm对每层输入进行归一化，减少内部协变量偏移。它稳定训练，允许更高学习率，并充当轻度正则化。
>>
>
> **💡 Intuition:**
> **(1) Doctor’s diagnostic flowchart (医生诊断流程图):**
>
> Training loss high + val loss high = underfitting ("”patient is weak” → build strength). Training loss low + val loss high = overfitting ("”patient overdoing it” → rest more). Both low and close = healthy model.
>
>> 训练损失高+验证损失高 = 欠拟合（"患者虚弱" → 增强体质）。训练损失低+验证损失高 = 过拟合（"患者过度训练" → 多休息）。两者都低且接近 = 健康模型。
>>
>
> **(2) Learning rate as the most common fix (学习率是最常见的修复):**
>
> When loss oscillates wildly → reduce learning rate. When loss plateaus early → increase learning rate or use learning rate scheduler. This is often the first thing to try.
>
>> 当损失剧烈振荡 → 降低学习率。当损失过早停滞 → 提高学习率或使用学习率调度器。这通常是第一个要尝试的。
>>
>
> **⚖️ Compare:**
> **(1) Symptom-diagnosis table (症状-诊断表):**
>
> | Symptom | Diagnosis | Solution |
> |---|---|---|
> | Both losses high | Underfitting | More capacity, more training, better data |
> | Train low, val high | Overfitting | Dropout, regularization, augmentation |
> | Loss oscillates | LR too high | Reduce learning rate |
> | Loss plateaus | LR too low / stuck | Increase LR, use scheduler |
>
>> | 症状 | 诊断 | 解决方案 |
>> |---|---|---|
>> | 两个损失都高 | 欠拟合 | 更多容量、更多训练、更好数据 |
>> | 训练低，验证高 | 过拟合 | Dropout、正则化、增强 |
>> | 损失振荡 | 学习率太高 | 降低学习率 |
>> | 损失停滞 | 学习率太低/停滞 | 提高LR、用调度器 |
>>
>
> **⚠️ Pitfall:**
> **(1) Applying overfitting fixes to underfitting (对欠拟合应用过拟合修复):**
>
> Adding dropout to an underfitting model reduces its capacity further. Adding regularization to a model that can't even learn the training data is counterproductive. Always check both losses first.
>
>> 对欠拟合模型添加dropout进一步减少其容量。对甚至无法学习训练数据的模型添加正则化是适得其反的。始终先检查两个损失。
>>
>
> **(2) Ignoring data quality (忽视数据质量):**
>
> Many "model problems" are actually data problems: mislabeled examples, class imbalance, insufficient variety. Always inspect data before tuning the model.
>
>> 许多"模型问题"实际上是数据问题：标注错误、类别不平衡、多样性不足。调优模型前始终先检查数据。
>>
>
> **📝 Exam:**
> **(1) 诊断题 (Diagnosis):**
> "Both training and validation loss remain high after many epochs. Diagnose and suggest fixes." → Underfitting. Solutions: increase model complexity, train longer, improve data preprocessing, reduce regularization.
>
>> "多个epoch后训练和验证损失都保持高位。诊断并提出解决方案。" → 欠拟合。解决方案：增加模型复杂度、训练更久、改善数据预处理、减少正则化。
>>
>
> **(2) 策略题 (Strategy):**
> "What should you try first when CNN training loss oscillates wildly?" → Reduce learning rate. If that doesn't help, check for data issues (e.g., NaN values, mislabeled data).
>
>> "CNN训练损失剧烈振荡时应该先尝试什么？" → 降低学习率。如果没用，检查数据问题（如NaN值、标注错误）。
>>

---

## 14. 期中考试详情 (Midterm Test Details)

![Page 32](week5_deep_learning_slides_pages/page_032.png)

**Midterm test slide:** Title "CST8508_26W - Midterm Test" on white background. Bullet list with exam logistics: date (Feb 19), time (7:00pm – 8:00pm), total marks (25), duration (60 min), calculators allowed, no other electronic devices, contributes 15% of final grade. Test format listed as sub-bullets: Multiple Choice Questions, Fill in the blanks Questions, Short answer Questions, Mathematical Questions.

**期中考试页：** 白色背景，标题"CST8508_26W - Midterm Test"。要点列表包含考试信息：日期（2月19日）、时间（7:00pm – 8:00pm）、总分（25分）、时长（60分钟）、允许使用计算器、不允许其他电子设备、占最终成绩15%。考试格式以子要点列出：选择题、填空题、简答题、数学题。

**CST8508_26W - Midterm Test:**

- Paper based exam on Feb 19 – 7.00pm – 8.00 pm — 2月19日纸质考试——晚7:00–8:00
- Total Marks: 25 — 总分：25
- Duration: 60 min — 时长：60分钟
- Calculators allowed — 允许使用计算器
- No other personal electronic devices allowed in the classroom during test — 考试期间不允许在教室使用其他个人电子设备
- Contributes to 15% of final grade — 占最终成绩的15%
- Test Format: — 考试格式：
  - Multiple Choice Questions — 选择题
  - Fill in the blanks Questions — 填空题
  - Short answer Questions — 简答题
  - Mathematical Questions — 数学题

---
