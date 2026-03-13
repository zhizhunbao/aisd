---
topic: pytorch
dimension: history
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Paper: [Paszke et al. 2019](https://arxiv.org/abs/1912.01703)"
  - "📖 Paper: [Theano 2016](https://arxiv.org/abs/1605.02688)"
  - "📖 Paper: [Abadi et al. TensorFlow 2016](https://arxiv.org/abs/1603.04467)"
expiry: 12m
status: current
---

# PyTorch 的故事线：从手动求导到 define-by-run

> **核心主题：** 深度学习框架如何从"让研究者痛苦地手写梯度"进化到"用 Python 写模型、框架自动搞定剩下的"
> **故事线：** 一个不断追求"更灵活、更易用、更高效"的框架演进历程

---

## 🎬 序幕：一切从什么问题开始？

### 一句话概括
> 2010 年代初，深度学习模型越来越复杂，但工具极度原始——研究者要么手推梯度公式，要么被框架的静态图束缚，能不能有个工具让写深度学习像写普通 Python 一样简单？

2006 年 Hinton 发表深层网络预训练论文，深度学习开始复兴。但当时的工具链极其落后：写一个新网络结构，不仅要推导前向传播公式，还要手动写每个参数的梯度计算。一个 3 层 MLP 就已经很麻烦，更不用说 ResNet、Attention 这些复杂结构了。

> 🔑 **问题提出：** 能不能让计算机自动帮我求导？

---

## 📚 第一章：Theano 时代——"能自动求导了，但好难用"（2010-2015）

> **关键人物：** Yoshua Bengio, James Bergstra (Université de Montréal)
> **关键论文：** Bergstra et al., [Theano: A CPU and GPU Math Compiler in Python](https://arxiv.org/abs/0908.3373), 2010

### 发生了什么？

蒙特利尔大学（MILA 前身）的团队开发了 Theano——第一个广泛使用的支持自动微分的深度学习库。Theano 将数学表达式编译成优化的 C/CUDA 代码，能自动计算梯度。

它的工作方式是**静态计算图**：先用符号变量定义数学表达式（构建图），然后编译成可执行函数。这就像写 SQL：先声明"我要什么"，然后由引擎优化执行。

### 为什么这很重要？

- **自动微分**成为现实——研究者终于不用手推梯度了
- **GPU 加速**透明化——同一份代码可以在 CPU/GPU 上运行
- 催生了 Lasagne、Blocks 等高层库，奠定了现代框架的基本范式

### 但还有一个问题……

Theano 的静态图虽然编译后高效，但**极度不灵活**：
- 编译一次需要几分钟
- 调试几乎不可能（断点打不进图里）
- 动态结构（变长序列、条件分支）需要极其丑陋的 workaround（`scan` 函数）

> 🔑 **故事转折点：** 深度学习进入 RNN/LSTM 时代，静态图的笨重让研究者叫苦不迭——该有新解法了。

---

## 📚 第二章：TensorFlow 1.x——"大厂入场，但还是静态图"（2015-2017）

> **关键人物：** Jeff Dean, Martín Abadi (Google Brain)
> **关键论文：** Abadi et al., [TensorFlow: A System for Large-Scale Machine Learning](https://arxiv.org/abs/1603.04467), 2016

### 发生了什么？

Google Brain 团队发布 TensorFlow，用更工程化的方式解决了 Theano 的编译慢、缺乏分布式支持等问题。TF 提供了完整的生态系统：TensorBoard（可视化）、TF Serving（部署）、分布式训练支持。

但它仍然是**静态图**：先 `tf.placeholder` 定义占位符、`tf.Session.run()` 执行图。虽然比 Theano 强大很多，但"define-and-run"的范式没变。

### 为什么这很重要？

- 深度学习框架从学术项目变成**工业级基础设施**
- 分布式训练、模型部署成为框架标配
- Google 的资源和影响力让 TF 迅速成为工业界首选

### 但还有一个问题……

对研究者来说，TF 1.x 依然痛苦：
- `Session`、`placeholder`、`feed_dict` 的三件套让人崩溃
- 想用 `if` 条件分支？请用 `tf.cond()`。想用 `for` 循环？请用 `tf.while_loop()`
- 调试时看到的是 tensor name 而不是值，`print` 打出来的是 Op 对象

> 🔑 **故事转折点：** 研究者需要一个"像写 Python 一样写模型"的框架，而不是"在 Python 里写另一门 DSL"。

---

## 📚 第三章：Chainer & DyNet——"define-by-run 先驱"（2015-2016）

> **关键人物：** Seiya Tokui (Preferred Networks), Chris Dyer (CMU/DeepMind)
> **关键论文：** Tokui et al., [Chainer: a Next-Generation Open Source Framework for Deep Learning](https://arxiv.org/abs/1908.00213)

### 发生了什么？

几乎同时，两个项目独立提出了**动态计算图（define-by-run）**的理念：

- **Chainer**（日本 Preferred Networks）：每次 `forward()` 实时构建计算图，用完就销毁
- **DyNet**（CMU）：专门为 NLP 优化的动态图框架，擅长处理变长序列

Chainer 的核心洞察是：**计算图不需要预先定义**。你写 Python 代码，每执行一步操作，框架自动在背后记录。需要求导？沿着记录的路径反向走一遍就行。

### 为什么这很重要？

- **证明了"灵活性"和"自动微分"不矛盾** — 可以同时拥有
- **NLP 社区首先受益** — RNN 和注意力机制经常有动态结构
- 直接启发了 PyTorch 的设计

### 但还有一个问题……

Chainer 和 DyNet 社区规模小，生态不完善，缺少 Google 和 Facebook 级别的工程资源来打磨框架的性能和部署能力。

> 🔑 **故事转折点：** Facebook AI Research (FAIR) 看到了 Chainer 的理念，决定用一流的工程能力把它做到极致——这就是 PyTorch 的起源。

---

## 📚 第四章：PyTorch 诞生——"研究者的救星"（2017-2019）

> **关键人物：** Soumith Chintala, Adam Paszke (FAIR)
> **关键论文：** Paszke et al., [PyTorch: An Imperative Style, High-Performance Deep Learning Library](https://arxiv.org/abs/1912.01703), NeurIPS 2019

### 发生了什么？

2017 年 1 月，Facebook AI Research 发布 PyTorch 0.1。它脱胎于 Torch（一个基于 Lua 的框架），但完全重写为 Python 优先的框架，核心理念直接来自 Chainer 的"define-by-run"。

PyTorch 做对了几件关键的事：
1. **Python 优先** — API 设计极度 Pythonic，`nn.Module` 就是 Python 类
2. **Eager 执行** — 每行代码立即得到结果，`print(x)` 直接看到值
3. **动态图** — `if`, `for`, `while` 直接用，`pdb` 直接调试
4. **高性能 C++ 后端** — ATen 张量库 + cuDNN 集成，性能不输静态图

### 为什么这很重要？

- 研究者终于可以用**正常的 Python 思维**写深度学习了
- 调试从"猜测" 变成 "`pdb` 一行行看"
- 到 2019 年，**学术界论文中 PyTorch 使用率首次超过 TensorFlow**
- NeurIPS 2019 论文正式阐明了 PyTorch 的设计哲学

### 但还有一个问题……

Eager mode 虽然灵活，但：
- **逐行解释执行有 Python 开销**，比优化的静态图慢
- **部署困难** — Eager Python 代码不能直接部署到移动端/嵌入式
- 需要某种方式在不牺牲灵活性的前提下获得性能

> 🔑 **故事转折点：** 能不能"写代码时动态图、部署时自动变静态图"？两全其美？

---

## 📚 第五章：torch.compile 时代——"两全其美"（2022-至今）

> **关键人物：** Jason Ansel, Horace He (Meta)
> **关键论文：** Ansel et al., [PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Capture](https://pytorch.org/blog/pytorch-2.0-release/)

### 发生了什么？

2022 年底，PyTorch 2.0 发布了 `torch.compile`，实现了"一个装饰器搞定性能优化"：

```python
@torch.compile
def train_step(model, data, target):
    output = model(data)
    loss = F.cross_entropy(output, target)
    loss.backward()
    return loss
```

底层技术栈：
- **TorchDynamo** — 通过 Python bytecode 分析，自动捕获计算图（不需要改用户代码）
- **TorchInductor** — 将捕获的图编译为优化的 Triton/C++ 内核
- **AOTAutograd** — Ahead-of-time 编译自动微分

### 为什么这很重要？

- **不破坏 Eager mode** — 用户代码不需要任何修改
- **复杂控制流照常工作** — DynaMo 能处理大部分 Python 控制流
- **显著加速** — 典型负载提速 30-50%，有些场景翻倍
- 标志着"灵活性 vs 性能"之争的终结

> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703)
> 📖 Docs: [torch.compile Tutorial](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)

---

## 🗺️ 全局回顾：技术演进路线图

```
2010          2015          2017          2019          2022
 │             │             │             │             │
 ▼             ▼             ▼             ▼             ▼
Theano ──→ TensorFlow ──→ PyTorch ──→ 学术主流 ──→ torch.compile
(自动微分)  (工业化)       (动态图)    (超越 TF)    (编译优化)
              │                          │
              ▼                          ▼
         Chainer/DyNet ──→ (启发) ──→ TF2 Eager
         (define-by-run)              (追随 PyTorch)
```

### 每一步升级解决了什么问题？

| 从 → 到 | 解决了什么核心问题？ |
|----------|-------------------| 
| 手动求导 → Theano | 自动微分，不需要手推梯度公式 |
| Theano → TensorFlow | 工程化、分布式、部署生态 |
| TF static → Chainer | 证明动态图可行（define-by-run） |
| Chainer → PyTorch | 一流工程 + Python 优先 + 动态图 |
| Eager only → torch.compile | 灵活性 + 编译优化兼得 |

> 📖 Paper: Paszke et al., [NeurIPS 2019](https://arxiv.org/abs/1912.01703), Section 1
