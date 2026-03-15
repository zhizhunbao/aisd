# 深度学习 Deep Learning

> 名词总表 · 来源：Goodfellow《DLBook》· Bishop《PRML》· 原始论文 · PyTorch/TensorFlow 官方文档

---

### 神经网络基础 Neural Network Foundations

| 名词 | 英文 |
|------|------|
| 人工神经元 | Artificial Neuron |
| 感知机 | Perceptron |
| 多层感知机 | MLP (Multi-Layer Perceptron) |
| 前馈神经网络 | Feedforward Neural Network |
| 全连接层 / 稠密层 | Dense Layer / Fully Connected Layer |
| 权重 | Weights |
| 偏置 | Bias |
| 仿射变换 | Affine Transformation |
| 通用近似定理 | Universal Approximation Theorem |
| 深度 vs 宽度 | Depth vs Width |
| 隐藏层 | Hidden Layer |
| 输出层 | Output Layer |
| 特征表示 | Feature Representation |
| 表征学习 | Representation Learning |

---

### 激活函数 Activation Functions

| 名词 | 英文 |
|------|------|
| Sigmoid | Sigmoid |
| Tanh | Hyperbolic Tangent |
| ReLU | Rectified Linear Unit |
| Leaky ReLU | Leaky ReLU |
| PReLU | Parametric ReLU |
| ELU | Exponential Linear Unit |
| SELU | Scaled Exponential Linear Unit |
| GELU | Gaussian Error Linear Unit |
| Swish / SiLU | Swish / Sigmoid Linear Unit |
| Softmax | Softmax |
| 饱和激活 | Saturating Activation |
| 非饱和激活 | Non-Saturating Activation |
| 死神经元 | Dead Neurons (Dying ReLU) |

---

### 损失函数 Loss Functions

| 名词 | 英文 |
|------|------|
| 均方误差 | MSE (Mean Squared Error) |
| 交叉熵损失 | Cross-Entropy Loss |
| 二元交叉熵 | Binary Cross-Entropy (BCE) |
| 分类交叉熵 | Categorical Cross-Entropy |
| 负对数似然 | Negative Log-Likelihood (NLL) |
| 铰链损失 | Hinge Loss |
| Huber 损失 | Huber Loss |
| 对比损失 | Contrastive Loss |
| 三元组损失 | Triplet Loss |
| 焦点损失 | Focal Loss |
| KL 散度 | KL Divergence |
| 重构损失 | Reconstruction Loss |

---

### 优化器 Optimizers

| 名词 | 英文 |
|------|------|
| 梯度下降 | Gradient Descent (GD) |
| 随机梯度下降 | SGD (Stochastic Gradient Descent) |
| 小批量梯度下降 | Mini-Batch GD |
| 动量 | Momentum |
| Nesterov 动量 | Nesterov Accelerated Gradient |
| AdaGrad | Adaptive Gradient |
| RMSProp | Root Mean Square Propagation |
| Adam | Adaptive Moment Estimation |
| AdamW | Adam with Weight Decay |
| 学习率 | Learning Rate |
| 学习率调度 | Learning Rate Scheduling |
| 学习率预热 | Warmup |
| 余弦退火 | Cosine Annealing |
| 梯度裁剪 | Gradient Clipping |
| 权重衰减 | Weight Decay |

---

### 反向传播与训练 Backpropagation & Training

| 名词 | 英文 |
|------|------|
| 反向传播 | Backpropagation |
| 计算图 | Computational Graph |
| 链式法则 | Chain Rule |
| 自动微分 | Automatic Differentiation (Autograd) |
| 前向传播 | Forward Pass |
| 反向传播 | Backward Pass |
| 梯度消失 | Vanishing Gradient |
| 梯度爆炸 | Exploding Gradient |
| 训练轮次 | Epoch |
| 批次大小 | Batch Size |
| 迭代 | Iteration |
| 损失曲面 | Loss Surface |
| 鞍点 | Saddle Point |
| 局部最小值 | Local Minimum |

---

### 正则化技术 Regularization Techniques

| 名词 | 英文 |
|------|------|
| L1 / L2 正则化 | L1 / L2 Regularization |
| Dropout | Dropout |
| 批归一化 | Batch Normalization (BatchNorm) |
| 层归一化 | Layer Normalization (LayerNorm) |
| 组归一化 | Group Normalization |
| 实例归一化 | Instance Normalization |
| 权重初始化 | Weight Initialization |
| Xavier 初始化 | Xavier / Glorot Initialization |
| He 初始化 | He / Kaiming Initialization |
| 数据增强 | Data Augmentation |
| 早停 | Early Stopping |
| 标签平滑 | Label Smoothing |
| Mixup | Mixup |
| CutMix | CutMix |
| 随机深度 | Stochastic Depth |
| DropPath | DropPath |

---

### 张量与计算 Tensors & Computation

| 名词 | 英文 |
|------|------|
| 张量 | Tensor |
| 标量 | Scalar |
| 向量 | Vector |
| 矩阵 | Matrix |
| 张量形状 | Tensor Shape |
| 广播 | Broadcasting |
| 张量运算 | Tensor Operations |
| 设备 | Device (CPU / GPU / TPU) |
| 混合精度训练 | Mixed Precision Training |
| FP16 / BF16 | Half Precision / BFloat16 |

---

### 卷积神经网络 CNN

| 名词 | 英文 |
|------|------|
| 卷积层 | Convolutional Layer |
| 卷积核 / 滤波器 | Kernel / Filter |
| 步幅 | Stride |
| 填充 | Padding (Same / Valid) |
| 特征图 | Feature Map |
| 感受野 | Receptive Field |
| 通道 | Channel |
| 深度可分离卷积 | Depthwise Separable Convolution |
| 空洞卷积 | Dilated / Atrous Convolution |
| 转置卷积 | Transposed Convolution |
| 1×1 卷积 | 1×1 Convolution (Pointwise) |
| 最大池化 | Max Pooling |
| 平均池化 | Average Pooling |
| 全局平均池化 | Global Average Pooling (GAP) |
| 自适应池化 | Adaptive Pooling |
| 参数共享 | Parameter Sharing |
| 平移不变性 | Translation Invariance |
| 平移等变性 | Translation Equivariance |

---

### 经典 CNN 架构 Classic CNN Architectures

| 名词 | 英文 |
|------|------|
| LeNet | LeNet-5 |
| AlexNet | AlexNet |
| VGGNet | VGG-16 / VGG-19 |
| GoogLeNet / Inception | GoogLeNet / Inception |
| ResNet | Residual Network |
| 残差连接 | Skip / Residual Connection |
| 瓶颈块 | Bottleneck Block |
| DenseNet | Densely Connected Network |
| MobileNet | MobileNet |
| EfficientNet | EfficientNet |
| 复合缩放 | Compound Scaling |
| 网络架构搜索 | NAS (Neural Architecture Search) |

---

### 循环神经网络 RNN

| 名词 | 英文 |
|------|------|
| 循环神经网络 | RNN (Recurrent Neural Network) |
| 隐藏状态 | Hidden State |
| 时间步 | Time Step |
| 序列建模 | Sequence Modeling |
| BPTT | Backpropagation Through Time |
| 长短期记忆 | LSTM (Long Short-Term Memory) |
| 遗忘门 | Forget Gate |
| 输入门 | Input Gate |
| 输出门 | Output Gate |
| 细胞状态 | Cell State |
| 门控循环单元 | GRU (Gated Recurrent Unit) |
| 双向 RNN | Bidirectional RNN |
| 序列到序列 | Seq2Seq (Sequence-to-Sequence) |
| 编码器-解码器 | Encoder-Decoder |
| 教师强制 | Teacher Forcing |

---

### 注意力与 Transformer Attention & Transformer

| 名词 | 英文 |
|------|------|
| 注意力机制 | Attention Mechanism |
| 自注意力 | Self-Attention |
| 缩放点积注意力 | Scaled Dot-Product Attention |
| 多头注意力 | Multi-Head Attention (MHA) |
| Query / Key / Value | Query / Key / Value |
| 注意力分数 | Attention Score |
| 注意力权重 | Attention Weights |
| 因果掩码 | Causal Mask |
| 填充掩码 | Padding Mask |
| Transformer | Transformer |
| 位置编码 | Positional Encoding |
| 正弦位置编码 | Sinusoidal Positional Encoding |
| 旋转位置编码 | RoPE (Rotary Position Embedding) |
| 可学习位置嵌入 | Learned Positional Embedding |
| 前馈网络 | FFN (Feed-Forward Network) |
| 残差连接 | Residual Connection |
| 层归一化 | Layer Normalization |
| Pre-Norm vs Post-Norm | Pre-Norm vs Post-Norm |
| 编码器 | Encoder |
| 解码器 | Decoder |
| 交叉注意力 | Cross-Attention |
| KV 缓存 | KV Cache |
| 闪存注意力 | Flash Attention |
| 稀疏注意力 | Sparse Attention |
| 线性注意力 | Linear Attention |
| 滑动窗口注意力 | Sliding Window Attention |

---

### 生成模型 Generative Models

| 名词 | 英文 |
|------|------|
| 自编码器 | Autoencoder (AE) |
| 变分自编码器 | VAE (Variational Autoencoder) |
| 隐空间 | Latent Space |
| 重参数化技巧 | Reparameterization Trick |
| 生成对抗网络 | GAN (Generative Adversarial Network) |
| 生成器 | Generator |
| 判别器 | Discriminator |
| 模式崩溃 | Mode Collapse |
| Wasserstein GAN | WGAN |
| 扩散模型 | Diffusion Model |
| 去噪过程 | Denoising Process |
| 正向扩散 | Forward Diffusion |
| 反向扩散 | Reverse Diffusion |
| 噪声调度 | Noise Schedule |
| 流模型 | Flow-Based Model |
| 可逆网络 | Invertible Network |

---

### 目标检测与分割 Detection & Segmentation

| 名词 | 英文 |
|------|------|
| 锚框 | Anchor Box |
| IoU | Intersection over Union |
| 非极大值抑制 | NMS (Non-Maximum Suppression) |
| 区域提议网络 | RPN (Region Proposal Network) |
| R-CNN 系列 | R-CNN / Fast R-CNN / Faster R-CNN |
| YOLO | You Only Look Once |
| SSD | Single Shot MultiBox Detector |
| 特征金字塔 | FPN (Feature Pyramid Network) |
| 语义分割 | Semantic Segmentation |
| 实例分割 | Instance Segmentation |
| 全景分割 | Panoptic Segmentation |
| U-Net | U-Net |
| Mask R-CNN | Mask R-CNN |

---

### 大语言模型 Large Language Models

| 名词 | 英文 |
|------|------|
| 语言模型 | Language Model (LM) |
| 自回归模型 | Autoregressive Model |
| 掩码语言模型 | Masked Language Model (MLM) |
| GPT | Generative Pre-trained Transformer |
| BERT | Bidirectional Encoder Representations |
| T5 | Text-to-Text Transfer Transformer |
| 预训练 | Pre-Training |
| 微调 | Fine-Tuning |
| 提示工程 | Prompt Engineering |
| 上下文学习 | In-Context Learning (ICL) |
| 思维链 | Chain-of-Thought (CoT) |
| 指令微调 | Instruction Tuning |
| RLHF | Reinforcement Learning from Human Feedback |
| LoRA | Low-Rank Adaptation |
| QLoRA | Quantized LoRA |
| 适配器 | Adapter |
| 分词器 | Tokenizer |
| BPE | Byte Pair Encoding |
| WordPiece | WordPiece |
| SentencePiece | SentencePiece |
| 嵌入层 | Embedding Layer |
| 温度 | Temperature |
| Top-k 采样 | Top-k Sampling |
| Top-p / 核采样 | Top-p / Nucleus Sampling |
| 束搜索 | Beam Search |
| 贪心解码 | Greedy Decoding |
| 困惑度 | Perplexity |
| 上下文窗口 | Context Window |
| 涌现能力 | Emergent Abilities |

---

### 迁移学习 Transfer Learning

| 名词 | 英文 |
|------|------|
| 预训练模型 | Pretrained Model |
| 微调 | Fine-Tuning |
| 特征提取 | Feature Extraction |
| 冻结层 | Freezing Layers |
| 领域适应 | Domain Adaptation |
| 知识蒸馏 | Knowledge Distillation |
| 教师模型 | Teacher Model |
| 学生模型 | Student Model |

---

### 模型压缩与部署 Model Compression & Deployment

| 名词 | 英文 |
|------|------|
| 量化 | Quantization |
| INT8 量化 | INT8 Quantization |
| 训练后量化 | PTQ (Post-Training Quantization) |
| 量化感知训练 | QAT (Quantization-Aware Training) |
| 剪枝 | Pruning |
| 结构化剪枝 | Structured Pruning |
| 非结构化剪枝 | Unstructured Pruning |
| 知识蒸馏 | Knowledge Distillation |
| ONNX | Open Neural Network Exchange |
| TensorRT | TensorRT |
| 推理优化 | Inference Optimization |
| 模型并行 | Model Parallelism |
| 数据并行 | Data Parallelism |
| 张量并行 | Tensor Parallelism |
| 流水线并行 | Pipeline Parallelism |

---

### 自监督与对比学习 Self-Supervised & Contrastive Learning

| 名词 | 英文 |
|------|------|
| 自监督学习 | Self-Supervised Learning (SSL) |
| 对比学习 | Contrastive Learning |
| SimCLR | Simple Contrastive Learning |
| MoCo | Momentum Contrast |
| BYOL | Bootstrap Your Own Latent |
| 正样本对 | Positive Pair |
| 负样本对 | Negative Pair |
| 投影头 | Projection Head |
| 信息噪声对比估计 | InfoNCE Loss |

---

### 图神经网络 Graph Neural Networks

| 名词 | 英文 |
|------|------|
| 图卷积网络 | GCN (Graph Convolutional Network) |
| 消息传递 | Message Passing |
| 节点嵌入 | Node Embedding |
| 图注意力网络 | GAT (Graph Attention Network) |
| 邻接矩阵 | Adjacency Matrix |
| 度矩阵 | Degree Matrix |
| 图池化 | Graph Pooling |
| 谱方法 | Spectral Methods |

---

### 深度学习框架 Deep Learning Frameworks

| 名词 | 英文 |
|------|------|
| PyTorch | PyTorch |
| TensorFlow | TensorFlow |
| Keras | Keras |
| nn.Module | nn.Module |
| 动态计算图 | Dynamic Computational Graph (Eager) |
| 静态计算图 | Static Computational Graph |
| DataLoader | DataLoader |
| Dataset | Dataset |
| 模型检查点 | Model Checkpoint |
| TensorBoard | TensorBoard |
| 分布式训练 | Distributed Training |
| DDP | DistributedDataParallel |
| FSDP | Fully Sharded Data Parallel |
| DeepSpeed | DeepSpeed |
| Hugging Face Transformers | Hugging Face Transformers |
