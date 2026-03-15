---
topic: loss_functions
dimension: history
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Paper: Gauss, 'Theoria Motus', 1809 — 最小二乘法"
  - "📖 Paper: Shannon, 'A Mathematical Theory of Communication', Bell System Technical Journal, 1948"
  - "📖 Paper: Kullback & Leibler, 'On Information and Sufficiency', Annals of Mathematical Statistics, 1951"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Lin et al., 'Focal Loss for Dense Object Detection', ICCV 2017"
expiry: never
status: current
---

# Loss Functions 的故事线：从最小二乘到交叉熵

> **核心主题：** 损失函数的进化，是一场"为神经网络选择最佳优化目标"的不断深化
> **故事线：** 每一代损失函数都在修复前一代在特定任务上的缺陷

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 如何用一个数字来衡量"预测有多差"——让机器知道该往哪个方向改进？

模型训练的本质是最优化：找到让某个"坏度指标"最小的参数。这个指标就是损失函数。但不同的指标定义了不同的"坏"，导致模型走向完全不同的解。选对损失函数 = 定义了正确的学习目标。

> 🔑 **问题提出：** 需要一个可微的标量函数来量化预测误差，且它的梯度必须能有效指导权重更新。

---

## 📚 第一章：最小二乘法的统治（1809-1980s）

> **关键人物：** Gauss, Legendre
> **关键论文：** Gauss, "Theoria Motus Corporum Coelestium", 1809

### 发生了什么？

1805-1809 年，Legendre 和 Gauss 独立发明了最小二乘法（Least Squares），最初用于天文学轨道计算。核心思想极其简单：$\text{minimize } \sum(y_i - \hat{y}_i)^2$。

Gauss 证明了当观测噪声服从高斯分布时，最小二乘估计等价于最大似然估计。这个优美的统计学基础使 MSE 成为回归任务的黄金标准，统治了近 200 年。

当神经网络在 1980s 复兴时，MSE 自然成为了所有任务（包括分类）的默认损失函数。

### 为什么这很重要？

MSE 建立了"损失函数 = 统计推断"的范式：选择损失函数等价于对数据的概率假设。这个洞见至今仍是深度学习损失函数设计的核心。

### 但还有一个问题……

当 MSE 被用于**分类任务**时，问题出现了：Sigmoid 输出层 + MSE 的梯度包含 $\sigma'(z)$ 项，在饱和区梯度消失。模型越"自信地"犯错，纠正能力越差。

> 🔑 **故事转折点：** MSE 是回归之王，但在分类任务中因 Sigmoid 饱和导致梯度消失——需要为分类任务量身定制的损失函数。

---

## 📚 第二章：信息论与交叉熵（1948-2000s）

> **关键人物：** Shannon; Kullback, Leibler
> **关键论文：** Shannon, "A Mathematical Theory of Communication", 1948

### 发生了什么？

1948 年，Shannon 发表了信息论奠基论文，定义了熵 $H(p) = -\sum p(x)\log p(x)$ 作为不确定性的度量。1951 年，Kullback 和 Leibler 定义了 KL 散度 $D_{KL}(p\|q)$ 来衡量两个分布之间的"距离"。

交叉熵 $H(p,q) = H(p) + D_{KL}(p\|q)$ 自然成为了"用模型分布 $q$ 逼近真实分布 $p$"的损失函数。而深度学习中的一个关键发现是：

$$\text{BCE + Sigmoid 的梯度} = \hat{y} - y \quad \text{（Sigmoid 导数被完美消除！）}$$

这个数学巧合（实际是 MLE 的必然结果）彻底解决了 MSE 在分类中的梯度消失问题。交叉熵迅速取代 MSE 成为分类任务的标准。

### 为什么这很重要？

交叉熵与 Sigmoid/Softmax 的配对是深度学习中最优美的数学设计之一。它不仅有信息论的理论支撑，还在工程上完美解决了梯度问题。

### 但还有一个问题……

标准交叉熵平等对待所有样本。当数据严重不平衡时（如 99% 负样本），模型只需"全猜负类"就能获得很低的 loss。

> 🔑 **故事转折点：** 交叉熵解决了分类的梯度问题，但对类别不平衡无能为力——需要自适应调整每个样本的权重。

---

## 📚 第三章：应对现实挑战（2017-至今）

> **关键人物：** Lin, Goyal, Girshick, He (Facebook AI)
> **关键论文：** Lin et al., "Focal Loss for Dense Object Detection", ICCV 2017

### 发生了什么？

2017 年，Lin 等人在目标检测（RetinaNet）中发现：海量的"简单负样本"（背景区域）主导了 loss，使模型无法专注于难分的正样本。他们提出了 **Focal Loss**：

$$L_{\text{focal}} = -\alpha(1-\hat{y})^\gamma \log(\hat{y})$$

$(1-\hat{y})^\gamma$ 是调制因子：当模型已经很"确定"时（$\hat{y}$ 接近 1），调制因子 → 0，该样本的 loss 贡献被抑制。模型的注意力自动集中在难分样本上。

同时期还出现了：
- **Label Smoothing (2015)**：将 hard label [0,0,1,0] 变为 soft label [0.025,0.025,0.925,0.025]，防止模型过度自信
- **Contrastive Loss, Triplet Loss (2015+)**：用于度量学习（人脸识别），不直接预测类别而是学习相似度

### 为什么这很重要？

Focal Loss 展示了损失函数不只是"正确答案 vs 预测"的度量，还可以是"难度自适应的学习策略"。它启发了一系列任务特定的损失设计。

> 🔑 **故事转折点：** 损失函数从"被动度量"进化为"主动学习策略"——告诉模型"该重点学什么"。

---

## 🗺️ 全局回顾：技术演进路线图

```
1809: Gauss                     最小二乘法 (MSE)
      │                         (回归之王，200 年标准)
      ▼
1948: Shannon                   信息论 / 熵
      │
1951: Kullback & Leibler        KL 散度
      │                         │
      ▼                         ▼
1986: Rumelhart et al.          交叉熵 (Cross-Entropy)
      │                         (消除 Sigmoid 饱和梯度问题)
      ▼
1990s-2000s: 深度学习社区        CE 成为分类标准
      │
      ╳  类别不平衡 / 任务特定需求
      │
      ▼
2015: Szegedy et al.            Label Smoothing
      │
2017: Lin et al.                Focal Loss
      │                         (难度自适应权重)
      ▼
2018+: 各领域                    任务特定损失函数爆发
                                (Contrastive, Triplet, DICE, ...)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| MSE → Cross-Entropy | 分类中 Sigmoid 饱和梯度消失 |
| CE → Focal Loss | 类别不平衡中简单样本主导 loss |
| CE → Label Smoothing | 模型过度自信 → soft label 正则化 |
| CE → Contrastive/Triplet | 不知道类别只知道"相似/不相似" |
