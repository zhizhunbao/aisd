# Advanced Deep Learning Knowledge Map

> 来源课程：CMU 10-707 Advanced Deep Learning (Ruslan Salakhutdinov)
> 级别：博士 PhD · 角色：ML 工程师
> 前置课程：`deep-learning` (研究生级)

## 课程定位

Advanced Deep Learning 是 PhD 级别的独立课程，与基础 Deep Learning 的区别：

| 维度 | Deep Learning (研究生) | Advanced Deep Learning (博士) |
|------|----------------------|------------------------------|
| 重点 | CNN/RNN/Transformer 架构与训练 | 概率图模型 + 深度生成模型的理论基础 |
| 数学深度 | 矩阵运算、链式法则、梯度计算 | 变分推断、蒙特卡洛方法、信息论 |
| 模型类型 | 判别式模型为主 | 生成式模型为主 (VAE, GAN, EBM, Flow) |
| 理论要求 | 直觉理解 + 实现能力 | 严格数学证明 + 理论分析能力 |
| 前置要求 | ML 导论 + 线性代数 + 概率论 | DL 基础 + 统计推断 + 优化理论 |

## 主题列表

| 主题 | 文件数 | 状态 | 描述 |
|------|--------|------|------|
| graphical_models | 0 | 🔲 planned | 概率图模型：有向/无向图模型、变分推断、信念传播 |
| linear_factor_models | 0 | 🔲 planned | 线性因子模型：PPCA、FA、ICA、稀疏编码 |
| autoencoders | 0 | 🔲 planned | 自编码器家族：DAE、稀疏AE、收缩AE、VAE、β-VAE |
| energy_based_models | 0 | 🔲 planned | 基于能量的模型：RBM、DBN、DBM、Helmholtz 机 |
| monte_carlo_methods | 0 | 🔲 planned | 蒙特卡洛方法：MCMC、Gibbs采样、AIS、对比散度 |
| learning_inference | 0 | 🔲 planned | 学习与推断：分数匹配、NCE、伪似然、IWAE |
| deep_generative_models | 0 | 🔲 planned | 深度生成模型：GAN、NADE、Flow、扩散模型、分数模型 |
| deep_rl | 0 | 🔲 planned | 深度强化学习：DQN、Policy Gradient、PPO、World Model |
| advanced_optimization | 0 | 🔲 planned | 高级优化：自然梯度、K-FAC、SAM、损失曲面分析 |
| dl_theory | 0 | 🔲 planned | 深度学习理论：NTK、双下降、隐式正则化、泛化界 |

## 与基础 DL 课程的主题对应

```
deep-learning (研究生)          advanced-deep-learning (博士)
──────────────────────          ──────────────────────────────
tensor                    ──→   (前置知识)
dense_layer               ──→   (前置知识)
activation_functions      ──→   (前置知识)
conv_layer                ──→   graphical_models
max_pool_layer            ──→   linear_factor_models
avg_pool_layer            ──→   autoencoders
cnn                       ──→   energy_based_models
mlp                       ──→   monte_carlo_methods
loss_functions            ──→   learning_inference
optimizers                ──→   deep_generative_models
vanishing_gradient        ──→   advanced_optimization
transformer               ──→   dl_theory
pytorch / tensorflow      ──→   deep_rl
keras                     ──→   (实现工具)
```
