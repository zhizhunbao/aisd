---
topic: activation_functions
dimension: history
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Paper: McCulloch & Pitts, 'A logical calculus of the ideas immanent in nervous activity', Bulletin of Mathematical Biophysics 1943"
  - "📖 Paper: Rosenblatt, 'The perceptron', Psychological Review 1958"
  - "📖 Paper: Rumelhart et al., 'Learning representations by back-propagating errors', Nature 1986"
  - "📖 Paper: Nair & Hinton, 'Rectified Linear Units Improve Restricted Boltzmann Machines', ICML 2010"
  - "📖 Paper: Glorot & Bengio, 'Understanding the difficulty of training deep feedforward neural networks', AISTATS 2010"
  - "📖 Paper: Ramachandran et al., 'Searching for Activation Functions', arXiv 2017"
  - "📖 Paper: Hendrycks & Gimpel, 'Gaussian Error Linear Units (GELUs)', arXiv 2016"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: never
status: current
---

# Activation Functions 的故事线：从阶跃函数到 GELU

> **核心主题：** 神经网络激活函数的进化，是一场"让梯度顺畅流过更深网络"的不断升级战
> **故事线：** 每一代激活函数都是为了解决前一代的致命缺陷而生

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 如何让人工神经元模拟生物神经元的"全或无"响应——发不发放电信号？

1943 年，神经科学家 McCulloch 和数学家 Pitts 提出了第一个人工神经元模型。他们观察到生物神经元的行为：当输入信号的加权总和超过阈值时，神经元"发放"（输出 1）；否则"沉默"（输出 0）。这就是最原始的"激活函数"——一个阶跃函数。

但问题是：阶跃函数不可微分，你无法用梯度下降来训练网络。这个矛盾将驱动此后 80 年的激活函数进化史。

> 🔑 **问题提出：** 阶跃函数虽然模拟了生物神经元，但不可微 → 无法用梯度训练 → 需要"光滑"的替代品。

---

## 📚 第一章：Sigmoid 时代（1986-2006）

> **关键人物：** Rumelhart, Hinton, Williams
> **关键论文：** Rumelhart et al., "Learning representations by back-propagating errors", Nature 1986

### 发生了什么？

1986 年，Rumelhart 等人重新发明了反向传播算法，并在 Nature 上发表了那篇改变深度学习历史的论文。他们需要一个**可微分**的激活函数来替代阶跃函数，选择了 Sigmoid：

$$\sigma(z) = \frac{1}{1+e^{-z}}$$

Sigmoid 完美符合需求：光滑可微、输出在 (0,1) 可解释为概率、形状类似阶跃函数但处处有梯度。在接下来的 20 年里，Sigmoid（和后来的 Tanh）统治了神经网络的隐藏层。

### 为什么这很重要？

Sigmoid 使得反向传播成为可能——网络终于可以"学习"了。它将神经网络从基于规则的符号 AI 竞争中带入了基于数据的学习范式。LeCun 的 LeNet（1998）和 Hinton 的 DBN（2006）都使用了 Sigmoid 或 Tanh。

### 但还有一个问题……

当网络超过 3-4 层时，训练变得极其困难。2006-2010 年，人们发现了"梯度消失"问题：Sigmoid 的梯度最大值只有 0.25，经过 $n$ 层后梯度缩小为 $0.25^n$。5 层 Sigmoid 网络的底层梯度仅为顶层的千分之一。深度学习被卡在了"浅层"。

> 🔑 **故事转折点：** Sigmoid 让反向传播成为现实，但 0.25 的最大梯度在深层网络中引发了灾难性的梯度消失——深度学习需要新的激活函数。

---

## 📚 第二章：ReLU 革命（2010-2012）

> **关键人物：** Nair, Hinton, Glorot, Bengio
> **关键论文：** Nair & Hinton, "Rectified Linear Units Improve Restricted Boltzmann Machines", ICML 2010

### 发生了什么？

2010 年，两篇关键论文几乎同时出现：

1. **Nair & Hinton (ICML 2010)** 发现在 RBM 中使用 ReLU 比 Sigmoid 效果更好
2. **Glorot & Bengio (AISTATS 2010)** 从理论上分析了为什么深层 Sigmoid 网络难以训练

ReLU 的公式极其简单：$\max(0, z)$。但这个简单的函数有三个革命性优势：
- 正区间梯度恒为 1 → 梯度不消失
- 计算只需比较和赋值 → 比 Sigmoid 快 6 倍
- 负区间输出 0 → 天然的稀疏性，类似生物神经元

2012 年，Krizhevsky 的 AlexNet 使用 ReLU 赢得了 ImageNet 竞赛，将深度学习推上了主流舞台。ReLU 是这场革命的关键技术之一。

### 为什么这很重要？

ReLU 打破了"深层网络无法训练"的魔咒。它证明了：最好的激活函数不是最复杂的，而是梯度最"通畅"的。从此，深度网络（10+层）成为可能，现代深度学习时代正式开启。

### 但还有一个问题……

ReLU 有一个致命缺陷："死神经元"问题。当一个神经元的输入持续为负时，ReLU 输出恒为 0，梯度也为 0，权重永远不再更新。在某些网络中，高达 40% 的 ReLU 神经元会"死亡"。

> 🔑 **故事转折点：** ReLU 解决了梯度消失，开启了深度学习革命，但"死神经元"成为新的隐患——需要让负区间也能传递信号。

---

## 📚 第三章：ReLU 变体涌现（2013-2016）

> **关键人物：** He, Clevert, Maas
> **关键论文：** He et al., "Delving Deep into Rectifiers", ICCV 2015; Clevert et al., "Fast and Accurate Deep Network Learning by ELU", ICLR 2016

### 发生了什么？

为了解决死神经元问题，研究者们提出了一系列 ReLU 变体：

- **Leaky ReLU (2013)**：Maas et al. 提出在负区间给一个小斜率 $\alpha=0.01$，让梯度不为零
- **PReLU (2015)**：He et al. 让负区间斜率 $\alpha$ 成为可学习参数，在 ImageNet 上首次超过人类准确率
- **ELU (2016)**：Clevert et al. 用指数函数 $\alpha(e^z-1)$ 代替负区间的线性，使输出均值更接近零

这些变体的共同思路：**保持 ReLU 正区间的优势（梯度=1），同时修复负区间的缺陷**。

### 为什么这很重要？

ReLU 变体展示了一个设计原则：好的激活函数不需要复杂，只需要在正区间保持线性（梯度通畅）、在负区间提供适度的信号（防止死亡）。同时，PReLU+He 初始化在 ImageNet 上超越人类，标志着深度学习的里程碑时刻。

### 但还有一个问题……

这些变体都是"手工设计"的——研究者凭直觉和实验来设计函数形状。有没有办法让机器自己搜索最优的激活函数？

> 🔑 **故事转折点：** 手工设计虽然有效，但搜索空间有限。能否让 AI 自己发现最好的激活函数？

---

## 📚 第四章：自动搜索与 Transformer 时代（2017-至今）

> **关键人物：** Ramachandran, Zoph (Google Brain); Hendrycks, Gimpel
> **关键论文：** Ramachandran et al., "Searching for Activation Functions", arXiv 2017; Hendrycks & Gimpel, "Gaussian Error Linear Units", arXiv 2016

### 发生了什么？

两个并行发展改变了激活函数的面貌：

1. **Swish (2017)**：Google Brain 团队用自动化搜索（NAS 思想）在组合空间中搜索最优激活函数，发现了 $\text{Swish}(z) = z \cdot \sigma(z)$。它在多个基准测试中超越了 ReLU，且具有光滑、非单调等优良性质。

2. **GELU (2016, 流行于 2018+)**：Hendrycks & Gimpel 从概率论角度设计了 $\text{GELU}(z) = z \cdot \Phi(z)$，可以看作"概率性地保留输入"。GELU 被 BERT、GPT 等 Transformer 架构采用为默认激活函数，稳定表现优于 ReLU。

### 为什么这很重要？

Swish 证明了 AI 可以发现人类未曾想到的激活函数。GELU 则展示了从概率论出发的设计思路。两者的成功标志着激活函数设计从"工程直觉"走向了"系统化搜索"和"理论驱动"。

### 但还有一个问题……

目前没有在所有任务上都最优的激活函数。ReLU 在 CNN 中仍然是最佳选择，GELU 在 Transformer 中表现最好。这暗示：最优的激活函数可能取决于网络架构和数据特性，未来可能走向"自适应激活函数"。

> 🔑 **故事转折点：** 激活函数的进化仍在继续。下一步可能是：每层甚至每个神经元自动选择最优激活函数。

---

## 🗺️ 全局回顾：技术演进路线图

```
1943: McCulloch & Pitts         阶跃函数 (Step Function)
      │                         (生物启发，不可微)
      ▼
1986: Rumelhart, Hinton et al.  Sigmoid σ(z)
      │                         (可微！反向传播成为可能)
      │
      ╳  20年的"浅层困境" —— 梯度消失限制了网络深度
      │
      ▼
2010: Nair & Hinton             ReLU max(0,z)
      │                         (梯度恒1，计算极快)
      ▼
2012: Krizhevsky (AlexNet)      ReLU + 深层 CNN
      │                         (ImageNet 革命)
      ▼
2013-2016: 多位研究者            Leaky ReLU / PReLU / ELU
      │                         (修复死神经元)
      ▼
2016-2017: Hendrycks; Google     GELU / Swish
      │                         (光滑+概率性/自动搜索)
      ▼
2018+: Vaswani, Devlin et al.   GELU 成为 Transformer 标配
                                (BERT, GPT 默认激活)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| 阶跃函数 → Sigmoid | 不可微 → 可微，使反向传播成为可能 |
| Sigmoid → ReLU | 梯度消失 → 正区间梯度恒1，深层网络可训练 |
| ReLU → Leaky ReLU/ELU | 死神经元 → 负区间保持梯度流通 |
| ReLU → Swish/GELU | 非光滑/手工设计 → 光滑/自动搜索/理论驱动 |
