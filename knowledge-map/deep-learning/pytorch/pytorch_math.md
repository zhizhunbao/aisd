---
topic: pytorch
dimension: math
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)"
  - "📖 Paper: [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)"
  - "📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Ch.6"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5"
expiry: 12m
status: current
---

# PyTorch 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../textbooks/goodfellow_deep_learning.pdf), Ch.6
> 📖 Docs: [Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| $x$ | 输入张量（叶子节点） | Input tensor | $\mathbb{R}^n$ |
| $w$ | 模型权重参数 | Weight parameter | $\mathbb{R}^{m \times n}$ |
| $b$ | 偏置参数 | Bias | $\mathbb{R}^m$ |
| $L$ | 损失函数输出（标量） | Loss (scalar) | $\mathbb{R}$ |
| $\frac{\partial L}{\partial w}$ | 损失对权重的梯度 | Gradient of loss w.r.t. weight | $\mathbb{R}^{m \times n}$ |
| $\eta$ | 学习率 | Learning rate | $(0, 1)$，常用 $10^{-3}$ |
| $f_i$ | 计算图中第 $i$ 步操作 | Operation function | 可微函数 |
| $y = f(x)$ | 前向传播输出 | Forward pass output | $\mathbb{R}^m$ |
| $\hat{y}$ | 模型预测值 | Prediction | $\mathbb{R}^m$ |
| $y^*$ | 真实标签 | Ground truth label | $\mathbb{R}^m$ |

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 核心公式

### 公式 1: 链式法则（反向传播的数学基础）

**直觉：** 复合函数的导数 = 每一层导数的乘积。这就是 Autograd 的数学核心——沿计算图从输出往输入逐步传递梯度。

$$
\frac{\partial L}{\partial x} = \frac{\partial L}{\partial f_n} \cdot \frac{\partial f_n}{\partial f_{n-1}} \cdots \frac{\partial f_2}{\partial f_1} \cdot \frac{\partial f_1}{\partial x}
$$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Eq. 6.44-6.47

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $L$ | 最终损失 | `loss = criterion(output, target)` |
| $f_i$ | 第 $i$ 步操作 | 每个 `nn.Module.forward()` |
| $\frac{\partial f_i}{\partial f_{i-1}}$ | 局部雅可比矩阵 | 每个 `.grad_fn` 计算的内容 |

**推导过程：**

$$
\text{Step 1: 设 } y = f_2(f_1(x)), \text{ 则 } \frac{\partial y}{\partial x} = \frac{\partial f_2}{\partial f_1} \cdot \frac{\partial f_1}{\partial x}
$$

$$
\text{Step 2: 推广到 n 层: } L = f_n \circ f_{n-1} \circ \cdots \circ f_1(x)
$$

$$
\text{Step 3: } \frac{\partial L}{\partial x} = \prod_{i=1}^{n} \frac{\partial f_i}{\partial f_{i-1}} \quad \text{（反向遍历）}
$$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Section 6.5.2

---

### 公式 2: SGD 参数更新

**直觉：** 沿梯度反方向走一小步来减小损失。学习率控制步长大小。

$$
w_{t+1} = w_t - \eta \cdot \frac{\partial L}{\partial w_t}
$$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Eq. 8.1

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $w_t$ | 当前权重 | `param.data` |
| $\eta$ | 学习率 | `lr=0.01` |
| $\frac{\partial L}{\partial w_t}$ | 当前梯度 | `param.grad` |

**推导过程：**

$$
\text{Step 1: 泰勒展开 } L(w + \Delta w) \approx L(w) + \nabla L(w)^T \Delta w
$$

$$
\text{Step 2: 要让 } L \text{ 减小最快，选 } \Delta w = -\eta \nabla L(w)
$$

$$
\text{Step 3: 因此 } w_{t+1} = w_t - \eta \nabla L(w_t)
$$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Section 8.3.1

---

### 公式 3: Adam 优化器

**直觉：** 给每个参数自适应调整学习率——用一阶矩（动量）加速收敛、用二阶矩（自适应缩放）稳定更新。

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t
$$

$$
v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2
$$

$$
\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}
$$

$$
w_{t+1} = w_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t
$$

> 📖 Paper: Kingma & Ba, [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980), 2014

**参数解释：**
| 参数 | 含义 | PyTorch 默认值 |
|------|------|---------------|
| $g_t$ | 当前梯度 | `param.grad` |
| $m_t$ | 一阶矩估计（动量） | — |
| $v_t$ | 二阶矩估计 | — |
| $\beta_1$ | 一阶矩衰减率 | 0.9 |
| $\beta_2$ | 二阶矩衰减率 | 0.999 |
| $\epsilon$ | 数值稳定项 | $10^{-8}$ |
| $\eta$ | 学习率 | 需手动设置 |

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), Algorithm 1

---

### 公式 4: 交叉熵损失

**直觉：** 衡量两个概率分布之间的距离。模型预测的分布越接近真实分布（one-hot），损失越小。

$$
L = -\sum_{c=1}^{C} y_c^* \log(\hat{y}_c) = -\log(\hat{y}_{y^*})
$$

其中 $\hat{y} = \text{softmax}(z)$，即：

$$
\hat{y}_c = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}
$$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Section 6.2.2.3

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $C$ | 类别数 | `num_classes` |
| $z_c$ | 第 $c$ 类的 logit | 模型最后一层输出 |
| $\hat{y}_c$ | 第 $c$ 类的预测概率 | softmax 输出 |
| $y^*$ | 真实类别索引 | `target` |

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Eq. 6.22

---


## 公式关系图

```
链式法则 ──→ 反向传播算法(Autograd) ──→ 计算梯度 ∂L/∂w
                                            │
                                            ↓
            交叉熵损失 ──→ 损失 L ──→ 梯度 ──→ SGD/Adam 参数更新
                ↑                              │
           Softmax 归一化                      ↓
                                         w_{t+1} = w_t - η·∇L
```

---


## 手算练习

### 练习 1: 简单链式法则

**题目：** 设 $f(x) = (2x + 1)^3$，求 $f'(x)$ 在 $x = 1$ 时的值。

**解答步骤：**

1. 令 $u = 2x+1$，则 $f = u^3$
2. $\frac{df}{dx} = \frac{df}{du} \cdot \frac{du}{dx} = 3u^2 \cdot 2 = 6(2x+1)^2$
3. 代入 $x=1$: $f'(1) = 6 \times (2+1)^2 = 6 \times 9 = 54$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Section 6.5

### 练习 2: SGD 手动更新

**题目：** 设 $w = 2.0$, $\frac{\partial L}{\partial w} = 0.5$, $\eta = 0.1$，计算一步更新后的 $w$。

**解答步骤：**

1. 代入公式: $w_{t+1} = w_t - \eta \cdot \frac{\partial L}{\partial w_t}$
2. 计算: $w_{t+1} = 2.0 - 0.1 \times 0.5 = 2.0 - 0.05 = 1.95$
3. 结果 $w_{t+1} = 1.95$

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Section 8.3

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 链式法则 | $\frac{\partial L}{\partial x} = \prod \frac{\partial f_i}{\partial f_{i-1}}$ | Autograd 核心 | — |
| SGD | $w_{t+1} = w_t - \eta \nabla L$ | 最简单的参数更新 | 链式法则 |
| Adam | $w_{t+1} = w_t - \frac{\eta}{\sqrt{\hat{v}_t}+\epsilon}\hat{m}_t$ | 自适应学习率更新 | 链式法则 |
| Softmax | $\hat{y}_c = \frac{e^{z_c}}{\sum e^{z_j}}$ | logit → 概率 | — |
| 交叉熵 | $L = -\log(\hat{y}_{y^*})$ | 分类损失 | Softmax |
| MSE | $L = \frac{1}{n}\sum(y - \hat{y})^2$ | 回归损失 | — |

> 📚 Book: Goodfellow et al., [Deep Learning](../../textbooks/goodfellow_deep_learning.pdf), Ch.6, Ch.8
