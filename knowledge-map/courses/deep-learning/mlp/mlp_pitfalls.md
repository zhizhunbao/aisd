---
topic: mlp
dimension: pitfalls
created: 2026-03-14
last_verified: 2026-03-14
source_versions:
  - "📚 Book: Goodfellow et al., Deep Learning Ch.6-8 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/goodfellow_deep_learning.pdf"
  - "📚 Book: Bishop, PRML Ch.5 — file:///C:/Users/40270/OneDrive/Desktop/workspace/aisd/textbooks/bishop_prml.pdf"
  - "📖 Paper: Glorot & Bengio 2010 — http://proceedings.mlr.press/v9/glorot10a.html"
  - "📖 Paper: He et al. 2015 — https://arxiv.org/abs/1502.01852"
  - "📖 Docs: PyTorch nn — https://pytorch.org/docs/stable/nn.html"
  - "🧪 经验: 常见 MLP 训练错误与调试经验"
expiry: 6m
status: current
---

# MLP (Multi-Layer Perceptron) 踩坑记录

> ⚠️ **这是知识库中最有价值的维度。** 每次踩坑后请追加条目。

---

## 坑 1: 忘记展平输入导致维度错误

**场景：** 将图像数据（如 MNIST `[B, 1, 28, 28]`）直接喂入 `nn.Linear` 层

**症状：** `RuntimeError: mat1 and mat2 shapes cannot be multiplied (32x1 and 784x128)`

**根因：** `nn.Linear` 期望 2D 输入 `[batch, features]`，但图像数据是 4D `[B, C, H, W]`

**解法：**

❌ 错误写法 — 直接传入未展平的张量

```python
class BadMLP(nn.Module):
    def forward(self, x):
        return self.fc1(x)  # x 形状 [B,1,28,28]，nn.Linear 无法处理
```

✅ 正确写法 — 在第一层之前展平

```python
class GoodMLP(nn.Module):
    def forward(self, x):
        x = x.view(x.size(0), -1)  # [B,1,28,28] → [B,784]
        # 或用 x = x.flatten(1)    # 等价写法 / Equivalent
        return self.fc1(x)
```

**教训：** MLP 要求输入是 2D 的 `[batch, features]`，图像输入必须先 flatten

> 📖 Docs: [PyTorch nn.Linear](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html)

---

## 坑 2: 未归一化输入导致训练不稳定

**场景：** 将原始像素值 [0, 255] 或特征范围差异很大的数据直接喂入 MLP

**症状：** 训练损失不下降、NaN loss、或收敛极慢

**根因：** 输入量级太大会导致激活值饱和（sigmoid/tanh）或梯度爆炸。不同特征量级差异大时，梯度方向被大量级特征主导。

**解法：**

❌ 错误写法 — 原始数据直接训练

```python
# 像素值 [0, 255] 直接喂入
x = torch.tensor(raw_image, dtype=torch.float32)
output = model(x)  # 大值导致梯度爆炸
```

✅ 正确写法 — 标准化输入

```python
# 方法 1: 归一化到 [0, 1]
transform = transforms.Compose([
    transforms.ToTensor(),                      # 自动缩放到 [0, 1]
    transforms.Normalize((0.1307,), (0.3081,))  # 进一步标准化
])

# 方法 2: StandardScaler (sklearn)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # 均值0, 方差1
X_test = scaler.transform(X_test)        # 用训练集的统计量!
```

**教训：** 永远标准化输入数据。用训练集的统计量（均值/方差）处理测试集。

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.1

---

## 坑 3: 全零初始化导致对称性问题

**场景：** 将所有权重初始化为 0 或相同值

**症状：** 隐藏层所有神经元输出完全相同，模型无法学习——等效于只有一个神经元

**根因：** 如果所有权重相同，那么所有隐藏单元收到相同的梯度，更新后仍然相同——这种对称性永远不会被打破

**解法：**

❌ 错误写法 — 全零初始化

```python
for p in model.parameters():
    nn.init.zeros_(p)  # 所有参数为 0，训练完还是 0
```

✅ 正确写法 — 使用 He 初始化（ReLU）或 Xavier 初始化（sigmoid/tanh）

```python
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
        nn.init.zeros_(m.bias)  # 偏置可以全零

model.apply(init_weights)
```

**教训：** 权重必须随机初始化打破对称性。偏置全零没问题，权重全零不行。

> 📖 Paper: Glorot & Bengio, [Xavier Init](http://proceedings.mlr.press/v9/glorot10a.html), 2010
> 📖 Paper: He et al., [He Init](https://arxiv.org/abs/1502.01852), 2015

---

## 坑 4: 忘记 model.eval() 和 torch.no_grad()

**场景：** 评估或推理时未切换模式

**症状：** 测试准确率不稳定（每次不一样）、推理速度慢

**根因：** `model.train()` 模式下 Dropout 仍在随机关闭神经元、BatchNorm 用当前 batch 统计量；未用 `no_grad()` 时 PyTorch 仍在构建计算图消耗显存

**解法：**

❌ 错误写法 — 评估时未切换模式

```python
# 推理时 Dropout 仍在生效，结果每次不同
output = model(test_data)
accuracy = compute_acc(output, labels)
```

✅ 正确写法 — 切换评估模式 + 禁用梯度

```python
model.eval()                  # 关闭 Dropout，BN 用全局统计量
with torch.no_grad():         # 不计算梯度，节省显存
    output = model(test_data)
    accuracy = compute_acc(output, labels)
model.train()                 # 记得切回训练模式
```

**教训：** 评估/推理时必须 `model.eval()` + `torch.no_grad()`，之后切回 `model.train()`

> 📖 Docs: [PyTorch nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

---

## 坑 5: CrossEntropyLoss 重复 softmax

**场景：** 在模型输出层加了 softmax，然后传入 `nn.CrossEntropyLoss()`

**症状：** 训练正常但准确率低于预期，梯度变得很小

**根因：** PyTorch 的 `nn.CrossEntropyLoss()` 内部已经包含了 `LogSoftmax + NLLLoss`。如果输出层又加了 softmax，等于对概率做了两次 softmax——压缩了分布，削弱了梯度信号

**解法：**

❌ 错误写法 — 双重 softmax

```python
class BadModel(nn.Module):
    def forward(self, x):
        x = self.fc(x)
        x = torch.softmax(x, dim=1)  # ❌ 多余的 softmax
        return x

criterion = nn.CrossEntropyLoss()  # 内部再做一次 softmax
```

✅ 正确写法 — 输出 logits（原始分数）

```python
class GoodModel(nn.Module):
    def forward(self, x):
        x = self.fc(x)
        return x  # ✅ 输出 logits，不加 softmax

criterion = nn.CrossEntropyLoss()  # 内部自动处理 softmax

# 如果需要概率，在推理时手动加
probs = torch.softmax(model(x), dim=1)
```

**教训：** 用 `nn.CrossEntropyLoss` 时，模型输出层**不要加 softmax**

> 📖 Docs: [PyTorch CrossEntropyLoss](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)

---

## 坑 6: Dying ReLU 问题

**场景：** 使用 ReLU 激活函数，学习率过大或初始化不当

**症状：** 部分或大量神经元输出永远为 0，模型容量实质性降低

**根因：** 当 ReLU 的输入 $z < 0$ 时，$\text{ReLU}'(z) = 0$，梯度为零。一旦大量输入导致 $z < 0$，该神经元的权重再也不会更新——"死掉了"

**解法：**

❌ 错误写法 — 高学习率 + ReLU

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.ReLU(),
    nn.Linear(256, 128), nn.ReLU(),
    nn.Linear(128, 10)
)
optimizer = optim.SGD(model.parameters(), lr=1.0)  # 学习率过大
```

✅ 正确写法 — 适当学习率 + LeakyReLU 替代

```python
model = nn.Sequential(
    nn.Linear(784, 256), nn.LeakyReLU(0.01),  # 负区间保留小梯度
    nn.Linear(256, 128), nn.LeakyReLU(0.01),
    nn.Linear(128, 10)
)
optimizer = optim.Adam(model.parameters(), lr=1e-3)  # 合理学习率

# 或使用 He 初始化
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity='leaky_relu')
model.apply(init_weights)
```

**教训：** 大比例神经元死亡时，考虑 LeakyReLU/ELU/GELU，或降低学习率、检查初始化

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.6.3.1

---

## 坑 7: 忘记 optimizer.zero_grad() 导致梯度累积

**场景：** 训练循环中未在每次迭代前清零梯度

**症状：** 损失不稳定、震荡、NaN，或者收敛到错误位置

**根因：** PyTorch 默认**累加**梯度。如果不清零，每次 `backward()` 的梯度会叠加到之前的梯度上

**解法：**

❌ 错误写法 — 遗漏 zero_grad

```python
for data, target in loader:
    output = model(data)
    loss = criterion(output, target)
    loss.backward()        # 梯度累加到上一次的梯度上!
    optimizer.step()
```

✅ 正确写法 — 每次迭代前清零

```python
for data, target in loader:
    optimizer.zero_grad()  # ✅ 先清零
    output = model(data)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()
```

**教训：** 训练循环的固定模式：`zero_grad → forward → loss → backward → step`

> 📖 Docs: [PyTorch Optimizer](https://pytorch.org/docs/stable/optim.html)

---

## 坑 8: 过深的 MLP 没有残差连接

**场景：** 堆叠了 10+ 层全连接层的 MLP

**症状：** 训练损失不下降，甚至比浅层模型更差

**根因：** 深层 MLP 面临梯度退化问题和优化困难——更深不一定更好。梯度信号经过多次相乘后可能消失。

**解法：**

❌ 错误写法 — 暴力堆叠

```python
# 10 层全连接，梯度消失
model = nn.Sequential(*[
    nn.Sequential(nn.Linear(256, 256), nn.ReLU())
    for _ in range(10)
])
```

✅ 正确写法 — 加入残差连接

```python
class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.fc2 = nn.Linear(dim, dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        residual = x                  # 保存输入
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return self.relu(x + residual)  # 残差连接

model = nn.Sequential(*[ResidualBlock(256) for _ in range(10)])
```

**教训：** MLP 一般 2-4 层就够用。如果确实需要深，加残差连接

> 📚 Book: Goodfellow et al., [《Deep Learning》](../../../textbooks/goodfellow_deep_learning.pdf), Ch.8.2.5

---

## 调试清单

1. [ ] **输入数据是否标准化？** → `StandardScaler` 或 `Normalize` 到均值 0 方差 1
2. [ ] **输入形状是否正确？** → `[batch, features]` 2D 张量，图像需 flatten
3. [ ] **权重是否正确初始化？** → He (ReLU) 或 Xavier (sigmoid/tanh)，不要全零
4. [ ] **学习率是否合适？** → 先试 1e-3 (Adam) 或 1e-2 (SGD+momentum)
5. [ ] **loss 是否匹配输出层？** → `CrossEntropyLoss` 不要加 softmax，`BCEWithLogitsLoss` 不要加 sigmoid
6. [ ] **eval 模式切换了吗？** → 评估时 `model.eval()` + `torch.no_grad()`
7. [ ] **每次迭代 zero_grad 了吗？** → `optimizer.zero_grad()` 在 forward 之前
8. [ ] **是否有 NaN/Inf？** → 检查数据中是否有异常值，降低学习率
9. [ ] **是否过拟合？** → 检查训练/验证 loss 曲线，加 Dropout/weight decay
10. [ ] **网络深度是否合理？** → MLP 一般 2-4 层，过深加残差
