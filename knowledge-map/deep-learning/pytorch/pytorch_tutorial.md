---
topic: pytorch
dimension: tutorial
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch Tutorials](https://pytorch.org/tutorials/) — v2.10"
  - "📖 Paper: [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)"
expiry: 6m
status: current
---

# PyTorch 教程

> **前置知识：** Python 基础 | NumPy 数组操作 | 微积分链式法则 | 线性代数基础
> **参考来源：** [PyTorch 官方教程](https://pytorch.org/tutorials/) | [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)

---


## Section 0: 前置知识速查

1. **Python 面向对象** — 理解类继承、`__init__`、方法重载（`nn.Module` 要求）
2. **NumPy 多维数组** — 理解 shape、broadcasting、indexing（Tensor 操作几乎一致）
3. **链式法则** — $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$（Autograd 的数学基础）
4. **矩阵乘法** — 理解 $(m \times n) \cdot (n \times k) = (m \times k)$（线性层核心操作）
5. **概率基础** — 理解 softmax、交叉熵的概率意义（分类任务必备）

> 📖 Docs: [Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)

---


## Section 1: 它解决什么问题（Why）

### 没有它会怎样？

- 🔧 **手动求导地狱** — 每换一个网络结构就要重新推导所有梯度公式，一个 ResNet-50 有 2500 万参数，谁来手算？
- 🐢 **CPU 瓶颈** — NumPy 不支持 GPU，训练一个 ImageNet 模型从"几天"变成"几个月"
- 🔒 **静态图束缚（TF1.x 时代）** — 定义完计算图才能运行，想加个 `if` 条件分支？对不起，用 `tf.cond`；想调试？对不起，断点进不去
- 🧩 **生态碎片化** — 数据加载用一个库、模型定义用另一个、训练循环自己写，拼接成本极高

### 它的核心价值

1. **Autograd 自动微分** — 你只管写前向传播，梯度自动算，换了网络结构也不用改反向传播代码
2. **GPU 无痛加速** — `.to('cuda')` 一行代码搞定，接口与 CPU 完全一致
3. **动态计算图** — Python 原生 `if/for/while` 直接用，`pdb` 直接调试，写模型像写普通 Python
4. **统一生态** — `torch.nn`（模型）+ `torch.optim`（优化）+ `torch.utils.data`（数据）+ `torchvision`（CV），一站式
5. **研究到生产** — 研究用 Eager mode，部署用 `torch.compile` / `torch.export` 优化

> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703), Section 1 (Motivation)
> 📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.1

---


## Section 2: 它怎么工作的（How — 底层原理）

### 2.1 核心工作流程

```
┌──────────────────────────────────────────────────────────────┐
│                    PyTorch 训练循环                           │
│                                                              │
│  ① 数据准备          ② 前向传播           ③ 计算损失         │
│  ┌──────────┐       ┌──────────┐        ┌──────────┐        │
│  │ Dataset  │──────→│ model(x) │───────→│ loss_fn  │        │
│  │ DataLoader│       │ (forward) │        │ (y, ŷ)   │        │
│  └──────────┘       └──────────┘        └────┬─────┘        │
│                          │                    │              │
│                 动态构建计算图 DAG              │              │
│                                               ↓              │
│  ⑥ 重复                ⑤ 更新参数          ④ 反向传播        │
│  ┌──────────┐       ┌──────────┐        ┌──────────┐        │
│  │ 下一个    │←──────│optimizer │←───────│ loss     │        │
│  │ batch    │       │ .step()  │        │ .backward()│       │
│  └──────────┘       └──────────┘        └──────────┘        │
│                          ↑                    │              │
│                     读取 param.grad    沿 DAG 计算梯度       │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 Autograd 动态图机制

PyTorch 的自动微分引擎是**反向模式自动微分（reverse-mode AD）**：

1. **前向传播** — 执行用户代码，每个 Tensor 操作同时做两件事：
   - 计算输出值
   - 在计算图中创建 `Function` 节点（存在 `.grad_fn` 属性），记录"怎么来的"
2. **构建 DAG** — 所有操作形成有向无环图，叶子 = 输入 Tensor，根 = loss
3. **反向传播** — 调用 `loss.backward()` 从根到叶遍历 DAG，每个节点的 `.grad_fn` 应用链式法则计算局部梯度
4. **累积梯度** — 结果存入 `tensor.grad`（注意：**梯度是累加的**，必须手动 `zero_grad()`）

**关键设计决策：图是临时的。** 每次 `forward()` 都重建图，这意味着：
- 可以在 `forward()` 中使用 Python 控制流（动态图的本质）
- `backward()` 后图默认被释放（除非 `retain_graph=True`）

### 2.3 Tensor 内存模型

```
      Tensor 对象
      ┌──────────────────────────────────┐
      │ data    → Storage (连续内存块)    │
      │ shape   → (3, 4)                 │
      │ stride  → (4, 1)                 │
      │ dtype   → float32                │
      │ device  → cuda:0                 │
      │ requires_grad → True             │
      │ grad    → Tensor (梯度)          │
      │ grad_fn → AddBackward0           │
      └──────────────────────────────────┘
```

- **Storage** — 底层连续内存，多个 Tensor 可共享同一 Storage（view 操作不复制数据）
- **Stride** — 描述从一个维度跳到下一个元素需要跨过的步数（转置只改 stride 不移数据）
- **Contiguous** — stride 与 shape 兼容时 Tensor 连续；`.contiguous()` 强制重新排列内存

### 2.4 nn.Module 生命周期

1. `__init__()` — 定义层和参数（`self.linear = nn.Linear(10, 5)`）
2. `forward(x)` — 描述数据如何流过各层（`return self.linear(x)`）
3. 调用 `model(x)` — 内部调用 `__call__()` → 触发 hooks → 调用 `forward(x)`
4. `parameters()` — 迭代所有可训练参数（递归包含子模块）
5. `state_dict()` — 导出参数字典（用于保存/加载）

> 📖 Docs: [Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)
> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703), Section 3-4
> 📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5

---


## Section 3: 局限性

1. **Eager mode 性能开销** — 逐行解释执行有 Python 解释器开销，比优化后的静态图慢（`torch.compile` 可缓解）
2. **显存管理** — GPU 显存有限，大模型容易 OOM；需要手动管理梯度累积、混合精度
3. **部署生态不如 TF** — 移动端（TFLite vs TorchMobile）、浏览器端（TF.js 更成熟）
4. **多 GPU 配置复杂** — DDP 虽然强大但学习曲线陡峭（spawn vs fork, 梯度同步策略）
5. **API 变动频繁** — 部分新特性迭代快，旧教程代码可能失效（如 `torch.compile` API 在快速演进）

---


## Section 4: 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------| 
| **PyTorch** | 动态图、调试友好、研究主流 | Eager 有性能开销、移动部署弱 | 研究原型、学术论文、NLP/CV |
| **TensorFlow 2** | Keras 高层 API、部署生态强 | 动态图非原生、API 两套混乱 | 生产部署、移动端、Google 生态 |
| **JAX** | 函数式、XLA 编译、vmap 向量化 | 学习曲线陡、生态小 | 大规模科学计算、TPU、研究前沿 |
| **PyTorch Lightning** | 工程化模板、减少样板代码 | 牺牲部分灵活性 | 团队协作、标准化训练 |

---


## 参考来源表

| 来源 | 类型 | 使用位置 |
|------|------|---------| 
| [PyTorch Official Docs](https://pytorch.org/docs/stable/) | 📖 官方文档 | 全文 API 引用 |
| [Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html) | 📖 官方文档 | Section 2.2 |
| [Paszke et al. 2019](https://arxiv.org/abs/1912.01703) | 📖 论文 | Section 1, 2 |
| [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf) | 📚 教科书 | Section 1, 2 |
| [Learn the Basics Tutorial](https://pytorch.org/tutorials/beginner/basics/intro.html) | 📖 官方教程 | Section 0 |
