---
topic: neural_network
dimension: tutorial
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Rumelhart et al. 1986 — https://www.nature.com/articles/323533a0"
  - "📖 Docs: PyTorch Tutorials — https://pytorch.org/tutorials/"
expiry: 12m
status: current
---

# Neural Network (神经网络) 教程

> **前置知识：** 线性代数（矩阵乘法）、微积分（链式法则）、线性回归/逻辑回归
> **参考来源：** Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6

---

## Section 0: 前置知识速查

1. **矩阵乘法**：$\mathbf{C} = \mathbf{A}\mathbf{B}$，$C_{ij} = \sum_k A_{ik} B_{kj}$ — 理解"加权求和"的数学形式
2. **链式法则**：$\frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx}$ — 反向传播的数学基础
3. **逻辑回归**：$P(y=1|x) = \sigma(\mathbf{w}^T \mathbf{x} + b)$ — 可以看作"单个神经元"
4. **梯度下降**：$\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$ — 参数更新规则
5. **导数/偏导**：$\frac{\partial f}{\partial x_i}$ — 对单个变量求变化率

---

## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔥 **痛点 1：线性模型的天花板** — 线性回归和逻辑回归只能学习线性决策边界。现实中，图像分类、语音识别、自然语言处理都需要捕捉复杂的非线性关系。你可以手动设计特征（多项式特征、核方法），但这需要领域专家花大量时间，且效果有限。
- 🔥 **痛点 2：手动特征工程不可扩展** — 传统机器学习要求人类专家手动设计特征（如 SIFT、HOG）。每换一个任务就要重新设计，无法通用化。ImageNet 上 1000 个类别，手动设计特征不现实。
- 🔥 **痛点 3：组合爆炸** — 用查表法精确存储所有输入-输出映射？如果输入是 $256 \times 256$ 的图像，状态空间是 $256^{65536}$，根本不可能。

### 它的核心价值

1. **自动特征学习** — 网络自动从原始数据中提取层次化的特征表示，不需要人工设计
2. **万能近似能力** — 理论上可以逼近任意连续函数（UAT），足够灵活
3. **端到端训练** — 从原始输入到最终输出，整个管线可以用梯度下降一起优化
4. **可组合性** — 层可以自由组合：全连接层处理特征交互，卷积层处理空间结构，注意力层处理长距离依赖

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.1.2, Ch.6.1
> 📖 Paper: Hornik et al., [Universal Approximation Theorem](https://doi.org/10.1016/0893-6080(89)90020-8), 1989

---

## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 生命周期 / 流程图

```
┌────────────────────────────────────────────────────────────────┐
│                    神经网络训练全流程                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ 输入 x   │───→│  前向传播     │───→│  预测 ŷ      │          │
│  └─────────┘    │ z=Wx+b       │    └──────┬───────┘          │
│                 │ h=σ(z)       │           │                   │
│                 │ (逐层重复L次)  │           ↓                   │
│                 └──────────────┘    ┌──────────────┐           │
│                                    │  计算损失 L    │           │
│                                    │  L=Loss(ŷ,y)  │           │
│                                    └──────┬───────┘           │
│                                           │                   │
│  ┌──────────────┐    ┌──────────────┐     │                   │
│  │  更新参数      │←──│  反向传播     │←────┘                   │
│  │ θ←θ-η∇L      │    │ ∂L/∂W,∂L/∂b │                         │
│  └──────────────┘    │ (链式法则)    │                         │
│         │            └──────────────┘                         │
│         └──────────────→ 重复 epoch 次 ──────→ 训练完成         │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 核心机制

**为什么用层级结构而不是扁平结构？**

深层网络比宽浅网络更高效，原因在于**复合函数的表达力**。一个 $L$ 层网络可以表达 $O(2^L)$ 级别的线性区域划分，而单层网络只能表达 $O(M)$ 个（$M$ 是神经元数）。这意味着深度换来了**指数级的表达能力提升**。

**为什么需要非线性激活函数？**

如果所有层都是线性的：$f = W_L W_{L-1} \cdots W_1 \mathbf{x} = W' \mathbf{x}$，无论多少层，最终结果等价于一个矩阵乘法。非线性激活打破了这一限制，使得每一层能学习到**不同抽象层次的特征**。

**为什么反向传播能工作？**

反向传播利用了两个关键事实：
1. 损失函数关于参数是可微的（因为所有运算都是可微的基本运算的复合）
2. 链式法则可以高效复用中间结果——计算 $n$ 个参数的梯度，时间复杂度只是前向传播的常数倍

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.4–6.5
> 📖 Paper: Rumelhart et al., [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0), 1986

---

## Section 3: 局限性

1. **缺乏可解释性** — 深度网络是黑盒模型，无法简单解释"为什么做出这个预测"。→ 应对：LIME, SHAP, Attention Visualization 等事后解释方法
2. **需要大量数据** — 参数越多需要越多训练数据，否则过拟合。→ 应对：数据增强、迁移学习、正则化
3. **超参数敏感** — 学习率、网络结构、batch size 等超参数对结果影响大。→ 应对：网格搜索、贝叶斯优化、学习率调度
4. **计算资源需求** — 训练大模型需要 GPU/TPU，耗电耗时。→ 应对：模型压缩（剪枝/量化/蒸馏）
5. **对抗样本脆弱** — 微小的输入扰动可以导致完全错误的输出。→ 应对：对抗训练、输入预处理

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.7 (正则化), Ch.12 (应用)

---

## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **线性模型** (Linear/Logistic) | 简单、快速、可解释 | 只能线性分割 | 特征已工程化、数据量小 |
| **决策树 / 随机森林** | 可解释、对异常值鲁棒 | 外推能力差、不易处理高维连续数据 | 表格数据、需要解释性 |
| **SVM + 核方法** | 数学优美、小样本强 | 大规模数据慢、核函数选择困难 | 中等规模、特征维度适中 |
| **Neural Network** | 自动特征学习、端到端、万能近似 | 黑盒、需要大数据和算力 | 图像/语音/NLP、大规模数据 |
| **k-NN** | 无需训练、简单直觉 | 预测慢、维度灾难 | 小数据集、低维 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.5

---

## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------|
| [《Deep Learning》Ch.6](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 全文核心参考 |
| [《PRML》Ch.5](../../../textbooks/bishop_prml.pdf) | 📚 教科书 | Section 2 训练原理 |
| [Rumelhart et al. 1986](https://www.nature.com/articles/323533a0) | 📖 论文 | Section 2 反向传播 |
| [Hornik et al. 1989](https://doi.org/10.1016/0893-6080(89)90020-8) | 📖 论文 | Section 1 万能近似定理 |
| [PyTorch Tutorials](https://pytorch.org/tutorials/) | 📖 文档 | Section 2 实现参考 |
