# 📚 Lab 5 教程：CNN 图像分类的数学推导

> **课程:** CST8508 Machine Vision | **主题:** CNN 的数学基础与推导  
> **核心问题:** Lab 代码给了实现，背后的数学推导是什么？  
> **数学前置：** [卷积运算](../../math/general/convolution.md) | [交叉熵](../../math/probability/cross_entropy.md) | [梯度下降](../../math/optimization/gradient_descent.md) | [链式法则](../../math/calculus/chain_rule_gradients.md)  
> 📋 输出解读 → [lab5_output_guide.md](lab5_output_guide.md)

---

## §0 前置知识与贯穿例子

### 0.1 贯穿例子：猫狗二分类

我们用 Lab 5 的真实场景贯穿整个教程：

```
场景：一张 128×128 的彩色图片，判断是猫（Cat=0）还是狗（Dog=1）

具体数值示例（一张猫的照片）：
  输入：张量形状 (1, 3, 128, 128)  ← batch=1, RGB, 128×128
  
  经过 SimpleCNN 后：
    logits = [2.1, 0.3]    ← 猫的分数=2.1, 狗的分数=0.3
    Softmax → [0.858, 0.142]   ← 85.8% 是猫, 14.2% 是狗
    argmax → 0             ← 预测：猫 ✅

  真实标签 = 0（猫）
  损失 = CrossEntropy = -log(0.858) = 0.153
```

### 0.2 本教程覆盖的推导

| 章节 | 核心推导 | Lab 代码对应 |
|------|---------|------------|
| §1 卷积操作 | 输出尺寸公式推导，权重共享原理 | `nn.Conv2d` |
| §2 池化 | MaxPooling 的平移不变性证明 | `nn.MaxPool2d` |
| §3 ReLU | 梯度消失问题与 ReLU 的解法 | `F.relu` |
| §4 交叉熵损失 | 从最大似然估计推导 CrossEntropy | `nn.CrossEntropyLoss` |
| §5 反向传播 | 梯度怎么从 loss 传回 Conv 层 | `loss.backward()` |
| §6 Adam | 自适应学习率的数学原理 | `optim.Adam` |
| §7 评估指标 | Precision/Recall 的概率解释 | `classification_report` |

---

## §1 卷积操作 (Convolution)

> 📚 Ref: Goodfellow *Deep Learning* §9.1–9.2

### 1.1 什么是卷积？

**Slides 给了：** 卷积层的存在，但没有解释为什么输出尺寸会变。

卷积操作是：用一个**滤波核（kernel）** $W \in \mathbb{R}^{K \times K \times C_{in}}$ 在输入特征图上滑动，对每个位置计算**点积**：

$$
(F \star W)[i, j] = \sum_{m=0}^{K-1} \sum_{n=0}^{K-1} \sum_{c=0}^{C_{in}-1} F[i+m,\; j+n,\; c] \cdot W[m, n, c]
$$

| 符号 | 含义 | 贯穿例子中 |
|------|------|----------|
| $F$ | 输入特征图 | 猫图，形状 (3, 128, 128) |
| $W$ | 滤波核（可学习参数）| 3×3×3 的小矩阵 |
| $K$ | 核大小 | 3 |
| $C_{in}$ | 输入通道数 | 3（RGB）|
| $(F \star W)[i,j]$ | 输出在位置 (i,j) 的值 | 该位置的激活值 |

> 📐 推导（tutorial 补充）：当有 $C_{out}$ 个不同的核时，输出是 $C_{out}$ 个特征图的叠加，每个特征图由其对应的核计算得到。

### 1.2 输出尺寸公式推导

**核心问题：** `Conv2d(3, 32, kernel_size=3, padding=1)` 为什么不改变空间尺寸？

不加 padding 时，核在尺寸为 $W_{in}$ 的输入上能滑 $W_{in} - K + 1$ 步，所以：

$$W_{out}^{(\text{no padding})} = W_{in} - K + 1$$

加了 padding $P$ 后，相当于在输入两侧各填充 $P$ 行/列，输入变成 $W_{in} + 2P$：

$$\boxed{W_{out} = \left\lfloor \frac{W_{in} - K + 2P}{S} \right\rfloor + 1}$$

**Lab 5 验证：**

$$W_{out} = \left\lfloor \frac{128 - 3 + 2 \times 1}{1} \right\rfloor + 1 = 128$$

所以 Conv2d 后空间尺寸不变（仍是 128）— "same" padding 的效果。

> 💡 **Slides 未强调：** 当 $K=3, P=1, S=1$ 时，空间尺寸严格不变。这是 CNN 设计中非常常见的配置，专门用于"卷积不改变空间尺寸"。

### 1.3 权重共享的参数量推导

**全连接层的参数量**（对比基准）：

$$\text{FC Params} = W_{in} \times H_{in} \times C_{in} \times n_{out} + n_{out}$$

对 128×128×3 输入，第一层 1024 个神经元：$128 \times 128 \times 3 \times 1024 = 50,331,648$

**卷积层的参数量（权重共享）：**

$$\text{Conv Params} = K \times K \times C_{in} \times C_{out} + C_{out}$$

对 `Conv2d(3, 32, 3, padding=1)`：$3 \times 3 \times 3 \times 32 + 32 = 896$

> ⚠️ **Slides 未强调：** 卷积层参数量**与输入空间尺寸无关**（$W_{in}, H_{in}$ 不出现在公式中），这是权重共享的核心优势。

---

## §2 MaxPooling 与平移不变性 (Max Pooling)

> 📚 Ref: Goodfellow *Deep Learning* §9.3

### 2.1 池化的输出尺寸

`MaxPool2d(2, 2)` 用 2×2 窗口取局部最大值，步长等于窗口大小：

$$W_{out} = \left\lfloor \frac{W_{in}}{K_{pool}} \right\rfloor$$

**Lab 5 中：** $W_{out} = 128 / 2 = 64$（每次减半）

### 2.2 为什么取最大值能引入平移不变性？

**📐 推导（tutorial 补充）：**

设一个强激活（被检测到的特征）在位置 $(r, c)$，值为 $v$。

如果特征稍微移动到 $(r+1, c)$（平移 1 像素），只要仍在同一个池化窗口内：

$$\max(v, v_1, v_2, v_3) = v \quad \text{（因为 } v \text{ 仍是最大值）}$$

池化输出**不变**。

> 💡 这就是为什么 "Max" Pooling 而非 "Average" Pooling 更适合特征检测：最大值保留最强的特征响应，而均值会被弱激活稀释。

---

## §3 ReLU 与梯度消失问题 (ReLU and Vanishing Gradient)

> 📚 Ref: Goodfellow §6.3.1, LeCun et al. 1998

### 3.1 为什么不用 Sigmoid？

早期神经网络使用 Sigmoid 激活函数：

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

导数：

$$\sigma'(x) = \sigma(x)(1 - \sigma(x)) \in (0, 0.25]$$

**梯度消失（Vanishing Gradient）问题：**

在反向传播中，梯度需要通过每一层的激活函数导数相乘。设网络有 $L$ 层：

$$\frac{\partial \mathcal{L}}{\partial W^{(1)}} = \prod_{l=1}^{L} \sigma'(z^{(l)}) \cdot \frac{\partial \mathcal{L}}{\partial z^{(L)}}$$

每个 $\sigma'$ 最大只有 0.25，经过 $L$ 层后：

$$\prod_{l=1}^{L} \sigma'(z^{(l)}) \leq (0.25)^L \to 0 \quad \text{当 } L \text{ 较大时}$$

**结果：** 浅层梯度几乎为零→无法有效训练。

### 3.2 ReLU 怎么解决的

$$f(x) = \max(0, x)$$

导数：

$$f'(x) = \begin{cases} 1 & x > 0 \\ 0 & x \le 0 \end{cases}$$

**关键：** 正区间导数恒为 1，不会压缩梯度。深层网络只要激活值为正，梯度就能原封不动地传回浅层。

> ⚠️ **Slides 未强调：** ReLU 的缺点是"死亡神经元（Dying ReLU）"——如果某个神经元的输入始终为负，梯度永远为 0，该神经元永久停止学习。Dropout 有助于缓解这一问题。

---

## §4 交叉熵损失的推导 (Cross-Entropy Loss Derivation)

> 📚 Ref: Goodfellow §6.2.1.1, Murphy *PML1* §2.5.3 (Multiclass logistic regression) & §10.3.2

### 4.1 为什么不用 MSE（均方误差）？

若用 MSE 作为分类损失：

$$\mathcal{L}_{MSE} = \frac{1}{N} \sum_{i} (y_i - \hat{p}_i)^2$$

对 Sigmoid 或 Softmax 输出，当预测完全错误（$\hat{p}_i \approx 0$，真实 $y_i = 1$）：

- 激活函数饱和区的梯度接近 0
- $\nabla \mathcal{L}_{MSE}$ 也接近 0 → 错得越离谱，更新越慢

**这与我们的直觉相反：** 预测最错的地方应该得到最大的更新。

### 4.2 从最大似然推导交叉熵

**假设：** 每张图片 $i$ 的真实标签 $y_i$ 来自 Categorical 分布，模型输出概率 $\hat{p}_{i,k}$。

**最大似然估计（MLE）：** 最大化数据在模型下的对数似然：

$$\log \mathcal{L}(\theta) = \sum_{i=1}^{N} \log p(y_i | x_i; \theta) = \sum_{i=1}^{N} \log \hat{p}_{i, y_i}$$

**最小化负对数似然** = 等价于最小化：

$$\mathcal{L}_{CE} = -\frac{1}{N} \sum_{i=1}^{N} \log \hat{p}_{i, y_i}$$

对单样本，若真实标签为第 $c$ 类：

$$\mathcal{L}_{CE} = -\log \hat{p}_c = -\log \frac{e^{z_c}}{\sum_j e^{z_j}}$$

> 📚 推导来源：Murphy *PML1* §10.3.2（Maximum likelihood estimation for multinomial logistic regression）

### 4.3 为什么"预测越错，更新越大"？

当 $\hat{p}_c \to 0$（预测完全错误）：

$$\mathcal{L}_{CE} = -\log(\hat{p}_c) \to +\infty$$

梯度 $\nabla_{z_c} \mathcal{L}_{CE} = \hat{p}_c - 1 \to -1$（非零！大更新）

当 $\hat{p}_c \to 1$（预测完全正确）：

$$\mathcal{L}_{CE} \to 0, \quad \nabla_{z_c} \mathcal{L}_{CE} \to 0$$（小更新）

> 💡 **这就是 CrossEntropy 优于 MSE 的关键：** 梯度的大小与预测误差成正比，满足"错得多→改得多"的直觉。

---

## §5 反向传播：梯度如何回传到卷积层

> 📚 Ref: Goodfellow §6.5.6

**Slides 给了：** 反向传播的概念图。**Slides 未给：** 梯度如何穿过 Conv → Pool → ReLU 层。

### 5.1 链式法则的应用

损失 $\mathcal{L}$ 关于卷积核 $W^{(1)}$ 的梯度（第一层）：

$$\frac{\partial \mathcal{L}}{\partial W^{(1)}} = \frac{\partial \mathcal{L}}{\partial z^{(L)}} \cdot \prod_{l=2}^{L} \frac{\partial z^{(l)}}{\partial z^{(l-1)}} \cdot \frac{\partial z^{(1)}}{\partial W^{(1)}}$$

### 5.2 通过 ReLU 的梯度

设 $z = \text{ReLU}(a) = \max(0, a)$，则：

$$\frac{\partial \mathcal{L}}{\partial a} = \frac{\partial \mathcal{L}}{\partial z} \cdot \frac{\partial z}{\partial a} = \frac{\partial \mathcal{L}}{\partial z} \cdot \mathbb{1}[a > 0]$$

> 📐 直觉：ReLU 就是一个"门"——正向输入时梯度直接通过（乘以 1），负向输入时梯度阻断（乘以 0）。

### 5.3 通过 MaxPooling 的梯度

MaxPooling 只将梯度传回**产生最大值的位置**，其他位置梯度为 0：

$$\frac{\partial \mathcal{L}}{\partial a_{i,j}} = \begin{cases} \frac{\partial \mathcal{L}}{\partial z_{pool}} & \text{若 } a_{i,j} \text{ 是池化窗口内的最大值} \\ 0 & \text{其他} \end{cases}$$

### 5.4 对卷积核的梯度

损失对核参数 $W[m,n,c]$ 的梯度是**对输出特征图所有位置求和**：

$$\frac{\partial \mathcal{L}}{\partial W[m,n,c]} = \sum_{i,j} \frac{\partial \mathcal{L}}{\partial F_{out}[i,j]} \cdot F_{in}[i+m,\; j+n,\; c]$$

> 📐 推导（tutorial 补充）：这是卷积的反向就是**梯度与输入的相关操作（cross-correlation）**，与前向传播的卷积形式相同，只是 kernel 翻转方向不同。

---

## §6 Adam 优化器的数学原理

> 📚 Ref: Kingma & Ba (2014) *Adam: A Method for Stochastic Optimization*

**背景：** SGD（随机梯度下降）对所有参数用同一学习率，Adam 为每个参数维护**独立的自适应学习率**。

Adam 维护两个移动平均：

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \quad \text{（梯度的一阶矩 / 动量）}$$

$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \quad \text{（梯度平方的二阶矩 / 方差估计）}$$

| 符号 | 含义 | 默认值 |
|------|------|--------|
| $g_t$ | 第 $t$ 步的梯度 | — |
| $\beta_1$ | 一阶矩衰减系数 | 0.9 |
| $\beta_2$ | 二阶矩衰减系数 | 0.999 |
| $m_t$ | 梯度的指数移动平均（方向）| — |
| $v_t$ | 梯度平方的指数移动平均（幅度）| — |

偏差修正（初始阶段 $m_t, v_t$ 偏小）：

$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$

参数更新：

$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

> 💡 **直觉：** $\sqrt{\hat{v}_t}$ 是梯度幅度的估计——如果某参数梯度一直很大，$\sqrt{\hat{v}_t}$ 大，学习率自动变小（避免超调）；如果梯度一直很小，学习率自动变大（加速学习）。

**Lab 5 中的 Adam：** `optim.Adam(model.parameters(), lr=1e-3)` —— 10 个 epoch 内从 62% 训练准确率稳定爬升到 88%，收敛过程平滑无震荡，这是 Adam 自适应性的体现。

---

## §7 分类评估指标的概率解释

> 📚 Ref: Manning et al. *Introduction to IR* §8.3

**Slides 给了：** precision, recall, f1 的公式。**Slides 未给：** 为什么这三个指标各自在什么情况下更重要？

### 7.1 混淆矩阵（以猫为正类）

|  | 预测猫（P）| 预测狗（N）|
|--|-----------|-----------|
| **真实猫（P）** | TP（正确识猫）| FN（漏识猫）|
| **真实狗（N）** | FP（错认狗为猫）| TN（正确识狗）|

### 7.2 各指标的应用场景

| 指标 | 公式 | 何时重要 | Lab 5 中的值 |
|------|------|---------|------------|
| Precision $= \frac{TP}{TP+FP}$ | 降低 FP | 误报代价高（如垃圾邮件过滤）| Cat: 0.90 |
| Recall $= \frac{TP}{TP+FN}$ | 降低 FN | 漏报代价高（如疾病检测）| Cat: 0.86 |
| F1 $= \frac{2PR}{P+R}$ | 综合平衡 | 类别不平衡时 | Cat: 0.88 |

### 7.3 Lab 5 的解读

**Cat: precision=0.90 > recall=0.86**
→ 模型预测"猫"时较自信（误报少），但有 14% 的真实猫被漏掉了。

**Dog: precision=0.87 < recall=0.91**
→ 模型捕捉到了 91% 的真实狗，但有 13% 预测为"狗"的其实是猫（误报多一些）。

> 📐 推导（tutorial 补充）：Precision 和 Recall 是互相 trade-off 的关系（Precision-Recall curve）。提高判断阈值 → Precision ↑，Recall ↓；降低阈值 → Precision ↓，Recall ↑。两者的调和平均 F1 提供了一个单一的综合指标。

---

## 参考索引表（Reference Index）

| 教程章节 | 教科书来源 | 核心内容 | Slides 覆盖？ |
|---------|-----------|---------|-------------|
| §1 卷积输出尺寸推导 | Goodfellow §9.1 | $(W_{in}-K+2P)/S+1$ 公式推导 | ❌ Slides 给了公式，未推导 |
| §1.3 权重共享参数量 | Goodfellow §9.2 | 参数量与空间尺寸无关的证明 | ❌ |
| §2 MaxPool 平移不变性 | Goodfellow §9.3 | 直觉证明：最大值在窗口内移动不变 | ⚠️ 提到概念，未证明 |
| §3 ReLU vs Sigmoid 梯度消失 | Goodfellow §6.3.1 | $(0.25)^L$ 消失证明 | ❌ |
| §4 CrossEntropy 从 MLE 推导 | Murphy PML1 §2.5.3, §10.3.2 | $-\log \hat{p}_c$ 的 MLE 来源 | ❌ Slides 给了公式，未推导 |
| §5 梯度回传经过 MaxPool | Goodfellow §9 | 只有 argmax 位置获得梯度 | ❌ |
| §6 Adam 自适应学习率 | Kingma & Ba 2014 | $m_t, v_t$ 偏差修正推导 | ❌ Lab 直接用，未解释为何选 Adam |
| §7 Precision/Recall trade-off | Manning §8.3 | PR curve，阈值调节的效果 | ⚠️ 给了定义，未展示权衡 |
