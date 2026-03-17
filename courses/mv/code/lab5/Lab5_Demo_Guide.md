# CST8508 Lab 5 Demo 代码逐行讲解（第一性原理版）

> **Accuracy:** 88.42% · **参数量:** ~8.5M · **不是 Transfer Learning，是从零训练**

## 参考文献索引

| 标记 | 来源 |
|------|------|
| [VGG] | Simonyan & Zisserman, "Very Deep Convolutional Networks", ICLR 2015, §2.1 |
| [Dropout] | Srivastava et al., "Dropout: A Simple Way to Prevent Overfitting", JMLR 2014, §4 & Table 5 |
| [Adam] | Kingma & Ba, "Adam: A Method for Stochastic Optimization", ICLR 2015, §2 Algorithm 1 |
| [ReLU] | Nair & Hinton, "Rectified Linear Units Improve RBMs", ICML 2010, §3 |
| [ImageNet] | Deng et al., "ImageNet: A Large-Scale Hierarchical Image Database", CVPR 2009 |
| [IN-norm] | PyTorch 官方文档: torchvision.models — 所有预训练模型统一使用 mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225] |
| [CrossEntropy] | Goodfellow, Bengio & Courville, "Deep Learning" (MIT Press 2016), §6.2.2 |
| [KL] | Shannon, "A Mathematical Theory of Communication", Bell System Tech. J. 1948 |
| [Backprop] | Rumelhart, Hinton & Williams, "Learning representations by back-propagating errors", Nature 1986 |
| [MaxPool] | Scherer, Müller & Behnke, "Evaluation of Pooling Operations in CNNs", ICANN 2010, §3 |
| [MiniBatch] | Goodfellow et al., "Deep Learning" (MIT Press 2016), §8.1.3 |
| [DataAug] | Shorten & Khoshgoftaar, "A survey on Image Data Augmentation for DL", J Big Data 2019, §3 |
| [ImageFolder] | PyTorch 官方文档: torchvision.datasets.ImageFolder |
| [PyTorch-train/eval] | PyTorch 官方文档: torch.nn.Module.train() / eval() |
| [CLT] | Casella & Berger, "Statistical Inference" (2nd ed.), §5.5 Central Limit Theorem |

---

## Cell 0: 数据集下载与清理

```python
# ── 导入 ──
# os:              操作系统接口，文件路径操作
# zipfile:         解压 .zip 压缩包（数据集以压缩包分发）
# urllib.request:  HTTP 下载（标准库，无需 pip install）
# pathlib.Path:    面向对象路径操作（比 os.path 更简洁）
# PIL.Image:       Pillow 图像库，verify() 检测 JPEG 文件是否损坏
# Why 全用标准库(除 PIL)？→ 最小依赖原则——环境越干净越不容易装错
#   🪨 不可再分：可移植性 = 代码在任何机器上都能跑
#   📖 Source: Python 标准库文档 (https://docs.python.org/3/library/)
import os
import zipfile
import urllib.request
from pathlib import Path
from PIL import Image

# ── 数据集 URL 和路径 ──
# 做什么：定义数据集下载地址、本地 ZIP 路径、解压后的文件夹路径
# 数据集：微软 Cats vs Dogs，12500 猫 + 12500 狗，~786MB
# Why 用这个数据集？→ 二分类经典数据集，图片量大(25K)，适合练 CNN
#   Why 需要这么多图？→ CNN 有 850 万参数，数据少会过拟合（死记硬背）
#   Why 过拟合是坏事？→ 只会背答案不会举一反三 → 新图片全猜错
#   🪨 不可再分：模型泛化能力 = 机器学习的终极目标
#   📖 Source: Goodfellow et al. (2016), "Deep Learning", MIT Press, §5.2 — Capacity, Overfitting and Underfitting
DATASET_URL  = "https://download.microsoft.com/download/.../kagglecatsanddogs_5340.zip"
ZIP_PATH     = Path("kagglecatsanddogs_5340.zip")
DATASET_PATH = Path("PetImages")

# ── 下载数据集 ──
# 做什么：如果本地没有 ZIP 也没有解压后的文件夹，就从微软服务器下载
# Why 先检查再下载？→ 786MB 很大，重复下载浪费时间
# Why 检查两个条件？→ ZIP 可能已删但已解压过 → 也不需要重新下载
if not ZIP_PATH.exists() and not DATASET_PATH.exists():
    print("Downloading dataset (~786 MB) ...")
    urllib.request.urlretrieve(DATASET_URL, ZIP_PATH)
    print("Download complete.")
else:
    print("Zip / dataset already present, skipping download.")

# ── 解压数据集 ──
# 做什么：将 ZIP 解压到当前目录，生成 PetImages/Cat/ 和 PetImages/Dog/ 文件夹
# 文件夹结构：PetImages/Cat/*.jpg + PetImages/Dog/*.jpg
# Why 这个结构？→ PyTorch ImageFolder 自动把文件夹名当类别标签(Cat=0, Dog=1) [ImageFolder]
#   Why 不用 CSV 列表？→ ImageFolder 零配置，文件夹名就是标签
#   🪨 不可再分：约定大于配置——减少人为错误
#   📖 Source: [ImageFolder] PyTorch 官方文档: torchvision.datasets.ImageFolder
if not DATASET_PATH.exists():
    print("Extracting ...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(".")
    print("Extraction complete.")

# ── 清理损坏图片 ──
# 做什么：逐个用 PIL 的 verify() 检查 JPEG 完整性，删除损坏文件
# Why 要 verify？→ 此数据集已知有损坏 JPEG
#   Why 损坏图片会出问题？→ DataLoader 解码失败 → 整个训练中断崩溃
#   Why 不能 try-except 跳过？→ DataLoader 的 collate 函数遇异常直接抛出，没法跳
#   Why JPEG 会损坏？→ JPEG 是压缩格式，依赖文件头+霍夫曼表，1 个字节错就废
#   🪨 不可再分：文件完整性是二进制层面的硬性约束
#   📖 Source: JPEG 标准 ITU-T T.81; Pillow docs — Image.verify() (https://pillow.readthedocs.io/)
removed = 0
for img_path in DATASET_PATH.rglob("*.jpg"):
    try:
        with Image.open(img_path) as img:
            img.verify()
    except Exception:
        img_path.unlink()
        removed += 1
print(f"Removed {removed} corrupted images.")
print(f"Dataset ready at: {DATASET_PATH.resolve()}")
```

---

## Cell 1: 数据加载与增强

```python
# ── 导入 ──
# random:                     控制数据分割的随机性，保证实验可复现
# torch:                      PyTorch 核心库（tensor 计算 + 自动求导 + GPU 加速）
# DataLoader:                 自动分 batch、打乱顺序、多进程预读取
# Subset:                     用索引列表从完整数据集中切出 train/test 子集（只存索引，不复制图片）
# datasets.ImageFolder:       按文件夹名自动分配类别标签 [ImageFolder]
# transforms:                 图像预处理流水线（Resize / Flip / Normalize 等）
import os, random
import torch
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

# ── 固定随机种子 ──
# 做什么：设定 random 和 torch 的随机种子为 42
# Why 设种子？→ 保证 train/test 分割每次一样 → 结果可复现
#   Why 要可复现？→ 不可复现就无法对比"改了参数后效果是变好还是变差"
#   🪨 不可再分：科学实验的基本要求——控制变量
#   📖 Source: PyTorch docs — Reproducibility (https://pytorch.org/docs/stable/notes/randomness.html)
random.seed(42)
torch.manual_seed(42)

# ── 选择计算设备 ──
# 做什么：检测 GPU 是否可用，优先使用 GPU
# Why 检测 CUDA？→ GPU 训练比 CPU 快 5-10 倍（矩阵并行计算）
#   Why GPU 快？→ GPU 有数千个小核心，同时算 batch 里所有样本的矩阵乘法
#   🪨 不可再分：并行计算是硬件架构优势
#   📖 Source: NVIDIA CUDA Programming Guide (https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# 做什么：定义数据加载函数 — 读取图片、做数据增强、分割 train/test、打包成 DataLoader
# Why 封装成函数？→ 主流程只需一行 load_dataset() 就完成所有数据准备
#   Why 参数化 split_ratio？→ 方便实验不同分割比例（80/20, 70/30 等）
#   🪨 不可再分：模块化 = 可复用 + 可测试 + 可维护
#   📖 Source: Martin (2003), "Clean Code", Prentice Hall — Single Responsibility Principle
def load_dataset(path, split_ratio=0.8):

    # ══════════════════════════════════════════════════
    # 训练集变换（有增强）
    # 做什么：用 transforms.Compose 将多个图像变换串成流水线，依次执行
    #         训练集额外加入 Flip 和 Rotation 做数据增强（测试集没有）
    # Why 数据增强？→ 让模型看到更多"变体"，防止死记硬背原图 [DataAug]
    #   Why 只增强训练集？→ 测试集模拟真实场景，不能人为修改
    #   🪨 不可再分：训练=学习、测试=考试，考试不能开卷
    #   📖 Source: [DataAug] Shorten & Khoshgoftaar (2019), "A survey on Image Data Augmentation", J Big Data 6(1), §3
    # ══════════════════════════════════════════════════
    train_transform = transforms.Compose([

        # 做什么：将所有图片统一缩放到 128×128 像素
        # Why Resize？→ 原图大小不一，必须统一才能组成 batch
        #   Why 必须统一？→ GPU 矩阵运算要求 batch 内所有数据形状一致
        #   Why 是 128？→ 比 ImageNet 标准(224)小 → 训练快 3 倍，Lab 演示够用
        #   Why 不是 64？→ 太小细节丢失太多（猫的胡须、狗的耳朵形状看不清）
        #   🪨 不可再分：GPU 并行计算硬性要求数据形状一致
        #   📖 Source: PyTorch docs — torch.utils.data.DataLoader, collate_fn 要求同形状 tensor
        transforms.Resize((128, 128)),

        # 做什么：以 50% 概率随机水平翻转图片（数据增强）
        # Why 翻转？→ 凭空产生新样本，等于数据量翻倍 [DataAug]
        #   Why 需要更多数据？→ 模型有 850 万参数，数据少会过拟合（死记硬背）
        #     Why 850万？→ 主要来自 FC1(全连接层1, Fully Connected Layer 1):
        #                  展平后 128×16×16=32768 维 × 256 个神经元 ≈ 839万参数，
        #                  加上 3 层 Conv(~9万) + FC2(514) ≈ 848万。详见 Cell 2 参数量统计
        #   Why 翻转不破坏标签？→ 猫左右翻转还是猫 → 语义不变
        #   Why 测试集不翻转？→ 测试=模拟真实使用，你不会把用户照片先翻转再识别
        #   🪨 不可再分：在「标签不变」前提下增加多样性 → 迫使学本质而非表面
        #   📖 Source: [DataAug] Shorten & Khoshgoftaar (2019), J Big Data 6(1); Krizhevsky et al. (2012), ImageNet paper §4.1
        transforms.RandomHorizontalFlip(),

        # 做什么：随机旋转 ±15°（数据增强）
        # Why 旋转？→ 模拟手机拍照时的角度倾斜 [DataAug]
        #   Why 是 ±15°？→ 太大(90°)产生不自然的空白；太小(2°)几乎没效果
        #   Why 拍照会有角度？→ 人手持相机不可能完美水平
        #   🪨 不可再分：模拟真实世界的数据分布 → 提升泛化
        #   📖 Source: [DataAug] Shorten & Khoshgoftaar (2019), J Big Data 6(1), §3 — Geometric Transformations
        transforms.RandomRotation(15),

        # 做什么：将 PIL 图片转为 PyTorch Tensor，像素值 [0,255] → [0,1]
        # Why ToTensor？→ PyTorch 只能处理 Tensor，这步是必须的
        #   Why 转 [0,1]？→ 浮点数范围小，梯度数值更稳定
        #   🪨 不可再分：框架的硬性输入要求
        #   📖 Source: PyTorch docs — torchvision.transforms.ToTensor (https://pytorch.org/vision/stable/transforms.html)
        transforms.ToTensor(),

        # 做什么：对 RGB 三通道分别标准化（减均值、除标准差）→ 均值≈0、标准差≈1
        # Why Normalize？→ 梯度下降在各维度尺度一致时收敛最快 [ImageNet][IN-norm]
        #   Why 尺度一致才快？→ 不一致 → 损失曲面是扁椭球 → 梯度方向被大尺度主导 → 来回震荡
        #   Why 用 ImageNet 的值？→ 120 万张图的统计量，业界标准，几乎所有模型通用
        #   🪨 不可再分：梯度下降在球形曲面上收敛最快——数学性质
        #   📖 Source: [ImageNet] Deng et al. (2009), CVPR; [IN-norm] PyTorch docs — torchvision.transforms.Normalize
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    # ══════════════════════════════════════════════════
    # 测试集变换（无增强！只有 Resize + ToTensor + Normalize）
    # 做什么：测试集只做尺寸统一和标准化，不做翻转/旋转
    # Why 没有 Flip 和 Rotation？→ 测试集 = 模拟真实场景，增强是训练专属的"作弊手段"
    #   🪨 不可再分：评估必须在不加干预的原始数据上才有意义
    #   📖 Source: Goodfellow et al. (2016), "Deep Learning", MIT Press, §5.2 — train/test separation principle
    # ══════════════════════════════════════════════════
    test_transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    # 做什么：用 ImageFolder 读取整个数据集，文件夹名自动变标签
    # Why ImageFolder？→ 零配置加载，文件夹名=标签，不需要手写 CSV 映射 [ImageFolder]
    #   🪨 不可再分：约定大于配置——减少人为错误
    #   📖 Source: [ImageFolder] PyTorch 官方文档: torchvision.datasets.ImageFolder
    full = datasets.ImageFolder(root=path, transform=train_transform)
    n = len(full)

    # 做什么：按 80/20 比例分割训练集和测试集
    # Why 80/20？→ 标准分割比例，训练~20000张，测试~5000张 [CLT]
    #   Why 不 50/50？→ 训练数据太少学不到足够的模式
    #   Why 不 99/1？→ 测试集太少(250张)评估不可靠
    #   Why 5000张够？→ 统计学：5000样本的精度置信区间 < ±1%
    #   🪨 不可再分：评估必须在「分布内但未见过」的数据上做
    #   📖 Source: [CLT] Casella & Berger, "Statistical Inference" (2nd ed.), §5.5; Goodfellow et al. (2016), §5.2
    train_n = int(n * split_ratio)

    # 做什么：随机打乱索引后分割，避免前半全是猫后半全是狗
    # Why 打乱？→ 原始数据按文件夹排列（前半猫后半狗），不乱分则训练集全猫
    #   🪨 不可再分：IID（独立同分布）是 SGD 收敛的理论前提
    #   📖 Source: Goodfellow et al. (2016), "Deep Learning", MIT Press, §8.1.3 — SGD convergence assumptions
    idx = list(range(n))
    random.shuffle(idx)
    train_data = Subset(full, idx[:train_n])
    test_data  = Subset(
        datasets.ImageFolder(root=path, transform=test_transform),
        idx[train_n:]
    )

    # 做什么：创建 DataLoader，每次取 32 张图组成一个 batch
    # Why batch_size=32？→「显存」和「梯度估计精度」的折中 [MiniBatch]
    #   Why 不把 20000 张一起算？→ GPU 显存放不下(需 3GB+ 纯数据 + 中间激活值)
    #   Why 不一张一张算？→ 单张图的梯度噪声极大 → 方向随机 → 收敛极慢
    #   Why 32 就够了？→ 中心极限定理：32 个样本的均值已是总体均值的合理近似 [CLT]
    #   🪨 不可再分：mini-batch = 有限计算资源下对真实梯度的蒙特卡洛近似
    #   📖 Source: [MiniBatch] Goodfellow et al. (2016), §8.1.3; [CLT] Casella & Berger, §5.5
    #
    # shuffle=True  → 不打乱则每轮按相同顺序看数据 → 参数更新有周期性偏差
    # num_workers=2 → 主进程算 GPU 时子进程提前读下一批图片 → GPU 不等 I/O
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True, num_workers=2)

    # shuffle=False → 测试不需要打乱，且方便复现
    test_loader = DataLoader(test_data, batch_size=32, shuffle=False, num_workers=2)
    print(f"Train: {train_n}  Test: {n - train_n}  Classes: {full.classes}")
    return train_loader, test_loader
```

---

## Cell 2: CNN 模型定义

```python
# ── 导入 ──
# torch.nn:            层定义（Conv2d / Linear / Dropout / MaxPool2d / Module 基类）
# torch.nn.functional: 无状态函数式 API（relu / softmax），不需要实例化
import torch.nn as nn
import torch.nn.functional as F

# 做什么：定义 SimpleCNN 类，继承 nn.Module（PyTorch 所有模型的基类）
# Why 继承 Module？→ 自动管理参数注册、GPU 搬移、train/eval 切换
#   Why 框架管理参数？→ 850万个 weight 手动跟踪不可能 → 必须自动化
#   🪨 不可再分："一切皆 Module" 是 PyTorch 的核心抽象
#   📖 Source: PyTorch docs — torch.nn.Module (https://pytorch.org/docs/stable/nn.html#torch.nn.Module)
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()

        # 做什么：第 1 个卷积层 — 输入 3 通道 RGB 图片，输出 32 个特征图，3×3 卷积核，补零 1
        #
        # 参数 in_channels=3
        # Why 是 3？→ RGB 彩色图有红/绿/蓝三个通道
        #   Why 不转灰度(1通道)？→ 颜色对区分猫狗有帮助(橘猫/黑狗)
        #   🪨 不可再分：图像本身就是 3 通道的物理表示
        #   📖 Source: Gonzalez & Woods (2018), "Digital Image Processing" (4th ed.), §6.1 — Color Fundamentals
        #
        # 参数 kernel_size=3
        # Why 3×3？→ VGGNet 证明：两个 3×3 = 一个 5×5 的感受野，但参数少 44% [VGG]
        #   Why 参数少重要？→ 850 万参数已经很多了，越多越容易过拟合
        #   Why 3×3 能提取特征？→ 看局部 9 个像素，堆叠多层逐步扩大视野
        #   Why 要看局部而非全局？→ 图像特征是局部构成的：边缘→纹理→部件→整体
        #   🪨 不可再分：图像有空间局部性——相邻像素强相关，远处弱相关（物理世界性质）[VGG §2.3]
        #   📖 Source: [VGG] Simonyan & Zisserman (2015), ICLR 2015, §2.1–2.3 (arXiv:1409.1556)
        #
        # 参数 padding=1
        # Why 补零？→ 让 3×3 卷积不改变图片尺寸：(128+2×1-3)/1+1=128
        #   Why 保持尺寸？→ 降维完全由 MaxPool 控制 → 架构设计更清晰
        #   Why 补零而不补别的？→ 零不携带信息、不引入偏置
        #   🪨 不可再分：让空间压缩可控——同一机制(Pool)统一管理
        #   📖 Source: [VGG] Simonyan & Zisserman (2015), §2.1 — same-padding + pooling design
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)

        # 做什么：第 2、3 个卷积层，通道数逐层翻倍 32→64→128
        # Why 递增？→ 浅层学简单特征(边缘)需要少；深层学复杂特征(眼睛形状)需要多
        #   Why 复杂特征需要更多 filter？→ 每个通道=一种特征检测器。边缘只有几种方向，毛发纹理千变万化
        #   Why 翻倍(×2)？→ 每次 Pool 空间减半(面积÷4)，通道翻倍补偿 → 总计算量大致不变
        #   🪨 不可再分：CNN 核心=逐层从"空间精度高+语义简单"到"空间精度低+语义丰富"
        #   📖 Source: Zeiler & Fergus (2014), "Visualizing and Understanding CNNs", ECCV 2014 — feature hierarchy
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        # 做什么：2×2 最大池化层 — 在每个 2×2 窗口中取最大值，宽高减半
        # Why 取最大？→ 最大值=该区域对某特征的最强响应。"有条线"比"平均有点像线"更有意义 [MaxPool]
        #   Why 要减少像素？→ 不减 → FC 层输入 128×128×128=200万维 → FC 参数超5亿 → 显存爆+过拟合
        #   Why 3次 Pool 刚好？→ 128÷2÷2÷2=16，再 Pool 变 8 太小，空间信息几乎没了
        #   🪨 不可再分：池化=信息论中的有损压缩——保留最显著特征、丢弃冗余
        #   📖 Source: [MaxPool] Scherer et al. (2010), "Evaluation of Pooling Operations in CNNs", ICANN 2010, §3
        self.pool = nn.MaxPool2d(2, 2)

        # 做什么：全连接层 1 — 将 128×16×16=32768 维特征压缩到 256 维
        # Why 是 128×16×16？→ 3次 Pool 后: 128通道 × (128÷2÷2÷2=16) × 16
        # Why 压到 256？→ 降维提取最终分类表示
        #   Why 不压到 64？→ 太小信息丢失，分不清
        #   Why 不压到 1024？→ 参数太多(3300万)，严重过拟合
        #   🪨 不可再分：维度 = 表达能力和过拟合风险的权衡
        #   📖 Source: Goodfellow et al. (2016), "Deep Learning", MIT Press, §5.2 — bias-variance tradeoff
        self.fc1 = nn.Linear(128 * 16 * 16, 256)

        # 做什么：Dropout 层 — 训练时随机关掉 50% 的 FC1 神经元
        # Why 要 Dropout？→ FC1 有 32768×256≈839万参数(占总参数99%)，最容易过拟合
        #   Why 随机关能防过拟合？→ 任何单个神经元都不能被依赖 → 被迫学冗余表示 → 更鲁棒
        #   Why 放 FC 不放 Conv？→ Conv 参数少(~9.3万)不太过拟合；FC 参数多(~839万)才是重灾区
        #   Why 是 0.5？→ Hinton 原论文推荐。0.5 使"子网络"组合数最大化: C(n,n/2) 是最大的 [Dropout §4, Table 5]
        #   🪨 不可再分：Dropout = 隐式 ensemble。每次训练不同子网络，推理用平均 [Dropout §7]
        #   📖 Source: [Dropout] Srivastava et al. (2014), JMLR 15, §4 Table 5 (p=0.5 optimal) & §7 (ensemble)
        self.dropout = nn.Dropout(0.5)

        # 做什么：全连接层 2（输出层） — 输出 2 个 logit: [猫的分数, 狗的分数]
        # Why 2 不是 1？→ CrossEntropyLoss 要求多分类格式(内部做 Softmax 需要 ≥2 个值)
        #   Why 不用 1+Sigmoid？→ 也可以，换成 BCEWithLogitsLoss 即可，效果等价
        #   Why 输出 logit 而非概率？→ 数值稳定性。Softmax+log 分开算有 log(0) 风险
        #   🪨 不可再分：浮点数有精度极限，框架合并计算避开浮点陷阱
        #   📖 Source: PyTorch docs — torch.nn.CrossEntropyLoss (LogSoftmax + NLLLoss fused for numerical stability)
        self.fc2 = nn.Linear(256, 2)

    def forward(self, x):                          # x: (B, 3, 128, 128)

        # 做什么：每层执行 Conv(不变尺寸) → ReLU(加非线性) → Pool(尺寸减半)
        #
        # ReLU = max(0, x): 负数变0，正数不变
        # Why 需要激活函数？→ 没有 → 多层线性=一层线性 → 网络再深也只能画直线分类
        #   Why 不用 Sigmoid？→ Sigmoid 导数最大 0.25，10层连乘=0.25^10≈0.000001 → 梯度消失
        #   Why ReLU 不消失？→ x>0 时导数=1，连乘还是 1 → 梯度畅通无阻 [ReLU]
        #   🪨 不可再分：反向传播=链式法则连乘。导数<1连乘→0(消失)，导数=1连乘→1(稳定) [Backprop]
        #   📖 Source: [ReLU] Nair & Hinton (2010), ICML; [Backprop] Rumelhart, Hinton & Williams (1986), Nature 323
        x = self.pool(F.relu(self.conv1(x)))       # → (B, 32, 64, 64)
        x = self.pool(F.relu(self.conv2(x)))       # → (B, 64, 32, 32)
        x = self.pool(F.relu(self.conv3(x)))       # → (B, 128, 16, 16)

        # 做什么：展平 + 全连接 + Dropout + 输出
        x = x.view(x.size(0), -1)                 # 展平: (B, 32768)
        x = F.relu(self.fc1(x))                    # → (B, 256)
        x = self.dropout(x)                        # 训练时随机关 50% 神经元
        x = self.fc2(x)                            # → (B, 2)
        return x
        # 注意: 最后没有 Softmax → CrossEntropyLoss 内部已包含，加两次会出错

# ══ 参数量统计 ══
# Conv1: 3×32×3×3 + 32         =       896
# Conv2: 32×64×3×3 + 64        =    18,496
# Conv3: 64×128×3×3 + 128      =    73,856
# FC1:   32768×256 + 256        = 8,388,864  ← 占 99%！
# FC2:   256×2 + 2              =       514
# 合计:                          ≈ 8,483,000
```

---

## Cell 3: 模型训练

```python
# ── 导入 ──
# torch.optim: 优化器集合（SGD / Adam / AdamW 等梯度更新算法）
import torch.optim as optim

# 做什么：设置训练轮数为 10（全部训练数据过 10 遍）
# Why 要过多遍？→ 一遍记不住（跟看教材一样）
#   Why 不过 100 遍？→ 过多 → 把训练集的噪声也学进去了（过拟合）
#   Why 不过 3 遍？→ 太少学不到足够的模式（欠拟合）
#   Why 10 轮？→ 从输出看 val_acc 还在涨(88%)，说明没学完但够展示
#   🪨 不可再分：epoch 数 = 「欠拟合」和「过拟合」之间的平衡点
#   📖 Source: Goodfellow et al. (2016), "Deep Learning", MIT Press, §7.8 — Early Stopping
def train_model(model, train_loader, test_loader, epochs=10):
    # 做什么：定义损失函数 — 交叉熵损失 = -log(预测对的那个类的概率)
    # Why 用交叉熵？→ 分类任务的理论最优损失函数（信息论推导）[CrossEntropy]
    #   Why 不用 MSE？→ MSE 在预测非常错时梯度反而小（学得慢），交叉熵越错梯度越大（学得快）
    #   Why -log？→ 信息论: -log(p) = "意外程度"。p=0.9→loss=0.1; p=0.1→loss=2.3 [KL]
    #   🪨 不可再分：交叉熵来自 KL 散度——衡量两个概率分布差异的理论最优度量
    #   📖 Source: [CrossEntropy] Goodfellow et al. (2016), §6.2.2; [KL] Shannon (1948), Bell System Tech. J.
    criterion = nn.CrossEntropyLoss()

    # 做什么：定义优化器 — Adam，学习率 0.001
    # Why Adam？→ 自动给每个参数分配独立学习率 → 不需要手动调参 [Adam]
    #   Why 不用 SGD？→ SGD 所有参数共享一个 lr，有的需要大步有的需要小步
    #   Why Adam 能自适应？→ 跟踪每个参数的梯度均值(方向)和方差(步幅) [Adam §2]
    #   Why lr=0.001？→ Adam 论文推荐默认值。太大(0.1)→震荡；太小(1e-6)→10轮学不到东西 [Adam §2 "suggested default: α=0.001"]
    #   🪨 不可再分：梯度下降=在高维曲面找最低点。Adam 用历史梯度统计自动调方向和步幅
    #   📖 Source: [Adam] Kingma & Ba (2015), ICLR 2015, §2 Algorithm 1 (arXiv:1412.6980)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, epochs + 1):

        # ════════ 训练阶段 ════════
        # 做什么：调用 model.train() 启用 Dropout
        # Why 调 train()？→ 启用 Dropout（随机关神经元）[PyTorch-train/eval]
        #   Why 验证时要关？→ 验证需要确定性结果 → eval() 自动关闭
        #   🪨 不可再分：训练和推理是两种不同的前向传播行为
        #   📖 Source: [PyTorch-train/eval] PyTorch docs — Module.train() / Module.eval()
        model.train()

        train_loss, correct, total = 0.0, 0, 0
        for imgs, labels in train_loader:           # 每次取 32 张图
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)

            # 做什么：① 清零旧梯度
            # Why 清零？→ PyTorch 默认累加梯度，不清=混入上一步的→更新方向全错
            #   Why 设计成累加？→ 方便梯度累积（显存不够时分多次小batch累积模拟大batch）
            #   🪨 不可再分：梯度必须精确反映「当前batch」对参数的偏导数
            #   📖 Source: PyTorch docs — Optimizer.zero_grad() (https://pytorch.org/docs/stable/optim.html)
            optimizer.zero_grad()

            # 做什么：② 前向传播 → ③ 算损失
            out = model(imgs)                        # → (32, 2) logits
            loss = criterion(out, labels)

            # 做什么：④ 反向传播 — 用链式法则算每个参数的梯度
            # Why？→ 链式法则从 loss 往回算每层参数的偏导数 [Backprop]
            #   🪨 不可再分：微积分链式法则 df/dx = df/dy × dy/dx
            #   📖 Source: [Backprop] Rumelhart, Hinton & Williams (1986), Nature 323; Goodfellow et al. (2016), §6.5
            loss.backward()

            # 做什么：⑤ 用梯度更新权重: w = w - lr × grad
            optimizer.step()

            # 5步循环总结:
            # zero_grad → forward → loss → backward → step
            # 清梯度   →  算预测  → 算误差 → 算梯度  → 更新权重

            # 做什么：累加本 batch 的 loss 和正确数
            # Why 乘 batch_size？→ criterion 返回 batch 平均 loss，乘回来还原总 loss
            #   → 最后除以总样本数算 epoch 平均，比直接平均 batch 更准（最后一个 batch 可能不满32）
            train_loss += loss.item() * imgs.size(0)

            # 做什么：argmax(1) 取 2 个 logit 中较大者的索引 → 0=Cat, 1=Dog
            correct += (out.argmax(1) == labels).sum().item()
            total += labels.size(0)

        train_loss /= total
        train_acc = correct / total

        # ════════ 验证阶段 ════════
        # 做什么：调用 model.eval() 关闭 Dropout，进入推理模式
        model.eval()

        val_loss, val_correct, val_total = 0.0, 0, 0

        # 做什么：关闭梯度计算（省显存+加速）
        # Why no_grad？→ 验证不需要反向传播，关掉省显存+加速
        #   Why 省显存？→ 不需要存中间激活值（正向时存的，供反向用）
        #   🪨 不可再分：梯度计算需要存中间结果，不算梯度就不用存
        #   📖 Source: PyTorch docs — torch.no_grad() (https://pytorch.org/docs/stable/generated/torch.no_grad.html)
        with torch.no_grad():
            for imgs, labels in test_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                out = model(imgs)
                val_loss += criterion(out, labels).item() * imgs.size(0)
                val_correct += (out.argmax(1) == labels).sum().item()
                val_total += labels.size(0)
        val_loss /= val_total
        val_acc = val_correct / val_total

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)
        print(f"Epoch [{epoch:02d}/{epochs}]  train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  val_loss={val_loss:.4f}  val_acc={val_acc:.4f}")

    return history

# ══ 实际训练输出 ══
# Epoch 01: train_acc=62%  val_acc=73%  ← 刚开始学
# Epoch 05: train_acc=83%  val_acc=85%  ← 快速提升
# Epoch 10: train_acc=88%  val_acc=88%  ← 差距≈0 → 没有过拟合！
#
# Why val_acc 初期 > train_acc？
#   → Dropout 只在训练时开（训练更难），验证时关（全力发挥）→ 训练分低是正常的
```

---

## Cell 4: 模型评估

```python
# 做什么：在测试集上评估模型，生成 accuracy 和分类报告（precision / recall / F1）
# Why 单独封装？→ 评估逻辑独立于训练，方便随时对任意模型+数据组合做评估
#   🪨 不可再分：训练和评估解耦 = 更灵活的实验流程
#   📖 Source: Software engineering — Separation of Concerns principle
def evaluate_and_predict(model, test_loader):
    # 做什么：切换到评估模式（关闭 Dropout）
    # Why eval()？→ 训练时 Dropout 随机关神经元，评估时要用全部神经元得到确定性结果 [PyTorch-train/eval]
    #   🪨 不可再分：评估必须是确定性的——同一输入必须得到同一输出
    #   📖 Source: [PyTorch-train/eval] PyTorch docs — Module.train() / Module.eval()
    model.eval()
    predictions, actual_labels = [], []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(DEVICE)

            # 做什么：取最大 logit 的索引作为预测类别（0=Cat, 1=Dog）
            # Why argmax？→ 2个logit中值更大的=模型更有信心的类别
            #   🪨 不可再分：分类=选概率最高的那个类
            #   📖 Source: Bishop (2006), "Pattern Recognition and ML", §1.5.4 — Minimizing misclassification rate
            preds = model(imgs).argmax(1)

            # 做什么：将 GPU tensor 搬回 CPU 并转为 Python list
            # Why .cpu()？→ sklearn 是纯 CPU 库，不能直接用 GPU tensor
            # Why .tolist()？→ sklearn 需要 Python list，不接受 Tensor
            #   🪨 不可再分：不同库之间的数据格式必须兼容
            #   📖 Source: scikit-learn docs — sklearn.metrics (https://scikit-learn.org/stable/modules/model_evaluation.html)
            predictions.extend(preds.cpu().tolist())
            actual_labels.extend(labels.tolist())

    accuracy = sum(p == a for p, a in zip(predictions, actual_labels)) / len(actual_labels)
    print(f"Accuracy: {accuracy:.4f}")

    # 做什么：打印 sklearn 分类报告（每类的 precision / recall / F1）
    # Why 用 classification_report 不只看 accuracy？
    #   → accuracy 只告诉你"总体对了多少"，看不出对猫好还是对狗好
    #   Why 需要看每类？→ 如果 1000猫全判成狗、1000狗全对 → accuracy=50% 但猫 recall=0%
    #   🪨 不可再分：单一指标隐藏了类别间的性能差异
    #   📖 Source: Sokolova & Lapalme (2009), "A systematic analysis of performance measures for classification tasks", Info. Proc. & Mgmt.
    # sklearn.metrics: scikit-learn 评估工具库
    from sklearn.metrics import classification_report
    print(classification_report(actual_labels, predictions, target_names=['Cat', 'Dog']))
    return accuracy, predictions, actual_labels

# ══ 实际输出 ══
#              precision  recall  f1-score
#     Cat        0.90      0.86     0.88
#     Dog        0.87      0.91     0.89
#     Accuracy                       0.88
#
# Precision = TP/(TP+FP) → "说是猫的里面 90% 真是猫"
# Recall    = TP/(TP+FN) → "100 只真猫能认出 86 只"
# F1 = 2PR/(P+R) → 调和平均，惩罚 P 和 R 差距大
#
# Why Cat recall < Dog recall？
#   → 14%猫被误判为狗 vs 9%狗被误判为猫 → 某些猫更"狗化"
```

---

## Cell 5: 主流程

```python
# 做什么：4步 pipeline — 加载数据 → 创建模型 → 训练 → 评估
# 模块化设计: 换模型只需改 SimpleCNN()，换数据只需改路径
train_loader, test_loader = load_dataset(str(DATASET_PATH))
model = SimpleCNN().to(DEVICE)
train_model(model, train_loader, test_loader, epochs=10)
accuracy, predictions, actual_labels = evaluate_and_predict(model, test_loader)
```
