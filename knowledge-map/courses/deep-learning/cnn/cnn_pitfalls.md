---
topic: cnn
dimension: pitfalls
created: 2026-03-12
last_verified: 2026-03-12
source_versions:
  - "📚 Book: [stevens_deep_learning_with_pytorch.pdf](../../../textbooks/stevens_deep_learning_with_pytorch.pdf) — Ch.8"
  - "📖 Docs: [PyTorch nn.Conv2d](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)"
  - "📖 Docs: [PyTorch Common Pitfalls](https://pytorch.org/docs/stable/notes/faq.html)"
  - "🧪 经验: CNN 训练实践经验总结"
expiry: 6m
status: current
---

# CNN 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---


## 坑 1: 输入尺寸不匹配导致 RuntimeError

**场景：** 将不同大小的图像输入 CNN，或修改网络结构后忘记更新全连接层的输入维度

**症状：** `RuntimeError: mat1 and mat2 shapes cannot be multiplied`

**根因：** 全连接层 `nn.Linear(in_features, ...)` 的 `in_features` 必须精确等于展平后的特征图大小。改了卷积层/池化层后，特征图尺寸变了，但 Linear 层没跟着改

**解法：**

❌ 错误写法 — 手动硬编码展平尺寸，改网络后忘记同步

    self.fc = nn.Linear(128 * 4 * 4, 10)  # 硬编码，换输入尺寸就炸

✅ 正确写法 — 用 Flatten + 动态计算，或用 AdaptiveAvgPool 固定输出

    # 方法1: 用 AdaptiveAvgPool 固定输出尺寸
    self.gap = nn.AdaptiveAvgPool2d((1, 1))  # 不管输入多大，输出都是 [B, C, 1, 1]
    self.fc = nn.Linear(128, 10)             # in_features = 通道数

    # 方法2: 用 dummy forward 自动计算
    def _get_flatten_size(self):
        dummy = torch.zeros(1, 3, 32, 32)
        x = self.features(dummy)
        return x.view(1, -1).size(1)

**教训：** 优先用 `AdaptiveAvgPool2d((1,1))` 替代 Flatten + 硬编码 Linear，网络结构变化时不会出错

> 📖 Docs: [PyTorch nn.AdaptiveAvgPool2d](https://pytorch.org/docs/stable/generated/torch.nn.AdaptiveAvgPool2d.html)

---


## 坑 2: 忘记 model.eval() 和 torch.no_grad()

**场景：** 测试/推理阶段直接用训练模式的模型

**症状：** 测试精度不稳定、每次推理结果不同、推理速度慢

**根因：** `model.train()` 模式下 BatchNorm 使用 batch 统计量（不稳定），Dropout 随机丢弃神经元。`torch.no_grad()` 不加会浪费显存存储梯度

**解法：**

❌ 错误写法 — 直接推理，忘记切模式

    # 训练完直接测试
    outputs = model(test_images)  # BN 和 Dropout 还在训练模式！

✅ 正确写法 — 切换到 eval 模式并禁用梯度

    model.eval()                           # 切换到评估模式
    with torch.no_grad():                  # 不计算梯度，省显存
        outputs = model(test_images)

**教训：** 测试/推理前**必须** `model.eval()` + `torch.no_grad()`，否则结果不可靠

> 📖 Docs: [PyTorch FAQ](https://pytorch.org/docs/stable/notes/faq.html)

---


## 坑 3: 数据未归一化导致训练不收敛

**场景：** 加载图像后直接丢进 CNN 训练

**症状：** Loss 不下降或下降极慢，训练不收敛

**根因：** 图像像素值范围 [0, 255]，数值太大导致梯度爆炸或优化困难。CNN 期望输入在 [-1, 1] 或 [0, 1] 范围内，最好按数据集均值/方差归一化

**解法：**

❌ 错误写法 — 只 ToTensor() 不 Normalize

    transform = transforms.Compose([
        transforms.ToTensor()               # 只转 [0,1]，没归一化
    ])

✅ 正确写法 — ToTensor + Normalize（使用数据集的均值和标准差）

    transform = transforms.Compose([
        transforms.ToTensor(),              # 转 [0,1]
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],     # ImageNet 均值（或自己数据集的）
            std=[0.229, 0.224, 0.225]       # ImageNet 标准差
        )
    ])

**教训：** **永远** Normalize，用 ImageNet 均值/方差（迁移学习）或自己数据集的统计量

> 📚 Book: Stevens et al., [《Deep Learning with PyTorch》](../../../textbooks/stevens_deep_learning_with_pytorch.pdf), Ch.8

---


## 坑 4: 过拟合——训练精度 99% 但测试精度 60%

**场景：** 小数据集训练深层 CNN，或没有使用任何正则化手段

**症状：** 训练 loss 持续下降到接近 0，测试 loss 先降后升，训练/测试精度差距越来越大

**根因：** 模型容量远大于数据量，网络"记住"了训练数据而非学到泛化特征

**解法：**

❌ 错误写法 — 没有任何正则化，直接堆层

    class OverfitNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 256, 3), nn.ReLU(),       # 太多参数
                nn.Conv2d(256, 512, 3), nn.ReLU(),
            )
            self.fc = nn.Linear(512 * 28 * 28, 10)    # 巨大的全连接层

✅ 正确写法 — 组合多种正则化手段

    class RegularizedNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 32, 3, padding=1),
                nn.BatchNorm2d(32),                    # ① BatchNorm
                nn.ReLU(),
                nn.MaxPool2d(2, 2),
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(32 * 16 * 16, 128),
                nn.Dropout(0.5),                       # ② Dropout
                nn.Linear(128, 10),
            )

    # ③ 数据增强
    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32, padding=4),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize(...)
    ])

    # ④ 权重衰减 (L2 正则化)
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

    # ⑤ 小数据？用迁移学习！
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

**教训：** 小数据集优先用迁移学习；自己训练时必须组合 BatchNorm + Dropout + 数据增强 + 权重衰减

> 🧪 经验: CNN 训练实践常见问题

---


## 坑 5: GPU/CPU 设备不一致导致 RuntimeError

**场景：** 模型在 GPU 上，但数据在 CPU 上（或反过来）

**症状：** `RuntimeError: Expected all tensors to be on the same device`

**根因：** PyTorch 不会自动把张量移到同一设备，需要手动确保 model 和 data 都在同一设备

**解法：**

❌ 错误写法 — 模型移到 GPU 但忘记移数据

    model = model.cuda()
    outputs = model(images)             # images 还在 CPU！

✅ 正确写法 — 统一用 device 变量管理

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    for images, labels in trainloader:
        images = images.to(device)      # 数据也移到同一设备
        labels = labels.to(device)
        outputs = model(images)

**教训：** 定义全局 `device` 变量，所有张量和模型都用 `.to(device)`

> 📖 Docs: [PyTorch CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)

---


## 坑 6: 通道顺序错误 (CHW vs HWC)

**场景：** 用 OpenCV/PIL 读图后直接输入 PyTorch CNN

**症状：** 模型输出异常或精度极低，但无报错

**根因：** PyTorch CNN 期望输入格式 `[B, C, H, W]`（通道在前），但 OpenCV 读取的是 `[H, W, C]`（通道在后），且是 BGR 顺序而非 RGB

**解法：**

❌ 错误写法 — 直接用 OpenCV 的 numpy 数组

    import cv2
    img = cv2.imread('cat.jpg')            # shape: (H, W, 3), BGR
    tensor = torch.from_numpy(img).float() # 还是 (H, W, 3)！
    tensor = tensor.unsqueeze(0)           # (1, H, W, 3) — 通道在最后，错了

✅ 正确写法 — 转 RGB + permute 通道

    import cv2
    img = cv2.imread('cat.jpg')            # (H, W, 3), BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # → RGB
    tensor = torch.from_numpy(img).float()
    tensor = tensor.permute(2, 0, 1)       # (H,W,C) → (C,H,W)
    tensor = tensor.unsqueeze(0) / 255.0   # 加 batch 维 + 归一化

    # 或者直接用 torchvision（自动处理）
    from torchvision import transforms
    from PIL import Image
    img = Image.open('cat.jpg')            # PIL 默认 RGB
    tensor = transforms.ToTensor()(img)    # 自动 HWC→CHW + [0,1]

**教训：** 优先用 `torchvision.transforms.ToTensor()` 或 PIL，避免手动处理通道顺序

> 📖 Docs: [torchvision.transforms.ToTensor](https://pytorch.org/vision/stable/generated/torchvision.transforms.ToTensor.html)

---


## 坑 7: 学习率设置不当

**场景：** 学习率太大或太小

**症状：** 太大 → Loss 剧烈震荡或 NaN；太小 → Loss 下降极慢或卡在局部最优

**根因：** CNN 不同层的梯度量级不同，固定学习率难以兼顾所有层

**解法：**

❌ 错误写法 — 用过大学习率且不调度

    optimizer = optim.SGD(model.parameters(), lr=0.1)  # 太大，可能发散
    # 训练 100 epoch，学习率始终不变

✅ 正确写法 — 合理初始值 + 学习率调度

    # Adam 默认 lr=0.001 通常是好的起点
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 或 SGD + 学习率调度
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

    for epoch in range(100):
        train_one_epoch(...)
        scheduler.step()                   # 每 30 epoch 学习率乘 0.1

**教训：** 新手用 Adam(lr=0.001)；进阶用 SGD + Momentum + Scheduler；训练时一定要可视化 loss 曲线

> 🧪 经验: 学习率是最重要的超参数之一

---


## 坑 8: 忘记 optimizer.zero_grad() 导致梯度累积

**场景：** 训练循环中漏写 `optimizer.zero_grad()`

**症状：** Loss 下降异常（可能震荡或不降），模型行为不可预测

**根因：** PyTorch 默认会**累积**梯度（而非覆盖），如果不手动清零，新的梯度会叠加在旧梯度上

**解法：**

❌ 错误写法 — 忘记清零梯度

    for images, labels in trainloader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()                    # 梯度在累积！
        optimizer.step()

✅ 正确写法 — 每个 batch 开始时清零

    for images, labels in trainloader:
        optimizer.zero_grad()              # ← 必须在 backward() 前清零
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

**教训：** 训练循环三步曲：`zero_grad()` → `backward()` → `step()`，顺序不能乱

> 📖 Docs: [PyTorch FAQ](https://pytorch.org/docs/stable/notes/faq.html)

---


## 调试清单

1. [ ] **输出尺寸正确吗？** → 用 `print(x.shape)` 在每层后打印 shape
2. [ ] **数据归一化了吗？** → 检查 `transforms.Normalize()` 参数
3. [ ] **model.eval() 了吗？** → 测试前必须调用
4. [ ] **设备一致吗？** → `model.device` 和 `tensor.device` 要相同
5. [ ] **通道顺序对吗？** → PyTorch 用 CHW，OpenCV 用 HWC
6. [ ] **Loss 在下降吗？** → 画 loss-epoch 曲线
7. [ ] **梯度正常吗？** → 检查是否有 NaN，用 `torch.nn.utils.clip_grad_norm_()` 裁剪
8. [ ] **过拟合了吗？** → 训练/测试 loss 曲线是否分叉
9. [ ] **optimizer.zero_grad() 了吗？** → 检查是否在正确位置
10. [ ] **学习率合适吗？** → 尝试 learning rate finder
