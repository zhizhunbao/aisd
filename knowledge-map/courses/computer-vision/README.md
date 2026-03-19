# Computer Vision Knowledge Map

> 来源课程：Stanford CS231N (Fei-Fei Li) · CMU 16-720 (Deva Ramanan) · Szeliski 教材
> 级别：研究生 Master · 角色：ML 工程师
> 前置课程：`deep-learning` (研究生级) · `machine-vision` (本科/工业级)

## 课程定位

Computer Vision 是研究生级别的独立课程，与 Machine Vision 和 Deep Learning 的关系：

| 维度 | Machine Vision (本科/工业) | Computer Vision (研究生) | Advanced Deep Learning (博士) |
|------|--------------------------|-------------------------|------------------------------|
| 重点 | 图像处理 + OpenCV + 工业检测 | 几何视觉 + 深度学习视觉 + 3D理解 | 概率模型 + 生成模型 + 理论 |
| 数学深度 | 卷积/频域变换 | 射影几何 + 多视图几何 + 优化 | 变分推断 + 蒙特卡洛 + 信息论 |
| 代表技术 | OpenCV / 滤波 / 形态学 | SfM / NeRF / YOLO / ViT / CLIP | VAE / GAN / EBM / NTK |
| 赛道 | 工业自动化 | 自动驾驶 / AR/VR / 机器人 | 学术研究 / 理论突破 |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| image_formation | 0 | 🔲 planned | 图像形成：针孔模型、内外参、畸变、光度学、BRDF |
| image_filtering | 0 | 🔲 planned | 图像滤波与特征：高斯金字塔、SIFT、ORB、HOG |
| geometric_transforms | 0 | 🔲 planned | 几何变换：仿射/透视变换、单应性、RANSAC、图像拼接 |
| epipolar_geometry | 0 | 🔲 planned | 对极几何：基础矩阵、本质矩阵、八点法、立体匹配 |
| motion_analysis | 0 | 🔲 planned | 运动分析：光流(Lucas-Kanade/Horn-Schunck)、视频跟踪 |
| 3d_reconstruction | 0 | 🔲 planned | 三维重建：SfM、MVS、Bundle Adjustment、NeRF、3DGS |
| image_classification | 0 | 🔲 planned | 图像分类：BoVW、CNN、迁移学习、数据增强 |
| imagenet | 11 | ✅ done | ImageNet数据集：ILSVRC竞赛、预训练范式、Top-k评估、架构演进驱动 |
| cnn_architectures | 0 | 🔲 planned | CNN 架构演进：LeNet→AlexNet→ResNet→ViT→ConvNeXt |
| object_detection | 11 | ✅ done | 目标检测：R-CNN系列、YOLO、FPN、DETR |
| image_segmentation | 0 | 🔲 planned | 图像分割：FCN、U-Net、DeepLab、Mask R-CNN、SAM |
| vision_transformer | 0 | 🔲 planned | 视觉Transformer：ViT、DeiT、Swin、Patch Embedding |
| generative_vision | 0 | 🔲 planned | 生成视觉：GAN、StyleGAN、Diffusion、超分辨率、风格迁移 |
| vision_language | 0 | 🔲 planned | 视觉语言模型：CLIP、VQA、Image Captioning、多模态 |
| self_supervised_vision | 0 | 🔲 planned | 自监督视觉：SimCLR、MoCo、MAE、DINO |

## 与相关课程的主题映射

```
machine-vision (本科/工业)     computer-vision (研究生)
──────────────────────────     ───────────────────────────
图像基础                  ──→   image_formation (+ 相机模型)
空间滤波 / 频域滤波       ──→   image_filtering (+ SIFT/ORB)
边缘检测 / 特征提取       ──→   geometric_transforms
几何变换                  ──→   epipolar_geometry (新增)
相机模型与标定            ──→   motion_analysis (新增)
目标检测与识别            ──→   3d_reconstruction (新增)
                               image_classification
                               cnn_architectures
deep-learning (研究生)         object_detection
──────────────────────────     image_segmentation
cnn                       ──→   vision_transformer (新增)
conv_layer / pool_layer   ──→   generative_vision
transformer               ──→   vision_language (新增)
                               self_supervised_vision (新增)
```
