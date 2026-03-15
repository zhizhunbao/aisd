---
topic: differentiation
dimension: tutorial
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.4,6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML, Ch.4-5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Docs: PyTorch Autograd — https://pytorch.org/docs/stable/autograd.html"
expiry: 12m
status: current
---

# 微分 教程

> **前置知识：** 函数、极限、线性代数（向量/矩阵乘法）
> **参考来源：** [《MML》Ch.5](../../../textbooks/deisenroth_mml.pdf) | [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)

---


## Section 0: 前置知识速查

1. **函数 (Function)**：$y = f(x)$，给定输入返回唯一输出
2. **极限 (Limit)**：$\lim_{h\to 0} g(h) = L$，$h$ 无限趋近 0 时 $g(h)$ 趋近 $L$
3. **向量 (Vector)**：$\mathbf{x} = [x_1, \ldots, x_n]^\top \in \mathbb{R}^n$
4. **矩阵乘法**：$(AB)_{ij} = \sum_k A_{ik} B_{kj}$，Jacobian 的链式法则依赖矩阵乘法

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.2 (线性代数), Ch.5.1 (极限)

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **无法训练模型：** ML 训练 = 最小化损失函数。没有微分，就没有梯度 $\nabla_\theta L$，就不知道参数该往哪个方向调整——相当于蒙眼下坡
- 🔥 **无法理解"灵敏度"：** 模型输出对输入的改变多敏感？特征重要性怎么量化？没有导数就无法回答"小变化引起多大影响"
- 🔥 **丢失 2000 亿参数网络的可训练性：** 大语言模型有数十亿到万亿参数，没有高效的自动微分（反向传播），逐个参数试错不可能在有限时间内完成
- 🔥 **缺乏最优性条件：** 怎么知道找到了最优解？$\nabla f = 0$ 且 $\mathbf{H} \succ 0$ 是判断局部极小值的必要条件，全部依赖微分

### 它的核心价值

1. **提供优化方向：** 梯度 = 最陡上升方向 → 负梯度 = 最陡下降方向 → 梯度下降
2. **量化变化：** 导数精确描述"输入变一点点，输出变多少"
3. **使大规模训练可行：** 链式法则 + 计算图 = 反向传播，一次遍历算出所有参数的梯度

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5
> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 微分的层次体系

```
┌──────────────────────────────────────────────────────────────┐
│                微分的完整层次体系                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: 一元导数                                           │
│  ┌─────────────────┐                                         │
│  │ f'(x) = lim     │  一个输入，一个输出 → 一个数（斜率）      │
│  │ [f(x+h)-f(x)]/h│                                         │
│  └────────┬────────┘                                         │
│           │ 推广到多个变量                                     │
│           ▼                                                  │
│  Level 2: 偏导数 + 梯度                                      │
│  ┌─────────────────┐                                         │
│  │ ∂f/∂x_i         │  多个输入，一个输出 → 向量（梯度 ∇f）    │
│  └────────┬────────┘                                         │
│           │ 推广到多个输出                                     │
│           ▼                                                  │
│  Level 3: Jacobian                                           │
│  ┌─────────────────┐                                         │
│  │ J_ij=∂f_i/∂x_j  │  多个输入，多个输出 → 矩阵（J）         │
│  └────────┬────────┘                                         │
│           │ 推广到二阶                                        │
│           ▼                                                  │
│  Level 4: Hessian                                            │
│  ┌─────────────────┐                                         │
│  │ H_ij=∂²f/∂x_i∂j │  二阶偏导 → 矩阵（曲率信息）           │
│  └─────────────────┘                                         │
└──────────────────────────────────────────────────────────────┘
```

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5.1-5.4

### 2.2 链式法则如何驱动反向传播

**为什么不直接算每个参数的导数，而要用链式法则？** 因为深度网络是多层复合：$L = \ell(f_N(\cdots f_2(f_1(\mathbf{x}; \theta_1); \theta_2) \cdots))$。直接对 $\theta_k$ 求偏导需要展开所有中间步骤，极其复杂。链式法则将其分解为每层的局部导数的乘积。

```
前向传播 (Forward Pass):
    x → h₁ = f₁(x;θ₁) → h₂ = f₂(h₁;θ₂) → ... → hₙ = fₙ(hₙ₋₁;θₙ) → L = ℓ(hₙ)

反向传播 (Backward Pass) — 链式法则反向应用:
    ∂L/∂hₙ → ∂L/∂hₙ₋₁ = ∂L/∂hₙ · ∂hₙ/∂hₙ₋₁ → ... → ∂L/∂θₖ
    
    每层只需知道:
    1. 自己的局部梯度 ∂hₖ/∂hₖ₋₁ 和 ∂hₖ/∂θₖ
    2. 从上游传来的 ∂L/∂hₖ
```

**关键效率：** 前向传播 $O(N)$，反向传播也是 $O(N)$（$N$ = 参数量）。而且一次反向传播就能同时算出**所有参数**的梯度。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5, Algorithm 6.3

### 2.3 三种微分计算方式对比

**为什么用自动微分，不用数值微分或符号微分？**

- **数值微分** $\frac{f(x+h)-f(x-h)}{2h}$: 简单，但 $h$ 太大截断误差大、$h$ 太小舍入误差大。一个 $n$ 维梯度需要 $2n$ 次前向计算
- **符号微分** (SymPy): 精确，但表达式在复合函数中指数膨胀。无法处理 if/else 控制流
- **自动微分** (PyTorch/JAX): 精确（无近似误差）+ 高效（一次反向传播算所有梯度）+ 可处理程序控制流

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5.6-6.5.7

### 2.4 计算图：自动微分的数据结构

```
     示例: L = (w·x + b)²

     计算图:
     
     x ──→ [*] ──→ a = w·x ──→ [+] ──→ z = a+b ──→ [²] ──→ L = z²
     w ──↗                       b ──↗

     前向: x=2, w=3, b=1
     a = 3·2 = 6
     z = 6+1 = 7
     L = 7² = 49

     反向 (链式法则):
     ∂L/∂z = 2z = 14
     ∂L/∂b = ∂L/∂z · ∂z/∂b = 14·1 = 14
     ∂L/∂a = ∂L/∂z · ∂z/∂a = 14·1 = 14
     ∂L/∂w = ∂L/∂a · ∂a/∂w = 14·x = 14·2 = 28
     ∂L/∂x = ∂L/∂a · ∂a/∂x = 14·w = 14·3 = 42
```

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5.1

---


## Section 3: 局限性

1. **不可微点：** $|x|$ 在 $x=0$、ReLU 在 $x=0$ 处不可微。实践中用次梯度（subgradient）或"假设导数=0"绕过，但理论上梯度不存在
2. **梯度消失/爆炸：** 链式法则涉及多个 Jacobian 矩阵相乘。当层数很深时，梯度可能指数衰减（消失）或增长（爆炸）。→ 需要 BatchNorm、ResNet、梯度裁剪
3. **二阶方法计算代价大：** Hessian 存储 $O(n^2)$、求逆 $O(n^3)$，对大模型（$n \sim 10^9$）不可行。→ 只能用一阶方法 (SGD/Adam) 或 Hessian 近似 (L-BFGS)
4. **离散目标不可微：** 分类准确率 (accuracy)、BLEU 分数等离散指标不可微。→ 需要用可微代理损失（交叉熵、CTC）或策略梯度 (REINFORCE)

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.2 (梯度消失)
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9 (二阶方法代价)

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **梯度下降 (一阶)** | 简单、内存少、可并行 | 收敛慢（线性收敛） | 大规模 DL 训练 |
| **牛顿法 (二阶)** | 快速收敛（二次收敛） | Hessian 代价 $O(n^3)$ | 小规模凸优化 |
| **L-BFGS (拟牛顿)** | 近似二阶、无需显式 Hessian | 需全批数据 | 中等规模、full-batch |
| **Adam (自适应一阶)** | 自适应学习率、鲁棒 | 可能不收敛到最优 | DL 训练标准选择 |
| **次梯度法** | 处理不可微函数 | 收敛很慢 | L1 正则化等 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《MML》Ch.5](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 全文核心（导数定义、梯度、Jacobian、Hessian） |
| [《Deep Learning》Ch.4,6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 反向传播、计算图、自动微分 |
| [《PRML》Ch.4-5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | 梯度在分类/回归中 |
| [《Convex Opt》Ch.2-3,9](../../../textbooks/boyd_convex_optimization.pdf) | 📚 教科书 | Hessian、凸性、优化方法 |
| [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html) | 📖 文档 | Section 2 (自动微分实现) |
