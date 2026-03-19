# 计算机视觉 Computer Vision

> 名词总表 · 来源：Szeliski《Computer Vision: Algorithms and Applications》· Hartley & Zisserman《Multiple View Geometry》· Stanford CS231N · CMU 16-720
>
> 级别：研究生 Master · 角色：ML 工程师

---

### 图像形成与表示 Image Formation & Representation

| 名词 | 英文 |
|------|------|
| 针孔相机模型 | Pinhole Camera Model |
| 薄透镜模型 | Thin Lens Model |
| 内参矩阵 | Intrinsic Matrix (K) |
| 外参矩阵 | Extrinsic Matrix [R|t] |
| 齐次坐标 | Homogeneous Coordinates |
| 投影矩阵 | Projection Matrix |
| 径向畸变 | Radial Distortion |
| 切向畸变 | Tangential Distortion |
| 相机标定 | Camera Calibration |
| 视场角 | Field of View (FoV) |
| 光度学 | Radiometry |
| BRDF | Bidirectional Reflectance Distribution Function |
| 光度立体 | Photometric Stereo |

---

### 图像滤波与特征 Image Filtering & Features

| 名词 | 英文 |
|------|------|
| 线性滤波 | Linear Filtering |
| 高斯滤波 | Gaussian Filter |
| 高斯金字塔 | Gaussian Pyramid |
| 拉普拉斯金字塔 | Laplacian Pyramid |
| 图像梯度 | Image Gradient |
| 边缘检测 | Edge Detection |
| Canny 检测器 | Canny Edge Detector |
| Harris 角点 | Harris Corner Detector |
| 尺度空间 | Scale Space |
| DoG 检测器 | Difference of Gaussians (DoG) |
| SIFT | Scale-Invariant Feature Transform |
| SURF | Speeded Up Robust Features |
| ORB | Oriented FAST and Rotated BRIEF |
| HOG | Histogram of Oriented Gradients |
| 特征描述子 | Feature Descriptor |
| 特征匹配 | Feature Matching |

---

### 几何变换与配准 Geometric Transformations & Alignment

| 名词 | 英文 |
|------|------|
| 仿射变换 | Affine Transformation |
| 透视变换 | Projective Transformation (Homography) |
| 单应性矩阵 | Homography Matrix |
| RANSAC | Random Sample Consensus |
| 最小二乘拟合 | Least Squares Fitting |
| 图像配准 | Image Registration |
| 图像拼接 | Image Stitching / Mosaicing |
| 图像变形 | Image Warping |
| 前向映射 / 后向映射 | Forward / Inverse Warping |
| 插值方法 | Interpolation (Bilinear / Bicubic) |

---

### 对极几何与立体视觉 Epipolar Geometry & Stereo Vision

| 名词 | 英文 |
|------|------|
| 对极几何 | Epipolar Geometry |
| 极点 | Epipole |
| 极线 | Epipolar Line |
| 基础矩阵 | Fundamental Matrix (F) |
| 本质矩阵 | Essential Matrix (E) |
| 八点法 | Eight-Point Algorithm |
| 立体匹配 | Stereo Matching |
| 视差图 | Disparity Map |
| 深度图 | Depth Map |
| 立体校正 | Stereo Rectification |
| 基线 | Baseline |
| 半全局匹配 | Semi-Global Matching (SGM) |

---

### 运动分析 Motion Analysis

| 名词 | 英文 |
|------|------|
| 光流 | Optical Flow |
| Lucas-Kanade 方法 | Lucas-Kanade Method |
| Horn-Schunck 方法 | Horn-Schunck Method |
| 亮度恒常假设 | Brightness Constancy Assumption |
| 孔径问题 | Aperture Problem |
| 稠密光流 | Dense Optical Flow |
| 稀疏光流 | Sparse Optical Flow |
| 运动场 | Motion Field |
| 自运动和场景 | Ego-Motion |
| 视频跟踪 | Visual Tracking |
| KLT 跟踪器 | KLT Tracker |
| 目标跟踪 | Object Tracking |

---

### 多视图几何与三维重建 Multi-View Geometry & 3D Reconstruction

| 名词 | 英文 |
|------|------|
| 运动恢复结构 | SfM (Structure from Motion) |
| 多视图立体 | MVS (Multi-View Stereo) |
| 三角化 | Triangulation |
| 捆绑调整 | Bundle Adjustment |
| 点云 | Point Cloud |
| 密集重建 | Dense Reconstruction |
| 稀疏重建 | Sparse Reconstruction |
| SLAM | Simultaneous Localization and Mapping |
| 视觉里程计 | Visual Odometry |
| 深度估计 | Depth Estimation |
| 神经辐射场 | NeRF (Neural Radiance Field) |
| 3D 高斯飞溅 | 3D Gaussian Splatting |

---

### 图像识别与分类 Image Recognition & Classification

| 名词 | 英文 |
|------|------|
| 图像分类 | Image Classification |
| 线性分类器 | Linear Classifier |
| K 近邻 | k-Nearest Neighbors (kNN) |
| 支持向量机 | SVM (Support Vector Machine) |
| 视觉词袋 | BoVW (Bag of Visual Words) |
| 卷积神经网络 | CNN (Convolutional Neural Network) |
| 迁移学习 | Transfer Learning |
| 数据增强 | Data Augmentation |
| ImageNet | ImageNet |
| Top-1 / Top-5 准确率 | Top-1 / Top-5 Accuracy |
| 混淆矩阵 | Confusion Matrix |

---

### CNN 架构演进 CNN Architecture Evolution

| 名词 | 英文 |
|------|------|
| LeNet | LeNet-5 |
| AlexNet | AlexNet |
| VGGNet | VGG-16 / VGG-19 |
| GoogLeNet / Inception | GoogLeNet / Inception |
| ResNet | Residual Network |
| 残差连接 | Skip / Residual Connection |
| DenseNet | Densely Connected Network |
| MobileNet | MobileNet |
| EfficientNet | EfficientNet |
| Vision Transformer | ViT (Vision Transformer) |
| Swin Transformer | Swin Transformer |
| ConvNeXt | ConvNeXt |

---

### 目标检测 Object Detection

| 名词 | 英文 |
|------|------|
| 骨干网络 | Backbone |
| 颈部网络 | Neck |
| 检测头 | Head (Detection Head) |
| 模型检查点 | Checkpoint |
| 锚框 | Anchor Box |
| IoU | Intersection over Union |
| 非极大值抑制 | NMS (Non-Maximum Suppression) |
| 区域提议网络 | RPN (Region Proposal Network) |
| R-CNN | Regions with CNN Features |
| Fast R-CNN | Fast R-CNN |
| Faster R-CNN | Faster R-CNN |
| YOLO | You Only Look Once |
| SSD | Single Shot MultiBox Detector |
| 特征金字塔 | FPN (Feature Pyramid Network) |
| DETR | Detection Transformer |
| mAP | Mean Average Precision |
| 先验框 | Prior / Default Box |

---

### 图像分割 Image Segmentation

| 名词 | 英文 |
|------|------|
| 语义分割 | Semantic Segmentation |
| 实例分割 | Instance Segmentation |
| 全景分割 | Panoptic Segmentation |
| FCN | Fully Convolutional Network |
| U-Net | U-Net |
| DeepLab | DeepLab (Atrous Convolution) |
| 空洞空间金字塔池化 | ASPP (Atrous Spatial Pyramid Pooling) |
| Mask R-CNN | Mask R-CNN |
| 条件随机场 | CRF (Conditional Random Field) |
| SAM | Segment Anything Model |
| 像素级分类 | Pixel-wise Classification |
| 上采样 / 反卷积 | Upsampling / Transposed Convolution |

---

### 注意力与视觉 Transformer Attention & Vision Transformer

| 名词 | 英文 |
|------|------|
| 自注意力 | Self-Attention |
| 多头注意力 | Multi-Head Attention |
| 位置编码 | Positional Encoding |
| Patch 嵌入 | Patch Embedding |
| 类别令牌 | [CLS] Token |
| ViT | Vision Transformer |
| DeiT | Data-efficient Image Transformer |
| Swin Transformer | Shifted Window Transformer |
| 窗口注意力 | Window Attention |
| 交叉注意力 | Cross-Attention |
| 多尺度特征 | Multi-Scale Features |

---

### 生成模型与视觉 Generative Models for Vision

| 名词 | 英文 |
|------|------|
| 图像生成 | Image Generation |
| GAN | Generative Adversarial Network |
| StyleGAN | StyleGAN |
| 条件 GAN | Conditional GAN (cGAN / pix2pix) |
| 图像翻译 | Image-to-Image Translation |
| 扩散模型 | Diffusion Model |
| Stable Diffusion | Stable Diffusion |
| 超分辨率 | Super-Resolution |
| 图像修复 | Image Inpainting |
| 风格迁移 | Style Transfer |
| 神经风格迁移 | Neural Style Transfer |

---

### 视觉语言模型 Vision-Language Models

| 名词 | 英文 |
|------|------|
| 图像描述 | Image Captioning |
| 视觉问答 | VQA (Visual Question Answering) |
| CLIP | Contrastive Language-Image Pre-training |
| 对比学习 | Contrastive Learning |
| 视觉基础模型 | Vision Foundation Model |
| 多模态学习 | Multimodal Learning |
| 零样本识别 | Zero-Shot Recognition |
| 开放词汇检测 | Open-Vocabulary Detection |
| 视觉提示 | Visual Prompting |

---

### 自监督视觉学习 Self-Supervised Visual Learning

| 名词 | 英文 |
|------|------|
| 自监督学习 | Self-Supervised Learning (SSL) |
| SimCLR | Simple Contrastive Learning |
| MoCo | Momentum Contrast |
| BYOL | Bootstrap Your Own Latent |
| MAE | Masked Autoencoder |
| DINO | Self-Distillation with No Labels |
| 预训练 | Pre-Training |
| 线性探测 | Linear Probing |
| 正样本对 / 负样本对 | Positive / Negative Pair |
| 投影头 | Projection Head |
