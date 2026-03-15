---
topic: optimizers
dimension: history
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📖 Paper: Robbins & Monro, 'A Stochastic Approximation Method', Annals of Mathematical Statistics, 1951"
  - "📖 Paper: Polyak, 'Some methods of speeding up the convergence', USSR Computational Mathematics, 1964"
  - "📖 Paper: Duchi et al., 'Adaptive Subgradient Methods', JMLR 2011"
  - "📖 Paper: Kingma & Ba, 'Adam', ICLR 2015 — https://arxiv.org/abs/1412.6980"
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: never
status: current
---

# Optimizers 的故事线：从梯度下降到 Adam

> **核心主题：** 优化器的进化，是一场"让训练更快、更稳、更省心"的不断升级战
> **故事线：** 每一代优化器都在修复前一代的核心缺陷

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括

> 如何自动找到让误差最小的模型参数——当参数有百万个时？

1847 年，柯西（Cauchy）提出了梯度下降法的基本思想：沿函数梯度的反方向走一步，函数值就会减小。但在深度学习时代，这个"简单"的想法面临三个巨大挑战：数据量太大、参数空间太复杂、收敛太慢。

> 🔑 **问题提出：** 全量梯度下降每步需要遍历全部数据，在大数据集上不可行 → 需要"随机化"。

---

## 📚 第一章：随机梯度下降的诞生（1951-1986）

> **关键人物：** Robbins, Monro
> **关键论文：** Robbins & Monro, "A Stochastic Approximation Method", 1951

### 发生了什么？

1951 年，Robbins 和 Monro 提出了随机逼近方法：不需要全部数据来计算精确梯度，只需用**一个样本（或一小批）** 来估计梯度，虽然有噪声，但在期望值上仍指向正确方向。这就是 SGD 的数学基础。

1986 年 Rumelhart 等人将 SGD + 反向传播结合，用于训练多层神经网络。SGD 成为神经网络训练的标准方法。

### 为什么这很重要？

SGD 将计算量从 O(N)（全部数据）降到 O(1)（一个 mini-batch），使大规模训练成为可能。今天所有深度学习优化器都是 SGD 的变体。

### 但还有一个问题……

SGD 在"窄长谷"损失地表上震荡严重：在陡峭方向来回晃，在平坦方向蠕动。收敛路径像"醉汉走路"——方向大致对，但走了太多冤枉路。

> 🔑 **故事转折点：** SGD 解决了"大数据上能训练"的问题，但在复杂损失地表上的震荡和慢收敛成为新瓶颈。

---

## 📚 第二章：动量的引入（1964-1999）

> **关键人物：** Polyak; Nesterov
> **关键论文：** Polyak, "Some methods of speeding up the convergence", 1964

### 发生了什么？

1964 年，Polyak 提出了动量（Momentum）方法：累积历史梯度作为"速度"，让优化过程拥有惯性。在一致的梯度方向上加速，在震荡方向上自动抑制。

1983 年，Nesterov 提出了改进版：先用动量"预测"下一步位置，再在预测位置计算梯度（"先看路再走"）。Nesterov 加速梯度被证明在凸优化中有最优收敛速率。

### 为什么这很重要？

Momentum 将 SGD 从"醉汉走路"变成了"轮滑运动员"——在平坦的走廊上加速滑行，拐弯时平滑减速。实际训练中通常加速 2-10 倍。

### 但还有一个问题……

Momentum 仍然对所有参数使用同一个学习率。但在实际模型中，不同参数的最优学习率可能差几个数量级——频繁更新的参数需要小学习率，稀疏参数需要大学习率。

> 🔑 **故事转折点：** Momentum 解决了震荡问题，但"一刀切"的全局学习率限制了在异构参数空间中的表现。

---

## 📚 第三章：自适应学习率（2011-2012）

> **关键人物：** Duchi, Hazan, Singer; Tieleman, Hinton
> **关键论文：** Duchi et al., "Adaptive Subgradient Methods", JMLR 2011

### 发生了什么？

2011 年，Duchi 等人提出 **AdaGrad**：为每个参数维护历史梯度的平方和，用它来缩放学习率。更新频繁的参数（梯度累积大）学习率自动减小；稀疏参数保持较大学习率。

2012 年，Hinton 在 Coursera 课程中提出 **RMSprop**（没有论文！）：用指数加权移动平均代替 AdaGrad 的简单累加，解决了 AdaGrad "学习率不断缩小到零"的致命缺陷。

### 为什么这很重要？

AdaGrad/RMSprop 开创了"每参数自适应学习率"的范式。不再需要手动为不同层设置不同学习率。在 NLP（词嵌入稀疏更新）和 RNN 训练中效果显著。

### 但还有一个问题……

AdaGrad/RMSprop 有自适应学习率但没有动量。需要把 Momentum 和自适应学习率结合起来。

> 🔑 **故事转折点：** 自适应学习率是大突破，但缺少动量的加速效果——能否两者兼得？

---

## 📚 第四章：Adam 统一一切（2015-至今）

> **关键人物：** Kingma, Ba
> **关键论文：** Kingma & Ba, "Adam: A Method for Stochastic Optimization", ICLR 2015

### 发生了什么？

2015 年，Kingma 和 Ba 提出了 **Adam**（Adaptive Moment Estimation）：将 Momentum（一阶矩/均值）和 RMSprop（二阶矩/方差）结合，再加上偏差修正。Adam 几乎不需要调超参数——默认的 $\beta_1=0.9, \beta_2=0.999, \eta=0.001$ 在绝大多数任务上都表现良好。

Adam 迅速成为深度学习的默认优化器。截至 2026 年，其论文被引用超过 20 万次，是深度学习领域引用量最高的论文之一。

后续改进包括：
- **AdamW (2019)**：Loshchilov & Hutter 提出解耦权重衰减，成为 Transformer 训练标准
- **NAdam**：结合 Nesterov Momentum 和 Adam

### 为什么这很重要？

Adam 极大降低了深度学习的上手门槛——"不知道用什么 optimizer 就用 Adam"成为社区共识。它让研究者和工程师可以专注于模型设计，而不是花时间调优化器超参数。

### 但还有一个问题……

研究发现 Adam 在某些情况下的泛化能力不如 SGD+Momentum。这引发了"Adam vs SGD"的长期争论。目前的共识是：快速原型用 Adam，追求最佳 CV 性能用 SGD+精细调度。

> 🔑 **故事转折点：** Adam 几乎成为"终极"优化器，但泛化问题提醒我们：没有免费的午餐。

---

## 🗺️ 全局回顾：技术演进路线图

```
1847: Cauchy                    梯度下降 (Gradient Descent)
      │                         (全量数据，每步 O(N))
      ▼
1951: Robbins & Monro           随机梯度下降 (SGD)
      │                         (mini-batch, 每步 O(B))
      ▼
1964: Polyak                    Momentum SGD
      │                         (加惯性，抑制震荡)
      ▼
1983: Nesterov                  Nesterov Accelerated Gradient
      │                         (先看路再走，理论最优)
      │
      ╳  需要"每参数"独立学习率
      │
      ▼
2011: Duchi et al.              AdaGrad
      │                         (自适应学习率，但单调衰减)
      ▼
2012: Hinton (no paper!)        RMSprop
      │                         (修复 AdaGrad 衰减问题)
      │
      ╳  需要同时拥有动量 + 自适应 lr
      │
      ▼
2015: Kingma & Ba               Adam
      │                         (Momentum + RMSprop + 偏差修正)
      ▼
2019: Loshchilov & Hutter       AdamW
                                (解耦权重衰减，Transformer 标配)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|---------|-------------------|
| GD → SGD | 全量计算太慢 → mini-batch 加速 |
| SGD → Momentum | 震荡太大 → 惯性累积平滑路径 |
| Momentum → AdaGrad | 全局学习率 → 每参数自适应 |
| AdaGrad → RMSprop | 学习率衰减到零 → 滑动窗口修复 |
| RMSprop → Adam | 缺少动量 → 动量+自适应+偏差修正 |
| Adam → AdamW | 权重衰减与 L2 耦合 → 解耦 |
