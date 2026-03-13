---
topic: tensor
dimension: pitfalls
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.3"
  - "📖 Docs: [PyTorch torch.Tensor](https://pytorch.org/docs/stable/tensors.html)"
  - "📖 Docs: [PyTorch Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)"
expiry: 6m
status: current
---

# Tensor 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---


## 坑 1: GPU Tensor 无法转 NumPy

**场景：** 在 GPU 上训练完，想把结果转成 NumPy 数组做可视化

**症状：** `TypeError: can't convert cuda:0 device type tensor to numpy.`

**根因：** NumPy 只支持 CPU 内存，GPU Tensor 必须先移回 CPU

**解法：**

❌ 错误写法 — 直接对 GPU Tensor 调 `.numpy()`

    t_gpu = torch.randn(3, device='cuda')
    result = t_gpu.numpy()   # TypeError!

✅ 正确写法 — 先 `.cpu()` 再 `.numpy()`

    result = t_gpu.cpu().numpy()

**教训：** GPU → NumPy 的转换链是 `.cpu().numpy()`，有梯度的加 `.detach()`

> 📖 Docs: [PyTorch Tensor Tutorial — Bridge with NumPy](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html#bridge-with-numpy)

---


## 坑 2: 有梯度的 Tensor 转 NumPy 报错

**场景：** 想查看模型参数的数值

**症状：** `RuntimeError: Can't call numpy() on Tensor that requires grad.`

**根因：** 追踪梯度的 Tensor 不允许直接转 NumPy（会破坏计算图的完整性）

**解法：**

❌ 错误写法 — 直接调 `.numpy()`

    param = model.weight   # requires_grad=True
    arr = param.numpy()     # RuntimeError!

✅ 正确写法 — 先 `.detach()` 断开计算图

    arr = param.detach().cpu().numpy()

**教训：** 完整转换链：`.detach().cpu().numpy()`（先断梯度 → 移 CPU → 转数组）

> 📖 Docs: [PyTorch Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)

---


## 坑 3: view() 在非连续 Tensor 上报错

**场景：** 对 `transpose()` 或 `permute()` 后的 Tensor 调用 `view()`

**症状：** `RuntimeError: view size is not compatible with input tensor's size and stride`

**根因：** `view()` 要求 Tensor 在内存中连续存储。转置操作只改变 stride，不搬数据，导致非连续

**解法：**

❌ 错误写法 — 转置后直接 `view()`

    t = torch.randn(3, 4)
    t_t = t.transpose(0, 1)   # 非连续!
    result = t_t.view(12)      # RuntimeError!

✅ 正确写法 — 用 `reshape()` 或先 `.contiguous()`

    result = t_t.reshape(12)               # 自动处理
    result = t_t.contiguous().view(12)     # 手动先变连续

**教训：** 优先用 `reshape()`，它自动处理连续性。只有确定 Tensor 连续时才用 `view()`

> 📖 Docs: [PyTorch Tensor Views](https://pytorch.org/docs/stable/tensor_view.html)

---


## 坑 4: 不同 Device 的 Tensor 运算报错

**场景：** 一个 Tensor 在 CPU，一个在 GPU，试图做加法

**症状：** `RuntimeError: Expected all tensors to be on the same device`

**根因：** PyTorch 不会自动迁移 Tensor，必须显式统一 device

**解法：**

❌ 错误写法 — 不检查 device 直接运算

    t_cpu = torch.randn(3)
    t_gpu = torch.randn(3, device='cuda')
    result = t_cpu + t_gpu    # RuntimeError!

✅ 正确写法 — 统一 device 后再运算

    result = t_cpu.to(t_gpu.device) + t_gpu

**教训：** 养成习惯在函数开头统一 device：`device = next(model.parameters()).device`

> 📖 Docs: [PyTorch CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)

---


## 坑 5: `torch.tensor()` vs `torch.from_numpy()` 内存差异

**场景：** 从 NumPy 数组创建 Tensor，修改 NumPy 数组后期望 Tensor 同步变化

**症状：** 用 `torch.tensor()` 创建的 Tensor 不随 NumPy 变化

**根因：** `torch.tensor()` 总是**拷贝**数据，`torch.from_numpy()` **共享**底层内存

**解法：**

❌ 错误期望 — 用 `torch.tensor()` 创建后期望共享

    np_arr = np.array([1.0, 2.0])
    t = torch.tensor(np_arr)
    np_arr[0] = 99
    print(t)    # tensor([1., 2.]) ← 没有变!

✅ 正确做法 — 用 `torch.from_numpy()` 共享内存

    t = torch.from_numpy(np_arr)
    np_arr[0] = 99
    print(t)    # tensor([99.,  2.]) ← 同步了!

**教训：** 需要共享用 `from_numpy()`，需要隔离用 `torch.tensor()`；不确定时用 `torch.as_tensor()`（尽量共享）

> 📖 Docs: [PyTorch torch.tensor](https://pytorch.org/docs/stable/generated/torch.tensor.html)

---


## 坑 6: 原地操作破坏 autograd 计算图

**场景：** 训练循环中用 `add_()` 等原地操作修改了需要梯度的 Tensor

**症状：** `RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation`

**根因：** 原地操作会覆盖 autograd 需要的中间值，导致反向传播无法计算正确梯度

**解法：**

❌ 错误写法 — 对需要梯度的 Tensor 做原地操作

    x = torch.tensor([1.0], requires_grad=True)
    y = x * 2
    y.add_(1)        # 原地修改 y！
    y.backward()     # RuntimeError!

✅ 正确写法 — 用 out-of-place 操作

    x = torch.tensor([1.0], requires_grad=True)
    y = x * 2
    y = y + 1        # 创建新 Tensor
    y.backward()     # ✅ 正常

**教训：** 在训练代码中避免 `_` 后缀的原地操作。只在推理或不需要梯度时使用

> 📖 Docs: [PyTorch Autograd Mechanics — In-place operations](https://pytorch.org/docs/stable/notes/autograd.html)

---


## 坑 7: 忘记梯度清零导致梯度累积

**场景：** 训练循环中多次 `backward()` 后，梯度越来越大

**症状：** 模型 loss 不降反升，或者出现 NaN

**根因：** PyTorch 默认**累积**梯度（`.grad += 新梯度`），不会自动清零

**解法：**

❌ 错误写法 — 训练循环中不清零

    for batch in dataloader:
        loss = model(batch)
        loss.backward()      # 梯度累积!
        optimizer.step()

✅ 正确写法 — 每个 batch 前清零

    for batch in dataloader:
        optimizer.zero_grad()   # ← 必须!
        loss = model(batch)
        loss.backward()
        optimizer.step()

**教训：** `optimizer.zero_grad()` 是训练循环的标准第一步，永远不要忘记

> 📖 Docs: [PyTorch Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)

---


## 坑 8: dtype 不匹配的隐蔽 bug

**场景：** 整数 Tensor 做除法得到错误结果

**症状：** `torch.tensor([5]) / torch.tensor([2])` 得到 `tensor([2])` 而不是 `2.5`（旧版行为）

**根因：** 整数 Tensor 之间的除法在某些版本中执行整数除法

**解法：**

❌ 容易忽略的问题 — 不关注 dtype

    t = torch.tensor([1, 2, 3])   # int64
    mean = t.sum() / len(t)        # 可能丢精度

✅ 正确写法 — 显式使用浮点类型

    t = torch.tensor([1, 2, 3], dtype=torch.float32)
    mean = t.sum() / len(t)        # 正确的浮点除法

**教训：** 需要浮点精度时，创建 Tensor 时就指定 `dtype=torch.float32`

> 📖 Docs: [PyTorch torch.dtype](https://pytorch.org/docs/stable/tensor_attributes.html)

---


## 坑 9: from_numpy 的共享内存陷阱

**场景：** 修改了原 NumPy 数组，导致 Tensor 数据意外改变

**症状：** 调试时 Tensor 的值和预期不一致

**根因：** `torch.from_numpy()` 创建的 Tensor 与原 NumPy 数组共享底层内存

**解法：**

❌ 危险写法 — 创建后继续修改原 NumPy 数组

    features = np.load('data.npy')
    t = torch.from_numpy(features)
    features[:] = 0    # 清空 NumPy → Tensor 也被清空!

✅ 安全写法 — 需要隔离时用 clone()

    t = torch.from_numpy(features).clone()   # 拷贝，互不影响

**教训：** 如果后续还会修改原 NumPy 数据，用 `.clone()` 或 `torch.tensor()` 隔离

> 📖 Docs: [PyTorch torch.from_numpy](https://pytorch.org/docs/stable/generated/torch.from_numpy.html)

---


## 坑 10: Broadcasting 维度不匹配的隐蔽错误

**场景：** 对两个看似兼容但实际含义不同的 Tensor 做逐元素运算

**症状：** 没有报错，但结果 shape 意外膨胀，或数值错误

**根因：** Broadcasting 会自动扩展维度，即使你并不希望这样

**解法：**

❌ 隐蔽的 bug — 维度含义不同但 shape 恰好兼容

    weights = torch.randn(10)        # (10,) — 10 个样本的权重
    features = torch.randn(10, 5)    # (10, 5) — 10 × 5 特征
    # 想按样本加权，但 broadcasting 把 weights 扩展成了 (10, 5)
    result = weights * features      # shape (10, 5) — 哪个维度在乘?

✅ 安全写法 — 显式 unsqueeze 明确维度

    result = weights.unsqueeze(1) * features   # (10, 1) * (10, 5) → (10, 5)

**教训：** Broadcasting 很强大但也很隐蔽。当 shape 模糊时，显式 `unsqueeze()` 或 `reshape()` 明确意图

> 📖 Docs: [PyTorch Broadcasting Semantics](https://pytorch.org/docs/stable/notes/broadcasting.html)

---


## 调试清单

1. [ ] **是否在正确的 device 上？** → `print(tensor.device)` 检查
2. [ ] **dtype 是否正确？** → `print(tensor.dtype)` 确认是 float32 还是 int64
3. [ ] **shape 是否符合预期？** → `print(tensor.shape)` 检查每个维度
4. [ ] **是否连续存储？** → `tensor.is_contiguous()` 检查（view 报错时）
5. [ ] **梯度是否清零？** → 训练循环开头 `optimizer.zero_grad()`
6. [ ] **是否有 NaN/Inf？** → `torch.isnan(tensor).any()` / `torch.isinf(tensor).any()`
7. [ ] **内存是否共享？** → `torch.from_numpy` 创建的要注意副作用
8. [ ] **Broadcasting 是否正确？** → 显式 `unsqueeze()` 避免歧义
9. [ ] **原地操作是否安全？** → 有 `requires_grad` 时避免 `_` 后缀方法
10. [ ] **GPU 内存是否足够？** → `torch.cuda.memory_summary()` 查看
