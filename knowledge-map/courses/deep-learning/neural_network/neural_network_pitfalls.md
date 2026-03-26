---
topic: neural_network
dimension: pitfalls
created: 2026-03-23
last_verified: 2026-03-23
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6–Ch.8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📖 Paper: Glorot & Bengio, 'Understanding the difficulty of training deep feedforward neural networks', AISTATS 2010 — http://proceedings.mlr.press/v9/glorot10a.html"
  - "📖 Paper: He et al., 'Delving Deep into Rectifiers', ICCV 2015 — https://arxiv.org/abs/1502.01852"
  - "📖 Docs: PyTorch Common Mistakes — https://pytorch.org/tutorials/"
  - "🧪 经验: 常见训练调试经验"
expiry: 6m
status: current
---

# Neural Network (神经网络) 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 损失不下降 — 学习率设置不当

**痛点类别：** 💻 代码跑不通 / 结果对不上

**场景：** 第一次训练神经网络，loss 从第一个 epoch 就不动或者 NaN

**症状：** loss 一直保持不变（太小的学习率），或者直接变成 NaN/inf（太大的学习率）

**根因：** 学习率是神经网络**最敏感的超参数**。太小导致参数几乎不更新；太大导致更新步幅过大、越过最小值、甚至数值溢出。

**解法：**

❌ 错误做法 — 随意设一个固定学习率就开始训练

```python
# 学习率 = 1.0 ← 对多数问题来说太大了
optimizer = optim.SGD(model.parameters(), lr=1.0)
```

✅ 正确做法 — 从常用默认值开始，配合学习率调度

```python
# Adam 的默认学习率 0.001 对大多数问题是好的起点
optimizer = optim.Adam(model.parameters(), lr=0.001)
# 每10个epoch衰减为之前的0.1倍 / Decay ×0.1 every 10 epochs
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
```

**教训：** 先用 Adam(lr=0.001) 作为基线，确认能训练后再调。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.1
> 🧪 经验: 几乎所有新手的第一个坑

---

## 坑 2: 梯度消失 / 爆炸 — 激活函数和初始化不匹配

**痛点类别：** 🧠 概念听不懂 / 似懂非懂 + 💻 代码跑不通

**场景：** 网络超过 5 层后，训练变得极慢或完全不动

**症状：** 浅层的梯度趋近于 0（消失）或极大值（爆炸），导致浅层参数几乎不更新

**根因：** Sigmoid/Tanh 的导数最大值 < 1，反向传播中连乘多次后梯度指数衰减。权重初始化太大则梯度爆炸，太小则梯度消失。

**解法：**

❌ 错误做法 — 深网络使用 Sigmoid + 随机初始化

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.Sigmoid(),  # Sigmoid 在深层网络中会导致梯度消失
    nn.Linear(256, 128), nn.Sigmoid(),
    nn.Linear(128, 64),  nn.Sigmoid(),
    nn.Linear(64, 10)
)
```

✅ 正确做法 — 使用 ReLU + He 初始化

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.ReLU(),  # ReLU 梯度不会连乘衰减
    nn.Linear(256, 128), nn.ReLU(),
    nn.Linear(128, 64),  nn.ReLU(),
    nn.Linear(64, 10)
)
# He 初始化 (配合 ReLU)
for m in model:
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
```

**教训：** 深度 > 3 层的网络，默认用 ReLU + He 初始化。只在输出层按需用 Sigmoid/Softmax。

> 📖 Paper: Glorot & Bengio, [Understanding difficulty of training deep feedforward NN](http://proceedings.mlr.press/v9/glorot10a.html), 2010
> 📖 Paper: He et al., [Delving Deep into Rectifiers](https://arxiv.org/abs/1502.01852), 2015

---

## 坑 3: 过拟合 — 训练正确率 99% 但测试只有 60%

**痛点类别：** 📝 作业不会做 / 不知道怎么开始

**场景：** 训练集上表现完美，拿到测试集上效果断崖式下降

**症状：** Train Loss 持续下降，Validation Loss 在某个 epoch 后开始上升

**根因：** 网络参数太多、数据太少时，网络会"背答案"而不是学规律。它记住了训练数据的噪声和细节，而不是泛化特征。

**解法：**

❌ 错误做法 — 用一个巨大的网络训练小数据集，不加任何正则化

```python
# 1000个样本用8层网络 ← 参数远多于数据
model = nn.Sequential(
    nn.Linear(784, 1024), nn.ReLU(),
    nn.Linear(1024, 1024), nn.ReLU(),
    nn.Linear(1024, 512), nn.ReLU(),
    nn.Linear(512, 10)
)
```

✅ 正确做法 — 控制模型大小 + 多种正则化

```python
model = nn.Sequential(
    nn.Linear(784, 128), nn.ReLU(),
    nn.Dropout(0.3),              # Dropout: 训练时随机关闭30%的神经元
    nn.Linear(128, 64), nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(64, 10)
)
# 配合 Early Stopping: 当 validation loss 连续 N 个 epoch 不下降时停止训练
# 配合 Weight Decay: optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```

**教训：** 过拟合是默认会发生的事。防线顺序：① 更多数据 ② 数据增强 ③ Dropout ④ 权重衰减 ⑤ Early Stopping ⑥ 减小模型。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.7

---

## 坑 4: 忘记 model.eval() — 推理时 Dropout/BN 行为不对

**痛点类别：** 💻 代码跑不通 / 结果对不上

**场景：** 训练完的模型在测试时结果不稳定或准确率比训练时低很多

**症状：** 每次推理结果不一样（Dropout 还在生效）；BatchNorm 使用了 batch 统计量而非全局统计量

**根因：** PyTorch 中 Dropout 和 BatchNorm 在 train/eval 模式下行为不同。如果不切换，推理时 Dropout 仍然随机丢弃神经元。

**解法：**

❌ 错误做法 — 训练完直接预测

```python
# 忘记切换模式 ← Dropout 仍然生效，每次结果不同
output = model(test_input)
```

✅ 正确做法 — 推理前切换 + 禁用梯度

```python
model.eval()                  # 关闭 Dropout，BN 用全局统计量
with torch.no_grad():         # 不计算梯度，节省内存
    output = model(test_input)
```

**教训：** 训练循环用 `model.train()`，推理/测试用 `model.eval()` + `torch.no_grad()`，这是 PyTorch 的固定套路。

> 📖 Docs: [PyTorch nn.Module train/eval](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)
> 🧪 经验: 几乎每个 PyTorch 新手都犯过

---

## 坑 5: 维度不匹配 — RuntimeError: mat1 and mat2 shapes cannot be multiplied

**痛点类别：** 💻 代码跑不通 / 结果对不上

**场景：** 第一次自定义网络结构就报维度错误

**症状：** `RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x784 and 256x128)`

**根因：** 上一层的输出维度 ≠ 下一层的输入维度。前一层 `nn.Linear(784, 256)` 输出 256 维，下一层必须 `nn.Linear(256, ...)` 开头。

**解法：**

❌ 错误做法 — 层与层之间维度不连贯

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.ReLU(),
    nn.Linear(128, 64),  nn.ReLU(),   # 128 ≠ 256 ← 报错！
    nn.Linear(64, 10)
)
```

✅ 正确做法 — 保证每层输入 = 上层输出

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.ReLU(),   # 输出 256
    nn.Linear(256, 128), nn.ReLU(),   # 输入 256 ← 匹配！
    nn.Linear(128, 10)                # 输入 128 ← 匹配！
)
```

**教训：** 定义网络时，用注释标注每层的输入/输出维度。复杂网络可以先用 `torchsummary` 打印shape。

> 🧪 经验: 最常见的 PyTorch 报错之一

---

## 超级避坑指南

### 学习避坑

1. [ ] **别死记公式** → 先理解"前向=加权求和+激活"，"反向=链式法则"
2. [ ] **别跳过手算** → 用 2×2 网络手算一次前向+反向传播，比看 10 篇教程有效
3. [ ] **别混淆反向传播和梯度下降** → 反向传播算梯度，梯度下降更新参数，两件事
4. [ ] **别被名词吓住** → "损失函数"就是"算差距"，"激活函数"就是"加非线性"
5. [ ] **从 XOR 开始** → 不要第一个项目就搞 ImageNet

### 作业/项目避坑

1. [ ] **先跑通最简版** → 2 层网络 + 小数据集，确认训练流程对了再加复杂度
2. [ ] **打印中间结果** → 每个 epoch 打印 loss、grad norm、accuracy
3. [ ] **固定随机种子** → `torch.manual_seed(42)` 保证可复现
4. [ ] **保存模型检查点** → `torch.save(model.state_dict(), 'best.pt')`
5. [ ] **Version Control** → 不同实验用 git branch 管理

### 考试/答辩避坑

1. [ ] **画计算图** → 被问反向传播时，先画出前向传播的计算图，再沿反方向写梯度
2. [ ] **回到直觉** → 被问公式时，先说一句白话解释
3. [ ] **UAT 的局限** → 万能近似定理只保证存在性，不保证能找到（考试常考）

### 调试清单（技术类）

1. [ ] **Loss 不下降？** → 检查学习率（试 1e-3, 1e-4），检查数据标签是否正确
2. [ ] **Loss = NaN？** → 学习率太大 / 数值溢出 → 降低学习率，检查 log(0) 或 exp(大数)
3. [ ] **准确率停在随机水平？** → 检查标签是否 shuffle，检查模型输出层（分类要用 Softmax/CE）
4. [ ] **过拟合？** → 加 Dropout, Weight Decay, Early Stopping
5. [ ] **GPU OOM？** → 减 batch_size，减模型大小，检查是否在 for loop 里累积了计算图
