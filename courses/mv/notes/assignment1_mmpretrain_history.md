# 🕰️ Assignment 1 技术演进历史线：从手写规则到 MobileNet V2

> **课程:** CST8508 Machine Vision | **主题:** 图像分类技术演进  
> **时间跨度:** 1998 — 2018  
> **核心脉络:** 手工特征 → 浅层CNN → 深层CNN → 超深残差网络 → 轻量高效网络

---

## 📍 全景时间线（Timeline Overview）

```
1998        2012         2014         2015          2017        2018
 │           │            │            │             │           │
 ▼           ▼            ▼            ▼             ▼           ▼
LeNet     AlexNet      VGGNet      ResNet        MobileNet   MobileNet
 │           │            │          V1 ⭐          V1          V2 ⭐
 │           │            │            │             │           │
手写数字    GPU+大数据    "更深=更好"  残差连接      深度可分离   倒残差
 识别       → 打败传统     的验证      解决退化       卷积        结构
             方法                     问题         为手机而生

                    同时：优化器演进
1951        1986         2011         2012         2014
SGD       Momentum    AdaGrad      RMSProp      Adam ⭐
 │           │            │            │           │
固定步长    加惯性      自适应步长   修复学习率   集大成者
                                    衰减问题
```

---

## 第 1 站：LeNet-5 (1998) — CNN 的开山之作

### 🧩 之前的问题

1990 年代的图像识别主要靠**手工设计的特征**（如边缘检测 + 模板匹配）。对于手写数字识别，研究者们需要手动设计"什么样的笔画对应什么数字"——规则多、脆弱、不泛化。

### 💡 核心创新

Yann LeCun 提出用**卷积神经网络（Convolutional Neural Network, CNN）**自动从像素学习特征：

- **卷积层：** 用可学习的滤波器代替手工特征
- **池化层：** 降低分辨率，获得位移不变性
- **端到端训练：** 输入原始像素，输出分类结果，中间特征自动学习

```
LeNet-5 架构：
  Input (32×32) → Conv → Pool → Conv → Pool → FC → FC → Output (10 类)

  参数量：约 60K（今天看来非常小）
```

### 👤 关键人物

| 人物           | 机构                 | 贡献                             |
| -------------- | -------------------- | -------------------------------- |
| **Yann LeCun** | AT&T Bell Labs / NYU | CNN 之父，设计了 LeNet           |
| Léon Bottou    | AT&T Bell Labs       | 参与 LeNet 训练，后推动 SGD 理论 |

论文：_Gradient-Based Learning Applied to Document Recognition_ (1998)

### 📊 里程碑数据

- 手写数字识别错误率：**0.8%**（在 MNIST 上）
- 被美国银行采用于支票数字识别（工业落地）

### ⚠️ 遗留问题

- 只能处理 32×32 的小灰度图像
- 计算资源有限 → 网络只有 5 层
- 对于复杂自然图像（猫、花、车）完全无力

### 🔗 与本课程的关联

- LeNet 的架构（Conv → Pool → FC）就是 Week 4 slides 讲的 **CNN 基本结构**
- Assignment 1 用的 ResNet-18 和 MobileNet V2 都是这个基本结构的演化

---

## 第 2 站：AlexNet (2012) — GPU + 大数据 = 深度学习爆发

### 🧩 之前的问题

LeNet 之后的 14 年，CNN 并未流行。主流方法是 **SIFT/HOG 特征 + SVM 分类器**（Week 3 内容）。原因：

1. 没有足够大的标注数据集
2. 没有足够强的计算硬件
3. 学术界认为"神经网络是过时的方法"

### 💡 核心创新

Alex Krizhevsky（在 Geoffrey Hinton 指导下）用 **两块 GTX 580 GPU** 训练了一个 8 层 CNN，在 ImageNet 竞赛上碾压传统方法：

- **GPU 加速训练：** 将原本需要数周的训练缩短到几天
- **ReLU 激活函数：** 替换 Sigmoid/Tanh，解决梯度消失，加速训练 6 倍
- **Dropout 正则化：** 随机丢弃神经元，防止过拟合
- **大数据（ImageNet）：** 120 万张标注图片，1000 类

### 👤 关键人物

| 人物                | 机构                  | 贡献                                   |
| ------------------- | --------------------- | -------------------------------------- |
| **Alex Krizhevsky** | University of Toronto | AlexNet 主要实现者                     |
| **Geoffrey Hinton** | University of Toronto | 深度学习教父，导师                     |
| Ilya Sutskever      | University of Toronto | 参与训练（后来成为 OpenAI 联合创始人） |

论文：_ImageNet Classification with Deep Convolutional Neural Networks_ (NeurIPS 2012)

### 📊 里程碑数据

- ImageNet Top-5 错误率：**15.3%**（第二名 26.2%，使用传统特征）
- 差距 10.9 个百分点——这不是改进，是**碾压**
- 这一天标志着深度学习时代的开始

### ⚠️ 遗留问题

- 8 层网络效果好 → 那更深的网络是不是更好？
- 架构设计主要靠直觉 → 有没有系统的方法？

### 🔗 与本课程的关联

- AlexNet 使用的 **ReLU 激活函数**在 Week 4 slides 中详细讲解
- Assignment 1 的配置中 `data_preprocessor` 使用的 **ImageNet 均值和标准差** `mean=[123.675, 116.28, 103.53]` 就来自这个数据集

---

## 第 3 站：VGGNet (2014) — "更深 = 更好"的验证

### 🧩 之前的问题

AlexNet 证明了 8 层 CNN 可以work，但**最佳深度是多少？** 更深是不是一定更好？

### 💡 核心创新

Karen Simonyan 和 Andrew Zisserman 用非常简洁的设计哲学做了系统实验：

- **只用 3×3 卷积核**（最小的能捕捉空间特征的尺寸）
- **每过一次 pooling，通道数翻倍**（64 → 128 → 256 → 512）
- 系统地测试了 11、13、16、19 层的效果

```
VGG-16 架构：
  Input → [Conv3×3]×2 → Pool
        → [Conv3×3]×2 → Pool
        → [Conv3×3]×3 → Pool
        → [Conv3×3]×3 → Pool
        → [Conv3×3]×3 → Pool
        → FC → FC → FC → Output

  简洁、规律、优雅
```

### 👤 关键人物

| 人物                 | 机构       | 贡献                 |
| -------------------- | ---------- | -------------------- |
| **Karen Simonyan**   | Oxford VGG | VGGNet 主要设计者    |
| **Andrew Zisserman** | Oxford VGG | 导师，计算机视觉大牛 |

论文：_Very Deep Convolutional Networks for Large-Scale Image Recognition_ (ICLR 2015)

> 📝 **命名来源：** VGG = **V**isual **G**eometry **G**roup（牛津大学视觉几何组）。巧的是，Assignment 1 的数据集 Oxford Flowers 17 也来自这个组！

### 📊 里程碑数据

- ImageNet Top-5 错误率：**7.3%**（VGG-16）
- 验证了"更深确实更好"——从 8 层（AlexNet）到 16-19 层

### ⚠️ 遗留问题

- 参数量巨大：VGG-16 有 **1.38 亿参数**（主要在 FC 层）
- 更关键的发现：20 层以上的网络**性能反而下降**！

```
实验数据（训练误差）：
  20 层网络：训练误差 4.2%
  56 层网络：训练误差 6.7%  ← 更深反而更差！

这不符合直觉 —— 更多参数理论上应该能拟合得更好
这个现象叫做"退化问题"（Degradation Problem）
```

### 🔗 与本课程的关联

- VGG 出品的 **Oxford Flowers 17** 就是 Assignment 1 使用的数据集
- VGG 的"3×3 卷积堆叠"设计理念贯穿了后续所有主流 CNN 架构

---

## 第 4 站：ResNet (2015) ⭐ — 残差连接解决退化问题

### 🧩 之前的问题

VGGNet 发现了 **退化问题（Degradation Problem）**：更深的网络收敛到更差的训练误差。这不是过拟合（过拟合是训练误差低但测试误差高），而是**连训练都训练不好**。

### 💡 核心创新

何恺明（Kaiming He）提出了优雅而深刻的解决方案——**残差学习（Residual Learning）**：

```
传统方法：让网络学习 H(x)（完整映射）
  x → [Conv → BN → ReLU → Conv → BN] → H(x)

残差方法：让网络学习 F(x) = H(x) - x（偏差/残差）
  x → [Conv → BN → ReLU → Conv → BN] → F(x) + x → H(x)
                                              ↗
                                     Skip Connection（捷径）
```

**直觉：** 如果增加的层不需要学什么，它只要学 F(x) = 0 就行（输出等于输入）。学"什么都不做"（F=0）比学"复制输入"（H=x）容易得多。

### 👤 关键人物

| 人物                     | 机构                    | 贡献              |
| ------------------------ | ----------------------- | ----------------- |
| **何恺明（Kaiming He）** | Microsoft Research Asia | ResNet 主要发明者 |
| 张祥雨                   | MSRA                    | 参与实验          |
| 任少卿                   | MSRA                    | 参与实验          |
| 孙剑                     | MSRA （后任旷视CTO）    | 导师              |

论文：_Deep Residual Learning for Image Recognition_ (CVPR 2016, **Best Paper**)

> 📝 **影响力：** ResNet 论文是深度学习领域**引用量最高**的论文之一（超过 20 万次引用），被认为是 CNN 发展史上最重要的突破。

### 📊 里程碑数据

| 模型          | 层数 | Top-5 错误率 | 参数量    |
| ------------- | ---- | ------------ | --------- |
| VGG-16        | 16   | 7.3%         | 138M      |
| **ResNet-18** | 18   | 10.9%        | **11.7M** |
| ResNet-50     | 50   | 5.25%        | 25.6M     |
| ResNet-152    | 152  | **3.57%**    | 60.2M     |

- 152 层的网络终于可以训练了！而且比 16 层的 VGG 更好！
- ResNet-18 参数量只有 VGG-16 的 **8.5%**

### ⚠️ 遗留问题

- 准确率更高了，但参数量和计算量仍然很大
- 在手机、嵌入式设备上无法实时运行
- 问题转向：能不能在**不损失太多准确率**的前提下**大幅减少计算量**？

### 🔗 与本课程的关联

- **Assignment 1 的第一个模型就是 ResNet-18**
- 配置文件中 `backbone=dict(type='ResNet', depth=18, num_stages=4)` 直接使用了这个架构
- ResNet-18 是 ResNet 家族中最小的（18 层），适合小数据集和快速实验

---

## 第 5 站：MobileNet V1/V2 (2017/2018) ⭐ — 为手机而生

### 🧩 之前的问题

ResNet 在服务器上跑得很好，但在手机/嵌入式设备上：

```
限制条件：
  - 内存：手机 GPU 通常只有 2-4 GB
  - 计算：手机 GPU 算力是服务器的 1/100
  - 延迟：用户期望实时响应（<100ms）
  - 功耗：不能让手机发烫、掉电快

ResNet-50 在手机上：
  - 推理时间 ~200ms → 太慢
  - 模型大小 ~100MB → 太大
  - 功耗高 → 不实用
```

### 💡 核心创新

**MobileNet V1 (2017)** — 深度可分离卷积（Depthwise Separable Convolution）：

```
标准卷积（ResNet 用的）：
  参数量 = K × K × C_in × C_out
  例：3×3 × 64 × 128 = 73,728

深度可分离卷积（MobileNet 用的）：
  = 深度卷积(K×K×1×C_in) + 逐点卷积(1×1×C_in×C_out)
  参数量 = K×K×C_in + C_in×C_out
  例：3×3×64 + 64×128 = 576 + 8,192 = 8,768

  节省比例：8,768 / 73,728 = 11.9%
  → 减少了 88% 的参数！
```

**MobileNet V2 (2018)** — 倒残差结构（Inverted Residual）：

```
ResNet 残差块（先压缩再展开）：
  256-dim → [1×1 Conv → 64-dim] → [3×3 Conv → 64-dim] → [1×1 Conv → 256-dim]
  宽 → 窄 → 宽（瓶颈结构）

MobileNet V2 倒残差块（先展开再压缩）：
  64-dim → [1×1 Conv → 384-dim] → [3×3 DW Conv → 384-dim] → [1×1 Conv → 64-dim]
  窄 → 宽 → 窄（倒瓶颈结构）

为什么"倒"着来？
  深度可分离卷积在低维空间信息损失大
  → 先用 1×1 卷积"膨胀"维度 → 在高维空间做卷积 → 再压缩回来
```

### 👤 关键人物

| 人物                 | 机构   | 贡献                    |
| -------------------- | ------ | ----------------------- |
| **Andrew G. Howard** | Google | MobileNet V1 主要设计者 |
| **Mark Sandler**     | Google | MobileNet V2 主要设计者 |
| Liang-Chieh Chen     | Google | 参与 V2 设计            |

论文：

- V1: _MobileNets: Efficient CNNs for Mobile Vision Applications_ (arXiv 2017)
- V2: _MobileNetV2: Inverted Residuals and Linear Bottlenecks_ (CVPR 2018)

### 📊 里程碑数据

| 模型             | 参数量   | Top-1 (ImageNet) | 推理时间 (Pixel 1) |
| ---------------- | -------- | ---------------- | ------------------ |
| ResNet-18        | 11.7M    | 69.8%            | ~100ms             |
| **MobileNet V2** | **3.4M** | **72.0%**        | **~75ms**          |
| VGG-16           | 138M     | 71.6%            | 不适合手机         |

MobileNet V2 用 **29% 的参数量**达到了**更高的 ImageNet 准确率**！

### ⚠️ 遗留问题

- 在某些任务上仍不如大模型（特别是需要细粒度特征的任务）
- 更新的方向：NAS（Neural Architecture Search）自动搜索最优架构 → EfficientNet (2019)

### 🔗 与本课程的关联

- **Assignment 1 的第二个模型就是 MobileNet V2**
- 配置文件中 `backbone=dict(type='MobileNetV2', widen_factor=1.0)` 使用了这个架构
- 在 Oxford Flowers 17 小数据集上，MobileNet V2 (90.07%) **大幅领先** ResNet-18 (77.21%)

---

## 📈 支线：优化器演进

### SGD (1951) → Momentum (1986) → Adam (2014)

```
SGD:       W = W - η × g              固定步长，所有参数一样
              ↓ 问题：容易震荡、收敛慢

Momentum:  v = μ × v + g
           W = W - η × v              加了惯性，跨越局部最优
              ↓ 问题：所有参数用同一个学习率

AdaGrad:   每个参数自适应学习率        解决了同一学习率的问题
 (2011)       ↓ 问题：学习率只减不增，后期停滞

RMSProp:   修复了 AdaGrad 的学习率
 (2012)    衰减问题
              ↓

Adam:      结合了 Momentum + RMSProp
 (2014)    = 动量 + 自适应学习率        集大成者 ⭐
```

| 优化器         | 发明者          | 年份      | Assignment 1 中       |
| -------------- | --------------- | --------- | --------------------- |
| SGD + Momentum | Polyak          | 1964/1986 | ResNet-18 使用        |
| **Adam**       | **Kingma & Ba** | **2014**  | **MobileNet V2 使用** |

> 📝 **命名来源：** Adam = **Ada**ptive **M**oment Estimation（自适应矩估计）

---

## 📊 对比总结表

| 技术             | 年份     | 核心创新                    | 解决的问题          | 参数量           | ImageNet Top-5    |
| ---------------- | -------- | --------------------------- | ------------------- | ---------------- | ----------------- |
| LeNet-5          | 1998     | CNN 基本架构                | 手工特征 → 自动学习 | 60K              | —                 |
| AlexNet          | 2012     | GPU + ReLU + Dropout        | 传统方法天花板      | 60M              | 15.3%             |
| VGGNet           | 2014     | 3×3 堆叠 + 系统实验         | 最佳深度探索        | 138M             | 7.3%              |
| **ResNet**       | **2015** | **残差连接**                | **退化问题**        | **11.7M** (R-18) | **3.57%** (R-152) |
| **MobileNet V2** | **2018** | **深度可分离卷积 + 倒残差** | **移动端部署**      | **3.4M**         | **5.6%**          |

---

## 🎯 考试相关

| #   | 可能的考点                       | 标准答案关键词                                         |
| --- | -------------------------------- | ------------------------------------------------------ |
| 1   | ResNet 的核心创新是什么？        | 残差连接 / Skip Connection / 学习 F(x) = H(x) - x      |
| 2   | 为什么需要 ResNet？              | VGGNet 发现的退化问题：更深的网络训练误差反而更高      |
| 3   | MobileNet 用什么技术减少计算量？ | 深度可分离卷积 = 深度卷积 + 逐点卷积                   |
| 4   | MobileNet V2 vs V1 的改进？      | 倒残差结构（Inverted Residual）：窄→宽→窄              |
| 5   | AlexNet 为什么是时代分水岭？     | GPU 训练 + ImageNet 大数据 + 碾压传统方法 10+ 个百分点 |
| 6   | VGG 的设计哲学？                 | 只用 3×3 卷积核，系统实验不同深度                      |
| 7   | Adam 的全称和核心思想？          | Adaptive Moment Estimation，结合动量和自适应学习率     |
