# Deep Learning Knowledge Map

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| [vanishing_gradient](vanishing_gradient/) | 8 | ✅ current | 梯度消失问题：根因分析、LSTM/GRU 解决方案、Transformer 替代方案 |
| [pytorch](pytorch/) | 8 | ✅ current | PyTorch 深度学习框架：张量计算、自动微分、训练循环、踩坑记录 |
| [cnn](cnn/) | 8 | ✅ current | 卷积神经网络：卷积/池化原理、数学推导、PyTorch 实现、LeNet→ResNet 演进 |
| [tensor](tensor/) | 8 | ✅ current | 张量：多维数组核心概念、内存模型(stride/view)、数学基础、PyTorch Tensor API、NumPy 互操作 |
| [mlp](mlp/) | 9 | ✅ current | 多层感知机：前向/反向传播、激活函数、万能近似定理、PyTorch/sklearn/NumPy 实现、从感知机到深度学习的历史演进 |
| [conv_layer](conv_layer/) | 9 | ✅ current | 卷积层：输出尺寸/参数量公式、标准/深度可分离/空洞/转置卷积变体、4种CNN架构代码、从Hubel-Wiesel到ConvNeXt的演进 |
| [tensorflow](tensorflow/) | 9 | ✅ current | TensorFlow/Keras：GradientTape 自动微分、Eager/Graph 模式、Pipeline→部署全链路、TPU/分布式训练 |
| [keras](keras/) | 8 | ✅ current | Keras 3：多后端(JAX/TF/PyTorch)深度学习 API、Sequential/Functional/Subclassing 三种建模方式、compile→fit→evaluate 训练流程、设计哲学第一性原理 |
| [transformer](transformer/) | 9 | ✅ current | Transformer：Self-Attention/Multi-Head Attention 数学推导、Encoder-Decoder 架构、从零实现+PyTorch API、从RNN→Attention→Transformer→BERT/GPT/LLM 完整演进、第一性原理（分布假说/全局可及性/可微分加权/位置可加性） |
| [dense_layer](dense_layer/) | 9 | ✅ current | Dense Layer (全连接层)：y=σ(Wx+b) 前向/反向传播数学推导、Xavier/He 初始化、PyTorch nn.Linear + Keras Dense 双平台 API、在 MLP/CNN/Transformer 中的角色演变、万能近似定理第一性原理 |
| [max_pool_layer](max_pool_layer/) | 9 | ✅ current | Max Pool Layer (最大池化层)：输出尺寸/梯度传播公式、Max vs Average vs Strided Conv 对比、PyTorch/Keras 双平台 API、从 LeNet subsampling 到 Transformer 替代池化的演进、平移不变性+稀疏激活第一性原理 |
| [avg_pool_layer](avg_pool_layer/) | 9 | ✅ current | Avg Pool Layer (平均池化层)：局部/全局(GAP)平均池化公式、梯度均匀分配推导、GAP替代FC层的NiN设计、Inception/SE-Net/BERT中的多元角色、局部平稳性+通道语义对应第一性原理 |
| [activation_functions](activation_functions/) | 9 | ✅ current | Activation Functions (激活函数)：Sigmoid/Tanh/ReLU/Softmax/GELU 完整公式推导+梯度计算、scikit-learn MLPClassifier + Keras Dense 双平台对比、从阶跃函数到GELU的80年演进、非线性必要性的第一性原理(UAT) |
| [optimizers](optimizers/) | 9 | ✅ current | Optimizers (优化器)：SGD/Momentum/AdaGrad/RMSprop/Adam/L-BFGS 完整更新公式推导+Adam偏差修正、sklearn solver + Keras optimizer 双平台对比、从1847年梯度下降到2019年AdamW的演进、可微性+最快下降+无偏估计第一性原理 |
| [loss_functions](loss_functions/) | 9 | ✅ current | Loss Functions (损失函数)：MSE/MAE/BCE/CCE/Huber 完整公式推导+BCE消除Sigmoid饱和证明、MLE→交叉熵推导、任务-激活-损失配对表、从1809年最小二乘到2017年Focal Loss的演进、MLE+联合设计第一性原理 |
| [neural_network](neural_network/) | 9 | ✅ current | Neural Network (神经网络)：前向传播/反向传播完整推导、单层UAT→深层指数效率、NumPy从零/PyTorch/Keras三平台实现、从McCulloch-Pitts(1943)到AlexNet(2012)的80年演进、可微可组合性+流形假设+ERM第一性原理 |
| [forward_propagation](forward_propagation/) | 9 | ✅ current | Forward Propagation (前向传播)：逐层仿射+激活的数学推导、手算练习、PyTorch nn.Module/Sequential 实现、Shape Mismatch/eval模式等5大踩坑、McCulloch-Pitts→ResNet历史演进、线性叠加+非线性+UAT第一性原理 |
