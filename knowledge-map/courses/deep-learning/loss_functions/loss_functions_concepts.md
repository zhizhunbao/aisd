---
topic: loss_functions
dimension: concepts
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.6 §6.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Docs: Keras Losses — https://keras.io/api/losses/"
expiry: 12m
status: current
---

# Loss Functions 核心概念

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4

---


## 术语定义

### 损失函数 (Loss Function / Cost Function / Objective Function)

衡量模型预测值 $\hat{y}$ 与真实值 $y$ 之间差距的标量函数。训练的目标就是通过调整权重来最小化它。损失函数定义了"好"和"坏"的标准——告诉优化器"往哪里走"。在 Keras 中通过 `model.compile(loss=...)` 指定。

> 易混淆：**Loss vs Metric** — Loss 用于训练（反向传播计算梯度），必须可微；Metric 用于评估（如 accuracy），可以不可微。训练用 cross-entropy 做 loss，但评估时看 accuracy。

### MSE (Mean Squared Error, 均方误差)

$$L = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

预测值与真实值之差的平方的平均。**回归任务**的默认损失函数。特点：对大误差惩罚更重（平方放大）。对应假设：目标变量服从高斯分布（$y \sim \mathcal{N}(\hat{y}, \sigma^2)$）时，最小化 MSE 等价于最大似然估计。

> 易混淆：**MSE vs RMSE** — RMSE = $\sqrt{MSE}$，量纲与目标变量一致（更易解释），但在训练中用 MSE（$\sqrt{}$ 不影响最优点）。

### MAE (Mean Absolute Error, 平均绝对误差)

$$L = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|$$

预测值与真实值之差的绝对值的平均。比 MSE 对异常值更鲁棒（线性惩罚 vs 平方惩罚）。对应假设：目标变量服从拉普拉斯分布。缺点：在 $y=\hat{y}$ 处不可微。

### Binary Cross-Entropy (BCE, 二分类交叉熵)

$$L = -\frac{1}{n}\sum_{i=1}^{n}[y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)]$$

**二分类任务**的标准损失函数。$\hat{y}_i$ 是 Sigmoid 输出的概率（0~1），$y_i$ 是真实标签（0 或 1）。当模型"自信地"预测错误时（如真实=1 但预测≈0），$-\log(0.01)=4.6$ 的惩罚非常大。

> 易混淆：**BCE vs Log Loss** — 完全相同的东西，不同叫法。scikit-learn 称之为 log_loss。

### Categorical Cross-Entropy (CCE, 分类交叉熵)

$$L = -\frac{1}{n}\sum_{i=1}^{n}\sum_{k=1}^{K} y_{i,k} \log(\hat{y}_{i,k})$$

**多分类任务**的标准损失函数。$y_{i,k}$ 是 one-hot 编码的标签，$\hat{y}_{i,k}$ 是 Softmax 输出的概率分布。由于 $y$ 是 one-hot，实际上只有真实类别 $k^*$ 的项非零：$L_i = -\log(\hat{y}_{i,k^*})$。

> 易混淆：**Categorical CE vs Sparse Categorical CE** — Categorical CE 要求标签是 one-hot 向量（如 [0,0,1]）；Sparse Categorical CE 要求标签是整数（如 2）。数学上完全等价，只是标签格式不同。

### Sparse Categorical Cross-Entropy

与 Categorical CE 数学完全相同，但接受整数标签而非 one-hot 向量。当类别数很多时（如 1000+），整数标签比 one-hot 节省大量内存。Keras 中 `sparse_categorical_crossentropy` 是最常用的多分类 loss。

### Hinge Loss (合页损失)

$$L = \frac{1}{n}\sum_{i=1}^{n}\max(0, 1 - y_i \cdot \hat{y}_i)$$

SVM 的经典损失函数。不要求输出是概率，只要求正确类的得分比错误类高出至少 margin=1。在 Keras 中可用但较少使用（深度学习更常用交叉熵）。

### Huber Loss

$$L = \begin{cases} \frac{1}{2}(y-\hat{y})^2 & \text{if } |y-\hat{y}| \leq \delta \\ \delta|y-\hat{y}| - \frac{1}{2}\delta^2 & \text{otherwise} \end{cases}$$

MSE 和 MAE 的混合体：误差小时用 MSE（梯度光滑），误差大时用 MAE（对异常值鲁棒）。兼具两者优点，用 $\delta$ 控制切换阈值。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4
> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---


## 概念辨析

### MSE vs Cross-Entropy（回归 vs 分类）

| 维度 | MSE | Cross-Entropy |
|------|-----|---------------|
| **任务类型** | 回归（连续输出） | 分类（概率输出） |
| **输出层激活** | Linear (Identity) | Sigmoid / Softmax |
| **输出范围** | $(-\infty, +\infty)$ | $(0, 1)$ |
| **梯度行为** | $\propto (\hat{y} - y)$ | 不饱和：$\propto (\hat{y} - y)$ |
| **对 Sigmoid 梯度** | 有饱和问题 | 消除了 Sigmoid 饱和 |
| **概率解释** | 高斯似然 | Bernoulli/Categorical 似然 |
| **推荐用途** | 房价、温度预测 | 图像分类、情感分析 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

### Categorical CE vs Sparse Categorical CE

| 维度 | Categorical CE | Sparse Categorical CE |
|------|---------------|----------------------|
| **标签格式** | One-hot 向量 [0,0,1,0] | 整数 2 |
| **数学** | 完全相同 | 完全相同 |
| **内存** | K 维向量/样本 | 1 整数/样本 |
| **何时用** | 标签已经是 one-hot | 标签是整数（更常见） |
| **Keras 名** | `'categorical_crossentropy'` | `'sparse_categorical_crossentropy'` |

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

### Loss vs Metric

| 维度 | Loss | Metric |
|------|------|--------|
| **用途** | 训练（反向传播） | 评估（监控） |
| **可微性** | 必须可微 | 无需可微 |
| **典型例子** | cross-entropy, MSE | accuracy, precision, F1 |
| **Keras 中** | `compile(loss=...)` | `compile(metrics=[...])` |
| **用 accuracy 当 loss？** | ❌ 不行（不可微） | ✅ 可以当 metric |

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---


## 核心属性

### 信息架构

```
┌──────────────────────────────────────────────────────────────┐
│                    Loss Functions 体系                         │
├──────────────────────────────────────────────────────────────┤
│  回归损失 (Regression Losses)                                  │
│  ├─ MSE (L2 Loss)         (y-ŷ)² 的均值                      │
│  ├─ MAE (L1 Loss)         |y-ŷ| 的均值                       │
│  ├─ Huber Loss             MSE+MAE 混合                       │
│  └─ Log-Cosh Loss          光滑版 MAE                         │
├──────────────────────────────────────────────────────────────┤
│  分类损失 (Classification Losses)                              │
│  ├─ Binary Cross-Entropy   二分类 (Sigmoid 输出)              │
│  ├─ Categorical CE         多分类 one-hot 标签                │
│  ├─ Sparse Categorical CE  多分类整数标签                     │
│  ├─ Hinge Loss             SVM 风格，margin 分类              │
│  └─ Focal Loss             处理类别不平衡                     │
├──────────────────────────────────────────────────────────────┤
│  正则化项 (Regularization Terms)                               │
│  ├─ L1 Regularization      加在 loss 上: L + λΣ|w|           │
│  └─ L2 Regularization      加在 loss 上: L + λΣw²            │
└──────────────────────────────────────────────────────────────┘
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### 任务-激活-损失 配对表 ⭐

| 任务类型 | 输出层激活 | 推荐损失函数 | Keras 名称 |
|---------|-----------|------------|-----------|
| **回归** | Linear / None | MSE | `'mse'` |
| **回归（有异常值）** | Linear | Huber | `keras.losses.Huber()` |
| **二分类** | Sigmoid | BCE | `'binary_crossentropy'` |
| **多分类 (one-hot)** | Softmax | CCE | `'categorical_crossentropy'` |
| **多分类 (整数)** | Softmax | Sparse CCE | `'sparse_categorical_crossentropy'` |
| **多标签** | Sigmoid (per label) | BCE | `'binary_crossentropy'` |
| **排序/SVM** | Linear | Hinge | `'hinge'` |

> 📖 Docs: [Keras Losses](https://keras.io/api/losses/)

---


## 速查表

| 损失函数 | 公式核心 | 输出层激活 | 任务 | 对异常值 |
|---------|---------|----------|------|---------|
| MSE | $(y-\hat{y})^2$ | Linear | 回归 | 敏感 |
| MAE | $\|y-\hat{y}\|$ | Linear | 回归 | 鲁棒 |
| Huber | MSE+MAE 混合 | Linear | 回归 | 鲁棒 |
| BCE | $-[y\log\hat{y}+(1-y)\log(1-\hat{y})]$ | Sigmoid | 二分类 | — |
| CCE | $-\sum y_k\log\hat{y}_k$ | Softmax | 多分类 | — |
| Sparse CCE | 同 CCE (整数标签) | Softmax | 多分类 | — |
| Hinge | $\max(0, 1-y\hat{y})$ | Linear | SVM 分类 | — |
| Focal | $-\alpha(1-\hat{y})^\gamma\log\hat{y}$ | Sigmoid/Softmax | 不平衡分类 | — |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2
