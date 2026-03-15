---
topic: optimizers
dimension: first_principles
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Boyd, 'Convex Optimization' Ch.9 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
  - "📖 Paper: Kingma & Ba, 'Adam', ICLR 2015 — https://arxiv.org/abs/1412.6980"
expiry: 12m
status: current
---

# Optimizers 第一性原理

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **优化器在做什么？** → 迭代更新参数 $W$，使损失函数 $L(W)$ 尽可能小
2. **为什么用迭代而不是直接求解？** → 因为深度学习的损失函数是高维非凸的，不存在解析解（closed-form solution）
3. **为什么沿梯度反方向更新？** → 因为负梯度是函数值下降最快的方向（一阶泰勒展开的最优方向）
4. **这个"最快下降"的根基是什么？** → 泰勒定理：$L(W + \Delta W) \approx L(W) + \nabla L^T \Delta W$，取 $\Delta W = -\eta \nabla L$ 时内积最小（柯西-施瓦茨不等式）
5. **泰勒定理的前提是什么？** → 函数可微（存在梯度）——这是不可再分的公理

> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---


## 公理与基本假设

### 公理 1: 损失函数可微 (Differentiability of Loss Function)

**陈述：** 损失函数 $L(W)$ 关于参数 $W$ 几乎处处可微，存在梯度 $\nabla L(W)$。

**白话：** 损失"地表"是光滑的——在任何一点都能算出"哪个方向是下坡"。

**来源：** 微积分基本假设。网络中使用的激活函数（Sigmoid, ReLU 等）和损失函数（MSE, Cross-Entropy）几乎处处可微。

**可验证性：** ReLU 在 $z=0$ 不可微，但次梯度在实践中有效。几乎所有深度学习的组件都满足"几乎处处可微"。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.5

### 公理 2: 负梯度是局部最快下降方向 (Gradient is Steepest Descent Direction)

**陈述：** 在一阶泰勒近似下，$\Delta W = -\eta \nabla L$ 使得 $L(W + \Delta W)$ 的下降量最大化。

**白话：** 如果只看"眼前一步"，跟着负梯度走是减小 loss 最快的方向。

**来源：** 柯西-施瓦茨不等式：$\nabla L^T \Delta W \geq -\|\nabla L\| \|\Delta W\|$，等号当 $\Delta W \propto -\nabla L$ 时取到。

**可验证性：** 仅在步长足够小时严格成立。步长过大时，二阶及以上项不可忽略，一阶近似失效。

> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

### 公理 3: 随机梯度是全量梯度的无偏估计 (Unbiased Gradient Estimation)

**陈述：** Mini-batch 上计算的梯度 $g_t = \nabla L(W; x^{(i)}, y^{(i)})$ 满足 $E[g_t] = \nabla L(W)$。

**白话：** 虽然每次只用一小批数据算梯度，但平均来看，方向是正确的。随机的"噪声"在期望上被消除。

**来源：** 概率论中期望的线性性。损失函数是所有样本损失的平均，子集的期望等于全集的平均。

**可验证性：** 需要数据是独立同分布采样的（i.i.d.）。在线学习中如果数据分布变化，此假设可能不完全成立。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8 §8.1.3

### 公理 4: 参数的最优学习率与曲率成反比 (Learning Rate and Curvature)

**陈述：** 对于参数 $w_i$，最优的学习率 $\propto \frac{1}{H_{ii}}$，其中 $H_{ii}$ 是 Hessian 矩阵的对角元素。

**白话：** 损失地表越"陡"的方向应该走越小的步，越"平"的方向应该走越大的步。这就是"自适应学习率"的理论基础。

**来源：** 牛顿法的更新规则 $\Delta W = -H^{-1} \nabla L$ 中，Hessian 的逆矩阵天然提供了曲率自适应。

**可验证性：** 精确的 Hessian 计算代价为 $O(d^2)$，深度学习中 $d$ 可达数十亿，不可行。Adam 的二阶矩是对角 Hessian 的"粗糙近似"。

> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---


## 从公理到技术的推导链

### Step 1: {公理 1} → 可以用梯度来指导更新

**推理：** 因为损失函数可微（公理 1），梯度 $\nabla L(W)$ 存在且可计算（通过反向传播）。

**结果：** 得到了更新方向的信息。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### Step 2: {公理 2} → 沿负梯度更新可以减小 loss

**推理：** 由公理 2，$-\nabla L$ 是局部最快下降方向。取 $W_{new} = W - \eta \nabla L$。

**结果：** 得到 Vanilla SGD 的更新规则。

> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

### Step 3: {公理 3} → 可以用 mini-batch 近似

**推理：** 由公理 3，mini-batch 梯度是全量梯度的无偏估计。用 $g_t$ 替代 $\nabla L$ 仍可收敛。

**结果：** SGD 可以在大数据集上高效训练。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### Step 4: {公理 4 + SGD 的缺陷} → 需要自适应学习率

**推理：** SGD 用全局 $\eta$，但公理 4 告诉我们每个参数的最优 $\eta$ 不同（与曲率成反比）。Adam 用二阶矩 $v_t$ 近似曲率，实现 per-parameter 自适应：$\eta_i \propto \frac{1}{\sqrt{v_t^{(i)}}}$。

**结果：** 得到 Adam 的核心设计原理——自适应学习率是对牛顿法的"轻量近似"。

> 📖 Paper: Kingma & Ba, [Adam](https://arxiv.org/abs/1412.6980), ICLR 2015

### 推导链全景图

```
公理 1 (可微) ─────┐
                   ├──→ Step 1-2: Vanilla SGD (W = W - η∇L)
公理 2 (最快下降) ─┘                    │
                                        │
公理 3 (无偏估计) ──→ Step 3: mini-batch SGD (可扩展) ──┐
                                                        │
公理 4 (曲率∝1/lr) ──→ Step 4: 自适应 lr 必要 ──────────┤
                                                        ▼
                                              Adam = Momentum + RMSprop
                                              (一阶矩 + 二阶矩 + 偏差修正)
```

---


## 如果公理不成立？

### 公理 1 失效：损失函数不可微

**如果不成立：** 激活函数不可微（如硬阈值/阶跃函数），或损失函数不可微（如 0-1 loss）

**技术后果：** 无法计算梯度 → 反向传播无法使用 → 所有基于梯度的优化器失效

**替代方案：** 次梯度法（subgradient）、进化算法（genetic algorithm）、强化学习中的 REINFORCE（不需要可微）、Straight-Through Estimator（STE）

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

### 公理 3 失效：mini-batch 梯度有偏

**如果不成立：** 数据不是 i.i.d. 采样（如时序数据相邻样本高度相关），或 batch 内数据分布与全局分布不同

**技术后果：** 梯度估计有偏 → SGD 不收敛到正确解 → 训练不稳定

**替代方案：** 数据打乱（shuffle）、经验回放（replay buffer，如 DQN）、分布式训练中的同步 SGD

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8

### 公理 4 失效：曲率信息不可靠

**如果不成立：** 非凸损失地表的 Hessian 可能有负特征值（鞍点）、Hessian 计算量太大无法获取

**技术后果：** Adam 的二阶矩只是对角 Hessian 的粗略近似，在某些方向上可能给出错误的 lr → Adam 的泛化有时不如 SGD

**替代方案：** Full-batch 训练 + 实际 Hessian（小模型）、K-FAC（分块近似 Hessian）、SGD + 人工调参（放弃自适应）

> 📖 Paper: Kingma & Ba, ICLR 2015; Wilson et al., NeurIPS 2017

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 公理 1 可微 | 损失函数几乎处处可微 | 使用连续激活/损失函数 | 无法反向传播 |
| 公理 2 最快下降 | 负梯度是局部最快下降方向 | 步长足够小 | 大步长时一阶近似失效 |
| 公理 3 无偏估计 | mini-batch 梯度 $E[g_t] = \nabla L$ | 数据 i.i.d. 采样 | SGD 不收敛 |
| 公理 4 曲率∝1/lr | 最优 lr 与 Hessian 对角成反比 | 凸或近凸区域 | Adam 的自适应 lr 可能不准 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📚 Book: Boyd, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9
