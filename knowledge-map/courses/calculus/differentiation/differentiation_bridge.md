---
topic: differentiation
dimension: bridge
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Deisenroth et al., Mathematics for Machine Learning, Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/deisenroth_mml.pdf"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.4,6,8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Boyd & Vandenberghe, Convex Optimization — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/boyd_convex_optimization.pdf"
expiry: 12m
status: current
---

# 微分 衔接与扩展

> 📚 Book: Deisenroth et al., [《Mathematics for Machine Learning》](../../../textbooks/deisenroth_mml.pdf), Ch.5

---

## ← 上一个概念 / 下一个概念 →

| 方向 | 主题 | 关系 | 链接 |
|------|------|------|------|
| ← 前置 | 极限 (Limits) | 导数定义依赖极限 | — |
| ← 前置 | 函数 (Functions) | 微分的对象 | — |
| ← 前置 | 线性代数 (Linear Algebra) | Jacobian/Hessian 是矩阵；链式法则是矩阵乘法 | — |
| → 后续 | 积分与求和 (Integration & Summation) | 积分是微分的逆运算 | [integration_summation_map.md](../integration_summation/integration_summation_map.md) |
| → 后续 | 梯度下降 / 优化 (Optimization) | 微分提供梯度，优化使用梯度 | — |
| → 后续 | 反向传播 (Backpropagation) | 链式法则的计算实现 | — |
| → 后续 | 卷积 (Convolution) | 卷积层的梯度计算 | [convolution_map.md](../convolution/convolution_map.md) |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.5

---

## 上游依赖

| 来自主题 | 复用的概念 | 在本主题中如何使用 |
|---------|-----------|-------------------|
| 极限 (Limits) | $\lim_{h\to 0}$ | 导数的定义 $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ |
| 函数 (Functions) | 复合函数 $f \circ g$ | 链式法则处理的对象 |
| 线性代数 | 矩阵乘法 | 多元链式法则 = Jacobian 矩阵乘法；Hessian 是对称矩阵 |
| 线性代数 | 特征值/特征向量 | Hessian 的特征值决定曲率方向和凸性 |

> 📚 Book: Deisenroth et al., [《MML》](../../../textbooks/deisenroth_mml.pdf), Ch.2, Ch.5

---

## 下游影响

| 去向主题 | 本主题提供的概念 | 在下游如何被使用 |
|---------|----------------|----------------|
| 梯度下降 | 梯度 $\nabla L$ | $\theta \leftarrow \theta - \eta \nabla L$（参数更新） |
| 反向传播 | 链式法则 | 深度网络逐层计算损失对参数的梯度 |
| 牛顿法 / L-BFGS | Hessian $\mathbf{H}$ | 二阶优化：$\theta \leftarrow \theta - \mathbf{H}^{-1}\nabla L$ |
| 积分 | 微积分基本定理 | $\int_a^b f(x)\,dx = F(b)-F(a)$，微分提供 $F$ |
| 概率 | 对数导数 | Score function $\nabla_\theta \log p(x|\theta)$ |
| 变分推断 | 重参数化梯度 | $\nabla_\phi \mathcal{L} = E[\nabla_\phi f(\epsilon, \phi)]$（VAE） |
| 正则化 | 梯度惩罚 | Gradient penalty in WGAN-GP |
| 物理仿真 | 可微渲染/仿真 | 物理引擎的梯度反传 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6, 8, 20
> 📚 Book: Boyd & Vandenberghe, [《Convex Optimization》](../../../textbooks/boyd_convex_optimization.pdf), Ch.9

---

## 概念演变追踪

| 概念 | 在早期/旧版中 | 在现代/新版中 | 变化 |
|------|-------------|-------------|------|
| 求导方式 | 手动推导 + 查表 | 自动微分框架（PyTorch/JAX） | 从人工到自动 |
| 梯度计算 | 手动实现每层的梯度公式 | `loss.backward()` 一行搞定 | 极大降低开发门槛 |
| 计算图 | 静态图（Theano/TF 1.x）| 动态图（PyTorch）+ torch.compile | 兼顾灵活性和性能 |
| 二阶方法 | 完整 Hessian（$O(n^2)$ 存储）| Hessian-free / L-BFGS / 对角近似 | 规避大规模 Hessian |
| 不可微处理 | 不支持 | 次梯度、Straight-Through Estimator、Gumbel-Softmax | 扩展到离散/稀疏场景 |

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5

---

## 📚 扩展阅读

### 深入理解

| 资源 | 类型 | 为什么值得读 | 难度 |
|------|------|------------|------|
| [《Deep Learning》Ch.6.5](../../../textbooks/goodfellow_deep_learning.pdf) | 📚 教科书 | 反向传播与计算图的权威讲解 | ⭐⭐⭐ |
| [《MML》Ch.5](../../../textbooks/deisenroth_mml.pdf) | 📚 教科书 | 向量微积分的完整体系 | ⭐⭐⭐ |
| [《Convex Opt》Ch.9](../../../textbooks/boyd_convex_optimization.pdf) | 📚 教科书 | 梯度方法 + 牛顿法的收敛分析 | ⭐⭐⭐⭐ |

### 横向对比

| 资源 | 对比点 | 何时读 |
|------|--------|--------|
| 积分知识库 [integration_summation_map.md](../integration_summation/integration_summation_map.md) | 微分的逆运算 | 学完微分后 |
| 卷积知识库 [convolution_map.md](../convolution/convolution_map.md) | 卷积的微分（反卷积/转置卷积） | 学 CNN 时 |

### 上层应用

| 资源 | 说明 | 何时读 |
|------|------|--------|
| [《Deep Learning》Ch.8](../../../textbooks/goodfellow_deep_learning.pdf) | 优化算法全景（SGD/Adam/二阶法）| 实际训练模型时 |
| [《Deep Learning》Ch.20](../../../textbooks/goodfellow_deep_learning.pdf) | 生成模型中的梯度估计 | 学 VAE/GAN 时 |
| [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html) | 自动微分实践指南 | 编码时 |

> 📚 Book: 综合以上教科书

---

## 与工作区已有知识库的关联

| 类别 | 数量 | 代表 | 学习点 |
|------|------|------|--------|
| 数学基础 | 2 | [integration_summation](../integration_summation/), [convolution](../convolution/) | 微分的逆运算 / 卷积的微分 |
| 深度学习 | 4 | [cnn](../../deep-learning/cnn/), [mlp](../../deep-learning/mlp/), [pytorch](../../deep-learning/pytorch/) | 反向传播在各架构中的应用 |
| 机器学习 | 5 | [logistic_regression](../../ml/logistic_regression/), [svm](../../ml/svm/) | 梯度下降训练经典模型 |
