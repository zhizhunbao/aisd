---
topic: differentiation
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Boyd & Vandenberghe, Convex Optimization, Ch.2-3 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
expiry: 12m
status: current
---

# 微分 第一性原理

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5
> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **微分在做什么？** → 计算函数在某点的瞬时变化率（导数 / 梯度）
2. **为什么需要瞬时变化率？** → 为了知道最小化损失函数时参数应该往哪个方向调整
3. **为什么"方向信息"能帮助优化？** → 因为函数在局部可以用线性函数 $f(x+\delta) \approx f(x) + f'(x)\delta$ 近似——小范围内变化是可预测的
4. **为什么函数局部可以线性近似？** → 因为**光滑函数（可微函数）在足够小的尺度下行为像直线**——这是可微性的定义
5. **可微性的根基是什么？** → **实数的序结构 + 极限的存在性**——极限 $\lim_{h\to 0}$ 能收敛到确定值（实数完备性）

> 📚 Book: 实分析（可微性定义）

---


## 公理与基本假设

> 列出本技术赖以成立的**不可再分的基本事实**。

### 公理 1: 函数的局部线性近似性（可微性）

**陈述：** 函数 $f$ 在 $x_0$ 可微，当且仅当存在线性映射 $L$ 使得 $f(x_0 + h) = f(x_0) + L(h) + o(\|h\|)$，即误差比 $h$ 收敛到零的速度更快。

**白话：** 如果你把函数"放大"到足够小的范围，它看起来就像一条直线（一维）或一个平面（多维）。导数就是这条"局部直线"的斜率。

**来源：** 微分的现代定义（Fréchet 导数），是微积分的数学基础。

**可验证性：** 对所有初等函数在其定义域内部成立。在不连续点（跳跃）或尖角处（如 $|x|$ 在 $x=0$）不成立。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1

### 公理 2: 极限的存在性与唯一性（实数完备性）

**陈述：** 在实数系 $\mathbb{R}$ 中，$\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ 如果存在，则唯一。

**白话：** 无论从左边还是右边趋近，"差商"的极限都收敛到同一个值。实数轴上"没有空隙"保证了这一点。

**来源：** 实数完备性公理（同积分的公理 1）。

**可验证性：** 在 $\mathbb{R}$ 中永远成立。在有理数 $\mathbb{Q}$ 中可能不成立（极限值可能不在 $\mathbb{Q}$ 中）。

> 📚 Book: 实分析基础

### 公理 3: 链式法则的复合性（函数复合的可微性）

**陈述：** 如果 $g$ 在 $x$ 可微，$f$ 在 $g(x)$ 可微，则 $f \circ g$ 在 $x$ 可微，且 $(f \circ g)'(x) = f'(g(x)) \cdot g'(x)$。

**白话：** 可微函数的复合仍然可微，而且复合的导数就是各层导数的乘积。这保证了深度网络（多层复合）的梯度一定可以逐层计算。

**来源：** 链式法则定理，从可微性定义直接推导。

**可验证性：** 只要每层函数可微，就成立。ReLU 在 $x=0$ 处不可微，但 $x=0$ 的概率为零（连续分布），实践中不影响。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2

### 公理 4: 梯度是最速上升方向

**陈述：** 对可微函数 $f: \mathbb{R}^n \to \mathbb{R}$，方向导数 $D_\mathbf{u}f = \nabla f \cdot \mathbf{u}$ 在 $\mathbf{u} = \nabla f / \|\nabla f\|$ 时取最大值。

**白话：** 在所有单位方向中，沿梯度方向函数增长最快。所以"负梯度方向 = 最快下降方向"是梯度下降的数学依据。

**来源：** 柯西-施瓦茨不等式 $|\mathbf{a} \cdot \mathbf{b}| \leq \|\mathbf{a}\|\|\mathbf{b}\|$，等号当且仅当 $\mathbf{a} \parallel \mathbf{b}$。

**可验证性：** 对任何可微函数成立。但"最速下降方向"只是局部最优——全局来看，梯度下降不保证到达全局最小值。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.2
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9.3

---


## 从公理到技术的推导链

### Step 1: {从公理 1 (可微性) + 公理 2 (极限)} → {导数存在且唯一}

**推理：** 函数的局部线性近似性（公理 1）保证差商 $\frac{f(x+h)-f(x)}{h}$ 在 $h \to 0$ 时有极限。实数完备性（公理 2）保证这个极限值唯一且是实数。

**结果：** 导数 $f'(x)$ 是一个良定义的实数——函数在该点的唯一变化率。

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1

### Step 2: {从 Step 1 + 公理 3 (链式法则)} → {反向传播算法}

**推理：** 深度网络 $L = f_N(\cdots f_1(\mathbf{x}) \cdots)$ 是多层可微函数的复合。公理 3 保证复合函数可微，且梯度可以通过逐层乘以局部 Jacobian 来计算：$\frac{\partial L}{\partial \theta_k} = \frac{\partial L}{\partial \mathbf{h}_N} \cdot \prod_{j=k+1}^{N} \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} \cdot \frac{\partial \mathbf{h}_k}{\partial \theta_k}$。

**结果：** 反向传播算法——从输出到输入逐层计算梯度，时间复杂度 $O(1)$ 倍前向传播。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

### Step 3: {从 Step 2 + 公理 4 (梯度=最速方向)} → {梯度下降训练}

**推理：** 反向传播给出梯度 $\nabla_\theta L$。公理 4 保证负梯度方向是损失在局部下降最快的方向。因此 $\theta \leftarrow \theta - \eta \nabla_\theta L$ 在步长足够小时保证损失减小。

**结果：** 梯度下降训练——深度学习的核心优化循环。

> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9.3

### 推导链全景图

```
公理 1 (可微性) ────┐
                    ├──→ 导数存在且唯一 ──┐
公理 2 (极限唯一) ──┘                     │
                                          ├──→ 反向传播 ──→ 梯度下降训练
公理 3 (链式法则) ──→ 复合函数可逐层求导 ──┘        │
                                                    │
公理 4 (最速方向) ──→ 负梯度 = 最优下降方向 ────────┘
```

---


## 如果公理不成立？

### 公理 1 失效：函数不可微

**如果不成立：** 函数有尖角（$|x|$ 在 $x=0$）、阶跃（$\text{sign}(x)$）或分形结构

**技术后果：** 导数不存在，梯度下降无法直接使用。BP 在不可微点"卡住"或产生未定义行为。

**替代方案：**
- **次梯度 (Subgradient)**：对凸函数的推广，在不可微点取"所有可能斜率"的集合
- **Straight-Through Estimator (STE)**：二值化网络的常用技巧——前向用不可微操作，反向"假装"可微
- **Gumbel-Softmax**：用连续放松近似离散采样
- **REINFORCE / 策略梯度**：用采样估计不可微目标的梯度

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.20

### 公理 2 失效：极限不存在

**如果不成立：** 函数在某点"左导数 ≠ 右导数"（如 $|x|$ 在 $x=0$），或函数处处振荡不收敛（如 Weierstrass 函数处处连续但处处不可微）

**技术后果：** 导数无法定义。梯度下降的"方向"无法确定。

**替代方案：** 光滑化——用可微的近似函数替代（如 $|x| \approx \sqrt{x^2 + \epsilon}$，SoftPlus 近似 ReLU）

> 📚 Book: 实分析（Weierstrass 反例）

### 公理 3 失效：复合不可微（某层不可微）

**如果不成立：** 网络某层使用了不可微操作（如硬阈值 $\mathbb{1}[x > 0]$、argmax、排序）

**技术后果：** 链式法则在该层断裂，梯度无法从该层继续传播。

**替代方案：**
- STE：在反向传播时"跳过"不可微层
- 可微松弛：用 Softmax 代替 argmax，用 Soft-sort 代替排序
- 策略梯度：把不可微操作视为"随机策略"，用 REINFORCE 估计梯度

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.20

### 公理 4 失效：梯度方向不是全局最优

**如果不成立：** 梯度只是**局部**最速方向。对非凸函数（如深度网络的损失面），梯度下降可能陷入局部极小值或鞍点。

**技术后果：** 训练停滞在次优解（实践中，大模型的鞍点问题比局部极小值更严重）。

**替代方案：**
- **动量 (Momentum)**：加入"惯性"帮助逃离浅鞍点
- **Adam/AdaGrad**：自适应学习率，不同参数不同步长
- **随机梯度 (SGD)**：噪声本身帮助逃离尖锐极小值
- **学习率调度**：Warm-up + 衰减，平衡探索与收敛

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.2-8.5
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|----------|---------|---------|
| 可微性 | 函数局部可线性近似 | 光滑函数（无尖角/跳跃） | 导数不存在，需次梯度/STE |
| 极限唯一性 | 差商极限存在且唯一 | 实数完备性 | 导数无法定义 |
| 链式法则 | 复合函数可逐层求导 | 每层可微 | BP 断裂，用可微松弛 |
| 最速方向 | 负梯度 = 局部最快下降 | 凸函数全局成立 | 非凸: 鞍点/局部极小值 |

> 📚 Book: 综合以上来源
