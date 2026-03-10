# Lab 5 — CNN 历史线 (History Timeline)

> 🕰️ 核心问题：**CNN 从哪里来？每个技术突破解决了什么问题？Lab 5 的 SimpleCNN 站在什么历史位置上？**  
> 🎯 故事线：[lab5_storyline.md](lab5_storyline.md) | 教程：[lab5_tutorial.md](lab5_tutorial.md)

---

## 📍 全景时间线 (Panoramic Timeline)

```
1989            1998            2012             2014             2015            2017+
  │               │               │                │                │               │
  ▼               ▼               ▼                ▼                ▼               ▼
LeCun           LeNet-5         AlexNet           VGG              ResNet         Transformer
原型诞生         奠定架构         深度学习元年       工程化验证         百层可能         注意力时代

"反向传播        "卷积+池化        "GPU加速+         "越深越好          "跳跃连接         "CNN 的
 训练卷积网络"   +全连接=CNN"      Dropout=突破"     但难训练"          解决退化"         地位被挑战"
     │               │               │                │                │               │
     ↓               ↓               ↓                ↓                ↓               ↓
仅限学术      工业级手写识别    ILSVRC错误率       错误率7.3%         错误率3.57%      ViT/DINO
 实验          准确率99.2%      从26% → 15.3%     比人类还低          超越人类         开始主导
```

---

## 🚉 各站详解

### 站 1: LeCun — CNN 的诞生 (1989)

**📌 之前的挑战：** 神经网络理论上可行，但反向传播算法（1986, Rumelhart & Hinton）如何应用于视觉任务尚不清楚。普通 MLP（多层感知机）对图像参数爆炸，无法实用。

**💡 核心创新（LeCun et al., 1989）：**

- 首次将**反向传播**与**权重共享的卷积结构**结合用于图像识别
- 关键洞察：手写数字的局部笔画特征可以用**滑动的小核**检测，核可以在整张图上共享
- 实现了用于 zip code（邮政编码）识别的紧凑网络

**👤 关键人物：**
- Yann LeCun（"卷积神经网络之父"，现为 Meta AI 首席科学家）
- Geoff Hinton（反向传播先驱，2018 年图灵奖）

**⚠️ 遗留问题：** 当时计算资源（CPU）太弱，只能处理小图像（28×28 像素）；数据集太小；训练时间以天计。

---

### 站 2: LeNet-5 — 标准 CNN 架构的确立 (1998)

**📌 之前的挑战：** 1989 年的原型网络结构不统一，缺乏系统的架构设计原则。

**💡 核心创新（LeCun et al., 1998, "Gradient-Based Learning Applied to Document Recognition"）：**

- 确立了 **[卷积层 → 池化层] × N → 全连接层** 的经典 CNN 架构模板
- LeNet-5 具体结构：Conv(6) → Pool → Conv(16) → Pool → FC(120) → FC(84) → FC(10)
- 使用 **Average Pooling**（而非今天常用的 Max Pooling）
- 激活函数使用 **Tanh**（ReLU 尚未普及）

**成果：** 在 MNIST 手写数字数据集上达到 **99.2% 准确率**，被美国邮政系统实际部署用于支票识别。

**⭐ 与 Lab 5 的联系：** Lab 5 的 SimpleCNN 就是 LeNet-5 思想的现代版本：
```
SimpleCNN:  Conv(32) → MaxPool → Conv(64) → MaxPool → Conv(128) → MaxPool → FC(256) → FC(2)
LeNet-5:    Conv(6)  → AvgPool → Conv(16)  → AvgPool → FC(120)  → FC(84)  → FC(10)
```
区别：MaxPool 替代 AvgPool，ReLU 替代 Tanh，Dropout 用于防止过拟合。

**⚠️ 遗留问题：** 仍只能处理小图像，无法扩展到自然图像（如猫狗照片）。

---

### 站 3: AlexNet — 深度学习元年 (2012)

**📌 之前的背景（2000-2011）：** 深度学习停滞期。CNN 被认为难以训练，SVM 等浅层方法占主流。ILSVRC（ImageNet 大型视觉识别挑战赛，2010 年启动）推动了大规模图像识别研究。

**💡 核心创新（Krizhevsky, Sutskever, Hinton, 2012）：**

- 5 Conv + 3 FC 的深度网络，在 ImageNet 上将错误率从 **26.2%** 降至 **15.3%**（超出第二名 10.8 个百分点）
- 三个关键技术使大网络可行：
  1. **ReLU 激活函数**：替代 Sigmoid/Tanh，解决梯度消失，训练速度提升 6×
  2. **GPU 并行训练**（两块 GTX 580，3GB 显存）：使在 ImageNet 上训练成为可能
  3. **Dropout（0.5）**：解决过拟合，等效于集成大量子网络

**成果：** 深度学习"大爆炸"的起点，开启了 ImageNet 竞赛的 CNN 时代。

**⭐ 与 Lab 5 的联系：** Lab 5 完整使用了 AlexNet 引入的两大技术：
```python
F.relu(self.conv1(x))    # ReLU 来自 AlexNet
self.dropout = nn.Dropout(0.5)  # Dropout 来自 AlexNet
```

**⚠️ 遗留问题：** 为什么网络深了就好？没有理论解释。网络加深后训练误差反而上升（退化问题）。

---

### 站 4: VGGNet — 深度的系统验证 (2014)

**📌 核心问题：** AlexNet 用了混合尺寸的卷积核（11×11, 5×5, 3×3），为什么这样设计？有没有更简洁的原则？

**💡 核心创新（Simonyan & Zisserman, Oxford VGG 组, 2014）：**

- 回答了"**深度比宽度更重要**"
- 全程只用 **3×3 卷积核**，通过堆叠提升感受野：
  - 两层 3×3 = 等效一层 5×5（感受野），但参数更少：$2(3^2 C^2) < 5^2 C^2$
  - 三层 3×3 = 等效一层 7×7
- VGG-16（16 层），VGG-19（19 层），错误率 **7.3%**

**⭐ 与 Lab 5 的联系：** Lab 5 的所有卷积核都是 **3×3 with padding=1** ——这就是 VGGNet 确立的设计原则。

---

### 站 5: ResNet — 突破深度极限 (2015)

**📌 核心问题：** VGGNet 验证了"越深越好"，但实验发现：层数从 20 到 56，训练误差反而升高（不是过拟合，是训练本身困难了）。

**💡 核心创新（He et al., Microsoft Research, 2015）：**

残差连接（Residual Connection / Skip Connection）：

$$\text{输出} = \mathcal{F}(x) + x$$

| 符号 | 含义 |
|------|------|
| $x$ | 输入（直接跳过几层）|
| $\mathcal{F}(x)$ | 几层卷积的输出（残差）|
| $\mathcal{F}(x) + x$ | 最终输出 |

**直觉：** 最坏情况下，残差块只需学 $\mathcal{F}(x) = 0$（恒等映射），不会比不加层更差。

成果：ResNet-152（152 层）在 ImageNet 上错误率 **3.57%，低于人类 5%**。

**⚠️ 遗留问题：** 参数量大（2500 万），推理慢，不适合移动端。

---

### 站 6: 移动和高效设计的时代 (2016-2020)

| 网络 | 年份 | 核心思路 | 亮点 |
|------|------|---------|------|
| SqueezeNet | 2016 | 1×1 卷积压缩通道数 | AlexNet 准确率，1/50 参数量 |
| MobileNet | 2017 | Depthwise Separable Convolution | 适合手机端实时推理 |
| EfficientNet | 2019 | 同时缩放深度/宽度/分辨率 | ImageNet SOTA，参数效率最高 |

---

### 站 7: Transformer 挑战 CNN 主导地位 (2020+)

**📌 背景：** NLP 领域 Transformer（2017, "Attention is All You Need"）大获成功。

**💡 关键工作：**

- **ViT（Vision Transformer, 2020）**：将图像切成 patch，用 Transformer 处理，在足够大的数据集上超越 CNN
- **DINO/DINOv2 (Meta, 2021-2023)**：无监督 ViT，特征质量超越监督 CNN
- **混合时代**：CNN 特征提取 + Transformer 注意力机制结合

**CNN 在什么场景仍占优？**
- 小数据集（ImageNet 20% 以下）
- 实时边缘推理（需要轻量化）
- 需要平移等变性的精确场景（医学图像分割等）

---

## 📊 Lab 5 的历史定位

```
时代            代表网络         Lab 5 用到了什么
────────────────────────────────────────────────────────
1989 LeCun      原型 CNN        ← 权重共享基本思想
1998 LeNet-5    经典 CNN 架构   ← [Conv→Pool]×N→FC 结构
2012 AlexNet    深度学习元年    ← ReLU + Dropout
2014 VGGNet     3×3 卷积原则   ← 全用 3×3 卷积核(padding=1)
2015 ResNet     残差连接        ✗ SimpleNet 未用
2017+ ViT       注意力机制      ✗ 本 Lab 超出范围

→ SimpleCNN = LeNet-5 架构 + AlexNet 训练技术 + VGGNet 卷积设计
              (1998 经典)         (2012 突破)        (2014 简洁化)
```

---

## 👤 关键人物

| 人物 | 贡献 | 机构 |
|------|------|------|
| Yann LeCun | 发明 CNN，LeNet | 贝尔实验室 → Meta AI |
| Geoff Hinton | 反向传播，深度学习先驱 | 多伦多大学 → Google Brain |
| Alex Krizhevsky | AlexNet | 多伦多大学 |
| Karen Simonyan | VGGNet | Oxford VGG 组 |
| Kaiming He | ResNet, PReLU | Microsoft Research → Meta AI |

---

## 🔗 课程关联

| 历史节点 | 技术 | Lab 5 代码位置 |
|---------|------|--------------|
| LeNet-5 (1998) | [Conv→Pool]×N 结构 | `SimpleCNN.__init__` 的 3 个 conv+pool |
| AlexNet (2012) | ReLU 激活 | `F.relu(self.conv1(x))` |
| AlexNet (2012) | Dropout | `self.dropout = nn.Dropout(0.5)` |
| AlexNet (2012) | GPU 训练 | `DEVICE = torch.device("cuda" ...)` |
| VGGNet (2014) | 3×3 卷积 + same padding | `kernel_size=3, padding=1` |
| AlexNet (2012) | Adam（后续改进 SGD）| `optim.Adam(model.parameters(), lr=1e-3)` |
