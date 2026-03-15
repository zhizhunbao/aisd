---
topic: loss_functions
dimension: tutorial
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: Keras Losses — https://keras.io/api/losses/"
expiry: 12m
status: current
---

# Loss Functions 教程

> **前置知识：** 概率论（条件概率，MLE）| 信息论（熵）| 激活函数（Sigmoid, Softmax）
> **参考来源：** [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | [Keras Losses](https://keras.io/api/losses/)

---


## Section 0: 前置知识速查

1. **概率**：$P(y|x)$ — 给定输入 $x$，输出 $y$ 的概率
2. **MLE**：找参数 $\theta$ 使得 $\prod P(y_i|x_i; \theta)$ 最大，等价于最小化 $-\sum\log P(y_i|x_i;\theta)$
3. **Sigmoid**：$\sigma(z) = \frac{1}{1+e^{-z}}$，输出 $(0,1)$，可解释为概率
4. **Softmax**：$\text{softmax}(z_k) = \frac{e^{z_k}}{\sum e^{z_j}}$，输出概率分布

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **没有方向**：优化器需要一个标量值来计算梯度——没有损失函数，优化器不知道"往哪里走"
- 🔥 **无法量化好坏**：模型预测了一个值，但"好不好"需要一个客观标准来衡量
- 🔥 **错误的度量导致错误的学习**：分类任务用 MSE → Sigmoid 饱和梯度消失 → 模型学不动；用交叉熵则完美解决

### 它的核心价值

1. **定义优化目标**：损失函数告诉模型"什么是好的预测"（loss 越低越好）
2. **提供梯度信号**：反向传播从损失函数开始逐层计算梯度，驱动权重更新
3. **匹配概率假设**：MSE 对应高斯噪声，CE 对应 Bernoulli/Categorical 分布——选对 loss = 选对概率模型
4. **消除梯度问题**：交叉熵与 Sigmoid/Softmax 配对后，梯度简化为 $\hat{y}-y$，消除饱和

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 损失函数在训练中的位置

```
┌────────────────────────────────────────────────────────────────┐
│                    训练一步的数据流                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Input X ──→ Model(W) ──→ Prediction ŷ                       │
│                                        ↓                       │
│                              Loss L = loss(y, ŷ) ←── Label y  │
│                                        ↓                       │
│                              ∂L/∂ŷ (损失对预测的梯度)          │
│                                        ↓                       │
│                              反向传播 → ∂L/∂W                  │
│                                        ↓                       │
│                              Optimizer 更新 W                  │
│                                                                │
│  Keras: model.compile(loss='...') 告诉框架用什么 loss          │
│         model.fit() 自动执行上述循环                            │
└────────────────────────────────────────────────────────────────┘
```

> 📖 Docs: [Keras Model Training](https://keras.io/api/models/model_training_apis/)

### 2.2 为什么分类不能用 MSE？

**这是理解损失函数最关键的问题。**

假设二分类任务，Sigmoid 输出 $\hat{y} = \sigma(z)$：

**MSE 的梯度经过 Sigmoid：**
$$\frac{\partial L_{\text{MSE}}}{\partial z} = 2(\hat{y} - y) \cdot \underbrace{\hat{y}(1-\hat{y})}_{\text{Sigmoid 导数}}$$

当 $\hat{y} \approx 0$ 或 $\hat{y} \approx 1$ 时，$\hat{y}(1-\hat{y}) \approx 0$ → **梯度消失！**

模型明明"自信地"犯了错（$\hat{y}=0.99$ 但 $y=0$），却因为 Sigmoid 饱和而得到极小的梯度，**无法纠正错误。**

**BCE 的梯度经过 Sigmoid：**
$$\frac{\partial L_{\text{BCE}}}{\partial z} = \hat{y} - y$$

Sigmoid 的导数被**完美消除**！无论 $\hat{y}$ 多接近 0 或 1，梯度都是 $|\hat{y} - y|$，与误差大小成正比。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

### 2.3 损失函数与概率的关系

```
               概率假设                    推导结果
┌──────────────────────────┐    ┌──────────────────────────┐
│ y ~ N(ŷ, σ²)  (高斯)    │ ──→│ 最小化 MSE               │
│ y ~ Bernoulli(ŷ)        │ ──→│ 最小化 Binary CE         │
│ y ~ Categorical(ŷ)      │ ──→│ 最小化 Categorical CE    │
│ y ~ Laplace(ŷ, b)       │ ──→│ 最小化 MAE               │
└──────────────────────────┘    └──────────────────────────┘

通用规则: MLE(最大似然) = 最小化 负对数似然 = 最小化 交叉熵
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

### 2.4 compile 中 loss 参数的作用

```python
model.compile(
    loss='sparse_categorical_crossentropy',   # ← 损失函数
    optimizer='adam',                          # ← 优化器
    metrics=['accuracy']                       # ← 评估指标
)
```

- **loss** 决定"模型的学习目标"——优化器沿着这个函数的梯度更新权重
- **optimizer** 决定"怎么更新权重"——SGD, Adam 等
- **metrics** 决定"训练时显示什么"——只用于监控，不参与梯度计算
- compile 只是"配置"，不执行训练；调用 `fit()` 才真正开始训练

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---


## Section 3: 局限性

1. **MSE 在分类中梯度消失**：Sigmoid 饱和 × MSE → 梯度 ≈ 0 → 学不动。分类必须用交叉熵
2. **交叉熵对 log(0) 不稳定**：当 $\hat{y} = 0$ 时 $\log(0) = -\infty$ → NaN。框架内部会 clip 到极小正数
3. **标准 CE 不处理类别不平衡**：少数类（如 1%）被大量多数类淹没 → 需要 Focal Loss 或加权 CE
4. **MSE 对异常值敏感**：一个极端误差被平方放大后主导整个 loss → 用 Huber 或 MAE 替代
5. **Loss ≠ Metric**：training loss 在下降不代表模型变好——可能在过拟合

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.7

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **MSE** | 简单，梯度光滑 | 对异常值敏感，分类中梯度消失 | 回归（无异常值） |
| **MAE** | 对异常值鲁棒 | $y=\hat{y}$ 处不可微，收敛慢 | 回归（有异常值） |
| **Huber** | MSE+MAE 混合优点 | 多一个超参数 $\delta$ | 回归（推荐） |
| **BCE** | 消除 Sigmoid 饱和 | 只适用于二分类/多标签 | 二分类 |
| **CCE** | 消除 Softmax 饱和 | 需要 one-hot 标签 | 多分类（one-hot） |
| **Sparse CCE** | 同 CCE + 节省内存 | — | **多分类（推荐）** |
| **Focal Loss** | 处理类别不平衡 | 多一个超参数 $\gamma$ | 目标检测 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [《PRML》Ch.4](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 交叉熵推导 |
| [Keras Losses](https://keras.io/api/losses/) | 📖 文档 | API 参考 |
