---
topic: optimizers
dimension: concepts
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Murphy, 'PML1' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📖 Paper: Kingma & Ba, 'Adam: A Method for Stochastic Optimization', ICLR 2015"
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
  - "📖 Docs: scikit-learn MLPClassifier — https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html"
expiry: 12m
status: current
---

# Optimizers 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📖 Paper: Kingma & Ba, "Adam", ICLR 2015

---


## 术语定义

### 优化器 (Optimizer)

用于在训练过程中根据损失函数的梯度来更新模型权重的算法。每一步训练包括：前向传播→计算损失→反向传播得到梯度→**优化器用梯度更新权重**。优化器决定了"往哪个方向走"和"走多大步"。在 Keras 中通过 `model.compile(optimizer=...)` 指定，在 scikit-learn 中通过 `solver` 参数指定。

> 易混淆：**优化器 vs 损失函数** — 损失函数定义"目标是什么"（衡量预测与真实值的差距），优化器定义"怎么达到目标"（用什么策略更新权重）。两者在 compile 中分别指定。

### 学习率 (Learning Rate, $\eta$ 或 lr)

控制每次权重更新的步长大小。$W \leftarrow W - \eta \cdot \nabla L$。学习率太大→权重在最优点附近震荡、甚至发散；太小→收敛极慢、容易卡在局部最优。它是神经网络训练中**最重要的超参数**，没有之一。

> 易混淆：**学习率 vs 学习率调度** — 学习率是初始步长值（如 0.001）；学习率调度是训练过程中动态调整学习率的策略（如每 10 epoch 衰减一半）。

### SGD (Stochastic Gradient Descent, 随机梯度下降)

最基础的优化器：每次用一小批数据（mini-batch）计算梯度，然后沿梯度反方向更新权重。"随机"指的是每次只用部分数据（而非全部数据）来估计梯度，引入了噪声但大大加速了计算。

> 易混淆：**SGD vs GD vs Mini-batch GD** — GD（批量梯度下降）每次用全部数据，计算慢但梯度准确；SGD 每次用 1 个样本，噪声大；实践中的"SGD"通常是 Mini-batch GD（每次用一批，如 32/64/128 个样本）。

### Momentum (动量)

在 SGD 基础上加入"惯性"：不仅考虑当前梯度，还累积之前梯度的方向。像一个在山坡上滚动的球——即使当前梯度很小，之前积累的速度也会推着球继续前进。参数 $\beta$（通常 0.9）控制动量的衰减。

> 易混淆：**Momentum vs Nesterov Momentum** — 标准 Momentum 先计算梯度再加动量；Nesterov 先用动量"预测"下一步位置，再在那个位置计算梯度，相当于"先看路再走"，通常收敛更快。

### AdaGrad (Adaptive Gradient)

为每个参数维护独立的学习率：更新频繁的参数学习率自动减小，更新稀疏的参数学习率保持较大。适合稀疏数据（如 NLP 中的词向量）。但问题是学习率会单调递减，最终变得太小而停止学习。

### RMSprop (Root Mean Square Propagation)

AdaGrad 的改进：用指数加权移动平均代替 AdaGrad 对历史梯度的简单求和，解决了学习率"单调缩减到零"的问题。由 Hinton 在 Coursera 课程中提出（没有正式论文），但被广泛使用。

> 易混淆：**RMSprop vs AdaGrad** — AdaGrad 累积所有历史梯度的平方（单调增长→学习率单调减小）；RMSprop 用指数衰减的移动平均（保持"窗口"→学习率不会消失）。

### Adam (Adaptive Moment Estimation, 自适应矩估计)

当前最流行的优化器，结合了 **Momentum**（一阶矩/均值估计）和 **RMSprop**（二阶矩/方差估计）的优点。对每个参数自适应调整学习率，且包含偏差修正。默认超参数 $\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}$ 在大多数情况下无需调整。

> 易混淆：**Adam vs AdamW** — Adam 的权重衰减实现与 L2 正则化耦合在一起；AdamW 将权重衰减解耦（decoupled weight decay），在 Transformer 训练中效果更好。

### L-BFGS (Limited-memory Broyden-Fletcher-Goldfarb-Shanno)

一种近似二阶优化方法（拟牛顿法），利用曲率信息（Hessian 的近似）来加速收敛。不需要手动设置学习率。适合小规模、参数量不大的问题。在 scikit-learn 的 MLPClassifier 中可用（`solver='lbfgs'`）。

> 易混淆：**L-BFGS vs SGD/Adam** — L-BFGS 是二阶方法（用曲率信息），收敛快但内存大、不适合大数据；SGD/Adam 是一阶方法（只用梯度），内存小、适合大规模训练。

### Batch Size (批量大小)

每次梯度更新使用的样本数。和优化器紧密相关：batch_size=1 是纯 SGD（噪声最大）；batch_size=全部数据 是批量 GD（最稳定但最慢）；常用 32/64/128/256。batch size 越大，梯度估计越准确但泛化可能变差。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📖 Paper: Kingma & Ba, ICLR 2015
> 📖 Docs: [Keras Optimizers](https://keras.io/api/optimizers/)

---


## 概念辨析

### SGD vs Momentum vs Adam（三代优化器）

| 维度 | SGD | Momentum SGD | Adam |
|------|-----|-------------|------|
| **更新规则** | $W - \eta \nabla L$ | 加入历史动量 | 动量 + 自适应学习率 |
| **学习率** | 全局固定 | 全局固定 | 每参数自适应 |
| **超参数数量** | 1 ($\eta$) | 2 ($\eta, \beta$) | 3 ($\eta, \beta_1, \beta_2$) |
| **对超参数敏感度** | 高（严重依赖 lr） | 中等 | 低（默认值通常就行） |
| **收敛速度** | 慢 | 中等 | 快 |
| **内存开销** | 0 额外 | 1× 参数量 | 2× 参数量 |
| **推荐场景** | 调参精细/研究 | CV 大规模训练 | 通用默认选择 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### scikit-learn solver vs Keras optimizer

| scikit-learn solver | 等价 Keras optimizer | 适用场景 |
|-------------------|---------------------|---------|
| `'sgd'` | `keras.optimizers.SGD()` | 需要精细调参、研究用途 |
| `'adam'` | `keras.optimizers.Adam()` | 通用默认（推荐） |
| `'lbfgs'` | 无直接等价 | 小数据集、参数量少 |
| — | `keras.optimizers.RMSprop()` | RNN/LSTM 训练 |
| — | `keras.optimizers.AdaGrad()` | 稀疏数据（NLP） |

> 📖 Docs: [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
> 📖 Docs: [Keras Optimizers](https://keras.io/api/optimizers/)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                     Optimizers 体系                            │
├──────────────────────────────────────────────────────────────┤
│  一阶方法 (First-Order: 只用梯度)                              │
│  ├─ 固定学习率                                                │
│  │  ├─ SGD (Vanilla)         W ← W - η∇L                    │
│  │  ├─ Momentum SGD          加入速度 v 累积                  │
│  │  └─ Nesterov Momentum     先预测再计算梯度                  │
│  ├─ 自适应学习率                                               │
│  │  ├─ AdaGrad               按历史梯度平方和缩放              │
│  │  ├─ RMSprop               指数加权移动平均修正              │
│  │  ├─ Adam                  Momentum + RMSprop               │
│  │  ├─ AdamW                 Adam + 解耦权重衰减              │
│  │  └─ NAdam                 Nesterov + Adam                  │
├──────────────────────────────────────────────────────────────┤
│  二阶方法 (Second-Order: 用曲率)                               │
│  ├─ Newton's Method          需要完整 Hessian（不实用）        │
│  └─ L-BFGS                   近似 Hessian（小模型可用）        │
└──────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### 适用场景 ✅

- **Adam**：通用默认选择，NLP、CV、推荐系统大多数任务
- **SGD + Momentum**：CV 大规模训练（ImageNet），配合学习率调度可达最佳泛化
- **AdamW**：Transformer 训练（BERT、GPT），解耦的权重衰减更适合
- **RMSprop**：RNN/LSTM 训练的传统选择
- **L-BFGS**：小数据集、传统 ML 风格的 MLP（scikit-learn）
- **AdaGrad**：稀疏特征（NLP 词向量、推荐系统 embedding）

### 不适用场景 ❌

- **SGD（无动量）用于深层网络**：收敛极慢，容易卡在鞍点
- **L-BFGS 用于大数据集**：内存需求随参数量线性增长，不适合百万参数以上的模型
- **AdaGrad 用于长训练**：学习率单调减小，后期停止学习
- **Adam 用于追求最佳泛化的 CV 研究**：在某些情况下 SGD + 精细调参的泛化更好

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---


## 速查表

| 优化器 | 更新核心 | 默认 lr | 额外内存 | 推荐场景 |
|--------|---------|---------|---------|---------|
| SGD | $W - \eta \nabla L$ | 0.01 | 0 | 研究/精细调参 |
| Momentum | $v = \beta v + \nabla L$; $W - \eta v$ | 0.01 | 1× | CV 大规模训练 |
| AdaGrad | $W - \frac{\eta}{\sqrt{G+\epsilon}} \nabla L$ | 0.01 | 1× | 稀疏数据/NLP |
| RMSprop | 指数加权移动平均修正 AdaGrad | 0.001 | 1× | RNN/LSTM |
| Adam | Momentum($m$) + RMSprop($v$) + 偏差修正 | 0.001 | 2× | **通用默认** |
| AdamW | Adam + decoupled weight decay | 0.001 | 2× | Transformer |
| L-BFGS | 近似 Hessian 拟牛顿法 | 自动 | large | 小模型/sklearn |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📖 Paper: Kingma & Ba, ICLR 2015
