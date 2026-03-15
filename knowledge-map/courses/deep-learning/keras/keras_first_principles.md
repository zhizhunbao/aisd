---
topic: keras
dimension: first_principles
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Paper: Chollet, 'Keras', 2015 — https://arxiv.org/abs/1508.01211"
  - "📖 Docs: Keras 3 Design Philosophy — https://keras.io/why_keras/"
  - "💻 Source: keras/keras GitHub — https://github.com/keras-team/keras"
  - "📚 Book: Goodfellow et al., 《Deep Learning》 Ch.11 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
expiry: 12m
status: current
---

# Keras 第一性原理

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015 — Section 1 "Design Principles"
> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)

---


## 核心问题链

> 用"5 个为什么"式的递归追问，从表面功能一路追到不可再分的基本事实。

### 问题链

1. **Keras 在做什么？** → 提供一个高层 Python API，让用户用最少的代码定义、训练和部署神经网络
2. **为什么需要高层 API？** → 底层框架 (JAX/TF/PyTorch) 的 API 太冗长，写训练循环需要 50+ 行样板代码；认知负荷高，影响实验效率
3. **为什么认知负荷会影响效率？** → 人类工作记忆有限（~7±2 个 chunk），API 越复杂 → 理解代码越慢 → 从想法到实验的周期越长 → 创新速度越慢
4. **这个约束的根基是什么？** → **人类认知资源的有限性**是生物学事实（Miller's Law），以及**深度学习工作流的可分解性**——任何 DL 项目都可拆为"定义模型 → 配置训练 → 执行训练 → 评估"四个独立阶段
5. **这些根基能否继续拆分？** → 不能 → **到达公理：人类认知有限 + DL 工作流可模块化 + 计算可委托**

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015
> 📖 Docs: [Why Keras?](https://keras.io/why_keras/) — "Keras reduces developer cognitive load"

---


## 公理与基本假设

> 列出 Keras 赖以成立的**不可再分的基本事实**。这些是"如果它们不成立，整个 Keras 就没有存在价值"的根基。

### 公理 1: 人类认知资源有限 (Cognitive Load Theory)

**陈述：** 人类的工作记忆容量有限，一次能处理的信息块数量约为 7±2 个（Miller, 1956）。API 设计必须最小化用户需要同时记住的概念数量。

**白话：** 人脑一次最多记住 5-9 个东西。API 越复杂，犯错越多，干活越慢。

**来源：** 认知心理学（Miller's Law, 1956）+ 软件工程中的认知负荷理论（John Sweller, 1988）。Chollet 在 Keras 论文中明确将此作为设计原则。

**可验证性：** 普遍成立。在任何需要人类编写代码的场景下成立。仅在完全由 AI 自动生成代码（无人类参与）时，此公理可被部分放松。

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015 — "Modularity" and "User-friendliness" principles

### 公理 2: 深度学习工作流可模块化 (DL Workflow Decomposability)

**陈述：** 任何深度学习项目都可以分解为若干独立阶段：数据准备 → 模型定义 → 训练配置 → 训练执行 → 评估 → 部署。这些阶段之间的接口可以被标准化。

**白话：** 每个 DL 项目干的事情都差不多——准备数据、搭模型、训练、评估。这些步骤可以用统一的 API 封装。

**来源：** 经验观察 + 软件工程的模块化原则 (Parnas, 1972 "On the Criteria for Decomposing Systems into Modules")。深度学习框架的演化（从 Caffe 到 TF 到 PyTorch）都在向标准化工作流收敛。

**可验证性：** 在标准 DL 任务（分类、回归、生成、序列建模）中完全成立。在强化学习、图神经网络、科学计算等非标准场景中，工作流可能无法完全标准化——这是 Keras 的边界。

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015 — "Easy extensibility"
> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py` — compile/fit/evaluate

### 公理 3: 计算操作可后端无关化 (Computation Backend Agnosticism)

**陈述：** 神经网络的核心计算操作（矩阵乘法、卷积、激活函数、自动微分）在数学上是唯一的，不依赖于具体的框架实现。因此，可以定义一套统一的操作 API (`keras.ops`)，在运行时委托给任意后端执行。

**白话：** 矩阵乘法就是矩阵乘法，不管是 TF 做的还是 PyTorch 做的，数学结果一样。所以可以用统一接口封装。

**来源：** 线性代数和微积分的数学唯一性 + BLAS/LAPACK 等标准化计算库的历史先例。

**可验证性：** 对于纯数学操作（matmul, conv, relu 等）完全成立。对于与框架内部状态紧密耦合的操作（如 PyTorch 的 autograd 动态图、JAX 的函数式约束、TF 的 XLA 特有优化）不完全成立——这就是 Keras 3 无法暴露后端特有功能的原因。

> 💻 Source: [keras](../../.github/keras/) `keras/src/ops/` — 跨后端操作抽象
> 📖 Docs: [Keras 3 — Ops API](https://keras.io/api/ops/)

### 公理 4: 渐进式复杂度原则 (Progressive Disclosure of Complexity)

**陈述：** 一个好的 API 应该让简单的事情简单做，复杂的事情可能做。用户应该能从最简单的用例（Sequential + fit）开始，按需逐步增加复杂度（Functional → Subclassing → 自定义训练循环），而不是被迫一次性学习全部概念。

**白话：** 新手用 `model.fit()` 就能训练模型；高手可以覆写 `train_step()` 做完全自定义。两者用同一个框架，不需要换工具。

**来源：** 人机交互设计原则 (Nielsen's "Recognition over recall", Shneiderman's "Eight Golden Rules")。

**可验证性：** 在 Keras 的 Sequential → Functional → Subclassing 三级 API 中得到验证。限制：如果所有任务都需要最高复杂度（如顶级研究），渐进性的价值会降低。

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015 — "Minimalism"
> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)

---


## 从公理到技术的推导链

> 展示如何**仅从上述公理出发**，一步步逻辑推导出 Keras 的完整技术方案。
> 每一步必须标注"用了哪个公理"，不允许跳步或引入未声明的假设。

### Step 1: {从公理 1 出发} → {需要极简 API}

**推理：** 因为人类认知有限（公理 1），所以 API 必须最小化用户需要同时记住的概念数量。这意味着训练一个模型不应该需要用户理解梯度计算、数据批次化、学习率调度等底层细节。

**结果：** 需要一个 **"配置式训练 API"**——用户只需声明"用什么优化器、什么损失函数"即可。

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015

### Step 2: {结合 Step 1 + 公理 2} → {compile-fit-evaluate 三步流程}

**推理：** 既然 DL 工作流可模块化（公理 2），我们可以把"配置"和"执行"分开。`compile()` 负责声明训练配置（优化器、损失、指标），`fit()` 负责执行训练循环。两个方法各司其职，用户不需要理解训练循环的内部实现。

**结果：** 得到 **`compile() → fit() → evaluate()` 标准流程**——这就是 Keras 训练 API 的核心。

> 💻 Source: [keras](../../.github/keras/) `keras/src/trainers/trainer.py`

### Step 3: {结合 Step 2 + 公理 3} → {多后端架构 + keras.ops}

**推理：** 既然核心计算操作是后端无关的（公理 3），我们可以在"配置式训练 API"下方插入一个适配层：`keras.ops` 提供统一操作接口，`Backend Trainer`（TensorFlowTrainer/JAXTrainer/TorchTrainer）负责后端特定的训练逻辑。用户代码完全不感知后端。

**结果：** 得到 **Keras 3 的多后端架构**——同一份模型代码可在 JAX/TF/PyTorch 上运行。

> 💻 Source: [keras](../../.github/keras/) `keras/src/models/model.py:20-35`

### Step 4: {结合 Step 3 + 公理 4} → {Sequential → Functional → Subclassing 三级 API}

**推理：** 渐进式复杂度（公理 4）要求 API 有多个入口点。Sequential 给新手——零配置线性堆叠。Functional API 给中级用户——可视化、可序列化的 DAG 图。Subclassing 给专家——完全自由的 Python 代码。三者共享同一个 `compile/fit` 基础设施。

**结果：** 得到 **Keras 的完整技术方案**——三种建模方式 + 统一训练 API + 多后端执行。

> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)

### 推导链全景图

```
公理 1 (认知有限) ──────┐
                        ├──→ 极简 API ──┐
公理 2 (工作流可模块化) ┘               ├──→ compile/fit/evaluate ──┐
                                        │                           │
公理 3 (后端无关) ───────────────────────┘                           │
                                                                    ├──→ Keras 3 完整方案
公理 4 (渐进复杂度) ──→ Sequential/Functional/Subclassing ──────────┘
```

---


## 如果公理不成立？

> 逐个"拔掉"公理，分析 Keras 会如何崩塌。这揭示了 Keras 的**真正边界**。

### 公理 1 失效：认知资源无限

**如果不成立：** 如果开发者拥有无限的工作记忆和注意力（例如未来的 AI 编程代理），那么 API 简洁性变得无关紧要——用户可以轻松驾驭任意复杂的底层 API。

**技术后果：** Keras 的核心价值消失——直接用 JAX/TF/PyTorch 原生 API 即可，不需要高层封装。

**替代方案：** 直接使用后端框架的原生 API + AI 代码生成工具。

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015

### 公理 2 失效：DL 工作流不可模块化

**如果不成立：** 如果每个 DL 项目的训练逻辑都截然不同（如强化学习中的环境交互、GAN 的对抗训练、元学习的 inner/outer loop），无法用统一的 `compile/fit` 封装。

**技术后果：** Keras 的 `fit()` 变得鸡肋——用户总是需要覆写 `train_step()` 或完全手写训练循环。

**替代方案：** 使用 PyTorch Lightning（提供结构化但更灵活的训练抽象）或完全手写训练循环。

> 📖 Docs: [Keras 3 — Custom Training Loops](https://keras.io/guides/writing_a_custom_training_loop_in_jax/)

### 公理 3 失效：计算操作无法后端无关化

**如果不成立：** 如果不同后端的数值计算结果显著不同（浮点精度差异、自定义 CUDA kernel 无法跨平台、框架特有状态管理无法抽象），那么"一份代码多后端运行"就是虚假承诺。

**技术后果：** Keras 3 的多后端架构崩塌——用户被迫回到框架锁定。

**替代方案：** 接受后端锁定，选择一个框架深度使用（回到 tf.keras 或纯 PyTorch 时代）。

> 💻 Source: [keras](../../.github/keras/) `keras/src/ops/` — 部分操作的跨后端数值差异

### 公理 4 失效：所有用户都需要最高复杂度

**如果不成立：** 如果所有 DL 项目都需要完全自定义的训练逻辑（自定义梯度、多阶段训练、自定义分布式策略），Sequential 和 Functional API 成为无用的"玩具"。

**技术后果：** Keras 退化为一个 Layer 库——只有 Layer/Layer 子类有价值，Model 的训练 API 不再有意义。

**替代方案：** 直接用后端框架 + 将 Keras 仅作为 Layer 定义工具使用（类似 `torch.nn.Module` 的角色）。

> 📖 Docs: [Keras 3 — Subclassing Guide](https://keras.io/guides/making_new_layers_and_models_via_subclassing/)

---


## 第一性原理速查表

| 公理/假设 | 一句话陈述 | 成立条件 | 失效后果 |
|----------|-----------|---------|---------|
| 公理 1: 认知有限 | 人脑一次处理 ~7 个概念 | 人类编写代码 | Keras 的核心价值消失 |
| 公理 2: 工作流可模块化 | DL 项目可拆为 数据→模型→训练→评估 | 标准 DL 任务 | compile/fit 变得鸡肋 |
| 公理 3: 后端无关 | 矩阵乘法不依赖具体框架 | 纯数学操作 | 多后端架构崩塌 |
| 公理 4: 渐进复杂度 | 简单事简单做，复杂事可能做 | 用户技能分布广 | Keras 退化为纯 Layer 库 |

> 📖 Paper: Chollet, [Keras](https://arxiv.org/abs/1508.01211), 2015
> 📖 Docs: [Why Keras?](https://keras.io/why_keras/)
