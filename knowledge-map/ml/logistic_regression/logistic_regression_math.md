---
topic: logistic_regression
dimension: math
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Hastie et al., ESL Ch.4.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/hastie_esl.pdf"
  - "📚 Book: Bishop, PRML Ch.4.3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📚 Book: Murphy, PML1 Ch.10 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/murphy_pml1.pdf"
  - "📚 Book: Deisenroth et al., MML Ch.12.2 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📖 Paper: Cox, 'The Regression Analysis of Binary Sequences', JRSS-B 1958 — https://doi.org/10.1111/j.2517-6161.1958.tb00292.x"
expiry: 12m
status: current
---

# Logistic Regression 数学基础

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.3

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------| 
| $N$ | 样本数 | number of samples | $N \geq 1$ |
| $p$ | 特征维度 | number of features | $p \geq 1$ |
| $K$ | 类别数 | number of classes | $K \geq 2$ |
| $\mathbf{x}_i$ | 第 $i$ 个样本的特征向量 | feature vector | $\mathbf{x}_i \in \mathbb{R}^p$ |
| $y_i$ | 第 $i$ 个样本的标签 | label | $y_i \in \{0, 1\}$（二分类） |
| $\mathbf{w}$ | 权重向量 | weight vector | $\mathbf{w} \in \mathbb{R}^p$ |
| $b$ | 偏置项（截距） | bias / intercept | $b \in \mathbb{R}$ |
| $z_i$ | 第 $i$ 个样本的线性组合 | linear predictor / logit | $z_i = \mathbf{w}^T\mathbf{x}_i + b$ |
| $\hat{p}_i$ | 预测概率 | predicted probability | $\hat{p}_i = \sigma(z_i) \in (0,1)$ |
| $\sigma(\cdot)$ | Sigmoid 函数 | sigmoid / logistic function | 输出 $(0,1)$ |
| $\mathcal{L}$ | 损失函数 | loss function | $\mathcal{L} \geq 0$ |
| $\lambda$ | 正则化系数 | regularization strength | $\lambda \geq 0$ |
| $C$ | 正则化的倒数（sklearn 用法） | inverse regularization | $C = 1/\lambda > 0$ |
| $\mathbf{H}$ | Hessian 矩阵 | Hessian matrix | $\mathbf{H} \in \mathbb{R}^{p \times p}$ |
| $\mathbf{W}$ | 对角权重矩阵（IRLS 用） | diagonal weight matrix | $W_{ii} = \hat{p}_i(1-\hat{p}_i)$ |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

---


## 核心公式

### 公式 1: Sigmoid 函数

**直觉：** 把线性预测值压缩到 (0,1) 区间变成概率，S 形曲线使得远离零点的值迅速趋近 0 或 1

$$
\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.59

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $z$ | 线性组合 $\mathbf{w}^T\mathbf{x} + b$ | 当 $z=0$ 时 $\sigma=0.5$ |

**关键性质：**

$$
\sigma(-z) = 1 - \sigma(z) \quad \text{（中心对称）}
$$

$$
\sigma'(z) = \sigma(z)(1 - \sigma(z)) \quad \text{（导数性质）}
$$

**推导过程：** 导数性质推导

$$
\text{Step 1: } \sigma(z) = (1+e^{-z})^{-1}
$$
$$
\text{Step 2: } \sigma'(z) = -(-e^{-z})(1+e^{-z})^{-2} = \frac{e^{-z}}{(1+e^{-z})^2}
$$
$$
\text{Step 3: } = \frac{1}{1+e^{-z}} \cdot \frac{e^{-z}}{1+e^{-z}} = \sigma(z) \cdot \frac{1+e^{-z}-1}{1+e^{-z}}
$$
$$
\text{Step 4: } = \sigma(z)(1 - \sigma(z))
$$

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.12.2

---

### 公式 2: 模型公式（对数几率线性）

**直觉：** Logistic Regression 的核心假设——对数几率 (log-odds) 是特征的线性函数

$$
\log \frac{P(Y=1|\mathbf{x})}{P(Y=0|\mathbf{x})} = \mathbf{w}^T\mathbf{x} + b
$$

等价地：

$$
P(Y=1|\mathbf{x}) = \sigma(\mathbf{w}^T\mathbf{x} + b) = \frac{1}{1 + \exp(-\mathbf{w}^T\mathbf{x} - b)}
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 4.17

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\mathbf{w}^T\mathbf{x} + b$ | 线性预测器 | 左侧 = log-odds |
| $w_j$ | 特征 $j$ 的权重 | $x_j$ 增加 1，log-odds 增加 $w_j$ |
| $e^{w_j}$ | 特征 $j$ 的 odds ratio | $x_j$ 增加 1，odds 变为 $e^{w_j}$ 倍 |

**推导过程：**

$$
\text{Step 1: 假设 } \log\frac{p}{1-p} = z = \mathbf{w}^T\mathbf{x} + b
$$
$$
\text{Step 2: 两边取指数 } \frac{p}{1-p} = e^z
$$
$$
\text{Step 3: 解出 } p = \frac{e^z}{1+e^z} = \frac{1}{1+e^{-z}} = \sigma(z)
$$

> 📖 Paper: Cox, [The Regression Analysis of Binary Sequences](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x), JRSS-B 1958

---

### 公式 3: 负对数似然 / 交叉熵损失

**直觉：** 最大化"正确标签的预测概率"，等价于最小化这个交叉熵损失

$$
\mathcal{L}(\mathbf{w}, b) = -\frac{1}{N}\sum_{i=1}^{N} \left[ y_i \log \hat{p}_i + (1-y_i)\log(1-\hat{p}_i) \right]
$$

其中 $\hat{p}_i = \sigma(\mathbf{w}^T\mathbf{x}_i + b)$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.90

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $y_i$ | 真实标签 | 0 或 1 |
| $\hat{p}_i$ | 预测为正类的概率 | $\sigma(z_i)$ |
| $N$ | 样本总数 | 归一化用 |

**推导过程：** 从 MLE 到交叉熵

$$
\text{Step 1: 似然函数 } L(\mathbf{w}, b) = \prod_{i=1}^N \hat{p}_i^{y_i}(1-\hat{p}_i)^{1-y_i}
$$
$$
\text{Step 2: 对数似然 } \ell = \sum_{i=1}^N \left[ y_i \log \hat{p}_i + (1-y_i)\log(1-\hat{p}_i) \right]
$$
$$
\text{Step 3: 负对数似然 (NLL) } \mathcal{L} = -\frac{1}{N}\ell \quad \text{（最小化 NLL = 最大化似然）}
$$

> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.2

---

### 公式 4: 梯度

**直觉：** 梯度形式优雅——误差 $(\hat{p}_i - y_i)$ 乘以特征 $\mathbf{x}_i$ 的加权平均

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{w}} = \frac{1}{N}\sum_{i=1}^N (\hat{p}_i - y_i)\mathbf{x}_i = \frac{1}{N}\mathbf{X}^T(\hat{\mathbf{p}} - \mathbf{y})
$$

$$
\frac{\partial \mathcal{L}}{\partial b} = \frac{1}{N}\sum_{i=1}^N (\hat{p}_i - y_i)
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 4.21

**推导过程：**

$$
\text{Step 1: 单样本损失对 } z_i \text{ 的导数}
$$
$$
\frac{\partial \mathcal{L}_i}{\partial z_i} = -y_i(1-\hat{p}_i) + (1-y_i)\hat{p}_i = \hat{p}_i - y_i
$$
$$
\text{Step 2: 链式法则 } \frac{\partial z_i}{\partial \mathbf{w}} = \mathbf{x}_i
$$
$$
\text{Step 3: } \frac{\partial \mathcal{L}}{\partial \mathbf{w}} = \frac{1}{N}\sum_{i=1}^N (\hat{p}_i - y_i)\mathbf{x}_i
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.91

---

### 公式 5: Hessian 矩阵

**直觉：** Hessian 是正半定的 (PSD)，证明了交叉熵损失是凸函数→全局最优解存在

$$
\mathbf{H} = \frac{\partial^2 \mathcal{L}}{\partial \mathbf{w} \partial \mathbf{w}^T} = \frac{1}{N}\mathbf{X}^T\mathbf{W}\mathbf{X}
$$

其中 $\mathbf{W} = \text{diag}(\hat{p}_1(1-\hat{p}_1), \ldots, \hat{p}_N(1-\hat{p}_N))$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 4.22

**参数解释：**
| 参数 | 含义 | 例子中对应 |
|------|------|-----------| 
| $\mathbf{W}$ | 对角权重矩阵 | $W_{ii} = \hat{p}_i(1-\hat{p}_i) > 0$ |
| $\mathbf{X}$ | 设计矩阵 $N \times p$ | 所有样本特征 |

**凸性证明：**

$$
\text{Step 1: 对任意 } \mathbf{v} \neq 0
$$
$$
\text{Step 2: } \mathbf{v}^T\mathbf{H}\mathbf{v} = \frac{1}{N}\mathbf{v}^T\mathbf{X}^T\mathbf{W}\mathbf{X}\mathbf{v} = \frac{1}{N}(\mathbf{X}\mathbf{v})^T\mathbf{W}(\mathbf{X}\mathbf{v})
$$
$$
\text{Step 3: } W_{ii} = \hat{p}_i(1-\hat{p}_i) > 0 \text{ (因为 } 0 < \hat{p}_i < 1\text{)}
$$
$$
\text{Step 4: } \therefore \mathbf{H} \text{ ≥ 0 (正半定), 损失函数是凸的}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.3.3

---

### 公式 6: Newton-Raphson / IRLS 更新

**直觉：** 每步用二阶信息加速收敛——把非线性问题局部近似为加权最小二乘

$$
\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \mathbf{H}^{-1}\nabla\mathcal{L}
$$

展开为 IRLS 形式：

$$
\mathbf{w}^{(t+1)} = (\mathbf{X}^T\mathbf{W}^{(t)}\mathbf{X})^{-1}\mathbf{X}^T\mathbf{W}^{(t)}\mathbf{z}^{(t)}
$$

其中**工作响应变量**为：

$$
\mathbf{z}^{(t)} = \mathbf{X}\mathbf{w}^{(t)} + (\mathbf{W}^{(t)})^{-1}(\mathbf{y} - \hat{\mathbf{p}}^{(t)})
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Eq. 4.23-4.26

**推导过程：**

$$
\text{Step 1: Newton 更新 } \mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \mathbf{H}^{-1}\mathbf{g}
$$
$$
\text{Step 2: 代入梯度 } \mathbf{g} = \frac{1}{N}\mathbf{X}^T(\hat{\mathbf{p}} - \mathbf{y})
$$
$$
\text{Step 3: 代入 Hessian } \mathbf{H} = \frac{1}{N}\mathbf{X}^T\mathbf{W}\mathbf{X}
$$
$$
\text{Step 4: } \mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - (\mathbf{X}^T\mathbf{W}\mathbf{X})^{-1}\mathbf{X}^T(\hat{\mathbf{p}} - \mathbf{y})
$$
$$
\text{Step 5: 令 } \mathbf{z} = \mathbf{X}\mathbf{w}^{(t)} + \mathbf{W}^{-1}(\mathbf{y} - \hat{\mathbf{p}}) \text{, 整理得 IRLS 形式}
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.99-4.100

---

### 公式 7: 正则化损失

**直觉：** 在原始损失上加惩罚项，限制权重大小，防止过拟合

$$
\mathcal{L}_{\text{reg}} = \mathcal{L} + \lambda \Omega(\mathbf{w})
$$

- **L2 (Ridge):** $\Omega(\mathbf{w}) = \frac{1}{2}\|\mathbf{w}\|_2^2 = \frac{1}{2}\sum_j w_j^2$
- **L1 (Lasso):** $\Omega(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_j |w_j|$
- **Elastic Net:** $\Omega(\mathbf{w}) = \rho\|\mathbf{w}\|_1 + \frac{1-\rho}{2}\|\mathbf{w}\|_2^2$

scikit-learn 用 $C = 1/\lambda$：

$$
\mathcal{L}_{\text{sklearn}} = \frac{1}{2}\|\mathbf{w}\|_2^2 + C\cdot\sum_{i} \text{loss}(y_i, \hat{p}_i)
$$

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.3.4 (L1/L2 理论) + Ch.4.4
> 📖 Docs: [scikit-learn Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

---

### 公式 8: Softmax (多分类扩展)

**直觉：** 将 K 个线性分数转化为概率分布——分数越高的类概率越大，所有类概率和为 1

$$
P(Y=k|\mathbf{x}) = \frac{\exp(\mathbf{w}_k^T\mathbf{x} + b_k)}{\sum_{j=1}^K \exp(\mathbf{w}_j^T\mathbf{x} + b_j)}
$$

交叉熵损失：

$$
\mathcal{L}_{\text{multi}} = -\frac{1}{N}\sum_{i=1}^N \sum_{k=1}^K \mathbf{1}[y_i = k]\log P(Y=k|\mathbf{x}_i)
$$

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Eq. 4.104
> 📚 Book: Murphy, [《PML1》](../../../textbooks/murphy_pml1.pdf), Ch.10.3

---


## 公式关系图

```
Sigmoid 函数 (公式1) ──→ 模型公式 (公式2: logit = wᵀx + b)
    │                         │
    │                         ▼
    │                    交叉熵损失 (公式3: NLL)
    │                         │
    ▼                         ├── 梯度 (公式4: X'(p̂-y))
Softmax (公式8)               │
  (多分类扩展)                 └── Hessian (公式5: X'WX)
                                      │
                                      ▼
                              IRLS 更新 (公式6: Newton-Raphson)
                                      │
                              正则化 (公式7: +λΩ(w))
```

---


## 手算练习

### 练习 1: 单步预测

**题目：** 给定 $\mathbf{w} = [0.5, -1.0]^T$, $b = 0.2$, 样本 $\mathbf{x} = [2, 1]^T$。

(a) 计算 $z$, $\hat{p}$, 和预测类别
(b) 若真实 $y=1$，计算该样本的交叉熵损失

**解答步骤：**

1. 计算线性组合: $z = 0.5 \times 2 + (-1.0) \times 1 + 0.2 = 1.0 - 1.0 + 0.2 = 0.2$
2. 代入 sigmoid: $\hat{p} = \sigma(0.2) = \frac{1}{1+e^{-0.2}} = \frac{1}{1+0.8187} = \frac{1}{1.8187} \approx 0.5498$
3. 预测类别: $\hat{p} = 0.5498 > 0.5$, 预测 $\hat{y} = 1$
4. 交叉熵损失: $-[1 \cdot \log(0.5498) + 0 \cdot \log(0.4502)] = -\log(0.5498) \approx 0.5981$

> 📚 Book: James et al., [《ISLR》](../../../textbooks/james_ISLR.pdf), Ch.4.3

### 练习 2: 梯度计算

**题目：** 沿用练习 1 的参数，计算对 $w_1$ 的梯度。

**解答步骤：**

1. 误差: $\hat{p} - y = 0.5498 - 1 = -0.4502$
2. 单样本梯度: $\frac{\partial \mathcal{L}}{\partial w_1} = (\hat{p} - y) \cdot x_1 = -0.4502 \times 2 = -0.9004$
3. 含义: 梯度为负，说明 $w_1$ 应该增大以减小损失（让 $\hat{p}$ 向 1 靠近）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

### 练习 3: Odds Ratio 解读

**题目：** 某 LR 模型中，特征"年龄"的系数 $w_{\text{age}} = 0.03$。如何解读？

**解答步骤：**

1. Odds Ratio: $e^{0.03} = 1.0305$
2. 解读: 年龄每增加 1 岁，事件发生的 odds 增加约 3.05%
3. 注意: 是 odds 增加，不是概率增加（odds 和概率是非线性关系）

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4

---


## 公式速查表

| 名称 | 公式 | 用途 | 前置公式 |
|------|------|------|---------| 
| Sigmoid | $\sigma(z) = \frac{1}{1+e^{-z}}$ | 将线性分数转概率 | 无 |
| 模型公式 | $\hat{p} = \sigma(\mathbf{w}^T\mathbf{x}+b)$ | 预测概率 | Sigmoid |
| 交叉熵 | $-\frac{1}{N}\sum[y\log\hat{p}+(1-y)\log(1-\hat{p})]$ | 损失函数 | 模型公式 |
| 梯度 | $\frac{1}{N}\mathbf{X}^T(\hat{\mathbf{p}}-\mathbf{y})$ | 优化方向 | 交叉熵 |
| Hessian | $\frac{1}{N}\mathbf{X}^T\mathbf{W}\mathbf{X}$ | 二阶优化 | 梯度 |
| IRLS | $(\mathbf{X}^T\mathbf{W}\mathbf{X})^{-1}\mathbf{X}^T\mathbf{W}\mathbf{z}$ | Newton 迭代 | Hessian |
| L2 正则 | $\mathcal{L}+\frac{\lambda}{2}\|\mathbf{w}\|_2^2$ | 防过拟合 | 交叉熵 |
| Softmax | $\frac{e^{z_k}}{\sum_j e^{z_j}}$ | 多分类扩展 | Sigmoid |

> 📚 Book: Hastie et al., [《ESL》](../../../textbooks/hastie_esl.pdf), Ch.4.4
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.4.3
