---
topic: optimizers
dimension: math
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Kingma & Ba, 'Adam: A Method for Stochastic Optimization', ICLR 2015 — https://arxiv.org/abs/1412.6980"
  - "📖 Paper: Duchi et al., 'Adaptive Subgradient Methods', JMLR 2011"
expiry: 12m
status: current
---

# Optimizers 数学基础

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015

---


## 符号对照表

| 符号 | 含义（白话） | 英文 | 取值范围 |
|------|-------------|------|---------|
| $W$ 或 $\theta$ | 模型的所有可学习参数 | parameters / weights | $\mathbb{R}^d$ |
| $\eta$ | 学习率（步长） | learning rate | 通常 $10^{-4}$ 到 $10^{-1}$ |
| $\nabla L$ 或 $g_t$ | 第 $t$ 步的梯度 | gradient at step $t$ | $\mathbb{R}^d$ |
| $L$ | 损失函数 | loss function | $\mathbb{R}^+$ |
| $v_t$ | 动量向量（速度） | velocity / momentum | $\mathbb{R}^d$ |
| $m_t$ | 一阶矩估计（梯度均值） | first moment estimate | $\mathbb{R}^d$ |
| $s_t$ 或 $v_t^{(\text{Adam})}$ | 二阶矩估计（梯度方差） | second moment estimate | $\mathbb{R}^d$ |
| $\beta$ | 动量系数 | momentum coefficient | 通常 0.9 |
| $\beta_1$ | Adam 一阶矩衰减系数 | first moment decay | 通常 0.9 |
| $\beta_2$ | Adam 二阶矩衰减系数 | second moment decay | 通常 0.999 |
| $\epsilon$ | 数值稳定性常数 | epsilon for stability | 通常 $10^{-8}$ |
| $t$ | 当前训练步数 | time step | $\mathbb{Z}^+$ |
| $G_t$ | AdaGrad 累积梯度平方和 | accumulated squared gradients | $\mathbb{R}^d$, 非负 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---


## 核心公式

### 公式 1: Vanilla SGD（随机梯度下降）

**直觉：** 沿着"下坡"最陡的方向（负梯度方向）走一小步。最简单的优化：看到坡就往下走。

$$
W_{t+1} = W_t - \eta \cdot g_t
$$

其中 $g_t = \nabla_W L(W_t; x^{(i)}, y^{(i)})$，是用 mini-batch 数据计算的梯度。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.3, Algorithm 8.1

**参数解释：**
| 参数 | 含义 | 典型值 |
|------|------|--------|
| $\eta$ | 学习率 | 0.01 |
| $g_t$ | 当前梯度 | 依数据而定 |

**问题：** 1) 所有参数用同一个学习率 2) 在鞍点/平坦区域极慢 3) mini-batch 梯度有噪声→路径震荡。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.3

---

### 公式 2: SGD with Momentum（动量 SGD）

**直觉：** 给"球"加上惯性——即使当前梯度在震荡，历史累积的"速度"依然推着球沿主方向前进，像在深谷中滑行。

$$
v_{t+1} = \beta \cdot v_t + g_t
$$
$$
W_{t+1} = W_t - \eta \cdot v_{t+1}
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.3.2, Algorithm 8.2

**推导为什么 Momentum 加速收敛：**

$$
\text{Step 1: 展开 } v_{t+1} = g_t + \beta g_{t-1} + \beta^2 g_{t-2} + \cdots
$$
$$
\text{Step 2: 如果梯度方向一致（沿谷底），各项叠加 → 加速}
$$
$$
\text{Step 3: 如果梯度方向交替（垂直谷壁），正负相消 → 抑制震荡}
$$

**结论：** Momentum 在一致方向上加速（指数累积），在震荡方向上减速（正负抵消），自动放大"主方向"并抑制"噪声方向"。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.3.2

---

### 公式 3: AdaGrad（自适应梯度）

**直觉：** 给每个参数"量体裁衣"的学习率——更新频繁的参数学习率自动变小（因为已经学了很多），更新稀疏的参数学习率保持大（因为还没学够）。

$$
G_t = G_{t-1} + g_t^2 \quad \text{(逐元素平方和累积)}
$$
$$
W_{t+1} = W_t - \frac{\eta}{\sqrt{G_t + \epsilon}} \cdot g_t
$$

> 📖 Paper: Duchi et al., "Adaptive Subgradient Methods", JMLR 2011

**问题：** $G_t$ 只增不减 → 学习率单调递减 → 训练后期学习率 → 0，提前停止学习。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.5.1

---

### 公式 4: RMSprop

**直觉：** AdaGrad 的修复版——用"滑动窗口"代替"全部累积"，只看最近的梯度大小来调整学习率，避免学习率衰减到零。

$$
s_t = \beta_2 \cdot s_{t-1} + (1 - \beta_2) \cdot g_t^2
$$
$$
W_{t+1} = W_t - \frac{\eta}{\sqrt{s_t + \epsilon}} \cdot g_t
$$

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.5.2

**关键区别：** 用 $\beta_2$（通常 0.9 或 0.999）做指数加权移动平均，而非 AdaGrad 的简单累加。旧的梯度信息会被自动"遗忘"。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.5.2

---

### 公式 5: Adam（自适应矩估计）⭐ 最常用

**直觉：** 融合"动量"（我一直在往哪走）和"RMSprop"（每个参数的梯度有多大波动），再加上偏差修正（训练初期估计不准，需要补偿）。

$$
m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t \qquad \text{(一阶矩：梯度均值估计)}
$$
$$
v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2 \qquad \text{(二阶矩：梯度方差估计)}
$$
$$
\hat{m}_t = \frac{m_t}{1 - \beta_1^t} \qquad \text{(偏差修正：补偿初始零值)}
$$
$$
\hat{v}_t = \frac{v_t}{1 - \beta_2^t} \qquad \text{(偏差修正)}
$$
$$
W_{t+1} = W_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \cdot \hat{m}_t
$$

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015, Algorithm 1

**推导为什么需要偏差修正：**

$$
\text{Step 1: } m_0 = 0 \text{ (初始化为零)}
$$
$$
\text{Step 2: } m_1 = \beta_1 \cdot 0 + (1-\beta_1) g_1 = (1-\beta_1) g_1
$$
$$
\text{Step 3: } E[m_1] = (1-\beta_1) E[g_1] \neq E[g_1] \text{ (有偏！)}
$$
$$
\text{Step 4: 修正: } \hat{m}_1 = \frac{m_1}{1-\beta_1^1} = \frac{(1-\beta_1)g_1}{1-\beta_1} = g_1 \text{ ✅ 无偏}
$$

> 📖 Paper: Kingma & Ba, ICLR 2015, §3

---

### 公式 6: L-BFGS（有限内存拟牛顿法）

**直觉：** 牛顿法用曲率信息（Hessian 矩阵）来"预判"最优方向，比梯度下降走更少的步就能到达。L-BFGS 用有限的历史梯度来*近似*这个曲率，节省内存。

$$
W_{t+1} = W_t - H_t^{-1} \cdot g_t
$$

其中 $H_t^{-1}$ 是 Hessian 的近似逆。L-BFGS 不直接存储 $H_t$，而是存储最近 $m$ 步的 $\{s_k, y_k\}$ 对来隐式计算（two-loop recursion）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.6

---


## 公式关系图

```
                Vanilla SGD: W ← W - η∇L
                     │
         ┌───────────┼───────────┐
         ▼                       ▼
  Momentum SGD              AdaGrad
  (加动量累积)           (自适应 per-param lr)
         │                       │
         │                       ▼
         │                   RMSprop
         │              (修复 AdaGrad 衰减)
         │                       │
         └───────────┬───────────┘
                     ▼
                   Adam
          (Momentum + RMSprop + 偏差修正)
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
           AdamW   NAdam   AMSGrad
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

---


## 手算练习

### 练习 1: Vanilla SGD 一步更新

**题目：** 参数 $W = 5.0$，梯度 $g = 2.0$，学习率 $\eta = 0.1$。计算更新后的 $W$。

**解答步骤：**

1. $W_{\text{new}} = W - \eta \cdot g = 5.0 - 0.1 \times 2.0 = 5.0 - 0.2 = 4.8$
2. 参数从 5.0 减小到 4.8，沿梯度反方向移动了 0.2

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### 练习 2: Adam 一步更新

**题目：** $W=1.0$, $g=0.5$, $\beta_1=0.9$, $\beta_2=0.999$, $\eta=0.001$, $\epsilon=10^{-8}$, $t=1$（第一步）, $m_0=0$, $v_0=0$。

**解答步骤：**

1. 一阶矩：$m_1 = 0.9 \times 0 + 0.1 \times 0.5 = 0.05$
2. 二阶矩：$v_1 = 0.999 \times 0 + 0.001 \times 0.25 = 0.00025$
3. 偏差修正 $m$：$\hat{m}_1 = \frac{0.05}{1 - 0.9^1} = \frac{0.05}{0.1} = 0.5$
4. 偏差修正 $v$：$\hat{v}_1 = \frac{0.00025}{1 - 0.999^1} = \frac{0.00025}{0.001} = 0.25$
5. 更新：$W_1 = 1.0 - \frac{0.001}{\sqrt{0.25} + 10^{-8}} \times 0.5 = 1.0 - \frac{0.001}{0.5} \times 0.5 = 1.0 - 0.001 = 0.999$
6. 注意：偏差修正将 $m_1=0.05$ 修正回 $0.5$（= 原始梯度），消除了初始化为零带来的偏差

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015

---


## 公式速查表

| 名称 | 更新规则 | 关键超参数 | 前置公式 |
|------|---------|-----------|---------|
| SGD | $W - \eta g$ | $\eta$ | 无 |
| Momentum | $v = \beta v + g$; $W - \eta v$ | $\eta, \beta$ | SGD |
| AdaGrad | $G += g^2$; $W - \frac{\eta}{\sqrt{G+\epsilon}} g$ | $\eta, \epsilon$ | SGD |
| RMSprop | $s = \beta_2 s + (1-\beta_2)g^2$; $W - \frac{\eta}{\sqrt{s+\epsilon}} g$ | $\eta, \beta_2$ | AdaGrad |
| Adam | $m$, $v$, 偏差修正; $W - \frac{\eta}{\sqrt{\hat{v}}+\epsilon} \hat{m}$ | $\eta, \beta_1, \beta_2$ | Momentum + RMSprop |
| L-BFGS | $W - H^{-1}g$ | $m$ (历史步数) | 牛顿法 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
