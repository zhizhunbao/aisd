---
topic: transfer_learning
dimension: pitfalls
created: 2026-03-18
last_verified: 2026-03-18
source_versions:
  - "📖 Paper: Yosinski et al., 'How transferable are features?', NeurIPS 2014 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/transfer_learning/yosinski_2014_transferable_features.pdf"
  - "📖 Paper: Howard & Ruder, 'ULMFiT', ACL 2018 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/.documents/papers/transfer_learning/howard_2018_ulmfit.pdf"
  - "📖 Docs: PyTorch Transfer Learning Tutorial — https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html"
  - "🧪 经验: 常见 Fine-tuning 和冻结层错误"
expiry: 6m
status: current
---

# Transfer Learning 踩坑记录

> ⚠️ **围绕学习痛点组织**，不是技术 debug 日志。每次踩坑后请追加条目。

---

## 坑 1: 忘了用 ImageNet 归一化参数

**痛点类别：** 代码类 — 预处理不匹配

**场景：** 用 ImageNet 预训练的 ResNet 做 Fine-tuning，但数据预处理时用了自己的均值/标准差或者干脆没做归一化。

**症状：** 模型性能很差，甚至不如从头训练。Loss 不下降或者一开始就很高。

**根因：** 预训练模型的卷积核是在 ImageNet 归一化后的数据上训练的（mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]）。输入分布不匹配，特征提取器的输出就是垃圾。

**解法：**

❌ 错误做法 — 不归一化或用错参数

```python
# ❌ 没有归一化
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),  # 只有 ToTensor，没有 Normalize
])
```

✅ 正确做法 — 使用 ImageNet 归一化参数

```python
# ✅ 必须用 ImageNet 的均值和标准差
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

**教训：** 预训练模型 = 特征提取器。特征提取器期望特定的输入格式，就像函数期望特定的输入类型一样。

> 📖 Docs: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

---

## 坑 2: Fine-tuning 学习率太大导致灾难性遗忘

**痛点类别：** 概念类 — 不理解学习率和预训练的关系

**场景：** 用标准学习率（如 1e-2）Fine-tune 预训练模型。

**症状：** 第一个 epoch 性能暴跌，之后缓慢恢复但达不到 Feature Extraction 的水平。

**根因：** 预训练参数处于损失曲面的一个好区域。太大的学习率一步就把参数推到了远离这个好区域的地方。预训练学到的边缘检测、纹理识别等通用特征被"冲掉"了——这叫**灾难性遗忘 (Catastrophic Forgetting)**。

**解法：**

❌ 错误做法 — 用标准学习率

```python
# ❌ 1e-2 对 Fine-tuning 太大了
optimizer = optim.SGD(model.parameters(), lr=0.01)
```

✅ 正确做法 — 用小学习率（比从头训练小 10-100 倍）

```python
# ✅ Fine-tuning 标准学习率范围
# CV: 1e-4 ~ 1e-5
# NLP (BERT): 2e-5 ~ 5e-5
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
```

**教训：** Fine-tuning ≠ 从头训练。起点不同，步长也要不同。

> 📖 Paper: Howard & Ruder, [ULMFiT (2018)](../../../.documents/papers/transfer_learning/howard_2018_ulmfit.pdf), Section 3.3

---

## 坑 3: 冻结层后忘了只优化可训练参数

**痛点类别：** 代码类 — 冻结但把所有参数传给优化器

**场景：** 设置了 `requires_grad = False` 冻结层，但 `optim.Adam(model.parameters(), ...)` 仍然传入了所有参数。

**症状：** 不会报错，但训练变慢（优化器维护了大量不需要的动量/方差状态）；且如果用了 weight_decay，会错误地衰减冻结参数。

**解法：**

❌ 错误做法 — 传入所有参数

```python
# ❌ 冻结了但还传入所有参数
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(512, 10)
optimizer = optim.Adam(model.parameters(), lr=1e-3)  # 浪费内存
```

✅ 正确做法 — 只传可训练参数

```python
# ✅ 用 filter 只传 requires_grad=True 的参数
optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-3
)
# 或者直接传新层的参数
# optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)
```

**教训：** 冻结只是把 `requires_grad` 关了，优化器不会自动忽略。

> 📖 Docs: [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

---

## 坑 4: 在差异太大的域之间迁移（负迁移）

**痛点类别：** 概念类 — 不理解域相似性的重要性

**场景：** 用 ImageNet（自然图片）预训练模型直接迁移到完全不同的域（如频谱图、卫星雷达图、医学 CT）。

**症状：** Fine-tuning 后性能不如从头训练。

**根因：** ImageNet 学到的边缘/纹理/物体部件等特征对自然图片有用，但对频谱图或雷达图可能完全无关。底层特征的迁移前提是"特征在两个域上都有用"。

**解法：**

✅ 正确做法 — 评估域相似性，必要时从头训练或用更相似的预训练模型

```python
# ✅ 策略 1: 找域更相似的预训练模型
# 医学影像 → 用在 CheXpert/RadImageNet 上预训练的模型
# 遥感影像 → 用在 SatlasPretrain 上预训练的模型

# ✅ 策略 2: 域差异大时，多解冻一些层
for param in model.parameters():
    param.requires_grad = True  # 全部解冻
# 用更小的学习率
optimizer = optim.Adam(model.parameters(), lr=1e-5)
```

**教训：** 迁移学习不是万能药。源域和目标域的相关性决定了迁移的收益。

> 📖 Paper: Yosinski et al., [How transferable are features? (2014)](../../../.documents/papers/transfer_learning/yosinski_2014_transferable_features.pdf), Section 5

---

## 坑 5: BERT Fine-tuning 不加 Warmup

**痛点类别：** 代码类 — NLP 特有的训练技巧

**场景：** Fine-tune BERT 时不加学习率预热（warmup），直接用目标学习率。

**症状：** 训练初期 loss 剧烈震荡，最终收敛效果差。

**根因：** 预训练模型的参数分布和 Fine-tuning 数据的梯度分布差异较大。初始时需要用很小的学习率"预热"（逐渐增大到目标值），让模型平滑地过渡。

**解法：**

❌ 错误做法 — 不加 warmup

```python
# ❌ 直接用目标学习率
training_args = TrainingArguments(
    learning_rate=2e-5,
    warmup_steps=0,  # ❌ 没有预热
)
```

✅ 正确做法 — 加 warmup（通常 6-10% 的总步数）

```python
# ✅ 加学习率预热
training_args = TrainingArguments(
    learning_rate=2e-5,
    warmup_steps=500,        # ✅ 或者用 warmup_ratio=0.06
    num_train_epochs=3,
)
```

**教训：** Warmup 是 Transformer Fine-tuning 的标配，不是可选项。

> 📖 Docs: [Hugging Face TrainingArguments](https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments)

---

## 超级避坑指南

### 学习避坑

1. [ ] **别混淆 Feature Extraction 和 Fine-tuning** → 前者冻结全部，后者解冻部分/全部
2. [ ] **别以为迁移学习总是好的** → 域差异太大时会负迁移
3. [ ] **别忘了预训练模型的输入格式要求** → ImageNet 归一化、BERT 分词器

### 作业/项目避坑

1. [ ] **归一化参数必须匹配预训练** → ImageNet: mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]
2. [ ] **Fine-tuning 学习率要小** → CV: 1e-4, NLP: 2e-5
3. [ ] **优化器只传可训练参数** → `filter(lambda p: p.requires_grad, ...)`
4. [ ] **BERT Fine-tuning 必须加 warmup** → warmup_ratio=0.06

### 调试清单（技术类）

1. [ ] **Fine-tuning 后性能暴跌？** → 学习率太大 → 降到 1e-5 试试
2. [ ] **Feature Extraction 效果差？** → 可能需要解冻更多层
3. [ ] **Loss 一开始就很高？** → 检查归一化参数是否匹配预训练
4. [ ] **模型很大但只有少量数据？** → 用 Feature Extraction 或 LoRA
5. [ ] **NLP 模型 loss 震荡？** → 加 warmup + 减小学习率
