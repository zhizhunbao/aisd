---
topic: loss_functions
dimension: first_principles
created: 2026-03-15
last_verified: 2026-03-15
source_versions:
  - "📚 Book: Goodfellow et al., 'Deep Learning' Ch.3, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, 'PRML' Ch.1, Ch.4 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
expiry: 12m
status: current
---

# Loss Functions 第一性原理

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3, Ch.6
> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1

---


## 核心问题链

### 问题链

1. **损失函数在做什么？** → 把模型预测 $\hat{y}$ 和真实值 $y$ 之间的差距映射为一个标量
2. **为什么要映射为标量？** → 因为优化器需要一个可微的标量函数来计算梯度——向量无法"最小化"
3. **为什么用特定的损失函数而不是随便定义一个？** → 因为损失函数隐含了概率假设——MSE 假设高斯噪声，CE 假设 Bernoulli/Categorical，错误的假设导致低效学习
4. **这个"概率假设"的根基是什么？** → MLE (最大似然估计)：找参数使数据出现的概率最大 → 最小化负对数似然 = 最小化损失
5. **MLE 的假设是什么？不能再拆分了吗？** → 数据 i.i.d. + 概率模型可微。这是统计推断的基本假设

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2

---


## 公理与基本假设

### 公理 1: 最大似然原理 (Maximum Likelihood Principle)

**陈述：** 最优的参数 $\theta^*$ 应使数据的对数似然最大：$\theta^* = \arg\max_\theta \sum\log P(y_i | x_i; \theta)$。

**白话：** 好的模型应该让"已经观察到的数据"在模型下出现的概率最大——用数据说话。

**来源：** Fisher, 1922。最大似然估计原理。当样本量趋于无穷时，MLE 是一致的、渐近有效的估计。

**可验证性：** MLE 的理论保证在样本量充足、模型包含真实分布时成立。

> 📚 Book: Bishop, [《PRML》](../../../textbooks/bishop_prml.pdf), Ch.1 §1.2.5

### 公理 2: 负对数似然等价于交叉熵 (NLL ≡ Cross-Entropy)

**陈述：** 最小化负对数似然 $-\sum\log q(y|x)$ 等价于最小化真实分布 $p$ 和模型分布 $q$ 的交叉熵 $H(p,q) = -\sum p \log q$。

**白话：** "让模型尽可能匹配数据"（MLE）和"让模型分布尽可能接近真实分布"（最小化交叉熵）是完全一回事。

**来源：** 信息论与统计学的交汇。Shannon (1948) + Kullback-Leibler (1951)。

**可验证性：** 当经验分布（训练数据）代替真实分布时严格成立。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3 §3.13, Ch.6 §6.2.1

### 公理 3: 输出层激活+损失联合设计消除梯度异常 (Co-design Principle)

**陈述：** 当输出层激活函数和损失函数从同一个概率分布的 MLE 推导出时，它们的组合梯度简化为 $\hat{y} - y$。

**白话：** Sigmoid 的导数 $\sigma'(z)$ 在 BCE 的梯度链中被完美抵消——这不是巧合，是 MLE 的数学结构必然产生的结果。

**来源：** 从指数族分布的充分统计量推导。Bernoulli → Sigmoid+BCE；Categorical → Softmax+CCE；Gaussian → Linear+MSE。

**可验证性：** 在上述三种配对中均可直接推导验证。配对错误的组合（如 Sigmoid+MSE）则不满足此性质。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6 §6.2.2

### 公理 4: 损失函数必须可微 (Differentiability Requirement)

**陈述：** 用于训练的损失函数必须关于模型参数几乎处处可微。

**白话：** 优化器依赖梯度来更新权重。如果 loss 不能算梯度（如 accuracy、0-1 loss），就无法用反向传播训练。

**来源：** 基于梯度的优化方法的前提条件。

**可验证性：** Accuracy = argmax 操作 → 不可微 → 只能当 metric 不能当 loss。所有常用 loss（MSE, CE, Huber）都满足此条件。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 从公理到技术的推导链

### Step 1: {公理 1} → 最优模型 = 最大化数据似然

**推理：** 由 MLE（公理 1），最优参数使 $\prod P(y_i|x_i;\theta)$ 最大。取对数：最大化 $\sum\log P(y_i|x_i;\theta)$。

**结果：** 训练目标 = 最小化负对数似然 $-\sum\log P(y_i|x_i;\theta)$。

### Step 2: {公理 2 + Step 1} → 回归用 MSE，分类用 CE

**推理：**
- 假设 $P(y|x) = \mathcal{N}(\hat{y}, \sigma^2)$ → $-\log P = \frac{1}{2\sigma^2}(y-\hat{y})^2 + \text{const}$ → **MSE**
- 假设 $P(y|x) = \text{Bernoulli}(\hat{y})$ → $-\log P = -[y\log\hat{y}+(1-y)\log(1-\hat{y})]$ → **BCE**
- 假设 $P(y|x) = \text{Cat}(\hat{y})$ → $-\log P = -\sum y_k\log\hat{y}_k$ → **CCE**

**结果：** 损失函数不是"拍脑袋"选的，而是由概率假设唯一确定的。

### Step 3: {公理 3 + Step 2} → 激活-损失配对消除梯度异常

**推理：** 由公理 3，Sigmoid+BCE 的梯度 = $\hat{y}-y$；Softmax+CCE 的梯度 = $\hat{y}_k-y_k$。Sigmoid 的饱和导数被 CE 的对数完美抵消。但 Sigmoid+MSE 不满足此性质 → 饱和区梯度消失。

**结果：** 必须使用匹配的激活-损失对。

### Step 4: {公理 4} → accuracy 不能当 loss

**推理：** accuracy 涉及 argmax（不可微），梯度为零或不存在。

**结果：** 训练用 CE（可微），评估用 accuracy（不可微但直观）。

### 推导链全景图

```
公理 1 (MLE) ─────────┐
                       ├──→ Step 1: 最小化负对数似然
公理 2 (NLL≡CE) ──────┘              │
                                      ├──→ Step 2: 高斯→MSE, Bernoulli→BCE
                                      │
公理 3 (联合设计) ──→ Step 3: Sigmoid+BCE 梯度=ŷ-y（消除饱和）
                                      │
公理 4 (可微性) ───→ Step 4: accuracy 不能当 loss
                                      │
                                      ▼
                          完整技术: Loss 选择原则
                          1. 回归=MSE, 分类=CE
                          2. 激活-损失必须配对
                          3. loss 必须可微
                          4. accuracy 只能当 metric
```

---


## 如果公理不成立？

### 公理 1 失效：MLE 假设不成立

**如果不成立：** 数据不是从模型族中的某个分布生成的；或样本量极小导致 MLE 过拟合。

**技术后果：** MLE 可能给出不合理的参数。Loss 下降但模型实际上没学好。

**替代方案：** 贝叶斯方法（加先验）、MAP 估计（= MLE + 正则化）、交叉验证选择损失函数。

### 公理 3 失效：激活-损失配对错误

**如果不成立：** 使用 Sigmoid+MSE 做分类。

**技术后果：** 梯度 $= 2(\hat{y}-y) \cdot \hat{y}(1-\hat{y})$。饱和区梯度 → 0。模型"自信地"犯错时无法纠正。

**替代方案：** 永远使用匹配的配对（Sigmoid+BCE, Softmax+CCE, Linear+MSE）。无例外。

### 公理 4 失效：hope 使用不可微的损失

**如果不成立：** 直接用 accuracy 或 0-1 loss 训练。

**技术后果：** 无法计算梯度 → 反向传播失败 → 需要无梯度优化方法。

**替代方案：** 进化算法、REINFORCE、代理损失（用可微的 CE 逼近不可微的 accuracy）。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 公理 1 MLE | 好参数 = 最大化数据似然 | 数据充足、模型包含真相 | 过拟合或次优解 |
| 公理 2 NLL≡CE | 最小化 NLL = 最小化交叉熵 | 经验分布代替真实分布 | 概念一致性丧失 |
| 公理 3 联合设计 | 配对的激活+loss 梯度 = ŷ-y | 从同一 MLE 推导 | 配对错误 → 梯度消失 |
| 公理 4 可微 | loss 必须能算梯度 | 使用连续可微函数 | 无法反向传播 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.3, Ch.6
