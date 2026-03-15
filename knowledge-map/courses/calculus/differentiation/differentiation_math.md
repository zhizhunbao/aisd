---
topic: differentiation
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.4,6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Boyd & Vandenberghe, Convex Optimization, Ch.2-3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
expiry: 12m
status: current
---

# 微分 数学基础

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $f'(x)$ 或 $\frac{df}{dx}$ | 函数 $f$ 对 $x$ 的导数 | Derivative | $\mathbb{R}$ |
| $\frac{\partial f}{\partial x_i}$ | $f$ 对 $x_i$ 的偏导数 | Partial derivative | $\mathbb{R}$ |
| $\nabla f$ | $f$ 的梯度向量 | Gradient | $\mathbb{R}^n$ |
| $\mathbf{J}$ | Jacobian 矩阵 | Jacobian | $\mathbb{R}^{m \times n}$ |
| $\mathbf{H}$ | Hessian 矩阵 | Hessian | $\mathbb{R}^{n \times n}$ |
| $h$ | 差分步长（极限中趋近 0） | Step size | $h \to 0$ |
| $\eta$ | 学习率（梯度下降步长） | Learning rate | $\eta > 0$ |
| $L(\theta)$ | 损失函数 | Loss function | $\mathbb{R}$ |
| $\theta$ | 模型参数向量 | Parameters | $\mathbb{R}^n$ |
| $D_\mathbf{u} f$ | 方向导数 | Directional derivative | $\mathbb{R}$ |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5 notation

---


## 核心公式

### 公式 1: 导数定义（极限定义）

**直觉：** 函数在某点的"瞬时速度"——当观测区间缩到无穷小时的平均变化率

$$
f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Def. 5.1

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $h$ | 自变量的微小增量 | 趋近 0 |
| $f(x+h)-f(x)$ | 函数值的变化量 | 因变量改变 |

**推导过程：**

$$
\text{Step 1: 平均变化率 } \frac{\Delta y}{\Delta x} = \frac{f(x + h) - f(x)}{h}
$$
$$
\text{Step 2: 令 } h \to 0\text{，"平均"变为"瞬时"}
$$
$$
\text{Step 3: } f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1

---

### 公式 2: 链式法则（一元 & 多元）

**直觉：** 复合函数的导数 = 外层导数 × 内层导数——"变化率的传递"

一元版：

$$
\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)
$$

多元版（Jacobian 乘法）：

$$
\frac{\partial \mathbf{f}}{\partial \mathbf{x}} = \frac{\partial \mathbf{f}}{\partial \mathbf{g}} \cdot \frac{\partial \mathbf{g}}{\partial \mathbf{x}} = \mathbf{J}_f \cdot \mathbf{J}_g
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Eq. 5.32
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Eq. 6.44

**推导过程：**

$$
\text{Step 1: 记 } y = g(x),\; z = f(y) = f(g(x))
$$
$$
\text{Step 2: } \frac{dz}{dx} = \lim_{h \to 0} \frac{f(g(x+h)) - f(g(x))}{h}
$$
$$
\text{Step 3: 设 } \Delta y = g(x+h) - g(x)
$$
$$
\text{Step 4: } = \lim_{h \to 0} \frac{f(g(x) + \Delta y) - f(g(x))}{\Delta y} \cdot \frac{\Delta y}{h}
$$
$$
\text{Step 5: } = f'(g(x)) \cdot g'(x) \quad (\text{当 } h \to 0,\; \Delta y \to 0)
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

---

### 公式 3: 梯度（Gradient）

**直觉：** 多元标量函数的"全方位导数"——收集所有偏导数形成一个向量，指向最陡上升方向

$$
\nabla f(\mathbf{x}) = \begin{bmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{bmatrix} \in \mathbb{R}^n
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Def. 5.6

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\frac{\partial f}{\partial x_i}$ | $f$ 对第 $i$ 个变量的偏导数 | 只改变 $x_i$，看 $f$ 怎么变 |

**推导过程：**

$$
\text{Step 1: 全微分 } df = \frac{\partial f}{\partial x_1}dx_1 + \frac{\partial f}{\partial x_2}dx_2 + \cdots = \nabla f^\top d\mathbf{x}
$$
$$
\text{Step 2: 方向导数 } D_\mathbf{u} f = \nabla f \cdot \mathbf{u}
$$
$$
\text{Step 3: 由柯西-施瓦茨不等式 } |\nabla f \cdot \mathbf{u}| \leq \|\nabla f\| \|\mathbf{u}\|
$$
$$
\text{Step 4: 等号成立当 } \mathbf{u} \parallel \nabla f\text{，即梯度方向是最大增长方向}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

---

### 公式 4: 梯度下降更新规则 (Gradient Descent)

**直觉：** 沿梯度的反方向"下坡"——每步按学习率 $\eta$ 缩放梯度来更新参数

$$
\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Eq. 4.7

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\theta_t$ | 当前参数 | 网络权重 |
| $\eta$ | 学习率 | 如 $0.001$ |
| $\nabla_\theta L$ | 损失对参数的梯度 | 反向传播结果 |

**推导过程：**

$$
\text{Step 1: Taylor 一阶展开 } L(\theta + \Delta\theta) \approx L(\theta) + \nabla_\theta L^\top \Delta\theta
$$
$$
\text{Step 2: 要使 } L \text{ 减小最快，选 } \Delta\theta = -\eta \nabla_\theta L \text{ （最优方向 = 负梯度）}
$$
$$
\text{Step 3: 代入 } L(\theta - \eta\nabla L) \approx L(\theta) - \eta \|\nabla L\|^2 < L(\theta) \quad (\eta \text{ 足够小时})
$$

> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9.3

---

### 公式 5: Jacobian 矩阵

**直觉：** 向量函数的"导数矩阵"——描述输入微小变化如何线性映射为输出变化

$$
\mathbf{J} = \frac{\partial \mathbf{f}}{\partial \mathbf{x}} = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\ \vdots & \ddots & \vdots \\ \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n} \end{bmatrix} \in \mathbb{R}^{m \times n}
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Def. 5.8

**关键性质：**
- $d\mathbf{f} \approx \mathbf{J} \cdot d\mathbf{x}$（局部线性近似）
- 行列式 $|\det \mathbf{J}|$ 是变换的体积缩放因子（概率分布变换中需要）

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.3

---

### 公式 6: Hessian 矩阵与二阶 Taylor 展开

**直觉：** 二阶导数矩阵描述曲面的"弯曲程度"——可用于判断极值点类型和牛顿法加速

$$
\mathbf{H} = \nabla^2 f = \begin{bmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots \\ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix}
$$

二阶 Taylor 展开：

$$
f(\mathbf{x} + \boldsymbol{\delta}) \approx f(\mathbf{x}) + \nabla f^\top \boldsymbol{\delta} + \frac{1}{2} \boldsymbol{\delta}^\top \mathbf{H} \boldsymbol{\delta}
$$

> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.3.1.2
> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.4

---

### 公式 7: 反向传播（多层链式法则展开）

**直觉：** 对 $L$→$L_{N}$→...→$L_1$ 的多层复合函数，梯度从输出向输入逐层回传

对于 $L = f_N(f_{N-1}(\cdots f_1(\mathbf{x}; \theta_1); \theta_2) \cdots; \theta_N)$：

$$
\frac{\partial L}{\partial \theta_k} = \frac{\partial L}{\partial \mathbf{h}_N} \cdot \frac{\partial \mathbf{h}_N}{\partial \mathbf{h}_{N-1}} \cdots \frac{\partial \mathbf{h}_{k+1}}{\partial \mathbf{h}_k} \cdot \frac{\partial \mathbf{h}_k}{\partial \theta_k}
$$

其中 $\mathbf{h}_k = f_k(\mathbf{h}_{k-1}; \theta_k)$ 是第 $k$ 层的输出。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5, Algorithm 6.3

---

### 公式 8: 常用导数公式表

**直觉：** ML 中最常用的基本导数——这些是链式法则的"原子构件"

| 函数 $f(x)$ | 导数 $f'(x)$ | 来源 |
|-------------|-------------|------|
| $x^n$ | $nx^{n-1}$ | 幂函数 |
| $e^x$ | $e^x$ | 指数函数 |
| $\ln x$ | $1/x$ | 对数函数 |
| $\sin x$ | $\cos x$ | 三角函数 |
| $\cos x$ | $-\sin x$ | 三角函数 |
| $\sigma(x) = \frac{1}{1+e^{-x}}$ | $\sigma(x)(1-\sigma(x))$ | Sigmoid |
| $\tanh(x)$ | $1 - \tanh^2(x)$ | 双曲正切 |
| $\text{ReLU}(x) = \max(0,x)$ | $\begin{cases}1 & x>0\\0 & x<0\end{cases}$ | ReLU |
| $\text{softmax}_i(\mathbf{z})$ | $s_i(\delta_{ij} - s_j)$ | Softmax |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5, Table 5.1
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

---


## 公式关系图

```
导数定义 (极限)
    │
    ├──→ 基本求导法则 (幂/指数/对数/三角)
    │         │
    │         ▼
    │    乘积法则 + 商法则
    │
    ├──→ 链式法则 ──→ 反向传播 (多层链式法则)
    │                      │
    │                      ▼
    │               计算图 + 自动微分
    │
    ├──→ 偏导数 ──→ 梯度 ∇f ──→ 梯度下降
    │                │              │
    │                ▼              ▼
    │           方向导数        SGD / Adam
    │
    ├──→ Jacobian (向量函数一阶) ──→ 变量替换 |det J|
    │
    └──→ Hessian (标量函数二阶) ──→ 牛顿法
                                    │
                                    ▼
                              凸性判定 (H ≻ 0)
```

---


## 手算练习

### 练习 1: 基本多项式求导

**题目：** 求 $f(x) = 3x^4 - 2x^2 + 5x - 7$ 的导数

**解答步骤：**

1. 幂函数法则逐项求导
2. $f'(x) = 3 \cdot 4x^3 - 2 \cdot 2x + 5 = 12x^3 - 4x + 5$
3. 结果：$f'(x) = 12x^3 - 4x + 5$

> 📚 Book: 基础微积分

### 练习 2: 链式法则

**题目：** 求 $f(x) = e^{-x^2/2}$ 的导数

**解答步骤：**

1. 外层 $e^u$，导数 $e^u$；内层 $u = -x^2/2$，导数 $-x$
2. 链式法则：$f'(x) = e^{-x^2/2} \cdot (-x) = -x \cdot e^{-x^2/2}$
3. 结果：$f'(x) = -xe^{-x^2/2}$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

### 练习 3: 梯度计算

**题目：** 求 $f(x_1, x_2) = x_1^2 + 3x_1 x_2 + x_2^3$ 的梯度，在点 $(1, 2)$ 处的值

**解答步骤：**

1. $\frac{\partial f}{\partial x_1} = 2x_1 + 3x_2$
2. $\frac{\partial f}{\partial x_2} = 3x_1 + 3x_2^2$
3. 在 $(1,2)$：$\nabla f = [2(1) + 3(2),\; 3(1) + 3(4)]^\top = [8, 15]^\top$
4. 结果：$\nabla f(1,2) = [8, 15]^\top$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

### 练习 4: Sigmoid 导数

**题目：** 证明 $\sigma'(x) = \sigma(x)(1 - \sigma(x))$，其中 $\sigma(x) = \frac{1}{1 + e^{-x}}$

**解答步骤：**

1. $\sigma(x) = (1 + e^{-x})^{-1}$
2. 链式法则：$\sigma'(x) = -(1+e^{-x})^{-2} \cdot (-e^{-x}) = \frac{e^{-x}}{(1+e^{-x})^2}$
3. 分子分母同除 $(1+e^{-x})^2$：$= \frac{1}{1+e^{-x}} \cdot \frac{e^{-x}}{1+e^{-x}} = \sigma(x) \cdot \frac{1+e^{-x}-1}{1+e^{-x}}$
4. $= \sigma(x)(1 - \sigma(x))$ ✅

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3

### 练习 5: Hessian 计算

**题目：** 求 $f(x_1, x_2) = x_1^2 + 4x_1 x_2 + x_2^2$ 的 Hessian，判断是否正定

**解答步骤：**

1. $\frac{\partial^2 f}{\partial x_1^2} = 2,\; \frac{\partial^2 f}{\partial x_1 \partial x_2} = 4,\; \frac{\partial^2 f}{\partial x_2^2} = 2$
2. $\mathbf{H} = \begin{bmatrix} 2 & 4 \\ 4 & 2 \end{bmatrix}$
3. 特征值：$\lambda_{1,2} = 2 \pm 4 = 6, -2$
4. 有一个负特征值 → **不正定**（鞍点或极大值方向存在）

> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.3

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| 导数定义 | $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ | 基础定义 | 极限 |
| 链式法则 | $(f \circ g)' = f'(g) \cdot g'$ | 复合函数求导 | 导数定义 |
| 梯度 | $\nabla f = [\partial f/\partial x_i]^\top$ | 最陡方向 | 偏导数 |
| 梯度下降 | $\theta \leftarrow \theta - \eta \nabla L$ | 参数优化 | 梯度 |
| Jacobian | $J_{ij} = \partial f_i / \partial x_j$ | 向量函数线性化 | 偏导数 |
| Hessian | $H_{ij} = \partial^2 f / \partial x_i \partial x_j$ | 曲率/凸性 | 梯度 |
| 反向传播 | $\frac{\partial L}{\partial \theta_k} = \prod \mathbf{J}_k$ | 网络训练 | 链式法则 |
| Sigmoid 导数 | $\sigma' = \sigma(1-\sigma)$ | 激活函数梯度 | 链式法则 |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6
