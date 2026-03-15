---
topic: tensorflow
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.6,8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: TensorFlow Guide — https://www.tensorflow.org/guide"
  - "📖 Docs: Keras Optimizers — https://keras.io/api/optimizers/"
expiry: 12m
status: current
---

# TensorFlow 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, 8

---

## 符号对照表

| 符号 | 含义 | TF 对应 | 取值范围 |
|------|------|---------|---------|
| $\mathbf{W} \in \mathbb{R}^{m \times n}$ | 权重矩阵 | `layer.kernel` / `tf.Variable` | 实数 |
| $\mathbf{b} \in \mathbb{R}^m$ | 偏置向量 | `layer.bias` / `tf.Variable` | 实数 |
| $\eta$ | 学习率 | `optimizer.learning_rate` | $> 0$ |
| $L(\theta)$ | 损失函数 | `loss_fn(y_true, y_pred)` | $\geq 0$ |
| $\nabla_\theta L$ | 梯度 | `tape.gradient(loss, vars)` | — |
| $\hat{y}$ | 预测 | `model(x)` / `model.predict(x)` | — |

---

## 核心公式

### 公式 1: 全连接层前向传播

$$\mathbf{h} = \sigma(\mathbf{W}\mathbf{x} + \mathbf{b})$$

> 📚 Book: Goodfellow et al., [《DL》](../../../textbooks/goodfellow_deep_learning.pdf), Eq.6.2
> 📖 Docs: `tf.keras.layers.Dense(units, activation)`

### 公式 2: 交叉熵损失（分类）

$$L = -\frac{1}{N}\sum_{i=1}^N \sum_{c=1}^C y_{ic} \log \hat{y}_{ic}$$

> 📖 Docs: `tf.keras.losses.CategoricalCrossentropy()`

### 公式 3: 均方误差损失（回归）

$$L = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2$$

> 📖 Docs: `tf.keras.losses.MeanSquaredError()`

### 公式 4: Adam 优化器

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

默认 $\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-7}$

> 📚 Book: Goodfellow et al., [《DL》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.5.3
> 📖 Docs: `tf.keras.optimizers.Adam(learning_rate=0.001)`

### 公式 5: Batch Normalization

$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta$$

$\mu_B, \sigma_B^2$: mini-batch 的均值和方差；$\gamma, \beta$: 可学习缩放和偏移

> 📚 Book: Goodfellow et al., [《DL》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.7.1
> 📖 Docs: `tf.keras.layers.BatchNormalization()`

### 公式 6: Dropout

训练时以概率 $p$ 随机将神经元输出置零（保留概率 $1-p$），推理时不 dropout 但输出缩放 $\times(1-p)$（或训练时放大 $\times\frac{1}{1-p}$，即 inverted dropout）

> 📚 Book: Goodfellow et al., [《DL》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.7.12
> 📖 Docs: `tf.keras.layers.Dropout(rate=0.5)`

### 公式 7: 卷积层

$$(f * g)[i, j] = \sum_m \sum_n f[m, n] \cdot g[i-m, j-n]$$

TF 实现为互相关（cross-correlation），kernel 翻转由优化吸收

> 📖 Docs: `tf.keras.layers.Conv2D(filters, kernel_size, strides, padding)`

### 公式 8: 学习率衰减

指数衰减：$\eta_t = \eta_0 \cdot d^{t/s}$（$d$ = 衰减率，$s$ = 衰减步数）

> 📖 Docs: `tf.keras.optimizers.schedules.ExponentialDecay()`

---

## 公式速查表

| 名称 | 公式 | TF API | 用途 |
|------|------|--------|------|
| 全连接 | $\sigma(Wx+b)$ | `Dense(units, activation)` | 线性变换+激活 |
| 交叉熵 | $-\sum y\log\hat{y}$ | `CategoricalCrossentropy` | 分类损失 |
| MSE | $\frac{1}{N}\sum(y-\hat{y})^2$ | `MeanSquaredError` | 回归损失 |
| Adam | 一阶矩+二阶矩自适应 | `Adam(lr)` | 自适应优化 |
| BN | 归一化+缩放 | `BatchNormalization` | 稳定训练 |
| Dropout | 随机置零 | `Dropout(rate)` | 正则化 |
| Conv2D | 互相关 | `Conv2D(filters, ks)` | 空间特征提取 |
| LR decay | $\eta_0 \cdot d^{t/s}$ | `ExponentialDecay` | 训练后期精细化 |

> 📚 Book: Goodfellow et al., [《DL》](../../../textbooks/goodfellow_deep_learning.pdf)
> 📖 Docs: [Keras API](https://keras.io/api/)
