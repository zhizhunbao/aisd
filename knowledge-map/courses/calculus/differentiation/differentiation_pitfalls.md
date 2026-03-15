---
topic: differentiation
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📖 Docs: PyTorch Autograd — https://pytorch.org/docs/stable/autograd.html"
  - "📚 Book: Goodfellow et al., Deep Learning, Ch.6,8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "🧪 经验: PyTorch 训练常见陷阱"
expiry: 6m
status: current
---

# 微分 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 忘记清零梯度导致梯度累积

**场景：** PyTorch 训练循环中未调用 `optimizer.zero_grad()` 或 `grad.zero_()`

**症状：** 损失不下降或震荡，梯度值异常偏大

**根因：** PyTorch 默认**累积**梯度（`.backward()` 将新梯度加到 `.grad` 上）。这个设计是为了支持 gradient accumulation（小 batch 模拟大 batch），但如果忘记清零，每步的梯度都是历史积累。

**解法：**

❌ 错误写法 — 忘记清零

```python
for batch in dataloader:
    loss = model(batch)
    loss.backward()       # 梯度累积到上一步的基础上！
    optimizer.step()
```

✅ 正确写法 — 每步先清零

```python
for batch in dataloader:
    optimizer.zero_grad()  # 先清零 / Zero gradients first
    loss = model(batch)
    loss.backward()
    optimizer.step()
```

**教训：** 训练循环的标准顺序永远是 `zero_grad → forward → backward → step`

> 📖 Docs: [PyTorch Autograd](https://pytorch.org/docs/stable/autograd.html)
> 🧪 经验: PyTorch 新手 #1 常见错误

---

## 坑 2: 在 `torch.no_grad()` 之外做参数更新

**场景：** 手动实现梯度下降时，参数更新操作被计算图追踪

**症状：** `RuntimeError: a leaf Variable that requires grad is being used in an in-place operation` 或梯度计算不正确

**根因：** `x -= lr * x.grad` 是 in-place 操作，会修改需要梯度追踪的叶节点，破坏计算图

**解法：**

❌ 错误写法 — 直接在有梯度的张量上操作

```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
loss = (x**2).sum()
loss.backward()
x -= 0.1 * x.grad   # RuntimeError!
```

✅ 正确写法 — 用 `with torch.no_grad()` 包裹更新

```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
loss = (x**2).sum()
loss.backward()

with torch.no_grad():           # 禁用梯度追踪 / Disable grad tracking
    x -= 0.1 * x.grad
    x.grad.zero_()               # 清零 / Zero grad
```

**教训：** 参数更新是"脱离计算图"的数值操作，必须用 `torch.no_grad()` 包裹

> 📖 Docs: [torch.no_grad()](https://pytorch.org/docs/stable/generated/torch.no_grad.html)

---

## 坑 3: 梯度消失 — 深层网络梯度趋近零

**场景：** 使用 Sigmoid/Tanh 激活的深层网络（>10 层）

**症状：** 前面几层的梯度接近 0，权重几乎不更新，模型不学习

**根因：** Sigmoid 的导数最大值为 0.25（$\sigma'(x) = \sigma(x)(1-\sigma(x)) \leq 0.25$）。10 层链式法则：$0.25^{10} \approx 10^{-6}$，梯度指数衰减。

**解法：**

❌ 错误写法 — 深层网络用 Sigmoid

```python
layers = []
for _ in range(20):
    layers.append(nn.Linear(100, 100))
    layers.append(nn.Sigmoid())         # 梯度消失的元凶
model = nn.Sequential(*layers)
```

✅ 正确写法 — 使用 ReLU + 残差连接 + BatchNorm

```python
# 方案 1: ReLU（导数为 0 或 1，不衰减）
layers = []
for _ in range(20):
    layers.append(nn.Linear(100, 100))
    layers.append(nn.ReLU())            # 梯度不衰减

# 方案 2: ResNet 残差连接
class ResBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim), nn.ReLU(),
            nn.Linear(dim, dim))
    def forward(self, x):
        return x + self.block(x)         # 残差: 梯度有"高速公路"

# 方案 3: BatchNorm
layers.append(nn.BatchNorm1d(100))       # 归一化中间层
```

**教训：** 深层网络必须用 ReLU 系列激活 + 残差连接，避免 Sigmoid/Tanh 在深度模型中使用

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.2.5

---

## 坑 4: 数值梯度检查时 h 选错

**场景：** 用数值微分验证自动微分结果

**症状：** 数值梯度和自动微分梯度差异很大（>1e-2），但代码其实是对的

**根因：** $h$ 太大导致截断误差，$h$ 太小导致浮点舍入误差。前向差分精度 $O(h)$，中心差分 $O(h^2)$

**解法：**

❌ 错误写法 — 使用前向差分 + 不合适的 h

```python
h = 1.0                    # 太大！
grad = (f(x + h) - f(x)) / h   # 前向差分，精度 O(h)
```

✅ 正确写法 — 中心差分 + h ≈ 1e-5

```python
h = 1e-5                                   # 经验最佳值
grad = (f(x + h) - f(x - h)) / (2 * h)    # 中心差分，精度 O(h²)

# 或用 PyTorch 内置检查
from torch.autograd import gradcheck
gradcheck(model, inputs, eps=1e-5)         # 自动对比
```

**教训：** gradient checking 用**中心差分 + h=1e-5**；差异 < 1e-5 则通过

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.5.7
> 🧪 经验: gradient checking 最佳实践

---

## 坑 5: detach/clone 搞混导致计算图泄漏

**场景：** 想把中间结果保存下来用于可视化或日志，但不小心保留了计算图引用

**症状：** 显存持续增长，最终 CUDA OOM

**根因：** 直接保存 `tensor` 会保留整个计算图的引用。PyTorch 的计算图在 `.backward()` 后被释放，但如果有外部引用则不会释放

**解法：**

❌ 错误写法 — 保存带梯度的中间张量

```python
losses = []
for batch in dataloader:
    loss = model(batch)
    losses.append(loss)    # 保持计算图引用 → 显存泄漏！
    loss.backward()
```

✅ 正确写法 — 用 .item() 或 .detach()

```python
losses = []
for batch in dataloader:
    loss = model(batch)
    losses.append(loss.item())      # 转为 Python 数字，释放图
    # 或 losses.append(loss.detach().cpu())  # 转到 CPU + 脱离图
    loss.backward()
```

**教训：** 任何不参与反向传播的中间结果，保存时必须 `.item()`、`.detach()` 或 `.detach().clone()`

> 📖 Docs: [tensor.detach()](https://pytorch.org/docs/stable/generated/torch.Tensor.detach.html)
> 🧪 经验: PyTorch 显存管理

---

## 坑 6: 对不可微点求梯度（ReLU 在 0 处）

**场景：** ReLU 在 $x=0$ 处导数未定义，但训练照常进行

**症状：** 通常无明显症状（PyTorch 将 ReLU 在 0 处的导数定义为 0），但理论上梯度不存在

**根因：** ReLU $\max(0, x)$ 在 $x=0$ 处不可微。实践中 $x$ 恰好等于 0 的概率极低（连续分布的零测集），PyTorch 约定导数为 0。但 Dead ReLU 问题——如果某个神经元的 $z$ 总是 $<0$，则导数永远为 0，该神经元"死亡"。

**解法：**

❌ 错误写法 — 忽略 Dead ReLU

```python
# 如果初始化太大 + 学习率太大，神经元可能全部"死掉"
model = nn.Sequential(nn.Linear(100, 100), nn.ReLU())
nn.init.normal_(model[0].weight, std=10.0)  # 初始化太大！
```

✅ 正确写法 — 使用 Leaky ReLU 或合理初始化

```python
# 方案 1: Leaky ReLU（负区域有小梯度 0.01）
model = nn.Sequential(nn.Linear(100, 100), nn.LeakyReLU(0.01))

# 方案 2: He 初始化（配合 ReLU）
nn.init.kaiming_normal_(model[0].weight, mode='fan_in', nonlinearity='relu')
```

**教训：** ReLU 的不可微性实践中影响不大，但 Dead ReLU 是真实问题——用 Leaky ReLU 或 He 初始化预防

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3.1
> 🧪 经验: ReLU 激活函数实践

---

## 调试清单

1. [ ] **损失不下降？** → 检查是否忘记 `optimizer.zero_grad()`
2. [ ] **RuntimeError in-place？** → 参数更新是否在 `torch.no_grad()` 内
3. [ ] **前几层不学习？** → 检查梯度消失（打印 `.grad.norm()`），换 ReLU + ResNet
4. [ ] **gradient check 失败？** → 用中心差分 + h=1e-5，检查 relative error
5. [ ] **显存持续增长？** → 用 `.item()` / `.detach()` 保存中间结果
6. [ ] **Dead ReLU（某些神经元永远输出 0）？** → 换 Leaky ReLU 或检查初始化
7. [ ] **梯度爆炸（NaN/Inf）？** → 使用 `torch.nn.utils.clip_grad_norm_`
8. [ ] **自定义 Function 梯度不对？** → 用 `gradcheck` 数值验证
9. [ ] **二阶梯度需要但报错？** → 确认 `create_graph=True` in `backward()`
10. [ ] **多 GPU 梯度不同步？** → 检查 `DistributedDataParallel` 配置
