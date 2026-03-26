---
topic: forward_propagation
dimension: pitfalls
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow, Bengio & Courville, Deep Learning, Ch.6 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Docs: PyTorch nn.Module — https://pytorch.org/docs/stable/generated/torch.nn.Module.html"
  - "🧪 经验: 常见初学者错误与调试经验"
expiry: 6m
status: current
---

# Forward Propagation 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: Shape Mismatch — 矩阵维度不匹配

**痛点类别：** 代码不会写 — "我代码一跑就报错 RuntimeError"

**场景：** 初学者随意设置 `nn.Linear` 的 `in_features` 和 `out_features`，没有对齐上一层的输出维度和下一层的输入维度。

**症状：** `RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x128 and 64x10)`

**根因：** `nn.Linear(in_features, out_features)` 的 `in_features` 必须等于上一层的 `out_features`。每个 Linear 层内部做 $z = xW^T + b$，输入 $x$ 的最后一维必须和 $W$ 的列数匹配。

**解法：**

❌ 错误做法 — 维度不对齐

```python
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(64, 10),   # ❌ 64 != 128, 上一层输出 128
)
```

✅ 正确做法 — 确保每层输入维度等于上一层输出维度

```python
model = nn.Sequential(
    nn.Linear(784, 128),   # 784 → 128
    nn.ReLU(),
    nn.Linear(128, 10),    # ✅ 128 → 10, 对齐了!
)
```

**教训：** 定义网络时，用链条思维——上一层的 out 就是下一层的 in，一环扣一环。

> 📖 Docs: [PyTorch nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)

---

## 坑 2: 忘记切换 eval 模式 — 推理结果不稳定

**痛点类别：** 概念不理解 — "为什么训练和推理结果不一样"

**场景：** 模型中用了 Dropout 或 BatchNorm，推理时忘记调用 `model.eval()`。

**症状：** 每次推理结果都不一样（因为 Dropout 随机丢弃），或者推理精度比训练时低很多。

**根因：** `model.train()` 模式下 Dropout 会随机丢弃神经元，BatchNorm 使用当前 batch 的均值/方差；`model.eval()` 模式下 Dropout 关闭，BatchNorm 使用训练时积累的全局统计量。

**解法：**

❌ 错误做法 — 推理时忘记 eval

```python
# 训练完毕后直接推理
y_hat = model(x_test)  # ❌ 还在 train 模式, Dropout 仍然激活
```

✅ 正确做法 — 推理前切换模式

```python
model.eval()               # ✅ 关闭 Dropout, 固定 BatchNorm
with torch.no_grad():      # ✅ 不追踪梯度, 省显存
    y_hat = model(x_test)
```

**教训：** 推理三件套——`model.eval()` + `torch.no_grad()` + 不 call `loss.backward()`。

> 📖 Docs: [model.eval()](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval)

---

## 坑 3: 直接调用 model.forward(x) 而不是 model(x)

**痛点类别：** 代码不会写 — "为什么不直接调 forward"

**场景：** 初学者看到 `forward()` 方法，以为应该直接调用它。

**症状：** 代码能跑，但 hooks 不触发，某些模块行为异常。

**根因：** 调用 `model(x)` 实际上调用的是 `model.__call__(x)`，它在调用 `forward()` 之前会执行注册的 hooks（如前向钩子、后向钩子）。直接调 `forward()` 跳过了这些步骤。

**解法：**

❌ 错误做法 — 直接调 forward

```python
y = model.forward(x)  # ❌ 跳过了 hooks 和其他 nn.Module 内部逻辑
```

✅ 正确做法 — 用 model(x)

```python
y = model(x)  # ✅ 触发 __call__() → 执行 hooks → 调用 forward()
```

**教训：** 永远用 `model(x)`，把 `forward()` 当做 PyTorch 帮你调的内部方法。

> 📖 Docs: [nn.Module.__call__](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

---

## 坑 4: 忘记 torch.no_grad() 推理时显存爆炸

**痛点类别：** 代码不会写 — "推理时 GPU 内存不够"

**场景：** 推理或验证时没有用 `torch.no_grad()` 包裹前向传播。

**症状：** 推理时显存消耗和训练时一样大，大 batch 时 OOM。

**根因：** 默认情况下 PyTorch 会为每次运算建立计算图并缓存中间值（为反向传播准备）。推理不需要这些，白白浪费显存。

**解法：**

❌ 错误做法 — 推理时不关梯度

```python
model.eval()
y_hat = model(x_test)  # ❌ 仍然在构建计算图, 缓存中间值
```

✅ 正确做法 — 用 no_grad 或 inference_mode

```python
model.eval()
with torch.no_grad():           # ✅ 不记录计算图
    y_hat = model(x_test)

# 或更高效的写法 (PyTorch 1.9+)
with torch.inference_mode():    # ✅ 比 no_grad 更快
    y_hat = model(x_test)
```

**教训：** 推理 = `eval()` + `no_grad()`，缺一不可。

> 📖 Docs: [torch.no_grad](https://pytorch.org/docs/stable/generated/torch.no_grad.html)

---

## 坑 5: 输入数据没有正确 reshape

**痛点类别：** 代码不会写 — "为什么我的图片输入报 shape 错误"

**场景：** 用 MNIST 图片（28×28）训练 MLP，但忘记把 2D 图片展平成 1D 向量。

**症状：** `RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x28 and 784x128)`

**根因：** `nn.Linear(784, 128)` 期望输入是 $(B, 784)$，但 MNIST 图片是 $(B, 1, 28, 28)$ 或 $(B, 28, 28)$，需要先 flatten。

**解法：**

❌ 错误做法 — 忘记展平

```python
x = images  # shape: (32, 1, 28, 28)
y = model(x)  # ❌ Linear 层期望 (32, 784)
```

✅ 正确做法 — 在 forward 中 reshape

```python
def forward(self, x):
    x = x.view(x.size(0), -1)  # ✅ (B, 1, 28, 28) → (B, 784)
    x = self.fc1(x)
    return x
```

**教训：** 在 forward 方法开头加 flatten/reshape，或用 `nn.Flatten()` 层。

> 📖 Docs: [torch.Tensor.view](https://pytorch.org/docs/stable/generated/torch.Tensor.view.html)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别只看公式不动手** → 把手算练习做一遍，前向传播的核心就是矩阵乘法
2. [ ] **别跳过 shape 追踪** → 在纸上写出每一层的输入和输出 shape
3. [ ] **别混淆 forward 和 backprop** → forward 算预测值，backprop 算梯度，两件事

### 作业/项目避坑

1. [ ] **先跑通最简模型** → 2 层 MLP 跑通了再加复杂度
2. [ ] **打印中间 shape** → 在 forward 里加 `print(x.shape)` 调试
3. [ ] **命名要清晰** → `fc1, fc2` 比 `layer_a, my_layer` 好

### 考试/答辩避坑

1. [ ] **能画流程图** → 前向传播就是"仿射→激活→仿射→激活→输出"
2. [ ] **能写出一层的公式** → $a = \sigma(Wx + b)$
3. [ ] **能说出训练和推理的区别** → 训练缓存中间值，推理不缓存

### 调试清单（技术类）

1. [ ] **Shape 报错？** → 打印每层输入输出 shape，检查维度链
2. [ ] **推理结果不稳定？** → 是否忘了 `model.eval()`
3. [ ] **显存 OOM？** → 是否忘了 `torch.no_grad()`
4. [ ] **输出全是 0？** → 检查是否用了 ReLU + 负初始化导致死神经元
5. [ ] **输出全一样？** → 检查是否忘了激活函数（纯线性无法区分）
