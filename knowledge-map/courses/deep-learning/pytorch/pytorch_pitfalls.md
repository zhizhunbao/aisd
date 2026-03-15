---
topic: pytorch
dimension: pitfalls
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📖 Docs: [PyTorch Documentation](https://pytorch.org/docs/stable/) — v2.10"
  - "📖 Docs: [Autograd Mechanics](https://pytorch.org/docs/stable/notes/autograd.html)"
  - "📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf)"
  - "🧪 经验: 常见社区反馈与 StackOverflow 高频问题"
expiry: 6m
status: current
---

# PyTorch 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---


## 坑 1: 忘记清零梯度

**场景：** 训练循环中连续执行多个 batch

**症状：** 梯度值异常大，loss 爆炸或训练不收敛

**根因：** PyTorch 的梯度默认是**累加**的（`grad += new_grad`），不调用 `zero_grad()` 会导致多个 batch 的梯度叠加

**解法：**

❌ 错误写法 — 忘记清零

    for data, target in loader:
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        # 没有 zero_grad()！梯度会越来越大

✅ 正确写法 — 每个 batch 前清零

    for data, target in loader:
        optimizer.zero_grad()          # ← 必须在 backward 之前
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

**教训：** 训练循环铁三角顺序：`zero_grad() → backward() → step()`

> 📖 Docs: [Optimizer.zero_grad](https://pytorch.org/docs/stable/generated/torch.optim.Optimizer.zero_grad.html)

---


## 坑 2: eval 模式忘记切换

**场景：** 模型训练完后做推理/评估

**症状：** 评估时准确率不稳定（每次不一样），或比预期低

**根因：** `model.train()` 时 Dropout 会随机丢弃神经元、BatchNorm 使用当前 batch 统计量；如果推理时不切换 `eval()`，这些随机行为会污染结果

**解法：**

❌ 错误写法 — 直接推理

    # 训练完直接预测，Dropout 还在随机丢弃
    output = model(test_data)

✅ 正确写法 — 切换模式 + 禁用梯度

    model.eval()                   # ← 关闭 Dropout 和 BN 训练行为
    with torch.no_grad():          # ← 禁用梯度计算，节省内存
        output = model(test_data)

**教训：** 推理时必须 `model.eval()` + `torch.no_grad()`，训练时必须 `model.train()`

> 📖 Docs: [nn.Module.eval](https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval)

---


## 坑 3: 模型和数据不在同一设备

**场景：** 模型在 GPU 上，但数据还在 CPU（或反过来）

**症状：** `RuntimeError: Expected all tensors to be on the same device`

**根因：** PyTorch 不会自动迁移 Tensor，模型和数据必须显式放在同一个 device 上

**解法：**

❌ 错误写法 — 设备不一致

    model = model.cuda()
    data = torch.randn(10, 3)     # 默认在 CPU
    output = model(data)          # 💥 RuntimeError!

✅ 正确写法 — 统一设备

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    data = data.to(device)        # ← 两者在同一设备
    output = model(data)

**教训：** 定义一个 `device` 变量，所有 `.to(device)` 统一管理

> 📖 Docs: [CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)

---


## 坑 4: CrossEntropyLoss 输入搞错

**场景：** 使用 `nn.CrossEntropyLoss` 进行分类

**症状：** loss 值异常、模型不收敛、或维度报错

**根因：** `CrossEntropyLoss` 内部已包含 `log_softmax`，如果你的模型输出已经加了 `softmax`，就等于做了**两次 softmax**

**解法：**

❌ 错误写法 — 模型输出加了 softmax，再用 CrossEntropyLoss

    class BadModel(nn.Module):
        def forward(self, x):
            x = self.fc(x)
            return torch.softmax(x, dim=1)  # ← 多余的 softmax
    # CrossEntropyLoss 内部再做一次 log_softmax → 结果错误

✅ 正确写法 — 返回 raw logits

    class GoodModel(nn.Module):
        def forward(self, x):
            x = self.fc(x)
            return x                         # ← 直接返回 logits
    # CrossEntropyLoss 内部会做 log_softmax + NLLLoss

**教训：** 用 `CrossEntropyLoss` 时模型最后一层直接输出 logits，不要加 softmax

> 📖 Docs: [CrossEntropyLoss](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)

---


## 坑 5: in-place 操作破坏计算图

**场景：** 在需要梯度的 Tensor 上做 in-place 操作（如 `x += 1`, `x.add_(1)`）

**症状：** `RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation`

**根因：** Autograd 需要前向传播中间值来计算梯度，in-place 操作会覆盖这些值，导致反向传播时数据不一致

**解法：**

❌ 错误写法 — in-place 修改需要梯度的 Tensor

    x = torch.randn(3, requires_grad=True)
    y = x * 2
    y += 1        # ← in-place, 会破坏计算图

✅ 正确写法 — 用 out-of-place 操作

    x = torch.randn(3, requires_grad=True)
    y = x * 2
    y = y + 1     # ← 创建新 Tensor，计算图完整

**教训：** 参与梯度计算的 Tensor 避免 `_` 后缀操作（`add_`, `mul_`, `zero_`）和 `+=`

> 📖 Docs: [In-place operations with autograd](https://pytorch.org/docs/stable/notes/autograd.html#in-place-operations-with-autograd)

---


## 坑 6: DataLoader num_workers 在 Windows 报错

**场景：** 在 Windows 上设置 `num_workers > 0`

**症状：** `BrokenPipeError` 或 `RuntimeError: freeze_support`

**根因：** Windows 不支持 `fork`，多进程需要 `spawn`，而 `spawn` 要求代码在 `if __name__ == '__main__':` 保护下运行

**解法：**

❌ 错误写法 — Windows 下直接多 workers 无保护

    # script.py 文件顶层直接写
    loader = DataLoader(dataset, num_workers=4)
    for batch in loader:  # 💥 BrokenPipeError on Windows
        pass

✅ 正确写法 — 用 main 保护

    if __name__ == '__main__':
        loader = DataLoader(dataset, num_workers=4)
        for batch in loader:
            pass

**教训：** Windows 上 `num_workers > 0` 必须在 `if __name__ == '__main__':` 内；或设 `num_workers=0`

> 🧪 经验: Windows 多进程 DataLoader 常见问题

---


## 坑 7: 保存模型的方式不当

**场景：** 保存和加载训练好的模型

**症状：** 加载时报错 `ModuleNotFoundError`，或模型行为异常

**根因：** `torch.save(model)` 使用 pickle 序列化整个对象（包括类定义的引用路径），换个环境类路径变了就加载失败

**解法：**

❌ 错误写法 — 保存整个模型对象

    torch.save(model, 'model.pth')        # ← 依赖类定义的路径
    model = torch.load('model.pth')       # 换环境可能报错

✅ 正确写法 — 保存 state_dict

    # 保存 / Save
    torch.save(model.state_dict(), 'model_weights.pth')

    # 加载 / Load
    model = MyModel()                      # 先实例化模型
    model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

**教训：** 永远用 `state_dict()` 保存/加载权重，不要 pickle 整个模型

> 📖 Docs: [Saving and Loading Models](https://pytorch.org/tutorials/beginner/saving_loading_models.html)

---


## 坑 8: view 和 reshape 的区别

**场景：** 改变 Tensor 形状时选择 `view` 还是 `reshape`

**症状：** `view` 报错 `RuntimeError: view size is not compatible with input tensor's size and stride`

**根因：** `view` 要求 Tensor 内存连续（contiguous），转置、permute 后内存可能不连续

**解法：**

❌ 错误写法 — 转置后直接 view

    x = torch.randn(3, 4)
    x = x.T               # 转置后不连续
    x = x.view(12)        # 💥 RuntimeError

✅ 正确写法 — 用 reshape（自动处理）或先 contiguous

    x = torch.randn(3, 4).T
    x = x.reshape(12)             # ← reshape 自动处理不连续情况
    # 或
    x = x.contiguous().view(12)   # ← 显式确保连续

**教训：** 不确定是否连续时用 `reshape`，它在连续时等价于 `view`，不连续时自动复制

> 📖 Docs: [Tensor Views](https://pytorch.org/docs/stable/tensor_view.html)

---


## 坑 9: 学习率设置不当

**场景：** 训练模型时 loss 不下降或震荡

**症状：** loss 不收敛、NaN loss、或 loss 下降极慢

**根因：** 学习率过大导致梯度爆炸；过小导致收敛极慢；不同优化器有不同的最佳范围

**解法：**

❌ 错误写法 — SGD 的学习率给 Adam

    # Adam 默认 lr 范围: 1e-4 ~ 3e-4
    optimizer = optim.Adam(params, lr=0.1)   # ← 太大，loss 爆炸

✅ 正确写法 — 按优化器选择合理范围

    # Adam 推荐
    optimizer = optim.Adam(params, lr=1e-3)
    # SGD 推荐
    optimizer = optim.SGD(params, lr=0.01, momentum=0.9)

**教训：** Adam 一般 `lr=1e-3`，SGD 一般 `lr=0.01~0.1`；搭配 LR Scheduler 渐进调整

> 📚 Book: Stevens et al., [Deep Learning with PyTorch](../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.5

---


## 坑 10: GPU 显存泄漏

**场景：** 训练过程中 GPU 显存不断增长，最终 OOM

**症状：** `CUDA out of memory` 错误，或 `nvidia-smi` 显示显存持续增长

**根因：** 常见原因：(1) 在记录 loss 时保留了计算图引用 `losses.append(loss)` 而非 `losses.append(loss.item())`；(2) 中间变量未释放

**解法：**

❌ 错误写法 — 记录 loss Tensor（保留整个计算图）

    losses = []
    for data, target in loader:
        loss = criterion(model(data), target)
        losses.append(loss)           # ← loss Tensor 引用了整个计算图！

✅ 正确写法 — 用 .item() 提取标量值

    losses = []
    for data, target in loader:
        loss = criterion(model(data), target)
        loss.backward()
        losses.append(loss.item())    # ← .item() 返回 Python float，释放图引用

**教训：** 记录 loss/metrics 时永远用 `.item()` 或 `.detach()`，不要保留 Tensor 引用到计算图外

> 📖 Docs: [CUDA Memory Management](https://pytorch.org/docs/stable/notes/cuda.html#memory-management)

---


## 调试清单

1. [ ] **loss 不下降？** → 检查学习率是否合理（Adam: 1e-3, SGD: 0.01）
2. [ ] **loss 是 NaN？** → 检查数据是否有 NaN/Inf，学习率是否过大
3. [ ] **梯度全是 0？** → 检查是否中间有 `.detach()` 或 `torch.no_grad()` 截断了图
4. [ ] **GPU OOM？** → 减小 batch_size，使用 `torch.cuda.empty_cache()`，检查 loss 记录是否用了 `.item()`
5. [ ] **准确率不稳定？** → 检查推理时是否调了 `model.eval()`
6. [ ] **设备不一致？** → 统一 `device` 变量，所有 tensor/model 用 `.to(device)`
7. [ ] **DataLoader 报错？** → Windows 检查 `if __name__ == '__main__':`，减少 `num_workers`
8. [ ] **加载模型报错？** → 确认用 `state_dict` 保存/加载，不是 pickle 整个模型
9. [ ] **维度不匹配？** → 用 `print(x.shape)` 追踪每层输出形状
10. [ ] **训练/测试差距大？** → 检查是否过拟合（加 Dropout、数据增强、减小模型）
