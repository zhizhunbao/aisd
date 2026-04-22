# Lecture 7 故事线：从零认识 PyTorch —— 深度学习框架的选择与实战

> **Source:** `Week 7 - Introduction to Pytorch.pptx`
> **核心主题：** 为什么深度学习需要专门的框架？PyTorch 如何从一个学术实验工具进化为工业级 CV 平台？
> **故事线：** 从手写梯度的痛苦，到 PyTorch 全自动训练流水线的构建 —— 一条「解放双手」的进化之路

---

## 🎬 序幕：我们在解决什么问题？

### 计算机视觉的核心困境

在机器视觉 (Machine Vision) 课程中，我们已经学过了图像处理的基本操作——边缘检测、形态学变换、特征提取。但当任务变成**图像分类、目标检测、语义分割**时，传统手工特征方法面临三大瓶颈：

1. **特征工程耗时**：每换一个任务就要重新设计特征（SIFT？HOG？LBP？），没有通用方案
2. **性能天花板**：手工特征在复杂场景下准确率难以突破
3. **数据规模**：深度学习需要处理海量图像数据，手写循环训练效率极低

> 💡 **关键问题**：如果我们要用神经网络来做 CV，需要什么工具？
> - 能高效处理大规模数组运算（图像本质是矩阵）
> - 能自动计算梯度（手写反向传播太痛苦）
> - 能利用 GPU 加速（CPU 太慢了）
> - 能灵活修改网络结构（研究需要快速迭代）

这就是**深度学习框架**要解决的问题。而 PyTorch，正是目前最适合 CV 研究和教学的答案。

---

## 📚 第一章：框架之争 —— 为什么是 PyTorch？

### 1.1 从 Lua 的 Torch 到 Python 的 PyTorch

深度学习框架的历史可以用一场**语言选择的进化**来理解：

| 时间 | 事件 | 关键意义 |
|------|------|----------|
| 2002 | Torch (Lua) 诞生 | ✅ 首个支持 GPU 加速的 ML 框架 |
| 2015 | TensorFlow (Google) 发布 | ✅ 静态计算图 + 工业级部署 |
| **2016** | **PyTorch (Facebook/FAIR) 发布** | **✅ 动态计算图 + Pythonic 设计** |
| 2017-2020 | PyTorch 快速增长 | Hugging Face 全面采用 |
| 2022 | 转入 Linux Foundation | 开放治理，非 Meta 独占 |
| 2023 | PyTorch 2.0 发布 | `torch.compile` 大幅提速 |

> 💡 **为什么 Torch (Lua) 失败了？** Lua 虽然运行快，但生态太小——Python 拥有 NumPy、SciPy、Pandas、Matplotlib 等海量科学计算库。PyTorch 的选择是：**把 Torch 的 GPU 加速能力包装在 Python 里**，让研究者不用学新语言。

### 1.2 PyTorch vs TensorFlow：静态图 vs 动态图

这是理解框架选择的**核心分歧**：

| 维度 | TensorFlow (静态图) | PyTorch (动态图) |
|------|:---:|:---:|
| 图的构建方式 | 先定义完整计算图，再喂数据 (Define-and-Run) | 边写边执行，每次前向传播即时构建图 (Define-by-Run) |
| 调试难度 | ❌ 需要专门工具（TensorBoard） | ✅ 可以直接用 `print()`、`pdb` 调试 |
| 灵活性 | ❌ 图结构固定后难以动态修改 | ✅ 条件分支、循环、变长输入都很自然 |
| 研究适用性 | ⚠️ 需要先画好蓝图再实验 | ✅ 像写普通 Python 一样搭网络 |
| 部署生态 | ✅ TFLite、TF Serving、TF.js | ⚠️ TorchScript、ONNX 在增长中 |

> 🔑 **一句话总结**：
> - **做研究/学习 → PyTorch**（灵活、直观、调试方便）
> - **做生产部署 → TensorFlow**（工具链成熟），但差距正在缩小

### 1.3 ❗ 前置知识的关键铺垫

在进入 PyTorch 组件之前，需要理解深度学习训练的**核心循环**：

```
数据（Tensor）→ 送入模型 → 计算预测 → 计算损失 → 反向传播求梯度 → 更新参数 → 重复
    ↑                                                                    ↓
    └────────────────────── 循环直到收敛 ──────────────────────────────────┘
```

PyTorch 为这个循环的**每一步**都提供了对应的组件。接下来，我们逐一拆解。

> 🔑 **故事转折点：** 知道「为什么选 PyTorch」之后，下一个问题是「它内部是怎么工作的？」→ 三大核心组件登场！

---

## 🎭 第二章：数据的容器 —— 张量 (Tensor)

### 2.1 一句话定义

> **张量 (Tensor) = 支持 GPU 加速的多维数组 = NumPy 的 ndarray + CUDA 能力**

### 2.2 从标量到张量的维度推广

| 维度 | 数学名称 | 例子 | PyTorch 表示 |
|------|----------|------|------|
| 0-D | 标量 (Scalar) | 温度 = 36.5 | `torch.tensor(36.5)` |
| 1-D | 向量 (Vector) | RGB = [255, 0, 0] | `torch.tensor([255, 0, 0])` |
| 2-D | 矩阵 (Matrix) | 灰度图 28×28 | `torch.zeros(28, 28)` |
| 3-D | 3阶张量 | 彩色图 3×28×28 | `torch.zeros(3, 28, 28)` |
| 4-D | 4阶张量 | 一批图片 batch×C×H×W | `torch.zeros(32, 3, 224, 224)` |

> 💡 **CV 中的记忆法**：在 PyTorch 中处理图像，数据形状永远是 `[Batch, Channel, Height, Width]`（BCHW 格式）。比如一批 32 张 224×224 的 RGB 图 → `(32, 3, 224, 224)`。

### 2.3 张量的三大超能力

1. **GPU 加速** → `tensor.to('cuda')` 一行代码把运算搬到显卡
2. **分布式处理** → 多 GPU、多服务器并行计算
3. **计算图追踪** → 每个张量记住「谁创建了它」→ 这正是自动微分的基础

> 💡 **类比**：张量就像一个**带导航功能的行李箱**——它不仅装着你的数据（数组），还记得自己是怎么到这里的（计算路径），走丢了还能原路返回（反向传播）。

> 🔑 **故事转折点：** 张量能追踪计算图，但谁来利用这个计算图自动求导？→ Autograd 登场！

---

## 📖 第三章：自动求导 —— Autograd 引擎

### 3.1 为什么需要自动微分？

训练神经网络的核心是**梯度下降 (Gradient Descent)**：

```
参数_新 = 参数_旧 − 学习率 × ∂Loss/∂参数
```

问题是：现代神经网络有**数百万个参数**，手写每个参数的偏导数不可能。

### 3.2 Autograd 的工作原理

PyTorch 的解决方案是**反向自动微分 (Reverse-mode Automatic Differentiation)**：

1. **前向传播 (Forward Pass)**：正常运行网络，计算预测值，同时悄悄**记录所有运算**到计算图
2. **计算损失 (Loss Calculation)**：用损失函数衡量预测和真实标签的差距
3. **反向传播 (Backward Pass)**：调用 `loss.backward()`，PyTorch 沿着计算图**反向**逐步求导（链式法则）
4. **参数更新**：优化器利用计算出的梯度更新参数

> 💡 **类比**：Autograd 就像**倒带功能**——前向传播是录像，`loss.backward()` 是倒放录像，沿着录像路径依次计算每一步对最终结果的影响（梯度）。

### 3.3 ❗ 关键要点

- 要参与梯度计算的张量需设置 `requires_grad=True`
- `loss.backward()` 之后，每个参数的 `.grad` 属性就存好了梯度
- **Autograd 解放了研究者**——你只需定义前向传播，反向传播全自动

> 🔑 **故事转折点：** 有了数据容器 (Tensor) 和求导引擎 (Autograd)，还缺什么？→ 需要一种**组织网络结构**的方式 → nn.Module 登场！

---

## 🏆 第四章：搭积木 —— nn.Module 与训练全流程

### 4.1 nn.Module：PyTorch 网络的骨架

PyTorch 用 `nn.Module` 作为所有网络的**基类**，提供了统一的「搭积木」接口：

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3)     # 卷积层
        self.relu  = nn.ReLU()                 # 激活函数
        self.fc    = nn.Linear(16*26*26, 10)   # 全连接层

    def forward(self, x):
        x = self.relu(self.conv1(x))          # 前向传播逻辑
        x = x.view(x.size(0), -1)             # 展平
        return self.fc(x)
```

> 💡 **设计哲学**：`__init__` 里列清单（有哪些层），`forward` 里画路线（数据怎么流）。就像一个**工厂蓝图**——先买好所有机器，再规定产品从第一台机器到最后一台机器的流转路线。

### 4.2 损失函数：衡量「差距」的标尺

| 任务类型 | 损失函数 | 直觉 |
|----------|----------|------|
| 分类 (Classification) | `nn.CrossEntropyLoss()` | 预测的概率分布和真实标签差多远 |
| 回归 (Regression) | `nn.MSELoss()` | 预测值和真实值的均方误差 |

### 4.3 优化器：驱动学习的引擎

| 优化器 | 特点 | 适用场景 |
|--------|------|----------|
| SGD | 最基础，需要手动调学习率 | 教学、简单任务 |
| Adam | 自适应学习率，收敛快 | ⭐ 大多数场景的默认选择 |
| RMSprop | 自适应，擅长处理稀疏梯度 | RNN、NLP |

### 4.4 端到端训练流程——三大阶段

```
┌─────────────────────┐
│  第一阶段：数据准备    │
│  - 原始数据 → Tensor   │
│  - Dataset + DataLoader │
│  - transforms 预处理    │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│  第二阶段：模型开发    │
│  - 定义网络 (nn.Module)│
│  - 选择损失函数        │
│  - 选择优化器          │
│  - 训练循环 (train)    │
│  - 验证循环 (val)      │
└────────┬────────────┘
         ▼
┌─────────────────────┐
│  第三阶段：模型部署    │
│  - torch.save()       │
│  - TorchScript 导出   │
│  - 部署到云/边缘设备   │
└─────────────────────┘
```

### 4.5 Dataset 与 DataLoader

- **Dataset**：定义「数据从哪来、怎么读」
  - 自定义 `__getitem__` 和 `__len__` 方法
- **DataLoader**：定义「数据怎么送进模型」
  - 自动批量化 (batching)、打乱 (shuffling)、多进程加载

> 💡 **类比**：Dataset 像是**菜市场**（定义了每种菜在哪、怎么挑），DataLoader 像是**外卖小哥**（自动打包、配送、还能并行送多单）。

> 🔑 **故事转折点：** 掌握了 Tensor + Autograd + nn.Module + DataLoader 四件套，我们已经能从零构建训练流程。但在 CV 中，很少从零训练 → 迁移学习登场！

---

## 📹 第五章：CV 实战 —— torchvision 与迁移学习

### 5.1 torchvision 生态系统

PyTorch 为计算机视觉专门提供了 `torchvision` 库，包含：

| 组件 | 功能 | 示例 |
|------|------|------|
| `torchvision.models` | 预训练模型 | ResNet、VGG、EfficientNet |
| `torchvision.datasets` | 标准数据集 | ImageNet、CIFAR-10、COCO |
| `torchvision.transforms` | 图像变换 | 裁剪、归一化、数据增强 |

### 5.2 迁移学习 (Transfer Learning)

> **核心思想**：不从零训练，而是**借用**在 ImageNet 上预训练好的模型，只替换最后分类层，用自己的数据微调。

```python
import torchvision.models as models

# 加载预训练 ResNet
model = models.resnet18(pretrained=True)

# 替换最后的全连接层（适配自己的类别数）
model.fc = nn.Linear(512, num_classes)
```

> 💡 **为什么迁移学习有效？** 预训练模型的前几层学到的是**通用视觉特征**（边缘、纹理、形状），这些特征在不同 CV 任务间是共享的。只需微调后几层就能适配新任务。

---

## ⚡ 第六章：生产级能力 —— 高级特性与最佳实践

### 6.1 从实验到生产的关键技术

| 技术 | 解决什么问题 | 一句话总结 |
|------|-------------|-----------|
| CUDA 支持 | CPU 太慢 | `.to('cuda')` 将计算搬到 GPU |
| 分布式训练 | 单 GPU 内存不够 | 多 GPU/多机器并行训练 |
| JIT 编译 (TorchScript) | Python 运行慢 | 将模型编译为优化的中间表示 |
| C++ 前端 | 需要嵌入 C++ 系统 | 脱离 Python 解释器部署 |

### 6.2 PyTorch 最佳实践清单

1. ✅ **尽可能使用 GPU** → `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`
2. ✅ **正确划分数据集** → 训练集 / 验证集 / 测试集
3. ✅ **用 DataLoader 管理数据** → 自动批处理和多进程
4. ✅ **定期保存模型** → `torch.save(model.state_dict(), 'model.pth')`
5. ✅ **代码模块化** → 数据、模型、训练逻辑分离
6. ✅ **良好文档化** → 记录超参数、实验结果

### 6.3 社区与生态系统

PyTorch 已转入 **Linux Foundation** 开放治理：
- 官方文档 + 教程完善
- PyTorch Forum 活跃的问答社区
- Hugging Face、Meta、Google 等持续贡献
- 2022+ 已是学术界论文实现的**首选框架**

---

## 🗺️ 全局回顾：PyTorch 知识路线图

```
┌──────────────────────────────────────────────────┐
│       PyTorch 学习路线图                           │
│                                                    │
│  ① 为什么需要框架？                                │
│  手写梯度太痛苦，需要自动化工具                     │
│         │                                          │
│         ▼                                          │
│  ② 为什么选 PyTorch？                              │
│  ✅ 动态图 ✅ 调试方便 ✅ 研究首选                  │
│  ❌ 部署生态不如 TensorFlow（但正在追赶）           │
│         │                                          │
│         ▼                                          │
│  ③ 核心组件三件套                                  │
│  Tensor（数据容器）                                │
│  → Autograd（自动求导）                            │
│  → nn.Module（网络骨架）                           │
│         │                                          │
│         ▼                                          │
│  ④ 训练全流程                                      │
│  DataLoader（数据加载）                            │
│  → Forward（前向传播）                             │
│  → Loss（计算损失）                                │
│  → Backward（反向传播）                            │
│  → Optimizer.step（更新参数）                      │
│         │                                          │
│         ▼                                          │
│  ⑤ CV 实战                                        │
│  torchvision + 迁移学习                            │
│  ResNet / VGG / EfficientNet                       │
│         │                                          │
│         ▼                                          │
│  ⑥ 生产级部署                                     │
│  CUDA + 分布式训练 + TorchScript                   │
└──────────────────────────────────────────────────┘
```

### 技术演进转折总结

| 从 → 到 | 解决了什么核心问题？ |
|---------|---------------------|
| 手写梯度 → Autograd | 自动求导，不再需要手动推导每个参数的偏导数 |
| NumPy 数组 → Tensor | GPU 加速 + 计算图追踪，适配深度学习训练 |
| 裸代码搭网络 → nn.Module | 统一的网络定义接口，模块化、可复用 |
| 手动数据循环 → DataLoader | 自动批处理、打乱、多进程并行加载 |
| 从零训练 → 迁移学习 | 借用预训练权重，小数据也能获得好效果 |
| Python 实验 → TorchScript | 编译优化，脱离 Python 解释器，可嵌入 C++ |

---

## 📝 考试/复习重点检查清单

- [ ] **PyTorch 定义**：开源 Python ML 库，以动态计算图、GPU 加速、Python 集成著称
- [ ] **历史演进**：Torch (Lua, 2002) → PyTorch (Python, 2016) → Linux Foundation (2022) → PyTorch 2.0 (2023)
- [ ] **动态图 vs 静态图**：Define-by-Run（PyTorch）vs Define-and-Run（TensorFlow）；动态图更灵活、更易调试
- [ ] **PyTorch vs TensorFlow 选型**：研究/灵活性 → PyTorch；企业部署/移动端 → TensorFlow
- [ ] **三大核心组件**：Tensor（数据容器 + GPU）、Autograd（自动微分）、Optimizer（参数更新）
- [ ] **Tensor 本质**：标量→向量→矩阵→高阶张量的维度推广；类似 NumPy ndarray 但支持 GPU
- [ ] **Tensor 三大优势**：GPU 加速、分布式处理、计算图追踪
- [ ] **Autograd 机制**：前向传播记录计算图 → `loss.backward()` 沿图反向求导 → `.grad` 存储梯度
- [ ] **nn.Module 结构**：`__init__` 定义层，`forward` 定义数据流
- [ ] **损失函数**：分类用 CrossEntropyLoss，回归用 MSELoss
- [ ] **优化器**：SGD（基础）、Adam（⭐ 默认推荐）、RMSprop（稀疏梯度）
- [ ] **训练三阶段**：数据准备（Dataset + DataLoader）→ 模型开发（训练 + 验证）→ 模型部署（save + deploy）
- [ ] **DataLoader**：自动批处理 (batching)、打乱 (shuffling)、多进程加载
- [ ] **torchvision**：预训练模型、标准数据集、图像变换
- [ ] **迁移学习**：加载预训练模型 → 替换最后分类层 → 微调
- [ ] **高级特性**：CUDA 加速、分布式训练、JIT 编译器 (TorchScript)、C++ 前端
- [ ] **最佳实践**：GPU 加速、数据集正确划分、定期保存模型、代码模块化

---

## 📚 参考资料

- [week7_pytorch_slides.md](week7_pytorch_slides.md) — 原始幻灯片提取（含双语翻译）
- [PyTorch 官方文档](https://pytorch.org/docs/)
- [PyTorch 教程](https://pytorch.org/tutorials/)
- [torchvision 文档](https://pytorch.org/vision/)
